# 在线nginx配置生成工具和nginx配置UI管理工具




## 一、在线配置生成工具

https://www.digitalocean.com/community/tools/nginx?global.app.lang=zhCN

## 二、nginx配置webUI管理工具

> 均为docker容器部署

### nginx proxy manager

#### 优点

可容器化部署，轻量化（两个容器占用共71M+45M内存）、无汉化

#### 缺点

谈不上缺点的缺点----两个容器
https://nginxproxymanager.com/
部署：
新建docker-compose.yml

```yaml
version: '3'
services:
  app:
    container_name: NginxProxyManager-WEB
    image: 'jc21/nginx-proxy-manager:latest'
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    environment:
      DB_MYSQL_HOST: "db"
      DB_MYSQL_PORT: 3306
      DB_MYSQL_USER: "npm"
      DB_MYSQL_PASSWORD: "npm"
      DB_MYSQL_NAME: "npm"
    volumes:
      - /tmp/NginxProxyManager/data:/data
      - /tmp/NginxProxyManager/letsencrypt:/etc/letsencrypt
  db:
    container_name: NginxProxyManager-DB
    image: 'jc21/mariadb-aria:latest'
    environment:
      MYSQL_ROOT_PASSWORD: 'npm'
      MYSQL_DATABASE: 'npm'
      MYSQL_USER: 'npm'
      MYSQL_PASSWORD: 'npm'
    volumes:
      - /tmp/NginxProxyManager/mysql:/var/lib/mysql
```

然后在上述文件目录下执行：`docker-compose up -d`

如果已有数据库，则运行以下命令：

```bash
docker run -itd --name=NginxProxyManager-WEB \
--restart=unless-stopped \
--link=db \
-e DB_MYSQL_HOST: "db" \
-e DB_MYSQL_PORT: 3306 \
-e DB_MYSQL_USER: "npm" \
-e DB_MYSQL_PASSWORD: "npm" \
-e DB_MYSQL_NAME: "npm" \
-v /tmp/NginxProxyManager/data:/data \
-v /tmp/NginxProxyManager/letsencrypt:/etc/letsencrypt \
jc21/nginx-proxy-manager:latest
```

### nginx webui

#### 优点

国人使用JAVA开发的，语言友善，只有一个容器，便于管理

#### 缺点

占用资源很大（同样环境中该容器占用205M内存）
http://www.nginxwebui.cn/
