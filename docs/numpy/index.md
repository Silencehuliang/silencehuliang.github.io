# NumPy

## NumPy
### 安装
- 通过安装Anaconda安装NumPy，一个开源的Python发行版本，其包含了conda、Python等180多个科学包及其依赖项，包含了大量的科学计算相关的包，其中就包括NumPy
- 通过pip安装，
    - 在windows中，控制台中输入命令安装  
    ```python
    >pip install numpy
    ```
    - 在ubuntu中,控制台输入命令安装
    ```python
    XXX:~/Desktop$sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
    ```
- 安装验证,进入python交互终端，输入命令，没有报错则安装成功
    ```python
    >python
    >>> import numpy as np
    ```
### numpy中最重要的对象---ndarray：    
**Ndarray对象指的是用于存放同类型元素的多维数据,它是一个多维容器，N代表着它的维度**


#### 创建ndarray对象
- 通过array方法创建   
    - 参数说明
        - 必选参数 
            - object 	数组或嵌套的数列
        - 可选参数
            - dtype 	数组元素的数据类型
            - copy 	    对象是否需要复制
            - order     创建数组的样式，C为行方向，F为列方向，A为任意方向（默认）
            - subok 	默认返回一个与基类类型一致的数组
            - ndmin 	指定生成数组的最小维度
    - demo
      ```python
      >>> from numpy as np
      >>> x = np.array([[1, 2, 3], [4, 5, 6]],dtype=np.int32,copy=True,order=None,subok=False,ndmin=0)
      >>> type(x) # 查看x类型
      <type 'numpy.ndarray'>
      >>> x.shape # 查看ndarray对象的维度
      (2, 3)
      >>> x.dtype # 查看x里的数据类型
      dtype('int32')
      ```
- 通过zeros/ones方法创建(创建指定大小的数组，数组元素以 0/1 来填充,)
    - 参数说明
        - 必要参数
            - shape 	数组形状
        - 可选参数
            - dtype 	数据类型
            - order 	'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组
    - demo
      ```python
      >>> np.zeros(5)
      array([0., 0., 0., 0., 0.])
      >>> np.zeros((3,3))
      array([[0., 0., 0.],
             [0., 0., 0.],
             [0., 0., 0.]])
      ```
- 通过empty方法创建（创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组：）
    - 参数说明
        - 必要参数
            - shape 	数组形状
        - 可选参数
            - dtype 	数据类型
            - 有"C"和"F"两个选项,分别代表，行优先和列优先，在计算机内存中的存储元素的顺序
    - demo
      ```python
      >>> x = np.empty((3,2),dtype=int)
      >>> x
      array([[0, 0],
            [0, 0],
            [0, 0]])
      >>> y = np.empty([3,2],dtype=int)
      >>> y
      array([[0, 0],
             [0, 0],
             [0, 0]])
      ```
- 其他方法：
    - 通过full方法创建（创建一个填充给定值的n * n数组）
    - demo
      ```python
      >>> np.full([3,3],3)
      array([[3, 3, 3],
             [3, 3, 3],
             [3, 3, 3]])
      ```
    - 通过eye方法创建（创建一个对角线是1，其余是0的多维数组）
    - demo
      ```python
      >>> np.eye(3)
      array([[1., 0., 0.],
             [0., 1., 0.],
             [0., 0., 1.]])
      >>> np.eye(1)
      array([[1.]])
      ```
    - 通过linspace方法创建（创建一个在指定的时间间隔内返回均匀间隔的数字的数组）
    - demo
      ```python 
      >>> np.linspace(0,8.8,num=5)
      array([0. , 2.2, 4.4, 6.6, 8.8])
      ```
    - 通过random方法创建（创建一个填充0到1之间随机值的数组）
    - demo
      ```python
      >>> np.random.random([3,3])
      array([[0.17647511, 0.79086009, 0.26275058],
             [0.83484953, 0.6386956 , 0.53928901],
             [0.26020885, 0.58836421, 0.39308341]])
      ```
      // TODO :补充
