# 接口测试:自动化脚本


## 接口自动化脚本

### 为什么要设计自动化脚本？
后台程序更新/发布新版之前需要验证下之前的功能是否能用
### 自动化脚本设计原则
1. 每个测试用例都是独立的
2. 测试用例都是可重复运行的
3. 测试数据与业务相分离（测试数据包括参数接口数据/ 测试执行所需要的系统数据)
4. 测试完成后，要删除不必要的测试数据。
### 自动化脚本设计组件分析
1. 使用数据库连接池
2. 使用setUp Thread Group线程组
3. 使用tearDown Thread Group线程组
4. 使用线程组
5. 使用函数
6. 使用关联
7. 添加断言
8. 使用sampler中请求
9. 添加聚合报告

## 性能脚本设计
### 为什么要设计性能脚本？
#### 问题
100虚拟用户请求服务器的时候，如何统计服务器响应时间和错误率？
### 什么是性能脚本？
概念：借助测试工具模拟多种业务需求操作对系统的各项性能指标进行测试的脚本
### 解决方案分析
1. 测试计划->线程组
2. 线程组->HTTP请求(查询学院-所有)
3. 测试计划->查看结果树
4. 测试计划->聚合报告
### 技术难点分析
1. 线程组-线程数
2. 测试计划-聚合报告(各指标意义)

### 项目-性能脚本设计
#### 性能脚本设计技巧
1. 新增、更新、删除：使用固定数值,比如新增100条,更新100条,删除100条
2. 查询：采用虚拟用户数和持续时间配合(比如，100用户，持续查询600秒)

#### 提示
1. 参数化：参数化尽量避免采用从外部读取参数，使用固定参数+函数形式( 如：${__counter(TRUE,)})
2. 察看结果树：必须清除单个接口内察看结果树
            (如不去掉，非常占用测试机自身性能)，在测试计划下添加一个察看结果树  
3. 报告：性能报告可根据实际需求选择，建议保留添加聚合报告  
4. 线程组：增删改查每一个功能点，都需建立单独线程组，而避免在同一个线程组内添加
           多个HTTP请求完成增删改查(一便参数化对单个请求做压测和并发)
5. 分布式：如并发数量大，采用分布式测试
6. 新增/删除：新增和删除接口建议不要采用时间模式来压测，直接使用线程数和循环；

## Jmeter 生成HTML报告

### 操作步骤：
#### 无jtl日志或csv日志文件生成报告
##### 基本命令格式

jmeter -n -t <test JMX file> -l <test log file> -e -o <Path to output folder>

##### 样例
jmeter -n -t E:\课件\Jmeter\Script\自动化脚本\Stu_AutoScript.jmx -l testLog -e -o ./output/report
##### 参数详解
-n ：以非GUI形式运行Jmeter
-t ：source.jmx 脚本路径
-l ：运行结果保存路径（.jtl）,此文件必须不存在
-e ：在脚本运行结束后生成html报告
-o ：保存html报告的地址, 此文件必须不存在


#### 有jtl日志或csv日志文件生成报告
##### 基本命令格式

jmeter -g <log file> -o <Path to output folder>

##### 样例

jmeter -g E:\课件\Jmeter\Script\自动化脚本\resultt.jtl -o ./outputreport

### HTML报告重点翻译
- APDEX(Application Performance Index)指数

- 聚合报告：类似于UI上的*Aggregate Report*

- Errors报告:展示不同错误类型的数量以及百分比

- 响应时间变化曲线:

  - 展示平均响应时间随时间变化情况
  - 类似于JMeter Plugins在UI上的*jp@gc - Response Times Over Time*
- 数据吞吐量时间曲线:

  - 展示每秒数据吞吐量随时间变化的情况
  - 类似于JMeter Plugins在UI上的*jp@gc - Bytes Throughput Over Time*
  Latency time变化曲线

- 展示Latency time随时间变化的情况  
  - 类似于JMeter Plugins在UI上的*jp@gc - Response Latencies Over Time*
  每秒点击数曲线
  - 类似于JMeter Plugins在UI上的*jp@gc - Hits per Second*

- HTTP状态码时间分布曲线

  - 展示响应状态码随时间的分布情况
  - 类似于JMeter Plugins在UI上的*jp@gc - Response Codes per Second*
- 吞吐量时间曲线(TPS)

  - 展示每秒处理的事务数随时间变化情况
  - 类似于JMeter Plugins在UI上的*jp@gc - Transactions per Second*
- 响应时间与每秒请求数的关系图
	- 展示平均响应时间与每秒请求数(可以理解为QPS)的关系

- Latency time与每秒请求数的关系图
	- 展示Latency time与每秒请求数的关系

- 响应时间百分位图
	- 响应时间百分位图

- 活动线程数变化曲线
	- 展示测试过程中活动线程数随时间变化情况

- 平均响应时间与线程数的关系图

  - 展示平均响应时间与线程数的关系
  - 类似于JMeter Plugins在UI上的*jp@gc - Response Times vs Threads*
- 柱状响应时间分布图 
	- 展示落在各个平均响应时间区间的请求数情况

## 接口测试基于Jmeter项目汇总


### API文档
1. 梳理业务需求整理接口清单
2. 提出相应不确定问题

### 接口清单
1. 设计测试用例
2. 设计功能脚本


### 测试用例

1. 设计参数化覆盖数据


### 功能脚本
1. HTTP请求默认值(设置服务器IP或域名；Content encoding：UTF-8)
2. HTTPHTTP信息头管理器(ContentType:application/json;charset=utf-8)
3. 线程组
4. Sampler(如:HTTP请求)  
 5. 新增-方法(POST)
 6. 更新-方法(PUT)
7. 删除-方法(DELETE)
8. 查询-方法(GET)
9. 查看结果树    
### 自动化脚本

1. 测试计划：勾选（独立运行每个线程组）确保脚本执行顺序，从上
2. 如不校验逆向数据，请去除CSV Data Set Config
3. 添加断言
4. 去除每个接口内的察看结果树元件
5. 动态数据使用**关联**(正则表达式/XPath)获取
6. 脚本执行顺序(先增数据，拿到新增数据ID后；在更新完毕数据后，查询新增数据；最后删除新增数据)  
7. 基于测试计划添加聚合报告和察看结果树

### 性能测试脚本

1. 线程组：设置线程数,调度器;
2. 监听器：察看结果树/聚合报告/用表格察看结果/Aggregate Graph
3. 检测服务器性能：(jp@gc - PerfMon Metrics Collector和ServerAgent插件)
