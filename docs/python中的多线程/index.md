# Python中的多线程


## 多线程

### 简介

在日常中经常使用多任务操作，多线程通常是使用最多的一种。

### 并发 

指任务数多余cpu核数，通过操作系统的任务调度算法快速切换任务，从而实现多任务

### 并行 

指任务数小于等于cpu核心数，操作系统可以分配不同的核心同时去实现多任务

### 线程

#### 定义

程序的最小执行流单元，是程序中一个单一的顺序控制流程

#### python中实现多线程的模块

thread和threading，不过threading更高级，是封装thread得到的

#### 简单的多线程

```python
import threading
import time
def run():
    print("我要减肥!")
    time.sleep(1)
if __name__ == '__main__':
    print(time.ctime())
    for i in range(10):
        t = threading.Thread(target=run)
        t.start()
    print(time.ctime())
```

补充：在python3中主进程会等待子进程结束后再结束



我们可以通过enumerate方法来查看当前运行的线程数量

```python
import threading
import time
def run():
    """跑步"""
    for i in range(3):
        print("我要减肥!")
        time.sleep(1)
if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()
    len = len(threading.enumerate())
    print('当前运行的线程数为：%d' % len)
```

#### 多线程间是共享全局变量的

栗子

```python
import threading
import time

weight = 130


def run():
    """跑步"""
    global weight
    for i in range(3):
        print("我要减肥!")
        weight -= 1


def eat():
    """吃东西"""
    global weight
    for i in range(3):
        print("我吃了一顿好吃的")
        weight += 2


if __name__ == '__main__':
    t_run = threading.Thread(target=run)
    t_eat = threading.Thread(target=eat)
    t_run.start()
    t_eat.start()
    time.sleep(0.5)
    print(weight)
```

由于多个线程都可以修改全局变量，会出现资源竞争，导致最后得到的数据可能不是我们想要的。

```python
import threading
import time

weight = 130

def run():
	"""跑步"""
    global weight
    for i in range(3):
        # print("我要减肥!")
        weight -= 1
    print(weight)

def eat():
	"""吃东西"""
    global weight
    for i in range(3):
        # print("我吃了一顿好吃的")
        weight += 1
    print(weight)

def sedentariness():
    """久坐"""
    global weight
    for i in range(3):
        weight += 1
    print(weight)

if __name__ == '__main__':
    t_run = threading.Thread(target=run)
    t_eat = threading.Thread(target=eat)
    t_sedentariness = threading.Thread(target=sedentariness)
    # t_run.start()
    t_eat.start()
    t_sedentariness.start()
```

这里我们可以看到eat方法和sendentariness方法都是加weight，我们想得到两个133，但是最后结果是一个133，一个136.（tips：线程只有在调用了start方法才会开启，这里没有调用run的start方法，所以没有开启run方法的线程）

这时候我们可以加上互斥锁，在一个线程使用全局变量时其他线程不能修改




