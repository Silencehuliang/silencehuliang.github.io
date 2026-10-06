---
title: "每天分享一个好用的Python库-Rich"
date: 2021-07-18T10:00:00+08:00
lastmod: 2021-07-18T10:00:00+08:00
draft: false
categories: ["python"]
tags: ["python库"]
description: "Rich:让命令行输出拥有颜色、表格、进度条与排版的能力的 Python 库"
---

## 前言

Python中有许多好用、有意思的库，有一些可以大大提高开发效率，有的可以为我们解决很多棘手的问题，从今天开始我会每天给大家分享一个Python库。今天分享的是一个能让命令行输出变得漂亮的库—rich

## Rich

### 简介

rich 是一个终端富文本渲染库，可以给命令行输出加上颜色、表格、进度条、语法高亮、Markdown 渲染等能力，写脚本和 CLI 工具的时候非常好用。

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install rich
  ```

### 简单使用

- 一行代码体验一下

  ```python
  >>> from rich import print
  >>> print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
  ```

- 打印一个漂亮的表格

  ```python
  from rich.table import Table
  from rich.console import Console

  console = Console()
  table = Table(title="我的博客文章")
  table.add_column("标题", style="cyan")
  table.add_column("分类", style="magenta")
  table.add_row("一篇文章学会Git", "一篇文章学会系列")
  table.add_row("Python学习之路-MongoDB基础", "MongoDB")
  console.print(table)
  ```

- 进度条

  ```python
  from rich.progress import track

  for step in track(range(100), description="处理中..."):
      do_something(step)
  ```

### 小结

写运维脚本、数据处理脚本时，rich 能让输出结果一目了然，强烈推荐。官方文档也写得非常漂亮：<https://rich.readthedocs.io/>
