# Python学习之路-编码风格


## 设计哲学

Python的设计哲学是“优雅”、“明确”、“简单”。它的重要准则被称为“Python之禅”。**Python之禅**又名[PEP 20](https://www.python.org/dev/peps/pep-0020/)，在Python解释器内运行`import this`可以获得完整的列表，下面是我的翻译与解读：

```
提姆·彼得斯（Tim Peters）撰写的《 Python之禅 》
优雅胜于丑陋（以编写优雅的代码为目标）
明确胜于晦涩（明确的代码增强了程序的可读性）
简单胜于复杂（简单的代码能解决复杂的问题）
复杂胜于凌乱（如果项目变得复杂，那代码间也要保持简洁）
扁平胜于嵌套（优雅的代码应该是扁平的，不能有太多嵌套）
间隔胜于紧凑（优雅的代码应当有适当的间隔，不要写一些为了缩减代码丢失了可读性）
可读性很重要（代码的可读的非常重要）
即便假借特例的实用性之名，也不可违背这些规则（这些规则是写Python程序的必备条件）
不要包容所有错误，除非你确定需要这样做（代码中不能存在错误，要善于使用捕获异常）
当存在多种可能，不要尝试去猜测
而是尽量找一种，最好是唯一一种明显的解决方案
虽然这并不容易，因为你不是 Python 之父（虽然你不是Guido，在设计程序时应该多思考，找出最好的解决方案）
做也许好过不做，但不假思索就动手还不如不做（要思考好之后再开始写代码）
如果你无法向人描述你的方案，那肯定不是一个好方案；反之亦然（好的方案是人人都能懂得方案）
命名空间是一种绝妙的理念，我们应当多加利用（要善于利用命令空间）
```

Python开发的哲学是“用一种方法，最好是只有一种方法来做一件事”。在设计Python程序时，如果面临多种选择，一般会拒绝花俏的语法，而选择明确没有或者很少有歧义的语法。



## 编码规范

PEP 8是由Guido van Rossum , Barry Warsaw , Nick Coghlan三位共同编写的一个Python代码风格规范。可以在[这里](https://www.python.org/dev/peps/pep-0008/)查看具体内容，如果英文不好可以在[菜鸟教程](https://www.runoob.com/w3cnote/google-python-styleguide.html)中查看主要的内容

### 检查工具

**pylint**是一个Python代码风格的检查工具, 它依据的标准是Guido van Rossum的[PEP 8](https://www.python.org/dev/peps/pep-0008/)。

pylint类似于PyChecker, 但提供了更多的功能, 如检查代码行的长度, 检查变量命名是否符合编码规范, 或检查声明的接口是否被真正的实现, 完整的检查功能请参见http://www.logilab.org/card/pylintfeatures。

pylint的最大优势在于其高度的可配置化和可定制化，你可以很容易地写一个小插件添加个人功能。

### 用法示例

```
 pylint.bat --reports=n --include-ids=y --disable-msg=W0122,W0702 xlsconverter.py > lint_result.txt
```

其中：

- --reports=n 表示不产生输出报告
- --include-ids=y 表示输出的错误信息包含错误编号
- --disable-msg=W0122,W0702 表示W0122和W0702这两个警告信息被过滤掉了
- xlsconverter.py 是被检查的脚本
- 检查的结果被输出到了lint_result.txt中。

{{< admonition tip "提示" true >}}

PEP 20和PEP 8应该陪伴我们整个学习和使用Python的过程，在编码前多思考。

{{< /admonition >}}
