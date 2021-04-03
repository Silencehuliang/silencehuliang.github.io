# Django初体验


**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 简介

在Django2.0以后，Django已经不支持python2.7，所以我们需要一个python3的系统环境，这里一python3.6为例

## 安装Django

### 三种方式安装

#### pip安装

- 一般情况下安装python后会帮你安装好pip，当你没安装时使用这个[链接](https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py)安装,记得更新到最新版本

- 安装并使用virtualenv

- 在创建好并激活的虚拟环境中输入一下命令

  ```python
  $ pip install Django
  ```

#### 通过第三方软件包

管理系统集成的Django

#### 安装开发版本

- 安装好[git](https://git-scm.com/)

- 输入一下命令下载Django

  ```bash
  $ git clone https://github.com/django/django.git
  ```

- 安装并使用virtualenv

- 在创建好并激活的虚拟环境中输入一下命令

  ```python
  $ pip install -e django/
  ```


安装好Django后可以通过一下命令查看当前Django版本

```python
$ python -m django --version
```



## Django初体验

### 安装并使用virtualenv

详细过程见[这个链接](http://49.235.231.121/2019/python搭建虚拟环境/)



### 创建Django项目

在项目存放目录打开命令行运行一下命令：

```python
$ django-admin startproject mysite
```

这句话执行过后会在当前目录生成一个名字为mysite的Django项目，目录结构为下

```bash
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

这些目录和文件的作用：

- mysite/目录：存放项目的容器，他的名字不重要可以更换为你喜欢的任何名字
- manage.py：Django项目的启动文件，他可以让你通过各种方式管理Django项目。
- mysite/mysite/目录：项目目录，里面存放项目相关的文件
- mysite/mysite/settings.py：Django项目的配置文件
- mysite/mysite/urls.py：Django项目的url声明文件,他将url对应相关的app的视图
- mysite/mysite/wsgi.py：Django项目wsgi服务器的入口

- 当输入以下命令，并进入浏览器输入：http://127.0.0.1:8000/看到Django启动成功

  ```python
  $ python manage.py runserver
  ```

  这里能启动成功是因为Django自带一个简易的服务器（用纯 Python 写的轻量级的 Web 服务器）。他能帮助我们快速开发。

  

### 创建一个应用

  - 将当前目录切换到manage.py所在的目录，输入下面的命令创建一个应用:

    ```python
    $ python manage.py startapp demo
    ```

    该应用的目录结构大致如下

    ```bash
    demo/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py
    ```

    这些目录和文件的作用：

    - admin.py：管理admin后台相关数据库模型
    - apps.py：该应用的相关配置
    - migrations/文件夹及其内容：数据库迁移相关的文件夹，里面存放着迁移版本，迁移信息等
    - models.py：编写模型类的文件
    - tests.py：用于测试的文件
    - view.py：编写视图的文件

    我们还要在项目配置文件中注册该app，打开settings.py文件，找到INSTALLED_APPS，在列表的最后添加demoapp

    ```python
    mysite/settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # 注册demo
        'demo.apps.DemoConfig'
    ]
    
    ```



### 编写第一个视图

视图在应用的views.py中编写

  ```python
  demo/views.py
  
  from django.http import HttpResponse
  
  def index(request):
  	return HttpResponse("Hello, world!")
  ```

  为了能看到效果我们还需要配置一下url，在demo目录下创建一个urls.py，并输入一下代码

  ```python
  /demo/urls.py
  
  from django.urls import path
  from . import views
  
  urlpatterns = [
  	path("",views.index,name='index'),
  ]
  ```

  更改项目url，通过修改项目urls.py文件修改路由

  ```python
  /mysite/urls.py
  
  from django.contrib import admin
  from django.urls import include, path
  
  urlpatterns = [
      path('demo/', include('demo.urls')),
      path('admin/', admin.site.urls),
  ]
  ```

  这里include是将demo/的路由转发到demo应用的urls.py里。每当 Django 遇到 include时，它会截断与此项匹配的 URL 的部分，并将剩余的字符串发送到 对应urls.py以供进一步处理。

  path有五个参数：route、view、kwargs、name、Pattern，其中route、view是必须传入的参数

  - route：匹配url的准则（类似于正则表达式）。当Django响应一个请求时，他会从urlpatterns的第一项开始，按顺序依次匹配，知道找到匹配的项
  - view：目标视图函数。当route找到匹配的项后，会调用当前的视图函数，并传入一个HttpRequest对象作为第一个参数，route中的参数一关键字参数的形式传入
  - kwargs：关键字参数。任意个关键字参数可以作为一个字典传递给目标视图函数。
  - name：为url取的名字。他可以使Django在任意地方引用他
  - Pattern：匹配模式

现在可以启动Django程序来看是否正常工作



### 数据库

#### 创建数据库

进入mysql并创建一个test数据库，字符设置为utf8

```mysql
$ mysql -uroot -p
mysql> create database test charset=utf8;
Query OK, 1 row affected (0.00 sec)
```

#### 数据库配置

首先我们需要配置mysite/setting.py中的数据库DATABASES选项，Django默认是sqlite数据库，如果个人项目不大的情况下可以使用这个，也可以使用自己熟悉的数据库，Django不仅支持sqlite，postgresql，mysql，或oracle，还支持很多有第三方插件的数据库，我使用mysql数据库

```python
/mysite/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名
        'NAME': 'test', 
        # 用户名
        'USER': 'root', 
        # 密码
        'PASSWORD': 'mysql'
        # 主机,默认为localhost
        'HOST': ''
        # 端口号，默认为3306
        'PORT': ''
    }
}
```



#### 数据库迁移

因为Django自带应用已经为我们编写了一些数据模型，即时我们不编写任何模型也可以直接使用数据库迁移命令进行迁移

```python
$ python manage.py migrate
```

会看到初始化了很多用户、权限相关的表

创建一个管理员账号，依次输入用户名、邮箱、密码、确认密码，建议密码设置复杂点

```python
$ python manage.py createsuperuser
用户名 (leave blank to use '02'): admin
电子邮件地址: 1@gmail.com
Password:
Password (again):
密码跟 用户名 太相似了。
密码长度太短。密码必须包含至少 8 个字符。
这个密码太常见了。
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```

接下来启动项目，并在浏览器中输入http://127.0.0.1:8000/admin，进入后台管理界面

![](https://tvax2.sinaimg.cn/large/006lmzsGgy1gav1o59elyj31h90s7dgw.jpg)

输入账号密码，点击登录即可

![](https://tvax4.sinaimg.cn/large/006lmzsGgy1gav1on3qmaj31h70s9js7.jpg)

数据库迁移，需要三步

- 编写models.py文件，改变模型。

- 运行 python manage.py makemigrations为模型的改变生成迁移文件。

- 运行 python manage.py migrate 来应用数据库迁移。

  

#### 创建一个图书模型

在demo应用下创建一个图书模型

```python
/demo/models.py

