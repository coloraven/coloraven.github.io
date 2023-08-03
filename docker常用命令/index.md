# Docker常用命令


## 进入正在运行的容器中

```bash
docker exec -it 1f6091e48979 /bin/sh
```

## 列出本地容器镜像

（包括运行中的容器使用的镜像和未运行的静态镜像文件）

```bash
docker image ls
```

## 查看容器的run参数

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike YOUR-CONTAINER-Name
```

## 重启整个docker服务（非重启容器）

，可解决容器运行久后，长期占用内存而不释放的问题。

```bash
systemctl restart  docker
```

## 修改容器重启策略，

portainer面板中可以修改

```bash
docker update --restart=on-failure:3 abebf7571666 hopeful_morse
```

## 更多请参考
http://honshen.xyz/2021/02/02/Docker/%E7%AC%AC2%E7%AB%A0-Docker%E7%9A%84%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4%E9%9B%86/
