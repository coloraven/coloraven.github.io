# Aardio语言中进行网络请求

```java
import console;
import web.rest.jsonLiteClient;
import web.json;
var restClient = web.rest.jsonLiteClient();  

/*
web.rest客户端对象所以执行HTTP请求的函数遵守以下规则：
如果成功，则第一个返回值jsonData为服务端返回数据解码并创建的aardio对象。
在HTTP请求遇到错误时，第一个返回值jsonData为空，第二个返回值errMsg为错误信息,返回值errCode为错误代码
一般我们可以省略errMsg，errCode这两个返回值不用写，直接判断返回值是否为空即可。  
*/

restClient.addHeaders = {
    ["Test"] = "test"
} 

var jsonData,errMsg,errCode = restClient.post("http://eu.httpbin.org/post",{
    用户名 = "用户名";
    密码 = "密码";
} )


//jsonData非空为请求成功
if( jsonData ){
	console.log(jsonData["url"]); //提取返回字典中对应键的值
}
else {
    /*
    出错了，如果restClient.lastStatusCode非空则说明服务端返回了HTTP状态代码
    */
    if(  restClient.lastStatusCode ){
        console.log( restClient.lastStatusMessage() ) //查看该状态码的说明
        restClient.lastResponse() //输出服务端最后返回的信息
    }
    else {
        //这通常是没有成功发送请求，在请求到达服务器以前就出错了
        console.log("HTTP请求遇到错误,WinInet错误代码：",errCode )
        console.log("关于WinInet错误代码的详细说明：http://support.microsoft.com/kb/193625 ")
    }
   
}
console.pause(true);
```

## 带参数`GET`请求
```java
import web.rest.jsonLiteClient;
var http = web.rest.jsonLiteClient()

http.referer = "https://item.jd.com/"
var jdClub = http.api("https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv13283")

var data = jdClub.get(
    productId="100004253893"; // 商品编号
    sortType=6; // 5表示推荐排序,6为按时间排序
    isShadowSku=0; // 仅显示当前商品评论
    score=3; // 好评
    page=1; // 分页索引
    pageSize=10;
    fold=1;
    rid=0;
)
```
