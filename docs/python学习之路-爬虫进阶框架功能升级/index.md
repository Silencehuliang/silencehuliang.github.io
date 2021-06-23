# Python学习之路-爬虫提高:框架功能升级


## 分布式爬虫

### 分布式爬虫原理

分布式爬虫设计原理：

多台服务器同时抓取数据，请求和指纹存储在同一个redis中

### 实现方案

利用redis实现队列

1. 注意pickle模块的使用：如果将对象存入redis中，需要先将其序列化为二进制数据，取出后反序列化就可以再得到原始对象
2. 接口定义一致性：利用redis使用一个Queue，使其接口同python的内置队列接口一致，可以实现无缝转换

```python
# scrapy_plus/queue.py
import time
import pickle

import redis
from six.moves import queue as BaseQueue

# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 10


# 利用redis实现一个Queue，使其接口同python的内置队列接口一致，可以实现无缝转换
class Queue(object):
    """
    A Queue like message built over redis
    """

    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3

    def __init__(self, maxsize=0, name=REDIS_QUEUE_NAME, host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB,
                lazy_limit=True, password=None):
        """
        Constructor for RedisQueue
        maxsize:    an integer that sets the upperbound limit on the number of
                    items that can be placed in the queue.
        lazy_limit: redis queue is shared via instance, a lazy size limit is used
                    for better performance.
        """
        self.name = name
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)
```

### 通过配置文件选择是否启用分布式

```python
# 项目文件夹/settings.py
......

# 设置调度器的内容是否要持久化
# 量个值：True和False
# 如果是True，那么就是使用分布式，同时也是基于请求的增量式爬虫
# 如果是False, 不会说那个redis队列，会使用python的set存储指纹和请求
SCHEDULER_PERSIST = False
```

### 修改调度器实现请求对象的持久化

```python
#scrapy_plus/core/scheduler.py
from six.moves.queue import Queue
from scrapy_plus.utils.queue import Queue as ReidsQueue
from scrapy_plus.conf.settings import SCHEDULER_PERSIST

class Scheduler:

    def __init__(self,collector):

        self._filter_container = set()
        if SCHEDULER_PERSIST: #如果使用分布式或者是持久化，使用redis的队列
            self.queue = ReidsQueue()

        else:
            self.queue = Queue()

        self.repeate_request_num = 0
```

需要实现分布式，除了请求对象需要存储在redis中，还需要对请求进行去重，包括自动退出判断问题(分布式的话通常不需要自动退出)

### 利用Redis的集合类型实现去重

如果分布式中请求去重的去重容器各个服务器用的不是同一个，那么就无法达到去重的目的，因此这里同样的需要使用redis来实现去重容器，也就是把所有的去重指纹都存储在redis中

实现一个自定义的set：

```python
# scrapy_plus/set.py
import redis
from scrapy_plus.conf import settings


class BaseFilterContainer(object):

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        pass

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        pass


class NoramlFilterContainer(BaseFilterContainer):
    '''利用python的集合类型'''

    def __init__(self):
        self._filter_container = set()

    def add_fp(self, fp):
        ''''''
        self._filter_container.add(fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        if fp in self._filter_container:
            return True
        else:
            return False

class RedisFilterContainer(BaseFilterContainer):

    REDIS_SET_NAME = settings.REDIS_SET_NAME
    REDIS_SET_HOST = settings.REDIS_SET_HOST
    REDIS_SET_PORT = settings.REDIS_SET_PORT
    REDIS_SET_DB = settings.REDIS_SET_DB

    def __init__(self):
        self._redis = redis.StrictRedis(host=self.REDIS_SET_HOST, port=self.REDIS_SET_PORT ,db=self.REDIS_SET_DB)
        self._name = self.REDIS_SET_NAME

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        self._redis.sadd(self._name, fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        return self._redis.sismember(self._name, fp)
```

在调度器中使用这个`set.py`， 使得分布式模式下的去重功能正常运作

