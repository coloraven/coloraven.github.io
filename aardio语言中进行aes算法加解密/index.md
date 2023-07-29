# Aardio语言中进行AES算法加解密

```java 实际是aardio，借用java语言实现高亮
import console;  
import crypt.bin;
import crypt.aes;

//创建AES加密算法容器
var aes = crypt.aes();

//设置密钥(最大32个字节)
aes.setPassword("panda&beta#12345");

//设置模式
aes.setKeyParamMode(2/*_CRYPT_MODE_ECB*/);

var encrypt_str = "53zlG1UPM3fHdW4rbD8gEGf3MoOlgNFnypUvM9y2sKM=";

//BASE64编码加密结果
//console.log( crypt.bin.encodeBase64( str ) );

//AES加密字符——>BASE64字符
base64str = crypt.bin.decodeBase64(encrypt_str);

//BASE64字符——>普通字符
decrypt_str = aes.decrypt(base64str);

console.log(decrypt_str);
console.pause(true);
```
