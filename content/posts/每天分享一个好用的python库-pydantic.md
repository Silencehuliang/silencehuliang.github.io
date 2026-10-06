---
title: "每天分享一个好用的Python库-pydantic"
date: 2021-07-20T10:00:00+08:00
lastmod: 2021-07-20T10:00:00+08:00
draft: false
categories: ["python"]
tags: ["python库"]
description: "pydantic:用类型注解做数据校验和配置管理,FastAPI 背后的数据校验引擎"
---

## 前言

Python中有许多好用、有意思的库，有一些可以大大提高开发效率，有的可以为我们解决很多棘手的问题，从今天开始我会每天给大家分享一个Python库。今天分享的是一个数据校验库—pydantic

## pydantic

### 简介

pydantic 利用 Python 的类型注解（type hints）来做数据解析和校验，数据不对就抛出清晰的错误，特别适合做接口入参校验、配置文件解析。著名的 FastAPI 框架的数据校验就是基于 pydantic 的。

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install pydantic
  ```

### 简单使用

- 定义模型并校验数据

  ```python
  from datetime import date
  from pydantic import BaseModel

  class Article(BaseModel):
      title: str
      views: int = 0
      published: date

  article = Article(title='一篇文章学会Git', views=100, published='2019-05-11')
  print(article.published)  # 2019-05-11，字符串被自动转成了 date 对象
  ```

- 类型不对会报友好的错误

  ```python
  >>> Article(title='测试', views='很多', published='2019-05-11')
  ValidationError: 1 validation error for Article
  views -> value is not a valid integer (type=type_error.integer)
  ```

### 小结

做 Web 后台或者写 SDK 的时候，用 pydantic 把"数据长什么样"声明出来，剩下的校验、转换它全包了，代码会干净很多。
