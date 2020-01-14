---
title: "Django2.x配置mysql"
description: "Django2.x配置mysql"
date: 2019-01-21
draft: false
categories: ["Django"] 
tags: ["pymsql","Django2.x"]
---

**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

## 简介

在Django中使用mysql数据库是很常见的,但是升级到Django2.0以后，已经不支持Python2.x，mysql的配置也需要随之改变



## 配置

### 配置settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST':'dbhost',
        'PORT':'dbport'
    }
}
```



### 使用pymysql

由于安装mysqlclient不支持python3，所以使用pymysql包，安装pymysql并导入

```python
pip install pymysql
```

配置pymysql，在settings.py所在的目录下的\_\_init\_\_.py文件中导入

```python
import pymysql
pymysql.install_as_MySQLdb()
```



### 修改源码中的问题

- 由于在python3中不在使用mysqlclient，所以源码中限制mysqlclient版本这一代码就不适用于现在的环境

  文件路径`django\db\backends\mysql\base.py`，将版本限制异常给注释掉在文件的第35-36行

  ```python
  # if version < (1, 3, 13):
  #     raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
  ```

- 由于python2的str是字节流(类似于bytes类型)需要通过decode转换成unicode类型才能使用，但在python3中str默认unicode类型不需要转换且没有decode解码所以要将这里的代码修改。在最新的Django源码中已经将这里修改了(可以通过Django官网或github查看)，在最新的源码中使用django.utils.encoding中force_str方法解决了该问题，force_str方法实际上是force_text方法，force_text方法通过判断传入参数的类型后将类型转为unicode类型的str之后返回

  ```python
  \django\utils\encoding.py
  ······
  def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
      """
      Similar to smart_text, except that lazy instances are resolved to
      strings, rather than kept as lazy objects.
  
      If strings_only is True, don't convert (some) non-string-like objects.
      """
      # Handle the common case first for performance reasons.
      if issubclass(type(s), str):
          return s
      if strings_only and is_protected_type(s):
          return s
      try:
          if isinstance(s, bytes):
              s = str(s, encoding, errors)
          else:
              s = str(s)
      except UnicodeDecodeError as e:
          raise DjangoUnicodeDecodeError(s, *e.args)
      return s
  ```

  最后修改\django\db\backends\mysql\operations.py文件中的last_executed_query方法（记得导入force_str）

  ```python
      from django.utils.encoding import force_str
      ···
      def last_executed_query(self, cursor, sql, params):
          # With MySQLdb, cursor objects have an (undocumented) "_executed"
          # attribute where the exact query sent to the database is saved.
          # See MySQLdb/cursors.py in the source distribution.
          # MySQLdb returns string, PyMySQL bytes.
          return force_str(getattr(cursor, '_executed', None), errors='replace')
  ```





