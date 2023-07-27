# VSCODE插件Remote-SSH配置

## ●Preface  
服务器很多时候都是部署在 Linux 远程机器上的，我们通常是 SSH 连过去然后用 vim 或者 emacs 去修改源文件。  
这种方式对我来说很麻烦，因为我已经习惯了全宇宙最好用的 C++IDE Visual Studio，离开 IDE 写代码实在太痛苦了。  
所以我只能借助 samba+sourceinsight 的组合来勉强度日。这个组合其实是比较好的，只不过配置特别麻烦，实在是不想折腾。  
这时，微软开发了一个 VSCode 的插件 Remote-SSH，可以说是目前比较完美的解决了在 windows 下开发 linux 程序的问题。  
Remote-SSH 配置简单，界面可视化，你可以把他看做是带 IDE 的 Putty。当然你也可以只把他当做一个远程 ssh 的连接工具来代替 putty，xshell。  


## ●安装 Remote-SSH  
（1）`VSCode` 左侧边栏上找到 `Extensions` 按钮，点击打开扩展插件面板。  
（2）在扩展搜索栏中搜索到 `Remote-SSH` 这个插件，然后点击下载安装这个插件。  
（3）此插件安装完毕后，侧边栏会出现一个名为 `Remote-SSH` 新的图标按钮。  
（4）点击 `VSCode` 左侧边栏上的 `Remote-SSH` 图标按钮，打开 `Remote-SSH` 面板。  
（5）在 `CONNECTIONS` 条目右边找到配置按钮图标 [Configure]，点击配置。  
（6）此时会弹出一个下拉框，选择 config 配置文件保存路径，比如 `C:\Users\Administrator\.ssh\config`  
（7）点击编辑这个 `config` 文件，编辑代码如下示例：
```yaml
        Host njdaby   #远程主机 1 别名 alias，注意主机别名不能包含 @符，否则会连接失败  
           HostName 117.78.41.7  
           User root  
           IdentityFile C:\Users\Administrator\.ssh\id_rsa
           #IdentityFile 指定秘钥名称路径 ，缺省路径为 `%HOME%\.ssh\id_rsa`，其中 %HOME%为用户目录
``` 
 （8）保存配置文件后，上面保存的远程主机别名就出现在 'CONNECTIONS' 条目的下拉列表中。  
 （9）在 'CONNECTIONS' 下拉列表中点击需要连接的主机别名，开始连接远程主机。  
         如果希望连接时，不要输入密码，那么还需要在本地创建密钥，并把公钥复制到远程服务器上。  


## ●注意事项  
①使用秘钥连接 ssh 时，如果不指定秘钥路径，默认秘钥路径为 '% HOME%\.ssh\id_rsa'，如果连接失败，就要检查确认该路径是否正确。  
②vscode 的配置文件 config 中，注意主机别名不能包含 @符，否则会连接失败。
