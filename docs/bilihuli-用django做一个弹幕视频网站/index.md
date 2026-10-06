# bilihuli:用Django做一个弹幕视频网站


## 前言

早在写「python学习之路-flask项目博客」系列的时候就有个想法：博客做完了，能不能再做一个稍微复杂一点的 Web 项目？作为一个老 B 站用户，我选择了模仿 Bilibili 做一个弹幕视频网站，取名 bilihuli。这个项目用的是我最早入门的 Django，正好把之前 Django 系列教程里学到的知识完整地串起来用一遍。

## 整体设计

项目分为两大部分：

- **后台逻辑**:Django 实现，负责用户、视频、弹幕的管理
- **前端展示**:视频播放页 + 弹幕渲染

### 数据模型设计

核心的模型有三个：用户（User）、视频（Video）、弹幕（Danmaku）。其中弹幕表是重头戏，除了内容本身，还要记录弹幕在视频时间轴上的位置（time）、模式（滚动/顶部/底部）、颜色和发送者：

```python
class Danmaku(models.Model):
    MODE_SCROLL = 1
    MODE_TOP = 5
    MODE_BOTTOM = 4
    MODE_CHOICES = (
        (MODE_SCROLL, '滚动'),
        (MODE_TOP, '顶部'),
        (MODE_BOTTOM, '底部'),
    )

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='danmaku')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    time = models.FloatField(help_text='弹幕出现的时间点(秒)')
    mode = models.SmallIntegerField(choices=MODE_CHOICES, default=MODE_SCROLL)
    color = models.CharField(max_length=7, default='#FFFFFF')
    created_at = models.DateTimeField(auto_now_add=True)
```

这样设计的好处是查询某条弹幕只需要按视频 + 时间范围过滤，配合索引效率很高。

## 弹幕协议

弹幕网站和普通视频网站最大的区别就是弹幕的发送与同步。bilihuli 里我采用了最简单的轮询方案：

- 发送弹幕:`POST /api/video/<id>/danmaku/`，带上 content、time、mode、color
- 拉取弹幕:`GET /api/video/<id>/danmaku/`，返回该视频的全部弹幕列表（JSON），前端播放器按 time 调度渲染

弹幕 JSON 的字段设计参考了主流弹幕播放器的格式，前端根据 mode 决定弹幕轨道，根据 color 渲染颜色。对一个小项目来说，轮询完全够用，也没有引入 WebSocket 的复杂度。

## 踩过的坑

1. **Django 版本差异**：项目断断续续写了一年多，中间跨了 Django 大版本，`on_delete` 从默认级联变成了必填参数，配置文件的写法也有一些变化，升级的时候要仔细看 release notes。
2. **视频存储**：一开始把视频文件直接放静态目录，体验很差。后来文件走对象存储，数据库里只存 URL，后台只管元数据。
3. **弹幕去重防刷**：同一用户对同一时间点的弹幕做了简单的频率限制，避免刷屏。

## 小结

这个项目让我把 Django 的模型设计、Admin 站点、视图、序列化这些东西完整地练了一遍，也体会到"从教程到项目"中间隔着无数个细节。项目目前在 GitHub 上私有仓库放着，以后有空再把弹幕协议升级成 WebSocket 版本。

