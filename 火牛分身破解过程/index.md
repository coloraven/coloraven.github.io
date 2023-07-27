# 火牛（紫狐）分身破解过程

## 紫狐分身概述
打开APP需要`卡密验证`，绕过卡密验证只需要劫持改包即可，具体见：火牛-紫狐分身的字符串加密-卡密验证环节破解。
正常卡密验证返回包为：`{"result":{"msg":"验证成功，卡密有效期至：2030-11-13 00:22:24"},"ts":1634142164901,"status":1}`
分身时会验证卡密是否曾经注册过，注册过则可以正常使用，否则不能正常使用，重点是：即时卡密过期也能正常使用。
## 第一步：卡密破解
## 抓包（过程略）
打开APP，随便输入一个卡密（随便几位数字），抓包查看`请求`和`返回`数据。
#### 请求详情
卡密验证`API`为`http://jyfya.top/Auth/Verify`
#### 返回详情
返回数据为：
```json
{"code":404,""msg":"\u6ce8\u518c\u7801\u4e0d\u5b58\u5728","data":[]}
```
尝试将此处的`404`改为`200`，竟然成功。
### 破解
#### 1、绕过卡密验证过程
搜索"is_verify"
在`smali`码里找到第45行，将`const/4 v0,0x0`改为`const/4 v0,0x1`
![2021-09-20T103846](2021-09-20T103846.png){height="585px" width="270px"}
这样打开`APP`就不会再有提示输入卡密的界面。
但是.....因为正常情况下，输入卡密，服务器验证成功后，会将卡密本地保存，以待后续使用APP时调用，如此直接绕过卡密验证过程，本地的卡密信息为空，在调用时会出错，导致添加分身后，进入分身配置界面时提示`当前连接不到服务器，请稍后重试`。`APP`无法继续使用。
#### 2、去除`当前连接不到服务器，请稍后重试`弹窗
抓包发现跳这个弹窗前，APP发起了一个请求（http://hw.jyfya.top:8080/v4/now/?nonce=cloneuser&token=&appversioncode=312&virtual_id=91d7ea36fee5bd281fd2a088810e8d20），目的不明，该请求的状态码是`200`，按理说应该不会弹`当前连接不到服务器，请稍后重试`，毕竟该请求是通的，但是响应体是**空白**的，估计是因为这个才导致弹窗的，但是没有正版卡密的情况下，不知道其正常的响应体长怎么样。
##### 意外
在不停折腾过程中，某次偶然情况，我在`卡密`输入框里输入的中文，然后篡改卡密验证时的响应数据，结果在打开分身应用时竟然不再弹窗，再查看请求过程，发现响应体竟然有数据。
![2021-09-20T105940](2021-09-20T105940.png){height="585px" width="270px"}
至此，拿到了正常的响应体数据。
##### 暴力去弹窗（备用）
根据弹窗`当前连接不到服务器，请稍后重试`中的关键字，全局代码搜索无果，搜索`Arsc`资源得到ID`7f1100b3`，以该ID在全局代码中搜索发现弹窗的逻辑。
![2021-09-20T112200](2021-09-20T112200.png){height="585px" width="270px"}
在smali码中将该方法删掉~~，再验证，发现不再弹窗了。
#### 虚拟定位破解
经过第1、2步破解后，可以正常进入分身应用设置界面了。
但是又遇到新的问题：
![2021-09-20T110915](2021-09-20T110915.png "在`位置保护`里选点虚拟位置后点击右下角`选择`时报错"){height="585px" width="270px"}
![2021-09-20T111022](2021-09-20T111022.png "抓包发现点击右下角`选择`时，后台请求"){height="585px" width="270px"}
![2021-09-20T111104](2021-09-20T111104.png "返回数据"){height="585px" width="270px"}
明显是服务器报错了，估计是因为`token`（即卡密）为中文导致的，后来尝试换成数字卡密还是会报错`Null is not a valid element`。
##### 突破
意外情况曾经拿到了虚拟定位正常返回数据
```json
{"message":"success","code":200,"data":"qv36S6TQFKpL4tieu90GS58wzdnSVR8/Qwkmcta8G7J/3KEIJNjmSR/2TBm/suMc"}
```
`data`值为使用AES-ECB-PK5加密的数据，data值解开后为形如以下结构的`字符串`(注意为字符串)：
```json
[{"lat":28.294743,"lon":112.896041}]
```
+++success  抓包情况
;;;id3 请求信息
请求方式：GET
请求URL：http://hw.jyfya.top:8080/v4/dbcell/?lat=28.288195462671396&lon=112.9000414965204&n=10&mnc=1&range=2&gps=1&incoord=bd09&coord=bd09&nonce=cloneuser&token=6699666&appversioncode=312&virtual_id=91d7ea36fee5bd281fd2a088810e8d20
;;;
;;;id3 请求头
User-Token: e3158c8b9687b4ca317b813431987b6c
X-Mgs-Proxy-Signature: 53efd12b437a15b7e85d55441127ea8e
X-UT-DID: HUAWEI_TAS-AN00|YUgEKXp38YEDAH5sndk4SKff
X-CHANNEL: null
User-Agant: B0a9ReUQDyrrqIRVHAMmXMQBYKbLssglkMXKUlEMd0szCaG0tpuZJv+bskFyD6Uh9T3Y7qpyiYaCkf7pyDemg==
Host: hw.jyfya.top:8080
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.14.9
;;;
+++





