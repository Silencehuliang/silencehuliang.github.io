# Python学习之路-初识爬虫:数据提取


## 什么是数据提取

简单的来说，数据提取就是从响应中获取我们想要的数据的过程

## 爬虫中数据的分类

- 结构化数据：json，xml等
  - 处理方式：直接转化为python类型
- 非结构化数据：HTML
  - 处理方式：正则表达式、xpath

## 数据提取之json

### 为什么要复习json

由于把json数据转化为python内建数据类型很简单，所以爬虫中，如果我们能够找到返回json数据的URL，就会尽量使用这种URL，而很多地方也都会返回json

### 什么是json

JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式，它使得人们很容易的进行阅读和编写。同时也方便了机器进行解析和生成。适用于进行数据交互的场景，比如网站前台与后台之间的数据交互。

### 我们如何确定数据在哪里

在url地址对应的响应中搜索关键字即可

但是注意：url地址对应的响应中，中文往往是被编码之后的内容，所以更推荐大家去搜索英文和数字；另外一个方法就是在`perview`中搜索，其中的内容都是转码之后的

### 切换手机版寻找返回json的地址

在chrome中点击切换手机版的选项，需要重新刷新页面才能够切换成功，部分网站还需要重新进入主页面之后再继续点击才能够切换成功，比如：豆瓣热映

现在我们找到了返回电影数据的地址：`https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=android&for_mobile=1&callback=jsonp1&start=0&count=18&loc_id=108288&_=1524495777522`

通过请求我们发现，并不能成功，那是为什么呢？

对比抓包的地址和现在的地址，会发现部分headers字段没有，通过尝试，会发现是`Referer`字段缺少的原因

在上面这个地址中，我们会发现响应中包含部分数据并不是我们想要的，如下：

```json
;jsonp1({"count": 18, "start": 0, "subject_collection_items": "...."})
```

其中`jsonp1`似乎是很眼熟，在请求的地址中包含一个参数`callback=jsonp1`，正是由于这个参数的存在，才导致结果中也会有这部分数据，对应的解决方法是：直接删除url地址中的`callback`字段即可,在url地址中很多字段都是没用的，比如这里的`&loc_id`,`_`等等，可以大胆尝试

### json数据格式化方法

- 在preview中观察

- 其中：
  - 红色方框部分表示json中的键
  - 蓝色方框部分由于是个列表，展开后，下面的数字表示列表中对应位置的值
- 在线解析工具进行解析
  - 比如：https://www.bejson.com/
- pycharm进行reformat code
  - 在pycharm中新建一个json文件，把数据存入后，点击code下面的reformat code，但是中文往往显示的是unicode格式

### json数据的其他来源

抓包app，app的抓包方式会在后面学习，但是很多时候app中的数据是被加密的，但是仍然值得尝试

### json模块中方法的学习

其中类文件对象的理解：

> 具有read()或者write()方法的对象就是类文件对象，比如f = open(“a.txt”,”r”) f就是类文件对象

具体使用方法：

```python
#json.dumps 实现python类型转化为json字符串
#indent实现换行和空格
#ensure_ascii=False实现让中文写入的时候保持为中文
json_str = json.dumps(mydict,indent=2,ensure_ascii=False)


#json.loads 实现json字符串转化为python类型
my_dict = json.loads(json_str)


#json.dump 实现把python类型写入类文件对象
with open("temp.txt","w") as f:
    json.dump(mydict,f,ensure_ascii=False,indent=2)

# json.load 实现类文件对象中的json字符串转化为python类型
with open("temp.txt","r") as f:
    my_dict = json.load(f)
```

### json模块的作用

Json在数据交换中起到了一个载体的作用，承载相互传递的数据

## 数据提取之正则

### 什么是正则表达式

用事先定义好的一些特定字符、及这些特定字符的组合，组成一个**规则字符串**，这个**规则字符串**用来表达对字符串的一种**过滤**逻辑。

### 正则表达式的常见语法

知识点

- 正则中的字符
- 正则中的预定义字符集
- 正则中的数量词

正则的语法很多，不能够全部复习，对于其他的语法，可以临时查阅资料，比如:表示或还能使用`|`

练习： 下面的输出是什么？

```python
string_a = '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n\t\t<meta http-equiv="content-type" content="text/html;charset=utf-8">\n\t\t<meta content="always" name="referrer">\n        <meta name="theme-color" content="#2932e1">'
ret = re.findall("<.*>",string_a)
print(ret)
```

### re模块的常见方法

- pattern.match（从头找一个）

- pattern.search（找一个）

- pattern.findall（找所有）

  - 返回一个列表，没有就是空列表
  - `re.findall("\d","chuan1zhi2") >> ["1","2"]`

- pattern.sub（替换）

  - `re.sub("\d","_","chuan1zhi2") >> ["chuan_zhi_"]`

- re.compile（编译）

  - 返回一个模型P，具有和re一样的方法，但是传递的参数不同

  - 匹配模式需要传到compile中

    ```python
    p = re.compile("\d",re.S)
    p.findall("chuan1zhi2")
    ```

### python中原始字符串r的用法

知识点

- 原始字符串
- 元是字符串的长度
- 原始字符串的使用

