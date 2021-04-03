# Django基础教程之请求与相应


**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

本教程为Django基础教程系列第四篇，前面篇章在以下链接：

[Django基础教程之Django介绍](http://49.235.231.121/2019/django基础教程一/)

[Django基础教程之工程搭建](http://49.235.231.121/2019/django基础教程二/)

[Django基础教程之配置文件详解](http://49.235.231.121/2019/django基础教程三/)

## 前言

在[Django基础教程之工程搭建](http://49.235.231.121/2019/django基础教程二/)中，[视图相关部分](http://49.235.231.121/2019/django基础教程二/#应用)提到过Django中视图的功能是接受请求，进行业务处理，返回响应。今天就来研究一下Django中的请求与相应部分。

## 请求

利用HTTP协议向服务器传参有几种途径？

- 提取URL的特定部分，可以通过服务器端路由中用正则表达式截取；
- 查询字符串（query string)；
- 请求体（body）中发送的数据，比如表单数据、json、xml；
- 在http报文的头（header）中。



### URL路径参数

在定义路由URL时，可以使用正则表达式提取参数的方法从URL中获取请求参数，Django会将提取的参数直接传递到视图的传入参数中。

- 未命名参数按定义顺序传递， 如

  ```python
  url(r'^weather/([a-z]+)/(\d{4})/$', views.weather),
  
  def weather(request, city, year):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```

- 命名参数按名字传递，如

  ```python
  url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),
  
  def weather(request, year, city):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```



### QueryDict对象

与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况，HttpRequest对象的属性GET、POST都是QueryDict类型的对象

- get方法：根据键获取值，如果一个键同时拥有多个值将获取最后一个值，如果键不存在则返回None值，可以设置默认值进行后续处理
- getlist方法：根据键获取值，值以列表返回，可以获取指定键的所有值，如果键不存在则返回空列表，可以设置默认值进行后续处理



### 查询字符串Query String

获取请求路径中的查询字符串参数，可以通过request.GET属性获取，返回QueryDict对象。**查询字符串不区分请求方式，即假使客户端进行POST方式的请求，依然可以通过request.GET获取请求中的查询字符串数据。**



### 请求体

请求体数据格式不固定，可以是表单类型字符串，可以是JSON字符串，可以是XML字符串，应区别对待。

可以发送请求体数据的请求方式有**POST**、**PUT**、**PATCH**、**DELETE**。

**Django默认开启了CSRF防护**，会对上述请求方式进行CSRF防护验证，在测试时可以关闭CSRF防护机制，方法为在settings.py文件中注释掉CSRF中间件



### 表单 Form Data

前端发送的表单类型的请求体数据，可以通过request.POST属性获取，返回QueryDict对象。**request.POST只能用来获取POST方式的请求体表单数据。**



### 非表单类型 Non-Form Data

非表单类型的请求体数据，Django无法自动解析，可以通过**request.body**属性获取最原始的请求体数据，自己按照请求体格式（JSON、XML等）进行解析。**request.body返回bytes类型。**



### 请求头

可以通过**request.META**属性获取请求头headers中的数据，**request.META为字典类型**。

常见的请求头如：

- `CONTENT_LENGTH` – 请求体的长度。
- `CONTENT_TYPE` – 请求体的类型。
- `HTTP_ACCEPT` – 响应的可接受内容类型。
- `HTTP_ACCEPT_ENCODING` – 可接受的响应码。
- `HTTP_ACCEPT_LANGUAGE` – 响应的可接受语言。
- `HTTP_HOST` – 客户端发送的HTTP主机报头。
- `HTTP_REFERER` – 参考页面。
- `HTTP_USER_AGENT` – 客户机的用户代理字符串。
- `QUERY_STRING` – 查询字符串，作为单个(未解析的)字符串。
- `REMOTE_ADDR` – 客户端的IP地址。
- `REMOTE_HOST` – 客户机的主机名。
- `REMOTE_USER` – Web服务器认证的用户。
- `REQUEST_METHOD` – 请求方式字符串，如"GET"或"POST"。
- `SERVER_NAME` – 服务器的主机名。
- `SERVER_PORT` – 服务器的端口。



### 其他常用HttpRequest对象属性

- **method**：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
- **user：请求的用户对象。**
- path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
- encoding：一个字符串，表示提交的数据的编码方式。
  - 如果为None则表示使用浏览器的默认设置，一般为utf-8。
  - 这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。

- FILES：一个类似于字典的对象，包含所有的上传文件。



## 响应

视图在接收请求并处理后，必须返回HttpResponse对象或子对象。HttpRequest对象由Django创建，HttpResponse对象由开发人员创建。



### HttpResponse

可以使用**django.http.HttpResponse**来构造响应对象。也可通过HttpResponse对象属性来设置响应体、状态码：

- content：表示返回的内容。
- status_code：返回的HTTP响应状态码。

响应头可以直接将HttpResponse对象当做字典进行响应头键值对的设置



### HttpResponse子类

Django提供了一系列HttpResponse的子类，可以快速设置状态码

- HttpResponseRedirect 301
- HttpResponsePermanentRedirect 302
- HttpResponseNotModified 304
- HttpResponseBadRequest 400
- HttpResponseNotFound 404
- HttpResponseForbidden 403
- HttpResponseNotAllowed 405
- HttpResponseGone 410
- HttpResponseServerError 500



### JsonResponse

若要返回json数据，可以使用JsonResponse来构造响应对象，作用：

- 帮助我们将数据转换为json字符串
- 设置响应头**Content-Type**为 **application/json**



### redirect重定向



## Cookie

Cookie，有时也用其复数形式Cookies，指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密）。Cookie最早是网景公司的前雇员Lou Montulli在1993年3月的发明。Cookie是由服务器端生成，发送给User-Agent（一般是浏览器），浏览器会将Cookie的key/value保存到某个目录下的文本文件内，下次请求同一网站时就发送该Cookie给服务器（前提是浏览器设置为启用cookie）。Cookie名称和值可以由服务器端开发自己定义，这样服务器可以知道该用户是否是合法用户以及是否需要重新登录等。服务器可以利用Cookies包含信息的任意性来筛选并经常性维护这些信息，以判断在HTTP传输中的状态。Cookies最典型记住用户名。

Cookie是存储在浏览器中的一段纯文本信息，建议不要存储敏感信息如密码，因为电脑上的浏览器可能被其它人使用。



### Cookie的特点

- Cookie以键值对的格式进行信息的存储。
- Cookie基于域名安全，不同域名的Cookie是不能互相访问的，如访问itcast.cn时向浏览器中写了Cookie信息，使用同一浏览器访问baidu.com时，无法访问到itcast.cn写的Cookie信息。
- 当浏览器请求某网站时，会将浏览器存储的跟网站相关的所有Cookie信息提交给网站服务器。



### 设置Cookie

可以通过**HttpResponse**对象中的**set_cookie**方法来设置cookie。



### 读取Cookie

可以通过**HttpRequest**对象的**COOKIES**属性来读取本次请求携带的cookie值。**request.COOKIES为字典类型**。



## Session

**Django项目默认启用Session。**如需禁用session，将上图中的session中间件注释掉即可。



### 存储方式

在settings.py文件中，可以设置session数据的存储方式，可以保存在数据库、本地缓存等。

#### 数据库

存储在数据库中，如下设置可以写，也可以不写，**这是默认存储方式**。

```python
SESSION_ENGINE='django.contrib.sessions.backends.db'
```

如果存储在数据库中，需要在项INSTALLED_APPS中安装Session应用。

```PYTHON
INSTALLED_APPS = [    
  		...
      'django.contrib.sessions',    
      ...
  ]
```

存储在数据库中会生成一个diango_session的表，表结构为：键、值、过期时间

#### 本地缓存

存储在本机内存中，如果丢失则不能找回，比数据库的方式读写更快。

```python
SESSION_ENGINE='django.contrib.sessions.backends.cache'
```

#### 混合存储

优先从本机内存中存取，如果没有则从数据库中存取。

```python
SESSION_ENGINE='django.contrib.sessions.backends.cached_db'
```

#### Redis

在redis中保存session，需要引入第三方扩展，我们可以使用**django-redis**来解决。

1） 安装扩展

```python
pip install django-redis
```

2）配置

在settings.py文件中做如下设置

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

#### 注意

如果redis的ip地址不是本地回环127.0.0.1，而是其他地址，访问Django时，可能出现Redis连接错误，如下：

解决方法：

修改redis的配置文件，添加特定ip地址。



#### Session操作

通过HttpRequest对象的session属性进行会话的读写操作。

1） 以键值对的格式写session。

```
request.session['键']=值
```

2）根据键读取值。

```
request.session.get('键',默认值)
```

3）清除所有session，在存储中删除值部分。

```
request.session.clear()
```

4）清除session数据，在存储中删除session的整条数据。

```
request.session.flush()
```

5）删除session中的指定键及值，在存储中只删除某个键及对应的值。

```
del request.session['键']
```

6）设置session的有效期

```
request.session.set_expiry(value)
```

- 如果value是一个整数，session将在value秒没有活动后过期。
- 如果value为0，那么用户session的Cookie将在用户的浏览器关闭时过期。
- 如果value为None，那么session有效期将采用系统默认值，**默认为两周**，可以通过在settings.py中设置**SESSION_COOKIE_AGE**来设置全局默认值。
