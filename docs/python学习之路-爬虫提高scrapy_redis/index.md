# Python学习之路-爬虫提高:scrapy_redis


## scrapy_redis是什么

Scrapy_redis ： Redis-based components for Scrapy.

Github地址：https://github.com/rmax/scrapy-redis

## 为什么要学习scrapy_redis

Scrapy_redis在scrapy的基础上实现了更多，更强大的功能，具体体现在：

- 请求对象的持久化
- 去重的持久化
- 和实现分布式

## scrapy_redis的原理分析

### scrapy_redis的流程

- 在scrapy_redis中，所有的带抓取的对象和去重的指纹都存在所有的服务器公用的redis中
- 所有的服务器公用一个redis中的request对象
- 所有的request对象存入redis前，都会在同一个redis中进行判断，之前是否已经存入过
- 在默认情况下所有的数据会保存在redis中

## redis的复习

### redis是什么

redis是一个开源的内存型数据库，支持多种数据类型和结构，比如列表、集合、有序集合等

### redis服务端和客户端的启动

- `/etc/init.d/redis-server start` 启动服务端
- `redis-cli -h <hostname> -p <端口号>` 客户端启动

### redis中的常见命令

1. `select 1` 切换db
2. `keys *` 查看所有的键
3. `tyep 键` 查看键的类型
4. `flushdb` 清空db
5. `flushall` 清空数据库

## scrapy_redis domz爬虫分析

### 拷贝源码中的demo文件

1、clone github scrapy-redis源码文件 `git clone https://github.com/rolando/scrapy-redis.git` 2、研究项目自带的三个demo `mv scrapy-redis/example-project ~/scrapyredis-project`

### 观察dmoz文件

在domz爬虫文件中，实现方式就是之前的`crawlspider`类型的爬虫

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['dmoztools.net']
    start_urls = ['http://dmoztools.net/']

    # 定义数据提取规则，使用了css选择器
    rules = [
        Rule(LinkExtractor(
            restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        ), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        for div in response.css('.title-and-desc'):
            yield {
                'name': div.css('.site-title::text').extract_first(),
                'description': div.css('.site-descr::text').extract_first().strip(),
                'link': div.css('a::attr(href)').extract_first(),
            }
```

但是在settings.py中多了一下几行,这几行表示`scrapy_redis`中重新实现的了去重的类，以及调度器，并且使用的`RedisPipeline`

```python
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True

ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
```

### 运行dmoz爬虫，观察现象

首先我们需要添加redis的地址，程序才能够使用redis

```
 REDIS_URL = "redis://127.0.0.1:6379"
 #或者使用下面的方式
 # REDIS_HOST = "127.0.0.1"
 # REDIS_PORT = 6379
```

我们执行domz的爬虫，会发现redis中多了一下三个键

继续执行程序，会发现程序在前一次的基础之上继续往后执行，所以domz爬虫是一个基于url地址的增量式的爬虫

## scrapy_redis的原理分析

我们从settings.py中的三个配置来进行分析 分别是：

- RedisPipeline
- RFPDupeFilter
- Scheduler

### Scrapy_redis之RedisPipeline

RedisPipeline中观察process_item，进行数据的保存，存入了redis中

### Scrapy_redis之RFPDupeFilter

RFPDupeFilter 实现了对request对象的加密

### Scrapy_redis之Scheduler

scrapy_redis调度器的实现了决定什么时候把request对象加入带抓取的队列，同时把请求过的request对象过滤掉

由此可以总结出request对象入队的条件

- request之前没有见过
- request的dont_filter为True，即不过滤
- start_urls中的url地址会入队，因为他们默认是不过滤

## scrapy_redis实现分布式爬虫

### RedisSpider

#### 分析demo中代码

通过观察代码：

- 继承自父类为RedisSpider
- 增加了一个redis_key的键，没有start_urls，因为分布式中，如果每台电脑都请求一次start_url就会重复
- 多了`__init__`方法，该方法不是必须的，可以手动指定allow_domains

### RedisCrawlSpider

#### 分析demo中的代码

和scrapy中的crawlspider的区别在于，继承自的父类不想听，redis_key需要添加

## crontab爬虫定时启动

### 安装

命令：`apt-get install cron`

### 使用

命令：`crontab -e 进入编辑页面(第一次会让你选择编辑器)`

`crontab -l`查看当前的定时任务

编辑：

分		小时	日		月		星期	命令

0-59	0-23	1-31	1-12	0-6		command

注意点：

1.星期中0表示周日

2.每隔两个小时的时候前面的不能为`*`，为`*`表示每分钟都会执行

## crontab在爬虫中的使用

### 使用流程

1. 把爬虫启动命令写入`.sh` 文件
2. 给`.sh`脚本添加可执行权限
3. 把`.sh` 添加到crontab脚本正

### myspier.sh例子

执行命令写入脚本

其中`>>`表示重定向，把print等信息导入log中

`2>&1`表示把标准错误作为标准输出，输入用0表示，标准输出用1表示，标准错误用2标识，通过该命令能够把错误一起输出到log中

```sh
 cd `dirname $0` || exit 1
 python ./main.py >> run.log 2>&1
```

添加可执行权限

`sudo chmod +x myspder.sh`

写入crontab中

sh脚本文件也可能会报错，对应的可以把其输出和错误重定向到run2.log中

```sh
 0 6 * * * /home/ubuntu/..../myspider.sh >> /home/ubuntu/.../run2.log 2>&1
```