from django.db import models

class Books(models.Model):
    # 书名
    book_name = models.CharField(max_length=200)
    # 作者
    author = models.CharField(max_length=50)
```

建立的模型有两个字段，书名和作者，使用了字符类型，增加了长度限制（**注意在使用CharField时必须要添加max_length限制**）

创建迁移模型并生成迁移文件

```python
$ python manage.py makemigrations demo
Migrations for 'demo':
  demo\migrations\0001_initial.py
    - Create model Books
```

会出现创建了Books这个模型，在demo应用的migrations文件夹下会多一个0001_initila.py的迁移文件，可以使用python manage.py sqlmigrate demo 0001可以查看这次数据库迁移的操作与具体的SQL语句

```python
$ python manage.py sqlmigrate demo 0001
BEGIN;
--
-- Create model Books
--
CREATE TABLE `demo_books` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `book_name` varchar(200) NOT NULL, `auhtor` varchar(50) NOT NULL);
COMMIT;
```

需要注意一下几点：

- 输出的内容与使用的数据库有关。
- 数据库的表名默认是“应用名_模型名的小写”，也可以自定义表名。
- 主键会默认自动创建，也可以自定义主键。
- Django会为使用的数据库定制相关SQL语句，例如主键：integer AUTO_INCREMENT NOT NULL PRIMARY KEY，varchar：NOT NULL
- sqlmigrate命令并没有真正执行迁移命令，他只是将迁移命令执行的流程输出到屏幕上，供你查看

执行check命令对项目做检查

```python
$ python manage.py check
System check identified no issues (0 silenced).
```

没有问题后执行迁移命令

```python
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, demo, sessions
Running migrations:
  Applying demo.0001_initial... OK
```

看到以上内容即完成了数据库迁移

通过Python命令行尝试

```python
$ python manage.py shell
>>> from demo.models import Books
>>> ggzh = Books(book_name="硅谷之火",author="迈克尔.斯韦因")
>>> ggzh.save()
>>> ggzh.id
1
>>> ggzh.book_name
'硅谷之火'
>>> ggzh.author
'迈克尔.斯韦因'
>>> Books.objects.all()
<QuerySet [<Books: Books object (1)>]>
```

这里我们看到<QuerySet [<Books: Books object (1)>]>这个并不能让我们知道这个对象的细节，通过修改Books模型来修复这个问题

```python
/demo/models.py

class Books(models.Model):
    # 书名
    book_name = models.CharField(max_length=200)
    # 作者
    author = models.CharField(max_length=50)
    
	def __str__(self):
        return self.book_name

