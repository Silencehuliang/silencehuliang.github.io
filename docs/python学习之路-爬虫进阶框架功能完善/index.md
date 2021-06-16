# Python学习之路-爬虫提高:框架功能完善


## 完善框架的基础功能

`项目`中除了实现main.py以外，还需要实现：

- 项目配置文件
- 爬虫文件
- 管道文件
- 中间件文件

`框架`中还需要实现：

- 框架配置文件，并且需要实现导入项目配置文件，同时覆盖默认配置文件的属性
- 支持多个爬虫的传入以及使用
- 支持多个管道的传入以及使用
- 支持多个中间件的传入以及使用

## 日志模块的使用

### 为什么要使用添加日志功能

1. 能够方便的对程序进行调试
2. 能够记录程序的运行状态，包括错误

### 日志模块简单使用

- 日志的等级

```python
import logging
# 日志的五个等级，等级依次递增
# 默认是WARNING等级
logging.DEBUG
logging.INFO
logging.WARNING
logging.ERROR
logging.CRITICAL
# 设置日志等级
logging.basicConfig(level=logging.INFO)
# 使用
logging.debug('DEBUG')
logging.info('INFO')
logging.warning('WARNING')
logging.error('ERROR')
logging.critical('CRITICAL')
```

- 捕获异常信息到日志。这里主要需要进行捕获异常才能记录下完整的异常信息

```Python
try:
    raise Exception("异常")
except Exception as e:
    logging.exception(e)
```

- 日志的输出格式 对于日志的输出格式，我们能够进行自定义，包括输出的`内容格式`和`时间格式`

format格式说明：

```txt
      %(name)s  Logger的名字
      %(levelno)s 数字形式的日志级别
      %(levelname)s 文本形式的日志级别
      %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
      %(filename)s 调用日志输出函数的模块的文件名
      %(module)s 调用日志输出函数的模块名
      %(funcName)s 调用日志输出函数的函数名
      %(lineno)d 调用日志输出函数的语句所在的代码行
      %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
      %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
      %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
      %(thread)d 线程ID。可能没有
      %(threadName)s 线程名。可能没有
      %(process)d 进程ID。可能没有
      %(message)s 用户输出的消息
```

- datefmt参数说明：

  ```
  %y 两位数的年份表示（00-99）
  %Y 四位数的年份表示（000-9999）
  %m 月份（01-12）
  %d 月内中的一天（0-31）
  %H 24小时制小时数（0-23）
  %I 12小时制小时数（01-12）
  %M 分钟数（00=59）
  %S 秒（00-59）
  %a 本地简化星期名称
  %A 本地完整星期名称
  %b 本地简化的月份名称
  %B 本地完整的月份名称
  %c 本地相应的日期表示和时间表示
  %j 年内的一天（001-366）
  %p 本地A.M.或P.M.的等价符
  %U 一年中的星期数（00-53）星期天为星期的开始
  %w 星期（0-6），星期天为星期的开始
  %W 一年中的星期数（00-53）星期一为星期的开始
  %x 本地相应的日期表示
  %X 本地相应的时间表示
  %Z 当前时区的名称
  %% %号本身
  ```

### 利用logger封装日志模块

在scrapy_plus目录下建立utils包 (utility：工具)，专门放置工具类型模块，如日志模块`log.py` 下面的代码内容是固定的，在任何地方都可以使用下面的代码实习日志内容的输出

```Python
# scrapy_plus/utils/log.py
import sys
import logging

# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称


class Logger(object):

    def __init__(self):
        # 1. 获取一个logger对象
        self._logger = logging.getLogger()
        # 2. 设置format对象
        self.formatter = logging.Formatter(fmt=DEFAULT_LOG_FMT,datefmt=DEFUALT_LOG_DATEFMT)
        # 3. 设置日志输出
        # 3.1 设置文件日志模式
        self._logger.addHandler(self._get_file_handler(DEFAULT_LOG_FILENAME))
        # 3.2 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 4. 设置日志等级
        self._logger.setLevel(DEFAULT_LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''返回一个文件日志handler'''
        # 1. 获取一个文件日志handler
        filehandler = logging.FileHandler(filename=filename,encoding="utf-8")
        # 2. 设置日志格式
        filehandler.setFormatter(self.formatter)
        # 3. 返回
        return filehandler

    def _get_console_handler(self):
        '''返回一个输出到终端日志handler'''
        # 1. 获取一个输出到终端日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 2. 设置日志格式
        console_handler.setFormatter(self.formatter)
        # 3. 返回handler
        return console_handler

    @property
    def logger(self):
        return self._logger

# 初始化并配一个logger对象，达到单例的
# 使用时，直接导入logger就可以使用
logger = Logger().logger
```

### 在框架中使用日志模块

使用参考

```Python
# scrapy_plus/core/engine.py
from datetime import datetime

from scrapy_plus.http.request import Request    # 导入Request对象
from scrapy_plus.middlewares.spider_middlewares import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddleware
from scrapy_plus.utils.log import logger    # 导入logger

from .spider import Spider
from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline


class Engine(object):

    ......

    def start(self):
        '''启动整个引擎'''
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时

......
```

