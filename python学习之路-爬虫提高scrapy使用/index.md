# Python学习之路-爬虫提高:scrapy使用


## scrapy项目实现流程

- 创建一个scrapy项目:`scrapy startproject mySpider`
- 生成一个爬虫:`scrapy genspider itcast "itcast.cn`
- 提取数据:`完善spider，使用xpath等方法`
- 保存数据:`pipeline中保存数据`

### 创建scrapy项目

下面以抓取传智师资库来学习scrapy的入门使用：http://www.itcast.cn/channel/teacher.shtml命令：`scrapy startproject +<项目名字>`

### 创建爬虫

命令：`scrapy genspider +<爬虫名字> + <允许爬取的域名>`

### 完善spider

完善spider即通过方法进行数据的提取等操作

注意：

1. `response.xpath`方法的返回结果是一个类似list的类型，其中包含的是selector对象，操作和列表一样，但是有一些额外的方法
2. `extract()` 返回一个包含有字符串的列表
3. `extract_first()` 返回列表中的第一个字符串，列表为空没有返回None
4. spider中的parse方法必须有
5. 需要抓取的url地址必须属于allowed_domains,但是start_urls中的url地址没有这个限制
6. 启动爬虫的时候注意启动的位置，是在项目路径下启动

### 数据传递到pipeline

为什么要使用yield？

- 让整个函数变成一个生成器，有什么好处呢？
- 遍历这个函数的返回值的时候，挨个把数据读到内存，不会造成内存的瞬间占用过高
- python3中的range和python2中的xrange同理

注意：

- yield能够传递的对象只能是：`BaseItem`,`Request`,`dict`,`None`

### 完善pipeline

pipeline在settings中能够开启多个，为什么需要开启多个？

- 不同的pipeline可以处理不同爬虫的数据
- 不同的pipeline能够进行不同的数据处理的操作，比如一个进行数据清洗，一个进行数据的保存

### pipeline使用注意点

- 使用之前需要在settings中开启
- pipeline在setting中键表示位置(即pipeline在项目中的位置可以自定义)，值表示距离引擎的远近，越近数据会越先经过
- 有多个pipeline的时候，process_item的方法必须`return item`,否则后一个pipeline取到的数据为None值
- pipeline中process_item的方法必须有，否则item没有办法接受和处理
- process_item方法接受item和spider，其中spider表示当前传递item过来的spider

### 输出日志LOG的设置

为了让我们自己希望输出到终端的内容能容易看一些，我们可以在setting中设置log级别

在setting中添加一行（全部大写）：`LOG_LEVEL = "WARNING”`

默认终端显示的是debug级别的log信息

## scrapy实现翻页请求

对于要提取所有页面上的数据该怎么办？

回顾requests模块是如何实现翻页请求的：

- 找到下一页的URL地址
- 调用requests.get(url)

思路：

1. 找到下一页的url地址
2. 构造url地址的请求，传递给引擎

### 实现翻页请求

1. 使用方法

   在获取到url地址之后，可以通过`scrapy.Request(url,callback)`得到一个request对象，通过yield关键字就可以把这个request对象交给引擎

2. 具体使用

   添加User-Agent

   同时可以再在setting中设置User-Agent：

   ```
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
   ```

3. 通过爬取腾讯招聘的页面的招聘信息,学习如何实现翻页请求

   地址：http://hr.tencent.com/position.php

   思路分析：

   1. 获取首页的数据
   2. 寻找下一页的地址，进行翻页获取数据

### scrapy.Request的更多参数

```
scrapy.Request(url[,callback,method="GET",headers,body,cookies,meta,dont_filter=False])
```

注意：

- 括号中的参数为可选参数
- callback：表示当前的url的响应交给哪个函数去处理
- meta：实现数据在不同的解析函数中传递，meta默认带有部分数据，比如下载延迟，请求深度等
- dont_filter:默认会过滤请求的url地址，即请求过的url地址不会继续被请求，对需要重复请求的url地址可以把它设置为Ture，比如贴吧的翻页请求，页面的数据总是在变化;start_urls中的地址会被反复请求，否则程序不会启动

## 定义Item

定义Item的原因：定义item即提前规划好哪些字段需要抓取，scrapy.Field()仅仅是提前占坑，通过item.py能够让别人清楚自己的爬虫是在抓取什么，同时定义好哪些字段是需要抓取的，没有定义的字段不能使用，防止手误

## 使用Item

Item使用之前需要先导入并且实例化，之后的使用方法和使用字典相同

```python
 from yangguang.items import YangguangItem
 item = YangguangItem() #实例化
```

## scrapy的深入使用

### scrapy shell的使用

scrapy shell是scrapy提供的一个终端工具，能够通过它查看scrapy中对象的属性和方法，以及测试xpath

使用方法：`scrapy shell http://www.itcast.cn/channel/teacher.shtml`

