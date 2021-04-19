# 使用Hugo搭建自己的博客并通过GitHub Pages部署


## 前言

由于前一段时间学习了Golang，在家查阅相关资料的时候发现了[**Hugo**](https://gohugo.io/)这个用Go语言编写的静态网站生成器，根据网站的介绍它有着速度快，易用，可配置程度高等[特点](https://gohugo.io/about/features/)，而且文章依赖于Markdown生成，非常适合作为博客、文档、个人简历这类型的网站，于是我准备用Hugo搭建一个属于自己的博客，并将之前写的文章都搬运过来，最后通过GitHub Pages部署，一起开始吧！

## 使用Hugo搭建博客

### 安装

Mac和Linux可以直接用Homebrew安装

```bash
brew install hugo
```

Windows在[github](https://github.com/gohugoio/hugo/releases)上下载解压后安装，

{{< admonition warning "注意" true >}}
Windows安装完毕记得添加环境变量！
{{< /admonition >}}


此外Hugo官方还提供了多种[安装方式](https://gohugo.io/getting-started/installing)，选择自己喜欢的即可

安装完毕后，可以通过查询Hugo版本验证是否安装成功

```bash
hugo version
```

### 创建新站点

```bash
hugo new site SilenceBlog
```

![](https://tvax1.sinaimg.cn/large/00729CCqgy1gp6qpmyiftj30fa053abx.jpg)

创建成功图片

### 添加并配置主题

Hugo收录的主题非常多，可以在[主题库](https://themes.gohugo.io/)中寻找自己喜欢的

从GitHub下载主题到站点存放主题的目录中：

```bash
git clone https://github.com/dillonzq/LoveIt.git SilenceBlog/themes/LoveIt
```

将主题添加到站点的配置文件中：

```bash
echo theme = \"LoveIt\" >> config.toml
```

查看主题官方文档，并根据自己的情况进行配置

{{< admonition info "" true >}}
[LoveIt主题说明](https://github.com/dillonzq/LoveIt/blob/master/README.zh-cn.md)、[主题文档相关配置介绍](https://hugoloveit.com/zh-cn/theme-documentation-basics/)
{{< /admonition >}}

### 添加一篇文章并在本地查看效果

可以在content/posts/下手动创建一个Markdown文件，但是需要我们手动输入所有内容。也可以直接通过new命令来创建文章，创建好的文章已经存在相应的模板内容

```bash
hugo new posts/firstpost.md
```

输入完后会提是我们创建成功和文章所在的位置

![](https://tva2.sinaimg.cn/large/00729CCqgy1gp6rljde02j30dh00u3yt.jpg)

接下来可以打开这个文件进行编辑，当我们编辑完毕保存退出后，可以启动Hugo服务器查看效果

```bash
hugo server -D
```

启动后我们可以看到，本次启动的一些信息

![](https://tvax4.sinaimg.cn/large/00729CCqgy1gp6rq42zxvj30i607vgnk.jpg)

在浏览器中打开`http://localhost:1313/`即可查看效果，并且效果是实时更新的，会随着对站点博客的操作自动更新相应的效果

最后当我们完成博客内容想对博客部署的时候可以通过hugo命令进行建立静态页面

```bash
hugo -d 文件路径
```

{{< admonition tip "提示" true >}}

默认情况下会保存在./public/目录中

{{< /admonition >}}

{{< admonition info "" true >}}

更详细的内容可以查看[Hugo官方文档](https://gohugo.io/documentation/)

{{< /admonition >}}

## 通过GitHub Pages部署

### 什么是GitHub Pages

GitHub Pages 是一种静态网站托管服务，它可以直接从 GitHub 上的仓库中获取 HTML、CSS 和 JavaScript 文件，并通过构建过程选择性地运行这些文件，然后发布一个网站。

上面我们通过`hugo -D`命令正是将站点生成一个静态网站，可以完美配合GitHub Pages进行部署

### 部署方式

1.首先我们要创建一个Github 仓库，仓库名必须是`<user>.github.io`的形式，如果是组织则为`<organization>.github.io`。仓库的可见性必须是Public。

{{< admonition tip "提示" true >}}

用户名的大小写不会影响GitHub Pages的部署。例如我的仓库为：[Silencehuliang](https://github.com/Silencehuliang)/**[silencehuliang.github.io](https://github.com/Silencehuliang/silencehuliang.github.io)**

{{< /admonition >}}

2.接下来进入仓库的设置页对GitHub Pages进行配置，找到GitHub Pages所在的位置，按下图配置好分支和站点存放路径即可

![](https://tva3.sinaimg.cn/large/00729CCqgy1gp6tnklllnj30rx0ipdo0.jpg)

3.配置完毕后，把仓库克隆下来，使用`hugo -D 路径`将站点生成的静态文件存放在配置文件中选择的路径下即可。最后将文件提交上去就可以打开对应域名进行查看了。

### 出现问题的解决方案

当我们将文件提交上去之后打开对应域名发现并没有我们想要的内容时可以通过查看提交记录查看错误原因，点击Deatils可以找到具体位置的具体错误

![](https://tvax3.sinaimg.cn/large/00729CCqgy1gp6u18wlivj30q606841s.jpg)

还可以在GitHub Pages的设置出找到错误原因

![](https://tvax4.sinaimg.cn/large/00729CCqgy1gp6tx8q1bej30r30jxq6f.jpg)

{{< admonition info "" true >}}

更详细的内容可以查看[Hugo官方部署文档](https://gohugo.io/hosting-and-deployment/hosting-on-github/)或[GitHub Pages入门教程文档](https://docs.github.com/en/pages/getting-started-with-github-pages)

{{< /admonition >}}
