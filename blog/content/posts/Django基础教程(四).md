---
title: "Django基础教程之请求与相应"
description: "Django配置文件详解"
date: 2019-02-26
lastmod: 2019-02-26
draft: false
categories: ["Django基础教程"] 
tags: ["Django2.x","教程"]

---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

本教程为Django基础教程系列第四篇，前面篇章在以下链接：

[Django基础教程之Django介绍](http://49.235.231.121/2019/django基础教程一/)

[Django基础教程之工程搭建](http://49.235.231.121/2019/django基础教程二/)

[Django基础教程之配置文件详解](http://49.235.231.121/2019/django基础教程三/)

## 前言

在[Django基础教程之工程搭建](http://49.235.231.121/2019/django基础教程二/)中，[视图相关部分]([http://49.235.231.121/2019/django%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B%E4%BA%8C/#%E5%BA%94%E7%94%A8](http://49.235.231.121/2019/django基础教程二/#应用))提到过Django中视图的功能是接受请求，进行业务处理，返回响应。今天就来研究一下Django中的请求与相应部分。

## 请求

利用HTTP协议向服务器传参有几种途径？

- 提取URL的特定部分，可以通过服务器端路由中用正则表达式截取；
- 查询字符串（query string)；
- 请求体（body）中发送的数据，比如表单数据、json、xml；
- 在http报文的头（header）中。



### URL路径参数

在定义路由URL时，可以使用正则表达式提取参数的方法从URL中获取请求参数，Django会将提取的参数直接传递到视图的传入参数中。

- 未命名参数按定义顺序传递， 如

  ```python
  url(r'^weather/([a-z]+)/(\d{4})/$', views.weather),
  
  def weather(request, city, year):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```

- 命名参数按名字传递，如

  ```python
  url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),
  
  def weather(request, year, city):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```

### QueryDict对象

