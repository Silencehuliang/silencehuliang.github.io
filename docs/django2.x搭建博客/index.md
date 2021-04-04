# Django2.x搭建博客


**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 简介

学完Django2.x可以搭建一个个人博客练练手

## 教程

### 创建项目

通过pycharm创建博客项目与虚拟环境

![](http://tva3.sinaimg.cn/large/00729CCqgy1g96ltpvg1pj30ln0et75l.jpg)

### 修改相关设置

#### 允许任何域名

在开发和测试的时候可以将这里填为*，后期部署上线后修改为指定域名即可 

```python
ALLOWED_HOSTS = ['*']
```

#### 注册应用

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册应用，当使用pycharm创建时会帮我们自动创建
    'post.apps.PostConfig',  
]
```

#### 配置模版 

```python
TEMPLATES = [
    {	
    	# 选择我们的模板引擎，刚刚用pycharm创建时已选择django自带的模板引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 注册我们模版文件夹的位置，刚刚用pycharm创建时已将名字定为`templates`
        'DIRS': [os.path.join(BASE_DIR, 'templates')] 
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

 注册完后，在项目根目录中（即manage.py所在的目录）创建templates文件夹，使用pycharm创建项目会自动帮我们创建 

#### 配置数据库

```python
DATABASES = {
    'default': {
        # 选择使用的数据库类型，这里为mysql
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名称
        'NAME': 'djangoblog', 
        # 数据库用户名
        'USER': 'root',  
        # 数据库密码
        'PASSWORD': '123456', 
        # 数据库ip，留空默认为localhost
        'HOST': '', 
        # 数据库端口，留空默认为3306
        'PORT': '3306', 
    }
}

```

#### 创建mysql数据库

在注册完数据库后创建mysql数据库

```mysql
>>> mysql -uroot -p
mysql> create database djangoblog charset=utf8;
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| blog               | 
| djangoblog         |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
6 rows in set (0.01 sec)
```

#### 数据库迁移

接下来进行数据库迁移，并创建django-admin管理员

按照之前的文章：[Django2.0正确配置MySQL](http://49.235.231.121/2019/记django2.x配置mysql/)，配置好MySQL数据库

接下来再进行数据库迁移	

```python
 (DjangoBlogEnv) hls-MacBook-Pro:DjangoBlog hl$ python manage.py makemigrations
 No changes detected
 (DjangoBlogEnv) hls-MacBook-Pro:DjangoBlog hl$ python manage.py migrate
 Operations to perform:
   Apply all migrations: admin, auth, contenttypes, sessions
 Running migrations:
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   Applying admin.0001_initial... OK
   Applying admin.0002_logentry_remove_auto_add... OK
   Applying admin.0003_logentry_add_action_flag_choices... OK
   Applying contenttypes.0002_remove_content_type_name... OK
   Applying auth.0002_alter_permission_name_max_length... OK
   Applying auth.0003_alter_user_email_max_length... OK
   Applying auth.0004_alter_user_username_opts... OK
   Applying auth.0005_alter_user_last_login_null... OK
   Applying auth.0006_require_contenttypes_0002... OK
   Applying auth.0007_alter_validators_add_error_messages... OK
   Applying auth.0008_alter_user_username_max_length... OK
   Applying auth.0009_alter_user_last_name_max_length... OK
   Applying auth.0010_alter_group_name_max_length... OK
   Applying auth.0011_update_proxy_permissions... OK
   Applying sessions.0001_initial... OK
```

 出现Applying sessions.0001_initial... OK 代表mysql数据库已配置完成，接下来创建django-admin管理员 

```python
(DjangoBlogEnv) hls-MacBook-Pro:DjangoBlog hl$ python manage.py createsuperuser
用户名 (leave blank to use 'hl'): silencehl
电子邮件地址: silencehuliang@163.com
Password: 
Password (again): 
密码跟 用户名 太相似了。
密码长度太短。密码必须包含至少 8 个字符。
这个密码太常见了。
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

出现Superuser created successfully.这一阶段数据库配置已完成，这里产生的数据库是Django自带的一些库 

#### 其他设置

- 区域语言设置，防止admin界面乱码 

  ```python
  # 设置语言为中文
  LANGUAGE_CODE = 'zh-hans' 
  
  # 设置时区为上海
  TIME_ZONE = 'Asia/Shanghai'
  ```

- 静态文件夹与多媒体文件夹设置

  ```python
  # 设置静态文件目录和名称
  STATIC_URL = '/static/'
  
  # 设置静态文件夹目录的路径
  STATICFILES_DIRS = (
      os.path.join(BASE_DIR, 'static'),
  )
  
  # 设置多媒体文件目录和名称
  MEDIA_URL = '/media/'
  # 设置多媒体文件目录的路径
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```

   在settings.py里设置完毕后，我们在项目中也创建这两个文件在，在项目根目录中创建static与media这两个文件夹 

#### 配置pycharm运行参数

  ![](http://tva4.sinaimg.cn/large/00729CCqgy1g96lui0oprj30ck07umx4.jpg)

  ![](http://tvax3.sinaimg.cn/large/00729CCqgy1g96luuhzosj30tx0iy3zp.jpg)

  配置完成后点击pycharm中的运行按钮，在浏览器中输入127.0.0.1:8000访问，出现小火箭升空表示Django安装成功， 访问Django-admin界面， 在浏览器中输入`127.0.0.1:8000/admin`，看到Django管理，需要输入用户名密码，输入用户名密码后可以跳转到Django管理页面表示Django-admin设置成功

### 数据库表分析

#### 文章表

| 字段        | 类型                 | 备注         |
| ----------- | -------------------- | ------------ |
| id          | PrimaryKey           | 主键         |
| title       | CharField            | 标题         |
| create_time | DateTimeField        | 创建时间     |
| views       | PositiveIntegerField | 阅读数       |
| summary     | TextField            | 摘要         |
| content     | TextField            | 内容         |
| category_id | ForeignKey           | 外键，分类id |
| tag_id      | ManyToManyField      | 外键，标签id |

#### 分类表

| 字段 | 类型       | 备注   |
| ---- | ---------- | ------ |
| id   | PrimaryKey | 主键   |
| name | CharField  | 分类名 |

#### 标签表

| 字段 | 类型       | 备注   |
| ---- | ---------- | ------ |
| id   | PrimaryKey | 主键   |
| name | CharField  | 标签名 |

#### 用户表

| 字段     | 类型       | 备注   |
| -------- | ---------- | ------ |
| id       | PrimaryKey | 主键   |
| name     | CharField  | 用户名 |
| password | CharField  | 密码   |

#### 评论表

| 字段        | 类型                 | 备注           |
| ----------- | -------------------- | -------------- |
| id          | PrimaryKey           | 主键           |
| user_id     | ManyToManyField      | 外键，用户名id |
| blog_id     | ManyToManyField      | 外键，博客id   |
| create_time | DateTimeField        | 创建时间       |
| content     | TextField            | 评论内容       |
| Parent_id   | PositiveIntegerField | 父评论id       |

### 编写模型类代码

根据数据库设计表格完成模型类代码

```python
# DjangoBlog/post/models.py

from django.db import models

class Category(models.Model):
		"""分类"""
    name = models.CharField('分类', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tags(models.Model):
		"""标签"""
    name = models.CharField('标签', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
		"""博客"""
    title = models.CharField('标题', max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    views = models.PositiveIntegerField('阅读数', default=0)
    summary = models.TextField('摘要')
    content = models.TextField('内容')
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类')
    tag_id = models.ManyToManyField(Tags, verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title


class User(models.Model):
		"""用户"""
    name = models.CharField('用户名', max_length=100)
    password = models.CharField('密码', max_length=100)

    class Meta:
        verbose_name = '用户名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
		"""评论"""
    user = models.ManyToManyField(User, verbose_name='用户')
    article = models.ManyToManyField(Article, verbose_name='博客')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    content = models.TextField('内容')
    Parent_id = models.PositiveIntegerField('父评论id')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
```

数据库迁移

```python
(DjangoBlogEnv) hls-MacBook-Pro:DjangoBlog hl$ python manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Article
    - Create model Category
    - Create model Tags
    - Create model User
    - Create model Comment
    - Add field category_id to article
    - Add field tag_id to article
(DjangoBlogEnv) hls-MacBook-Pro:DjangoBlog hl$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
```

### 用django-admin管理

数据库迁移完成会在post应用下生成一个迁移的文件，接下来在django-admin中注册模型，便于我们用django-admin管理

```python
/post/admin.py

from django.contrib import admin
from .models import Article, Category, Tags, User, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
		# 在后台显示的字段
    list_display = ('id', 'title', 'create_time', 'category_id', 'views')
    # 分页的个数
    list_per_page = 10
    # 按时间倒序排序
    ordering = ('-create_time',)
    # 点击修改的字段
    list_display_links = ('id', 'title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id',  'content',  'create_time')
```

登陆Django管理后台，查看模型是否可以被管理，尝试点击添加与修改，没问题就说明注册成功



### 集成Markdown

很多人喜欢用markdown格式写博客，我们可以通过集成Django-mdeditor 来实现这个功能

 1.安装django-mdeditor 

```python
pip install django-mdeditor
```

2.在apps中注册

```python
INSTALLED_APPS = [
...
'mdeditor',
]
```

3.在media下创建editor文件夹

```bash
cd media
mkdir editor
```

4.集成到路由中

```python
/blog/urls.py

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
...

urlpatterns = [
...
url(r'mdeditor/', include('mdeditor.urls'))
]

if settings.DEBUG:
# static files (images, css, javascript, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

5.集成到models中

```python
from mdeditor.fields import MDTextField
class Article(models.Model):
...
    content = MDTextField()
...
```

再次进入admin，选择文章修改就可以看到集成的markdown编辑器了



### 实现视图

首先找到一套你喜欢的模版，将模版下载下来，html部分放入templates中，其他静态文件放入static中

将重复出现的部分提取出来，这个根据自己的模版抽取，每个都不相同，静态文件加载

如果一次没有提取好，可以慢慢一点点的抽取，对于一个后端程序员来说这个是一个慢工出细活的过程.可以写一个简单的视图，然后开着Django一边抽取一遍调试



接下来实现首页试图

首先在urls.py中配置路由

```python
DjangoBlog/u rls.py
...
from blog import views

urlpatterns = [
 	...
  path('', views.index, name='index')
]
```

这里path里第一个参数为访问的url，匹配采用正则表达式，第二个参数为视图函数，第三个为取的名字

接下来在blog应用的views.py中编写视图函数

```python
blog/views.py
...
def index(request):
    return render(request, 'index.html')
```

这样当我们重新访问127.0.0.1:8000时，我们修改的前端代码就被加载了



接下来我们实现将分类加载,将index视图修改为一下代码

```python
blog/views.py
...
from .models import Category

# 从models里导入Category类
def index(request):
    categorys = Category.objects.all()
    # 把查询出来的分类封装到上下文里
    context = {
        'categorys': categorys,
    }
    print(context)
    return render(request, 'index.html', context)
```



在前端代码中渲染，我们找到base.html,将ul标签中的除首页以外的代码改为一下代码

```django
<header class="header-navigation" id="header">
    <nav>
        <div class="logo"><a href="/">胡亮个人博客</a></div>
        <h2 id="mnavh"><span class="navicon"></span></h2>
        <ul id="starlist">
            <li><a href="index.html">首页</a></li>
  					+++
						+++
        </ul>
    </nav>
</header>
```

+号中间的内容为          

**{% for category in categorys %}**

**{% endfor %}**

这样分类栏就加载出来了，如果没有数据可以通过admin添加数据


