# trojan搭建

## trojan安装
### 先更新系统证书，否则再申请网站证书时会失败
```bash
yum update ca-certificates
```
### 再拉取运行脚本
```bash
source <(curl -sL https://git.io/trojan-install)
```

### `No route to host`错误的解决
症状：客户端能连上，一切正常，但是无法出境浏览网站。
排错：登录服务器查看日志，发现有`cannot establish connection to remote server www.google.com:443: No route to ho`报错记录。
`Google`搜索发现是因为`VPS`同时支持`IPV4`和`IPV6`导致的，详情见:https://github.com/trojan-gfw/trojan/issues/327
解决方案：在`/etc/gai.conf`中增加一行`precedence ::ffff:0:0/96  100`，然后`reboot`大法。

## xray一键脚本
```bash
bash <(curl -sL https://raw.githubusercontent.com/daveleung/hijkpw-scripts-mod/main/xray_mod1.sh)
```
