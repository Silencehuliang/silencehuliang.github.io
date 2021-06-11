# Python学习之路-DRF基础:Serializer序列化器


## 序列化器的作用

- 进行数据的校验

- 对数据对象进行转换

## 定义Serializer

### 定义方法

Django REST framework中的Serializer使用类来定义，须继承自rest_framework.serializers.Serializer。

例如，我们已有了一个数据库模型类BookInfo

```python
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期', null=True)
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
```

我们想为这个模型类提供一个序列化器，可以定义如下：

```python
class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
```

**注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。**serializer是独立于数据库之外的存在。

### 字段与选项

#### 常用字段类型

|          字段           |                         字段构造方式                         |
| :---------------------: | :----------------------------------------------------------: |
|    **BooleanField**     |                        BooleanField()                        |
|  **NullBooleanField**   |                      NullBooleanField()                      |
|      **CharField**      | CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True) |
|     **EmailField**      | EmailField(max_length=None, min_length=None, allow_blank=False) |
|     **RegexField**      | RegexField(regex, max_length=None, min_length=None, allow_blank=False) |
|      **SlugField**      | SlugField(max*length=50, min_length=None, allow_blank=False) 正则字段，验证正则模式 [a-zA-Z0-9*-]+ |
|      **URLField**       | URLField(max_length=200, min_length=None, allow_blank=False) |
|      **UUIDField**      | UUIDField(format='hex_verbose') format: 1) `'hex_verbose'` 如`"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` 2） `'hex'` 如 `"5ce0e9a55ffa654bcee01238041fb31a"` 3）`'int'` - 如: `"123456789012312313134124512351145145114"` 4）`'urn'` 如: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"` |
|   **IPAddressField**    | IPAddressField(protocol='both', unpack_ipv4=False, **options) |
|    **IntegerField**     |         IntegerField(max_value=None, min_value=None)         |
|     **FloatField**      |          FloatField(max_value=None, min_value=None)          |
|    **DecimalField**     | DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None) max_digits: 最多位数 decimal_palces: 小数点位置 |
|    **DateTimeField**    | DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None) |
|      **DateField**      | DateField(format=api_settings.DATE_FORMAT, input_formats=None) |
|      **TimeField**      | TimeField(format=api_settings.TIME_FORMAT, input_formats=None) |
|    **DurationField**    |                       DurationField()                        |
|     **ChoiceField**     |        ChoiceField(choices) choices与Django的用法相同        |
| **MultipleChoiceField** |                 MultipleChoiceField(choices)                 |
|      **FileField**      | FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
|     **ImageField**      | ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL) |
|      **ListField**      |     ListField(child=, min_length=None, max_length=None)      |
|      **DictField**      |                      DictField(child=)                       |

#### 选项参数

|      参数名称       |       作用       |
| :-----------------: | :--------------: |
|   **max_length**    |     最大长度     |
|   **min_lenght**    |     最小长度     |
|   **allow_blank**   |   是否允许为空   |
| **trim_whitespace** | 是否截断空白字符 |
|    **max_value**    |      最小值      |
|    **min_value**    |      最大值      |

#### 通用参数

|      参数名称      |                     说明                      |
| :----------------: | :-------------------------------------------: |
|   **read_only**    |     表明该字段仅用于序列化输出，默认False     |
|   **write_only**   |    表明该字段仅用于反序列化输入，默认False    |
|    **required**    |   表明该字段在反序列化时必须输入，默认True    |
|    **default**     |            反序列化时使用的默认值             |
|   **allow_null**   |     表明该字段是否允许传入None，默认False     |
|   **validators**   |              该字段使用的验证器               |
| **error_messages** |         包含错误编号与错误信息的字典          |
|     **label**      |     用于HTML展示API页面时，显示的字段名称     |
|   **help_text**    | 用于HTML展示API页面时，显示的字段帮助提示信息 |

### 创建Serializer对象

定义好Serializer类后，就可以创建Serializer对象了。

Serializer的构造方法为：

```python
Serializer(instance=None, data=empty, **kwarg)
```

说明：

1）用于序列化时，将模型类对象传入**instance**参数

2）用于反序列化时，将要被反序列化的数据传入**data**参数

