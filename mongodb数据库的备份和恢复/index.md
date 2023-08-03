# MongoDB数据库的备份和恢复


[**https://blog.51cto.com/jack88/2145833**](https://blog.51cto.com/jack88/2145833)



mongodb数据备份和恢复主要分为二种：

> 一种是针对库的mongodump和mongorestore，
>
> 一种是针对库中表的mongoexport和mongoimport。

## 一、 mongodump备份数据库

### 1.常用命令格式

​                mongodump -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -c 表 -o 文件存放路径              

参数说明：-h 指明数据库宿主机的IP--port 指明数据库的端口 -u 指明数据库的用户名-p 指明数据库的密码-d 指明数据库的名字-c 指明collection的名字-o 指明到要导出的文件名-q 指明导出数据的过滤条件

### 2.导出所有数据库

```bash
mongodump -o /data/mongobak/            
```

### 3.导出指定数据库

```bash
mongodump -d SERVERLOG -o /data/mongobak/SERVERLOG.bak/       
```

​       

## 二、 mongorestore恢复数据库

自行补充：

恢复其他数据库中的表到已有数据库中，已有数据库已经有表，且数据库有账号密码验证：

```bash
mongorestore -u 用户名 -p 密码 --authenticationDatabase admin -d leanote --dir /leanote_install_data/
```

### 1.常用命令格式

​                mongorestore -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 --drop 文件存在路径              

​                --drop：先删除所有的记录，然后恢复.              

### 2.恢复所有数据库到mongodb中

​                mongorestore /data/mongobak/ #所有库的备份路径              

### 3. 恢复指定的数据库

```bash
mongorestore -d SERVERLOG /data/mongobak/SERVERLOG.bak/SERVERLOG/ # SERVERLOG这个数据库的备份路径 mongorestore -d SERVERLOG_new /data/mongobak/SERVERLOG.bak/SERVERLOG/ #将SERVERLOG备份数据还原到SERVERLOG_new数据库中    
```

​          

## 三、 mongoexport导出（表或者表中部分字段）

### 1. 常用命令格式

```bash
mongoexport -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -c 表名 -f 字段 -q 条件导出 --csv -o 文件名    
```

​          

参数重点说明：-f 导出指定字段，以逗号分割，-f uid,name,age导出uid,name,age这三个字段-q 可以根据查询条件导出，-q '{ "uid" : "100" }' 导出uid为100的数据--csv 表示导出的文件格式为csv的。这个比较有用，因为大部分的关系型数据库都是支持csv，在这里有共同点

### 2. 导出整张表

```bash
mongoexport -d SERVERLOG -c users -o /data/mongobak/SERVERLOG.bak/
# users.dat connected to: 127.0.0.1 exported 4 records 
```

### 3. 导出表中部分字段

```bash
mongoexport -d SERVERLOG -c users --csv -f uid,name,age -o /data/mongobak/SERVERLOG.bak/
# users.csv connected to: 127.0.0.1 exported 4 records
```

### 4. 根据条件导出数据

```bash
mongoexport -d SERVERLOG -c users -q '{uid:{$gt:1}}' -o /data/mongobak/SERVERLOG.bak/
# users.json connected to: 127.0.0.1 exported 3 records
```



## 四、 mongoimport导入（表或者表中部分字段）

### 1. 常用命令格式

恢复整表导出的非csv文件

```bash
mongoimport -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -c 表名 --upsert --drop 文件名
```

> --upsert:插入或者更新现有数据

恢复部分字段的导出文件

```bash
mongoimport -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -c 表名 --upsertFields 字段 --drop 文件名
```

> --upsertFields:更新部分的查询字段，必须为索引,以逗号分隔.

恢复导出的csv文件

```bash
mongoimport -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -c 表名 --type 类型 --headerline --upsert --drop 文件名
```

> --type：导入的文件类型（默认json）

### 2. 恢复导出的表数据

```bash
mongoimport -d SERVERLOG -c users --upsert /data/mongobak/SERVERLOG.bak/
# users.dat connected to: 127.0.0.1 Tue Dec 3 08:26:52.852 imported 4 objects
```



### 3. 部分字段的表数据导入

```bash
mongoimport -d SERVERLOG -c users --upsertFields uid,name,age /data/mongobak/SERVERLOG.bak/
# users.datconnected to: 127.0.0.1 Tue Dec 3 08:31:15.179 imported 4 objects
```

### 4. 恢复csv文件

```bash
mongoimport -d SERVERLOG -c users --type csv --headerline --file /data/mongobak/SERVERLOG.bak/
# users.csv connected to: 127.0.0.1 Tue Dec 3 08:37:21.961 imported 4 objects
```

> --file:需要导入的文件

