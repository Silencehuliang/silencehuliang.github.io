# Python学习之路-爬虫提高:selenium


## 什么是selenium

Selenium是一个Web的自动化测试工具，最初是为网站自动化测试而开发的，Selenium 可以直接运行在浏览器上，它支持所有主流的浏览器（包括PhantomJS这些无界面的浏览器），可以接收指令，让浏览器自动加载页面，获取需要的数据，甚至页面截屏

## PhantomJS的介绍

PhantomJS 是一个基于Webkit的“无界面”(headless)浏览器，它会把网站加载到内存并执行页面上的 JavaScript

- 下载地址：http://phantomjs.org/download.html

## Chromedriver的介绍

Chromedriver 也是一个能够被selenium驱动的浏览器，但是和PhantomJS的区别在于它是有界面的

- 下载地址：https://npm.taobao.org/mirrors/chromedriver

## driver的安装

最简单的安装方式是：解压后把bin目录下的可执行文件移动到环境变量下，比如`/usr/bin` 或者是`/usr/local/bin`下面

注意：Chromedriver和电脑上的chrome版本有对应关系，建议使用最新的Chromedriver版本并且更新chrome浏览器到最新版

## selenium的入门使用

- 知识点：

  - 掌握如何发送请求，加载网页
  - 掌握如何进行简单的元素定位
  - 掌握如何从获取浏览器中的数据

- 加载网页： selenium通过控制浏览器，所以对应的获取的数据都是elements中的内容

  ```python
    from selenium import webdriver 
    driver = webdriver.PhantomJS(“c:…/pantomjs.exe”)
    driver.get("http://www.baidu.com/")
    driver.save_screenshot("长城.png")
  ```

- 定位和操作：

  ```python
    driver.find_element_by_id(“kw”).send_keys(“长城”)
    driver.find_element_by_id("su").click()
  ```

- 查看请求信息：

  ```python
    driver.page_source
    driver.get_cookies()
    driver.current_url
  ```

- 退出

  ```python
    driver.close() #退出当前页面
    driver.quit()  #退出浏览器
  ```

## selenium的定位操作

- 知识点：

  - 掌握定位元素的方法
  - 掌握获取元素中数据的方法

- 定位元素语法：

  ```python
    find_element_by_id (返回一个元素)
    find_elements_by_xpath （返回一个包含元素的列表）
    find_elements_by_link_text （根据连接文本获取元素列表）
    find_elements_by_partial_link_text （根据连接包含的文本获取元素列表）
    find_elements_by_tag_name (根据标签名获取元素列表)
    find_elements_by_class_name （根据类名获取元素列表）
  ```

  注意： `find_element`和`find_elements`的区别 `by_link_text`和`by_partial_link_tex`的区别：全部文本和包含某个文本

- 使用：

  以豆瓣首页为例:https://www.douban.com/

  ```python
    from selenium import webdriver
  
    driver =webdriver.Chrome()
  
    driver.get("https://www.douban.com/")
  
    ret1 = driver.find_element_by_id("anony-nav")
    print(ret1)
    # 输出为：<selenium.webdriver.remote.webelement.WebElement (session="ea6f94544ac3a56585b2638d352e97f3", element="0.5335773935305805-1")>
  
    ret2 = driver.find_elements_by_id("anony-nav")
    print(ret2)
    #输出为：[<selenium.webdriver.remote.webelement.WebElement (session="ea6f94544ac3a56585b2638d352e97f3", element="0.5335773935305805-1")>]
  
    ret3 = driver.find_elements_by_xpath("//*[@id='anony-nav']/h1/a")
    print(len(ret3))
     #输出为：1
  
    ret4 = driver.find_elements_by_tag_name("h1")
    print(len(ret4))
     #输出为：1
  
    ret5 = driver.find_elements_by_link_text("下载豆瓣 App")
    print(len(ret5))
     #输出为：1
  
    ret6 = driver.find_elements_by_partial_link_text("豆瓣")
    print(len(ret6))
     #输出为：28
  
    driver.close()
  ```

- 获取数据语法

  - find_element仅仅能够获取元素，不能顾直接获取其中的数据，`find_element_by_xapth`也是这样
  - 获取文本：`element.text`
  - 获取属性值：`element.get_attribute("href")`

- 使用示例：

  ```python
  from selenium import webdriver
  
  driver =webdriver.Chrome()
  
  driver.get("https://www.douban.com/")
  
  ret4 = driver.find_elements_by_tag_name("h1")
  print(ret4[0].text)
  #输出：豆瓣
  
  ret5 = driver.find_elements_by_link_text("下载豆瓣 App")
  print(ret5[0].get_attribute("href"))
  #输出：https://www.douban.com/doubanapp/app?channel=nimingye
  
  driver.close()
  ```

## selenium 处理cookie

通过`driver.get_cookies()`能够获取所有的cookie

```python
# 把cookie转化为字典
{cookie[‘name’]: cookie[‘value’] for cookie in driver.get_cookies()}

#删除一条cookie
driver.delete_cookie("CookieName")
# 删除所有的cookie
driver.delete_all_cookies()
```

## 页面等待

- 为什么需要等待

  如果网站采用了动态html技术，那么页面上的部分元素出现时间便不能确定，这个时候就可以设置一个等待时间，强制要求在时间内出现，否则报错

- 页面等待的方法 `time.sleep(10)`

## 使用selenium切换frame

frame是html中常用的一种技术，即一个页面中嵌套了另一个网页，selenium默认是访问不了frame中的内容的，对应的解决思路是 `driver.switch_to.frame()`

动手：模拟登陆qq邮箱

在使用selenium登录qq邮箱的过程中，我们会发现，无法在邮箱的登录input标签中输入内容，通过观察源码可以发现，form表单在一个frame中，所以需要切换到frame中

## selenium的优缺点

- selenium能够执行页面上的js，对于js渲染的数据和模拟登陆处理起来非常容易
- selenium由于在获取页面的过程中会发送很多请求，所以效率非常低，所以在很多时候需要酌情使用
