# Python学习之路-Tornado基础:HelloTornado


## 前言

### 回想Django的部署方式

以Django为代表的python web应用部署时采用wsgi协议与服务器对接（被服务器托管），而这类服务器通常都是基于**多线程**的，也就是说**每一个网络请求服务器都会有一个对应的线程来用web应用（如Django）进行处理**。

### 考虑两类应用场景

- 用户量大，高并发

如秒杀抢购、双十一某宝购物、春节抢火车票

- 大量的HTTP持久连接

使用同一个TCP连接来发送和接收多个HTTP请求/应答，而不是为每一个新的请求/应答打开新的连接的方法。

对于HTTP 1.0，可以在请求的包头（Header）中添加**Connection: Keep-Alive**。

对于HTTP 1.1，所有的连接默认都是持久连接。

对于这两种场景，通常基于多线程的服务器很难应对。

### C10K问题

对于前文提出的这种高并发问题，我们通常用C10K这一概念来描述。C10K—— **C**oncurrently handling **ten thousand** connections，即并发10000个连接。对于单台服务器而言，根本无法承担，而采用多台服务器分布式又意味着高昂的成本。如何解决C10K问题？

### Tornado

Tornado在设计之初就考虑到了性能因素，旨在解决C10K问题，这样的设计使得其成为一个拥有非常高性能的**解决方案**（服务器与框架的集合体）。

## Tornado是为何物

### 简介

Tornado全称Tornado Web Server，是一个用Python语言写成的Web服务器兼Web应用框架，由FriendFeed公司在自己的网站FriendFeed中使用，被Facebook收购以后框架在2009年9月以开源软件形式开放给大众。

### 特点

- 作为Web框架，是一个轻量级的Web框架，类似于另一个Python web框架Web.py，其拥有异步非阻塞IO的处理方式。
- 作为Web服务器，Tornado有较为出色的抗负载能力，官方用nginx反向代理的方式部署Tornado和其它Python web应用框架进行对比，结果最大浏览量超过第二名近40%。

### 性能

 Tornado有着优异的性能。它试图解决C10k问题，即处理大于或等于一万的并发。Tornado框架和服务器一起组成一个WSGI的全栈替代品。单独在WSGI容器中使用tornado网络框架或者tornaod http服务器，有一定的局限性，为了最大化的利用tornado的性能，推荐同时使用tornaod的网络框架和HTTP服务器

## 与Django对比

### Django

Django是走**大而全**的方向，注重的是**高效开发**，它最出名的是其全自动化的管理后台：只需要使用起ORM，做简单的对象定义，它就能自动生成数据库结构、以及全功能的管理后台。

Django提供的方便，也意味着Django内置的ORM跟框架内的其他模块耦合程度高，应用程序必须使用Django内置的ORM，否则就不能享受到框架内提供的种种基于其ORM的便利。

- session功能
- 后台管理
- ORM

### Tornado

Tornado走的是**少而精**的方向，注重的是**性能优越**，它最出名的是异步非阻塞的设计方式。

- HTTP服务器
- 异步编程
- WebSockets
