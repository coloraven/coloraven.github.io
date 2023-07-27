# 腾讯云函数Python依赖包安装打包过程

官方文档：https://cloud.tencent.com/document/product/583/39780
通过官方文档可知，在云函数在线编辑器那里可以启动终端并在终端中进行包的安装.......下文可以忽略了



## 背景
腾讯云函数运行环境提供的库有限，有些库需要自行打包好后上传才能使脚本正常运行，而本地打包时又对打包所处的环境有要求，因为腾讯云函数运行环境为`centos7`+`python3.6.1`，所以本地如果是`windows`+`python3.8`等非`centos7`+`python3.6.1`环境，可能会导致脚本不能运行，故需要临时使用`centos7`+`python3.6.1`环境来打包。

### 第一步：使用docker安装centos7+python3.6环境
来源：docker学习2-快速搭建centos7-python3.6环境
docker search python
## 此命令用来搜索与python有关的docker镜像
      结果如下：
[root@yoyo ~]# docker search python
NAME                             DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
python                           Python is an interpreted, interactive, objec…   4288                [OK]                
django                           Django is a free web application framework, …   847                 [OK]                
.....（人工省略）                                                     
centos/python-36-centos7         Platform for building and running Python 3.6…   17                                      
.....（人工省略） 
python 3.6.5 with requirements last update s…   0                                       
openshift/python-33-centos7      DEPRECATED: A Centos7 based Python v3.3 imag…   0                                       
[root@yoyo ~]#

上面找的想要下载的镜像centos/python-36-centos7,接下来下载到自己本地
docker pull centos/python-36-centos7


二、运行交互式的容器——可以直接在宿主机的终端进入并操作docker容器系统的终端（下称 docker 终端）
1、进入docker终端（宿主机终端）
docker run -i -t centos/python-36-centos7 /bin/bash

2、在docker容器里面安装pipreqs（docker 终端）
为避免国内网络环境下载速度慢，临时使用-i参数，指定国内下载源。
pip3 install pipreqs -i https://pypi.tuna.tsinghua.edu.cn/simple

3、将脚本从宿主机复制到docker容器里面（宿主机终端）。
docker cp 本地文件路径 ID全称:容器路径
         
        其中查看容器ID全称的命令为（宿主机终端）：
docker ps -a

4、然后在定位到复制进来的脚本所在目录，使用pipreqs来生成当前目录中脚本运行所需的requirements.txt（docker 终端）
pipreqs ./
## 如果是Windows系统，会报编码错误： 
## (UnicodeDecodeError: 'gbk' codec can't decode byte 0xa8 in position 24: illegal multibyte sequence)  
## 使用时，指定编码格式
pipreqs ./ --encoding=utf8

5、使用pip3将requirements.txt中的库安装到到当前目录（docker 终端）
pip3 install -r requirements.txt -t ./ -i https://pypi.tuna.tsinghua.edu.cn/simple
         
     经过步骤4-5，可能还是会有一些库文件没有被pipreqs识别，比如pymongo需要dnspython库不会被pipreqs识别，此时只要用pip3单独安装缺失的库到当前目录即可。
pip3 install dnspython -t ./ -i https://pypi.tuna.tsinghua.edu.cn/simple
6、将当前目录下所有内容打包成zip压缩文件——腾讯云函数只认zip格式的压缩包（docker 终端）
zip -r 压缩包文件名.zip ./*

7、将压缩包从docker容器复制到宿主机（宿主机终端）
docker cp ID全称:容器路径 本地文件路径

三、上传zip文件到云函数
      （完）.........
