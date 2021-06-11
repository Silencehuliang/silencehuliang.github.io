# Python学习之路-Django基础:Admin站点




## 简介

假设我们要设计一个新闻网站，我们需要编写展示给用户的页面，网页上展示的新闻信息是从哪里来的呢？**是从数据库中查找到新闻的信息，然后把它展示在页面上**。但是我们的网站上的新闻每天都要更新，这就意味着对数据库的增、删、改、查操作，那么我们需要每天写sql语句操作数据库吗? 如果这样的话，是不是非常繁琐，所以我们可以设计一个页面，通过对这个页面的操作来实现对新闻数据库的增删改查操作。那么问题来了，老板说我们需要在建立一个新网站，是不是还要设计一个页面来实现对新网站数据库的增删改查操作，但是这样的页面具有一个很大的重复性，那有没有一种方法能够让我们很快的生成管理数据库表的页面呢？**有，那就是我们接下来要给大家讲的Django的后台管理**。Django能够根据定义的模型类自动地生成管理页面。

使用Django的管理模块，需要按照如下步骤操作：

1. 管理界面本地化
2. 创建管理员
3. 注册模型类
4. 自定义管理页面

## 使用Admin站点

### 管理界面本地化

在settings.py中设置语言和时区

```python
LANGUAGE_CODE = 'zh-hans' # 使用中国语言
TIME_ZONE = 'Asia/Shanghai' # 使用中国上海时间
```

### 创建超级管理员

创建管理员的命令如下，按提示输入用户名、邮箱、密码。

```shell
python manage.py createsuperuser
```

打开浏览器，在地址栏中输入如下地址后回车。

```html
http://127.0.0.1:8000/admin/
```

输入前面创建的用户名、密码完成登录。

登录成功后界面如下，但是并没有我们自己应用模型的入口，接下来进行第三步操作。

{{< admonition tip "提示" true >}}

如果想要修改密码可以执行`python manage.py changepassword 用户名`

{{< /admonition >}}

### App应用配置

在每个应用目录中都包含了apps.py文件，用于保存该应用的相关信息。在创建应用时，Django会向apps.py文件中写入一个该应用的配置类，如

```python
from django.apps import AppConfig

class BooktestConfig(AppConfig):
    name = 'booktest'
```

我们将此类添加到工程settings.py中的INSTALLED_APPS列表中，表明注册安装具备此配置属性的应用。

- **AppConfig.name** 属性表示这个配置类是加载到哪个应用的，每个配置类必须包含此属性，默认自动生成。

- **AppConfig.verbose_name** 属性用于设置该应用的直观可读的名字，此名字在Django提供的Admin管理站点中会显示，如

  ```python
  from django.apps import AppConfig
  
  class BooktestConfig(AppConfig):
      name = 'booktest'
      verbose_name = '图书管理'
  ```

### 注册模型类

登录后台管理后，默认没有我们创建的应用中定义的模型类，需要在自己应用中的admin.py文件中注册，才可以在后台管理中看到，并进行增删改查操作。打开booktest/admin.py文件，编写如下代码：

```python
from django.contrib import admin
from booktest.models import BookInfo,HeroInfo

admin.site.register(BookInfo)
admin.site.register(HeroInfo)
```

到浏览器中刷新页面，可以看到模型类BookInfo和HeroInfo的管理了。点击类名称"BookInfo"（图书）可以进入列表页，默认只有一列。在列表页中点击"增加"可以进入增加页，Django会根据模型类的不同，生成不同的表单控件，按提示填写表单内容后点击"保存"，完成数据创建，创建成功后返回列表页。在列表页中点击某行的第一列可以进入修改页。按照提示进行内容的修改，修改成功后进入列表页。在修改页点击“删除”可以删除一项。删除：在列表页勾选想要删除的复选框，可以删除多项。点击执行后进入确认页面，删除后回来列表页面。

### 定义与使用Admin管理类

Django提供的Admin站点的展示效果可以通过自定义**ModelAdmin**类来进行控制。

定义管理类需要继承自**admin.ModelAdmin**类，如下

```python
from django.contrib import admin

class BookInfoAdmin(admin.ModelAdmin):
    pass
```

使用管理类有两种方式：

- 注册参数

  ```python
  admin.site.register(BookInfo,BookInfoAdmin)
  ```

- 装饰器

  ```python
  @admin.register(BookInfo)
  class BookInfoAdmin(admin.ModelAdmin):
      pass
  ```

## 调整列表页展示

### 页大小

- 每页中显示多少条数据，默认为每页显示100条数据，属性如下：

  ```python
  list_per_page=100
  ```

- 打开booktest/admin.py文件，修改AreaAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      list_per_page = 2
  ```

- 在浏览器中查看区域信息的列表页面

### "操作选项"的位置

顶部显示的属性，设置为True在顶部显示，设置为False不在顶部显示，默认为True。

```python
actions_on_top=True
```

底部显示的属性，设置为True在底部显示，设置为False不在底部显示，默认为False。

```python
actions_on_bottom=False
```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      actions_on_top = True
      actions_on_bottom = True
  ```

- 在浏览器中刷新效果如下图：

### 列表中的列

