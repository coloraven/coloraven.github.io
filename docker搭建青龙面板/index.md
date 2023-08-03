# Docker搭建青龙面板

```bash
docker run -dit \
  -v /userdatas/Sandisk/ql/config:/ql/config \
  -v /userdatas/Sandisk/ql/log:/ql/log \
  -v /userdatas/Sandisk/ql/db:/ql/db \
  -v /userdatas/Sandisk/ql/repo:/ql/repo \
  -v /userdatas/Sandisk/ql/raw:/ql/raw \
  -v /userdatas/Sandisk/ql/scripts:/ql/scripts \
  -v /userdatas/Sandisk/ql/jbot:/ql/jbot \
  -v /userdatas/Sandisk/ql/ninja:/ql/ninja \
  -p 5678:5700 \
  -p 6789:5701 \
  --name qinglong \
  --restart unless-stopped \
  whyour/qinglong:latest
```
