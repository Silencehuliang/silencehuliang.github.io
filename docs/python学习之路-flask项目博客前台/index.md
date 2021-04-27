# Python学习之路-Flask项目:博客前台


## 前言

前一篇完成了项目开发前的所有准备工作，本篇将完成整个博客的前台相关工作。

## 首页

### 前言

首页主要为我们提供各个分类入口已经按时间顺序的文章列表和列表排行等数据，是进入博客中第一眼看到的，接下来就来实现吧。

### 排行展示

#### 前言

在请求根路由时去数据库查询按点击量排行的10条文章

#### 后端实现

```python
@index_blu.route('/')
def index():
    ...
    # 获取点击排行数据
    blog_list = None
    try:
        blog_list = Blog.query.order_by(Blog.clicks.desc()).limit(constants.CLICK_RANK_MAX_BLOG)
    except Exception as e:
        current_app.logger.error(e)

    click_blog_list = []
    for blog in blog_list if blog_list else []:
        click_blog_list.append(blog.to_basic_dict())

    data = {
        "user_blog": user.to_dict() if user else None,
        "click_blog_list": click_blog_list,
    }

    return render_template('blog/index.html', data=data)
```

### 分类展示

#### 前言

分类展示是将博客按我们想要的分类进行分割的一个关键部分，需要我们通过分类将其展示出来。

#### 后端实现

在请求根路由的时候去查询博客分类，并默认设置第1个分类选中

```python
@index_blu.route('/')
def index():
    ...
    # 获取博客分类数据
    categories = Category.query.all()
    # 定义列表保存分类数据
    categories_dicts = []

    for category in enumerate(categories):
        # 拼接内容
        categories_dicts.append(category.to_dict())

    data = {
        "user_blog": user.to_dict() if user else None,
        "click_blog_list": click_blog_list,
        "categories": categories_dicts
    }
    return render_template('blog/index.html', data=data)
```

### 文章列表

#### 前言

文章列表是整个博客最重要的一部分，当我们点击分类时需要去获取当前分类下的文章数据，当我们点击标签时需要去获取当前标签下的文章数据。在展示的时候需要更新文章列表界面，不需要整体页面刷新，所以文章数据也使用 ajax 的方式去请求后台接口进行获取。

#### 接口设计

- URL：/blog_list
- 请求方式：GET
- 传入参数：JSON格式
- 参数

|  参数名  |  类型  | 是否必须 |              参数说明              |
| :------: | :----: | :------: | :--------------------------------: |
|   cid    | string |    是    |               分类id               |
|   page   |  int   |    否    |       页数，不传即获取第1页        |
| per_page |  int   |    否    | 每页多少条数据，如果不传，默认10条 |

- 返回类型：JSON

|          参数名          |  类型  | 是否必须 |       参数说明       |
| :----------------------: | :----: | :------: | :------------------: |
|          errno           |  int   |    是    |        错误码        |
|          errmsg          | string |    是    |       错误信息       |
|           cid            | string |    是    | 当前文章数据的分类id |
|        totalPage         |  int   |    否    |        总页数        |
|       currentPage        |  int   |    否    |       当前页数       |
|         blogList         |  list  |    否    |       列表数据       |
|      blogList.title      | string |    是    |         标题         |
|     blogList.source      | string |    是    |         来源         |
|     blogList.digest      | string |    是    |         摘要         |
|   blogList.create_time   | string |    是    |         时间         |
| blogList.index_image_url | string |    是    |        索引图        |

- 返回示例：

```json
{
    "cid": "0",
    "currentPage": 1,
    "errmsg": "OK",
    "errno": "0",
    "blogList": [
        {
            "clicks": 105,
            "create_time": "2020-06-13 06:51:31",
            "digest": "前面几篇学习了`Flask`的基础知识，从今天开始开发一个个人博客项目来练练手。",
            "id": 54,
            "index_image_url": "https://tvax1.sinaimg.cn/large/00729CCqgy1gp1q41no6dj306k0a9q35.jpg",
            "source": "Silence",
            "status": 0,
            "title": "Python学习之路-Flask项目:开发准备"
        },
        {
            "clicks": 99,
            "create_time": "2020-05-30 07:21:55",
            "digest": "`ORM`全拼`Object-Relation Mapping`，中文意为 `对象-关系映射`。主要实现模型对象到关系数据库数据的映射.",
            "id": 53,
            "index_image_url": "https://tva4.sinaimg.cn/large/00729CCqgy1gp1qfrpi14j305k05k745.jpg",
            "source": "Silence",
            "status": 0,
            "title": "Python学习之路-Flask基础:数据库"
        }
    ],
    "totalPage": 6
}
```

#### 后端实现

- 在`index/views.py`中定义视图函数。在查询的时候，如果用户分类id传0，则不添加分类查询条件

