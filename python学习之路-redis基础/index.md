# Python学习之路-Redis基础


## 前言

前面学习数据库的时候学习了用的最多的关系型数据库`MySQL`，这次来学习用的最多的非关系型数据库`Redis`。

## 简介

**Redis**是一个使用ANSI C编写的开源、支持网络、基于内存、分布式、可选持久性的键值对存储数据库。根据月度排行网站DB-Engines.com的数据，Redis是最流行的键值对存储数据库。



## 安装

### 下载

使用以下命令下载，提取和编译Redis：

```bash
$ wget https://download.redis.io/releases/redis-5.0.7.tar.gz
$ tar xzf redis-5.0.7.tar.gz
$ cd redis-5.0.7
$ make
```

### 运行

`src` 目录 中现在提供了已编译的二进制文件 。使用以下命令运行Redis：

```bash
$ src/redis-server
```

### 测试

可以使用内置客户端与Redis进行交互：

```bash
$ src/redis-cli
redis> set foo bar
OK
redis> get foo
"bar"
```

### 常用配置

Redis的配置信息在/etc/redis/redis.conf下，使用vi进行编辑配置：

```bash
sudo vi /etc/redis/redis.conf
```

#### ip与端口

绑定绑定⼀个真实ip。端⼝默认为6379

```bash
bind 127.0.0.1
port 6379
```

**如果需要远程访问，可将ip⾏注释**

#### 守护进程

如果以守护进程运⾏，则不会在命令⾏阻塞，类似于服务。如果以⾮守护进程运⾏，则当前终端被阻塞。设置为yes表示守护进程，设置为no表示⾮守护进程。推荐设置为yes

```bash
daemonize yes
```

#### 数据⽂件

```bash
# 数据文件名
dbfilename dump.rdb
# 存储路径
dir /var/lib/redis
```

#### ⽇志⽂件

```bash
# 日志文件存储位置
logfile "/var/log/redis/redis-server.log"
```

#### 数据库

数据库个数，默认有16个

```bash
database 16
```

#### 主从复制

类似于双机备份

```bash
slaveof
```

#### 其他配置

redis-5.0.3配置https://blog.csdn.net/suprezheng/article/details/90679790

## 相关命令

### 服务端

- 启动服务端的命令为：`redis-server`。
- 查看帮助⽂档：`redis-server --help`
- 查看redis服务器进程：`ps aux | grep redis`
- 杀死redis服务器：`sudo kill -9 pid `
- 指定加载的配置文件：`sudo redis-server /etc/redis/redis.conf`

### 客户端

- 进入客户端的命令为：`redis-cli`

- 查看帮助⽂档：`redis-cli --help`

- 运⾏测试命令：`ping`

  ```redis
  127.0.0.1:6379> ping
  PONG
  ```
  
- 切换数据库，数据库没有名称，默认有16个，通过0-15来标识，连接redis默认选择第一个数据库

  ```redis
  > select 2
  OK
  127.0.0.1:6379[2]> 
  ```

## 数据结构

redis是key-value的数据结构，每条数据都是⼀个键值对，键的类型是字符串

{{< admonition warning "注意" true >}}

键不能重复

{{< /admonition >}}

值的类型分为五种：

- 字符串`string`：字符串类型是`Redis`中最为基础的数据存储类型，一个 key 对应一个 value。

  {{< admonition info "提示" true >}}

  `string`类型在`Redis`中是二进制安全的。这便意味着该类型可以接受任何格式的数据，比如JPEG图像数据或JSON对象描述信息等。在`Redis`中字符串类型的Value最多可以容纳的数据长度是512M。

  {{< /admonition >}}

- 哈希`hash`：是一个键值(key=>value)对集合。特别适合用于存储对象。

- 列表`list`：简单的字符串列表，按照插入顺序排序。可以添加一个元素到列表的头部(左边)或者尾部(右边)。

- 集合`set`：string 类型的无序集合。通过哈希表实现的，添加，删除，查找的复杂度都是 O(1)。

- 有序集合`zset`：和 set 一样也是string类型元素的集合，且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。zset的成员是唯一的,但分数(score)却可以重复。

## 数据操作

### string

#### 存储

- 设置键值：`set key value`，例：

  ```redis
  127.0.0.1:6379[2]> set name xiaoliang
  OK
  ```

- 设置键值及过期时间，单位为秒：`setex key seconds value`，例：

  ```redis
  127.0.0.1:6379[2]> setex name 3 xiaoliang 
  OK
  ```

