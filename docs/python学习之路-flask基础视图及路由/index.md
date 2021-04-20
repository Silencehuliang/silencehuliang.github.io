# Python学习之路-Flask基础:视图及路由


## 路由

### 作用

#### 指定路由地址

```python
# 指定访问路径为 demo1
@app.route('/demo1')
def demo1():
    return 'demo1'
```

#### 给路由传参示例

有时我们需要将同一类 URL 映射到同一个视图函数处理，比如：使用同一个视图函数来显示不同用户的个人信息。

```python
# 路由传递参数
@app.route('/user/<user_id>')
def user_info(user_id):
    return 'hello %s' % user_id
```

- 路由传递的参数默认当做 string 处理，也可以指定参数的类型

```python
# 路由传递参数
@app.route('/user/<int:user_id>')
def user_info(user_id):
    return 'hello %d' % user_id
```

{{< admonition tip "提示" true >}}

这里指定int，尖括号中的内容是动态的，在此暂时可以理解为接受 int 类型的值，实际上 int 代表使用 IntegerConverter 去处理 url 传入的参数

{{< /admonition >}}

#### 指定请求方式

在 Flask 中，定义一个路由，默认的请求方式为：

- GET
- OPTIONS(自带)
- HEAD(自带)

如果想添加请求方试，那么可以如下指定：

```python
@app.route('/demo2', methods=['GET', 'POST'])
def demo2():
    # 直接从请求中取到请求方式并返回
    return request.method
```

### 正则匹配路由

在 web 开发中，可能会出现限制用户访问规则的场景，那么这个时候就需要用到正则匹配，根据自己的规则去限定请求参数再进行访问，具体实现步骤为：

- 导入转换器基类：在 Flask 中，所有的路由的匹配规则都是使用转换器对象进行记录
- 自定义转换器：自定义类继承于转换器基类
- 添加转换器到默认的转换器字典中
- 使用自定义转换器实现自定义匹配规则

#### 代码实现

- 导入转换器基类

```python
from werkzeug.routing import BaseConverter
```

- 自定义转换器

```python
# 自定义正则转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # 将接受的第1个参数当作匹配规则进行保存
        self.regex = args[0]
```

- 添加转换器到默认的转换器字典中，并指定转换器使用时名字为: re

```python
app = Flask(__name__)

# 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: re
app.url_map.converters['re'] = RegexConverter
```

- 使用转换器去实现自定义匹配规则，当前此处定义的规则是：3位数字

```python
@app.route('/user/<re("[0-9]{3}"):user_id>')
def user_info(user_id):
    return "user_id 为 %s" % user_id
```

运行测试：http://127.0.0.1:5000/user/123 ，如果访问的url不符合规则，会提示找不到页面

#### 自定义转换器其他两个函数实现

继承于自定义转换器之后，还可以实现 to_python 和 to_url 这两个函数去对匹配参数做进一步处理：

- to_python：

  该函数参数中的 value 值代表匹配到的值，可输出进行查看，匹配完成之后，对匹配到的参数作最后一步处理再返回，比如：转成 int 类型的值再返回：

  ```python
  class RegexConverter(BaseConverter):
      def __init__(self, url_map, *args):
          super(RegexConverter, self).__init__(url_map)
          # 将接受的第1个参数当作匹配规则进行保存
          self.regex = args[0]

      def to_python(self, value):
          return int(value)
  ```
  
  运行测试，在视图函数中可以查看参数的类型，由之前默认的 str 已变成 int 类型的值
  
- to_url:

  在使用 url_for 去获取视图函数所对应的 url 的时候，会调用此方法对 url_for 后面传入的视图函数参数做进一步处理，具体可参见 Flask 的 app.py 中写的示例代码：ListConverter

#### 系统自带转换器

  ```python
  DEFAULT_CONVERTERS = {
      'default':          UnicodeConverter,
      'string':           UnicodeConverter,
      'any':              AnyConverter,
      'path':             PathConverter,
      'int':              IntegerConverter,
      'float':            FloatConverter,
      'uuid':             UUIDConverter,
  }
  ```

