# 每天分享一个好用的Python库-sqlparse


## 前言

今天分享一个可以对SQL语句进行解析、拆分和格式化的第三方库：`sqlparse`。

## sqlparse

### 简介

`sqlparse` 是 Python 的非验证 SQL 解析器。 它提供对 SQL 语句的解析、拆分和格式化的支持。 该模块与 Python 3.5 兼容，并根据新 BSD 许可条款发布。 

### 安装

```python
pip install sqlparse
```

### 简单使用

- 拆分包含两个 SQL 语句的字符串：

  ```python
  >>> import sqlparse
  >>> raw = 'select * from blog; select * from post;'
  >>> statements = sqlparse.split(raw)
  >>> statements
  ['select * from blog;', 'select * from post;']
  
  ```

- 格式化第一条语句并打印出来：

  ```bash
  >>> first = statements[0]
  >>> print(sqlparse.format(first, reindent=True, keyword_case='upper'))
  SELECT *
  FROM book;
  ```
  
- 解析一条 SQL 语句：

  ```python
  >>> parsed = sqlparse.parse('select * from blog')[0]
  >>> parsed.tokens
  [<DML 'select' at 0x10E808980>, <Whitespace ' ' at 0x10E808A60>, <Wildcard '*' at 0x10E808AD0>, <Whitespace ' ' at 0x10E808B40>, <Keyword 'from' at 0x10E8089F0>, <Whitespace ' ' at 0x10E808C20>, <Identifier 'blog' at 0x10E7DFED0>]
  ```

### 作用

`sqlparse`可以帮助我们一定程度上去处理SQL语句，使我们对SQL处理起来更方便。

## 尾巴

像`sqlparse`这种工具类的库，可以使我们平时少造轮子，根据具体需求改一改就可以解决我们的问题，大大提高开发效率。

[官方文档地址](https://pypi.org/project/sqlparse/)
