# 使用CSharp带参数调用外部EXE


### 1.**问题意义**

据说界面程序开发,首选C#(像lebview之类的也很好)
 但是,**能不能用其他语言开发核心代码,只用C#做界面?**毕竟每种语言都有自己擅长的领域.

### 2.exe程序

比如有个example.exe,能接受4个参数.用cmd的调用方法是



```bash
example.exe "1" "a" "2" "3"
```

### 3.C#调用方法



```csharp
// 调用exe的函数
using System.Diagnostics;

public bool StartProcess(string runFilePath, params string[] args)
{
        string s = "";
        foreach (string arg in args)
        {
            s = s + arg + " ";
        }
        s = s.Trim();
        Process process = new Process();//创建进程对象    
        ProcessStartInfo startInfo = new ProcessStartInfo(runFilePath, s); // 括号里是(程序名,参数)
        process.StartInfo = startInfo;
        process.Start();
        return true;
}

private void start_craw(object sender, EventArgs e)
{
    string exe_path = "E:/example.exe";  // 被调exe
    string[] the_args = { "1","2","3","4"};   // 被调exe接受的参数
    StartProcess(exe_path, the_args);
}
```

### 4.实战

<img src="https://upload-images.jianshu.io/upload_images/3132923-6f9f8d763243ce56.png?imageMogr2/auto-orient/strip|imageView2/2/w/598/format/webp" alt="界面设计" style="zoom:100%;" />





<img src="https:////upload-images.jianshu.io/upload_images/3132923-37e318b07b7b67f5.png?imageMogr2/auto-orient/strip|imageView2/2/w/915/format/webp" alt="代码" style="zoom:80%;" />





给按键添加点击事件,点击事件触发start_craw函数



<img src="https:////upload-images.jianshu.io/upload_images/3132923-415b9a266d54d37b.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp" alt="点击事件与函数关联" style="zoom:80%;" />



### 5.StartProcess更多的设置

```csharp
public bool StartProcess(string runFilePath, params string[] args)
{
        string s = "";
        foreach (string arg in args)
        {
            s = s + arg + " ";
        }
        s = s.Trim();
        Process process = new Process();//创建进程对象    
        ProcessStartInfo startInfo = new ProcessStartInfo(runFilePath, s); // 括号里是(程序名,参数)
        process.StartInfo = startInfo;
        //process.StartInfo.UseShellExecute = true;    //是否使用操作系统的shell启动
        //startInfo.RedirectStandardInput = true;      //接受来自调用程序的输入     
        //startInfo.RedirectStandardOutput = true;     //由调用程序获取输出信息
        //startInfo.CreateNoWindow = true;             //不显示调用程序的窗口 
        process.Start();
        return true;
}
```

### 6.疑难解答

调用外部exe时,当这个exe运行出错时,会闪退,无法看清错误原因
 **解决:**
 直接去调试这个被调用的exe即可.



作者：xigua1234
链接：https://www.jianshu.com/p/43aa64992706
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