3）除了instance和data参数外，在构造Serializer对象时，还可通过**context**参数额外添加数据，如

```python
serializer = AccountSerializer(account, context={'request': request})
```

**通过context参数附加的数据，可以通过Serializer对象的context属性获取。**

## 序列化使用

### 简介

我们在django shell中来学习序列化器的使用。

```shell
python manage.py shell
```

### 基本使用

- 先查询出一个图书对象

  ```python
  from booktest.models import BookInfo

  book = BookInfo.objects.get(id=2)
  ```

- 构造序列化器对象

  ```python
  from booktest.serializers import BookInfoSerializer

  serializer = BookInfoSerializer(book)
  ```

- 获取序列化数据，通过data属性可以获取序列化后的数据

  ```python
  serializer.data
  # {'id': 2, 'btitle': '天龙八部', 'bpub_date': '1986-07-24', 'bread': 36, 'bcomment': 40, 'image': None}
  ```

- 如果要被序列化的是包含多条数据的查询集QuerySet，可以通过添加**many=True**参数补充说明

  ```python
  book_qs = BookInfo.objects.all()
  serializer = BookInfoSerializer(book_qs, many=True)
  serializer.data
  # [OrderedDict([('id', 2), ('btitle', '天龙八部'), ('bpub_date', '1986-07-24'), ('bread', 36), ('bcomment', 40), ('image', N]), OrderedDict([('id', 3), ('btitle', '笑傲江湖'), ('bpub_date', '1995-12-24'), ('bread', 20), ('bcomment', 80), ('image'ne)]), OrderedDict([('id', 4), ('btitle', '雪山飞狐'), ('bpub_date', '1987-11-11'), ('bread', 58), ('bcomment', 24), ('ima None)]), OrderedDict([('id', 5), ('btitle', '西游记'), ('bpub_date', '1988-01-01'), ('bread', 10), ('bcomment', 10), ('im', 'booktest/xiyouji.png')])]
  ```

### 关联对象嵌套序列化

如果需要序列化的数据中包含有其他关联对象，则对关联对象数据的序列化需要指明。

例如，在定义英雄数据的序列化器时，外键hbook（即所属的图书）字段如何序列化？

我们先定义HeroInfoSerialzier除外键字段外的其他部分

```python
class HeroInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20)
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
```

对于关联字段，可以采用以下几种方式：

- PrimaryKeyRelatedField，此字段将被序列化为关联对象的主键。

  ```python
  hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
  或
  hbook = serializers.PrimaryKeyRelatedField(label='图书', queryset=BookInfo.objects.all())
  ```

  指明字段时需要包含read_only=True或者queryset参数：

  - 包含read_only=True参数时，该字段将不能用作反序列化使用
  - 包含queryset参数时，将被用作反序列化时参数校验使用

  使用效果：

  ```python
  from booktest.serializers import HeroInfoSerializer
  from booktest.models import HeroInfo
  hero = HeroInfo.objects.get(id=6)
  serializer = HeroInfoSerializer(hero)
  serializer.data
  # {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 2}
  ```

- StringRelatedField，此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）

  ```python
  hbook = serializers.StringRelatedField(label='图书')
  ```

  使用效果

  ```python
  {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': '天龙八部'}
  ```

- HyperlinkedRelatedField，此字段将被序列化为获取关联对象数据的接口链接

  ```python
  hbook = serializers.HyperlinkedRelatedField(label='图书', read_only=True, view_name='books-detail')
  ```

	必须指明view_name参数，以便DRF根据视图名称寻找路由，进而拼接成完整URL。

	使用效果

  ```python
  {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 'http://127.0.0.1:8000/books/2/'}
  ```

	我们暂时还没有定义视图，此方式不再演示。

- SlugRelatedField，此字段将被序列化为关联对象的指定字段数据

  ```python
  hbook = serializers.SlugRelatedField(label='图书', read_only=True, slug_field='bpub_date')
  ```

	slug_field指明使用关联对象的哪个字段，使用效果

  ```python
  {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': datetime.date(1986, 7, 24)}
  ```

