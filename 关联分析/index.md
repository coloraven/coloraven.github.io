# 关联分析

## 树形关系分析
根据`id`,`pid`还原树形关系的完整树，找出每个树的每个节点的`rootid`，以便导入`neo4j`数据库。
```python
import duckdb
from joblib import Parallel, delayed

def find_related_ids(current_id,phone,cursor): 
    path_ids = [current_id]
    id_phone_dict = {current_id:phone}

    def find_son_ids(current_id):
        # 父 ID 等于上面 ID 的 phone, 即儿子的 ID
        cursor.execute(f"select id, phone from ref{phone} where pid='{current_id}';")
        son_ids = cursor.fetchall()
        for son_id_tuple in son_ids:
            son_id, son_phone = son_id_tuple
            if son_id:
                path_ids.append(son_id)
                id_phone_dict[son_id] = son_phone
                find_son_ids(son_id)

    def find_parent_ids(current_id):
        # id 等于上面 PID 的 phone, 即父亲的 ID
        cursor.execute(f"select pid, phone from ref{phone} where id='{current_id}';")
        parent_ids = cursor.fetchall()
        for pid_tuple in parent_ids:
            parent_id, parent_phone = pid_tuple
            if parent_id:
                path_ids.insert(0, parent_id)  # 在列表前方插入父亲 ID，保持父辈在前，子辈在后的顺序
                id_phone_dict[parent_id] = parent_phone
                find_parent_ids(parent_id)

    find_son_ids(current_id)
    find_parent_ids(current_id)

    return path_ids, id_phone_dict

def add_path(init_phone):
    cursor = conn.cursor()
    """找出特定phone的上下级路径并形成路径后保存到path列"""
    # 找出phone对应的credit，然后再根据credit找出同样credit的所有行，并将结果保存到新建的临时表中，递归查询关系时只在当前credit中查找，大量减少时间。
    cursor.sql(
        f"CREATE OR REPLACE TEMP TABLE ref{init_phone} AS SELECT * FROM datas WHERE credit IN (SELECT credit FROM datas WHERE phone='{init_phone}');"
        )
    # phone 对应的所有 id
    cursor.execute(f"select DISTINCT id from ref{init_phone} where phone='{init_phone}';")
    current_ids = [i[0] for i in cursor.fetchall()]
    # print('该phone共对应ID数：',len(current_ids))
    for current_id in current_ids:
        tree_id_list, id_phone_dict = find_related_ids(current_id,init_phone,cursor)
        # tree_id_list = list(filter(None,tree_id_list))
        tree_id_list = list(set(tree_id_list))
        # 更新 path 和 level
        if len(tree_id_list)>1:
            # path_of_phone = '->'.join([str(id_phone_dict[id]) for id in tree_id_list])
            # print('    path_of_phone:\t',path_of_phone,end='\n\n')
            # print('treeidlist:',tree_id_list)
            for i, id in enumerate(tree_id_list):
                phone = id_phone_dict[id]
                # print(id_phone_dict)
                # conn.execute(f"update datas set path = '{path_of_phone}',level={i} where phone='{phone}' and id='{id}';")
                try:
                    cursor.sql(f"update datas set rootid = '{current_id}' where phone='{phone}' and id='{id}';")
                except:
                    pass


with duckdb.connect(r'abcd.db') as conn:
    conn.execute("SELECT DISTINCT phone FROM datas WHERE pid ISNULL;") # AND phone IN('18801973844','13524003126','18635087722','18608143124','18981102776','13429916439','18535904920');")
    phones = [phone[0] for phone in conn.fetchall()]
    Parallel(n_jobs=100, backend='threading')(delayed(add_path)(phone) for phone in phones)
    # for phone in tqdm(phones):
    #     print('当前查找phone：',phone,end=',')
    #     start = time.time()
    #     add_path(phone)
    #     print('耗时：',time.time()-start)
```
## 数据加密
将生产数据加密成测试数据，数据结构和数据关系不变
```python
import duckdb
from faker import Faker
import pandas as pd

fake = Faker('zh_CN')

def gendata(column_name:str,table_name:str,fake_type):
    conn.execute(f"SELECT {column_name} FROM {table_name};")
    origin_lists = {i[0] for i in conn.fetchall()} # 返回结果去重
    encrypt_data = {} # 储存“旧---新”的映射
    fakedata_list = []
    for origin_ele in origin_lists:
        if origin_ele not in encrypt_data:
            while 1:
                fakedata = fake_type()
                if fakedata not in fakedata_list:
                    break
            encrypt_data[origin_ele]=fakedata
    # 将字典转化为df
    df = pd.DataFrame(list(encrypt_data.items()),columns=['old','new'])
    #df 写入临时表
    conn.sql("DROP TABLE IF EXISTS mapping;CREATE TEMP TABLE mapping AS SELECT * FROM df;")
    # 根据映射写入表中
    conn.sql(f"UPDATE {table_name} SET {column_name}=mapping.new FROM mapping WHERE {table_name}.{column_name}=mapping.old")


# 操作时间,操作人,操作IP,MAC地址,部门,模块,操作类型,受理编号,名称,对象,phone,id,pid,"path","level"
with duckdb.connect('abcd.duckdb') as conn:
    gendata('phone','datas',fake.phone_number)
    gendata('名称','datas',fake.company)
    # ......
    # id和pid加密
    conn.sql("update datas set id=md5(md5(md5(id))) ,pid = md5(md5(md5(pid)));")
```

