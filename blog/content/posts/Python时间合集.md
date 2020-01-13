---
title: "Python时间合集"
date: 2019-01-17T15:58:54+08:00
draft: false
categories: ["Python"] 
tags: ["虚拟环境"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## python3中时间的表示形式

### 格式化时间字符串 

格式化时间字符串（string_time）,指**格式化输出指定输出参数的格式与相对位置的字符串参数**，与python中的format作用类似，常见的格式化时间字符串：**"%Y-%m-%d %H:%M:%S %z,%a,%A,%b,%B,%c,%I,%p"**

- 常用的表

| 名&nbsp;&nbsp;称 |           含&nbsp;&nbsp;义           |                       例&nbsp;&nbsp;子                       |
| :--------------: | :----------------------------------: | :----------------------------------------------------------: |
|        %Y        |    有世纪并用0填充的十进制数年份     |           0001, 0002, …, 2013, 2014, …, 9998, 9999           |
|        %m        |        用零填充十进制数的月份        |                        01, 02, …, 12                         |
|        %d        |    用零填充十进制数的月中的某一天    |                        01, 02, …, 31                         |
|        %H        |  24小时格式的用0填充的十进制数小时   |                        00, 01, …, 23                         |
|        %M        |        用0填充的十进制数分钟         |                        00, 01, …, 59                         |
|        %S        |         用0填充的十进制数秒          |                        00, 01, …, 59                         |
|        %z        | 用零填充的十进制小时分钟秒毫秒的时差 |    (empty), +0000, -0400, +1030, +063415, -030712.345216     |
|        %a        |     根据区域设置的缩写的星期名称     |      Sun, Mon, …, Sat (en_US)<br>So, Mo, …, Sa (de_DE)       |
|        %A        |      根据区域设置的完整星期名称      | Sunday, Monday, …, Saturday (en_US)<br>Sonntag, Montag, …, Samstag (de_DE) |

吐槽一下官网注释秒的范围是0-59，实测0-61都可以

- 官方的完整表：
  以下是C标准（1989版）所需的所有格式代码的列表，这些代码适用于具有标准C实现的所有平台。请注意，1999版C标准添加了其他格式代码。  

| 名&nbsp;&nbsp;称 |                  含&nbsp;&nbsp;义                  |                       例&nbsp;&nbsp;子                       |
| :--------------: | :------------------------------------------------: | :----------------------------------------------------------: |
|        %a        |            根据区域设置的缩写的星期名称            |        Sun, Mon, …, Sat (en_US)So, Mo, …, Sa (de_DE)         |
|        %A        |             根据区域设置的完整星期名称             | Sunday, Monday, …, Saturday (en_US)Sonntag, Montag, …, Samstag (de_DE) |
|        %w        | 将工作日变成十进制数，其中0表示星期日，6表示星期六 |                          0, 1, …, 6                          |
|        %d        |           用零填充十进制数的月中的某一天           |                        01, 02, …, 31                         |
|        %b        |              根据区域设置的缩写月份名              |      Jan, Feb, …, Dec (en_US);Jan, Feb, …, Dez (de_DE)       |
|        %B        |                根据区域改变月份全称                | January, February, …, December (en_US)Januar, Februar, …, Dezember (de_DE) |
|        %m        |               用零填充十进制数的月份               |                        01, 02, …, 12                         |
|        %y        |          没有世纪并用0填充的十进制数年份           |                        00, 01, …, 99                         |
|        %Y        |           有世纪并用0填充的十进制数年份            |           0001, 0002, …, 2013, 2014, …, 9998, 9999           |



### 时间戳 

时间戳（Timestamp）,指**字符串或编码信息用于辨识记录下来的时间日期**，维基百科解释的不容易懂，我的个人理解是**从1970年1月1日到现在过去了多少秒**。



### 时间元祖 

时间元祖(struct_time),**指包含9个特殊元素的元祖**，（tm_year，tm_mon，tm_mday，tm_hour，tm_min，tm_sec，tm_wday，tm_yday，tm_isdst），详情见下表格

| 名&nbsp;&nbsp;称 | 含&nbsp;&nbsp;义 |               值                |
| :--------------: | :--------------: | :-----------------------------: |
|     tm_year      |        年        |       具体年份，例：2017        |
|      tm_mon      |        月        |              1-12               |
|     tm_mday      |        日        |              1-31               |
|     tm_hour      |        时        |              1-23               |
|      tm_min      |        分        |              0-59               |
|      tm_sec      |        秒        |              0-61               |
|     tm_wday      |        周        |        0-6（从周末开始）        |
|     tm_yday      | 在一年中的第几天 |              1-666              |
|     tm_isdst     |   是否为夏令时   | -1,0,1（能表示true和flase的值） |



### 时间对象

时间对象（time_object）,指**通过某些时间类生成的对象**，例如datetime对象。



## python中两大时间库：

### time 

#### 简介：

常用于具体时间操作

#### 常量

- Variables with simple values，值简单的变量

  - altzone，-32400
  - daylight，0
  - timezone，-28800
  - _STRUCT_TM_ITEMS，11

- variables with complex values，值复杂的变量

  - tzname 但是如果直接调用会得到一个乱码的值，看不懂，查阅资料后发现通过重新编码解码可以看到真实值，这里很感谢这个爱思考的博主，这里编码解码参考他的博客，这条博文在这里：https://www.cnblogs.com/luo630/p/9555684.html，里面讲的很详细

  ```python
  >>> time.tzname[0].encode('latin-1').decode('gbk')
  '中国标准时间'
  >>> time.tzname[1].encode('latin-1').decode('gbk')
  '中国夏令时'
  ```

#### 方法：

- asctime：将时间元组转换为字符串，当没有传入参数时，调用localtime()返回的当前时间，参数类型：元祖，返回类型：字符串。例如：

  ```python
  >>> import time
  >>> time.asctime()
  'Tue Jun 11 16:07:40 2017'
  >>> time.asctime((2017,6,11,16,7,40,59,59,59)) # 这里必须要穿一个包含9个数字的元组，且年月日时分都必须符合时间逻辑，秒必须小于等于61，不知道为什么是61，后面三位逻辑暂时还没弄明白，但是跟前面对应的年月日有关
  'Thu Jun 11 16:07:40 2017'
  ```

- clock：计时器函数，在进程结束后返回从开始到第一次调用该函数使用的时间，返回类型：浮点数。例如：

  ```python
  >>> time.clock()
  5e-07
  >>> time.sleep(1)
  >>> time.clock()
  11.9833418
  >>> time.sleep(10)
  >>> time.clock()
  35.1999596
  ```

- ctime：将时间戳转换为以本地时间为单位的字符串。相当于asctime(localtime(seconds))。当没有传入参数时，使用localtime()返回的当前时间。参数类型：时间戳，返回类型：字符串。例如：

  ```python
  >>> time.ctime(1555555550)
  'Thu Apr 18 10:45:50 2017'
  >>> time.ctime()
  'Tue Jun 11 17:08:44 2017'
  ```

- get_clock_info：获取有关指定时钟的信息作为命名空间对象。支持的时钟名称和读取其值的相应函数是：  

  - 'clock'： time.clock()
  - 'monotonic'： time.monotonic()
  - 'perf_counter'： time.perf_counter()
  - 'process_time'： time.process_time()
  - 'thread_time'： time.thread_time()
  - 'time'： time.time()  
    结果具有以下属性：
    adjustable：True如果时钟可以自动更改（例如通过NTP守护程序）或由系统管理员手动更改，False否则
    implementation：用于获取时钟值的基础C函数的名称。有关可能的值，请参阅时钟ID常量。
    单调：True如果时钟不能倒退， False否则分辨率：时钟的分辨率（秒）（float）

- gmtime：将时间戳转换为时间元祖，当没有传入参数时，返回当前世界标准时间的时间元祖。参数类型：时间戳，返回类型：元祖（但是查看源码只有一个pass）。例如：

  ```python
  >>> time.gmtime(1555555550)
  time.struct_time(tm_year=2017, tm_mon=4, tm_mday=18, tm_hour=2, tm_min=45, tm_sec=50, tm_wday=3, tm_yday=108, tm_isdst=0)
  >>> time.gmtime()
  time.struct_time(tm_year=2017, tm_mon=6, tm_mday=11, tm_hour=9, tm_min=18, tm_sec=54, tm_wday=1, tm_yday=162, tm_isdst=0)
  ```

- localtime：与gmtime功能类似，但是返回的时间变成了当地时间。例如：

  ```python
  >>> time.localtime(1555555550)
  time.struct_time(tm_year=2017, tm_mon=4, tm_mday=18, tm_hour=10, tm_min=45, tm_sec=50, tm_wday=3, tm_yday=108, tm_isdst=0)
  >>> time.localtime()
  time.struct_time(tm_year=2017, tm_mon=6, tm_mday=11, tm_hour=17, tm_min=28, tm_sec=34, tm_wday=1, tm_yday=162, tm_isdst=0)
  ```

- mktime：将时间元祖转化为时间戳，返回时间戳。参数类型：时间元祖（9个元素），返回类型：时间戳。例如：

  ```python
  >>> time.mktime((2017,4,18,10,45,50,3,108,0))
  1555555550.0
  ```

- monotonic: 一个单调的计时器，不能倒转。不知道从什么时候开始的，返回类型：浮点型。例如：

  ```python
  >>> def func():
  ...     print(time.monotonic())
  ...     time.sleep(1)
  ...
  >>> i = 0
  >>> while i<5:
  ...     func()
  ...     i+=1
  ...
  461875.89
  461876.89
  461877.89
  461878.89
  461879.89
  ```

- perf_counter：性能计数器用于基准测试。不服跑个分！返回类型：浮点型。例如：

  ```python
  >>> time.perf_counter()
  3674.2299851
  >>> time.perf_counter()
  3675.2086447
  >>> time.perf_counter()
  3675.9990329
  ```

- process_time：用于分析的进程时间:内核和用户空间CPU时间的总和。返回类型：浮点型。例如：

  ```python
  >>> time.process_time()
  4.40625
  ```

- sleep:将执行延迟数秒。参数类型：int or float ,返回类型：无，这就不演示了...浪费时间


- strftime：根据格式规范将时间元组转换为字符串。有关格式化代码，请参阅库参考手册。当没有传入参数时，使用localtime()返回的当前时间。传入参数：配对字符串,时间元祖（与字符串配对），返回参数：时间字符串,例：

  ```python 
  # 根据前面的格式化字符串来生成对应时间字符串
  >>> time.strftime("%Y-%m-%d %H:%M:%S", (2017, 1, 1, 1, 1, 1, 1, 13, 0))
  '2017-01-01 01:01:01'
  >>> time.strftime("%Y-%m-%d %H:%M:%S %I", (2017, 1, 1, 1, 1, 1, 1, 13, 0))
  '2017-01-01 01:01:01 01'
  >>> time.strftime("%Y-%m-%d %H:%M:%S %z,%a,%A,%b,%B,%c,%I,%p", (2017, 1, 1, 1, 1, 1, 1, 13, 0))
  '2017-01-01 01:01:01 +0800,Tue,Tuesday,Jan,January,Tue Jan  1 01:01:01 2017,01,AM'
  ```

- strptime：根据格式规范将字符串解析为时间元组。有关格式化代码，请参阅库参考手册(与strftime ())。传入参数：时间字符串，配对字符串。返回参数：时间元祖

例：
    ```python
    >>> time.strptime("2017-01-01 01:01:02", "%Y-%m-%d %H:%M:%S")
    time.struct_time(tm_year=2017, tm_mon=1, tm_mday=1, tm_hour=1, tm_min=1, tm_sec=2, tm_wday=1, tm_yday=1, tm_isdst=-1)
    ```

- time：以秒为单位返回从纪元开始的当前时间。如果系统时钟提供这些信息，那么可能只存在几分之一秒。就是我们常说的时间戳。返回参数：浮点数

### datetime

#### 由五个模块组成

#### date：

##### 简介

表示日期的类。常用的属性有year, month, day。

##### 常量

- date.min = date(1, 1, 1)，date.max = date(9999, 12, 31)，date.resolution = timedelta(days=1)，分别规定了date对象的最小值、最大值，date对象的最小单位，为天

##### 类方法

  - fromtimestamp：将时间戳转化为date对象，参数类型：float，int，返回类型：date对象

    ```python
    >>> from datetime import date
    >>> date.fromtimestamp(1560415206)
    datetime.date(2017, 6, 13)
    >>> type(date.fromtimestamp(1560415206))
    <class 'datetime.date'>
    ```

  - today：获得今天的日期，返回类型：date对象

    ```python
    >>> date.today()
    datetime.date(2017, 6, 13)
    >>> type(date.today())
    <class 'datetime.date'>
    ```

  - fromordinal：跟fromtimestamp类似

    ```python
    >>> date.fromtimestamp(1560415206)
    datetime.date(2017, 6, 13)
    >>> type(date.fromtimestamp(1560415206))
    <class 'datetime.date'>
    ```

##### 实例方法

  - ctime：返回将日期对象转化为标准时间日期的 00:00:00
    
    ```python
    >>> date(2017,6,13).ctime()
    'Thu Jun 13 00:00:00 2017'
    ```
    
  - strftime，返回将date对象转化为指定格式的date对象
    
    ```python
    >>> d = date(2017,1,1)
    >>> d.strftime("%d/%m/%y")
    '01/01/17'
    >>> type(d)
    <class 'datetime.date'>
    ```
    
  - isoformat,返回将date对象转化为'YYYY-MM-DD'格式的date对象,
    
    ```python
    >>> d = date(2017,2,2)
    >>> d.isoformat()
    '2017-02-02'
    >>> type(d)
    <class 'datetime.date'>
    ```
    
  - timetuple,返回与time.localtime()兼容的本地时间元组
    
    ```python
    >>> date(2017,7,7).timetuple()
    time.struct_time(tm_year=2017, tm_mon=7, tm_mday=7, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=188, tm_isdst=-1)
    ```
    
  - toordinal,按年、月、日返回子午线格列高利教序数。返回类型：int
    
    ```python
    >>> d = date(2017,7,7).toordinal()
    >>> type(d)
    <class 'int'>
    ```
    
  - replace,根据传入的年月日修改date对象的年月日,参数类型：int,返回类型:date对象
    
    ```python
    >>> d = date(2017,7,7)
    >>> d.replace(month=8,day=8)
    datetime.date(2017, 8, 8)
    ```
    
  - weekday,根据date对象，判断该日期为星期几,返回类型：int,0-6分别对应星期一到星期天
    
    ```python
    >>> d = date(2017,6,12)
    >>> a = d.weekday()
    0
    >>> type(a)
    <class 'int'>
    ```
    
  - isoweekday，根据date对象，判断该日期为星期几,返回类型：int,1-7分别对应星期一到星期天
    
    ```python
    >>> d = date(2017,6,12)
    >>> a = d.isoweekday()
    1
    >>> type(a)
    <class 'int'>
    ```
    
  - isocalendar,根据date对象，判断该日期为第几周的星期几，返回类型：包含年，第几周，星期几的元祖
    
    ```python
    >>> d = date(2017,6,12)
    >>> d.isocalendar()
    (2017, 24, 1)
    >>> d = date(2017,7,12)
    >>> d.isocalendar()
    (2017, 28, 3)
    ```

##### 魔法属性

year,month,day：返回年、月、日

```python
>>> d = date(2017,6,13)
>>> d.year
2017
>>> d.month
6
>>> d.day
13
```

#### time
##### 简介
表示时间的类。常用的属性有hour, minute, second, microsecond。
##### 参数

hour=0, minute=0, second=0, microsecond=0, tzinfo=None, fold=0，

- hour，minute，小时和分钟必须传入，小时为0-23，分钟为0-59
- second，microsecond，秒和毫秒，默认为0，可以不传，秒为0-59，毫秒为0-999999
- tzinfo，时区默认为None,可以填你想要的时区
- fold，在[0,1]。用于消除重复间隔期间的墙壁时间的歧义。(当时钟在夏令时结束时回滚，或由于政治原因降低当前区域的UTC偏移量时，会出现重复间隔。)值0(1)表示具有相同壁面时间表示的两个时刻中较早(较晚)的时刻。

##### 常量

- time.min，最早可表示的时间，时间(0,0,0,0)。
- time.max，最新可表示时间，时间(23,59,59,999999)。
- time.resolution在不相等的时间对象之间可能存在的最小差异是时间增量(微秒=1)，不过请注意，不支持对时间对象进行算术。

##### 魔法属性

- hour、minute、second、microsecond、tzinfo、fold分别返回时、分、秒、毫秒、时区与折叠关键字

  ```python
  >>> from datetime import time
  >>> t = time(9,9)
  >>> t.hour
  9
  >>> t.minute
  9
  >>> t.second
  0
  >>> t.microsecond
  0
  >>> t.tzinfo
  >>> t.fold
  0
  ```

##### 实例方法

- isoformat，返回按ISO格式格式化的时间字符串。完整的格式是'HH:MM:SS.mmmmmm+zz:zz'可选参数：timespec，指定附加的数量所包括的时间条款

  ```python
  >>> t = time(8,8)
  >>> a = t.isoformat()
  >>> a
  '08:08:00'
  >>> type(a)
  <class 'str'>
  ```

- strftime，返回一个表示时间的字符串，由显式格式字符串控制。参数

  ```python
  datetime.time(9, 9)
  >>> t = time(9,9)
  >>> t
  datetime.time(9, 9)
  >>> t.strftime("%H/%H/%S")
  '09/09/00'
  ```

- replace,返回根据关键字替换datetime.time对象中的值,参数：hour, minute, second, microsecond, tzinfo,fold

  ```python
  >>> time(9,9).replace(8,8)
  datetime.time(8, 8)
  ```

- utcoffset,根据utc返回以东的时区偏移（可以理解为时差），以分钟为单位，如果没有设置tzinfo则返回none。

  ```python
  >>> class UTC(tzinfo):
  ...     def __init__(self,offset = 0):
  ...         self._offset = offset
  ...     def utcoffset(self,dt):
  ...         return timedelta(hours=self._offset)
  ...     def tzname(self,dt):
  ...         return "UTC +%s" % self._offset
  ...     def dst(self, dt):
  ...         return timedelta(hours=self._offset)
  ...
  >>> time(9,9).utcoffset()
  >>>
  >>> time(9,9,tzinfo=UTC(8)).utcoffset()
  datetime.timedelta(0, 28800)
  ```

- tzname,返回时区的名字

  ```python
  >>> time(9,9,tzinfo=UTC(8)).tzname()
  'UTC +8'
  ```

- dst,返回dst偏移信息，如果没有则返回none

  ```python
  >>> time(9,9,tzinfo=UTC(8)).dst()
  datetime.timedelta(0, 28800)
  >>> time(9,9).dst()
  >>>
  ```

#### datetime

##### 简介

表示日期+时间

##### 参数

year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, fold=0，年，月，日参数是必需的。 tzinfo可以是None，或者是tzinfo子类的实例。其余参数可以是整数，在以下范围内：

- MINYEAR <= year <= MAXYEAR，
- 1 <= month <= 12，
- 1 <= day <= number of days in the given month and year，
- 0 <= hour < 24，
- 0 <= minute < 60，
- 0 <= second < 60，
- 0 <= microsecond < 1000000，
- fold in [0, 1]。

##### 魔法属性

hour,minute,second,microsecond,tzinfo,fold.根据datetime对象返回对应的信息

##### 类方法

- today,返回当前的本地datetime对象

  ```python
  >>> datetime(2017,6,6).today()
  datetime.datetime(2018, 1, 17, 13, 59, 12, 846817)
  ```

- now,可选参数：tz，时区信息，返回当前本地datetime对象，如果没有传tz则得到结果与today一样

  ```python
  >>> datetime.now()
  datetime.datetime(2018, 1, 16, 13, 59, 58, 221440)
  >>> datetime.now()
  >>> datetime.now(UTC(2))
  datetime.datetime(2018, 1, 16, 8, 8, 5, 84489, tzinfo=<__main__.UTC object at 0x0000016B860D0EB8>)
  ```

- utcnow,返回当前的UTCdatetime对象

  ```python
  >>> datetime.utcnow()
  datetime.datetime(2018, 1, 16, 6, 5, 14, 668355)
  ```

- fromtimestamp,根据时间戳参数返回当前的datetime对象

  ```python
  >>> datetime.fromtimestamp(1516083000)
  datetime.datetime(2018, 1, 16, 14, 10)
  ```

- utcfromtimestamp，根据时间戳参数返回UTC的datetime对象

  ```python
  >>> datetime.utcfromtimestamp(1516083000)
  datetime.datetime(2018, 1, 16, 6, 10)
  ```

- combine,返回指定日期与时间的datetime对象

  ```python
  >>> datetime.combine(date(2018,1,1),time(6,6))
  datetime.datetime(2018, 1, 1, 6, 6)
  ```

- strptime，根据参数中的时间字符串格式返回对应的时间字符串

  ```python
  >>> datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  '2019-07-17 14:41:52'
  ```

##### 实例方法

- timetuple,根据datetime对象的信息返回时间元祖

  ```python
  >>> datetime(2018,1,1).timetuple()
  time.struct_time(tm_year=2018, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=1, tm_isdst=-1)
  ```

- timestamp,根据datetime对象的信息返回对应的时间戳

  ```python
  >>> datetime(2018,1,1).timestamp()
  1514736000.0
  ```

- utctimetuple，根据datetime对象的信息返回对应的utc时间元祖

  ```python
  >>> datetime(2018,1,1).utctimetuple()
  time.struct_time(tm_year=2018, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=1, tm_isdst=0)
  ```

- date,根据datetime对象的信息返回对应的datetime.date对象

  ```python
  >>> datetime(2018,1,1).date()
  datetime.date(2018, 1, 1)
  ```

- time,根据datetime对象的信息返回对应的datetime.time对象，没有则为datetime.time(0,0)

  ```python
  >>> datetime(2018,1,1).time()
  datetime.time(0, 0)
  >>> datetime(2018,1,1,14,59).time()
  datetime.time(14, 59)
  ```

- timetz,根据datetime对象的tzinfo信息返回对应的datetime.time对象，在没有设置tzinfo时与time效果一样

  ```python
  >>> datetime(2018,1,1,14,59).timetz()
  datetime.time(14, 59)
  >>> datetime(2018,1,1,14,59,tzinfo=UTC(5)).timetz()
  datetime.time(14, 59, tzinfo=<__main__.UTC object at 0x0000016B883D8588>)
  ```

- replace,根据传入的关键字返回一个新的datetime对象

  ```python
  >>> datetime(2018,1,1,14,59).replace(2018,1,1)
  datetime.datetime(2018, 1, 1, 14, 59)
  ```

- astimezone,返回一个具有tzinfo的datetime对象，如果没有设置tz则为本地的时区信息

  ``` python
  >>> datetime(2018,1,1,14,59).astimezone()
  datetime.datetime(2018, 1, 1, 14, 59, tzinfo=datetime.timezone(datetime.timedelta(0, 28800), '?D1¨²¡À¨º¡Á?¨º¡À??'))
  ```

- ctime，返回按c格式格式化的时间字符串

  ```python
  >>> datetime(2018,1,1,14,59).ctime()
  'Mon Jan  1 14:59:00 2018'
  ```

- isoformat,返回一个按iso格式格式化的事件字符串，完整的格式看起来像'YYYY-MM-DD HH:MM:SS.mmmmmm'，如果设置了tzinfo，则UTC偏移量也会被格式化，这时候完整的格式'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM'，可选参数sep默认为T，指定日期与时间之间的分隔符

  ```python
  >>> datetime(2018,1,1,14,59).isoformat()
  '2018-01-01T14:59:00'
  ```

- utcoffset,返回UTC以东的时区偏移，以分钟为单位

  ```python
  >>> datetime.now(UTC(8)).utcoffset()
  datetime.timedelta(0, 28800)
  ```

- tzname,返回datetime对象的时区名字

  ```python
  >>> datetime.now(UTC(8)).tzname()
  'UTC +8'
  ```

- dst,返回datetime对象的dst偏移

  ```python
  >>> datetime.now(UTC(8)).dst()
  datetime.timedelta(0, 28800)
  ```

#### timedelta

##### 简介

表示两个datetime对象之间的差异。

- 支持比较的方式：

  ```python
  - 加减时间
  - 一元正，一元负，绝对值
  - 与时间比较
  - 乘以，除以int
  ```

  此外，datetime支持减去两个datetime对象返回一个时间增量，以及一个datetime的加减法以及给出datetime的时间增量。

##### 参数
days=0, seconds=0, microseconds=0,milliseconds=0,     minutes=0, hours=0, weeks=0

##### 魔法属性

  - days,返回日,不足一日则为0

    ```python
    >>> timedelta(hours=1).days
    0
    >>> timedelta(hours=25).days
        1
    ```

  - seconds，[秒]

    ```python
    >>> timedelta(hours=1).seconds
    3600
    >>> timedelta(hours=2).seconds
    7200
    ```

  - microseconds

    ```python
    >>> timedelta(seconds=1).microseconds
        0
    >>> timedelta(microseconds=1).microseconds
        1
    ```

  - total_seconds，计算timedelta对象的秒数

    ```python
    >>> timedelta(hours=1).total_seconds()
    3600.0
    ```

    

#### tzinfo

##### 简介

与时区有关的相关信息

##### 用法

时区信息类，他是一个抽象类，不能直接实例化，需要派生一个具体的子类。

    ```python
    >>> from datetime import tzinfo, datetime, timedelta
    >>> class UTC(tzinfo):
    ...     def __init__(self,offset = 0):
    ...         self._offset = offset
    ...     def utcoffset(self,dt):
    ...         return timedelta(hours=self._offset)
    ...     def tzname(self,dt):
    ...         return "UTC +%s" % self._offset
    ...     def dst(self, dt):
    ...         return timedelta(hours=self._offset)
    >>> sh = datetime(2017,6,12,0,0,0,tzinfo=UTC)
    >>> sh
    datetime.datetime(2017, 6, 12, 0, 0, tzinfo=<__main__.UTC_add_8 object at 0x0000021499624588>)
    ```


​        