# Python学习之路-单元测试


## 为什么要测试

程序开发过程一般包括以下几个阶段：需求分析，设计阶段，实现阶段，测试阶段。其中测试阶段通过人工或自动来运行测试某个系统的功能。目的是检验其是否满足需求，并得出特定的结果，以达到弄清楚预期结果和实际结果之间的差别的最终目的。

## 测试的分类

测试从软件开发过程可以分为：

- 单元测试：对单独的代码块(例如函数)分别进行测试,以保证它们的正确性
- 集成测试：对大量的程序单元的协同工作情况做测试
- 系统测试：同时对整个系统的正确性进行检查,而不是针对独立的片段

在众多的测试中，与程序开发人员最密切的就是单元测试，因为单元测试是由开发人员进行的，而其他测试都由专业的测试人员来完成。所以我们主要学习单元测试。

## 什么是单元测试

程序开发过程中，写代码是为了实现需求。当我们的代码通过了编译，只是说明它的语法正确，功能能否实现则不能保证。 因此，当我们的某些功能代码完成后，为了检验其是否满足程序的需求。可以通过编写测试代码，模拟程序运行的过程，检验功能代码是否符合预期。

单元测试就是开发者编写一小段代码，检验目标代码的功能是否符合预期。通常情况下，单元测试主要面向一些功能单一的模块进行。

举个例子：一部手机有许多零部件组成，在正式组装一部手机前，手机内部的各个零部件，CPU、内存、电池、摄像头等，都要进行测试，这就是单元测试。

在开发过程中，单元测试实际上就是一些“断言”（assert）代码。

断言就是判断一个函数或对象的一个方法所产生的结果是否符合你期望的那个结果。 `Python`中`assert`断言是声明布尔值为真的判定，如果表达式为假会发生异常。单元测试中，一般使用`assert`来断言结果。

## 常用的断言方法

```
assertEqual     如果两个值相等，则pass
assertNotEqual  如果两个值不相等，则pass
assertTrue      判断bool值为True，则pass
assertFalse     判断bool值为False，则pass
assertIsNone    不存在，则pass
assertIsNotNone 存在，则pass
```

## 基本写法

**首先**，定义一个类，继承自unittest.TestCase

```python
import unittest
class TestClass(unitest.TestCase):
    pass
```

**其次**，在测试类中，定义两个测试方法

```python
import unittest
class TestClass(unittest.TestCase):

    #该方法会首先执行，方法名为固定写法
    def setUp(self):
        pass

    #该方法会在测试代码执行完后执行，方法名为固定写法
    def tearDown(self):
        pass
```

**最后**，在测试类中，编写测试代码

```python
import unittest
class TestClass(unittest.TestCase):

    #该方法会首先执行，相当于做测试前的准备工作
    def setUp(self):
        pass

    #该方法会在测试代码执行完后执行，相当于做测试后的扫尾工作
    def tearDown(self):
        pass
    #测试代码
    def test_app_exists(self):
        pass
```


