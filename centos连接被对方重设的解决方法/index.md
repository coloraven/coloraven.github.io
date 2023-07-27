# CentOS“连接被对方重设”的解决方法


curl: 56 Recv failure: 连接被对方重设
curl56 Recv failure: Connection reset by peer

```bash
systemctl disable firewalld  
systemctl stop firewalld  
```


