# 如何将 VSCode 变成绿色版本



## 介绍
指导性文章 : [Portable Mode in Visual Studio Code](https://xie.infoq.cn/link?target=https%3A%2F%2Fcode.visualstudio.com%2Fdocs%2Feditor%2Fportable)

## 为什么要设置成绿色版
- 移植方便，到了新的电脑环境，直接拷贝文件夹就完成 VSCode 环境搭建

- 管理方便，原来的插件，配置文件不在一个地方，而且路径藏的过深
如图，绿色版本的结构很清晰，除了应用程序之外就是一个存放 **扩展 (extensions)** 和 **用户数据 (user-data)** 的 **数据文件夹 (code-portable-data)**. 当我使用新的一台电脑的时候，只需要将 **VSCode 文件夹** 拷贝到新电脑就装有 相同配置，相同扩展的一模一样的 VSCode 编辑器，无需额外下载和配置.
![](https://static001.geekbang.org/infoq/cf/cfe66d03969c990c2c8c68a25ff4dd09.png)

## 如何将 VSCode 编程绿色版本
### 第一种情况：从零开始配置 VSCode
- 下载压缩包
下载地址 : [Download Visual Studio Code - Mac, Linux, Windows](https://code.visualstudio.com/download)
最后一个支持Win7的版本：[VSCode-win32-x64-1.70.3.zip](https://vscode.cdn.azure.cn/stable/a21a160d630530476218b85db95b0fd2a8cd1230/VSCode-win32-x64-1.70.3.zip)
- 下载完毕，解压到任意文件夹
- 创建数据文件夹 (放置插件以及用户设置)
- Mac 在 VSCode 同一层级的目录下创建文件夹 `code-portable-data`
- Windows 在解压后的文件夹内 创建文件夹 `data`
绿色版制作完成


### 第二种情况：在 VSCode 已经有配置的前提下变成绿色版
1. 下载压缩包
- 下载地址 : [Download Visual Studio Code - Mac, Linux, Windows](https://code.visualstudio.com/download)
最后一个支持Win7的版本：[VSCode-win32-x64-1.70.3.zip](https://vscode.cdn.azure.cn/stable/a21a160d630530476218b85db95b0fd2a8cd1230/VSCode-win32-x64-1.70.3.zip)
- 下载完毕，解压到任意文件夹
- 创建数据文件夹 (放置插件以及用户设置)
- Mac 在 VSCode 同一层级的目录下创建文件夹 `code-portable-data`
- Windows 在解压后的文件夹内 创建文件夹 `data`
1. 拷贝已有的插件和用户数据到数据文件夹
- 用户数据默认路径 (剪切到第 2 步建立的数据文件夹下，将 Code 改名为 data)
```bash Windows
%APPDATA%\Code
```

- 插件默认路径 (直接剪切到第 2 步建立的数据文件夹下)
```bash Windows
%USERPROFILE%\.vscode\extensions
```
版权声明：本文为 InfoQ 作者【lmymirror】的原创文章。

原文链接:【[https://xie.infoq.cn/article/2c6dd3742d5daf4b2d0df20af](https://xie.infoq.cn/article/2c6dd3742d5daf4b2d0df20af)】。文章转载请联系作者。
