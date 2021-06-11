# Python学习之路-Flask基础:数据库


## ORM

### 简介

`ORM`全拼`Object-Relation Mapping`，中文意为 `对象-关系映射`。主要实现模型对象到关系数据库数据的映射.

### 优点 

- 只需要面向对象编程, 不需要面向数据库编写代码。对数据库的操作都转化成对类属性和方法的操作，不用编写各种数据库的`sql`语句。
- 实现了数据模型与数据库的解耦，屏蔽了不同数据库操作上的差异。不在关注用的是`mysql`、`oracle`...等。通过简单的配置就可以轻松更换数据库, 而不需要修改代码.

### 缺点 

- 相比较直接使用SQL语句操作数据库,有性能损失。
- 根据对象的操作转换成SQL语句,根据查询的结果转化成对象, 在映射过程中有性能损失。

### SQLALchemy 

`SQLALchemy`实际上是对数据库的抽象，让开发者不用直接和`SQL`语句打交道，而是通过`Python`对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升。`SQLAlchemy`是一个关系型数据库框架，它提供了高层的 `ORM`和底层的原生数据库的操作。`flask-sqlalchemy`是一个简化了`SQLAlchemy`操作的flask扩展。

文档地址：http://docs.jinkan.org/docs/flask-sqlalchemy

#### 安装

- 安装 flask-sqlalchemy

```bash
pip install flask-sqlalchemy
```

- 如果连接的是 mysql 数据库，需要安装 mysqldb

```bash
pip install flask-mysqldb
```

#### 数据库连接设置

- 在 Flask-SQLAlchemy 中，数据库使用URL指定，而且程序使用的数据库必须保存到Flask配置对象的 **SQLALCHEMY_DATABASE_URI** 键中

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'
```

- 其他设置：

```python
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
```

- 配置完成需要去 MySQL 中创建项目所使用的数据库

```bash
$ mysql -uroot -pmysql
$ create database test charset utf8;
```

- 其他配置

| 名字                      | 备注                                                         |
| :------------------------ | :----------------------------------------------------------- |
| SQLALCHEMY_DATABASE_URI   | 用于连接的数据库 URI 。例如:sqlite:////tmp/test.dbmysql://username:password@server/db |
| SQLALCHEMY_BINDS          | 一个映射 binds 到连接 URI 的字典。更多 binds 的信息见[*用 Binds 操作多个数据库*](http://docs.jinkan.org/docs/flask-sqlalchemy/binds.html#binds)。 |
| SQLALCHEMY_ECHO           | 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。(打印sql语句) |
| SQLALCHEMY_RECORD_QUERIES | 可以用于显式地禁用或启用查询记录。查询记录 在调试或测试模式自动启用。更多信息见get_debug_queries()。 |
| SQLALCHEMY_NATIVE_UNICODE | 可以用于显式禁用原生 unicode 支持。当使用 不合适的指定无编码的数据库默认值时，这对于 一些数据库适配器是必须的（比如 Ubuntu 上 某些版本的 PostgreSQL ）。 |
| SQLALCHEMY_POOL_SIZE      | 数据库连接池的大小。默认是引擎默认值（通常 是 5 ）           |
| SQLALCHEMY_POOL_TIMEOUT   | 设定连接池的连接超时时间。默认是 10 。                       |
| SQLALCHEMY_POOL_RECYCLE   | 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定 这个值为 2 小时。 |

#### 连接其他数据库

完整连接 URI 列表请跳转到 SQLAlchemy 下面的文档 ([Supported Databases](http://www.sqlalchemy.org/docs/core/engines.html)) 。这里给出一些 常见的连接字符串。

- Postgres:

```
postgresql://scott:tiger@localhost/mydatabase
```

- MySQL:

```
mysql://scott:tiger@localhost/mydatabase
```

- Oracle:

```
- oracle://scott:tiger@127.0.0.1:1521/sidname
```

- SQLite （注意开头的四个斜线）:

```
sqlite:////absolute/path/to/foo.db
```

#### 常用的字段类型

|    类型名    |   python中类型    |                        说明                         |
| :----------: | :---------------: | :-------------------------------------------------: |
|   Integer    |        int        |                普通整数，一般是32位                 |
| SmallInteger |        int        |            取值范围小的整数，一般是16位             |
|  BigInteger  |     int或long     |                  不限制精度的整数                   |
|    Float     |       float       |                       浮点数                        |
|   Numeric    |  decimal.Decimal  |                普通整数，一般是32位                 |
|    String    |        str        |                     变长字符串                      |
|     Text     |        str        |    变长字符串，对较长或不限长度的字符串做了优化     |
|   Unicode    |      unicode      |                  变长Unicode字符串                  |
| UnicodeText  |      unicode      | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
|   Boolean    |       bool        |                       布尔值                        |
|     Date     |   datetime.date   |                        时间                         |
|     Time     | datetime.datetime |                     日期和时间                      |
| LargeBinary  |        str        |                     二进制文件                      |

#### 常用的列选项

|   选项名    |                       说明                        |
| :---------: | :-----------------------------------------------: |
| primary_key |             如果为True，代表表的主键              |
|   unique    |      如果为True，代表这列不允许出现重复的值       |
|    index    |     如果为True，为这列创建索引，提高查询效率      |
|  nullable   | 如果为True，允许有空值，如果为False，不允许有空值 |
|   default   |                                                   |

#### 常用的关系选项

| 选项名         | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| backref        | 在关系的另一模型中添加反向引用                               |
| primary join   | 明确指定两个模型之间使用的联结条件                           |
| uselist        | 如果为False，不使用列表，而使用标量值                        |
| order_by       | 指定关系中记录的排序方式                                     |
| secondary      | 指定多对多关系中关系表的名字                                 |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件 |

#### 数据库基本操作

- 在Flask-SQLAlchemy中，插入、修改、删除操作，均由数据库会话管理。会话用 db.session 表示。在准备把数据写入数据库前，要先将数据添加到会话中然后调用 commit() 方法提交会话。
- 在 Flask-SQLAlchemy 中，查询操作是通过 query 对象操作数据。最基本的查询是返回表中所有数据，可以通过过滤器进行更精确的数据库查询。

#### 在视图函数中定义模型类

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s'%self.name
if __name__ == '__main__':
    app.run(debug=True)
```

