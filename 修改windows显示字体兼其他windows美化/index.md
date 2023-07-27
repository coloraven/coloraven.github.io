# 修改Windows显示字体

最终显示效果如图：
![桌面截图](2022-12-30T103541.png){height="400px"}


## 背景
最近将笔记本装上了`Phoenix`团队精简的系统`X-Lite`，其默认显示语言为英文，可以下载安装中文语言包，但是貌似有以下几个问题：
1. 会出现方块（乱码）
2. 微软拼音无法启动（通过临时启动`ctfmon.exe`或将其设为开机启动解决）
3. ~~中文字相较原版win11镜像难看（细小不齐等）~~
4. 命令行中文字乱码（[解决方法](https://blog.csdn.net/a11101171/article/details/43576469)）

## 添加中文语言包
### 走过的弯路
1. 使用该精简内置的优化工具`Winaero Tweaker`修改为`HarmonyOS_Sans_Medium.ttf`字体，结果发现只能修改只对英文生效。
2. 通过修改注册表，参见：https://blog.csdn.net/amoscn/article/details/106224359


### 正确姿势

~~详细情况参见：https://www.revi.cc/revios/workspace/lang#h.ry7gga391br1~~：

1. 先打开系统更新
2. 在设置里面添加中文语言包
2. 注销之后中文显示正常
3. 使用`dism /Online /Get-Packages`获取已安装语言包，找到包名类似`Microsoft-Windows-Client-LanguagePack-Package~31bf3856ad364e35~amd64~en-US~10.0.19041.1`（取决于你的系统），
4. 使用`dism /Online /Remove-Package /PackageName:XXX`删除英文语言包，在系统设置界面中删除英文语言....
5. 解决锁屏界面仍然是英文的现象，（参考此文进行设置：https://jingyan.baidu.com/article/fcb5aff7c6dc90adaa4a71b5.html）
    以下为备份：
在资源管理器中输入`控制面板\时钟和区域\日期和时间`-->`更改日期和时间(D)`-->`更改日历设置`，切换到`管理`选项卡-->`复制设置`-->勾选最底下`欢迎屏幕和系统账户`。
![2023-01-02T084052](2023-01-02T084052.png)


### 字体美化正确姿势
使用`noMeiryoUI`([下载地址](https://github.com/Tatsu-syo/noMeiryoUI/releases))进行修改，字体使用`HarmonyOS_Sans_SC_Medium.ttf`。你就能如愿以偿了。以下是我的配置截图：
![配置截图](2022-12-30T104044.png){height="300px"}
2023/1/1日更新，从上图可以看到，`noMeiryoUI`([下载地址](https://github.com/Tatsu-syo/noMeiryoUI/releases))并不支持`窗口标题`字体的修改，这时我们可以用`Winaero Tweaker`来进行，可以说两者互为补充。


## Everything的黑色主题美化与配置备份
效果如下图
![Everything美化效果](2023-01-01T094834.png)
1. 定位到`Everything`目录；
2. 退出`Everything`；
3. 将下面内容替换到`Everything.exe`所在目录的`Everything.ini`中；
4. 重启`Everything`。（如果你再打开`Everything.ini`，会发现已经将你提供的配置信息`吸收`了）
```ini Everything.ini   mark:28-29
[Everything]
; 交错行
alternate_row_color=1
show_mouseover=1
; 无关键词时空结果
hide_empty_search_results=1
; 切换窗口快捷键
toggle_window_key=602
; 在状态栏显示大小
show_size_in_statusbar=1
single_click_tray=1
double_click_path=1
auto_scroll_view=1
; 复制时自动加双引号
double_quote_copy_as_path=1
focus_search_on_activate=1
; 大小格式——自动
size_format=0
; 索引文件夹大小
index_folder_size=1
; 显示筛选器
filters_visible=1
filter=EVERYTHING
; 结果排序规则——文件（夹）大小
sort=Size
; 结果排序规则——正向
sort_ascending=0
; 字体，需要先安装对应字体才会生效
result_list_font=HarmonyOS Sans SC Medium
; 配色
normal_background_color=#21252b
normal_foreground_color=#aaaaaa
highlighted_foreground_color=#008080
current_sort_background_color=#1c2026
current_sort_highlighted_background_color=#21252b
mouseover_background_color=#2b2a33
mouseover_highlighted_background_color=#ff0080
```

网页制作的多种配色方案：https://www.voidtools.com/forum/viewtopic.php?t=7240

## 去除不想要的右键菜单
使用火绒自带的右键菜单管理工具即可


## WPS相关

### 去除WPS云文档入口
注册表，找到如下位置删除文件。（不是右边的数值）
1. 资源管理左导航栏：（中间数字可能有区别，看好开头结尾即可）
```textile
HKEY_USERS\S-1-5-21-1514480548-2261916930-102402149-1001\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{7AE6DE87-C956-4B40-9C89-3D166C9841D3}
```
2. 资源管理我的电脑：
```textile
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace
```


## 隐藏资源管理器左侧不想要的文件夹
1. 弯路：`dism++`默认提供7个文件夹的隐藏，但是下载和桌面我经常用到，这就需要自己动手定制了。
    https://github.com/Chuyu-Team/Dism-Multi-language/issues/527

    https://jingyan.baidu.com/article/75ab0bcbb47b09d6864db2cc.html
2. 直接右键该文件夹，选择`从"快速访问"取消固定`即可，如图。
![2022-12-30T113240](2022-12-30T113240.png){height="300px"}

### 另参考文章
Windows 10 资源管理器隐藏网络、3D对象、视频、图片、文档等多余文件夹：
`https://blog.csdn.net/m0_46463321/article/details/125387284`

### windows美化相关网站、视频
https://cleodesktop.gumroad.com/
https://cleodesktop.com/obetal-tequila-theme-for-windows-11/
https://zhutix.com/tag/win11-zhuti/
https://www.youtube.com/watch?v=To1AXc9ESwU及https://github.com/niivu/Windows-11-themes
Windows 字体美化经验：
    https://www.xianyukang.com/windows-font-optimization.html
    https://www.bilibili.com/video/BV1pP4y187bR/?vd_source=7b484be4a84a335a3d197df33bc93481

<!-- ## 图案列表 No.2 -->
![](https://w.wallhaven.cc/full/1k/wallhaven-1k9o13.png)
![](https://w.wallhaven.cc/full/q2/wallhaven-q21pjd.png)
{.gallery data-height="240"}



