# Python学习之路-多任务:协程


## 简介

协程，又称微线程，纤程。英文名Coroutine。协程是python个中另外一种实现多任务的方式，只不过比线程更小占用更小执行单元（理解为需要的资源）。 为啥说它是一个执行单元，因为它自带CPU上下文。这样只要在合适的时机， 我们可以把一个协程 切换到另一个协程。 只要这个过程中保存或恢复 CPU上下文那么程序还是可以运行的。

通俗的理解：在一个线程中的某个函数，可以在任何地方保存当前函数的一些临时变量等信息，然后切换到另外一个函数中执行，注意不是通过调用函数的方式做到的，并且切换的次数以及什么时候再切换到原来的函数都由开发者自己确定

## 协程和线程差异

在实现多任务时, 线程切换从系统层面远不止保存和恢复 CPU上下文这么简单。 操作系统为了程序运行的高效性每个线程都有自己缓存Cache等等数据，操作系统还会帮你做这些数据的恢复操作。 所以线程的切换非常耗性能。但是协程的切换只是单纯的操作CPU的上下文，所以一秒钟切换个上百万次系统都抗的住。

## 迭代

迭代是访问集合元素的一种方式。使用for...in...的循环语法从其中依次拿到数据进行使用，我们把这样的过程称为遍历，也叫迭代。

## 迭代器

迭代器是一个可以记住遍历的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。

## 可迭代对象

把可以通过for...in...这类语句迭代读取一条数据供我们使用的对象称之为可迭代对象（Iterable）。可以使用 isinstance() 判断一个对象是否是可迭代对象 Iterable 对象。

### 可迭代对象的本质

我们分析对可迭代对象进行迭代使用的过程，发现每迭代一次（即在for...in...中每循环一次）都会返回对象中的下一条数据，一直向后读取数据直到迭代了所有数据后结束。那么，在这个过程中就应该有一个“人”去记录每次访问到了第几条数据，以便每次迭代都可以返回下一条数据。我们把这个能帮助我们进行数据迭代的“人”称为迭代器(Iterator)。

可迭代对象的本质就是可以向我们提供一个这样的中间“人”即迭代器帮助我们对其进行迭代遍历使用。

可迭代对象通过`__iter__`方法向我们提供一个迭代器，我们在迭代一个可迭代对象的时候，实际上就是先获取该对象提供的一个迭代器，然后通过这个迭代器来依次获取对象中的每一个数据.

那么也就是说，一个具备了`__iter__`方法的对象，就是一个可迭代对象。

{{< admonition warning "注意" true >}}

可以通过iter()函数获取这些可迭代对象的迭代器(`iter()`函数实际上就是调用了可迭代对象的`__iter__`方法)，然后我们可以对获取到的迭代器不断使用`next()`函数来获取下一条数据(使用`next()`函数的时候，调用的就是迭代器对象的`__next__`方法)。当我们已经迭代完最后一个数据之后，再次调用next()函数会抛出StopIteration的异常，来告诉我们所有数据都已迭代完成，不用再执行next()函数了。

{{< /admonition >}}

### for...in...循环的本质

for item in Iterable 循环的本质就是先通过iter()函数获取可迭代对象Iterable的迭代器，然后对获取到的迭代器不断调用next()方法来获取下一个值并将其赋值给item，当遇到StopIteration的异常后循环结束。

## 生成器

### 简介

生成器是一类特殊的迭代器。利用迭代器，我们可以在每次迭代获取数据（通过next()方法）时按照特定的规律进行生成。但是我们在实现一个迭代器时，关于当前迭代到的状态需要我们自己记录，进而才能根据当前状态生成下一个数据。为了达到记录当前状态，并配合next()函数进行迭代使用，我们可以采用更简便的语法，即生成器(generator)

### 创建生成器方法

- 只要把一个列表生成式的 [ ] 改成 ( )，如下

  ```python
  In [1]: A = [ x*2 for x in range(5)]
  
  In [2]: A
  Out[2]: [0, 2, 4, 6, 8]
  
  In [3]: B = ( x*2 for x in range(5))
  
  In [4]: B
  Out[4]: <generator object <genexpr> at 0x7f626c132db0>
  ```

  创建 L 和 G 的区别仅在于最外层的 [ ] 和 ( ) ， L 是一个列表，而 G 是一个生成器。我们可以直接打印出列表L的每一个元素，而对于生成器G，我们可以按照迭代器的使用方法来使用，即可以通过next()函数、for循环、list()等方法使用。

  ```python
  In [5]: next(G)
  Out[5]: 0
  
  In [6]: next(G)
  Out[6]: 2
  
  In [7]: next(G)
  Out[7]: 4
  
  In [8]: next(G)
  Out[8]: 6
  
  In [9]: next(G)
  Out[9]: 8
  
  In [10]: next(G)
  ---------------------------------------------------------------------------
  StopIteration                             Traceback (most recent call last)
  <ipython-input-24-380e167d6934> in <module>()
  ----> 1 next(G)
  
  StopIteration:
    
  In [11]:
  In [12]: G = ( x*2 for x in range(5))
  
  In [13]: for x in G:
     ....:     print(x)
     ....:     
  0
  2
  4
  6
  8
  
  In [14]:
  ```