系统自带的转换器具体使用方式在每种转换器的注释代码中有写，请留意每种转换器初始化的参数。

### 装饰器路由

#### 两大核心

Flask有两大核心：Werkzeug和Jinja2

```
- Werkzeug实现路由、调试和Web服务器网关接口
- Jinja2实现了模板。
```

#### Werkzeug

Werkzeug是一个遵循WSGI协议的python函数库

```
- 其内部实现了很多Web框架底层的东西，比如request和response对象；
- 与WSGI规范的兼容；支持Unicode；
- 支持基本的会话管理和签名Cookie；
- 集成URL请求路由等。
```

Werkzeug库的 routing 模块负责实现 URL 解析。不同的 URL 对应不同的视图函数，routing模块会对请求信息的URL进行解析，匹配到URL对应的视图函数，执行该函数以此生成一个响应信息。routing模块内部有：

- Rule类：用来构造不同的URL模式的对象，路由URL规则
- Map类：存储所有的URL规则和一些配置参数
- BaseConverter的子类：负责定义匹配规则
- MapAdapter类：负责协调Rule做具体的匹配的工作

## 视图

### 作用

#### 返回JSON

在使用 Flask 写一个接口时候需要给客户端返回 JSON 数据，在 Flask 中可以直接使用 **jsonify** 生成一个 JSON 的响应

```python
# 返回JSON
@app.route('/demo3')
def demo3():
    json_dict = {
        "user_id": 10,
        "user_name": "laowang"
    }
    return jsonify(json_dict)
```

{{< admonition tip "提示" true >}}

不推荐使用 json.dumps 转成 JSON 字符串直接返回，因为返回的数据要符合 HTTP 协议规范，如果是 JSON 需要指定 content-type:application/json

{{< /admonition >}}

#### 重定向

- 重定向到 **百度** 官网

```python
# 重定向
@app.route('/demo4')
def demo4():
    return redirect('http://www.baidu.com')
```

重定向到自己写的视图函数，可以直接填写自己 url 路径，也可以使用 url_for 生成指定视图函数所对应的 url

```python
@app.route('/demo5')
def demo5():
    return 'demo5'

# 重定向
@app.route('/demo6')
def demo6():
    return redirect(url_for('demo5'))
```

- 重定向到带有参数的视图函数，在 url_for 函数中传入参数

```python
# 路由传递参数
@app.route('/user/<int:user_id>')
def user_info(user_id):
    return 'hello %d' % user_id

# 重定向
@app.route('/demo7')
def demo7():
    # 使用 url_for 生成指定视图函数所对应的 url
    return redirect(url_for('user_info', user_id=100))
```

#### 自定义状态码

- 在 Flask 中，可以很方便的返回自定义状态码，以实现不符合 http 协议的状态码，例如：status code: 666

```python
@app.route('/demo8')
def demo8():
    return '状态码为 666', 666
```

## 请求勾子

### 为什么

在客户端和服务器交互的过程中，有些准备工作或扫尾工作需要处理，比如：

- 在请求开始时，建立数据库连接；
- 在请求开始时，根据需求进行权限校验；
- 在请求结束时，指定数据的交互格式；

### 怎么用

为了让每个视图函数避免编写重复功能的代码，Flask提供了通用设施的功能，即请求钩子。请求钩子是通过装饰器的形式实现，Flask支持如下四种请求钩子：

- before_first_request：在处理第一个请求前执行
- before_request：在每次请求前执行，如果在某修饰的函数中返回了一个响应，视图函数将不再被调用
- after_request：如果没有抛出错误，在每次请求后执行，接受一个参数：视图函数作出的响应，在此函数中可以对响应值在返回之前做最后一步修改处理，需要将参数中的响应在此参数中进行返回
- teardown_request：在每次请求后执行，接受一个参数：错误信息，如果有相关错误抛出

### 代码测试

