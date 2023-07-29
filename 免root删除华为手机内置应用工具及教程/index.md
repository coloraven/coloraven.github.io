# 免ROOT删除华为手机内置应用工具及教程

文末附下载地址
## 原理：adb调试情况下，将系统应用禁用
```batch
ECHO OFF
MODE con: COLS=80 LINES=38
TITLE EMUI 系统精简
color 3f
:STARTS 
CLS
ECHO.                           华为系统精简 
ECHO. =============================================================================
ECHO.            请确定已经安装好驱动,并以经打开USB调试模式
ECHO.                     双清系统后，应用自动恢复                    华为花粉俱乐部
ECHO. ============================================================================== 
ECHO. 功能选择项（请输入相对应的序号按回车键确认）：
ECHO.
ECHO.              华为系统类                              测试命令类
ECHO.
ECHO. 1.卸载 华山动态        27.卸载 相机             0.查看连接设备状态
ECHO. 2.卸载 学生模式        28.卸载 备份             80.卸载Google套件
ECHO. 3.卸载 推送体验上传    29.卸载 华为移动服务     81.查看系统应用
ECHO. 4.卸载 互动图片屏保    30.卸载 会员服务         82.屏幕分辨率
ECHO. 5.卸载 文件取词标记    31.卸载 游戏助手         83.修改屏幕密度480
ECHO. 6.卸载 天际通          32.卸载 工作资料设置     84.完美动画修改0.76
ECHO. 7.卸载 K歌htm打印      33.卸载 彩信服务         85.查看电池状态
ECHO. 8.卸载 百度输入法      34.卸载 杂志锁屏         86.进入BL模式 
ECHO. 9.卸载 隐私空间        35.卸载 华为浏览器       87.进入REC模式
ECHO.10.卸载 智慧搜索        36.卸载 手势服务         88.禁止系统更新
ECHO.11.卸载 智能截屏        37.卸载 智能检测         89.重新启动
ECHO.12.卸载 智能识屏        38.卸载 省电精灵             
ECHO.13.卸载 语音助手        39.卸载 查找手机             
ECHO.14.卸载 sim卡应用       40.卸载 计算器             
ECHO.15.卸载 搜狐讯飞引擎    41.卸载 电子邮件           
ECHO.16.卸载 华为share       42.卸载 图库      
ECHO.17.卸载 悬浮导航        43.卸载 个人紧急信息          
ECHO.18.卸载 灭屏显示        44.卸载 智能助手        
ECHO.19.卸载 视频编辑        45.卸载 融合定位         
ECHO.20.卸载 多屏互动        46.卸载 时钟           
ECHO.21.卸载 备忘录          47.卸载  主题           
ECHO.22.卸载 音乐视频        48.卸载 应用商店     
ECHO.23.卸载 桌面                              
ECHO.24.卸载 华为钱包 NFC                
ECHO.25.卸载 银联支付保护                   
ECHO.26.卸载 镜子                                    
ECHO. ………………………………………………………………………………………………………
set choice= 
set /p choice=输入对应数字，然后按回车键（Success代表成功）:
if /i "%choice%"=="0" goto 0
if /i "%choice%"=="1" goto 1
if /i "%choice%"=="2" goto 2
if /i "%choice%"=="3" goto 3
if /i "%choice%"=="4" goto 4
if /i "%choice%"=="5" goto 5
if /i "%choice%"=="6" goto 6
if /i "%choice%"=="7" goto 7
if /i "%choice%"=="8" goto 8
if /i "%choice%"=="9" goto 9
if /i "%choice%"=="10" goto 10
if /i "%choice%"=="11" goto 11
if /i "%choice%"=="12" goto 12
if /i "%choice%"=="13" goto 13
if /i "%choice%"=="14" goto 14
if /i "%choice%"=="15" goto 15
if /i "%choice%"=="16" goto 16
if /i "%choice%"=="17" goto 17
if /i "%choice%"=="18" goto 18
if /i "%choice%"=="19" goto 19
if /i "%choice%"=="20" goto 20
if /i "%choice%"=="21" goto 21
if /i "%choice%"=="22" goto 22
if /i "%choice%"=="23" goto 23
if /i "%choice%"=="24" goto 24
if /i "%choice%"=="25" goto 25
if /i "%choice%"=="26" goto 26
if /i "%choice%"=="27" goto 27
if /i "%choice%"=="28" goto 28
if /i "%choice%"=="29" goto 29
if /i "%choice%"=="30" goto 30
if /i "%choice%"=="31" goto 31
if /i "%choice%"=="32" goto 32
if /i "%choice%"=="33" goto 33
if /i "%choice%"=="34" goto 34
if /i "%choice%"=="35" goto 35
if /i "%choice%"=="36" goto 36
if /i "%choice%"=="37" goto 37
if /i "%choice%"=="38" goto 38
if /i "%choice%"=="39" goto 39
if /i "%choice%"=="40" goto 40
if /i "%choice%"=="41" goto 41
if /i "%choice%"=="42" goto 42
if /i "%choice%"=="43" goto 43
if /i "%choice%"=="44" goto 44
if /i "%choice%"=="45" goto 45
if /i "%choice%"=="46" goto 46
if /i "%choice%"=="47" goto 47
if /i "%choice%"=="48" goto 48
if /i "%choice%"=="49" goto 49
if /i "%choice%"=="50" goto 50
if /i "%choice%"=="51" goto 51
if /i "%choice%"=="52" goto 52
if /i "%choice%"=="53" goto 53
if /i "%choice%"=="54" goto 54
if /i "%choice%"=="55" goto 55
if /i "%choice%"=="56" goto 56
if /i "%choice%"=="57" goto 57
if /i "%choice%"=="58" goto 58
if /i "%choice%"=="59" goto 59
if /i "%choice%"=="60" goto 60
if /i "%choice%"=="61" goto 61
if /i "%choice%"=="62" goto 62
if /i "%choice%"=="63" goto 63
if /i "%choice%"=="64" goto 64
if /i "%choice%"=="65" goto 65
if /i "%choice%"=="66" goto 66
if /i "%choice%"=="67" goto 67
if /i "%choice%"=="68" goto 68
if /i "%choice%"=="69" goto 69
if /i "%choice%"=="70" goto 70
if /i "%choice%"=="71" goto 71
if /i "%choice%"=="72" goto 72
if /i "%choice%"=="73" goto 73
if /i "%choice%"=="74" goto 74
if /i "%choice%"=="75" goto 75
if /i "%choice%"=="76" goto 76
if /i "%choice%"=="77" goto 77
if /i "%choice%"=="78" goto 78
if /i "%choice%"=="79" goto 79
if /i "%choice%"=="80" goto 80
if /i "%choice%"=="81" goto 81
if /i "%choice%"=="82" goto 82
if /i "%choice%"=="83" goto 83
if /i "%choice%"=="84" goto 84
if /i "%choice%"=="85" goto 85
if /i "%choice%"=="86" goto 86
if /i "%choice%"=="87" goto 87
if /i "%choice%"=="88" goto 88
if /i "%choice%"=="89" goto 89
if /i "%choice%"=="90" goto 90
if /i "%choice%"=="91" goto 91
if /i "%choice%"=="92" goto 92
if /i "%choice%"=="93" goto 93
if /i "%choice%"=="94" goto 94
if /i "%choice%"=="95" goto 95
if /i "%choice%"=="96" goto 96
if /i "%choice%"=="97" goto 97
if /i "%choice%"=="98" goto 98
if /i "%choice%"=="99" goto 99

echo 选择无效，请重新输入
echo.
:0
CLS
COLOR 2f
adb devices
pause
GOTO STARTS
:1
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.livewallpaper.matewenty
adb shell pm uninstall --user 0 com.android.wallpaper.livepicker
adb shell pm uninstall --user 0 com.huawei.himovie.partner1
adb shell pm uninstall --user 0 com.huawei.himovie.partner2
pause
GOTO STARTS
:2
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.parentcontrol
adb shell pm uninstall --user 0 com.huawei.ihealth
pause
GOTO STARTS
:3
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.pushagent
adb shell pm uninstall --user 0 com.huawei.bd
adb shell pm uninstall --user 0 com.huawei.android.UEInfoCheck
adb shell pm uninstall --user 0 com.android.calllogbackup
pause
GOTO STARTS
:4
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.dreams.phototable
adb shell pm uninstall --user 0 com.android.dreams.basic
pause
GOTO STARTS
:5
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.documentsui
adb shell pm uninstall --user 0 com.huawei.contentsensor
adb shell pm uninstall --user 0 com.android.apps.tag
pause
GOTO STARTS
:6
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.hiskytone
adb shell pm uninstall --user 0 com.huawei.skytone
pause
GOTO STARTS
:7
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.karaoke
adb shell pm uninstall --user 0 com.android.htmlviewer
adb shell pm uninstall --user 0 com.android.printspooler
pause
GOTO STARTS
:8
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.baidu.input_huawei
adb shell pm uninstall --user 0 com.huawei.secime
pause
GOTO STARTS
:9
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.securitymgr
pause
GOTO STARTS
:10
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.search
pause
GOTO STARTS
:11
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.qeexo.smartshot
pause
GOTO STARTS
:12
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.hitouch
pause
GOTO STARTS
:13
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.vassistant
pause
GOTO STARTS
:14
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.stk
pause
GOTO STARTS
:15
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.sohu.sohuvideo.emplayer
adb shell pm uninstall --user 0 com.iflytek.speechsuite
pause
GOTO STARTS
:16
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.instantshare
pause
GOTO STARTS
:17
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.FloatTasks
pause
GOTO STARTS
:18
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.aod
pause
GOTO STARTS
:19
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.videoeditor
pause
GOTO STARTS
:20
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.airsharing
pause
GOTO STARTS
:21
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.example.android.notepad
pause
:22
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.mediacenter
adb shell pm uninstall --user 0 com.huawei.himovie
pause
GOTO STARTS
:23
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.launcher
pause
GOTO STARTS
:24
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.wallet
adb shell pm uninstall --user 0 com.android.nfc
pause
GOTO STARTS
:25
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.trustspace
adb shell pm uninstall --user 0 com.unionpay.tsmservice
pause
GOTO STARTS
:26
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.hwmirror
pause
GOTO STARTS
:27
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.camera
pause
GOTO STARTS
:28
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.KoBackup
pause
GOTO STARTS
:29
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.hwid
pause
GOTO STARTS
:30
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.phoneservice
pause
GOTO STARTS
:31
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.gameassistant
pause
GOTO STARTS
:32
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.managedprovisioning
pause
GOTO STARTS
:33
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.mms.service
pause
GOTO STARTS
:34
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.keyguard
pause
GOTO STARTS
:35
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.browser
pause
GOTO STARTS
:36
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.motionservice
pause
GOTO STARTS
:37
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.hwdetectrepair
pause
GOTO STARTS
:38
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.powergenie
pause
GOTO STARTS
:39
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.findmyphone
pause
GOTO STARTS
:40
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.calculator2
pause
GOTO STARTS
:41
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.email
pause
GOTO STARTS
:42
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.gallery3d
pause
GOTO STARTS
:43
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.emergency
pause
GOTO STARTS
:44
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.suggestion
adb shell pm uninstall --user 0 com.huawei.intelligent
pause
GOTO STARTS
:45
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.location.fused
pause
GOTO STARTS
:46
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.android.deskclock
pause
GOTO STARTS
:47
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.android.thememanager
pause
GOTO STARTS

:48
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.huawei.appmarket
pause
GOTO STARTS





:80
CLS
COLOR 2f
adb shell pm uninstall --user 0 com.google.android.gms
adb shell pm uninstall --user 0 com.google.android.gsf
adb shell pm uninstall --user 0 com.android.vending
adb shell pm uninstall --user 0 com.google.android.onetimeinitializer
adb shell pm uninstall --user 0 com.google.android.partnersetup
adb shell pm uninstall --user 0 com.google.android.marvin.talkback
adb shell pm uninstall --user 0 com.android.ext.services
adb shell pm uninstall --user 0 com.google.android.backuptransport

adb shell pm uninstall --user 0 com.google.android.gsf.login
adb shell pm uninstall --user 0 com.google.android.printservice.recommendation
adb shell pm uninstall --user 0 com.google.android.feedback
adb shell pm uninstall --user 0 com.google.android.syncadapters.calendar
adb shell pm uninstall --user 0 com.google.android.syncadapters.contacts
adb shell pm uninstall --user 0 com.google.android.gsf.login


pause
GOTO STARTS
:81
CLS
COLOR 2f
adb shell pm list packages -s >系统应用bbb.txt
pause
GOTO STARTS
:82
CLS
COLOR 2f
adb shell wm size
pause
GOTO STARTS
:83
CLS
COLOR 2f
adb shell wm density 480
pause
GOTO STARTS
:84
CLS
COLOR 2f
adb shell settings put global window_animation_scale 0.96
adb shell settings put global transition_animation_scale 0.96
adb shell settings put global animator_duration_scale 0.43
pause
GOTO STARTS
:85
CLS
COLOR 2f
adb shell dumpsys battery
pause
GOTO STARTS
:86
CLS
COLOR 2f
adb reboot bootloader
pause
GOTO STARTS
:87
CLS
COLOR 2f
adb reboot recovery
pause
GOTO STARTS
:88
CLS
COLOR 2f
adb shell pm disable-user com.huawei.android.hwouc
pause
GOTO STARTS
:89
CLS
COLOR 2f
adb reboot
pause
GOTO STARTS
```

