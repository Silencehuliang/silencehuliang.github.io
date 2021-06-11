# Python学习之路-爬虫进阶:爬虫框架运行


## 框架安装

### 安装框架的目的

利用setup.py将框架安装到python环境中，在编写爬虫时候，作为第三方模块来调用

### 框架安装第一步：完成`setup.py`的编写

- 以下代码相当于一个模板，只用更改name字段出，改为对应的需要安装的模块名称就可以，比如这里是：scrapy_plus
- 将setup.py文件放到scrapy_plus的同级目录下

```python
from os.path import dirname, join
# from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='scrapy-plus',  # 模块名称
    version=version,
    description='A mini spider framework, like Scrapy',  # 描述
    packages=find_packages(exclude=[]),
    author='itcast',
    author_email='your@email.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='#',
    install_requires=parse_requirements("requirements.txt"),  # 所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
```

注意： 上面代码中可能会报错需要额外安装packaging模块，更新setuptools

- `pip install packaging`
- `pip install --upgrade setuptools`

pip.req可能不存在，对应的可以：

```Python
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]
```

### 框架安装第二步：完成`requirements.txt`的编写

功能：

- 写明依赖环境所支持的模块及其版本

使用：

- 在setup.py中使用
- 放置在setup.py同级目录下

```txt
requests>=2.18.4
six>=1.11.0
```

### 框架安装第三步：完成`VERSION.txt`的编写

功能：

- 标明当前版本，一个合格的模块，应当具备相应的版本号

使用：

- 在setup.py中使用
- 放置在setup.py同级目录下

```txt
1.0
```

### 框架安装第四步：执行安装命令

步骤：

- 切换到setup.py所在目录
- 切换到对应需要python虚拟环境下
- 在终端执行`python setup.py install`

## 框架运行

## 编写`main.py`

新在其他路径下创建一个项目文件夹 project_dir

```Python
# project_dir/main.py

from scrapy_plus.core.engine import Engine    # 导入引擎

if __name__ == '__main__':
    engine = Engine()    # 创建引擎对象
    engine.start()    # 启动引擎
```

运行结果：管道中打印的item对象

```shell
item对象:<scrapy_plus.item.Item object at 0x10759eef0>
```


