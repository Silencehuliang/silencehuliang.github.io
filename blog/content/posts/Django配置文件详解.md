---
÷title: "Django配置文件详解"
date: 2019-01-06T15:58:54+08:00
draft: false
categories: ["Django"] 
tags: ["配置文件"]
---

## 简介

学习Django可以从Django配置文件的各项开始，由简入深的了解其作用，从而一步一步学习。本篇文章主要是介绍各项的作用以及如何配置，可以根据需求按需配置。

## 内容

### 绝对路径映射

`ABSOLUTE_URL_OVERRIDES`

作用：将应用的模型字符串映射到采用模型对象并返回其url，基于get_absolute_url方法。无论实际模型类名称的大小写如何，此设置中使用的模型名称均应全部小写。

### 绝对路径映射

`ADMINS`

作用：用于接收代码错误的人员列表，列表中的元素格式为（全名，电子邮箱）

### Django项目根路径

`BASE_DIR`

作用：以项目根路径为基础衍生其他文件

```python
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

- 从内到外一步一步剖析
  - \_\_file\_\_：返回当前文件
  - os.path.abspath(\_\_file\_\_)：返回当前文件的绝对路径
    - os.path.dirname(os.path.abspath(\_\_file\_\_))：返回当前文件的父目录
  - os.path.dirname(os.path.dirname(os.path.abspath(\_\_file\_\_)))：返回当前文件父目录的父目录

可能这样还不太清楚，将\_\_file\_\_换成settings.py,可以看出来BASE_DIR是manage.py所在的目录，即整个项目的根目录

   

### 秘钥

`SECRET_KEY`

作用：校验，主要用于表单、session、csrf

```
  SECRET_KEY = "adsasdasdsafdasfldasfklasdlfnlasdnfklnasdfklnasldfklkdasf"
```



### 调试模式

`DEBUG`

  作用：当开启时，运行出现bug会在前端直接显示，开发，测试过程可以开启

```python
  DEBUG = True
```

  

### 允许访问的主机

`ALLOWED_HOSTS`

  作用：在开发的时候可以使用\*，当项目上线后需要更换为指定的主机(域名和ip都可以)

```python
  ALLOWED_HOSTS = []
```

  

### 应用、模块注册

`INSTALLED_APPS`

  作用：将独立的应用或模块接入Django（**注意应用名称或者模块名称必须是唯一的**）

```python
  INSTALLED_APPS = [    
      'django.contrib.admin',    
      'django.contrib.auth',    
      'django.contrib.contenttypes',    
      'django.contrib.sessions',    
      'django.contrib.messages',    
      'django.contrib.staticfiles',       
  ]
```

  通常INSTALLED_APPS默认包含以下Django自带的应用

  - django.contrib.admin：管理员站点，可以通过admin管理项目（数据、用户、权限等），使用admin必须完成以下配置

    - 他依赖django.contrib.auth、django.contrib.contenttypes、django.contrib.sessions、django.contrib.messages四个模块

    - MIDDLEWARE设置必须包括 django.contrib.auth.middleware.AuthenticationMiddleware并且django.contrib.messages.middleware.MessageMiddleware

    - 在项目url配置中必须加入admin

      ```python
      urls.py
      
      from django.contrib import admin
      from django.urls import path
      
      urlpatterns = [
          path('admin/', admin.site.urls),
      ]
      ```

      可以使用django-admin createsuperuser创建管理员用户

  - django.contrib.auth：认证授权系统。主要负责校验用户信息与用户权限，由以下部分组成

    - 用户：用户管理

    - 权限：以二进制的形式标识指定用户是否可以执行的特殊任务

    - 组：管理多个用户的权限

    - 可配置的密码哈希话系统

    - 为登录用户或限制内容提供表单和视图工具

    - 可插拔的后端系统

      **需要注意的是它不提供密码强度检查、限制登录尝试、第三方身份验证，对象级权限**

  - django.contrib.contenttypes：内容类型框架,他可以跟踪Django驱动的项目中安装的所有模型，为模型提供高级的通用界面

  - django.contrib.sessions：会话框架

  - django.contrib.messages：消息框架

  - staticfiles：管理静态文件框架

  除了这些常见的自带应用外，在我们使用自己注册的应用和第三方模块时，记得第一时间来这里注册，否则会用不了哦



### 中间件

`MIDDLEWARE`

  作用：中间件是Django请求/响应处理的钩子框架，用于改变Django的输入或输出

  中间件可以放在Python路径上的任何地方，可以自己编写中间件，中间件可以是函数也可以是类。

  函数形式的中间件

```python
  def simple_middleware(get_response):
  	# 首次配置和初始化
      def middleware(request):
      	# 每个请求之前或调用视图函数之前执行的代码
      	
          response = get_response(request)
          
          # 每个响应、请求或者调用视图函数之后执行的代码
          
          return response
      return middleware
