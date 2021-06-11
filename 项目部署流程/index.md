# Python常见项目部署流程

### 项目部署流程
#### 更新系统源
```sudo apt-get update```

更新系统源是因为我们购买的云主机里装的系统中有很多软件都还没有更新到最新版本，后续安装可能会出现问题

#### 安装依赖包

```
#安装gcc g++的依赖库
sudo apt-get install build-essential
sudo apt-get install libtool

#安装 pcre依赖库
sudo apt-get install libpcre3 libpcre3-dev

#安装 pcre依赖库
sudo apt-get install zlib1g-dev

#安装 ssl依赖库
sudo apt-get install openssl
```
更新依赖库是为了防止在后续安装nginx的过程中出现错误

#### 安装工具包
```
#安装git
sudo apt-get install git
#安装上传rz、下载sz工具
sudo apt-get install lrzsz
```
可以通过git或者rz上传我们的项目到云服务器中，使用pycharm的同学可以用tools工具中的deployment工具同步更新项目

#### 安装python3与pip3
```
sudo apt install python3
sudo apt install python3-pip
```
现在大多数的项目都是基于python3，用系统中自带的python可能会出现问题，一般ubuntu系统自带有python3，16.04自带python3.5,18.04自带python3.6，想要其他版本的同学可以自行安装自己想要的版本，pip的版本建议更新到最新，目前是19的版本

#### 安装虚拟环境管理virtualenv
```sudo pip3 install virtualenv```

虚拟环境是一个相对独立的环境，可以为不同的项目创建不同的虚拟环境，在python中可以通过安装virtualenv来管理虚拟环境，这里要注意的是一定要用pip3来安装

#### 建立项目文件夹与虚拟环境文件夹
```
#项目文件夹
1.sudo mkdir -p /home/admin/project

#虚拟环境文件夹
2.sudo mkdir -p /home/admin/projectenv
```
#### 创建并启动虚拟环境并测试
```
# 查看python3的路径
in:which python3
out:/usr/bin/python3

# 进入虚拟环境文件夹
cd /home/admin/projectenv

# 创建指定python版本的虚拟环境
sudo virtualenv -p /usr/bin/python3 demoenv

# 启动虚拟环境 
source  /home/admin/projectenv/demoenv/bin/activate
虚拟环境启动成功后,会在当前用户名前面显示当前虚拟环境的名字

# 测试虚拟环境
python -V
pip -V
# 通过查看python与pip的版本判断当前虚拟环境是否是我们需要的虚拟环境
```

#### 上传项目并测试项目
```
# 通过git或者rz上传项目
git clone url
rz

# 进入项目文件夹，安装项目所需的库
sudo pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 切换到项目入口目录启动项目测试
python manage.py runserver 0.0.0.0:8000
# 这里通过控制ip与端口号保证该项目能够顺利运行，ip写0.0.0.0保证对外可以访问，端口号要在服务器的安全组或者防火墙中配置,在浏览器中输入服务器的公网ip:port测试是否能访问

# 设置超级管理员账户，并测试Django后台页面
python manage.py createsuperuser
# 访问ip:port/admin测试Django
```
可能出现的问题：
1.admin界面没有css
解决方案：
将debug设置为true

#### 安装uwsgi
1.在虚拟环境中安装uwsgi
in:sudo pip install uwsgi
2


1.在settings文件中设置STATIC_ROOT目录
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
2.在项目入口下执行collectstatic命令
python manage.py collectstatic
执行这个命令会将项目的所有css与js都下载到项目根目录下的static目录中






