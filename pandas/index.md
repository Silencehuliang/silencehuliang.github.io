# Pandas

## Pandas
### 参考资料

**https://www.jianshu.com/p/a77b0bc736f2;  
http://pandas.pydata.org/pandas-docs/stable/reference/index.html；  
https://www.jianshu.com/p/161364dd0acf**  

**注意：以下所有代码在没有创建新的Series或DataFrame的情况下都沿用之前那个**

### 安装

- 通过安装Anaconda安装Pandas,一般情况下，安装Anaconda是自带Pandas的，有的人会选择安装精简版的Anaconda，可能会没有Pandas，可以在命令行输入conda install pands
- 通过pip安装Anaconda，在命令行输入pip install pandas,在安装Pandas时，会帮你安装时NumPy等一些其他的包
### 数据结构

#### Series

##### 简介

可以理解为是建立在Numpy中array的基础上增加索引的一维数组。

##### 使用

- 创建Series，创建Series时可以传入两个参数data和index，和NumPy一样data可以传列表、元祖，index也是如此，当传入字典的时候，它的键会作为index，值作为data,还可以传array
    ```python
    >>> import pandas as pd
    >>> import numpy as np
    >>> pd.Series([1,2,3,4],["a","b","c","d"])
    a    1
    b    2
    c    3
    d    4
    >>> pd.Series((1,2,3,4),("a","b","c","d"))
    a    1
    b    2
    c    3
    d    4
    dtype: int64
    >>> pd.Series({"a":1,"b":2,"c":3,"d":4})
    a    1
    b    2
    c    3
    d    4
    dtype: int64
    >>> pd.Series(np.arange(4))
    0    0
    1    1
    2    2
    3    3
    dtype: int32
    ```
- 选择数据，在选择数据的时候，Series可以直接根据索引来选择，他也可以进行切片和遍历的操作
    ```python
    >>> s1[0]
    0
    >>> for i in s1:
    ...     print(i)
    ...
    0
    1
    2
    3
    >>> s1[1:3]
    1    1
    2    2
    dtype: int32
    ```
    - Series还可以根据条件选择数据
      ```python
      >>> s1[s1>0]
      1    1
      2    2
      3    3
      dtype: int32
      ```
- Series简单的数学运算，Series跟NumPy里的array一样，也可以进行四则运算，不仅可以和数，也可以和Series对象进行，在和Series对象进行运算的时候，根据索引来操作，假如有存在空的时候会出现NaN
    ```python
    >>> s1 = pd.Series(np.arange(4))
    >>> s1+5
    0    5
    1    6
    2    7
    3    8
    dtype: int32
    >>> s1-3
    0   -3
    1   -2
    2   -1
    3    0
    dtype: int32
    >>> s1*2
    0    0
    1    2
    2    4
    3    6
    dtype: int32
    >>> s1/6
    0    0.000000
    1    0.166667
    2    0.333333
    3    0.500000
    dtype: float64
    >>> s2 = pd.Series(np.random.random(3))
    >>> s2
    0    0.038811
    1    0.860956
    2    0.751210
    dtype: float64
    >>> s1+s2
    0    0.038811
    1    1.860956
    2    2.751210
    3         NaN
    dtype: float64
    >>> s1-s2
    0   -0.038811
    1    0.139044
    2    1.248790
    3         NaN
    dtype: float64
    >>> s1*s2
    0    0.000000
    1    0.860956
    2    1.502420
    3         NaN
    dtype: float64
    >>> s1/s2
    0    0.000000
    1    1.161500
    2    2.662372
    3         NaN
    dtype: float64
    ```
    **在进行不同精度的四则运算时，Pandas会让结果的精度和两个Series中精度更精确的那个一样**
    - 同样也可以使用add/sub等这样的方法进行操作
      ```python
      >>> s1.add(s2)
      0    0.038811
      1    1.860956
      2    2.751210
      3         NaN
      dtype: float64
      >>> s1.sub(s2)
      0   -0.038811
      1    0.139044
      2    1.248790
      3         NaN
      dtype: float64
      ```
#### DataFrames

##### 简介

他是一种类似于NumPy中的二维数组，是一种表结构的数据。跟NumPy中的array不同的是DataFrames里的每一列每一行的数据都可以是任意数据类型。

##### 使用

- 创建DataFrame，创建DataFrame时必须要传入一个数据data，和NumPy一样data可以传列表、元祖，当传嵌套字典时，pandas就会把外层字典的键作为列，内层键则作为行索引；在Dataframe中index成为单独的一列，即索引列，同样也可以传入列表和元祖；创建DataFrame时还可以设置columns,他必须传列表
    ```python
    >>> pd.DataFrame((1,2,3,4),index=(1,2,3,4),columns=['a'])
       a
    1  1
    2  2
    3  3
    4  4
    >>> a = {'a':{1:1},'b':{2:2}}
    >>> pd.DataFrame(a)
         a    b
    1  1.0  NaN
    2  NaN  2.0
    
    ```
    在创建DataFrame时，如果传入数据的数据量不匹配，在结果中会产生缺失值，如果传入了columns，结果会按columns传入的顺序显示
- 一些常见的方法
    - head,默认获取前五行数据，可以传入想获取的行数
      ```python
      >>> df = pd.DataFrame({'animal':['alligator', 'bee', 'falcon', 'lion',
      ...                    'monkey', 'parrot', 'shark', 'whale', 'zebra']})
      >>> df
            animal
      0  alligator
      1        bee
      2     falcon
      3       lion
      4     monkey
      5     parrot
      6      shark
      7      whale
      8      zebra
      >>> df.head()
            animal
      0  alligator
      1        bee
      2     falcon
      3       lion
      4     monkey
      >>> df.head()
            animal
      0  alligator
      1        bee
      2     falcon
      3       lion
      4     monkey
      ```
    - tail,默认获取后五行数据，可以传入想获取的行数
      ```python
      >>> df.tail()
         animal
      4  monkey
      5  parrot
      6   shark
      7   whale
      8   zebra
      >>> df.tail(3)
        animal
      6  shark
      7  whale
      8  zebra
      ```
    - shape,查看DataFrame的行列个数
      ```python
      >>> df.shape
      (9, 1)
      ```
    - info,查看索引、数据类型和内存信息
      ```python
      >>> df.info()
      <class 'pandas.core.frame.DataFrame'>
      RangeIndex: 9 entries, 0 to 8
      Data columns (total 1 columns):
      animal    9 non-null object
      dtypes: object(1)
      memory usage: 152.0+ bytes
      ```
    - mean,所有列的平均数
      ```python
      >>> df = pd.DataFrame(np.random.rand(5,5))
      >>> df
                0         1         2         3         4
      0  0.987926  0.556055  0.774863  0.926501  0.029973
      1  0.635812  0.698311  0.402425  0.727675  0.048129
      2  0.001094  0.329329  0.364231  0.754038  0.405464
      3  0.975270  0.388988  0.598047  0.355597  0.189753
      4  0.171976  0.334893  0.931219  0.967504  0.323952
      >>> df.mean()
      0    0.554416
      1    0.461516
      2    0.614157
      3    0.746263
      4    0.199454
      dtype: float64
      ```
    - count,每一列中非空值的个数
      ```python
      >>> df.count()
      0    5
      1    5
      2    5
      3    5
      4    5
      dtype: int64
      ```
    - max,每一列的最大值
      ```python
      >>> df.max()
      0    0.987926
      1    0.698311
      2    0.931219
      3    0.967504
      4    0.405464
      dtype: float64
      ```
    - min,每一列的最小值
      ```python
      >>> df.min()
      0    0.001094
      1    0.329329
      2    0.364231
      3    0.355597
      4    0.029973
      dtype: float64
      ```
    - median,每一列的中位数
      ```python
      >>> df.median()
      0    0.635812
      1    0.388988
      2    0.598047
      3    0.754038
      4    0.189753
      dtype: float64
      ```
    - std,每一列的标准差
      ```python
      >>> df.std()
      0    0.453900
      1    0.161072
      2    0.241820
      3    0.242105
      4    0.165573
      dtype: float64
      ```
    - corr,列与列之间的相关系数
      ```python
      >>> df.corr()
                0         1         2         3         4
      0  1.000000  0.517374  0.142778 -0.401999 -0.836540
      1  0.517374  1.000000 -0.262423  0.076483 -0.882558
      2  0.142778 -0.262423  1.000000  0.458608 -0.044045
      3 -0.401999  0.076483  0.458608  1.000000  0.032442
      4 -0.836540 -0.882558 -0.044045  0.032442  1.000000
      ```