#### NumPy支持的数据类型（ndarray对象支持的数据类型）
名称 | 描述
---|---
bool_ 	    |   布尔型数据类型（True 或者 False）
int_ 	    |   默认的整数类型（类似于 C 语言中的 long，int32 或 int64）
intc 	    |   与 C 的 int 类型一样，一般是 int32 或 int 64
intp 	    |   用于索引的整数类型（类似于 C 的 ssize_t，一般情况下仍然是 int32 或 int64）
int8 	    |   字节（-128 to 127）
int16 	    |   整数（-32768 to 32767）
int32 	    |   整数（-2147483648 to 2147483647）
int64 	    |   整数（-9223372036854775808 to 9223372036854775807）
uint8 	    |   无符号整数（0 to 255）
uint16 	    |   无符号整数（0 to 65535）
uint32 	    |   无符号整数（0 to 4294967295）
uint64 	    |   无符号整数（0 to 18446744073709551615）
float_ 	    |   float64 类型的简写
float16 	|   半精度浮点数，包括：1 个符号位，5 个指数位，10 个尾数位
float32 	|   单精度浮点数，包括：1 个符号位，8 个指数位，23 个尾数位
float64 	|   双精度浮点数，包括：1 个符号位，11 个指数位，52 个尾数位
complex_ 	|   complex128 类型的简写，即 128 位复数
complex64 	|   复数，表示双 32 位浮点数（实数部分和虚数部分）
complex128 	|   复数，表示双 64 位浮点数（实数部分和虚数部分）


#### ndarray对象的属性
属性 | 说明
---|---
ndarray.ndim 	|   数组的轴（维度）的个数。在Python世界中，维度的数量被称为rank。
ndarray.shape 	|   数组的维度。这是一个整数的元组，表示每个维度中数组的大小。对于有n行和m列的矩阵，shape将是(n,m)。因此，shape元组的长度就是rank或维度的个数 ndim。
ndarray.size 	|   数组元素的总数。这等于shape的元素的乘积。
ndarray.dtype 	|   一个描述数组中元素类型的对象。可以使用标准的Python类型创建或指定dtype。另外NumPy提供它自己的类型。例如numpy.int32、numpy.int16和numpy.float64。
ndarray.itemsize| 	数组中每个元素的字节大小。例如，元素为 float64 类型的数组的 itemsize 为8（=64/8），而 complex32 类型的数组的 itemsize 为4（=32/8）。它等于 ndarray.dtype.itemsize 。
ndarray.flags 	|   ndarray 对象的内存信息
ndarray.real 	|   ndarray元素的实部
ndarray.imag 	|   ndarray 元素的虚部
ndarray.data 	|   该缓冲区包含数组的实际元素。通常，我们不需要使用此属性，因为我们将使用索引访问数组中的元素。
demo
  ```python
  >>> a = np.full((3,3),3)
  >>> a
  array([[3, 3, 3],
         [3, 3, 3],
         [3, 3, 3]])
  >>> a.ndim
  2
  >>> a.shape
  (3, 3)
  >>> a.size
  9
  >>> a.dtype
  dtype('int32')
  >>> a.itemsize
  4
  >>> a.flags
    C_CONTIGUOUS : True
    F_CONTIGUOUS : False
    OWNDATA : True
    WRITEABLE : True
    ALIGNED : True
    WRITEBACKIFCOPY : False
    UPDATEIFCOPY : False
  >>> a.real
  array([[3, 3, 3],
         [3, 3, 3],
         [3, 3, 3]])
  >>> a.imag
  array([[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]])
  >>> a.data
  <memory at 0x0FE0E990>
  ```

#### ndarray对象的的基本操作
- 加减乘除四则运算
    ```python
    >>> a = np.full((3,3),3)
    >>> a
    array([[3, 3, 3],
           [3, 3, 3],
           [3, 3, 3]])
    >>> a+1
    array([[4, 4, 4],
           [4, 4, 4],
           [4, 4, 4]])
    >>> a-2
    array([[1, 1, 1],
           [1, 1, 1],
           [1, 1, 1]])
    >>> a*5
    array([[15, 15, 15],
           [15, 15, 15],
           [15, 15, 15]])
    >>> a/3
    array([[1., 1., 1.],
           [1., 1., 1.],
           [1., 1., 1.]])
    >>> a
    array([[3, 3, 3],
           [3, 3, 3],
           [3, 3, 3]])
    
    >>> b = np.full((3,3),3)
    >>> b
    array([[3, 3, 3],
           [3, 3, 3],
           [3, 3, 3]])
    >>> a+b
    array([[6, 6, 6],
           [6, 6, 6],
           [6, 6, 6]])
    >>> a += b
    >>> a
    array([[6, 6, 6],
           [6, 6, 6],
           [6, 6, 6]])
    
    ```
    **注意：虽然可以对两个ndarray对象进行操作，但是如果没有赋值，不会改变原来的ndarray对象**    

