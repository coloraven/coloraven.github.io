# 搭建Android 7.0+下的HTTPS抓包环境

转载自：https://blog.csdn.net/djzhao627/article/details/108658332
## 准备
### 一台已`root`的手机
### 安装`Openssl`
下载地址：https://slproweb.com/products/Win32OpenSSL.html
安装完毕后将`openssl.exe`所在目录放入环境变量中，否则下面的`openssl`指令前需要加绝对路径。
## 证书生成
1. 将`Filddler`或者其他抓包程序的证书导出，一般为`xxx.cer`或者`xxx.pem`
2. 使用`openssl`的`x509`指令进行`cer`证书转`pem`证书 和 用`md5`方式显示`pem`证书的`hash`值
3. 证书转换，已经是pem格式的证书不需要执行这一步
```bash
openssl x509 -inform DER -in xxx.cer -out cacert.pem
```

## 获取证书`MD5`的`hash`显示
1. 查看`openssl`版本的指令`openssl version`
    #openssl版本在`1.0`以上的版本的执行这一句
    `openssl x509 -inform PEM -subject_hash_old -in cacert.pem`

    #`openssl`版本在`1.0`以下的版本的执行这一句
    `openssl x509 -inform PEM -subject_hash -in cacert.pem`

2. 将第二条指令输出的类似`347bacb5`的值进行复制

## 将`pem`证书重命名
使用上面复制的值（类似于`347bacb5`）对`pem`证书进行重命名
```bash
mv cacert.pem 347bacb5.0
```

## 将新证书放入手机系统证书目录并设置权限
手机系统目录位置是：
`/system/etc/security/cacerts`

需要拷贝至此目录必须拥有`root`权限
修改证书的权限为`644`，可查看同目录下其他证书权限，照抄设置

## 重启`Android`设备以生效
拷贝证书至`/system/etc/security/cacerts`之后，重启手机就可以使证书生效了
