# Python学习之路-模块和包


## 模块

### 简介

模块是 Python 程序架构的一个核心概念。每一个以扩展名 `py` 结尾的 `Python` 源代码文件都是一个模块，模块名同样也是一个标识符，需要符合标识符的命名规则。在模块中定义的全局变量、函数、类都是提供给外界直接使用的工具。模块就好比是工具包，要想使用这个工具包中的工具，就需要先导入这个模块。

### 导入方式

- `import`导入：是一次性把模块中 所有工具全部导入

  ```python
  import 模块名
  ```

  - 在导入模块时，每个导入应该独占一行
  - 通过 `模块名.` 使用模块提供的工具

  {{< admonition tip "提示" true >}}

  开发时 `import` 代码应该统一写在代码的顶部，更容易及时发现冲突。一旦发现冲突，可以使用 `as`关键字给其中一个工具起一个别名：`import 模块名 as 模块别名`

  {{< /admonition >}}

- `from...import`导入：如果希望从某一个模块中，导入部分工具，就可以使用 `from ... import` 的方式。`import 模块名` 

  ```python
  # 从 模块 导入 某一个工具
  from 模块名1 import 工具名
  ```

  导入之后不需要通过 `模块名.`可以直接使用模块提供的工具。

  {{< admonition warning "注意" true >}}

  如果两个模块，存在同名的函数，那么后导入模块的函数，会覆盖掉先导入的函数

  {{< /admonition >}}

- from...import *（不推荐）

  ```python
  # 从 模块 导入 所有工具
  from 模块名1 import *
  ```

  {{< admonition warning "注意" true >}}

  这种方式不推荐使用，因为函数重名并没有任何的提示，出现问题不好排查
  
  {{< /admonition >}}



### 模块的搜索顺序

`Python` 的解释器在导入模块时，会先搜索当前目录指定模块名的文件，如果有就直接导入，如果没有，再搜索系统目录。

{{< admonition warning "注意" true >}}

在开发时，给文件起名，不要和系统的模块文件重名。

{{< /admonition >}}

{{< admonition tip "提示" true >}}

`Python` 中每一个模块都有一个内置属性 `__file__` 可以查看模块的完整路径。

{{< /admonition >}}



### `__name__` 属性

`__name__` 是 `Python` 的一个内置属性，记录着一个字符串。如果是被其他文件导入的，`__name__`就是模块名。如果 是当前执行的程序`__name__`是`__main__`。`__name__`属性可以做到，测试模块的代码只在测试情况下被运行，而在被导入时不会被执行！

{{< admonition tip "补充" true >}}

在导入时，模块中所有没有任何缩进的代码都会被执行一遍！在实际开发中通常会在模块下方增加一些测试代码仅在模块内使用，被导入到其他文件中不需要执行。可以在`if __name__ == "__main__":`下方缩进中编写测试代码，从而不会被执行

{{< /admonition >}}

## 包

包是一个包含多个模块的特殊目录，目录下有一个特殊的文件：`__init__.py`。包名的命名方式和变量名一致。使用 `import 包名` 可以一次性导入包中所有的模块

## 发布模块

如果希望自己开发的模块，分享给其他人，可以按照以下步骤操作：

- 创建 setup.py

```python
from distutils.core import setup

setup(name="hm_message",  # 包名
      version="1.0",  # 版本
      description="itheima's 发送和接收消息模块",  # 描述信息
      long_description="完整的发送和接收消息模块",  # 完整描述信息
      author="itheima",  # 作者
      author_email="itheima@itheima.com",  # 作者邮箱
      url="www.itheima.com",  # 主页
      py_modules=["hm_message.send_message",
                  "hm_message.receive_message"])

```

{{< admonition tip "补充" true >}}

有关字典参数的详细信息，可以参阅[官方网站](https://docs.python.org/2/distutils/apiref.html)

{{< /admonition >}}

- 构建模块

  ```bash
  $ python3 setup.py build
  ```

- 生成发布压缩包

  ```bash
  $ python3 setup.py sdist
  ```

  {{< admonition warning "注意" true >}}

  要制作哪个版本的模块，就使用哪个版本的解释器执行！

  {{< /admonition >}}

- 安装模块

  ```bash
  $ tar -zxvf hm_message-1.0.tar.gz 
  $ sudo python3 setup.py install
  ```

  {{< admonition tip "提示" true >}}

  **卸载模块**

  直接从安装目录下，把安装模块的 **目录** 删除就可以

  ```python
  $ cd /usr/local/lib/python3.5/dist-packages/
  $ sudo rm -r hm_message*
  ```

  {{< /admonition >}}

## 安装第三方模块

第三方模块通常是指由知名的第三方团队开发的并且被程序员广泛使用的`Python`包 / 模块。例如 `request` 就是一套非常成熟的HTTP 服务模块。`pip` 是一个现代的，通用的 `Python` 包管理工具，提供了对 `Python` 包的查找、下载、安装、卸载等功能。

安装和卸载命令如下：

```bash
$ sudo pip3 install requests
$ sudo pip3 uninstall requests
```


