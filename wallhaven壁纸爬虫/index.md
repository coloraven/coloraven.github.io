# Wallhaven壁纸爬虫-自动上传到指定图床


```python
#wallhaven热门图片采集下载
# —*—coding: utf-8 -*-
import requests,time,random,os
from lxml import etree
from fake_useragent import UserAgent
from tqdm import tqdm


def parse_html(pageNum):
    """提取单页中地图片链接地址，需要自定义查询参数，举例如下："""
    url = f"https://wallhaven.cc/search?categories=111&purity=111&ratios=landscape&topRange=1y&sorting=toplist&order=desc&page={pageNum}"
    ua = UserAgent().random
    html = requests.get(url=url, headers={'user-agent': ua}, timeout=6).content.decode('utf-8')
    tree = etree.HTML(html)
    imgsrcs = tree.xpath('//ul/li/figure/img/@data-src')

    imgurls = []
    for imgsrc in imgsrcs:
        img = imgsrc.replace("th", "w").replace("small", "full")
        imgs = img.split('/')
        imgurl = f"{'/'.join(imgs[:-1])}/wallhaven-{imgs[-1]}"
        try:
            # 使用head请求探测（不会下载图片，加快速度）地址是否正确
            r = requests.head(url=imgurl, headers={'user-agent': ua}, timeout=6)
            if r.status_code==200:
                # print("进入条件一",r.status_code)
                imgurls.append(imgurl)
            else:
                # print("进入条件二",r.status_code)
                imgurl = imgurl.replace('jpg', 'png')
                print(imgurl)
                imgurls.append(imgurl)
        except Exception as e:
            print(f"出错，错误代码：{e}")
        # 休息0-0.2秒
        pause_time = random.uniform(0,0.2)
        time.sleep(pause_time)
    return imgurls


def img_downloader(imgurl,savepath):
    """根据图片链接下载图片到本地，在脚本所在目录新建savepath变量内容对应地文件夹，所有图片保存到其中，文件名为服务器中图片地编码"""
    ua = UserAgent().random
    r = requests.get(url=imgurl, headers={'user-agent': ua}, timeout=6)
    if r.status_code==200:
        with open(f'{savepath}\{imgurl[-10:]}', 'wb') as f:
            f.write(r.content)
        print(f"\t{imgurl[-10:]} 成功保存图片！")
    else:
        print('图片下载失败:',r.status_code,'图片编码',end='\t')
        print(imgurl[-10:])


def start():
    '''爬取图片链接保存到文件（文件名wallhaven.txt），不下载图片，此处文件名改了地话，down_pic_from_file函数中也要相应修改'''
    """需要自定义页数"""
    result = []
    for i in range(1,100):
        result += parse_html(i)
    result = '\n'.join(set(result))
    with open('wallhaven.txt','w',encoding='utf-8') as f:
        f.writelines(result)

def down_pic_from_file():
    """利用os.listdir方法来获取已下载文件名，并与wallhaven.txt中链接对应文件名比对过滤，避免重复下载"""
    '''读取文件中的图片链接并下载'''
    with open('wallhaven.txt','r',encoding='utf-8') as f:
        result = f.readlines()
    result = [i.strip() for i in result]
    savepath = 'wallheaven'
    # 读取目录中已经下载的图片
    done_down_imgs = os.listdir(savepath) 
    remain_list = [i for i in result if i[-10:] not in done_down_imgs] # 如果目录中不存在该图片才下载
    print('剩余',len(remain_list))
    for url in tqdm(remain_list):
        if url[-10:] not in done_down_imgs: 
            # print(url)
            img_downloader(url,savepath)
            time.sleep(random.uniform(0,1))
```

以上是`爬取链接保存到文件`和`根据链接下载图片到本地`，两个步骤相互独立。