## 框架中实现配置文件

### 实现框架的默认配置文件

在scrapy_plus下建立conf包文件夹在它下面建立default_settings.py：设置默认配置的配置

```Python
import logging

# 默认的日志配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s[line:%(lineno)d] \
                  %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称
```

再在conf下创建settings.py文件

```Python
# scrapy_plus/conf/settings
from .default_settings import *    # 全部导入默认配置文件的属性
```

### 在框架中使用

利用框架配置文件改写`log.py`

```Python
# scrapy_plus/utils/log.py
import sys
import logging

from scrapy_plus.conf import settings    # 导入框架的settings文件


class Logger(object):

    def __init__(self):
        # 1. 获取一个logger对象
        self._logger = logging.getLogger()
        # 2. 设置format对象
        self.formatter = logging.Formatter(fmt=settings.DEFAULT_LOG_FMT,datefmt=settings.DEFUALT_LOG_DATEFMT)
        # 3. 设置日志输出
        # 3.1 设置文件日志模式
        self._logger.addHandler(self._get_file_handler(settings.DEFAULT_LOG_FILENAME))
        # 3.2 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 4. 设置日志等级
        self._logger.setLevel(settings.DEFAULT_LOG_LEVEL)

......
```

### 创建项目配置文件，并实现修改框架默认配置文件属性

项目文件夹下创建项目配置文件`settings.py`:

```Python
# project_dir/settings.py
# 修改默认日志文件名称
DEFAULT_LOG_FILENAME = '日志.log'    # 默认日志文件名称
```

修改框架的settings.py文件，实现修改默认配置文件属性的目的

```Python
# scrapy_plus/conf/settings
from .default_settings import *    # 全部导入默认配置文件的属性
# 这里导入的settings，是项目文件夹的settings文件
from settings import *
```

## 多爬虫实现

### 多请求实现

#### 需求分析

在发送关于start_url中的请求的时候，往往我们的请求并不是只有一个，而且在解析了响应之后，可能需要继续构造请求并且发送，那么对应的需要在引擎中进行修改。

#### 项目中实现爬虫文件

- 在main.py同级目录下建立`spiders.py`，存放定义的爬虫类

  ```python
    # project_dir/spiders.py
    from scrapy_plus.core.spider import Spider
  
    # 继承框架的爬虫基类
    class BaiduSpider(Spider):
  
        start_url = 'http://www.baidu.com'    # 设置初始请求url
  ```

- 修改`main.py`

  ```python
    # project_dir/main.py
    from scrapy_plus.core.engine import Engine    # 导入引擎
  
    from spiders import BaiduSpider
  
    if __name__ == '__main__':
        spider = BaiduSpider()    # 实例化爬虫对象
        engine = Engine(spider)    # 传入爬虫对象
        engine.start()    # 启动引擎
  ```

- 修改`engine.py`，设置为接收外部传入的爬虫对象

  ```python
    # scrapy_plus/core/engine.py
    ...
    class Engine(object):
  
        def __init__(self, spider):    # 接收外部传入的爬虫对象
            self.spider = spider    # 爬虫对象
            self.scheduler = Scheduler()    # 初始化调度器对象
            self.downloader = Downloader()    # 初始化下载器对象
            self.pipeline = Pipeline()    # 初始化管道对象
  
            self.spider_mid = SpiderMiddleware()
            self.downloader_mid = DownloaderMiddleware()
    ...
  ```

### 实现发起多个请求

#### 修改框架的爬虫组件文件 `spider.py`:

- 设置为初始请求url为多个
- 修改start_requests方法，将返回多个请求对象
- 利用生成器方式实现start_requests，提高程序的资源消耗

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

    start_urls = []    # 默认初始请求地址

    # def start_requests(self):
    #     '''构建初始请求对象并返回'''
    #     request_list = []
    #     for url in self.start_urls:
    #         request_list.append(Request(url))
    #     return request_list

    # 利用生成器方式实现，提高程序的资源消耗
    def start_requests(self):
        '''构建初始请求对象并返回'''
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        '''解析请求
        并返回新的请求对象、或者数据对象
        返回值应当是一个容器，如start_requests返回值方法一样，改为生成器即可
        '''
        yield Item(response.body)   # 返回item对象 改为生成器即可
```

#### 修改引擎 `engine.py`

- 将代码拆分为两个方法，便于维护，提高代码可读性
- 统计总共完成的响应数
- 设置程序退出条件：当总响应数等于总请求数时，退出
- 实现处理start_requests方法返回多个请求的功能
- 实现处理parse解析函数返回多个对象的功能

```python
# scheduler/core/engine.py
'''引擎
a. 对外提供整个的程序的入口
b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
'''
import time
from datetime import datetime

from .downloader import Downloader
from .pipeline import  Pipeline
from .scheduler import  Scheduler
from .spider import Spider