- 获取数据
    - 切片操作可以运用在一下所有的方法里
    - df[columns],获取列，返回列，数据类型为Series
      ```python
      >>> df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],index=['cobra', 'viper', 'sidewinder'],columns=['max_speed', 'shield'])
      >>> df
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      >>> df['max_speed']
      cobra         1
      viper         4
      sidewinder    7
      Name: max_speed, dtype: int64
      ```
    - df[columns1,columns2],返回多列，数据类型为DataFrame
      ```python
      >>> df[['max_speed','shield']]
          max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      ```
    - df.loc[0,0]，通过对应行列的索引名称来获取,当填入行列时返回单个元素，当只填行或者列的时候返回一个行或者列的Series
      ```python 
      >>> df.loc["cobra","max_speed"]
      1
      >>> df.loc["cobra":,"max_speed":]
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      >>> df.loc["cobra":,]
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      
      ```
    - df.iloc[0,0]，通过位置来获取,当填入行列时返回单个元素，当只填行或者列的时候返回一个行或者列的Series
      ```python
      >>> df.iloc[0,0]
      1
      >>> df.iloc[0:,0:]
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      >>> df.iloc[0:,]
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      >>> df.loc["cobra":,]
      ```
    - df.ix[0,0]，结合了loc与iloc，既可以通过位置，又可以通过索引名。当只填行或者列的时候返回一个行或者列的Series
      ```python
              >>> df.ix['viper',1:2]
      shield    5
      Name: viper, dtype: int64
      >>> df.ix['viper',0:1]
      max_speed    4
      Name: viper, dtype: int64
      ```
    - df.values[:,:],通过位置返回所有的数据，当只填行或者列的时候返回一个行或者列的array
      ```python
      >>> df.values[0:,:]
      array([[1, 2],
             [4, 5],
             [7, 8]], dtype=int64)
      >>> df.values[:1,:]
      array([[1, 2]], dtype=int64)
      >>>
      ```
    - df[df[columns]>10],根据条件选出符合条件的列
      ```python
      >>> df[df['max_speed']>0]
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      ```
    - df.sort_values([columns1,columns2],ascending=[False,True]),按照某列的升降序排列，当填入两个以上的列时，按照先后顺序升降序排列
      ```python
      >>> df.sort_values('max_speed')
                  max_speed  shield
      cobra               1       2
      viper               4       5
      sidewinder          7       8
      >>> df.sort_values('max_speed',ascending=False)
                  max_speed  shield
      sidewinder          7       8
      viper               4       5
      cobra               1       2
      >>> df.sort_values(['max_speed','shield'],ascending=False)
                  max_speed  shield
      sidewinder          7       8
      viper               4       5
      cobra               1       2
      ```
    - df.groupby([columns1,columns2]),按一列或者多列进行分组，返回分组对象
      ```python
      >>> df.groupby('max_speed')
      <pandas.core.groupby.generic.DataFrameGroupBy object at 0x000001DF64584588>
      >>> df.groupby('max_speed').mean()
                 shield
      max_speed
      1               2
      4               5
      7               8
      ```
    
- 数据清洗
    - df.columns = ['a','b','c','d'],重新给列命名
      ```python
      >>> df.columns=['a','b']
      >>> df
                  a  b
      cobra       1  2
      viper       4  5
      sidewinder  7  8
      ```
    - df.rename(data,axis),改变行索引或者列索引，axis里选择行列
      ```python
      >>> df.rename(index=str,columns={'a':'A','b':'B'})
                  A  B
      cobra       1  2
      viper       4  5
      sidewinder  7  8
      >>> df.rename(str.lower,axis='columns')
                  a  b
      cobra       1  2
      viper       4  5
      sidewinder  7  8
      >>> df.rename({'cobra':'A','viper':'B','sidewinder':'C'},axis='index')
         a  b
      A  1  2
      B  4  5
      C  7  8
      ```
    - df.set_index('column_one')：设置索引列
      ```python
      >>> df = pd.DataFrame({'month': [1, 4, 7, 10],
      ...                    'year': [2012, 2014, 2013, 2014],
      ...                    'sale': [55, 40, 84, 31]})
      >>> df
         month  year  sale
      0      1  2012    55
      1      4  2014    40
      2      7  2013    84
      3     10  2014    31
      >>> df.set_index('month')
             year  sale
      month
      1      2012    55
      4      2014    40
      7      2013    84
      10     2014    31
      ```
    - df.reset_index,重新设置行索引
      ```python
      >>> df = pd.DataFrame([('bird', 389.0),
      ...                    ('bird', 24.0),
      ...                    ('mammal', 80.5),
      ...                    ('mammal', np.nan)],
      ...                   index=['falcon', 'parrot', 'lion', 'monkey'],
      ...                   columns=('class', 'max_speed'))
      >>> df
               class  max_speed
      falcon    bird      389.0
      parrot    bird       24.0
      lion    mammal       80.5
      monkey  mammal        NaN
      >>> df.reset_index()
          index   class  max_speed
      0  falcon    bird      389.0
      1  parrot    bird       24.0
      2    lion  mammal       80.5
      3  monkey  mammal        NaN
      ```
    - df.isnull,判断DataFrame中有没有空值，有空值返回True，没有返回False
      ```python
      >>> df = pd.DataFrame({'age': [5, 6, np.NaN],
      ...                    'born': [pd.NaT, pd.Timestamp('1939-05-27'),
      ...                             pd.Timestamp('1940-04-25')],
      ...                    'name': ['Alfred', 'Batman', ''],
      ...                    'toy': [None, 'Batmobile', 'Joker']})
      >>> df
         age       born    name        toy
      0  5.0        NaT  Alfred       None
      1  6.0 1939-05-27  Batman  Batmobile
      2  NaN 1940-04-25              Joker
      >>> df.isnull()
           age   born   name    toy
      0  False   True  False   True
      1  False  False  False  False
      2   True  False  False  False
      >>> df.isna()
           age   born   name    toy
      0  False   True  False   True
      1  False  False  False  False
      2   True  False  False  False
      ```
    - df.notnull,判断DataFrame中有没有非空值，有非空值返回True，没有返回False
      ```python
      >>> df.notna()
           age   born  name    toy
      0   True  False  True  False
      1   True   True  True   True
      2  False   True  True   True
      ```
    - df.dropna(axis),删除所有包含空值的行或者列，axis=0为行，axis=1为列
      ```python
      >>> df.dropna() 
         age       born    name        toy
      1  6.0 1939-05-27  Batman  Batmobile
      >>> df 
         age       born    name        toy
      0  5.0        NaT  Alfred       None
      1  6.0 1939-05-27  Batman  Batmobile
      2  NaN 1940-04-25              Joker
      ```
    - df.fillna(n),用n来替换DataFrame中的所有空值
      ```python
      >>> df.fillna('hahaha')
            age                 born    name        toy
      0       5               hahaha  Alfred     hahaha
      1       6  1939-05-27 00:00:00  Batman  Batmobile
      2  hahaha  1940-04-25 00:00:00              Joker
      ```
    - df.replace('a','b'),用'b'来替换DataFrme中所有的'a'
      ```python
      >>> df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
      ...                    'B': [5, 6, 7, 8, 9],
      ...                    'C': ['a', 'b', 'c', 'd', 'e']})
      >>> df.replace(0, 5)
         A  B  C
      0  5  5  a
      1  1  6  b
      2  2  7  c
      3  3  8  d
      4  4  9  e
      >>> df.replace(0,5)
         A  B  C
      0  5  5  a
      1  1  6  b
      2  2  7  c
      3  3  8  d
      4  4  9  e
      ```
    - df[['a','b']].astype(type),改变DataFrme中某几列的数据类型，即改变Series的数据类型
      ```python
      >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
      >>> df.rename(index=str, columns={"A": "a", "B": "c"})
         a  c
      0  1  4
      1  2  5
      2  3  6
      df = pd.DataFrame([('bird', 389.0),('bird', 24.0),('mammal', 80.5),('mammal', np.nan)],index=['falcon', 'parrot', 'lion', 'monkey'],columns=('class', 'max_speed'))
      ```
