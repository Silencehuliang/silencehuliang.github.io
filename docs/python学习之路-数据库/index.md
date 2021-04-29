# Python学习之路-数据库


## ORM框架

### 简介

O是object，也就**类对象**的意思，R是relation，翻译成中文是关系，也就是关系数据库中**数据表**的意思，M是mapping，是**映射**的意思。在ORM框架中，它帮我们把类和数据表进行了一个映射，可以让我们**通过类和类对象就能操作它所对应的表格中的数据**。ORM框架还有一个功能，它可以**根据我们设计的类自动帮我们生成数据库中的表格**，省去了我们自己建表的过程。

django中内嵌了ORM框架，不需要直接面向数据库编程，而是定义模型类，通过模型类和对象完成数据表的增删改查操作。

使用django进行数据库开发的步骤如下：

1. 配置数据库连接信息
2. 在models.py中定义模型类
3. 迁移
4. 通过类和对象完成数据增删改查操作

### 配置

- 在settings.py中保存了数据库的连接配置信息，Django默认初始配置使用**sqlite**数据库。

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }
  }
  ```

- 使用**MySQL**数据库首先需要安装驱动程序

  ```shell
  pip install PyMySQL
  ```

- 在Django的工程同名子目录的__init__.py文件中添加如下语句

  ```python
  from pymysql import install_as_MySQLdb

  install_as_MySQLdb()
  ```
  
  作用是让Django的ORM能以mysqldb的方式来调用PyMySQL。
  
- 修改**DATABASES**配置信息

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'HOST': '127.0.0.1',  # 数据库主机
          'PORT': 3306,  # 数据库端口
          'USER': 'root',  # 数据库用户名
          'PASSWORD': 'mysql',  # 数据库用户密码
          'NAME': 'django_demo'  # 数据库名字
      }
  }
  ```

- 在MySQL中创建数据库

  ```mysql
  create database django_demo default charset=utf8;
  ```

### 定义模型类

#### 简介

模型类被定义在"应用/models.py"文件中。，模型类必须继承自Model类，位于包django.db.models中。

#### 定义

创建应用booktest，在models.py 文件中定义模型类。

```python
from django.db import models

#定义图书模型类BookInfo
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle

#定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    hname = models.CharField(max_length=20, verbose_name='名称') 
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')  
    hcomment = models.CharField(max_length=200, null=True, verbose_name='描述信息') 
    hbook = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname
```

- 数据库表名

  模型类如果未指明表名，Django默认以 **小写app应用名_小写模型类名** 为数据库表名。

  可通过**db_table** 指明数据库表名。

- 关于主键

  django会为表创建自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置某属性为主键列后django不会再创建自动增长的主键列。

  默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。

- 属性命名限制
  - 不能是python的保留关键字。

  - 不允许使用连续的下划线，这是由django的查询方式决定的。

  - 定义属性时需要指定字段类型，通过字段类型的参数指定选项，语法如下：

    ```python
    属性=models.字段类型(选项)
    ```

- 字段类型

  | 类型             | 说明                                                         |
  | :--------------- | :----------------------------------------------------------- |
  | AutoField        | 自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性 |
  | BooleanField     | 布尔字段，值为True或False                                    |
  | NullBooleanField | 支持Null、True、False三种值                                  |
  | CharField        | 字符串，参数max_length表示最大字符个数                       |
  | TextField        | 大文本字段，一般超过4000个字符时使用                         |
  | IntegerField     | 整数                                                         |
  | DecimalField     | 十进制浮点数， 参数max_digits表示总位数， 参数decimal_places表示小数位数 |
  | FloatField       | 浮点数                                                       |
  | DateField        | 日期， 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为False； 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False; 参数auto_now_add和auto_now是相互排斥的，组合将会发生错误 |
  | TimeField        | 时间，参数同DateField                                        |
  | DateTimeField    | 日期时间，参数同DateField                                    |
  | FileField        | 上传文件字段                                                 |
  | ImageField       | 继承于FileField，对上传的内容进行校验，确保是有效的图片      |

- 选项

  | 选项        | 说明                                                         |
  | :---------- | ------------------------------------------------------------ |
  | null        | 如果为True，表示允许为空，默认值是False                      |
  | blank       | 如果为True，则该字段允许为空白，默认值是False                |
  | db_column   | 字段的名称，如果未指定，则使用属性的名称                     |
  | db_index    | 若值为True, 则在表中会为此字段创建索引，默认值是False        |
  | default     | 默认                                                         |
  | primary_key | 若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用 |
  | unique      | 如果为True, 这个字段在表中必须有唯一值，默认值是False        |
  
  **null是数据库范畴的概念，blank是表单验证范畴的**

