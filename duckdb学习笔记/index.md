# DuckDB学习笔记

## 概述
貌似`duckdb`能自动识别文件的`encoding`。
## 实现`emeditor`的列拆分功能
### 关键函数
1. regexp_matches，查询字符串是否包含`正则表达式字符`
2. regexp_split_to_array，按给定的`正则表达式字符`进行拆分
3. unnest，将数组转为行
4. contains，判断是否包含特定字符（不支持正则表达式）
### 数据样本
| phone | introduce        | name           |
|-------|------------------|----------------|
| 111   | New York&#124;Chicago | Jean Vasquez   |
| 222   | HK;Tokoy&#124;USA     | Nakayama Yuito |
| 333   | Chinese Shanghai | Jean Vasquez   |
### 以单个分隔符拆分
#### `duckdb`代码
```sql
--对包含;的列进行拆分，然后转为行。注意：UNION ALL 前后的列顺序必须一致
SELECT
    --与 UNION ALL 关键字 后面的列顺序必须一致
	phone,
	UNNEST(regexp_split_to_array(introduce,	';')) introduce,
	name
FROM
	read_csv('testfile.csv', delim=',', header=True, columns={'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR'})
WHERE
	contains(introduce,	';')
UNION ALL
-- 与不包含;的行进行合并，实际中要去掉
SELECT
    --与 UNION ALL 关键字 前面的列顺序必须一致
	*
FROM
	read_csv('testfile.csv', delim=',', header=True, columns={'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR'})
WHERE
	not contains(introduce,	';')
```
#### 结果
| phone | introduce        | name           |
|-------|------------------|----------------|
| 222   | HK               | Nakayama Yuito |
| 222   | Tokoy&#124;USA        | Nakayama Yuito |
| 111   | New York&#124;Chicago | Jean Vasquez   |
| 333   | Chinese Shanghai | Jean Vasquez   |

### 以多个分隔符进行拆分
支持按多个分隔符进行列拆分，此处为将`introduce`列按`;`和`|`进行拆分。
#### `duckdb`代码
```sql
SELECT
	phone,
	UNNEST(regexp_split_to_array(introduce,	'[;|]')) introduce,
	name
	
FROM
	read_csv('testfile.csv', delim=',', header=True, columns={'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR'})
WHERE
	regexp_matches(introduce,'[;|]')
UNION ALL
SELECT
	*
FROM
	read_csv('testfile.csv', delim=',', header=True, columns={'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR'})
WHERE
	not regexp_matches(introduce,'[;|]')
```
#### 结果
| phone | introduce        | name           |
|-------|------------------|----------------|
| 111   | New York         | Jean Vasquez   |
| 111   | Chicago          | Jean Vasquez   |
| 222   | HK               | Nakayama Yuito |
| 222   | Tokoy            | Nakayama Yuito |
| 222   | USA              | Nakayama Yuito |
| 333   | Chinese Shanghai | Jean Vasquez   |


## 基于csv文件的分析结果写入到csv文件
```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```
如，将上节的分析结果写入csv文件的语句是:
```sql
--对包含;的列进行拆分，然后转为行。注意：UNION ALL 前后的列顺序必须一致
COPY (
	SELECT
		phone,
		UNNEST(regexp_split_to_array(introduce,	'[;|]')) introduce,
		name
	FROM
		read_csv('testfile.csv',delim = ',',header = True,columns = {'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR' })
	WHERE
		regexp_matches(introduce,
	'[;|]')
	UNION ALL
	SELECT
		*
	FROM
		read_csv('testfile.csv',delim = ',',header = True,columns = {'phone':'BIGINT','introduce':'VARCHAR','name':'VARCHAR' })
	WHERE
		not regexp_matches(introduce,'[;|]')
)
  TO 'output.csv' (HEADER, DELIMITER ',');
```
## 将`csv`文件导入到`duckdb`数据库
以下语句将会自动新建数据表`ontime`并导入csv文件数据。
`CREATE TABLE ontime AS SELECT * FROM 'flights.csv';`
## 递归查询
  暂未掌握，附源文档链接
  https://duckdb.org/docs/sql/query_syntax/with


## 实现低内存占用的`CSV`文件按指定列去重
`CSV`文件中有`A,B,C,D,E,F`6列，E列为`日期时间`列。
### 只保留要去重的列
基于哪几列去重就只保留哪几列
```sql
COPY (SELECT DISTINCT A,B,C,D FROM '待去重CSV文件路径') TO 'output.csv' (HEADER, DELIMITER ',');
```
### 保留所有字段
基于`A,B,C,D`四列去重，同时保留`E,F`两个字段（值随意），因为`GROUP BY`的作用，会出现一组`A,B,C,D`的值对应多组E,F的值，所以使用`ANY_VALUE`函数来随机选取`E,F`列的值。
```sql
COPY (SELECT A,B,C,D,ANY_VALUE(E),ANY_VALUE(F) FROM '待去重CSV文件路径' GROUP BY A,B,C,D) TO 'output.csv' (HEADER, DELIMITER ',');
```
### 保留`最早`和`日晚``日期时间`
基于`A,B,C,D`四列去重，同时保留`E`中最早和最晚两个值，使用`MAX`、`MIN`函数分别获取最晚、最早`日期时间`:
```sql
COPY (SELECT A,B,C,D,MAX(E) 最晚日期时间,MIN(e) 最早日期时间 FROM '待去重CSV文件路径' GROUP BY A,B,C,D) TO 'output.csv' (HEADER, DELIMITER ',');
```

## 获取特定表的所有列名
```sql
SELECT column_name	FROM information_schema.columns	WHERE table_name = '表名';
```
**Output:**
|column_name|
|-----------|
|phone|
|uid|
|个人信息|
|备注|
### 结果保存为数组
```sql
SELECT ARRAY_AGG(column_name)	FROM information_schema.columns	WHERE table_name = '表名';
```
**Output:**
|array_agg(column_name)|
|----------------------|
|['phone','uid','个人信息','备注']|

