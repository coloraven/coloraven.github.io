# Python执行JS的几种方式

<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/#code代码块 -->
<!-- https://shoka.lostyu.me/computer-science/note/theme-shoka-doc/special/ -->

https://juejin.cn/post/7015603661225066532

### 1.PyExecJS
>经测试，比js2py快5倍多

安装依赖  
pip3 install PyExecJS  
使用方式  
add.js 文件

```python
function add(a,b){
    return a+b;
}
复制代码
```

py 文件去调用

```python
import execjs

with open('add.js', 'r', encoding='UTF-8') as f:
    js_code = f.read()
context = execjs.compile(js_code)
result = context.call("add", 2, 3) // 参数一为函数名，参数二和三为函数的参数
print(result)
复制代码
```

运行

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/258d2db7971b4530bc0b1e1ec373804c~tplv-k3u1fbpfcp-watermark.awebp)

### 2.js2py

安装依赖库  
pip3 install js2py

还是上面的 add.js 文件

python 调用

```python
import js2py
with open('add.js', 'r', encoding='UTF-8') as f:
    js_code = f.read()
context = js2py.EvalJs()
context.execute(js_code)
result = context.add("1", "2")
print(result)
复制代码
```

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f1563b7eb8ec4f10bfe8de5fdb94188d~tplv-k3u1fbpfcp-watermark.awebp)

### 3.Node.js

实际上是使用 Python 的 os.popen 执行 node 命令，执行 JS 脚本  
首先，确保本地已经安装了 Node.js 环境

对 js 代码添加打印

```python
function add(a,b){
    return Number(a)+Number(b);
}
console.log(add(process.argv[2], process.argv[3]));  // 运行脚本传进来的参数
复制代码
```

用 python 调用控制台方式去使用

```python
import os
nodejs = os.popen('node add.js '+'2'+' '+'3')
m = nodejs.read()
nodejs.close()
print(m)
复制代码
```

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d7a834b413bd4aa5a1dcb2e6b25ea441~tplv-k3u1fbpfcp-watermark.awebp)

或者使用另一种方式

```python
function add(a,b){
    return Number(a)+Number(b);
}
// console.log(add(process.argv[2], process.argv[3]));

//新增一个导出函数（node方式）
module.exports.init = function (arg1, arg2) {
    //调用函数，并返回
    console.log(add(arg1, arg2));
};
复制代码
```

```python
import os
cmd = 'node -e "require(\"%s\").init(%s,%s)"' % ('./add.js', 2, 3)
pipeline = os.popen(cmd)
result = pipeline.read()
print(result)
复制代码
```

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1495bcf259bf41c891ed752e180c2093~tplv-k3u1fbpfcp-watermark.awebp)

### 4.node 服务

用 node 做一个服务，提供 api

还是 add.js 文件

```python
function add(a,b){
    return Number(a)+Number(b);
}

module.exports =  {
    add: function (arg1, arg2) {
        return add(arg1, arg2);
    }
};
复制代码
```

新建 add_api.js

下载 express 和 body-parser 两个包

```python
var express = require('express')
var app = express()
var func = require('./add.js')  // 导入js模块，并命名为func
var bodyParser = require('body-parser');  // 导入请求体解析器
// 调整参数大小限制，否则会提示参数过大。
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// 设置路由
app.post('/add', function(req, res) {
    // 获取请求的真实IP
	var ip = req.headers['x-real-ip'] ? req.headers['x-real-ip'] : req.ip.replace(/::ffff:/, '');
	// 获取请求时间
	var time = new Date().toString().replace(/+0800.*/, '');
	// 打印请求时间、IP、方法、路由
	console.log('INFO:', time, ip, req.method, req.originalUrl, '200 OK!');
	// 获取POST请求的formdata
	let result = req.body;
	// let code = result.code;
    // let seed = result.seed;
    // let ts = result.ts;
    console.log("result: ", result);
	console.log("num1: ", result.num1);
	console.log("num2: ", result.num2);

	// 调用cook模块中的get_cookie方法，该方法需要提前module.exports导出
	var response = func.add(result.num1, result.num2);
	// 设置响应头，如果不设置，通过asyncio_requests请求的res.json()会报错，因为它是根据响应头解析json数据
	// 而requests可以直接使用res.json()解析，因为它是根据响应信息解析
	res.set('Content-Type', 'application/json')
	// 将JSON后的数据返回客户端
	res.send(JSON.stringify({"result": response}));
});

app.listen(8919, () => {
	console.log("开启服务，端口8919", new Date().toString().replace(/+0800.*/, ''))
})
复制代码
```

运行，用 python 写个 post 请求

```python
import requests
response = requests.post("http://127.0.0.1:8919/add", data={"num1": 2, "num2": 3})
print(response.text)
复制代码
```

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0645f19417e14c4c86f097c23621502e~tplv-k3u1fbpfcp-watermark.awebp)

### 5.实测代码
```python
import execjs,time,js2py
sstr = "76483603481904696764816450136512980"
with open('md5js.js','r') as f:# js脚本下载地址：http://sydwperson.hnsydwpx.cn/template/pc/ckplayer/md5.js
    js_code = f.read()

start = time.time()
js=execjs.compile(js_code)
result=js.call('md5',sstr)
print(result)
print(time.time()- start,end = '\n\n')
# c6652bbf3b665178f231fee20bfb7b99
# 0.023935794830322266

start = time.time()
context = js2py.EvalJs()
context.execute(js_code)
result = context.md5(sstr)
print(result)
print(time.time()- start)
# c6652bbf3b665178f231fee20bfb7b99
# 0.11571598052978516
```
