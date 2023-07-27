# Python实现对大文件的增量读取

## 背景

前段时间在做一个算法测试，需要对源于日志的数据进行分析才能获取到结果；日志文件较大，所以想要获取数据的变化曲线，增量读取是最好的方式。


网上有很多人的技术博客都是写的用`for`循环`readline`以及一个计数器去增量读取，假如文件很大，遍历一次太久。而且对于很多大文件的增量读取，如果遍历每一行比对历史记录的输出或者全都加载到内存通过历史记录的索引查找，是非常浪费资源的，

获取文件句柄的基本理论中就包含指针操作。`linux`的文件描述符的`struct`里有一个`f_pos`的这么个属性，里面存着文件当前读取位置，通过这个东东经过`vfs`的一系列映射就会得到硬盘存储的位置了，所以很直接，很快。

在`Python`中的读取文件的方法也有类似的属性。


## 具体实现

`Python`中相关方法的核心函数如下：

函数     | 作用         
------ | -----------
tell() | 返回文件当前位置   
seek() | 从指定位置开始读取信息

其中seek()有三种模式：

> * f.seek(p,0) 移动当文件第p个字节处，绝对位置

> * f.seek(p,1) 移动到相对于当前位置之后的p个字节

> * f.seek(p,2) 移动到相对文章尾之后的p个字节

参考代码：

```python
#!/usr/bin/python
fd=open("test.txt",'r') #获得一个句柄
for i in xrange(1,3): #读取三行数据
    fd.readline()
label=fd.tell() #记录读取到的位置
fd.close() #关闭文件
#再次阅读文件
fd=open("test.txt",'r') #获得一个句柄
fd.seek(label,0)# 把文件读取指针移动到之前记录的位置
fd.readline() #接着上次的位置继续向下读取
```



## 拓展


### 如何得知这个大文件行数，以及变化


我的想法：  
**方式1：** 遍历`\n`字符。  
**方式2：** 开始时就在`for`循环中对`fd.readline()`计数，变化的部分（用上文说的`seek`、`tell`函数做）再用`for`循环`fd.readline()`进行统计。

### 如何避免文件读取时，内存溢出

* 可以通过 `read` 函数的`chunk`关键字来指定每次读区数据的大小
* 使用生成器确保只有在数据被调用时才会生成  

具体方法封装如下：

```python
def read_in_chunks(file_path,  chunk=100 * 100):  # 通过chunk指定每次读取文件的大小防止内存占用过大
    file_object = open(file_path, "r")
    while True:
        data = file_object.read(chunk)
        if not data:
            file_object.close()
            break
        # 使用generator（生成器）使数据只有在被使用时才会迭代时占用内存
        yield data
```

## 应用

根据博客园一个朋友的实际问题写的一段应用代码，解决程序运行异常、断点再读问题：

```python
#! /usr/bin/python
# coding:utf-8 
""" 
@author:Bingo.he 
@file: 20191129-file.py 
@time: 2019/11/29 
"""
import os
import glob

class opened(object):
    def __init__(self, filename):
        self.filename = filename
        self.handle = open(filename)
        if filename in get_read_info().keys():
            self.handle.seek(get_read_info()[filename], 0)

    def __enter__(self):
        return self.handle

    def __exit__(self, exc_type, exc_value, exc_trackback):
        seek_num = self.handle.tell()
        set_read_info(self.filename, seek_num)
        self.handle.close()
        if exc_trackback is None:
            print(f"文件【{self.filename}】读取正常退出。")
        else:
            print(f"文件【{self.filename}】读取退出异常！")

def get_read_info():
    """
    读取已读取的文件的句柄位置
    :return:
    """
    file_info = {}

    # 如果文件不存在则创建一个空文件
    if not os.path.exists("temp"):
        with open("temp", 'w', encoding="utf-8") as f:
            pass
        return file_info

    with open("temp", 'r', encoding="utf-8") as f:
        datas = f.readlines()
        for data in datas:
            name, line = data.split("===")
            file_info[name] = int(line)
    return file_info

def set_read_info(filename, seek_num):
    """
    设置为已经读取的文件的句柄位置
    :param filename: 文件名称
    :param seek_num: 句柄位置
    :return:
    """
    flag = True
    with open("temp", 'r', encoding="utf-8") as f:
        datas = f.readlines()
        for num, data in enumerate(datas):
            if filename in data:
                flag = False
                datas[num] = f"{filename}==={seek_num}\n"
        if flag:
            datas.append(f"{filename}==={seek_num}\n")
    # print(datas)
    with open("temp", 'w', encoding="utf-8") as f:
        f.writelines(datas)

# 测试代码
# 注：文件读完之后，存储在temp文件中的，第二次读取时不会再读，可以以删除temp文件或者修改其中信息
pys = glob.glob("*.py")  # 获取当前目录以Py结尾的文件

for py in pys:
    with opened(py) as fp:  # 默认为读模式
        for line_data in fp:
            print(line_data)
```

## 来源
https://www.cnblogs.com/Detector/p/8975335.html