+++ # 第二步：`登录`逆向
### 登录抓包情况
#### 请求详情
#### 返回详情
```json
{"message": "success", "code": 200, "data": "ZB5pocrTQ8oJg/iHuV8fAyO4ay7FfrpM/kDeD4lYZDjbEO4c/YAlio1WP8VkaWsDcpY0yF79RsDBf8/CKwNcNQionGuaPjKyan0NFe9vEYVrAMD0p4RX0m/qfqIdYK/fCwq0LrRFwe5wuLcv+YBFf+jUoCgOL0aQCWGtgRotMIgmEut7yOR340uXmYFKfO2s4jQY9yoPhP/t6+rLLAcINDvhILdYivbax7XKmZtQ1KtcEof3DC/kLwG4V6EurxgWV7it2XEryRiuUyrXKmxe3b2cG3EDxNoF8bZjEDZ+lET+rjaQ3ok0WY1yK5jrFIykdM7sGm7RN9cfRZk4sDRsGVR76HTz1dXuy58kLbozCLx4IAlZvl3gJIaNXZ1DjZg2j0vkQH7sKKO0ao8nZV6MPFFyChZdBOMvLbe+R1aQiWoBtlXcvOW+ug2B5ZfkmveG6u9zgk6qyEP5XEDYzzWfGSbh+L7p6zl0iBo4/Rfs/0WzqshBjv+W71Vi2lxQ3f4OLlBXVkodR5TtXRwwRCQB2mJAvqlFDpAhNcT76DQTdPMGdMjpxRpq29z02ipG5S0QAfn6rSjKTV1LWdoes1aEj1g2Rm8DEMUBX+Sm4syqe4A1ogd4DTABNSdgt+G4vrQ6Pxi7K6pFJf4JmPBaR3rwuigcNhkuUJlWekMl4oY0coVtn9yUIkIGwO9gJ5lrxSwniPASn10a5/KYDzmbEs/u4DKe8qp0yc962Op0rtjjDtp4PeEhSrC3iw2ORnZCsIC68hGPqwoUiJrice1m6KLTW5VKFZS2HhReSS7Jt52rMl4zayIwPBg3gh79Pi/0CXjkFvY53ctkzi0/evuqtiiBB9pibZB88KzUEVRzP/MlaYqUVJhrT5XIILTiLU1nkkqJeVuW3+Z2aWanydszY7pio7Esk9Qir4YHniLjfpOhCITCZeEbRzlAIvPbc3+6PRTp"}
```
#### 根据请求与返回情况，查找情况：
疑似登录逻辑代码所在类`z1.w22`，代码如下（找到以下代码走了很多弯路，花费很长时间，后来才发现，直接查找请求参数`cloneuser`可直接找到此处）：
```java mark:18
public static class d implements i30<ApiResult> {
    /* renamed from: b */
    public ApiResult a(j30 j30, Type type, h30 h30) throws n30 {
        if (!j30.A()) {
            return null;
        }
        m30 m30 = (m30) j30;
        int k = m30.K("code").k();
        String x = m30.P("message") ? m30.K("message").x() : "";
        ApiResult apiResult = new ApiResult();
        apiResult.setCode(k);
        apiResult.setMessage(x);
        Type type2 = ((ParameterizedType) type).getActualTypeArguments()[0];
        j30 K = m30.K("data");
        if (apiResult.isSuccessSign()) {
            String x2 = m30.K("data").x();
            f0.i().q(o.C0);
            String destrcode = AES.destrcode(x2, "a1ccb0d670efba1bc4353b1bc8ddf4f7");
            o30 o30 = new o30();
            if (destrcode != null) {
                apiResult.setData(h30.a(o30.c(destrcode), type2));
                apiResult.setCode(ApiResult.HTTP_OK);
                v.f(destrcode);
            } else {
                apiResult.setCode(ApiResult.HTTP_OK_SIGN_FAILE);
            }
        } else if (apiResult.isSuccess()) {
            apiResult.setData(h30.a(m30.K("data"), type2));
        } else if (K != null && (K.A() || K.y())) {
            apiResult.setData(h30.a(K, type2));
        }
        if (k == ApiResult.TOKEN_EXPIRE) {
            zh2.f().q(new h22());
        }
        return apiResult;
    }
}
```
跟踪上面高亮行中的`destrcode`方法得到：
```java
public static String destrcode(String str, String str2) {
        try {
            byte[] b = b(str);
            String str3 = "";
            for (byte b2 : b) {
                str3 = str3 + ((int) b2) + ",";
            }
            Cipher instance = Cipher.getInstance("AES/ECB/PKCS5Padding");
            instance.init(2, secretKeySpec(str2));
            return new String(instance.doFinal(b), "UTF-8");
        } catch (Exception e) {
            e.toString();
            return null;
        }
    }
```
使用`https://8gwifi.org/CipherFunctions.jsp`解密成功，如下图：
![2021-09-18T231840](2021-09-18T231840.png){height="585px" width="270px"}
```json
 {"radar_dl": "2019-01-01 00:00:00", "inchina": 1, "versioncode": "8", "tag": 0, "deadline": 1696246150000, "stonetime": 1586396889000, "googleversioncode": "-1", "points": 0, "viptype": 6, "username": "18276802235", "radar_viptype": 6, "inviteid": "GU5HB49X", "imsis": "", "virtual_id": "91d7ea36fee5bd281fd2a088810e8d20", "imeis": "58095A0D87FF688ACD1AFF7F90458AE0|Xiaomi_MI8SE,DF1E0D493251CEA30873A45A49D6CB53|HUAWEI_BKL-AL20 088E959F0FF35615BEC1DBF76CD6B107|Xiaomi_MINOTELTE", "invitenum": 1, "radar_userid": "None", "fatherid": "HDVDBGBD", "userid": "F68F66FC2B6F91C1FCE52A9AB531D07D|HUAWEI_BKL-AL20", "token": "e3158c8b9687b4ca317b813431987b6c", "vipphone": "", "channel": "zhuoyao", "starttime": 1568120195000}
```
+++