## 另一篇介绍了哪些可删
https://zhuanlan.zhihu.com/p/107371855
以下截取自该文章
```bash
package:com.huawei.hifolder //华为精品应用文件夹，   
package:com.android.mediacenter //华为音乐，一堆广告，还要登录华为ID...
package:com.huawei.hidisk //文件管理,功能挺全，但是竟然强行绑定云空间...
package:com.huawei.android.thememanager //主题，里面一堆巨丑&要付费的主题
package:com.huawei.intelligent //手机桌面滑到最左侧的智能情景模式...全是广告，唉
package:com.huawei.appmarket //华为应用市场，连skype、google都搜不出来的市场有鸟用？
package:com.huawei.wallet //华为钱包，用不着，刷卡有云闪付，公交卡有大都会。
package:com.huawei.android.findmyphone //查找手机，1000块的手机查找什么手机？
package:com.huawei.phoneservice //会员服务，不好意思，不是会员
package:com.android.browser //（华为）浏览器，看到我的文章上方推送的新闻了吧    
package:com.android.soundrecorder //录音机，卸载防止系统悄咪咪的监听我
package:com.baidu.input_huawei //百度输入法-华为版，起到1+1>2的效果，笑死我了
package:com.android.contacts //联系人，注意EMUI系统的拨号是属于联系人的子功能，
因此你会发现最终手机主页上的拨号+联系人都不见了
package:com.android.stk //SIM卡应用，已经过了2G时代，永别了
package:com.huawei.trustspace //支付保护中心，类似360沙箱，太麻烦不需要
package:com.android.calendar //日历，土味太浓，删了
package:com.huawei.vassistant //语音助手，防窃听，不多说
package:com.android.gallery3d //图库（系统相册），功能挺好，强绑华为云空间令人不爽，卸了
package:com.huawei.himovie //华为视频，本文一开头的罪魁祸首出现了，干掉你！
```
## 再一篇介绍哪些可以删
https://woj.app/7121.html
```bash
adb shell pm  disable-user com.android.emergency	##停用	个人紧急信息
adb shell pm uninstall --user 0 com.huawei.hicar	##卸载 智慧汽车
adb shell pm  disable-user com.huawei.trustspace	##（支付保护中心）停用
adb shell pm uninstall --user 0 com.huawei.hwstartupguide	#首次开机时、引导用户设置系列信息。你不是第一次开机了吧？卸载 
adb shell pm uninstall --user 0 com.android.dreams.phototable	##动态屏保 这玩意除了耗电一无是处。删
adb shell pm  disable-user com.huawei.trustagent 	##智能解锁  手环来解手机的锁，无用
adb shell pm uninstall --user 0 com.huawei.vassistant	##语音助手  小艺
adb shell pm  uninstall --user 0 com.huawei.hwireader	##华为阅读
adb shell pm  uninstall --user 0 com.huawei.iconnect	##扫描发现穿戴设备后进行连接提醒。用不着的话删
adb shell pm  uninstall --user 0 com.huawei.synergy		##可以帮您将手机端的消息同步到您的穿戴设备上。同上。
adb shell pm  uninstall --user 0 com.android.wallpaper.livepicker	##桌面动态壁纸。费电，删。
adb shell pm  disable-user com.huawei.android.UEInfoCheck	##用户体验计划监控。停用
adb shell pm  disable-user com.huawei.intelligent		##情景智能。 这是就是负一页的那个。
adb shell pm  disable-user com.huawei.android.karaoke	##卡拉OK  k歌音效
adb shell pm  disable-user com.huawei.rcsserviceapplication  ##智能推荐系统。用于华为智能助手服务推荐，EMUI亮点特性推荐以及智能通知管理。
adb shell pm  uninstall --user 0 com.huawei.hiview	##Emui日志上传功能
adb shell pm  uninstall --user 0 com.huawei.hiviewtunnel	##Emui日志上传功能
adb shell pm  disable-user com.huawei.regservice	##华为注册服务
adb shell pm  disable-user com.android.cts.ctsshim		##CTS兼容性检测
adb shell pm  disable-user com.android.cts.priv.ctsshim	##CTS
adb shell pm  disable-user com.huawei.android.pushagent	##华为推送服务 给个性化信息及广告用的
adb shell pm  disable-user com.huawei.nearby		##无需联网，通过蓝牙即可实现"附近的人"相互聊天，国内用不了
adb shell pm  uninstall --user 0 com.vmall.client	##华为商城
adb shell pm  uninstall --user 0 com.huawei.fans	##花粉俱乐部
```

