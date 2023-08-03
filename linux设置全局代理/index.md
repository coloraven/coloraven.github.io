# Linux设置全局代理




cover:
---

所有shell
这种情况可以修改/etc/profile、/etc/environment、、HOME/.bashrc、HOME/.zshrc配置文件，一般来说，只需要修改.bashrc或.zshrc就可以使所有的shell走代理（除非特殊情况）。

```shell
# set
export {http,https}_proxy="http://127.0.0.1:1280"
# unset
unset {http,https}_proxy
# test
curl -v checkip.dyndns.org
curl --head -v www.google.com
```

若希望立即见效，则?source 或HOME/.zshrc?或?sourceHOME/.bashrc。

因为linux终端不支持sock5，需要使用privoxy将HTTP流量转到本地sock5代理端口

1.安装Privoxy

```shell
sudo apt-get install privoxy
```

2.配置Privoxy
修改/etc/privoxy/config文件（先清空原文件内容，再将以下内容粘贴进去）

```yaml
user-manual /usr/share/doc/privoxy/user-manual
confdir /etc/privoxy
logdir /var/log/privoxy
actionsfile match-all.action # Actions that are applied to all sites and maybe overruled later on.
actionsfile default.action   # Main actions file
actionsfile user.action      # User customizations
filterfile default.filter
filterfile user.filter      # User customizations
logfile logfile
toggle  1
enable-remote-toggle  0
enable-remote-http-toggle  0
enable-edit-actions 0
enforce-blocks 0
buffer-limit 4096
enable-proxy-authentication-forwarding 0
forwarded-connect-retries  0
accept-intercepted-requests 0
allow-cgi-request-crunching 0
split-large-forms 0
keep-alive-timeout 5
tolerate-pipelining 1
socket-timeout 300
#listen-address  127.0.0.1:8118
#listen-address  [::1]:8118
listen-address  0.0.0.0:8118
forward-socks5 / 127.0.0.1:1280 .
```

3.重载配置文件

```shell
sudo service privoxy restart
```

二、设置全局代理
1.使用Privoxy将Socks5代理转换为http代理
详细步骤参考使用树莓派建立公共Http代理服务器
2.输入以下命令

```shell
export http_proxy=127.0.0.1:8118
export https_proxy=127.0.0.1:8118
export ftp_proxy=127.0.0.1:1280
```

http和https协议走Privoxy的http代理，ftp协议可以走socks代理

3.设置为默认代理
将上述命令添加到/etc/profile 文件末端，就可以使每次开启终端都自动设置代理。

```bash
vi /etc/profile 
```

在后面添加如下内容：

```yaml
export http_proxy=127.0.0.1:8118
export https_proxy=127.0.0.1:8118
export ftp_proxy=127.0.0.1:1280
```

添加完成后保存退出，执行以下命令即可生效。

```shell
source /etc/profile
```

4.部分程序需要单独设置，如git
