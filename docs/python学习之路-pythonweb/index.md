# Python学习之路-Django基础:PythonWeb


## Python Web 框架要点

### 处理流程

![](https://tva1.sinaimg.cn/large/00729CCqgy1gpzewf19i8j30nm0dggoo.jpg)

图片来源于[未来的小牛的CSDN博客](https://blog.csdn.net/m15511023218/article/details/84931862)

### 意义

用于搭建Web应用程序，免去不同Web应用相同代码部分的重复编写，只需关心Web应用核心的业务逻辑实现

### Web应用程序的本质

接收并解析HTTP请求，获取具体的请求信息，处理本次HTTP请求，即完成本次请求的业务逻辑处理，构造并返回处理结果——HTTP响应。

### Web框架学习方法

如何搭建工程程序

- 工程的组建
- 工程的配置
- 路由定义
- 视图函数定义

如何获取请求数据（操作request对象）

如何构造响应数据（构造response对象）

如何使用中间层

框架提供的其他功能组件的使用

- 数据库
- 模板
- admin
