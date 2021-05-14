# Python学习之路-Tornado基础:异步与WebSocket


## 认识异步

### 同步

我们用两个函数来模拟两个客户端请求，并依次进行处理：

```python
# coding:utf-8

def req_a():
    """模拟请求a"""
    print('开始处理请求req_a')
    print('完成处理请求req_a')

def req_b():
    """模拟请求b"""
    print('开始处理请求req_b')
    print('完成处理请求req_b')

def main():
    """模拟tornado框架，处理两个请求"""
    req_a()
    req_b()

if __name__ == "__main__":
    main()
```

执行结果：

```python
开始处理请求req_a
完成处理请求req_a
开始处理请求req_b
完成处理请求req_b
```

**同步是按部就班的依次执行，始终按照同一个步调执行，上一个步骤未执行完不会执行下一步。**

如果在处理请求req_a时需要执行一个耗时的工作（如IO），其执行过程如何？

```python
# coding:utf-8

import time

def long_io():
    """模拟耗时IO操作"""
    print("开始执行IO操作")
    time.sleep(5)
    print("完成IO操作")
    return "io result"

def req_a():
    print("开始处理请求req_a")
    ret = long_io()
    print("ret: %s" % ret)
    print("完成处理请求req_a")

def req_b():
    print("开始处理请求req_b")
    print("完成处理请求req_b")

def main():
    req_a()
    req_b()

if __name__=="__main__":
    main()
```

执行过程：

```python
开始处理请求req_a
开始执行IO操作
完成IO操作
完成处理请求req_a
开始处理请求req_b
完成处理请求req_b
```

在上面的测试中，我们看到耗时的操作会将代码执行阻塞住，即req_a未处理完req_b是无法执行的。

### 异步

#### 简介

对于耗时的过程，我们将其交给别人（如其另外一个线程）去执行，而我们继续往下处理，当别人执行完耗时操作后再将结果反馈给我们，这就是我们所说的异步。我们用容易理解的线程机制来实现异步。

#### 回调写法实现原理

```python
import time
import thread

def long_io(callback):
    """将耗时的操作交给另一线程来处理"""
    def fun(cb): # 回调函数作为参数
        """耗时操作"""
        print("开始执行IO操作")
        time.sleep(5)
        print("完成IO操作，并执行回调函数")
        cb("io result")  # 执行回调函数
    thread.start_new_thread(fun, (callback,))  # 开启线程执行耗时操作

def on_finish(ret):
    """回调函数"""
    print("开始执行回调函数on_finish")
    print "ret: %s" % ret
    print("完成执行回调函数on_finish")

def req_a():
    print("开始处理请求req_a")
    long_io(on_finish)
    print("离开处理请求req_a")

def req_b():
    print "开始处理请求req_b"
    time.sleep(2) # 添加此句来突出显示程序执行的过程
    print "完成处理请求req_b"

def main():
    req_a()
    req_b()
    while 1: # 添加此句防止程序退出，保证线程可以执行完
        pass

if __name__ == '__main__':
    main()
```

执行过程:

```python
开始处理请求req_a
离开处理请求req_a
开始处理请求req_b
开始执行IO操作
完成处理请求req_b
完成IO操作，并执行回调函数
开始执行回调函数on_finish
ret: io result
完成执行回调函数on_finish
```

**异步的特点是程序存在多个步调，即本属于同一个过程的代码可能在不同的步调上同时执行。**

#### 协程写法实现原理

在使用回调函数写异步程序时，需将本属于一个执行逻辑（处理请求a）的代码拆分成两个函数req_a和on_finish，这与同步程序的写法相差很大。而同步程序更便于理解业务逻辑，所以我们能否用同步代码的写法来编写异步程序？