```python
# scrapy_plus/core/scheduler.py
from hashlib import sha1

import w3lib.url
from six.moves.queue import Queue
from scrapy_plus.conf import settings
from scrapy_plus.queue import Queue as RedisQueue
from scrapy_plus.set import NoramlFilterContainer, RedisFilterContainer
from scrapy_plus.utils.log import logger

......

class Scheduler(object):
    '''
    1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重判断
    '''

    def __init__(self,collector):

        if SCHEDULER_PERSIST: #如果使用分布式或者是持久化，使用redis的队列
            self.queue = ReidsQueue()
            self._filter_container = RedisFilterContainer() #使用redis作为python的去重的容器
        else: #如果不适用分布式或者持久化，使用python的set作为去重的容器
            self.queue = Queue()
            self._filter_container = NoramlFilterContainer()
        self.repeate_request_num = 0

    def _filter_request(self, request):
        # 去重容器：存储已经发过的请求的特征 url    选用集合类型：set()
        # 利用请求的url method data  求出一个指纹  利用sha1

        request.fp = self._gen_fp(request) #把指纹作为request的一个属性
        if not self._filter_container.exists(request.fp):
            self._filter_container.add_fp(request.fp)
            # logger.info("添加新的请求：<%s>" % request.url)
            return True
        else:
            logger.info("发现重复的请求：<%s>" % request.url)
            self.repeate_request_num +=1
            return False
```

### 程序结束的条件

在之前的单机版本的代码中，通过：总的响应+总的重复数>=总的请求来判断程序结束，但是在分布式的版本那种，每个服务器的请求数量和响应数量不在相同

因为每个服务器存入队列的请求，和成功发送的请求中间可能很多请求被其他的服务器发送了，导致数量不一致，所以可以把总的请求，总的响应，总的重复等信息记录在redis中，那么所有的服务端修改的数据的位置是同一个redis中的内容，所有的服务端判断退出的时候也是通过比较同一个redis中的这些数据来决定

此时，在utils中新建stats_collector.py文件，来实现对各种数量的统计，包括总的请求数量，总的响应数量，总的重复数量

```python
import redis
from scrapy_plus.conf.settings import REDIS_QUEUE_NAME, REDIS_QUEUE_HOST, REDIS_QUEUE_PORT, REDIS_QUEUE_DB


# redis队列默认配置
# REDIS_QUEUE_NAME = 'request_queue'
# REDIS_QUEUE_HOST = 'localhost'
# REDIS_QUEUE_PORT = 6379
# REDIS_QUEUE_DB = 10


class StatsCollector(object):

    def __init__(self, spider_names=[], host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, \
                 db=REDIS_QUEUE_DB, password=None):

        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        #存储请求数量的键
        self.request_nums_key = "_".join(spider_names) + "_request_nums"
        #存储响应数量的键
        self.response_nums_key = "_".join(spider_names) + "_response_nums"
        #存储重复请求的键
        self.repeat_request_nums_key = "_".join(spider_names) + "_repeat_request_nums"
        #存储start_request数量的键
        self.start_request_nums_key = "_".join(spider_names) + "_start_request_nums"

    def incr(self, key):
        '''给键对应的值增加1，不存在会自动创建，并且值为1，'''
        self.redis.incr(key)

    def get(self, key):
        '''获取键对应的值，不存在是为0，存在则获取并转化为int类型'''
        ret = self.redis.get(key)
        if not ret:
            ret = 0
        else:
            ret = int(ret)
        return ret

    def clear(self):
        '''程序结束后清空所有的值'''
        self.redis.delete(self.request_nums_key, self.response_nums_key, \
                          self.repeat_request_nums_key, self.start_request_nums_key)

    @property
    def request_nums(self):
        '''获取请求数量'''
        return self.get(self.request_nums_key)

    @property
    def response_nums(self):
        '''获取响应数量'''
        return self.get(self.response_nums_key)

    @property
    def repeat_request_nums(self):
        '''获取重复请求数量'''
        return self.get(self.repeat_request_nums_key)

    @property
    def start_request_nums(self):
        '''获取start_request数量'''
        return self.get(self.start_request_nums_key)
```

修改`engine.py`

