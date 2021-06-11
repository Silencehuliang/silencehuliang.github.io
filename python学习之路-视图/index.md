# Python学习之路-DRF基础:视图


## 视图概览

### 简介

REST framework 提供了众多的通用视图基类与扩展类，以简化视图的编写。

### 视图的继承关系

![](https://tva3.sinaimg.cn/large/00729CCqgy1gq9sr8b478j34m00rsac4.jpg)

### 视图的方法与属性

![](https://tvax2.sinaimg.cn/large/00729CCqgy1gq9st71vfpj34mq43shdt.jpg)

## 视图说明

### 两个基类

#### APIView

##### 简介

`rest_framework.views.APIView`

`APIView`是REST framework提供的所有视图的基类，继承自Django的`View`父类。

`APIView`与`View`的不同之处在于：

- 传入到视图方法中的是REST framework的`Request`对象，而不是Django的`HttpRequeset`对象；
- 视图方法可以返回REST framework的`Response`对象，视图会为响应数据设置（render）符合前端要求的格式；
- 任何`APIException`异常都会被捕获到，并且处理成合适的响应信息；
- 在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。

##### 支持定义的属性

- **authentication_classes** 列表或元祖，身份认证类
- **permissoin_classes** 列表或元祖，权限检查类
- **throttle_classes** 列表或元祖，流量控制类

在`APIView`中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。

举例：

```python
from rest_framework.views import APIView
from rest_framework.response import Response

# url(r'^books/$', views.BookListView.as_view()),
class BookListView(APIView):
    def get(self, request):
        books = BookInfo.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        return Response(serializer.data)
```



#### GenericAPIView

##### 简介

`rest_framework.generics.GenericAPIView`

继承自`APIVIew`，增加了对于列表视图和详情视图可能用到的通用支持方法。通常使用时，可搭配一个或多个Mixin扩展类。

##### 支持定义的属性

- 列表视图与详情视图通用：
  - **queryset** 列表视图的查询集
  - **serializer_class** 视图使用的序列化器
- 列表视图使用：
  - **pagination_class** 分页控制类
  - **filter_backends** 过滤控制后端
- 详情页视图使用：
  - **lookup_field** 查询单一数据库对象时使用的条件字段，默认为'`pk`'
  - **lookup_url_kwarg** 查询单一数据时URL中的参数关键字名称，默认与**look_field**相同

##### 提供的方法

- 列表视图与详情视图通用：

  - **get_queryset(self)**

    返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回`queryset`属性，可以重写，例如：

    ```python
    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()
    ```

  - **get_serializer_class(self)**

    返回序列化器类，默认返回`serializer_class`，可以重写，例如：

    ```python
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullAccountSerializer
        return BasicAccountSerializer
    ```

  - ##### get_serializer(self, *args, **kwargs)

    返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。

    **注意，在提供序列化器对象的时候，REST framework会向对象的context属性补充三个数据：request、format、view，这三个数据对象可以在定义序列化器时使用。**

- 详情视图使用：

  - **get_object(self)** 返回详情视图所需的模型类数据对象，默认使用`lookup_field`参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。

    **若详情访问的模型类对象不存在，会返回404。**

    **该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问。**

### 五个扩展类

#### ListModelMixin

##### 简介

列表视图扩展类，提供`list(request, *args, **kwargs)`方法快速实现列表视图，返回200状态码。

该Mixin的list方法会对数据进行过滤和分页。

##### 源代码

```python
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

#### CreateModelMixin

##### 简介

创建视图扩展类，提供`create(request, *args, **kwargs)`方法快速实现创建资源的视图，成功返回201状态码。

如果序列化器对前端发送的数据验证失败，返回400错误。

##### 源代码

```python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # 获取序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

#### RetrieveModelMixin

##### 简介

详情视图扩展类，提供`retrieve(request, *args, **kwargs)`方法，可以快速实现返回一个存在的数据对象。如果存在，返回200， 否则返回404。

##### 源代码

```python
class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        # 获取对象，会检查对象的权限
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

#### UpdateModelMixin

##### 简介

更新视图扩展类，提供`update(request, *args, **kwargs)`方法，可以快速实现更新一个存在的数据对象。

同时也提供`partial_update(request, *args, **kwargs)`方法，可以实现局部更新。

成功返回200，序列化器校验数据失败时，返回400错误。

##### 源代码

```python
class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```

#### DestroyModelMixin

##### 简介

删除视图扩展类，提供`destroy(request, *args, **kwargs)`方法，可以快速实现删除一个存在的数据对象。成功返回204，不存在返回404。

##### 源代码

```python
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```

### 几个可用子类视图

#### CreateAPIView

##### 说明

提供 post 方法，继承自： GenericAPIView、CreateModelMixin

#### ListAPIView

提供 get 方法，继承自：GenericAPIView、ListModelMixin

#### RetireveAPIView

提供 get 方法，继承自: GenericAPIView、RetrieveModelMixin

#### DestoryAPIView

提供 delete 方法，继承自：GenericAPIView、DestoryModelMixin

#### UpdateAPIView

提供 put 和 patch 方法，继承自：GenericAPIView、UpdateModelMixin

#### RetrieveUpdateAPIView

提供 get、put、patch方法，继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

#### RetrieveUpdateDestoryAPIView

提供 get、put、patch、delete方法，继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin

## 视图集ViewSet

### 简介

使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：

- list() 提供一组数据
- retrieve() 提供单个数据
- create() 创建数据
- update() 保存数据
- destory() 删除数据

ViewSet视图集类不再实现get()、post()等方法，而是实现动作 **action** 如 list() 、create() 等。

视图集只在使用as_view()方法的时候，才会将**action**动作与具体请求方式对应上。如：

```python
class BookInfoViewSet(viewsets.ViewSet):

    def list(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...
```

在设置路由时，我们可以如下操作

```python
urlpatterns = [
    url(r'^books/$', BookInfoViewSet.as_view({'get':'list'}),
    url(r'^books/(?P<pk>\d+)/$', BookInfoViewSet.as_view({'get': 'retrieve'})
]
```

### action属性

在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。

例如：

```python
def get_serializer_class(self):
    if self.action == 'create':
        return OrderCommitSerializer
    else:
        return OrderDataSerializer
```

### 常用视图集父类

#### ViewSet

继承自`APIView`，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等。

在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。

#### GenericViewSet

继承自`GenericAPIView`，作用也与GenericAPIVIew类似，提供了get_object、get_queryset等方法便于列表视图与详情信息视图的开发。

#### ModelViewSet

继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin。

#### ReadOnlyModelViewSet

继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin。

### 视图集中定义附加action动作

在视图集中，除了上述默认的方法动作外，还可以添加自定义动作。

添加自定义动作需要使用`rest_framework.decorators.action`装饰器。

以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。

action装饰器可以接收两个参数：

- **methods**: 该action支持的请求方式，列表传递

- detail

  : 表示是action中要处理的是否是视图资源的对象（即是否通过url路径获取主键）

  - True 表示使用通过URL获取的主键对应的数据对象
  - False 表示不使用URL获取主键

## 路由Routers

### 简介

对于视图集ViewSet，我们除了可以自己手动指明请求方式与动作action之间的对应关系外，还可以使用Routers来帮助我们快速实现路由信息。

REST framework提供了两个router

- **SimpleRouter**
- **DefaultRouter**

### 使用方法

- 创建router对象，并注册视图集，例如

  ```python
  from rest_framework import routers

  router = routers.SimpleRouter()
  router.register(r'books', BookInfoViewSet, base_name='book')
  ```

  register(prefix, viewset, base_name)

  - prefix 该视图集的路由前缀
  - viewset 视图集
  - base_name 路由名称的前缀

  如上述代码会形成的路由如下：

  ```python
  ^books/$    name: book-list
  ^books/{pk}/$   name: book-detail
  ```

- 添加路由数据，可以有两种方式：

  ```python
  urlpatterns = [
      ...
  ]
  urlpatterns += router.urls
  ```

	或

  ```python
  urlpatterns = [
      ...
      url(r'^', include(router.urls))
  ]
  ```

### 视图集中包含附加action的

```python
class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    @action(methods=['get'], detail=False)
    def latest(self, request):
        ...

    @action(methods=['put'], detail=True)
    def read(self, request, pk):
        ...
```

此视图集会形成的路由：

```python
^books/latest/$    name: book-latest
^books/{pk}/read/$  name: book-read
```

### 路由router形成URL的方式

1） SimpleRouter

![SimpleRouter](https://tvax1.sinaimg.cn/large/00729CCqgy1gq9tfy4swej31940gwdj7.jpg)

2）DefaultRouter

![DefaultRouter](https://tvax3.sinaimg.cn/large/00729CCqgy1gq9tgjblz9j318y0j4wii.jpg)

DefaultRouter与SimpleRouter的区别是，DefaultRouter会多附带一个默认的API根视图，返回一个包含所有列表视图的超链接响应数据。



## Request 

### 简介

REST framework 传入视图的request对象不再是Django默认的HttpRequest对象，而是REST framework提供的扩展了HttpRequest类的**Request**类的对象。

REST framework 提供了**Parser**解析器，在接收到请求后会自动根据Content-Type指明的请求数据类型（如JSON、表单等）将请求数据进行parse解析，解析为类字典对象保存到**Request**对象中。

**Request对象的数据是自动根据前端发送数据的格式进行解析之后的结果。**

无论前端发送的哪种格式的数据，我们都可以以统一的方式读取数据。

### 常用属性

- .data：`request.data` 返回解析之后的请求体数据。类似于Django中标准的`request.POST`和 `request.FILES`属性，但提供如下特性：

  - 包含了解析之后的文件和非文件数据
  - 包含了对POST、PUT、PATCH请求方式解析后的数据
  - 利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据

- .query_params：`request.query_params`与Django标准的`request.GET`相同，只是更换了更正确的名称而已。

## Response

### 简介

```
rest_framework.response.Response
```

REST framework提供了一个响应类`Response`，使用该类构造响应对象时，响应的具体数据内容会被转换（render渲染）成符合前端需求的类型。

REST framework提供了`Renderer` 渲染器，用来根据请求头中的`Accept`（接收数据类型声明）来自动转换响应数据到对应格式。如果前端请求中未进行Accept声明，则会采用默认方式处理响应数据，我们可以通过配置来修改默认响应格式。

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
    )
}
```

### 构造方式

```python
Response(data, status=None, template_name=None, headers=None, content_type=None)
```

`data`数据不要是render处理之后的数据，只需传递python的内建类型数据即可，REST framework会使用`renderer`渲染器处理`data`。

`data`不能是复杂结构的数据，如Django的模型类对象，对于这样的数据我们可以使用`Serializer`序列化器序列化处理后（转为了Python字典类型）再传递给`data`参数。

参数说明：

- `data`: 为响应准备的序列化处理后的数据；
- `status`: 状态码，默认200；
- `template_name`: 模板名称，如果使用`HTMLRenderer` 时需指明；
- `headers`: 用于存放响应头信息的字典；
- `content_type`: 响应数据的Content-Type，通常此参数无需传递，REST framework会根据前端所需类型数据来设置该参数。

### 常用属性

- .data：传给response对象的序列化后，但尚未render处理的数据

- .status_code：状态码的数字

- .content：经过render处理后的响应数据

## 状态码

### 简介

为了方便设置状态码，REST framewrok在`rest_framework.status`模块中提供了常用状态码常量。

### 常见状态码

#### 信息告知

```python
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
```

#### 成功

```python
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS
```

#### 重定向

```python
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT
```

#### 客户端错误

```python
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
```

#### 服务器错误

```python
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_507_INSUFFICIENT_STORAGE
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
```


