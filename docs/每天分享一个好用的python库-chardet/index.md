# 每天分享一个Python库-Chardet


## 前言
Python中有许多好用、有意思的库，有一些可以大大提高开发效率，有的可以为我们解决很多棘手的问题，从今天开始我会每天给大家分享一个Python库。今天分享的是一个跟字符串编码有关的库---chardet

## Chardet

### 简介

chardet是一个识别字符串编码的第三方库，支持繁简中文、日语、韩文等多种语言

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install chardet
  ```

- 通过安装Anaconda进行安装，由于Anaconda中已经帮我们安装了chardet，可以直接使用

### 简单使用

- 识别字符串格式

  ```python
  >>> import chardet
  >>> chardet.detect(b'Hello chardet!')
  {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
  ```

  返回的结果中，`encoding`对应的键为编码类型，`confidence`对应的键为识别可信度为1，即为100%，`language`对应的键为语言，这里没有检测出来

- 识别中文格式

  ```python
  >>> chardet.detect('你好'.encode('utf-8'))
  >>> {'encoding': 'utf-8', 'confidence': 0.7525, 'language': ''}
  ```

  这次可以看到检测出了编码类型为utf-8，可信度为75.25%，从这里可以看出检测中文的准确率没有那么高

- 对外语进行检测

  ```python
  >>> chardet.detect('こんにちは'.encode('euc-jp'))
  >>> {'encoding': 'EUC-JP', 'confidence': 0.99, 'language': 'Japanese'}
  ```

  对日语的检测可信度为99%且成功检测出来了语言

### 作用

前面介绍了一下`chardet`库，与其简单的使用方法，那我们什么场景可以使用它呢，我举一个例子：当我们从网页爬取一段内容后，不清楚编码类型，就可以使用`chardet`库来进行检测，然后将不同的类型转化为`utf-8`来进行后续操作。还有其他使用场景欢迎大家补充！

## 尾巴

从上可以看出，`chardet`库非常的简单易用，核心目的也比较明确：检测字符串编码类型。以后在字符串编码不清楚的时候可以使用`chardet`库，而不是自己去试，可以大大提高开发效率。

[官方文档地址](https://pypi.org/project/chardet/1.0/)


