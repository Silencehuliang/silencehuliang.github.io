---
title: "Django基础教程之工程搭建"
description: "Django介绍"
date: 2019-02-17
draft: false
categories: ["Django"] 
tags: ["Django教程"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

本教程为Django基础教程系列第二篇，前面篇章在以下链接：

[Django基础教程之Django介绍](http://49.235.231.121/2019/django基础教程一/)



## 简介

每个工程项目的开始阶段往往决定了项目的大致走向，在工程搭建的过程中要为后面的项目开发做好准备。

为了不受Python环境的影响，最好建立虚拟环境，在虚拟环境中搭建项目

## 教程

### 安装环境
#### 安装virtualenv 
[virtualenv](https://pypi.org/project/virtualenv/)是一个用于创建Python虚拟环境的工具包，可以通过pip直接安装

```python
pip3 install virtualenv
```



#### 创建虚拟环境

```python
virtualenv --python=/usr/bin/python3 django2.2.2_py3
```

django2.2.2_py3为虚拟环境的名字，这里是以Django的版本+Python版本命名，--python指定了Python的位置。



#### 激活虚拟环境

```python
source django2.2.2_py3/bin/activate
```

激活完成后会在命令行最前面显示当前的虚拟环境名



#### 安装Django

本教程使用django2.2.2版本

```python
pip install django==2.2.2
```



### 项目工程

在Django中，项目的工程目录可以通过Django提供的命令来创建。



#### 创建

创建工程的命令为：

```python
django-admin startproject 工程名称
```

例如你想在做面食创建一个demo的工程项目，可以执行如下命令：

```python
cd ~/Desktop/
django-admin startproject demo
```

执行完毕后，会在当前目录即`Desktop`目录下生成一个名为demo的目录，该目录存放着整个Django工程



#### 工程目录说明

查看创建的工程目录，结构如下

```python
(django2.2.2_py3) ~/Desktop/demo$ tree
.
|-- demo
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
`-- manage.py

1 directory, 5 files
```

- **demo**：与项目同名的目录，存放项目相关文件。
- **settings.py**：项目的配置文件。
- **urls.py**：项目的总URL配置文件。
- **wsgi.py**：项目与WSGI兼容的Web服务器入口。
- **manage.py** 项目管理文件，通过它管理项目，同时也是启动项目的入口。



#### 运行开发服务器

在开发阶段，为了能够快速预览到开发的效果，Djnago提供了一个纯python编写的轻量级web服务器，提供开发阶段使用。

运行服务器命令如下：

```python
python manage.py runserver
```

**默认IP是127.0.0.1，默认端口为8000，可以写指定IP与端口，格式为：ip:端口**

启动后可以看到以下信息

```
(django2.2.2_py3) ~/Desktop/demo$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

February 17, 2019 - 05:29:56
Django version 2.2.2, using settings 'demo.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

在浏览器中输入网址“127.0.0.1:8000”便可看到效果。

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1gazi40lmx6j31h70s5t9z.jpg)

- django默认工作在调式Debug模式下，如果增加、修改、删除文件，服务器会自动重启。
- 按ctrl+c停止服务器。



### 应用

在Web开发中通常一个大型项目是由无数个应用构成的。将开发中的工程项目拆分成不同的功能模块，可以让各功能模块之间保持相对独立，更利于我们开发与管理。



#### 创建

Django为我们提供了创建应用的命令，创建应用的命令为：

```python
python manage.py startapp 子应用名称
```

**需要注意的是，创建应用时必须在manage.py所在的目录下**

现在创建一个用户相关的应用users，可以执行：

```python
python manage.py startapp users
```

执行后，可以看到工程目录中多出了一个名为users的子目录。



#### 应用目录说明

```bash
(django2.2.2_py3) ~/Desktop/demo$ ls
db.sqlite3  demo  manage.py  users
(django2.2.2_py3) ~/Desktop/demo$ tree
.
|-- db.sqlite3
|-- demo
|   |-- __init__.py
|   |-- __pycache__
|   |   |-- __init__.cpython-36.pyc
|   |   |-- settings.cpython-36.pyc
|   |   |-- urls.cpython-36.pyc
|   |   `-- wsgi.cpython-36.pyc
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- manage.py
`-- users
    |-- __init__.py
    |-- admin.py
    |-- apps.py
    |-- migrations
    |   `-- __init__.py
    |-- models.py
    |-- tests.py
    `-- views.py

4 directories, 17 files
```

- **admin.py**：后台管理配置信息。
- **apps.py**：配置信息。
- **migrations** 存放数据库迁移历史文件。
- **models.py**：保存数据库模型类。
- **tests.py**：用于开发测试用例，编写单元测试。

#### 注册应用

创建完应用后Django并不能自动将项目与应用联系起来，需要我们在工程配置文件`settings.py`中注册才能使用。

在工程配置文件`settings.py`中的**INSTALLED_APPS**项负责注册安装好的应用，初始工程中的INSTALLED_APPS如下：

![](https://tva3.sinaimg.cn/large/006lmzsGgy1gazjj3xb2dj318s0pun2d.jpg)

这些默认应用的作用可以看这篇文章：[Django配置文件详解]()

**注册一个应用的方法是将应用的配置信息文件apps.py中的Config类添加到INSTALLED_APPS列表中。**

例如，注册刚创建的users应用，可在INSTALLED_APPS列表中添加**'users.apps.UsersConfig'**。

![](https://tva3.sinaimg.cn/large/006lmzsGgy1gazjpcuif9j31mq0uq45b.jpg)



#### 创建视图

视图用于编写应用的业务逻辑，Django的视图是在应用中views.py中的

进入users应用，在views.py中编写视图代码。

```python
from django.http import HttpResponse

def index(request):
    """
    视图index
    :param request: 包含了请求信息的请求对象
    :return: 响应对象
    """
    return HttpResponse("hello Django")
```

说明：

[Django基础教程之Django介绍]([http://49.235.231.121/2019/django%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B%E4%B8%80/#mvt%E6%A8%A1%E5%BC%8F](http://49.235.231.121/2019/django基础教程一/#mvt模式))中提到过，Django中视图的功能是接受请求，进行业务处理，返回响应。在这里request是接受请求的对象，业务处理是生成`hello Django`字符串，而HttpResponse是返回响应的对象。



### 路由

#### 什么是路由

在Django中，路由是将请求的URL分发给视图的系统。



#### 路由定义的位置

一般情况下会有两种路由定义的位置，一种是[项目工程中](# 工程目录说明)的urls.py中，一种是每个应用下的urls.py中。[项目工程中](# 工程目录说明)的urls.py是Django解析路由的入口



#### 路由解析顺序

Django在接收到请求时会先从[项目工程](# 工程目录说明)urls.py中的urlpatterns列表中从上至下的顺序查找对应路由规则，如果发现规则为include包含，则再进入被包含的urls中的urlpatterns列表由上至下进行查询。



#### 路由命名

在定义路由的时候，可以为路由命名，方便查找特定视图的具体路径信息。

- 在定义include函数定义路由时，可以使用namespace参数定义路由的命名空间，如

  ```python
  url(r'^users/', include('users.urls', namespace='users')),
  ```

  命名空间表示，凡是users.urls中定义的路由，均属于namespace指明的users名下。

  **命名空间的作用：避免不同应用中的路由使用了相同的名字发生冲突，使用命名空间区别开。**

- 在定义普通路由时，可以使用name参数指明路由的名字，如

  ```python
  urlpatterns = [
      url(r'^index/$', views.index, name='index'),
  ]
  ```

#### 路径结尾斜线的说明

Django中定义路由时，通常以斜线结尾，其好处是用户访问不以斜线结尾的相同路径时，Django会把用户重定向到以斜线/结尾的路径上，而不会返回404不存在。如

```python
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
]
```

用户访问 index 或者 index/ 网址，均能访问到index视图。

虽然路由结尾带斜线能带来上述好处，但是却违背了HTTP中URL表示资源位置路径的设计理念。具体是否结尾带斜线以个人风格为准。



接下来我们要通过路由将工程->应用->视图给联系起来

首先在工程的[总路由](#工程目录说明)中添加users应用的路由信息

```python
from django.contrib import admin
+ from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
 +  path('users/', include('users.urls')),
]
```

说明：

- 'users/'表示所有/users/开头的请求
- include表示以/users/匹配到users应用中urls.py的所有路由，即只要请求的URL是/users/开头都会去users应用中的urls.py中匹配剩下的路由。



将总路由引到users应用后，需要修改users应用中urls.py的信息

```python
from django.conf.urls import url,re_path
  
from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
		# re_path是通过正则表达式来构造路由
  	# re_path(路由正则表达式，视图)
    re_path(r'^index/$', views.index),
]                                                              
```

说明：

- 现在完整的请求url为：/users/index/

路由修改完成后，重启Django程序，就可以在浏览器中看到返回的信息了

