---
title: "一篇文章学会Git"
date: 2020-01-15
description: "一篇文章学会Git"
lastmod: 2020-01-15
draft: false
categories: ["工具"] 
tags: ["一篇文章学会系列"]
---

## 简介

### 什么是Git

Git是一个免费的开源分布式版本控制系统，也是目前为止世界上最先进的分布式版本控制系统。Git官方有一个视频介绍，可以[点此观看](https://git-scm.com/video/what-is-git)

### 什么是版本控制系统？

一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。简单点理解就是一个可以帮助我们记录文件修改的系统。Git官方有一个视频介绍，可以[点此观看](https://git-scm.com/video/what-is-version-control)

### 什么是分布式版本控制系统？

分布式版本控制系统时相对于集中式版本控制系统的。

集中式版本控制系统将版本库存放在中央服务器中集中管理，当你需要时从中央服务器中拉取最新的版本，修改完后将修改提交给中央服务器。这就会带来例如当中央服务器宕机时整个版本控制系统就会崩溃；推送或者拉取一个较大的文件时就会消耗很多时间等弊端。

分布式版本控制系统中，每个人电脑都是一个仓库，自己的文件可以在本地管理，当需要多人协同时只需要管理好本地仓库与协同仓库的版本即可

## 安装

### Mac

在mac上有多种方法可以安装Git，最简单的事通过Xcode命令行工具安装。

#### 通过Xcode安装

1.下载并安装Xcode

2.在终端中运行git即可，如果尚未安装，它将提示您安装。

#### 通过homebrew安装

1.安装homebrew

```bash
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

```

2.安装git

```bash
$ brew install git
```

#### 通过安装包安装

1.点击此[下载最新版本](https://git-scm.com/download/mac)

2.下载完成后打开安装包，一直下一步安装即可





### Linux 

在Linux发行版上安装GIt，可以通过附带的软件包管理工具来安装

#### Debian/Ubuntu

```bash
$ apt-get install git
```

其他发行版本见这个[链接](https://git-scm.com/download/linux)

### Windows

#### 下载安装包

根据操作系统位数选择，[链接](https://git-scm.com/download/win)

#### 安装

默认选项安装即可

### 配置Git

#### 配置文件介绍

Git有一个`git config`的工具，可以设置和获取配置，用来控制Git外观及操作。这些变量可以存放在三个不同的位置，根据存放位置不同作用的范围也不同。

1.`/etc/gitconfig`：包含系统上每个用户及其存储库的配置。

2.`~/.gitconfig`或`~/.config/git/config`：每个用户专属的配置

3.`config.git/config`：当前使用存储库的git目录，用于该存储库的配置

如果有相同配置项时，每个级别都会覆盖上一个级别中的值，即：3>2>1

可以使用一下命令查看所有设置以及设置的所属：

```bash
$ git config --list --show-origin
```

#### 常见配置

下面介绍一些常见配置

##### 身份配置

安装完Git做的第一件事应该是设置用户名和电子邮箱。

```bash
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```

**使用global后，该信息将会始终作用域Git操作上**

##### 配置Git编辑器

Git默认的编辑器是系统默认编辑器

如果要是用其他文本编辑器（例如vim），则可以执行以下操作：

```bash
$ git config --global core.editor vim
```



 