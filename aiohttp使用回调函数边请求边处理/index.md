# aiohttp使用回调函数边请求边处理

我们平时使用Requests的时候，一般是这样写代码的：
```python
import requests

def parse(html):
    print('对 html 进行处理')

html = requests.get('url')
parse(html)
```
这是一种非常常见的直线性思维，我先请求网站拿到 html，然后我再把 html 传给负责处理的函数。在整个过程中，“我“担任着调度的角色。

在这种思维方式的影响下，有些同学即使在使用aiohttp写异步爬虫，也是这样写的：
```python
import aiohttp
import asyncio


async def request(url):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        html = await resp.text(encoding='utf-8')

def parse(html):
    print('处理 html')


async def main():
    url_list = [url1, url2, url3, url4]
    tasks = []
    for url in url_list:
        tasks.append(request(url))
    html_list = await asyncio.gather(*tasks)
    for html in html_list:
        parse(html)


if __name__ == '__main__':
    asyncio.run(main())
```

确实，这些 URL 的网络请求是异步了，但是却必须等到所有 URL 全部请求完成以后，才能开始处理这些 HTML。假如其中一个 URL 访问只需要1秒钟，其他的 URL 请求需要3秒钟。那么这个1秒钟的请求结束以后，还需要等待2秒，才能开始进行处理。

于是，有些同学会修改代码，多包装一层函数：
```python
import aiohttp
import asyncio


async def request(url):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        html = await resp.text(encoding='utf-8')

def parse(html):
    print('处理 html')

async def get(url):
    html = await request(url)
    parse(html)

async def main():
    url_list = [url1, url2, url3, url4]
    tasks = []
    for url in url_list:
        tasks.append(get(url))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
```

get()函数整体负责获取一个 URL 的源代码并对它进行解析。然后让 get()函数异步。

这样做确实能够解决问题，但是大家如果仔细体会就会发现，在get()函数里面的代码写法，还是用的同步处理的思想。

既然要写异步代码，那么我们脑子里就要一直记住——很多个请求会同时发出，但是我们并不知道他们什么时候完成。与其让我们去等待它完成，然后再把完成结果传给另外一个函数。不如让这些请求在结束的时候，自行主动把结果传给处理函数。

有了这种思想以后，我们再来修改一下上面的代码：
```python
import aiohttp
import asyncio


async def request(url, callback):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        html = await resp.text(encoding='utf-8')
    callback(html)


def parse(html):
    print('处理 html: ', html)


async def main():
    url_list = [
 'http://exercise.kingname.info/exercise_middleware_ip/1',
 'http://exercise.kingname.info/exercise_middleware_ip/2',
 'http://exercise.kingname.info/exercise_middleware_ip/3',
 'http://exercise.kingname.info/exercise_middleware_ip/4',
 'http://exercise.kingname.info/exercise_middleware_ip/5',
 'http://exercise.kingname.info/exercise_middleware_ip/6',
 ]
    tasks = []
    for url in url_list:
        tasks.append(request(url, parse))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
```

运行效果如下图所示：

![2021-11-27T170037](2021-11-27T170037.png)
这种写法，初看起来与用get()函数包装没什么区别，但是他们在思维方式上却完全不一样。

这种不一样，接下来的几篇文章会进一步演示。
## 来源
[Callback ——从同步思维切换到异步思维](https://cloud.tencent.com/developer/article/1621134)
