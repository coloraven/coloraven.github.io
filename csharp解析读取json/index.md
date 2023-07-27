# CSharp解析读取JSON


https://blog.csdn.net/dslobo/article/details/108815969

## 要读取的json文件内容

```json
{
    "accepttime": 1600966807,
    "certificate": "",
    "completetext": "",
    "completetime": 1601010419,
    "createtime": 1600966807,
    "deleteflag": 0,
    "endtimestr": "12:00",
    "gid": 42,
    "netbarCameraList": [{
        "account": "admin",
        "address": "172.16.36.17",
        "cameraid": 21,
        "gid": 42,
        "name": "36",
        "password": "52358",
        "port": 554
    }],
    "netbarname": "36新亚网吧",
    "uniacid": 6,
    "userid": 66
}
```

## 使用到的关键库

```csharp
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
```

## 实现代码

```csharp
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Text;
using System.Windows.Forms;
 
namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
 
        private void button1_Click(object sender, EventArgs e)
        {
            // 读取外部json格式文件
            string text = File.ReadAllText(@"C:\Users\Administrator\Desktop\111.txt");
            byte[] mybyte = Encoding.UTF8.GetBytes(text);
            string aaa = Encoding.UTF8.GetString(mybyte);
            //Console.WriteLine(aaa); aaa为字符串类型
 
 
            //将JSON反序列化为.NET对象。
            JObject jo1 = (JObject)JsonConvert.DeserializeObject(aaa);
 
 
            //第一层
            string name = jo1["netbarname"].ToString();
            Console.WriteLine(name);
 
            string netbarCameraList = jo1["netbarCameraList"].ToString();
            Console.WriteLine(netbarCameraList);
 
 
            //第二层
            string account = jo1["netbarCameraList"][0]["account"].ToString();
            Console.WriteLine(account);
 
            string address = jo1["netbarCameraList"][0]["address"].ToString();
            Console.WriteLine(address);
 
        }
    }
}
```