```

  类形式的中间件

```python
      def __init__(self, get_response):
          self.get_response = get_response
          # 首次配置和初始化
  
      def __call__(self, request):
          # 每个请求之前或调用视图函数之前执行的代码
  
          response = self.get_response(request)
  
          # 每个响应、请求或者调用视图函数之后执行的代码
  
          return response
```

  - 上述方法中调用get_response方法并不是实际视图中的，而是处理程序的包装方法，它负责应用视图中间件，调用具有适当的URL参数的视图，并应用模板响应和第三方中间件。

  - 在使用类形式的中间件时，\_\_init_\_方法必须接受get_response参数，还可以初始化中间件的一些局部状态。

  - 想使用中间件就必须在settings.py文件中的MIDDLEWARE中激活。激活的方式是使用字符串表示指向中间件完整的Python路径

  - 在Django中MIDDLEWARE可以为空，但是强烈建议至少激活CommonMiddleware

  - 由于某些中间件也会依赖其他中间件所以中间件在MIDDLEWARE中的顺序很重要，Django会按自上而下的顺序调用中间件

    

### 路由根路径

`ROOT_URLCONF`

  作用：Django在处理请求时会最先从此处寻找url

  需要注意的是，此处的路径是基于BASE_DIR的路径

  

### 模板引擎配置

`TEMPLATES`

  作用：在Django中使用模板引擎的设置列表，列表中每个元素都是一个字典，字典里配置模板引擎



  **常用的配置参数**：

  - `BACKEND`：项目使用的模板引擎，Django内置了两个
    - django.template.backends.django.DjangoTemplates
    - django.template.backends.jinja2.Jinja2
  - `DIRS`：模板文件夹的位置
  - `APP_DIRS`：模板引擎是否在已安装的应用中讯在模板源文件
  - `OPTIONS`：传给后端模板的额外参数



### 内置服务器的路径  

`WSGI_APPLICATION`

  作用：用于调式Django程序的内置服务器，

  

### 数据库配置

`DATABASES`

  在mysite/mysite/settings.py中，默认的数据库为SQLite，还支持PostgreSQL、mysql、oracle等其他第三方（这些非官方后端支持的Django版本和ORM功能差异很大。有关这些非官方后端的具体功能的查询以及任何支持查询，应该针对每个第三方项目提供的支持渠道）

```
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }
  }
```

  - ENGINE，数据库引擎，可选的ENGINE还有

```
  django.db.backends.postgresql、django.db.backends.mysql、django.db.backends.oracle、第三方数据库
