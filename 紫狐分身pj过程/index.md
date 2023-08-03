# 紫狐分身PJ过程

<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/#code代码块 -->
<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/ -->
原始可用APK已备份

类名：
com.cloudinject.feature.App
```java
public void attachBaseContext(Context context) {
        try {
            StringBuilder sb = new StringBuilder();
            sb.append("JkmuyJoL");
            File file = new File(context.getFilesDir(), "decode");
            if (!file.mkdirs()) {
                sb.append(".");
            } else {
                file.delete();
            }
            if (f9216 == null || IV == null || key == null) {
                f9216 = new DESKeySpec(sb.toString().getBytes("UTF-8"));
                key = SecretKeyFactory.getInstance("DES").generateSecret(f9216);
                IV = new IvParameterSpec(sb.toString().getBytes("UTF-8"));
            }
        } catch (Exception unused) {
        }
        m11271(context);
        super.attachBaseContext(context);
    }
```
## 类名
## p011cd.C9813
```java
package p011cd;

import rxc.internal.operators.CryptoBox;

/* renamed from: cd.̗̙̖̗̙̗ */
public final class C9813 {
    public static String HOST = "http://360stat.org";

    /* renamed from: ̗̖̖̗ */
    public static String f34125 = null;

    /* renamed from: ̗̖̖̙ */
    public static String f34126 = null;

    /* renamed from: ̗̖̗̙ */
    public static String f34127 = null;

    /* renamed from: ̗̖̙̖ */
    public static String f34128 = "http://log-report.com/report";

    /* renamed from: ̗̖̙̗ */
    public static String f34129 = "https://storage.googleapis.com/ij-cloud/j.cap";

    /* renamed from: ̗̖̙̙ */
    public static String f34130 = "http://checksum.cc";

    /* renamed from: ̗̙̗̖ */
    public static String f34131 = "https://bellaluna4ala.s3.ap-east-1.amazonaws.com/j2.cap";

    /* renamed from: ̗̙̗̗ */
    public static String f34132 = "https://storage.googleapis.com/ij-cloud/f.cap1";

    /* renamed from: ̙̗̖ */
    public static String f34133 = "https://bellaluna4ala.s3.ap-east-1.amazonaws.com/f2.cap";

    public static void reload() {
        HOST = C9739.getHost();
        f34130 = C9739.m464();
        f34126 = HOST + CryptoBox.decrypt("D077E94E47201AC629F795C43B20AF1C");
        f34125 = HOST + CryptoBox.decrypt("D077E94E47201AC6ECAF95B536BDF70725E120A4E6663FB9");
        f34127 = f34130 + CryptoBox.decrypt("310A51B8EA767DD6");
    }
```

com.cloudinject.feature.App
```java
public void onCreate() {
    super.onCreate();
    f9214 = this;
    f34454 = this;
    C9761.m497(C9778.m533(C9809.decode(APP_ID.substring(0, 5), f34451)));
    C9805.m549().f500 = f9214.getSharedPreferences("eysFvaLOxnPc9vLZ", 0);
    Thread.setDefaultUncaughtExceptionHandler(new C9741());
    registerActivityLifecycleCallbacks(new C9746());
}
```

### 以上信息得知，请求URL路径的解密方式为
  加密方式：
  "DES/CBC/PKCS5Padding"
  密钥和偏移：
  "JkmuyJoL"
  字符编码：HEX
        
        f34126 = HOST + CryptoBox.decrypt("D077E94E47201AC629F795C43B20AF1C"); # 解密后为 /config
        f34125 = HOST + CryptoBox.decrypt("D077E94E47201AC6ECAF95B536BDF70725E120A4E6663FB9"); # 解密后为pack/verify
        f34127 = f34130 + CryptoBox.decrypt("310A51B8EA767DD6"); # 解密后为 v2?