- 设置多个键值：`mset key1 value1 key2 value2 ...`，例：
	```redis
	127.0.0.1:6379[2]> mset name xiaoliang age 18
  OK
  ```

- 追加值：`append key value`，例：

	```redis
  127.0.0.1:6379[2]> set name xiaoliang
  OK
  127.0.0.1:6379[2]> append name liang
  (integer) 14
  127.0.0.1:6379[2]> get name
  "xiaoliangliang"
  ```

#### 获取

- 根据键获取值，如果不存在此键则返回nil：`get key`，例：

  ```redis
  127.0.0.1:6379[2]> get name
  "xiaoliang"
  ```

- 根据多个键获取多个值：`mget key1 key2 ...`，例：

  ```
  127.0.0.1:6379[2]> mget name age
  1) "xiaoliang"
  2) "18"
  ```

- 查看所有键：keys *

- 查找键，参数⽀持正则表达式：`keys pattern`，例：

  ```redis
  127.0.0.1:6379[2]> keys n*
  1) "name"
  ```

- 判断键是否存在，如果存在返回1，不存在返回0：`exists key`，例：

  ```redis
  127.0.0.1:6379[2]> exists name
  (integer) 1
  127.0.0.1:6379[2]> exists namee
  (integer) 0
  ```

- 查看键对应的value的类型：`type key`，例：

  ```redis
  127.0.0.1:6379[2]> type name
  string
  ```

#### 删除

- 删除键及对应的值：`del key1 key2 ...`，例：

  ```redis
  del name age
  (integer) 2
  ```
> mget name age
  1) (nil)
  2) (nil)
  
  ```
  
  ```


- 设置过期时间，以秒为单位：`expire key seconds`，例

  ```redis
  127.0.0.1:6379[2]> expire name 10
  (integer) 1
  127.0.0.1:6379[2]> ttl name
  (integer) 4
  ```

  {{< admonition warning "注意" true >}}

  如果没有指定过期时间则⼀直存在，直到使⽤DEL移除

  {{< /admonition >}}

### hash

#### 存储

- 设置单个属性：`hset key field value`，例：

  ```redis
  127.0.0.1:6379[2]> hset user name xiaoliang 
  (integer) 1
  ```

  {{< admonition info "提示" true >}}

  可能会出现错误：MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.

  Redis被配置为保存数据库快照，但它目前不能持久化到硬盘。用来修改集合数据的命令不能用

  原因：强制关闭Redis快照导致不能持久化。

  解决方案：运行config set stop-writes-on-bgsave-error no　命令后，关闭配置项stop-writes-on-bgsave-error解决该问题。

  {{< /admonition >}}

- 设置多个属性：`hmset key field1 value1 field2 value2 ...`，例：

  ```redis
  127.0.0.1:6379[2]> hset user name xiaoliang age 18
  (integer) 1
  ```

#### 获取

- 获取指定键所有的属性：`hkeys key`，例：

  ```redis
  127.0.0.1:6379[2]> hkeys user
  1) "name"
  2) "age"
  ```

- 获取⼀个属性的值：`hget key field`，例：

  ```redis
  127.0.0.1:6379[2]> hget user name
  "xiaoliang"
  ```

- 获取多个属性的值：`hmget key field1 field2 ...`，例：

  ```redis
  127.0.0.1:6379[2]> hmget user name age
  1) "xiaoliang"
  2) "18"
  ```

- 获取所有属性的值：`hvals key`，例：

  ```redis
  127.0.0.1:6379[2]> hvals user
  1) "xiaoliang"
  2) "18"
  ```

#### 删除

- 删除整个hash键及值，使⽤del命令

- 删除属性，属性对应的值会被⼀起删除：`hdel key field1 field2 ...`，例子：

  ```redis
  127.0.0.1:6379[2]> hdel user age
  (integer) 1
  127.0.0.1:6379[2]> hkeys user
  1) "name"
  ```

  

### list

#### 存储

- 在左侧插⼊数据：`lpush key value1 value2 ...`，例：

  ```redis
  127.0.0.1:6379[2]> lpush name si liang
  (integer) 2
  127.0.0.1:6379[2]> lrange name 0 2
  1) "liang"
  2) "si"
  ```

