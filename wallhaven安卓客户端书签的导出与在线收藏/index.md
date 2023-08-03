# wallhaven安卓客户端书签的导出与在线收藏

<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/#code代码块 -->
<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/ -->
## 前言
最近折腾博客时，找到壁纸网站`wallhaven.cc`，官方没有手机客户端，只有第三方客户端，但是第三方客户端又不能在浏览图片时对喜欢的图片放入自己账号的收藏夹，而是作为本地`Bookmark`标记，一旦APP卸载，自己整理的喜欢的壁纸就丢失了。所以这里有两个概念：
- 1、本地书签（BookMark），跟着APP走
- 2、在线收藏（跟着账号走）
## APP下载链接
[谷歌商店地址](https://play.google.com/store/apps/details?id=net.softandroid.simplewallpapers)
## 将喜欢的图片加入本地书签
![加入本地书签](2021-10-06T090129.png)
## 导出书签
找到并进入书签界面
![2021-10-06T090210](2021-10-06T090210.png)
点击右上角更多（···），选择分享bookmark，发送到聊天工具即可。
![2021-10-06T090245](2021-10-06T090245.png)
## 用`py`脚本自动将本地书签转为在线收藏。
### 本地bookmark文件结构:
```json
[
    {
        "n": "j3y8pm",
        "o": "https://th.wallhaven.cc/lg/j3/j3y8pm.jpg",
        "r": 284,
        "s": 1632674055901,
        "p": "https://whvn.cc/j3y8pm",
        "q": "1920x1080"
    },
    {
        "n": "l3jqxl",
        "o": "https://th.wallhaven.cc/lg/l3/l3jqxl.jpg",
        "r": 116,
        "s": 1632674060537,
        "p": "https://whvn.cc/l3jqxl",
        "q": "1920x1080"
    }
]
```
### 登录`wallhaven.cc`
```python
def login():
    '''登录，获取token'''
    print('开始登录...')
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    login_index_url = 'https://wallhaven.cc/login'
    response = s.get(login_index_url, headers=header)
    html = response.text
    bf = BeautifulSoup(html, 'lxml')
    hidden = bf.find_all('input', {'type':'hidden'})
    for i in hidden:
        _token = i['value']
    data = {
        '_token' : _token,
        'username': '***', # 账号
        'password': '******'  # 密码
    }
    login_url = 'https://wallhaven.cc/auth/login'
    response = s.post(login_url, headers=header, data=data)
    if response.status_code == 200:
        print("login success")
        token = re.findall('<input type="hidden" name="_token" value="(.*?)">',response.text)[0]
        return token
    else:
        print('login failed')
        return response.status_code
```
### 构造`加入收藏`的链接
通过抓包图片详情页点击`Add to Favorites`的动作，发现加入收藏的链接已经在访问图片详情页时返回了，其链接格式如下：
`https://wallhaven.cc/favorites/add?wallHashid=图片ID&collectionId=收藏夹ID&_token=40位长度的字符串`
而且所有的图片收藏链接token都一致，猜测可能是登录后分配的统一token。
于是查看登录请求的返回源码发现确实有token返回，于是可以直接构造加入收藏的链接。
```python
f'https://wallhaven.cc/favorites/add?wallHashid={pic_hashid}&collectionId={collectionID}&_token={token}'
```
### 完整代码
结合收藏夹图片信息爬取去重：http://coloraven.github.io/2021/9/Wallhaven壁纸爬虫/#完整代码
```python
import requests,json,re,time
from bs4 import BeautifulSoup

s = requests.Session()

def login(userinfo):
    '''登录，获取token'''
    print('开始登录...')
    login_index_url = 'https://wallhaven.cc/login'
    response = s.get(login_index_url)
    html = response.text
    bf = BeautifulSoup(html, 'lxml')
    hidden = bf.find_all('input', {'type':'hidden'})
    for i in hidden:
        _token = i['value']
    data = {
        '_token' : _token,
    }
    data.update(userinfo)
    login_url = 'https://wallhaven.cc/auth/login'
    response = s.post(login_url, data=data, allow_redirects=False)
    username = response.headers['location'].split('/')[-1] # 获取跳转URL
    response = s.get(response.headers['location'])
    if response.status_code == 200:
        print("login success")
        token = re.findall('<input type="hidden" name="_token" value="(.*?)">',response.text)[0]
        return username,token
    else:
        print('login failed')
        return response.status_code


def  AddtoFav(pic_hashid,token,collectionID):
    """构造加入收藏的链接并请求"""
    s.headers.update({"referer": f"https://wallhaven.cc/w/{pic_hashid}"})
    favLink = f'https://wallhaven.cc/favorites/add?wallHashid={pic_hashid}&collectionId={collectionID}&_token={token}'
    r = s.get(favLink)
    if r.status_code==200:
        print('成功加入收藏')
        return 200
    elif r.status_code==429:
        print(r.text)
        return 429
    else:
        print(r.text)
        return 3


def GetCollectionPicIDs(apikey, collectionID, nickname):
    '''返回相应ID在线收藏夹中图片ID列表'''
    # 第一步获取改ID收藏夹的图片总条数
    params = { "apikey": apikey }
    r = requests.get('https://wallhaven.cc/api/v1/collections', params=params)
    for i in r.json()['data']:
        if i['id']==collectionID:
            count = i['count']
    print(f'正在获取在线收藏夹图片ID，约等待 {(count//24+2)*1.5} 秒.')
    ids = []
    pages = count//24+2
    for page in range(1,pages):
        print('Remain Time:\t',pages*1.5)
        params = { "apikey": apikey,
                    "page": page,
                 }
        r = requests.get(f'https://wallhaven.cc/api/v1/collections/{nickname}/{collectionID}', params=params)
        ids += [record['id'] for record in r.json()['data']]
        time.sleep(1.5) # 限制每分钟45次，QOS=1.3333
        pages-=1
    return ids


def main(userinfo:dict,pic_ids,collectionID,apikey):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    s.headers.update(headers)
    nickname,token = login(userinfo)
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,zh-HK;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    s.headers.update(headers)
    OnlinePicIDs = GetCollectionPicIDs(apikey, collectionID, nickname)
    PicIDsReady2Add = [pic_id for pic_id in pic_ids if pic_id not in OnlinePicIDs]
    length  = len(PicIDsReady2Add)
    if len(token)==40:
        for picid in PicIDsReady2Add:
            print('Still Remain:\t',length,end='\t')
            time.sleep(1.5) # 休眠1.5秒可保证服务器不提示请求过于频繁
            code = AddtoFav(picid,token,collectionID)
            if code == 429:
                time.sleep(3) # 429错误时，暂停1分钟再重试
                AddtoFav(picid,token,collectionID)
                print(picid)
            elif code == 1:
                time.sleep(3) # 防止报429 Too Many Requests 错误，间隔5秒请求
                continue
            elif code ==3: # 其他错误时打印图片ID，供下次继续
                print(picid)
            length -= 1
    print('All Done!')


if __name__ == '__main__':
    with open('bookmarks.json','r') as f:
        bookmarks = json.load(f)
    pic_ids = [bookmark["n"] for bookmark in bookmarks]

    apikey = "***********************"

    userinfo = {'username': '******', # 账号-为邮箱
                'password': '++KwN9NGC@F34s3Ed++'}  # 密码 

    collectionID = 972651

    main(userinfo,pic_ids,collectionID,apikey)
```
