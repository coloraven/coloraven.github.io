# 随机使用Pexels收藏壁纸为博客背景图

## 使用API获取收藏夹中的图片链接地址
请求地址：https://api.pexels.com/v1/collections/pwgv2sw?per_page=80&type=photos

### 请求参数:
```json
{
	"per_page": "80",
	"type": "photos"
}
```
### 请求头：
```json
{
	"Authorization": "API KEY"
}
```
### 完整`Python`代码
```python
import requests

headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    'Authorization': 'API KEY',
    'Content-Type': 'application/json',
}

params = (
    ('per_page', '80'),
    ('type', 'photos'),
)

response = requests.get('https://api.pexels.com/v1/collections/pwgv2sw', headers=headers, params=params)
```
### 响应数据示例：
```json
{
	"page": 1,
	"per_page": 80,
	"media": [
        {
            "type": "Photo",
            "id": 1011302,
            "width": 2448,
            "height": 3696,
            "url": "https://www.pexels.com/photo/green-orchid-plant-1011302/",
            "photographer": "Julia Sakelli",
            "photographer_url": "https://www.pexels.com/@juliasakelli",
            "photographer_id": 259751,
            "avg_color": "#404222",
            "src": {
                "original": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg",
                "large2x": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                "large": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
                "medium": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&h=350",
                "small": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&h=130",
                "portrait": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
                "landscape": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
                "tiny": "https://images.pexels.com/photos/1011302/pexels-photo-1011302.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280"
            },
            "liked": false
	    }
	],
	"total_results": 413,
	"next_page": "https://api.pexels.com/v1/collections/pwgv2sw/?page=2&per_page=80&type=photos",
	"id": "pwgv2sw"
}
```

## 遍历收藏夹图片信息：
### 第一次请求：
```python
results = []
response = requests.get('https://api.pexels.com/v1/collections/pwgv2sw', headers=headers, params=params)
result = response.json()
results+=result["media"]
```
获取响应中的`next_page`
### 后续递归遍历：
```python
def get_pic_info(result):
    if 'next_page' in result:
        response = requests.get(result.json()['next_page'],headers=headers)
        result = response.json()
        return result["media"]+=get_pic_info(result)
    else:
        return []
```
### 提取图片链接信息：
```python
for i in results:
    large2x = i["src"]["large2x"]
```
### 最终代码
```python
import requests

headers = {
    # "user-agent": "ApiPOST Runtime +https://www.apipost.cn",
    'Authorization': '563492ad6f91700001000001dab470950ea14cdca736ef73a9d7e101',
    'Content-Type': 'application/json',
}

params = (
    ('per_page', '80'),
    ('type', 'photos')
)

results = []
response = requests.get('https://api.pexels.com/v1/collections/pwgv2sw', headers=headers, params=params)
result = response.json()
results+=result["media"]

def get_pic_info(result):
    if 'next_page' in result:
        next_page = result['next_page']
        response = requests.get(next_page,headers=headers)
        result = response.json()
        return result["media"]+get_pic_info(result)
    else:
        return []

results+=get_pic_info(result)
print(len(results))
```

