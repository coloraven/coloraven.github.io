# Github Actions Artifacts（Github工件）下载加速思路

## 背景
用`Github Actions` build 带谷歌框架和`root`权限的安卓子系统，结果`build`出来的`artifacts`有将近4个G，挂代理（US和HK切换都一样）下载只有500K / S的速度，平时release可以跑满10M/S代理速度。

## 解决思路
不管是什么原因，思路是先利用国外VPS下载好再从VPS下回来，经过实验，这回可以跑满10M了。

## 要解决的问题
`wget`不能直接下载，原因也不多说，估计是`headers`或者`账号验证`之类的。
通过搜索：首先登录网站https://nightly.link，对相应仓库进行授权....
然后将欲下载工件地址填入，比如：
```
https://github.com/LSPosed/MagiskOnWSA/suites/4908840299/artifacts/141256770
```
这个网站会自动将链接转换成如下：
```
https://nightly.link/LSPosed/MagiskOnWSA/suites/4998111090/artifacts/146483433
```
这个转换出来的URL就可以直接在VPS上`wget`进行下载：
```bash
wget https://nightly.link/LSPosed/MagiskOnWSA/suites/4998111090/artifacts/146483433
```
