# Python学习之路-DRF工程搭建


## 环境安装与配置

DRF需要以下依赖：

- Python (2.7, 3.2, 3.3, 3.4, 3.5, 3.6)
- Django (1.10, 1.11, 2.0)

**DRF是以Django扩展应用的方式提供的，所以我们可以直接利用已有的Django环境而无需从新创建。（若没有Django环境，需要先创建环境安装Django）**

### 安装DRF

```shell
pip install djangorestframework
```

### 添加rest_framework应用

我们利用在Django框架学习中创建的demo工程，在**settings.py**的**INSTALLED_APPS**中添加'rest_framework'。

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

接下来就可以使用DRF进行开发了。

## 见识DRF的魅力

我们仍以在学习Django框架时使用的图书英雄为案例，使用Django REST framework快速实现图书的REST API。

### 创建序列化器

在booktest应用中新建serializers.py用于保存该应用的序列化器。

创建一个BookInfoSerializer用于序列化与反序列化。

```python
class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo
        fields = '__all__'
```

- **model** 指明该序列化器处理的数据字段从模型类BookInfo参考生成
- **fields** 指明该序列化器包含模型类中的哪些字段，'__all__'指明包含所有字段

### 编写视图

在booktest应用的views.py中创建视图BookInfoViewSet，这是一个视图集合。

```python
from rest_framework.viewsets import ModelViewSet
from .serializers import BookInfoSerializer
from .models import BookInfo

class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
```

- **queryset** 指明该视图集在查询数据时使用的查询集
- **serializer_class** 指明该视图在进行序列化或反序列化时使用的序列化器

### 定义路由

在booktest应用的urls.py中定义路由信息。

```python
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    ...
]

router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'books', views.BookInfoViewSet)  # 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
```

### 运行测试

运行当前程序（与运行Django一样）

```shell
python manage.py runserver
```

在浏览器中输入网址127.0.0.1:8000，可以看到DRF提供的API Web浏览页面：

1）点击链接127.0.0.1:8000/books/ 可以访问**获取所有数据的接口**，呈现如下页面：

2）在页面底下表单部分填写图书信息，可以访问**添加新图书的接口**，保存新书：

点击POST后，返回如下页面信息：

3）在浏览器中输入网址127.0.0.1:8000/books/1/，可以访问**获取单一图书信息的接口**（id为1的图书），呈现如下页面：

4）在页面底部表单中填写图书信息，可以访问**修改图书的接口**：

点击PUT，返回如下页面信息：

5）点击DELETE按钮，可以访问**删除图书的接口**：

返回，如下页面：

至此，是不是发现Django REST framework很好用！
