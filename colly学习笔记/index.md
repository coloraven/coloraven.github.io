# Colly学习笔记

## go语言爬虫框架Colly学习
https://darjun.github.io/2021/06/30/godailylib/colly/
以下代码是自己结合ChatGPT的回答与测试的结果。
```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"strings"
	"time"

	"github.com/gocolly/colly/v2"
	"github.com/gocolly/colly/v2/debug"
)

// 创建一个新的collector
var c = colly.NewCollector( // 启用异步请求
	colly.Async(true),
	colly.AllowURLRevisit(),
	// 附加调试器
	colly.Debugger(&debug.WebDebugger{}),
	// 下面是用法和区别
	// 1. LogDebugger
	// colly.Debugger(&debug.LogDebugger{})
	// 控制台输入日志形如：
	// [000068] 1 [    66 - responseHeaders] map["status":"OK" "url":"https://httpbin.org/post"] (744.2505ms)
	// [000067] 1 [     1 - responseHeaders] map["status":"OK" "url":"https://httpbin.org/cookies?param1=value1&param2=value2"] (744.2505ms)

	// 2. WebDebug,用网页展示请求状态，默认访问路径http://127.0.0.1:7676/
	// colly.Debugger(&debug.WebDebugger{}),
	// 结果形如：
	// Current Requests (1)#                                  Finished Requests (115)
	// https://httpbin.org/post                               https://httpbin.org/post
	// Collector #1 - 2023-04-12T08:00:01.0840252+08:00       Collector #1 - 64.4904635s
)

func init() {
	initialCookie := &http.Cookie{
		Name:   "initial_cookie",
		Value:  "initial_value",
		Domain: "httpbin.org",
	}

	// 创建一个新的cookiejar
	jar, _ := cookiejar.New(nil)
	hosturl, _ := url.Parse("https://httpbin.org")
	jar.SetCookies(hosturl, []*http.Cookie{initialCookie})

	// 创建一个自定义的http.Client，以使用设置好的cookiejar
	client := &http.Client{
		Jar: jar,
	}

	// 将自定义的http.Client设置为collector的客户端
	c.SetClient(client)

	// 使用OnRequest回调为所有请求设置初始headers
	initialHeaders := map[string]string{
		"User-Agent":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
		"Accept-Custom": "en-US,en;q=0.9",
	}

	// 设置代理
	err := c.SetProxy("http://127.0.0.1:8889")
	if err != nil {
		log.Fatal("设置代理失败:", err)
	}

	// 设置并发限制
	c.Limit(&colly.LimitRule{
		DomainGlob:  "*",
		Parallelism: 5, // 设置并发数
		RandomDelay: 5 * time.Second,
	})

	// 使用OnRequest回调处理请求
	c.OnRequest(func(r *colly.Request) {
		if r.Method == "GET" {
			fmt.Println("👉正准备发起GET请求，当前处于请求前中间件函数")
		} else if r.Method == "POST" {
			fmt.Println("👆正准备发起POST请求，当前处于请求前中间件函数")
		}

		// 设置初始headers
		for k, v := range initialHeaders {
			r.Headers.Set(k, v)
		}

		// 根据URL路径临时修改headers
		if strings.Contains(r.URL.Path, "headers") {
			r.Headers.Set("Custom-Header", "Custom-Value")
		}
	})

}
func main() {
	// 设置访问的URL
	urls := []string{"https://httpbin.org/cookies", "https://httpbin.org/html", "https://httpbin.org/headers"}

	// 某一个URL请求成功后，Colly将会自动调用该函数进行响应的处理，此处写响应处理逻辑。
	c.OnResponse(func(r *colly.Response) {
		// 根据请求URL路径，选择不同的处理方法，此处嵌套调用c.OnHTML
		url := r.Request.URL.String() // 请求的URL
		if strings.Contains(url, "https://httpbin.org/html") {
			c.OnHTML("body h1", func(e *colly.HTMLElement) {
				fmt.Println("Processing HTML response...", e.Text)
			})
		} else {
			// 在这里处理其他类型的响应
			fmt.Println("Processing non-HTML response...", string(r.Body))
		}
		// fmt.Println(time.Now().Format("2006-01-02 15:04:05"), "Finished Visited URL:", r.Request.URL, r.Request.Method)
		// if r.Request.Method == "POST" {
		// 	fmt.Println(r.Request.Body)
		// }
		// fmt.Println("Response body:", string(r.Body))
	})

	// 使用Visit方法开始抓取(Visit方法只能实现GET请求) 同时也是并发测试
	for _, baseURL := range urls {
		// 设置查询参数
		queryParams := url.Values{}
		queryParams.Add("param1", "value1")
		queryParams.Add("param2", "value2")

		// 将查询参数附加到基本URL
		requestURL := fmt.Sprintf("%s?%s", baseURL, queryParams.Encode())
		err := c.Visit(requestURL)
		if err != nil {
			fmt.Println("Visit error:", err)
		}
	}

	// POST请求  同时也是并发测试
	for i := 1; i < 10; i += 2 {
		postURL := "https://httpbin.org/post"
		postData := map[string]string{
			"param1": fmt.Sprintf("%d", i),
			"param2": "value2",
		}

		err := c.Post(postURL, postData)
		if err != nil {
			log.Println("POST request error:", err)
		}
	}
	// 等待所有请求完成——开启异步时需要该设置
	c.Wait()
}
```

