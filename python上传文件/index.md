# Python上传文件

## requests
来源：https://stackoverflow.com/a/22974646 



简言之, `files`参数takes a dictionary with the key being the name of the form field and the value being either a string or a 2, 3 or 4-length tuple, as described in the section [POST a Multipart-Encoded File](https://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file) in the Requests quickstart:

```python
url = 'http://httpbin.org/post'
files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
```

上面的`tuple`解析（压缩）成:

```python
tuple(filename, data, content_type, headers)
```

如果`files`的值仅仅是字符串, 那么文件名将与键名相同:

```python
files = {'obvius_session_id': '72c2b6f406cdabd578c5fd7598557c52'}

Content-Disposition: form-data; name="obvius_session_id"; filename="obvius_session_id"
Content-Type: application/octet-stream
```

如果值是`tuple`且第一个值是`None`,那么`filename`属性将不会被包含:

```python
files = {'obvius_session_id': (None, '72c2b6f406cdabd578c5fd7598557c52')}

Content-Disposition: form-data; name="obvius_session_id"
Content-Type: application/octet-stream

```
## aiohttp
来源：https://www.cnblogs.com/lianzhilei/p/10126349.html


### ① 单个文件上传

#### 服务端

```python
async def post(self, request):
       reader = await request.multipart()
       # /!\ 不要忘了这步。（至于为什么请搜索 Python 生成器/异步）/!\
       file = await reader.next()
       filename = file.filename
       # 如果是分块传输的，别用Content-Length做判断。
       size = 0
       with open(filename, 'wb') as f:
           while True:
               chunk = await file.read_chunk()  # 默认是8192个字节。
               if not chunk:
                   break
               size += len(chunk)
               f.write(chunk)
 
       return web.Response(text='{} sized of {} successfully stored'
                                ''.format(filename, size))
```
#### 客户端
```python
import aiohttp
import asyncio
 
url = 'http://127.0.0.1:8080/'
files = {'file': open('files/1M.wav', 'rb'),}
 
async def fetch(session, url):
    async with session.post(url,data=files) as response:
        return await response.text()
 
 
async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://127.0.0.1:8080')
        print(html)
 
 
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### ② 传输多个文件及其他参数

#### 服务端
```python
async def post(self, request):
    reader = await request.multipart()
    data = {}
    async for read in reader:
        filename = read.filename
        if filename is not None:
            size = 0
            with open('./' + filename, 'wb') as f:
                while True:
                    chunk = await read.read_chunk()  # 默认是8192个字节。
                    if not chunk:
                        break
                    size += len(chunk)
                    f.write(chunk)
        else:
            value = await read.next()
            key = read.name
            data[key] = str(value, encoding='utf-8')
    print(data)
    return web.Response()
```
#### 客户端
```python
import aiohttp
import asyncio
 
url = 'http://127.0.0.1:8080/'
files = {'file': open('files/1M.wav', 'rb'),
         'file2': open('files/0.5M.wav', 'rb'),
         'name':'000001',
         }
 
async def fetch(session, url):
    async with session.post(url,data=files) as response:
        return await response.text()
 
 
async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://127.0.0.1:8080')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
