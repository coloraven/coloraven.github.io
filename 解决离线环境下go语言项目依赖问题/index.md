# 解决离线环境下go语言项目依赖问题

思路：
实现原理：`GOPROXY`变量可以设置为本地目录的特点。
以下为实现方法（均为`Windows`系统）
### 联网电脑上的操作
目的：将需要的包下载到移动硬盘
1. 在移动硬盘根目录新建`gomods`文件夹；
2. 使用`set GOPATH=x:\gomods`将`GOPATH`临时设置为`x:\gomods`，
3. 新建一个项目（for_dl_mods）并初始化，在该项目中将需要的依赖写进去，如下：
```go
package main

import (
    // `_`意思只导入不使用
	_ "github.com/gocolly/colly"
	_ "github.com/tidwall/gjson"
)
```
3. 在该目录下使用`go mod download`命令，将会自动下载`colly`等依赖及其子依赖到`x:\gomods`下，

### 离线电脑上的操作
目的：将需要的包从移动硬盘自动复制到本地`gopath`中，并自动整理`go.mod`和`go.sum`两个文件。
4. 将移动硬盘插入离线机器，
5. 使用`set GOPROXY=file:///x:\gomods\cache\download`将获取依赖的服务器指向本地目录(注意：file后面是三个`/`，路径使用`\`符号)
6. 在开发的目录中运行`go mod tidy`。

> 第4、5步需要保持移动硬盘插在离线电脑上，如果不想这样，可以先从移动硬盘复制到离线电脑的本地磁盘，再相应改`GOPROXY`指向地址。

以上仍没有解决，因为go mod tidy会将下载的包与go官方进行一次哈希校验如下：
```text
main imports
    github.com/gocolly/colly: github.com/gocolly/colly@v1.2.0:
    verifying module: github.com/gocolly/colly@v1.2.0:
    Get "https://sum.golang.org/lookup/github.com/gocolly/colly@v1.2.0":
    dial tcp 142.251.42.241:443:
    connectex: A connection attempt failed because the connected party did not properly respond after a period of time, 
    or established connection failed because connected host has failed to respond.
```

参考文章：
[go-offline-packager](https://github.com/go-sharp/go-offline-packager)
https://pkg.go.dev/github.com/go-sharp/go-offline-packager#section-readme
https://gist.github.com/gmolveau/f09c1038ca622620e54d0579ba06ea96
以下为备份
## Using go mod vendor

### 0 - With an existing module

- copy `go.mod` and `go.sum` files from the offline PC to the internet PC

### 0bis - New module

- create a folder on the internet PC
- create a go module : `go mod init test` 

### 1 - Download dependencies via vendor folder

- create a `offline_modules.go` file :

```
package offline_modules

func main() {}
```

- add the dependencies you want to download (use `_`) :

```
package offline_modules

import (
	_ "github.com/gorilla/mux"
	_ "github.com/sirupsen/logrus"
)

func main() {}
```

- run `go mod vendor`

- the vendor folder should have new folders in it representing dependencies

### 2 - Back to offline

- copy `go.mod`, `go.sum` and `vendor`
- paste them on your offline PC, edit `go.mod` module name if necessary
- run your go commands with the flag `-mod=vendor` like `go run -mod=vendor main.go`

## Using git

TODO
