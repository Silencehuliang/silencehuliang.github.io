# Python学习之路-爬虫进阶:爬虫框架雏形


## 代码实现分析

### 明确模块之间的逻辑关系

五个核心模块和三个内置的对象是关键模块，需要优先实现

先抛开中间件，分析下它们之间的逻辑关系是：

1. 构造spider中start_urls中的请求
2. 传递给调取器进行保存，之后从中取出
3. 取出的request对象交给下载的进行下载，返回response
4. response交给爬虫模块进行解析，提取结果
5. 如果结果是request对象，重新交给调度器，如果结果是item对象，交给管道处理

以上的逻辑是在引擎中完成的

### 设计代码结构

1. 首先给框架起一个名称，如：

   ```
    scrapy_plus
   ```

2. 继续分类以及解耦的设计思想：

   - 把核心模块放置在一起

   - 请求对象模块和响应对象模块统一作为http模块

   - 数据对象单独作为一个分类

     代码结构如下：

     ```
     -- scrapy_plus
       -- __init__.py
       -- core
         -- __init__.py
         -- spider.py
         -- scheduler.py
         -- downloader.py
         -- pipeline.py
         -- engine.py
       -- http
         -- __init__.py
         -- request.py
         -- response.py
       -- item.py
     ```

到这里，我们完成了框架的大致结构是设计，那么接下来我们就需要实现模块中的具体内容了

## request对象的封装

对HTTP基本的请求属性进行简单封装，实现一个Request对象

```python
# scrapy/http/request.py
'''封装Request对象'''

class Request(object):
    '''框架内置请求对象，设置请求信息'''

    def __init__(self, url, method='GET',\
              headers=None, params=None, data=None):
        self.url = url    # 请求地址
        self.method = method    # 请求方法
        self.headers = headers    # 请求头
        self.params = params    # 请求参数
        self.data = data    # 请求体
```

## response对象的封装

对HTTP基本的响应属性进行简单封装，实现一个Response对象

```python
# scrapy/http/response.py
'''封装Response对象'''

class Response(object):
    '''框架内置Response对象'''
    def __init__(self, url, status_code, headers, body):
        self.url = url    # 响应url
        self.status_code = status_code    # 响应状态码
        self.headers = headers    # 响应头
        self.body = body    # 响应体
```

## item对象的封装

对数据进行简单封装，实现Item对象：

```python
# scrapy/item.py
'''item对象'''


class Item(object):
    '''框架内置Item对象'''
    def __init__(self, data):
        # data表示传入的数据
        self._data = data    # 设置为简单的私有属性

    @property
    def data(self):
      '''对外提供data进行访问，一定程度达到保护的作用'''
      return self._data
```

其中`property`的理解：

- `property` 能够让调用一个方法和调用一个属性一样容易，即不用打括号
- `property` 能够让这个属性的值是只读的，即不能够对其进行重新赋值，达到一定的保护的目的

## spider模块的封装

### 爬虫组件功能

- 构建请求信息(初始的)，也就是生成请求对象(Request)
- 解析响应对象，返回数据对象(Item)或者新的请求对象(Request)

#### 实现方案

- 实现start_requests方法，返回请求对象
- 实现parse方法，返回Item对象或者新的请求对象

```python
# scrapy_plus/core/spider.py
'''爬虫组件封装'''
from scrapy_plus.item import Item    # 导入Item对象
from scrapy_plus.http.request import Request    # 导入Request对象


class Spider(object):
    '''
    1. 构建请求信息(初始的)，也就是生成请求对象(Request)
    2. 解析响应对象，返回数据对象(Item)或者新的请求对象(Request)
    '''

    start_url = 'http://www.baidu.com'    # 默认初始请求地址   
                                      #这里以请求百度首页为例

    def start_requests(self):
        '''构建初始请求对象并返回'''
        return Request(self.start_url)

    def parse(self, response):
        '''解析请求
        并返回新的请求对象、或者数据对象
        '''
        return Item(response.body)   # 返回item对象
```

### 调度器模块的封装

#### 调度器功能

