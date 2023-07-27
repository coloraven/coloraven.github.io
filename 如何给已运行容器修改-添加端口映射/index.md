# 如何给已运行容器修改 \ 添加端口映射


### 准备

如果要操作的容器在运行，停掉正在运行的容器

### 第一步

获取容器所使用的镜像`ID`

```bash
docker inspect 容器名称|grep Id
```

镜像ID形如：`bde9b0f3a3a40521e60f10dfbce9a15d3ea0d0708ef65c303cea73656fbc5acb`

### 第二步

打开已停止容器的配置文件, 配置文件位置：`/var/lib/docker/containers/第一步获取到的镜像ID/hostconfig.json`.

### 第三步

找到`PortBindings`区域并根据需要修改:

```json
.......
    .
    .
    .
    "PortBindings": {
        "80/tcp": [{
            "HostIp": "",
            "HostPort": "8000"
        }]
    },
    "RestartPolicy": {
        "Name": "always",
        "MaximumRetryCount": 0
    },
    .
    .
    .
    .
.......
```

### 第四步

重启整个 docker 服务: `service docker restart`
