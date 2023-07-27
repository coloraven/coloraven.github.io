# Python中AES加解密

使用模块：`PyCryptodome`
+++success  实现代码
;;;id3 样例一
以下代码最后测试于2021年9月20日(`AES/ECB/PKCS5Padding`模式测试通过)
来源：https://www.cxyzjd.com/article/weixin_43755186/108254464
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
;;;
;;;id3 样例二
以下代码测试于2020年
```python
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES #pycryptodome库
import base64
import json
class AESCipher:
    """
    Tested under Python 3.x and PyCrypto 2.6.1.
    """

    def __init__(self, key='FfCcu4q6/x2z3XOO'):
        #加密需要的key值
        self.key=key.encode("utf-8")###
        self.BLOCK_SIZE = 256#16  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                        chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    def encrypt(self, raw):
        raw = self.pad(raw)
        #通过key值，使用ECB模式进行加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        #返回得到加密后的字符串进行解码然后进行64位的编码
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    def decrypt(self, enc):
        enc=enc.encode("utf-8")###
        #首先对已经加密的字符串进行解码
        enc = b64decode(enc)
        #通过key值，使用ECB模式进行解密
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_text = self.unpad(cipher.decrypt(enc)).decode('utf8')
        decrypted_text = decrypted_text.replace('\/','/')#网址正常化
        decrypted_text = decrypted_text.encode('utf8').decode('unicode_escape')#unicode字符转中文
        return decrypted_text


if __name__ == "__main__":
    key= ''
    crypted_data=''
    #调用解密函数
    decrypted_text = AESCipher(key).decrypt(crypted_data)
    # decrypted_text =decrypted_text.encode('utf8').decode('unicode_escape') # unicode字符转中文
    print(decrypted_text)
```
;;;
+++





