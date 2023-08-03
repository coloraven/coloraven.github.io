# Postgres快速导入csv文件

## `psql`的`copy`命令导入
### 第一步
连接数据库：
`psql -U <user_name> -d <database_name> -h 远程数据库IP地址 -p 端口`，
`psql`位于安装目录的bin目录下，建议将路径`X:\XXX\PostgreSQL\15\bin\`添加到环境变量中
如果想免密码，则需要设置环境变量 PGPASSWORD

### 第二步
使用`\copy`命令导入，该命令必须在服务端运行，不能通过`pg_admin`、`dbeaver`等数据库管理客户端的`sql`命令执行。
`\copy bbb FROM 'D:\NavicatExports\aaa.csv' DELIMITER ',' NULL '' CSV HEADER;`
其中`bbb`是事先创建好的表的名称，下同
### 常见错误
**报错:** `ERROR:  character with byte sequence 0xba 0x22 in encoding "GBK" has no equivalent in encoding "UTF8"`
**原因:** `csv`文件内容为`utf-8 no bom`编码，其中有中文。
**解决方案:** `\encoding UTF8`

### 其他
#### 启用计时功能——可查看导入等操作的耗时
`\timing`
#### 切换数据库
`\c 目标数据库名`
#### 导入时的目标表名不能是中文，csv文件名可以是中文

通过实践，目标表名不能是中文，但文件名可以是中文。
`\copy bbb FROM 'C:\我是中文.csv' WITH (FORMAT CSV,DELIMITER ',' , HEADER TRUE);`

#### csv文件的分隔符为Tab符的表达
`\copy bbb FROM 'C:\我是中文.csv' WITH (FORMAT CSV,DELIMITER E'\t' , HEADER TRUE);`

## 另外的方式
### pgfutter--自动建表
专用于`postgresql`的导入工具[`pgfutter`](https://github.com/lukasmartinelli/pgfutter)，支持 `CSV` 和 `JSON` 格式数据的导入。
使用方法：
```sh
pgfutter --host "地址" --db "数据库" --port "端口" --user "用户名" --pw "密码" --schema "public" --table "表名" csv 待导入的csv文件.csv
```

Database connection details can be provided via environment variables or as separate flags.
| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `DB_NAME` | `postgres` | database name |
| `DB_HOST` | `localhost` | host name |
| `DB_PORT` | `5432` | port |
| `DB_SCHEMA` | `import` | schema to create tables for |
| `DB_USER` | `postgres` | database user |
| `DB_PASS` |  | password (or empty if none) |

更多用法参见[官方文档](https://github.com/lukasmartinelli/pgfutter/blob/master/README.md)

经测试，导入时对第一行最后一列为空的数据的数据导入出错。
### pgloader
#### 支持从文件加载或迁移数据库
其中数据库迁移包括：
- 从 MySQL 迁移到 PostgreSQL
- 从 SQLite 迁移到 PostgreSQL
- 从 MS SQL Server® 迁移到 PostgreSQL
其中文件包括：
- CSV 系列
- 固定列格式---作者也不清楚是什么
- dBase 文件 ( db3) 
- IBM IXF 文件
#### 其他特色亮点
- pgloader 支持存档格式zip、tar和gzip ：直接在临时文件中提取存档，然后加载扩展文件。
- 支持`出错时停止`或者`出错时继续`
#### 缺点
- 导入参数必须通过脚本文件定义，然后再通过pgloader加载脚本来导入。
