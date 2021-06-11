# Python学习之路-Flask项目:开发准备


## 前言

前面几篇学习了`Flask`的基础知识，从今天开始开发一个个人博客项目来练练手。

## 项目分析

- 关于个人博客的Web项目，主要为自己提供一个记录与技术输出的平台。
- 以个人编写或者转载优秀的文章作为博文的主要来源
- 基于 Flask 框架，以 **前后端不分离** 的形式实现具体业务逻辑

### 技术实现

- 基于`Python 3.7.7` + `Flask`框架实现
- 数据存储使用`Redis` + `MySQL` 实现
- 第三方扩展：七牛云(文件存储平台)
- 布署：基于macOS 10.15.4系统，使用 Gunicorn + Nginx 进行布署

### 功能模块

- 博客模块
  - 首页博客列表
  - 博客详情
- 关于模块
  - 个人信息展示
- 联系模块
  - 联系我功能
- 后台管理
  - 博文的管理
  - 访问数据统计

### 具体需求

1. 首页
   - 根据近期文章列表展示
   - 翻页加载更多数据
   - 点击新窗口跳转到文章详情页
   - 顶部显示博客各大版块
   - 右侧显示最新文章、归档、分类、标签云与RSS订阅相关信息
2. 文章详情
   - 文章内容 html 数据展示
   - 可以评论该文章
   - 右侧显示文章目录、最新文章、归档、分类、标签云与RSS订阅
3. 关于页
   - 展示作者相关信息
4. 联系页
   - 填写相关信息提供联系作者功能
5. 后台-登录
   - 提供后台登录页面
6. 后台-用户统计
   - 登录到后台界面之后展示用户统计界面
   - 显示各类用户访问数据
   - 展示当前月访问新增人数
   - 展示当前日访问新增人数
7. 后台-发布文章
   - 提供`markdown`编辑器进行文章实时预览
   - 发布文章
   - 草稿文章
8. 文章信息展示
   - 进入默认展示所有文章数据
   - 可以根据文章标题搜索文章
9. 文章分类管理
   - 展示所有分类列表
   - 可以添加/修改分类

## 项目框架搭建

### 创建项目

- 新建项目，虚拟环境选择python3版本，创建 `manage.py` 文件

  ```python
  from flask import Flask

  app = Flask(__name__)

  @app.route('/')
  def hello_world():
      return 'Hello World!'

  if __name__ == '__main__':
      app.run()
  ```

### 使用 GIT 管理源代码