通过在线解密工具http://des.online-domain-tools.com/能大概解密出来
```java
com.mob.tools.network.NetworkHelper
public String httpPostFiles(String str, ArrayList<KVPair<String>> arrayList, ArrayList<KVPair<String>> arrayList2, ArrayList<KVPair<String>> arrayList3, int i, NetworkTimeOut networkTimeOut) throws Throwable {
        final HashMap hashMap = new HashMap();
        httpPost(str, arrayList, arrayList2, arrayList3, i, new HttpResponseCallback() {
            /* class com.mob.tools.network.NetworkHelper.C39883 */

            @Override // com.mob.tools.network.HttpResponseCallback
            public void onResponse(HttpConnection httpConnection) throws Throwable {
                int responseCode = httpConnection.getResponseCode();
                if (responseCode == 200 || responseCode < 300) {
                    StringBuilder sb = new StringBuilder();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(httpConnection.getInputStream(), Charset.forName("utf-8")));
                    for (String readLine = bufferedReader.readLine(); readLine != null; readLine = bufferedReader.readLine()) {
                        if (sb.length() > 0) {
                            sb.append('\n');
                        }
                        sb.append(readLine);
                    }
                    bufferedReader.close();
                    hashMap.put("resp", sb.toString());
                    return;
                }
                StringBuilder sb2 = new StringBuilder();
                BufferedReader bufferedReader2 = new BufferedReader(new InputStreamReader(httpConnection.getErrorStream(), Charset.forName("utf-8")));
                for (String readLine2 = bufferedReader2.readLine(); readLine2 != null; readLine2 = bufferedReader2.readLine()) {
                    if (sb2.length() > 0) {
                        sb2.append('\n');
                    }
                    sb2.append(readLine2);
                }
                bufferedReader2.close();
                HashMap hashMap = new HashMap();
                hashMap.put(UContent.f16213N, sb2.toString());
                hashMap.put("status", Integer.valueOf(responseCode));
                throw new Throwable(new Hashon().fromHashMap(hashMap));
            }
        }, networkTimeOut);
        return (String) hashMap.get("resp");
    }
```

## 启动APP后，验证卡密时的请求：
### 请求方式：GET，
URL：http://360stat.org/feature/pack/verify?platform=2&secret=596bbb4570&app_id=bcc47d4f54f5ec3c0000ba22bb5590fe&version_code=4&app_version=1.3&device_code=befc2fe28fb837f7&api_version=1
### 响应头：
```
HTTP/1.1 200 OK
Server: openresty/1.13.6.2
Date: Thu, 16 Sep 2021 20:30:41 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 106
Connection: keep-alive
sign: 4bfdad943c93a58242246650f06fed54
eagleid: 2ca65aa0e01858fe1fcac57de6fe0b3b
resp: cf1096c3ecbbe53653679f37526bd773
```
### 响应体
```json
{"result":{"msg":"验证成功，卡密有效期至：2021-12-16 04:30:41"},"ts":1631824241729,"status":1}
```

## 定位时的返回
```json
{"message": "success", 
"code": 200, 
"data": "r52fVRuqRKZwpOlKry70HcCa3ExP+fVYgu4LaHDYX1+zoT8gsIN9kq/xDYCpXxgHO7Pzo0q4P9G60j2+xSmwzNfE14TpohR342SDqb3oexA/4foWowknL2EcV6l/xQcWW8G+dvcdaZOi4dE6zA5f8Vu9JWNUshiOJeBELoAPo/u7QkD2cI1xbjDj6gDEM60X0vqT/6+dRSPYu/pOWZVz4O8F9Zb2Fdiq/ZcCCF5au0CLPnjhN2g5Bcyu8/bpwDaG4mQ8VOo1cgjkkHNPmhWoCvhfKkNh6ZxVHZtSUas2Qf6szxngq0+hFrkAxGbU6vVuai5r8wQpj4UEbAsriVEZ9V3pqdah1YZIiIC6ucqWes6vYUY36aNIPoWybgHjyFfFSDTb6gxQrl+EbsAw/fkNTcrXW/BmX0mQJoqnLhVh0yqxHgNgnF+9re3AoruBR+eHaWSgg3ewHXCsxrqNXbPJuyVQSjyUs7OUQiFynuiIsCmxWyxNisZqktJe4/FfX2b/"
}
```

