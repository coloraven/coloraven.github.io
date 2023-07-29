# 【转载】基于alpine镜像构建自己的flask镜像


python官方镜像地址：

http://hub.docker.com/_/python

拉取官方的python镜像

```bash
docker pull python:3.7-alpine
```

交互式方式生成一个python容器

```bash
docker run -it --name python37 --rm python:3.7-alpine /bin/sh
```

进入交互式容器，查看当前python版本

```bash
python --version
```

设置pip的阿里云镜像源

```bash
mkdir $HOME/.pip/
 
tee $HOME/.pip/pip.conf <<-'EOF'
[global]
trusted-host=mirrors.aliyun.com
index-url=https://mirrors.aliyun.com/pypi/simple
EOF
```

确认一下是否配置成功

```bash
cat $HOME/.pip/pip.conf
```

我们的python使用的是alpine系统

`alpine`使用的是`apk`包管理器

命令如：

```bash
apk add
 
apk update
 
apk del
```

`alpine`默认的镜像源也比较慢，我们也换成国内的

设置alpine镜像源

```bash
echo http://mirrors.ustc.edu.cn/alpine/v3.7/main > /etc/apk/repositories
 
echo http://mirrors.ustc.edu.cn/alpine/v3.7/community >> /etc/apk/repositories
```

设置后要执行

```bash
apk update && apk upgrade
```

安装flask

```bash
python -m pip install -U flask
```

编写test.py

```python
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def hello():
    return 'Hello World!'
 
@app.route('/abc')
def abc():
    return 'Hello abc'
 
if __name__ == '__main__':
    app.run()
```

### 第一种执行这个py文件方式

```bash
python test.py
```

然后在另一个终端以交互式方式进入这个python容器

```bash
docker exec -it python37 /bin/sh
```

下载`curl`命令

```bash
apk add curl
```

使用`curl`访问`flask`服务

```bash
curl localhost:5000
 
curl localhost:5000/abc
```

### 第二种执行这个py文件的方式

```bash
# 设置环境变量
export FLASK_APP=/test.py

# flask运行起来
flask run
```

### 第三种执行这个py文件的方式

```bash
FLASK_APP=test.py flask run
```

## 根据上面的操作步骤，我们可以来编写Dockerfile生成自己的flask镜像

### 先退出上面的交互式容器，按：ctrl+D

创建一个flask目录，并进入

```bash
mkdir flask
cd flask
```

创建一个pip.conf文件，将pip镜像源写进去

```bash
tee pip.conf <<-'EOF'
[global]
trusted-host=mirrors.aliyun.com
index-url=https://mirrors.aliyun.com/pypi/simple
EOF
```

编写Dockerfile文件

```dockerfile
FROM python:3.7-alpine
RUN echo http://mirrors.ustc.edu.cn/alpine/v3.7/main > /etc/apk/repositories && \
    echo http://mirrors.ustc.edu.cn/alpine/v3.7/community >> /etc/apk/repositories
RUN apk update && apk upgrade
RUN mkdir $HOME/.pip/
COPY ./pip.conf $HOME/.pip/
RUN pip install flask
EXPOSE 5000
CMD ["flask", "run"]
```

执行docker build命令进行镜像构建

```bash
docker build -t myflask:1.0 .
```

确认是否构建成功

```bash
docker images
```

ok！镜像构建成功！

怎么运行？？

创建一个myapp目录

```bash
mkdir myapp
```

放入上面的test.py文件

```python
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def hello():
    return 'Hello World!'
 
@app.route('/abc')
def abc():
    return 'Hello abc'
 
if __name__ == '__main__':
    app.run()
```

然后通过刚刚构建的镜像生成我们的容器

```bash
docker run --name myapp --rm -d -p 8080:5000 -v ~/myapp:/app -e FLASK_APP=/app/test.py myflask:1.0
```

确认容器是否启动

```bash
docker ps
```

恩，启动了！

但是我们无法通过外网访问服务器ip的8080端口访问到容器里面

为什么？

`flash`默认只允许本机访问！

怎么办？

停掉刚刚生成的容器

```bash
docker stop myapp
```

重新生成容器，指定允许ip为0.0.0.0，然外部可以访问

```bash
docker run --name myapp --rm -d -p 8080:5000 -v ~/myapp:/app -e FLASK_APP=/app/test.py myflask:1.0 flask run -h 0.0.0.0
```

通过外网浏览器访问

```
http://服务器ip:8080
```

ok，可以访问到flask搭建的程序了！

原文链接：http://www.mi360.cn/articles/34
