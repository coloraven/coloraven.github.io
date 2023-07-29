# requests、aiohttp、httpx对比


来源：https://learnku.com/articles/54989
在 Python 众多的 HTTP 客户端中，最有名的莫过于 `requests`、`aiohttp` 和 `httpx`。在不借助其他第三方库的情况下，`requests` 只能发送同步请求；`aiohttp` 只能发送异步请求；`httpx` 既能发送同步请求，又能发送异步请求。

所谓的同步请求，是指在单进程单线程的代码中，发起一次请求后，在收到返回结果之前，不能发起下一次请求。所谓异步请求，是指在单进程单线程的代码中，发起一次请求后，在等待网站返回结果的时间里，可以继续发送更多请求。

今天我们来一个浅度测评，仅仅以多次发送 GET 请求这个角度来对比这三个库的性能。

当然测试结果与网速有关，不过在同一段时间的同一个网络测试出来，还是能看得出来问题的。

## requests 
### 发送请求
```python
import requests
 
url = 'https://www.baidu.com/'
headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
def main():
    res = requests.get(url,headers=headers)
    print(res.status_code)
 
if __name__ == '__main__':
    main()
```
使用 `requests.post` 每次都会创建新的连接，速度较慢。而如果首先初始化一个 `Session`，那么 `requests` 会保持连接，从而大大提高请求速度。所以在这次测评中，我们分别对两种情况进行测试
### 有Session

```python
import time,requests
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
def make_request():
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
 
def main():
    start = time.time()
    for _ in range(100):
        make_request()
    end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    main()
```

> 发送 100 次请求，耗时：10.295854091644287

### 无Session

```python
import time,requests
 
session = requests.session()
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
def make_request():
    resp = session.get(url, headers=headers)
    print(resp.status_code)
 
def main():
    start = time.time()
    for _ in range(100):
        make_request()
    end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    main()
```

> 发送 100 次请求，耗时：4.679062128067017，很明显快了接近 6s

## httpx 

### 发送同步请求

```python
import httpx
 
url = 'https://www.baidu.com/'
headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
def main():
    res = httpx.get(url,headers=headers)
    print(res.status_code)
 
if __name__ == '__main__':
      main()
```

> httpx 的同步模式与 requests 代码重合度 99%，只需要把 requests 改成 httpx 即可正常运行。

### 发送异步请求

```python
import httpx,asyncio
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(resp.status_code)
 
if __name__ == '__main__':
    asyncio.run(main())
```

### 同步模式

```python
import time
import httpx
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
def make_request():
    resp = httpx.get(url, headers=headers)
    print(resp.status_code)
 
def main():
    start = time.time()
    for _ in range(100):
        make_request()
    end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    main()
```

> 发送 100 次请求，耗时：16.60569405555725

### 异步模式：只创建一次`httpx.AsyncClient` 

```python
import httpx
import asyncio
import time
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def make_request(client):
    resp = await client.get(url, headers=headers)
    print(resp.status_code)
 
async def main():
    async with httpx.AsyncClient() as client:
        start = time.time()
        tasks = [asyncio.create_task(make_request(client)) for _ in range(100)]
        await asyncio.gather(*tasks)
        end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    asyncio.run(main())
```

> 发送 100 次请求，耗时：4.359861135482788

### 异步模式：每次都创建 `httpx.AsyncClient` 

```python
import httpx
import asyncio
import time
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def make_request():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(resp.status_code)
 
async def main():
    start = time.time()
    tasks = [asyncio.create_task(make_request()) for _ in range(100)]
    await asyncio.gather(*tasks)
    end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    asyncio.run(main())
```

> 发送 100 次请求，耗时：6.378381013870239


## aiohttp 
### 发送请求
```python
import asyncio,aiohttp
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def main():
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=headers) as resp:
            print(resp.text)
            print(resp.status)
 
if __name__ == '__main__':
    asyncio.run(main())
```

> aiohttp 的代码与 httpx 异步模式的代码重合度 90%，只不过把 AsyncClient 换成了 ClientSession


### 只创建一次 `aiohttp.ClientSession` 

```python
import time,asyncio,aiohttp
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def make_request(client):
    async with client.get(url, headers=headers) as resp:
        print(resp.status)
 
async def main():
    async with aiohttp.ClientSession() as client:
        start = time.time()
        tasks = [asyncio.create_task(make_request(client)) for _ in range(100)]
        await asyncio.gather(*tasks)
        end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    asyncio.run(main())
```

> 发送 100 次请求，耗时：2.235464334487915

### 每次都创建 `aiohttp.ClientSession` 

```python
import time,asyncio,aiohttp
 
url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
 
async def make_request():
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=headers) as resp:
            print(resp.status)
 
def main():
    start = time.time()
    tasks = [asyncio.ensure_future(make_request()) for _ in range(100)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print(f'发送100次请求，耗时：{end - start}')
 
if __name__ == '__main__':
    main()
```

------

> 发送 100 次请求，耗时：2.6662471294403076



## 请求 100 次速度排名

`aiohttp`（只创建一次`client`）> `aiohttp`（每次都创建`client`）> `httpx`异步只创建一次只创建一次`client` > `requests.session` > `httpx`异步 每次都创建每次都创建`client` > `requests` > `httpx`异步

## 总结

- 如果你只发几条请求。那么使用 `requests` 或者 `httpx` 的同步模式，代码最简单。
- `requests` 是否创建一个 `session` 保持连接，速度差别比较大，在没有反爬的情况下，只追求速度，建议用 `requests.session` 
- 如果你要发送很多请求，但是有些地方要发送同步请求，有些地方要发送异步请求，那么使用 `httpx` 最省事。
- 如果你要发送很多请求，并且越快越好，那么使用 `aiohttp` 最快。
