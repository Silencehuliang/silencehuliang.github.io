# 用GitHub Actions把Docker镜像转存到阿里云


## 前言

这两年国内拉 Docker Hub 镜像越来越难，官方源基本拉不动，各种加速器也是时好时坏。家里有几台自用的服务器要拉镜像，被折磨了几次之后，我决定用 GitHub Actions 搭一条"镜像搬运"线路：让 GitHub 的服务器把国外镜像拉下来，推到阿里云的私有镜像仓库，国内服务器再从阿里云拉。

方案本身基于开源项目 [docker_image_pusher](https://github.com/technology-shrimp/docker_image_pusher)（作者技术爬爬虾），我只是按自己的需求做了部署和调优。这里把原理和踩坑记录一下。

## 原理

整个流程非常简单，三步：

1. 在一个文本文件里列出要转存的镜像名，比如 `nginx:latest`、`grafana/grafana:10.0.0`
2. GitHub Actions 定时/手动触发一个 workflow：对每个镜像执行 `docker pull` → `docker tag` 成阿里云仓库地址 → `docker push`
3. 国内服务器从阿里云私有仓库 `docker pull`

相当于借了 GitHub 机器的"国际网络"和阿里云仓库的"国内高速"。

## 配置要点

阿里云侧:

- 开通**容器镜像服务**，创建命名空间和个人版仓库（个人版免费，额度完全够用）
- 生成固定密码，配到 GitHub 仓库的 Secrets 里（不要明文写在 workflow 里）

GitHub 侧:

- 镜像列表一个仓库一行，支持 `gcr.io`、`ghcr.io`、`k8s.io` 等前缀
- Actions 里对每个镜像顺序执行 pull/tag/push，失败的要收集起来最后汇总，方便下次重试

```yaml
- name: Pull and Push image
  run: |
    echo "${{ secrets.ALIPASSWORD }}" | docker login --username=${{ secrets.ALIUSERNAME }} --password-stdin registry.cn-hangzhou.aliyuncs.com
    docker pull ${image}
    docker tag ${image} registry.cn-hangzhou.aliyuncs.com/myns/${image}
    docker push registry.cn-hangzhou.aliyuncs.com/myns/${image}
```

## 踩过的坑

1. **GitHub Actions 的并发与时长限制**：免费额度对公开仓库基本够用，但一次塞太多大镜像容易超时，建议分批。
2. **镜像名里的坑**：有的镜像 tag 带 `@sha256:` 摘要，tag/rename 的时候要原样保留；官方镜像（无 namespace 的 `nginx`）要补上 `library/`。
3. **阿里云个人版仓库数有上限**：每个镜像一个仓库名，超过 1000 个要清理或改用同一仓库多 tag 的方式。
4. **不要无脑转存 latest**：有条件的话固定版本号，否则哪天上游更新把你的服务搞挂了都不知道。

## 小结

这套东西搭好之后，国内服务器拉镜像又回到了"秒拉"的舒爽状态，而且完全免费。本质上还是白嫖了 GitHub Actions 的算力和阿里云的存储，感谢开源社区。原始项目地址:<https://github.com/technology-shrimp/docker_image_pusher>

