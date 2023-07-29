# LeanCloud数据库操作

## 新建表与添加记录

```python 新建表与添加记录
import leancloud

leancloud.init("AppID", "AppKey")
# 或者使用 Master Key
# leancloud.init("AppID-gzGzoHsz", master_key="master_key")
# 新建表
tableObject = leancloud.Object.extend('表名') # 新建表
tableObject = tableObject()
# 增加一条记录
x = tableObject.set({'a':[{'a':1}],'b':'randombg'})
x.add('abc','dddd')#在此行末尾新增字段，待实验
# 提交到服务器
tableObject.save()

```

## 条件查询表格

```python 条件查询表格
# 查询表
query = leancloud.Query('RandomBG')  # 这里也可以直接传递一个 Class 名字的字符串作为构造参数

# 方法一：返回唯一值
result = query.get('61833be7cf725328f0274093')
print(result.dump()) # 返回唯一记录的dict对象值
print(result.get('wallhaven')) # 查询返回唯一记录的某个字段值
result.set('wallhaven',[{'abc':333}]) # 对唯一返回进行修改
result.save() # 对唯一返回进行修改

# 方法二：返回所有值
reslut = query.find()
for i in reslut:
    i.set('wallhaven',[{'333':333}])
    i.save()
```