- 将原本在迭代器`__next__`方法中实现的基本逻辑放到一个函数中来实现，但是将每次迭代返回数值的return换成了yield，此时新定义的函数便不再是函数，而是一个生成器了。简单来说：只要在def中有yield关键字的 就称为 生成器。用生成器实现斐波那契数列

  ```python
  In [15]: def fib(n):
     ....:     current = 0
     ....:     num1, num2 = 0, 1
     ....:     while current < n:
     ....:         num = num1
     ....:         num1, num2 = num2, num1+num2
     ....:         current += 1
     ....:         yield num
     ....:     return 'done'
     ....:
  
  In [16]: F = fib(5)
  
  In [17]: next(F)
  Out[17]: 1
  
  In [18]: next(F)
  Out[18]: 1
  
  In [19]: next(F)
  Out[19]: 2
  
  In [20]: next(F)
  Out[20]: 3
  
  In [21]: next(F)
  Out[21]: 5
  
  In [22]: next(F)
  ---------------------------------------------------------------------------
  StopIteration                             Traceback (most recent call last)
  <ipython-input-22-8c2b02b4361a> in <module>()
  ----> 1 next(F)
  
  StopIteration: done
  ```

  此时按照调用函数的方式( 案例中为F = fib(5) )使用生成器就不再是执行函数体了，而是会返回一个生成器对象（ 案例中为F ），然后就可以按照使用迭代器的方式来使用生成器了。

  ```python
  In [23]: for n in fib(5):
     ....:     print(n)
     ....:     
  1
  1
  2
  3
  5
  ```

  

  但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中：

  ```python
  In [25]: g = fib(5)
  
  In [26]: while True:
     ....:     try:
     ....:         x = next(g)
     ....:         print("value:%d"%x)      
     ....:     except StopIteration as e:
     ....:         print("生成器返回值:%s"%e.value)
     ....:         break
     ....:     
  value:1
  value:1
  value:2
  value:3
  value:5
  生成器返回值:done
  ```

### 使用send唤醒

我们除了可以使用next()函数来唤醒生成器继续执行外，还可以使用send()函数来唤醒执行。使用send()函数的一个好处是可以在唤醒的同时向断点处传入一个附加数据。

例子：执行到yield时，gen函数作用暂时保存，返回i的值; temp接收下次c.send("python")，send发送过来的值，c.next()等价c.send(None)

```python
In [27]: def gen():
   ....:     i = 0
   ....:     while i<5:
   ....:         temp = yield i
   ....:         print(temp)
   ....:         i+=1
   ....:
```

使用send

```python
In [28]: f = gen()

In [29]: next(f)
Out[29]: 0

In [30]: f.send('haha')
haha
Out[30]: 1

In [31]: next(f)
None
Out[31]: 2

In [32]: f.send('haha')
haha
Out[32]: 3
```

使用next函数

```python
In [33]: f = gen()

In [34]: next(f)
Out[34]: 0

In [35]: next(f)
None
Out[35]: 1

In [36]: next(f)
None
Out[36]: 2

In [37]: next(f)
None
Out[37]: 3

In [38]: next(f)
None
Out[38]: 4

In [39]: next(f)
None
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-17-468f0afdf1b9> in <module>()
----> 1 next(f)

StopIteration:
```

使用`__next__()`方法（不常使用）

```python
In [40]: f = gen()

In [41]: f.__next__()
Out[41]: 0

In [42]: f.__next__()
None
Out[42]: 1

In [43]: f.__next__()
None
Out[43]: 2

In [44]: f.__next__()
None
Out[44]: 3

In [45]: f.__next__()
None
Out[45]: 4

In [46]: f.__next__()
None
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-24-39ec527346a9> in <module>()
----> 1 f.__next__()

StopIteration:
```

## 简单实现协程

```python
import time

def work1():
    while True:
        print("----work1---")
        yield
        time.sleep(0.5)

def work2():
    while True:
        print("----work2---")
        yield
        time.sleep(0.5)

def main():
    w1 = work1()
    w2 = work2()
    while True:
        next(w1)
        next(w2)

if __name__ == "__main__":
    main()
```

运行结果：

```python
----work1---
----work2---
----work1---
----work2---
----work1---
----work2---
----work1---
----work2---
----work1---
----work2---
----work1---
----work2---
...省略...
```

## greenlet

为了更好使用协程来完成多任务，python中的greenlet模块对其封装，从而使得切换任务变的更加简单

### 安装

使用如下命令安装greenlet模块:

```bash
sudo pip3 install greenlet
```

### 简单实现

```python
from greenlet import greenlet
import time

def test1():
    while True:
        print "---A--"
        gr2.switch()
        time.sleep(0.5)

def test2():
    while True:
        print "---B--"
        gr1.switch()
        time.sleep(0.5)

gr1 = greenlet(test1)
gr2 = greenlet(test2)

#切换到gr1中运行
gr1.switch()
```

