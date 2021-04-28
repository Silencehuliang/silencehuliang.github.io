# Python学习之路-Flask项目:博客后台


## 前言

上一篇完成了博客前台的相关内容，接下来进行博客后台的相关开发。

## 管理员登录

### 需求分析

 管理员用户进行登录，并且根据不同的情况报出不同的错误信息，如果当前已登录用户是管理员，在访问登录页面时直接跳转到后台管理主页。登录界面可以直接使用 Form 表单提交(也可以采用 ajax 的方式)

### 代码准备

在 **templates** 目录下创建 `admin` 文件夹，将 `static/admin/`目录下 `login.html` 与 `index.html` 拖动到 `admin` 目录下

### 代码实现

- 在 `admin/views.py` 中，添加登录视图函数

  ```python
  @admin_blu.route('/login')
  def admin_login():
      return render_template('admin/login.html')
  ```

访问测试

- 修改上一步视图函数，添加 post 请求方式，并添加登录相关逻辑

  ```python
  @admin_blu.route('/login', methods=["GET", "POST"])
  def admin_login():
      if request.method == "GET":    
          return render_template('admin/login.html')

      # 取到登录的参数
      username = request.form.get("username")
      password = request.form.get("password")
      if not all([username, password]):
          return render_template('admin/login.html', errmsg="参数不足")

      try:
          user = User.query.filter(User.mobile == username).first()
      except Exception as e:
          current_app.logger.error(e)
          return render_template('admin/login.html', errmsg="数据查询失败")

      if not user:
          return render_template('admin/login.html', errmsg="用户不存在")

      if not user.check_passowrd(password):
          return render_template('admin/login.html', errmsg="密码错误")

      if not user.is_admin:
          return render_template('admin/login.html', errmsg="用户权限错误")

      session["user_id"] = user.id
      session["nick_name"] = user.nick_name
      session["mobile"] = user.mobile
      session["is_admin"] = True

      # TODO 跳转到后台管理主页,暂未实现
      return "登录成功，需要跳转到主页"
  ```

 ## 管理后台主页

### 需求分析

为后台主页提供专门的视图函数，需要带入当前管理员用户相关信息以便在界面进行展示

### 代码实现

- 在 `modules/admin/views.py` 文件中添加视图函数

  ```python
  @admin_blu.route('/index')
  @user_login_data
  def admin_index():
      user = g.user
      return render_template('admin/index.html', user=user.to_dict())
  ```

访问测试

- 完善登录视图函数跳转界面逻辑

  ```python
  @admin_blu.route('/login', methods=["GET", "POST"])
  def admin_login():
      ...
      # 跳转到后台管理主页
      return redirect(url_for('admin.admin_index'))
  ```

- 完善如果已登录的管理员用户访问登录页面直接跳转到主页逻辑

  ```python
  def admin_login():
      if request.method == "GET":
          # 去 session 中取指定的值
          user_id = session.get("user_id", None)
          is_admin = session.get("is_admin", False)
          # 如果用户id存在，并且是管理员，那么直接跳转管理后台主页
          if user_id and is_admin:
              return redirect(url_for('admin.admin_index'))
          return render_template('admin/login.html')
      ...
  ```

## 后台访问权限控制

### 需求分析

解决普通用户登录之后直接访问后台具体的视图函数的问题，如果是普通用户访问后台的视图函数，直接跳转到项目主页，不再执行后续的逻辑判断，后台后续要实现多个视图函数，如果每一个函数内部都去判断用户权限，那么代码重复率高，冗余代码较多，所以得有一个统一判断入口，后台模块中，除了登录页面，后台的其他页面都要判断是否具有管理员权限，采用的方式为：请求勾子中的 before_request，来请求之前进行判断

### 代码实现

- 在 `modules/admin/__init__.py` 文件中，添加请求勾子函数

  ```python
  @admin_blu.before_request
  def before_request():
      # 判断如果不是登录页面的请求
      if not request.url.endswith(url_for("admin.admin_login")):
          user_id = session.get("user_id")
          is_admin = session.get("is_admin", False)

          if not user_id or not is_admin:
              # 判断当前是否有用户登录，或者是否是管理员，如果不是，直接重定向到项目主页
              return redirect('/')
  ```

