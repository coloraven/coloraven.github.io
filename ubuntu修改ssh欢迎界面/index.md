# Ubuntu修改SSH欢迎界面

`Ubuntu` 与别的 `Linux` 不同，直接修改`/etc/motd`文件重登录后无效。因为这里 `/etc/motd` 是一个符号链接，指向 `/var/run/motd`，应该是一个启动后在生成的文件。在版本 10.04 中，找到生成的脚本在目录  `/etc/update-motd.d/`  中，那几个有序号的文件就是，包括 `00-header`，`20-cpu-checker` ，`90-updates-available`， `98-reboot-required`，`10-help-text`，`50-landscape-sysinfo`，`91-release- upgrade`，`99-footer`。修改这几个文件，可以得到自己想要的结果。我使用的是 `Ubuntu 12.04 Server LTS`，目录下有这几个文件：

> 00-header
> 10-help-text
> 50-landscape-sysinfo
> 90-updates-available
> 91-release-upgrade
> 98-fsck-at-reboot
> 98-reboot-required
> 99-footer

基于我的需求，我修改到了以下几个文件：
> 00-header
> 50-landscape-sysinfo
> 90-updates-available

例如显示系统相关信息：
```bash
System load: 0.0 Processes: 75
Usage of /: 2.7% of 73.47GB Users logged in: 2
Memory usage: 48% IP address for eth0: 61.166.76.27
Swap usage: 0%
```
此信息就是文件 “50-landscape-sysinfo” 里面的如下语句控制的：`/usr/bin/landscape-sysinfo`在前面用 “#” 号将其注释，保存即可。修改后用`sudo run-parts /etc/update-motd.d`去执行就会立即见到效果，而不用反复注销登录。
