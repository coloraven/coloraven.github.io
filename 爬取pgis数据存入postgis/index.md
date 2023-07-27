# 爬取PGIS数据，存入POSTGIS


## 第一步：爬取PGIS数据
```python
import requests,json

session = requests.session()

cookies=""

def getcodes(parents_code:str=430100000000)->list:
    headers ={
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "15",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookies,
        "Host": "65.47.1.103",
        "Origin": "http://65.47.1.103",
        "Referer": "http://65.47.1.103/PGIS_APP_Collection/app/area/main",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://65.47.1.103/PGIS_APP_Collection/app/ztree/getOrgTree"
    formdata = {
    "id": parents_code
    }
    r=session.post(url,data=formdata,headers=headers)
    qxdm = [{i["name"]:i['id']} for i in r.json()]
    return qxdm
    # print(r.json())

# print(getcodes())

def GetGeoJson(dm:str):
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "159",
        "Content-Type": "application/json",
        "Cookie": cookies,
        "Host": "65.47.1.103",
        "Origin": "http://65.47.1.103",
        "Referer": "http://65.47.1.103/PGIS_APP_Collection/app/area/main",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://65.47.1.103/PGIS_APP_Collection/app/collection/function/query"
    pre_payload={"from":0,"size":1,
                 "query":{"bool":{"must":{"match":{
                                 "zzjgdm": dm
                                 }}}}}
    payload={"endpoint":"/gis430100000000/fq_jyglfq_pg/_search",
             "json":json.dumps(pre_payload)
            }
    r=session.post(url,data=json.dumps(payload),headers=headers)
    result = r.json()
    data = json.loads(r.json()['data'])
    result['data']=data
    # return result
    try:
        result = result['data']['hits']['hits'][0]["_source"]['shape']['coordinates']
        return result
    except Exception as e:
        print(data)
        print(e)

# x=GetGeoJson("430124000000")
# print(x)

qx_codes:list = getcodes()

quanshi = [] # 存放全市结果
# quxian = [] # 存放区县结果
# SqGeoJsons = [] # 存放社区结果
# PcsGeoJsons = [] # 存放派出所结果
for qx in qx_codes:
    qxname,qxcode=list(qx.items())[0]
    print(qxname,qxcode)
    QxGeoJson = GetGeoJson(qxcode)
    pcs_codes = getcodes(qxcode)
    PcsGeoJsons_ = []
    for pcs in pcs_codes:
        pcs_name,pcs_code=list(pcs.items())[0]
        print('\t',pcs_name,pcs_code)
        PcsGeoJson= GetGeoJson(pcs_code)
        sq_codes = getcodes(pcs_code)
        SqGeoJson_ = []
        for sq in sq_codes:
            sq_name,sq_code=list(sq.items())[0]
            print('\t\t',sq_name,sq_code)
            SqGeoJson = GetGeoJson(sq_code)
#             SqGeoJsons.append({"name":sq_name,'qxdm':qxcode,'pcsdm':pcs_code,"sqdm":sq_code,"coordinates":SqGeoJson}) #总表
            SqGeoJson_.append({"name":sq_name,'qxdm':qxcode,'pcsdm':pcs_code,"sqdm":sq_code,"coordinates":SqGeoJson}) #临时表
        PcsGeoJsons_.append({"name":pcs_name,'qxdm':qxcode,'pcsdm':pcs_code,"coordinates":PcsGeoJson,'社区':SqGeoJson_}) #临时表
#         PcsGeoJsons.append({"name":pcs_name,'qxdm':qxcode,'pcsdm':pcs_code,"coordinates":PcsGeoJson,'社区':SqGeoJson_}) #总表
    quxian.append({"name":qxname,'qxdm':qxcode,"coordinates":QxGeoJson})
#     quanshi.append({"name":qxname,'qxdm':qxcode,"coordinates":QxGeoJson,'派出所':PcsGeoJsons_})

with open(r"结果\全市-关系数据.json", "w", encoding="utf-8") as f:
    json.dump(quanshi, f, ensure_ascii=False)

# with open(r"结果\区县.json", "w", encoding="utf-8") as f:
#     json.dump(quxian, f, ensure_ascii=False)

# with open(r"结果\派出所.json", "w", encoding="utf-8") as f:
#     json.dump(PcsGeoJsons, f, ensure_ascii=False)

# with open(r"结果\社区.json", "w", encoding="utf-8") as f:
#     json.dump(SqGeoJsons, f, ensure_ascii=False)
```

