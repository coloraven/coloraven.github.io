# 异步并发aiohttp


```python
import time
from aiohttp import ClientSession,TCPConnector
from pprint import pprint as print
import asyncio
 
url = 'https://api.panhvhg.xyz/api/v3/channels/968/connect'
url='https://api.panhvhg.xyz/api/v3/channels/0/connect'
headers = {
    'Host': 'api.panhvhg.xyz',
    'api-version': 'v3.0',
    'request_raw_response_body_tag_header': '8',
    'accept': 'application/json',
    'content-type': 'application/json',
    'accept-language': 'zh-CN',
    'device-identifier': '6961EB763D32FDD1116C00092E0B9365',
    'device-type': 'ANDROID',
    'product-identifier': 'panda',
    'authorization': 'Bearer eyJleHAiOjE3MTM4OTc1NjcsInVzZXJJZCI6MzUyNzQ3NjksImRldmljZUlkIjozNTIzNDgxMCwiaWF0IjoxNjI3NDk3NTY3fQ.AMxXjoPi1HdPTlQ9h3eUq8VFpS40kLDvKTVCt787HQA',
    'user-agent': 'okhttp/4.9.0 android/10(ufkckcuuuccucfc) panda/5.5.0(91)',
   # 'x-timestamp': '1627507529',
    'content-length': '0',
    'accept-encoding': 'gzip',
}
 
async def make_request(client):
    async with client.post(url, headers=headers) as resp:
        s=await resp.json()
        return s
 
async def main():
    cons = TCPConnector(limit=11) # 限制QOS，具体以网速不同而不同，需要测试，同时，需要先导入aiohttp.TCPConnector模块
    async with ClientSession(connector=cons) as client:
        starttime = time.time()
        tasks = [asyncio.create_task(make_request(client)) for _ in range(1000)]
        s = await asyncio.gather(*tasks)
        endtime = time.time()
        print(f"QOS:{len(tasks)/(starttime-endtime)}")
        return s
        
if __name__ == '__main__':
    start = time.time()
    s=asyncio.run(main()) # jupyter环境使用await main()
    print(len(s))
    end = time.time()
    print(f'发送10次请求，耗时：{end - start}')
```