```

  - NAME，数据库名称，如果使用SQLite,他会在根目录生成一个数据库文件

  - 当不使用SQLite时，还会有一下常用参数，其他参数可以查阅文档[`DATABASES`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DATABASES) 

    - NAME：数据库名字

    - USER：数据库的用户名

    - PASSWORD：数据库的密码

    - HOST：数据库的主机

    - PORT：数据库的端口

    - OPTIONS：连接到数据库时要使用的其他参数。可用参数取决于数据库后端。

    - TEST：测试数据库

      测试数据库也具备一些设置，也是采用键值对的方式对数据库进行设置

      - CHARSET：创建测试数据库时使用的字符集编码
      - COLLATION：创建测试数据库时使用的排序规则
      - DEPENDENCIES：数据库的创建顺序依耐性
      - MIRROR：测试期间该数据库应镜像的数据库别名。
      - NAME：运行测试套件时要使用的数据库的名称。
      - SERIALIZE：一个布尔值，用于控制默认测试运行程序在运行测试之前是否将数据库序列化为内存中的JSON字符串。`False`如果没有任何带有测试类，可以将其设置为加快创建时间。
      - TEMPLATE：PostgreSQL的特定设置。从中创建测试数据库的模板（例如`'template0'`）的名称。
      - CREATE_DB：默认为True，Oracle特定的设置。如果将其设置为`False`，则测试表空间将不会在测试开始时自动创建，也不会在测试结束时自动删除。
      - CREATE_USER：默认为True，Oracle特定的设置。如果将其设置为`False`，则不会在测试开始时自动创建测试用户，并在测试结束时自动将其删除。
      - USER：默认为None，Oracle特定的设置。连接到运行测试时将使用的Oracle数据库时使用的用户名。如果未提供，则Django将使用。`'test_' + USER`
      - PASSWORD：默认为None，Oracle特定的设置。连接到运行测试时将使用的Oracle数据库的密码。如果未提供，Django将生成一个随机密码。
      - TBLSPACE：默认为None，Oracle特定的设置。运行测试时将使用的表空间的名称。如果未提供，则Django将使用。`'test_' + USER`
      - TBLSPACE_TMP：默认为None，Oracle特定的设置。运行测试时将使用的临时表空间的名称。如果未提供，则Django将使用。`'test_' + USER + '_temp'`
      - DATAFILE：默认为None，这是Oracle特定的设置。用于TBLSPACE的数据文件的名称。如果未提供，则Django将使用。`TBLSPACE + '.dbf'`
      - DATAFILE_TMP：默认为None，Oracle特定的设置。用于TBLSPACE_TMP的数据文件的名称。如果未提供，则Django将使用。`TBLSPACE_TMP + '.dbf'`
      - DATAFILE_MAXSIZE：默认为500M，Oracle特定的设置。允许DATAFILE增大到的最大大小。
      - DATAFILE_TMP_MAXSIZE：默认为500M，Oracle特定的设置。DATAFILE_TMP允许增加到的最大大小。
      - DATAFILE_SIZE：默认为50M，Oracle特定的设置。DATAFILE的初始大小。
      - DATAFILE_TMP_SIZE：默认为50M，Oracle特定的设置。DATAFILE_TMP的初始大小。
      - DATAFILE_EXTSIZE：默认为25M，Oracle特定的设置。需要更多空间时，DATAFILE_TMP的扩展量。

    其他的配置：

    - ATOMIC_REQUESTS：默认为False，当设置为True时将每个视图包装在该数据库的事务中
    - AUTOCOMMIT:默认为True，当设置为False时警用Django的事务管理，可以自己编写事务管理机制
    - CONN_MAX_AGE：数据库连接的生存期，以秒为单位。用于`0`在每个请求结束时关闭数据库连接-Django的历史行为-并 `None`用于无限的持久连接。
    - TIME_ZONE：默认为None，用一个字符串表示存储在此数据库中的时区


​    

### 数据库路由器列表

`DATABASE_ROUTERS`

作用：执行数据库查询时将用来确定要使用哪个数据库的路由器列表。

​    

### 阈值检查

`DATA_UPLOAD_MAX_NUMBER_FIELDS`

作用：调用SuspiciousOperation检查GET或POST接受的最大值，当设为None时禁用检查

​    

### 显示日期的默认格式

`DATE_FORMAT`

作用：在任何地方显示日期字段的默认格式。

​    

### 密码强度列表

`AUTH_PASSWORD_VALIDATORS`

作用：用于检查用户密码强度的验证器列表

​    

### 语言

`LANGUAGE_CODE`

作用：项目语言，默认为‘en-us’

​    

### 时区

`TIME_ZONE`

作用：一个字符串表达的时区默认为'UTC'

​    

### 翻译系统

`USE_I18N`

作用：指定是否启用Django的翻译系统，默认为True

​    

### 本地化

`USE_L10N`

作用：指定默认情况下是否启用数据本地化格式，默认为True



### 时区    

`USE_TZ`

作用：指定日期时间默认情况下是否支持时区

​    

### 静态文件夹的路径

`STATIC_URL`

作用：引用位于静态文件时使用的URL

​    



### 静态文件的绝对路径

`STATIC_ROOT`

作用：在部署时收集静态文件的绝对路径

​    