## 新的树形关系分析
```python
# 先在duckdb中进行数据清洗
# --第一次清洗
# -- 其他字段相同的情况下，保留pid非空的记录
# CREATE TABLE datas_clean AS SELECT * FROM datas
# DELETE FROM datas_clean 
# WHERE pid IS NULL AND phone IN (
#     SELECT phone
#     FROM datas
#     WHERE pid IS NOT NULL
# ) AND id IN (
#     SELECT id
#     FROM datas
#     WHERE pid IS NOT NULL
# );

# --第二次清洗
# --基于id和pid相同合并phone列，保存到datas_clean_clean表中
# CREATE TABLE datas_clean_clean AS
# SELECT
#  MAX(credit) AS credit,
#  MAX(company) AS company,
#  MAX(name) AS name,
#  array_agg(phone) AS phones,
#  id,
#  pid,
#  MAX(rootid) AS rootid
# FROM
#  datas_clean
# GROUP BY
#  id,
#  pid;

import duckdb
import pandas as pd

df = pd.DataFrame(columns=['id', 'rootid', 'phones'])
def find_related_ids(current_id,phone): 
    id_phone_dict = {current_id:[phone]}

    def find_son_ids(current_id):
        nonlocal id_phone_dict  # 修改函数外部变量
        # 父 ID 等于上面 ID 的 phone, 即儿子的 ID
        conn.execute(f"select id, phones from temp_table{phone} where pid='{current_id}';")
        son_ids = conn.fetchall()
        for son_id_tuple in son_ids:
            son_id, son_phone = son_id_tuple
            if son_id:
                id_phone_dict[son_id] = son_phone
                find_son_ids(son_id)

    def find_parent_ids(current_id):
        nonlocal id_phone_dict  # 修改函数外部变量
        # id 等于上面 PID 的 phone, 即父亲的 ID
        conn.execute(f"select pid, phones from temp_table{phone} where id='{current_id}';")
        parent_ids = conn.fetchall()
        for pid_tuple in parent_ids:
            parent_id, parent_phone = pid_tuple
            if parent_id:
                # path_ids.insert(0, parent_id)  # 在字典前方插入父亲 ID，保持父辈在前，子辈在后的顺序
                temp_id_phone_dict = {parent_id:parent_phone}
                temp_id_phone_dict.update(id_phone_dict)
                id_phone_dict= temp_id_phone_dict
                # id_phone_dict[parent_id] = parent_phone
                find_parent_ids(parent_id)

    find_son_ids(current_id)
    # find_parent_ids(current_id)

    return id_phone_dict

def add_path(init_phone:str):
    global df
    # start = time.time()
    """找出特定phone的上下级路径并形成路径后保存到path列"""
    # 找出phone对应的credit，然后再根据credit找出同样credit的所有行，并将结果保存到新建的临时表中，递归查询关系时只在当前credit中查找，大量减少时间。
    sqlstr = f"CREATE OR REPLACE TABLE temp_table{init_phone} AS SELECT * FROM datas_clean_clean WHERE credit IN (SELECT credit FROM datas_clean_clean WHERE list_contains(phones,'{init_phone}'));"
    conn.sql(
        sqlstr
        )
    # phone 对应的所有 id
    conn.execute(f"select DISTINCT id from datas_clean_clean where list_contains(phones,'{init_phone}')")
    current_ids = [i[0] for i in conn.fetchall()]
    print('# 该phone共对应ID：',end='')
    print(current_ids)
    # 以这些id为基础，进行id所在树的还原
    current_ids_path = []
    for current_id in current_ids:
        temp_path = find_related_ids(current_id,init_phone)
        # current_ids_path = current_ids_path.append(temp_path)
        # if current_id in 
        id_phone_dict = temp_path
        if len(id_phone_dict)>1:
            print(id_phone_dict)
            # 将字典转换为dataframe
            tmp_df = pd.DataFrame(list(id_phone_dict.items()), columns=['id', 'phone'])
            # 添加rootid列
            tmp_df['rootid'] = list(id_phone_dict.keys())[0]
            # print('\n','->'.join(list(id_phone_dict.keys())),'\n')
            # df = df.append(tmp_df, ignore_index=True)
            df = pd.concat([tmp_df, df],ignore_index=True)



with duckdb.connect(r'E:\数据分析\zfrz.db') as conn:
    phones = ['3116','9688','4892']
    for phone in phones:
        add_path(phone)
    print(df)
    #df 写入临时表
    conn.sql("DROP TABLE IF EXISTS mapping;CREATE TEMP TABLE mapping AS SELECT * FROM df;")
    # # 根据映射写入表中
    conn.sql(f"UPDATE datas_clean_clean SET rootid=mapping.rootid FROM mapping WHERE datas_clean_clean.id =mapping.id")
    conn.execute("SELECT  credit, company, name ,phones, id, pid, rootid  FROM datas_clean_clean  WHERE rootid NOT NULL GROUP BY credit, company, name ,phones, id, pid, rootid;")
    otherdf = conn.fetch_df()

otherdf.to_csv('tree.csv',index=False)

# neo4j导入节点

# LOAD CSV WITH HEADERS FROM 'file:///tree.csv' AS row
# CREATE (n:ZFRZ {
#   credit: row.credit,
#   company: row.company,
#   name: row.name,
#   phones: row.phones,
#   id: row.id,
#   pid: row.pid,
#   rootid: row.rootid
# })


# neo4j 创建关系

# LOAD CSV WITH HEADERS FROM 'file:///tree.csv' AS row

# // Find the parent node (B) using the pid value
# MATCH (parent:ZFRZ {id: row.pid})

# // Find the child node (A) using the id value
# MATCH (child:ZFRZ {id: row.id})

# // Create the relationship from parent to child
# CREATE (parent)-[:SON]->(child)
```
