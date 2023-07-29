# JD签到部署自动CK服务

## 部署教程
### 1、安装必要的运行环境
```bash
yum install wget unzip -y
```

### 2、下载工具使用的相关文件
```bash
# 首先进入我们上篇文章将的docker目录（以下教程我们将从root目录开始）
cd ..
cd docker

# 创建目录放配置以及chromium
mkdir nolanjdc && cd nolanjdc

# 下载config.json 配置文件 并且修改自己的配置 不能缺少（以下二选一即可）
# 魔法网络环境
wget -O Config.json  https://raw.githubusercontent.com/NolanHzy/nvjdc/main/Config.json
#大陆网络环境
wget -O Config.json   https://ghproxy.com/https://raw.githubusercontent.com/NolanHzy/nvjdc/main/Config.json

# 创建chromium文件夹并进入
mkdir -p  .local-chromium/Linux-884014 && cd .local-chromium/Linux-884014

# 下载chromium文件
wget https://mirrors.huaweicloud.com/chromium-browser-snapshots/Linux_x64/884014/chrome-linux.zip && unzip chrome-linux.zip

# 删除刚刚下载的压缩包
rm  -f chrome-linux.zip

# 回到刚刚创建的nolanjdc目录
cd ..
cd ..

# 拉镜像（目前最新0.5版本）
docker pull nolanhzy/nvjdc:0.5
# 博主在拉取的时候失败了好几次，大家失败了也可以多拉取几次
```

### 3、修改配置文件
```bash
# 使用vi修改配置文件，修改方法参考文件内的注释
vi Config.json
```
配置文件参考：
```json
{
  ///浏览器最多几个网页
  "MaxTab": "4",
  //网站标题
  "Title": "京东自动签到登录",
  //网站公告
  "Announcement": "本项目脚本收集于互联网。为了您的财产安全，请关闭京东免密支付！",
  ///XDD PLUS Url  http://IP地址:端口/api/login/smslogin
  "XDDurl": "",
  ///xddToken
  "XDDToken": "",
  ///青龙配置 注意 如果不要青龙  Config :[]
  "Config": [
    {
      //序号必填从1 开始
      "QLkey": 1,
      //服务器名称
      "QLName": "XX之家",
      //青龙地址，末尾不能是 '/'，此处因为和青龙面板在同一个主机，并且使用--link到了青龙面板，所以使用本地地址
      "QLurl": "http://ql:5700",
      //青龙2,9 OpenApi Client ID
      "QL_CLIENTID": "2puJ",
      //青龙2,9 OpenApi Client Secret
      "QL_SECRET": "lEfJqbe2OKG",
      //CK最大数量
      "QL_CAPACITY": 40,
      "QRurl": ""
    }
  ]
}
```
clientid与secret获取方式如下图：
![2021-11-07T225930](2021-11-07T225930.png)
### 4、启动NVJDC
```bash
# Docker启动命令
docker run --name nolanjdc -p 5679:80 -d  -v  /userdatas/Sandisk/jd/nolanjdc/Config.json:/app/Config/Config.json:ro -v /userdatas/Sandisk/jd/nolanjdc/.local-chromium:/app/.local-chromium --link=qinglong:ql -itd --privileged=true  nolanhzy/nvjdc:0.5

# 启动完成后使用以下命令查看输出日志
docker logs -f nolanjdc
```

转载自：https://6b7.org/391.html
参考：https://www.kejiwanjia.com/jiaocheng/32627.html