在终端输入上述命令后，能够进入python的交互式终端

小知识点：

- response.url：当前响应的url地址
- response.request.url：当前响应对应的请求的url地址
- response.headers：响应头
- response.body：响应体，也就是html代码，默认是byte类型
- response.requests.headers：当前响应的请求头

### 认识scrapy中的setting文件

- 为什么项目中需要配置文件

  - 在配置文件中存放一些公共变量，在后续的项目中便便修改，注意其中的变量名一般全部大写

- 配置文件中的变量使用方法

  - 导入即可使用

- `settings.py`中的重点字段和内涵

  - `USER_AGENT` 设置ua
  - `ROBOTSTXT_OBEY` 是否遵守robots协议，默认是遵守
  - `CONCURRENT_REQUESTS` 设置并发请求的数量，默认是16个
  - `DOWNLOAD_DELAY` 下载延迟，默认无延迟
  - `COOKIES_ENABLED` 是否开启cookie，即每次请求带上前一次的cookie，默认是开启的
  - `DEFAULT_REQUEST_HEADERS` 设置默认请求头
  - `SPIDER_MIDDLEWARES` 爬虫中间件，设置过程和管道相同
  - `DOWNLOADER_MIDDLEWARES` 下载中间件

  ### 管道中的`open_spider`和`close_spider` 的方法

  在管道中，除了必须定义process_item之外，还可以定义两个方法：

  - `open_spider(spider)` :能够在爬虫开启的时候执行一次
  - `close_spider(spider)` :能够在爬虫关闭的时候执行一次

  所以，上述方法经常用于爬虫和数据库的交互，在爬虫开启的时候建立和数据库的连接，在爬虫关闭的时候断开和数据库的连接

  

## crawlspider类的使用

### crawlspider是什么

  回顾之前的代码中，我们有很大一部分时间在寻找下一页的url地址或者是内容的url地址上面，这个过程能更简单一些么？

  思路：

  - 从response中提取所有的满足规则的url地址
  - 自动的构造自己requests请求，发送给引擎

  对应的crawlspider就可以实现上述需求，匹配满足条件的url地址，才发送给引擎，同时能够指定callback函数

### 认识crawlspider爬虫

#### 创建crawlspdier爬虫的命令

```
scrapy genspider –t crawl itcast itcast.cn
```

#### 观察爬虫内的默认内容

spider中默认生成的内容如下，其中重点在rules中

- rules是一个元组或者是列表，包含的是Rule对象
- Rule表示规则，其中包含`LinkExtractor`,`callback`和`follow`
- `LinkExtractor`:连接提取器，可以通过正则或者是xpath来进行url地址的匹配
- `callback` :表示经过连接提取器提取出来的url地址响应的回调函数，可以没有，没有表示响应不会进行回调函数的处理
- `follow`：表示进过连接提取器提取的url地址对应的响应是否还会继续被rules中的规则进行提取，True表示会，Flase表示不会

```python
class Itcast1Spider(CrawlSpider):
    name = 'itcast1'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://itcast.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #使用xpath进行数据的提取或者url地址的提取
        return i
```

#### crawlspider使用的注意点 

- 可以用命令创建一个crawlspider的模板，也可以手动创建
- CrawlSpider中不能再有以parse为名字的数据提取方法，这个方法被CrawlSpider用来实现基础url提取等功能
- 一个Rule对象接收很多参数，首先第一个是包含url规则得到LinkExtractor对象，常用的还有callback(制定满足规则的url的解析函数的字符串)和follow(response中提取的链接是否需要跟进)
- 不指定callback函数的请求下，如果follow为True，满足该rule的url还会继续被请求
- 如果多个Rule都满足某一个url，会从rules中选择第一个满足的进行操作

#### crawlspider的补充知识点

LindExtractor更多常见参数：

allow：满足括号中"正则表达式"的url会被提取，如果为空，则全部匹配

deny：满足括号中"正则表达式"的url一定不提取(优先级高于allow)

allow_domains：会被提取的链接的domains

deny_domains：一定不会被提取链接的domains

restrict_xpaths：使用xpath表达式，和allow共同作用过滤链接，即xpath满足范围内的url地址会被提取

spiders.Rule常见参数：

link_extractor：是一个Link Extractor对象，用于定义需要提取的链接

callback：从link_extractor中每获取到链接时，参数所指定的值作为回调函数

follow：是一个布尔值，制定了根据该规则从response提取的链接是否需要跟进。如果callback为None，follow默认设置为True，否则默认为False

process_links：指定该spider中那个的函数将会被调用，从link_extractor中获取到链接列表时将会调用该函数，该方法主要用来过滤url

process_request:指定该spider中那个的函数将会被调用，该规则提取到每个request时都会调用该函数，用来过滤request

## 下载中间件和模拟登陆

### scrapy中下载中间件的使用

#### 使用方法

