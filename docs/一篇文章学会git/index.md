# 一篇文章学会Git


## 简介

### 什么是Git

Git是一个免费的开源分布式版本控制系统，也是目前为止世界上最先进的分布式版本控制系统。Git官方有一个视频介绍，可以[点此观看](https://git-scm.com/video/what-is-git)



#### 什么是版本控制系统？

一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。简单点理解就是一个可以帮助我们记录文件修改的系统。Git官方有一个视频介绍，可以[点此观看](https://git-scm.com/video/what-is-version-control)



#### 什么是分布式版本控制系统？

分布式版本控制系统时相对于集中式版本控制系统的。

集中式版本控制系统将仓库存放在中央服务器中集中管理，当你需要时从中央服务器中拉取最新的版本，修改完后将修改提交给中央服务器。这就会带来例如当中央服务器宕机时整个版本控制系统就会崩溃；推送或者拉取一个较大的文件时就会消耗很多时间等弊端。

分布式版本控制系统中，每个人电脑都是一个仓库，自己的文件可以在本地管理，当需要多人协同时只需要管理好本地仓库与协同仓库的版本即可



### Git有什么作用

进行源代码管理



### 为什么要进行源代码管理

- 方便多人协同开发

- 方便代码版本控制

  

### Git的特点

- 分布式版本控制系统，服务器和客户端都有版本控制能力,都能进行代码的提交、合并等操作。
- 在使用Git的时候会自动创建一个.git的隐藏文件夹作为本地仓库



### Git操作流程

![](https://tvax3.sinaimg.cn/large/00729CCqgy1gdbwnczj2hj30bh0fct9l.jpg)

- `clone`：第一次从Git服务器获取项目
- add：将修改添加到本地仓库
- commit：将修改提交到本地仓库
- push：将本地仓库的修改提交到Git服务器
- pull：将Git服务器中的项目获取到本地仓库



### Git仓库

#### 什么是仓库

仓库的英文名是**repository**，又被称为版本库。它是一个被Git管理的文件目录。



### 工作区，暂存区和仓库

- 工作区：对代码的新增，修改，删除等操作的区域。
- 暂存区：存储工作区的操作的区域。
- 仓库区：即本地仓库区域，会记录完成的操作与历史版本。

![](https://tva2.sinaimg.cn/large/00729CCqgy1gdbxah8gyzj30k909fgol.jpg)



### Git操作

#### 安装

##### Mac

在mac上有多种方法可以安装Git，最简单的事通过Xcode命令行工具安装。

- 通过Xcode安装

  1.下载并安装Xcode

  2.在终端中运行git即可，如果尚未安装，它将提示您安装。

- 通过homebrew安装

  1.安装homebrew

  ```bash
  $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
  
  2.安装git

  ```bash
  $ brew install git
  ```

- 通过安装包安装

  1.点击此[下载最新版本](https://git-scm.com/download/mac)

  2.下载完成后打开安装包，一直下一步安装即可



##### Linux 

在Linux发行版上安装GIt，可以通过附带的软件包管理工具来安装

- Debian/Ubuntu

  ```bash
  $ apt-get install git
  ```

其他发行版本见这个[链接](https://git-scm.com/download/linux)



##### Windows

- 下载安装包

  根据操作系统位数选择，[链接](https://git-scm.com/download/win)

- 安装默认选项安装即可



安装完成后通过可以通过`git --version`查看安装版本



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



##### Git编辑器配置

Git默认的编辑器是系统默认编辑器

如果要是用其他文本编辑器（例如vim），则可以执行以下操作：

```bash
$ git config --global core.editor vim
```



##### 查看配置

如果要查看配置，可以使用`git config --list`命令列出Git可以找到的所有设置

你可能会看到很多配置项，找不到你想要的，这时候你可以通过`git config <key>`来查看特定的配置，例：

```
$ git config user.name
silencehuliang
```



### 帮助

#### 获取方式

Git获取帮助的方式有三种`git help <verb>`、`git <verb> --help`、`man git-<verb>`

例如，可以通过`git help config`获取config的相关帮助

如果只需要快速了解Git命令的可用选项也可以用`-h`来查看相关帮助

例如`git add -h`



### 创建项目

1.将本地不收版本控制的目录转换为Git仓库

①进入本地目录

```bash
$ cd ~/Desktop/project
```

②输入转化命令

```bash
$ git init
```

此时会在当前目录下创建一个`.git`目录，里面存放着Git仓库中所有的必须文件

```bash
$ ls -a
.	..	.git
```

2.从其他地方克隆现有的Git仓库

①进入我们需要存放仓库的路径

```bash
$ cd ~/Desktop/
```

②将现有的仓库克隆下来

```bash
$ git clone https://github.com/Silencehuliang/project
```

### 

### 查看状态

- 可以通过`git status` 查看仓库中稳健的状态
- 绿色表示文件在暂存区
- 红色表示文件在工作区

可以通过`git add` 将工作区文件添加到暂存区

- 添加项目中所有文件：`git add .`

- 添加指定文件：`git add xxx.py`

可以通过`git commit`将暂存区文件提交到仓库区

- `git commit -m "修改描述"`，其中-m参数后面跟的是对本次修改的描述
- `git commit -am "修改描述"`,可以通过-am来实现添加和提交合并操作



### 查看历史版本

通过`git log`或者`git relog`可以查看历史版本



### 回退版本

- 通过版本号会退版本

  ```git
    git reset --hard 版本号
  ```

- 通过`HEAD`回退版本

  当工作区文件发生了意外需要回退到上一个版本时可以通过

  ```git
  `git reset --hard HEAD`
  ```

  - `HEAD`表示当前最新版本
  - `HEAD^`表示当前最新版本的前一个版本
  - `HEAD^^`表示当前最新版本的前两个版本，**以此类推...**
  - `HEAD~1`表示当前最新版本的前一个版本
  - `HEAD~10`表示当前最新版本的前10个版本，**以此类推...**



### 撤销修改

- 只能撤销工作区、暂存区的代码,不能撤销仓库区的代码

- 撤销仓库区的代码就相当于回退版本操作

  - 撤销工作区代码

    - 新加代码`num3 = 30`，不`add`到暂存区，保留在工作区

      ```
      git checkout 文件名
      ```

  - 撤销暂存区代码

    - 新加代码`num3 = 30`，并`add`到暂存区

      ```
      # 第一步：将暂存区代码撤销到工作区
      git reset HEAD  文件名
      # 第二步：撤销工作区代码
      git checkout 文件名
      ```



### 对比版本

对比版本库与工作区

- 新加代码`num3 = 30`，不`add`到暂存区，保留在工作区
- `git diff HEAD -- xxx.py`

对比版本库

- 新加代码`num3 = 30`，并`add`到暂存区
- `git diff HEAD HEAD^ -- xxx.py`



### 删除文件

删除文件分为确定删除和误删

- 在项目中新建`test.py`文件，并添加和提交到仓库

  - 确定删除处理：

    ```
      # 删除文件
      rm 文件名
      # git确定删除文件，对比添加文件git add 
      git rm 文件名
      # 删除后记录删除操作版本
      git commit -m '删除描述'
    ```

- 误删处理：撤销修改即可

  ```
    # 删除文件
    rm 文件名
    # git撤销修改
    git checkout -- 文件名
  ```



### 代码冲突

**提示**：多人协同开发时，避免不了会出现代码冲突的情况

**原因**：多人同时修改了同一个文件

**危害**：会影响正常的开发进度

**注意**：一旦出现代码冲突，必须先解决再做后续开发

#### 解决冲突

- 原则：谁冲突谁解决，并且一定要协商解决
- 方案：保留所有代码 或者 保留某一人代码
- 解决完冲突代码后，依然需要`add`、`commit`、`push`，如果执行`pull`没有影响，就算真正解决了冲突代码

#### 补充：

- **容易冲突的操作方式**
  - 多个人同时操作了同一个文件
  - 一个人一直写不提交
  - 修改之前不更新最新代码
  - 提交之前不更新最新代码
  - 擅自修改同事代码
- **减少冲突的操作方式**
  - 养成良好的操作习惯,先`pull`在修改,修改完立即`commit`和`push`
  - 一定要确保自己正在修改的文件是最新版本的
  - 各自开发各自的模块
  - 如果要修改公共文件,一定要先确认有没有人正在修改
  - 下班前一定要提交代码,上班第一件事拉取最新代码
  - 一定不要擅自修改同事的代码



### 标签

- 当某一个大版本完成之后,需要打一个标签
- 作用：
  - 记录大版本
  - 备份大版本代码

#### 在本地打标签

```
git tag -a 标签名 -m '标签描述'
```

#### 推送标签到远程仓库

```
git push origin 标签名
```

删除本地和远程标签

```
  # 删除本地标签
  git tag -d 标签名
  # 删除远程仓库标签
  git push origin --delete tag 标签名
```



### 分支

- 作用：
  - 区分生产环境代码以及开发环境代码
  - 研究新的功能或者攻关难题
  - 解决线上bug
- 特点：
  - 项目开发中公用分支包括master、dev
  - 分支master是默认分支，用于发布，当需要发布时将dev分支合并到master分支
  - 分支dev是用于开发的分支，开发完阶段性的代码后，需要合并到master分支

#### 查看当前分支

```
  git branch
```



#### 创建并切换到dev分支

```
 git checkout -b dev
```



#### 设置本地分支跟踪远程指定分支（将分支推送到远程）

```
  git push -u origin dev
```



分支合并到master分支

- 先切换到master分支

  ```
    git checkout master
  ```

- 分支合并到master分支

  ```
    git merge dev
  ```