- 外键

  在设置外键时，需要通过**on_delete**选项指明主表删除数据时，对于外键引用表数据如何处理，在django.db.models中包含了可选常量：

  - **CASCADE** 级联，删除主表数据时连通一起删除外键表中数据

  - **PROTECT** 保护，通过抛出**ProtectedError**异常，来阻止删除主表中被外键应用的数据

  - **SET_NULL** 设置为NULL，仅在该字段null=True允许为null时可用

  - **SET_DEFAULT** 设置为默认值，仅在该字段设置了默认值时可用

  - **SET()** 设置为特定值或者调用特定方法，如

    ```python
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.db import models

    def get_sentinel_user():
        return get_user_model().objects.get_or_create(username='deleted')[0]

    class MyModel(models.Model):
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET(get_sentinel_user),
        )
    ```
    
  - **DO_NOTHING** 不做任何操作，如果数据库前置指明级联性，此选项会抛出**IntegrityError**异常

#### 迁移

将模型类同步到数据库中。

- 生成迁移文件

  ```python
  python manage.py makemigrations
  ```

- 同步到数据库中

  ```python
  python manage.py migrate
  ```

### 数据库操作

#### 增加

增加数据有两种方法。

- save，通过创建模型类对象，执行对象的save()方法保存到数据库中。

  ```python
  >>> from datetime import date
  >>> book = BookInfo(
      btitle='西游记',
      bput_date=date(1988,1,1),
      bread=10,
      bcomment=10
  )
  >>> book.save()
  >>> hero = HeroInfo(
      hname='孙悟空',
      hgender=0,
      hbook=book
  )
  >>> hero.save()
  >>> hero2 = HeroInfo(
      hname='猪八戒',
      hgender=0,
      hbook_id=book.id
  )
  >>> hero2.save()
  ```

- create，通过模型类.objects.create()保存。

  ```python
  >>> HeroInfo.objects.create(
      hname='沙悟净',
      hgender=0,
      hbook=book
  )
  <HeroInfo: 沙悟净>
  ```

#### 查询

##### 基本查询

- **get** 查询单一结果，如果不存在会抛出**模型类.DoesNotExist**异常。

- **all** 查询多个结果。

- **count** 查询结果数量。

  ```python
  >>> BookInfo.objects.all()
  <QuerySet [<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>, <BookInfo: 笑傲江湖>, <BookInfo: 雪山飞狐>, <BookInfo: 西游记>]>
  >>> book = BookInfo.objects.get(btitle='西游记')
  >>> book.id
  5

  >>> BookInfo.objects.get(id=3)
  <BookInfo: 笑傲江湖>
  >>> BookInfo.objects.get(pk=3)
  <BookInfo: 笑傲江湖>
  >>> BookInfo.objects.get(id=100)
  Traceback (most recent call last):
    File "<console>", line 1, in <module>
    File "/Users/delron/.virtualenv/dj/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
      return getattr(self.get_queryset(), name)(*args, **kwargs)
    File "/Users/delron/.virtualenv/dj/lib/python3.6/site-packages/django/db/models/query.py", line 380, in get
      self.model._meta.object_name
  db.models.DoesNotExist: BookInfo matching query does not exist.

  >>> BookInfo.objects.count()
  6
  ```

##### 过滤查询

实现SQL中的where功能，包括

- **filter** 过滤出多个结果
- **exclude** 排除掉符合条件剩下的结果
- **get** 过滤单一结果

对于过滤条件的使用，上述三个方法相同，故仅以**filter**进行讲解。

过滤条件的表达语法如下：

```python
属性名称__比较运算符=值
# 属性名称和比较运算符间使用两个下划线，所以属性名不能包括多个下划线
```

###### 相等

**exact：表示判等。**

例：查询编号为1的图书。

```
BookInfo.objects.filter(id__exact=1)
可简写为：
BookInfo.objects.filter(id=1)
```

###### 模糊查询

**contains：是否包含。**

{{< admonition tip "说明" true >}}

如果要包含%无需转义，直接写即可。

{{< /admonition >}}

例：查询书名包含'传'的图书。

```python
BookInfo.objects.filter(btitle__contains='传')
```

**startswith、endswith：以指定值开头或结尾。**

例：查询书名以'部'结尾的图书

```python
BookInfo.objects.filter(btitle__endswith='部')
```

