# 每天分享一个好用的Python库-Pygments


## 前言

今天分享一个用语法高亮器，适用于代码托管、论坛、维基或其他需要美化源代码的应用程序的第三方库：`Pygments`。

## Pygments

### 简介

`Pygments` 是一个支持500多种语言和其他文本格式的语法高亮库。可以轻松添加对新语言和格式的支持（大多数语言使用简单的基于正则表达式的机制）。

### 安装

```python
pip install Pygments
```

### 简单使用

- 输出一个Html的高亮显示：

  ```python
  from pygments import highlight
  from pygments.lexers import PythonLexer
  from pygments.formatters import HtmlFormatter
  
  code = 'print "Hello World"'
  print(highlight(code, PythonLexer(), HtmlFormatter()))
  
  # 输出
  <div class="highlight"><pre><span></span><span class="nb">print</span> <span class="s2">&quot;Hello World&quot;</span>
  </pre></div>
  ```

  `Pygments`默认情况下使用CSS类，而不是内联样式，避免一遍又一遍地输出多余的样式信息。

- 包含所有可能在输出中使用的 CSS 类的 CSS 样式表可以通过以下方式生成：

  ```bash
  print(HtmlFormatter().get_style_defs('.highlight'))
  ```

- 参数 to`get_style_defs()`用作额外的 CSS 选择器，输出可能如下所示：

  ```python
  .highlight .k { color: #AA22FF; font-weight: bold }
  .highlight .s { color: #BB4444 }
  ...
  ```

### 命令行使用

- 可以使用**pygmentize** 脚本从命令行使用 Pygments ：

  ```bash
  >>> pygmentize test.py
  ```
  
  将使用 ANSI 转义序列（又名终端颜色）突出显示 Python 文件 test.py 并将结果打印到标准输出。
  
- 要输出 HTML，请使用以下`-f`选项：

  ```bash
  >>> pygmentize -f html -o test.html test.py
  ```

- 将 HTML 突出显示的 test.py 版本写入文件 test.html。请注意，它只会是一段 HTML，如果想要完整的 HTML 文档，请使用“完整”选项：

  ```bash
  >>> pygmentize -f html -O full -o test.html test.py
  ```

  这将生成一个包含样式表的完整 HTML 文档。可以使用 选择样式。`-O style=<name>`

- 如果需要使用 Pygments CSS 类的现有 HTML 文件的样式表，可以使用以下方法创建：

  ```
  >>> pygmentize -S default -f html > style.css
  ```

  `default`样式名称在哪里。

更多选项和技巧可以在[命令行参考中找到](https://pygments.org/docs/cmdline/)。

### 作用

`Pygments`有多种输出格式可用，其中包括HTML、RTF、LaTeX和ANSI序列是一个非常好用的工具。

## 尾巴

`Pygments`这个工具可以让我们对代码中的各类语法获得高亮显示，增加了代码的可读性，不过最重要的还是代码整体的质量。

[官方文档地址](https://pygments.org/)