- 数据合并
    - df.append(df2),将df2中的数据根据列追加到df中的末尾,注意如果两个df的列名不相同，会显示所有列，在没有的列添加NaN
      ```python
      >>> df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
      >>> df
         A  B
      0  1  2
      1  3  4
      >>> df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
      >>> df2
         A  B
      0  5  6
      1  7  8
      >>> df.append(df2)
         A  B
      0  1  2
      1  3  4
      0  5  6
      1  7  8
      >>> df3 = pd.DataFrame([[5, 6], [7, 8]], columns=list('BC'))
      >>> df3
         B  C
      0  5  6
      1  7  8
      >>> df.append(df3,sort=True) # sort设置排序规则
           A  B    C
      0  1.0  2  NaN
      1  3.0  4  NaN
      0  NaN  5  6.0
      1  NaN  7  8.0
      >>> df.append(df3,sort=True,ignore_index=True) # ignore_index重新设置索引
           A  B    C
      0  1.0  2  NaN
      1  3.0  4  NaN
      2  NaN  5  6.0
      3  NaN  7  8.0
      ```
    - pd.concat([df1,df2],axis=1)，将df2中的数据根据axis选择行列追加到df1的尾部
      ```python
      >>> df1 = pd.DataFrame([['a', 1], ['b', 2]],columns=['letter', 'number'])
      >>> df1
        letter  number
      0      a       1
      1      b       2
      >>> df2 = pd.DataFrame([['c', 3], ['d', 4]],columns=['letter', 'number'])
      >>> df2
        letter  number
      0      c       3
      1      d       4
      >>> pd.concat([df1,df2])
        letter  number
      0      a       1
      1      b       2
      0      c       3
      1      d       4
      >>> pd.concat([df1,df2],axis=1)
        letter  number letter  number
      0      a       1      c       3
      1      b       2      d       4
      ```
    - df1.join(df2,on=columns,how='out')
      ```python
      >>> df = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3', 'K4', 'K5'],'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})
      >>> df
        key   A
      0  K0  A0
      1  K1  A1
      2  K2  A2
      3  K3  A3
      4  K4  A4
      5  K5  A5
      >>> df2 = pd.DataFrame({'key': ['K0', 'K1', 'K2'],'B': ['B0', 'B1', 'B2']})
      >>> df2
        key   B
      0  K0  B0
      1  K1  B1
      2  K2  B2
      >>> df.join(df2,lsuffix='_caller',rsuffix='_other') # lsuffix设置df左侧的重叠列中使用的列名，同理rsuffix为右侧
        key_caller   A key_other    B
      0         K0  A0        K0   B0
      1         K1  A1        K1   B1
      2         K2  A2        K2   B2
      3         K3  A3       NaN  NaN
      4         K4  A4       NaN  NaN
      5         K5  A5       NaN  NaN
      ```
    - df1.merge(df2,left_on='column1',right_on='column2')
      ```python
      >>> df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'], 'value': [1, 2, 3, 5]})
      >>> df1
        lkey  value
      0  foo      1
      1  bar      2
      2  baz      3
      3  foo      5
      >>> df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'], 'value': [5, 6, 7, 8]})
      >>> df2
        rkey  value
      0  foo      5
      1  bar      6
      2  baz      7
      3  foo      8
      >>> df1.merge(df2,left_on='lkey',right_on='rkey')
        lkey  value_x rkey  value_y
      0  foo        1  foo        5
      1  foo        1  foo        8
      2  foo        5  foo        5
      3  foo        5  foo        8
      4  bar        2  bar        6
      5  baz        3  baz        7
      ```