```python
import time
import thread

gen = None # 全局生成器，供long_io使用

def long_io():
    def fun():
        print("开始执行IO操作")
        global gen
        time.sleep(5)
        try:
            print("完成IO操作，并send结果唤醒挂起程序继续执行")
            gen.send("io result")  # 使用send返回结果并唤醒程序继续执行
        except StopIteration: # 捕获生成器完成迭代，防止程序退出
            pass
    thread.start_new_thread(fun, ())

def req_a():
    print("开始处理请求req_a")
    ret = yield long_io()
    print("ret: %s" % ret)
    print("完成处理请求req_a")

def req_b():
    print("开始处理请求req_b")
    time.sleep(2)
    print("完成处理请求req_b")

def main():
    global gen
    gen = req_a()
    gen.next() # 开启生成器req_a的执行
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
```

执行过程：

```python
开始处理请求req_a
开始处理请求req_b
开始执行IO操作
完成处理请求req_b
完成IO操作，并send结果唤醒挂起程序继续执行
ret: io result
完成处理请求req_a
```

#### 升级版本

我们在上面编写出的版本虽然req_a的编写方式很类似与同步代码，但是在main中调用req_a的时候却不能将其简单的视为普通函数，而是需要作为生成器对待。

现在，我们试图尝试修改，让req_a与main的编写都类似与同步代码。

```python
# coding:utf-8

import time
import thread

gen = None # 全局生成器，供long_io使用

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        global gen
        gen = f()
        gen.next()
    return wrapper

def long_io():
    def fun():
        print("开始执行IO操作")
        global gen
        time.sleep(5)
        try:
            print("完成IO操作，并send结果唤醒挂起程序继续执行")
            gen.send("io result")  # 使用send返回结果并唤醒程序继续执行
        except StopIteration: # 捕获生成器完成迭代，防止程序退出
            pass
    thread.start_new_thread(fun, ())

@gen_coroutine
def req_a():
    print("开始处理请求req_a")
    ret = yield long_io()
    print("ret: %s" % ret)
    print("完成处理请求req_a")

def req_b():
    print("开始处理请求req_b")
    time.sleep(2)
    print("完成处理请求req_b")

def main():
    req_a()
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
```

执行过程：

```python
开始处理请求req_a
开始处理请求req_b
开始执行IO操作
完成处理请求req_b
完成IO操作，并send结果唤醒挂起程序继续执行
ret: io result
完成处理请求req_a
```

#### 最终版本

刚刚完成的版本依然不理想，因为存在一个全局变量gen来供long_io使用。我们现在再次改写程序，消除全局变量gen。

```python
# coding:utf-8

import time
import thread

def gen_coroutine(f):
    def wrapper(*args, **kwargs):
        gen_f = f()  # gen_f为生成器req_a
        r = gen_f.next()  # r为生成器long_io
        def fun(g):
            ret = g.next() # 执行生成器long_io
            try:
                gen_f.send(ret) # 将结果返回给req_a并使其继续执行
            except StopIteration:
                pass
        thread.start_new_thread(fun, (r,))
    return wrapper

def long_io():
    print("开始执行IO操作")
    time.sleep(5)
    print("完成IO操作，yield回操作结果")
    yield "io result"

@gen_coroutine
def req_a():
    print("开始处理请求req_a")
    ret = yield long_io()
    print("ret: %s" % ret)
    print("完成处理请求req_a")

def req_b():
    print("开始处理请求req_b")
    time.sleep(2)
    print("完成处理请求req_b")

def main():
    req_a()
    req_b()
    while 1:
        pass

if __name__ == '__main__':
    main()
```

执行过程：

```python
开始处理请求req_a
开始处理请求req_b
开始执行IO操作
完成处理请求req_b
完成IO操作，yield回操作结果
ret: io result
完成处理请求req_a
```

**这个最终版本就是理解Tornado异步编程原理的最简易模型，但是，Tornado实现异步的机制不是线程，而是epoll，即将异步过程交给epoll执行并进行监视回调。**

**需要注意的一点是，我们实现的版本严格意义上来说不能算是协程，因为两个程序的挂起与唤醒是在两个线程上实现的，而Tornado利用epoll来实现异步，程序的挂起与唤醒始终在一个线程上，由Tornado自己来调度，属于真正意义上的协程。虽如此，并不妨碍我们理解Tornado异步编程的原理。**

## Tornado异步

### 简介

因为epoll主要是用来解决网络IO的并发问题，所以Tornado的异步编程也主要体现在网络IO的异步上，即异步Web请求。

