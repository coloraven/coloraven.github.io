#pylint:disable=W0105
import requests,json,time,uuid,os
from aiohttp import ClientSession 
import asyncio
from Crypto.Cipher import AES
"""
PandaVpn_PRO 节点信息自动获取
"""


class AESCipher:
    """
    Tested under Python 3.x and PyCrypto 2.6.1.
    """

    def __init__(self, key='FfCcu4q6/x2z3XOO'):
        #加密需要的key值
        self.key=key.encode("utf-8")###
        self.BLOCK_SIZE = 256#16  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                        chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    def encrypt(self, raw):
        raw = self.pad(raw)
        #通过key值，使用ECB模式进行加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        #返回得到加密后的字符串进行解码然后进行64位的编码
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    def decrypt(self, enc):
        enc=enc.encode("utf-8")###
        #首先对已经加密的字符串进行解码
        enc = b64decode(enc)
        #通过key值，使用ECB模式进行解密
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_text = self.unpad(cipher.decrypt(enc)).decode('utf8')
        decrypted_text = decrypted_text.replace('\/','/')#网址正常化
        decrypted_text = decrypted_text.encode('utf8').decode('unicode_escape')#unicode字符转中文
        return decrypted_text


def gen_UUID() -> str:
    """
    生成/读取、返回UUID
    uuid：32位随机字符串
    """
    # isold = 1
    now = time.time()
    if os.path.exists('Panda_UUID'):
        with open('Panda_UUID') as f:
            data = json.load(f)
        if now-data['store_time'] >= 85680:
            print('Token失效，即将重新注册')
            UUID = "".join(str(uuid.uuid4()).split("-")).upper()
            # isold = 0
            with open('Panda_UUID', 'w') as f:
                json.dump({'store_time': now, 'UUID': UUID}, f)
        else:
            UUID = data['UUID']
            print('使用旧UUID：%s' % UUID)
    else:
        print('不存在UUID文件，即将新注册UUID写入文件')
        UUID = "".join(str(uuid.uuid4()).split("-")).upper()
        # isold = 0
        with open('Panda_UUID', 'w') as f:
            json.dump({'store_time': now, 'UUID': UUID}, f)
    return UUID


