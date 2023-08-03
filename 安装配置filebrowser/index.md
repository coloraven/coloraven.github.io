# 安装配置Filebrowser


docker安装

```bash
docker run -itd \
--name=filebrowser \ # 镜像别名
-v /:/srv \ # filebrowser 管理的路径
-v /etc/filebrowser/config.json:/etc/config.json \ # filebrowser 配置
-v /etc/filebrowser/database.db:/etc/database.db \ # filebrowser 数据库
-p 80:80 \ # filebrowser 映射端口
filebrowser/filebrowser
```

一键安装脚本,下面的可以不用看了

```bash
bash <(curl -s -L https://233blog.com/filebrowser.sh)
```

另一个详细教程文章
https://233blog.com/post/26/

## 第一步

```bash
curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
```

## 第二步

生成初始化配置文件

```bash
sudo filebrowser -d /etc/filebrowser/filebrowser.db config init
```

## 第三步

修改配置文件（通过命令）

```bash
# 设置监听地址
sudo filebrowser -d /etc/filebrowser/filebrowser.db config set --address 0.0.0.0  
# 设置监听端口
sudo filebrowser -d /etc/filebrowser/filebrowser.db config set --port 8088
# 设置语言环境
sudo filebrowser -d /etc/filebrowser/filebrowser.db config set --locale zh-cn
# 设置日志位置
sudo filebrowser -d /etc/filebrowser/filebrowser.db config set --log /var/log/filebrowser.log
# 添加一个用户,其中的root和password分别是用户名和密码，根据自己的需求更改。
sudo filebrowser -d /etc/filebrowser/filebrowser.db users add root password --perm.admin
```

## 第四步

打开8088端口

```bash
firewall-cmd --zone=public --add-port=8088/tcp --permanent
# 开放端口后要重启防火墙生效
# 重启防火墙
systemctl restart firewalld
```

## 第五步 前台运行

启动file browser
配置修改好以后，就可以启动 File Browser 了，使用`-d`参数指定配置数据库路径，`-r`参数指定使用的目录。示例：

```bash
filebrowser -d /etc/filebrowser/filebrowser.db -r /tmp/
```

## 第六步 后台运行

File Browser 默认是前台运行，如何让它后台运行呢？

### 第一种 nohup 大法：

运行：`nohup filebrowser -d /etc/filebrowser.db >/dev/null 2>&1 &`

停止运行：`kill -9 $(pidof filebrowser)`

开机启动：`sed -i '/exit 0/i\nohup filebrowser -d \/etc\/filebrowser.db >\/dev\/null 2>&1 &' /etc/rc.local`

取消开机启动：`sed -i '/nohup filebrowser -d \/etc\/filebrowser.db >\/dev\/null 2>&1 &/d' /etc/rc.local`

### 第二种 systemd 大法（**推荐**）

编写service文件：`vi /etc/systemd/system/filebrowser.service`

> 参照：https://blog.csdn.net/ywd1992/article/details/93030495

ExecStart根据自己的实际目录修改

```
[Unit]
Description=File Browser
After=network.target

[Service]
ExecStart=/usr/local/bin/filebrowser -d /etc/filebrowser/filebrowser.db

[Install]
WantedBy=multi-user.target
```

然后输入

```bash
systemctl daemon-reload
systemctl start filebrowser
systemctl enable filebrowser
```

停止运行：`systemctl stop filebrowser`

开机启动：`systemctl enable filebrowser`

取消开机启动：`systemctl disable filebrowser`

查看运行状态：`systemctl status filebrowser`

我推荐使用 systemd 的方法来后台运行，当然，前提是你所使用的操作系统支持 systemd。

## HTTPS

File Browser 2.0 起开始内建 HTTPS 支持，只需要配置 SSL 证书即可。

配置 SSL：`filebrowser -d /etc/filebrowser.db config set --cert example.com.crt --key example.com.key`，其中`example.com.crt`和`example.com.key`分别是 SSL 证书和**路径，根据自身情况进行更改。配置完 SSL 后，只可以使用 HTTPS 访问，不可以使用 HTTP。

取消 SSL：`filebrowser -d /etc/filebrowser.db config set --cert "" --key ""`

当然，你也可以使用 Nginx 等 Web 服务器对 File Browser 进行反向代理，以达到 HTTPS 访问的目的。

还有就是使用 Caddy，这是一个开源、支持 HTTP/2 的 Web 服务器，它的一个显著特点就是默认启用 HTTPS 访问，会自己申请 SSL 证书，同时支持大量的插件，File Browser 就可以作为其插件运行。

参考：
https://blog.csdn.net/Homewm/article/details/87931165
https://www.pianshen.com/article/3979763347/
