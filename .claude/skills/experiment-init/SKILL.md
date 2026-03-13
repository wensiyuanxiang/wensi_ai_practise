---
name: experiment-init
description: 初始化 AI 实验主题目录结构。当用户说"开始新实验"、"新建主题"、"创建实验目录"或类似表达时，使用此技能创建标准的实验目录结构和初始文档。
---

# Experiment Initializer

## 概述

自动初始化 wensi_ai_practise 项目的实验主题目录结构。

## 使用场景

当用户说以下内容时触发：
- "开始新实验"
- "新建主题"
- "创建实验目录"
- "初始化实验"
- "新建一个实验主题叫 xxx"
- 或其他表示要开始新实验主题的表达

## 工作流程

1. **确认主题信息**
   - 询问或推断主题名称（英文，kebab-case）
   - 确认主题序号（如 01, 02... 查看现有 experiments/ 目录确定下一个序号）
   - 确认主题中文描述

2. **创建目录结构**
   ```
   experiments/{序号}-{主题名}/
   ├── README.md
   ├── notebooks/
   ├── scripts/
   └── outputs/.gitkeep
   ```

3. **初始化 README.md**
   - 使用 assets/README.template.md 作为模板
   - 填充主题名称、序号、描述

4. **更新主 README.md**
   - 在路线图部分添加新主题（标记为 [ ] 待完成）

## 目录序号规则

查看 `experiments/` 目录下已有的文件夹，按序号递增：
- 已有 `01-llm-basics/` → 下一个是 `02-`
- 已有 `01-xxx/`, `02-yyy/` → 下一个是 `03-`

## 资源

- 模板文件: [assets/README.template.md](assets/README.template.md)