def get_number():
    """
    注册账号：纯数字ID
    返回：{"data":24167214}
    """
    while 1:
        _uuid = "21EF467FDBF12FB2F29D462C543A851E" # gen_UUID()
        api = 'https://api.panhvhg.xyz/api/register/user-number'
        headers = {
            "accept": "application/json",
            "Accept-Language": "zh-CN",
            "api-version": "v1.0",
            "device-identifier": _uuid,
            "device-type": "ANDROID",
            "product-identifier": "panda",
            "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
            "X-Timestamp": str(int(time.time())),
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "97",
            "Host": "api.panhvhg.xyz",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        form = {"clientVersion": "5.3.2",
                "deviceToken": _uuid, "deviceType": "ANDROID"}
        r = requests.post(api, headers=headers, json=form)
        if r.status_code == 200:
            try:
                userNumber = r.json()['data']
                return _uuid, userNumber
            except:
                continue


def trier_reg(_uuid,userNumber)->str:
    """
    申请试用
    返回：accessToken
    服务器返回数据：
    {
        "data":{
                "id":16626416,
                "userNumber":24167214,
                "emailChecked":false,
                "role":"TRIER",
                "registerAt":"2020-10-08T04:10:10Z",
                "accessToken":"eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2ODg1MzAyMTAsInVzZXJJZCI6MTY2MjY0MTYsImRldmljZUlkIjoxNjkyODYzNywiaWF0IjoxNjAyMTMwMjEwfQ.DdRVzrbrMKvW2_ZWVRBxn_DAdP2DoVvKQY3U_ryPca8","expireAt":"2023-07-05T04:10:09Z","dueTime":"2020-10-11T04:10:10Z","invitationLink":"https://www.panhdpe.xyz/i/24167214","maxDeviceCount":1,"webAccessToken":"919c36686ee0d647496aa4269340590bfca0",
                "resetPassword":true,
                "unreadMessageCount":0,
                "expireRemindType":"NEVER",
                "leftDays":3
                    }
            }"""

    api = 'https://api.panhvhg.xyz/api/register/trier-account-auto-generation'
    headers= {
                "accept": "application/json",
                "Accept-Language": "zh-CN",
                "api-version": "v1.0",
                "device-identifier": _uuid,
                "device-type": "ANDROID",
                "product-identifier": "panda",
                "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
                "X-Timestamp": str(int(time.time())),
                "Content-Type": "application/json; charset=UTF-8",
                "Content-Length": "180",
                "Host": "api.panhvhg.xyz",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }

    form = {
        "clientVersion": "5.3.2", 
        "deviceName": "Android 5.1.1 SDK 22 OnePlus HD1910",
        "deviceToken": _uuid, 
        "deviceType": "ANDROID", 
        "number": userNumber, 
        "password": ""
        }
    r=requests.post(api,headers=headers,json=form)
    print(r.json())
    if r.status_code==200:
        return r.json()['data']['accessToken'],r.json()['data']['webAccessToken']


def get_userinfo(_uuid):
    # 获取用户信息
    # 返回：accessToken
    # 服务器返回 {"data":{"id":16626416,"userNumber":24167214,"emailChecked":false,"role":"TRIER","registerAt":"2020-10-08T04:10:10Z","accessToken":"eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2ODg1MzAyMTAsInVzZXJJZCI6MTY2MjY0MTYsImRldmljZUlkIjoxNjkyODYzNywiaWF0IjoxNjAyMTMwMjEwfQ.DdRVzrbrMKvW2_ZWVRBxn_DAdP2DoVvKQY3U_ryPca8","expireAt":"2023-07-05T04:10:09Z","dueTime":"2020-10-11T04:10:12Z","invitationLink":"https://www.panhdpe.xyz/i/24167214","maxDeviceCount":1,"webAccessToken":"919c36686ee0d647496aa4269340590bfca0","resetPassword":true,"unreadMessageCount":0,"bindInvitationCodeSwitch":true,"expireRemindType":"NEVER","leftDays":3}}
    """
    GET https://api.panhvhg.xyz/api/users/info HTTP/1.1
    
    """
    api = "https://api.panhvhg.xyz/api/users/info"
    headers={
        "accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "zh-CN",
        "api-version": "v1.0",
        "device-identifier": _uuid,
        "device-type": "ANDROID",
        "product-identifier": "panda",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2ODg1MzAyMTAsInVzZXJJZCI6MTY2MjY0MTYsImRldmljZUlkIjoxNjkyODYzNywiaWF0IjoxNjAyMTMwMjEwfQ.DdRVzrbrMKvW2_ZWVRBxn_DAdP2DoVvKQY3U_ryPca8",
        "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
        "X-Timestamp": str(int(time.time())),
        "Host": "api.panhvhg.xyz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        }
    r=requests.get(api,headers=headers)
    if r.status_code==200:
        return r.json()['data']['accessToken'],r.json()['data']['webAccessToken']


def get_all_tagid(_uuid,accessToken)->dict:
    url ='https://api.panhvhg.xyz/api/v2/channels/with-group'
    headers = {
        "api-version": "v2.0",
        "accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "zh-CN",
        "device-identifier": _uuid,
        "device-type": "ANDROID",
        "product-identifier": "panda",
        "Authorization": "Bearer %s"%accessToken,
        "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
        "X-Timestamp": str(int(time.time())),
        "Host": "api.panhvhg.xyz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
                    }
    r=requests.get(url,headers=headers)
    print(r.json())
    # print('with-group:\t',r.json())
    # result=[]
    # if r.status_code == 200:
    #     for group in r.json()['data'][0]["levelRelationshipList"]:
    #         if 'SVIP 线路' in group['name']: #使用组名过滤
    #             r1 = [{'group':group['name'],'tag_id':sub_server['id'],'name':sub_server['name'].replace("[SVIP]","").replace(" ","")} for sub_server in group['relationChannels']]
    #             result+=r1
    #     return result


def get_server_config(_uuid,tagid,accessToken):
    """
    获取单个节点配置信息
    """
    url = 'https://api.panhvhg.xyz/api/v3/channels/%s/connect'%tagid
    headers={
        "api-version": "v3.0",
        "request_raw_response_body_tag_header": "8",
        "accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "zh-CN",
        "device-identifier": _uuid,
        "device-type": "ANDROID",
        "product-identifier": "panda",
        "Authorization": "Bearer %s"%accessToken,
        "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
        "X-Timestamp": str(int(time.time())),  # 时间戳
        "Content-Length": "0",
        "Host": "api.panhvhg.xyz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
            }
    r = requests.post(url,headers=headers)
    print(r.json())
    return r.json()


async def request(sem, _uuid,tag_id,accessToken):
        h_detail = {
        "api-version": "v3.0",
        "request_raw_response_body_tag_header": "8",
        "accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "zh-CN",
        "device-identifier": _uuid,
        "device-type": "ANDROID",
        "product-identifier": "panda",
        "Authorization": "Bearer %s"%accessToken,
        "User-Agent": "okhttp/3.8.0 android/5.1.1(HD1910) panda/5.3.2(74)",
        "X-Timestamp": str(int(time.time())),
        "Content-Length": "0",
        "Host": "api.panhvhg.xyz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
            }
        async with sem:
                async with ClientSession() as session:
                        async with session.post('https://api.panhvhg.xyz/api/v3/channels/%i/connect'%tag_id,headers=h_detail) as response:
                                r = await response.json()
                                print(r)
                                if 'data' in r:
                                    encrypt_server_config_info=r["data"]
                                    decrypted_config=AESCipher("panda&beta#12345").decrypt(encrypt_server_config_info)
                                    decrypted_config=json.loads(decrypted_config)
                                    decrypted_config = {'method':decrypted_config['method'],'server':decrypted_config['server'][0],'server_port':decrypted_config['server_port'],'password':decrypted_config['password']}
                                    print(decrypted_config)
                                    return decrypted_config
                                else:
                                        print(r)
                                        return {'tag_id':tag_id}


def async_get_detail(args:list,uuid,access_token):
        loop = asyncio.get_event_loop()
        tasks = []
        ######################
        #  限制协程并发量
        ######################
        sem = asyncio.Semaphore(100)  # 限制并发数
        for tag_id in args:
                        task = asyncio.ensure_future(request(sem,uuid, tag_id,access_token))
                        tasks.append(task)
        
        feature = asyncio.ensure_future(asyncio.gather(*tasks))
        results=loop.run_until_complete(feature)
        return results


if __name__ == "__main__":
    uuid,userNumber=get_number()
    print('uuid:\t',uuid,'userNumber:\t',userNumber)
    # accessToken,webAccessToken=trier_reg(uuid,userNumber)
    accessToken,webAccessToken=get_userinfo(uuid)
    print('accessToken:\t',accessToken,'webAccessToken:\t',webAccessToken)
    get_all_tagid(uuid,accessToken)
    print(get_server_config(uuid,'1190',accessToken))