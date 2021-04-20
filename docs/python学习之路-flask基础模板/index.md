# Python学习之路-Flask基础:模板


## 前言

在前面的学习中，视图函数的主要作用是生成请求的响应，这是最简单的请求。实际上，视图函数有两个作用：处理业务逻辑和返回响应内容。在大型应用中，把业务逻辑和表现内容放在一起，会增加代码的复杂度和维护成本。本次学到的模板，它的作用即是承担视图函数的另一个作用，即返回响应内容。

## 简介

### 什么是模板

模板其实是一个包含响应文本的文件，其中用占位符(变量)表示动态部分，告诉模板引擎其具体的值需要从使用的数据中获取，使用真实值替换变量，再返回最终得到的字符串，这个过程称为“渲染”。Flask是使用 **Jinja2** 这个模板引擎来渲染模板

### 好处

视图函数只负责业务逻辑和数据处理(业务逻辑方面)，而模板则取到视图函数的数据结果进行展示(视图展示方面)，代码结构清晰，耦合度低。

## Jinja2

### 简介

Jinja2是 Python 下一个被广泛应用的模板引擎，是由Python实现的模板语言，他的设计思想来源于 Django 的模板引擎，并扩展了其语法和一系列强大的功能，其是Flask内置的模板语言。

### 模板语言

模板语言是一种被设计来自动生成文档的简单文本格式，在模板语言中，一般都会把一些变量传给模板，替换模板的特定位置上预先定义好的占位变量名。

## 渲染模版函数

Flask提供的 **render_template** 函数封装了该模板引擎，**render_template** 函数的第一个参数是模板的文件名，后面的参数都是键值对，表示模板中变量对应的真实值。

## 使用

### 代码块

- {{}} 来表示变量名，这种 {{}} 语法叫做**变量代码块**

  ```html
  <h1>{{ post.title }}</h1>
  ```

  Jinja2 模版中的变量代码块可以是任意 Python 类型或者对象，只要它能够被 Python 的 str() 方法转换为一个字符串就可以，比如，可以通过下面的方式显示一个字典或者列表中的某个元素:

  ```python
  {{your_dict['key']}}
  {{your_list[0]}}
  ```

- 用 {**%%**} 定义的**控制代码块**，可以实现一些语言层次的功能，比如循环或者if语句

```html
{% if user %}
    {{ user }}
{% else %}
    hello!
<ul>
    {% for index in indexs %}
    <li> {{ index }} </li>
    {% endfor %}
</ul>
```

### 注释

