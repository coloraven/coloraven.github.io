# Python计算大文件行数方法及性能比较

如何使用Python快速高效地统计出大文件的总行数, 下面是一些实现方法和性能的比较。
## 实现方法

### `readlines`方法读所有行

```python
def readline_count(file_name):
    return len(open(file_name).readlines())
```
### 依次读取每行
```python
def simple_count(file_name):
    lines = 0
    for _ in open(file_name):
        lines += 1
    return lines
```
### 使用`sum`函数计数
```python
def sum_count(file_name):
    return sum(1 for _ in open(file_name))
```

### `enumerate`枚举计数
```python
def enumerate_count(file_name):
    with open(file_name) as f:
        for count, _ in enumerate(f, 1):
            pass
    return count
```

### `buff`+`count`每次读取固定大小,然后统计行数
```python
def buff_count(file_name):
    with open(file_name, 'rb') as f:
        count = 0
        buf_size = 1024 * 1024
        buf = f.read(buf_size)
        while buf:
            count += buf.count(b'\n')
            buf = f.read(buf_size)
        return count
```

### `wc`+`count`调用使用`wc`命令计算行
```python
def wc_count(file_name):
    import subprocess
    out = subprocess.getoutput("wc -l %s" % file_name)
    return int(out.split()[0])
```

### `partial`+`count`
在`buff_count`基础上引入`partial`
```python
def partial_count(file_name):
    from functools import partial
    buffer = 1024 * 1024
    with open(file_name) as f:
        return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))
```

### iter count
在buff_count基础上引入itertools模块
```python
def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)
```

## 效率比较
下面是在4-Core 8GB Python3.6的环境下,分别测试100M、500M、1G、10G大小文件运行的时间，单位:秒：
方法    | 100M | 500M | 1G   | 10G  
--------------- | ---- | ---- | ---- | -----
1.readline_count  | 0.25 | 1.82 | 3.27 | 45.04
2.simple_count    | 0.13 | 0.85 | 1.58 | 13.53
3.sum_count       | 0.15 | 0.77 | 1.59 | 14.07
4.enumerate_count | 0.15 | 0.80 | 1.60 | 13.37
5.buff_count      | 0.13 | 0.62 | 1.18 | 10.21
6.wc_count        | 0.09 | 0.53 | 0.99 | 9.47 
7.partial_count   | 0.12 | 0.55 | 1.11 | 8.92 
8.iter_count      | 0.08 | 0.42 | 0.83 | 8.33 

## 来源
https://www.cnblogs.com/jhao/p/13488867.html
