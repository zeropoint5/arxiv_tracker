# [ArXiv Tracker](https://zeropoint5.github.io/arxiv_tracker/)

## 项目概述

ArXiv Tracker 是一个自动化工具，用于跟踪和总结 arXiv 上特定领域的最新研究论文。该项目使用大型语言模型（LLM）来翻译和总结论文摘要，并通过 MkDocs 生成易于浏览的网页文档。

## 主要功能

1. 自动跟踪 arXiv 上特定领域的最新论文
2. 使用 LLM 翻译和总结论文摘要
3. 生成按月份组织的论文列表（Markdown 格式）
4. 使用 MkDocs 发布整理好的论文信息
5. 可自定义配置（通过 `arxiv_conf.yml` 文件）

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/arxiv-tracker.git
cd arxiv-tracker
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 配置

在项目根目录下创建 `arxiv_conf.yml` 文件，配置示例如下：

```yaml
DB_PATH: db/arxiv_articles.db

DOMAINS:
  Retrieval Augmented Generation:
    - "abs:retrieval AND abs:augmented AND abs:generation"

  Emission Trading System:
    - "abs:Emission AND abs:Trading AND abs:System"
```

## 使用方法

1. 运行任务：

```bash
python main.py
```

2. 预览生成的文档：

```bash
./preview.sh
```

3. 部署到 GitHub Pages：

```bash
./deploy.sh
```

## 项目结构

```
arxiv-tracker/
│
├── main.py
├── src/
│   └── arxiv_tracker.py
├── docs/
│   └── (自动生成的 Markdown 文件)
├── db/
│   └── (自动生成的数据库文件)
├── mkdocs.yml
├── requirements.txt
├── arxiv_conf.yml
├── preview.sh
├── deploy.sh
└── README.md
```

## 自动生成的文档

- 文档按领域和月份组织
- 每个月的论文集合存储在一个单独的 Markdown 文件中
- 文档包含论文标题、链接、更新时间、作者列表和中文摘要

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可证

本项目采用 MIT 许可证。
