# pipreqs使用踩坑

## 安装
```bash
pip install pipreqs
```
## 使用
```bash
pipreqs .
```
## `GBK`报错
加 `--encoding=utf8`参数
```bash
pipreqs . --encoding=utf8
```
## check_hostname requires server_hostname
这可能是因为使用代理造成的，不管怎么样，解决方法是降低urllib3版本：
```bash
pip install  urllib3==1.25.11
```
