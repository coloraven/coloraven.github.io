# Docker搭建WebDAV服务


亲测可用的

```bash
docker run --name webdav -d \
--restart=unless-stopped \
-p 369:80 \
-v /mnt/data_part/webdav_server:/media \
-e USERNAME=你的账号 \
-e PASSWORD=你的密码 \
-e TZ=Aisa/Shanghai \
-e UDI=1000 \
-e GID=1000 \
ugeek/webdav:amd64
```


