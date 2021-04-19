# Python学习之路-Python操作MySQL


## 简介

## PyMySQL

`PyMySQL`是在 `Python3.x `版本中用于连接`MySQL`服务器的一个库，`PyMySQL`遵循`Python`数据库 API v2.0 规范，并包含了 pure-Python MySQL 客户端库。

### 安装

```bash
pip install pymsql
```

### 连接

通过`Connection`对象与数据库建立连接

```python
from pymysql import connect

conn=connect(参数列表)
```

- 参数host：连接的`MySQL`主机，如果本机是`localhost`
- 参数port：连接的`MySQL`主机的端口，默认是`3306`
- 参数database：数据库的名称
- 参数user：连接的用户名
- 参数password：连接的密码
- 参数charset：通信采用的编码方式，推荐使用utf8

#### 对象的方法

- `close()`：关闭连接
- `commit()`：提交
- `cursor()`：返回`Cursor`对象，用于执行`SQL`语句并获得结果

### 执行sql语句

通过`Cursor`对象的`execute()`方法执行sql语句，调用`Connection`对象的`cursor()`方法获取`Cursor`对象

```python
cs=conn.cursor()
cs.execute("SQL语句")
```

#### 对象的方法

- `close()`：关闭
- `execute(operation [, parameters ])`：执行语句，返回受影响的行数，主要用于执行insert、update、delete语句，也可以执行create、alter、drop等语句
- `fetchone()`：执行查询语句时，获取查询结果集的第一个行数据，返回一个元组
- `fetchall()`：执行查询时，获取结果集的所有行，一行构成一个元组，再将这些元组装入一个元组返回

#### 对象的属性

- `rowcount`只读属性，表示最近一次`execute()`执行后受影响的行数
- `connection`获得当前连接对象

### SQL注入

sql语句的参数化，可以有效防止sql注入


