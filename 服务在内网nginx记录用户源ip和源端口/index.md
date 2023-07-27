# 服务在“内网”，nginx记录用户源IP和源端口


转载自https://www.cnblogs.com/linuxk/p/12033796.html

## 服务器架构前面加了防火墙，Nginx如何获取客户端真实ip？？？

在大部分实际业务场景中，网站访问请求并不是简单地从用户（访问者）的浏览器直达网站的源站服务器，中间可能经过所部署的CDN、高防IP、WAF等代理服务器。例如，网站可能采用这样的部署架构：用户 > CDN/高防IP/WAF > 源站服务器。这种情况下，访问请求在经过多层加速或代理转发后，源站服务器该如何获取发起请求的真实客户端IP？

一般情况下，透明的代理服务器在将用户的访问请求转发到下一环节的服务器时，会在HTTP的请求头中添加一条X-Forwarded-For记录，用于记录用户的真实IP，其记录格式为X-Forwarded-For:用户IP。如果期间经历多个代理服务器，则X-Forwarded-For将以该格式记录用户真实IP和所经过的代理服务器IP：X-Forwarded-For:用户IP, 代理服务器1-IP, 代理服务器2-IP, 代理服务器3-IP, ……。

因此，常见的Web应用服务器可以使用X-Forwarded-For的方式获取访问者真实IP。

**Nginx配置方案**

- 1、确认nginx安装时已经安装http_realip_module模块

为实现负载均衡，Nginx使用http_realip_module模块来获取真实IP。`# nginx -V | grep http_realip_module`命令查看是否已安装该模块。如未安装，则需要重新编译Nginx服务并加装该模块。方法如下：

```bash
wget http://nginx.org/download/nginx-1.14.2.tar.gz
tar zxvf nginx-1.14.2.tar.gz
cd nginx-1.14.2
./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --without-http-cache --with-http_ssl_module --with-http_realip_module
make
make install
kill -USR2 `cat /usr/local/nginx/logs/nginx.pid`
kill -QUIT `cat /usr/local/nginx/logs/ nginx.pid.oldbin`
```

- 2、修改Nginx对应server的配置

打开www.conf配置文件，在location / {} 中加入以下内容：

```bash
set_real_ip_from ip_range1;    #真实服务器上一级代理的IP地址或者IP段,可以写多行
set_real_ip_from ip_range2;
...
set_real_ip_from ip_rangex;
real_ip_header    X-Forwarded-For;    #从哪个header头检索出需要的IP地址
real_ip_recursive on;    #递归排除set_real_ip_from里面出现的IP,其余没有出现的认为是用户真实IP
```

**说明:** 其中，ip_range1，2，...，x 指WAF的回源IP地址，需要分多条分别添加。

如何获取WAF的回源IP地址？？？

打开WAF界面-->设置-->产品信息-->即可查看到回源IP段，将这里的IP段按照上面的方式写进nginx配置当中即可，查看nginx访问日志就是客户端真实ip了。不过要说的是阿里的回源IP段真多，用notepad++处理好配置再写上去更方便！

- 3、修改日志记录格式

log_format一般在nginx.conf配置文件中的http配置部分。在log_format中，添加x-forwarded-for字段，替换原来remote-address字段，即将log_format修改为以下内容：

```bash
log_format  main  '$http_x_forwarded_for - $remote_user [$time_local] "$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" ';
```

Don't forget the beginner's mind
