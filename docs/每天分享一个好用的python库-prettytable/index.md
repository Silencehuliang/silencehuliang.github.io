# 每天分享一个好用的Python库-Prettytable

## 前言
今天分享的是一个主要用于在终端或浏览器端构建格式化的输出的库：`Prettytable`。

## Prettytable

### 简介

`PrettyTable` 是Python中一个可用来生成美观的ASCII格式表格的第三方库。

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install PrettyTable
  ```


### 简单使用

- 创建一个`PrettyTable`对象，并添加数据

  ```python
  import prettytable as pt
  
  tb = pt.PrettyTable()
  tb.field_names = ["股票名称", "持仓数量", "最新价", "盈亏比例%"]
  tb.add_row(["贵州茅台", 1200, 2078.17, 520])
  tb.add_row(["宁德时代", 5900, 446.78, 1314])
  tb.add_row(["常山北明", 11200, 12.13, 1996])
  tb.add_row(["中远海控", 135700, 27.64, 1997])
  
  print(tb)
  ```

  效果如下：

  ![](https://tva3.sinaimg.cn/large/00729CCqgy1grmd7zpt2mj30je089mz0.jpg)

- 添加一列数据

  ```python
  tb.add_column('盈亏', [24960004, 2631400, 135856, 3750748])
  print(tb)
  ```

  效果如下：

  ![](https://tva2.sinaimg.cn/large/00729CCqgy1grmdeehg32j30nb08ggnv.jpg)

- 设置输出风格

  ```python
  tb.set_style(pt.PLAIN_COLUMNS)
  print(tb)
  ```

  效果如下：

  ![](https://tva3.sinaimg.cn/large/00729CCqgy1grmdgprfwrj30vc05v0ua.jpg)

- 设置随机输出风格

  ```python
  tb.set_style(pt.RANDOM)
  print(tb)
  ```

  {{< admonition tip "提醒" true >}}

  还可以自定义表格输出的样式，选择有很多，可以看文档进行选择

  {{< /admonition >}}

  


### 作用

这个库与昨天分享的`Colorama`都是为我们个性化控制台输出给出更多的可能，爱折腾的人可以调试一个自己喜欢的样式来优化控制台的输出效果！

## 尾巴

从上可以看出，`Prettytable`库也非常的简单易用，这些库可能有些人觉得很没用，但是当你需要用到的时候就会发现，他真的很简单很好用，值得尝试！

[官方文档地址](https://pypi.org/project/prettytable/)