- 使用关联对象的序列化器

  ```python
  hbook = BookInfoSerializer()
  ```

	使用效果

  ```python
  {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': OrderedDict([('id', 2), ('btitle', '天龙八部')te', '1986-07-24'), ('bread', 36), ('bcomment', 40), ('image', None)])}
  ```

- 重写to_representation方法

  序列化器的每个字段实际都是由该字段类型的to_representation方法决定格式的，可以通过重写该方法来决定格式。

  **注意，to_representations方法不仅局限在控制关联对象格式上，适用于各个序列化器字段类型。**

	自定义一个新的关联字段：

  ```python
  class BookRelateField(serializers.RelatedField):
      """自定义用于处理图书的字段"""
      def to_representation(self, value):
          return 'Book: %d %s' % (value.id, value.btitle)
  ```

	指明hbook为BookRelateField类型

  ```python
  hbook = BookRelateField(read_only=True)
  ```

  使用效果

  ```python
  {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 'Book: 2 天龙八部'}
  ```

### many参数

如果关联的对象数据不是只有一个，而是包含多个数据，如想序列化图书BookInfo数据，每个BookInfo对象关联的英雄HeroInfo对象可能有多个，此时关联字段类型的指明仍可使用上述几种方式，只是在声明关联字段时，多补充一个many=True参数即可。

此处仅拿PrimaryKeyRelatedField类型来举例，其他相同。

在BookInfoSerializer中添加关联字段：

```python
class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 新增
```

使用效果：

```python
from booktest.serializers import BookInfoSerializer
from booktest.models import BookInfo
book = BookInfo.objects.get(id=2)
serializer = BookInfoSerializer(book)
serializer.data
# {'id': 2, 'btitle': '天龙八部', 'bpub_date': '1986-07-24', 'bread': 36, 'bcomment': 40, 'image': None, 'heroinfo_set': [6,8, 9]}
```

## 反序列化使用

### 验证

使用序列化器进行反序列化时，需要对数据进行验证后，才能获取验证成功的数据或保存成模型类对象。

在获取反序列化的数据前，必须调用**is_valid()**方法进行验证，验证成功返回True，否则返回False。

验证失败，可以通过序列化器对象的**errors**属性获取错误信息，返回字典，包含了字段和字段的错误。如果是非字段错误，可以通过修改REST framework配置中的**NON_FIELD_ERRORS_KEY**来控制错误字典中的键名。

验证成功，可以通过序列化器对象的**validated_data**属性获取数据。

在定义序列化器时，指明每个字段的序列化类型和选项参数，本身就是一种验证行为。

如我们前面定义过的BookInfoSerializer

```python
class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
```

通过构造序列化器对象，并将要反序列化的数据传递给data构造参数，进而进行验证

```python
from booktest.serializers import BookInfoSerializer
data = {'bpub_date': 123}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # 返回False
serializer.errors
# {'btitle': [ErrorDetail(string='This field is required.', code='required')], 'bpub_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].', code='invalid')]}
serializer.validated_data  # {}

data = {'btitle': 'python'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # True
serializer.errors  # {}
serializer.validated_data  #  OrderedDict([('btitle', 'python')])
```

is_valid()方法还可以在验证失败时抛出异常serializers.ValidationError，可以通过传递**raise_exception=True**参数开启，REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

如果觉得这些还不够，需要再补充定义验证行为，可以使用以下三种方法：

- `validate_<field_name>`，对`<field_name>`字段进行验证，如

  ```python
  class BookInfoSerializer(serializers.Serializer):
      """图书数据序列化器"""
      ...

      def validate_btitle(self, value):
          if 'django' not in value.lower():
              raise serializers.ValidationError("图书不是关于Django的")
          return value
  ```

	测试

  ```python
  from booktest.serializers import BookInfoSerializer
  data = {'btitle': 'python'}
  serializer = BookInfoSerializer(data=data)
  serializer.is_valid()  # False   
  serializer.errors
  #  {'btitle': [ErrorDetail(string='图书不是关于Django的', code='invalid')]}
  ```

