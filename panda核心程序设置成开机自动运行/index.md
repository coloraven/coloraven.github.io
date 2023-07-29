# Panda核心程序设置成开机自动运行

## 自建开机启动脚本
将`ss-local`和`bypass-lan-china.acl`放入`/usr/bin/`（环境变量path）中
在 `/etc/init.d/` 中创建自己的开机运行脚本
> 这里的文件名 mystart 可以修改为任何你喜欢的名称，但是必须放在/etc/init.d/目录中
```bash
cd /etc/init.d
sudo vim /etc/init.d/proxy.sh
```
写入需要执行的命令,ss-local无需root权限
```bash
#!/bin/bash
### BEGIN INIT INFO
# Provides:          tuzixini
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: self define auto start
# Description:       self define auto start
### END INIT INFO
```
> 上面的部分也必须写上，后面放上你需要开机执行的命令，这里是挂载一个硬盘
```bash
ss-local  -s [服务器IP] -p [服务端端口] -b 0.0.0.0 -l [本地端口] -k [密码] -m chacha20-ietf-poly1305 --acl bypass-lan-china.acl
```
修改脚本文件权限(将命令中的mystart.sh替换成实际的脚本文件名称)
```bash
sudo chmod 755 /etc/init.d/proxy.sh
```

加入开机启动(将命令中的mystart.sh替换成实际的脚本文件名称)
```bash
sudo update-rc.d proxy.sh defaults 90
```

ok，完成，后面系统启动的时候就会自动运行这段命令。

CentOS系统：
将要开机启动的脚本放入`/etc/rc.d/init.d`中
```bash
cd /etc/rc.d/init.d
chkconfig --add 要开机启动的脚本.sh
chkconfig 要开机启动的脚本.sh on
```
## 替换shadowsock-lib包
### 使用linux系统包管理命令安装shadowsock-lib
```bash
apt install shadowsocks-libev
```
### 替换`ss-local`
进入`/usr/bin`目录，里面会有`shadowsocks-libev`的核心程序`ss-local`，将其替换成`panda`的核心二进制文件`ss-local`。

然后，编辑`/etc/shadowsocks-libev/config.json`:
```json
{
    "server":"122.xx.xx.9",
    "server_port":10xx,
    "local_port":128xx,
    "local_address":"0.0.0.0",
    "password":"sslslsllslslslslssl",
    "timeout":60,
    "method":"chacha20-ietf-poly1305"
}
```

shadowsock-libev的安装与配置文件的修改，参考：
https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux%E7%A7%91%E5%AD%A6%E4%B8%8A%E7%BD%91/#pc-%E8%BF%9E%E6%8E%A5%E5%88%B0-ssr-local


https://wiki.archlinux.org/title/Shadowsocks

centos 安装
https://zzz.buzz/zh/gfw/2018/03/21/install-shadowsocks-client-on-centos-7/
