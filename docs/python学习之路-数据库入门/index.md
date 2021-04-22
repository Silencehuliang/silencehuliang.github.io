# Python学习之路-数据库入门


## 简介

数据库就是一种特殊的文件，其中存储着需要的数据。

## 类型

当前主要使用两种类型的数据库：关系型数据库、非关系型数据库，本篇主要讨论关系型数据库，对于非关系型数据库会在后面学习。所谓的关系型数据库RDBMS，是建立在关系模型基础上的数据库，借助于集合代数等数学概念和方法来处理数据库中的数据。

关系型数据库的主要产品：

- oracle：在以前的大型项目中使用,银行,电信等项目
- mysql：web时代使用最广泛的关系型数据库
- ms sql server：在微软的项目中使用
- sqlite：轻量级数据库，主要应用在移动平台

## RDBMS和数据库的关系



![](https://tvax3.sinaimg.cn/large/00729CCqgy1gpj3602s6zj30sn0elgmc.jpg)

图片取材于[布布扣](http://www.bubuko.com/infodetail-2885871.html)，更详细的内容可以参考其博客

## SQL

SQL(Structured Query Language)是结构化查询语言，是一种用来操作RDBMS的数据库语言，当前关系型数据库都支持使用SQL语言进行操作，也就是说可以通过 SQL 操作`oracle`，`sql`，`server`，`mysql`，`sqlite` 等等所有的关系型的数据库。

SQL语句主要分为：

- DQL：数据查询语言，用于对数据进行查询，如select
- DML：数据操作语言，对数据进行增加、修改、删除，如insert、udpate、delete
- TPL：事务处理语言，对事务进行处理，包括begin transaction、commit、rollback
- DCL：数据控制语言，进行授权与权限回收，如grant、revoke
- DDL：数据定义语言，进行数据库、表的管理等，如create、drop
- CCL：指针控制语言，通过控制指针完成表的操作，如declare cursor

{{< admonition info "提示" true >}}

SQL 是一门特殊的语言,专门用来操作关系数据库。不区分大小写

{{< /admonition >}}

## MySQL

### 简介

MySQL是一个关系型数据库管理系统，由瑞典MySQL AB公司开发，后来被Sun公司收购，Sun公司后来又被Oracle公司收购，目前属于Oracle旗下产品。[MySQL官方网站](http://www.mysql.com/)

### 特点

- 使用C和C++编写，并使用了多种编译器进行测试，保证源代码的可移植性

- 支持多种操作系统，如Linux、Windows、AIX、FreeBSD、HP-UX、MacOS、NovellNetware、OpenBSD、OS/2 Wrap、Solaris等

- 为多种编程语言提供了API，如C、C++、Python、Java、Perl、PHP、Eiffel、Ruby等

- 支持多线程，充分利用CPU资源

- 优化的SQL查询算法，有效地提高查询速度

- 提供多语言支持，常见的编码如GB2312、BIG5、UTF8

- 提供TCP/IP、ODBC和JDBC等多种数据库连接途径

- 提供用于管理、检查、优化数据库操作的管理工具

- 大型的数据库。可以处理拥有上千万条记录的大型数据库

- 支持多种存储引擎

- MySQL 软件采用了双授权政策，它分为社区版和商业版，由于其体积小、速度快、总体拥有成本低，尤其是开放源码这一特点，一般中小型网站的开发都选择MySQL作为网站数据库

- MySQL使用标准的SQL数据语言形式

- Mysql是可以定制的，采用了GPL协议，你可以修改源码来开发自己的Mysql系统

- 在线DDL更改功能

- 复制全局事务标识

- 复制无崩溃从机

- 复制多线程从机

  {{< admonition info "提示" true >}}

  开源、免费、不要钱、使用范围广，跨平台支持性好，提供了多种语言调用的API，是学习数据库开发的首选

  {{< /admonition >}}

### 安装与配置

#### 安装服务器端

在终端中输入如下命令，回车后，然后按照提示输入

```bash
sudo apt-get install mysql-server
```

启动服务

```bash
sudo service mysql start
```

查看进程中是否存在mysql服务

```bash
ps ajx|grep mysql
```

停止服务

```bash
sudo service mysql stop
```

重启服务

```bash
sudo service mysql restart
```

#### 配置

配置文件目录为/etc/mysql/mysql.cnf

主要配置项如下：

```bash
bind-address表示服务器绑定的ip，默认为127.0.0.1

port表示端口，默认为3306

datadir表示数据库目录，默认为/var/lib/mysql

general_log_file表示普通日志，默认为/var/log/mysql/mysql.log

log_error表示错误日志，默认为/var/log/mysql/error.log
```

#### 安装客户端

在终端运行如下命令，按提示填写信息

```bash
sudo apt-get install mysql-client
```

详细连接的命令可以查看帮助文档

```bash
mysql --help
```

### 数据完整性

一个数据库就是一个完整的业务单元，可以包含多张表，数据被存储在表中。在表中为了更加准确的存储数据，保证数据的正确有效，可以在创建表的时候，为表添加一些强制性的验证，包括数据字段的类型、约束

#### 数据类型

- 可以通过查看帮助文档查阅所有支持的数据类型
- 使用数据类型的原则是：够用就行，尽量使用取值范围小的，而不用大的，这样可以更多的节省存储空间
- 常用数据类型如下：
  - 整数：int，bit
  - 小数：decimal
  - 字符串：varchar,char
  - 日期时间: date, time, datetime
  - 枚举类型(enum)
- 特别说明的类型如下：
  - decimal表示浮点数，如decimal(5,2)表示共存5位数，小数占2位
  - char表示固定长度的字符串，如char(3)，如果填充'ab'时会补一个空格为`'ab '`
  - varchar表示可变长度的字符串，如varchar(3)，填充'ab'时就会存储'ab'
  - 字符串text表示存储大文本，当字符大于4000时推荐使用
  - 对于图片、音频、视频等文件，不存储在数据库中，而是上传到某个服务器上，然后在表中存储这个文件的保存路径
- 更全的数据类型可以参考http://blog.csdn.net/anxpp/article/details/51284106

#### 约束

- 主键primary key：物理上存储的顺序
- 非空not null：此字段不允许填写空值
- 惟一unique：此字段的值不允许重复
- 默认default：当不填写此值时会使用默认值，如果填写时以填写为准
- 外键foreign key：对关系字段进行约束，当为关系字段填写值时，会到关联的表中查询此值是否存在，如果存在则填写成功，如果不存在则填写失败并抛出异常
- 说明：虽然外键约束可以保证数据的有效性，但是在进行数据的crud（增加、修改、删除、查询）时，都会降低数据库的性能，所以不推荐使用，那么数据的有效性怎么保证呢？答：可以在逻辑层进行控制

数值类型(常用)

| 类型        | 字节大小 | 有符号范围(Signed)                         | 无符号范围(Unsigned)     |
| :---------- | :------- | :----------------------------------------- | :----------------------- |
| TINYINT     | 1        | -128 ~ 127                                 | 0 ~ 255                  |
| SMALLINT    | 2        | -32768 ~ 32767                             | 0 ~ 65535                |
| MEDIUMINT   | 3        | -8388608 ~ 8388607                         | 0 ~ 16777215             |
| INT/INTEGER | 4        | -2147483648 ~2147483647                    | 0 ~ 4294967295           |
| BIGINT      | 8        | -9223372036854775808 ~ 9223372036854775807 | 0 ~ 18446744073709551615 |

字符串

| 类型    | 字节大小 | 示例                                                         |
| :------ | :------- | :----------------------------------------------------------- |
| CHAR    | 0-255    | 类型:char(3) 输入 'ab', 实际存储为'ab ', 输入'abcd' 实际存储为 'abc' |
| VARCHAR | 0-255    | 类型:varchar(3) 输 'ab',实际存储为'ab', 输入'abcd',实际存储为'abc' |
| TEXT    | 0-65535  | 大文本                                                       |

日期时间类型

| 类型      | 字节大小 | 示例                                                  |
| :-------- | :------- | :---------------------------------------------------- |
| DATE      | 4        | '2020-01-01'                                          |
| TIME      | 3        | '12:29:59'                                            |
| DATETIME  | 8        | '2020-01-01 12:29:59'                                 |
| YEAR      | 1        | '2017'                                                |
| TIMESTAMP | 4        | '1970-01-01 00:00:01' UTC ~ '2038-01-01 00:00:01' UTC |

### 命令行脚本

#### 登陆与退出

最基本的连接命令如下，输入后回车

```bash
mysql -u root -p
# 回车后输入密码
```

 退出

```bash
quit 或者 exit
或
ctrl+d
```

登录成功后，输入如下命令查看效果

```bash
查看版本：select version();
显示当前时间：select now();
```

#### 数据库相关操作

查看所有数据库

```sql
show databases;
```

使用数据库

```sql
use 数据库名;
```

查看当前使用的数据库

```sql
select database();
```

创建数据库

```sql
create database 数据库名 charset=utf8;
```

删除数据库

```sql
drop database 数据库名;
```

#### 数据表相关操作

查看当前数据库中所有表

```sql
show tables;
```

 查看表结构

```sql
desc 表名;
```

创建表

{{< admonition info "提示" true >}}

auto_increment表示自动增长

{{< /admonition >}}

```sql
CREATE TABLE table_name(
    column1 datatype contrai,
    column2 datatype,
    column3 datatype,
    .....
    columnN datatype,
    PRIMARY KEY(one or more columns)
);
```

{{< admonition info "提示" true >}}

auto_increment表示自动增长

{{< /admonition >}}

修改表-添加字段

```sql
alter table 表名 add 列名 类型;
```

修改表-修改字段：重命名版

```sql
alter table 表名 change 原名 新名 类型及约束;
```

修改表-修改字段：不重命名版

```sql
alter table 表名 modify 列名 类型及约束;
```

修改表-删除字段

```sql
alter table 表名 drop 列名;
```

删除表

```sql
drop table 表名;
```

查看表的创建语句

```sql
show create table 表名;
```

#### 增删改查

##### 查询

###### 查询所有列

```sql
select * from 表名;
```

###### 查询指定列

```sql
select 列1,列2,... from 表名;
```

{{< admonition info "提示" true >}}

可以使用as为列或表指定别名

{{< /admonition >}}

###### 条件查询

使用where子句对表中的数据筛选，结果为true的行会出现在结果集中，语法如下：

```sql
select * from 表名 where 条件;
```

where后面支持多种运算符，进行条件的处理：比较运算符、逻辑运算符、模糊查询、范围查询、空判断

###### 模糊查询

- like
- %表示任意多个任意字符
- _表示一个任意字符

```sql
select * from 表名 where 条件 like '模糊查询字符%';
```

###### 范围查询

```sql
select * from 表名 where 条件 in('范围查询');
```

{{< admonition info "提示" true >}}

in表示在一个非连续的范围内

{{< /admonition >}}

###### 空判断

```sql
select * from 表名 where 条件 is null;
```

 {{< admonition info "提示" true >}}

null与''是不同的，判空is null

{{< /admonition >}}

###### 优先级

优先级由高到低的顺序为：小括号，not，比较运算符，逻辑运算符，and比or先运算，如果同时出现并希望先算or，需要结合()使用。



##### 增加

全列插入：值的顺序与表中字段的顺序对应

```sql
insert into 表名 values(...)
```

{{< admonition info "提示" true >}}

说明：主键列是自动增长，但是在全列插入时需要占位，通常使用0或者 default 或者 null 来占位，插入成功后以实际数据为准

{{< /admonition >}}

部分列插入：值的顺序与给出的列顺序对应

```sql
insert into 表名(列1,...) values(值1,...)
```

全列多行插入：值的顺序与给出的列顺序对应

```sql
insert into 表名 values(...),(...)...;
或
insert into 表名(列1,...) values(值1,...),(值1,...)...;
```

{{< admonition info "提示" true >}}

上面的语句一次可以向表中插入一行数据，还可以一次性插入多行数据，这样可以减少与数据库的通信

{{< /admonition >}}

##### 修改

```sql
update 表名 set 列1=值1,列2=值2... where 条件
```

##### 删除

```sql
delete from 表名 where 条件
```

逻辑删除，本质就是修改操作

```sql
update 表名 set isdelete=1 where 条件;
```

#### 排序

为了方便查看数据，可以对数据进行排序，语法如下：

```sql
select * from 表名 order by 列1 asc|desc [,列2 asc|desc,...]
```

行数据按照列1进行排序，如果某些行列1的值相同时，则按照列2排序，以此类推。默认按照列值从小到大排列。asc从小到大排列，即升序。desc从大到小排序，即降序。

#### 聚合函数

为了快速得到统计数据，经常会用到如下5个聚合函数

##### 总数

count(*)表示计算总行数，括号中写星与列名，结果是相同的

```sql
select count(*) from 表名;
```

##### 最大值

max(列)表示求此列的最大值

```sql
select max(列) from 表名 where 条件;
```

##### 最小值

min(列)表示求此列的最小值

```sql
select min(列) from 表名 where 条件;
```

##### 求和

sum(列)表示求此列的和

```sql
select sum(列) from 表名 where 条件;
```

##### 平均值

avg(列)表示求此列的平均值

```sql
select avg(列) from 表名 where 条件;
```

#### 分组

group by，将查询结果按照1个或多个字段进行分组，字段值相同的为一组。可用于单个字段分组，也可用于多个字段分组

##### group by + group_concat()

group_concat(字段名)可以作为一个输出字段来使用，表示分组之后，根据分组结果，使用group_concat()来放置每一组的某字段的值的集合

##### group by + 集合函数

通过group_concat()的启发，我们既然可以统计出每个分组的某字段的值的集合，那么我们也可以通过集合函数来对这个`值的集合`做一些操作

##### group by + having

having 条件表达式：用来分组查询后指定一些条件来输出查询结果。having作用和where一样，但having只能用于group by

##### group by + with rollup

with rollup的作用是：在最后新增一行，来记录当前列里所有记录的总和

#### 分页

当数据量过大时，在一页中查看数据是一件非常麻烦的事情，可以通过分行来解决，语法如下：

```sql
select * from 表名 limit start,count
```

从start开始，获取count条数据

#### 连接查询

当查询结果的列来源于多张表时，需要将多张表连接成一个大的数据集，再选择合适的列返回，mysql支持三种类型的连接查询，分别为：

- 内连接查询：查询的结果为两个表匹配到的数据

- 右连接查询：查询的结果为两个表匹配到的数据，右表特有的数据，对于左表中不存在的数据使用null填充

- 左连接查询：查询的结果为两个表匹配到的数据，左表特有的数据，对于右表中不存在的数据使用null填充

  语法如下：
  
  ```sql
  select * from 表1 inner或left或right join 表2 on 表1.列 = 表2.列
  ```

#### 子查询

在一个 select 语句中,嵌入了另外一个 select 语句, 那么被嵌入的 select 语句称之为子查询语句

##### 主查询和子查询的关系

子查询是嵌入到主查询中；子查询是辅助主查询的,要么充当条件,要么充当数据源；子查询是可以独立存在的语句,是一条完整的 select 语句

##### 子查询分类

- 标量子查询: 子查询返回的结果是一个数据(一行一列)
- 列子查询: 返回的结果是一列(一列多行)
- 行子查询: 返回的结果是一行(一行多列)

##### 子查询中特定关键字使用

- in 范围
- 格式: 主查询 where 条件 in (列子查询)

#### 备份

运行mysqldump命令

```sql
mysqldump –uroot –p 数据库名 > python.sql;

# 按提示输入mysql的密码
```

#### 恢复

连接mysql，创建新的数据库，退出连接，执行如下命令

```sql
mysql -uroot –p 新数据库名 < python.sql

# 根据提示输入mysql密码
```

### 数据库设计

关系型数据库建议在E-R模型的基础上，需要根据产品经理的设计策划，抽取出来模型与关系，制定出表结构，这是项目开始的第一步。在开发中有很多设计数据库的软件，常用的如power designer，db desinger等，这些软件可以直观的看到实体及实体间的关系。设计数据库，可能是由专门的数据库设计人员完成，也可能是由开发组成员完成，一般是项目经理带领组员来完成。

#### 三范式

经过研究和对使用中问题的总结，对于设计数据库提出了一些规范，这些规范被称为范式(Normal Form)。目前有迹可寻的共有8种范式，一般需要遵守3范式即可：

- 第一范式（1NF）：强调的是列的原子性，即列不能够再分成其他几列。
- 第二范式（2NF）：首先是 1NF，另外包含两部分内容，一是表必须有一个主键；二是没有包含在主键中的列必须完全依赖于主键，而不能只依赖于主键的一部分。
- 第三范式（3NF）：首先是 2NF，另外非主键列必须直接依赖于主键，不能存在传递依赖。即不能存在：非主键列 A 依赖于非主键列 B，非主键列 B 依赖于主键的情况。

#### E-R模型

- E表示entry，实体，设计实体就像定义一个类一样，指定从哪些方面描述对象，一个实体转换为数据库中的一个表
- R表示relationship，关系，关系描述两个实体之间的对应规则，关系的类型包括包括一对一、一对多、多对多
- 关系也是一种数据，需要通过一个字段存储在表中
- 实体A对实体B为1对1，则在表A或表B中创建一个字段，存储另一个表的主键值
- 实体A对实体B为1对多：在表B中创建一个字段，存储表A的主键值
- 实体A对实体B为多对多：新建一张表C，这个表只有两个字段，一个用于存储A的主键值，一个用于存储B的主键值

#### 逻辑删除

- 对于重要数据，并不希望物理删除，一旦删除，数据无法找回
- 删除方案：设置isDelete的列，类型为bit，表示逻辑删除，默认值为0
- 对于非重要数据，可以进行物理删除
- 数据的重要性，要根据实际开发决定
