# Docker搭建Jupyter服务


### 一、运行容器

````bash
docker run -itd --name=jupyter -v /userdatas/Sandisk/Jupyter:/home/jovyan -p 10000:8888 --restart=unless-stopped jupyter/minimal-notebook:latest
````



映射目录到宿主机：/userdatas/Sandisk/Jupyter
此容器的更多运行参数：https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#docker-options

### 二、修改宿主机目录权限

```bash
chown 1000:1000 /userdatas/Sandisk/Jupyter -R
```

### 三、生成密码的sha1值

在线生成https://tool.oschina.net/encrypt?type=2

### 四、修改配置文件

修改之前先进入容器里执行`jupyter notebook --generate-config`命令，就会在宿主机/userdatas/Sandisk/Jupyter/.jupyter目录下生成`jupyter_notebook_config.py`文件

或者
直接touch生成该文件，文件内容如下：

```python
c.NotebookApp.password = u'sha1:第三步生成的密码sha1值'
c.NotebookApp.password_required = True
```

### 最后，修改`jupyter_notebook_config.py`文件的权限

```python
chown 1000:1000 jupyter_notebook_config.py
```