{{< admonition tip "说明" true >}}

以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.

{{< /admonition >}}

###### 空查询

**isnull：是否为null。**

例：查询书名不为空的图书。

```python
BookInfo.objects.filter(btitle__isnull=False)
```

###### 范围查询

**in：是否包含在范围内。**

例：查询编号为1或3或5的图书

```python
BookInfo.objects.filter(id__in=[1, 3, 5])
```

###### 比较查询

- **gt** 大于 (greater then)
- **gte** 大于等于 (greater then equal)
- **lt** 小于 (less then)
- **lte** 小于等于 (less then equal)

例：查询编号大于3的图书

```python
BookInfo.objects.filter(id__gt=3)
```

**不等于的运算符，使用exclude()过滤器。**

例：查询编号不等于3的图书

```python
BookInfo.objects.exclude(id=3)
```

###### 日期查询

**year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。**

例：查询1980年发表的图书。

```python
BookInfo.objects.filter(bpub_date__year=1980)
```

例：查询1980年1月1日后发表的图书。

```python
BookInfo.objects.filter(bpub_date__gt=date(1990, 1, 1))
```

#### F对象

之前的查询都是对象的属性与常量值比较，两个属性怎么比较呢？ 答：使用F对象，被定义在django.db.models中。

语法如下：

```
F(属性名)
```

例：查询阅读量大于等于评论量的图书。

```python
from django.db.models import F

BookInfo.objects.filter(bread__gte=F('bcomment'))
```

可以在F对象上使用算数运算。

例：查询阅读量大于2倍评论量的图书。

```python
BookInfo.objects.filter(bread__gt=F('bcomment') * 2)
```

#### Q对象

**多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字。**

例：查询阅读量大于20，并且编号小于3的图书。

```python
BookInfo.objects.filter(bread__gt=20,id__lt=3)
或
BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)
```

**如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符**，Q对象被义在django.db.models中。

语法如下：

```
Q(属性名__运算符=值)
```

例：查询阅读量大于20的图书，改写为Q对象如下。

```python
from django.db.models import Q

BookInfo.objects.filter(Q(bread__gt=20))
```

Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。

例：查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现

```python
BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))
```

Q对象前可以使用~操作符，表示非not。

例：查询编号不等于3的图书。

```python
BookInfo.objects.filter(~Q(pk=3))
```

#### 聚合函数

使用aggregate()过滤器调用聚合函数。聚合函数包括：**Avg** 平均，**Count** 数量，**Max** 最大，**Min** 最小，**Sum** 求和，被定义在django.db.models中。

例：查询图书的总阅读量。

```python
from django.db.models import Sum

BookInfo.objects.aggregate(Sum('bread'))
```

注意aggregate的返回值是一个字典类型，格式如下：

```python
  {'属性名__聚合类小写':值}
  如:{'bread__sum':3}
```

使用count时一般不使用aggregate()过滤器。

例：查询图书总数。

```python
BookInfo.objects.count()
```

注意count函数的返回值是一个数字。

##### 排序

使用**order_by**对结果进行排序

```python
BookInfo.objects.all().order_by('bread')  # 升序
BookInfo.objects.all().order_by('-bread')  # 降序
```

##### 关联查询

由一到多的访问语法：

一对应的模型类对象.多对应的模型类名小写_set 例：

```python
b = BookInfo.objects.get(id=1)
b.heroinfo_set.all()
```

由多到一的访问语法:

多对应的模型类对象.多对应的模型类中的关系类属性名 例：

```python
h = HeroInfo.objects.get(id=1)
h.hbook
```

访问一对应的模型类关联对象的id语法:

多对应的模型类对象.关联类属性_id

例：

```python
h = HeroInfo.objects.get(id=1)
h.hbook_id
```

##### 关联过滤查询

**由多模型类条件查询一模型类数据**:

语法如下：

```python
关联模型类名小写__属性名__条件运算符=值
```

**注意：如果没有"__运算符"部分，表示等于。**

例：

查询图书，要求图书英雄为"孙悟空"

```python
BookInfo.objects.filter(heroinfo__hname='孙悟空')
```

查询图书，要求图书中英雄的描述包含"八"

```python
BookInfo.objects.filter(heroinfo__hcomment__contains='八')
```

**由一模型类条件查询多模型类数据**:

语法如下：

```
一模型类关联属性名__一模型类属性名__条件运算符=值
```

**注意：如果没有"__运算符"部分，表示等于。**

例：

查询书名为“天龙八部”的所有英雄。