编写一个`Downloader Middlewares`和我们编写一个pipeline一样，定义一个类，然后在setting中开启

1. `Downloader Middlewares`默认的方法：

   - process_request(self, request, spider)：

     - 当每个request通过下载中间件时，该方法被调用。
     - 返回None值：继续请求
     - 返回Response对象：不在请求，把response返回给引擎
     - 返回Request对象：把request对象交给调度器进行后续的请求

   - process_response(self, request, response, spider)：

     ```
      - 当下载器完成http请求，传递响应给引擎的时候调用
      - 返回Resposne：交给process_response来处理
      - 返回Request对象：交给调取器继续请求
     ```

2. 定义实现随机User-Agent的下载中间件

   ```python
    class UserAgentMiddleware(object):
        def process_request(self,request,spider):
            agent = random.choice(agents)
            request.headers['User-Agent'] = agent
   ```

3. 定义实现随机使用代理的下载中间件

   ```pyhton
    class ProxyMiddleware(object):
        def process_request(self,request,spider):
            proxy = random.choice(proxies)
            request.meta['proxy'] = proxy
   ```

   User-Agent池在这里

   ```
    ```python
    USER_AGENTS = [ "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)", "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5" ]
   ```
   ```

### 使用scrapy进行模拟登陆

#### 回顾之前的模拟登陆的方法

1. requests是如何模拟登陆的？
   1. 直接携带cookies请求页面
   2. 找接口发送post请求存储cookie
2. selenium是如何模拟登陆的？
   1. 找到对应的input标签，输入文字点击登录

scrapy来说，有两个方法模拟登陆：

```
1、直接携带cookie
2、找到发送post请求的url地址，带上信息，发送请求
```

#### scrapy携带cookie进行模拟登陆

1. 携带cookie进行模拟登陆应用场景：

   1. cookie过期时间很长，常见于一些不规范的网站
   2. 能在cookie过期之前把搜有的数据拿到
   3. 配合其他程序使用，比如其使用selenium把登陆之后的cookie获取到保存到本地，scrapy发送请求之前先读取本地cookie

2. scrapy的start_requests方法的学习

   scrapy中start_url是通过start_requests来进行处理的，其实现代码如下

   ```python
    def start_requests(self):
        cls = self.__class__
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead (see %s.%s)." % (
                    cls.__module__, cls.__name__
                ),
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)
   ```

   所以对应的，如果start_url地址中的url是需要登录后才能访问的url地址，则需要重写`start_request`方法并在其中手动添加上cookie

在settings中开启cookie_debug

在settings.py中通过设置`COOKIES_DEBUG=TRUE` 能够在终端看到cookie的传递传递过程

#### scrapy发送post请求

1. scrapy中发送post请求的方法 通过`scrapy.FormRequest`能够发送post请求，同时需要添加`fromdata`参数作为请求体，以及`callback`

   ```python
    yield scrapy.FormRequest(
                "https://github.com/session",
                formdata={
                    "authenticity_token":authenticity_token,
                    "utf8":utf8,
                    "commit":commit,
                    "login":"noobpythoner",
                    "password":"zhoudawei123"
                },
                callback=self.parse_login
            )
   ```

2. 使用scrapy模拟登陆github

   思路分析

   1. 找到post的url地址

      点击登录按钮进行抓包，然后定位url地址为`https://github.com/session`

   2. 找到请求体的规律

      分析post请求的请求体，其中包含的参数均在前一次的响应中

   3. 验证是否登录成功

      通过请求个人主页，观察是否包含用户名

      代码实现如下：

      ```python
      #spider/github.py
      # -*- coding: utf-8 -*-
      import scrapy
      import re
      
      class GithubSpider(scrapy.Spider):
       name = 'github'
       allowed_domains = ['github.com']
       start_urls = ['https://github.com/login']
      
       def parse(self, response):
           authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
           utf8 = response.xpath("//input[@name='utf8']/@value").extract_first()
           commit = response.xpath("//input[@name='commit']/@value").extract_first()
      
           yield scrapy.FormRequest(
               "https://github.com/session",
               formdata={
                   "authenticity_token":authenticity_token,
                   "utf8":utf8,
                   "commit":commit,
                   "login":"noobpythoner",
                   "password":"***"
               },
               callback=self.parse_login
           )
      
       def parse_login(self,response):
           ret = re.findall("noobpythoner",response.text,re.I)
           print(ret)
      ```

#### scrapy进行表单提交

1. 方法介绍

   scrapy中具有一个方法：`scrapy.Formrequest.from_response`能够自动的从响应中寻找form表单，然后把formdata中的数据提交到action对应的url地址中

   使用实例如下

   ```python
     def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,#自动的从中寻找action对应的url地址
            formdata={
                "login":"noobpythoner",
                "password":"***"
            },
            callback = self.parse_login
        )
   ```

2. 使用`scrapy.Formrequest.from_response`进行模拟登陆github
