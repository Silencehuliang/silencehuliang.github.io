---
title: "Python搭建虚拟环境"
description: "Python搭建虚拟环境"
date: 2019-01-13
draft: false
categories: ["Python"] 
tags: ["虚拟环境"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 为什么要搭建虚拟环境。

平时开发的过程中会遇到不同的项目，往往不同的项目之间需要的第三方包会有所差异，如果我们都在系统的python环境中会导致遇到很多问题，通过虚拟环境搭建一套独立的python运行环境，可以让项目之间互不干扰。

## 如何搭建

一般我们搭建虚拟环境都会用上virtualenv，它是一个可以创建并管理python虚拟环境的第三方包。

### 安装

- 不论是windows还是linux还是mac都可以直接通过pip 安装，需要注意的是系统中存在两个python的时候，注意pip的版本，选择对应的版本安装

  ```python
  pip install virtualenv
  ```

### 创建虚拟环境

我们通常会创建一个文件夹为env(当然你也可以去任何你喜欢的名字)，专门用来存放不同的虚拟环境

进入到env文件夹中通过命令创建一个虚拟环境，名为first_env

```python
virtualenv first_env
```

相关参数说明

- -p:选择要使用的Python解释器，默认为安装virtualenv的解释器
- --prompt=xx:将xx设置为虚拟环境的提示前缀

### 使用虚拟环境

- Windows

  - 进入虚拟环境的Scripts目录
  - 在此处打开命令行工具
  - 输入activate，当命令提示符多了一个虚拟环境名字的前缀时即激活成功![](F:\我的坚果云\图片\虚拟环境激活.png)

- Linux or Mac

  - 通过source激活使用，当命令提示符多了一个虚拟环境名字的前缀时即激活成功

    ```python
    source first_env/bin/activate
    ```

  

  


### 退出虚拟环境

在当前虚拟环境中输入deactivate，当命令提示符虚拟环境名字的前缀消失时即退出

### 删除虚拟环境

在我们不需要这个虚拟环境的时候只需要将该虚拟环境的整个包删除即可