from scrapy_plus.http.request import Request
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddleware
from scrapy_plus.middlewares.spider_middlewares import SpiderMiddleware
from scrapy_plus.utils.log import logger

class Engine:
    '''完成对引擎模块的封装'''

    def __init__(self,spider):
        '''
        实例化其他的组件，在引起中能够通过调用组件的方法实现功能
        '''
        # self.spider = Spider()
        self.spider = spider
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.scheduler = Scheduler()
        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()
        self.total_request_nums = 0
        self.total_response_nums = 0


    def start(self):
        '''
        提供引擎启动的入口
        :return:
        '''
        start_time = datetime.now()
        logger.info("爬虫启动：{}".format(start_time))
        self._start_engine()
        end_time = datetime.now()
        logger.info("爬虫结束：{}".format(start_time))
        logger.info("爬虫一共运行：{}秒".format((end_time-start_time).total_seconds()))
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))


    def _start_request(self):
        for start_request in self.spider.start_requests():
            #1. 对start_request进过爬虫中间件进行处理
            start_request = self.spider_mid.process_request(start_request)

            #2. 调用调度器的add_request方法，添加request对象到调度器中
            self.scheduler.add_request(start_request)
            #请求数+1
            self.total_request_nums += 1

    def _execute_request_response_item(self):
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

        #request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        #4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        #response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        #response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        #5. 调用爬虫的parse方法，处理响应
        for result in self.spider.parse(response):
            #6.判断结果的类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                #在解析函数得到request对象之后，使用process_request进行处理
                result = self.spider_mid.process_request(result)
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            #7如果不是，调用pipeline的process_item方法处理结果
            else:
                self.pipeline.process_item(result)

        self.total_response_nums += 1

    def _start_engine(self):
        '''
        具体的实现引擎的细节
        :return:
        '''
        self._start_request()
        while True:
            time.sleep(0.001)
            self._execute_request_response_item()
            if self.total_response_nums>= self.total_request_nums:
                break
```

#### 修改调度器 `scheduler.py`：

- 将从队列获取请求对象设置为非阻塞，否则会造成程序无法退出
- 统计请求总数，用于判断程序退出

```python
# scrapy_plus/core/scheduler.py
'''调度器模块封装'''
# 利用six模块实现py2和py3兼容
from six.moves.queue import Queue


class Scheduler(object):
    '''
    1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重判断
    '''
    def __init__(self):
        self.queue = Queue()
        # 记录总共的请求数
        self.total_request_number = 0

    def add_request(self, request):
        '''添加请求对象'''
        self.queue.put(request)
        self.total_request_number += 1    # 统计请求总数

    def get_request(self):
        '''获取一个请求对象并返回'''
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def _filter_request(self):
        '''请求去重'''
        pass
```

## 爬虫实现多个解析函数

### 响应对象的解析方法封装

为response对象封装xpath、正则、json、等方法和属性，以支持对数据的解析和提取

```Python
# scrapy_plus/http/response.py
import re
import json

from lxml import etree


class Response(object):
    '''框架内置Response对象'''
    def __init__(self, url, status_code, headers, body):
        self.url = url    # 响应url
        self.status_code = status_code    # 响应状态码
        self.headers = headers    # 响应头
        self.body = body    # 响应体

    def xpath(self, rule):
        '''提供xpath方法'''
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        '''提供json解析
        如果content是json字符串，是才有效
        '''
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        '''封装正则的findall方法'''
        if data is None:
            data = self.body
        return re.findall(rule, data)
```

### 实现多个解析函数

由于现在不同的请求对应不同的解析函数，因此需要为请求对象指明它的解析函数，因此为请求对象增加一个属性

```Python
# scrapy_plus/http/request.py
class Request(object):
    '''框架内置请求对象，设置请求信息'''

    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse'):
        self.url = url    # 请求地址
        self.method = method    # 请求方法
        self.headers = headers    # 请求头
        self.params = params    # 请求参数
        self.data = data    # 请求体
        self.parse = parse    # 指明它的解析函数, 默认是parse方法
        self.meta = None
# scrapy_plus/http/response.py
class Response:
    '''完成对响应对象的封装'''

    def __init__(self, url, body, headers, status_code, meta={}):
        '''
        初始化resposne对象
        :param url: 响应的url地址
        :param body: 响应体
        :param headers:  响应头
        :param status_code: 状态码
        '''
        self.url = url
        self.headers = headers
        self.status_code = status_code
        self.body = body
        self.meta = meta
```

### 在引擎中需要动态的判断和获取对应的解析函数

```Python
# scrapy_plus/core/engine.py
class Engine(object):

    ......

    def _execute_request_response_item(self):
        '''根据请求、发起请求获取响应、解析响应、处理响应结果'''

        ......

       #request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        #4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        response.meta = request.meta

        #response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        #response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        #parse方法
        parse = getattr(self.spider,request.parse)

        #5. 调用爬虫的parse方法，处理响应
        for result in parse(response):
            #6.判断结果的类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                #在解析函数得到request对象之后，使用process_request进行处理
                result = self.spider_mid.process_request(result)
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            #7如果不是，调用pipeline的process_item方法处理结果
            else:
                self.pipeline.process_item(result)

        self.total_response_nums += 1

        ......
