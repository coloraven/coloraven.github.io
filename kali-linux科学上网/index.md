# 转载-Kali Linux科学上网

转载自：https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/
用于备份该文章，以免源博客文章突然消失后找不到。
本文只讲解 Kali Linux 下针对`SS`和 `SSR`的客户端配置。由于 Kali 基于 Debian，所以其它基于 Debian 的 Linux 类似，例如Ubuntu。

关于科学上网的具体介绍请参见我的另一篇博客 [科学上网](https://wsxq2.55555.io/blog/2019/07/07/科学上网)。本文是它的子集

**温馨提示**：如果你的 Kali Linux 在虚拟机中且主机已经实现了科学上网，那么你没必要再折腾，直接使用[通过已经可以科学上网的电脑实现科学上网](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#通过已经可以科学上网的电脑实现科学上网)这个方法即可


## SS

本部分最后更新时间：2018-04-08。

### shadowsocks-qt5[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#使用-shadowsocks-qt5)

2019-07-02更新： 客户端选择`shadowsocks-qt5`是因为它简单，界面友好（好吧，是因为当初只听说过它）。现在的我更倾向于使用`shadowsocks-libev`作为客户端，因为它最近一次更新在 2019 年 7 月，而 shadowsocks（即原始的 Python 版）最后更新时间是 2018 年 10 月，shadowsocks-qt5 最近一次更新则是在 2018 年 8 月

具体环境说明：

* 客户端操作系统：Kali-Linux

    * 使用的 shadowsocks 实现（客户端）：[shadowsocks-qt5](https://github.com/shadowsocks/shadowsocks-qt5)
    * 使用的用户：root

另外，对于其它的 shadowsocks 实现，参考相应的官网文档操作即可。它们的官网链接在[Shadowsocks - Implementations](https://shadowsocks.org/en/spec/Implementations.html)页面中

#### 简介[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#简介)

> Shadowsocks-Qt5 is a native and cross-platform shadowsocks GUI client with advanced features.
>
> ### Features
>
> * Shadowsocks-Qt5 is written in C++ with Qt 5.
> * Support traffic statistics
> * Support server latency (lag) test
> * Use multiple profiles simultaneously
> * config.ini is located under ~/.config/shadowsocks-qt5/ on *nix platforms, or under the application’s directory on Windows.
>
> ——引用自[shadowsocks/shadowsocks-qt5: A cross-platform shadowsocks GUI client](https://github.com/shadowsocks/shadowsocks-qt5)

#### 安装[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#安装)

1.  在`/etc/apt/sources.list`文件末尾添加: `deb http://ppa.launchpad.net/hzwhuang/ss-qt5/ubuntu devel main`
2.  更新 apt 软件列表：

```bash
    apt update #这里会提示错误，以下两步解决该错误
     gpg --keyserver keyserver.ubuntu.com --recv 6DA746A05F00FA99
     gpg --export --armor 6DA746A05F00FA99 | sudo apt-key add -
     apt update #这一步成功后便可安装shadowsocks-qt5了
```


3.  安装shadowsocks-qt5: `apt install shadowsocks-qt5 `。

#### 配置[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#配置)

1.  安装后在`bash`中输入`ss-qt5`, 完成配置, 配置好后的图如下：

    ![ss-qt5](http://wsxq12.55555.io/Kali-Linux科学上网/ss-qt5主界面.png)

    图中使用的服务器账号是我花**180元/年**租用的搬瓦工的 
    VPS (见下图)（大家也可以搭建一个属于自己的 
    SS 服务器，可以学到不少东西）

    ![bwg](http://wsxq12.55555.io/Kali-Linux科学上网/bwg主机信息界面.png)

#### 设置 

PAC[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#设置-pac)

1.  获得 pac 文件：

    ```bash
      pip install genpac
      pip install --upgrade genpac
      mkdir ~/vpnPAC
      cd ~/vpnPAC
      touch user-rules.txt
      genpac -p "SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" --output="autoproxy.pac" --gfwlist-url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt" --user-rule-from="user-rules.txt"
    ```

2.  系统设置自动代理: **设置->网络->网络代理**，**方式**改为**自动**，**配置
    URL**改为：`file://root/vpnPAC/autoproxy.pac`

#### 优化[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#优化)

1.  设置开机启动：通过`kali linux`自带的优化工具实现: `Win+a`, 直接输入优化工具，出现优化工具图标（当然你也可以自己找），双击，找到开机启动程序，添加`shadowsock-qt5`
2.  自动连接某个节点：打开`bash`，输入`ss-qt5`，**右键某个节点->编辑->程序启动时自动连接**
3.  通过快捷键开启或关闭shadowsocks-qt5: **设置->键盘->添加自定义快捷键**（滑到最下面你会看到一个`+`）， **名字**可以随意，**命令**输入`ss-qt5`（关闭时输入`pkill ss-qt5`），**按键**设置成你喜欢的即可。

### shadowsocks-libev[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#使用-shadowsocks-libev)

#### 简介[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#简介-1)

> shadowsocks-libev 是一个 shadowsocks 协议的轻量级实现，是 shadowsocks-android, shadowsocks-ios 以及 shadowsocks-openwrt 的上游项目。其具有以下特点：
>
> * 体积小巧，静态编译并打包后只有 100 KB。
>
> * 高并发，基于 libev 实现的异步 I/O，以及基于线程池的异步 DNS，同时连接数可上万。
>
> * 低资源占用，几乎不占用 CPU 资源，服务器端内存占用一般在 3MB 左右。
>
> * 跨平台，适用于所有常见硬件平台，已测试通过的包括 x86 ARM 和 MIPS。也适用于大部分 POSIX 的操作系统或平台，包括 Linux，OS X 和 gwin 等。
>
> * 协议及配置兼容，完全兼容 shadowsocks 协议，且兼容标准实现中的 JSON 风格配置文件，可与任意实现的 shadowsocks 端或服务端搭配使用。
>
>
> ——引用自[CentOS 7 配置 shadowsocks-libev 服务器端进行科学上网 | 鸣沙山侧 月牙泉畔](https://roxhaiy.wordpress.com/2017/08/04/430/)

#### 安装[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#安装-1)

```bash
apt install shadowsocks-libev
```

查看该软件包中有哪些文件：

```bash
dpkg -l shadowsocks-libev
```

#### 配置[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#配置-1)

修改配置文件`/etc/shadowsocks-libev/config.json`：

```json
{
    "server":"serverip",
    "server_port":1234,
    "local_address": "0.0.0.0",
    "local_port":1080,
    "password":"shadowsocks",
    "timeout":60,
    "method":"aes-256-cfb"
}
```

#### 控制[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#控制)

使用如下命令启动：

```bash
systemctl start shadowsocks-libev-local@config
```

其中`config`是你的配置文件的名字（`config.json`），如果变了，则这里也需要变

使用如下命令设置开机自启：

```bash
systemctl enable shadowsocks-libev-local@config
```

……

#### 查看日志[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#查看日志)

* `/var/log/syslog`
* `journalctl -u shadowsocks-libev-local@config`

#### 后续步骤[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#后续步骤)

参见 [PC 连接到 SSR Local](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#pc-连接到-ssr-local)

## SSR[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#ssr)

SSR 的诸多实现如下（和 
SS 类似）：

实现                   | 编程语言            | 适用平台                | 最近一次更新  | 服务器 or 客户端
-------------------- | --------------- | ------------------- | ------- | ----------
shadowsocksr         | Python          | Linux, OSX          | 2018-05 | both      
shadowsocksr-libev   | C               | Linux, OSX, openwrt | 2018-03 | both      
shadowsocksr-android | Java,Go         | Android             | 2018-03 | client    
shadowsocks-csharp   | C#              | Windows             | 2018-04 | client    
electron-ssr         | JavaScript, Vue | Linux, OSX, Windows | 2019-05 | client    

### shadowsocksr（Python 版）（

SSR Local 连接到 

SSR Server[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#shadowsocksrpython-版ssr-local-连接到-ssr-server)

* 操作系统：Kali Linux。实际上只要是 Linux 将本文内容稍加修改也适用。毕竟核心的东西是不变的

    * 使用的 

        SSR 客户端：shadowsocksr（Python 版）。

2019-07-05 更新： 该部分阐述了如何让 
SSR Local 连接到 
SSR Server。在 
SSR Local 和 
SSR Server 通信的过程中使用的协议为 
SSR

之所以使用 Python 版，是因为我只找到 Python 版的，/笑哭。 这一步是最重要的，后面的方法都建立在这个基础之上

2019-07-03 更新：事实上，
SSR 现在可用的 Linux 客户端有三个，shadowsocksr, shadowsocksr-libev, electron-ssr，参见前文的表格

#### 安装[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#安装-2)

获得 Python 版 
SSR 的相关文件：

```bash
cd ~/
git clone https://github.com/shadowsocksrr/shadowsocksr
```

经测试，其实只有 shadowsocksr 下的 shadowsocks 目录是必须的

#### 配置[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#配置-2)

根据你的服务器配置修改配置文件`~/shadowsocksr/config.json`:

```json
{
    "server": "<ip address>",
    "server_ipv6": "::",
    "server_port": 8388,
    "local_address": "127.0.0.1",
    "local_port": 1080,

    "password": "password",
    "method": "none",
    "protocol": "auth_chain_a",
    "protocol_param": "",
    "obfs": "plain",
    "obfs_param": "",
    "speed_limit_per_con": 0,
    "speed_limit_per_user": 0,

    "additional_ports" : {},
    "additional_ports_only" : false,
    "timeout": 120,
    "udp_timeout": 60,
    "dns_ipv6": false,
    "connect_verbose_info": 0,
    "redirect": "",
    "fast_open": false
}
```

#### 启动[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#启动)

启动
SSR客户端：

```bash
cd ~/shadowsocksr/shadowsocks
python2 local.py -c ~/shadowsocksr/config.json
```

#### 测试[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#测试)

下面的每个步骤都建立在前一个步骤成功的基础上：

1.  使用命令`ss -ltn | grep 1080`，其输出应当如下：

    ```bash
    LISTEN     0      128          127.0.0.1:1080                     *:*
    ```

    如果失败，说明启动失败，可能是配置文件错误导致的

2.  使用浏览器进行测试，即选择 [浏览器全局代理](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#浏览器全局代理) 这部分的方法进行测试

    如果失败，则可能是服务器连不上导致的

#### 自动化[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#自动化)

每次手动启动实在太麻烦，可以写个脚本让它在打开终端时自动启动，也可以让它开机自启。对于前者，可将如下bash脚本添加到`~/.bashrc`文件中（我自己写的，欢迎提建议）：

```bash
function pg(){
  ps aux | grep -v "grep" |grep $1 
}
function ssr(){
	ps aux |grep "[l]ocal\.py" > /dev/null
	if [ $? -eq 1 ]; then
		python ~/shadowsocksr/shadowsocks/local.py -c ~/shadowsocksr/config.json -d start
	else
		if [ -n "$1" ]; then
			kill `pg "local\.py" | awk '{print $2}'`
		else
			echo "ssr has been run!"
		fi
	fi
}
ssr
```

简要说一下上面那个函数`ssr`的用法：直接在 bash 中输入`ssr`后回车则后台启动（关闭终端也能继续运行）ssr客户端，输入`ssr <任意字符>`则关闭已启动的ssr客户端。

#### 后续步骤[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#后续步骤-1)

参见 [PC 连接到 
SSR Local](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#pc-连接到-ssr-local)

## PC 连接到SSR Local[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#pc-连接到-ssr-local)

2019-07-03 更新： 该部分阐述了如何让 
SSR Local 监听到数据，即如何让应用程序走本地代理。本地代理使用的协议为 socks5。

### 浏览器全局代理[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#浏览器全局代理)

2019-07-04 更新：本部分的目标在于让浏览器浏览所有网页时都走代理。只需在浏览器中设置手动代理即可

以 FireFox 为例：

1.  找到浏览器中的手动代理设置的位置：点击右上角的菜单，选择**Preferences**，选择**General**，滑到最下面，选择**Network Proxy**标签下的**Settings**，选择**Manual proxy configuration**
2.  配置：找到**SOCKS Host**一栏，填入`127.0.0.1`和`1080`，在下面选择**SOCKS v5**，其它栏留空（如**HTTP Proxy**）。并在之后的**No Proxy for**中填入不需要代理的网址或 
    IP 地址或网段（例如 127.0.0.1、192.168.0.0/16等）。

    2019-07-04 更新：记得勾选下方的**Proxy 
    DNS when using 
    SOCKS v5**以防止 
    GFW 的 
    DNS 污染。此外，对第 2 步的手动配置代理中的说明如下：
    * **HTTP Proxy**：

        HTTP 代理服务器地址。须知，使用前面的方法在`127.0.0.1 1080`处搭建的代理服务器是 

        SOCKS 代理服务器（不是 

        HTTP 代理服务器），且使用的是 socks5 协议（不是 socks4/socks4a 协议）。所以在这里填写`127.0.0.1 1080`将无法访问（即必须留空）

    * **SSL Proxy**：访问 

        HTTPS 站点时使用的代理服务器地址，其实就是 

        HTTP 代理服务器地址。留空原因同上

    * **FTP Proxy**：访问 

        FTP 站点时使用的代理服务器地址，其实就是 

        HTTP 代理服务器地址（不过需要注意的是 

        FTP 代理是存在的，例如使用工具`ftp.proxy`）。留空原因同上

    * **SOCKS Host**：访问任意站点时使用的代理服务器地址。

完！

这时便可以访问[https://www.google.com](https://www.google.com/)了，简单吧？

### 系统全局代理[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#系统全局代理)

在系统设置中的网络代理方式设为**手动**，并将相应的**Socks Host**改为`127.0.0.1 1080`即可。具体步骤如下：

1.  设置系统手动代理：设置->网络->网络代理，方式改为**手动**，**SOCKS Host**改为`127.0.0.1 1080`，其它留空（留空的理由和前文类似）

    **温馨提示**：该处的设置依赖于`network-manager`服务，应确保其正在运行。（有的人因为`network-manager.service`和`networking.service`冲突所以采取网上的建议将`network-manager.service`给禁用了，结果导致系统设置中和网络相关的设置均不可用。好吧，说的就是我自己`-_-`）可以使用`systemctl`命令查看`network-manager.service`的状态，如下所示：

    ```bash
    root@kali:~# systemctl status network-manager.service 
    ● NetworkManager.service - Network Manager
       Loaded: loaded (/lib/systemd/system/NetworkManager.service; enabled; vendor preset: enabled)
       Active: active (running) since Thu 2019-07-04 23:30:33 CST; 19h ago
         Docs: man:NetworkManager(8)
     Main PID: 396 (NetworkManager)
        Tasks: 3 (limit: 4695)
       Memory: 13.8M
       CGroup: /system.slice/NetworkManager.service
               └─396 /usr/sbin/NetworkManager --no-daemon

    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.6270] manager: NetworkManager state is now CONNECTED_GLOBAL
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7143] modem-manager: ModemManager available
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7188] device (eth0): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7203] device (eth0): state change: prepare -> config (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7210] device (eth0): state change: config -> ip-config (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7215] device (eth0): state change: ip-config -> ip-check (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7226] device (eth0): state change: ip-check -> secondaries (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.7233] device (eth0): state change: secondaries -> activated (reason 'none', sys-iface-state: 'external')
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.8065] device (eth0): Activation: successful, device activated.
    7月 04 23:30:35 kali.abc.com NetworkManager[396]: <info>  [1562254235.8200] manager: startup complete
    root@kali:~#
    ```

    另外，这一步中的设置完成后，每次打开新终端的时候，检查代理相关的环境变量，你会发现：

    ```bash
    root@kali:~# env|grep -i proxy
    ALL_PROXY=socks://127.0.0.1:1080/
    no_proxy=
    NO_PROXY=
    all_proxy=socks://127.0.0.1:1080/
    root@kali:~#
    ```

    所以这个步骤的实质只是设置了下环境变量 ![:joy:](https://github.githubassets.com/images/icons/emoji/unicode/1f602.png ":joy:")

    假如你在系统的网络代理设置中将所有代理均设置为`127.0.0.1 1080`且**Ignore Hosts**设置为`127.0.0.1, 192.168.0.0/16`，那么在新打开的终端中检查代理相关的环境变量，你会发现：

    ```bash
    root@kali:~# env|grep -i proxy
    HTTP_PROXY=http://127.0.0.1:1080/
    FTP_PROXY=http://127.0.0.1:1080/
    https_proxy=http://127.0.0.1:1080/
    http_proxy=http://127.0.0.1:1080/
    ALL_PROXY=socks://127.0.0.1:1080/
    no_proxy=127.0.0.1,192.168.0.0/16
    NO_PROXY=127.0.0.1,192.168.0.0/16
    HTTPS_PROXY=http://127.0.0.1:1080/
    all_proxy=socks://127.0.0.1:1080/
    ftp_proxy=http://127.0.0.1:1080/
    root@kali:~#
    ```

    同样印证了上述结论——在 Kali 系统设置中的网络代理设置处进行手动代理设置实质上是修改了代理相关的环境变量

    需要注意的是（如前文所述），通用代理只有两种：
    HTTP 代理（使用 http 协议）和 
    SOCKS 代理（使用 socks4/socks4a/socks5 协议）。即代理相关环境变量中，每个变量`=`后面的协议部分必需是`http/socks4/socks4a/socks5`之一（对于`curl`还支持`socks5h`）

2.  测试：打开浏览器，输入网址`www.google.com`看是否访问成功

    2019-07-05 更新：如果使用的浏览器是 FireFox，则还需要将网络代理设置为**Use system proxy settings**。同样要记得勾选下方的**Proxy 
    DNS when using 
    SOCKS v5**以防止 
    GFW 的 
    DNS 污染

### 真·系统全局代理（透明代理）[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#真系统全局代理透明代理)

如前所述，在 Kali 系统设置中的网络代理设置处进行手动代理设置实质上是修改了代理相关的环境变量。对于 linux 下不支持代理的程序而言，前面的设置并没有什么用，即并非真的实现了全局代理。那么如果要实现真正意义上的全局代理，即让所有应用都经过代理服务器该怎么办？答案是使用 tsocks：

* [tsocks 官网](http://tsocks.sourceforge.net/)
* [tsocks 下载链接](https://sourceforge.net/projects/tsocks/files/tsocks/)
* [tsocks 手册](https://linux.die.net/man/8/tsocks)

> tsocks 利用 LD_PRELOAD 机制，代理程序里的`connect`函数，然后就可以代理所有的 
> TCP 请求了。不过对于 dns 请求，默认是通过 udp 来发送的，所以 tsocks 不能代理 dns 请求。
>
> 默认情况下，tsocks 会先加载`~/.tsocks.conf`，如果没有，再加载`/etc/tsocks.conf`。对于 local ip 不会代理。
>
> 使用方法：
>
> ```bash
> sudo apt-get install tsocks
> LD_PRELOAD=/usr/lib/libtsocks.so wget http://www.facebook.com
> ```
>
>
> ——引用自[科学上网的一些原理 | 横云断岭的专栏](http://hengyunabc.github.io/something-about-science-surf-the-internet/)

### 通过 SOCKS 代理进行 DNS 查询[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#通过-socks-代理进行-dns-查询)

使用 [dns2socks](https://sourceforge.net/projects/dns2socks/)（Github 上也有其项目地址https://github.com/qiuzi/dns2socks）或 [overture](https://github.com/shawn1m/overture)

此外，shadowsocks-libev 中的 ss-tunnel 也能实现该功能。和 dns2socks 相比，ss-tunnel 走 
TCP（即 socks5），而 dns2socks 走 
UDP

具体步骤就不详述了

对了，
HTTP 代理 
DNS 的解析必然是通过代理的：

> 对于 
> HTTP/
> HTTPS 类型的代理服务器而言，请求的域名会作为 
> HTTP 协议的一部分直接发往代理服务器，不会在本地进行任何解析操作。也就是说，域名的解析与连接目标服务器，是代理服务器的职责。浏览器本身甚至无须知道最终服务器的 
> IP 地址。据我所知，此行为无法通过浏览器选项等更改。
>
> 也就是说，理论上使用 
> HTTP/
> HTTPS 类型的代理服务器时，本地的 
> DNS 解析、缓存、 hosts 文件等都不使用，与本地设置的 
> DNS 服务器地址无关。
> DNS 解析完全在代理服务器上进行。
>
> ——引用自[请问在设置http/https代理后DNS的解析还是通过proxy吗?](https://github.com/FelisCatus/SwitchyOmega/issues/963#issuecomment-270055221)
### 转换 SOCKS 代理为 HTTP 代理[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#转换-socks-代理为-http-代理)

2019-07-04 更新：相关的工具有很多，例如 Polipo、privoxy等。这里使用的工具是 Polipo。需要注意的是 Polipo 最后一次更新是在 2014-05-15（参见 [Polipo - Wikipedia](https://en.wikipedia.org/wiki/Polipo)）

如前所述，通用代理只有两种：
HTTP 代理（使用 
HTTP 协议）和 
SOCKS 代理（使用 socks4/socks4a/socks5 协议）。最常见且最普及的是前者，有的应用不支持后者。所以为了让那些不支持 
SOCKS 代理的应用程序使用代理，需要将 
SOCKS 转换为 
HTTP 代理。

`Polipo`可以用来将`SOCKS`的代理转换为`HTTP`的代理，从而使那些只支持`HTTP`代理的软件（如`wget`，部分浏览器，部分操作系统（如 Windows 就只支持 http 代理和 socks4 代理，这是我通过抓包分析发现的））也可以科学上网

1.  安装`polipo`:

    ```bash
    apt install polipo
    ```

2.  修改`/etc/polipo/config`文件为如下内容：

    ```bash
    logSyslog = true
    logFile = /var/log/polipo/polipo.log

    socksParentProxy = "127.0.0.1:1080"
    socksProxyType = socks5
    proxyAddress = "0.0.0.0"
    proxyPort = 8123
    ```

3.  重启`polipo`（安装后它会自动启动，故这里说重启）：

    ```bash
    systemctl restart polipo
    ```

4.  验证 polipo 是否正常工作：

    ```bash
    export http_proxy=http://127.0.0.1:8123/
    curl www.google.com
    ```

    如果正常，就会返回抓取到的 Google 网页内容。可通过`man polipo`查看其帮助文档。

### 浏览器自动代理[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#浏览器自动代理)

2019-07-04 更新：本部分的目标在于让浏览器根据浏览的网站的不同自动选择是否走代理，例如对于国外网站走代理，对于国内网站不走代理。方法也很简单，使用浏览器插件即可，FireFox 用 FoxyProxy，Chrome 用 SwitchyOmega。

FoxyProxy 是 Firefox 浏览器中的一个非常好用的代理插件。因为有科学上网需求的主要是浏览器，故若只是为了让浏览器科学上网，则可采用此方法。当然，如果用的是 Chrome ，则可采用 Chrome + SwitchyOmega 的方案替代之。

1.  安装`FoxyProxy`插件：https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/
2.  设置`FoxyProxy`选项：

    1.  **Add Proxy**: `Proxy Type`选`SOCKS5`，`IP address`填`127.0.0.1`，`Port`填`1080`，记得最后点下`Save`
    2.  添加`Patterns`: 在选项主界面，点击刚刚添加的`Proxy`的`Patterns`，根据自己的需要添加`Patterns`
3.  启用`FoxyProxy`：单击浏览器中右上角相应的图标，选择`Use Enabled Proxies By Patterns and Priority`
4.  测试：输入网址`www.google.com`看是否访问成功

### PAC（代理自动配置）[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#pac代理自动配置)

> 代理自动配置（英语：Proxy auto-config，简称
> PAC）是一种网页浏览器技术，用于定义浏览器该如何自动选择适当的代理服务器来访问一个网址。
>
> 一个
> PAC文件包含一个JavaScript形式的函数“FindProxyForURL(url, host)”。这个函数返回一个包含一个或多个访问规则的字符串。用户代理根据这些规则适用一个特定的代理器或者直接访问。当一个代理服务器无法响应的时候，多个访问规则提供了其他的后备访问方法。浏览器在访问其他页面以前，首先访问这个
> PAC文件。
> PAC文件中的
> URL可能是手工配置的，也可能是是通过网页的网络代理自动发现协议（
> WPAD）自动配置的。
>
> ——引用自[代理自动配置 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/代理自动配置)

2019-07-06 更新：另外还可参见 [breakwa11/gfw_whitelist: gfw_whitelist](https://github.com/breakwa11/gfw_whitelist) 了解关于 
PAC 的更多信息

此方法主要使用了`genpac`（GENerate 
PAC file）生成 
PAC 文件，并将系统设置中的网络代理方式改为自动，将其`Configuration URL`指向相应的 
PAC 文件位置。具体过程如下：

1.  安装`genpac`：

    ```bash
    #安装
    pip install genpac
    #更新
    pip install --upgrade genpac
    ```

2.  生成

    PAC文件：

    ```bash
    mkdir ~/.pac
    cd ~/.pac
    touch user-rules.txt #可在此文件中添加用户自定义规则，此处省略
    genpac --pac-proxy "SOCKS5 127.0.0.1:1080" --output="ProxyAutoConfig.pac" --user-rule-from="user-rules.txt"
    ```

3.  设置系统自动代理：**设置->网络->网络代理**，方式改为**自动**，`Configuration URL`改为`file:///root/.pac/ProxyAutoConfig.pac`（注意我用的是root用户，如果非root用户请将`/root`改为`/home/<your username>`）
4.  测试：打开浏览器，输入网址`www.google.com`看是否访问成功

2019-07-03 更新：该方法存在的问题是如果你的 
PAC 文件失效了，可能需要重新下载 
PAC 文件，即重新执行第 2 步中的`genpac`步骤。

### 关于终端下的代理设置[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#关于终端下的代理设置)

#### 终端代理环境变量[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#终端代理环境变量)

如前文所述，通用代理只有两种：
HTTP 代理（使用 http 协议）和 
SOCKS 代理（使用 socks4/socks4a/socks5 协议）。即代理相关环境变量中，每个变量`=`后面的协议部分必需是`http/socks4/socks4a/socks5`之一（对于`curl`还支持`socks5h`）。如下所示则全将其设置为了`socks5`：

```bash
# Set Proxy
function sp(){
    export all_proxy=socks5://127.0.0.1:1080/
    export ALL_PROXY=socks5://127.0.0.1:1080/ #有的命令行工具使用大写的变量名，如 curl
    export http_proxy=socks5://127.0.0.1:1080/ #有的命令行工具使用小写的变量名，如 curl、wget
    export ftp_proxy=socks5://127.0.0.1:1080/ #有的命令行工具使用小写的变量名，如 wget
    export FTP_PROXY=socks5://127.0.0.1:1080/ #有的命令行工具使用大写的变量名，如 curl
    export https_proxy=socks5://127.0.0.1:1080/ #有的命令行工具使用小写的变量名，如 wget
    export HTTPS_PROXY=socks5://127.0.0.1:1080/ #有的命令行工具使用大写的变量名，如 curl
    export no_proxy=localhost,127.0.0.1,192.168.0.0 #有的命令行工具使用小写的变量名，如 wget
    export NO_PROXY=localhost,127.0.0.1,192.168.0.0 #有的命令行工具使用大写的变量名，如 curl
}

# Unset Proxy
function up() {
    unset all_proxy ALL_PROXY http_proxy ftp_proxy FTP_PROXY https_proxy HTTPS_PROXY no_proxy NO_PROXY
}
```

其中的`http_proxy`表示访问`http`协议站点使用的代理，而不是使用`http`代理访问`http`协议站点。同理`ftp_proxy`表示访问`ftp`站点时使用的代理

#### 使用程序的代理相关参数[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#使用程序的代理相关参数)

1.  `git`：已知（亲测）支持`socks5`、`http`这两种代理方式，支持上述的终端代理环境变量。也可单独设置代理以覆盖全局设置：

    ```bash
    # 设置`socks5`代理
    git config --global http.proxy 'socks5://127.0.0.1:1080'
    git config --global https.proxy 'socks5://127.0.0.1:1080'
    # 设置`http`代理
    git config --global https.proxy http://127.0.0.1:1080
    git config --global https.proxy https://127.0.0.1:1080
    # 取消代理
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    ```

    对应的`.gitconfig`配置文件内容如下：

    ```text
    [http]
        proxy = socks5://127.0.0.1:1080
    [https]
        proxy = socks5://127.0.0.1:1080
    ```

2.  `curl`：支持`socks4`、`socks4a`、`socks5`、`http`这几种代理方式，支持上述的终端代理环境变量。也可单独设置代理以覆盖全局设置：

    ```
    curl -i4 -m3 -x socks5://192.168.56.11:1080 https://www.google.com
    curl -i4 -m3 -x socks5h://192.168.56.11:1080 https://www.google.com
    ```

    注意`socks5`和`socks5h`的区别，前者解析域名时不使用代理，后者解析域名时要使用代理，由于国内 
    DNS 可能被污染，故建议使用`socks5h`。详情参见`man curl`：

    > –socks5-hostname <host[:port]>
    >
    > Use the specified SOCKS5 proxy (and let the proxy resolve the host name). If the port number is not specified, it is assumed at port 1080. (Added in 7.18.0)
    >
    > –socks5 <host[:port]>
    >
    > Use the specified SOCKS5 proxy - but resolve the host name locally. If the port number is not specified, it is assumed at port 1080.

3.  `wget`: 似乎只支持`http`协议代理，支持上述的终端代理环境变量。不可单独设置代理以覆盖全局变量

## 通过已经可以科学上网的电脑实现科学上网[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#通过已经可以科学上网的电脑实现科学上网)

也就是说，如果你有一台设备通过上述的方法之一实现了科学上网，那么你就可以借助那台设备轻松地让其它和那台设备**属于同一局域网的设备**实现科学上网。比如你的实体机（如 Windows）实现了科学上网，那么对于你的 kali 虚拟机你就没必要想尽各种办法让它与你的实体机进行类似的配置以实现科学上网。具体方法如下：

前提条件：和可以科学上网的主机处于**同一局域网**

实验环境：主机 Windows10 （已实现科学上网），虚拟机 Kali Linux（需要实现科学上网），对于虚拟机 Kali，我使用了两个网卡，**网络地址转换**和**仅主机网络**，前者保证能连上 Internet，后者保证让 主机和虚拟机处于同一局域网（网段为 192.168.56.0/24）

实现步骤（以 
SSR 为例）：

1.  配置主机的 

    SSR 客户端，使其**允许来自局域网的连接**。于我而言，我是这么设置的：**右键小飞机->选项设置->勾选来自局域网的连接**

2.  在虚拟机中，配置 FireFox 浏览器中的网络代理或系统代理，选择手动代理，在所有代理中填入主机的 

    IP 地址和其默认的端口（我的是`192.168.56.100`和`1080`）

3.  完成

## 链接[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#链接)

下面总结了本文中使用的所有链接：



* [CentOS 7 配置 shadowsocks-libev 服务器端进行科学上网 | 鸣沙山侧 月牙泉畔](https://roxhaiy.wordpress.com/2017/08/04/430/)
* [Polipo - Wikipedia](https://en.wikipedia.org/wiki/Polipo)
* [Shadowsocks - Implementations](https://shadowsocks.org/en/spec/Implementations.html)
* [breakwa11/gfw_whitelist: gfw_whitelist](https://github.com/breakwa11/gfw_whitelist)
* [bwg](http://wsxq12.55555.io/Kali-Linux科学上网/bwg主机信息界面.png)
* [dns2socks](https://sourceforge.net/projects/dns2socks/)
* [overture](https://github.com/shawn1m/overture)
* [shadowsocks-qt5](https://github.com/shadowsocks/shadowsocks-qt5)
* [ss-qt5](http://wsxq12.55555.io/Kali-Linux科学上网/ss-qt5主界面.png)
* [tsocks 下载链接](https://sourceforge.net/projects/tsocks/files/tsocks/)
* [tsocks 官网](http://tsocks.sourceforge.net/)
* [tsocks 手册](https://linux.die.net/man/8/tsocks)
* [代理自动配置 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/代理自动配置)
* [科学上网](https://wsxq2.55555.io/blog/2019/07/07/科学上网)
* [科学上网的一些原理 | 横云断岭的专栏](http://hengyunabc.github.io/something-about-science-surf-the-internet/)
* [请问在设置http/https代理后DNS的解析还是通过proxy吗?](https://github.com/FelisCatus/SwitchyOmega/issues/963#issuecomment-270055221)



## 缩略语[](https://wsxq2.55555.io/blog/2018/10/20/Kali-Linux科学上网/#缩略语)


* **ARM**: Advanced RISC Machines
* **CPU**: Central Processing Unit
* **CST**: China Standard Time
* **DNS**: Domain Name System
* **FTP**: File Transfer Protocol
* **GFW**: Great Firewall
* **HTTP**: Hypertext Transfer Protocol
* **HTTPS**: HTTP Secure
* **IP**: Internet Protocol
* **JSON**: JavaScript Object Notation
* **KB**: Kilobyte
* **MB**: Megabyte
* **MIPS**: Microprocessor without Interlocked Pipeline Stages
* **OS**: Operating System
* **PAC**: Proxy auto-config
* **PC**: Personal Computer
* **PID**: Process ID
* **POSIX**: Portable Operating System Interface, formerly IEEE-IX
* **SOCKS**: SOCKetS
* **SS**: shadowsocks
* **SSL**: Secure Socket Layer
* **SSR**: shadowsocksr
* **TCP**: Transmission Control Protocol
* **UDP**: User Datagram Protocol
* **URL**: Uniform Resource Locator
* **VPS**: Virtual Processing System
* **WPAD**: Web Proxy Autodiscovery Protocol