运行效果：

```python
---A--
---B--
---A--
---B--
---A--
---B--
---A--
---B--
...省略...
```

## gevent

greenlet已经实现了协程，但是这个还的人工切换，是不是觉得太麻烦了，不要捉急，python还有一个比greenlet更强大的并且能够自动切换任务的模块`gevent`

其原理是当一个greenlet遇到IO(指的是input output 输入输出，比如网络、文件操作等)操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。

由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO

### 安装

使用如下命令安装gevent模块:

```bash
pip3 install gevent
```

### 简单实现

```python
import gevent

def f(n):
    for i in range(n):
        print(gevent.getcurrent(), i)

g1 = gevent.spawn(f, 5)
g2 = gevent.spawn(f, 5)
g3 = gevent.spawn(f, 5)
g1.join()
g2.join()
g3.join()
```

运行结果

```python
<Greenlet at 0x10e49f550: f(5)> 0
<Greenlet at 0x10e49f550: f(5)> 1
<Greenlet at 0x10e49f550: f(5)> 2
<Greenlet at 0x10e49f550: f(5)> 3
<Greenlet at 0x10e49f550: f(5)> 4
<Greenlet at 0x10e49f910: f(5)> 0
<Greenlet at 0x10e49f910: f(5)> 1
<Greenlet at 0x10e49f910: f(5)> 2
<Greenlet at 0x10e49f910: f(5)> 3
<Greenlet at 0x10e49f910: f(5)> 4
<Greenlet at 0x10e49f4b0: f(5)> 0
<Greenlet at 0x10e49f4b0: f(5)> 1
<Greenlet at 0x10e49f4b0: f(5)> 2
<Greenlet at 0x10e49f4b0: f(5)> 3
<Greenlet at 0x10e49f4b0: f(5)> 4
```

可以看到，3个greenlet是依次运行而不是交替运行

### 切换执行

```python
import gevent

def f(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        #用来模拟一个耗时操作，注意不是time模块中的sleep
        gevent.sleep(1)

g1 = gevent.spawn(f, 5)
g2 = gevent.spawn(f, 5)
g3 = gevent.spawn(f, 5)
g1.join()
g2.join()
g3.join()
```

运行结果

```python
<Greenlet at 0x7fa70ffa1c30: f(5)> 0
<Greenlet at 0x7fa70ffa1870: f(5)> 0
<Greenlet at 0x7fa70ffa1eb0: f(5)> 0
<Greenlet at 0x7fa70ffa1c30: f(5)> 1
<Greenlet at 0x7fa70ffa1870: f(5)> 1
<Greenlet at 0x7fa70ffa1eb0: f(5)> 1
<Greenlet at 0x7fa70ffa1c30: f(5)> 2
<Greenlet at 0x7fa70ffa1870: f(5)> 2
<Greenlet at 0x7fa70ffa1eb0: f(5)> 2
<Greenlet at 0x7fa70ffa1c30: f(5)> 3
<Greenlet at 0x7fa70ffa1870: f(5)> 3
<Greenlet at 0x7fa70ffa1eb0: f(5)> 3
<Greenlet at 0x7fa70ffa1c30: f(5)> 4
<Greenlet at 0x7fa70ffa1870: f(5)> 4
<Greenlet at 0x7fa70ffa1eb0: f(5)> 4
```

### 给程序打补丁

```python
from gevent import monkey
import gevent
import random
import time

def coroutine_work(coroutine_name):
    for i in range(10):
        print(coroutine_name, i)
        time.sleep(random.random())

gevent.joinall([
        gevent.spawn(coroutine_work, "work1"),
        gevent.spawn(coroutine_work, "work2")
])
```

运行结果

```python
work1 0
work1 1
work1 2
work1 3
work1 4
work1 5
work1 6
work1 7
work1 8
work1 9
work2 0
work2 1
work2 2
work2 3
work2 4
work2 5
work2 6
work2 7
work2 8
work2 9
```

### monkey

```python
from gevent import monkey
import gevent
import random
import time

# 有耗时操作时需要
monkey.patch_all()  # 将程序中用到的耗时操作的代码，换为gevent中自己实现的模块

def coroutine_work(coroutine_name):
    for i in range(10):
        print(coroutine_name, i)
        time.sleep(random.random())

gevent.joinall([
        gevent.spawn(coroutine_work, "work1"),
        gevent.spawn(coroutine_work, "work2")
])
```

运行结果

```python
work1 0
work2 0
work1 1
work1 2
work1 3
work2 1
work1 4
work2 2
work1 5
work2 3
work1 6
work1 7
work1 8
work2 4
work2 5
work1 9
work2 6
work2 7
work2 8
work2 9
```



## 进程、线程、协程对比

1. 进程是资源分配的单位
2. 线程是操作系统调度的单位
3. 进程切换需要的资源很最大，效率很低
4. 线程切换需要的资源一般，效率一般（当然了在不考虑GIL的情况下）
5. 协程切换任务资源很小，效率高
6. 多进程、多线程根据cpu核数不一样可能是并行的，但是协程是在一个线程中 所以是并发
