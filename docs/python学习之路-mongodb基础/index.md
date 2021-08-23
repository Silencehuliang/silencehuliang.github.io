# Python学习之路-MongoDB基础与简单使用


## NoSQL的介绍

“NoSQL”⼀词最早于1998年被⽤于⼀个轻量级的关系数据库的名字。随着web2.0的快速发展， NoSQL概念在2009年被提了出来，NoSQL在2010年⻛⽣⽔起， 现在国内外众多⼤⼩⽹站， 如facebook、 google、 淘宝、 京东、 百度等， 都在使⽤NoSQL开发⾼性能的产品。对于⼀名程序员来讲， 使⽤nosql已经成为⼀条必备技能。NoSQL最常⻅的解释是“non-relational”， “Not Only SQL”也被很多⼈接受， 指的是⾮关系型的数据库

## 关系型和非关系型的介绍

对于关系型数据库，存储数据的时候需要提前建表建库，随着数据的复杂度越来越高，所建的表的数量也越来越多；但是非关系型却不需要

## MongoDB的优势

- 易扩展： NoSQL数据库种类繁多， 但是⼀个共同的特点都是去掉关系数据库的关系型特性。 数据之间⽆关系， 这样就⾮常容易扩展
- ⼤数据量， ⾼性能： NoSQL数据库都具有⾮常⾼的读写性能， 尤其在⼤数据量下， 同样表现优秀。 这得益于它的⽆关系性， 数据库的结构简单
- 灵活的数据模型： NoSQL⽆需事先为要存储的数据建⽴字段， 随时可以存储⾃定义的数据格式。 ⽽在关系数据库⾥， 增删字段是⼀件⾮常麻烦的事情。 如果是⾮常⼤数据量的表， 增加字段简直就是⼀个噩梦

## MongoDB的安装

### 命令安装

```bash
sudo apt-get install -y mongodb-org

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
```

### 源码安装

- 解压
  ```bash
  tar -zxvf mongodb-linux-x86_64-ubuntu1604-3.4.0.tgz
  ```

- 移动到/usr/local/目录下

  ```bash
  sudo mv -r mongodb-linux-x86_64-ubuntu1604-3.4.0/ /usr/local/mongodb
  ```

- 将可执行文件添加到PATH路径中

  ```bash
  export PATH=/usr/local/mongodb/bin:$PATH
  ```


## 启动MongoDB

### 服务端MongoDB的启动

- 查看帮助：mongod –help
- 启动：sudo service mongod start
- 停止：sudo service mongod stop
- 重启：sudo service mongod restart
- 查看是否启动成功：ps -ef|grep mongod
- 配置文件的位置：/etc/mongod.conf，
- 默认端⼝：27017
- 日志的位置：/var/log/mongodb/mongod.log

### 客户端MongoDB

- 启动本地客户端:mongo
- 查看帮助：mongo –help
- 退出：exit或者ctrl+c

### 服务端MongoDB无法启动的解决方法

```
sudo mongod --config /etc/mongod.conf &
```

### MongoDB的官方文档

位置：https://docs.mongodb.com/manual/introduction/

## MongoDB的基本使用

### MongoDB数据库的命令

- 查看当前的数据库：db
- 查看所有的数据库：show dbs /show databases
- 切换数据库：use db_name
- 删除当前的数据库：db.dropDatabase()

### MongoDB集合的命令

- 不手动创建集合： 向不存在的集合中第⼀次加⼊数据时， 集合会被创建出来
- 手动创建结合：
  - db.createCollection(name,options)
  - db.createCollection("stu")
  - db.createCollection("sub", { capped : true, size : 10 } )
  - 参数capped： 默认值为false表示不设置上限,值为true表示设置上限
  - 参数size： 当capped值为true时， 需要指定此参数， 表示上限⼤⼩,当⽂档达到上限时， 会将之前的数据覆盖， 单位为字节
- 查看集合：show collections
- 删除集合：db.集合名称.drop()

### MongoDB中常见的数据类型

#### 常见类型

- Object ID： ⽂档ID
- String： 字符串， 最常⽤， 必须是有效的UTF-8
- Boolean： 存储⼀个布尔值， true或false
- Integer： 整数可以是32位或64位， 这取决于服务器
- Double： 存储浮点值
- Arrays： 数组或列表， 多个值存储到⼀个键
- Object： ⽤于嵌⼊式的⽂档， 即⼀个值为⼀个⽂档
- Null： 存储Null值
- Timestamp： 时间戳， 表示从1970-1-1到现在的总秒数
- Date： 存储当前⽇期或时间的UNIX时间格式

