import io,json,requests,time

count = 0 # `sm.ms`限制一小时只能上传100`张，此变量用来计算，
ys = {}            # 用来存放wallhaven地址与图床外链地址的映射关系字典
huishou = []   # 用爱存放大于5M图片的链接
def upload(imgurl):
    global ys,huishou,count #声明全局变量


    imgsize = requests.head(imgurl).headers["Content-Length"] # 用head请求，仅探测图片大小，不会下载图片
    if int(imgsize) <= 5242880: # 图片小于5M的就进行上传
        imgbyte = requests.get(imgurl).content
        base64string = base64.b64encode(io.BytesIO(imgbyte)) # 使用io.BytesIO方法，将下载的图片数据紧接着转手上传出去，全部在内存中完成，不占用磁盘空间。


        res=res.json()
        if res['code']=="success":
            count+=1
            print('wallhaven地址',imgurl,'图片外链地址：',res["data"]["url"])
            ys[imgurl] = res["data"]["url"]
            if count%100==0:
                time.sleep(3600)
        elif res['code']=='image_repeated':
            print('该链接图片已上传',imgurl)
        else:
            print(res['message'])
    else:
        print("该链接图片大于5M", imgurl)
        huishou.append(imgurl)


if __name__ == "__main__":
    with open("wallhaven.txt", "r", encoding="utf-8") as f:
        result = f.readlines()
    result = [i.strip() for i in result]
    for url in result:
        upload(url)
    with open('映射关系.json','w') as f:
        json.dump(ys)
    with open('5m+.json','w') as f:
        json.dump(huishou)