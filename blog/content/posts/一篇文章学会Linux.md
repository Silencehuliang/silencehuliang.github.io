---
title: "一篇文章学会Linux"
date: 2020-01-09T15:58:54+08:00
draft: false
categories: ["操作系统"]
tags: ["一篇文章学会系列"]
---

## 简介

### Linux

**Linux**是一种自由和开放源码的类UNIX操作系统。该操作系统的内核由林纳斯·托瓦兹在1991年10月5日首次发布，在加上用户空间的应用程序之后，成为Linux操作系统。只要遵循GNU 通用公共许可证（GPL），任何个人和机构都可以自由地使用Linux的所有底层源代码，也可以自由地修改和再发布。大多数Linux系统还包括像提供GUI的X Window之类的程序。除了一部分专家之外，大多数人都是直接使用Linux 发行版，而不是自己选择每一样组件或自行设置。[详细介绍](https://zh.wikipedia.org/wiki/Linux)

### linux发行版

**Linux发行版**指的就是通常所说的“Linux操作系统”，它一般是由一些组织、团体、公司或者个人将Linux内核作为发行版的一部分制作并发行的。通常来讲，一个Linux发行版包括Linux内核，以及将整个软件安装到电脑上的一套安装工具，还有各种GNU软件，和其他的一些自由软件，在一些Linux发行版中可能会包含一些专有软件。当前，超过三百个发行版被积极的开发，最普遍被使用的发行版有大约十二个。较为知名的有Debian、Ubuntu、Fedora和openSUSE等。

[**Linux发行版**份额排名](http://7z.cx/dsc/)，也可以在Linux终端用命令查看：`wget -qO - 7z.cx/o|sh`，Ubuntu以39.1%的占比遥遥领先，中国武汉深之度科技有限公司开发的deepin是国产**Linux发行版**中排名最高的，占比12.6%在排行榜中排名第三（截止于2020-01-10 13:54:19）

## 安装

如果是初次安装系统建议先通过在虚拟机上安装。

### 下载

下面提供较为知名的**Linux发行版**下载地址

[Ubuntu](https://ubuntu.com/download)、[manjaro](https://manjaro.org/download/)、[deepin](https://www.deepin.org/download/)、[CentOS](https://www.centos.org/download/)、[Arch](https://www.archlinux.org/download/)、[Debian](https://www.debian.org/CD/http-ftp/)、[Mint](https://linuxmint.com/download.php)、[Fedora](https://getfedora.org/en/workstation/download/)

**Linux发行版**提供了Server版和Desktop版，初次使用建议直接安装Server版。

### 安装

以Ubuntu Server 16.10为例

将镜像写入U盘后，开机以U盘为第一启动项启动，可以看到以下界面

![](https://tvax3.sinaimg.cn/large/006lmzsGgy1garfy9umhyj32lc1gitf0.jpg)

选择第一项安装Ubuntu Server

下一步选择语言，这里选择英语，防止乱码与文件名是中文的问题

![](https://tva1.sinaimg.cn/large/006lmzsGgy1garg0vpw3aj32lc1gin9h.jpg)

下一步选择区域，没有中国，所以先选其他

![](https://tvax3.sinaimg.cn/large/006lmzsGgy1garg3lx7z7j32lc1gi47j.jpg)

接下来选择亚洲Asia

![](https://tvax3.sinaimg.cn/large/006lmzsGgy1garg53j1esj32lc1gi7c9.jpg)

接着选这中国

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1garg6dwrcgj32lc1gi146.jpg)

下一步选择字符集，这里选择美国的UTF-8字符集，即en_US.UTF-8

![](https://tva4.sinaimg.cn/large/006lmzsGgy1garg86wyw6j32lc1giaka.jpg)

下一步检测键盘，选择否

![](https://tva1.sinaimg.cn/large/006lmzsGgy1gargbbgpkvj32lc1gidma.jpg)

接着让我们设置键盘的类型与布局

![](https://tvax4.sinaimg.cn/large/006lmzsGgy1gargc4ptctj32lc1giakp.jpg)

![](https://tva1.sinaimg.cn/large/006lmzsGgy1gargcii9fjj32lc1gin9c.jpg)

下一步是设置主机名称，默认为ubuntu，可以改为你喜欢的名称

![](https://tva3.sinaimg.cn/large/006lmzsGgy1gargeb4ovtj32lc1gi10d.jpg)

设置用户名

![](https://tva3.sinaimg.cn/large/006lmzsGgy1gargg9wwiwj32lc1gido1.jpg)

下一步设置登陆账号

![](https://tvax4.sinaimg.cn/large/006lmzsGgy1gargjunehkj32lc1gidna.jpg)

设置密码，可以在下面选择显示密码，可以确认一次

![](https://tva4.sinaimg.cn/large/006lmzsGgy1garglfwh0zj32lc1gi7bb.jpg)

再次输入，确认密码

![](https://tvax3.sinaimg.cn/large/006lmzsGgy1gargodu0a4j32lc1gidm7.jpg)

是否加密home文件夹，选择否

![](https://tva4.sinaimg.cn/large/006lmzsGgy1gargpfimajj32lc1gi0zz.jpg)

下一步系统根据区域推断出我们的市区是上海，没有问题，所以选择是

![](https://tva4.sinaimg.cn/large/006lmzsGgy1gargu0lqf0j32lc1gijxb.jpg)

选择分区方式，这里选择Guided - use entire disk and set up LVM

![](https://tva2.sinaimg.cn/large/006lmzsGgy1gargvdgj5oj32lc1gik05.jpg)

选择安装的硬盘

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1gargx0vgedj32lc1giqbb.jpg)

这里告诉我们会格式化这个盘确认选择

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1gargycrtkdj32lc1gi7b8.jpg)

选择自动安装

![](https://tva3.sinaimg.cn/large/006lmzsGgy1garhjbqigij32lc1gin2q.jpg)

确认分区

![](https://tvax3.sinaimg.cn/large/006lmzsGgy1garhkbocmdj32lc1giwob.jpg)

确认安装

![](https://tva4.sinaimg.cn/large/006lmzsGgy1garhleuym5j32lc1gin5f.jpg)

选择代理，没有就跳过

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1garhr55hyrj32lc1giwm2.jpg)



选择升级方式，这里选择不自动升级No automatic updates

![](https://tva1.sinaimg.cn/large/006lmzsGgy1garhogo0lkj32lc1giqbw.jpg)

安装完成后会重启，选择ubuntu启动即可

![](https://tva3.sinaimg.cn/large/006lmzsGgy1gari7smoekj32lc1giwkc.jpg)

进入系统后输入用户名密码就可以登录上ubuntu了，到此安装完毕

![](https://tva4.sinaimg.cn/large/006lmzsGgy1gari9dj5bgj32lc1gijyt.jpg)

## linux 根目录