- 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度：
- 对请求对象进行去重判断：实现去重方法`_filter_request`，该方法对内提供，因此设置为私有方法

#### 实现方案

- 利用队列FIFO存储请求；
- 实现add_request方法添加请求，接收请求对象作为参数；
- 实现get_request方法对外提供从队列取出的请求对象

```python
# scrapy_plus/core/scheduler.py
'''调度器模块封住'''
# 利用six模块实现py2和py3兼容
from six.moves.queue import Queue


class Scheduler(object):
    '''
    1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重判断
    '''
    def __init__(self):
        self.queue = Queue()

    def add_request(self, request):
        '''添加请求对象'''
        self.queue.put(request)

    def get_request(self):
        '''获取一个请求对象并返回'''
        request = self.queue.get()
        return request

    def _filter_request(self):
        '''请求去重'''
        # 暂时不实现
        pass
```

### 下载器模块的封装

#### 下载器功能

根据请求对象(Request)，发起HTTP、HTTPS网络请求，拿到HTTP、HTTPS响应，构建响应对象(Response)并返回

#### 实现方案

- 利用requests、urllib2等模块发请求，这里使用requests模块
- 实现get_response方法，接收request请求对象作为参数，发起请求，获取响应

```python
# scrapy_plus/core/downloader.py
'''下载器组件'''
import requests
from scrapy_plus.http.response import Response

class Downloader(object):
    '''根据请求对象(Request)，发起HTTP、HTTPS网络请求，拿到HTTP、HTTPS响应，构建响应对象(Response)并返回'''

    def get_response(self, request):
        '''发起请求获取响应的方法'''
        # 1. 根据请求对象，发起请求，获取响应
        #    判断请求方法：
        if request.method.upper() == 'GET':
            resp = requests.get(request.url, headers=request.headers,\
                          params=request.params)
        elif request.method.upper() == 'POST':
            resp = requests.post(request.url,headers=request.headers,\
                      params=request.params,data=request.data)
        else:
            # 如果方法不是get或者post，抛出一个异常
            raise Exception("不支持的请求方法")
        # 2. 构建响应对象,并返回
        return Response(resp.url, resp.status_code, resp.headers, resp.content)
```

### 管道模块的封装

#### 管道组件功能

负责处理数据对象

#### 实现方案

- 实现process_item方法，接收数据对象作为参数

```python
# scrapy_plus/core/pipeline.py
'''管道组件封装'''


class Pipeline(object):
    '''负责处理数据对象(Item)'''

    def process_item(self, item):
        '''处理item对象'''
        print("item: ", item)
```

### 引擎模块的封装

#### 引擎组件功能

- 对外提供整个的程序的入口
- 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)

#### 实现方案

- 利用init方法初始化其他组件对象，在内部使用
- 实现start方法，由外部调用，启动引擎
- 实现`_start_engine`方法，完成整个框架的运行逻辑
- 具体参考上一小节中雏形结构引擎的逻辑

```python
# scrapy_plus/core/engine.py
'''引擎组件'''
from scrapy_plus.http.request import Request    # 导入Request对象

from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline
from .spider import Spider


class Engine(object):
    '''
    a. 对外提供整个的程序的入口
    b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    '''

    def __init__(self):
        self.spider = spider()    # 接收爬虫对象
        self.scheduler = Scheduler()    # 初始化调度器对象
        self.downloader = Downloader()    # 初始化下载器对象
        self.pipeline = Pipeline()    # 初始化管道对象

    def start(self):
        '''启动整个引擎'''
        self._start_engine()

    def _start_engine(self):
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        # 1. 爬虫模块发出初始请求
        start_request = self.spider.start_requests()

        # 2. 把初始请求添加给调度器
        self.scheduler.add_request(start_request)
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)

        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        result = self.spider.parse(response)
        # 6. 判断结果对象
        # 6.1 如果是请求对象，那么就再交给调度器
        if isinstance(result, Request):
            self.scheduler.add_request(result)
        # 6.2 否则，就交给管道处理
        else:
            self.pipeline.process_item(result)
```