适用于本教程AES加密解密的python脚本，来源：https://www.cxyzjd.com/article/weixin_43755186/108254464
```python
import base64
from Crypto.Cipher import AES


class EncryptDate:
    def __init__(self, key):
        self.key = key.encode("utf-8")  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0 : -ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode("utf-8"))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


eg = EncryptDate("a1ccb0d670efba1bc4353b1bc8ddf4f7")  # 这里密钥的长度必须是16的倍数
text = '[{"lat": 20.36253, "lon": 127.840366}]'
res = eg.encrypt(text)
print(res)
print(eg.decrypt(res))
```

## 火牛-紫狐分身的字符串加密-卡密验证环节破解
字符串使用DES/CBC/PKCS5Padding模式进行了加密（[在线加解密地址](https://the-x.cn/en-us/cryptography/Des.aspx)），加密密钥和偏移量均为`JkmuyJoL`的`HEX`码"4a 6b 6d 75 79 4a 6f 4c"。
比如：`请输入卡密`，加密后的字符串变为：`4D4EB9A4E93156AD7D2FD9C80AC8ACBB`，
![2021-10-15T152703](2021-10-15T152703.png "加密过程截图"){height="585px" width="270px"}
故如要通过APP的字符串来搜索代码进行逆向，需要先将字符串按上述模式进行加密，获取对应`HEX`码，再进行搜索。
通过以上方式加密卡密验证请求参数`platorm`字符串，再用加密后字符串进行搜索，来到以下代码：
```java
public static String m540(String str, int i, Map<String, String> map) {
    Throwable th;
    Throwable th2;
    BufferedReader bufferedReader = null;
    if (i > f34070) {
        return null;
    }
    try {
        if (C9808.m553(map)) {
            map = new Hashtable();
        }
        map.put(CryptoBox.decrypt("01CEACFC0AF45D87"), App.APP_ID);//app_id
        map.put(CryptoBox.decrypt("9DDC6D94B5D5A82195F4039E4BCB96E9"), C9823.m570(App.getContext()));//device_code
        map.put(CryptoBox.decrypt("F933F932FC1BBCC4F641AA1302651920"), String.valueOf(App.f34457));//platform
        map.put(CryptoBox.decrypt("755D2E8EE7A5F9617BF0CDC6C3476784"), String.valueOf(App.f34458));//api_version
        map.put(CryptoBox.decrypt("F06BA0D8EBD24E7610D4F2CE7DB58654"), App.f34452); //app_version
        map.put(CryptoBox.decrypt("9752D144A1F714491ACBD84E2BFEDD05"), String.valueOf(App.f34456));//version_code
        HttpURLConnection httpURLConnection = (HttpURLConnection) new URL(str + CryptoBox.decrypt("9BECF8203DFEAF53") + m541(map)).openConnection();// ?
        httpURLConnection.setConnectTimeout(2000);
        httpURLConnection.setReadTimeout(2000);
        httpURLConnection.connect();
        BufferedReader bufferedReader2 = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream(), CryptoBox.decrypt("13169925E946FA96")));//utf-8
        try {
            StringBuilder sb = new StringBuilder();
            while (true) {
                String readLine = bufferedReader2.readLine();
                if (readLine == null) {
                    break;
                }
                sb.append(readLine);//字符串拼接
            }
            // 此处的C9804.m548的代码在下面贴出（通过可以阅读看出是求MD5的方法。即：eagleid算法为：拼接返回值的每一行，再拼接'1'后将字符串求MD5。
            if (!httpURLConnection.getHeaderField(CryptoBox.decrypt("D29A3C6F78CE2E83")).equals(C9804.m548(sb.toString().concat(CryptoBox.decrypt("19B19EF55618DC53"))))) {//前：eagleid ，后：1
                C9812.m559(bufferedReader2);
                return null;
            }
            String sb2 = sb.toString();
            C9812.m559(bufferedReader2);
            return sb2;
        } catch (Throwable th3) {
            th = th3;
            bufferedReader = bufferedReader2;
            C9812.m559(bufferedReader);
            throw th;
        }
    } catch (Throwable th4) {
        th2 = th4;
        m542(CryptoBox.decrypt("8E90A3E7E9C0E8EE9D221F6DC0BC9B82"), C9810.m557(App.getContext(), th2));//http error.
        Thread.sleep(100);
        String r8 = m540(str, i + 1, map);
        C9812.m559(bufferedReader);
        return r8;
    }
}
```

```java C9804.m548
package p011cd;

import java.io.PrintStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import rxc.internal.operators.CryptoBox;

/* renamed from: cd.̗̙̖̗̖̖ */
public class C9804 {

    /* renamed from: ̗ */
    protected static MessageDigest f497;

    /* renamed from: ̗ */
    protected static char[] f498 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

    static {
        f497 = null;
        try {
            f497 = MessageDigest.getInstance(CryptoBox.decrypt("019EDB52DF54D0CF"));//MD5
        } catch (NoSuchAlgorithmException e) {
            PrintStream printStream = System.err;
            printStream.println(C9804.class.getName() + CryptoBox.decrypt("1C63A63473AFCA62EB0ED209B599B1D195382B0F8E6F0CFFBB0D002A1603C36F8787230B9932B9F170BF114D256396D801FAD473922044F2"));//初始化失败，MessageDigest不支持MD5Util。
            e.printStackTrace();
        }
    }

    /* renamed from: ̗̖ */
    public static String m548(String str) {
        f497.update(str.getBytes());
        byte[] digest = f497.digest();
        int length = digest.length;
        StringBuffer stringBuffer = new StringBuffer(length * 2);
        int i = length + 0;
        for (int i2 = 0; i2 < i; i2++) {
            byte b = digest[i2];
            char[] cArr = f498;
            char c = cArr[(b & 240) >> 4];
            char c2 = cArr[b & 15];
            stringBuffer.append(c);
            stringBuffer.append(c2);
        }
        return stringBuffer.toString();
    }
}
```

## 分身过程逆向
经过分析，分身过程的请求参数key并未加密，但是参数值存在大量的
直接搜索`"appversioncode"`即可找出来:
```java 代码片段
private class C8579b implements ehh {
    private C8579b() {
    }

    @Override // p109z1.ehh
    /* renamed from: a */
    public ehp mo59189a(ehh.AbstractC8788a aVar) throws IOException {
        ehn a = aVar.mo59741a();
        ehn.C8795a f = a.mo59874f();
        if (a.mo59868a().toString().contains(PathConst.f18227e)) {
            f.mo59891b("User-Agent", dwc.m44271a().mo59261b(AppConst.f18045e)).mo59891b("User-Md5", duz.m43551r());
        } else if (a.mo59868a().toString().contains(PathConst.f18222a)) {
            String str = RetrofitHelper.m43305b() + "";
            String str2 = (dwj.m44508d() / 1000) + "";
            ehg.C8787a a2 = a.mo59868a().mo59708v().mo59714a("nonce", str).mo59714a(C9111lm.f32050f, str2).mo59714a("appversioncode", duz.m43543n() + "").mo59714a("signature", RetrofitHelper.this.m43304a(a, str, duz.m43547p().toLowerCase(), str2));
            if (UserManager.m43341a().mo59207b()) {
                a2.mo59714a("token", ShTool.mGetString(dwm.m44562a(), "token", dwc.m44271a().mo59261b(AppConst.f18009aE)));
                a2.mo59714a("virtual_id", UserManager.m43341a().mo59208c().getVirtualId());
                a2.mo59714a("ut_did", PhoneUtils.m44228e());
            }
            ehg c = a2.mo59723c();
            dvs.m44154a((Object) ("---------" + c.mo59679a().toString()));
            f.mo59887a(c);
        }
        return aVar.mo59742a(f.mo59896d());
    }
}
```
