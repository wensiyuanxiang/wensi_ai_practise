"""
项目统一日志配置
所有实验脚本在入口处调用 setup_logging()，保证格式与级别一致；业务输出使用 logger，禁止裸 print。
"""

import logging
import os
import sys
from typing import Optional, TextIO

# 默认格式：时间、级别、logger 名、消息
_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DEFAULT_DATE_FORMAT = "%H:%M:%S"


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None,
    stream: Optional[TextIO] = None,
) -> None:
    """
    配置根 logger，供脚本入口调用一次即可。
    未指定 level 时从环境变量 LOG_LEVEL 读取，否则为 INFO。
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    if format_string is None:
        format_string = _DEFAULT_FORMAT
    if date_format is None:
        date_format = _DEFAULT_DATE_FORMAT
    out: TextIO = stream if stream is not None else sys.stdout

    numeric = getattr(logging, level, logging.INFO)
    if not isinstance(numeric, int):
        numeric = logging.INFO

    logging.basicConfig(
        level=numeric,
        format=format_string,
        datefmt=date_format,
        stream=out,
        force=True,
    )
