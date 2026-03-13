"""
百度搜索工具 - BaiduSearchTool
使用 requests 进行百度搜索并解析结果
"""

import re
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool


class BaiduSearchTool(BaseTool):
    """百度搜索工具"""

    name: str = "BaiduSearchTool"
    description: str = "通过百度搜索引擎搜索网络信息，返回相关网页摘要和链接。输入：搜索关键词（字符串）。"

    def __init__(self, num_results: int = 5):
        super().__init__(name=self.name, description=self.description)
        self.num_results = num_results
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _run(self, query: str) -> str:
        """执行搜索并返回结果"""
        try:
            search_results = self._search(query)
            return self._format_results(search_results)
        except Exception as e:
            return f"搜索出错: {str(e)}"

    def _search(self, query: str) -> List[Dict[str, str]]:
        """执行百度搜索"""
        results = []
        encoded_query = quote(query)
        url = f"https://www.baidu.com/s?wd={encoded_query}&rn={self.num_results}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            result_divs = soup.find_all("div", class_="result")

            for idx, div in enumerate(result_divs[:self.num_results]):
                try:
                    title_elem = div.find("h3")
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    link_elem = title_elem.find("a")
                    link = link_elem.get("href", "") if link_elem else ""

                    # 获取摘要
                    abstract_elem = div.find("div", class_="c-abstract")
                    abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""

                    # 尝试获取真实链接（百度链接会重定向）
                    real_link = self._resolve_baidu_link(link) if link else ""

                    results.append({
                        "title": title,
                        "link": real_link or link,
                        "abstract": abstract,
                        "index": idx + 1
                    })
                except Exception:
                    continue

            time.sleep(0.5)  # 避免请求过快

        except requests.RequestException as e:
            print(f"请求错误: {e}")

        return results

    def _resolve_baidu_link(self, baidu_link: str) -> Optional[str]:
        """解析百度跳转链接获取真实 URL"""
        try:
            if not baidu_link.startswith("http"):
                return None
            # 发送 HEAD 请求获取重定向目标
            resp = requests.head(baidu_link, headers=self.headers, allow_redirects=True, timeout=5)
            return resp.url
        except Exception:
            return None

    def _format_results(self, results: List[Dict[str, str]]) -> str:
        """格式化搜索结果"""
        if not results:
            return "未找到相关搜索结果。"

        formatted = f"百度搜索结果（共 {len(results)} 条）：\n"
        formatted += "=" * 60 + "\n\n"

        for res in results:
            formatted += f"[{res['index']}] {res['title']}\n"
            formatted += f"    链接: {res['link']}\n"
            if res['abstract']:
                formatted += f"    摘要: {res['abstract']}\n"
            formatted += "\n"

        formatted += "=" * 60 + "\n"
        formatted += "提示：请使用 ScrapeWebsiteTool 工具抓取重要链接的详细内容。"

        return formatted


# 全局实例
baidu_search_tool = BaiduSearchTool(num_results=5)