```python
HeroInfo.objects.filter(hbook__btitle='天龙八部')
```

查询图书阅读量大于30的所有英雄

```python
HeroInfo.objects.filter(hbook__bread__gt=30)
```

#### 修改

修改更新有两种方法

- save，**修改模型类对象的属性，然后执行save()方法**

  ```python
  hero = HeroInfo.objects.get(hname='猪八戒')
  hero.hname = '猪悟能'
  hero.save()
  ```

- update，**使用模型类.objects.filter().update()**，会返回受影响的行数

  ```python
  HeroInfo.objects.filter(hname='沙悟净').update(hname='沙僧')
  ```

#### 删除

删除有两种方法

- 模型类对象delete

  ```python
  hero = HeroInfo.objects.get(id=13)
  hero.delete()
  ```

- 模型类.objects.filter().delete()

  ```python
  HeroInfo.objects.filter(id=14).delete()
  ```

### 查询集 QuerySet

#### 概念

Django的ORM中存在查询集的概念。

查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。

当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：

- all()：返回所有数据。
- filter()：返回满足条件的数据。
- exclude()：返回满足条件之外的数据。
- order_by()：对结果进行排序。

对查询集可以再次调用过滤器进行过滤，如

```python
BookInfo.objects.filter(bread__gt=30).order_by('bpub_date')
```

也就意味着查询集可以含有零个、一个或多个过滤器。过滤器基于所给的参数限制查询的结果。

**从SQL的角度讲，查询集与select语句等价，过滤器像where、limit、order by子句。**

**判断某一个查询集中是否有数据**：

- exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。

#### 两大特性

##### 惰性执行

创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用

例如，当执行如下语句时，并未进行数据库查询，只是创建了一个查询集qs

```python
qs = BookInfo.objects.all()
```

继续执行遍历迭代操作后，才真正的进行了数据库的查询

```python
for book in qs:
    print(book.btitle)
```

##### 缓存

使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

**情况一**：如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。

```python
from booktest.models import BookInfo
[book.id for book in BookInfo.objects.all()]
[book.id for book in BookInfo.objects.all()]
```

**情况二**：经过存储后，可以重用查询集，第二次使用缓存中的数据。

```python
qs=BookInfo.objects.all()
[book.id for book in qs]
[book.id for book in qs]
```

#### 限制查询集

可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。

{{< admonition warning "注意" true >}}

不支持负数索引。

{{< /admonition >}}

**对查询集进行切片后返回一个新的查询集，不会立即执行查询。**

如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。

示例：获取第1、2项，运行查看。

```python
qs = BookInfo.objects.all()[0:2]
```

### 管理器Manager

#### 简介

管理器是Django的模型进行数据库操作的接口，Django应用的每个模型类都拥有至少一个管理器。

我们在通过模型类的**objects**属性提供的方法操作数据库时，即是在使用一个管理器对象objects。当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，它是**models.Manager**类的对象。

#### 自定义管理器

我们可以自定义管理器，并应用到我们的模型类上。

{{< admonition warning "注意" true >}}

一旦为模型类指明自定义的过滤器后，Django不再生成默认管理对象objects。

{{< /admonition >}}

自定义管理器类主要用于两种情况：

- 修改原始查询集，重写all()方法。
  - 打开booktest/models.py文件，定义类BookInfoManager

    ```python
    #图书管理器
    class BookInfoManager(models.Manager):
        def all(self):
            #默认查询未删除的图书信息
            #调用父类的成员语法为：super().方法名
            return super().filter(is_delete=False)
    ```
  
  - 在模型类BookInfo中定义管理器

    ```python
    class BookInfo(models.Model):
        ...
        books = BookInfoManager()
    ```

	- 使用方法

    ```python
    BookInfo.books.all()
    ```

- 在管理器类中补充定义新的方法
  - 打开booktest/models.py文件，定义方法create。

    ```python
    class BookInfoManager(models.Manager):
        #创建模型类，接收参数为属性赋值
        def create_book(self, title, pub_date):
            #创建模型类对象self.model可以获得模型类
            book = self.model()
            book.btitle = title
            book.bpub_date = pub_date
            book.bread=0
            book.bcommet=0
            book.is_delete = False
            # 将数据插入进数据表
            book.save()
            return book
    ```

	- 为模型类BookInfo定义管理器books语法如下

    ```python
    class BookInfo(models.Model):
          ...
        books = BookInfoManager()
    ```

	- 调用语法如下：

    ```python
    book=BookInfo.books.create_book("abc",date(1980,1,1))
    ```