输出结果（部分省略）
```bash
C:\Users\admin\Desktop\Colly学习>go run .
👉正准备发起GET请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👉正准备发起GET请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👆正准备发起POST请求，当前处于请求前中间件函数
👉正准备发起GET请求，当前处于请求前中间件函数
2023-04-11 23:02:46 Finished Visited URL: https://httpbin.org/post POST
2023-04-11 23:02:46 Finished Visited URL: https://httpbin.org/cookies?param1=value1&param2=value2 GET
2023-04-11 23:02:46 Finished Visited URL: https://httpbin.org/headers?param1=value1&param2=value2 GET
2023-04-11 23:02:47 Finished Visited URL: https://httpbin.org/post POST
2023-04-11 23:02:47 Finished Visited URL: https://httpbin.org/post POST
2023-04-11 23:02:47 Finished Visited URL: https://httpbin.org/cookies?param1=value1&param2=value2 GET
2023-04-11 23:02:47 Finished Visited URL: https://httpbin.org/cookies?param1=value1&param2=value2 GET
2023-04-11 23:02:47 Finished Visited URL: https://httpbin.org/cookies?param1=value1&param2=value2 GET
C:\Users\admin\Desktop\Colly学习>
```


## 自定义参数的传递
```go
package main

import (
	"fmt"
	"github.com/gocolly/colly/v2"
)

func main() {
	// 初始化collector
	c := colly.NewCollector()

	// 设置访问url
	url := "https://www.httpbin.org/headers"

	// 在请求之前处理
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())

		// 使用Context传递自定义参数
		r.Ctx.Put("customData", "Hello, I'm custom data!")
	})

	// 处理响应
	c.OnResponse(func(r *colly.Response) {
		// 从Context中获取自定义参数
		customData := r.Ctx.Get("customData")
		fmt.Printf("获取传递的自定义参数: %s\n", customData)
	})

	// 开始爬取
	err := c.Visit(url)
	if err != nil {
		fmt.Println("Error:", err)
	}
}
```

## 在Visit或Post方法中传递自定义参数给Onresponse方法
这种情形用于每个不同的请求，自定义参数给下一个环节的response处理。
```go
package main

import (
	"fmt"
	"github.com/gocolly/colly/v2"

)

func main() {
	// 初始化collector
	c := colly.NewCollector()

	// 设置访问url
	url := "https://www.example.com"

	// 在请求之前处理
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
	})

	// 处理响应
	c.OnResponse(func(r *colly.Response) {
		// 从Context中获取自定义参数
		customData := r.Ctx.Get("customData")
		fmt.Printf("Response received, customData: %s\n", customData)
	})

	// 创建一个新的Context
	ctx := colly.NewContext()
	ctx.Put("customData", "Hello, I'm custom data!")

	// 使用WithContext方法在访问时传入自定义Context
	err := c.Request("GET", url, nil, ctx, nil)  // 使用`Request`方法——（`Visit`和`Post`的底层实现）
	if err != nil {
		fmt.Println("Error:", err)
	}
}
```
> 不过,如果任务足够复杂或具有不同类型的子任务，建议对一个抓取作业使用多个`Collector`。比如一个解析列表视图并处理分页，另一个收集详细信息。
使用多个`Collector`的中文例子:https://darjun.github.io/2021/06/30/godailylib/colly/
官方例子：https://go-colly.org/docs/best_practices/multi_collector/

## 利用Context计算请求耗时
```go
package main

import (
	"fmt"
	"time"

	"github.com/gocolly/colly/v2"
)

func main() {
	// 初始化collector
	c := colly.NewCollector()

	// 设置访问url
	url := "https://www.163.com"

	// 在请求之前处理
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())

		// 记录请求开始时间
		startTime := time.Now()

		// 使用Context传递请求开始时间，将时间转换为字符串
		r.Ctx.Put("startTime", startTime.Format(time.RFC3339Nano))
	})

	// 处理响应
	c.OnResponse(func(r *colly.Response) {
		// 从Context中获取请求开始时间，将字符串转换为time.Time类型
		startTimeStr := r.Ctx.Get("startTime")
		startTime, err := time.Parse(time.RFC3339Nano, startTimeStr)
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		// 计算请求耗时
		duration := time.Since(startTime)
		fmt.Printf("Response received, duration: %v\n", duration)
	})

	// 开始爬取
	err := c.Visit(url)
	if err != nil {
		fmt.Println("Error:", err)
	}
}
```
