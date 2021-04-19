# Python学习之路-Redis进阶


## 主从

### 概念

⼀个master可以拥有多个slave，⼀个slave⼜可以拥有多个slave，如此下去，形成了强⼤的多级服务器集群架构。master用来写数据，slave用来读数据，经统计：网站的读写比率是10:1，通过主从配置可以实现读写分离。master和slave都是一个redis实例(redis服务)

### 配置

#### 主服务器

- 修改etc/redis/redis.conf文件

  ```bash
  sudo vi redis.conf
  bind 192.168.1.1
  ```

- 重启redis服务

  ```bash
  sudo service redis stop
  redis-server redis.conf
  ```

#### 从服务器

- 复制etc/redis/redis.conf文件

  ```bash
  sudo cp redis.conf ./slave.conf
  ```

- 修改redis/slave.conf文件

  ```
  sudo vi slave.conf
  ```

- 编辑内容

  ```bash
  bind 192.168.1.1
  slaveof 192.168.1.1 6379
  port 6378
  ```

- 配置redis服务

  ```bash
  sudo redis-server slave.conf
  ```

- 查看主从关系

  ```bash
  redis-cli -h 192.168.26.128 info Replication
  ```

  

### 数据操作

  - 在master和slave分别执⾏info命令，查看输出信息 进入主客户端

    ```bash
    redis-cli -h 192.168.1.1 -p 6379
    ```

- 进入从的客户端

  ```bash
  redis-cli -h 192.168.26.128 -p 6378
  ```

- 在master上写数据

- 在slave上读数据

## 集群

### 为什么要有

之前我们已经讲了主从的概念，一主可以多从，如果同时的访问量过大(1000w),主服务肯定就会挂掉，数据服务就挂掉了或者发生自然灾难。大公司都会有很多的服务器(华东地区、华南地区、华中地区、华北地区、西北地区、西南地区、东北地区、台港澳地区机房)

### 概念

集群是一组相互独立的、通过高速网络互联的计算机，它们构成了一个组，并以单一系统的模式加以管理。一个客户与集群相互作用时，集群像是一个独立的服务器。集群配置是用于提高可用性和可缩放性。当请求到来首先由负载均衡服务器处理，把请求转发到另外的一台服务器上。

### 分类

- 软件层面：只有一台电脑，在这一台电脑上启动了多个redis服务。
- 硬件层面：存在多台实体的电脑，每台电脑上都启动了一个redis或者多个redis服务。

### 搭建

#### 配置机器1

在conf⽬录下创建⽂件7000.conf，编辑内容如下

```bash
port 7000
bind 192.168.1.1
daemonize yes
pidfile 7000.pid
cluster-enabled yes
cluster-config-file 7000_node.conf
cluster-node-timeout 15000
appendonly yes
```

在conf⽬录下创建⽂件7001.conf，编辑内容如下

```bash
port 7001
bind 192.168.1.1
daemonize yes
pidfile 7001.pid
cluster-enabled yes
cluster-config-file 7001_node.conf
cluster-node-timeout 15000
appendonly yes
```

在conf⽬录下创建⽂件7002.conf，编辑内容如下

```bash
port 7002
bind 192.168.1.1
daemonize yes
pidfile 7002.pid
cluster-enabled yes
cluster-config-file 7002_node.conf
cluster-node-timeout 15000
```

三个⽂件的配置区别在port、pidfile、cluster-config-file三项

使⽤配置⽂件启动redis服务

```bash
redis-server 7000.conf
redis-server 7001.conf
redis-server 7002.conf
```

#### 配置机器2

在conf⽬录下创建⽂件7003.conf，编辑内容如下

```bash
port 7003
bind 192.168.1.2
daemonize yes
pidfile 7003.pid
cluster-enabled yes
cluster-config-file 7003_node.conf
cluster-node-timeout 15000
appendonly yes
```

在conf⽬录下创建⽂件7004.conf，编辑内容如下

```bash
port 7004
bind 192.168.1.2
daemonize yes
pidfile 7004.pid
cluster-enabled yes
cluster-config-file 7004_node.conf
cluster-node-timeout 15000
appendonly yes
```

在conf⽬录下创建⽂件7005.conf，编辑内容如下

```bash
port 7005
bind 192.168.1.2
daemonize yes
pidfile 7005.pid
cluster-enabled yes
cluster-config-file 7005_node.conf
cluster-node-timeout 15000
appendonly yes
```