## 第二步：搭建POSTGIS（最快的空间数据库）
docker一键搭建，搭建完后，使用数据库管理软件连接数据库，并新建数据库，这时我们的demo数据库只是个普通的postgresql数据库，是不支持空间相关功能的，在新建的数据库上执行`CREATE EXTENSION postgis`来为该数据库安装postgis扩展模块，成功之后我们的数据库就变成了空间数据库，支持空间相关的各种功能。[具体请参考](https://blog.51cto.com/u_15064641/2598516)
## 第三步：将第一步爬取的数据存入POSTGIS数据库中
代码如下：
```python
import json

import geojson
from geopandas import GeoDataFrame, GeoSeries
from shapely.geometry import shape
from sqlalchemy import create_engine

# 将geodataframe写入postgis
# Set up database connection engine
# 数据库类型://用户名:密码@主机IP:端口/数据库名称
dbconfig = "postgresql://postgres:password@192.168.1.100:54321/geotest"
# 创建引擎
engine = create_engine(dbconfig)

def write2postgis(gdf: GeoDataFrame, tablename: str):
    # GeoDataFrame to PostGIS
    gdf.to_postgis(
        con=engine,
        name=tablename,
    )

def to_wkt(geojson_obj):
    # geojson = {"coordinates":[[[23.314208,37.768469],[24.039306,37.768469],[24.039306,38.214372],[23.314208,38.214372],[23.314208,37.768469],]],"type":"Polygon",}
    s = json.dumps(geojson_obj)
    g1 = geojson.loads(s)
    g2 = shape(g1)
    return g2.wkt

with open("/opt/notebooks/全市PGIS信息/最新脚本及结果/全市-关系数据.json", "r", encoding="utf-8") as f:
    datas = json.load(f)

result = []
pcs_result = []
sq_result = []
for quxian in datas:
    # 第一层
    geojson_data = {"type": "Polygon", "coordinates": []}  # 字段名  # 字段类型
    if quxian["coordinates"]:
        geojson_data["coordinates"] = quxian["coordinates"]
        try:
            polygon_wkt = to_wkt(geojson_data)
        except:
            geojson_data["type"] = "MultiPolygon"
            polygon_wkt = to_wkt(geojson_data)
        result.append(
            {
                "name": quxian["name"],
                "code": int(quxian["qxdm"]),
                "geometry": polygon_wkt,
            }
        )
    # 第二层
    for pcs in quxian["派出所"]:
        geojson_data = {"type": "Polygon", "coordinates": []}  # 字段名  # 字段类型
        if pcs["coordinates"]:
            geojson_data["coordinates"] = pcs["coordinates"]
            try:
                polygon_wkt = to_wkt(geojson_data)
            except:
                geojson_data["type"] = "MultiPolygon"
                polygon_wkt = to_wkt(geojson_data)
            pcs_result.append(
                {
                    "name": pcs["name"],
                    "code": int(pcs["pcsdm"]),
                    "qxname": quxian["name"],
                    "geometry": polygon_wkt,
                }
            )
        # 第三层
        for sq in pcs["社区"]:
            geojson_data = {"type": "Polygon", "coordinates": []}  # 字段名  # 字段类型
            if sq["coordinates"]:
                geojson_data["coordinates"] = sq["coordinates"]
                try:
                    polygon_wkt = to_wkt(geojson_data)
                except:
                    geojson_data["type"] = "MultiPolygon"
                    polygon_wkt = to_wkt(geojson_data)
                sq_result.append(
                    {
                        "name": sq["name"],
                        "code": int(sq["pcsdm"]),
                        "qxname": quxian["name"],
                        "pcsname": pcs["name"],
                        "geometry": polygon_wkt,
                    }
                )

quxian_df = GeoDataFrame(result)
quxian_df["geometry"] = GeoSeries.from_wkt(
    quxian_df["geometry"], crs=4326
)  # 将geometry列转为geopandas的空间对象，crs坐标系为WGS84
# df.head(11)
write2postgis(quxian_df, "QuXian")

pcs_df = GeoDataFrame(pcs_result)
pcs_df["geometry"] = GeoSeries.from_wkt(
    pcs_df["geometry"], crs=4326
)  # 将geometry列转为geopandas的空间对象，crs坐标系为WGS84
# df.head(11)
write2postgis(pcs_df, "PCS")

sq_df = GeoDataFrame(sq_result)
sq_df["geometry"] = GeoSeries.from_wkt(
    sq_df["geometry"], crs=4326
)  # 将geometry列转为geopandas的空间对象，crs坐标系为WGS84
# df.head(11)
write2postgis(sq_df, "SheQu")
```
