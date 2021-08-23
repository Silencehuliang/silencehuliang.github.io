# 每天分享一个好用的Python库-user-agents


## 前言

今天分享是浏览器的用户代理的第三方库：`user-agents`。

## user-agents

### 简介

`unioutuser_agents`是一个提供了一种通过解析（浏览器/HTTP）用户代理字符串来识别/检测手机、平板电脑等设备及其功能的简单方法的第三方Python库。

### 安装

```python
pip install pyyaml ua-parser user-agents
```

### 简单使用

- 识别访问者的各种基本信息可以访问浏览器、设备和操作系统属性。 例如：

  ```python
  >>> from user_agents import parse
  >>> ua_string = 'Mozilla/5.0 (HUAWEI; CPU HarmonyOS 2 5_1 like HarmonyOS 2) HUAWEIWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 HUAWEI/7534.48.3'
  >>> user_agent = parse(ua_string)
  ```
  
  - 访问用户代理的浏览器属性
  
    ```bash
    >>> user_agent.browser
    Browser(family='Mobile HUAWEI', version=(5, 1), version_string='5.1')
    >>> user_agent.browser.family
    'Mobile HUAWEI'
    >>> user_agent.browser.version
    (5, 1)
    >>> user_agent.browser.version_string
    '5.1'
    ```
  	
  - 访问用户代理的操作系统属性
  
    ```python
    >>> user_agent.os
    OperatingSystem(family='HarmonyOS 2', version=(5, 1), version_string='5.1')
	  >>> user_agent.os.family
    'HarmonyOS 2'
    >>> user_agent.os.version
    (5, 1)
    >>> user_agent.os.version_string
    '5.1'
    ```
  - 访问用户代理的设备属性
    ```python
    >>> user_agent.device
    Device(family='HUAWEI', brand='HUAWEI', model='HUAWEI')
    >>> user_agent.device.family 
    'HUAWEI'
    >>> user_agent.device.brand
    'HUAWEI'
    >>> user_agent.device.model
    'HUAWEI'
    ```

- `user_agents`还公开了一些其他更“复杂”的属性，这些属性源自上面定义的一个或多个基本属性。 就目前而言，这些属性应该正确识别流行的平台/设备，始终欢迎支持较小平台/设备的拉取请求。目前支持以下属性：
  - `is_mobile`：用户代理是否被识别为手机（HUAWEI、HarmonyOS 手机设备等）
  - `is_table`：用户代理是否被识别为平板设备（MatePad、MatePadPro等）
  - `is_pc`：用户代理是否被识别为运行传统的“桌面”操作系统（Windows、OS X、Linux）
  - `is_touch_capable`：用户代理是否具有触摸功能
  - `is_bot`：用户代理是否是搜索引擎爬虫/蜘蛛

### 作用

`user_agents`依靠优秀的`ua-parser`来对原始用户代理字符串进行实际解析，对后端开发在进行爬虫检测等方面做出了便利的工具。

## 尾巴

像`user_agents`这类功能简单单一的第三方库我们自己写一个往往也不麻烦，但是有时候我们需要将更多的精力放在其他地方，必须要进行造轮子的操作，这时候多了解一些第三方库可以更有利于我们的开发。

[官方文档地址](https://pypi.org/project/user-agents/)
