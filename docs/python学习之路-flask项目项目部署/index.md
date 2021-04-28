# Python学习之路-Flask项目:项目部署


## 部署环境

基于MacOS 10.15.4系统，使用 Gunicorn + Nginx 进行布署，云服务器为阿里云

## 服务器选择

### 阿里云服务器

- [地址](https://www.aliyun.com)

- [个人免费试用](https://free.aliyun.com/)

- 进入控制台,查看实例创建情况

- 给安全组配置规则，添加5000端口(一并加上5001端口)

- 利用命令行进行远程服务器登录

  ```
  ssh 用户名@ip地址
  ```

## 相关环境安装

以下操作都在远程服务器上进行操作

- 先更新 apt 相关源

  ```bash
  sudo apt-get update
  ```

- mysql安装

  ```bash
  apt-get install mysql-server
  apt-get install libmysqlclient-dev
  ```

- redis安装

  ```bash
  sudo apt-get install redis-server
  ```

- 安装虚拟环境

  ```bash
  pip install virtualenv
  pip install virtualenvwrapper
  ```

- 使得安装的virtualenvwrapper生效，编辑~/.bashrc文件，内容如下:

  ```bash
  export WORKON_HOME=$HOME/.virtualenvs
  export PROJECT_HOME=$HOME/workspace
  source /usr/local/bin/virtualenvwrapper.sh
  ```

- 使编辑后的文件生效

  ```bash
  source ~/.bashrc
  ```

## requirements文件

Python 项目中可以包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号，以便在新环境中进行部署操作。

- 在虚拟环境使用以下命令将当前虚拟环境中的依赖包以版本号生成至文件中：

  ```bash
  pip freeze > requirements.txt
  ```

- 当需要创建这个虚拟环境的完全副本，可以创建一个新的虚拟环境，并在其上运行以下命令：

  ```bash
  pip install -r requirements.txt
  ```

- 在安装 Flask-MySQLdb 的时候可能会报错，可能是依赖包没有安装，执行以下命令安装依赖包：

  ```bash
  sudo apt-get build-dep python-mysqldb
  ```

## Nginx

- 采用 C 语言编写
- 实现分流、转发、负载均衡

### 相关操作

- 安装

  ```bash
  $ sudo apt-get install nginx
  ```

- 运行及停止

  ```bash
  /etc/init.d/nginx start #启动
  /etc/init.d/nginx stop  #停止
  ```

- 配置文件

  编辑文件:/etc/nginx/sites-available/default

  ```python
  # 如果是多台服务器的话，则在此配置，并修改 location 节点下面的 proxy_pass 
  upstream flask {
          server 127.0.0.1:5000;
          server 127.0.0.1:5001;
  }
  server {
          # 监听80端口
          listen 80 default_server;
          listen [::]:80 default_server;
  
          root /var/www/html;
  
          index index.html index.htm index.nginx-debian.html;
  
          server_name _;
  
          location / {
                  # 请求转发到gunicorn服务器
                  proxy_pass http://127.0.0.1:5000;
                  # 请求转发到多个gunicorn服务器
                  # proxy_pass http://flask;
                  # 设置请求头，并将头信息传递给服务器端 
                  proxy_set_header Host $host;
                  # 设置请求头，传递原始请求ip给 gunicorn 服务器
                  proxy_set_header X-Real-IP $remote_addr;
          }
  }
  ```

## Gunicorn

- Gunicorn（绿色独角兽）是一个Python WSGI的HTTP服务器
- 从Ruby的独角兽（Unicorn ）项目移植
- 该Gunicorn服务器与各种Web框架兼容，实现非常简单，轻量级的资源消耗
- Gunicorn直接用命令启动，不需要编写配置文件

### 相关操作

- 安装

  ```bash
  pip install gunicorn
  ```

- 查看选项

  ```bash
  gunicorn -h
  ```

- 运行

  ```bash
  # -w: 表示进程（worker） -b：表示绑定ip地址和端口号（bind）
  gunicorn -w 2 -b 127.0.0.1:5000 运行文件名称:Flask程序实例名
  ```

参考阅读： Gunicorn相关配置：https://blog.csdn.net/y472360651/article/details/78538188

## 其他操作

- 拷贝本地代码到远程

  ```bash
  scp -r 本地文件路径 root@39.106.21.198:远程保存路径
  ```


