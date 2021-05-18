# Python学习之路-初识爬虫:requests


## requests的作用

作用：发送网络请求，返回响应数据

中文文档 ： http://docs.python-requests.org/zh_CN/latest/index.html

## 为什么学requests而不是urllib

- requests的底层实现就是urllib
- requests在python2 和python3中通用，方法完全一样
- requests简单易用
- Requests能够自动帮助我们解压(gzip压缩的等)网页内容

## response.text 和response.content的区别

- `response.text`
  - 类型：str
  - 解码类型： 根据HTTP 头部对响应的编码作出有根据的推测，推测的文本编码
  - 如何修改编码方式：`response.encoding=”gbk”`
- `response.content`
  - 类型：bytes
  - 解码类型： 没有指定
  - 如何修改编码方式：`response.content.deocde(“utf8”)`

获取网页源码的通用方式：

1. `response.content.decode()`
2. `response.content.decode("GBK")`
3. `response.text`

以上三种方法从前往后尝试，能够100%的解决所有网页解码的问题

所以：更推荐使用`response.content.deocde()`的方式获取响应的html页面

## 发送带header的请求

### 思考

对比浏览器上百度首页的网页源码和代码中的百度首页的源码，有什么不同？

代码中的百度首页的源码非常少，为什么？

### 为什么请求需要带上header？

模拟浏览器，欺骗服务器，获取和浏览器一致的内容

### header的形式

```
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
```

### 用法

```
requests.get(url,headers=headers)
```

## 发送带参数的请求

### 什么叫做请求参数

错误的列1： http://www.webkaka.com/tutorial/server/2015/021013/

正确的例2：https://www.baidu.com/s?wd=python&c=b

### 参数的形式

```
kw = {'wd':'长城'}
```

### 用法

```
requests.get(url,params=kw)
```

### 关于参数的注意点

在url地址中，很多参数是没有用的，比如百度搜索的url地址，其中参数只有一个字段有用，其他的都可以删除

对应的，在后续的爬虫中，越到很多参数的url地址，都可以尝试删除参数

## requests模块发送POST请求

### 哪些地方我们会用到POST请求：

- 登录注册（ POST 比 GET 更安全）
- 需要传输大文本内容的时候（ POST 请求对数据长度没有要求）

所以同样的，我们的爬虫也需要在这两个地方回去模拟浏览器发送post请求

### 使用requests模块发送post请求

- 用法： `response = requests.post("http://www.baidu.com/", data = data,headers=headers)`
- data 的形式：字典

## 使用代理

### 为什么要使用代理

- 让服务器以为不是同一个客户端在请求
- 防止我们的真实地址被泄露，防止被追究

### 理解正向代理和反向代理的区别

正向代理：对于浏览器知道服务器的真实地址，例如VPN 反向代理：浏览器不知道服务器的真实地址，例如nginx

### 代理的使用

- 用法： `requests.get("http://www.baidu.com", proxies = proxies)`
- proxies的形式：字典
- 例如：

```json
proxies = { 
    "http": "http://12.34.56.79:9527", 
    "https": "https://12.34.56.79:9527", 
    }
```

### 代理IP的分类

根据代理服务器端的配置，向目标地址发送请求时，REMOTE_ADDR， HTTP_VIA，HTTP_X_FORWARDED_FOR三个变量不同而可以分为下面四类：

- 透明代理(Transparent Proxy)

  ```txt
    REMOTE_ADDR = Proxy IP
    HTTP_VIA = Proxy IP
    HTTP_X_FORWARDED_FOR = Your IP
  ```

  透明代理虽然可以直接“隐藏”你的IP地址，但是还是可以从HTTP_X_FORWARDED_FOR来查到你是谁。

- 匿名代理(Anonymous Proxy)

  ```txt
    REMOTE_ADDR = proxy IP
    HTTP_VIA = proxy IP
    HTTP_X_FORWARDED_FOR = proxy IP
  ```

  匿名代理比透明代理进步了一点：别人只能知道你用了代理，无法知道你是谁。

- 混淆代理(Distorting Proxies)

  ```txt
    REMOTE_ADDR = Proxy IP
    HTTP_VIA = Proxy IP
    HTTP_X_FORWARDED_FOR = Random IP address
  ```

  如上，与匿名代理相同，如果使用了混淆代理，别人还是能知道你在用代理，但是会得到一个假的IP地址，伪装的更逼真