#### 注意点

- 创建⽇期语句如下 ：参数的格式为YYYY-MM-DD new Date('2017-12-20')

- 每个⽂档都有⼀个属性， 为_id， 保证每个⽂档的唯⼀性

  可以⾃⼰去设置_id插⼊⽂档，如果没有提供， 那么MongoDB为每个⽂档提供了⼀个独特的_id， 类型为objectID

- objectID是⼀个12字节的⼗六进制数,每个字节两位，一共是24 位的字符串： 前4个字节为当前时间戳 接下来3个字节的机器ID 接下来的2个字节中MongoDB的服务进程id 最后3个字节是简单的增量值

### MongoDB的增删改查

#### MongoDB的插入

命令：`db.集合名称.insert(document)`

```
  db.stu.insert({name:'gj',gender:1})
  db.stu.insert({_id:"20170101",name:'gj',gender:1})
```

插⼊⽂档时， 如果不指定_id参数， MongoDB会为⽂档分配⼀个唯⼀的ObjectId

#### MongoDB的保存

命令：`db.集合名称.save(document)` 如果⽂档的_id已经存在则修改， 如果⽂档的_id不存在则添加

#### MongoDB的简单查询

命令：`db.集合名称.find()`

#### MongoDB的更新

命令：`db.集合名称.update(<query> ,<update>,{multi: <boolean>})`

- 参数query:查询条件
- 参数update:更新操作符
- 参数multi:可选， 默认是false，表示只更新找到的第⼀条记录， 值为true表示把满⾜条件的⽂档全部更新

```
db.stu.update({name:'hr'},{name:'mnc'})   更新一条
db.stu.update({name:'hr'},{$set:{name:'hys'}})    更新一条
db.stu.update({},{$set:{gender:0}},{multi:true})   更新全部
```

注意："multi update only works with $ operators"

#### MongoDB的删除

命令：`db.集合名称.remove(<query>,{justOne: <boolean>})`

- 参数query:可选，删除的⽂档的条件
- 参数justOne:可选， 如果设为true或1， 则只删除⼀条， 默认false， 表示删除多条

### MongoDB的高级查询

#### 数据查询

- ⽅法find()： 查询

  `db.集合名称.find({条件⽂档})`

- ⽅法findOne()：查询，只返回第⼀个

  `db.集合名称.findOne({条件⽂档})`

- ⽅法pretty()： 将结果格式化

  `db.集合名称.find({条件⽂档}).pretty()`

#### 比较运算符

- 等于： 默认是等于判断， 没有运算符
- ⼩于：`$lt （less than）`
- ⼩于等于：`$lte （less than equal）`
- ⼤于：`$gt （greater than）`
- ⼤于等于：`$gte`
- 不等于：`$ne`

#### 逻辑运算符

逻辑运算符主要指与、或逻辑

- and：在json中写多个条件即可
- or:使⽤$or， 值为数组， 数组中每个元素为json

#### 范围运算符

使⽤`$in`， `$nin` 判断数据是否在某个数组内

#### ⽀持正则表达式

使⽤//或$regex编写正则表达式

#### skip和limit

- ⽅法limit()： ⽤于读取指定数量的⽂档

- ⽅法skip()： ⽤于跳过指定数量的⽂档

注意：先使用skip在使用limit的效率要高于前者

#### 自定义查询

由于mongo的shell是一个js的执行环境 使⽤$where后⾯写⼀个函数， 返回满⾜条件的数据

#### 投影

在查询到的返回结果中， 只选择必要的字段

命令：`db.集合名称.find({},{字段名称:1,...})`

参数为字段与值， 值为1表示显示， 值为0不显 特别注意： 对于_id列默认是显示的， 如果不显示需要明确设置为0

#### 排序

⽅法sort()， ⽤于对 集进⾏排序

命令：`db.集合名称.find().sort({字段:1,...})`

参数1为升序排列 参数-1为降序排列

#### 统计个数

⽅法count()⽤于统计结果集中⽂档条数

命令：`db.集合名称.find({条件}).count()` 命令：`db.集合名称.count({条件})`

####  消除重复

⽅法`distinct()`对数据进⾏去重

命令：`db.集合名称.distinct('去重字段',{条件})`
