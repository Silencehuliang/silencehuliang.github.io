# Python学习之路-HelloPython


## Python解释器

### 简介

前面说到Python是解释型语言，Python解释器的作用就是用于"翻译"Python程序。Python规定了一个Python语法规则，根据该规则可编写Python解释器。

### 常见的Python解释器

- [CPython](https://zh.wikipedia.org/wiki/CPython)：官方提供的解释器，由C语言实现，这是最常用的Python解释器。

- [PyPy](https://zh.wikipedia.org/wiki/PyPy)：一种用Python语言实现的解释器，可用于替代CPython。PyPy采用即时编译通常运行速度比CPython快很多。多数Python代码可以很好的运行在PyPy之上，除非代码依赖于CPython扩展，

- [Jython](https://zh.wikipedia.org/wiki/Jython):一种用Java语言实现的解释器，Jython可以直接调用Java的各种函数库。

## 安装

Python是一门跨平台的脚本语言，不同平台的安装过程稍有区别。

{{< admonition info "注意" true >}}

以下安装部分内容仅针对CPython。内容参考Python官方的[安装教程](https://docs.python.org/zh-cn/3.6/using/index.html)，由我摘选出来各平台比较方便快捷的安装方式。如果不符合需求，可以查看官方[安装教程](https://docs.python.org/zh-cn/3.6/using/index.html)搜索需要的内容。

{{< /admonition >}}

### Linux

Python预装在大多数Linux发行版上，并作为一个包提供给所有其他用户。 也可以从源代码编译最新版本的Python。

如果Python没有预先安装并且不在发行版提供的库中，也可以轻松地为自己使用的发行版创建包。 参阅以下链接：

[Debian](https://www.debian.org/doc/manuals/maint-guide/first.en.html)、[OpenSuse](https://en.opensuse.org/Portal:Packaging)、[Fedora](https://docs-old.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-creating-rpms.html)、[Slackware](http://www.slackbook.org/html/package-management-making-packages.html)

从源代码编译

- 首先要做的是获取 [source](https://www.python.org/downloads/source/) 。您可以下载最新版本的源代码，也可以直接提取最新的 [clone](https://devguide.python.org/setup/#getting-the-source-code) 。

- 构建过程由常用命令组成：

  ```bash
  ./configure
  make
  make install
  ```

{{< admonition tip "提示" true >}}

特定Unix平台的配置选项和注意事项通常记录在Python源代码的根目录下的 [README.rst](https://github.com/python/cpython/tree/3.9/README.rst) 文件中。

{{< /admonition >}}

{{< admonition warning "" true >}}

`make install` 可以覆盖或伪装 `python3` 二进制文件。因此，建议使用 `make altinstall` 而不是 `make install` ，因为后者只安装了 `*exec_prefix*/bin/python*version*` 。

{{< /admonition >}}

### Windows

- 从[Python官方](https://www.python.org/downloads/windows/)获取安装包

- 根据需求进行安装包安装

  ![](https://tvax1.sinaimg.cn/large/00729CCqgy1gp9z3w3ik3j30im0bit9r.jpg)

- 安装完毕后将Python解释器的路径添加到系统环境变量中
  
  {{< admonition tip "提示" true >}}
  
  √上`Add Python 3.x to PATH`后安装程序会自动将PythonPython解释器的路径添加到系统环境变量中)
  
  {{< /admonition >}}

### Mac OS X

通过Homebrew安装

{{< admonition tip "提示" true >}}

使用`brew install python3`默认安装最新版本，可以通过安装pyenv后安装指定版本的Python。根据需求自行选择

{{< /admonition >}}

  - 安装`pyenv`
    ```bash
    brew install pyenv
    ```

  - 将`pyenv`添加到shell中

    ```bash
    echo -e 'if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi'>> ~/.bash_profile
    ```

  - 使shell生效
    ```bash
    exec "$SHELL"
    ```

  - 查看可安装的Python版本
    ```bash
    pyenv install -l
    ```

  - 安装需求的Python版本
    ```bash
    pyenv install 3.7.1
    ```

  - 指定全局的Python环境
    ```bash
    pyenv global 3.7.1
    ```

  - 查看已安装的Python版本和正在使用的Python版本
    ```bash
    pyenv versions
    ```

### 检查

安装完毕之后可以通过查看Python版本号的方式来检查是否安装成功

```bash
python3 -V
Python 3.7.7
```

或者进入Python交互式命令行中查看，在交互式命令行输入`python3`能进入交互式命令行并且版本对则安装成功



## 第一个Python程序

### 交互式命令行

#### 简介

在控制台输入Python3即可进入Python3解释器集成的一个交互式命令行。

```bash
python3
Python 3.7.1 (default,  Oct. 20, 2018, 15:43:33) 
[Clang 11.0.0 (clang-1100.0.33.17)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

这里我们可以看到Python的版本、当前版本发布的时间和查询相关信息的指令，例如输入`help()`可以查询到帮助相关的信息。

#### 使用

在交互式命令行中写入`print('Hello Python!')`按回车

  ```python
  >>> print("Hello Python!")
  Hello Python!
  ```

这里使用了Python一个内置的print()方法，其作用是将传入的对象在控制台打印出来。就这么简单的完成了学习Python的第一个程序，可以看到Python的语法非常简单易懂。

由于在交互式命令行中编写的Python代码无法保存，当需要保存代码的时候可以用文本编辑器或集成开发环境来编写Python代码。

{{< admonition tip "提示" true >}}

通过quit()方法退出Python的交互式命令行。

{{< /admonition >}}



### 文本编辑器和集成开发环境

#### 简介

**文本编辑器**是计算机软件中的一种。主要用于用来编写和查看文本文件。有一些特殊的文本编辑器支持增加自有的格式来丰富文档的表现形式。操作系统或者集成开发环境通常会带有可以查看和编辑纯文本的编辑器，可增加格式的文本编辑器通常是个人用户或者公司在制作需要格式的文件中使用。因为程序和程序的配置文件通常是以纯文本形式储存，所以程序员也需要使用纯文本编辑器来编辑程序和配置文件。

**集成开发环境**（Integrated Development Environment，简称**IDE**）是一种辅助程序开发人员开发软件的应用软件，在开发工具内部就可以辅助编写源代码文本、并编译打包成为可用的程序，有些甚至可以设计图形接口。IDE通常包括编程语言编辑器、自动构建工具、通常还包括调试器。

**在初学阶段建议用文本编辑器来进行开发，更有利于掌握Python基础相关知识。**

#### 使用

- 首先打开一个文本编辑器(系统自带的即可)，写入`print("Hello Python!")`

  {{< admonition note "注意" true >}}

  这句话一定要顶格写，Python对缩进的要求非常严格。注意`print`方法名的小写和中英文字符问题！

  {{< /admonition >}}

- 将文本保存为`Hello.py`在控制台中切换到当前目录，输入`python3 Hello.py`来运行该程序

  ```bash
  python3 Hello.py
  Hello Python!
  ```

  看到`Hello Python!`代码第一个程序执行成功。

  {{< admonition info "说明" true >}}

  Python程序以`.py`结尾。控制台中输入的`python3`为指定的Python解释器

  {{< /admonition >}}
