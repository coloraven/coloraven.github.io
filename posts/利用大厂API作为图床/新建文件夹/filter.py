import time,requests,random
# from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool


session = requests.Session()

count = 0
def get_imgsize(url):
    global count
    count +=1
    print('第',count,'次调用')
    try:
        imgsize = session.head(url).headers["Content-Length"] # 用head请求，仅探测图片大小，不会下载图片
        if  int(imgsize) <= 5242880: # 图片小于5M的就进行上传
            return url
    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    with open("wallhaven.txt", "r", encoding="utf-8") as f:
        result = f.readlines()
    result = [i.strip() for i in result]
    small=[]
    pool = ThreadPool(10)
    results = pool.map(get_imgsize, result)
    pool.close()
    pool.join()
    small = [i for i in results if i is not None]
    # print(small)
    # for url in tqdm(result):
    #     time.sleep(random.uniform(0,0.5))
    #     imgsize = get_imgsize(url)
    #     if  imgsize <= 5242880: # 图片小于5M的就进行上传
    #         small.append(url)
    with open("wallhaven_smallerthan5mb.txt", "w", encoding="utf-8") as f:
         f.writelines('\n'.join(small))
