# 如何给已经运行的容器添加映射路径


类似地，貌似通过修改容器配置文件，可以实现端口映射等其他最初运行容器时未设置的参数。
端口映射的修改请看：[如何给已运行容器修改 / 添加端口映射](http://www.baidu.com/Docker/30.html)

## 方法一 通过修改已有容器配置文件实现

### 准备

如果要操作的容器在运行，停掉正在运行的容器

### 第一步

获取容器所使用的镜像`ID`

```bash
docker inspect 容器名称|grep Id
```

镜像ID形如：`bde9b0f3a3a40521e60f10dfbce9a15d3ea0d0708ef65c303cea73656fbc5acb`

### 第二步

打开已停止容器的配置文件, 配置文件位置：`/var/lib/docker/containers/第一步获取到的镜像ID/config.v2.json` 旧版本的可能是旧版本的docker可能是config.json.

### 第三步

找到`MountPoints`区域,未做过路径映射的应该是空的: `"MountPoints":{}`，然后用形如如下格式的内容替换你可以从其他做过路径映射的容器的配置文件中获取你可以从其他做过路径映射的容器的配置文件中获取:

```json
"MountPoints": {
      "/mnt": {                               # 容器路径
      "Source": "/home/<user-name>",          # 宿主机路径
      "Destination": "/mnt",                  # 容器路径
      "RW": true,
      "Name": "",
      "Driver": "",
      "Type": "bind",
      "Propagation": "rprivate",
      "Spec": {
        "Type": "bind",
        "Source": "/home/<user-name>",        # 宿主机路径
        "Target": "/mnt"                      # 容器路径
      },
      "SkipMountpointCreation": false
    }
  }
```

### 第四步

重启整个 docker 服务: `service docker restart`

## 方法二 通过将现有容器提交为镜像实现

### 第一步

停掉要操作的容器`docker stop 容器名字`。
`docker ps -a`获取该容器的容器ID

### 第二步

将当前容器提交为新的镜像`docker commit 容器ID 指定新的镜像名称（须与原来的不同）`

### 第三步

在第二步创建的镜像上重新运行容器（经过实验，原来的映射等参数均丢失，需要全部重新指定）

```bash
docker run -it -v "$PWD/somedir":/somedir 新容器名称 /bin/bash
```

原文在此，仅作翻译：https://stackoverflow.com/a/53516263