- validate，在序列化器中需要同时对多个字段进行比较验证时，可以定义validate方法来验证，如

  ```python
  class BookInfoSerializer(serializers.Serializer):
      """图书数据序列化器"""
      ...

      def validate(self, attrs):
          bread = attrs['bread']
          bcomment = attrs['bcomment']
          if bread < bcomment:
              raise serializers.ValidationError('阅读量小于评论量')
          return attrs
  ```

	测试

  ```python
  from booktest.serializers import BookInfoSerializer
  data = {'btitle': 'about django', 'bread': 10, 'bcomment': 20}
  s = BookInfoSerializer(data=data)
  s.is_valid()  # False
  s.errors
  #  {'non_field_errors': [ErrorDetail(string='阅读量小于评论量', code='invalid')]}
  ```

- validators，在字段中添加validators选项参数，也可以补充验证行为，如

  ```python
  def about_django(value):
      if 'django' not in value.lower():
          raise serializers.ValidationError("图书不是关于Django的")

  class BookInfoSerializer(serializers.Serializer):
      """图书数据序列化器"""
      id = serializers.IntegerField(label='ID', read_only=True)
      btitle = serializers.CharField(label='名称', max_length=20, validators=[about_django])
      bpub_date = serializers.DateField(label='发布日期', required=False)
      bread = serializers.IntegerField(label='阅读量', required=False)
      bcomment = serializers.IntegerField(label='评论量', required=False)
      image = serializers.ImageField(label='图片', required=False)
  ```

  测试：

  ```python
  from booktest.serializers import BookInfoSerializer
  data = {'btitle': 'python'}
  serializer = BookInfoSerializer(data=data)
  serializer.is_valid()  # False   
  serializer.errors
  #  {'btitle': [ErrorDetail(string='图书不是关于Django的', code='invalid')]}
  ```

REST framework提供的validators:

- UniqueValidator

  单字段唯一，如

  ```python
  from rest_framework.validators import UniqueValidator
  
  slug = SlugField(
      max_length=100,
      validators=[UniqueValidator(queryset=BlogPost.objects.all())]
  )
  ```

- UniqueTogetherValidation

  联合唯一，如

  ```python
  from rest_framework.validators import UniqueTogetherValidator
  
  class ExampleSerializer(serializers.Serializer):
      # ...
      class Meta:
          validators = [
              UniqueTogetherValidator(
                  queryset=ToDoItem.objects.all(),
                  fields=('list', 'position')
              )
          ]
  ```

### 保存

如果在验证成功后，想要基于validated_data完成数据对象的创建，可以通过实现create()和update()两个方法来实现。

```python
class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def create(self, validated_data):
        """新建"""
        return BookInfo(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        return instance
```

如果需要在返回数据对象的时候，也将数据保存到数据库中，则可以进行如下修改

```python
class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def create(self, validated_data):
        """新建"""
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance
```

实现了上述两个方法后，在反序列化数据的时候，就可以通过save()方法返回一个数据对象实例了

```python
book = serializer.save()
```

如果创建序列化器对象的时候，没有传递instance实例，则调用save()方法的时候，create()被调用，相反，如果传递了instance实例，则调用save()方法的时候，update()被调用。

```python
from db.serializers import BookInfoSerializer
data = {'btitle': '封神演义'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # True
serializer.save()  # <BookInfo: 封神演义>

from db.models import BookInfo
book = BookInfo.objects.get(id=2)
data = {'btitle': '倚天剑'}
serializer = BookInfoSerializer(book, data=data)
serializer.is_valid()  # True
serializer.save()  # <BookInfo: 倚天剑>
book.btitle  # '倚天剑'
```

### 两点说明

- 在对序列化器进行save()保存时，可以额外传递数据，这些数据可以在create()和update()中的validated_data参数获取到

  ```python
  serializer.save(owner=request.user)
  ```

- 默认序列化器必须传递所有required的字段，否则会抛出验证异常。但是我们可以使用partial参数来允许部分字段更新

  ```python
  # Update `comment` with partial data
  serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)
  ```

## 模型类序列化器ModelSerializer

### 简介

如果我们想要使用序列化器对应的是Django的模型类，DRF为我们提供了ModelSerializer模型类序列化器来帮助我们快速创建一个Serializer类。

ModelSerializer与常规的Serializer相同，但提供了：

- 基于模型类自动生成一系列字段
- 基于模型类自动为Serializer生成validators，比如unique_together
- 包含默认的create()和update()的实现

