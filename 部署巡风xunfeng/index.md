# 部署巡风[xunfeng]


https://github.com/ysrc/xunfeng/blob/master/docs/install/Docker.md

dokcer容器实验摸索结果：

1. /opt/xunfeng目录下含配置文件，其中`Config.py`定义web前端的登录账号密码及数据库端口、账号密码，内容如下

```python
class Config(object):
    ACCOUNT = 'admin'
    PASSWORD = 'xunfeng321'
 
class ProductionConfig(Config):
    DB = '127.0.0.1'
    PORT = 65521
    DBUSERNAME = 'scan'
    DBPASSWORD = 'scanlol66'
    DBNAME = 'xunfeng'
```

1. /data用于存放MongoDB数据库文件，扫描历史结果、POC漏洞插件设置情况等等都在此。

为了持久化扫描结果数据，建议将`/data`目录映射到宿主机

故启动参数如下：

```bash
docker run -d --name=xunfeng \
-p 8118:80 \
-p 2717:65521 \
-v /userdatas/Sandisk/xunfeng:/data \
ysrc/xunfeng:latest
```