```python
from flask import Flask
from flask import abort

app = Flask(__name__)


# 在第一次请求之前调用，可以在此方法内部做一些初始化操作
@app.before_first_request
def before_first_request():
    print("before_first_request")


# 在每一次请求之前调用，这时候已经有请求了，可能在这个方法里面做请求的校验
# 如果请求的校验不成功，可以直接在此方法中进行响应，直接return之后那么就不会执行视图函数
@app.before_request
def before_request():
    print("before_request")



# 在执行完视图函数之后会调用，并且会把视图函数所生成的响应传入,可以在此方法中对响应做最后一步统一的处理
@app.after_request
def after_request(response):
    print("after_request")
    response.headers["Content-Type"] = "application/json"
    return response


# 请每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息
@app.teardown_request
def teardown_request(e):
    print("teardown_request")


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    app.run(debug=True)
```

- 在第1次请求时的打印：

```bash
before_first_request
before_request
after_request
teardown_request
```

- 在第2次请求时的打印：

```bash
before_request
after_request
teardown_request
```

## request

### 简介

request 就是flask中代表当前请求的 request 对象，其中一个请求上下文变量(理解成全局变量，在视图函数中直接使用可以取到当前本次请求)，常用的属性如下：

|  属性   |              说明              |      类型      |
| :-----: | :----------------------------: | :------------: |
|  data   | 记录请求的数据，并转换为字符串 |       *        |
|  form   |      记录请求中的表单数据      |   MultiDict    |
|  args   |      记录请求中的查询参数      |   MultiDict    |
| cookies |     记录请求中的cookie信息     |      Dict      |
| headers |       记录请求中的报文头       | EnvironHeaders |
| method  |     记录请求使用的HTTP方法     |    GET/POST    |
|   url   |       记录请求的URL地址        |     string     |
|  files  |       记录请求上传的文件       |       *        |

### 示例

获取上传的图片并保存到本地

```python
@app.route('/', methods=['POST'])
def index():
    pic = request.files.get('pic')
    pic.save('./static/p.png')
    return 'index'
```

## 状态保持

### 原因

因为 http 是一种无状态协议，浏览器请求服务器是无状态的。

### 无状态

指一次用户请求时，浏览器、服务器无法知道之前这个用户做过什么，每次请求都是一次新的请求。

### 无状态原因

浏览器与服务器是使用 socket 套接字进行通信的，服务器将请求结果返回给浏览器之后，会关闭当前的 socket 连接，而且服务器也会在处理页面完毕之后销毁页面对象。

### 实现状态保持的方式

- 在客户端存储信息使用`Cookie`

- 在服务器端存储信息使用`Session`

{{< admonition tip "提示" true >}}

无状态协议：协议对于事务处理没有记忆能力，对同一个 url 请求没有上下文关系，每次的请求都是独立的，它的执行情况和结果与前面的请求和之后的请求是无直接关系的，它不会受前面的请求应答情况直接影响，也不会直接影响后面的请求应答情况，服务器中没有保存客户端的状态，客户端必须每次带上自己的状态去请求服务器

{{< /admonition >}}

#### Cookie

##### 简介

指某些网站为了辨别用户身份、进行会话跟踪而储存在用户本地的数据（通常经过加密）。Cookie最早是网景公司的前雇员Lou Montulli在1993年3月的发明。Cookie是由服务器端生成，发送给客户端浏览器，浏览器会将Cookie的key/value保存，下次请求同一网站时就发送该Cookie给服务器（前提是浏览器设置为启用cookie）。Cookie的key/value可以由服务器端自己定义。

{{< admonition tip "提示" true >}}

Cookie是存储在浏览器中的一段纯文本信息，建议不要存储敏感信息如密码，因为电脑上的浏览器可能被其它人使用，Cookie基于域名安全，不同域名的Cookie是不能互相访问的，如访问baidu.com时向浏览器中写了Cookie信息，使用同一浏览器访问google.com时，无法访问到baidu.com写的Cookie信息。浏览器的同源策略，当浏览器请求某网站时，会将本网站下所有Cookie信息提交给服务器，所以在request中可以读取Cookie信息

{{< /admonition >}}

##### 设置