### 定义

比如我们创建一个BookInfoSerializer

```python
class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo
        fields = '__all__'
```

- model 指明参照哪个模型类
- fields 指明为模型类的哪些字段生成

我们可以在python manage.py shell中查看自动生成的BookInfoSerializer的具体实现

```python
>>> from booktest.serializers import BookInfoSerializer
>>> serializer = BookInfoSerializer()
>>> serializer
BookInfoSerializer():
    id = IntegerField(label='ID', read_only=True)
    btitle = CharField(label='名称', max_length=20)
    bpub_date = DateField(allow_null=True, label='发布日期', required=False)
    bread = IntegerField(label='阅读量', max_value=2147483647, min_value=-2147483648, required=False)
    bcomment = IntegerField(label='评论量', max_value=2147483647, min_value=-2147483648, required=False)
    image = ImageField(allow_null=True, label='图片', max_length=100, required=False)
```

### 指定字段

- 使用**fields**来明确字段，`__all__`表名包含所有字段，也可以写明具体哪些字段，如

  ```python
  class BookInfoSerializer(serializers.ModelSerializer):
      """图书数据序列化器"""
      class Meta:
          model = BookInfo
          fields = ('id', 'btitle', 'bpub_date')
  ```

- 使用**exclude**可以明确排除掉哪些字段

  ```python
  class BookInfoSerializer(serializers.ModelSerializer):
      """图书数据序列化器"""
      class Meta:
          model = BookInfo
          exclude = ('image',)
  ```

- 默认ModelSerializer使用主键作为关联字段，但是我们可以使用**depth**来简单的生成嵌套表示，depth应该是整数，表明嵌套的层级数量。如：

  ```python
  class HeroInfoSerializer2(serializers.ModelSerializer):
      class Meta:
          model = HeroInfo
          fields = '__all__'
          depth = 1
  ```

	形成的序列化器如下：

  ```python
  HeroInfoSerializer():
      id = IntegerField(label='ID', read_only=True)
      hname = CharField(label='名称', max_length=20)
      hgender = ChoiceField(choices=((0, 'male'), (1, 'female')), label='性别', required=False, validators=[<django.core.valators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
      hcomment = CharField(allow_null=True, label='描述信息', max_length=200, required=False)
      hbook = NestedSerializer(read_only=True):
          id = IntegerField(label='ID', read_only=True)
          btitle = CharField(label='名称', max_length=20)
          bpub_date = DateField(allow_null=True, label='发布日期', required=False)
          bread = IntegerField(label='阅读量', max_value=2147483647, min_value=-2147483648, required=False)
          bcomment = IntegerField(label='评论量', max_value=2147483647, min_value=-2147483648, required=False)
          image = ImageField(allow_null=True, label='图片', max_length=100, required=False)
  ```

- 显示指明字段，如：

  ```python
  class HeroInfoSerializer(serializers.ModelSerializer):
      hbook = BookInfoSerializer()

      class Meta:
          model = HeroInfo
          fields = ('id', 'hname', 'hgender', 'hcomment', 'hbook')
  ```

- 指明只读字段，可以通过**read_only_fields**指明只读字段，即仅用于序列化输出的字段

  ```python
  class BookInfoSerializer(serializers.ModelSerializer):
      """图书数据序列化器"""
      class Meta:
          model = BookInfo
          fields = ('id', 'btitle', 'bpub_date'， 'bread', 'bcomment')
          read_only_fields = ('id', 'bread', 'bcomment')
  ```

### 添加额外参数

我们可以使用**extra_kwargs**参数为ModelSerializer添加或修改原有的选项参数

```python
class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo
        fields = ('id', 'btitle', 'bpub_date', 'bread', 'bcomment')
        extra_kwargs = {
            'bread': {'min_value': 0, 'required': True},
            'bcomment': {'min_value': 0, 'required': True},
        }

# BookInfoSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    btitle = CharField(label='名称', max_length=20)
#    bpub_date = DateField(allow_null=True, label='发布日期', required=False)
#    bread = IntegerField(label='阅读量', max_value=2147483647, min_value=0, required=True)
#    bcomment = IntegerField(label='评论量', max_value=2147483647, min_value=0, required=True)
```
