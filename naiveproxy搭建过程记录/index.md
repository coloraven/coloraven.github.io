# NaiveProxy搭建过程记录

原`Naiveproxy`的搭建脚本有个弊端，域名证书需要手动申请，比较蛋疼，这次找到的一键搭建脚本可以自动申请证书（暂时未找到到期续期的脚本，可以重置服务器，重新运行脚本来实现变相续期）。
脚本地址如下：https://github.com/crazypeace/naive
修改用户名密码：修改/etc/caddy/Caddyfile
```nginx
{
  order forward_proxy before file_server
}
:443, np.mydomain.com {
  tls e16d9cb045d7@gmail.com
  forward_proxy {
    basic_auth 用户名 密码
    hide_ip
    hide_via
    probe_resistance
  }
  file_server {
    root /var/www/html
  }
}
```
然后重启：`service caddy restart`