- 在右侧插⼊数据：`rpush key value1 value2 ...`，例：

  ```redis
  127.0.0.1:6379[2]> rpush name liang si 
  (integer) 4
  127.0.0.1:6379[2]> lrange name 0 4
  1) "liang"
  2) "si"
  3) "liang"
  4) "si"
  ```

- 在指定元素的前或后插⼊新元素：`linsert key before或after 现有元素 新元素`，例：

  ```redis
  127.0.0.1:6379[2]> linsert name before si yao
  (integer) 5
  127.0.0.1:6379[2]> lrange name 0 6
  1) "liang"
  2) "yao"
  3) "si"
  4) "liang"
  5) "si"
  ```

#### 获取

- 返回列表⾥指定范围内的元素：`lrange key start stop`()，例：

  {{< admonition info "提示" true >}}

  start、stop为元素的下标索引，索引从左侧开始，第⼀个元素为0，索引可以是负数，表示从尾部开始计数，如-1表示最后⼀个元素

  {{< /admonition >}}

  ```redis
  # 获取name列表所有元素
  127.0.0.1:6379[2]> lrange name 0 -1
  1) "liang"
  2) "yao"
  3) "si"
  4) "liang"
  5) "si"
  ```

- 设置指定索引位置的元素值：`lset key index value`，例：

  {{< admonition info "提示" true >}}

  索引从左侧开始，第⼀个元素为0。索引可以是负数，表示尾部开始计数，如-1表示最后⼀个元素

  {{< /admonition >}}

  ```redis
  127.0.0.1:6379[2]> lset name 4 si
  OK
  127.0.0.1:6379[2]> lrange name 0 -1
  1) "liang"
  2) "yao"
  3) "si"
  4) "liang"
  5) "si"
  ```

  #### 删除

  - 删除指定元素：`lrem key count value`，例：

    {{< admonition info "提示" true >}}

    将列表中前count次出现的值为value的元素移除，count > 0: 从头往尾移除，count < 0: 从尾往头移除，count = 0: 移除所有

    {{< /admonition >}}

    ```redis
    127.0.0.1:6379[2]> lrem name 0 liang
    (integer) 2
    127.0.0.1:6379[2]> lrange name 0 -1 
    1) "yao"
    2) "si"
    3) "si"
    ```

    ### set

    #### 存储

    - 添加元素：`sadd key member1 member2 ...`，例：

      ```rediss
      127.0.0.1:6379[2]> sadd name liang si
      (integer) 2
      ```

    #### 获取

    - 返回所有的元素：`smembers key`，例：

      ```redis
      127.0.0.1:6379[2]> smembers name
      1) "si"
      2) "liang"
      ```

    #### 删除

    - 删除指定元素：`srem key`，例：

      ```redis
      127.0.0.1:6379[2]> srem name liang 
      (integer) 1
      127.0.0.1:6379[2]> smembers name
      1) "si"
      ```

    ### zset

    #### 存储

    - 添加：`zadd key score1 member1 score2 member2 ...`，例：

      ```redis
      127.0.0.1:6379[2]> zadd name 2 liang 1 si 
      (integer) 2
      ```

    #### 获取

    - 返回指定范围内的元素：`zrange key start stop`，例：

      {{< admonition info "提示" true >}}

      start、stop为元素的下标索引，索引从左侧开始，第⼀个元素为0，索引可以是负数，表示从尾部开始计数，如-1表示最后⼀个元素

      {{< /admonition >}}

      ```redis
      127.0.0.1:6379[2]> zrange name 0 -1
      1) "si"
      2) "liang"
      ```

    - 返回score值在min和max之间的成员：`zrangebyscore key min max`，例：

      ```redis
      127.0.0.1:6379[2]> zrangebyscore name 1 2
      1) "si"
      2) "liang"
      ```

    - 返回成员member的score值：`zscore key member`，例：

      ```redis
      127.0.0.1:6379[2]> zscore name liang
      "2"
      ```

    ### 删除

    - 删除指定元素：`zrem key member1 member2 ...`，例：

      ```redis
      127.0.0.1:6379[2]> zrem name liang
      (integer) 1
      127.0.0.1:6379[2]> zrange name 0 -1
      1) "si"
      ```

    - 删除权重在指定范围的元素：`zremrangebyscore key min max`，例：

      ```redis
      127.0.0.1:6379[2]> zremrangebyscore name 0 2
      (integer) 1
      127.0.0.1:6379[2]> zrange name 0 -4
      (empty array)
      ```

      
