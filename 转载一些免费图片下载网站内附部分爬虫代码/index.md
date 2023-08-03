# 【转载】一些免费图片下载网站（内附部分爬虫代码）

大兄弟你进来一定不是看我废话的吧，嗯，安排上，咱用图和爬虫说话，这些网站真的很不错！  
emm…顺便和想看详细解析的兄弟说一句，这里有个详细的样例， [爬虫爬取精美图片详介传送门 ](https://blog.csdn.net/dally2/article/details/106385467)

### 内容检索

* * * * [1. hippopx](https://blog.csdn.net/dally2/article/details/107655955#1_hippopx_5)
            * [2. colorhub](https://blog.csdn.net/dally2/article/details/107655955#2_colorhub_66)
            * [3. pikrepo](https://blog.csdn.net/dally2/article/details/107655955#3_pikrepo_130)
            * [4. wallhaven](https://blog.csdn.net/dally2/article/details/107655955#4_wallhaven_185)
            * [5. 还有这些不错的网站](https://blog.csdn.net/dally2/article/details/107655955#5__244)
            * * [5.1 pixabay](https://blog.csdn.net/dally2/article/details/107655955#51__pixabay_245)
                * [5.2 ssyer](https://blog.csdn.net/dally2/article/details/107655955#52_ssyer_249)
                * [5.3 不错的插画](https://blog.csdn.net/dally2/article/details/107655955#53__252)
                * [5.4 visualhunt](https://blog.csdn.net/dally2/article/details/107655955#54_visualhunt_255)
                * [5.5 pexels](https://blog.csdn.net/dally2/article/details/107655955#55_pexels_259)
                * [5.6 unsplash](https://blog.csdn.net/dally2/article/details/107655955#56_unsplash_262)
                * [5.7 极简壁纸](https://blog.csdn.net/dally2/article/details/107655955#57__265)

#### 1. hippopx

https://www.hippopx.com/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729095947252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)  
嘘~悄悄附上爬虫代码：

非高清：

```python
#这里以爬取小猫图片为例，倘若兄弟想爬取其他的，改一下参数就成噢
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,65):
    url = "https://www.hippopx.com/zh/query?q=cat&page=%s"%(i)      #q表示你要找到的名称，这里是cat，page用来确定第几页
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    img_all = soup.find_all('link',{"itemprop": "thumbnail"})
    for img4 in img_all:
        urlimg = img4['href']
        print(urlimg)
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Cat/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```

高清图片下载

```python
#Cat下载High-Definition
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(2,100):
    url = "https://www.hippopx.com/zh/query?q=cat&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    img_all = soup.find_all('img',{"itemprop": "contentUrl"})
    for img in img_all:
        urlimg = img['src']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Cat_HighDefinition/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```

#### 2. colorhub

https://www.colorhub.me/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729101011480.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)  
非高清下载：

```python
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,10):
    url = "https://www.colorhub.me/search?tag=dog&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    img_all = soup.find_all('img',{"class": "card-img-top"})
    for img4 in img_all:
        urlimg ="http:"+img4['src']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Image_experiment/DOG/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```


高清下载：

```python
from bs4 import BeautifulSoup
import requests
import re

gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,2):
    url = "https://www.colorhub.me/search?tag=dog&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    href_all = soup.find_all('div',{"class":"card"})
    for href in href_all:
        href_url = href.a['href']
        html4 = requests.get(href_url,headers=gHeads).content
        soup4 = BeautifulSoup(html4, 'lxml')
        img4 = soup4.find('a',{"data-magnify":"gallery"})
        urlimg ="http:"+img4['href']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Image/DOG/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```


#### 3. pikrepo

https://www.pikrepo.com/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729151144866.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

非高清下载：

```python
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,100):
    url = "https://www.pikrepo.com/search?q=mountain&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    img_all = soup.find_all('img',{"itemprop": "thumbnail"})
    for img4 in img_all:
        urlimg = img4['data-src']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Image_experiment/mountain/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```


高清下载：

```python
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(3,10):
    url = "https://www.pikrepo.com/search?q=mountain&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    img_all = soup.find_all('link',{"itemprop": "contentUrl"})
    for img in img_all:
        urlimg = img['href']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Image/Mountain/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```


#### 4. wallhaven

https://wallhaven.cc/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729190800634.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)  
非高清下载：

```python
from bs4 import BeautifulSoup
import requests
import re
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,200):
    url = "https://wallhaven.cc/search?q=FOG&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads).content
    soup = BeautifulSoup(html, 'lxml')
    img_ul = soup.find_all("img",{"alt":"loading"})
    for img in img_ul:
        imgstr = str(img)
        url = img['data-src']
        r = requests.get(url, stream=True)
        image_name = url.split('/')[-1]
        with open('F:/Image_experiment/FOG/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
print('end...........')
```


高清图片下载：

```python
from bs4 import BeautifulSoup
import requests
gHeads = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
}
for i in range(1,20):
    url = "https://wallhaven.cc/search?q=DOG&page=%s"%(i)
    print(url)
    html = requests.get(url,headers=gHeads)
    html = html.content
    soup = BeautifulSoup(html, 'lxml')
    href_all = soup.find_all( 'a',{"class": "preview"})
    for href in href_all:
        href_url = href['href']
        html4 = requests.get(href_url,headers=gHeads).content
        soup4 = BeautifulSoup(html4, 'lxml')
        img4 = soup4.find( 'img',{"id": "wallpaper"})
        urlimg = img4['data-cfsrc']
        r = requests.get(urlimg, stream=True)
        image_name = urlimg.split('/')[-1]
        with open('F:/Image/DOG/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    print("end.....................")
```


#### 5. 还有这些不错的网站

##### 5.1 pixabay

https://pixabay.com/images/search/sea/?pagi=2  
图片高清且不涉及版权问题，哇，抱歉我的能力有限，不能近距离观赏啦（没爬成功，囧…），那…就远观吧  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729170420933.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.2 ssyer

https://www.ssyer.com/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729190602133.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.3 不错的插画

https://mixkit.co/free-stock-art/discover/dog/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729193114169.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.4 visualhunt

https://visualhunt.com/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729193728531.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.5 pexels

https://www.pexels.com/zh-cn/search/DOG/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020072919332825.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.6 unsplash

https://unsplash.com/  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200729193434900.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)

##### 5.7 极简壁纸

https://bz.zzzmh.cn/index  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210629215157170.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhbGx5Mg==,size_16,color_FFFFFF,t_70)
