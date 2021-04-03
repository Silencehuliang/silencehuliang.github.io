# Windows10在此处打开cmd


**声明：以下内容均为我个人的理解，如果发现错误或者疑问可以联系我共同探讨**

在Windows10中我们经常需要在某个文件夹下打开cmd窗口，虽然可以在地址栏输入cmd打开，但还是比较麻烦，可以修改注册表添加一个右键菜单来解决这个问题。

### 步骤

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
