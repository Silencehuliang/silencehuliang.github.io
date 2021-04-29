# Python学习之路-工程搭建


## 环境安装

### 创建虚拟环境

```bash
mkvirtualenv django_1.11.10 -p python3
```

### 安装Django

使用`Django 1.11.10`版本

```bash
pip install django==1.11.10
```

## 创建工程

在使用Flask框架时，项目工程目录的组织与创建是需要我们自己手动创建完成的。在django中，项目工程目录可以借助django提供的命令帮助我们创建。

### 创建

创建工程的命令为：

```bash
django-admin startproject 工程名称
```

例如：想要在桌面的`DjangoProject`目录中创建一个名为`demo`的项目工程，可执行如下命令：

```bash
cd ~/Desktop/DjangoProject
django-admin startproject demo
```

执行后，会多出一个新目录名为demo，此即为新创建的工程目录。

### 工程目录说明

查看创建的工程目录

- 与项目同名的目录，此处为demo。
- **settings.py** 是项目的整体配置文件。
- **urls.py** 是项目的URL配置文件。
- **wsgi.py** 是项目与WSGI兼容的Web服务器入口。
- **manage.py** 是项目管理文件，通过它管理项目。

### 运行开发服务器

在开发阶段，为了能够快速预览到开发的效果，django提供了一个纯python编写的轻量级web服务器，仅在开发阶段使用。运行服务器命令如下：

```bash
python manage.py runserver ip:端口
或：
python manage.py runserver
```

**可以不写IP和端口，默认IP是127.0.0.1，默认端口为8000**。

在浏览器中输入网址“127.0.0.1:8000”便可看到效果。

{{< admonition tip "提示" true >}}

django默认工作在调式Debug模式下，如果增加、修改、删除文件，服务器会自动重启。按ctrl+c停止服务器。

{{< /admonition >}}

## 创建子应用

在Web应用中，通常有一些业务功能模块是在不同的项目中都可以复用的，故在开发中通常将工程项目拆分为不同的子功能模块，各功能模块间可以保持相对的独立，在其他工程项目中需要用到某个特定功能模块时，可以将该模块代码整体复制过去，达到复用。

在Flask框架中也有类似子功能应用模块的概念，即蓝图Blueprint。

**Django的视图编写是放在子应用中的。**

### 创建

在django中，创建子应用模块目录仍然可以通过命令来操作，即：

```bash
python manage.py startapp 子应用名称
```

**manage.py** 为上述创建工程时自动生成的管理文件。

例如，在刚才创建的demo工程中，想要创建一个用户users子应用模块，可执行：

```bash
cd ~/Desktop/code/demo
python manage.py startapp users
```

执行后，可以看到工程目录中多出了一个名为users的子目录。

### 子应用目录说明

查看此时的工程目录，结构如下：

- **admin.py** 文件跟网站的后台管理站点配置相关。
- **apps.py** 文件用于配置当前子应用的相关信息。
- **migrations** 目录用于存放数据库迁移历史文件。
- **models.py** 文件用户保存数据库模型类。
- **tests.py** 文件用于开发测试用例，编写单元测试。
- **views.py** 文件用于编写Web应用视图。

### 注册安装子应用

创建出来的子应用目录文件虽然被放到了工程项目目录中，但是django工程并不能立即直接使用该子应用，需要注册安装后才能使用。

在工程配置文件settings.py中，**INSTALLED_APPS**项保存了工程中已经注册安装的子应用，初始工程中的INSTALLED_APPS如下：

**注册安装一个子应用的方法，即是将子应用的配置信息文件apps.py中的Config类添加到INSTALLED_APPS列表中。**

例如，将刚创建的users子应用添加到工程中，可在INSTALLED_APPS列表中添加**'users.apps.UsersConfig'**。

## 创建视图

同Flask框架一样，Django也用视图来编写Web应用的业务逻辑。Django的视图是定义在子应用的views.py中的。

### 创建

打开刚创建的users模块，在views.py中编写视图代码。

```python
from django.http import HttpResponse

def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象
    :return: 响应对象
    """
    return HttpResponse("Hello Django")
```

{{< admonition tip "说明" true >}}

视图函数的第一个传入参数必须定义，用于接收Django构造的包含了请求数据的**HttpReqeust**对象，通常名为**request**。视图函数的返回值必须为一个响应对象，不能像Flask一样直接返回一个字符串，可以将要返回的字符串数据放到一个**HTTPResponse**对象中。

{{< /admonition >}}

### 定义路由URL

- 在子应用中新建一个urls.py文件用于保存该应用的路由。

- 在users/urls.py文件中定义路由信息。

  ```python
  from django.conf.urls import url

  from . import views

  # urlpatterns是被django自动识别的路由列表变量
  urlpatterns = [
      # 每个路由信息都需要使用url函数来构造
      # url(路径, 视图)
      url(r'^index/$', views.index),
  ]
  ```

- 在工程总路由demo/urls.py中添加子应用的路由数据。

  ```python
  from django.conf.urls import url, include
  from django.contrib import admin

  urlpatterns = [
      url(r'^admin/', admin.site.urls),  # django默认包含的

      # 添加
      url(r'^users/', include('users.urls')), 
  ]
  ```
	使用include来将子应用users里的全部路由包含进工程路由中；**r'^users/'** 决定了`users`子应用的所有路由都已**/users/**开头，如我们刚定义的视图index，其最终的完整访问路径为**/users/index/**。
	
	**include**函数除了可以传递字符串之外，也可以直接传递应用的urls模块，如

  ```python
  from django.conf.urls import url, include
  from django.contrib import admin
  import users.urls  # 先导入应用的urls模块

  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      # url(r'^users/', include('users.urls')),
      url(r'^users/', include(users.urls)),  # 添加应用的路由
  ]
  ```

- 启动运行

  重新启动django程序

  ```bash
  python manage.py runserver
  ```

  在浏览器中输入网址**127.0.0.1:8000/users/index/** 可看到返回的信息
