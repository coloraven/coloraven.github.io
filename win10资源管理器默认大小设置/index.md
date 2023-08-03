# Win10资源管理器默认大小设置

解决方案来源：https://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1785990

> 终于解决了，方法在这里：http://www.oystd.com/blog/2010/10/15/32.html
> 打开注册表编辑器，定位到 HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell

> 将Bags删除，注销，或者下载Default-Windows-Size.zip。


二、将IE8的窗口恢复到默认大小的方法。

将IE8的窗口恢复到默认大小最简单的方法：新建文本文档，复制下面内容，以reg格式保存，双击导入注册表，重启IE8。其实就是将Window_Placement这个键删除，重启IE后自动重新生成并赋以默认值。
```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main]

"Window_Placement"=-
```
