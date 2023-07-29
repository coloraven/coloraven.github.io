# 青龙面板京东签到

## 脚本备份
```
【10.2】https://www.juan920.com/1125.html 	ql repo https://github.com/smiek2221/scripts.git "jd_|gua_" "" "ZooFaker_Necklace.js|JDJRValidator_Pure.js|sign_graphics_validate.js"	0 0 * * *	

【混沌】 	ql repo https://github.com/whyour/hundun.git "quanx" "tokens|caiyun|didi|donate|fold|Env"	0 0 * * *	

【ddo（hyzaw）】 	ql repo https://ghproxy.com/https://github.com/shufflewzc/hyzaw.git "ddo_"	0 0 * * *	

【star】 	ql repo https://github.com/star261/jd.git "scripts" "code"	0 0 * * *	

【curtinlv仓库】 	ql repo https://github.com/curtinlv/JD-Script.git	0 0 * * *	

【Faker集合仓库】 	ql repo https://ghproxy.com/https://github.com/shufflewzc/faker2.git "jd_|jx_|getJDCookie" "activity|backUp" "^jd[^_]|USER|ZooFaker_Necklace"	0 0 * * *	

扫码获取京东cookie 	task Annyoo2021_scripts_main_getJDCookie.js	38 15 * * *	

拉取脚本 	ql repo https://github.com/smiek2221/scripts.git "jd_|gua_" "" "ZooFaker_Necklace.js|JDJRValidator_Pure.js|sign_graphics_validate.js"	0 0 * * *

【怨念集合仓库】 	ql repo https://github.com/yuannian1112/jd_scripts.git "jd_|jx_|getJDCookie" "activity|backUp" "^jd[^_]|USER|utils"	0 0 * * *

更新面板 	ql update	50 0 * * *	

删除日志 	ql rmlog 7	30 7 */7 * *	
```
## 变量名称
京东Cookies环境变量名称：`JD_COOKIE`

青龙面板容器启动指令：
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
