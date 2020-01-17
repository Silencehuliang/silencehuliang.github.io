---
title: "Django基础教程之Django介绍"
description: "Django介绍"
date: 2019-02-14
draft: false
categories: ["Django"] 
tags: ["Django教程"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

本教程为Django基础教程系列第一篇



## 前言

为什么网上有很多Django的学习资料，我还想自己写一个Django的教程呢，一是想通过写教程发现自己的不足，二是想通过自己的总结让那些想学习Django的小伙伴们少走一些弯路，当然我写的内容有可能也是错的，欢迎大家纠正，我们可以共同探讨，共同进步。



## 简介

Django是一个高级Python Web框架，可以快速开发和简洁实用的设计。Django负责处理网站开发中遇到的问题，编程人员只需要专注于应用编写，无需重新造轮子。它是免费和开源的。



## 特点

### 完备性

Django原生提供了众多的功能组件，对于开发人员来说Django几乎做到了开箱即用。

### 安全

Django认真对待安全性，并帮助开发人员避免许多常见的安全性错误，例如SQL注入，跨站点脚本编写，跨站点请求伪造和点击劫持。其用户身份验证系统提供了一种安全的方式来管理用户帐户和密码。

### 可扩展性

Django强调代码复用，多个组件可以以"插件"的形式服务于整个框架，Django还有许多功能强大的第三方插件，你也可以开发自己的工具包。



## MVT模式

Django采用MVT程序设计模式

- M全拼为Model，主要封装对数据库层的访问，对数据库中的数据进行增、删、改、查操作。
- V全拼为View，用于接收请求，进行业务处理，返回应答。
- T全拼为Template，用于封装结果，负责封装构造要返回的html。



## Django学习资料

- [Django官网](https://www.djangoproject.com/)
- [Django项目Github](https://github.com/django/django)
- [Django Book 教程](http://djangobook.com/)
- [Mozilla Django教程](https://developer.mozilla.org/zh-CN/docs/learn/Server-side/Django)