### 保存为字典（结构体）
```sql
SELECT row(column_name,data_type) as name_type FROM information_schema.columns WHERE table_name = '表名';
```
**Output**
|name_type|
|---------|
|\{'column_name': phone, 'data_type': BIGINT\}|
|\{'column_name': uid, 'data_type': BIGINT\}|
|\{'column_name': 个人信息, 'data_type': VARCHAR\}|
|\{'column_name': 备注, 'data_type': VARCHAR\}|
### 其他与列相关`基础信息`的查询
```sql
SELECT * FROM information_schema.columns WHERE table_name = '表名';
```
**Output:**
|table_catalog|table_schema|table_name|column_name|ordinal_position|column_default|is_nullable|data_type|character_maximum_length|character_octet_length|numeric_precision|numeric_precision_radix|numeric_scale|datetime_precision|interval_type|interval_precision|character_set_catalog|character_set_schema|character_set_name|collation_catalog|collation_schema|collation_name|domain_catalog|domain_schema|domain_name|udt_catalog|udt_schema|udt_name|scope_catalog|scope_schema|scope_name|maximum_cardinality|dtd_identifier|is_self_referencing|is_identity|identity_generation|identity_start|identity_increment|identity_maximum|identity_minimum|identity_cycle|is_generated|generation_expression|is_updatable|
|-------------|------------|----------|-----------|----------------|--------------|-----------|---------|------------------------|----------------------|-----------------|-----------------------|-------------|------------------|-------------|------------------|---------------------|--------------------|------------------|-----------------|----------------|--------------|--------------|-------------|-----------|-----------|----------|--------|-------------|------------|----------|-------------------|--------------|-------------------|-----------|-------------------|--------------|------------------|----------------|----------------|--------------|------------|---------------------|------------|
|test|main|表名|phone|1||YES|BIGINT|||64|2|0||||||||||||||||||||||||||||||||
|test|main|表名|uid|2||YES|BIGINT|||64|2|0||||||||||||||||||||||||||||||||
|test|main|表名|个人信息|3||YES|VARCHAR|||||||||||||||||||||||||||||||||||||
|test|main|表名|备注|4||YES|VARCHAR|||||||||||||||||||||||||||||||||||||

### 获取`当前DuckDB文件`所有`数据库`名
其中`catalog`为可见的`schema`(通俗理解的`数据库`)名称
```sql
SELECT * FROM information_schema.schemata;
```
**Output:**
|catalog_name|schema_name|schema_owner|default_character_set_catalog|default_character_set_schema|default_character_set_name|sql_path|
|------------|-----------|------------|-----------------------------|----------------------------|--------------------------|--------|
|system|information_schema|duckdb|||||
|system|main|duckdb|||||
|system|pg_catalog|duckdb|||||
|temp|information_schema|duckdb|||||
|temp|main|duckdb|||||
|temp|pg_catalog|duckdb|||||
|test|information_schema|duckdb|||||
|test|main|duckdb|||||
|test|pg_catalog|duckdb|||||
### 获取`某数据库`下所有的数据表名
#### 第一种方式
```sql
SELECT table_name FROM information_schema.tables WHERE table_catalog = 'test';
```
**Output:**
|table_name|
|----------|
|table1|
|table2|
|test|
#### 第二种方式【推荐】
```sql
PRAGMA show_tables;
```
**Output:**
|table_name|
|----------|
|table1|
|table2|
|test|
## 限制使用内存大小和并发数

