# vscode-hexo-utils使用教程

## 前言
为了解决`Typecho`需要自建服务器，容易数据丢失的问题，从`Typecho`转移到`Hexo`，但是`Hexo`需要解决只能本地写博客，而且还要安装一堆依赖的问题，又从网上学到了`Hexo`+`Github Acitons`的组合，这样只要有浏览器就能登录`Github`写博客。

> 最稳妥的的还是使用原生的`Hexo`环境（`node.js`），这样可以本地先预览博客最终效果，再发布，这样可以减少`commit`次数。

只是本地写博客如果采用`Hexo`最原始的方式，即：先`cd`到Hexo目录->再`hexo new post`->再到`_posts`目录中找到新建的`md文件`进行编辑，就显得非常繁琐不友好了。

**经过一番折腾，终于找到了`vscode-hexo-utils`这款神器。**

## 介绍
`vscode-hexo-utils`是一款VSCODE插件，可以实现在`VSCODE`中方便的写`Hexo`博客（新建、编辑、管理MD文件），省去了先`cd`到`Hexo`目录->再`hexo new post`->再到`_posts`中找到新建的`md文件`进行编辑的步骤，而且支持粘贴图片后自动保存到相应目录并插入进MD中，简直美滋滋。
同时还支持按`Draft`、`Post`、`Categories`、`Tags`管理文章，具体效果如图：
<img src="2021-08-23T095907.png" alt="2021-08-23T095907" style="zoom:20%" />
## 安装
首先得安装`VSCODE`...此步略。
然后在`VSCODE`的插件市场（`Ctrl+Shift+X`调出）中搜索`vscode-hexo-utils`，找到并安装它。

## 设置
安装完毕后，进入VSCODE的设置(`Ctrl+,`)，在新界面顶部搜索框输入`@ext:fantasy.vscode-hexo-utils`将插件的设置项筛选出来。这里介绍几个重要的设置。
### Hexo: Generate Time Format
这里设置新建文章、插入图片时自动生成的时间格式，留空的话，生成的时间形如：`2021-08-21T07:27:21+08:00`，可以自定义，具体变量[参考](https://day.js.org/docs/en/parse/string-format)，举个栗子：
>1、YYYY-MM-DD HH:mm:ss
生成的时间形如:`2021-08-23 14:18:57`
>2、YYYY-MM-DD HH:mm
生成的时间形如:`2021-08-23 14:18`

### Hexo: Hexo Project Root
这里设置Hexo博客所在目录，建议留空，并设置为不同步。

### Hexo › Markdown: Resource
这个配置项会开启代码中的 `markdown` 插件，用于支持一些 `hexo` 自己的语法。

### Hexo: Upload
设置是否自动将图片上传到图床，支持路过图床和腾讯oss，下面的两个设置对应路过图床和腾讯OSS，点击`在setting.json中编辑`，将自己平台的账号密码填入：
```json
"hexo.uploadImgchr": {
    "username": "用户名",
    "password": "密码"
}
```
### Hexo: Upload Type
选择默认的图床服务

## 使用
首先使用`VSCODE`打开`Hexo`项目目录，
然后在`VSCODE`左侧找到`vscode-hexo-utils`插件图标。<img src="2021-08-23T102122.png" style="zoom:50%" />
### 新建文章
鼠标放在`POST`栏目的Bar上，就能看到新增和刷新按钮，点击新增即可按照事先在`Hexo`设置的模板新建文章。
<img src="2021-08-23T102540.png" alt="2021-08-23T102540" style="zoom:50%" />


### 在文章中插入图片
- 1、使用图床
不知道是不是我设置的问题，路过图床总时提示失败，后来发现是路过图床更换了域名，已联系插件作者修复。
<img src="https://z3.ax1x.com/2021/08/23/h9sVtU.png" alt="" style="zoom:10%" />

- 2、不使用图床
插件会自动将图片保存至MD文件所在目录的同名子目录中。

### 使用插件提供的代码片段
插件默认附带了一些用来写`Hexo`博客的代码片段，可选择使用。
插件默认的代码片段如下，该文件的保存在`C:\Users\Administrator\.vscode\extensions\fantasy.vscode-hexo-utils-0.1.26\snippets`，可以自行添加代码片段，但是修改的东西不会同步到vscode云端，如需同步，可参考我的另一篇文章{% post_link VSCODE写HEXO博客时自动插入FrontMatter的实现 [VSCODE写HEXO博客时自动插入FrontMatter的实现] %}
```json
{
  "hexo.post_path": {
    "prefix": ["hexo.post_path"],
    "body": ["{% post_path ${1:filename} %}"],
    "description": "Include links to other posts."
  },
  "hexo.post_link": {
    "prefix": ["hexo.post_link"],
    "body": ["{% post_link ${1:filename} ${2:[title] [escape]} %}"],
    "description": "Include links to other posts."
  },
  "hexo.asset_path": {
    "prefix": ["hexo.asset_path"],
    "body": ["{% asset_path ${1:filename} %}"],
    "description": "Include post assets."
  },
  "hexo.asset_img": {
    "prefix": ["hexo.asset_img"],
    "body": ["{% asset_img ${1:filename} ${2:[title]} %}"],
    "description": "Include post assets."
  },
  "hexo.asset_link": {
    "prefix": ["hexo.asset_link"],
    "body": ["{% post_link ${1:filename} ${2:[title] [escape]} %}"],
    "description": "Include post assets."
  },
  "hexo.raw": {
    "prefix": ["hexo.raw"],
    "body": ["{% raw %}", "${1:content}", "{% endraw %}", "$0"],
    "description": "If certain content is causing processing issues in your posts, wrap it with the raw tag to avoid rendering errors."
  },
  "hexo.more": {
    "prefix": "hexo.more",
    "body": ["<!-- more -->", "$0"],
    "description": "Use text placed before the <!-- more --> tag as an excerpt for the post. excerpt: value in the front-matter, if specified, will take precedent."
  }
}
```
