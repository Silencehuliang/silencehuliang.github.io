# Python学习之路-综合练习:学生管理系统


目前已经学习了变量、流程控制、函数、模块，可以利用已学习的知识开发一个学生管理系统

## 项目需求

- 系统有首页介绍页面与功能菜单
- 系统功能由查询、显示、修改与删除功能
- 可以使用数字选择不同的功能
- 学生信息需要记录：姓名、性别、年龄、班级

## 项目搭建

### 步骤

#### 创建文件

- 新建`student_main.py`文件，用于编写主程序功能代码，并作为程序的入口每一次启动名片管理系统都通过这个文件启动

- 新建`student_tools.py`文件，用于编写功能函数，将对系统的 **新增**、**查询**、**修改**、**删除** 等功能封装在不同的函数中

#### 梳理业务逻辑，编写业务流程

```python
# 通过死循环控制整个业务主体运行

# 编写系统欢迎界面，并显示功能菜单

# 提供用户输入选项

# 对输入选项进行输出

# 根据用户输入决定后续的操作
```

{{< admonition tip "提示" true >}}

在进行编码前最好进行业务逻辑的梳理，然后根据需求编写一个业务流程。编码前思考再进行编码能大大提高整体的效率。

{{< /admonition >}}

#### 完成主程序编码

```python
# 通过死循环控制整个业务主体运行
while True:
    # 编写系统欢迎界面，并显示功能菜单
    print("*" * 20)
    print("欢迎使用【学生管理系统】1.0\n\n1. 新增学生\n2. 显示全部学生\n3. 查询学生\n0. 退出系统")
    print("*" * 20)
    # 提供用户输入选项
    options = input("请选择操作功能：")

    # 对输入选项进行输出
    print("您选择的操作是：%s" % options)

    # 根据用户输入决定后续的操作
    if options in ["1", "2", "3"]:
        pass
      	# TODO 后续操作业务
    elif options == "0":
        print("欢迎再次使用【名片管理系统】")
        break
    else:
        print("输入错误，请重新输入")
```

{{< admonition tip "提示" true >}}

在 `#` 后跟上 `TODO`，用于标记需要去做的工作

{{< /admonition >}}

#### 学生管理相关业务流程

##### 新增学生

```python
# 新增学生模块信息提示

# 提示用户输入学生信息

# 判断学生是否存在

# 存在则提示学生已存在

# 不存在将学生信息保存到一个字典

# 并将学生字典添加到学生列表

# 提示添加成功信息
```

##### 显示所有学生

```python
# 显示全部学生模块信息提示

# 遍历列表显示全部学生信息
```



##### 查询学生

```python
# 查询学生信息模块信息提示

# 提示用户输入搜索学生的姓名

# 遍历字典进行查询

# 找到后进行后续操作：修改/删除

# 没有找到输出提示信息
```



##### 修改与删除学生信息

```python
# 修改学生信息模块信息提示

# 提示用户输入修改学生的相关信息

# 提示修改成功信息

# 提示删除成功信息
```



##### 完成相关业务流程代码

```python
student_list = []


def new_student():
    """新建名片"""
    # 新增学生模块信息提示
    print("-" * 50)
    print("功能：新建学生")
    # 提示用户输入学生信息
    name = input("请输入姓名：")
    gender = input("请输入性别：")
    age = input("请输入年龄：")
    team = input("请输入班级：")
    # 将学生信息保存到一个字典
    student_dict = {"name": name,
                    "gender": gender,
                    "age": age,
                    "team": team}
    # 将学生字典添加到学生列表
    student_list.append(student_dict)

    # 提示添加成功信息
    print("成功添加学生：%s" % student_dict["name"])


def show_all_student():
    """显示全部学生"""
    # 显示全部学生模块信息提示
    print("-" * 50)
    print("功能：显示全部学生")

    # 遍历列表显示全部学生信息
    for name in ["姓名", "性别", "年龄", "班级"]:
        print(name, end="\t\t")
    print("")
    # 打印分隔线
    print("=" * 50)
    # 格式化输出信息
    for student_dict in student_list:
        print("%s\t\t%s\t\t%s\t\t%s" % (student_dict["name"],
                                        student_dict["gender"],
                                        student_dict["age"],
                                        student_dict["team"]))


def search_student():
    """查询学生信息"""
    # 查询学生信息模块信息提示
    print("-" * 50)
    print("功能：搜索名片")
    # 提示用户输入搜索学生的姓名
    find_name = input("请输入要查询的学生姓名：")
    # 遍历字典进行查询
    for student_dict in student_list:
        if student_dict["name"] == find_name:
            print("姓名\t\t\t性别\t\t\t年龄\t\t\t班级")
            print("-" * 40)
            print("%s\t\t\t%s\t\t\t%s\t\t\t%s" % (
                student_dict["name"],
                student_dict["gender"],
                student_dict["age"],
                student_dict["team"]))
            print("-" * 40)
            # 找到后进行后续操作：修改/删除
            # 提示用户输入修改学生的相关信息
            options = input("请选择要执行的操作[1] 修改 [2] 删除 [0] 返回上级菜单")
            if options == "1":
                student_dict["name"] = input("请输入姓名：")
                student_dict["gender"] = input("请输入性别：")
                student_dict["age"] = input("请输入年龄：")
                student_dict["team"] = input("请输入班级：")
                # 提示修改成功信息
                print("学生：'%s'的信息修改成功" % student_dict["name"])
            elif options == "2":
                student_list.remove(student_dict)
                # 提示删除成功信息

                print("学生：'%s'的信息删除成功" % student_dict["name"])
            break
    else:
        # 没有找到输出提示信息
        print("没有找到 %s" % find_name)
```

##### 将相关业务流程代码导入主流程,补充主流程中TUDO部分

```python
from student_tools import new_student,show_all_student,search_student

# 通过死循环控制整个业务主体运行
while True:
    # 编写系统欢迎界面，并显示功能菜单
    print("*" * 20)
    print("欢迎使用【学生管理系统】1.0\n\n1. 新增学生\n2. 显示全部学生\n3. 查询学生\n0. 退出系统")
    print("*" * 20)
    # 提供用户输入选项
    option = input("请选择操作功能：")

    # 对输入选项进行输出
    print("您选择的操作是：%s" % option)

    # 根据用户输入决定后续的操作
    if option in ["1", "2", "3"]:
        if option == "1":
            new_student()
        elif option == "2":
            show_all_student()
        elif option == "3":
            search_student()
    elif option == "0":
        print("欢迎再次使用【名片管理系统】")
        break
    else:
        print("输入错误，请重新输入")
```

{{< admonition tip "提示" true >}}

在代码中大量使用/n和/t等转义字符用于优化字符串输出样式，Python中可以使用的转移字符串如下表格：

| 转义字符     | 描述                                                     |
| :----------- | :------------------------------------------------------- |
| \\(在行尾时) | 续行符                                                   |
| \\\\         | 反斜杠符号                                               |
| \'           | 单引号                                                   |
| \"           | 双引号                                                   |
| \a           | 响铃                                                     |
| \b           | 退格(Backspace)                                          |
| \e           | 转义                                                     |
| \000         | 空                                                       |
| \n           | 换行                                                     |
| \v           | 纵向制表符                                               |
| \t           | 横向制表符                                               |
| \r           | 回车                                                     |
| \f           | 换页                                                     |
| \oyy         | 八进制数，y 代表 0~7 的字符，例如：\012 代表换行。       |
| \xyy         | 十六进制数，以 \x 开头，yy代表的字符，例如：\x0a代表换行 |
| \other       | 其它的字符以普通格式输出                                 |

{{< /admonition >}}
