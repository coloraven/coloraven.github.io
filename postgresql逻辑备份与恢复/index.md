# postgresql逻辑备份与恢复

## 背景
拿到一个`postgresql`数据库导出的`SQL`备份文件（4.3G大小），需要重新导入数据库中开展后续工作。
## 弯路
使用`postgresql`官方管理工具`pgAdmin`及有名的`Navicat`进行导入操作，均报错。因工作急需将备份文件恢复到数据库，转而使用`emeditor`打开，并使用正则匹配的方式提取需要的字段，再导入数据库，因数据量庞大，硬件性能有限，整个过程花费将近3个小时。
## 解决
虽然走弯路解决了问题，但是备份文件所承载的数据信息仍未完整呈现。于是不停地网上搜索，发现下面链接：https://www.xmmup.com/pgluojibeifenhuifuluojidaochudaoru.html
### 找到psql.exe文件，运行如下命令。
`psql --username=postgres --host=192.168.66.35 --port=15433 --dbname=sbtest --file=/bk/sbtest.sql`
