# CSharp网络请求


已测试成功的
使用到的库`using System.Net.Http;`

```csharp
static void Main(string[] args)
            {
            using var client = new HttpClient();
            client.BaseAddress = new Uri("http://restapi.amap.com");
            //client.DefaultRequestHeaders.Add("User-Agent", "C# console program");
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            var url = "/v3/geocode/geo?key=5d47448e3c3aceff5db10319829c5450&address=长沙市芙蓉区解放西路长沙市公安局&city=changsha";
            HttpResponseMessage response = await client.GetAsync(url);
            response.EnsureSuccessStatusCode();
            var resp = await response.Content.ReadAsStringAsync();
            //将json字符串解析为json对象
            JObject jobj = (JObject)JsonConvert.DeserializeObject(resp);  
            //访问json对象中的成员
            string name2 = jobj["geocodes"][0]["location"].ToString();    
            Console.WriteLine(name2);
            Console.ReadKey();
        }
```

异步：https://blog.csdn.net/zzulishulei/article/details/77751436