```python
@index_blu.route('/bloglist')
def get_blog_list():
    """
    获取指定分类的博客列表
    :return: 包含文章列表的jsonify对象
    """

    # 1. 获取参数
    args_dict = request.args
    page = args_dict.get("p", '1')
    per_page = args_dict.get("per_page", constants.HOME_PAGE_MAX_BLOG)
    category_id = args_dict.get("cid", '1')

    # 2. 校验参数
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3. 查询数据并分页
    filters = []
    # 如果分类id不为1，那么添加分类id的过滤
    if category_id != "1":
        filters.append(Blog.category_id == category_id)
    try:
        paginate = Blog.query.filter(*filters).order_by(Blog.create_time.desc()).paginate(page, per_page, False)
        # 获取查询出来的数据
        items = paginate.items
        # 获取到总页数
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    blog_list = []
    for blog in items:
        blog_list.append(blog.to_basic_dict())

    # 4. 返回数据
    return jsonify(errno=RET.OK, errmsg="OK", totalPage=total_page, currentPage=current_page, blogList=blog_list, cid=category_id)
```

## 详情页

### 前言

博客详情页是整个博客的精髓所在，我们需要完成：基类模板抽取、使用装饰器的形式完成用户数据的查询并传递到视图函数中、查询博客详情页数据并使用模板语言进行数据的展示、写出文章评论的后端逻辑、写出文章点赞的后端逻辑等功能。

### 准备工作

博客详情页面的前端页面为 `blog/detail.html`，创建博客详情页的模块`blog`，并在该模块下创建视图函数存储的 py 文件 `views.py`

- 创建蓝图

  ```python
  from flask import Blueprint

  blog_blu = Blueprint("blog", __name__, url_prefix='/blog')

  from . import views
  ```

- 注册蓝图

  ```python
  def create_app(config_name):
      ...
      # 注册蓝图
      from blog.modules.index import index_blu
      app.register_blueprint(index_blu)
  
      from blog.modules.passport import passport_blu
      app.register_blueprint(passport_blu)
  
      from blog.modules.blog import blog_blu
      app.register_blueprint(blog_blu)
      ...
      return app
  ```
  
- 提供文章详情页访问的视图函数，将文章详情页界面移动到模板文件夹，视图函数需要接受文章 id 作为参数，以便后续查询文章详情数据

  ```python 
  @blog_blu.route('/<int:blog_id>')
  def blog_detail(blog_id):
      return render_template('blog/detail.html')
 
  ```

### 数据展示

文章内容数据，查询文章数据并返回

```python
@blog_blu.route('/<int:blog_id>')
@user_login_data
def blog_detail(blog_id):
    try:
        blog = blog.query.get(blog_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    if not blog:
        # 返回数据未找到的页面
        abort(404)

    blog.clicks += 1
    data = {
        "blog": blog.to_dict(),
        "user_blog": g.user.to_dict() if g.user else None,
    }
    return render_template('blog/detail.html', data=data)
```



### 文章排行

- 查询文章点击量数据，并返回

```python
@blog_blu.route('/<int:blog_id>')
@user_login_data
def blog_detail(blog_id):
    ...
    # 获取点击排行数据
    blog_list = None
    try:
        blog_list = blog.query.order_by(blog.clicks.desc()).limit(constants.CLICK_RANK_MAX_blog)
    except Exception as e:
        current_app.logger.error(e)

    click_blog_list = []
    for blog in blog_list if blog_list else []:
        click_blog_list.append(blog.to_basic_dict())
    data = {
        "blog": blog.to_dict(),
        "click_blog_list": click_blog_list,
        "user_blog": g.user.to_dict() if g.user else None,
    }
    return render_template('blog/detail.html', data=data)\
```

### 文章评论

#### 需求分析

用户如果在登录的情况下，可以进行评论，未登录，点击评论弹出登录框。用户可以直接评论当前文章

#### 后端实现

##### 接口设计

- URL：/blog/blog_comment
- 请求方式：POST
- 传入参数：JSON格式
- 参数

|  参数名   |  类型  | 是否必须 |    参数说明    |
| :-------: | :----: | :------: | :------------: |
|  blog_id  |  int   |    是    |     文章id     |
|  comment  | string |    是    |    评论内容    |
| parent_id |  int   |    否    | 回复的评论的id |

- 返回类型：JSON

| 参数名 |  类型  | 是否必须 | 参数说明 |
| :----: | :----: | :------: | :------: |
| errno  |  int   |    是    |  错误码  |
| errmsg | string |    是    | 错误信息 |

##### 代码实现

在 `blog/views.py` 文件中添加评论文章的视图函数

```python
@blog_blu.route('/blog_comment', methods=["POST"])
@user_login_data
def add_blog_comment():
    """添加评论"""

    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    # 获取参数
    data_dict = request.json
    blog_id = data_dict.get("blog_id")
    comment_str = data_dict.get("comment")
    parent_id = data_dict.get("parent_id")

    if not all([blog_id, comment_str]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        blog = blog.query.get(blog_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not blog:
        return jsonify(errno=RET.NODATA, errmsg="该文章不存在")

    # 初始化模型，保存数据
    comment = Comment()
    comment.user_id = user.id
    comment.blog_id = blog_id
    comment.content = comment_str
    if parent_id:
        comment.parent_id = parent_id

    # 保存到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存评论数据失败")

    # 返回响应
    return jsonify(errno=RET.OK, errmsg="评论成功", data=comment.to_dict())
```

