# ESXI-打开端口


参考：https://blog.51cto.com/68240021/1970732
VMWare esxi中打开端口的实现

步骤1. 新增ESXi主机的firewall配置文件

在ESXi主机的/etc/vmware/firewall目录下增加name.xml的防火墙配置文件，内容格式如下：

```xml
<!-- FirewallRule for  yourname--> #yourname将会是在shell中显示的名称
<ConfigRoot>
    <service>
        <id>yourname</id>
        <rule id = '0000'>
            <direction>inbound</direction>
            <protocol>tcp</protocol>
            <porttype>dst</porttype>
            <port>
                <begin>1280</begin> #端口
                <end>1280</end> #端口
            </port>
        </rule>
        <enabled>true</enabled>
        <required>false</required>
    </service>
</ConfigRoot>
```

步骤2. 刷新防火墙规则

```bash
esxcli network firewall refresh
```

检查规则是否生效：

```bash
esxcli network firewall ruleset list | grep yourname
```

结果看到提示yourname ,状态true即开启，说明成功：

> yourname true
