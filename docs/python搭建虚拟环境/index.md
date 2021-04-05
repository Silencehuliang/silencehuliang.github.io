# Python搭建虚拟环境


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
  - 输入activate，当命令提示符多了一个虚拟环境名字的前缀时即激活成功

- Linux or Mac

  - 通过source激活使用，当命令提示符多了一个虚拟环境名字的前缀时即激活成功

    ```python
    source first_env/bin/activate
    ```



### 退出虚拟环境

在当前虚拟环境中输入deactivate，当命令提示符虚拟环境名字的前缀消失时即退出

### 删除虚拟环境

在我们不需要这个虚拟环境的时候只需要将该虚拟环境的整个包删除即可

## Pipenv

### 简介

Pipenv是Kenneth Reitz在2017年1月发布的Python依赖管理工具，现在由PyPA维护。可以把它看做是pip和virtualenv的组合。

### 为什么使用Pipenv

Pipenv会自动帮你管理虚拟环境和依赖文件，并且提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作。简而言之，它更方便、完善和安全。

### 如何使用Pipenv

#### 安装

```bash
pip install pipenv
```

#### 创建

在项目根目录下执行`pipenv install`，Pipenv会根据项目文件夹的名称创建一个虚拟环境，并且会在项目根目录下生成 Pipfile 和 Pipfile.lock 用于管理项目依赖（以后使用 Pipenv 安装的依赖会自动写入 Pipfile 文件，无需再手动维护 requirements.txt 文件)

{{< admonition tip "提示" true >}}

默认情况下Pipenv会将虚拟环境创建在~/.virtualenvs 目录下，在项目根目录下执行 `pipenv --venv` 可以查看到项目对应的虚拟环境的具体位置

{{< /admonition >}}

#### 激活使用

两种方式

- 在项目根目录下执行`pipenv shell`
- 在项目根目录下执行`pipenv run + 命令`


