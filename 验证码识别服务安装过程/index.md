# 验证码识别服务安装过程


1、按官方步骤安装muggle-ocr

```bash
python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com muggle-ocr
```

2、安装相应依赖库

```bash
apt update && apt install libgl1-mesa-glx
```

3、降低tf版本

```bash
pip install --upgrade tensor
```