## 上传图床
我的最终目的是给本博客作为随机背景图，因为`wallhaven`国内访问速度慢，所以想到将这些图片上传到国内图床再进行使用。
以下是读取`wallhaven.txt`中的图片链接，下载并上传到图床`sm.ms`的代码，我使用的是国外`vps`跑的，奈何`sm.ms`一小时的上传数量限制是`100`张图片，尼玛，后来才发现还有一个限制：一天`200`张上限。
```python mark:13
import io,json,requests,time

count = 0 # `sm.ms`限制一小时只能上传100`张，此变量用来计算，
ys = {}            # 用来存放wallhaven地址与图床外链地址的映射关系字典
huishou = []   # 用爱存放大于5M图片的链接
def upload(imgurl):
    global ys,huishou,count #声明全局变量
    token = "WFyjCGBrKJ9iQqlKyedmnHruZaREHVsn" # sm.ms个人密钥
    headers = {"Authorization": token}
    imgsize = requests.head(imgurl).headers["Content-Length"] # 用head请求，仅探测图片大小，不会下载图片
    if int(imgsize) <= 5242880: # 图片小于5M的就进行上传
        imgbyte = requests.get(imgurl).content
        files = {"smfile": io.BytesIO(imgbyte)} # 使用io.BytesIO方法，将下载的图片数据紧接着转手上传出去，全部在内存中完成，不占用磁盘空间。
        sm_ms_url = "https://sm.ms/api/v2/upload"
        res = requests.post(sm_ms_url, files=files, headers=headers)
        res=res.json()
        if res['code']=="success":
            count+=1
            print('wallhaven地址',imgurl,'图片外链地址：',res["data"]["url"])
            ys[imgurl] = res["data"]["url"]
            if count%100==0:
                time.sleep(3600)
        elif res['code']=='image_repeated':
            print('该链接图片已上传',imgurl)
        else:
            print(res['message'])
    else:
        print("该链接图片大于5M", imgurl)
        huishou.append(imgurl)


if __name__ == "__main__":
    with open("wallhaven.txt", "r", encoding="utf-8") as f:
        result = f.readlines()
    result = [i.strip() for i in result]
    for url in result:
        upload(url)
    with open('映射关系.json','w') as f:
        json.dump(ys)
    with open('5m+.json','w') as f:
        json.dump(huishou)
```

## 多线程筛选小于5M的图片链接
```python 登录wallhaven
import time,requests,random
# from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

s = requests.Session()

def login():
    '''登录'''
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
        'username': '', # 账号
        'password': ''  # 密码
    }
    login_url = 'https://wallhaven.cc/auth/login'
    response = s.post(login_url, headers=header, data=data)
    if response.status_code == 200:
        print("login success")
        return 200
    else:
        print('login failed')
        return response.status_code
```

```python
count = 0

def get_imgsize(url):
    global count
    count +=1
    print('第',count,'次调用')
    try:
        imgsize = session.head(url).headers["Content-Length"] # 用head请求，仅探测图片大小，不会下载图片
        if  int(imgsize) <= 5242880: 
            return url
    except Exception as e:
        print(e)


if __name__ == "__main__":
    with open("wallhaven.txt", "r", encoding="utf-8") as f:
        result = f.readlines()
    result = [i.strip() for i in result]
    small=[]
    pool = ThreadPool(10)
    results = pool.map(get_imgsize, result)
    pool.close()
    pool.join()
    small = [i for i in results if i is not None]

    with open("wallhaven_smallerthan5mb.txt", "w", encoding="utf-8") as f:
         f.writelines('\n'.join(small))
```

## 收藏夹图片信息获取（使用API KEY）
```
w1G9hS9Ci80pNuvWAwX8hz519JoqAZUh
```
API KEY使用限制：1分钟45次，
使用方法：
- 1、请求参数中：`apikey=xxxx`
- 2、请求头中 ：`{"X-API-Key": "XXXX"}`

请求连接：https://wallhaven.cc/api/v1/collections/blackelk/972651
请求方式：GET
### 完整代码
```python
import requests,json,time

headers = {"X-API-Key": "w1G9hS9Ci80pNuvWAwX8hz519JoqAZUh"}

url = 'https://wallhaven.cc/api/v1/collections/blackelk/972651'
# https://wallhaven.cc/api/v1/collections/用户名/收藏夹ID
r = requests.get(url,headers=headers)
result = r.json()
results = result["data"]
total_page = result["meta"]["last_page"]
count = 1 # 用于计算请求次数，防止超出每分钟45次频率
print(f'current page: {page} / {total_page}')
for page in range(2,total_page+1):
    print(f'current page: {page} / {total_page}')
    if count % 45 ==0 :
        time.sleep(60)
    params = {'page': page}
    r = requests.get(url,headers=headers,params=params)
    count+=1
    results+=r.json()["data"]
with open('wallhaven.json','w') as f:
    json.dump(results,f)
```


## 参考
https://blog.csdn.net/qq_29367075/article/details/111940621
https://cloud.tencent.com/developer/article/1799246
登录模拟参考 https%3A%2F%2Fgithub.com%2FRoarpalm%2Fwallhaven%2Fblob%2F779a10bdc3d24e03f9bf2915339ccd58ee165780%2Fnew%20GUI%20Wallhaven%20Setu%20Machine.py%23L62
