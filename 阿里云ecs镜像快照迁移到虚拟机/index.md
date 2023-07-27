# 阿里云ECS镜像快照迁移到虚拟机




- https://mefj.com.cn/lur2853.html



### 找到ECS实例创建快照
{% asset_img image-1.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-1.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->
{% asset_img image-2.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-2.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->

### 等待镜像创建100%
{% asset_img image-3.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-3.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->
{% asset_img image-4.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-4.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->

### 导出到阿里云OSS存储。阿里云镜像不可以直接下载到本地，只能通过OSS下载到本地
{% asset_img image-5.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-5.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->
{% asset_img image-6.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-6.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->
{% asset_img image-7.png %}

<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-7.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->

{% asset_img image-8.png %}

<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-8.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> --> -->

### 下载到本地，OSS流量比较贵，建议没有特殊情况不要随意使用，我这里镜像下载了10个多GB，费用在五六块钱
{% asset_img image-9.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-9.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:60%;" /> -->

### 本地找到下载镜像文件格式为**.raw.tar.gz**的文件，解压到本地
{% asset_img image-10.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-10.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:80%;" /> -->

### 使用[qemu](https://mefj.com.cn/wp-content/themes/begin-lts-1/inc/go.php?url=https://share.mefj.com.cn/装机文件/系统镜像/qemu-img-win-x64-2_3_0.zip)工具将raw格式转换成VMware可以使用的vmdk格式
{% asset_img image-11.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-11.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:80%;" /> -->
{% asset_img image-12.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-12.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:80%;" /> -->

注：raw为最原始的虚拟机镜像文件，vmdk是vmware的虚拟机镜像文件，如果要查看raw文件中的内容可以先把raw文件转换为vmdk文件，然后再用vmware虚拟机打开vmdk文件。

### 创建虚拟机，选择现有磁盘（这步很重要）
{% asset_img image-13.png %}
<!-- <img src="/阿里云ECS镜像快照迁移到虚拟机/image-13.png" alt="阿里云ECS镜像快照迁移到虚拟机" style="zoom:80%;" /> -->

### 启动创建的虚拟机即可