##### 当对两个ndarray对象数据类型精度不一样进行操作时，结果的精度为更精确的那个数据类型
```python
>>> a = np.array([[0.1,0.2,0.3],[0.3,0.2,0.1]],dtype=np.float32)
>>> a
array([[0.1, 0.2, 0.3],
       [0.3, 0.2, 0.1]], dtype=float32)
>>> b = np.array([[0.3,0.2,0.1],[0.1,0.2,0.3]],dtype=np.float64)
>>> b
array([[0.3, 0.2, 0.1],
       [0.1, 0.2, 0.3]])
>>> c = a+b
>>> c
array([[0.4       , 0.4       , 0.40000001],
       [0.40000001, 0.4       , 0.4       ]])
>>> c.dtype
dtype('float64')

```
- 常用数学函数sum、min、max等
```python
>>> a = np.arange(12).reshape(4,3) # reshape可以设置输出时的维度
>>> a
array([[ 0,  1,  2],
       [ 3,  4,  5],
       [ 6,  7,  8],
       [ 9, 10, 11]])
>>> a.sum()
66
>>> a.sum(axis=0)   # axis=0表示求列的相关操作
array([18, 22, 26]) # axis=1表示求行的相关操作
>>> a.sum(axis=1)
array([ 3, 12, 21, 30])
>>> a.min()
0
>>> a.min(axis=0)   
array([0, 1, 2])
>>> a.min(axis=1)
array([0, 3, 6, 9])
>>> a.max()
11
>>> a.max(axis=0)
array([ 9, 10, 11])
>>> a.max(axis=1)
array([ 2,  5,  8, 11])
>>> np.sin(a)
array([[ 0.        ,  0.84147098,  0.90929743],
       [ 0.14112001, -0.7568025 , -0.95892427],
       [-0.2794155 ,  0.6569866 ,  0.98935825],
       [ 0.41211849, -0.54402111, -0.99999021]])
>>> np.cos(a)
array([[ 1.        ,  0.54030231, -0.41614684],
       [-0.9899925 , -0.65364362,  0.28366219],
       [ 0.96017029,  0.75390225, -0.14550003],
       [-0.91113026, -0.83907153,  0.0044257 ]])
>>> np.tan(a)
array([[ 0.00000000e+00,  1.55740772e+00, -2.18503986e+00],
       [-1.42546543e-01,  1.15782128e+00, -3.38051501e+00],
       [-2.91006191e-01,  8.71447983e-01, -6.79971146e+00],
       [-4.52315659e-01,  6.48360827e-01, -2.25950846e+02]])
```
- 类似于python中列表的操作
    - 索引,一维数组的索引和列表一样，多维数组的索引需要根据维度索引
    ```python
    >>> a = np.arange(12)
    >>> a
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
    >>> a[0]
    0
    >>> a[11]
    11
    >>> b = np.arange(12).reshape(2,6)
    >>> b[0,0]
    0
    >>> b[5,5]
    >>> b[1,5]
    11
    ```
    - 切片，与python中的列表相似，也是左包含右不包含
    ```python
    >>> b[:,5]
    array([ 5, 11])
    >>> b[1,1:2]
    array([7])
    >>> b[1,1:5]
    array([ 7,  8,  9, 10])
    ```
    **多维数组切片时，一定要注意好维度，根据维度来切片**
    - 迭代，与python的列表相似，都可以用for in 来遍历ndarray对象，一维数组遍历和列表一样，多维数组遍历会得到次维的数组
    ```python
    >>> for i in b:
    ...     print(i)
    ...
    [0 1 2 3 4 5]
    [ 6  7  8  9 10 11]
    ```
