# (WSA)安卓子系统折腾笔记

## 设置代理
```cmd
<!-- 使用 adb shell 设置 -->

<!-- 打开windows terminal -->

adb connect WSA的IP和端口

<!-- 设置代理 -->
adb shell settings put global http_proxy ip:端口
<!-- 关闭代理(无需重启) -->
adb shell settings put global http_proxy :0
```
