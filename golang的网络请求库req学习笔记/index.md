# Golang的网络请求库req学习笔记

```go
package main

import (
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/imroc/req/v3" // 国人开发的强大网络请求库，有中文文档https://req.cool/zh/docs/prologue/introduction/
)
var (
	errMsg ErrorMessage
	client = req.C().
		// 在每个请求的请求级别启用转储，仅
		// 暂时将转储内容存储在内存中，因此我们可以调用
		// desp.dump（）在需要时获取转储内容中间件。
		// EnableDumpEachRequest().
		OnAfterResponse(func(client *req.Client, resp *req.Response) error { // 响应中间件
			if resp.Err != nil { //当存在基本错误时忽略，例如网络错误。
				return nil
			}
			// 将非成功响应视为错误，将原始转储内容记录在错误消息中。
			if !resp.IsSuccessState() { // 状态代码不在200到299之间。
				resp.Err = fmt.Errorf("bad response, raw content:\n%s", resp.Dump())
			}
			return nil
		}). // 请求客户端统一设置参数
		SetTimeout(60 * time.Second).
		SetCommonHeaders(map[string]string{
			"host":             "12.15.5.172",
			"proxy-connection": "keep-alive",
			"content-length":   "105",
			"accept":           "application/json, text/javascript, */*; q=0.01",
			"origin":           "https://httpbin.org",
			"x-requested-with": "XMLHttpRequest",
			"user-agent":       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
			"content-type":     "application/x-www-form-urlencoded; charset=UTF-8",
			"referer":          "https://httpbin.org",
			"accept-encoding":  "gzip, deflate",
			"accept-language":  "zh-CN,zh;q=0.9",
		})
)

func main(){
    // 默认开启自动解码，关闭自动解码如下
	// client.DisableAutoDecode()
	// 设置代理
    client.SetProxyURL("http://127.0.0.1:8889")

    // 启用调试
    client.EnableDebugLog()

    // 设置cookies
	cookieStr := fmt.Sprintf("cf_clearance=5v3CUcJ7MVgRn8u.Z1Gbiyso0; __Host-next-auth.csrf-token=88a2e1e11900d8fbb60c7a4aeb011a|830f6605; __Secure-next-auth.callback-url=https://chat.openai.com; _cfuvid=gXYxKWDPuZr_24800000; intercom-device-id-dgkjq2bp=b88f30WQ; _puid=user-FFb339PNbfoDI6RYvkzqkkbM:1680876948-=; __cf_bm=1IIT8Cdx=%s; intercom-session-dgkjq2bp=MWhSUGtrM3d0Rmp", jwt)
	BatSetCookies(cookieStr, client)
    
    // POST请求
    onMissionPostData := map[string]string{
		"caseTypeVal":  "allType",
		"caseName":     "",
		"startTime":    "missionStart",
		"endTime":      "missionEnd",
		"checkAllFlag": "0",
		"status":       "0",
		"caseStatus":   "",
	}

    resp, err := client.R().
		EnableForceMultipart().
        // 请求级别临时设置请求头，一次设置多个标题
		SetHeaders(map[string]string{ 
			"my-custom-header": "My Custom Value",
			"user":             "imroc",
		}).
		SetFormData(onMissionPostData).
		Post(url)
	if err != nil {
		log.Fatal(err)
	}
    fmt.Println(resp.String())

    // GET请求
    queryparam := "abc"
	url := "https://httpbin.org/get"
	headers := map[string]string{
		"Accept-Encoding":           "gzip, deflate",
		"Accept-Language":           "zh-CN,zh;q=0.9",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent":                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
		"Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Referer":                   "",
		"Connection":                "keep-alive",
	}
	resp, _ := client.R().
		SetQueryParams(map[string]string{
			"objId":   queryparam,
			"objType": "1001",
		}).
        // 一次设置多个字段的请求头
		SetHeaders(headers).
		Get(url)

	fmt.Println(resp.String())
}


func BatSetCookies(cookieStr string, client *req.Client) {
	// 根据字符串，批量设置Cookies
	cookiePairs := strings.Split(cookieStr, ";")
	for _, pair := range cookiePairs {
		pair = strings.TrimSpace(pair)
		if len(pair) == 0 {
			continue
		}
		parts := strings.SplitN(pair, "=", 2)
		if len(parts) != 2 {
			continue
		}
		cookie := &http.Cookie{
			Name:  parts[0],
			Value: parts[1],
		}
		client.SetCommonCookies(cookie)
	}
}
