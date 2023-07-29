# 使用腾讯云函数搭建简单API后端

非flask等框架的云函数模板：
其入口函数为：
`main_handler(event,content)`
该函数位于src目录下的index.py文件中。

其中event参数用来传递“腾讯整个云函数系统”传递过来的参数，event的值为(见https://cloud.tencent.com/document/product/583/12513)：
```json
{
 "requestContext": {
   "serviceId": "service-f94sy04v",
   "path": "/test/{path}",
   "httpMethod": "POST",
   "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
   "identity": {
     "secretId": "abdcdxxxxxxxsdfs"
   },
   "sourceIp": "10.0.2.14",
   "stage": "release"
 },
 "headers": {
   "accept-Language": "en-US,en,cn",
   "accept": "text/html,application/xml,application/json",
   "host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
   "user-Agent": "User Agent String"
 },
 "body": "{\"test\":\"body\"}",
 "pathParameters": {
   "path": "value"
 },
 "queryStringParameters": {
   "foo": "bar"
 },
 "headerParameters":{
   "Refer": "10.0.2.14"
 },
 "stageVariables": {
   "stage": "release"
 },
 "path": "/test/value",
 "queryString": {
   "foo" : "bar",
   "bob" : "alice"
 },
 "httpMethod": "POST"
}
```


## 代码示例
```python
# -*- coding: utf-8 -*-

import sys
import logging
import json
import hashlib
import time

def md5_convert(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

logger.info('加载函数')

kami_resp = {"result":{"msg":"恭喜你，超级VIP用户！用到官方倒闭为止。"},"ts":int(round(time.time()*1000)),"status":1}
normal_resp = {"result":{"notice":None,"stat":None,"onlineDialog":None,"splash":None,"bind":None,"register":{"probationExt":None,"probation":0,"useText":"进入软件","themeColor":"#ee00ee","neutralText":"","neutralActionType":0,"neutralExt":"","cancelText":"","cancelActionType":0,"cancelExt":"http://146.56.247.24:8002/liebiao/B6CB3C0D89FA2B14","message":"欢迎使用"},"version":None},"ts":int(round(time.time()*1000)),"status":1}


def main_handler(event,content):
    logger.info('进入主函数')
    logger.info(event["path"])
    if event["path"] == "/ZiHuFenShen/feature/pack/verify": # 验证卡密
        return {
                   "isBase64Encoded": False,
                   "statusCode": 200,
                   "headers": {"Content-Type": "application/json;charset=UTF-8", "eagleid": md5_convert(json.dumps(kami_resp, ensure_ascii=False)+'1')},
                   "body": json.dumps(kami_resp, ensure_ascii=False)
                }
    if event["path"] == "/ZiHuFenShen/feature/config": # 验证其他
        return {
                   "isBase64Encoded": False,
                   "statusCode": 200,
                   "headers": {"Content-Type": "application/json;charset=UTF-8", "eagleid": md5_convert(json.dumps(normal_resp, ensure_ascii=False)+'1')},
                   "body": json.dumps(normal_resp, ensure_ascii=False)
                }
    if event["path"] == "/ZiHuFenShen/feature/302": # 验证其他
        return {
                   "isBase64Encoded": False,
                   "statusCode": 302,
                #    "headers": {"Content-Type": "application/json;charset=UTF-8", "eagleid": md5_convert(json.dumps(normal_resp, ensure_ascii=False)+'1')},
                   "body": json.dumps(normal_resp, ensure_ascii=False)
                }
```
