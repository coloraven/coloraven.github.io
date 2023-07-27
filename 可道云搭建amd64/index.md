# 可道云+onlyoffice搭建【amd64+arm64】

## 运行可道云
`kodcloud/kodexplorer:latest`含`arm64`架构镜像
`docker run -d -p 3563:80 kodcloud/kodexplorer:latest`

## 运行`onlyoffice`
`docker run -i -t -d --name onlyoffice -p 5646:80 onlyoffice/documentserver`
官方只支持`amd64`
下面是支持`arm64`的第三方
`https://github.com/jiriks74/Docker-DocumentServer-Arm64`
对应镜像：`jiriks74/onlyoffice-documentserver-arm64`

## 下载'onlyoffice'插件
`https://github.com/sit17/kodexplorer_onlyoffice`

将下载好的压缩包解压，将`onlyoffice`目录丢入可道云的`plugins`目录中，再在插件中心启用。

然后插件中心点击`onlyoffice`插件进行配置，将`onlyoffice`地址填入其中。

## 免费版批量添加用户脚本（先复制好cookies）
```python
import requests


def add_user(name):
    cookies = {
        'KOD_SESSION_SSO': '3824713901f6ead71c6e2a0ec2feba74',
        'HOST': 'http%3A//192.168.1.100%3A3563/',
        'APP_HOST': 'http%3A//192.168.1.100%3A3563/',
        'kodUserLanguage': 'zh-CN',
        'KOD_SESSION_ID_7da51': '94b57f9211f2e95b82425f6c64d727a0',
        'X-CSRF-TOKEN': 'iYekIw5nXYfNzpnSkB4t',
        'kodUserID': '1',
        'kodToken': '75412d60d177626ad7211faf70c806ae',
        'kodVersionCheck': 'check-at-1652286052',
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-CSRF-TOKEN': 'iYekIw5nXYfNzpnSkB4t',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://192.168.1.100:3563',
        'Referer': 'http://192.168.1.100:3563/index.php?setting',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,zh-HK;q=0.6',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'KOD_SESSION_SSO=3824713901f6ead71c6e2a0ec2feba74; HOST=http%3A//192.168.1.100%3A3563/; APP_HOST=http%3A//192.168.1.100%3A3563/; kodUserLanguage=zh-CN; KOD_SESSION_ID_7da51=94b57f9211f2e95b82425f6c64d727a0; X-CSRF-TOKEN=iYekIw5nXYfNzpnSkB4t; kodUserID=1; kodToken=75412d60d177626ad7211faf70c806ae; kodVersionCheck=check-at-1652286052',
    }
    data = {
        'name': name, #先url编码
        'nickName': name,#先url编码
        'password': 'password',
        'sizeMax': '2',
        'role': '2',
        'groupInfo': '%7B%221%22%3A%22write%22%7D', # '{"1":"write"}',
    }
    response = requests.post('http://192.168.1.100:3563/index.php?systemMember/add', cookies=cookies, headers=headers, data=data, verify=False)

add_user('555')
```
