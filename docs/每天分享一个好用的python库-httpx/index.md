# 每天分享一个好用的Python库-httpx


## 前言

Python中有许多好用、有意思的库，有一些可以大大提高开发效率，有的可以为我们解决很多棘手的问题，从今天开始我会每天给大家分享一个Python库。今天分享的是一个新一代 HTTP 客户端—httpx

## httpx

### 简介

httpx 是一个功能齐全的 HTTP 客户端，可以理解为 requests 的升级版：API 几乎完全兼容，同时支持 HTTP/2 和异步请求，还自带连接池、超时重试等能力。写过爬虫的同学可以无痛迁移。

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install httpx
  ```

### 简单使用

- 用法和 requests 一模一样

  ```python
  >>> import httpx
  >>> r = httpx.get('https://httpbin.org/get')
  >>> r.status_code
  200
  >>> r.json()['url']
  'https://httpbin.org/get'
  ```

- 异步用法（配合协程批量抓取很舒服）

  ```python
  import asyncio
  import httpx

  async def main():
      async with httpx.AsyncClient() as client:
          r = await client.get('https://httpbin.org/get')
          print(r.status_code)

  asyncio.run(main())
  ```

### 小结

之前分享过的爬虫系列里我们一直用 requests，如果你的项目需要上异步，httpx 几乎是零成本迁移的最佳选择。