```

## 多爬虫文件

### 为什么需要优化现有的爬虫结构

当爬虫比较少的时候，我们的项目结构相对合理，但是当要抓取的网站比较多的时候，可以借鉴scrapy的方法，把不同网站的爬虫分别在不同的py文件中编写，之后放在一个目录下；同时，我们很多时候还希望能够有同时启动项目中的所有的爬虫

### 同时执行多个不同的爬虫

可以将多个爬虫一起启动并执行，传入形式可以使用字典传入多个爬虫

在引擎中用到爬虫对象的地方都要做相应的修改

`engine.py`：

```python
'''引擎
a. 对外提供整个的程序的入口
b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
'''
......
class Engine(object):

    def __init__(self, spiders):    # 接收外部传入的多个爬虫对象
        self.spiders = spiders    # 爬虫对象

        ......

    ......

    def _start_requests(self):
        '''向调度器添加初始请求'''
        # 1. 爬虫模块发出初始请求
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                # 2. 把初始请求添加给调度器
                # 利用爬虫中间件预处理请求对象
                start_request = self.spider_mid.process_request(start_request)
                start_request.spider_name = spider_name    #为请求对象绑定它所属的爬虫的名称
                self.scheduler.add_request(start_request)

    def _execute_request_response_item(self):
        '''根据请求、发起请求获取响应、解析响应、处理响应结果'''

        ......

        spider = self.spiders[request.spider_name]  # 根据请求的spider_name属性，获取对应的爬虫对象

        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        parse = getattr(spider, request.parse)    # 获取对应的解析函数
        results = parse(response)    # parse函数的返回值是一个容器，如列表或者生成器对象
        for result in results:
           # 6. 判断结果对象
           # 6.1 如果是请求对象，那么就再交给调度器
           if isinstance(result, Request):
               # 利用爬虫中间件预处理请求对象
               result = self.spider_mid.process_request(result)
               result.spider_name = request.spider_name  # 为请求对象绑定它所属的爬虫的名称
               self.scheduler.add_request(result)
           # 6.2 否则，就交给管道处理
           ......
    ......
```

安装代码，并运行`main.py`，直到调试成功

最后将每个爬虫的名称直接设置为爬虫类的一个属性

## 实现多个管道

###  为什么需要多个管道

同爬虫文件一样，不同的爬虫可能需要不同的管道文件，因此管道文件需要在项目中进行实现

### 项目文件夹中实现管道文件

在项目文件夹下建立pipelines.py文件，不同在于：

- 这里的process_item必须把item对象最后再返回回来，因为是多个管道文件的设置了
- 需要增加一个参数，也就是传入爬虫对象，以此来判断当前item是属于那个爬虫对象的

### 修改引擎的代码

- 管道对象将从外部传入
- 调用管道的process_item方法时，需要遍历出管道
- 并且需要传递第二个参数，爬虫对象

```python
# scrapy_plus/core/engine.py
......

class Engine:
    '''完成对引擎模块的封装'''

    def __init__(self,spiders,pipelines=[]):
        '''
        实例化其他的组件，在引起中能够通过调用组件的方法实现功能
        '''
        # self.spider = Spider()
        self.spiders = spiders
        self.downloader = Downloader()
        self.pipelines = pipelines
        self.scheduler = Scheduler()
        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()
        self.total_request_nums = 0
        self.total_response_nums = 0


    def start(self):
        '''
        提供引擎启动的入口
        :return:
        '''
        start_time = datetime.now()
        logger.info("爬虫启动：{}".format(start_time))
        self._start_engine()
        end_time = datetime.now()
        logger.info("爬虫结束：{}".format(start_time))
        logger.info("爬虫一共运行：{}秒".format((end_time-start_time).total_seconds()))
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))


    def _start_request(self):
        for spider_name,spider in self.spiders.items():
            for start_request in spider.start_requests():
                #1. 对start_request进过爬虫中间件进行处理
                start_request = self.spider_mid.process_request(start_request)
                start_request.spider_name = spider_name

                #2. 调用调度器的add_request方法，添加request对象到调度器中
                self.scheduler.add_request(start_request)
                #请求数+1
                self.total_request_nums += 1

    def _execute_request_response_item(self):
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

        #request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        #4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        response.meta = request.meta

        #response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        #response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        #parse方法
        spider = self.spiders[request.spider_name]
        parse = getattr(spider,request.parse)

        #5. 调用爬虫的parse方法，处理响应
        for result in parse(response):
            #6.判断结果的类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                #在解析函数得到request对象之后，使用process_request进行处理
                result = self.spider_mid.process_request(result)
                result.spider_name = request.spider_name
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            #7如果不是，调用pipeline的process_item方法处理结果
            else:
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result,spider)

        self.total_response_nums += 1