- 属性如下：

  ```
  list_display=[模型字段1,模型字段2,...]
  ```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      list_display = ['id','btitle']
  ```
  
  **点击列头可以进行升序或降序排列。**

###  将方法作为列

列可以是模型字段，还可以是模型方法，要求方法有返回值。**通过设置short_description属性，可以设置在admin站点中显示的列名。**

- 打开booktest/models.py文件，修改BookInfo类如下：

  ```python
  class BookInfo(models.Model):
      ...
      def pub_date(self):
          return self.bpub_date.strftime('%Y年%m月%d日')

      pub_date.short_description = '发布日期'  # 设置方法字段在admin中显示的标题
  ```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      list_display = ['id','atitle','pub_date']
  ```

- 方法列是不能排序的，如果需要排序需要为方法指定排序依据。

  ```
  admin_order_field=模型类字段
  ```

- 打开booktest/models.py文件，修改BookInfo类如下：

  ```python
  class BookInfo(models.Model):
      ...
      def pub_date(self):
          return self.bpub_date.strftime('%Y年%m月%d日')
  
      pub_date.short_description = '发布日期'
      pub_date.admin_order_field = 'bpub_date'
  ```

  


### 关联对象

无法直接访问关联对象的属性或方法，可以在模型类中封装方法，访问关联对象的成员。

- 打开booktest/models.py文件，修改HeroInfo类如下：

  ```python
  class HeroInfo(models.Model):
      ...
      def read(self):
          return self.hbook.bread

      read.short_description = '图书阅读量'
  ```

- 打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

  ```python
  class HeroInfoAdmin(admin.ModelAdmin):
      ...
      list_display = ['id', 'hname', 'hbook', 'read']
  ```


### 右侧栏过滤器

- 属性如下，只能接收字段，会将对应字段的值列出来，用于快速过滤。一般用于有重复值的字段。

  ```
  list_filter=[]
  ```

- 打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

  ```python
  class HeroInfoAdmin(admin.ModelAdmin):
      ...
      list_filter = ['hbook', 'hgender']
  ```

### 搜索框

- 属性如下，用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。

  ```
  search_fields=[]
  ```

- 打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

  ```python
  class HeroInfoAdmin(admin.ModelAdmin):
      ...
      search_fields = ['hname']
  ```

## 调整编辑页展示

### 显示字段

- 属性如下：

  ```
  fields=[]
  ```

- 点击某行ID的链接，可以转到修改页面：

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      fields = ['btitle', 'bpub_date']
  ```

### 分组显示

- 属性如下：

  ```
  fieldset=(
      ('组1标题',{'fields':('字段1','字段2')}),
      ('组2标题',{'fields':('字段3','字段4')}),
  )
  ```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      # fields = ['btitle', 'bpub_date']
      fieldsets = (
          ('基本', {'fields': ['btitle', 'bpub_date']}),
          ('高级', {
              'fields': ['bread', 'bcomment'],
              'classes': ('collapse',)  # 是否折叠显示
          })
      )
  ```

说明：fields与fieldsets两者选一使用。

#### 3. 关联对象

在一对多的关系中，可以在一端的编辑页面中编辑多端的对象，嵌入多端对象的方式包括表格、块两种。

- 类型InlineModelAdmin：表示在模型的编辑页面嵌入关联模型的编辑。
- 子类TabularInline：以表格的形式嵌入。
- 子类StackedInline：以块的形式嵌入。

- 打开booktest/admin.py文件，创建HeroInfoStackInline类。

  ```python
  class HeroInfoStackInline(admin.StackedInline):
      model = HeroInfo  # 要编辑的对象
      extra = 1  # 附加编辑的数量
  ```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      inlines = [HeroInfoStackInline]
  ```

可以用表格的形式嵌入。

- 打开booktest/admin.py文件，创建HeroInfoTabularInline类。

  ```python
  class HeroInfoTabularInline(admin.TabularInline):
      model = HeroInfo
      extra = 1
  ```

- 打开booktest/admin.py文件，修改BookInfoAdmin类如下：

  ```python
  class BookInfoAdmin(admin.ModelAdmin):
      ...
      inlines = [HeroInfoTabularInline]
  ```

## 调整站点信息

Admin站点的名称信息也是可以自定义的。

- **admin.site.site_header** 设置网站页头
- **admin.site.site_title** 设置页面标题
- **admin.site.index_title** 设置首页标语

在booktest/admin.py文件中添加一下信息

```python
from django.contrib import admin

admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'
```

## 上传图片

### 简介

Django有提供文件系统支持，在Admin站点中可以轻松上传图片。

使用Admin站点保存图片，需要安装Python的图片操作包

```python
pip install Pillow
```

### 配置

默认情况下，Django会将上传的图片保存在本地服务器上，需要配置保存的路径。

我们可以将上传的文件保存在静态文件目录中，如我们之前设置的static_files目录中在settings.py 文件中添加如下上传保存目录信息

```python
MEDIA_ROOT=os.path.join(BASE_DIR,"static_files/media")
```

### 为模型类添加ImageField字段

我们为之前的BookInfo模型类添加一个ImageFiled

```python
class BookInfo(models.Model):
    ...
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
```

- upload_to 选项指明该字段的图片保存在MEDIA_ROOT目录中的哪个子目录

进行数据库迁移操作

```python
python manage.py makemigrations
python manage.py migrate
```

### 使用Admin站点上传图片

进入Admin站点的图书管理页面，选择一个图书，能发现多出来一个上传图片的字段

选择一张图片并保存后，图片会被保存在**static_files/media/booktest/**目录下。

在数据库中，我们能看到image字段被设置为图片的路径