## 常用ADB命令

### 1.获取设备状态
输入db get-state 回车
device：设备正常连接
offline：连接出现异常，设备无响应
unknown：没有连接设备

### 2.查看系统应用
查看所有应用：adb shell pm list packages
查看系统应用：adb shell pm list packages -s
查看用户应用：adb shell pm list packages -3

### 3．查看禁用的系统应用命令
先输入ADB-tools> adb shell
HWEVR:/ $ pm list packages -s -d  回车
再输入pm list packages -s -d   回车

### 4.重启命令
重启手机：adb reboot
重启到recovery：adb reboot recovery
重启到fastboot：adb reboot fastboot

### 5.禁用、启用、删除应用的命令
禁用程序为adb shell pm disable-user+空格+程序名；
启用程序为adb shell pm enable+空格+程序名；
删除程序为adb shell pm uninstall --user 0+空格+程序名

## 禁用服务清单-表格带说明

1.本表格重要的功能全是禁用命令，请自己选择删除还是禁用（具体命令在表格最后）		
2.自由选择需要禁用的应用，需要保留哪一个功能的，请删除那一行的代码即可		
5.禁用后，不满意，可以重新启用，删除则不可以。		
6.如果想一次性恢复所有禁用的应用，请打开设置-应用-应用管理-右上角的三个点，选择恢复默许设置-重置，重启即可		
7.代码可以复制多行，但不要含有汉字，必须是全英文，否则会不成功		
8.个人认为135行系统更新（刷绿色）之后的应用和功能不禁用为好，娱乐工作两不误，体验更佳。	
| 应用包名                                                     | 显示名称                          | 说明                       |
|----------------------------------------------------------|-------------------------------|--------------------------|
| com.huawei.livewallpaper.matetwenty                      | 华山动态主题                        | 无用                       |
| com.huawei.locationsharing                               | 位置共享                          | 除了费电，其它好像也没用处            |
| com.google.Android.backuptransport                       | 自动备份                          | 不影响华为云备份及普通备份            |
| com.huawei.hicar                                         | 智慧汽车连接                        | 不实用                      |
| com.huawei.hwpolicyservice                               | 旅行助手服务管理                      | 不用旅行助手的                  |
| com.huawei.trustcircle                                   | 银联支付保护中心                      | 没有支付宝微信安全，就是个坑           |
| com.huawei.trustspace                                    | 支付保护中心                        | 无用                       |
| com.huawei.desktop.explorer                              | 我的文件                          | 无用                       |
| com.android.sharedstoragebackup                          | 备份                            | 删除后，无法云备份                |
| com.huawei.contactscamcard                               | 名片全能王                         |                          |
| com.iflytek.speechsuite                                  | 迅飞语音引擎                        | 禁用后无影响                   |
| com.huawei.hwstartupguide                                | 引导用户设置                        | 首次开机时有效，其它时候无用           |
| com.huawei.android.findmyphone                           | 查找我的手机                        |                          |
| com.huawei.hiskytone                                     | 天际通                           |                          |
| com.android.wallpaper.livepicker                         | 动态壁纸                          |                          |
| com.huawei.skytone                                       | 天际通数据                         |                          |
| com.huawei.cloud                                         | 华为云                           | 禁用后不影响云空间及云备份            |
| com.android.email                                        | 电子邮件                          | 用第三方邮件代替                 |
| com.huawei.lives                                         | 华为生活服务                        |                          |
| com.android.dreams.basic                                 | 基本互动屏保                        |                          |
| com.huawei.search                                        | 华为搜索                          |                          |
| com.huawei.videoeditor                                   | 视频编辑                          |                          |
| com.huawei.android.karaoke                               | 卡拉ok                          |                          |
| com.google.android.marvin.talkback                       | 盲人辅助语音                        |                          |
| com.huawei.KoBackup                                      | 备份                            | 禁用不影响                    |
| com.huawei.powergenie                                    | 省电精灵                          | 禁用后更省电，如果游戏掉帧，请启用        |
| com.huawei.android.remotecontroller                      | 智能遥控器                         | 红外遥控器                    |
| com.android.keyguard                                     | 华为杂志锁屏                        |                          |
| com.android.apps.tag                                     | 标记                            |                          |
| com.android.emergency                                    | 个人紧急信息                        |                          |
| com.huawei.contentsensor                                 | 取词                            | 智能识屏里的插件                 |
| com.huawei.android.UEInfoCheck                           | 用户体验计划监控                      | 不解释                      |
| com.huawei.gameassistant                                 | 游戏助手                          |                          |
| com.huawei.gamebox                                       | 华为游戏中心                        | 如果想启用，请不要禁用应用市场          |
| com.android.calculator2                                  | 计算器                           |                          |
| com.huawei.nearby                                        | 无需联网，通过蓝牙即可实现"附近的人"相互聊天，国内用不了 |                          |
| com.huawei.android.pushagent                             | 华为推送服务                        | 给个性化信息及广告用的，很费电          |
| com.huawei.phoneservice                                  | 服务                            | 服务，删除后无法第一时间尝鲜升级         |
| com.huawei.motionservice                                 | 手势服务                          | 禁用不影响全面屏手势，需要分屏功能的勿禁用    |
| com.huawei.hilink.framework                              | 智能产品框架                        |                          |
| com.huawei.regservice                                    | 华为注册服务                        |                          |
| com.huawei.nlp                                           | 人工智能语言管理                      |                          |
| com.google.ar.core                                       | 谷歌 AR                         |                          |
| com.huawei.arengine.service                              | AR  EngineServer              |                          |
| com.huawei.hiai                                          | 华为智能AI                        |                          |
| com.huawei.vrservice                                     | 华为VR服务                        |                          |
| com.huawei.fastapp                                       | 快应用中心                         |                          |
| adb shell pm disable-user  com.huawei.aod                | 灭屏显示                          |                          |
| adb shell pm disable-user  com.huawei.lbs                | 物理硬件位置服务                      | 无用，还狂费电                  |
| com.huawei.rcsserviceapplication                         | 华为RCS服务                       | 增强短信功能，移动卡之间免费短信         |
| com.android.frameworkres.overlay                         | 可以禁用，不知道是什么                   |                          |
| com.huawei.wallet                                        | 华为钱包                          |                          |
| adb shell pm disable-user  com.huawei.android.hwpay      | 华为钱包支付                        |                          |
| adb shell pm disable-user  com.android.dreams.phototable | 相片保护程序                        | 只有当内存不足时才会启用             |
| adb  shell pm disable-user com.huawei.scanner            | 扫一扫                           | 禁用不影响所有应用的扫一扫功能          |
| 以下为系统预装应用                                                |                               | 预装应用全部是删除命令              |
| com.suning.mobile.ebuy                                   | 苏宁易购                          |                          |
| com.ximalaya.ting.android                                | 喜马拉雅                          |                          |
| cn.TuHu.android                                          | 途虎                            |                          |
| com.zhihu.android                                        | 知乎                            |                          |
| com.sohu.newsclient                                      | 搜狐新闻                          |                          |
| com.booking                                              | 阅读                            |                          |
| com.microsoft.translator                                 | 微软翻译                          |                          |
| com.tencent.qqlivehuawei                                 | 腾讯视频                          |                          |
| com.huawei.compass                                       | 指南针                           |                          |
| com.huawei.hwireader                                     | 华为阅读                          |                          |
| com.hicloud.android.clone                                | 手机克隆                          |                          |
| com.dianping.v1                                          | 大众点评                          |                          |
| com.taobao.taobao                                        | 淘宝                            |                          |
| com.sina.weibo                                           | 微博                            |                          |
| cn.wps.moffice_eng                                       | WPS                           |                          |
| com.baidu.BaiduMap                                       | 百度地图                          |                          |
| com.baidu.searchbox                                      | 百度搜索                          |                          |
| com.ss.android.article.news                              | 今日头条                          |                          |
| com.jingdong.app.mall                                    | 京东                            |                          |
| com.sankuai.meituan                                      | 美团                            |                          |
| com.UCMobile                                             | uc浏览器                         |                          |
| com.vmall.client                                         | 华为商城                          |                          |
| com.huawei.fans                                          | 花粉俱乐部                         |                          |
| com.netease.newsreader.activity                          | 网易新闻                          |                          |
| com.sohu.sohuvideo.emplayer                              | 华为搜狐视频                        |                          |
| com.huawei.hwvplayer.youku                               | 华为视频优酷版                       |                          |
| ctrip.android.view                                       | 携程                            |                          |
| com.android.mediacenter                                  | 华为音乐                          |                          |
| com.ss.android.ugc.aweme                                 | 抖音                            |                          |
| com.huawei.smarthome                                     | 智能家居                          |                          |
| com.android.hwmirror                                     | 镜子                            | 美女留下                     |
| com.huawei.scenepack                                     | 旅行助手                          |                          |
| com.huawei.android.tips                                  | 玩机技巧                          |                          |
| com.huawei.mmitest                                       | 首次开机测试                        |                          |
| com.huawei.android.chr                                   | HwChrService                  | 检测异常，收集异常关键信息，很费电        |
| com.huawei.bd                                            | 用户体验计划                        |                          |
| com.huawei.android.hwupgradeguide                        | 升级向导                          |                          |
| com.huawei.wifiprobqeservice                             | 评估WIFI质量                      |                          |
| com.huawei.hiview                                        | Emui日志上传功能                    |                          |
| com.huawei.hiviewtunnel                                  | Emui日志上传功能                    |                          |
| com.huawei.himovie.partner1                              | 系统视频缓存区                       | 除了增加手机的拉圾外，别无它用          |
| com.huawei.himovie.partner2                              | 系统视频缓存区                       | 除了增加手机的拉圾外，别无它用          |
| com.huawei.hifolder                                      | 精品推荐                          | 打开文件夹，会推荐应用的那个拉圾         |
| com.huawei.mycenter                                      | 会员中心                          |                          |
| com.eg.android.AlipayGphone                              | 支付宝                           |                          |
| 谷歌服务                                                     | 禁用命令                          |                          |
| com.google.android.configupdater                         | 谷歌服务更新                        | 谷歌可以全禁用或删除，没有任何问题        |
| com.google.android.overlay.settingsProvider              | 多层设置                          | 国内也用不了                   |
| com.google.android.overlay.gmsconfig                     | 在谷歌地地图上显示位置                   |                          |
| com.google.ar.core                                       | AR                            |                          |
| com.android.vending                                      | 谷歌应用市场                        |                          |
| com.android.cts.priv.ctsshim                             | CTS                           |                          |
| com.android.calllogbackup                                | 电话标签备份                        |                          |
| com.android.cts.ctsshim                                  | CTS兼容性检测                      |                          |
| com.android.companiondevicemanager                       |                               |                          |
| com.google.android.configupdater                         | 无线更新不可执行的系统                   |                          |
| com.google.android.tts                                   | 文本转语音无障碍服务                    |                          |
| com.android.inputmethod.latin                            | 安卓虚拟键盘                        |                          |
| com.google.android.syncadapters.contacts                 | 谷歌通讯录同步                       |                          |
| 华为的智能服务                                                  | 禁用命令                          |                          |
| com.huawei.android.FloatTasks                            | 悬浮导航                          | 禁用，没发现什么问题               |
| adb shell pm disable-user  com.huawei.hiboard            | 智能助手                          | mate20系列没有，其它老华为手机有      |
| adb shell pm disable-user  com.huawei.suggestion         | 情景智能                          |                          |
| com.huawei.hwdetectrepair                                | 智能检测                          | 检测硬件的，用不到                |
| com.huawei.pengine                                       | 智能建议                          |                          |
| com.huawei.hiaction                                      | 智能识屏                          | 无用                       |
| com.huawei.hitouch                                       | 智能识屏中爆炸文字                     |                          |
| com.huawei.trustagent                                    | 智能解锁                          | 手环来解手机的锁，无用              |
| com.qeexo.smartshot                                      | 智能截屏                          | 禁用后不影响正常截屏               |
| com.huawei.android.hwouc                                 | 系统更新                          | 最好禁用，想升级系统就恢复启用即可        |
| com.huawei.vassistant                                    | 语音助手                          | 小艺                       |
| com.huawei.android.hsf                                   | 华为框架                          | 停用它，WLAN闲时流量更新和后台自动安装没法用 |
| com.android.frameworkhwext.HONOR                         | 华为框架服务                        | 可删                       |
| com.huawei.tips                                          | 智能提醒                          |                          |
| com.huawei.intelligent                                   | 情景智能                          | 负一屏，最左边的那个智能助手           |
| 工作类应用                                                    | 禁用命令                          |                          |
| com.huawei.android.dsdscardmanager                       | 双卡管理                          | 单卡用户可禁用                  |
| com.huawei.android.airsharing                            | 多屏互动                          | 工作神器，自己判断                |
| com.android.stk                                          | sim卡应用                        | 有SIM-NFC卡的，不要禁用          |
| com.android.nfc                                          | NFC服务                         | 有NFC公交卡、门禁卡不要禁用          |
| com.android.printspooler                                 | 打印处理任务                        | 无线打印，需要办公的请不要禁用          |
| com.google.android.printservice.recommendation           | 发现和配置网络打印机                    | 无线打印，需要办公的请不要禁用          |
| com.huawei.printservice                                  | 打印服务                          | 无线打印，需要办公的请不要禁用          |
| com.android.bips                                         | 默认打印                          | 无线打印，需要办公的请不要禁用          |
| com.huawei.android.instantshare                          | Huawei Share                  |                          |
| com.huawei.screenrecorder                                | 屏幕录制                          |                          |
| com.huawei.HwMultiScreenShot                             | 滚动截屏                          |                          |
| 华为自带的应用                                                  | 禁用命令                          |                          |
| com.huawei.android.thememanager                          | 华为主题                          |                          |
| com.huawei.health                                        | 华为运动健康                        |                          |
| adb shell pm  disable-usercom.huawei.himovie             | 华为视频                          | 如果要用无线投屏的话，不要禁用视频        |
| com.huawei.appmarket                                     | 华为应用市场                        |                          |
| com.huawei.securitymgr                                   | 隐私空间                          |                          |
| com.huawei.browser                                       | 华为浏览器                         |                          |
| com.android.soundrecorder                                | 华为录音机                         |                          |
| com.example.android.notepad                              | 备忘录                           |                          |
| com.huawei.android.totemweather                          | 华为天气                          |                          |
| com.android.deskclock                                    | 华为时钟                          |                          |
| com.android.calendar                                     | 华为日历                          |                          |
| com.baidu.input_huawei                                   | 百度输入法                         | 先安装其它输入法再删除              |


## 还一篇
https://zhuanlan.zhihu.com/p/27853169


下载地址：[免ROOT删除华为手机内置应用工具附件](https://coloraven.github.io/2021/8/免ROOT删除华为手机内置应用工具及教程/删除华为手机内置应用.rar)

