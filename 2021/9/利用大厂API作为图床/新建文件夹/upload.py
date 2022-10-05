#wallhaven 热门图片采集下载
# —*—coding: utf-8 -*-
import requests,time,random,os
from lxml import etree
from fake_useragent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup

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
        'username': 'sirliu110@gmail.com', # 账号
        'password': 'KwN9NGC@F34s3Ed'  # 密码
    }
    login_url = 'https://wallhaven.cc/auth/login'
    response = s.post(login_url, headers=header, data=data)
    if response.status_code == 200:
        print("login success")
        return 200
    else:
        print('login failed')
        return response.status_code


def parse_html(pageNum,url="https://wallhaven.cc/search?categories=111&purity=111&ratios=landscape&topRange=1y&sorting=toplist&order=desc&page="):
    """提取单页中地图片链接地址，需要自定义查询参数，举例如下："""
    url = f"{url}{pageNum}"
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
            # 使用 head 请求探测（不会下载图片，加快速度）地址是否正确
            r = requests.head(url=imgurl, headers={'user-agent': ua}, timeout=6)
            if r.status_code==200:
                # print ("进入条件一",r.status_code)
                imgurls.append(imgurl)
            else:
                # print ("进入条件二",r.status_code)
                imgurl = imgurl.replace('jpg', 'png')
                print(imgurl)
                imgurls.append(imgurl)
        except Exception as e:
            print(f"出错，错误代码：{e}")
        # 休息 0-0.2 秒
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
    for i in range(1,14):
        result += parse_html(i,url="https://wallhaven.cc/favorites?page=" )
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


if __name__ == '__main__':
    if login()==200:
        start()