......
```

### 修改`main.py`

为引擎传入项目中的管道对象

## 实现项目中传入多个中间件

### 为什么需要多个中间件

不同的中间件可以实现对请求或者是响应对象进行不同的处理，通过不同的中间件实现不同的功能，让逻辑更加清晰

### 在项目文件夹中创建middlewares文件

- 项目文件夹中的spider_middlewares.py：

  ```Python
  class TestSpiderMiddleware1(object):
  
      def process_request(self, request):
          '''处理请求头，添加默认的user-agent'''
          print("TestSpiderMiddleware1: process_request")
          return request
  
      def process_item(self, item):
          '''处理数据对象'''
          print("TestSpiderMiddleware1: process_item")
          return item
  
  class TestSpiderMiddleware2(object):
  
      def process_request(self, request):
          '''处理请求头，添加默认的user-agent'''
          print("TestSpiderMiddleware2: process_request")
          return request
    
      def process_item(self, item):
          '''处理数据对象'''
          print("TestSpiderMiddleware2: process_item")
          return item
  ```




- 项目文件夹中的downloader_middlewares.py:

  ```Python
  class TestDownloaderMiddleware1(object):
  
      def process_request(self, request):
          '''处理请求头，添加默认的user-agent'''
          print("TestDownloaderMiddleware1: process_request")
          return request
  
      def process_response(self, item):
          '''处理数据对象'''
          print("TestDownloaderMiddleware1: process_response")
          return item
  
  class TestDownloaderMiddleware2(object):
  
      def process_request(self, request):
          '''处理请求头，添加默认的user-agent'''
          print("TestDownloaderMiddleware2: process_request")
          return request
  
      def process_response(self, item):
          '''处理数据对象'''
          print("TestDownloaderMiddleware2: process_response")
          return item
  ```

### 修改项目文件夹中的`main.py`

为引擎传入多个中间件

### 因此相应的的修改`engine.py`

改为使用多个中间件

```Python
# scrapy_plus/core/engine.py
.....

class Engine:
    '''完成对引擎模块的封装'''

    def __init__(self,spiders,pipelines=[],spider_mids=[],downloader_mids=[]):
        '''
        实例化其他的组件，在引起中能够通过调用组件的方法实现功能
        '''
        # self.spider = Spider()
        self.spiders = spiders
        self.downloader = Downloader()
        self.pipelines = pipelines
        self.scheduler = Scheduler()
        self.spider_mids = spider_mids
        self.downloader_mids = downloader_mids
        self.total_request_nums = 0
        self.total_response_nums = 0


    def start(self):
        '''
        提供引擎启动的入口
        :return:
        '''
        start_time = datetime.now()
        logger.info("爬虫启动：{}".format(start_time))
        self._start_engine()
        end_time = datetime.now()
        logger.info("爬虫结束：{}".format(start_time))
        logger.info("爬虫一共运行：{}秒".format((end_time-start_time).total_seconds()))
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))


    def _start_request(self):
        for spider_name,spider in self.spiders.items():
            for start_request in spider.start_requests():
                #1. 对start_request进过爬虫中间件进行处理
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                start_request.spider_name = spider_name

                #2. 调用调度器的add_request方法，添加request对象到调度器中
                self.scheduler.add_request(start_request)
                #请求数+1
                self.total_request_nums += 1

    def _execute_request_response_item(self):
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

        #request对象经过下载器中间件的process_request进行处理
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        #4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        response.meta = request.meta

        #response对象经过下载器中间件的process_response进行处理
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)
        #response对象经过下爬虫中间件的process_response进行处理
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)

        #parse方法
        spider = self.spiders[request.spider_name]
        parse = getattr(spider,request.parse)

        #5. 调用爬虫的parse方法，处理响应
        for result in parse(response):
            #6.判断结果的类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                #在解析函数得到request对象之后，使用process_request进行处理
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                result.spider_name = request.spider_name
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            #7如果不是，调用pipeline的process_item方法处理结果
            else:
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result,spider)

        self.total_response_nums += 1

    def _start_engine(self):
        '''
        具体的实现引擎的细节
        :return:
        '''
        self._start_request()
        while True:
            time.sleep(0.001)
            self._execute_request_response_item()
            if self.total_response_nums>= self.total_request_nums:
                break
    ......
