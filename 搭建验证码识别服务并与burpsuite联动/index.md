# 搭建验证码识别服务并与BurpSuite联动


### 出处

https://www.ddosi.com/xp_captcha/
https://github.com/smxiazi/NEW_xp_CAPTCHA

## xp_CAPTCHA白嫖版白嫖版

### 说明

xp_CAPTCHA 白嫖版白嫖版

- 验证码识别
- burp插件

### 安装

需要python3 小于3.7的版本

#### 安装 `muggle_ocr` 模块（大概400M左右）

```bash
python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com muggle-ocr
```

[![image](https://user-images.githubusercontent.com/30351807/115872316-3f4b6780-a474-11eb-8f25-a2de13274510.png#vwid=1000&vhei=123)](https://user-images.githubusercontent.com/30351807/115872316-3f4b6780-a474-11eb-8f25-a2de13274510.png#vwid=1000&vhei=123)

#### 运行 server.py

见文末

[![image](https://user-images.githubusercontent.com/30351807/115872339-470b0c00-a474-11eb-8339-109b82f464eb.png#vwid=992&vhei=241)](https://user-images.githubusercontent.com/30351807/115872339-470b0c00-a474-11eb-8339-109b82f464eb.png#vwid=992&vhei=241)

等待显示出 Starting server, listen at: 0.0.0.0:8899 访问 [http://127.0.0.1](http://127.0.0.1/):8899/ 显示下面界面即为正常。

[![image](https://user-images.githubusercontent.com/30351807/115872365-4ffbdd80-a474-11eb-8be6-cd4150242d66.png#vwid=903&vhei=205)](https://user-images.githubusercontent.com/30351807/115872365-4ffbdd80-a474-11eb-8be6-cd4150242d66.png#vwid=903&vhei=205)

linux 下安装可能会需要

[![image](https://user-images.githubusercontent.com/30351807/115872401-58ecaf00-a474-11eb-9a1a-e933173585a7.png#vwid=645&vhei=241)](https://user-images.githubusercontent.com/30351807/115872401-58ecaf00-a474-11eb-9a1a-e933173585a7.png#vwid=645&vhei=241)

安装即可

```bash
yum install libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64
```

### 验证码识别率

[![image](https://user-images.githubusercontent.com/30351807/115872436-61dd8080-a474-11eb-8971-02c7144ff91e.png#vwid=566&vhei=172)](https://user-images.githubusercontent.com/30351807/115872436-61dd8080-a474-11eb-8971-02c7144ff91e.png#vwid=566&vhei=172)

[![image](https://user-images.githubusercontent.com/30351807/115872450-673acb00-a474-11eb-8865-a12383727615.png#vwid=380&vhei=117)](https://user-images.githubusercontent.com/30351807/115872450-673acb00-a474-11eb-8865-a12383727615.png#vwid=380&vhei=117)

[![image](https://user-images.githubusercontent.com/30351807/115872463-6ace5200-a474-11eb-9a8e-a93de9ba0f47.png#vwid=300&vhei=131)](https://user-images.githubusercontent.com/30351807/115872463-6ace5200-a474-11eb-9a8e-a93de9ba0f47.png#vwid=300&vhei=131)

[![image](https://user-images.githubusercontent.com/30351807/115872476-702b9c80-a474-11eb-9d48-cdf2e02348d0.png#vwid=339&vhei=117)](https://user-images.githubusercontent.com/30351807/115872476-702b9c80-a474-11eb-9d48-cdf2e02348d0.png#vwid=339&vhei=117)

[![image](https://user-images.githubusercontent.com/30351807/115872496-73bf2380-a474-11eb-9d92-147c69e28452.png#vwid=321&vhei=122)](https://user-images.githubusercontent.com/30351807/115872496-73bf2380-a474-11eb-9d92-147c69e28452.png#vwid=321&vhei=122)

### 使用方法

把图片base64编码后POST发送至接口[http://localhost](http://localhost/):8899/base64 的base64参数即可，返回结果为识别的后的结果。

[![image](https://user-images.githubusercontent.com/30351807/115872517-791c6e00-a474-11eb-89ad-307efa56d7f1.png#vwid=1002&vhei=607)](https://user-images.githubusercontent.com/30351807/115872517-791c6e00-a474-11eb-89ad-307efa56d7f1.png#vwid=1002&vhei=607)

[![image](https://user-images.githubusercontent.com/30351807/115872532-7d488b80-a474-11eb-9886-74519894d224.png)](https://user-images.githubusercontent.com/30351807/115872532-7d488b80-a474-11eb-9886-74519894d224.png)

### burp联动识别验证码爆破

如果 server.py 在服务器上跑的话，xp_CAPTCHA.py需要修改对应的IP。

[![image](https://user-images.githubusercontent.com/30351807/115872564-85083000-a474-11eb-85b1-98523a93a60e.png)](https://user-images.githubusercontent.com/30351807/115872564-85083000-a474-11eb-85b1-98523a93a60e.png)

修改完后导入burp

[![image](https://user-images.githubusercontent.com/30351807/115872601-918c8880-a474-11eb-9b43-6aa958a12172.png)](https://user-images.githubusercontent.com/30351807/115872601-918c8880-a474-11eb-9b43-6aa958a12172.png)

[![image](https://user-images.githubusercontent.com/30351807/115872621-994c2d00-a474-11eb-8072-bbe22b2c8033.png)](https://user-images.githubusercontent.com/30351807/115872621-994c2d00-a474-11eb-8072-bbe22b2c8033.png)

Attack type处选择 Pitchfork,在http头部位置插入xiapao:验证码的URL地址

[![image](https://user-images.githubusercontent.com/30351807/115872650-a10bd180-a474-11eb-9a34-b30a974d145d.png)](https://user-images.githubusercontent.com/30351807/115872650-a10bd180-a474-11eb-9a34-b30a974d145d.png)

此处导入字典

[![image](https://user-images.githubusercontent.com/30351807/115872672-a79a4900-a474-11eb-818f-a3e0c47cfb21.png)](https://user-images.githubusercontent.com/30351807/115872672-a79a4900-a474-11eb-818f-a3e0c47cfb21.png)

选择验证码识别

[![image](https://user-images.githubusercontent.com/30351807/115872696-ad902a00-a474-11eb-814e-305faaa20756.png)](https://user-images.githubusercontent.com/30351807/115872696-ad902a00-a474-11eb-814e-305faaa20756.png)

[![image](https://user-images.githubusercontent.com/30351807/115872713-b1bc4780-a474-11eb-8e03-df7eab39885f.png)](https://user-images.githubusercontent.com/30351807/115872713-b1bc4780-a474-11eb-8e03-df7eab39885f.png)

然后把线程设置为1

[![image](https://user-images.githubusercontent.com/30351807/115872728-b5e86500-a474-11eb-8d4f-32344006ee36.png)](https://user-images.githubusercontent.com/30351807/115872728-b5e86500-a474-11eb-8d4f-32344006ee36.png)

### 源码

#### server.py

```python
#!/usr/bin/env python
# -*- conding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import muggle_ocr
import re,time,base64,os
 
host = ('0.0.0.0', 8899)
 
class Resquest(BaseHTTPRequestHandler):
    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())
 
    def do_GET(self):
        print(self.requestline)
        if self.path != '/':
            self.send_error(404, "Page not Found!")
            return
 
        data = '<title>xp_CAPTCHA</title><body style="text-align:center"><h1>验证码识别：xp_CAPTCHA</h1><a href="http://www.nmd5.com">author:算命縖子</a></body>'
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()
        self.wfile.write(data.encode())
 
    def do_POST(self):
        #print(self.headers)
        #print(self.command)
        if self.path != '/base64':
            self.send_error(404, "Page not Found!")
            return
 
        img_name = time.time()
        req_datas = self.rfile.read(int(self.headers['content-length']))
        req_datas = req_datas.decode()
        base64_img = re.search('base64=(.*?)$',req_datas)
        #print(base64_img.group(1)) #post base64参数的内容
 
        with open("temp/%s.png"%img_name, 'wb') as f:
            f.write(base64.b64decode(base64_img.group(1)))
            f.close()
 
        #验证码识别
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        with open(r"temp/%s.png"%img_name, "rb") as f:
            b = f.read()
        text = sdk.predict(image_bytes=b)
        print(text) #识别的结果
 
        #删除掉图片文件，以防占用太大的内存
        os.remove("temp/%s.png"%img_name)
 
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))
 
if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
```

#### xp_CAPTCHA.py

```python
#!/usr/bin/env python
#coding:gbk
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
import base64
import json
import re
import urllib2
import ssl
 
host = ('127.0.0.1', 8899)
 
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        #注册payload生成器
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        #插件里面显示的名字
        callbacks.setExtensionName("xp_CAPTCHA")
        print 'xp_CAPTCHA  中文名:瞎跑验证码\nblog：http://www.nmd5.com/\nT00ls：https://www.t00ls.net/ \nThe loner安全团队 author:算命縖子\n\n用法：\n在head头部添加xiapao:验证码的URL\n\n如：\n\nPOST /login HTTP/1.1\nHost: www.baidu.com\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0\nAccept: text/plain, */*; q=0.01\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\nX-Requested-With: XMLHttpRequest\nxiapao:http://www.baidu.com/get-validate-code\nContent-Length: 84\nConnection: close\nCookie: JSESSIONID=24D59677C5EDF0ED7AFAB8566DC366F0\n\nusername=admin&password=admin&vcode=8888\n\n'
 
    def getGeneratorName(self):
        return "xp_CAPTCHA"
 
    def createNewInstance(self, attack):
        return xp_CAPTCHA(attack)
 
class xp_CAPTCHA(IIntruderPayloadGenerator):
    def __init__(self, attack):
        tem = "".join(chr(abs(x)) for x in attack.getRequestTemplate()) #request内容
        cookie = re.findall("Cookie: (.+?)\r\n", tem)[0] #获取cookie
        xp_CAPTCHA = re.findall("xiapao:(.+?)\r\n", tem)[0]
        ssl._create_default_https_context = ssl._create_unverified_context #忽略证书，防止证书报错
        print xp_CAPTCHA+'\n'
        print 'cookie:' + cookie+'\n'
        self.xp_CAPTCHA = xp_CAPTCHA
        self.cookie = cookie
        self.max = 1 #payload最大使用次数
        self.num = 0 #标记payload的使用次数
        self.attack = attack
 
    def hasMorePayloads(self):
        #如果payload使用到了最大次数reset就清0
        if self.num == self.max:
            return False  # 当达到最大次数的时候就调用reset
        else:
            return True
 
    def getNextPayload(self, payload):  # 这个函数请看下文解释
        xp_CAPTCHA_url = self.xp_CAPTCHA #验证码url
 
        print xp_CAPTCHA_url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Cookie":self.cookie}
        request = urllib2.Request(xp_CAPTCHA_url,headers=headers)
        CAPTCHA = urllib2.urlopen(request) #获取图片
        CAPTCHA_base64 = base64.b64encode(CAPTCHA.read()) #把图片base64编码
 
        request = urllib2.Request('http://%s:%s/base64'%host, 'base64='+CAPTCHA_base64)
        response = urllib2.urlopen(request).read()
        print(response)
        return response
 
    def reset(self):
        self.num = 0  # 清零
        return
```

