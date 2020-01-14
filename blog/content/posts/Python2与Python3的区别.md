---
title: "Python2与Python3的区别"
description: "Python2与Python3的区别"
date: 2019-01-09
draft: false
categories: ["Python"] 
tags: ["Python3"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 简介

目前用Python开发的项目有两个Python版本，分别是Python2.x与Python3.x，由于Python3相对于python2有着较大的升级，所以Python3将会是现在与未来的主流版本。



### Python3时间轴

- Python3.0发布于2008.12.3
- Python3.1发布于2009.6.27
- Python3.2发布于2011.2.20
- Python 3.3 发布于 2012.9.29
- Python 3.4 发布于 2014.3.16
- Python 3.5 发布于 2015.9.13
- Python 3.6 发布于 2016.12.23

为了不带入过多的累赘，在Python3.0设计的时候没有考虑向下兼容，所以早期的项目都无法在Python3.0上正常运行。为了早期的项目可以逐步迁移到Python3.0，Python官方提供了Python2.6过度版本（基于Python2的语法与库，允许使用部分Python3的语法和函数），2010年中推出Python2.7为最后一个Python2.x版本。了解Python3版本的变化对我们日常开发与项目维护都十分重要



## Python3.0后的变化

### 解释器名称

Python2.x的解释器为python，Python3.x的解释器为python3

其他语言实现的解释器：

| PyPy       | Python实现的Python解释器，支持 JIT 即时编译 |
| ---------- | ------------------------------------------- |
| cpython    | C语言基于官方版本实现的Python解释器         |
| Jython     | 运行在Java上的Python解释器                  |
| IronPython | 运行在.NET与Mono平台的Python解释器          |



### 字符串

Python2中字符串是基于ASCII编码的str字符串，当调用字符串变量时会打印其bytes值（16进制表示的字符串内存地址）。 而unicode是一个单独的类型。

Python3中字符串原生支持unicode，byte也变成了一个单独的字节类，并且Python3源码文件默认使用utf-8编码所以中文也可以做变量名。



### import

Python2中import导包采用相对路径，导致标准库导入变困难。

Python3中import导包采用绝对路径



### print

Python2中的print是一种特殊的语句，在Python3中print变成了print函数



### range函数与xrange函数

xrange函数在Python3中被废弃，range函数的机制进行修改实现了xrange函数返回可迭代对象的效果



### 老式类与新式类

Python2中存在老式类与新式类，在Python3中统一采用新式类（新式类申明要求继承object），且必须使用新式类应用多重继承



### 除法与取余

- Python2 中若两个整形进行运算，结果为整形，但若其中有一个浮点数类型，则结果为浮点数。python3为真除法，运算结果为float类型。

- Python2 中取余返回小于除法运算结果的最大整数，从类型上讲，与"/"运算符返回类型逻辑一致。Python3中与python2作用相同。



### raw_input函数与input函数

raw_input函数在Python3中被废弃，统一使用input函数



### 缩进

Python3采用更严格的缩进方式，tab和space不能共存



### long

long整型被Python3废弃，统一使用int，int具有long的特性



### file

file函数被废弃，统一使用open函数



### 不等运算符

Python3废除<>，只有!=



### 方法返回值

Python3 中这些方法再不再返回 list 对象：dictionary 关联的 keys()、values()、items()，zip()，map()，filter()，但是可以通过 list 强行转换



### next()函数

迭代器 iterator 的 next()函数被 Python3 废弃，统一使用 next(iterator)



### exec

exec 语句被 python3 废弃，统一使用 exec 函数



### has_key 函数

has_key 函数被 Python 废弃，统一使用 in 关键词



### round函数

Python2中，round函数返回float类型值。Python3中，round函数返回int类型值。



### 比较操作符

Python2中任意两个对象都可以比较。Python3中只有同一类型数据的对象才可以进行比较。