#### 文章评论列表

在文章详情的视图函数中，添加查询当前文章评论的逻辑

```python
@blog_blu.route('/<int:blog_id>')
@user_login_data
def blog_detail(blog_id):
    ...
    # 获取当前文章的评论
    comments = []
    try:
        comments = Comment.query.filter(Comment.blog_id == blog_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
    comment_list = []
    for item in comments:
        comment_dict = item.to_dict()
        comment_list.append(comment_dict)

    is_collected = False
    # 判断用户是否收藏过该文章
    if g.user:
        if blog in g.user.collection_blog:
            is_collected = True
    data = {
        "blog": blog.to_dict(),
        "click_blog_list": click_blog_list,
        "is_collected": is_collected,
        "user_blog": g.user.to_dict() if g.user else None,
        "comments": comment_list
    }
    return render_template('blog/detail.html', data=data)
```

#### 评论点赞功能

##### 需求分析

- 后端提供点赞和取消点赞功能
- 当用户点击未点赞按钮，执行点赞逻辑，向后端发起点赞请求，取消点赞则反之
- 在文章显示完成之后，底部评论会根据当前登录用户显示是否点赞图标

##### 接口设计

- URL：/blog/comment_like
- 请求方式：POST
- 传入参数：JSON格式
- 参数

|   参数名   |  类型  | 是否必须 |                 参数说明                  |
| :--------: | :----: | :------: | :---------------------------------------: |
| comment_id |  int   |    是    |                  评论id                   |
|  blog_id   |  int   |    是    |                  文章id                   |
|   action   | string |    是    | 点赞操作类型：add(点赞)，remove(取消点赞) |

- 返回类型：JSON

| 参数名 |  类型  | 是否必须 | 参数说明 |
| :----: | :----: | :------: | :------: |
| errno  |  int   |    是    |  错误码  |
| errmsg | string |    是    | 错误信息 |

##### 后端代码实现

- 在 `blog/views.py` 中添加点赞/取消点赞视图函数

```python
@blog_blu.route('/comment_like', methods=["POST"])
@user_login_data
def set_comment_like():
    """评论点赞"""

    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    # 获取参数
    comment_id = request.json.get("comment_id")
    blog_id = request.json.get("blog_id")
    action = request.json.get("action")

    # 判断参数
    if not all([comment_id, blog_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if action not in ("add", "remove"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 查询评论数据
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not comment:
        return jsonify(errno=RET.NODATA, errmsg="评论数据不存在")

    if action == "add":
        comment_like = CommentLike.query.filter_by(comment_id=comment_id, user_id=g.user.id).first()
        if not comment_like:
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = g.user.id
            db.session.add(comment_like)
            # 增加点赞条数
            comment.like_count += 1
    else:
        # 删除点赞数据
        comment_like = CommentLike.query.filter_by(comment_id=comment_id, user_id=g.user.id).first()
        if comment_like:
            db.session.delete(comment_like)
            # 减小点赞条数
            comment.like_count -= 1

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="操作失败")
    return jsonify(errno=RET.OK, errmsg="操作成功")
```

## 404 页面

### 需求

在用户访问一些不存在网址的时候弹出404页面

### 实现逻辑

可以使用 app.errorhandle(code_or_exception) 装饰器

### 代码实现

因为404页面没有底部的内容，所以在 `templates/blog/base.html` 里面将底部的内容设置成为一个 block

```html
{% block bottomBlock %}
    <div class="footer">
        <div class="footer_links">
            <a href="">关于我们</a>
            <span>|</span>
            <a href="">联系我们</a>
            <span>|</span>
            <a href="">招聘人才</a>
            <span>|</span>
            <a href="">友情链接</a>
        </div>
        <p class="copyright">
            CopyRight © 2020 Silence All Rights Reserved<br />
          电话：010-****888    京ICP备*******8号
        </p>
    </div>
{% endblock %}
```

- 将 `static/blog/404.html` 文件拖到 `templates/blog/` 目录下，并继承于基类模板

```html
{% extends 'blog/base.html' %}
{% block titleBlock %}
404
{% endblock %}

{% block contentBlock %}
    <div class="error_con">
        <img src="../../static/blog/images/not_found.png" alt="404">
        <h3>OOPS!</h3>
        <h4>该内容不存在</h4>
        <p>请检查你输入的网址是否正确，请点击以下按钮返回主页或者发送错误报告</p>
        <a href="/">返回首页</a>
    </div>
{% endblock %}

{% block rankBlock %}
{% endblock %}

{% block bottomBlock %}
{% endblock %}
```

- 在 `blog/__init__.py` 文件中的 `create_app` 函数中添加以下逻辑

```python
def create_app(config_name):
    ...

    @app.errorhandler(404)
    @user_login_data
    def page_not_found(_):
        user = g.user
        data = {"user_blog": user.to_dict() if user else None}
        return render_template('blog/404.html', data=data)
        return app
```

> 在浏览器里面输入网址进行测试
