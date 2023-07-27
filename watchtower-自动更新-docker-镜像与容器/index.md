# Watchtower - 自动更新 Docker 镜像与容器


转载自：https://p3terx.com/archives/docker-watchtower.html

## 前言

Docker 容器的部署有一种在手机上装 App 的感觉，但 Docker 容器并不会像手机 App 那样会自动更新，而如果我们需要更新容器一般需要以下四个步骤：

- 停止容器：`docker stop <CONTAINER>`
- 删除容器：`docker rm <CONTAINER>`
- 更新镜像：`docker pull <IMAGE>`
- 启动容器：`docker run <ARG> ... <IMAGE>`

停止容器这个步骤可以在删除容器时使用 `-f` 参数来代替，即使这样还是需要三个步骤。如果部署了大量的容器需要更新使用这种传统的方式工作量是巨大的。

[Watchtower](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL2NvbnRhaW5ycnIvd2F0Y2h0b3dlcg) 是一个可以实现自动化更新 Docker 基础镜像与容器的实用工具。它监视正在运行的容器以及相关的镜像，当检测到 reg-istry 中的镜像与本地的镜像有差异时，它会拉取最新镜像并使用最初部署时相同的参数重新启动相应的容器，一切好像什么都没发生过，就像更新手机上的 App 一样。

## 快速开始

Watch-tower 本身被打包为 Docker 镜像，因此可以像运行任何其他容器一样运行它：

```bash
docker run -d \
    --name watchtower \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower
```

然后所有容器都会自动更新，也包括 Watch-tower 本身。

## 选项参数



<details style="display: block; color: rgb(238, 238, 238); font-family: BlinkMacSystemFont, &quot;Microsoft YaHei&quot;, &quot;Segoe UI&quot;, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;; font-size: 15.96px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(17, 61, 61); text-decoration-style: initial; text-decoration-color: initial;"><summary style="display: list-item;">点击查看</summary></details>



## 自动清除旧镜像

官方给出的默认启动命令在长期使用后会堆积非常多的标签为 `none` 的旧镜像，如果放任不管会占用大量的磁盘空间。要避免这种情况可以加入 `--cleanup` 选项，这样每次更新都会把旧的镜像清理掉。

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower \
    --cleanup
```

`--cleanup` 选项可以简写为 `-c`：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c
```

## 选择性自动更新

某些容器可能需要稳定的运行，经常更新或重启可能会造成一些问题，这时我们可以使用一些选项参数来选择与控制容器的更新。

### 容器更新列表

假设我们只想更新 `nginx`、`redis` 这两个容器，我们可以把容器名称追加到启动命令的最后面，就像下面这个例子：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    nginx redis
```

博主觉得把需要更新的容器名称写在启动命令中不利于管理，于是想了个更好的方法，建立一个更新列表文件。

```bash
$ cat ~/.watchtower.list
aria2-pro
unlockmusic
mtg
...
```

通过变量的方式去调用这个列表：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    $(cat ~/.watchtower.list)
```

这样只需要调整列表后删除 Watch-tower 容器并重新执行上面的命令重新启动 Watch-tower 即可。

### 设置单个容器自动更新特征

给容器中添加 `com.centurylinklabs.watchtower.enable` 这个 LA-BEL 并设置它的值为 `false`，或者在启动命令中加入 `--label com.centurylinklabs.watchtower.enable=false` 参数可以排除相应的容器。下面这个例子是博主的 `openwrt-mini` 镜像的容器启动命令，Watch-tower 将永远忽略它的更新，即使它包含在自动更新列表中。

```bash
docker run -d \
    --name openwrt-mini \
    --restart always \
    --network openwrt \
    --privileged \
    --label com.centurylinklabs.watchtower.enable=false \
    p3terx/openwrt-mini \
    /sbin/init
```

当容器启动命令中加入 `--label com.centurylinklabs.watchtower.enable=true` 参数，并且给 Watch-tower 加上 `--label-enable` 选项时，Watch-tower 将只更新这些包含此参数的容器。

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --label-enable
```

`--label-enable` 可以简写为 `-e`：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -ce
```

因为需要在容器启动时进行设置，且设置后就无法直接更改，只能重建容器，所以这种方式的灵活性不如更新列表法。尤其是在设置 `com.centurylinklabs.watchtower.enable=false` 参数后容器将永远被 Watch-tower 忽略，也包括后面将要提到的手动更新方式，所以一般不推荐这样做，除非你愿意手动重建的原生方式更新。

## 设置自动更新检查频率

默认情况下 Watch-tower 每 5 分钟会轮询一次，如果你觉得这个频率太高了可以使用如下选项来控制更新检查的频率，但二者只能选择其一。

- `--interval`, `-i` - 设置更新检测时间间隔，单位为秒。比如每隔 1 个小时检查一次更新：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --interval 3600
```

- `--schedule`, `-s` - 设置定时检测更新时间。格式为 6 字段 Cron 表达式，而非传统的 5 字段，即第一位是秒。比如每天凌晨 2 点检查一次更新：

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --schedule "0 0 2 * * *"
```

## 手动更新

前面的使用方式都是让 Watch-tower 以 `detached`（后台）模式在运行并自动更新容器，而 Watch-tower 也支持以 `foreground`（前台）模式来使用，即运行一次退出并删掉容器，来实现手动更新容器。这对于偶尔更新一次那些不在自动更新列表中的容器非常有用。

对于 `foreground` 模式，需要加上 `--run-once` 这个专用的选项。下面的例子 Docker 会运行一次 Watch-tower 并检查 `aria2-pro` 容器的基础镜像更新，最后删掉本次运行创建的 Watch-tower 容器。

```bash
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --run-once \
    aria2-pro
```

`--run-once` 可以简写为 `-R`：

```bash
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -cR \
    aria2-pro
```

需要注意的是当这个容器设置过 `com.centurylinklabs.watchtower.enable=false` 参数时不会更新。

## 尾巴

以上是博主在使用 Watch-tower 中总结的一些使用方式和方法，当然它还有一些其它的功能与使用方式，比如电子邮件通知、监视私人注册表的镜像、更新远程主机上的容器等，这些对于一般用户来说可能很少会用到，所以这里就不赘述了，感兴趣的小伙伴可以去研究 [Watchtower 官方文档](https://p3terx.com/go/aHR0cHM6Ly9jb250YWlucnJyLmdpdGh1Yi5pby93YXRjaHRvd2VyLw)。
