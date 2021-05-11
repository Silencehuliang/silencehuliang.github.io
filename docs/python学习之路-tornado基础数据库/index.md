# Python学习之路-Tornado基础:数据库


## 简介

与Django框架相比，Tornado没有自带ORM，对于数据库需要自己去适配。我们使用MySQL数据库。

在Tornado3.0版本以前提供tornado.database模块用来操作MySQL数据库，而从3.0版本开始，此模块就被独立出来，作为torndb包单独提供。torndb只是对MySQLdb的简单封装，不支持Python 3。

## 连接初始化

我们需要在应用启动时创建一个数据库连接实例，供各个RequestHandler使用。我们可以在构造Application的时候创建一个数据库实例并作为其属性，而RequestHandler可以通过self.application获取其属性，进而操作数据库实例。

```python
import torndb

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # 创建一个全局mysql连接实例供handler使用
        self.db = torndb.Connection(
            host="127.0.0.1",
            database="itcast",
            user="root",
            password="mysql"
        )
```

## 使用数据库

- 新建数据库与表
- 执行语句，执行语句主要用来执行非查询语句。

  - execute(query, *parameters, **kwparameters) 返回影响的最后一条自增字段值
  - execute_rowcount(query, *parameters, **kwparameters) 返回影响的行
  - query为要执行的sql语句，parameters与kwparameters为要绑定的参数
- 查询语句

  - get(query, *parameters, **kwparameters) 返回单行结果或None，若出现多行则报错。返回值为torndb.Row类型，是一个类字典的对象，即同时支持字典的关键字索引和对象的属相访问。
  - query(query, *parameters, **kwparameters) 返回多行结果，torndb.Row的列表。