```python
# coding=utf-8
import datetime
import time
import importlib
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, \
    SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, MAX_ASYNC_NUMBER,ASYNC_TYPE

if ASYNC_TYPE == "coroutine":
    from gevent.monkey import patch_all
    patch_all()
    from gevent.pool import Pool
elif ASYNC_TYPE == "thread":
    from multiprocessing.dummy import Pool

from .downloader import Downloader
from .scheduler import Scheduler

from scrapy_plus.http.request import Request
from scrapy_plus.utils.log import logger
from scrapy_plus.utils.stats_collector import StatsCollector


class Engine:
    def __init__(self):
        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)
        self.downloader = Downloader()
        self.pipelines = self._auto_import_instances(PIPELINES)
        self.collector = StatsCollector(self.spiders)
        self.scheduler = Scheduler(self.collector)
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)
        # self.total_request_num = 0
        # self.total_response_num = 0
        self.pool = Pool(4)
        self.is_running = False

    def _auto_import_instances(self, path=[], isspider=False):
        instances = {} if isspider else []
        for p in path:
            model_name = p.rsplit(".", 1)[0]
            cls_name = p.rsplit(".", 1)[-1]
            model = importlib.import_module(model_name)
            cls = getattr(model, cls_name)
            if isspider:
                instances[cls.name] = cls()
            else:
                instances.append(cls())
        return instances

    def start(self):
        t_start = datetime.datetime.now()
        logger.info("爬虫开始启动：{}".format(t_start))
        logger.info("爬虫运行模式：{}".format(ASYNC_TYPE))
        logger.info("最大并发数：{}".format(MAX_ASYNC_NUMBER))
        logger.info("启动的爬虫有：{}".format(list(self.spiders.keys())))
        logger.info("启动的下载中间件有：\n{}".format(DOWNLOADER_MIDDLEWARES))
        logger.info("启动的爬虫中间件有：\n{}".format(SPIDER_MIDDLEWARES))
        logger.info("启动的管道有：\n{}".format(PIPELINES))
        self._start_engine()
        t_end = datetime.datetime.now()
        logger.info("爬虫结束：{}".format(t_end))
        logger.info("耗时：%s" % (t_end - t_start).total_seconds())
        # logger.info("一共获取了请求：{}个".format(self.total_request_num))
        # logger.info("重复的请求：{}个".format(self.scheduler.repeate_request_num))
        # logger.info("成功的请求：{}个".format(self.total_response_num))
        logger.info("一共获取了请求：{}个".format(self.collector.request_nums))
        logger.info("重复的请求：{}个".format(self.collector.repeat_request_nums))
        logger.info("成功的请求：{}个".format(self.collector.response_nums))
        self.collector.clear()

    def _start_request_callback(self,temp):
        self.collector.incr(self.collector.start_request_nums_key)

    def _start_request(self):
        def _func(spider_name,spider):
            for start_request in spider.start_requests():
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                start_request.spider_name = spider_name
                self.scheduler.add_request(start_request)
                #使用collector进行数据的收集
                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)

        for spider_name, spider in self.spiders.items():
            self.pool.apply_async(_func,args=(spider_name,spider),callback=self._start_request_callback)

    def _execute_request_response_item(self):
        request = self.scheduler.get_request()
        if request is None:
            return

        spider = self.spiders[request.spider_name]

        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)
        response = self.downloader.get_response(request)
        response.meta = request.meta
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)

        parse = getattr(spider, request.parse)

        for ret in parse(response):
            if isinstance(ret, Request):
                ret.spider_name = request.spider_name
                for spider_mid in self.spider_mids:
                    ret = spider_mid.process_request(ret)
                self.scheduler.add_request(ret)
                #使用collector进行数据的收集
                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)
            else:
                for pipeline in self.pipelines:
                    pipeline.process_item(ret, spider)
        #使用collector进行数据的收集
        # self.total_response_num += 1
        self.collector.incr(self.collector.response_nums_key)

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        # spider中的start_url开始启动
        self.is_running = True
        self.pool.apply_async(self._start_request)
        for i in range(MAX_ASYNC_NUMBER):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

        while True:
            time.sleep(0.001)

            # if self.total_response_num+self.scheduler.repeate_request_num >= self.total_request_num
            #当start_request的执行数量和爬虫的数量相同的时候
            if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                    self.is_running = False
                    break
```

