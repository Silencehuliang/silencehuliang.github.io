# 每天分享一个好用的Python库-difflib

## 前言
由于生病了几天，导致该系列拖更了，今天稍微好点了，继续开始更新。今天分享是一个Python标准库，主要用于计算文本间的差异：`difflib`。

## difflib

### 简介

`difflib` 是Python标准库中一个可用于对比文本之间的差异，并且支持输出HTML文档的库。

### 安装

Python标准库，无需安装。

### 简单使用

#### 常见类

- `Differ`：是一个用于比较文本行序列的类，并且产生人类可读的差异或增量。

  - `compare`：比较两个行序列； 生成结果增量。

    ```python
    >>> print(''.join(Differ().compare('one\ntwo\nthree\n'.splitlines(True),
            ...                                'ore\ntree\nemu\n'.splitlines(True))),
            ...       end="")
            - one
            ?  ^
            + ore
            ?  ^
            - two
            - three
            ?  -
            + tree
            + emu
    ```

- `HtmlDiff`：用于生成 HTML 并与更改亮点进行比较。此类可用于创建 HTML 表格（或包含该表格的完整 HTML 文件），显示文本与行间和行内更改突出显示的并排、逐行比较。该表可以以完整或上下文差异模式生成。为 HTML 生成提供了以下方法：

  - `make_table`：为单个并排表格生成 HTML。
    - `make_file`：使用一个并排表格生成完整的 HTML 文件。
  
#### 常用方法

`ratio`：用[0,1]的范围返回序列相似性的度量，作为[0,1]范围内的浮点数。值超过 0.6 意味着序列接近匹配。


### 作用

这个库与Linux下的`vimdiff`命令功能一样，在Python中可以更好的让我们处理对比文档的结果。

## 尾巴

Python标准库也需要大家都进行学习的，里面充满着很多有意思的库，不需要在重复造轮子了。

大家一定要保重身体，身体才是革命的本钱。由于本人目前还很虚弱，爬虫系列的更新会再晚一些，请再给我一点时间。

[官方文档地址](https://docs.python.org/zh-cn/3/library/difflib.html)