#### 模型之前的关联

##### 一对多

```python
class Role(db.Model):
    ...
    #关键代码
    user = db.relationship('User', backref='role', lazy='dynamic')
    ...

class User(db.Model):
    ...
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

- 其中realtionship描述了Role和User的关系。在此文中，第一个参数为对应参照的类"User"
- 第二个参数backref为类User申明新属性的方法
- 第三个参数lazy决定了什么时候SQLALchemy从数据库中加载数据
  - 如果设置为子查询方式(subquery)，则会在加载完Role对象后，就立即加载与其关联的对象，这样会让总查询数量减少，但如果返回的条目数量很多，就会比较慢
    - 设置为 subquery 的话，role.users 返回所有数据列表
  - 另外,也可以设置为动态方式(dynamic)，这样关联对象会在被使用的时候再进行加载，并且在返回前进行过滤，如果返回的对象数很多，或者未来会变得很多，那最好采用这种方式
    - 设置为 dynamic 的话，role.users 返回查询对象，并没有做真正的查询，可以利用查询对象做其他逻辑，比如：先排序再返回结果

##### 多对多

```python
registrations = db.Table('registrations',  
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),  
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))  
)  
class Course(db.Model):
    ...
class Student(db.Model):
    ...
    courses = db.relationship('Course',secondary=registrations,  
                                    backref='students',  
                                    lazy='dynamic')
