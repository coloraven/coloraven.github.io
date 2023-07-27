# CentOS挂载NTFS分区


CentOS挂载NTFS分区：https://my.oschina.net/u/4364192/blog/3326016

## 先安装ntfsprogs

截止到2021年4月27日，最新版仍是2017.3.23。

```bash
# 下载此软件
wget http://tuxera.com/opensource/ntfs-3g_ntfsprogs-2017.3.23.tgz

# 解压 
tar -zxvf ntfs-3g_ntfsprogs-2017.3.23.tgz

# 进入解压后的目录
cd ntfs-3g_ntfsprogs-2017.3.23/

# 建立一个目录ntfs3g用以安装当前软件
mkdir /usr/local/ntfs3g/

# 指定编译路径
./configure --prefix=/usr/local/ntfs3g/

# 开始编译和安装
make&&make install
```

## 挂载NTFS分区

挂载命令格式（较非NTFS分区的挂载，其中加入了ntfs-3g参数）

```bash
mount -t ntfs-3g /dev/sdb1 /mnt/udisk
```

## 实现开机自动挂载

要想实现自动开机挂载NTFS格式的USB硬盘，需要进行以下操作：

```bash
# 首先备份fstab表
cp /etc/fstab /etc/fstabbakup

# 然后打开vi编辑器
vi /etc/fstab

# 在fstab表最后一行添加如下信息 
/dev/sdb1   /mnt/udisk    ntfs-3g defaults     0 0
```
