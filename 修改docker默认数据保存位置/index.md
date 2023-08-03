# 修改Docker默认数据保存位置


## 第一步
停止wsl
```cmd
wsl --shutdown
```
## 第二步
移动默认位置（`C:\Users\xxxxx\AppData\Local\Docker\wsl\data`）下的`ext4.vhdx`到新位置，这里我们移动到`D:\Docker\data`目录下。

## 第三步
`regedit`打开注册表，定位到`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Lxss`
将其下的`DistributionName`为`docker-desktop-data`所在项对应的`BasePath`修改为新位置目录`\\?\D:\Docker\data`

## 完成
重新打开`Docker Desktop`

## 限制 `wsl2` 内存使用
这个解决方案来自 [github](https://github.com/microsoft/WSL/issues/4166)，简单来说就是创建一个 `%UserProfile%\.wslconfig` 文件来限制 wsl 使用的内存总量。比如说我在 Windows 中使用的用户是 tinychen，那么我就在 `C:\Users\tinychen` 中创建了一个`.wslconfig` 文件，在里面加入以下内容来限制 wsl2 的内存总大小：

```ini
[wsl2]
memory=1GB
swap=8GB
swapFile=%USERPROFILE%\AppData\Local\Temp\swap.vhdx
localhostForwarding=true
```
复制以下内容粘贴到cmd中一键解决，然后重新启动`Docker Desktop`
```cmd
wsl --shutdown
echo [wsl2] > %UserProfile%\.wslconfig
echo memory=1GB >> %UserProfile%\.wslconfig
echo swap=8GB >> %UserProfile%\.wslconfig
echo swapFile=^%USERPROFILE^%\AppData\Local\Temp\swap.vhdx >> %UserProfile%\.wslconfig
echo localhostForwarding=true >> %UserProfile%\.wslconfig
```

注意修改完成之后需要重启 wsl2 才能生效。更多详细的配置可以查看[官方文档](https://docs.microsoft.com/en-us/windows/wsl/wsl-config%23configure-global-options-with-wslconfig)。

## 其他
通过此方式，重装系统后，可以复用重装系统之前使用的`Docker`产生的`镜像`及`容器`，即`Docker`数据持久化，同样，可用于`Docker`镜像、容器的移植。

