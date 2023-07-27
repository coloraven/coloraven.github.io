# Docker部署IP和地址行政区域归属查询工具


## 构建Dockerfile

Dockerfile如下

```dockerfile
FROM postgis/postgis:13-3.1-alpine
WORKDIR /app
RUN apk --update --no-cache add python3-dev libffi-dev gcc musl-dev make libevent-dev build-base py3-pip python3 \
    &&pip install wheel \
    &&pip install gevent \
    &&pip install --no-cache-dir flask gunicorn shapely aiohttp psycopg2 \
    &&apk del python3-dev libffi-dev gcc musl-dev make libevent-dev build-base
COPY . .
EXPOSE 8848 5432
CMD gunicorn app:app -c gunicorn.conf.py
```

因为构建镜像基于alpine，遇到安装上面代码中提到的python库文件错误时解放方案来源网络
alpine安装gevent成功：

```bash
apk --update --no-cache add python3-dev libffi-dev gcc musl-dev make libevent-dev build-base
```

来源https://stackoverflow.com/a/66952652

alpine python 安装psycopg2失败的解决方案：

```bash
apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
pip install psycopg2 ---no-cache-dir#不缓存安装
apk --purge del .build-deps #删掉编译库
```

https://www.codenong.com/46711990/

alpine python安装shapely失败的解决方案：

```bash
apk --update add build-base libxslt-dev
apk add --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gcc libc-dev geos-dev geos && \
    runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | xargs -r apk info --installed \
    | sort -u)" && \
    apk add --virtual .rundeps $runDeps
geos-config --cflags
```

来源：https://serverfault.com/questions/947044/installing-shapely-on-alpine-docker

alpine python 安装aiohttp失败的解决方案：

```bash
RUN apk add gcc g++ libffi-dev musl-dev \
    && python -m pip install --no-cache-dir brotlipy \
    && apk del gcc g++ libffi-dev musl-dev
```

## 创建镜像

第一步的Dockerfile和应用已经发布到github私有仓库Quer
下载该仓库，上传到服务器，解压并执行以下命令创建镜像

```bash
docker build -t ipquery:3.0 . 
```

## 运行容器

```bash
docker run -itd --name=ipquery -p 8848:8848 -p 54321:5432 -e POSTGRES_PASSWORD=password ipquery:3.0
```

## 导入数据

具体参照`http://www.sirliu.top:8000/archives/81/`
数据库客户端Navicat连接postgis，新建数据库`csgeo`该名称已在代码中写死该名称已在py代码中写死，不可更改，并将数据库设置为地理空间数据库，具体方法见上面链接文章。

## 结束