git相关内容可以查看之前的[相关文章](https://learnku.com/articles/56481)

#### 本地提交

- 初始化`git`

  ```bash
  Desktop % cd flaskblog 
  flaskblog % git init
  Initialized empty Git repository in /Users/huliang/Desktop/flaskblog/.git/
  ```
  
- 配置当前项目`git`提交信息(可省略此步，如不配置则使用全局配置)

  ```bash
  flaskblog % git config user.email xxx@xxx.com
  flaskblog % git config user.name xxxx
	```

- 添加忽略文件

  ```bash
  flaskblog % touch .gitignore
  ```

- 设置忽略文件内容(后续根据需要再添加)

  ```bash
  .idea
  *.py[cod]
  ```

- 添加所有文件到暂存区

  ```bash
  flaskblog % git add .
  ```

- 提交到本地仓库并填写注释

  ```bash
  flaskblog % git commit -m'初次提交'  
  ```

#### 远程提交

使用`GitHub`：https://github.com/ 作为在线 git 源代码仓库

- 在GitHub上创建名为flaskblog的仓库

- 创建完成后将本地项目提交至仓库中

  ```bash
  flaskblog % cd flaskblog
  flaskblog % git remote add origin xxx/flaskblog.git
  flaskblog % git push -u origin master
  ```

### 项目基本配置

#### Config类

先在当前类中定义配置的类，并从中加载配置

```python
...
app = Flask(__name__)

class Config(object):
    """工程配置信息"""
    DEBUG = True


app.config.from_object(Config)
...
```

运行测试

#### SQLAlchemy

- 导入数据库扩展，并在配置中填写相关配置

  ```python
  from flask_sqlalchemy import SQLAlchemy

  ...

  class Config(object):
      """工程配置信息"""
      DEBUG = True
      # 数据库的配置信息
      SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flaskblog"
      SQLALCHEMY_TRACK_MODIFICATIONS = False

  app.config.from_object(Config)
  db = SQLAlchemy(app)
  ```

- 在终端创建数据库

  ```bash
  mysql> create database flaskblog charset utf8;
  ```
  
  运行测试

#### Redis

创建redis存储对象，并在配置中填写相关配置

```python
import redis
...

class Config(object):
    """工程配置信息"""
    ...
    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
```

运行测试

#### CSRF

包含请求体的请求都需要开启CSRF

```python
from flask_wtf.csrf import CSRFProtect
...
app.config.from_object(Config)
...
CSRFProtect(app)
```

CSRFProtect只做验证工作，cookie中的 csrf_token 和表单中的 csrf_token 需要我们自己实现

#### Session

- 利用 flask-session扩展，将 session 数据保存到 Redis 中

  ```python
  from flask_session import Session
  ...

  class Config(object):
      """工程配置信息"""
      SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
      ...
      # flask_session的配置信息
      SESSION_TYPE = "redis" # 指定 session 保存到 redis 中
      SESSION_USE_SIGNER = True # 让 cookie 中的 session_id 被加密签名处理
      SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT) # 使用 redis 的实例
      PERMANENT_SESSION_LIFETIME = 86400 # session 的有效期，单位是秒

  app.config.from_object(Config)
  ...
  Session(app)
  ```

运行测试

#### Flask-Script与数据库迁移扩展

```python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
...
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)
...

if __name__ == '__main__':
    manager.run()
```

运行测试

### 代码抽取

#### 目标

将特定逻辑代码抽取到指定的类中，各司其职，放便后续项目维护

#### 配置文件

- 在与 `manage.py` 同级目录下创建 `config.py` 文件，用作于项目的配置文件

  ```python
  import redis

  class Config(object):
      """工程配置信息"""
      SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"

      DEBUG = True
    
      # 数据库的配置信息
      SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flaskblog"
      SQLALCHEMY_TRACK_MODIFICATIONS = True
    
      # redis配置
      REDIS_HOST = "127.0.0.1"
      REDIS_PORT = 6379
    
      # session 配置
      SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
      SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
      SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
      PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒
  ```

- 在 `manager.py` 中引入 `Config` 类，直接使用

  ```python
  from config import Config

  app = Flask(__name__)

  # 配置
  app.config.from_object(Config)
  ```

  运行测试

#### 业务逻辑独立

在整个项目文件夹中，除了启动文件 `manage.py` 和配置文件 `config.py` 放在根目录，其他具体业务逻辑文件都放在一个单独的文件夹内，与 `manage.py` 同级

- 创建 `blog` Package，与 `manage.py` 同级

- `manage.py` 只做最基本的启动工作，将 `app` 的创建操作移动到 `blog` 的 `__init__.py` 文件中

  ```python
  import redis
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
  from flask_wtf.csrf import CSRFProtect
  from flask_session import Session
  from config import Config

  app = Flask(__name__)

  # 配置
  app.config.from_object(Config)
  # 配置数据库
  db = SQLAlchemy(app)
  # 配置redis
  redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
  # 开启csrf保护
  CSRFProtect(app)
  # 设置session保存位置
  Session(app)
  ```

- `manage.py` 的代码为

  ```python
  from flask_script import Manager
  from flask_migrate import Migrate, MigrateCommand
  from blog import app, db

  # Flask-script
  manager = Manager(app)
  # 数据库迁移
  Migrate(app, db)
  manager.add_command('db', MigrateCommand)

  @app.route('/index')
  def index():
    return 'index'

  
  if __name__ == '__main__':
      manager.run()
  ```
  
  运行测试

#### 项目多种配置

一个web程序在开发阶段可能与生产阶段所需要的配置信息可能不一样，所以为了实现此功能，可以给不同情况创建不同的配置类，比如开发阶段使用的配置类名为 `DevelopementConfig`，生产阶段使用的配置类名为 `ProdutionConfig`，修改 `config.py` 文件的配置文件如下

```python
import redis


class Config(object):
    """工程配置信息"""

    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flaskblog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒


class DevelopementConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    pass
```

接下来思考如何能才更快速的针对不同的布署环境去使用不同的配置

#### 工厂类方法

要在不同环境下去使用不同的配置，那么可以在 `manage.py` 文件中给 `blog` 包传入不同的配置信息，让 ihome 去根据传入指定配置去创建 `app`，所以可以在 `blog` 的 `__init__.py` 文件中添加一个工厂方法，根据传入的配置不同创建其对应的应用实例

- 在 `config.py` 文件中添加以下代码

  ```
  # 定义配置字典
  config = {
      "development": DevelopementConfig,
      "production": ProductionConfig
  }
  ```

- 修改 `blog` 文件夹下 `__init__.py`，添加 `create_app` 的工厂方法

  ```python
  def create_app(config_name):
      """通过传入不同的配置名字，初始化其对应配置的应用实例"""
      pass
  ```

- 修改 `manage.py` 文件中的代码

  ```python
  from blog import create_app, db

  # 创建 app，并传入配置模式：development / production
  app = create_app('development')
  ```

- 将 `__init__.py` 文件中创建 app 实例的方法移动到 `create_app` 方法中

  ```python
  from config import config
  
  # 数据库
  db = SQLAlchemy()
  redis_store = None

  def create_app(config_name):
      """通过传入不同的配置名字，初始化其对应配置的应用实例"""

      app = Flask(__name__)
    
      # 配置
      app.config.from_object(config[config_name])
      # 配置数据库
      db.init_app(app)
      # 配置redis
      global redis_store
      redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
      # 开启csrf保护
      CSRFProtect(app)
      # 设置session保存位置
      Session(app)
    
      return app
  ```

## 日志

### 简介

日志是一种可以追踪某些软件运行时所发生事件的方法。软件开发人员可以向他们的代码中调用日志记录相关的方法来表明发生了某些事情。一个事件可以用一个可包含可选变量数据的消息来描述。此外，事件也有重要性的概念，这个重要性也可以被称为严重性级别（level）

### 作用

通过log的分析，可以方便用户了解系统或软件、应用的运行情况；如果你的应用log足够丰富，也可以分析以往用户的操作行为、类型喜好、地域分布或其他更多信息；如果一个应用的log同时也分了多个级别，那么可以很轻易地分析得到该应用的健康状况，及时发现问题并快速定位、解决问题，补救损失。

简单来讲就是我们通过记录和分析日志可以了解一个系统或软件程序运行情况是否正常，也可以在应用程序出现故障时快速定位问题。不仅在开发中，在运维中日志也很重要

日志的作用可以简单总结为以下几点：程序调试、了解软件程序运行情况，是否正常、软件程序运行故障分析与问题定位、如果应用的日志信息足够详细和丰富，还可以用来做用户行为分析

### 等级

我们先来思考下下面的两个问题：

- 作为开发人员，在开发一个应用程序时需要什么日志信息？在应用程序正式上线后需要什么日志信息？
- 作为应用运维人员，在部署开发环境时需要什么日志信息？在部署生产环境时需要什么日志信息？

在软件开发阶段或部署开发环境时，为了尽可能详细的查看应用程序的运行状态来保证上线后的稳定性，我们可能需要把该应用程序所有的运行日志全部记录下来进行分析，这是非常耗费机器性能的。当应用程序正式发布或在生产环境部署应用程序时，我们通常只需要记录应用程序的异常信息、错误信息等，这样既可以减小服务器的I/O压力，也可以更加方便的进行故障排查。那么，怎样才能在不改动应用程序代码的情况下实现在不同的环境记录不同详细程度的日志呢？这就是日志等级的作用了，我们通过配置文件指定我们需要的日志等级就可以了。不同的应用程序所定义的日志等级可能会有所差别，分的详细点的会包含以下几个等级：

- FATAL/CRITICAL = 重大的，危险的
- ERROR = 错误
- WARNING = 警告
- INFO = 信息
- DEBUG = 调试
- NOTSET = 没有设置

### 字段信息与日志格式

输出一条日志时，日志内容和日志级别是需要开发人员明确指定的。对于而其它字段信息，只需要是否显示在日志中就可以了。

### 功能的实现

Python 自身提供了一个用于记录日志的标准库模块：logging。

#### logging 模块

##### 简介

logging 模块定义的函数和类为应用程序和库的开发实现了一个灵活的事件日志系统。logging 模块是 Python 的一个标准库模块，由标准库模块提供日志记录 API 的关键好处是所有 Python 模块都可以使用这个日志记录功能。

 ##### 日志级别

logging模块默认定义了以下几个日志等级，它允许开发人员自定义其他日志级别，但是这是不被推荐的，尤其是在开发供别人使用的库时，因为这会导致日志级别的混乱。

- DEBUG 最详细的日志信息，典型应用场景是 问题诊断
- INFO 信息详细程度仅次于DEBUG，通常只记录关键节点信息，用于确认一切都是按照我们预期的那样进行工作
- WARNING 当某些不期望的事情发生时记录的信息（如，磁盘可用空间较低），但是此时应用程序还是正常运行的
- ERROR 由于一个更严重的问题导致某些功能不能正常运行时记录的信息
- FATAL/CRITICAL 整个系统即将/完全崩溃

开发应用程序或部署开发环境时，可以使用 DEBUG 或 INFO 级别的日志获取尽可能详细的日志信息来进行开发或部署调试；应用上线或部署生产环境时，应该使用 WARNING 或 ERROR 或 CRITICAL 级别的日志来降低机器的I/O压力和提高获取错误日志信息的效率。

{{< admonition info "提示" true >}}

日志级别的指定通常都是在应用程序的配置文件中进行指定的。

{{< /admonition >}}

##### 使用方式介绍

- loggers 提供应用程序代码直接使用的接口
- handlers 用于将日志记录发送到指定的目的位置
- filters 提供更细粒度的日志过滤功能，用于决定哪些日志记录将会被输出（其它的日志记录将会被忽略）
- formatters 用于控制日志信息的最终输出格式

  ```python
  # 设置日志的记录等级
  logging.basicConfig(level=logging.DEBUG) # 调试debug级
  # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
  file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
  # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
  formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
  # 为刚创建的日志记录器设置日志记录格式
  file_log_handler.setFormatter(formatter)
  # 为全局的日志工具对象（flask app使用的）添加日志记录器
  logging.getLogger().addHandler(file_log_handler)
  ```

##### 函数记录

###### 最简单的日志输出

先来试着分别输出一条不同日志级别的日志记录：

```python
import logging

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
```

也可以这样写：

```python
logging.log(logging.DEBUG, "This is a debug log.")
logging.log(logging.INFO, "This is a info log.")
logging.log(logging.WARNING, "This is a warning log.")
logging.log(logging.ERROR, "This is a error log.")
logging.log(logging.CRITICAL, "This is a critical log.")
```

###### 修改配置改变输出内容

```python
logging.basicConfig(level=logging.DEBUG)
```

{{< admonition warning "切记" true >}}

设置 `Configurations` 中的 **Working directory** 为当前项目

{{< /admonition >}}

### 集成日志到当前项目

- 在 `config.py` 文件中在不同的环境的配置下添加日志级别

  ```python
  class Config(object):
      ...

      # 默认日志等级
      LOG_LEVEL = logging.DEBUG

  class ProductionConfig(Config):
      """生产模式下的配置"""
      LOG_LEVEL = logging.ERROR
  ```

- 在 `blog` 目录下的 `init.py` 文件中添加日志配置的相关方法

  ```python
  def setup_log(config_name):
      """配置日志"""

      # 设置日志的记录等级
      logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
      # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
      file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
      # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
      formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
      # 为刚创建的日志记录器设置日志记录格式
      file_log_handler.setFormatter(formatter)
      # 为全局的日志工具对象（flask app使用的）添加日志记录器
      logging.getLogger().addHandler(file_log_handler)
  ```

- 在 `create_app` 方法中调用上一步创建的方法，并传入 `config_name`

  ```python
  def create_app(config_name):
      ...

      # 配置项目日志
      setup_log(config_name)
      app = Flask(__name__)
      ...
  ```

- 在项目根目录下创建日志目录文件夹 `logs`

  {{< admonition info "提示" true >}}

  运行项目，当前项目日志已输出到 `logs` 的目录下自动创建的 log 文件中

  {{< /admonition >}}

- 在 logs 文件夹下创建 .gitkeep 文件，以便能将 logs 文件夹添加到远程仓库，并在 .gitignore 文件中添加忽略提交生成的日志文件

```bash
logs/log*
```

在 Flask框架 中，其自己对 Python 的 logging 进行了封装，在 Flask 应用程序中，可以以如下方式进行输出 log:

```bash
current_app.logger.debug('debug')
current_app.logger.error('error')
```

## 蓝图

项目的蓝图模块可以按以下方式来分：

- 按功能模块来分，比如：文章模块、关于模块
- 按接口版本来分，某个版本的接口放一个文件夹下面

因为本项目是前后端不分离的项目，界面数据大部分都使用模板的形式进行渲染，很少涉及到通过接口的形式返回数据，所以本项目使用按功能模块来划分蓝图。

- 在 `blog` 目录下创建 `modules` Package，modules 存放当前项目所有的模块

- 在 `modules` 文件夹下创建 `index` 文件夹， 并在此文件夹下创建 `views.py` 文件，将 `manage.py` 中定义的路由拷贝至该文件中

  ```python
  @app.route('/index')
  def index():
      return 'index'
  ```

  暂时忽略报错，此处的index文件夹就是一个模块

- 到这一步 `manage.py` 中内容基本上都抽取完成，剩余内容如下：

  ```python
  from flask_script import Manager
  from flask_migrate import Migrate, MigrateCommand
  from info import create_app, db

  app = create_app('development')

  # 添加扩展命令行
  manager = Manager(app)

  # 数据库迁移
  Migrate(app, db)
  manager.add_command('db', MigrateCommand)

  if __name__ == '__main__':
      manager.run()
  ```

- 在 `index` 文件夹中的 `__init__.py`创建其自已的蓝图

  ```python
  from flask import Blueprint
  
  index_blu = Blueprint("index", __name__)
  
  from . import views
  ```

- 在 `views.py` 中导入蓝图，并使用该蓝图注册路由

  ```python
  from . import index_blu

  @index_blu.route('/index')
  def index():
      return 'index'
  ```
  
- 将上一步创建出来的蓝图注册到 app 中

  ```python
  def create_app(config_name):
      ...
  
      # 注册蓝图
      from info.modules.index import index_blu
      app.register_blueprint(index_blu)
  
      return app
  ```

  运行测试

## 数据库表

### 分析

根据需求分析需要4个表格：

- 文章(Post)：

  |        字段        |      类型       |                条件                |     备注     |
  | :----------------: | :-------------: | :--------------------------------: | :----------: |
  |       title        |    CharField    |           max_length=100           |     标题     |
  |        body        |    TextField    |                 -                  |     正文     |
  |    created_time    |  DateTimeField  |                 -                  |   创建时间   |
  | last_modified_time |  DateTimeField  |                 -                  | 最后修改时间 |
  |      abstract      |    CharField    |     max_length=200, blank=True     |     摘要     |
  |      category      |   ForeignKey    | Category, on_delete=models.CASCADE |     分类     |
  |        tags        | ManyToManyField |          Tag, blank=True           |     标签     |
  |       author       |   ForeignKey    |   User, on_delete=models.CASCADE   |     作者     |

  

- 分类(Category)：

  | 字段 |   类型    |      条件      |  备注  |
  | :--: | :-------: | :------------: | :----: |
  | name | CharField | max_length=100 | 分类名 |

  

- 标签(Tag)：

  | 字段 |   类型    |      条件      |  备注  |
  | :--: | :-------: | :------------: | :----: |
  | name | CharField | max_length=100 | 标签名 |

  

- 用户(Info)：

  |   字段   |   类型    |      条件      |  备注  |
  | :------: | :-------: | :------------: | :----: |
  |   name   | CharField | max_length=50  | 作者名 |
  | homepage | CharField | max_length=100 |  主页  |

### 数据库表迁移

- 确认当前配置的数据库是否存在

  ```bash
  mysql> use flaskblog;
  ```
  
- 将 `constants.py` 和 `models.py` 文件拷贝到项目的 `blog` 目录下

  {{< admonition info "提示" true >}}

  constants.py 是当前项目中要使用的一些常量，预先定义好的，models.py 文件中需要使用到该文件中的一些常量

  {{< /admonition >}}

- 并在 `manage.py` 中导入 `models`

  ```python
  form info import models
  ```
  
  {{< admonition info "提示" true >}}
  
  在迁移的时候以便能读取到对应模型
  
  {{< /admonition >}}

- 执行数据库迁移

  ```bash
  flaskblog % python manage.py db init
  flaskblog % python manage.py db migrate -m"initial"
  flaskblog % python manage.py db upgrade
  ```

- 查看数据库表是否创建完成

  ```bash
  mysql> show tables;
  ```

- 执行导入初始分类的 SQL 语句

  ```bash
  mysql> source info_info_category.sql
  ```
  
  {{< admonition info "提示" true >}}
  
  生成的迁移文件不需要提交到 git 保存，所以需要在 .gitignore 文件中添加以下内容以便忽略迁移所生成的系列文件
  
  {{< /admonition >}}
  
  ```bash
  migrations
  ```

### 测试数据的添加

- 先添加分类测试数据

```bash
mysql> source 路径/flaskblog_category.sql
```

- 再添加新闻测试数据

```bash
mysql> source 路径/flaskblog_blog.sql
```

## 静态文件导入

- 在项目 `blog` 目录下创建 `static` 文件夹

- 将前端人员开发好的 `blog` 和 `admin` 两个静态文件夹拖入到项目
  - `news`文件夹内代表新闻前台页面
  - `admin`文件夹内代表新闻的后台页面

- 运行项目，使用浏览器访问：http://127.0.0.1:5000/static/blog/index.html 查看效果

## 注册根路由

### 创建模板目录

在 **static** 同级目录创建 **templates** 文件夹，并在此目录下创建 **post** 文件夹用于存放新闻前台模板文件。(此步可以省略，只是在 Pycharm 中标识该目录为模板目录)设置 **templates** 目录成模板目录属性，操作方式：右键点击 **templates** 目录，选择 `Mark Directory as` -> `Template Folder`如果没有设置模板语言，会弹出是否设置模板语言，点击 **Yes**，跳转到模板语言设置界面，设置模板语言为 Jinja2

### 添加模板并创建根路由视图函数

使用 Pycharm 将 `static/news/index.html` 文件移动到 `templates/news/` 目录下，并在 `index.py` 中添加根路由访问视图

```python
from . import index_blu
from flask import render_template


@index_blu.route('/')
def index():
    return render_template('news/index.html')
```

运行，访问根路由测试

## 网站图标展示

- 自定义视图函数，访问网站图标，send_static_file 是系统访问静态文件所调用的方法

```python
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
```


