# 将CentOS、RHEL 7/8引导到紧急模式（Emergency mode）/恢复模式（Recovery mode）


作为Linux管理员，您可能需要对某些实例进行故障排除和修复引导问题，这通常是通过从Grub菜单将系统引导到紧急模式（Emergency mode）/恢复模式（Recovery mode）来实现的。在本文中，您将学习诊断问题并从紧急模式恢复系统。

 

**将CentOS、RHEL 7/8引导到紧急模式（Emergency mode）/恢复模式（Recovery mode）**

启动您的CentOS 7/8、RHEL 7/8 Linux机器，当出现引导加载程序菜单时，请按Enter键以外的任何键以中断倒计时：

![将CentOS 7/8、RHEL 7/8引导到紧急模式/恢复模式的方法](https://ywnz.com/uploads/allimg/20/1-20021R11Q55D.JPG)

按e键编辑当前条目，以便我们可以修改默认的引导加载程序条目并登录到紧急模式：

![将CentOS 7/8、RHEL 7/8引导到紧急模式/恢复模式的方法](https://ywnz.com/uploads/allimg/20/1-20021R11R61R.JPG)

现在，使用光标键导航到以linux开头的行，您需要将systemd.unit=emergency.target添加到行尾，如上图方框所示。

按Ctrl+x键以使用修改后的配置启动。

输入root密码登录到紧急模式（Emergency mode）：

![将CentOS 7/8、RHEL 7/8引导到紧急模式/恢复模式的方法](https://ywnz.com/uploads/allimg/20/1-20021R11Sa94.JPG)

使用mount命令重新安装对/文件系统的读/写操作，这将使您能够编辑文件系统：

\# mount -o remount,rw /

参考：[mount命令_Linux mount命令使用详解：用于加载文件系统到指定的加载点](https://ywnz.com/linux/mount/)。

这时，您应该能够从紧急模式中拯救出故障的系统。
