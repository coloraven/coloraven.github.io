# 利用大厂API作为图床

## 源于`即刻图床`
偶然遇到`即刻图床`这款插件，打开了我的新世界大门。
即刻图床利用阿里、京东、新浪等大厂的API上传图片作为图床，无需注册，无上传个数限制，无流量限制，且访问速度超快。
下面是各厂商图床API的python实现代码
## JD
```python 京东API
import requests,base64,lxml.html,json,os
from requests_toolbelt import MultipartEncoder


def img_to_base64(imagefile):
    image_data = open(imagefile, 'rb').read()
    return base64.b64encode(image_data)


def upload_to_JD(imagefile):
    url = 'https://imio.jd.com/uploadfile/file/post.do'
    headers = {
        'authority': 'imio.jd.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'dnt': '1',
        'accept': 'application/json',
        'origin': 'chrome-extension://dckaeinoeaogebmhijpkpmacifmpgmcb',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'cookie': 'shshshfpa=file-dd.jd.local_file-dd.jd.local',
    }

    form_data = {
      'appId': 'im.customer',
      'aid': 'undefined',
      'clientType': 'comet',
      'pin': 'undefined',
      's': img_to_base64(imagefile)
    }

    # 生成可用于multipart/form-data上传的数据
    m = MultipartEncoder(form_data)
    # 自动生成Content-Type类型和随机码
    headers['Content-Type'] = m.content_type

    # 使用data上传文件
    r = requests.post(url, headers=headers, data=m)
    json_strs = lxml.html.document_fromstring(r.text).find('body').text
    try:
        json_obj = json.loads(json_strs)
        if json_obj['desc'] == "上传成功":
            print(json_obj['path'])
            return json_obj['path']
        else:
            print(imagefile,json_obj)
    except Exception as e:
        print('遇到错误:',e,'图片文件：','')


'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    # filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    # fsize = fsize/float(1024*1024)
    return fsize


if __name__ == '__main__':
    files = os.listdir() # 获取当前目录中的文件名
    result = {}
    for file in files:
        if get_FileSize(file) <= (10*1024*1024):
            imgurl = upload_to_JD(file)
            result[file]=imgurl
    with open('upload_result.json','w',encoding='utf-8') as f:
        json.dump(result,f)
```
