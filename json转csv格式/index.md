# JSON转CSV格式


https://pypi.org/project/python-json2csv/

## Project description

Convert json array data to csv.

_Note:_ zencore-json2csv rename to python-json2csv

## 安装

```bash
pip install python-json2csv
```

## 用法

```bash
E:\>json2csv --help
Usage: json2csv [OPTIONS]

Options:
-f, --file FILENAME     Input file name, use - for stdin.
--file-encoding TEXT    Input file encoding.
-o, --output FILENAME   Output file name, use - for stdout.
--output-encoding TEXT  Output file encoding.
-k, --keys TEXT         Output field names. Comma separated string list.
-p, --path TEXT         Path of the data.
--help                  Show this message and exit.
```

## 案例

### 案例 1

**输入数据:**

```json
[
    [1,2,3],
    [2,3,4]
]
```
**命令:**

```bash
cat input.txt | json2csv -o output.txt
```

**结果:**

```bash
1,2,3
2,3,4
```



### 案例 2

**输入数据:**

```json
[
    {"f1": 11, "f2": 12, "f3": 13},
    {"f1": 21, "f3": 23, "f2": 22}
]
```

**命令:**

```bash
cat input.txt | json2csv -o output.txt -k f1,f2,f3
```
**结果:**

```bash
11,12,13
21,22,23
```


### 案例 3（嵌套）

**输入:**

```json
{
    "data": {
        "list": [
            [1,2,3],
            [2,3,4],
        ]
    }
}
```

**命令:**

```bash
cat input.txt | json2csv -o output.txt -p data.list
```

**结果:**

```bash
1,2,3
2,3,4
```
