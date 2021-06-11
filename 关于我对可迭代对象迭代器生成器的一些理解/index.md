# 关于我对可迭代对象，迭代器，生成器的一些理解

## 可迭代对象(iterable)

可以返回一个迭代器的对象可以称之为可迭代对象。本质上，具备了\__iter\__方法的对象是可迭代对象。在python中我们可以通过isinstance()判断一个对象是否是可迭代对象，常见的可迭代对象有：list，set，dict，tuple，str。

### 实例

```python
In [1]: from collections import Iterable

In [2]: isinstance([],Iterable)
Out[2]: True

In [3]: isinstance(set(),Iterable)
Out[3]: True

In [4]: isinstance(dict(),Iterable)
Out[4]: True

In [5]: isinstance((1,),Iterable)
Out[5]: True

In [6]: isinstance('hello world',Iterable)
Out[6]: True

```

### \_\_iter\__方法

可以返回一个迭代器

### 自定义简单的可迭代对象

```python
In [7]: class A(object):
   ...:     def __iter__(self):
   ...:         """返回一个迭代器"""
   ...:         pass  

In [8]: a = A()
In [9]: isinstance(a,Iterable)
Out[9]: True
```

## 迭代器(Iterator):

在调用next()方法的时候返回可迭代对象中的下一个值的对象可称为迭代器。本质上，实现 \__iter\_\_方法和\_\_next__(python2中next())方法的对象就是迭代器(从这里可以看出迭代器本身也是可迭代对象)

### 实例

```python
In [10]: from collections import Iterator

In [11]: isinstance([], Iterator)
Out[11]: False

In [12]: isinstance(iter([]), Iterator)
Out[12]: True

In [13]: isinstance(iter("abc"), Iterator)
Out[13]: True
```

### _\_iter\_\_方法

可以返回迭代器本身

### \_\_next\_\_方法

可以返回可迭代对象中的下一个值，如果可迭代对象中没有下一个值了，则会抛出StopIteration异常。

在python中我们可以使用isinstance()方法判断一个对象是否为迭代器对象。

### 自定义简单的迭代器

```python
In [14]: class B(object):
    ...: 
    ...:     def __next__(self):
    ...:		“”“记录当前迭代位置”“”
    ...:         pass
    ...: 
    ...:     def __iter__(self):
    ...:		“”“返回迭代器本身”“”
    ...:         pass
    ...:     

In [15]: b = B()

In [16]: from collections import Iterator

In [17]: isinstance(b,Iterable)
Out[17]: True

```

## 生成器(generator)

一次生成一个值的特殊类型函数可称为生成器。简单的说就是在函数的执行过程中，yield语句会把你需要的值返回给调用生成器的地方，然后退出函数，下一次调用生成器函数的时候又从上次中断的地方开始执行，而生成器内的所有变量参数都会被保存下来供下一次使用。

当我们自己实现一个迭代器的时候，当前迭代到的状态需要自己记录，进而才能根据当前状态生成下一个数据，而生成器可以通过yield语句记录当前状态，即生成器是一类特殊的迭代器。

由于生成器是特殊的迭代器所以生成器可以通过next()函数，for循环，list()等方法使用

**tips：在python3在中range()方法返回的对象是一个生成器对象，python2中则是返回遍历结果**

### 使用生成器写斐波那契数列

```python
In [18]: def fib(n):
   ....:     current = 0
   ....:     num1, num2 = 0, 1
   ....:     while current < n:
   ....:         num = num1
   ....:         num1, num2 = num2, num1+num2
   ....:         current += 1
   ....:         yield num
   ....:     return 'None'
```
### yield语句

python解释器执行到yield这一行时会停下，将yield后面的变量返回，再次调用激活yield(调用next()方法等)的时候，会继续执行yield后面的代码(python3中return后面可以添加返回值，python2中return只能退出生成器，后面不能添加返回值)

## 总结

***1.可迭代对象是可以进行迭代操作的对象，具有__iter__方法，调用__iter__方法可以返回一个迭代器
2.迭代器是特殊的可迭代对象，可以记录当前访问位置的对象，具有__next__方法，当通过next()调用__next__(python2中为next)方法时，会返回下一个位置的值。迭代器是一个特殊的可迭代对象，当调用__iter__方法时，会将自己返回。
3.生成器是特殊的迭代器，他自动记录当前迭代的状态，当我们调用调用next()方法的时候会帮我们从上一次停下来的地方继续执行***