```

#### 常用的查询过滤器

|   过滤器    |                       说明                       |
| :---------: | :----------------------------------------------: |
|  filter()   |      把过滤器添加到原查询上，返回一个新查询      |
| filter_by() |    把等值过滤器添加到原查询上，返回一个新查询    |
|    limit    |         使用指定的值限定原查询返回的结果         |
|  offset()   |       偏移原查询返回的结果，返回一个新查询       |
| order_by()  | 根据指定条件对原查询结果进行排序，返回一个新查询 |
| group_by()  | 根据指定条件对原查询结果进行分组，返回一个新查询 |

#### 常用的查询执行器

|      方法      |                     说明                     |
| :------------: | :------------------------------------------: |
|     all()      |         以列表形式返回查询的所有结果         |
|    first()     |  返回查询的第一个结果，如果未查到，返回None  |
| first_or_404() |  返回查询的第一个结果，如果未查到，返回404   |
|     get()      |   返回指定主键对应的行，如不存在，返回None   |
|  get_or_404()  |   返回指定主键对应的行，如不存在，返回404    |
|    count()     |              返回查询结果的数量              |
|   paginate()   | 返回一个Paginate对象，它包含指定范围内的结果 |

#### 创建表

```
db.create_all()
```

#### 删除表

```
db.drop_all()
```

#### 插入一条数据

```
ro1 = Role(name='admin')
db.session.add(ro1)
db.session.commit()
#再次插入一条数据
ro2 = Role(name='user')
db.session.add(ro2)
db.session.commit()
```

#### 一次插入多条数据

```python
us1 = User(name='wang',email='wang@163.com',password='123456',role_id=ro1.id)
us2 = User(name='zhang',email='zhang@189.com',password='201512',role_id=ro2.id)
us3 = User(name='chen',email='chen@126.com',password='987654',role_id=ro2.id)
us4 = User(name='zhou',email='zhou@163.com',password='456789',role_id=ro1.id)
us5 = User(name='tang',email='tang@itheima.com',password='158104',role_id=ro2.id)
us6 = User(name='wu',email='wu@gmail.com',password='5623514',role_id=ro2.id)
us7 = User(name='qian',email='qian@gmail.com',password='1543567',role_id=ro1.id)
us8 = User(name='liu',email='liu@itheima.com',password='867322',role_id=ro1.id)
us9 = User(name='li',email='li@163.com',password='4526342',role_id=ro2.id)
us10 = User(name='sun',email='sun@163.com',password='235523',role_id=ro2.id)
db.session.add_all([us1,us2,us3,us4,us5,us6,us7,us8,us9,us10])
db.session.commit()


