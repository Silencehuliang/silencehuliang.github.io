---
title: "一篇文章学会Vim"
date: 2020-01-08
lastmod: 2020-01-14
draft: false
categories: ["工具"] 
tags: ["一篇文章学会系列"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 简介

**Vim**是一个高度可定制的终端文本编辑器，它可以很方便的创建和修改任何类型的文本。作为**vi**的升级版，有许多新的特性(以下列出的特性为比较常用的，详细特性可以查看[help vi_diff](http://vimdoc.sourceforge.net/cgi-bin/vim2html2.pl?page=vi_diff.txt#vi_diff.txt).)：

- 无限撤销：可以无限制的撤销
- 可移植性：Vi仅在Unix上可用，Vim还可以在Windows、Macintosh，Amiga，OS / 2，VMS，QNX和其他系统上运行。
- 语法高亮：当用Vim进行编程的时候，他可以根据正在编辑的文件类型，使其以内容以不同的颜色或样式突出显示。Vim捆绑了数百种语法突出显示规则集。
- 图形用户界面：Vim在控制台上运行良好，也可以在许多GUI中本地运行，包括Mac OS和Windows。它还可以操作剪贴板。
- vi兼容模式：紧要关头，您可以强制Vim像vi一样。使Vim与vi不兼容的所有改进和错误修复都已关闭，您将获得100％与vi兼容的编辑器。

**Vim**作为许多程序员最喜欢的文本编辑器之一，它具有像：多级撤销、代码补全、支持数百种编程语言和文本格式、强大的搜索和替换功能等。

## 安装与卸载

### 安装

#### Windows

先把[安装包](https://www.vim.org/download.php)下载下来，然后根据提示安装。

#### Unix

在[Github](https://github.com/vim/vim/releases)上下载源文件安装

#### Mac

在[github](https://www.vim.org/download.php)下载，根据文件类型安装。

#### [详细安装教程](https://www.vim.org/download.php#unix)

### 卸载

#### Unix or Mac

##### 源代码安装

在控制台输入 

```
 make uninstall
```

##### 软件包管理器安装

根据不同软件包管理器的卸载命令卸载

#### Windows

找到安装目录下的 "uninstall-gui" 程序进行卸载

## 教程

### **vimtutor**

Vim自带教程**vimtutor**是你从零开始学习Vim最好的老师，教程包含了日常所需要的各个命令和功能，还有实操教学。如果你的系统语言是中文，那么打开**vimtutor**时默认是中文版的教程，中文版教程由**梁昌泰** 先生进行译制。在命令行中输入`vimtutor`，就可以打开该教程,学习完该教程大约需要30分钟左右。

有一款游戏[Vim Adventure](http://vim-adventures.com/)，可以作为学习Vim的一种放松。

### 帮助

在控制台中输入vim就可以查看Vim的相关信息

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1gaq8qqqumnj30va0iotag.jpg)

根据图片所示我们可以知道，当前VIM的版本为8.0.1365，想退出需要输入":q"，查看在线帮助文档可以输入":help"，查看版本信息可以输入":help version8"

在英文模式下输入":help"回车后便可以看到

![](https://tva4.sinaimg.cn/large/006lmzsGgy1gaq90e91hcj30vc0iu43p.jpg)

在这里有详细的Vim教程，教你玩转Vim。