### tornado.httpclient.AsyncHTTPClient

Tornado提供了一个异步Web请求客户端tornado.httpclient.AsyncHTTPClient用来进行异步Web请求。

#### fetch(request, callback=None)

用于执行一个web请求request，并异步返回一个tornado.httpclient.HTTPResponse响应。

request可以是一个url，也可以是一个tornado.httpclient.HTTPRequest对象。如果是url，fetch会自己构造一个HTTPRequest对象。

#### HTTPRequest

HTTP请求类，HTTPRequest的构造函数可以接收众多构造参数，最常用的如下：

- **url** (string) – 要访问的url，此参数必传，除此之外均为可选参数
- **method** (string) – HTTP访问方式，如“GET”或“POST”，默认为GET方式
- **headers** (HTTPHeaders or dict) – 附加的HTTP协议头
- **body** – HTTP请求的请求体

#### HTTPResponse

HTTP响应类，其常用属性如下：

- **code**: HTTP状态码，如 200 或 404
- **reason**: 状态码描述信息
- **body**: 响应体字符串
- **error**: 异常（可有可无）

### 测试接口

新浪IP地址库

接口说明

1.请求接口（GET）：

http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=[ip地址字串]

2.响应信息：

（json格式的）国家 、省（自治区或直辖市）、市（县）、运营商

3.返回数据格式：

```json
{"ret":1,"start":-1,"end":-1,"country":"\u4e2d\u56fd","province":"\u5317\u4eac","city":"\u5317\u4eac","district":"","isp":"","type":"","desc":""}
```

### 回调异步

```python
class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            if 1 == data["ret"]:
                self.write(u"国家：%s 省份: %s 城市: %s" % (data["country"], data["province"], data["city"]))
            else:
                self.write("查询IP信息错误")
        self.finish() # 发送响应信息，结束请求处理
```

#### tornado.web.asynchronous

此装饰器用于回调形式的异步方法，并且应该仅用于HTTP的方法上（如get、post等）。

此装饰器不会让被装饰的方法变为异步，而只是告诉框架被装饰的方法是异步的，当方法返回时响应尚未完成。只有在request handler调用了finish方法后，才会结束本次请求处理，发送响应。

不带此装饰器的请求在get、post等方法返回时自动完成结束请求处理。

### 协程异步

在上一节中我们自己封装的装饰器get_coroutine在Tornado中对应的是tornado.gen.coroutine。

```python
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24")
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            if 1 == data["ret"]:
                self.write(u"国家：%s 省份: %s 城市: %s" % (data["country"], data["province"], data["city"]))
            else:
                self.write("查询IP信息错误")
```

也可以将异步Web请求单独出来：

```python
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        rep = yield self.get_ip_info("14.130.112.24")
        if 1 == rep["ret"]:
            self.write(u"国家：%s 省份: %s 城市: %s" % (rep["country"], rep["province"], rep["city"]))
        else:
            self.write("查询IP信息错误")

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip)
        if response.error:
            rep = {"ret:0"}
        else:
            rep = json.loads(response.body)
        raise tornado.gen.Return(rep)  # 此处需要注意
```

**代码中我们需要注意的地方是get_ip_info返回值的方式，在python 2中，使用了yield的生成器可以使用不返回任何值的return，但不能return value，因此Tornado为我们封装了用于在生成器中返回值的特殊异常tornado.gen.Return，并用raise来返回此返回值。**

### 并行协程

Tornado可以同时执行多个异步，并发的异步可以使用列表或字典，如下：

```python
class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        ips = ["14.130.112.24",
            "15.130.112.24",
            "16.130.112.24",
            "17.130.112.24"]
        rep1, rep2 = yield [self.get_ip_info(ips[0]), self.get_ip_info(ips[1])]
        rep34_dict = yield dict(rep3=self.get_ip_info(ips[2]), rep4=self.get_ip_info(ips[3]))
        self.write_response(ips[0], rep1) 
        self.write_response(ips[1], rep2) 
        self.write_response(ips[2], rep34_dict['rep3']) 
        self.write_response(ips[3], rep34_dict['rep4']) 

    def write_response(self, ip, response):
        self.write(ip) 
        self.write(":<br/>") 
        if 1 == response["ret"]:
            self.write(u"国家：%s 省份: %s 城市: %s<br/>" % (response["country"], response["province"], response["city"]))
        else:
            self.write("查询IP信息错误<br/>")

    @tornado.gen.coroutine
    def get_ip_info(self, ip):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip)
        if response.error:
            rep = {"ret:1"}
        else:
            rep = json.loads(response.body)
        raise tornado.gen.Return(rep)
```

