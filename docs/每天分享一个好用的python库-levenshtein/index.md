# 每天分享一个好用的Python库-Levenshtein

## 前言
最近几天处于恢复期间，会不定期更新，感谢大家的关心与支持。今天分享是一个计算字符串相似度的第三方库：`Levenshtein`。

## Levenshtein

### 简介

`Levenshtein`：莱文斯坦距离，又称Levenshtein距离，是编辑距离的一种。 指两个字串之間，由一个转成另一个所需的最少编辑操作次数。 允许的编辑操作包括将一个字符替换成另一个字符，插入一个字符，刪除一个字符。

### 安装

```python
pip install python-Levenshtein
```

### 简单使用

#### 常见方法

- `hamming`：计算汉明距离，两个字符串的长度必须相同。返回两个字串之间对应位置上不同字符的个数。

  ```python
  >>> hamming('Hello world!', 'Holly grail!')
      7
  >>> hamming('Brian', 'Jesus')
      5
  ```

- `distance`：计算一个字串转化成另一个字串最少的操作次数，在其中的操作包括插入、删除、替换

  ```python
  >>> distance('Levenshtein', 'Lenvinsten')
      4
  >>> distance('Levenshtein', 'Levensthein')
      2
  >>> distance('Levenshtein', 'Levenshten')
      1
  >>> distance('Levenshtein', 'Levenshtein')
      0
  ```
- `ratio`：计算莱文斯坦比。计算公式为  r = (sum - ldist) / sum, 其中sum是指str1 和 str2 字串的长度总和，ldist是类编辑距离。

  ```python
  >>> ratio('Hello world!', 'Holly grail!')  # doctest: +ELLIPSIS
      0.583333...
  >>> ratio('Brian', 'Jesus')
      0.0
  ```

  {{< admonition warning "注意" true >}}
  这里的类编辑距离不是2中所说的编辑距离，2中三种操作中每个操作+1，而在此处，删除、插入依然+1，但是替换+2，这样ratio('a', 'c')，sum=2，按2中计算为（2-1）/2 = 0.5，’a'，'c'没有重合，显然不合算，但是替换操作+2，就可以解决这个问题。

  {{< /admonition >}}

- `jaro`：计算两个字符串的 Jaro 字符串相似度度量。

  ```python
  >>> jaro('Brian', 'Jesus')
      0.0
  >>> jaro('Thorkel', 'Thorgier')  # doctest: +ELLIPSIS
      0.779761...
  >>> jaro('Dinsdale', 'D')  # doctest: +ELLIPSIS
      0.708333...
  ```

  {{< admonition info "提示" true >}}

  Jaro 字符串相似度度量适用于短字符串，例如个人姓氏。 对于完全不同的字符串，它是 0 并且1 表示相同的字符串。

  {{< /admonition >}}

- `jaro_winkler`：计算两个字符串的 Jaro 字符串相似度度量。

  ```python
  >>> jaro_winkler('Brian', 'Jesus')
      0.0
  >>> jaro_winkler('Thorkel', 'Thorgier')  # doctest: +ELLIPSIS
      0.867857...
  >>> jaro_winkler('Dinsdale', 'D')  # doctest: +ELLIPSIS
      0.7375...
  >>> jaro_winkler('Thorkel', 'Thorgier', 0.25)
      1.0
  ```

  {{< admonition info "提示" true >}}

  Jaro-Winkler 字符串相似度度量是对 Jaro 的修改，度量给予公共前缀更多的权重，因为拼写错误是更可能出现在词尾附近。

  {{< /admonition >}}


### 作用

这个库是一个专门用于处理两个字符串间差异的库，目前该库很久没有维护，大家可以根据需求来使用。

## 尾巴

该项目的作者正在寻找新的维护者，如果对该项目感兴趣的朋友可以联系作者，将该库一直维护下去！

[官方文档地址](https://pypi.org/project/python-Levenshtein/)
