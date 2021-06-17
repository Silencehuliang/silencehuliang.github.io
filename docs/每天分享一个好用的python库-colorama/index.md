# 每天分享一个好用的Python库 Colorama


## 前言
今天分享的是一个主要用来给文本添加各种颜色的库：`colorama`。

## colorama

### 简介

`colorama`是一个可以跨多终端显示不同颜色字符与背景的第三方库。

### 安装

- 使用`pip`进行安装

  ```bash
  $ pip install colorama
  ```


### 简单使用

#### 常用参数

|          |                           字体颜色                           |                         字体背景颜色                         |            字体格式            |
| :------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------: |
| 对应名字 |                             Fore                             |                             Back                             |             Style              |
| 可用颜色 | BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET | BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET | DIM, NORMAL, BRIGHT, RESET_ALL |

{{< admonition waring "注意" true >}}

颜色都需要大写。

{{< /admonition >}}

#### 初次使用

```python
from colorama import Fore, Back, Style
print(Fore.RED + '你好')
print(Back.BLUE + 'colorama库')
print(Style.DIM + '这是字体DIM')
print(Style.RESET_ALL)
print('这是重置后的情况')
```

可以从代码里看出，使用的方法非常简单，结果显示也很酷！

![](https://tva4.sinaimg.cn/large/00729CCqgy1grlcp00aimj30cd05aaao.jpg)

#### Init关键字参数

- `autoreset`：自动重置，可以在每次打印输出后重置对字体相关和背景的修改，默认为False

- `convert`：覆盖是否将输出中的 ANSI 代码转换为 win32 调用。默认行为是在 Windows 上进行转换，并且输出是 tty（终端）

- `strip`：盖是否应从输出中删除 ANSI 代码。默认行为是在 Windows 上或重定向输出（不是 tty）时剥离。

- `wrap`：在 Windows 上，Colorama 通过用 代理对象替换`sys.stdout`和`sys.stderr 来工作`，代理对象会覆盖`.write()`方法来完成它们的工作。如果这种包装给你带来了问题，那么可以通过传递`init(wrap=False)`来禁用它 。如果`autoreset`或 `strip`或`convert`为 True，则默认行为是换`行`。

  禁用环绕后，非 Windows 平台上的彩色打印将继续正常工作。做跨平台彩色输出，可以直接使用Colorama的`AnsiToWin32`代理




### 作用

这个库最棒的作用就是可以个性化控制台输出，爱折腾的人可以调试一个自己喜欢的样式来优化控制台的输出效果！

## 尾巴

从上可以看出，`colorama`库非常的简单易用，其目的也很单一，就是优化控制台输出的样式。提供给那些爱折腾的人一个好玩的选项，当然在项目中需要输出样式有调整的时候也可以用上它，它就是那种小而美的一个库

[官方文档地址](https://pypi.org/project/colorama/)


