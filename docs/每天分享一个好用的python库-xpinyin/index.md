# 每天分享一个好用的Python库-xpinyin


## 前言

今天分享是一个将汉字转换为拼音的的第三方库：`xpinyin`。

## shortuuid

### 简介

将汉字转换为拼音的的第三方库：`xpinyin`

### 安装

- `Python`版本大于等于3.6

  ```python
  pip install -U xpinyin
  ```

- `Python`版本小于3.6

  ```python
  pip install xpinyin==0.5.7
  ```

  

### 简单使用

- 默认分隔符为`-`

  ```python
  >>> from xpinyin import Pinyin
  >>> p = Pinyin()
  >>> p.get_pinyin("上海")
  'shang-hai'
  ```
  
- 显示声调

  ```python
  >>> p.get_pinyin("上海", tone_marks='marks')
  'shàng-hǎi'
  >>> p.get_pinyin("上海", tone_marks='numbers')
  >>> 'shang4-hai3'
  ```

- 去掉分隔符

  ```python
  >>> p.get_pinyin("上海", '')
  'shanghai'
  ```

- 指定分隔符

  ```python
  >>> p.get_pinyin("上海", ' ')
  'shang hai'
  
  ```

- 获取首字母，并修改分隔符

  ```python
  >>> p.get_initial("上")
  'S'
  >>> p.get_initials("上海")
  'S-H'
  >>> p.get_initials("上海", '')
  'SH'
  >>> p.get_initials("上海", ' ')
  'S H'
  ```
  
- 获取声母
  
  ```python
  >>> p.get_initials("上海", splitter='-', with_retroflex=True)
  'SH-H'
  ```
  
- 获取多种读音的组合

  ```python
  >>> p.get_pinyins('模型', splitter=' ', tone_marks='marks')
  ['mó xíng', 'mú xíng']
  >>> p.get_pinyins('模样', splitter=' ', tone_marks='marks')
  ['mó yáng', 'mó yàng', 'mó xiàng', 'mú yáng', 'mú yàng', 'mú xiàng']
  ```

  

### 作用

这个库的作用很简单，就是从字转音的方式教大家认识汉语，学明白汉语！

## 尾巴

这个库是在大力宣传汉语呀，给想学习汉语的人一个学习的机会吧，要大力支持！

[官方文档地址](https://pypi.org/project/xpinyin/)