```

## 动态导入模块

### 目前代码存在的问题

通过前面的代码编写，我们已经能够完成大部分的任务，但是在`main.py` 中的代码非常臃肿，对应的我们可以再`settings.py` 配置哪些爬虫，管道，中间件需要开启，能够让整个代码的逻辑更加清晰

### 模块动态导入的方法

- 利用`importlib.import_modle`能够传入模块的路径，即可即可实现根据模块的位置的字符串，导入该模块的功能
- 在项目路径下新建`test.py`观察现象，插入如下代码观察现象

### 在settings中设置SPIDER，MIDDLEWARES

利用在配置文件中设置需要启用的爬虫类、管道类、中间件类

利用importlib模块，在引擎中动态导入并实例化

```Python
  ....
  from scrapy_plus.conf.settings import SPIDERS, PIPELINES, \
      SPIDER_MIDDLEWARES,DOWNLOADER_MIDDLEWARES

  class Engine:
      '''完成对引擎模块的封装'''

      def __init__(self):
          '''
          实例化其他的组件，在引起中能够通过调用组件的方法实现功能
          '''
          self.spiders = self._auto_import_instances(SPIDERS,isspider=True)
          self.downloader = Downloader()
          self.scheduler = Scheduler()

          self.pipelines = self._auto_import_instances(PIPELINES)
          self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)
          self.downloader_mids =self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
          self.total_request_nums = 0
          self.total_response_nums = 0

      def _auto_import_instances(self,path=[],isspider=False):
          '''通过配置文件，动态导入类并实例化
          path: 表示配置文件中配置的导入类的路径
          isspider: 由于爬虫需要返回的是一个字典，因此对其做对应的判断和处理
          '''
          # 该方法不仅实例化动态导入爬虫，还有管道和中间件，而前者返回应是字典类型
          if isspider is True:
              instances = {}
          else:
              instances = []    # 存储对应类的实例对象

          for p in path:
              module_name = p.rsplit(".",1)[0]    # 取出模块名称
              cls_name = p.rsplit(".",1)[1]    # 取出类名称
              ret = importlib.import_module(module_name)    # 动态导入爬虫模块
              cls = getattr(ret, cls_name)    # 根据类名称获取类对象
              if isspider is True:
                  instances[cls.name] = cls()
              else:
                  instances.append(cls())    # 实例化类对象
          return instances    # 返回类对象
  ......
```

### 修改`main.py`

这样main.py就不用再导入并传入那么多对象了：

```Python
# project_dir/main.py
from scrapy_plus.core.engine import Engine    # 导入引擎

if __name__ == '__main__':
    engine = Engine()  # 创建引擎对象
    engine.start()    # 启动引擎
```

## 去重原理

### 去重的理解

其实就只是对以往数据进行一个比对，判断是否已经存在

可大致分为：对原始数据比对、对利用原始数据生成的特征值进行比对两种方式

原始数据比对很好理解，就是比对的时候参照值就是原始数据；而利用特征值比对，比如最典型的就是利用原始数据生成一个指纹，比对的参照值就是这个指纹，不是原始数据本身，主要应用于单个原始数据比较大的情况，另外一种常用就是布隆过滤器，这种方式原始利用一种"特征值"，应用场景是海量数据的去重(但具有一定几率的误判)。

### 爬虫请求去重原理和实现

根据请求的url、请求方法、请求参数、请求体进行唯一标识，进行比对，由于这四个数据加到一起，内容较长，因此使用求指纹的方式来进行去重判断。

指纹计算方法，最常用的就是md5、sha1等hash加密算法，来求指纹

具体实现如下：

```Python
# scrapy_plus/core/scheduler.py
# 利用six模块实现py2和py3兼容
# coding=utf-8
# from six.moves.queue import Queue
from scrapy_plus.utils.log import logger
import w3lib.url
from hashlib import sha1
import six
from scrapy_plus.utils.queue import Queue
from scrapy_plus.utils.set import RedisFilterContainer,NoramlFilterContainer
from scrapy_plus.conf.settings import SCHEDULER_PERSIST


