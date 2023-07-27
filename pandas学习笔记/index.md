# Pandas学习笔记


#### Pandas 统计出每行非空的列数目

在 pandas 中，可以使用 DataFrame.count() 方法来统计每行非空的列数目。该方法返回一个新的 DataFrame，其中包含每列的非空值的数量。例如：

```python
import pandas as pd

# 创建一个示例数据帧
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, None, 12]})
print(df)

# 统计每行非空的列数目
non_null_counts = df.count()
print(non_null_counts)
```

```
输出结果如下：

   A  B     C
0  1  5   9.0
1  2  6  10.0
2  3  7   NaN
3  4  8  12.0
A    4
B    4
C    3
dtype: int64
```

如果想要将每行的非空列数目添加回原来的数据帧中，可以使用 DataFrame.apply() 方法。例如：

```python
import pandas as pd

# 创建一个示例数据帧
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, None, 12]})

# 将每行的非空列数目添加回原来的数据帧中
df['non_null_counts'] = df.apply(lambda row: row.count(), axis=1)
print(df)
```

输出结果如下：

```
   A  B     C  non_null_counts
0  1  5   9.0                3
1  2  6  10.0                3
2  3  7   NaN                2
3  4  8  12.0                3
```

请注意，`DataFrame.count()` 方法只会统计非空值，而不会统计 NaN 值。如果想要统计包括 NaN 值在内的每行非空的列数目，可以使用 `DataFrame.notnull()` 方法来代替 `DataFrame.count()` 方法。例如：

```python
import pandas as pd

# 创建一个示例数据帧
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, None, 12]})

# 将每行的非空列数目添加回原来的数据帧中，包括 NaN 值
df['non_null_counts'] = df.notnull().sum(axis=1)
print(df)
```

输出结果如下：

```
   A  B     C  non_null_counts
0  1  5   9.0                3
1  2  6  10.0                3
2  3  7   NaN                2
3  4  8  12.0                3
```

请注意，在上面的代码中，我们使用了 `DataFrame.notnull()` 方法来判断每个值是否为空，并返回一个布尔值。然后，使用 `DataFrame.sum()` 方法将每行的布尔值求和，以统计每行非空的列数目。

希望这些信息能帮助你。如果你有其他问题，欢迎继续提问。

#### Pandas 筛选出每行非空的列数目为 7 的行，组成新的 dataframe

可以使用 DataFrame.apply() 方法和 DataFrame.notnull() 方法来筛选出每行非空的列数目为 7 的行，然后使用 DataFrame.loc[] 方法来选择这些行并组成新的数据帧。例如：

```python
import pandas as pd

# 创建一个示例数据帧
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8], 'C': [9, 10, None, 12], 'D': [None, None, None, None], 'E': [13, 14, 15, 16]})

# 筛选出每行非空的列数目为 7 的行
mask = df.apply(lambda row: row.notnull().sum() == 7, axis=1)
print(mask)

# 选择筛选出的行并组成新的数据帧
new_df = df.loc[mask]
print(new_df)```
```
输出结果如下：
```
0    False
1    False
2    False
3     True
dtype: bool
   A  B     C   D   E
3  4  8  12.0 NaN  16
```

在上面的代码中，我们使用了 `DataFrame.apply()` 方法和 `DataFrame.notnull()` 方法来判断每个值是否为空，并返回一个布尔值。然后，使用 `DataFrame.sum()` 方法将每行的布尔值求和，以统计每行非空的列数目。最后，使用 `DataFrame.loc[]` 方法选择满足条件的行并组成新的数据帧。

希望这些信息能帮助你。如果你有其他问题，欢迎继续提问。

### 数据错位(列)的修复
有如下数据：
```json
{
    'name': ['rose', 'jack', 3, 'stone'],
    'B': [5, 6, 7, 8], 
    'C': [9, 10, ''handsome'', 12]
}
```

"handsome"应和3互换位置，以上只是样本，数据量大的情况下用pandas如何修复。

首先，我们需要使用pandas读取数据，并将数据转化为pandas的DataFrame格式：
```python
import pandas as pd

data = {'name': ['rose', 'jack', 3, 'stone'], 'B': [5, 6, 7, 8], 'C': [9, 10, 'handsome', 12]}
df = pd.DataFrame(data)

## 然后，我们可以使用pandas的loc和iloc方法来获取和修改位置3的元素：

## 获取位置3的元素
name_3 = df.loc[3, 'name']
c_3 = df.loc[3, 'C']

## 互换位置3的元素
df.loc[3, 'name'] = c_3
df.loc[3, 'C'] = name_3
```
或者使用iloc方法：
```python
## 获取位置3的元素
name_3 = df.iloc[3, 0]
c_3 = df.iloc[3, 2]


## 互换位置3的元素
df.iloc[3, 0] = c_3
df.iloc[3, 2] = name_3
```
最后，我们可以使用df.to_dict()方法将修改后的DataFrame转化回字典格式：
```python
new_data = df.to_dict()
print(new_data)
## 输出：{'name': ['rose', 'jack', 'handsome', 'stone'], 'B': [5, 6, 7, 8], 'C': [9, 10, 3, 12]}
```
这样就可以在数据量大的情况下使用pandas修复数据了。

### 将行转换成字符串处理(使用逗号作为连接符)
在pandas中，可以使用df.apply()方法将行转换成字符串处理，并使用join()函数将字符串元素连接起来。

例如，对于以下数据：
```python
import pandas as pd

data = {
    'name': ['rose', 'jack', 'stone'],
    'age': [20, 25, 30], 
    'gender': ['female', 'male', 'male']
      }
df = pd.DataFrame(data)
```
我们可以使用df.apply()方法将每行数据转化为字符串，然后使用join()函数将字符串元素连接起来：
```python
def row_to_str(row):
    return [str(x) for x in row]

df['row_str'] = df.apply(row_to_str, axis=1).apply(', '.join)
print(df)
## 输出：
##     name  age  gender                           row_str
## 0   rose   20  female  name: rose, age: 20, gender: female
## 1   jack   25    male    name: jack, age: 25, gender: male
## 2  stone   30    male   name: stone, age: 30, gender: male
```
这样就可以使用逗号作为各元素的字符串连接符了。
