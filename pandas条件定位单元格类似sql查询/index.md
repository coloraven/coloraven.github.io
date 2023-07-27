# Pandas条件定位单元格【类似select 字段 from 表 where 其他字段=某值】

## 背景
实践当中，经常需要在`Excel`表中根据某一列的值去查看另一列对应的值。
比如，根据下表（假设存放在`datas.xlsx`）中姓名，查找其对应电话号码。
这里顺便记录一下这个网站可以方便的在`excel`、`json`、`csv`、`yaml`、`markdown`、`xml`、`html表格`之间互转：https://tableconvert.com/excel-to-markdown


| 序号 | 姓名  |  电话号码   | 年龄 | 性别 |
|:-:|:-:|:-:|:-:|:-:|
| 1  | 张三  | 4563453 | 39 | 男  |
| 2  | 李四  | 3453453 | 25 | 男  |
| 3  | 王五  | 2323423 | 18 | 女  |
| 4  |  李六 | 2342342 | 18 | 男  |

## 实操
```python
import pandas as pd
df = pd.read_excel('datas.xlsx',header=0,encoding='gbk') 
# header默认为0，即从第1行开始读取数据。 gbk为了支持中文
```
### 第一步
读取后`Pandas`默认会根据行数从`0`开始设置行索引，而不是将第一列作为行索引。
将`姓名`列设为行索引
```python
df = df.set_index('姓名')
```
### 第二步
使用函数进行定位
`at`和`loc`两个函数均可，听说`loc`更快
```python
df.at['李六','电话号码']
```
## 列数据转换
列数据转换，比如，将`电话号码`列数据转换为字符串类型
```
df[' 电话号码'] = df[' 电话号码'].apply(str)
```

