# Python学习之路-Python操作redis


## 前言

在Python中操作`Redis`可以直接用`redis`模块

## 安装

安装Redis的有3种方式https://github.com/andymccurdy/redis-py

- 第一种：进⼊虚拟环境py_django，联⽹安装包redis

  ```bash
  pip install redis
  ```

- 第二种：进⼊虚拟环境py_django，联⽹安装包redis

  ```bash
  easy_install redis
  ```

- 第三种：到中⽂官⽹-客户端下载redis包的源码，使⽤源码安装：

  - 下载：执行 wget https://github.com/andymccurdy/redis-py/archive/master.zip
  - 解压：unzip master.zip
  - 安装：先进入文件夹`cd redis-py-master`通过`setup.py`安装`sudo python setup.py install`

## 使用

### 引入

引⼊模块：`from redis import *`

{{< admonition warning "注意" true >}}

这个模块中提供了StrictRedis对象(Strict严格)，⽤于连接redis服务器，并按照不同类型提供 了不同⽅法，进⾏交互操作

{{< /admonition >}}

### StrictRedis对象

通过创建对象，指定参数host、port与指定的服务器和端⼝连接，host默认为localhost，port默认为6379，db默认为0

```python
sr = StrictRedis(host='localhost', port=6379, db=0)
# 简写
sr=StrictRedis()
```

{{< admonition info "提示" true >}}

根据不同的类型，拥有不同的实例⽅法可以调⽤，与前⾯学的redis命令对应，⽅法需要的参数与命令的参数⼀致

{{< /admonition >}}

### 指令

#### string

- set
- setex
- mset
- append
- get
- mget
- key

#### keys

- exists
- type
- delete
- expire
- getrange
- ttl

#### hash

- hset
- hmset
- hkeys
- hget
- hmget
- hvals
- hdel

#### list

- lpush
- rpush
- linsert
- lrange
- lset
- lrem

#### set

- sadd
- smembers
- srem

#### zset

- zadd
- zrange
- zrangebyscore
- zscore
- zrem
- zremrangebyscore


