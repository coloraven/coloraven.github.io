# pymongo操作

## 修改数据库中的值
数据量小的情况下，
1.先全部查询`find()`；
2.清空数据库`delete_many({})`;
3.修改;
4.完毕后再插入数据库`collection.insert_many(result, ordered=False)`。

## 随机查询
```python 实现随机返回一条符合条件的记录
with MongoClient("mongodb://local/?authSource=admin") as client:
    c =client.DBs.collection
#     regx = re.compile(".*?台湾|日本|香港|韩国|新加坡.*?")
    r = c.aggregate( [ {"$match":# 筛选条件
                            {"$text":{ 
                                "$search": "台湾|日本|香港|韩国|新加坡" #建立相应字段索引后进行文本搜索
                                }
                                }
                        } ,
                        { "$sample":  # 随机取样
                            { 
                            "size": 1 # 取样的数量
                            } 
                        } 
                     ]
                    )
```