## 增量爬虫

### 增量爬虫设计原理

增量抓取，意即针对某个站点的数据抓取，当网站的新增数据或者该站点的数据发生了变化后，自动地抓取它新增的或者变化后的数据

### 实现关闭请求去重

为Request对象增加属性filter

```python
# scrapy/http/reqeust.py
'''封装Request对象'''


class Request(object):
    '''请求对象，设置请求信息'''

    def __init__(self, url, method='GET', headers=None, params=None, data=None, filter=True):
        self.url = url    # 请求地址
        self.method = method    # 请求方法
        self.headers = headers    # 请求头
        self.params = params    # 请求参数
        self.data = data    # 请求体
        self.filter = filter    # 是否进行去重，默认是True
```

### 

1. 修改调度器，进行判断

```python
# scrapy_plus/core/scheduler.py
class Scheduler(object):

    ......

    def add_request(self, request):
        '''添加请求对象'''

        # 先判断是否要去重
        if request.filter is False:
            self.queue.put(request)
            logger.info("添加请求成功<disable去重>[%s %s]" % (request.method, request.url))
            self.total_request_number += 1  # 统计请求总数
            return # 必须return

        # 添加请求对象前，先进性去重判断
        fp = self._gen_fp(request)
        if not self.filter_request(fp, request):    # 如果指纹不存在，那么添加该请求
            self.queue.put(request)
            logger.info("添加请求成功[%s %s]"%(request.method, request.url))
            self._filter_container.add_fp(fp)     # 添加完请求后，将指纹也记录下来
            self.total_request_number += 1    # 统计请求总数
        else:
            logger.info("发现重复的请求 [%s %s]" % (request.method, request.url))
            self.repeat_request_number += 1

    ......
```

### 实现无限发起请求

在start_reqeusts中改成无限循环，并设置对应请求为非去重模式。但由于框架调用start_requests方法时同步，如果设置为死循环后，那么位于之后的爬虫的start_requests方法就不会被调用，因此需要在调用每个爬虫的start_reqeusts时设置为异步的。让程序的主线程在，多个start_reqeusts方法都没执行完毕前，不要进行退出判断，避免退出过早

## 断点续爬

### 断点续爬设计分析

断点续爬设计原理介绍：

断点续爬的效果：爬虫程序中止后，再次启动，对已经发起的请求不再发起，而是直接从之前的队列中获取请求继续执行。这也就意味着需要实现以下两点：

1.去重标识(历史请求的指纹)持久化存储，使得新的请求可以和以前的请求进行去重对比

2.请求队列也需要持久化存储

其实也就是程序的中止不会造成请求队列和去重容器的消失，再次启动程序后，还能继续访问它们。

### 断点续爬无丢失方案的实现

断点续爬无丢失的代码实现：

- 添加备份容器：利用redis的hash类型类对每一个请求对象进行存储
- 为Request对象设置重试次数属性
- 在调度器的get_request方法中实现响应的逻辑判断
- 实现delete_request方法：从备份中删除对应的Reqeust对象
- 实现add_lost_request方法
- 在引擎中调用这些方法，完成断点续爬无丢失需求

```Python
# scrapy_plus/redis_hash.py
'''实现一个对redis哈希类型的操作封装'''
import redis
import pickle

from scrapy_plus.http.request import Request
from scrapy_plus.conf import settings


class RedisBackupRequest(object):
    '''利用hash类型，存储每一个请求对象，key是指纹，值就是请求对象'''

    REDIS_BACKUP_NAME = settings.REDIS_BACKUP_NAME
    REDIS_BACKUP_HOST = settings.REDIS_BACKUP_HOST
    REDIS_BACKUP_PORT = settings.REDIS_BACKUP_PORT
    REDIS_BACKUP_DB = settings.REDIS_BACKUP_DB


    def __init__(self):
        self._redis = redis.StrictRedis(host=self.REDIS_BACKUP_HOST, port=self.REDIS_BACKUP_PORT ,db=self.REDIS_BACKUP_DB)
        self._name = self.REDIS_BACKUP_NAME

    # 增删改查
    def save_request(self, fp, request):
        '''将请求对象备份到redis的hash中'''
        bytes_data = pickle.dumps(request)
        self._redis.hset(self._name, fp, bytes_data)

    def delete_request(self, fp):
        '''根据请求的指纹，将其删除'''
        self._redis.hdel(self._name, fp)

    def update_request(self, fp, request):
        '''更新已有的fp'''
        self.save_request(fp, request)

    def get_requests(self):
        '''返回全部的请求对象'''
        for fp, bytes_request in self._redis.hscan_iter(self._name):
            request = pickle.loads(bytes_request)
            yield request
```

