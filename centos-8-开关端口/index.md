# CentOS 8 开关端口


[来源参考](https://blog.csdn.net/qq_32656561/article/details/105619911)

1. 查看防火墙某个端口是否开放
   ```bash
   firewall-cmd --query-port=3306/tcp
   ```
2. 开放防火墙端口3306
   ```bash
   firewall-cmd --zone=public --add-port=3306/tcp --permanent
   ```
   **注意：开放端口后要重启防火墙生效**
3. 重启防火墙
   ```bash
   systemctl restart firewalld
   ```
4. 关闭防火墙端口
   ```bash
   firewall-cmd --remove-port=3306/tcp --permanent
   ```
5. 查看防火墙状态
   ```bash
   systemctl status firewalld
   ```
6. 关闭防火墙
   ```bash
   systemctl stop firewalld
   ```
7. 打开防火墙
   ```bash
   systemctl start firewalld
   ```
8. 开放一段端口
   ```bash
   firewall-cmd --zone=public --add-port=40000-45000/tcp --permanent
   ```
9. 查看开放的端口列表
   ```bash
   firewall-cmd --zone=public --list-ports
   ```
10. 查看被监听Listen的端口
   ```bash
   netstat -lntp
   ```
11. 检查端口被哪个进程占用
   ```bash
   netstat -lnp|grep 3306
   ```