```python
from flask imoprt Flask,make_response
@app.route('/cookie')
def set_cookie():
    resp = make_response('this is to set cookie')
    resp.set_cookie('username', 'xiaoliang')
    return resp
```

设置过期时间

```python
@app.route('/cookie')
def set_cookie():
    response = make_response('this is to set cookie')
    response.set_cookie('username', 'xiaoliang', max_age=3600)
    return response
```

##### 获取

```python
from flask import Flask,request
#获取cookie
@app.route('/request')
def resp_cookie():
    resp = request.cookies.get('username')
    return resp
```

#### Session

##### 简介

对于敏感、重要的信息，建议要存储在服务器端，不能存储在浏览器中，如用户名、余额、等级、验证码等信息。在服务器端进行状态保持的方案就是`Session`

{{< admonition tip "提示" true >}}

Session依赖于Cookie

{{< /admonition >}}

##### 获取

session:请求上下文对象，用于处理http请求中的一些数据内容

```python
@app.route('/index1')
def index1():
    session['username'] = 'xiaoliang'
    return redirect(url_for('index'))
@app.route('/')
def index():
    return session.get('username')
```

## 上下文

### 简介

相当于一个容器，保存了 Flask 程序运行过程中的一些信息。Flask中有两种上下文，请求上下文和应用上下文

### 请求上下文(request context)

#### 简介

在 flask 中，可以直接在视图函数中使用`request`这个对象进行获取相关数据，而`request`就是请求上下文的对象，保存了当前本次请求的相关数据，请求上下文对象有：`request`、`session`

#### request

封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。

#### session

用来记录请求会话中的信息，针对的是用户信息。举例：session['name'] = user.id，可以记录用户信息。还可以通过session.get('name')获取用户信息。

### 应用上下文(application context)

#### 简介

它的字面意思是 应用上下文，但它不是一直存在的，它只是request context 中的一个对 app 的代理(人)，所谓local proxy。它的作用主要是帮助 request 获取当前的应用，它是伴 request 而生，随 request 而灭的。应用上下文对象有：current_app，g

#### current_app

应用程序上下文,用于存储应用程序中的变量，可以通过current_app.name打印当前app的名称，也可以在current_app中存储一些变量，例如：

- 应用的启动脚本是哪个文件，启动时指定了哪些参数
- 加载了哪些配置文件，导入了哪些配置
- 连了哪个数据库
- 有哪些public的工具类、常量
- 应用跑再哪个机器上，IP多少，内存多大

```python
current_app.name
current_app.test_value='value'
```

#### g变量

g 作为 flask 程序全局的一个临时变量,充当者中间媒介的作用,我们可以通过它传递一些数据，g 保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别

```python
g.name='abc'
```

{{< admonition warning "注意" true >}}

不同的请求，会有不同的全局变量

{{< /admonition >}}

#### 两者区别

- 请求上下文：保存了客户端和服务器交互的数据
- 应用上下文：flask 应用程序运行过程中，保存的一些配置信息，比如程序名、数据库连接、应用信息等

## Flask-Script 扩展

### 为什么

通过使用Flask-Script扩展，我们可以在Flask服务器启动的时候，通过命令行的方式传入参数。而不仅仅通过app.run()方法中传参，比如我们可以通过：

```python
python hello.py runserver -host ip地址
```

以上代码告诉服务器在哪个网络接口监听来自客户端的连接。默认情况下，服务器只监听来自服务器所在的计算机发起的连接，即localhost连接。

我们可以通过python hello.py runserver --help来查看参数。

### 代码实现

- 安装 Flask-Script 扩展

```bash
pip install flask-script
```

- 集成 Flask-Script

```python
from flask import Flask
from flask_script import Manager

app = Flask(__name__)
# 把 Manager 类和应用程序实例进行关联
manager = Manager(app)

@app.route('/')
def index():
    return 'Hello flask-script'

if __name__ == "__main__":
    manager.run()
```

{{< admonition tip "提示" true >}}

Flask-Script 还可以为当前应用程序添加脚本命令

{{< /admonition >}}