- 完善退出登录相关代码，在退出登录时候，也要清空是否是管理员的相关数据，在 `modules/passport/views.py` 中
  ```python
  @passport_blu.route("/logout", methods=['POST'])
  def logout():
      """
      清除session中的对应登录之后保存的信息
      :return:
      """
      session.pop('user_id', None)
      session.pop('nick_name', None)
      session.pop('mobile', None)
      session.pop('is_admin', None)
  
      # 返回结果
      return jsonify(errno=RET.OK, errmsg="OK")
  ```

## 用户统计

### 需求分析

展示当前总人数，月活跃人数，日活跃人数，使用图表的形式展示活跃曲线

### 实现准备

将 `static/admin/user_count.html` 拖到 `templates/admin/` 目录下

### 代码实现

- 实现思路：
  - 月新增数：获取到本月第1天0点0分0秒的时间对象，然后查询最后一次登录比其大的所有数据
  - 日新增数：获取到当日0点0分0秒时间对象，然后查询最后一次登录比其大的所有数据
  - 图表查询：遍历查询数据每一天的数据(当前天数，减去某些天)
- 后端查询数据实现

  ```python
  @admin_blu.route('/user_count')
  def user_count():
      # 查询总人数
      total_count = 0
      try:
          total_count = User.query.filter(User.is_admin == False).count()
      except Exception as e:
          current_app.logger.error(e)

      # 查询月新增数
      mon_count = 0
      try:
          now = time.localtime()
          mon_begin = '%d-%02d-01' % (now.tm_year, now.tm_mon)
          mon_begin_date = datetime.strptime(mon_begin, '%Y-%m-%d')
          mon_count = User.query.filter(User.is_admin == False, User.create_time >= mon_begin_date).count()
      except Exception as e:
          current_app.logger.error(e)

      # 查询日新增数
      day_count = 0
      try:
          day_begin = '%d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
          day_begin_date = datetime.strptime(day_begin, '%Y-%m-%d')
          day_count = User.query.filter(User.is_admin == False, User.create_time > day_begin_date).count()
      except Exception as e:
          current_app.logger.error(e)

      # 查询图表信息
      # 获取到当天00:00:00时间

      now_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
      # 定义空数组，保存数据
      active_date = []
      active_count = []

      # 依次添加数据，再反转
      for i in range(0, 31):
          begin_date = now_date - timedelta(days=i)
          end_date = now_date - timedelta(days=(i - 1))
          active_date.append(begin_date.strftime('%Y-%m-%d'))
          count = 0
          try:
              count = User.query.filter(User.is_admin == False, User.last_login >= day_begin,
                                        User.last_login < day_end).count()
          except Exception as e:
              current_app.logger.error(e)
          active_count.append(count)

      active_date.reverse()
      active_count.reverse()

      data = {"total_count": total_count, "mon_count": mon_count, "day_count": day_count, "active_date": active_date,
              "active_count": active_count}

      return render_template('admin/user_count.html', data=data)
  ```

## 用户列表

### 需求

按用户最后一次登录倒序分页展示用户列表

### 实现准备

将 `static/admin/user_list.html` 拖到 `templates/admin/` 目录下

### 代码实现

后端逻辑

```python
@admin_blu.route('/user_list')
def user_list():
    """获取用户列表"""

    # 获取参数
    page = request.args.get("p", 1)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 设置变量默认值
    users = []
    current_page = 1
    total_page = 1

    # 查询数据
    try:
        paginate = User.query.filter(User.is_admin == False).order_by(User.last_login.desc()).paginate(page, constants.ADMIN_USER_PAGE_MAX_COUNT, False)
        users = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    # 将模型列表转成字典列表
    users_list = []
    for user in users:
        users_list.append(user.to_admin_dict())

    context = {"total_page": total_page, "current_page": current_page, "users": users_list}
    return render_template('admin/user_list.html',
                           data=context)
```

## 文章版式编辑

### 需求分析

- 以分页的形式按文章创建时间倒序展示出文章数据
- 可以使用关键这这对文章标题进行搜索
- 点击编辑进入编辑详情页面

### 实现准备

- 将 `static/admin/` 目录下的 `blog_edit.html` 以及 `blog_edit_detail.html` 拖到 `templates/admin/` 目录下

### 代码实现

- 在 `admin/views.py` 文件中添加视图函数以返回文章列表

