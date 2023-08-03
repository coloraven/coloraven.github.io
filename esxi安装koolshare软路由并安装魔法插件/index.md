# ESXI安装KoolShare软路由并安装魔法插件


固件下载地址：
https://firmware.koolshare.cn/LEDE_X64_fw867/
转盘~
安装完毕后。
SSH连接输入以下命令，不然无法安装魔法插件：

```
sed -i 's/\tdetect_package/\t# detect_package/g' /koolshare/scripts/ks_tar_install.sh
```

魔法插件下载地址
https://github.com/hq450/fancyss_history_package/tree/master/fancyss_X64


