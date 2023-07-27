# Win下利用DockerDesktop打造Linux开发环境

## 开发环境要求
1. 基于Ubuntu或者Debian，系统源改为国内源，
2. 系统时间为东八区
3. 安装node、golang、python，源都改为国内源
4. 使用ssh秘钥登录，方便vscode链接
5. 生产目录映射到宿主机目录，防止工作数据丢失
6. 暴露端口数至少40个，以满足折腾需求
7. 解决中文乱码问题
## 符合要求的Dockerfile
参考此链接：https://blog.csdn.net/shykevin/article/details/105305322
```dockerfile
FROM node:19-bullseye-slim
# 修改更新源为阿里云
RUN sed -i "s@http://\(deb\|security\).debian.org@http://mirrors.163.com@g" /etc/apt/sources.list
# ADD . /
# 时区为上海
ENV TZ Asia/Shanghai

# 设置时区,设置utf-8编码
RUN apt-get update && apt-get install -y tzdata locales python3-pip cron openssh-server python3 curl wget git && apt-get clean all && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    locale-gen en_US.UTF-8 && mkdir ~/.pip&&touch ~/.pip/pip.conf

# 将pip国内源配置文件写入~/.pip中
RUN echo '[global]'>~/.pip/pip.conf \
echo 'index-url = http://pypi.douban.com/simple'>>~/.pip/pip.conf \
echo 'trusted-host = pypi.douban.com'>>~/.pip/pip.conf


# 解决中文乱码问题
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment && \
	echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
	echo "LANG=en_US.UTF-8" > /etc/locale.conf && \
	locale-gen en_US.UTF-8

# 安装golang     &&source /root/.bashrc
RUN curl -L https://gitee.com/blackelk/update-golang/raw/master/update-golang.sh | bash

#设置go国内源
RUN /root/.go/bin/go env -w GO111MODULE=on && \
    /root/.go/bin/go env -w GOPROXY=https://goproxy.cn,direct

# 设置npm国内源
RUN npm config set registry https://mirrors.huaweicloud.com/repository/npm/

# 开启ssh服务
RUN service ssh start
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "root:123" | chpasswd

RUN mkdir -p /workdir
VOLUME /workdir
EXPOSE 22
EXPOSE 8000-9000
# /etc/init.d/ssh start
ENTRYPOINT service ssh restart && bash 
```