- 高匿代理(Elite proxy或High Anonymity Proxy)

  ```txt
    REMOTE_ADDR = Proxy IP
    HTTP_VIA = not determined
    HTTP_X_FORWARDED_FOR = not determined
  ```

  可以看出来，高匿代理让别人根本无法发现你是在用代理，所以是最好的选择。

从使用的协议：代理ip可以分为http代理，https代理，socket代理等，使用的时候需要根据抓取网站的协议来选择

### 代理IP使用的注意点

- 反反爬

  使用代理ip是非常必要的一种`反反爬`的方式,但是即使使用了代理ip，对方服务器任然会有很多的方式来检测我们是否是一个爬虫

  比如：

  - 一段时间内，检测IP访问的频率，访问太多频繁会屏蔽

  - 检查Cookie，User-Agent，Referer等header参数，若没有则屏蔽

  - 服务方购买所有代理提供商，加入到反爬虫数据库里，若检测是代理则屏蔽

    所以更好的方式是购买质量更高的代理，或者自己搭建代理服务器，组装自己的`代理IP池`，同时在使用的时候使用随机的方式进行选择使用，不要每次都用一个代理ip，没事没有任何效果的

- 代理ip池的更新

  购买的代理ip很多时候大部分(超过60%)可能都没办法使用，这个时候就需要通过程序去检测哪些可用，把不能用的删除掉。对应的实现方式在我们学习了`超时参数的使用`之后大家会了解

## 使用requests处理cookie相关的请求

### 回顾cookie和session的区别

- cookie数据存放在客户的浏览器上，session数据放在服务器上。
- cookie不是很安全，别人可以分析存放在本地的cookie并进行cookie欺骗。
- session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能。
- 单个cookie保存的数据不能超过4K，很多浏览器都限制一个站点最多保存20个cookie。

### 爬虫中为什么要使用cookie

- 带上cookie的好处
  - 能够访问登录后的页面
  - 正常的浏览器在请求服务器的时候肯定会带上cookie（第一次请求某个地址除外），所以对方服务器有可能会通过是否携带cookie来判断我们是否是一个爬虫，对应的能够起到一定的反爬的效果
- 带上cookie的坏处
  - 一套cookie往往对应的是一个用户的信息，请求太频繁有更大的可能性被对方识别为爬虫
  - 那么上面的问题如何解决 ?使用多个账号

### requests处理cookie相关的请求之session

- requests 提供了一个叫做session类，来实现客户端和服务端的`会话保持`
- 会话保持有两个内涵：
  - 保存cookie
  - 实现和服务端的长连接

- 使用方法

  ```python
    session = requests.session()
    response = session.get(url,headers)
  ```

  session实例在请求了一个网站后，对方服务器设置在本地的cookie会保存在session中，下一次再使用session请求对方服务器的时候，会带上前一次的cookie

- 动手：

  动手尝试使用session来登录人人网： `http://www.renren.com/PLogin.do`(先不考虑这个url地址从何而来)，请求体的格式：`{"email":"username", "password":"password"}`

### requests处理cookie相关的请求之cookie放在headers中

了解headers中cookie

- headers中的cookie：
  - 使用分号(;)隔开
  - 分号两边的类似a=b形式的表示一条cookie
  - a=b中，a表示键（name），b表示值（value）
  - 在headers中仅仅使用了cookie的name和value

cookie的具体组成的字段

由于headers中对cookie仅仅使用它的name和value，所以在代码中我们仅仅需要cookie的name和value即可

在headers中使用cookie

```python
headers = {
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"Cookie":" Pycharm-26c2d973=dbb9b300-2483-478f-9f5a-16ca4580177e; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1512607763; Pycharm-26c2d974=f645329f-338e-486c-82c2-29e2a0205c74; _xsrf=2|d1a3d8ea|c5b07851cbce048bd5453846445de19d|1522379036"}

requests.get(url,headers=headers)
```

cookie有过期时间，所以直接复制浏览器中的cookie可能意味着下一程序继续运行的时候需要替换代码中的cookie，对应的我们也可以通过一个程序专门来获取cookie供其他程序使用；当然也有很多网站的cookie过期时间很长，这种情况下，直接复制cookie来使用更加简单

### requests处理cookie相关的请求之使用cookies参数

- cookies的形式：字典

```json
cookies = {"cookie的name":"cookie的value"}
```

- 使用方法：

```python
requests.get(url,headers=headers,cookies=cookie_dict}
```

