# Python并发/并行执行循环任务


来源:https://blog.csdn.net/qq_23869697/article/details/84798614

```python
from multiprocessing.dummy import Pool as ThreadPool
def process(item):
    log = _get_logger(item)
    log.info("item: %s" % item)
    time.sleep(5)
 
items = ['apple', 'bananan', 'cake', 'dumpling']
pool = ThreadPool()
results = pool.map(process, items)
pool.close()
pool.join()
```