#### 赋值、浅拷贝与深拷贝
##### 当我们操作ndarray对象时，他们的数据存在着三种常见的操作：赋值、浅拷贝与深拷贝，分清楚操作的核心才能清楚ndarray对象是否改变
- 赋值
    - 当ndarray对象被赋值操作时，跟python里的赋值操作一样，都是将新对象的指针指向赋值对象的内存，所以当我们改变被赋值对象时，赋值对象也会跟着改变
    - demo
    ```python
    >>> import numpy as np
    >>> a = np.arange(12).reshape(4,3)
    >>> a
    array([[ 0,  1,  2],
           [ 3,  4,  5],
           [ 6,  7,  8],
           [ 9, 10, 11]])
    >>> b = a
    >>> b is a
    True
    >>> b.shape = 3,4
    >>> a.shape
    (3, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])
    ```
- 浅复制or视图（在NumPy中文文档里是浅复制，实际测试中base为False但是又可以改变原ndarray，测试版本为numpy 1.16.2）
    - 在NumPy中可以使用view方法创建一个新的数组对象，它与原数组对象共享数据，具体来说，b = a[:]会创建一个新的对象 b，所以 id(b) 和id(a) 返回的结果是不一样的，但是 b 的数据完全来自于a，和 a 保持完全一致，换句话说，b的数据完全由a保管，他们两个的数据变化是一致的。切片本质上也是视图操作，所有的切片操作返回的都是视图。
    - demo
    ```python
    >>> c = a.view() # 使用view方法浅复制a
    >>> c
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]]) # 此时c的数据与a一样
    >>> c is a  
    False
    >>> c.base is a # base属性可以告诉我们是否有视图或原始数组。
    False
    >>> c.flags.owndata # ndarray.flags 有关数组内存分布的信息。
    False
    >>> c.shape = 2,6
    >>> a.shape
    (3, 4)
    >>> c[0,4]=123
    >>> a
    array([[  0,   1,   2,   3],
           [123,   5,   6,   7],
           [  8,   9,  10,  11]])
    >>> x = a[:,1:3]
    >>> x[:]
    array([[ 1,  2],
           [ 5,  6],
           [ 9, 10]])
    >>> a
    array([[  0,   1,   2,   3],
           [123,   5,   6,   7],
           [  8,   9,  10,  11]])
    >>> x[:] = 10
    >>> a
    array([[  0,  10,  10,   3],
           [123,  10,  10,   7],
           [  8,  10,  10,  11]])
    ```
- 深拷贝
    - 在numpy中可以通过copy方法生成数组以及其数据的完整拷贝，即深拷贝
    - demo
    ```python
    >>> d=a.copy()
    >>> d
    array([[   0,   10,   10,    3],
           [1234,   10,   10,    7],
           [   8,   10,   10,   11]])
    >>> d is a
    False
    >>> d.base is a
    False
    >>> d[0,0] = 999
    >>> d
    array([[ 999,   10,   10,    3],
           [1234,   10,   10,    7],
           [   8,   10,   10,   11]])
    >>> a
    array([[   0,   10,   10,    3],
           [1234,   10,   10,    7],
           [   8,   10,   10,   11]])
    ```
### NumPy常用操作

- IO操作
    - load(file[, mmap_mode, allow_pickle, …]) 从.npy，.npz或pickle文件加载数组或pickle对象。
    - save(file, arr[, allow_pickle, fix_imports]) 将数组保存为NumPy .npy格式的二进制文件。
    - savez(file, args, *kwds) 将多个数组以未压缩的.npz格式保存到单个文件中。
    - savez_compressed(file, args, *kwds) 将多个数组以压缩的.npz格式保存到单个文件中。
    - loadtxt(fname[, dtype, comments, delimiter, …]) 从文本文件加载数据。
    - savetxt(fname, X[, fmt, delimiter, newline, …]) 从文本文件加载数据。
    - genfromtxt(fname[, dtype, comments, …]) 从文本文件加载数据，并按指定处理缺失值。
    - fromregex(file, regexp, dtype[, encoding]) 使用来自文本文件构造数组
    - fromfile(file[, dtype, count, sep]) 根据文本或二进制文件中的数据构造数组。
    - ndarray.tofile(fid[, sep, format]) 将数组作为文本或二进制写入文件（默认）。
