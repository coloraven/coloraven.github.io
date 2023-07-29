# 撸飞鸟加速器

```python
import requests,random,time

def register():
    deviceid = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',20)+random.sample('abcdefghijklmnopqrstuvwxyz1234567890',20))
    headers = {
        'User-Agent': 'okhttp/3.10.0',
        'device': deviceid,
        'platform': 'android',
        'device_id': deviceid,
        'token': '',
        'channel': '1',
        'Content-Length': '0',
        'Host': 'and.feiniaojiasu.com:10000',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }

    params = (
        ('device_id', deviceid),
        ('channel', '1'),
    )

    response = requests.post('http://and.feiniaojiasu.com:10000/api/user/tourist', headers=headers, params=params)
    # print(response.json())
    try:
        token=response.json()["data"]["token"]
        print('device_id:\t',deviceid)
        print('token:\t',token)
        return deviceid,token
    except:
        print(response.json())


def nodes_detail(device_id,token,_id):
    headers = {
                'User-Agent': 'okhttp/3.10.0',
                'device': device_id,
                'platform': 'android',
                'device_id': device_id,
                'token': token,
                'channel': '1',
                'Content-Length': '0',
                'Host': 'and.feiniaojiasu.com:10000',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
            }
    params = (
        ('id', _id),
        ('token', token),
    )
    url =  'http://and.feiniaojiasu.com:10000/api/mine/serviceDetail'
    r= requests.post(url, headers=headers, params=params)
    try:
        print(r.json()['data']['name']+r.json()['data']['bandwidth'],r.json()['data']['service_str'])
    except:
        print(r.json())


def get_nodes(device_id,token):
    headers = {
        'User-Agent': 'okhttp/3.10.0',
        'device': device_id,
        'platform': 'android',
        'device_id': device_id,
        'token': token,
        'channel': '1',
        'Content-Length': '0',
        'Host': 'and.feiniaojiasu.com:10000',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }

    params = (
        ('vip', '1'),
        ('token', token),
    )

    response = requests.get('http://and.feiniaojiasu.com:10000/api/mine/service', headers=headers, params=params)
    return response.json()['data']


device_id,token = register()
nodes = {"status":1,"message":"成功","data":[{"id":266,"name":"超级线路（Tw11）","type":1,"pro":76,"vip":1,"ip_num":228,"bandwidth":600,"ip_max":300,"created_at":"2021-11-17 15:04:12"},{"id":267,"name":"超级线路（Tw10）","type":1,"pro":70,"vip":1,"ip_num":210,"bandwidth":600,"ip_max":300,"created_at":"2021-11-21 10:03:44"},{"id":257,"name":"超级线路（Tw）","type":1,"pro":71,"vip":1,"ip_num":250,"bandwidth":600,"ip_max":350,"created_at":"2021-10-01 18:12:59"},{"id":246,"name":"超级线路（Tw7）","type":1,"pro":70,"vip":1,"ip_num":246,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:57:02"},{"id":252,"name":"超级线路（Tw0）","type":1,"pro":71,"vip":1,"ip_num":250,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 14:12:01"},{"id":237,"name":"超级线路（Tw1）","type":1,"pro":72,"vip":1,"ip_num":255,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:36:32"},{"id":238,"name":"超级线路（Tw3）","type":1,"pro":71,"vip":1,"ip_num":251,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:39:27"},{"id":239,"name":"超级线路（Tw5）","type":1,"pro":71,"vip":1,"ip_num":251,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:39:45"},{"id":250,"name":"超级线路（Tw8）","type":1,"pro":72,"vip":1,"ip_num":254,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 14:05:26"},{"id":249,"name":"超级线路（Tw9）","type":1,"pro":69,"vip":1,"ip_num":243,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 14:04:22"},{"id":245,"name":"超级线路（Tw6）","type":1,"pro":52,"vip":1,"ip_num":185,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:56:57"},{"id":240,"name":"超级线路（Tw4）","type":1,"pro":44,"vip":1,"ip_num":154,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:41:02"},{"id":243,"name":"超级线路（Hk1）","type":2,"pro":48,"vip":1,"ip_num":170,"bandwidth":50,"ip_max":350,"created_at":"2021-09-04 13:47:06"},{"id":236,"name":"超级线路（Hk3）","type":1,"pro":0,"vip":1,"ip_num":0,"bandwidth":600,"ip_max":350,"created_at":"2021-09-04 13:36:21"},{"id":255,"name":"超级线路（Us1）","type":2,"pro":8,"vip":1,"ip_num":29,"bandwidth":100,"ip_max":350,"created_at":"2021-09-12 22:24:02"},{"id":242,"name":"超级线路（Us2）","type":1,"pro":2,"vip":1,"ip_num":6,"bandwidth":1000,"ip_max":300,"created_at":"2021-09-04 13:44:45"},{"id":241,"name":"超级线路（Us3）","type":1,"pro":8,"vip":1,"ip_num":24,"bandwidth":1000,"ip_max":300,"created_at":"2021-09-04 13:43:53"},{"id":253,"name":"超级线路（Us4）","type":2,"pro":1,"vip":1,"ip_num":4,"bandwidth":100,"ip_max":300,"created_at":"2021-09-04 14:17:00"},{"id":247,"name":"超级线路（Hk5）","type":1,"pro":19,"vip":1,"ip_num":69,"bandwidth":1000,"ip_max":350,"created_at":"2021-09-04 14:01:24"},{"id":244,"name":"超级线路（Jp1）","type":2,"pro":20,"vip":1,"ip_num":40,"bandwidth":50,"ip_max":200,"created_at":"2021-09-04 13:47:44"},{"id":231,"name":"超级线路（Jp2）","type":2,"pro":5,"vip":1,"ip_num":10,"bandwidth":50,"ip_max":200,"created_at":"2021-09-04 12:32:22"},{"id":233,"name":"超级线路（Jp3）","type":2,"pro":27,"vip":1,"ip_num":55,"bandwidth":100,"ip_max":200,"created_at":"2021-09-04 13:33:06"},{"id":254,"name":"超级线路（Kr1）","type":1,"pro":0,"vip":1,"ip_num":2,"bandwidth":1024,"ip_max":400,"created_at":"2021-09-04 14:20:00"},{"id":248,"name":"超级线路（Hk4）","type":1,"pro":5,"vip":1,"ip_num":23,"bandwidth":1000,"ip_max":400,"created_at":"2021-09-04 14:01:30"},{"id":232,"name":"超级线路（Kr2）","type":2,"pro":18,"vip":1,"ip_num":37,"bandwidth":20,"ip_max":200,"created_at":"2021-09-04 13:27:19"}]}
for node in nodes['data']:
    _id = node['id']
    nodes_detail(device_id,token,_id)
    time.sleep(3)
```

AES/CBC/PKCS5Padding：
密钥：z7HyKhkHBbYW9bktlyAQCIijwsf45sxm
I V：1238389483762837

![2021-11-22T195738](2021-11-22T195738.png)