- IO操作
    - 导入：
        - pd.read_csv,读取csv格式文件
            - 参数解读
                - filepath_or_buffer 可以传入文件路径、URL和文件对象
                  ```python
                  >>> import pandas as pd
                  >>> pd.read_csv('test.csv') # 直接传入文件路径
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> with open('test.csv', encoding='utf-8') as f: # 通过with open 生成文件对象读取
                  ...     df = pd.read_csv(f)
                  ...     print(df)
                  ...
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - sep 分隔符，默认为‘，’,可以传入正则表达式
                  ```python
                  >>> pd.read_csv('test.csv',sep=',') # 默认情况下为，
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',sep=' ') # 将分隔符改为空格后读出变为一行
                                   a,b,c,d,e
                  0  0,a,2019/03/27,09:30,请问
                  1   1,b,2019/03/26,10:00,二
                  2  2,c,2019/03/25,10:30,同意
                  3  3,d,2019/03/24,11:00,UI
                  4  4,e,2019/03/23,11:30,欧赔
                  5    5,f,2019/03/22,13:00,
                  6  6,g,2019/03/21,13:30,东方
                  7  7,h,2019/03/20,14:00,更换
                  8   8,,2019/03/19,14:30,接口
                  9  9,j,2019/03/18,15:00,执行
                  >>> df['a,b,c,d,e']
                  0    0,a,2019/03/27,09:30,请问
                  1     1,b,2019/03/26,10:00,二
                  2    2,c,2019/03/25,10:30,同意
                  3    3,d,2019/03/24,11:00,UI
                  4    4,e,2019/03/23,11:30,欧赔
                  5      5,f,2019/03/22,13:00,
                  6    6,g,2019/03/21,13:30,东方
                  7    7,h,2019/03/20,14:00,更换
                  8     8,,2019/03/19,14:30,接口
                  9    9,j,2019/03/18,15:00,执行
                  Name: a,b,c,d,e, dtype: object
                  ```
                - header 选择开始读取位置，默认为infer，即从第一行开始读取，则第一行为列索引。可以穿int和int列表，当传入int列表的时表头会显示传入的行，第一个标记的行为列索引，其他行在下面显示，当和skip_blank_lines=True一起使用的时候可以跳过注释和空行
                  ```python
                  >>> pd.read_csv('test.csv',header='infer')
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test.csv',header=1)
                     0    a  2019/03/27  09:30   请问
                  0  1    b  2019/03/26  10:00    二
                  1  2    c  2019/03/25  10:30   同意
                  2  3    d  2019/03/24  11:00   UI
                  3  4    e  2019/03/23  11:30   欧赔
                  4  5    f  2019/03/22  13:00  NaN
                  5  6    g  2019/03/21  13:30   东方
                  6  7    h  2019/03/20  14:00   更换
                  7  8  NaN  2019/03/19  14:30   接口
                  8  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',header=[5,3])
                  >>> df
                     4    e  2019/03/23  11:30   欧赔
                     2    c  2019/03/25  10:30   同意
                  0  3    d  2019/03/24  11:00   UI
                  1  4    e  2019/03/23  11:30   欧赔
                  2  5    f  2019/03/22  13:00  NaN
                  3  6    g  2019/03/21  13:30   东方
                  4  7    h  2019/03/20  14:00   更换
                  5  8  NaN  2019/03/19  14:30   接口
                  6  9    j  2019/03/18  15:00   执行
                  >>> df['e']
                       c
                  0    d
                  1    e
                  2    f
                  3    g
                  4    h
                  5  NaN
                  6    j
                  ```
                - skip_blank_lines  表示是否跳过注释和空行，传入bool类型即可，默认为True
                  ```python
                  >>> pd.read_csv('test.csv',skip_blank_lines=True)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - name 生成新的列索引，传入列表，传入后原来的列索引会被覆盖，如果文件不包含标题行,则应显式传递header=None。此列表中的重复将导致发出用户警告。可以传入类数组
                  ```python
                  >>> pd.read_csv('test.csv')['a'] # a这一列原本是int64类型
                  0    0
                  1    1
                  2    2
                  3    3
                  4    4
                  5    5
                  6    6
                  7    7
                  8    8
                  9    9
                  Name: a, dtype: int64
                  >>> df = pd.read_csv('test.csv',names=['Java','Python','C++','JavaScript']) # 在我们重新设置列索引这一行后由于数量没对上，a这一列变成了行索引，数据类型变成了字符串
                  >>> df
                    Java      Python    C++ JavaScript
                  a    b           c      d          e
                  0    a  2019/03/27  09:30         请问
                  1    b  2019/03/26  10:00          二
                  2    c  2019/03/25  10:30         同意
                  3    d  2019/03/24  11:00         UI
                  4    e  2019/03/23  11:30         欧赔
                  5    f  2019/03/22  13:00        NaN
                  6    g  2019/03/21  13:30         东方
                  7    h  2019/03/20  14:00         更换
                  8  NaN  2019/03/19  14:30         接口
                  9    j  2019/03/18  15:00         执行
                  >>> df['Java']
                  a      b
                  0      a
                  1      b
                  2      c
                  3      d
                  4      e
                  5      f
                  6      g
                  7      h
                  8    NaN
                  9      j
                  Name: Java, dtype: object
                  >>> df.loc['9','Python'] # 这里通过位置可以把某一个元素取出来
                  '2019/03/18'
                  # 因为a这一列与原先索引重复，可能没有说服力，我将文件中a这一列删除再次重新设置索引
                  >>> pd.read_csv('test.csv')
                       b           c      d    e
                  0    a  2019/03/27  09:30   请问
                  1    b  2019/03/26  10:00    二
                  2    c  2019/03/25  10:30   同意
                  3    d  2019/03/24  11:00   UI
                  4    e  2019/03/23  11:30   欧赔
                  5    f  2019/03/22  13:00  NaN
                  6    g  2019/03/21  13:30   东方
                  7    h  2019/03/20  14:00   更换
                  8  NaN  2019/03/19  14:30   接口
                  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',names=['Java','Python','C++'])
                  >>> df
                             Java Python  C++
                  b             c      d    e
                  a    2019/03/27  09:30   请问
                  b    2019/03/26  10:00    二
                  c    2019/03/25  10:30   同意
                  d    2019/03/24  11:00   UI
                  e    2019/03/23  11:30   欧赔
                  f    2019/03/22  13:00  NaN
                  g    2019/03/21  13:30   东方
                  h    2019/03/20  14:00   更换
                  NaN  2019/03/19  14:30   接口
                  j    2019/03/18  15:00   执行
                  >>> df.loc['a','Java']
                  '2019/03/27' # 从这里我们可以看出，在DataFrame中，第一列应该一直是行索引
                  >>> df = pd.read_csv('test.csv',names=['Java','Python','C++','JavaScript','Php','Sql']) # 当给的列索引比原来的列多时，会新生产一个全为空值得列，这里显示为NaN
                     Java Python         C++ JavaScript  Php  Sql
                  0     a      b           c          d    e  NaN
                  1     0      a  2019/03/27      09:30   请问  NaN
                  2     1      b  2019/03/26      10:00    二  NaN
                  3     2      c  2019/03/25      10:30   同意  NaN
                  4     3      d  2019/03/24      11:00   UI  NaN
                  5     4      e  2019/03/23      11:30   欧赔  NaN
                  6     5      f  2019/03/22      13:00  NaN  NaN
                  7     6      g  2019/03/21      13:30   东方  NaN
                  8     7      h  2019/03/20      14:00   更换  NaN
                  9     8    NaN  2019/03/19      14:30   接口  NaN
                  10    9      j  2019/03/18      15:00   执行  NaN
                  >>> df = pd.read_csv('test.csv',names=['Java','Python','C++','JavaScript','Python']) # 当出现重复的时候会出现警告，并将名字改为x:x.1 
                  x:xxx: UserWarning: Duplicate names specified. This will raise an error
                  in the future.
                    return _read(filepath_or_buffer, kwds)
                  >>> df
                     Java Python         C++ JavaScript Python.1
                  0     a      b           c          d        e
                  1     0      a  2019/03/27      09:30       请问
                  2     1      b  2019/03/26      10:00        二
                  3     2      c  2019/03/25      10:30       同意
                  4     3      d  2019/03/24      11:00       UI
                  5     4      e  2019/03/23      11:30       欧赔
                  6     5      f  2019/03/22      13:00      NaN
                  7     6      g  2019/03/21      13:30       东方
                  8     7      h  2019/03/20      14:00       更换
                  9     8    NaN  2019/03/19      14:30       接口
                  10    9      j  2019/03/18      15:00       执行
                  ```
                - index_col  将某一列或者多列变成行索引列，可传入int，对应位置的列作为索引列,在传入多个的时候,第一列为索引列，在获取元素的时候会出现警告
                  ```python
                  >>> df = pd.read_csv('test.csv',index_col=1)
                  >>> df
                       a           c      d    e
                  b
                  a    0  2019/03/27  09:30   请问
                  b    1  2019/03/26  10:00    二
                  c    2  2019/03/25  10:30   同意
                  d    3  2019/03/24  11:00   UI
                  e    4  2019/03/23  11:30   欧赔
                  f    5  2019/03/22  13:00  NaN
                  g    6  2019/03/21  13:30   东方
                  h    7  2019/03/20  14:00   更换
                  NaN  8  2019/03/19  14:30   接口
                  j    9  2019/03/18  15:00   执行
                  >>> df.loc['a','a']
                  0
                  >>> df = pd.read_csv('test.csv',index_col=[1,3,4])
                  >>> df
                                 a           c
                  b   d     e
                  a   09:30 请问   0  2019/03/27
                  b   10:00 二    1  2019/03/26
                  c   10:30 同意   2  2019/03/25
                  d   11:00 UI   3  2019/03/24
                  e   11:30 欧赔   4  2019/03/23
                  f   13:00 NaN  5  2019/03/22
                  g   13:30 东方   6  2019/03/21
                  h   14:00 更换   7  2019/03/20
                  NaN 14:30 接口   8  2019/03/19
                  j   15:00 执行   9  2019/03/18
                  >>> df.loc['a','a'] 
                  __main__:1: PerformanceWarning: indexing past lexsort depth may impact performance.
                  d      e
                  09:30  请问    0
                  Name: a, dtype: int64
                  >>> df.loc['09:30','a']
                  ```
                - usecols 选择读取的列，可传入数字列表或者列名列表，不能混合传。读取结果为传入列表中的列
                  ```python
                  >>> pd.read_csv('test.csv',usecols=[1,3])
                       b      d
                  0    a  09:30
                  1    b  10:00
                  2    c  10:30
                  3    d  11:00
                  4    e  11:30
                  5    f  13:00
                  6    g  13:30
                  7    h  14:00
                  8  NaN  14:30
                  9    j  15:00
                  >>> pd.read_csv('test.csv',usecols=['a','c'])
                     a           c
                  0  0  2019/03/27
                  1  1  2019/03/26
                  2  2  2019/03/25
                  3  3  2019/03/24
                  4  4  2019/03/23
                  5  5  2019/03/22
                  6  6  2019/03/21
                  7  7  2019/03/20
                  8  8  2019/03/19
                  9  9  2019/03/18
                  ```
                - squeeze 当获取数据只有一列时将它转换为Series,默认为Fales
                  ```python
                  >>> df = pd.read_csv('test.csv',usecols=['a'])
                  >>> df
                     a
                  0  0
                  1  1
                  2  2
                  3  3
                  4  4
                  5  5
                  6  6
                  7  7
                  8  8
                  9  9
                  >>> type(df)
                  <class 'pandas.core.frame.DataFrame'>
                  >>> df = pd.read_csv('test.csv',usecols=['a'],squeeze=True)
                  >>> df
                  0    0
                  1    1
                  2    2
                  3    3
                  4    4
                  5    5
                  6    6
                  7    7
                  8    8
                  9    9
                  Name: a, dtype: int64
                  >>> type(df)
                  <class 'pandas.core.series.Series'>
                  ```
                - prefix 当读取的csv文件没有列索引行时,可以为其添加列名
                  ```python 
                  >>> df = pd.read_csv('test.csv',prefix='g',header=None)
                  >>> df
                     g0   g1          g2     g3   g4
                  0   a    b           c      d    e
                  1   0    a  2019/03/27  09:30   请问
                  2   1    b  2019/03/26  10:00    二
                  3   2    c  2019/03/25  10:30   同意
                  4   3    d  2019/03/24  11:00   UI
                  5   4    e  2019/03/23  11:30   欧赔
                  6   5    f  2019/03/22  13:00  NaN
                  7   6    g  2019/03/21  13:30   东方
                  8   7    h  2019/03/20  14:00   更换
                  9   8  NaN  2019/03/19  14:30   接口
                  10  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',prefix=['a','b','c','d','g'],header=None) # 这是个待优化的地方，不能传多个值，他会将多个值变成一个值
                  >>> df
                     ['a', 'b', 'c', 'd', 'g']0 ['a', 'b', 'c', 'd', 'g']1 ['a', 'b', 'c', 'd', 'g']2 ['a', 'b', 'c', 'd', 'g']3 ['a', 'b', 'c', 'd', 'g']4
                  0                           a                          b                          c                          d                          e
                  1                           0                          a                 2019/03/27                      09:30                         请问
                  2                           1                          b                 2019/03/26                      10:00                          二
                  3                           2                          c                 2019/03/25                      10:30                         同意
                  4                           3                          d                 2019/03/24                      11:00                         UI
                  5                           4                          e                 2019/03/23                      11:30                         欧赔
                  6                           5                          f                 2019/03/22                      13:00                        NaN
                  7                           6                          g                 2019/03/21                      13:30                         东方
                  8                           7                          h                 2019/03/20                      14:00                         更换
                  9                           8                        NaN                 2019/03/19                      14:30                         接口
                  10                          9                          j                 2019/03/18                      15:00                         执行
                  ```
                - mangle_dupe_cols 将重复列重命名，demo：'x' ,'x.1',默认为True
                  ```python
                  >>> df = pd.read_csv('test.csv',mangle_dupe_cols=False)
                  ValueError: Setting mangle_dupe_cols=False is not supported yet # 还不支持将它设置为False = =这个目前可以忽略了，考虑到索引重名会影响选择数据等问题，我觉得目前不支持也很正常
                  ```
                - dtype 设置列的数据类型，传入字典，键为列名，值为列的类型
                  ```python
                  >>> import numpy as np
                  >>> pd.read_csv('test.csv')['a']
                  0    0
                  1    1
                  2    2
                  3    3
                  4    4
                  5    5
                  6    6
                  7    7
                  8    8
                  9    9
                  Name: a, dtype: int64
                  >>> pd = pd.read_csv('test.csv',dtype={'a':np.float64})
                       a    b           c      d    e
                  0  0.0    a  2019/03/27  09:30   请问
                  1  1.0    b  2019/03/26  10:00    二
                  2  2.0    c  2019/03/25  10:30   同意
                  3  3.0    d  2019/03/24  11:00   UI
                  4  4.0    e  2019/03/23  11:30   欧赔
                  5  5.0    f  2019/03/22  13:00  NaN
                  6  6.0    g  2019/03/21  13:30   东方
                  7  7.0    h  2019/03/20  14:00   更换
                  8  8.0  NaN  2019/03/19  14:30   接口
                  9  9.0    j  2019/03/18  15:00   执行
                  >>> pd['a']
                  0    0.0
                  1    1.0
                  2    2.0
                  3    3.0
                  4    4.0
                  5    5.0
                  6    6.0
                  7    7.0
                  8    8.0
                  9    9.0
                  Name: a, dtype: float64
                  ```
                - engine 选择解释器引擎，可以选'c'、'python'，C解释器速度更快，Python解释器功能更多
                  ```python
                  >>> pd.read_csv('test.csv',engine='c') 
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test.csv',engine='python') # 直接用python引擎读会乱码因为python3 中的字符串默认为 Unicode 编码，这说明默认的解释器引擎应该是C
                     a    b           c      d     e
                  0  0    a  2019/03/27  09:30   璇烽棶
                  1  1    b  2019/03/26  10:00    浜�
                  2  2    c  2019/03/25  10:30   鍚屾剰
                  3  3    d  2019/03/24  11:00    UI
                  4  4    e  2019/03/23  11:30   娆ц禂
                  5  5    f  2019/03/22  13:00   NaN
                  6  6    g  2019/03/21  13:30   涓滄柟
                  7  7    h  2019/03/20  14:00   鏇存崲
                  8  8  NaN  2019/03/19  14:30   鎺ュ彛
                  9  9    j  2019/03/18  15:00  鎵ц��
                  >>> pd.read_csv('test.csv',engine='python',encoding='utf-8') # 加上编码格式 后成功读出中文
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - converters
                  就跟他的名字一样，他可以把数据转换为另一种数据，不仅限于数据类型，他还可以改变数据，需传入字典，键为列名或者列所在的位置，值传函数名
                  ```python
                  >>> def fun(x):
                  ...     x = int(x)+1
                  ...     return x
                  ...
                  >>> pd.read_csv('test.csv',converters = {'a':fun})
                      a    b           c      d    e
                  0   1    a  2019/03/27  09:30   请问
                  1   2    b  2019/03/26  10:00    二
                  2   3    c  2019/03/25  10:30   同意
                  3   4    d  2019/03/24  11:00   UI
                  4   5    e  2019/03/23  11:30   欧赔
                  5   6    f  2019/03/22  13:00  NaN
                  6   7    g  2019/03/21  13:30   东方
                  7   8    h  2019/03/20  14:00   更换
                  8   9  NaN  2019/03/19  14:30   接口
                  9  10    j  2019/03/18  15:00   执行
                  ```
                - true_values 将一列的值认为是True
                  ```python
                  >>> pd.read_csv('test.csv',true_values=['a'])
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',true_values=['a']) # 我目前还没发现这个有啥用，如果有大佬知道，求告诉我一下
                  >>> df['a']
                  0    0
                  1    1
                  2    2
                  3    3
                  4    4
                  5    5
                  6    6
                  7    7
                  8    8
                  9    9
                  Name: a, dtype: int64
                  ```
                - false_values 将一列的值认为是False
                  ```python
                  >>> df = pd.read_csv('test.csv',false_values=['a'])
                  >>> df['a']
                  0    0
                  1    1
                  2    2
                  3    3
                  4    4
                  5    5
                  6    6
                  7    7
                  8    8
                  9    9
                  Name: a, dtype: int64
                  ```
                - skiprows 从顶部开始跳过，然后开始列索引也随之改变，可以传int，和任何可迭代的数据，当传迭代的数据时，在没有0的情况下列索引不会被改变，有0的情况下会将下一个跳过的行作为列索引，如果连续，则为最后一个连续的行作为索引行
                  ```python
                  >>> df = pd.read_csv('test.csv',skiprows=5) # 只传入一个，所以直接将行索引为5作为索银行开始读取
                  >>> df
                     4    e  2019/03/23  11:30   欧赔
                  0  5    f  2019/03/22  13:00  NaN
                  1  6    g  2019/03/21  13:30   东方
                  2  7    h  2019/03/20  14:00   更换
                  3  8  NaN  2019/03/19  14:30   接口
                  4  9    j  2019/03/18  15:00   执行
                  >>> df.loc[0,'e']
                  'f'
                  >>> df = pd.read_csv('test.csv',skiprows=[1,3,4]) # 这里传入多个后,由于没有从第一行开始，所以原来的列索引没有改变
                  >>> df
                     a    b           c      d    e
                  0  1    b  2019/03/26  10:00    二
                  1  4    e  2019/03/23  11:30   欧赔
                  2  5    f  2019/03/22  13:00  NaN
                  3  6    g  2019/03/21  13:30   东方
                  4  7    h  2019/03/20  14:00   更换
                  5  8  NaN  2019/03/19  14:30   接口
                  6  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',skiprows=[0,2,3,4]) # 从第一行开始跳过而且不连续所以列索引就为第一行
                  >>> df
                     0    a  2019/03/27  09:30   请问
                  0  4    e  2019/03/23  11:30   欧赔
                  1  5    f  2019/03/22  13:00  NaN
                  2  6    g  2019/03/21  13:30   东方
                  3  7    h  2019/03/20  14:00   更换
                  4  8  NaN  2019/03/19  14:30   接口
                  5  9    j  2019/03/18  15:00   执行
                  >>> df = pd.read_csv('test.csv',skiprows=[0,1,2,3,4]) # 从第一行开始且传入连续的，所以会直接跳过前面所有的直接从索引为4的位置开始，即将原来索引为4的行作为列索引
                  >>> df
                     4    e  2019/03/23  11:30   欧赔
                  0  5    f  2019/03/22  13:00  NaN
                  1  6    g  2019/03/21  13:30   东方
                  2  7    h  2019/03/20  14:00   更换
                  3  8  NaN  2019/03/19  14:30   接口
                  4  9    j  2019/03/18  15:00   执行
                  ```
                - skipfooter 从底部开始跳过，不支持C引擎，默认为0，只能传入单个int
                  ```python
                  >>> df = pd.read_csv('test.csv',skipfooter=1) # 不指定Python引擎就会出警告
                  __main__:1: ParserWarning: Falling back to the 'python' engine because the 'c' engine does not support ski
                  pfooter; you can avoid this warning by specifying engine='python'.
                  >>> df = pd.read_csv('test.csv',skipfooter=1,engine='python',encoding='utf-8') # 
                  >>> df
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  >>> df = pd.read_csv('test.csv',skipfooter=5,engine='python',encoding='utf-8') # 这个不支持迭代器，只能传单个数字
                  >>> df
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  ```
                - nrows 读取指定行数，读取顺序为从顶部到底部，必须为int
                  ```python
                  >>> pd.read_csv('test.csv',nrows=5)
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  ```
                - na_values 可以将制定值变为缺失值NaN,将多个值放入可迭代对象也可以将多个值都转化为NaN,不想看到它，就把它放进去吧，哈哈
                  ```python
                  >>> pd.read_csv('test.csv',na_values=[0,1,2])
                       a    b           c      d    e
                  0  NaN    a  2019/03/27  09:30   请问
                  1  NaN    b  2019/03/26  10:00    二
                  2  NaN    c  2019/03/25  10:30   同意
                  3  3.0    d  2019/03/24  11:00   UI
                  4  4.0    e  2019/03/23  11:30   欧赔
                  5  5.0    f  2019/03/22  13:00  NaN
                  6  6.0    g  2019/03/21  13:30   东方
                  7  7.0    h  2019/03/20  14:00   更换
                  8  8.0  NaN  2019/03/19  14:30   接口
                  9  9.0    j  2019/03/18  15:00   执行
                  ```
                - keep_default_na 是否保留默认应该转化为缺失值的列表,默认为True,如果你想显示文档的所有内容可以将其改为False并且不传入任何na_values
                  ```python
                  >>> pd.read_csv('test.csv',keep_default_na=False)
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8     2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  ```
                - na_filter 是否不过滤掉所有NA，默认为True
                  ```python
                  >>> pd.read_csv('test.csv',na_filter=False) 
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8     2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_csv('test.csv',na_filter=False,na_values=[0,1,2]) # 从这里可以看出，na_values的优先级比na_filter高
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8     2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  ```
                - verbose 显示标注NA的一些参数   
                    **Tokenization took: 0.00 ms**  
                    **Type conversion took: 0.00 ms**  
                    **Parser memory cleanup took: 0.00 ms**
                  ```python
                  >>> pd.read_csv('test.csv',verbose=True)
                  Tokenization took: 0.00 ms
                  Type conversion took: 0.00 ms
                  Parser memory cleanup took: 0.00 ms
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - skip_blank_lines 是否跳过空白行,默认为True
                  ```python
                  >>> pd.read_csv('test.csv',skip_blank_lines=True,keep_default_na=False,na_filter=False) # 这里可以看出skip_blank_lines的优先级比keep_default_na和na_filter的优先级都高
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8     2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  ```
                - parse_dates 解析数据为时间格式。  
                    **传入boolean格式时，会尝试解析索引;**  
                    **传入int or column name or list 时，解析指定列;(实际测试中出现这个错误TypeError: Only booleans, lists, and dictionaries are accepted for the 'parse_dates' parameter，说明目前版本还不支持int and column name)** 
                    **传入[[]]时会将列表里的解析为一个时间格式;**  
                    **传入dict时会将字典值里的两列合并为时间格式赋值给键**
                  ```python
                  >>> pd.read_csv('test.csv',parse_dates=True)['c']
                  0    2019/03/27
                  1    2019/03/26
                  2    2019/03/25
                  3    2019/03/24
                  4    2019/03/23
                  5    2019/03/22
                  6    2019/03/21
                  7    2019/03/20
                  8    2019/03/19
                  9    2019/03/18
                  Name: c, dtype: object
                  >>> pd.read_csv('test.csv',parse_dates=True)['d']
                  0    09:30
                  1    10:00
                  2    10:30
                  3    11:00
                  4    11:30
                  5    13:00
                  6    13:30
                  7    14:00
                  8    14:30
                  9    15:00
                  Name: d, dtype: object
                  >>> pd.read_csv('test.csv',parse_dates=[2])['c']
                  0   2019-03-27
                  1   2019-03-26
                  2   2019-03-25
                  3   2019-03-24
                  4   2019-03-23
                  5   2019-03-22
                  6   2019-03-21
                  7   2019-03-20
                  8   2019-03-19
                  9   2019-03-18
                  Name: c, dtype: datetime64[ns]
                  >>> pd.read_csv('test.csv',parse_dates=[3])['d'] # 当数据时分时时会在前面加入了当前的日期
                  0   2019-03-27 09:30:00
                  1   2019-03-27 10:00:00
                  2   2019-03-27 10:30:00
                  3   2019-03-27 11:00:00
                  4   2019-03-27 11:30:00
                  5   2019-03-27 13:00:00
                  6   2019-03-27 13:30:00
                  7   2019-03-27 14:00:00
                  8   2019-03-27 14:30:00
                  9   2019-03-27 15:00:00
                  Name: d, dtype: datetime64[ns]
                  >>> pd.read_csv('test.csv',parse_dates=[2])['c'] # 当数据时日期是会将他的类型改变
                  0   2019-03-27
                  1   2019-03-26
                  2   2019-03-25
                  3   2019-03-24
                  4   2019-03-23
                  5   2019-03-22
                  6   2019-03-21
                  7   2019-03-20
                  8   2019-03-19
                  9   2019-03-18
                  Name: c, dtype: datetime64[ns]
                  >>> pd.read_csv('test.csv',parse_dates={'时间':[2,3]})
                    时间  a    b    e
                  0 2019-03-27 09:30:00  0    a   请问
                  1 2019-03-26 10:00:00  1    b    二
                  2 2019-03-25 10:30:00  2    c   同意
                  3 2019-03-24 11:00:00  3    d   UI
                  4 2019-03-23 11:30:00  4    e   欧赔
                  5 2019-03-22 13:00:00  5    f  NaN
                  6 2019-03-21 13:30:00  6    g   东方
                  7 2019-03-20 14:00:00  7    h   更换
                  8 2019-03-19 14:30:00  8  NaN   接口
                  9 2019-03-18 15:00:00  9    j   执行
                  >>> pd.read_csv('test.csv',parse_dates={'时间':[2,3]})['时间']
                  0   2019-03-27 09:30:00
                  1   2019-03-26 10:00:00
                  2   2019-03-25 10:30:00
                  3   2019-03-24 11:00:00
                  4   2019-03-23 11:30:00
                  5   2019-03-22 13:00:00
                  6   2019-03-21 13:30:00
                  7   2019-03-20 14:00:00
                  8   2019-03-19 14:30:00
                  9   2019-03-18 15:00:00
                  Name: 时间, dtype: datetime64[ns]
                  ```
                - infer_datetime_format 开启datetime解析，如果和parse_dates同时开启速度回快5-10倍,默认为Fasle
                  ```pyton
                  >>> pd.read_csv('test.csv',parse_dates={'时间':[2,3]},infer_datetime_format=True) # 没感觉快多少啊，可能数据量比较小，看不出来
                     时间  a    b    e
                  0 2019-03-27 09:30:00  0    a   请问
                  1 2019-03-26 10:00:00  1    b    二
                  2 2019-03-25 10:30:00  2    c   同意
                  3 2019-03-24 11:00:00  3    d   UI
                  4 2019-03-23 11:30:00  4    e   欧赔
                  5 2019-03-22 13:00:00  5    f  NaN
                  6 2019-03-21 13:30:00  6    g   东方
                  7 2019-03-20 14:00:00  7    h   更换
                  8 2019-03-19 14:30:00  8  NaN   接口
                  9 2019-03-18 15:00:00  9    j   执行
                  ```
                - keep_date_col 在parse_dates传入字典时可以保存原始列
                  ```python
                  >>> pd.read_csv('test.csv',parse_dates={'时间':[2,3]},keep_date_col=True)
                     时间  a    b           c      d    e
                  0 2019-03-27 09:30:00  0    a  2019/03/27  09:30   请问
                  1 2019-03-26 10:00:00  1    b  2019/03/26  10:00    二
                  2 2019-03-25 10:30:00  2    c  2019/03/25  10:30   同意
                  3 2019-03-24 11:00:00  3    d  2019/03/24  11:00   UI
                  4 2019-03-23 11:30:00  4    e  2019/03/23  11:30   欧赔
                  5 2019-03-22 13:00:00  5    f  2019/03/22  13:00  NaN
                  6 2019-03-21 13:30:00  6    g  2019/03/21  13:30   东方
                  7 2019-03-20 14:00:00  7    h  2019/03/20  14:00   更换
                  8 2019-03-19 14:30:00  8  NaN  2019/03/19  14:30   接口
                  9 2019-03-18 15:00:00  9    j  2019/03/18  15:00   执行
                  ```
                - date_parser 通过特殊函数将字符串转化为datatime格式
                  ```python
                  >>> def my_date_parser(dt):
                  ...     return datetime(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]))
                  ...
                  >>> pd.read_csv('test.csv',date_parser=my_date_parser,parse_dates={'time':[2]})
                          time  a    b      d    e
                  0 2019-03-27  0    a  09:30   请问
                  1 2019-03-26  1    b  10:00    二
                  2 2019-03-25  2    c  10:30   同意
                  3 2019-03-24  3    d  11:00   UI
                  4 2019-03-23  4    e  11:30   欧赔
                  5 2019-03-22  5    f  13:00  NaN
                  6 2019-03-21  6    g  13:30   东方
                  7 2019-03-20  7    h  14:00   更换
                  8 2019-03-19  8  NaN  14:30   接口
                  9 2019-03-18  9    j  15:00   执行
                  >>> pd.read_csv('test.csv',date_parser=my_date_parser,parse_dates={'time':[2]})['time']
                  0   2019-03-27
                  1   2019-03-26
                  2   2019-03-25
                  3   2019-03-24
                  4   2019-03-23
                  5   2019-03-22
                  6   2019-03-21
                  7   2019-03-20
                  8   2019-03-19
                  9   2019-03-18
                  Name: time, dtype: datetime64[ns]
                  ```
                - dayfirst 是否开启日期解析 默认为否
                  ```python
                  >>> pd.read_csv('test.csv',dayfirst=True)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test.csv',dayfirst=True)['c']
                  0    2019/03/27
                  1    2019/03/26
                  2    2019/03/25
                  3    2019/03/24
                  4    2019/03/23
                  5    2019/03/22
                  6    2019/03/21
                  7    2019/03/20
                  8    2019/03/19
                  9    2019/03/18
                  Name: c, dtype: object
                  >>> pd.read_csv('test.csv',dayfirst=True)['d']
                  0    09:30
                  1    10:00
                  2    10:30
                  3    11:00
                  4    11:30
                  5    13:00
                  6    13:30
                  7    14:00
                  8    14:30
                  9    15:00
                  Name: d, dtype: object
                  ```
                - iterator 是否将结果转为可迭代对象，还可以通过get_chunk方法获取
                  ```python
                  >>> pd.read_csv('test.csv',iterator=True)
                  <pandas.io.parsers.TextFileReader object at 0x0000017A2836A518>
                  >>> for i in pd.read_csv('test.csv',iterator=True):
                  ...     print(i)
                  ...
                  <built-in function print>
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test.csv',iterator=True).get_chunk()
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  
                  ```
                - chunksize 将提供的行数变成可迭代对象，同样可以通过get_chunk方法获取
                  ```python
                  >>> pd.read_csv('test.csv',chunksize=1)
                  <pandas.io.parsers.TextFileReader object at 0x00000183F582A1D0>
                  >>> for i in pd.read_csv('test.csv',chunksize=5): # 这里遍历的时候好像是将它切割开
                  ...     print(i)
                  ...
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                     a    b           c      d    e
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> for i in pd.read_csv('test.csv',chunksize=1):
                  ...     print(i)
                  ...
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                     a  b           c      d  e
                  1  1  b  2019/03/26  10:00  二
                     a  b           c      d   e
                  2  2  c  2019/03/25  10:30  同意
                     a  b           c      d   e
                  3  3  d  2019/03/24  11:00  UI
                     a  b           c      d   e
                  4  4  e  2019/03/23  11:30  欧赔
                     a  b           c      d   e
                  5  5  f  2019/03/22  13:00 NaN
                     a  b           c      d   e
                  6  6  g  2019/03/21  13:30  东方
                     a  b           c      d   e
                  7  7  h  2019/03/20  14:00  更换
                     a   b           c      d   e
                  8  8 NaN  2019/03/19  14:30  接口
                     a  b           c      d   e
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_csv('test.csv',chunksize=1).get_chunk()
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  >>> pd.read_csv('test.csv',chunksize=5).get_chunk()
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  ```
                - compression 解压缩，可选{‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, 默认‘infer’
                  ```python
                  >>> pd.read_csv('test.zip',compression='zip')
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - thousands 千位分隔符
                  ```python
                  >>> df = pd.read_csv('test.csv') # 因为它没有上千的数字
                  >>> df['a']=df['a']*99999 # 于是我将a列全都×99999
                  >>> df
                          a    b           c      d    e
                  0       0    a  2019/03/27  09:30   请问
                  1   99999    b  2019/03/26  10:00    二
                  2  199998    c  2019/03/25  10:30   同意
                  3  299997    d  2019/03/24  11:00   UI
                  4  399996    e  2019/03/23  11:30   欧赔
                  5  499995    f  2019/03/22  13:00  NaN
                  6  599994    g  2019/03/21  13:30   东方
                  7  699993    h  2019/03/20  14:00   更换
                  8  799992  NaN  2019/03/19  14:30   接口
                  9  899991    j  2019/03/18  15:00   执行
                  >>> df.to_csv('test2.csv') # 将结果存入test2
                  >>> pd.read_csv('test2.csv') # 读出test2查看是否正确
                     Unnamed: 0       a    b           c      d    e
                  0           0       0    a  2019/03/27  09:30   请问
                  1           1   99999    b  2019/03/26  10:00    二
                  2           2  199998    c  2019/03/25  10:30   同意
                  3           3  299997    d  2019/03/24  11:00   UI
                  4           4  399996    e  2019/03/23  11:30   欧赔
                  5           5  499995    f  2019/03/22  13:00  NaN
                  6           6  599994    g  2019/03/21  13:30   东方
                  7           7  699993    h  2019/03/20  14:00   更换
                  8           8  799992  NaN  2019/03/19  14:30   接口
                  9           9  899991    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test2.csv',thousands='/') # 但是一顿操作猛如虎，结果啥都没变
                     Unnamed: 0       a    b         c      d    e
                  0           0       0    a  20190327  09:30   请问
                  1           1   99999    b  20190326  10:00    二
                  2           2  199998    c  20190325  10:30   同意
                  3           3  299997    d  20190324  11:00   UI
                  4           4  399996    e  20190323  11:30   欧赔
                  5           5  499995    f  20190322  13:00  NaN
                  6           6  599994    g  20190321  13:30   东方
                  7           7  699993    h  20190320  14:00   更换
                  8           8  799992  NaN  20190319  14:30   接口
                  9           9  899991    j  20190318  15:00   执行
                  ```
                
                - decimal 识别成小数点的字符，默认为‘.’注意，只能穿一个长度的str
                  ```python
                  >>> pd.read_csv('test.csv',decimal=':')
                     a    b           c     d    e
                  0  0    a  2019/03/27   9.3   请问
                  1  1    b  2019/03/26  10.0    二
                  2  2    c  2019/03/25  10.3   同意
                  3  3    d  2019/03/24  11.0   UI
                  4  4    e  2019/03/23  11.3   欧赔
                  5  5    f  2019/03/22  13.0  NaN
                  6  6    g  2019/03/21  13.3   东方
                  7  7    h  2019/03/20  14.0   更换
                  8  8  NaN  2019/03/19  14.3   接口
                  9  9    j  2019/03/18  15.0   执行
                  ```
                - lineterminator 行结束标识符，会根据传入的str结束行，只对C引擎有效
                  ```python
                  >>> pd.read_csv('test.csv',lineterminator=',')
                               a
                  0            b
                  1            c
                  2            d
                  3       e\r\n0
                  4            a
                  5   2019/03/27
                  6        09:30
                  7      请问\r\n1
                  8            b
                  9   2019/03/26
                  10       10:00
                  11      二\r\n2
                  12           c
                  13  2019/03/25
                  14       10:30
                  15     同意\r\n3
                  16           d
                  17  2019/03/24
                  18       11:00
                  19     UI\r\n4
                  20           e
                  21  2019/03/23
                  22       11:30
                  23     欧赔\r\n5
                  24           f
                  25  2019/03/22
                  26       13:00
                  27       \r\n6
                  28           g
                  29  2019/03/21
                  30       13:30
                  31     东方\r\n7
                  32           h
                  33  2019/03/20
                  34       14:00
                  35     更换\r\n8
                  36  2019/03/19
                  37       14:30
                  38     接口\r\n9
                  39           j
                  40  2019/03/18
                  41       15:00
                  42      执行\r\n
                  ```
                - quotechar 
                // TODO 引用分隔符
                - quoting 
                // TODO 引用
                - doublequote
                // TODO 引用啥咧
                - escapechar 将一个长度为1的字符串变为转义字符
                  ```python 
                  >>> pd.read_csv('test.csv',escapechar='/')
                     a    b         c      d    e
                  0  0    a  20190327  09:30   请问
                  1  1    b  20190326  10:00    二
                  2  2    c  20190325  10:30   同意
                  3  3    d  20190324  11:00   UI
                  4  4    e  20190323  11:30   欧赔
                  5  5    f  20190322  13:00  NaN
                  6  6    g  20190321  13:30   东方
                  7  7    h  20190320  14:00   更换
                  8  8  NaN  20190319  14:30   接口
                  9  9    j  20190318  15:00   执行
                  ```
                - comment 
                //TODO 注释相关
                - encoding 编码方式
                  ```python
                  >>> pd.read_csv('test.csv',engine='python')
                     a    b           c      d     e
                  0  0    a  2019/03/27  09:30   璇烽棶
                  1  1    b  2019/03/26  10:00    浜�
                  2  2    c  2019/03/25  10:30   鍚屾剰
                  3  3    d  2019/03/24  11:00    UI
                  4  4    e  2019/03/23  11:30   娆ц禂
                  5  5    f  2019/03/22  13:00   NaN
                  6  6    g  2019/03/21  13:30   涓滄柟
                  7  7    h  2019/03/20  14:00   鏇存崲
                  8  8  NaN  2019/03/19  14:30   鎺ュ彛
                  9  9    j  2019/03/18  15:00  鎵ц��
                  >>> pd.read_csv('test.csv',engine='python',encoding='utf-8')
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - dialect 
                  ```python
                  
                  ```
                - tupleize_cols 
                  ```python
                  >>> pd.read_csv('test.csv',tupleize_cols=True)
                  xxx:885: FutureWarning: The'tupleize_cols' argument has been deprecated and will be removed in a future version. Column tuples will t
                  hen always be converted to MultiIndex.
                  self.options, self.engine = self._clean_options(options, engine)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - error_bad_lines 将问题行删除,默认为True
                  ```python
                  >>> pd.read_csv('test.csv',error_bad_lines=False)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - warn_bad_lines 显示问题行的警告，默认为True
                  ```python
                  >>> pd.read_csv('test.csv',warn_bad_lines=False)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - delim_whitespace 将换行符换成空格，等效于sep='\s+'，默认为False
                  ```python
                  >>> pd.read_csv('test.csv',delim_whitespace =True)
                   a,b,c,d,e
                  0  0,a,2019/03/27,09:30,请问
                  1   1,b,2019/03/26,10:00,二
                  2  2,c,2019/03/25,10:30,同意
                  3  3,d,2019/03/24,11:00,UI
                  4  4,e,2019/03/23,11:30,欧赔
                  5    5,f,2019/03/22,13:00,
                  6  6,g,2019/03/21,13:30,东方
                  7  7,h,2019/03/20,14:00,更换
                  8   8,,2019/03/19,14:30,接口
                  9  9,j,2019/03/18,15:00,执行
                  ```
                - low_memory 减少对df数据类型的选择，降低消耗内存，大白话就是为了减少内存消耗放弃一些数据类型的精度
                  ```python
                  >>> pd.read_csv('test.csv',low_memory =False)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - memory_map 将文件加载到内存中，提高读取效率
                  ```python
                  >>> pd.read_csv('test.csv',memory_map =True)
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  ```
                - float_precision 在C引擎在，可以优化浮点数
                  ```python
                  >>> pd.read_csv('test.csv',float_precision=":")
                     a    b           c      d    e
                  0  0    a  2019/03/27  09:30   请问
                  1  1    b  2019/03/26  10:00    二
                  2  2    c  2019/03/25  10:30   同意
                  3  3    d  2019/03/24  11:00   UI
                  4  4    e  2019/03/23  11:30   欧赔
                  5  5    f  2019/03/22  13:00  NaN
                  6  6    g  2019/03/21  13:30   东方
                  7  7    h  2019/03/20  14:00   更换
                  8  8  NaN  2019/03/19  14:30   接口
                  9  9    j  2019/03/18  15:00   执行
                  >>> pd.read_csv('test.csv',float_precision=".",dtype={'a':np.float64})['a'] # 貌似没啥用啊
                  0    0.0
                  1    1.0
                  2    2.0
                  3    3.0
                  4    4.0
                  5    5.0
                  6    6.0
                  7    7.0
                  8    8.0
                  9    9.0
                  Name: a, dtype: float64
                  ```
        - pd.read_table  
        **Deprecated since version 0.24.0. Use pandas.read_csv() instead, passing sep='\t' if necessary.  
        Also supports optionally iterating or breaking of the file into chunks.  
        Additional help can be found in the online docs for IO Tools.**  
        这是官方文档里写的一段话，大致意思就是在pandas 0.24.0以后的版本中不推荐使用read_table,你们可以用read_csv()代替，用sep='\t'设置分隔符，所以read_table,就say 88 啦~~~
        - pd.read_excel,读取Excel格式文件
            - 参数解读
                - io 文件路径或者文件对象或者URL，跟read_csv中的filepath_or_buffer参数有点类似
                  ```python
                  >>> pd.read_excel('test.xls')
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'))
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  ```
                - sheet_name 表名，可以传int或者str或者list，默认为0，0表示第一个表str直接写表明，list可以传多个表，可以int和str混用
                  ```python
                  >>> pd.read_excel(open('test.xlsx','rb'),sheet_name='Sheet1')
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),sheet_name=0)
                     a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),sheet_name=[0,'Sheet2'])
                  OrderedDict([(0,    a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行), ('Sheet2',    a  b           c      d   e
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行)])
                  ```
                - header 表头开始的位置，不管是int还是header，第一个出现的行作为索引行
                  ```python
                  >>> pd.read_excel(open('test.xlsx','rb'),header=1) # 从第一行开始，即将第一行变成列索引
                     0  a  2019/03/27  09:30  请问
                  0  1  b  2019/03/26  10:00   二
                  1  2  c  2019/03/25  10:30  同意
                  2  3  d  2019/03/24  11:00  UI
                  3  4  e  2019/03/23  11:30  欧赔
                  4  5  f  2019/03/22  13:00  爱思
                  5  6  g  2019/03/21  13:30  东方
                  6  7  h  2019/03/20  14:00  更换
                  7  8  i  2019/03/19  14:30  接口
                  8  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),header=[1,2,3,4]) # 将1,2,3,4行变成表头
                     0  a  2019/03/27  09:30  请问
                     1  b  2019/03/26  10:00   二
                     2  c  2019/03/25  10:30  同意
                     3  d  2019/03/24  11:00  UI
                  0  4  e  2019/03/23  11:30  欧赔
                  1  5  f  2019/03/22  13:00  爱思
                  2  6  g  2019/03/21  13:30  东方
                  3  7  h  2019/03/20  14:00  更换
                  4  8  i  2019/03/19  14:30  接口
                  5  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),header=[1,2,3,4])['a'] # 因为是从第一行，所以索引为a'
                     b
                     c
                     d
                  0  e
                  1  f
                  2  g
                  3  h
                  4  i
                  5  j
                  >>> pd.read_excel(open('test.xlsx','rb'),header=[0,1,2,3,4]) #  从第0行开始，即0行是列索引行
                     a  b           c      d   e
                     0  a  2019/03/27  09:30  请问
                     1  b  2019/03/26  10:00   二
                     2  c  2019/03/25  10:30  同意
                     3  d  2019/03/24  11:00  UI
                  0  4  e  2019/03/23  11:30  欧赔
                  1  5  f  2019/03/22  13:00  爱思
                  2  6  g  2019/03/21  13:30  东方
                  3  7  h  2019/03/20  14:00  更换
                  4  8  i  2019/03/19  14:30  接口
                  5  9  j  2019/03/18  15:00  执行
                  ```
                - names 列名
                  ```python
                  >>> pd.read_excel(open('test.xlsx','rb'),names=[1,2,3,4,5]) # 当列表跟表中列数匹配时，将列索引名更换为names里的名
                     1  2           3      4   5
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),names=[1,2,3,3,5]) # 当出现重复时，会变成x:x.1
                     1  2           3    3.1   5
                  0  0  a  2019/03/27  09:30  请问
                  1  1  b  2019/03/26  10:00   二
                  2  2  c  2019/03/25  10:30  同意
                  3  3  d  2019/03/24  11:00  UI
                  4  4  e  2019/03/23  11:30  欧赔
                  5  5  f  2019/03/22  13:00  爱思
                  6  6  g  2019/03/21  13:30  东方
                  7  7  h  2019/03/20  14:00  更换
                  8  8  i  2019/03/19  14:30  接口
                  9  9  j  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),names=[1,2,3,5]) # 当数量不匹配时会报错
                  ...
                  ValueError: Number of passed names did not match number of header fields in the file
                  ```
                - index_col
                  ```python
                  >>> pd.read_excel(open('test.xlsx','rb'),index_col=1)
                     a           c      d   e
                  b
                  a  0  2019/03/27  09:30  请问
                  b  1  2019/03/26  10:00   二
                  c  2  2019/03/25  10:30  同意
                  d  3  2019/03/24  11:00  UI
                  e  4  2019/03/23  11:30  欧赔
                  f  5  2019/03/22  13:00  爱思
                  g  6  2019/03/21  13:30  东方
                  h  7  2019/03/20  14:00  更换
                  i  8  2019/03/19  14:30  接口
                  j  9  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),index_col='e')
                      a  b           c      d
                  e
                  请问  0  a  2019/03/27  09:30
                  二   1  b  2019/03/26  10:00
                  同意  2  c  2019/03/25  10:30
                  UI  3  d  2019/03/24  11:00
                  欧赔  4  e  2019/03/23  11:30
                  爱思  5  f  2019/03/22  13:00
                  东方  6  g  2019/03/21  13:30
                  更换  7  h  2019/03/20  14:00
                  接口  8  i  2019/03/19  14:30
                  执行  9  j  2019/03/18  15:00
                  >>> pd.read_excel(open('test.xlsx','rb'),index_col=['e',0])
                  TypeError: list indices must be integers or slices, not str
                  >>> pd.read_excel(open('test.xlsx','rb'),index_col=[1,0])
                                c      d   e
                  b a
                  a 0  2019/03/27  09:30  请问
                  b 1  2019/03/26  10:00   二
                  c 2  2019/03/25  10:30  同意
                  d 3  2019/03/24  11:00  UI
                  e 4  2019/03/23  11:30  欧赔
                  f 5  2019/03/22  13:00  爱思
                  g 6  2019/03/21  13:30  东方
                  h 7  2019/03/20  14:00  更换
                  i 8  2019/03/19  14:30  接口
                  j 9  2019/03/18  15:00  执行
                  >>> pd.read_excel(open('test.xlsx','rb'),index_col=[1,0]).loc['a','c']
                  a
                  0    2019/03/27
                  Name: c, dtype: object
                  ```
                - parse_cols 给列起别名
                Deprecated since version 0.21.0: Use usecols instead. 
                - usecols 
                Deprecated since version 0.24.0: Pass in a list of int instead from 0 to usecols inclusive.
        - pd.read_sql,读取SQL格式文件
        - pd.read_json,读取JSON格式文件
        - pd.read_html,读取html格式文件
        - pd.read_clipbard,读取剪切板数据
    - 导出：
        - df.to_csv,
        - df.to_excel,
        - df.tp_sql,
        - df.to_json,
