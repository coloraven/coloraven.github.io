# Docker搭建VSCODE-Server


### 宿主机环境装备

先在宿主机建立用户数据目录

```bash
mkdir /userdatas/mycode
```

给上面目录授权（否则将会出现docker挂载该目录时拒绝访问的错误）

```bash
chmod 777 /userdatas/mycode
```

### 启动vscode-server容器

```bash
docker run -it -d \
  --restart=always \
  --name code-server -p 6688:8080 \
  -v "/userdatas/mycode:/home/coder" \
  codercom/code-server:latest
```

### 登录密码的修改

进入宿主机`/userdatas/mycode/.config/code-server`目录，其中`config.yaml`中password后面的值就是密码。

> 修改密码也是在此文件。
> 修改密码后，需要重启容器`docker restart code-server`才能生效。

访问xxx.xx:6688即可享用`vscode WebIDE`

## `Python`开发环境打磨

### 安装pip管理包

`vscode`服务端（即docker容器）是基于`debian`系统，未安装pip，需要进入容器中进行安装，进入容器的方法有两种。

#### 一、`WebIDE`界面进入

登录`WebIDE`后，在`WebIDE`的终端中进行。

```bash
sudo apt update
sudo apt install python3-pip
```

#### 二、在宿主机中进入

宿主机运行以下命令进入容器

```bash
docker exec -it code-server /bin/bash
```

然后执行 一、`WebIDE`界面安装 步骤中的代码。

### 配置远程调试运行环境

在`WebIDE`左侧的`插件`商店中安装`python`插件
重启容器`docker restart code-server`
然后再次进入`WebIDE`,进入左侧的`运行和调试`，点击`创建 launch.json`,在编辑界面输入以下内容并保存：

```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 当前文件",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "internalConsole"
        }
    ]
}
```

然后就可以按`Ctrl+F5`愉快的执行。

### 设置`WebIDE`不显示配置文件

在`WebIDE`的设置当中搜索`files.exclude`,添加一条规则`**/.*`

~~### 安装等宽字体`JetBrains Mono`~~
~~下载地址：`https://www.jetbrains.com/lp/mono/`~~
~~安装方法见：`https://blog.csdn.net/jiaobuchong/article/details/108891406`~~