### 关于数据库的异步说明

网站基本都会有数据库操作，而Tornado是单线程的，这意味着如果数据库查询返回过慢，整个服务器响应会被堵塞。

数据库查询，实质上也是远程的网络调用；理想情况下，是将这些操作也封装成为异步的；但Tornado对此并**没有**提供任何支持。

这是Tornado的**设计**，而不是缺陷。

一个系统，要满足高流量；是必须解决数据库查询速度问题的！

数据库若存在查询性能问题，整个系统无论如何优化，数据库都会是瓶颈，拖慢整个系统！

异步并**不能**从本质上提到系统的性能；它仅仅是避免多余的网络响应等待，以及切换线程的CPU耗费。

如果数据库查询响应太慢，需要解决的是数据库的性能问题；而不是调用数据库的前端Web应用。

对于实时返回的数据查询，理想情况下需要确保所有数据都在内存中，数据库硬盘IO应该为0；这样的查询才能足够快；而如果数据库查询足够快，那么前端web应用也就无将数据查询封装为异步的必要。

就算是使用协程，异步程序对于同步程序始终还是会提高复杂性；需要衡量的是处理这些额外复杂性是否值得。

**如果后端有查询实在是太慢，无法绕过，Tornaod的建议是将这些查询在后端封装独立封装成为HTTP接口，然后使用Tornado内置的异步HTTP客户端进行调用。**

## WebSocket

### 简介

WebSocket是HTML5规范中新提出的客户端-服务器通讯协议，协议本身使用新的ws://URL格式。

WebSocket 是独立的、创建在 TCP 上的协议，和 HTTP 的唯一关联是使用 HTTP 协议的101状态码进行协议切换，使用的 TCP 端口是80，可以用于绕过大多数防火墙的限制。

WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端直接向客户端推送数据而不需要客户端进行请求，两者之间可以创建持久性的连接，并允许数据进行双向传送。

目前常见的浏览器如 Chrome、IE、Firefox、Safari、Opera 等都支持 WebSocket，同时需要服务端程序支持 WebSocket。

### Tornado的WebSocket模块

Tornado提供支持WebSocket的模块是tornado.websocket，其中提供了一个WebSocketHandler类用来处理通讯。

#### WebSocketHandler.open()

当一个WebSocket连接建立后被调用。

#### WebSocketHandler.on_message(message)

当客户端发送消息message过来时被调用，**注意此方法必须被重写**。

#### WebSocketHandler.on_close()

当WebSocket连接关闭后被调用。

#### WebSocketHandler.write_message(message, binary=False)

向客户端发送消息messagea，message可以是字符串或字典（字典会被转为json字符串）。若binary为False，则message以utf8编码发送；二进制模式（binary=True）时，可发送任何字节码。

#### WebSocketHandler.close()

关闭WebSocket连接。

#### WebSocketHandler.check_origin(origin)

判断源origin，对于符合条件（返回判断结果为True）的请求源origin允许其连接，否则返回403。可以重写此方法来解决WebSocket的跨域请求（如始终return True）。

### 前端JavaScript编写

在前端JS中使用WebSocket与服务器通讯的常用方法如下：

```javascript
var ws = new WebSocket("ws://127.0.0.1:8888/websocket"); // 新建一个ws连接
ws.onopen = function() {  // 连接建立好后的回调
   ws.send("Hello, world");  // 向建立的连接发送消息
};
ws.onmessage = function (evt) {  // 收到服务器发送的消息后执行的回调
   alert(evt.data);  // 接收的消息内容在事件参数evt的data属性中
};
```