- 三个⽂件的配置区别在port、pidfile、cluster-config-file三项

- 使⽤配置⽂件启动redis服务

  ```bash
  redis-server 7003.conf
  redis-server 7004.conf
  redis-server 7005.conf
  ```

#### 创建集群

- redis的安装包中包含了redis-trib.rb，⽤于创建集群，接下来的操作在191.168.1.1机器上进⾏将命令复制，这样可以在任何⽬录下调⽤此命令：

```bash
sudo cp /usr/share/doc/redis-tools/examples/redis-trib.rb /usr/local/bin/
```

- 安装ruby环境，因为redis-trib.rb是⽤ruby开发的

```bash
sudo apt-get install ruby
```

- 在提示信息处输⼊y，然后回⻋继续安装

- 运⾏如下命令创建集群

  ```bash
  redis-trib.rb create --replicas 1 191.168.1.1:7000 192.168.1.1:7001 192.168.1.1:7002 192.168.1.2:7003 192.168.1.2:7004 192.168.1.2:7000
  ```

  执⾏上⾯这个指令在某些机器上可能会报错，主要原因是由于安装的ruby不是最新版本！天朝的防⽕墙导致⽆法下载最新版本，所以需要设置 gem 的源解决办法如下：

  ```bash
  -- 先查看⾃⼰的 gem 源是什么地址
  gem source -l -- 如果是https://rubygems.org/ 就需要更换
  -- 更换指令为
  gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
  -- 通过 gem 安装 redis 的相关依赖
  sudo gem install redis
  -- 然后重新执⾏指令
  ```

- 提示完成，集群搭建成功

#### 数据验证

当前搭建的主服务器为7000、7001、7003，对应的从服务器是7004、7005、7002，在192.168.1.2机器上连接7002，加参数-c表示连接到集群

```
redis-cli -h 172.16.179.131 -c -p 7002
```

写⼊数据，⾃动跳到了7003服务器，并写⼊数据成功，在7003可以获取数据，如果写入数据又重定向到7000(负载均衡)

### 在哪个服务器上写数据：CRC16

- redis cluster在设计的时候，就考虑到了去中⼼化，去中间件，也就是说，集群中 的每个节点都是平等的关系，都是对等的，每个节点都保存各⾃的数据和整个集 群的状态。每个节点都和其他所有节点连接，⽽且这些连接保持活跃，这样就保 证了我们只需要连接集群中的任意⼀个节点，就可以获取到其他节点的数据
- Redis集群没有并使⽤传统的⼀致性哈希来分配数据，⽽是采⽤另外⼀种叫做哈希 槽 (hash slot)的⽅式来分配的。redis cluster 默认分配了 16384 个slot，当我们 set⼀个key 时，会⽤CRC16算法来取模得到所属的slot，然后将这个key 分到哈 希槽区间的节点上，具体算法就是：CRC16(key) % 16384。所以我们在测试的 时候看到set 和 get 的时候，直接跳转到了7000端⼝的节点
- Redis 集群会把数据存在⼀个 master 节点，然后在这个 master 和其对应的salve 之间进⾏数据同步。当读取数据时，也根据⼀致性哈希算法到对应的 master 节 点获取数据。只有当⼀个master 挂掉之后，才会启动⼀个对应的 salve 节点，充 当 master
- 需要注意的是：必须要3个或以上的主节点，否则在创建集群时会失败，并且当存 活的主节点数⼩于总节点数的⼀半时，整个集群就⽆法提供服务了

### Python交互

安装包：`pip install redis-py-cluster`，redis-py-cluster源码地址https://github.com/Grokzen/redis-py-cluster

创建⽂件redis_cluster.py，示例码如下：

```python
from rediscluster import *
if __name__ == '__main__':
  try:
    # 构建所有的节点，Redis会使⽤CRC16算法，将键和值写到某个节点上
    startup_nodes = [
        {'host': '192.168.26.128', 'port': '7000'},
        {'host': '192.168.26.130', 'port': '7003'},
        {'host': '192.168.26.128', 'port': '7001'},
    ]
    # 构建StrictRedisCluster对象
    src=StrictRedisCluster(startup_nodes=startup_nodes,decode_responses=True)
    # 设置键为name、值为itheima的数据
    result=src.set('name','itheima')
    print(result)
    # 获取键为name
    name = src.get('name')
    print(name)
  except Exception as e:
    print(e)
```
