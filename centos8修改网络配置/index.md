# centos8修改网络配置


centos8已经发布了，下载了一个体验一下，新安装好的centos8默认网卡是没有启动的，安装好后需要先配置网络。在/etc/sysconfig/network-scripts目录下存放着网卡的配置文件，文件名称是ifcfg- 网卡名称。

一 修改配置文件

设置网络时首先打开配置文件，配置文件默认如下所示，如果使用dhcp自动获取ip，只需将ONBOOT=no修改为ONBOOT=yes即可。

## 网卡配置文件按默认配置
```bash
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=e4987998-a4ce-4cef-96f5-a3106a97f5bf
DEVICE=ens33
ONBOOT=no  #如果使用dhcp分配ip的话，只需要将这里no改为yes，然后重启网络服务就行
```


如果需要配置静态ip，则按照以下修改方法修改

```bash
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static   #将dhcp修改为stati表示使用静态ip
DEFROUTE=yes
IPADDR=192.168.128.129   #设置IP地址
NETMASK=255.255.255.0    #设置子网掩码
GATEWAY=192.168.128.1    #设置网关
DNS1=114.114.114.114     #设置dns
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=e4987998-a4ce-4cef-96f5-a3106a97f5bf
DEVICE=ens33
ONBOOT=yes  #将no改为yes
```


二 重启网络服务

使用nmcli c reload命令重启网络服务，网络这块算是centos8改动较大的一块了，nmcli命令的参数如下所示：

```bash
[hk@localhost network-scripts]$ nmcli  -h
Usage: nmcli [OPTIONS] OBJECT { COMMAND | help }

OPTIONS
  -o[verview]                                    overview mode (hide default values)
  -t[erse]                                       terse output
  -p[retty]                                      pretty output
  -m[ode] tabular|multiline                      output mode
  -c[olors] auto|yes|no                          whether to use colors in output
  -f[ields] <field1,field2,...>|all|common       specify fields to output
  -g[et-values] <field1,field2,...>|all|common   shortcut for -m tabular -t -f
  -e[scape] yes|no                               escape columns separators in values
  -a[sk]                                         ask for missing parameters
  -s[how-secrets]                                allow displaying passwords
  -w[ait] <seconds>                              set timeout waiting for finishing operations
  -v[ersion]                                     show program version
  -h[elp]                                        print this help

OBJECT
  g[eneral]       NetworkManager's general status and operations
  n[etworking]    overall networking control
  r[adio]         NetworkManager radio switches
  c[onnection]    NetworkManager's connections  # 网络管理一般使用 nmcli c
  d[evice]        devices managed by NetworkManager
  a[gent]         NetworkManager secret agent or polkit agent
  m[onitor]       monitor NetworkManager changes

[hk@localhost network-scripts]$ 
```


网络管理一般使用 nmcli c，用法如下：

```bash
[hk@localhost network-scripts]$ nmcli c -h
Usage: nmcli connection { COMMAND | help }

COMMAND := { show | up | down | add | modify | clone | edit | delete | monitor | reload | load | import | export }

  show [--active] [--order <order spec>]
  show [--active] [id | uuid | path | apath] <ID> ...

  up [[id | uuid | path] <ID>] [ifname <ifname>] [ap <BSSID>] [passwd-file <file with passwords>]

  down [id | uuid | path | apath] <ID> ...

  add COMMON_OPTIONS TYPE_SPECIFIC_OPTIONS SLAVE_OPTIONS IP_OPTIONS [-- ([+|-]<setting>.<property> <value>)+]

  modify [--temporary] [id | uuid | path] <ID> ([+|-]<setting>.<property> <value>)+

  clone [--temporary] [id | uuid | path ] <ID> <new name>

  edit [id | uuid | path] <ID>
  edit [type <new_con_type>] [con-name <new_con_name>]

  delete [id | uuid | path] <ID>

  monitor [id | uuid | path] <ID> ...

  reload

  load <filename> [ <filename>... ]

  import [--temporary] type <type> file <file to import>

  export [id | uuid | path] <ID> [<output file>]

[hk@localhost network-scripts]$ 
```