原始字符串定义(raw string)：所有的字符串都是直接按照字面的意思来使用，没有转义特殊或不能打印的字符，原始字符串往往针对特殊字符而言。例如`"\n"`的原始字符串就是`"\\n"`

- 原始字符串的长度

  ```python
    In [19]: len("\n")
    Out[19]: 1
  
    In [20]: len(r"\n")
    Out[20]: 2
  
    In [21]: r"\n"[0]
    Out[21]: '\\'
  ```

- 正则中原始字符串的使用

  ```python
    In [13]: r"a\nb" == "a\\nb"
    Out[13]: True
  
    In [14]: re.findall("a\nb","a\nb")
    Out[14]: ['a\nb']
  
    In [15]: re.findall(r"a\nb","a\nb")
    Out[15]: ['a\nb']
  
    In [16]: re.findall("a\\nb","a\nb")
    Out[16]: ['a\nb']
  
    In [17]: re.findall("a\\nb","a\\nb")
    Out[17]: []
  
    In [18]: re.findall(r"a\\nb","a\\nb")
    Out[18]: ['a\\nb']
  ```

  上面的现象说明什么？

> 正则中使用原始字符串`r`能够忽略转义符号带来的影响，加上原始字符串`r`之后，待匹配的字符串中有多少个`\`，正则中就添加多少个`\`即可

- windows中原始字符串r的使用

## xpath和lxml类库

### 为什么要学习xpath和lxml

lxml是一款高性能的 Python HTML/XML 解析器，我们可以利用XPath，来快速的定位特定元素以及获取节点信息

### 什么是xpath

XPath (XML Path Language) 是一门在 HTML\XML 文档中查找信息的**语言**，可用来在 HTML\XML 文档中对**元素和属性进行遍历**。

### 认识xml

知识点：

- html和xml的区别

- xml中各个元素的的关系和属性

### html和xml的区别

| 数据格式 |      描述      |                   设计目标                   |
| :------: | :------------: | :------------------------------------------: |
|   XML    | 可拓展标记语言 | 被设计为传输与存储数据，其聚焦点是数据的内容 |
|   HTML   | 超文本标记语言 |        显示数据以及如何更好的显示数据        |

### xpath的节点关系

#### 是什么

每个XML的标签我们都称之为节点，其中最顶层的节点称为根节点。

####  xpath中节点选择的工具

- Chrome插件 XPath Helper
  - 下载地址：https://pan.baidu.com/s/1UM94dcwgus4SgECuoJ-Jcg 密码:337b
- Firefox插件 XPath Checker

注意： 这些工具是用来**学习xpath语法**的，他们都是**从elements中**匹配数据，elements中的数据和url地址对应的响应不相同，所以在代码中，不建议使用这些工具进行数据的提取

### xpath语法

#### 选取节点

XPath 使用路径表达式来选取 XML 文档中的节点或者节点集。这些路径表达式和我们在常规的**电脑文件系统中看到的表达式**非常相似。

**使用chrome插件选择标签时候，选中时，选中的标签会添加属性class="xh-highlight"**

下面列出了最有用的表达式：

|  表达式  |                            描述                            |
| :------: | :--------------------------------------------------------: |
| nodename |                        选中该元素。                        |
|    /     |          从根节点选取、或者是元素和元素间的过渡。          |
|    //    | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
|    .     |                       选取当前节点。                       |
|    ..    |                   选取当前节点的父节点。                   |
|    @     |                         选取属性。                         |
|  text()  |                         选取文本。                         |

#### 查找特定的节点

|             路径表达式              |                             结果                             |
| :---------------------------------: | :----------------------------------------------------------: |
|        //title[@lang="eng"]         |              选择lang属性值为eng的所有title元素              |
|         /bookstore/book[1]          |        选取属于 bookstore 子元素的第一个 book 元素。         |
|       /bookstore/book[last()]       |       选取属于 bookstore 子元素的最后一个 book 元素。        |
|      /bookstore/book[last()-1]      |      选取属于 bookstore 子元素的倒数第二个 book 元素。       |
|    /bookstore/book[position()>1]    |        选择bookstore下面的book元素，从第二个开始选择         |
| //book/title[text()='Harry Potter'] | 选择所有book下的title元素，仅仅选择文本为Harry Potter的title元素 |
| /bookstore/book[price>35.00]/title  | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

注意点: 在xpath中，第一个元素的位置是1，最后一个元素的位置是last(),倒数第二个是last()-1

#### 选取未知节点

XPath 通配符可用来选取未知的 XML 元素。

| 通配符 |         描述         |
| :----: | :------------------: |
|   *    |  匹配任何元素节点。  |
|   @*   |  匹配任何属性节点。  |
| node() | 匹配任何类型的节点。 |

### lxml的认识

在前面学习了xpath的语法，那么在代码中我们如何使用xpath呢，对应的我们需要lxml

安装方式：pip install lxml

### lxml模块的入门使用

导入lxml 的 etree 库 (导入没有提示不代表不能用)

`from lxml import etree`

利用etree.HTML，将字符串转化为Element对象,Element对象具有xpath的方法,返回结果的列表，能够接受bytes类型的数据和str类型的数据

```python
html = etree.HTML(text) 
ret_list = html.xpath("xpath字符串")
```

把转化后的element对象转化为字符串，返回bytes类型结果 `etree.tostring(element)`
