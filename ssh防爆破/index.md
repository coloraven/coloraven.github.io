# ssh防爆破


来源：https://github.com/FunctionClub/Fail2ban

## 原理

Fail2ban会通过检查日志来匹配错误信息，从而使用iptables来防止暴力破解。理论上只要是能够在服务器本地输出错误日志和访问日志的程序都可以使用Fail2ban来保驾护航。

## 脚本介绍

一键安装部署Fail2ban，自动配置防SSH爆破。可自定义ip封禁时间，最高重试次数。

## 安装

```bash
wget https://raw.githubusercontent.com/FunctionClub/Fail2ban/master/fail2ban.sh && bash fail2ban.sh 2>&1 | tee fail2ban.log
```

## 卸载

```bash
wget https://raw.githubusercontent.com/FunctionClub/Fail2ban/master/uninstall.sh && bash uninstall.sh
```

## 脚本运行截图

<img src="2699326682-162893297153527.png" />