## 搭建微服务（Docker容器）
实现：从文件中读取图片信息集，并随机抽取图片链接
### flask代码
~~待完善的地方：~~
~~wallhaven图片大小过滤，NSFW开关，~~
~~pexels与wallhaven选择~~
```python app.py
from flask import Flask,redirect,request
import json,requests,random,time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

headers = {
        'Authorization': '563492ad6f91700001000001dab470950ea14cdca736ef73a9d7e101',
        'Content-Type': 'application/json',
    }


@app.route("/",methods=['get'])
def getimg():
    print("进入获取图片链接函数")
    # 尝试获取参数
    if request.args.get("source"): # 接受pexels或者wallhaven或者both，默认为both
        source=request.args.get("source")
        if '?' in source:
            source=source.split('?')[0]
    else:
        source='both'

    if request.args.get("size"):           # 接受整数......过滤wallhaven壁纸大小,默认为0==无限制。
        if '?' in request.args.get("size"):
            size=request.args.get("size").split('?')[0]
            size = int(size)
    else:
        size= 0

    if request.args.get("nsfw"):         # 接受on或者off，对应打开或者关闭，默认关闭。
        nsfw=request.args.get("nsfw")
        if '?' in nsfw:
            nsfw=nsfw.split('?')[0]
    else:
        nsfw='off'


    # 尝试读取文件
    try:
        with open('pexels_pics.json','r') as f:
            pexels_pics=json.load(f)
            pexels_pics=[i['src']["large2x"] for i in pexels_pics]

        with open('wallhaven.json','r') as ff:
            wallhaven_pics=json.load(ff)
    except Exception as e:
        print(e)
        print("某个必须文件不存在！准备进行更新")
        update()
        with open('pexels_pics.json','r') as f:
            pexels_pics=json.load(f)
            pexels_pics=[i['src']["large2x"] for i in pexels_pics]
        with open('wallhaven.json','r') as ff:
            wallhaven_pics=json.load(ff)

    # 根据请求参数过滤wallhaven图片路径信息
    if nsfw=='off':
        if size==0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics if i["purity"]!='nsfw']
        elif size!=0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics if i["file_size"]<=size&i["purity"]!='nsfw']
    elif nsfw == 'on':
        if size != 0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics if i["file_size"]<=size]
        elif size==0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics ]
    elif nsfw == 'only': #参数设置不正确，则返回空
        CountOfNsfw = len([i["path"] for i in wallhaven_pics if i["purity"]=='nsfw'])
        if size==0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics if i["purity"]=='nsfw']
        elif size!=0:
            wallhaven_pics=[i["path"] for i in wallhaven_pics if i["file_size"]<=size&i["purity"]=='nsfw']
        print(f'nsfw only total have {CountOfNsfw} pics')
    else:
        wallhaven_pics=[]

    if source=='pexels':
        img_link =  random.choice(pexels_pics)
        return redirect(img_link)
    elif source=='wallhaven':
        img_link =  random.choice(wallhaven_pics)
        return redirect(img_link)
    elif source=='both':
        img_link =  random.choice(pexels_pics+wallhaven_pics)
        return redirect(img_link)
    else:#参数设置不正确，则返回空
        return ''


def get_pic_info(result):
    """用于被update函数调用"""
    if 'next_page' in result:
        next_page = result['next_page']
        print(next_page)
        response = requests.get(next_page,headers=headers)
        result = response.json()
        return result["media"]+get_pic_info(result)
    else:
        return []


@app.route("/update",methods=['GET'])
def update():
    print("进入更新图片函数")
    params = {
        'per_page': 80,
        'type': 'photos'
    }

    results = []
    response = requests.get('https://api.pexels.com/v1/collections/pwgv2sw', headers=headers, params=params,verify=False)
    result = response.json()
    results+=result["media"]
    results+=get_pic_info(result)
    with open('pexels_pics.json','w') as f:
        json.dump(results,f)
        print(f'共计写入{len(results)}条')

    # 更新wallhaven收藏壁纸
    wallhaven_headers = {"X-API-Key": "w1G9hS9Ci80pNuvWAwX8hz519JoqAZUh"}
    url = 'https://wallhaven.cc/api/v1/collections/blackelk/972651'
    # https://wallhaven.cc/api/v1/collections/用户名/收藏夹ID
    r = requests.get(url,headers=wallhaven_headers)
    result = r.json()
    results = result["data"]
    total_page = result["meta"]["last_page"]
    print(f'预计等待{total_page*7-2}秒')
    count = 1 # 用于计算请求次数，防止超出每分钟45次频率
    print(f'current page: 1 / {total_page}')
    for page in range(2,total_page+1):
        print(f'current page: {page} / {total_page}')
        time.sleep(5)
        params = {'page': page}
        r = requests.get(url,headers=wallhaven_headers,params=params,verify=False)
        count+=1
        results+=r.json()["data"]
    with open('wallhaven.json','w') as f:
        json.dump(results,f)


if __name__ == '__main__':    
    # 开启debug模式方法二
    app.run(debug=True,host='0.0.0.0',port=8448)
```
### gunicorn.conf.py配置文件
此处使用之前弄好的，使用`gunicorn`可以实现并发访问，给`flask`赋能。
```python
workers = 4 # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent" # 采用gevent库，支持异步处理请求，提高吞吐量
debug = True
capture_output = True
timeout = 200
bind = "0.0.0.0:8448" # 监听IP端口，以便于Docker之间、Docker和宿主机之间的通信
loglevel = "debug"
```
### Dockerfile
```dockerfile
FROM python:3.9.6-alpine3.14
WORKDIR /app
RUN apk --update --no-cache add --virtual .all python3-dev libffi-dev gcc musl-dev make libevent-dev build-base \
&&pip install --no-cache-dir gevent flask gunicorn requests \
&&apk --purge del .all
COPY . .
EXPOSE 8448
CMD gunicorn app:app -preload -c gunicorn.conf.py
```
