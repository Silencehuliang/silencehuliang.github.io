---
title: "Windows10在此处打开cmd"
date: 2019-01-08T15:58:54+08:00
draft: false
categories: ["系统优化"] 
tags: ["cmd"]
---

windows添加在此处打开cmd

- 新建一个文本文档

- 将 一下内容复制粘贴到文本文档中

```bash
Windows Registry Editor Version 5.00

[-HKEY_CLASSES_ROOT\Directory\shell\runas]

[HKEY_CLASSES_ROOT\Directory\shell\runas]

@="Open cmd here as admin"             

"HasLUAShield"=""

[HKEY_CLASSES_ROOT\Directory\shell\runas\command]

@="cmd.exe /s /k pushd \"%V\""

[-HKEY_CLASSES_ROOT\Directory\Background\shell\runas]

[HKEY_CLASSES_ROOT\Directory\Background\shell\runas]

@="Open cmd here as admin"           

"HasLUAShield"=""

[HKEY_CLASSES_ROOT\Directory\Background\shell\runas\command]

@="cmd.exe /s /k pushd \"%V\""

[-HKEY_CLASSES_ROOT\Drive\shell\runas]

[HKEY_CLASSES_ROOT\Drive\shell\runas]

@="Open cmd here as admin"           

"HasLUAShield"=""

[HKEY_CLASSES_ROOT\Drive\shell\runas\command]

@="cmd.exe /s /k pushd \"%V\""
    
```

- 另存为xxx.reg文件

- 双击运行