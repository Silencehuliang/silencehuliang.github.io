# 每天分享一个好用的Python库-shortuuid


## 前言

今天分享是一个一组简洁URL/UUID函数库的第三方库：`shortuuid`。

## shortuuid

### 简介

`shortuuid` 是一个简单的第三方`Python` 库，可以生成简洁、明确、URL 安全的 UUID。

### 安装

```python
pip install shortuuid
```

### 简单使用

- 生成短的uuid

  ```python
  >>> import shortuuid
  >>> shortuuid.uuid()
  'TNEbNCHXTNos848uxHqkd6'
  ```
  
- 根据DNS或者URL生成uuid

  ```python
  >>> shortuuid.uuid(name="baidu.com")
  'KJ65furhUxu7TE6Xue95MD'
  >>> shortuuid.uuid(name="https://silencehuliang.github.io/")
  'cteCmrh3fC6DeX5jzXxxXf'
  ```

- 生成指定长度的uuid

  ```python
  >>> shortuuid.ShortUUID().random(length=8)
  '73mjzeqZ'
  ```

- 查看用于生成uuid的字符

  ```python
  >>> shortuuid.get_alphabet()
  '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  ```

- 指定用于生成uuid的字符

  ```python
  >>> shortuuid.set_alphabet("huliang")
  >>> shortuuid.uuid()
  'auauhhaunhliunagulnnluilhuglhughhiaaahuniuuaug'
  ```

  {{< admonition warning "注意" true >}}

  这里可以看到由于我们给的用于生成uuid的字符比较少，为了安全考虑对应生成的uuid变长了，这个时候指定数量会使用默认的字符，当我们设置更长的字符时，对应生成的uuid就会变短。

  {{< /admonition >}}

  ```python
  >>> shortuuid.ShortUUID().random(length=8)
  'Xwp6drW8'
  >>> shortuuid.set_alphabet("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxy")
  >>> shortuuid.uuid()
  '27FTRikpT2vh7k7aYy5h2sm'
  ```

  


### 作用

该库可以很好地帮助我们设置一个符合我们需求的uuid，不需要我们在对`uuid`库进行二次开发.

## 尾巴

最近生病了还在恢复中，各类文章会逐步更新起来，谢谢大家关心！大家一定要注意身体，这个时候容易生病！

[官方文档地址](https://pypi.org/project/shortuuid/)