class Scheduler:

    def __init__(self,collector):
        self.queue = Queue()
        self._filter_container = set()
        self.repeate_request_num = 0 #统计重复的数量

    def add_request(self, request):
        if self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        try:
            return self.queue.get(False)
        except:
            return None

    def _filter_request(self, request):
        # 去重容器：存储已经发过的请求的特征 url    选用集合类型：set()
        # 利用请求的url method data  求出一个指纹  利用sha1
        request.fp = self._gen_fp(request)
        if request.fp not in self._filter_container:
            self._filter_container.add_fp(request.fp)
            # logger.info("添加新的请求：<%s>" % request.url)
            return True
        else:
            logger.info("发现重复的请求：<%s>" % request.url)
            self.repeate_request_num +=1
            return False

    def _gen_fp(self, request):
        '''请求去重，计算指纹'''
        # 用来判断请求是否重复的属性：url，method，params，data
        # 为保持唯一性，需要对他们按照同样的排序规则进行排序
        # 1. url排序：借助w3lib.url模块中的canonicalize_url方法
        url = w3lib.url.canonicalize_url(request.url)
        # 2. method不需要排序，只要保持大小写一致就可以
        method = request.method.upper()
        # 4. data排序：如果有提供则是一个字典，如果没有则是空字典
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x: x[0])

        # 5. 利用sha1算法，计算指纹
        s1 = sha1()
        # 为了兼容py2和py3，利用_to_bytes方法，把所有的字符串转化为字节类型
        s1.update(self._to_bytes(url))
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp

    @staticmethod
    def _to_bytes(string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:  #如果是python2的unicode类型，转化为字节类型
                return string.encode("utf-8")
        elif six.PY3:
            if isinstance(string, str): #如果是python3的str类型，转化为字节类型
                return string.encode("utf-8")
            else:
                return string
```

### 修改engine模块

现在统计了总的重复数量，所以，在engine中阻塞的位置判断程序结束的条件：成功的响应数+重复的数量>=总的请求数量程序结束

```python
#scrapy_plus/core/engine.py
.....
def _start_engine(self):
        '''
        具体的实现引擎的细节
        :return:
        '''
        self._start_request()
        while True:
            time.sleep(0.001)
            self._execute_request_response_item()
            #成功的响应数+重复的数量>=总的请求数量 程序结束
            if self.total_response_nums+self.scheduler.repeat_request_number >= self.total_request_nums:
                break
.....
```

## 利用线程池实现异步

### 异步任务分析：

在引擎中，实现的主要功能如下

- 上面的方框中是关于start_urls中的请求处理
- 下面的方框中是一个请求从调度器取出请求，进行下载之后交给爬虫解析再交给管道的过程 在以上两个过程中，他们之间没有直接的联系，都可以通过异步多线程的方式分别实现，加快程序执行的速度 

那么具体该如何实现该逻辑

- multiprocessing.dummy 提供的Pool 类具有apply_async的方法，能够异步的执行让他运行的函数
- apply_async方法能够接收一个callback，即其中的函数执行完成之后继续会做的事情，在这里，我们可以定义一个callback，其中让他继续执行上图中下方框的任务，同时给他一个停止条件，

### 利用回调实现循环

利用回调实现递归，可以达到循环的目的

```Python
# scrapy_plus/core/engine.py
import time
from multiprocessing.dummy import Pool    # 导入线程池对象
import importlib
from datetime import datetime

from scrapy_plus.http.request import Request    # 导入Request对象
from scrapy_plus.utils.log import logger    # 导入logger
from scrapy_plus.conf import settings

from .scheduler import Scheduler
from .downloader import Downloader


class Engine(object):
    '''
    a. 对外提供整个的程序的入口
    b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    '''

    def __init__(self):

        self.scheduler = Scheduler()    # 初始化调度器对象
        self.downloader = Downloader()    # 初始化下载器对象

        self.spiders = self._auto_import_instances(settings.SPIDERS, True)  # 动态导入并实例化爬虫对象
        self.pipelines = self._auto_import_instances(settings.PIPELINES)  # 动态导入并实例化管道对象
        self.spider_mids = self._auto_import_instances(settings.SPIDER_MIDDLEWARES)  # 动态导入并实例化爬虫中间件对象
        self.downloader_mids = self._auto_import_instances(settings.DOWNLOADER_MIDDLEWARES)  # 动态导入并实例化下载器中间件对象

        self.total_response_number = 0

        self.pool = Pool()  # 创建线程池对象
        self.running = False  # 记录是否退出程序的状态

    def start(self):
        '''启动整个引擎'''
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时

    def _start_requests(self):
        '''向调度器添加初始请求'''
        # 1. 爬虫模块发出初始请求
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                # 2. 把初始请求添加给调度器
                # 利用爬虫中间件预处理请求对象
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                start_request.spider_name = spider_name  # 为请求对象绑定它所属的爬虫的名称
                self.scheduler.add_request(start_request)

    def _execute_request_response_item(self):
        '''根据请求、发起请求获取响应、解析响应、处理响应结果'''
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        if request is None:
            return
        # 利用下载器中间件预处理请求对象
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)
        # 利用下载器中间件预处理响应对象
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        spider = self.spiders[request.spider_name]  # 根据请求的spider_name属性，获取对应的爬虫对象

        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        parse = getattr(spider, request.parse)    # 获取对应的解析函数
        results = parse(response)    # parse函数的返回值是一个容器，如列表或者生成器对象
        for result in results:
            # 6. 判断结果对象
            # 6.1 如果是请求对象，那么就再交给调度器
            if isinstance(result, Request):
                # 利用爬虫中间件预处理请求对象
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                result.spider_name = request.spider_name  # 为请求对象绑定它所属的爬虫的名称
                self.scheduler.add_request(result)
            # 6.2 否则，就交给管道处理
            else:
                # 利用爬虫中间件预处理数据对象
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_item(result)
                for pipeline in self.pipelines:    # 多个管道对象，轮流处理item对象
                    result = pipeline.process_item(result, spider)

        # 统计响应总数
        self.total_response_number += 1

    def _callback(self, temp):
        '''执行新的请求的回调函数，实现循环'''
        if self.running is True:  # 如果还没满足退出条件，那么继续添加新任务，否则不继续添加，终止回调函数，达到退出循环的目的
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        self.running = True  # 启动引擎，设置状态为True
        # 向调度器添加初始请求
        self.pool.apply_async(self._start_requests)  # 使用异步

        self.pool.apply_async(self._execute_request_response_item, callback=self._callback)  # 利用回调实现循环

        # 设置循环，处理多个请求
        while True:
            time.sleep(0.0001)  # 避免cpu空转，消耗性能

            # 根据请求、发起请求获取响应、解析响应、处理响应结果
            # self._execute_request_response_item()

            # 设置退出条件：当请求数和响应数相等时，退出循环
            # 因为异步，需要增加判断，请求数不能为0
            if self.total_response_number >= self.scheduler.total_request_number and self.scheduler.total_request_number != 0:
                self.running = False  # 满足循环退出条件后，设置运行状态为False
                break

        self.pool.close()
        self.pool.join()
