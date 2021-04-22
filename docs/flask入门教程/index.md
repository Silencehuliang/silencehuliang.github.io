# Flask入门教程


## 简介

Flask是由Armin ronacher于2010年用Python语言基于 Werkzeug 工具箱编写的轻量级Web开发框架。

## 特点

Flask只提供核心功能，其他几乎所有的功能都需要用到拓展，比如可以通过Flask-SQLAlchemy拓展对数据库进行操作等等。

## 核心

由[Werkzeug](https://werkzeug.palletsprojects.com/en/0.15.x/)与[Jinja2](https://jinja.palletsprojects.com/en/2.10.x/)组成，Werkzeug是一个全面的[WSGI](https://wsgi.readthedocs.io/en/latest/) Web应用程序库，Jinja是一种现代且设计友好的Python模板语言。

## Flask常用扩展

- [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)：操作数据库
- [Flask-script](https://flask-script.readthedocs.io/en/latest/)：插入脚本
- [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)：管理迁移数据库
- Flask-Session：Session存储方式指定

## 相关文档

1. [中文文档](http://docs.jinkan.org/docs/flask/)
2. [英文文档](https://flask.palletsprojects.com/en/1.0.x/)

##  Flask初体验

### 安装并使用虚拟环境

#### virtualenv 创建和管理虚拟环境

```bash
# 安装
pip install virtualenv
# 创建
virtualenv flask_env
# 使用
source flask_env/bin/activate
```

#### Pipenv 创建和管理虚拟环境

```bash
# 安装
pip install pipenv
# 创建
pipenv install
# 使用
pipenv shell
```

### 安装指定版本flask框架

```bash
sudo pip install flask==1.0.2
```

### 创建一个文件，并带入编写第一个Flask程序

```bash
touch helloflask.py
vim helloflask.py
```

在文件中写入以下代码
```python
# 导入Flask类
from flask import Flask

# 传递__name__参数，创建一个叫app的Flask实例，该实例将会成为我们的 WSGI 应用。
app = Flask(__name__)

# 通过route装饰器来告诉Flask触发函数的URL 
@app.route('/')
# index视图函数，在访问根路径时会调用该函数通过其返回值得到结果
def index():
    return 'Hello Flask'
  
if __name__ == '__main__':
  	# 通过run方法启动web服务器
    app.run()
```

退出编辑模式，运行该程序

```bash
python helloflask.py
```

可以看到以下结果

![](https://tva2.sinaimg.cn/large/00729CCqgy1gewpfqhiujj30ff02tgmp.jpg)

这样就启动了一个非常简单的内建的服务器。这个服务器用于测试应该是足够了，但是 用于生产可能是不够的。现在在浏览器中打开 http://127.0.0.1:5000/ ，应该可以看到 Hello Flask! 字样。

![](https://tva2.sinaimg.cn/large/00729CCqgy1gewpiolwj7j30aq03d0sy.jpg)





## 相关配置参数

### 初始化参数

创建Flask项目的第一步就是实例化Flask对象，以下是实例化对象需要的参数详解

- import_name：Flask程序所在的包(模块)，传 `__name__` 就可以，
- static_url_path：静态文件访问路径，可以不传，默认为：`/ + static_folder`
- static_folder：静态文件存储的文件夹，可以不传，默认为 `static`
- static_host：使用远程主机存储静态文件的地址，默认为None。当host_matching为True时，可以通过static_folder配置静态文件存储的文件夹
- host_matching：设置`url_map.host_matching`属性，默认为False
- subdomain_matching：匹配路由时，请考虑与以下项相关的子域：data:`SERVER_NAME'。默认为False。
- template_folder：模板文件存储的文件夹，可以不传，默认为 `templates`

- instance_path：默认情况下，应用程序的备用实例路径假定包或模块旁边的文件夹“instance”为实例路径。
- instance_relative_config：如果将用于加载配置的相对文件名设置为“True”，则假定该文件名相对于实例路径而不是应用程序根。
- root_path：默认情况下，Flask将自动计算应用程序根路径。在某些情况下，这无法实现（例如，如果包是Python 3命名空间包），需要手动定义。



### 程序加载配置

在Flask程序运行前，我们可以给Flask设置相关配置，例如ENV(应用程序在什么环境中运行)，DEBUG(是否启用调试模式)TESTING(启用测试模式)等配置，常见的有两种方式来实现.
- 从配置文件中加载：`app.config.from_pyfile()`

  创建一个配置文件

  ```bash
  touch config.ini
  vim config.ini 
  ```

  写入配置信息
  ```python
  DEBUG = True
  ```

	选择从配置文件加载
  ```python
  # 创建 Flask 类对象,指向程序所在的包的名称
  app = Flask(__name__)
  
  # 从配置文件中加载配置
  app.config.from_pyfile('config.ini')
  ```

- 从配置对象中加载：app.config.from_object()

  创建一个配置类，然后将类名传入即可

  ```  python
  # 配置类
  class ConfigObject(object):
      DEBUG = True
  
  # 创建 Flask 类对象,指向程序所在的包的名称
  app = Flask(__name__)
  
  # 从配置对象中加载配置
  app.config.from_object(Config)
  ```



### 程序运行配置

这个demo中Flask项目程序启动的入口是app.run()。常见的配置选项有host, port,debug，分别是设置运行主机的ip地址，端口号，是否打开调试模式，当配置文件与这里都有debug时，最终会以这里的debug为准。


```python
app.run(host="127.0.0.1", port=8000)
```





路由

在Web开发中，路由是一种将URL转发到对应视图的程序。






