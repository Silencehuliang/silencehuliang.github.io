# Python学习之路-配置、静态文件与路由


## 配置文件

### BASE_DIR

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

当前工程的根目录，Django会依此来定位工程内的相关文件，我们也可以使用该参数来构造文件路径。

### DEBUG

调试模式，创建工程后初始值为**True**，即默认工作在调试模式下。

作用：

- 修改代码文件，程序自动重启

- Django程序出现异常时，向前端显示详细的错误追踪信息，例如

  而非调试模式下，仅返回Server Error (500)

**注意：部署线上运行的Django不要运行在调式模式下，记得修改DEBUG=False。**

### 本地语言与时区

Django支持本地化处理，即显示语言与时区支持本地化。

本地化是将显示的语言、时间等使用本地的习惯，这里的本地化就是进行中国化，中国大陆地区使用**简体中文**，时区使用**亚洲/上海**时区，注意这里不使用北京时区表示。

初始化的工程默认语言和时区为英语和UTC标准时区

```python
LANGUAGE_CODE = 'en-us'  # 语言
TIME_ZONE = 'UTC'  # 时区
```

将语言和时区修改为中国大陆信息

```python
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

## 静态文件

### 简介

项目中的CSS、图片、js都是静态文件。一般会将静态文件放到一个单独的目录中，以方便管理。在html页面中调用时，也需要指定静态文件的路径，Django中提供了一种解析的方式配置静态文件路径。静态文件可以放在项目根目录下，也可以放在应用的目录下，由于有些静态文件在项目中是通用的，所以推荐放在项目的根目录下，方便管理。

为了提供静态文件，需要配置两个参数：

- **STATICFILES_DIRS** 存放查找静态文件的目录
- **STATIC_URL** 访问静态文件的URL前缀

### 示例

在项目根目录下创建static_files目录来保存静态文件。在demo/settings.py中修改静态文件的两个参数为

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]
```

此时在static_files添加的任何静态文件都可以使用网址 **/static/文件在static_files中的路径** 来访问了。

例如，我们向static_files目录中添加一个index.html文件，在浏览器中就可以使用127.0.0.1:8000/static/index.html来访问。

或者我们在static_files目录中添加了一个子目录和文件goods/detail.html，在浏览器中就可以使用127.0.0.1:8000/static/goods/detail.html来访问。

{{< admonition warning "注意" true >}}

Django 仅在调试模式下（DEBUG=True）能对外提供静态文件。

当DEBUG=False工作在生产模式时，Django不再对外提供静态文件，需要是用collectstatic命令来收集静态文件并交由其他静态文件服务器来提供。（详细在部署时会讲）

{{< /admonition >}}

## 路由说明

### 定义位置

Django的主要路由信息定义在工程同名目录下的urls.py文件中，该文件是Django解析路由的入口。

每个子应用为了保持相对独立，可以在各个子应用中定义属于自己的urls.py来保存该应用的路由。然后用主路由文件包含各应用的子路由数据。

除了上述方式外，也可将工程的全部路由信息都定义在主路由文件中，子应用不再设置urls.py。如：

```
from django.conf.urls import url
from django.contrib import admin
import users.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/index/$', users.views.index)
]
```

### 解析顺序

Django在接收到一个请求时，从主路由文件中的urlpatterns列表中以由上至下的顺序查找对应路由规则，如果发现规则为include包含，则再进入被包含的urls中的urlpatterns列表由上至下进行查询。

值得关注的**由上至下**的顺序，有可能会使上面的路由屏蔽掉下面的路由，带来非预期结果。例如：

```python
urlpatterns = [
    url(r'^say', views.say),
    url(r'^sayhello', views.sayhello),
]
```

即使访问sayhello/路径，预期应该进入sayhello视图执行，但实际优先查找到了say路由规则也与sayhello/路径匹配，实际进入了say视图执行。

{{< admonition tip "提示" true >}}

需要注意定义路由的顺序，避免出现屏蔽效应。

{{< /admonition >}}

### 路由命名

在定义路由的时候，可以为路由命名，方便查找特定视图的具体路径信息。

- 在使用include函数定义路由时，可以使用namespace参数定义路由的命名空间，如

  ```python
  url(r'^users/', include('users.urls', namespace='users')),
  ```
  
  命名空间表示，凡是users.urls中定义的路由，均属于namespace指明的users名下。
  
  **命名空间的作用：避免不同应用中的路由使用了相同的名字发生冲突，使用命名空间区别开。**

- 在定义普通路由时，可以使用name参数指明路由的名字，如

  ```python
  urlpatterns = [
      url(r'^index/$', views.index, name='index'),
      url(r'^say', views.say, name='say'),
  ]
  ```

### reverse反解析

使用reverse函数，可以根据路由名称，返回具体的路径，如：

  ```python
  from django.urls import reverse  # 注意导包路径
  
  def index(request):
      return HttpResponse("hello the world!")
  
  def say(request):
      url = reverse('users:index')  # 返回 /users/index/
      print(url)
      return HttpResponse('say')
  ```

  对于未指明namespace的，reverse(路由name)；对于指明namespace的，reverse(命名空间namespace:路由name)


### 结尾斜线`/`的说明

Django中定义路由时，通常以斜线/结尾，其好处是用户访问不以斜线/结尾的相同路径时，Django会把用户重定向到以斜线/结尾的路径上，而不会返回404不存在。如

```python
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
]
```

用户访问 index 或者 index/ 网址，均能访问到index视图。

{{< admonition tip "说明" true >}}

虽然路由结尾带/能带来上述好处，但是却违背了HTTP中URL表示资源位置路径的设计理念。

是否结尾带/以所属公司定义风格为准。

{{< /admonition >}}