第一种【推荐】
```sql
-- 设置内存大小限制
SET memory_limit='10GB';
-- configure the system to use 1 thread 待测试作用
SET threads TO 1;

-- 查看所有可用设置，同时可在网页中查看所有可用设置：https://duckdb.org/docs/sql/configuration#configuration-reference
SELECT * FROM duckdb_settings();
-- 查看特定的设置值
SELECT current_setting('access_mode');
-- 将内存限制重置为默认，默认好像是程序自动的。
RESET memory_limit;
```
第二种
```sql
-- 设置内存大小限制
PRAGMA memory_limit='1GB';
-- 设置并行查询数
PRAGMA threads=4;
```
更多关于数据库基础设置信息详见：
1. https://duckdb.org/docs/sql/pragmas
2. https://duckdb.org/docs/sql/configuration
3. 见[DuckDB`设置`参数描述翻译](#DuckDB`设置`参数描述翻译)
## 关于`删除大表不会改变数据库文件的大小`疑问
从数据库中删除了一个数据量巨大的表。但是，数据库文件的大小保持不变，尝试使用` commit() `和` VACCUM` 语句也无济于事。
找到相关的话题：https://github.com/duckdb/duckdb/discussions/7152
结论：删除表不会改变存储空间，以在将来插入新数据时重新利用，这是个问题，将来会解决。

## DuckDB`设置`参数描述翻译
获取当前版本所有可用参数：`SELECT * FROM duckdb_settings();`
| 参数                           | 默认值              | 中文描述                                                     | 英文描述                                                                                                                                                    | 值类型     |
|------------------------------|------------------|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| access_mode                  | automatic        | 数据库的访问模式（AUTOMATIC，READ_ONLY或READ_WRITE）                 | Access mode of the database (AUTOMATIC, READ_ONLY or READ_WRITE)                                                                                        | VARCHAR |
| checkpoint_threshold         | 16.7MB           | 自动触发检查点的WAL大小阈值（例如1GB）                                   | The WAL size threshold at which to automatically trigger a checkpoint (e.g. 1GB)                                                                        | VARCHAR |
| debug_checkpoint_abort       | none             | DEBUG设置：出于测试目的，在检查点时触发中止                                 | DEBUG SETTING: trigger an abort while checkpointing for testing purposes                                                                                | VARCHAR |
| debug_force_external         | FALSE            | DEBUG设置：对支持它的操作符强制进行核外计算，用于测试                            | DEBUG SETTING: force out-of-core computation for operators that support it, used for testing                                                            | BOOLEAN |
| debug_force_no_cross_product | FALSE            | DEBUG设置：当超图未连接时，强制禁用交叉产品生成，用于测试                          | DEBUG SETTING: Force disable cross product generation when hyper graph isn't connected, used for testing                                                | BOOLEAN |
| debug_asof_iejoin            | FALSE            | DEBUG设置：强制使用IEJoin实现AsOf连接                               | DEBUG SETTING: force use of IEJoin to implement AsOf joins                                                                                              | BOOLEAN |
| debug_window_mode            | NULL             | DEBUG设置：切换要使用的窗口模式                                       | DEBUG SETTING: switch window mode to use                                                                                                                | VARCHAR |
| default_collation            |                  | 未指定时使用的排序设置                                              | The collation setting used when none is specified                                                                                                       | VARCHAR |
| default_order                | asc              | 未指定时使用的排序类型（ASC或DESC）                                    | The order type used when none is specified (ASC or DESC)                                                                                                | VARCHAR |
| default_null_order           | nulls_last       | 未指定时使用的空值排序（NULLS_FIRST或NULLS_LAST）                      | Null ordering used when none is specified (NULLS_FIRST or NULLS_LAST)                                                                                   | VARCHAR |
| disabled_optimizers          |                  | DEBUG设置：禁用特定的优化器集（逗号分隔）                                  | DEBUG SETTING: disable a specific set of optimizers (comma separated)                                                                                   | VARCHAR |
| enable_external_access       | TRUE             | 允许数据库访问外部状态（例如通过加载/安装模块，COPY TO/FROM，CSV读取器，pandas替换扫描等） | Allow the database to access external state (through e.g. loading/installing modules, COPY TO/FROM, CSV readers, pandas replacement scans, etc)         | BOOLEAN |
| enable_fsst_vectors          | FALSE            | 允许对FSST压缩段进行扫描以发出压缩向量以利用后期解压缩                            | Allow scans on FSST compressed segments to emit compressed vectors to utilize late decompression                                                        | BOOLEAN |
| allow_unsigned_extensions    | FALSE            | 允许加载具有无效或缺失签名的扩展                                         | Allow to load extensions with invalid or missing signatures                                                                                             | BOOLEAN |
| custom_extension_repository  |                  | 覆盖远程扩展安装的自定义端点                                           | Overrides the custom endpoint for remote extension installation                                                                                         | VARCHAR |
| enable_object_cache          | FALSE            | 是否使用对象缓存来缓存例如Parquet元数据                                  | Whether or not object cache is used to cache e.g. Parquet metadata                                                                                      | BOOLEAN |
| enable_http_metadata_cache   | FALSE            | 是否使用全局http元数据来缓存HTTP元数据                                  | Whether or not the global http metadata is used to cache HTTP metadata                                                                                  | BOOLEAN |
| enable_profiling             | NULL             | 启用分析，并设置输出格式（JSON，QUERY_TREE，QUERY_TREE_OPTIMIZER）       | Enables profiling, and sets the output format (JSON, QUERY_TREE, QUERY_TREE_OPTIMIZER)                                                                  | VARCHAR |
| enable_progress_bar          | FALSE            | 启用进度条，将长查询的进度打印到终端                                       | Enables the progress bar, printing progress to the terminal for long queries                                                                            | BOOLEAN |
| enable_progress_bar_print    | TRUE             | 在'enable_progress_bar'为true时，控制进度条的打印                    | Controls the printing of the progress bar, when 'enable_progress_bar' is true                                                                           | BOOLEAN |
| experimental_parallel_csv    | NULL             | 是否使用实验性的并行CSV阅读器                                         | Whether or not to use the experimental parallel CSV reader                                                                                              | BOOLEAN |
| explain_output               | physical_only    | EXPLAIN语句的输出（ALL，OPTIMIZED_ONLY，PHYSICAL_ONLY）           | Output of EXPLAIN statements (ALL, OPTIMIZED_ONLY, PHYSICAL_ONLY)                                                                                       | VARCHAR |
| extension_directory          |                  | 设置存储扩展的目录                                                | Set the directory to store extensions in                                                                                                                | VARCHAR |
| external_threads             | 0                | 处理DuckDB任务的外部线程数。                                        | The number of external threads that work on DuckDB tasks.                                                                                               | BIGINT  |
| file_search_path             |                  | 用于搜索输入文件的目录的逗号分隔列表                                       | A comma separated list of directories to search for input files                                                                                         | VARCHAR |
| force_compression            | Auto             | DEBUG设置：强制使用特定的压缩方法                                      | DEBUG SETTING: forces a specific compression method to be used                                                                                          | VARCHAR |
| force_bitpacking_mode        | auto             | DEBUG设置：强制使用特定的位打包模式                                     | DEBUG SETTING: forces a specific bitpacking mode                                                                                                        | VARCHAR |
| home_directory               |                  | 设置系统使用的主目录                                               | Sets the home directory used by the system                                                                                                              | VARCHAR |
| log_query_path               | NULL             | 指定应记录查询的路径（默认：空字符串，不记录查询）                                | Specifies the path to which queries should be logged (default: empty string, queries are not logged)                                                    | VARCHAR |
| immediate_transaction_mode   | FALSE            | 是否应在需要时懒惰地启动事务，或在调用BEGIN TRANSACTION时立即启动                | Whether transactions should be started lazily when needed, or immediately when BEGIN TRANSACTION is called                                              | BOOLEAN |
| integer_division             | 0                | /操作符是否默认为整数除法，还是浮点除法                                     | Whether or not the / operator defaults to integer division, or to floating point division                                                               | BOOLEAN |
| max_expression_depth         | 1000             | 解析器中的最大表达式深度限制。警告：增加此设置并使用非常深的表达式可能会导致栈溢出错误。             | The maximum expression depth limit in the parser. WARNING: increasing this setting and using very deep expressions might lead to stack overflow errors. | UBIGINT |
| max_memory                   | 13.4GB           | 系统的最大内存（例如1GB）                                           | The maximum memory of the system (e.g. 1GB)                                                                                                             | VARCHAR |
| memory_limit                 | 13.4GB           | 系统的最大内存（例如1GB）                                           | The maximum memory of the system (e.g. 1GB)                                                                                                             | VARCHAR |
| null_order                   | nulls_last       | 未指定时使用的空值排序（NULLS_FIRST或NULLS_LAST）                      | Null ordering used when none is specified (NULLS_FIRST or NULLS_LAST)                                                                                   | VARCHAR |
| ordered_aggregate_threshold  | 262144           | 排序前累积的行数，用于调优                                            | the number of rows to accumulate before sorting, used for tuning                                                                                        | UBIGINT |
| password                     | NULL             | 要使用的密码。出于遗留兼容性而忽略。                                       | The password to use. Ignored for legacy compatibility.                                                                                                  | VARCHAR |
| perfect_ht_threshold         | 12               | 使用完美哈希表的字节阈值（默认值：12）                                     | Threshold in bytes for when to use a perfect hash table (default: 12)                                                                                   | BIGINT  |
| pivot_limit                  | 100000           | 数据透视语句中的最大数据透视列数（默认值：100000）                             | The maximum numer of pivot columns in a pivot statement (default: 100000)                                                                               | BIGINT  |
| preserve_identifier_case     | TRUE             | 是否保留标识符大小写，而不是始终将所有非引用标识符小写                              | Whether or not to preserve the identifier case, instead of always lowercasing all non-quoted identifiers                                                | BOOLEAN |
| preserve_insertion_order     | TRUE             | 是否保留插入顺序。如果设置为false，则允许系统重新排序不包含ORDER BY子句的任何结果。         | Whether or not to preserve insertion order. If set to false the system is allowed to re-order any results that do not contain ORDER BY clauses.         | BOOLEAN |
| profiler_history_size        | NULL             | 设置分析器历史记录大小                                              | Sets the profiler history size                                                                                                                          | BIGINT  |
| profile_output               |                  | 应保存分析输出的文件，或为空以打印到终端                                     | The file to which profile output should be saved, or empty to print to the terminal                                                                     | VARCHAR |
| profiling_mode               | NULL             | 分析模式（STANDARD或DETAILED）                                  | The profiling mode (STANDARD or DETAILED)                                                                                                               | VARCHAR |
| profiling_output             |                  | 应保存分析输出的文件，或为空以打印到终端                                     | The file to which profile output should be saved, or empty to print to the terminal                                                                     | VARCHAR |
| progress_bar_time            | 2000             | 设置查询需要多长时间（以毫秒为单位）才开始打印进度条                               | Sets the time (in milliseconds) how long a query needs to take before we start printing a progress bar                                                  | BIGINT  |
| schema                       | main             | 设置默认搜索模式。相当于将search_path设置为单个值。                          | Sets the default search schema. Equivalent to setting search_path to a single value.                                                                    | VARCHAR |
| search_path                  |                  | 将默认搜索路径设置为逗号分隔的值列表                                       | Sets the default search search path as a comma-separated list of values                                                                                 | VARCHAR |
| temp_directory               | d:\fk.duckdb.tmp | 设置要写入临时文件的目录                                             | Set the directory to which to write temp files                                                                                                          | VARCHAR |
| threads                      | 16               | 系统使用的总线程数。                                               | The number of total threads used by the system.                                                                                                         | BIGINT  |
| username                     | NULL             | 要使用的用户名。出于遗留兼容性而忽略。                                      | The username to use. Ignored for legacy compatibility.                                                                                                  | VARCHAR |
| user                         | NULL             | 要使用的用户名。出于遗留兼容性而忽略。                                      | The username to use. Ignored for legacy compatibility.                                                                                                  | VARCHAR |
| wal_autocheckpoint           | 16.7MB           | 自动触发检查点的WAL大小阈值（例如1GB）                                   | The WAL size threshold at which to automatically trigger a checkpoint (e.g. 1GB)                                                                        | VARCHAR |
| worker_threads               | 16               | 系统使用的总线程数。                                               | The number of total threads used by the system.                                                                                                         | BIGINT  |
| binary_as_string             |                  | 在Parquet文件中，将二进制数据解释为字符串。                                | In Parquet files, interpret binary data as a string.                                                                                                    | BOOLEAN |
| TimeZone                     | Asia/Shanghai    | 当前时区                                                     | The current time zone                                                                                                                                   | VARCHAR |
| Calendar                     | gregorian        | 当前日历                                                     | The current calendar                                                                                                                                    | VARCHAR |

## 查看当前版本所有可用扩展
```sql
select * from duckdb_extensions();
```
**Output:**
|extension_name|loaded|installed|install_path|description|aliases|
|--------------|------|---------|------------|-----------|-------|
|autocomplete|false|false||Add supports for autocomplete in the shell|[]|
|fts|false|false||Adds support for Full-Text Search Indexes|[]|
|httpfs|false|false||Adds support for reading and writing files over a HTTP(S) connection|['http','https','s3']|
|icu|true|true|(BUILT-IN)|Adds support for time zones and collations using the ICU library|[]|
|inet|false|false||Adds support for IP-related data types and functions|[]|
|jemalloc|false|false||Overwrites system allocator with JEMalloc|[]|
|json|true|true|(BUILT-IN)|Adds support for JSON operations|[]|
|motherduck|false|false||Enables motherduck integration with the system|['md']|
|parquet|true|true|(BUILT-IN)|Adds support for reading and writing parquet files|[]|
|postgres_scanner|false|false||Adds support for reading from a Postgres database|['postgres']|
|spatial|true|true|C:\\spatial.duckdb_extension|Geospatial extension that adds support for working with spatial data and functions|[]|
|sqlite_scanner|false|true|C:\\sqlite_scanner.duckdb_extension|Adds support for reading SQLite database files|['sqlite','sqlite3']|
|tpcds|false|false||Adds TPC-DS data generation and query support|[]|
|tpch|false|false||Adds TPC-H data generation and query support|[]|
|visualizer|true||||[]|
### 扩展的安装与加载
```sql
INSTALL spatial;
LOAD spatial;
```

## 内存与临时文件
默认情况下，如果 DuckDB 在内存模式下运行，它不会尝试将数据缓存到磁盘，而当使用磁盘支持的数据库时，DuckDB 将尝试将数据缓存到目录mydb.db.tmp。您也可以手动指定要缓存的目录，也可以使用SET temp_directory='/tmp/mytmp.duck';
## 进行连接查询时，内存消耗殆尽
下文是问题描述
https://github.com/duckdb/duckdb/discussions/3820
下面的`ISSUE`说是已经解决这个问题，实现了支持超过内存大小的`连接查询`
https://github.com/duckdb/duckdb/pull/4189

## DuckDB VS ClickHouse VS DataBend
https://github.com/datafuselabs/databend/discussions/11357


## DuckDB快速排序
[这篇文章](https://duckdb.org/2021/08/27/external-sorting.html)中，介绍 `DuckDB` 如何排序，以及它与其他数据管理系统的比较。

因为人们通常在笔记本电脑或其他个人电脑上运行数据分析，因此此文在`2020 MacBook Pro`上运行这些实验。该笔记本电脑具有基于`ARM`的Apple M1 CPU。M1处理器具有8个核心：4个高性能核心和4个能效核心，`16GB`内存，固态硬盘。
我们将比较以下数据库系统的差异：
|数据库|版本|
|-|-|
|ClickHouse|21.7.5|
|HyPer|2021.2.1.12564|
|Pandas|1.3.2|
|SQLite|3.36.0|

**结论**
DuckDB 的新并行排序实现可以有效地对`超出内存容量`的数据进行排序，从而利用现代 SSD 的速度。在其他系统因内存不足或切换到速度慢得多的外部排序策略而崩溃的情况下，DuckDB 的性能会在超过内存限制时优雅地下降。
性能测试的源代码：https://github.com/lnkuiper/experiments/tree/master/sorting

## DuckDB计算树路径(关联分析)
### 数据样本（含下面一、二的数据）
`数据样本`使用`excel`的`randombetween`函数及`excel`办公助手插件生成的虚假测试数据，如与您的个人信息一致，纯乃天意。
[数据样本.csv](test.csv)
数据样本中号码`15834961213`两次在phone中出现，且都处于树形关系的路径中间。
### 数据样本（一）结构
|phone|id|pid|
|--|--|--|
|18693044740|37775|78340|
|14580719766|78340|47070|
|15834961213|47070|10960|
|13395855488|10960|67272|
|15657298376|67272|55701|
|15889121934|55701||
|18631569256|14280||
|13807639997|15582||
#### duckdb代码，花费6秒：
```python
import duckdb

def find_all_son_phones(phone): 
    path = [phone]
    def find_son_phones(phone):
        # phone对应的id
        conn.execute(f"select id from datas where phone='{phone}';")
        current_id = conn.fetchone()[0]
        # 父ID等于上面ID的Phone,即儿子的Phone
        conn.execute(f"select phone from datas where pid='{current_id}';")
        son_phone_array = conn.fetchone()
        if son_phone_array:  # 有儿子的情况
            son_phone = son_phone_array[0]
            path.append(son_phone)
            find_son_phones(son_phone)
    find_son_phones(phone)
    return path

def add_path(phone):
    """找出特定号码的子孙号码形成路径后保存到path列"""
    tree_list = find_all_son_phones(phone)
    tree_list = [str(i) for i in tree_list]
    if len(tree_list)>1:
        for i,e in enumerate(tree_list):
            conn.execute(f"update datas set path = '{'->'.join(tree_list)}',level={i} where phone ={e};")

def gen_phone_trees():
	# 全表生成数关系
    root_phones = conn.execute("select phone from datas where id NOTNULL AND pid ISNULL;").fetchall()
    root_phones = [j for i in root_phones for j in i]
    for phone in root_phones:
        add_path(phone)

conn = duckdb.connect('test.duckdb')
conn.execute("CREATE TABLE IF NOT EXISTS datas AS SELECT * FROM 'C:\\Users\\xxxxxx\\test.csv';")
conn.execute("ALTER TABLE datas ADD COLUMN IF NOT EXISTS path VARCHAR;")
conn.execute("ALTER TABLE datas ADD COLUMN IF NOT EXISTS level INT;")
# 创建索引，数据量大的时候测试是否有价值【待测试】。
conn.execute("CREATE INDEX p_id_pid_idx ON datas (phone, id,pid);")

gen_phone_trees()
conn.close()
```
上述代码只能对给定号码出现在一个数中的情况进行处理，并且只能查找下子孙元素，以下是改进后的代码，能够：
1. 从树的任意位置元素开始，还原整个树的路径；
2. 处理同一个号码出现在多个树中的情况。
缺陷：没有考虑一个PID对应多个同级ID的情况。
```py 花费15秒
import duckdb
import time

count= 0
def find_related_ids(current_id,phone): 
    path_ids = [current_id]
    id_phone_dict = {current_id:phone}

    def find_son_ids(current_id):
        # 父ID等于上面ID的Phone,即儿子的ID
        conn.execute(f"select id, phone from datas where pid='{current_id}';")
        son_ids = conn.fetchall()
        for son_id_tuple in son_ids:
            son_id, son_phone = son_id_tuple
            path_ids.append(son_id)
            id_phone_dict[son_id] = son_phone
            find_son_ids(son_id)
    
    def find_parent_ids(current_id):
        # id等于上面PID的Phone,即父亲的ID
        conn.execute(f"select pid, phone from datas where id='{current_id}';")
        parent_ids = conn.fetchall()
        for pid_tuple in parent_ids:
            parent_id, parent_phone = pid_tuple
            path_ids.insert(0, parent_id)  # 在列表前方插入父亲ID，保持父辈在前，子辈在后的顺序
            id_phone_dict[parent_id] = parent_phone
            find_parent_ids(parent_id)

    find_son_ids(current_id)
    # find_parent_ids(current_id)

    return path_ids, id_phone_dict

def add_path(init_phone):
    global count
    """找出特定号码的上下级路径并形成路径后保存到path列"""
    # phone对应的所有id
    conn.execute(f"select DISTINCT id from datas where phone='{init_phone}';")
    current_ids = [i[0] for i in conn.fetchall()]
    print('该号码共对应ID数：',len(current_ids))
    for current_id in current_ids:
        tree_id_list, id_phone_dict = find_related_ids(current_id,init_phone)
        # tree_id_list = list(filter(None,tree_id_list))
        tree_id_list = list(set(tree_id_list))
        # 更新path和level
        if len(tree_id_list)>1:
            count+=len(tree_id_list)
            print(len(tree_id_list),'\ntree_id_list:\t',tree_id_list)
            print('  id_phone_dict:\t',id_phone_dict)
            path_of_phone = '->'.join([str(id_phone_dict[id]) for id in tree_id_list])
            print('    path_of_phone:\t',path_of_phone,end='\n\n')
            for i, id in enumerate(tree_id_list):
                phone = id_phone_dict[id]
                conn.execute(f"update datas set path = '{path_of_phone}',level={i} where phone='{phone}' and id='{id}';")


with duckdb.connect('test.duckdb') as conn:
    ceshi = ['']
    ceshi_str = ','.join([f"'{item}'" for item in ceshi])
    # 有记录的
    conn.execute(f'SELECT DISTINCT phone FROM datas WHERE phone IN ({ceshi_str});')
    phones = [phone[0] for phone in conn.fetchall()]
    for phone in phones:
        print('当前查找号码：',phone,end=',')
        start = time.time()
        add_path(phone)
        print('耗时：',time.time()-start)
    # add_path("97891706516")
print(count)
```
#### Pandas代码，花费22+秒:
```python
import pandas as pd

df = pd.read_csv(r"test.csv", encoding='utf-8', dtype='str',usecols=["name","phone","id","pid"])

def find_all_son_phones(df, phone): 
    path = [phone]
    def find_son_phones(df, phone):
        # phone对应的id
        current_id = df[df['phone'] == phone]['id'].values[0]
        # 父ID等于上面ID的Phone,即儿子的Phone
        son_phone_array = df[df['pid'] == current_id]['phone'].values
        if son_phone_array.any():  # 有儿子的情况
            son_phone = son_phone_array[0]
            path.append(son_phone)
            find_son_phones(df,son_phone)
    find_son_phones(df, phone)
    return path


def add_path(df,phone):
    """找出特定号码的子孙号码形成路径后保存到path列"""
    if 'path' not in df:
        df['path'] = None
    if 'level' not in df:
        df['level']= None
    tree_list = find_all_son_phones(df, phone)
    if len(tree_list)>1:
        for i,e in enumerate(tree_list):
            df.loc[df['phone']==e,'path'] =  '->'.join(tree_list)
            df.loc[df['phone']==e,'level'] = str(i)

# 为所有父ID为空而ID不为空的号码生成子孙路径关系
def gen_phone_trees(df): 
    root_phones = df[(df['id']!='')&(df['pid'].isnull())]['phone'].values
    for phone in root_phones:
        add_path(df,phone)
gen_phone_trees(df)
```
### 数据样本（二）结构
|phone|pphone|
|-|-|
|18693044740|14580719766|
|14580719766|15834961213|
|15834961213|13395855488|
|13395855488|15657298376|
|15657298376|15889121934|
|15889121934||
|18815083183|13918139598|
|13918139598|15762062144|
|15762062144|18109707945|
|18109707945|13254675670|
|13254675670||
#### Pandas代码，花费7.5秒
```python
import pandas as pd

df = pd.read_csv(r"test.csv", encoding='utf-8', dtype='str',usecols=["name","phone","pphone"])

def find_all_son_phones(df, phone): 
    path = [phone]
    def find_son_phones(df, phone):
        # phone对应的id
        # 父ID等于上面ID的Phone,即儿子的Phone
        son_phone_array = df[df['pphone'] == phone]['phone'].values
        if son_phone_array.any():  # 有儿子的情况
            son_phone = son_phone_array[0]
            path.append(son_phone)
            find_son_phones(df,son_phone)
    find_son_phones(df, phone)
    return path


def add_path(df,phone):
    """找出特定号码的子孙号码形成路径后保存到path列"""
    if 'path' not in df:
        df['path'] = None
    if 'level' not in df:
        df['level']= None
    tree_list = find_all_son_phones(df, phone)
    if len(tree_list)>1:
        for i,e in enumerate(tree_list):
            df.loc[df['phone']==e,'path'] =  '->'.join(tree_list)
            df.loc[df['phone']==e,'level'] = str(i)


# 为所有父ID为空而ID不为空的号码生成子孙路径关系
def gen_phone_trees(df): 
    root_phones = df[(df['phone']!='')&(df['pphone'].isnull())]['phone'].values
    for phone in root_phones:
        add_path(df,phone)
gen_phone_trees(df)

# 找出特定号码的子孙树关系
# add_path(df,'15834961213')

df[~df['path'].isnull()]
```

#### DuckDB代码，花费3.3秒
```python
import duckdb
# import functools

conn = duckdb.connect('zfrz.duckdb')
conn.execute("CREATE TABLE IF NOT EXISTS datas AS SELECT * FROM 'C:\\Users\\xxx\\编程\\test.csv';")
conn.execute("ALTER TABLE datas ADD COLUMN IF NOT EXISTS path VARCHAR;")
conn.execute("ALTER TABLE datas ADD COLUMN IF NOT EXISTS level INT;")
# conn.execute("CREATE INDEX p_id_pid_idx ON datas (phone, id,pid);")

def find_all_son_phones(phone): 
    path = [phone]
    def find_son_phones(phone):
        conn.execute(f"select phone from datas where pphone='{phone}';")
        # 父ID等于上面ID的Phone,即儿子的Phone
        son_phone_array = conn.fetchone()
        if son_phone_array:  # 有儿子的情况
            son_phone = son_phone_array[0]
            path.append(son_phone)
            find_son_phones(son_phone)
    find_son_phones(phone)
    return path


def add_path(phone):
    """找出特定号码的子孙号码形成路径后保存到path列"""
    tree_list = find_all_son_phones(phone)
    tree_list = [str(i) for i in tree_list]
    if len(tree_list)>1:
        for i,e in enumerate(tree_list):
            conn.execute(f"update datas set path = '{'->'.join(tree_list)}',level={i} where phone ={e};")


def gen_phone_trees():
    root_phones = conn.execute("select phone from datas where pphone ISNULL;").fetchall()
    root_phones = [j for i in root_phones for j in i]
    for phone in root_phones:
        add_path(phone)

# add_path(15834961213)
gen_phone_trees()

conn.close()
```

## 树形关系新思路
### 第一步
postgres数据库的datas表中有phone,id,pid,path,level,rootid等6个字段，path,level,rootid三个字段本来均为NULL，根据id和pid的关联关系，计算出每个id对应的子节点，并以数组形式将id保存到path列，同时将此节点的根节点id保存到rootid，将节点在树形结构中的层级保存到level（根节点为0，依此类推）。
| phone       | id    | pid   | path | level | rootid |
|-------------|-------|-------|------|-------|--------|
| 15889121934 | 55701 |       |
| 15657298376 | 67272 | 55701 |
| 13395855488 | 10960 | 67272 |
| 15834961213 | 47070 | 10960 |
| 14580719766 | 78340 | 47070 |
| 18693044740 | 37775 | 78340 |
| 18693044741 | 37775 | 78340 |
| 18631569256 | 14280 |       |
| 13807639997 | 15582 |       |
| 13254675670 | 75663 |       |
| 18109707945 | 12959 | 75663 |
| 15834961213 | 22099 | 12959 |
| 13918139598 | 22099 | 12959 |
| 18815083183 | 83540 | 22099 |
| 13875678880 | 58053 |       |
| 15793943526 | 72534 |       |
| 18739688136 | 75579 |       |
| 13028479619 | 51390 |       |
| 13339189047 | 90300 | 51390 |
| 15834961213 | 46686 | 90300 |
| 18073413108 | 53266 | 46686 |
| 15154627416 | 50707 | 53266 |
| 13722872673 | 84764 |

```sql
WITH RECURSIVE datas_cte AS (
  SELECT id, pid,   ARRAY[id] as path,   0 as level,  id as rootid  FROM datas  WHERE pid IS NULL
  UNION ALL
  SELECT d.id,   d.pid,  
  c.path || d.id,  
  c.level + 1,  c.rootid  FROM datas d
  JOIN datas_cte c ON d.pid = c.id
)
UPDATE datas
SET path = datas_cte.path, 
    level = datas_cte.level, 
    rootid = datas_cte.rootid
FROM datas_cte
WHERE datas.id = datas_cte.id;
```
| phone       | id    | pid   | path                                  | level | rootid |
|-------------|-------|-------|---------------------------------------|-------|--------|
| 15889121934 | 55701 |       | [55701]                               | 0     | 55701  |
| 15657298376 | 67272 | 55701 | [55701,67272]                         | 1     | 55701  |
| 13395855488 | 10960 | 67272 | [55701,67272,10960]                   | 2     | 55701  |
| 15834961213 | 47070 | 10960 | [55701,67272,10960,47070]             | 3     | 55701  |
| 14580719766 | 78340 | 47070 | [55701,67272,10960,47070,78340]       | 4     | 55701  |
| 18693044740 | 37775 | 78340 | [55701,67272,10960,47070,78340,37775] | 5     | 55701  |
| 18693044741 | 37775 | 78340 | [55701,67272,10960,47070,78340,37775] | 5     | 55701  |
| 18631569256 | 14280 |       |                                       |       |        |
| 13807639997 | 15582 |       |                                       |       |        |
| 13254675670 | 75663 |       | [75663]                               | 0     | 75663  |
| 18109707945 | 12959 | 75663 | [75663,12959]                         | 1     | 75663  |
| 15834961213 | 22099 | 12959 | [75663,12959,22099]                   | 2     | 75663  |
| 13918139598 | 22099 | 12959 | [75663,12959,22099]                   | 2     | 75663  |
| 18815083183 | 83540 | 22099 | [75663,12959,22099,83540]             | 3     | 75663  |
| 13875678880 | 58053 |       |                                       |       |        |
| 15793943526 | 72534 |       |                                       |       |        |
| 18739688136 | 75579 |       |                                       |       |        |
| 13028479619 | 51390 |       | [51390]                               | 0     | 51390  |
| 13339189047 | 90300 | 51390 | [51390,90300]                         | 1     | 51390  |
| 15834961213 | 46686 | 90300 | [51390,90300,46686]                   | 2     | 51390  |
| 18073413108 | 53266 | 46686 | [51390,90300,46686,53266]             | 3     | 51390  |
| 15154627416 | 50707 | 53266 | [51390,90300,46686,53266,50707]       | 4     | 51390  |
| 13722872673 | 84764 |

### 第二步
将相同rootid的level值最大的path列数组中的id转化为对应的phone,一个id对应多个phone的，使用`#`连接多个phone，此时path仍然为数组，
然后将path的数组元素用->连接，此时path为字符串类型。
```sql
-- 创建一个临时表，将每个id对应的所有电话号码用#连接起来
CREATE TEMP TABLE temp_id_phone AS
SELECT id, STRING_AGG(phone, '#') as phone
FROM datas
GROUP BY id;

-- 找出每个 rootid 组里面 level 最大的记录
WITH max_level AS (
  SELECT rootid, MAX(level) as level
  FROM datas
  GROUP BY rootid
),
max_level_datas AS (
  SELECT d.*
  FROM datas d
  JOIN max_level m ON d.rootid = m.rootid AND d.level = m.level
),
-- 更新这些记录的 path，将 id 替换为对应的电话号码
updated_path AS (
  SELECT mld.id, mld.pid,
         ARRAY_TO_STRING(ARRAY(
           SELECT t.phone::TEXT
           FROM unnest(mld.path::INTEGER[]) p(id)
           JOIN temp_id_phone t ON p.id = t.id
         ), '->') as path
  FROM max_level_datas mld
)
UPDATE datas d
SET path = up.path
FROM updated_path up
WHERE d.id = up.id AND d.pid = up.pid;

-- 删除临时表
DROP TABLE temp_id_phone;
```
### 第三步
将相同rootid的path列值设置为相同rootid且level值最大的path列的值。
要更新一个表中的一列的值，基于同一表中的其他行的值，你需要使用一个自连接。
```sql
UPDATE datas AS d1
SET path = d2.path
FROM (
    SELECT rootid, path
    FROM datas
    WHERE level = (
        SELECT MAX(level)
        FROM datas AS d3
        WHERE d3.rootid = datas.rootid
    )
) AS d2
WHERE d1.rootid = d2.rootid;
```
先创建一个子查询 d2，该查询对于每一个 rootid 找到对应 level 最大的 path。
然后，我们将原表 datas 更新为子查询 d2 中找到的 path。
这个查询假设 rootid 和 level 的组合是唯一的，也就是说，在同一 rootid 中，不可能有两行具有相同的最大 level 值。如果这不是你的情况，你可能需要对查询进行进一步的调整以处理这种情况。
### 以上三步的完整代码
```sql
--CREATE TABLE datas AS SELECT * FROM 'C:\Users\xxx\Desktop\tree.csv';
--ALTER table datas ADD COLUMN path varchar DEFAULT null;
--ALTER table datas ADD COLUMN rootid varchar DEFAULT null;
--ALTER table datas ADD COLUMN level int DEFAULT null;
---------------------------------------------------------------------------
-- 创建一个递归查询来获取每一行的根节点、路径和级别
WITH RECURSIVE datas_cte AS (
  SELECT id, 
         pid, 
         ARRAY[id] as path, 
         0 as level,
         id as rootid
  FROM datas
  WHERE pid IS NULL
  UNION ALL
  SELECT d.id, 
         d.pid, 
         c.path || ARRAY[d.id], 
         c.level + 1,
         c.rootid
  FROM datas d
  JOIN datas_cte c ON d.pid = c.id
)
UPDATE datas
SET path = datas_cte.path, 
    level = datas_cte.level, 
    rootid = datas_cte.rootid
FROM datas_cte
WHERE datas.id = datas_cte.id;
---------------------------------------------------------------------------

UPDATE datas SET path=null,level=null,rootid=null;

---------------------------------------------------------------------------
-- 找出rootid个数大于1的所有记录，即树形节点大于1的记录
SELECT d.*
FROM datas d
WHERE d.rootid IN (
  SELECT rootid
  FROM datas
  GROUP BY rootid
  HAVING COUNT(*) > 1
);

---------------------------------------------------------------------------
-- 创建一个中间表，将每个id对应的所有电话号码用#连接起来
CREATE TEMP TABLE temp_id_phone AS
SELECT id, STRING_AGG(phone, '#') as phone
FROM datas
GROUP BY id;

-- 更新路径，将id替换为对应的电话号码
WITH RECURSIVE datas_cte AS (
  SELECT d.id, 
         d.pid, 
         ARRAY[t.phone::TEXT] as path, 
         0 as level,
         d.id as rootid
  FROM datas d
  JOIN temp_id_phone t ON d.id = t.id
  WHERE pid IS NULL
  UNION ALL
  SELECT d.id, 
         d.pid, 
         c.path || ARRAY[t.phone::TEXT], 
         c.level + 1,
         c.rootid
  FROM datas d
  JOIN datas_cte c ON d.pid = c.id
  JOIN temp_id_phone t ON d.id = t.id
)
UPDATE datas
SET path = ARRAY_TO_STRING(datas_cte.path, '->'), 
    level = datas_cte.level, 
    rootid = datas_cte.rootid
FROM datas_cte
WHERE datas.id = datas_cte.id;

-- 删除临时表
DROP TABLE temp_id_phone;
---------------------------------------------------------------------------


---------------------------------------------------------------------------
-- 将level值最大的path列数组中的id替换成phone
-- 创建一个临时表，将每个id对应的所有电话号码用#连接起来
CREATE TEMP TABLE temp_id_phone AS
SELECT id, STRING_AGG(phone, '#') as phone
FROM datas
GROUP BY id;

-- 找出每个 rootid 组里面 level 最大的记录
WITH max_level AS (
  SELECT rootid, MAX(level) as level
  FROM datas
  GROUP BY rootid
),
max_level_datas AS (
  SELECT d.*
  FROM datas d
  JOIN max_level m ON d.rootid = m.rootid AND d.level = m.level
),
-- 更新这些记录的 path，将 id 替换为对应的电话号码
updated_path AS (
  SELECT mld.id, mld.pid,
         ARRAY_TO_STRING(ARRAY(
           SELECT t.phone::TEXT
           FROM unnest(mld.path::INTEGER[]) p(id)
           JOIN temp_id_phone t ON p.id = t.id
         ), '->') as path
  FROM max_level_datas mld
)
UPDATE datas d
SET path = up.path
FROM updated_path up
WHERE d.id = up.id AND d.pid = up.pid;

-- 删除临时表
DROP TABLE temp_id_phone;
---------------------------------------------------------------------------


---------------------------------------------------------------------------
--将rootid相同的所有行的path设置为：rootid相同的对应level列值最大的对应的path的值。
UPDATE datas AS d1
SET path = d2.path
FROM (
    SELECT rootid, path
    FROM datas
    WHERE level = (
        SELECT MAX(level)
        FROM datas AS d3
        WHERE d3.rootid = datas.rootid
    )
) AS d2
WHERE d1.rootid = d2.rootid;
---------------------------------------------------------------------------
```
