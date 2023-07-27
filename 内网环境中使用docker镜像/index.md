# 内网环境中使用Docker镜像

### 背景
内网环境（与互联网隔离）或者无网络的电脑上已经安装好`docker demon`，现在需要将互联网中的镜像拷贝到内网主机上运行。操作如下：
最关键的是，学会使用 `docker` 的 `save` 命令。

你需要做的主要有 3 步骤：
1.先从一个有网络的电脑下载 `docker` 镜像
`docker pull centos`
2.保存镜像到本地文件
`docker save -o centos_image.docker centos`
3.把镜像拷贝到无网络的电脑，然后通过 `docker` 加载镜像即可。
`docker load -i centos_image.docker`

来源：https://blog.csdn.net/wangkai_123456/article/details/78538168