- 使用 {# #} 进行注释，注释的内容不会在html中被渲染出来

```
{# {{ name }} #}
```

## 实操

- 在项目下创建 `templates` 文件夹，用于存放所有的模板文件，并在目录下创建一个模板html文件 `temp_demo1.html`

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
  我的模板html内容
  </body>
  </html>
  ```

- 创建视图函数，将该模板内容进行渲染返回

  ```python
  @app.route('/')
  def index():
      return render_template('temp_demo1.html')
  ```

- 代码中传入字符串，列表，字典到模板中

  ```python
  @app.route('/')
  def index():
      # 往模板中传入的数据
      my_str = 'Hello 模板'
      my_int = 1101
      my_array = [1, 2, 3, 4, 5, 6]
      my_dict = {
          'name': 'xiaoliang',
          'age': 18
      }
      return render_template('temp_demo1.html',
                             my_str=my_str,
                             my_int=my_int,
                             my_array=my_array,
                             my_dict=my_dict
                             )
  ```

- 模板中代码

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
  我的模板html内容
  <br/>{{ my_str }}
  <br/>{{ my_int }}
  <br/>{{ my_array }}
  <br/>{{ my_dict }}

  </body>
  </html>
  ```

- 运行效果

  <!DOCTYPE html>
  我的模板html内容
  Hello 模板
  1101
  [1, 2, 3, 4, 5, 6]
  {'name': 'xiaoliang', 'age': 18}

- 相关运算，取值

  ```html
  <br/> my_int + 10 的和为：{{ my_int + 10 }}
  <br/> my_int + my_array第0个值的和为：{{ my_int + my_array[0] }}
  <br/> my_array 第0个值为：{{ my_array[0] }}
  <br/> my_array 第1个值为：{{ my_array.1 }}
  <br/> my_dict 中 name 的值为：{{ my_dict['name'] }}
  <br/> my_dict 中 age 的值为：{{ my_dict.age }}
  ```

- 结果

  <!DOCTYPE html>
  my_int + 10 的和为：1111 
  my_int + my_array第0个值的和为：1102 
  my_array 第0个值为：1 
  my_array 第1个值为：2 
  my_dict 中 name 的值为：xiaoliang 
  my_dict 中 age 的值为：18

## 过滤器

### 本质

过滤器的本质就是函数。有时候我们不仅仅只是需要输出变量的值，我们还需要修改变量的显示，甚至格式化、运算等等，而在模板中是不能直接调用 Python 中的某些方法，那么这就用到了过滤器。

### 使用方式

- 过滤器的使用方式为：变量名 | 过滤器。

```python
{{variable | filter_name(*args)}}
```

- 如果没有任何参数传给过滤器,则可以把括号省略掉

```python
{{variable | filter_name}}
```

### 链式调用

在 jinja2 中，过滤器是可以支持链式调用的，示例如下：

```python
{{ "hello world" | reverse | upper }}
```

### 常见内建过滤器

#### 字符串操作

- safe：禁用转义

```python
<p>{{ '<em>hello</em>' | safe }}</p>
```

- capitalize：把变量值的首字母转成大写，其余字母转小写

```python
<p>{{ 'hello' | capitalize }}</p>
```

- lower：把值转成小写

```python
<p>{{ 'HELLO' | lower }}</p>
```

- upper：把值转成大写

```python
<p>{{ 'hello' | upper }}</p>
```

- title：把值中的每个单词的首字母都转成大写

```python
<p>{{ 'hello' | title }}</p>
```

- reverse：字符串反转

```python
<p>{{ 'olleh' | reverse }}</p>
```

- format：格式化输出

```python
<p>{{ '%s is %d' | format('name',17) }}</p>
```

- striptags：渲染之前把值中所有的HTML标签都删掉

```python
<p>{{ '<em>hello</em>' | striptags }}</p>
```

- truncate: 字符串截断

```python
<p>{{ 'hello every one' | truncate(9)}}</p>
```

#### 列表操作

- first：取第一个元素

```python
<p>{{ [1,2,3,4,5,6] | first }}</p>
```

- last：取最后一个元素

```python
<p>{{ [1,2,3,4,5,6] | last }}</p>
```

- length：获取列表长度

```python
<p>{{ [1,2,3,4,5,6] | length }}</p>
```

- sum：列表求和

```python
<p>{{ [1,2,3,4,5,6] | sum }}</p>
```

- sort：列表排序

```
<p>{{ [6,2,3,1,5,4] | sort }}</p>
```

#### 语句块过滤

```pyhton
{% filter upper %}
    #一大堆文字#
{% endfilter %}
```

### 自定义过滤器

过滤器的本质是函数。当模板内置的过滤器不能满足需求，可以自定义过滤器。自定义过滤器有两种实现方式：

- 一种是通过Flask应用对象的 **add_template_filter** 方法
- 通过装饰器来实现自定义过滤器

{{< admonition warning "注意" true >}}

自定义的过滤器名称如果和内置的过滤器重名，会覆盖内置的过滤器。

{{< /admonition >}}

### 控制代码块

控制代码块主要包含两个：

```python
- if/else if /else / endif
- for / endfor
```

#### if语句

Jinja2 语法中的if语句跟 Python 中的 if 语句相似,后面的布尔值或返回布尔值的表达式将决定代码中的哪个流程会被执行:

```python
{%if user.is_logged_in() %}
    <a href='/logout'>Logout</a>
{% else %}
    <a href='/login'>Login</a>
{% endif %}
```

过滤器可以被用在 if 语句中:

```python
{% if comments | length > 0 %}
    There are {{ comments | length }} comments
{% else %}
    There are no comments
{% endif %}
```

#### 循环

- 我们可以在 Jinja2 中使用循环来迭代任何列表或者生成器函数

```python
{% for post in posts %}
    <div>
        <h1>{{ post.title }}</h1>
        <p>{{ post.text | safe }}</p>
    </div>
{% endfor %}
```

- 循环和if语句可以组合使用，以模拟 Python 循环中的 continue 功能，下面这个循环将只会渲染post.text不为None的那些post：

```python
{% for post in posts if post.text %}
    <div>
        <h1>{{ post.title }}</h1>
        <p>{{ post.text | safe }}</p>
    </div>
{% endfor %}
```

- 在一个 for 循环块中你可以访问这些特殊的变量:

  | 变量           | 描述                                           |
  | :------------- | :--------------------------------------------- |
  | loop.index     | 当前循环迭代的次数（从 1 开始）                |
  | loop.index0    | 当前循环迭代的次数（从 0 开始）                |
  | loop.revindex  | 到循环结束需要迭代的次数（从 1 开始）          |
  | loop.revindex0 | 到循环结束需要迭代的次数（从 0 开始）          |
  | loop.first     | 如果是第一次迭代，为 True 。                   |
  | loop.last      | 如果是最后一次迭代，为 True 。                 |
  | loop.length    | 序列中的项目数。                               |
  | loop.cycle     | 在一串序列间期取值的辅助函数。见下面示例程序。 |

- 在循环内部,你可以使用一个叫做loop的特殊变量来获得关于for循环的一些信息，比如：要是我们想知道当前被迭代的元素序号，并模拟Python中的enumerate函数做的事情，则可以使用loop变量的index属性,例如:

  ```python
  {% for post in posts%}
  {{loop.index}}, {{post.title}}
  {% endfor %}
  ```

- 会输出这样的结果

  ```python
  1, Post title
  2, Second Post
  ```

- cycle函数会在每次循环的时候,返回其参数中的下一个元素,可以拿上面的例子来说明:

  ```python
  {% for post in posts%}
  {{loop.cycle('odd','even')}} {{post.title}}
  {% endfor %}
  ```

- 会输出这样的结果：

  ```python
  odd Post Title
  even Second Post
  ```

## 代码复用

### 简介

在模板中，可能会遇到以下情况：

- 多个模板具有完全相同的顶部和底部内容
- 多个模板中具有相同的模板代码内容，但是内容中部分值不一样
- 多个模板中具有完全相同的 html 代码块内容

像遇到这种情况，可以使用 JinJa2 模板中的 宏、继承、包含来进行实现

### 宏

#### 简介

把它看作 Jinja2 中的一个函数，它会返回一个模板或者 HTML 字符串，为了避免反复地编写同样的模板代码，出现代码冗余，可以把他们写成函数以进行重用，需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复。

#### 使用

- 定义宏

```python
{% macro input(name,value='',type='text') %}
    <input type="{{type}}" name="{{name}}"
        value="{{value}}" class="form-control">
{% endmacro %}
```

- 调用宏

```python
{{ input('name' value='xiaoliang')}}
```

- 这会输出

```python
<input type="text" name="name"
    value="zs" class="form-control">
```

- 把宏单独抽取出来，封装成html文件，其它模板中导入使用，文件名可以自定义macro.html

```python
{% macro function(type='text', name='', value='') %}
<input type="{{type}}" name="{{name}}"
value="{{value}}" class="form-control">

{% endmacro %}
```

- 在其它模板文件中先导入，再调用

```python
{% import 'macro.html' as func %}
{% func.function() %}
```

### 继承

#### 简介

模板继承是为了重用模板中的公共内容。一般Web开发中，继承主要使用在网站的顶部菜单、底部。这些内容可以定义在父模板中，子模板直接继承，而不需要重复书写。

#### 使用

- 标签定义的内容

```python
{% block top %} {% endblock %}
```

- 相当于在父模板中挖个坑，当子模板继承父模板时，可以进行填充。
- 子模板使用 extends 指令声明这个模板继承自哪个模板
- 父模板中定义的块在子模板中被重新定义，在子模板中调用父模板的内容可以使用super()

#### 父模板

- base.html

```python
{% block top %}
  顶部菜单
{% endblock top %}

{% block content %}
{% endblock content %}

{% block bottom %}
  底部
{% endblock bottom %}
```

#### 子模板

- extends指令声明这个模板继承自哪

```python
{% extends 'base.html' %}
{% block content %}
 需要填充的内容
{% endblock content %}
```

 #### 注意点

- 不支持多继承
- 为了便于阅读，在子模板中使用extends时，尽量写在模板的第一行。
- 不能在一个模板文件中定义多个相同名字的block标签。
- 当在页面中使用多个block标签时，建议给结束标签起个名字，当多个block嵌套时，阅读性更好。

### 包含

#### 简介

Jinja2模板中，除了宏和继承，还支持一种代码重用的功能，叫包含(Include)。它的功能是将另一个模板整个加载到当前模板中，并直接渲染。

#### 使用

- include的使用

```python
{% include 'hello.html' %}
```

包含在使用时，如果包含的模板文件不存在时，程序会抛出**TemplateNotFound**异常，可以加上 `ignore missing` 关键字。如果包含的模板文件不存在，会忽略这条include语句。

- include 的使用加上关键字ignore missing

```python
{% include 'hello.html' ignore missing %}
```

## 特有的变量和函数

### 简介

可以在自己的模板中访问一些 Flask 默认内置的函数和对象

### config

你可以从模板中直接访问Flask当前的config对象:

```python
{{config.SQLALCHEMY_DATABASE_URI}}
sqlite:///database.db
```

### request

就是flask中代表当前请求的request对象：

```python
{{request.url}}
http://127.0.0.1
```

### session

为Flask的session对象

```python
{{session.new}}
True
```

### g变量

在视图函数中设置g变量的 name 属性的值，然后在模板中直接可以取出

```python
{{ g.name }}
```

### url_for()

url_for会根据传入的路由器函数名,返回该路由对应的URL,在模板中始终使用url_for()就可以安全的修改路由绑定的URL,则不比担心模板中渲染出错的链接:

```python
{{url_for('home')}}
/
```

如果我们定义的路由URL是带有参数的,则可以把它们作为关键字参数传入url_for(),Flask会把他们填充进最终生成的URL中:

```python
{{ url_for('post', post_id=1)}}
/post/1
```

### get_flashed_messages()

这个函数会返回之前在flask中通过flask()传入的消息的列表，flash函数的作用很简单,可以把由Python字符串表示的消息加入一个消息队列中，再使用get_flashed_message()函数取出它们并消费掉：

```python
{%for message in get_flashed_messages()%}
    {{message}}
{%endfor%}
```

## Web表单

### 简介

Web 表单是 Web 应用程序的基本功能。它是HTML页面中负责数据采集的部件。表单有三个部分组成：表单标签、表单域、表单按钮。表单允许用户输入数据，负责HTML页面数据采集，通过表单将用户输入的数据提交给服务器。在Flask中，为了处理web表单，我们可以使用 Flask-WTF 扩展，它封装了 WTForms，并且它有验证表单数据的功能

### WTForms支持的HTML标准字段

| 字段对象           | 说明                                      |
| :----------------- | :---------------------------------------- |
| StringField        | 文本字段                                  |
| TextAreaField      | 多行文本字段                              |
| PasswordField      | 密码文本字段                              |
| HiddenField        | 隐藏文件字段                              |
| DateField          | 文本字段，值为 datetime.date 文本格式     |
| DateTimeField      | 文本字段，值为 datetime.datetime 文本格式 |
| IntegerField       | 文本字段，值为整数                        |
| DecimalField       | 文本字段，值为decimal.Decimal             |
| FloatField         | 文本字段，值为浮点数                      |
| BooleanField       | 复选框，值为True 和 False                 |
| RadioField         | 一组单选框                                |
| SelectField        | 下拉列表                                  |
| SelectMutipleField | 下拉列表，可选择多个值                    |
| FileField          | 文件上传字段                              |
| SubmitField        | 表单提交按钮                              |
| FormField          | 把表单作为字段嵌入另一个表单              |
| FieldList          | 一组指定类型的字段                        |

### WTForms常用验证函数

| 验证函数     | 说明                                     |
| :----------- | :--------------------------------------- |
| DataRequired | 确保字段中有数据                         |
| EqualTo      | 比较两个字段的值，常用于比较两次密码输入 |
| Length       | 验证输入的字符串长度                     |
| NumberRange  | 验证输入的值在数字范围内                 |
| URL          | 验证URL                                  |
| AnyOf        | 验证输入值在可选列表中                   |
| NoneOf       | 验证输入值不在可选列表中                 |

使用 Flask-WTF 需要配置参数 SECRET_KEY。

CSRF_ENABLED是为了CSRF（跨站请求伪造）保护。 SECRET_KEY用来生成加密令牌，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。

## CSRF

### 简介

`CSRF`全拼为`Cross Site Request Forgery`，译为跨站请求伪造。`CSRF`指攻击者盗用了你的身份，以你的名义发送恶意请求。包括：以你名义发送邮件，发消息，盗取你的账号，甚至于购买商品，虚拟货币转账......，造成的问题：个人隐私泄露以及财产安全。

### 防止 CSRF 攻击

1. 在客户端向后端请求界面数据的时候，后端会往响应中的 cookie 中设置 csrf_token 的值
2. 在 Form 表单中添加一个隐藏的的字段，值也是 csrf_token
3. 在用户点击提交的时候，会带上这两个值向后台发起请求
4. 后端接受到请求，以会以下几件事件：
   - 从 cookie中取出 csrf_token
   - 从 表单数据中取出来隐藏的 csrf_token 的值
   - 进行对比
5. 如果比较之后两值一样，那么代表是正常的请求，如果没取到或者比较不一样，代表不是正常的请求，不执行下一步操作

### 在 Flask 项目中解决 CSRF 攻击

在 Flask 中， Flask-wtf 扩展有一套完善的 csrf 防护体系，对于我们开发者来说，使用起来非常简单

#### 在 FlaskForm 中实现校验

- 设置应用程序的 secret_key，用于加密生成的 csrf_token 的值

```python
app.secret_key = "#此处可以写随机字符串#"
```

- 在模板的表单中添加以下代码

```html
<form method="post">
    {{ form.csrf_token() }}
    {{ form.username.label }} {{ form.username }}<br/>
    {{ form.password.label }} {{ form.password }}<br/>
    {{ form.password2.label }} {{ form.password2 }}<br/>
    {{ form.submit }}
</form>
```

{{< admonition warning "注意" true >}}

 设置完毕，cookie 中的 csrf_token 不需要我们关心，会自动帮我们设置

{{< /admonition >}}

#### 单独使用

- 设置应用程序的 secret_key，用于加密生成的 csrf_token 的值

```python
app.secret_key = "#此处可以写随机字符串#"
```

- 导入 flask_wtf.csrf 中的 CSRFProtect 类，进行初始化，并在初始化的时候关联 app

```python
from flask.ext.wtf import CSRFProtect
CSRFProtect(app)
```

- 如果模板中有表单，不需要做任何事。与之前一样:

```html
<form method="post">
    {{ form.csrf_token }}
    ...
</form>
```

- 但如果模板中没有表单，你仍需要 CSRF 令牌:

```html
<form method="post" action="/">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
</form>
```


