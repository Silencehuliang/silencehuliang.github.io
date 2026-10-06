# Silence Blog 维护手册

> 2026-10 由线上发布产物逆向重建了 Hugo 源码。本文档记录技术栈、日常维护流程与已知问题。

## 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| [Hugo](https://gohugo.io/) | **0.74.3 extended** | 静态站点生成器,必须用 extended 版(需编译 SCSS) |
| [LoveIt](https://github.com/dillonzq/LoveIt) | **v0.2.10** | 主题,已锁定 tag,放在 `themes/LoveIt` |
| 发布方式 | GitHub Pages | `master` 分支的 `/docs` 目录 |
| 评论 | [Valine](https://valine.js.org/) + LeanCloud | appId 已配置在 `config.toml` |
| 搜索 | lunr(中文分词) | 构建时生成 `docs/index.json` |

## 目录结构

```
├── config.toml        # 站点配置(含菜单、评论、SEO 等全部参数)
├── content/
│   ├── posts/         # 所有文章(一篇文章一个 .md 文件)
│   └── about.md       # 关于页
├── static/            # 静态资源(favicon 等,直接拷贝到站点根)
├── themes/LoveIt/     # 主题(v0.2.10,一般不要改)
├── docs/              # 构建产物 = GitHub Pages 发布目录(勿手改)
├── bin/hugo.exe       # 本地 Hugo 二进制(已 gitignore,可删)
└── scripts/extract.py # 2026 年源码重建脚本(留档)
```

## 写一篇新文章

```bash
# 1. 新建文章(文件名决定 URL,如 my-post.md -> /my-post/)
./bin/hugo.exe new posts/我的新文章.md
# 2. 编辑 content/posts/我的新文章.md,把 draft: true 改为 false
# 3. 本地预览(浏览器打开 http://localhost:1313/)
./bin/hugo.exe server -D
# 4. 构建并发布:构建输出到 docs/,连同源文件一起提交推送
./bin/hugo.exe
git add -A && git commit -m "new post" && git push
```

push 后 1-2 分钟,GitHub Pages 自动更新 https://silencehuliang.github.io/

### 文章 front matter 模板

```markdown
---
title: "文章标题"
date: 2026-10-06T00:00:00+08:00
lastmod: 2026-10-06T00:00:00+08:00
draft: false
categories: ["分类名"]
tags: ["标签1", "标签2"]
description: "摘要(可选)"
featuredImage: ""      # 头图(可选)
toc:
  enable: true
math:
  enable: false
---

正文支持 Markdown + LoveIt 短代码(提示块、折叠块等),如:

{{< admonition tip "小贴士" >}}
提示内容
{{< /admonition >}}
```

> 注意:图片请勿再使用新浪图床(已全面防盗链),建议传到自己的
> [Picture_bed](https://github.com/Silencehuliang/Picture_bed) 仓库走 jsDelivr/GitHub raw 引用。

## 升级 Hugo / 主题(谨慎)

- Hugo 升级:下载新版 [extended](https://github.com/gohugoio/hugo/releases) 覆盖 `bin/hugo.exe`,
  本地构建后全站对比无异常再发布。LoveIt 0.2.10 与 0.74.3 是经过验证的组合。
- 主题升级:LoveIt 大版本(0.3.x)配置结构有变化,升级前先读主题 CHANGELOG。

## 已知问题与处理记录

1. **历史图片全部失效(未解决)**:全站 74 张文章配图存于新浪图床(tva*.sinaimg.cn),
   现已 403 防盗链无法访问,Wayback Machine 也无存档。找回途径:
   - 找到当年写作时的本地原图(Typora 默认保留本地副本);
   - 或有空时补图/删图。另有 1 张图链接写的是 `127.0.0.1:8000`(tornado 系列文章),本来就是无效链接。
2. **favicon 缺失(已修复)**:原站 head 引用了 favicon 但从未上传,2026-10 补了一
   套(生成于 `static/`,可自行替换)。
3. **主页 GitHub 链接拼接错误(已修复)**:原配置 `social.GitHub` 填了完整 URL,
   导致渲染成 `https://github.com/https://github.com/Silencehuliang`,已改为用户名。
4. **源码重建说明**:原始 Hugo 源仓库已遗失,GitHub 上只有构建产物 `docs/`。
   2026-10 用 `scripts/extract.py` 从 134 篇发布页反推出 Markdown 源文件与
   `config.toml`,重建后全站文本与线上版本相似度 99.7%(差异仅为 HTML 实体
   写法等视觉等价形式)。

## 快速排错

- `Error: TOCSS: failed to transform ...`:用了非 extended 版 Hugo。
- 构建后图片 404:检查 `content` 里图片链接与 `static/` 目录。
- 评论加载不出:LeanCloud 控制台确认应用未停用、域名白名单含
  `silencehuliang.github.io`。