```

### 实现异步并发控制

在配置文件中设置最大并发数，并在引擎中使用

```Python
# scrapy_plus/core/engine.py
class Engine(object):

    ......

    def _start_engine(self):
        self.running = True
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        # 向调度器添加初始请求
        self.pool.apply_async(self._start_requests)    # 使用异步

        # 控制最大并发数
        for i in range(settings.MAX_ASYNC_NUMBER):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)    # 利用回调实现循环

        while True:
            time.sleep(0.0001)    # 避免cpu空转，消耗性能
            # 设置退出条件：当请求数和响应数相等时，退出循环
            # 因为异步，需要增加判断，请求数不能为0
            if self.total_response_number >= self.scheduler.total_request_number and self.scheduler.total_request_number != 0:
                self.running = False    # 满足循环退出条件后，设置运行状态为False
                break
        self.pool.close()
        self.pool.join()
```

### 对异步任务进行异常控制，增加异常回调函数error_callback

```Python
# scrapy_plus/core/engine.py
class Engine(object):

    ......

    def _callback(self, temp):
        '''执行新的请求的回调函数，实现循环'''
        if self.running is True:    # 如果还没满足退出条件，那么继续添加新任务，否则不继续添加，终止回调函数，达到退出循环的目的
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)

    def _error_callback(self, exception):
        '''异常回调函数'''
        try:
            raise exception    # 抛出异常后，才能被日志进行完整记录下来
        except Exception as e:
            logger.exception(e)

    def _start_engine(self):
        self.running = True
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        # 向调度器添加初始请求
        self.pool.apply_async(self._start_requests, error_callback=self._error_callback)    # 使用异步

        for i in range(settings.MAX_ASYNC_NUMBER):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)    # 利用回调实现循环

        while True:
            time.sleep(0.0001)    # 避免cpu空转，消耗性能
            # 设置退出条件：当请求数和响应数相等时，退出循环
            # 因为异步，需要增加判断，请求数不能为0
            if self.total_response_number >= self.scheduler.total_request_number and self.scheduler.total_request_number != 0:
                self.running = False    # 满足循环退出条件后，设置运行状态为False
                break
        self.pool.close()
        self.pool.join()
```

## 使用gevent的Pool实现异步并发

### 为什么使用gevent

对于I/O密集型任务，gevent能对性能做很大提升的，协程的创建、调度开销都比线程小的多。

### 通过配置文件设置属性，来判断所使用的异步方式

```Python
# 异步方式  thread、coroutine
ASYNC_TYPE = 'coroutine'
```

### 让gevent的Pool和线程池Pool的接口一致

因此需要单独对gevent的Pool进行一下修改，具体如下： 在scrapy_plus下创建async包，随后创建coroutine.py模块

```Python
# scrapy_plus/async/coroutine.py
'''
由于gevent的Pool的没有close方法，也没有异常回调参数
引出需要对gevent的Pool进行一些处理，实现与线程池一样接口，实现线程和协程的无缝转换
'''
from gevent.pool import Pool as BasePool
import gevent.monkey
gevent.monkey.patch_all()    # 打补丁，替换内置的模块


class Pool(BasePool):
    '''协程池
    使得具有close方法
    使得apply_async方法具有和线程池一样的接口
    '''
    def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
        return super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        '''什么都不需要执行'''
        pass
```

### 在引擎中使用上：

```Python
# scrapy_plus/core/engine.py
import time
import importlib
from datetime import datetime

from scrapy_plus.http.request import Request    # 导入Request对象
from scrapy_plus.utils.log import logger    # 导入logger
from scrapy_plus.conf import settings

# 判断使用什么异步模式，改用对应的异步池
if settings.ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool    # 导入线程池对象
elif settings.ASYNC_TYPE == 'coroutine':
    from scrapy_plus.async.coroutine import Pool
else:
    raise Exception("不支持的异步类型：%s, 只能是'thread'或者'coroutine'"%settings.ASYNC_TYPE)

# 注意：
# 由于打patch补丁是为了替换掉socket为非阻塞的
# 而下载器中正好使用了requests模块，如果在这之后导入协程池，会导致requests中使用的socket没有被替换成功
# 从而有可能导致使用出现问题
from .scheduler import Scheduler
from .downloader import Downloader

class Engine(object):
    ......
```