```

修改完成后重新进入交互终端，再次查询就可以显示书名了，这里可以自己定义想显示的字段或内容

```python
$ python manage.py shell
>>> from demo.models import Books
>>> Books.objects.all()
<QuerySet [<Books: 硅谷之火>]>
```

再添加一本书，聚合函数

```python
>>> qbsz = Books(book_name="史蒂夫*乔布斯传",author="沃尔特·艾萨克森")
>>> qbsz.save()
>>> Books.objects.all()
<QuerySet [<Books: 硅谷之火>, <Books: 史蒂夫*乔布斯传>]>
>>> Books.objects.count()
2
>>> Books.objects.filter(book_name="硅谷之火")
<QuerySet [<Books: 硅谷之火>]>
```

接下来我们将Books模型添加到admin管理，通过register方法，将Books交给admin管理

```python
/demo/admin

from django.contrib import admin

from .models import Books

admin.site.register(Books)
```

重新运行项目，在地址栏输入：http://127.0.0.1:8000/admin/，输入账号密码登录即可查看到这个模型

![](https://tva4.sinaimg.cn/large/006lmzsGgy1gav1r45uowj31h70s9wfe.jpg)

点进去可以查看该模型的数据，右上角可以添加，动作可以删除，点图书名可以看到更多细节

![后台管理图书](https://tvax3.sinaimg.cn/large/006lmzsGgy1gav1rig51bj31hb0s83zk.jpg)

### 视图与模板

在models.py中添加一个图书模型

```python
/demo/models.py

from django.db import models


class Books(models.Model):
    # 书名
    name = models.CharField('书名', max_length=200)
    # 作者
    author = models.CharField('作者', max_length=50)
    publish_house = models.CharField('出版社', max_length=50)
    publish_date = models.CharField('出版日期', max_length=50)
    price = models.IntegerField('价格')
    synopsis = models.TextField('简介')

    def __str__(self):
        return self.name
```

在admin.py中注册Books

迁移数据库

在Django后台中添加图书数据

在应用的views.py中编写一个展示图书的视图

```python
/demo/views.py

from django.http import HttpResponse
from .models import Books


def book_list(request):
    book_list = Books.objects.all()
    books = {book.name : book.id for book in book_list}
    return render(request, 'index.html', context={'books': books})
```

通过模板渲染

在templates目录下新建一个index.html文件

```
/tempaltes/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<div>图书管理系统：</div>
<ul>
    {% for key,value in books.items  %}
        <li><a href="{% url 'detail' value %}/">{{ key }}</a> </li>
    {% endfor %}
</ul>
</body>
</html>
```

在项目的urls.py文件中添加一个关于图书的路由

```python
/mysite/urls.py

from django.contrib import admin
from django.urls import path

from demo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('demo.urls')),
]
```

在demo目录中新建一个urls.py文件，并添加一个路由

```python
/demo/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list, name='index'),
]

```


启动项目，访问：http://127.0.0.1:8000/book/

图书列表页完成了，接下来编写图书详情页

在demo项目中的urls.py文件中添加一个详情页的路由

```python
/demo/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list, name='index'),
    path('<int:id>/', views.detail, name='detail'),
]
```

在demo项目中的views.py文件中编写详情页相关视图函数

```python
/demo/views.py

def detail(request, id):
    book = Books.objects.filter(id=id).all()[0]
    content = {
        "name": book.name,
        "author": book.author,
        'publish_house': book.publish_house,
        'publish_date': book.publish_date,
        'price': book.price,
        'synopsis': book.synopsis
    }
    return render(request, 'detail.html', context=content)
```

在templates文件夹里新建一个detail.html文件,并写入一下代码

```django
/templates/detail.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table>
    <tr>
        <td>书名</td>
        <td>作者</td>
        <td>出版社</td>
        <td>出版日期</td>
        <td>价格</td>
        <td>简介</td>
    </tr>
    <tr>
        <td>{{ name }}</td>
        <td>{{ author }}</td>
        <td>{{ publish_house }}</td>
        <td>{{ publish_date }}</td>
        <td>{{ price }}</td>
        <td>{{ synopsis }}</td>
    </tr>
</table>

</body>
</html>
```

启动项目，访问：http://127.0.0.1:8000/book/，点击其中一个图书就可以看到详情页，或者直接选择一个id访问详情页，这时候就会出现一个问题，当访问一个不存在的id时就会出错，我们需要定制一下错误页面，修改detail视图函数。

```python
/demo/views.py
from django.http import Http404
...
def detail(request, id):
    books = Books.objects.filter(id=id).all()
    if len(books):
        book = books[0]
        content = {
            "name": book.name,
            "author": book.author,
            'publish_house': book.publish_house,
            'publish_date': book.publish_date,
            'price': book.price,
            'synopsis': book.synopsis
        }
        return render(request, 'detail.html', context=content)
    else:
        raise Http404("图书不存在")
```

这里调用的是Django自带的404错误页面，我们需要返回错误说明