```python
@admin_blu.route('/blog_edit')
def blog_edit():
    """返回文章列表"""

    page = request.args.get("p", 1)
    keywords = request.args.get("keywords", "")
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    blog_list = []
    current_page = 1
    total_page = 1

    try:
        filters = []
        # 如果有关键词
        if keywords:
            # 添加关键词的检索选项
            filters.append(blog.title.contains(keywords))

        # 查询
        paginate = blog.query.filter(*filters) \
            .order_by(blog.create_time.desc()) \
            .paginate(page, constants.ADMIN_blog_PAGE_MAX_COUNT, False)

        blog_list = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    blog_dict_list = []
    for blog in blog_list:
        blog_dict_list.append(blog.to_basic_dict())

    context = {"total_page": total_page, "current_page": current_page, "blog_list": blog_dict_list}

    return render_template('admin/blog_edit.html', data=context)
```

## 新闻版式编辑详情

### 编辑详情界面数据

- 在 `admin/views.py` 中添加新闻编辑详情视图函数，接收新闻id为参数

```python
@admin_blu.route('/blog_edit_detail')
def blog_edit_detail():
    """新闻编辑详情"""

    # 获取参数
    blog_id = request.args.get("blog_id")

    if not blog_id:
        return render_template('admin/blog_edit_detail.html', data={"errmsg": "未查询到此新闻"})

    # 查询新闻
    blog = None
    try:
        blog = blog.query.get(blog_id)
    except Exception as e:
        current_app.logger.error(e)

    if not blog:
        return render_template('admin/blog_edit_detail.html', data={"errmsg": "未查询到此新闻"})

    # 查询分类的数据
    categories = Category.query.all()
    categories_li = []
    for category in categories:
        c_dict = category.to_dict()
        c_dict["is_selected"] = False
        if category.id == blog.category_id:
            c_dict["is_selected"] = True
        categories_li.append(c_dict)
    # 移除`最新`分类
    categories_li.pop(0)

    data = {"blog": blog.to_dict(), "categories": categories_li}
    return render_template('admin/blog_edit_detail.html', data=data)
```

### 新闻编辑提交

- 修改视图函数，使其能够接受POST请求执行保存编辑操作，并实现其代码

```python
@admin_blu.route('/blog_edit_detail', methods=["GET", "POST"])
def blog_edit_detail():
    """新闻编辑详情"""
    if request.method == "GET":
        ...
        return render_template('admin/blog_edit_detail.html', data=data)

    blog_id = request.form.get("blog_id")
    title = request.form.get("title")
    digest = request.form.get("digest")
    content = request.form.get("content")
    index_image = request.files.get("index_image")
    category_id = request.form.get("category_id")
    # 1.1 判断数据是否有值
    if not all([title, digest, content, category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

    blog = None
    try:
        blog = blog.query.get(blog_id)
    except Exception as e:
        current_app.logger.error(e)
    if not blog:
        return jsonify(errno=RET.NODATA, errmsg="未查询到新闻数据")

    # 1.2 尝试读取图片
    if index_image:
        try:
            index_image = index_image.read()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

        # 2. 将标题图片上传到七牛
        try:
            key = storage(index_image)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.THIRDERR, errmsg="上传图片错误")
        blog.index_image_url = constants.QINIU_DOMIN_PREFIX + key
    # 3. 设置相关数据
    blog.title = title
    blog.digest = digest
    blog.content = content
    blog.category_id = category_id

    # 4. 保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")
    # 5. 返回结果
    return jsonify(errno=RET.OK, errmsg="编辑成功")
```

## 新闻分类管理

### 需求分析

可以修改当前新闻分类名，可以添加新闻分类

### 实现准备

将 `static/admin/blog_type.html` 文件拖到 `templates/admin/` 目录下

### 代码实现

在 `admin/views.py` 文件中添加视图函数以返回分类列表

```python
@admin_blu.route('/blog_category')
def get_blog_category():
    # 获取所有的分类数据
    categories = Category.query.all()
    # 定义列表保存分类数据
    categories_dicts = []

    for category in categories:
        # 获取字典
        cate_dict = category.to_dict()
        # 拼接内容
        categories_dicts.append(cate_dict)

    categories_dicts.pop(0)
    # 返回内容
    return render_template('admin/blog_type.html', data={"categories": categories_dicts})
```