"""
查询所有用户数据
查询有多少个用户
查询第1个用户
查询id为4的用户[3种方式]
查询名字结尾字符为g的所有数据[开始/包含]
查询名字不等于wang的所有数据[2种方式]
查询名字和邮箱都以 li 开头的所有数据[2种方式]
查询password是 `123456` 或者 `email` 以 `itheima.com` 结尾的所有数据
查询id为 [1, 3, 5, 7, 9] 的用户列表
查询name为liu的角色数据
查询所有用户数据，并以邮箱排序
每页3个，查询第2页的数据
"""
```

#### 查询:

##### filter_by

精确查询,例：返回名字等于wang的所有人

```bash
User.query.filter_by(name='wang').all()
```

##### first

返回查询到的第一个对象

```bash
User.query.first()
```

##### all

返回查询到的所有对象

```bash
User.query.all()
```

##### filter

模糊查询，例：返回名字结尾字符为g的所有数据。

```python
User.query.filter(User.name.endswith('g')).all()
```

##### get

参数为主键，如果主键不存在没有返回内容

```python
User.query.get()
```

##### !=

逻辑非，返回条件满足的所有数据，例：返回名字不等于`wang`的所有数据

```python
User.query.filter(User.name!='wang').all()
```

##### not_

相当于取反，返回条件满足的所有数据，例：返回名字不等于`chen`的所有数据

```python
from sqlalchemy import not_
User.query.filter(not_(User.name=='chen')).all()
```

##### and_

逻辑与，返回条件满足的所有数据，例：返回名字不等于`wang`且邮箱以`163.com`结尾的所有数据

```python
from sqlalchemy import and_
User.query.filter(and_(User.name!='wang',User.email.endswith('163.com'))).all()
```

##### or_

逻辑或，返回条件满足的所有数据，例：返回名字不等于`wang`或者邮箱以`163.com`结尾的所有数据

```python
from sqlalchemy import or_
User.query.filter(or_(User.name!='wang',User.email.endswith('163.com'))).all()
```

#### 查询数据后删除

```python
user = User.query.first()
db.session.delete(user)
db.session.commit()
User.query.all()
```

#### 更新数据

```python
user = User.query.first()
user.name = 'dong'
db.session.commit()
User.query.first()
```

## 数据库迁移

### 简介

在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据。更好的解决办法是使用数据库迁移框架，它可以追踪数据库模式的变化，然后把变动应用到数据库中。在Flask中可以使用Flask-Migrate扩展，来实现数据迁移。并且集成到Flask-Script中，所有操作通过命令就能完成。为了导出数据库迁移命令，Flask-Migrate提供了一个MigrateCommand类，可以附加到flask-script的manager对象上。

### 使用

- 首先要在虚拟环境中安装Flask-Migrate。

  ```bash
  pip install flask-migrate
  ```

- 代码文件内容：

  ```python
  #coding=utf-8
  from flask import Flask
  
  from flask_sqlalchemy import SQLAlchemy
  from flask_migrate import Migrate,MigrateCommand
  from flask_script import Shell,Manager
  
  app = Flask(__name__)
  manager = Manager(app)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test'
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  db = SQLAlchemy(app)
  
  #第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
  migrate = Migrate(app,db) 
  
  #manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
  manager.add_command('db',MigrateCommand)
  
  #定义模型Role
  class Role(db.Model):
      # 定义表名
      __tablename__ = 'roles'
      # 定义列对象
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(64), unique=True)
      user = db.relationship('User', backref='role')
  
      #repr()方法显示一个可读字符串，
      def __repr__(self):
          return 'Role:'.format(self.name)
  
  #定义用户
  class User(db.Model):
      __talbe__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(64), unique=True, index=True)
      #设置外键
      role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  
      def __repr__(self):
          return 'User:'.format(self.username)
        
  if __name__ == '__main__':
      manager.run()
  ```

- 创建迁移仓库
  

  ```bash
  #这个命令会创建migrations文件夹，所有迁移文件都放在里面。
  python database.py db init
  ```

- 创建迁移脚本

  自动创建迁移脚本有两个函数：

  - upgrade()：函数把迁移中的改动应用到数据库中。
  - downgrade()：函数则将改动删除。

  自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。对比不一定完全正确，有可能会遗漏一些细节，需要进行检查

  ```
  python database.py db migrate -m 'initial migration'
  ```

- 更新数据库

  ```bash
  python database.py db upgrade
  ```

- 返回以前的版本

  可以根据history命令找到版本号,然后传给downgrade命令:

  ```bash
  python app.py db history
  
  输出格式：<base> ->  版本号 (head), initial migration
  ```

  - 回滚到指定版本

  ```bash
  python app.py db downgrade 版本号
  ```

## 信号机制

### 简介

Flask信号(signals, or event hooking)允许特定的发送端通知订阅者发生了什么（既然知道发生了什么，那我们可以根据自己业务需求实现自己的逻辑）。Flask提供了一些信号（核心信号）且其它的扩展提供更多的信号。信号依赖于**Blinker**库。

flask内置信号列表：http://docs.jinkan.org/docs/flask/api.html#id17

```python
template_rendered = _signals.signal('template-rendered')
request_started = _signals.signal('request-started')
request_finished = _signals.signal('request-finished')
request_tearing_down = _signals.signal('request-tearing-down')
got_request_exception = _signals.signal('got-request-exception')
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')
appcontext_pushed = _signals.signal('appcontext-pushed')
appcontext_popped = _signals.signal('appcontext-popped')
message_flashed = _signals.signal('message-flashed')
```

### 应用场景

Flask-User 这个扩展中定义了名为 user_logged_in 的信号，当用户成功登入之后，这个信号会被发送。我们可以订阅该信号去追踪登录次数和登录IP：

```python
from flask import request
from flask_user.signals import user_logged_in

@user_logged_in.connect_via(app)
def track_logins(sender, user, **extra):
    user.login_count += 1
    user.last_login_ip = request.remote_addr
    db.session.add(user)
    db.session.commit()
```

### Flask-SQLAlchemy 信号支持

在 Flask-SQLAlchemy 模块中，0.10 版本开始支持信号，可以连接到信号来获取到底发生什么了的通知。存在于下面两个信号：

- models_committed：这个信号在修改的模型提交到数据库时发出。发送者是发送修改的应用，模型 和 操作描述符 以 (model, operation) 形式作为元组，这样的元组列表传递给接受者的 changes 参数。该模型是发送到数据库的模型实例，当一个模型已经插入，操作是 'insert' ，而已删除是 'delete' ，如果更新了任何列，会是 'update' 。
- before_models_committed：除了刚好在提交发送前发生，与 models_committed 完全相同。

```python
from flask_sqlalchemy import models_committed

# 给 models_committed 信号添加一个订阅者，即为当前 app
@models_committed.connect_via(app)
def models_committed(a, changes):
    print(a, changes)
```
