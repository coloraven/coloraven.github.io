# FastAPI直接使用请求与响应

FastAPI是一个非常好用的web框架,今天我要介绍的是它直接使用请求和响应的方法.  
有些时候,我们不能确定客户端的参数,这时候,我们可以直接使用请求和响应,可以获取到更底层的一些信息,已经不确定的参数.
https://www.starlette.io/responses/

## 1. 请求

众所周知,fastapi站在巨人的肩膀上,其中,请求和和响应部分来自于[starlette](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.starlette.io%2F).这里给出[官网对请求解释的部分](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.starlette.io%2Frequests%2F).  
当我们使用fastapi时,可以声明一个类型为starlette.request.Request类型的参数,他将接受原始的请求对象:

```python 此代码实现了响应体内容（json形式）为请求头内容
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

app=FastAPI()

@app.get("/")
def func(request:Request):
    print(request.headers)
    return request.headers

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=True)
```

请求对象支持的操作:  
* request.cookies:cookie  
* request.query_params:查询参数  
* request.url:url对象  
* request.headers:请求头  
* async def request.form():获取表单信息,注意这是一个异步函数.  
* async def request.json():获取json信息,这两个只能用一个,这也是一个异步函数.  
* async def request.body():直接获取body数据,未经过转换

## 2.响应

可以从[官网对响应的解释](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.starlette.io%2Fresponses%2F)上看到全部内容.  
有很多种响应,包括:

* Response(content:str,statuc_code:int=200,headers:dict=None,media_type):基本的响应
* RedirectResponse(url,status_code,headers):重定向到url
* FileResponse(path,status_code,media_type):文件响应,path为本地文件路径,需要安装aiofiles库才可以使用.
* StreamingResponse(data,media_type):流响应,支持一个可迭代对象(包括文件和BytesIO,StringIO等类文件对象)  

    直接返回即可,关于StreamingResponse还有[一篇文章](https://www.jianshu.com/p/86c020ad7f4f),讲述了如何利用它传输文件.

```python 此代码实现了自定义响应头。更多查看https://www.starlette.io/responses/
import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

app=FastAPI()

@app.get("/")
def func():
    ss = {
        "_id": "616fc0d46da5004b0f738538",
        "id": 606,
        "name": "李三",
        "raw_resp": {
            "meta": {
                "deviceType": "ANDROID",
                "deviceName": "Android 5.1.1 SDK 22 OnePlus HD1910",
                "expiredTime": "2031-10-27T02:02:46Z",
            }
        },
        "time": "2021年10月20日 07:10"
        }
    response = JSONResponse(ss, headers={"media_type":'text/plain'})
    return response

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=True)
```

更多方法参考：https://www.pythonf.cn/read/142674

## 读取请求头中某个参数：
```python
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None),Authorization: Optional[str] = Header(None)):
    return {"User-Agent": user_agent,'Authorization':Authorization}
```
上面例子读取了请求头中`user_agent`和`Authorization`两个参数，然后作为响应体（json字典类型）返回了。
## 读取`Cookies`
```python
from typing import Optional

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}
```
## 响应头设置
拜见：https://www.cnblogs.com/poloyy/p/15366453.html
