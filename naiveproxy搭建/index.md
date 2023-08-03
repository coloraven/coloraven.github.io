# NaiveProxy搭建

一键脚本地址：
https://github.com/imajeason/nas_tools/blob/main/NaiveProxy/install.sh
防走失备份如下：
```bash
#!/bin/bash

red='\e[91m'
green='\e[92m'
yellow='\e[93m'
magenta='\e[95m'
cyan='\e[96m'
none='\e[0m'
_red() { echo -e ${red}$*${none}; }
_green() { echo -e ${green}$*${none}; }
_yellow() { echo -e ${yellow}$*${none}; }
_magenta() { echo -e ${magenta}$*${none}; }
_cyan() { echo -e ${cyan}$*${none}; }

# Root
[[ $(id -u) != 0 ]] && echo -e "\n 哎呀……请使用 ${red}root ${none}用户运行 ${yellow}~(^_^) ${none}\n" && exit 1

cmd="apt-get"

sys_bit=$(uname -m)

case $sys_bit in
# i[36]86)
#     v2ray_bit="32"
#     caddy_arch="386"
#     ;;
'amd64' | x86_64)
    v2ray_bit="64"
    caddy_arch="amd64"
    ;;
# *armv6*)
#     v2ray_bit="arm32-v6"
#     caddy_arch="arm6"
#     ;;
# *armv7*)
#     v2ray_bit="arm32-v7a"
#     caddy_arch="arm7"
#     ;;
*aarch64* | *armv8*)
    v2ray_bit="arm64-v8a"
    caddy_arch="arm64"
    ;;
*)
    echo -e " 
    哈哈……这个 ${red}辣鸡脚本${none} 不支持你的系统。 ${yellow}(-_-) ${none}

    备注: 仅支持 Ubuntu 16+ / Debian 8+ / CentOS 7+ 系统
    " && exit 1
    ;;
esac

# 笨笨的检测方法
if [[ $(command -v apt-get) || $(command -v yum) ]] && [[ $(command -v systemctl) ]]; then

    if [[ $(command -v yum) ]]; then

        cmd="yum"

    fi
    if [[ $(command -v apt-get) ]]; then

        apt-get update -y
        apt-get install curl -y

    fi

else

    echo -e " 
    哈哈……这个 ${red}辣鸡脚本${none} 不支持你的系统。 ${yellow}(-_-) ${none}

    备注: 仅支持 Ubuntu 16+ / Debian 8+ / CentOS 7+ 系统
    " && exit 1

fi

uuid=$(cat /proc/sys/kernel/random/uuid)
systemd=true
# _test=true

_sys_timezone() {
    IS_OPENVZ=
    if hostnamectl status | grep -q openvz; then
        IS_OPENVZ=1
    fi

    echo
    timedatectl set-timezone Asia/Shanghai
    timedatectl set-ntp true
    echo "已将你的主机设置为Asia/Shanghai时区并通过systemd-timesyncd自动同步时间。"
    echo

    if [[ $IS_OPENVZ ]]; then
        echo
        echo -e "你的主机环境为 ${yellow}Openvz${none} ，建议使用${yellow}v2ray mkcp${none}系列协议。"
        echo -e "注意：${yellow}Openvz${none} 系统时间无法由虚拟机内程序控制同步。"
        echo -e "如果主机时间跟实际相差${yellow}超过90秒${none}，v2ray将无法正常通信，请发ticket联系vps主机商调整。"
    fi
}

_sys_time() {
    echo -e "\n主机时间：${yellow}"
    timedatectl status | sed -n '1p;4p'
    echo -e "${none}"
    [[ $IS_OPENV ]] && pause
}

naive_config() {

    echo

    while :; do
        echo -e "请输入 "$yellow"NaiveProxy"$none" 端口 ["$magenta"1-65535"$none"]，不能选择 "$magenta"80"$none"端口"
        read -p "$(echo -e "(默认端口: ${cyan}443$none):")" naive_port
        [ -z "$naive_port" ] && naive_port=443
        case $naive_port in
        80)
            echo
            echo " ...都说了不能选择 80 端口了咯....."
            error
            ;;
        [1-9] | [1-9][0-9] | [1-9][0-9][0-9] | [1-9][0-9][0-9][0-9] | [1-5][0-9][0-9][0-9][0-9] | 6[0-4][0-9][0-9][0-9] | 65[0-4][0-9][0-9] | 655[0-3][0-5])
            echo
            echo
            echo -e "$yellow naive_port 端口 = $cyan$naive_port$none"
            echo "----------------------------------------------------------------"
            echo
            break
            ;;
        *)
            error
            ;;
        esac
    done

    while :; do
        echo
        echo -e "请输入一个 ${magenta}正确的域名${none}，一定一定一定要正确，不！能！出！错！"
        read -p "(例如：n.abc.com): " domain
        [ -z "$domain" ] && error && continue
        echo
        echo
        echo -e "$yellow 你的域名 = $cyan$domain$none"
        echo "----------------------------------------------------------------"
        break
    done
    
    while :; do
        echo
        echo -e "请输入一个 ${magenta}邮箱${none}，邮箱不能乱输，格式要对。"
        read -p "(例如：name@abc.com): " email
        [ -z "$email" ] && error && continue
        echo
        echo
        echo -e "$yellow 你的邮箱 = $cyan$email$none"
        echo "----------------------------------------------------------------"
        break
    done
    get_ip
    echo
    echo
    echo -e "$yellow 请将 $magenta$domain$none $yellow 解析到: $cyan$ip$none"
    echo
    echo -e "$yellow 请将 $magenta$domain$none $yellow 解析到: $cyan$ip$none"
    echo
    echo -e "$yellow 请将 $magenta$domain$none $yellow 解析到: $cyan$ip$none"
    echo "----------------------------------------------------------------"
    echo

    while :; do

        read -p "$(echo -e "(是否已经正确解析: [${magenta}Y$none]):") " record
        if [[ -z "$record" ]]; then
            error
        else
            if [[ "$record" == [Yy] ]]; then
                domain_check
                echo
                echo
                echo -e "$yellow 域名解析 = ${cyan}我确定已经有解析了$none"
                echo "----------------------------------------------------------------"
                echo
                break
            else
                error
            fi
        fi

    done

}


install_info() {
    clear
    echo
    echo " ....准备安装了咯..看看有毛有配置正确了..."
    echo
    echo "---------- 安装信息 -------------"
    echo
    echo -e "$yellow NaiveProxy 端口 = $cyan$naive_port$none"
    echo
    echo -e "$yellow 你的域名 = $cyan$domain$none"
    echo
    echo -e "$yellow 域名解析 = ${cyan}我确定已经有解析了$none"
    echo
    echo -e "$yellow 自动配置 TLS = $cyan$install_caddy_info$none"

    echo
    echo "---------- END -------------"
    echo
    pause
    echo
}

domain_check() {
    # if [[ $cmd == "yum" ]]; then
    #     yum install bind-utils -y
    # else
    #     $cmd install dnsutils -y
    # fi
    # test_domain=$(dig $domain +short)
    # test_domain=$(ping $domain -c 1 -4 | grep -oE -m1 "([0-9]{1,3}\.){3}[0-9]{1,3}")
    # test_domain=$(wget -qO- --header='accept: application/dns-json' "https://cloudflare-dns.com/dns-query?name=$domain&type=A" | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" | head -1)
    test_domain=$(curl -sH 'accept: application/dns-json' "https://cloudflare-dns.com/dns-query?name=$domain&type=A" | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" | head -1)
    if [[ $test_domain != $ip ]]; then
        echo
        echo -e "$red 检测域名解析错误....$none"
        echo
        echo -e " 你的域名: $yellow$domain$none 未解析到: $cyan$ip$none"
        echo
        echo -e " 你的域名当前解析到: $cyan$test_domain$none"
        echo
        echo "备注...如果你的域名是使用 Cloudflare 解析的话..在 Status 那里点一下那图标..让它变灰"
        echo
        exit 1
    fi
}

install_go() {
    cd /opt
    rm /opt/go1.19.linux-amd64.tar.gz -rf
    wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
    tar -zxf go1.19.linux-amd64.tar.gz -C /usr/local/
    echo export GOROOT=/usr/local/go >> /etc/profile
    echo export PATH=$GOROOT/bin:$PATH >> /etc/profile
    source /etc/profile
    export GOROOT=/usr/local/go
    export PATH=$GOROOT/bin:$PATH
    go version
}

install_caddy() {
    # download caddy file then install
    mkdir /root/src && cd /root/src/
    go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest
    ~/go/bin/xcaddy build --with github.com/caddyserver/forwardproxy@caddy2=github.com/klzgrad/forwardproxy@naive
    cp caddy /usr/bin/
    /usr/bin/caddy version        # 2022-4-8 23:09
    #v2.4.6 h1:HGkGICFGvyrodcqOOclHKfvJC0qTU7vny/7FhYp9hNw=  
    setcap cap_net_bind_service=+ep /usr/bin/caddy  # 设置bind权限，可443
}


install_certbot() {
    if [[ $cmd == "apt-get" ]]; then
        $cmd install -y lrzsz git zip unzip curl wget qrencode libcap2-bin dbus tar 
        $cmd install -y certbot
    else
        # $cmd install -y lrzsz git zip unzip curl wget qrencode libcap iptables-services
        $cmd install -y lrzsz git zip unzip curl wget qrencode libcap epel-release tar openssl-devel ca-certificates
        $cmd install -y certbot
    fi

}


caddy_config() {
    password=$uuid

    cat > /etc/caddy/caddy_config.json << EOF
{
  "admin": {
    "disabled": true
  },
  "apps": {
    "http": {
      "servers": {
        "srv0": {
          "listen": [
            ":$naive_port"
          ],
          "routes": [
            {
              "handle": [
                {
                  "handler": "subroute",
                  "routes": [
                    {
                      "handle": [
                        {
                          "auth_user_deprecated": "User",
                          "auth_pass_deprecated": "$password",
                          "handler": "forward_proxy",
                          "hide_ip": true,
                          "hide_via": true,
                          "probe_resistance": {}
                        }
                      ]
                    },
                    {
                      "match": [
                        {
                          "host": [
                            "$domain"
                          ]
                        }
                      ],
                      "handle": [
                        {
                          "handler": "file_server",
                          "root": "/var/www/html",
                          "index_names": [
                            "index.html"
                          ]
                        }
                      ],
                      "terminal": true
                    }
                  ]
                }
              ]
            }
          ],
          "tls_connection_policies": [
            {
              "match": {
                "sni": [
                  "$domain"
                ]
              }
            }
          ],
          "automatic_https": {
            "disable": true
          }
        }
      }
    },
    "tls": {
      "certificates": {
        "load_files": [
          {
            "certificate": "/etc/letsencrypt/live/$domain/fullchain.pem",
            "key": "/etc/letsencrypt/live/$domain/privkey.pem"
          }
        ]
      }
    }
  }
}
EOF

cat > /etc/systemd/system/naive.service << EOF
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=root
Group=root
ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/caddy_config.json
ExecReload=/usr/bin/caddy reload --config /etc/caddy/caddy_config.json
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    do_service restart naive
    echo 
    echo "........... NaiveProxy 已启动  .........." 
    do_service enable naive
    echo 
    echo "........... NaiveProxy 设置自动启动完成 .........." 

    echo 
    echo "........... NaiveProxy 服务状态  .........." 

    do_service status naive --no-pager

}

config() {
    mkdir -p /etc/ssl/caddy
    # 存放Caddyfile的目录
    mkdir /etc/caddy/
    mkdir /var/www -p
    echo index > /var/www/html 
    # 生成密码
    # /etc/letsencrypt/live/x.dongvps.com/

    if [[ $(ls /etc/letsencrypt/live/ | pgrep "$domain") ]] ;then
        certbot renew
    else
        certbot certonly --standalone -d $domain --agree-to --email $email
    fi
    # 生成json

    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    _sys_timezone
    _sys_time

    

    
}


edit_port() {
    # 修改端口
    get_ip
    domain=`egrep 'domain' /etc/caddy/.autoconfig | awk -F'=' '{print $2}'`
    user=`egrep 'user' /etc/caddy/.autoconfig | awk -F'=' '{print $2}'`
    password=`egrep 'password' /etc/caddy/.autoconfig | awk -F'=' '{print $2}'`
    naive_port=`egrep 'port' /etc/caddy/.autoconfig | awk -F'=' '{print $2}'`
    email=`egrep 'email' /etc/caddy/.autoconfig | awk -F'=' '{print $2}'`

    
    while :; do
        echo -e "请输入 "$yellow"NaiveProxy"$none" 端口 ["$magenta"1-65535"$none"]，不能选择 "$magenta"80"$none"端口"
        read -p "$(echo -e "(默认端口: ${cyan}443$none):")" naive_port
        [ -z "$naive_port" ] && naive_port=443
        case $naive_port in
        80)
            echo
            echo " ...都说了不能选择 80 端口了咯....."
            error
            ;;
        [1-9] | [1-9][0-9] | [1-9][0-9][0-9] | [1-9][0-9][0-9][0-9] | [1-5][0-9][0-9][0-9][0-9] | 6[0-4][0-9][0-9][0-9] | 65[0-4][0-9][0-9] | 655[0-3][0-5])
            echo
            echo
            echo -e "$yellow naive_port 端口 = $cyan$naive_port$none"
            echo "----------------------------------------------------------------"
            echo
            break
            ;;
        *)
            error
            ;;
        esac
    done
    # 输入端口
    cat > /etc/caddy/caddy_config.json << EOF
{
  "admin": {
    "disabled": true
  },
  "apps": {
    "http": {
      "servers": {
        "srv0": {
          "listen": [
            ":$naive_port"
          ],
          "routes": [
            {
              "handle": [
                {
                  "handler": "subroute",
                  "routes": [
                    {
                      "handle": [
                        {
                          "auth_user_deprecated": "User",
                          "auth_pass_deprecated": "$password",
                          "handler": "forward_proxy",
                          "hide_ip": true,
                          "hide_via": true,
                          "probe_resistance": {}
                        }
                      ]
                    },
                    {
                      "match": [
                        {
                          "host": [
                            "$domain"
                          ]
                        }
                      ],
                      "handle": [
                        {
                          "handler": "file_server",
                          "root": "/var/www/html",
                          "index_names": [
                            "index.html"
                          ]
                        }
                      ],
                      "terminal": true
                    }
                  ]
                }
              ]
            }
          ],
          "tls_connection_policies": [
            {
              "match": {
                "sni": [
                  "$domain"
                ]
              }
            }
          ],
          "automatic_https": {
            "disable": true
          }
        }
      }
    },
    "tls": {
      "certificates": {
        "load_files": [
          {
            "certificate": "/etc/letsencrypt/live/$domain/fullchain.pem",
            "key": "/etc/letsencrypt/live/$domain/privkey.pem"
          }
        ]
      }
    }
  }
}
EOF
    do_service restart naive
    echo 
    echo "........... Naiveproxy 已重启  .........."
    
    do_service enable naive
    echo 
    echo "........... Naiveproxy 设置自动启动完成  .........."
    
    echo > /etc/caddy/.autoconfig
    echo -e "本机ip       =$ip" >> /etc/caddy/.autoconfig
    echo -e "域名domain   =$domain" >> /etc/caddy/.autoconfig
    echo -e "端口port     =$naive_port" >> /etc/caddy/.autoconfig
    echo -e "用户名user   =User" >> /etc/caddy/.autoconfig
    echo -e "密码password =$password" >> /etc/caddy/.autoconfig
    echo -e "邮箱email    =$email" >> /etc/caddy/.autoconfig

    echo 
    echo "........... NaiveProxy 服务状态  .........." 
    do_service status naive --no-pager

    cat /etc/caddy/.autoconfig


}


get_ip() {
    ip=$(curl -s https://ipinfo.io/ip)
    [[ -z $ip ]] && ip=$(curl -s https://api.ip.sb/ip)
    [[ -z $ip ]] && ip=$(curl -s https://api.ipify.org)
    [[ -z $ip ]] && ip=$(curl -s https://ip.seeip.org)
    [[ -z $ip ]] && ip=$(curl -s https://ifconfig.co/ip)
    [[ -z $ip ]] && ip=$(curl -s https://api.myip.com | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}")
    [[ -z $ip ]] && ip=$(curl -s icanhazip.com)
    [[ -z $ip ]] && ip=$(curl -s myip.ipip.net | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}")
    [[ -z $ip ]] && echo -e "\n$red 这垃圾小鸡扔了吧！$none\n" && exit
}

error() {

    echo -e "\n$red 输入错误！$none\n"

}

pause() {

    read -rsp "$(echo -e "按 $green Enter 回车键 $none 继续....或按 $red Ctrl + C $none 取消.")" -d $'\n'
    echo
}
do_service() {
    if [[ $systemd ]]; then
        systemctl $1 $2
    else
        service $2 $1
    fi
}
show_config_info() {
    clear
    # mkdir -p .local/share/caddy/config
    echo > /etc/caddy/.autoconfig
    echo -e "本机ip       =$ip" >> /etc/caddy/.autoconfig
    echo -e "域名domain   =$domain" >> /etc/caddy/.autoconfig
    echo -e "端口port     =$naive_port" >> /etc/caddy/.autoconfig
    echo -e "用户名user   =User" >> /etc/caddy/.autoconfig
    echo -e "密码password =$password" >> /etc/caddy/.autoconfig
    echo -e "邮箱email    =$email" >> /etc/caddy/.autoconfig
    echo
    echo "........... Naiveproxy 配置信息  .........."
    echo
    cat /etc/caddy/.autoconfig

}

install() {
    if [[ -f /usr/bin/caddy && -f /etc/caddy/caddy_config.json ]] ; then
        echo
        echo " 安装 NaiveProxy已存在..."
        echo
        echo -e "继续安装请输入1,退出请输入任意值"
        read -p "$(echo -e "请选择 [${magenta}1-2$none]:")" choose2
        case $choose2 in
        1)
            echo " 继续安装..."
            do_service stop naive
            ;;
        *)
            exit 1
            ;;
        esac
        
    fi
    # 安装依赖以及certbot命令
     
    
    # 配置代理信息，比如域名
    naive_config
    # blocked_hosts
    install_info
    # [[ $caddy ]] && domain_check
    install_certbot
    install_go
    if [[ $caddy || $v2ray_port == "443" ]]; then
        if [[ $cmd == "yum" ]]; then
            [[ $(pgrep "nginx") ]] && systemctl stop nginx
            [[ $(command -v nginx) ]] && yum remove nginx -y
            [[ $(pgrep "httpd") ]] && systemctl stop httpd
            [[ $(command -v httpd) ]] && yum remove httpd -y
        else
            [[ $(pgrep "apache2") ]] && service apache2 stop
            [[ $(command -v apache2) ]] && apt-get remove apache2* -y
        fi
    fi
    install_caddy

    ## bbr
    # _load bbr.sh
    # _try_enable_bbr


    config
    caddy_config


    get_ip
    add_cron
    allow_port
    show_config_info
    # do_service restart naive
}
uninstall() {

    if [[ -f /usr/bin/caddy && -f /etc/caddy/caddy_config.json ]]; then
        do_service disable naive
        do_service stop naive
        echo -e "
        $red 仅仅是停止服务了...$none
        " && exit 1
    fi

}

show_config() {
    echo
    echo "........... Naiveproxy 配置信息  .........."
    cat /etc/caddy/.autoconfig
}

add_cron() {
    echo 
    echo "........... 证书自动更新  .........."
    cat > /etc/caddy/.renew.sh << EOF
    
#!/usr/bin/env bash
systemctl stop naive
certbot renew
systemctl start naive
EOF
    chmod +x /etc/caddy/.renew.sh
    if [ `grep -c "caddy" /var/spool/cron/root` -lt '1' ];then
        echo "0 1 * * * /etc/caddy/.renew.sh" >> /var/spool/cron/root
    fi
    crontab -l
    # crontab -l > /tmp/conf && echo "0 1 * * * /etc/caddy/.renew.sh" >> /tmp/conf && crontab /tmp/conf && rm -f /tmp/conf
    echo 
    echo "........... 证书自动更新设置完成  .........."
    crontab -l
}

allow_port() {

    if [[ $(command -v yum) ]]; then

        firewall-cmd --zone=public --add-port=$naive_port/tcp --permanent
        firewall-cmd --zone=public --add-port=$naive_port/udp --permanent
        firewall-cmd --reload

    fi
    if [[ $(command -v apt-get) ]]; then

        iptables -I INPUT -p tcp --dport $naive_port -j ACCEPT
        iptables -I INPUT -p udp --dport $naive_port -j ACCEPT
        iptables-save

    fi
    echo 
    echo "........... 防火墙已开放端口$naive_port  .........."
}


while :; do
    echo
    echo "........... Naiveproxy 一键安装脚本 & 管理脚本  .........."
    echo
    echo
    echo " 1. 安装"
    echo
    echo " 2. 显示信息"
    echo
    echo " 3. 修改端口"
    echo
    echo " 4. 停止"
    echo
    if [[ $local_install ]]; then
        echo -e "$yellow 温馨提示.. 本地安装已启用 ..$none"
        echo
    fi
    read -p "$(echo -e "请选择 [${magenta}1-4$none]:")" choose
    case $choose in
    1)
        install
        break
        ;;
    2)
        show_config
        break
        ;;
    3)
        edit_port
        break
        ;;
    4)
        uninstall
        break
        ;;
    *)
        error
        ;;
    esac
done
```

一键安装
```bash
yum install -y wget&&wget https://raw.githubusercontent.com/imajeason/nas_tools/main/NaiveProxy/install.sh&&bash install.sh
```
已测试可用系统 `debian10`/`debian11`/`centos7`
关于3个月证书到期更新问题，我加了定时任务，但是不确定都能正常，如果证书到期需要手动执行 certbot renew然后systemctl restart naive重启服务即可。

## 2023年3月23日更新
naiveproxy一键脚本发布（无须编译caddy，支持多端口复用，自定义伪装网页），演示甲骨文纯IPV4（mack-a）+纯IPV6(X-UI)与naiveproxy共存方式的教程：https://ygkkk.blogspot.com/2022/11/naiveproxy-yg-youtube.html
https://gitlab.com/rwkgyg/naiveproxy-yg


https://github.com/klzgrad/naiveproxy/releases
https://github.com/v2fly/v2ray-core
https://github.com/Qv2ray/Qv2ray/releases