- 为Request对象增加重试次数属性：

  ```Python
    class Request(object):
        '''框架内置请求对象，设置请求信息'''
  
        def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse', filter=True, meta=None):
            self.url = url    # 请求地址
            self.method = method    # 请求方法
            self.headers = headers    # 请求头
            self.params = params    # 请求参数
            self.data = data    # 请求体
            self.parse = parse    # 指明它的解析函数， 默认是parse方法
            self.filter = filter  # 是否进行去重，默认是True
            self.retry_time = 0    # 重试次数
            self.meta = meta
  ```

- 修改调度器，实现对应的逻辑以及方法：

  ```Python
    # scrapy_plus/core/scheduler.py
    ......
    from scrapy_plus.redis_hash import RedisBackupRequest
    ......
  
    class Scheduler(object):
        '''
        缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
        对请求对象进行去重判断
        '''
        def __init__(self,collector):
  
            if SCHEDULER_PERSIST: #如果使用分布式或者是持久化，使用redis的队列
                self.queue = ReidsQueue()
                self._filter_container = RedisFilterContainer()
            else:
                self.queue = Queue()
                self._filter_container = NoramlFilterContainer()
            self.collector = collector
  
        def add_reqeust(self, request):
            '''存储request对象进入队列
            return： None
            '''
            # 先判断是否要去重
            if request.filter is False:
                self.queue.put(request)
                logger.info("添加请求成功<disable去重>[%s %s]" % (request.method, request.url))
                self.total_request_number += 1  # 统计请求总数
                return # 必须return
  
            # 判断去重，如果重复，就不添加，否则才添加
            fp = self._gen_fp(request)
            if not self.filter_request(fp, request):
                # 往队列添加请求
                logger.info("添加请求成功[%s %s]"%(request.method.upper(), request.url))
                self.queue.put(request)
                if settings.ROLE in ['master', 'slave']:
                    self._backup_request.save_request(fp, request)   # 对请求进行备份
                # 如果是新的请求，那么就添加进去重容器，表示请求已经添加到了队列中
                self._filter_container.add_fp(fp)
  
                self.total_request_number += 1
            else:
                self.repeat_request_number += 1
  
        def get_request(self):
            '''从队列取出一个请求对象
            return： Request Object
            '''
            try:
                request = self.queue.get(False)
            except:
                return None
            else:
                if request.filter is True and settings.ROLE in ['master', 'slave']:  # 先判断 是否需要进行去重
                    # 判断重试次数是否超过规定
                    fp = self._gen_fp(request)
                    if request.retry_time >= settings.MAX_RETRY_TIMES:
                        self._backup_request.delete_request(fp)    # 如果超过，那么直接删除
                        logger.warnning("出现异常请求，且超过最大尝试的次数：[%s]%s"%(request.method, request.url))
                    request.retry_time += 1   # 重试次数+1
  
                    self._backup_request.update_request(fp, request)  # 并更新到备份中
                return request
  
        def delete_request(self, request):
            '''根据请求从备份删除对应的请求对象'''
            if settings.ROLE in ['master', 'slave']:
                fp = self._gen_fp(request)
                self._backup_request.delete_request(fp)
  
        def add_lost_reqeusts(self):
            '''将丢失的请求对象再添加到队列中'''
            # 从备份容器取出来，放到队列中
            if settings.ROLE in ['master', 'slave']:
                for request in self._backup_request.get_requests():
                    self.queue.put(request)
        ......
  ```
