# Python学习之路-Flask基础:HelloFlask


## 前言

Web(World Wide Web)诞生最初的目的，是为了利用互联网交流工作文档。web网站发展至今，特别是服务器端，涉及到的知识、内容，非常广泛。这对程序员的要求会越来越高。如果采用成熟，稳健的框架，那么一些基础的工作，比如，安全性，数据流控制等都可以让框架来处理，那么程序开发人员可以把精力放在具体的业务逻辑上面。使用框架的优点：

- 稳定性和可扩展性强
- 可以降低开发难度，提高开发效率。

总结一句话：**避免重复造轮子**。在 Python 中常用的 Web 框架有：flask、django、tornado等

## 简介

Flask诞生于2010年，是Armin ronacher（人名）用 Python 语言基于 Werkzeug 工具箱编写的轻量级Web开发框架。Flask 本身相当于一个内核，其他几乎所有的功能都要用到扩展（邮件扩展Flask-Mail，用户认证Flask-Login，数据库Flask-SQLAlchemy），都需要用第三方的扩展来实现。比如可以用 Flask 扩展加入ORM、窗体验证工具，文件上传、身份验证等。Flask 没有默认使用的数据库，你可以选择 MySQL，也可以用 NoSQL。其 WSGI 工具箱采用 Werkzeug（路由模块），模板引擎则使用 Jinja2。这两个也是 Flask 框架的核心。

## 相关文档

- 英文文档（https://flask.palletsprojects.com/）
- 中文文档（http://docs.jinkan.org/docs/flask/）

## Hello Flask

- 创建项目文件夹

  ```bash
  mkdir hello_flask
  ```

- 创建虚拟环境

  ```bash
  pipenv install
  ```

- 使用虚拟环境

  ```
  pipenv shell
  ```

- 安装flask

  ```bash
  (hello_flask) % hello_flask % pip install flask==1.1.1
  ```

- 创建项目文件

  ```bash
  (hello_flask) % touch helloflask.py
  ```

- 编辑项目

  使用vim编辑

  ```bash
  (hello_flask) % vim helloflask.py   
  ```

  内容如下：

  ```python
  from flask import Flask
  
  app = Flask(__name__)
  
  @app.route('/')
  def index():
      return 'Hello Flask'
  
  if __name__ == '__main__':
      app.run()              
  ```

- 运行项目

  ```
  (hello_flask) % python helloflask.py 
  ```

  运行成功时会看到输出的提示信息：

  ```
  * Serving Flask app "helloflask" (lazy loading)
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

  这时候打开浏览器输入`http://127.0.0.1:5000/`看到`Hello Flask`就说明运行成功了

目前已经实现了一个最简单的 Flask 应用程序，只使用了7行代码，接来对 Flask 程序的创建，运行配置做进一步的了解

## 相关配置参数

### 初始化参数

Flask 程序实例在创建的时候，需要默认传入当前 Flask 程序所指定的包(模块)，接下来就来详细查看一下 Flask 应用程序在创建的时候一些需要我们关注的参数：

- import_name：Flask程序所在的包(模块)，传 `__name__` 就可以，其可以决定 Flask 在访问静态文件时查找的路径
- static_path：静态文件访问路径(不推荐使用，使用 static_url_path 代替)
- static_url_path：静态文件访问路径，可以不传，默认为：`/ + static_folder`
- static_folder：静态文件存储的文件夹，可以不传，默认为 `static`
- template_folder：模板文件存储的文件夹，可以不传，默认为 `templates`

### 程序加载配置

在 Flask 程序运行的时候，可以给 Flask 设置相关配置，比如：配置 Debug 模式，配置数据库连接地址等等，设置 Flask 配置有以下三种方式：

- 从配置对象中加载(常用)：`app.config.form_object()`
- 从配置文件中加载：`app.config.form_pyfile()`
- 从环境变量中加载(了解)：`app.config.from_envvar()`

{{< admonition tip "提示" true >}}

以下演练以设置应用程序的 DEBUG(调试模式) 为例，设置应用为调式模式这后，可以实现以下功能：

1. 程序代码修改后可以自动重启服务器
2. 在服务器出现相关错误的时候可以直接将错误信息进行抛出到控制台打印

{{< /admonition >}}

#### 使用方式

##### 配置对象

从配置对象中加载，创建配置的类，代码如下：

```python
# 配置对象，里面定义需要给 APP 添加的一系列配置
class Config(object):
    DEBUG = True

# 创建 Flask 类的对象,指向程序所在的包的名称
app = Flask(__name__)

# 从配置对象中加载配置
app.config.from_object(Config)
```

运行测试，在修改代码之后直接保存，会自动重启服务器

##### 配置文件

- 创建配置文件 `config.ini`，在配置文件中添加配置`DEBUG = True`

- 使用代码去加载配置

  ```python
  # 创建 Flask 类的对象,指向程序所在的包的名称
  app = Flask(__name__)

  # 从配置文件中加载配置
  app.config.from_pyfile('config.ini')
  ```

##### 环境变量(了解)

- 编辑运行的相关配置

  

  ![](https://tva2.sinaimg.cn/large/00729CCqgy1gpq164xjkej309t04pmxx.jpg)

  ![](https://tvax4.sinaimg.cn/large/00729CCqgy1gpq1a0xbh2j30tt0iraiq.jpg)

  

- 使用代码去加载配置

```python
# 创建 Flask 类的对象,指向程序所在的包的名称
app = Flask(__name__)
# 加载指定环境变量名称所对应的相关配置
app.config.from_envvar('FLASKCONFIG')
```

##### 读取配置

- app.config.get()
- 在视图函数中使用 current_app.config.get()

{{< admonition tip "提示" true >}}

Flask 应用程序将一些常用的配置设置成了应用程序对象的属性，也可以通过属性直接设置/获取某些配置：app.debug = True

{{< /admonition >}}

##### app.run的参数

- 可以指定运行的主机IP地址，端口，是否开启调试模式等

```python
app.run(host="0.0.0.0", port=5000, debug = True)
```