- 字符串操作
    - add(x1, x2) 返回两个str或unicode数组的逐元素字符串连接。
    - multiply(a, i) 返回(a * i)， 即字符串多个连接，逐个元素。
    - mod(a, values) 返回（a％i），即Python之前的2.6字符串格式化（插值），对于str或unicode等一对数组的元素。
    - capitalize(a) 返回a的副本，其中只有每个元素的第一个字符大写。
    - center(a, width[, fillchar]) 返回a的副本，其元素以长度为一的字符串为中心。
    - decode(a[, encoding, errors]) 逐元素方式调用str.decode。
    - encode(a[, encoding, errors]) 逐元素方式调用str.encode。
    - join(sep, seq) 返回一个字符串，它是序列seq中字符串的串联。
    - ljust(a, width[, fillchar]) 返回一个数组，其中包含左对齐的元素，长度为宽度的字符串。
    - lower(a) 返回一个数组，其元素转换为小写。
    - lstrip(a[, chars]) 对于a中的每个元素，返回删除了前导字符的副本。
    - partition(a, sep) 将每个元素分成一个周围的sep。
    - replace(a, old, new[, count]) 对于a中的每个元素，返回一个字符串的副本，其中所有出现的substring old都替换为new。
    - rjust(a, width[, fillchar]) 返回一个数组，其中右对齐元素的长度为宽度。
    - rpartition(a, sep) 对最右边的分隔符周围的每个元素进行分区（拆分）。
    - rsplit(a[, sep, maxsplit]) 对于a中的每个元素，使用sep作为分隔符字符串，返回字符串中单词的列表。
    - rstrip(a[, chars]) 对于a中的每个元素，返回一个删除了尾随字符的副本。
    - split(a[, sep, maxsplit]) 对于a中的每个元素，使用sep作为分隔符字符串，返回字符串中单词的列表。
    - splitlines(a[, keepends]) 对于a中的每个元素，返回元素中的行列表，在行边界处断开。
    - strip(a[, chars]) 对于a中的每个元素，返回一个删除了前导和尾随字符的副本。
    - swapcase(a) 返回元素的字符串副本，大写字符转换为小写，反之亦然。
    - title(a) 返回元素字符串的字符串或unicode的版本。
    - translate(a, table[, deletechars]) 对于a中的每个元素，返回字符串的副本，其中删除可选参数deletechars中出现的所有字符，并通过给定的转换表映射其余字符。
    - upper(a) 返回一个数组，其元素转换为大写。
    - zfill(a, width) 返回左边用零填充的数字字符串
    - equal(x1, x2) 返回 (x1 == x2) 逐元素。
    - not_equal(x1, x2) 返回 (x1 != x2) 逐元素。
    - greater_equal(x1, x2) 返回 (x1 >= x2) 逐元素。
    - less_equal(x1, x2) 返回 (x1 <= x2) 逐元素。
    - greater(x1, x2) 返回 (x1 > x2) 逐元素。
    - less(x1, x2) 返回 (x1 < x2) 逐元素。
    - count(a, sub[, start, end]) 返回一个数组，其中包含[start, end]范围内substring sub的非重叠出现次数。
    - find(a, sub[, start, end]) 对于每个元素，返回找到substring sub的字符串中的最低索引。
    - index(a, sub[, start, end]) 与find一样，但在找不到子字符串时会引发ValueError。
    - isalpha(a) 如果字符串中的所有字符都是字母并且至少有一个字符，则返回每个元素的true，否则返回false。
    - isdecimal(a) 对于每个元素，如果元素中只有十进制字符，则返回True。
    - isdigit(a) 如果字符串中的所有字符都是数字并且至少有一个字符，则返回每个元素的true，否则返回false。
    - islower(a) 如果字符串中的所有外壳字符都是小写且至少有一个外壳字符，则为每个元素返回true，否则返回false。
    - isnumeric(a) 对于每个元素，如果元素中只有数字字符，则返回True。
    - isspace(a) 如果字符串中只有空格字符并且至少有一个字符，则为每个元素返回true，否则返回false。
    - istitle(a) 如果元素是一个带有标题的字符串并且至少有一个字符，则为每个元素返回true，否则返回false。
    - isupper(a) 如果字符串中的所有外壳字符都是大写且至少有一个字符，则为每个元素返回true，否则返回false。
    - rfind(a, sub[, start, end]) 对于a中的每个元素，返回找到substring sub的字符串中的最高索引，使得sub包含在[start, end]中。
    - rindex(a, sub[, start, end]) 和rfind一样，但是当找不到substring sub时会引发ValueError。
    - startswith(a, prefix[, start, end]) 返回一个布尔数组，该数组为True，其中a中的字符串元素以prefix开头，否则为False。