## requests模块获取cookie

`requests.utils.dict_from_cookiejar`:把cookiejar对象转化为字典

```python
import requests

url = "http://www.baidu.com"
response = requests.get(url)
print(type(response.cookies))

cookies = requests.utils.dict_from_cookiejar(response.cookies)
print(cookies)
```

输出为:

```python
<class 'requests.cookies.RequestsCookieJar'>
{'BDORZ': '27315'}
```

在前面的requests的session类中，我们不需要处理cookie的任何细节，如果有需要，我们可以使用上述方法来解决

## requests处理证书错误

经常我们在网上冲浪时，经常能够看到ssl的证书不安全

那么如果在代码中请求会怎么样呢？

```python
import requests

url = "https://www.12306.cn/mormhweb/"
response = requests.get(url)
```

返回

```
ssl.CertificateError ...
```

为了在代码中能够正常的请求，我们修改添加一个参数

```python
import requests

url = "https://www.12306.cn/mormhweb/"
response = requests.get(url,verify=False)
```

## 超时参数的使用

在平时网上冲浪的过程中，我们经常会遇到网络波动，这个时候，一个请求等了很久可能任然没有结果

对应的，在爬虫中，一个请求很久没有结果，就会让整个项目的效率变得非常低，这个时候我们就需要对请求进行强制要求，让他必须在特定的时间内返回结果，否则就报错

使用方法如下：

```
response = requests.get(url,timeout=3)
```

通过添加timeout参数，能够保证在3秒钟内返回响应，否则会报错

这个方法还能够拿来检测代理ip的质量，如果一个代理ip在很长时间没有响应，那么添加超时之后也会报错，对应的这个ip就可以从代理ip池中删除

## retrying模块的使用

上述方法能够加快我们整体的请求速度，但是在正常的网页浏览过成功，如果发生速度很慢的情况，我们会做的选择是**刷新页面**，那么在代码中，我们是否也可以刷新请求呢？

对应的，retrying模块就可以帮助我们解决

- retrying模块的地址：https://pypi.org/project/retrying/
- retrying 模块的使用
  - 使用retrying模块提供的retry模块
  - 通过装饰器的方式使用，让被装饰的函数反复执行
  - retry中可以传入参数`stop_max_attempt_number`,让函数报错后继续重新执行，达到最大执行次数的上限，如果每次都报错，整个函数报错，如果中间有一个成功，程序继续往后执行

所以我们可以结合前面的知识点和retrying模块，把我们需要反复使用的请求方法做一个简单的封装，在后续任何其他地方需要使用的时候，调用该方法就行

代码参考

```python
# parse.py
import requests
from retrying import retry

headers = {}


@retry(stop_max_attempt_number=3) #最大重试3次，3次全部报错，才会报错
def _parse_url(url)
    response = requests.get(url, headers=headers, timeout=3) #超时的时候回报错并重试
    assert response.status_code == 200 #状态码不是200，也会报错并充实
    return response


def parse_url(url)
    try: #进行异常捕获
        response = _parse_url(url)
    except Exception as e:
        print(e)
        response = None
    return response
```

## 为什么需要新建隐身窗口

在打开隐身窗口的时候，第一次请求某个网站是没有携带cookie的，和代码请求一个网站一样，不携带cookie。这样就能够尽可能的理解代码请求某个网站的结果；除非数据是通过js加载出来的，不然爬虫请求到的数据和浏览器请求的数据大部分时候都是相同的

## chrome中network的更多功能

### Perserve log

默认情况下，页面发生跳转之后，之前的请求url地址等信息都会消失，勾选perserve log后之前的请求都会被保留

### filter过滤

在url地址很多的时候，可以在filter中输入部分url地址，对所有的url地址起到一定的过滤效果，具体位置在上面第二幅图中的2的位置

### 观察特定种类的请求

在上面第二幅图中的3的位置，有很多选项，默认是选择的`all`，即会观察到所有种类的请求

很多时候处于自己的目的可以选择`all`右边的其他选项，比如常见的选项：

- XHR:大部分情况表示ajax请求
- JS:js请求
- CSS:css请求

但是很多时候我们并不能保证我们需要的请求是什么类型，特别是我们不清楚一个请求是否为ajax请求的时候，直接选择`all`,从前往后观察即可，其中js，css，图片等不去观察即可

不要被浏览器中的一堆请求吓到了，这些请求中除了js，css，图片的请求外，其他的请求并没有多少个
