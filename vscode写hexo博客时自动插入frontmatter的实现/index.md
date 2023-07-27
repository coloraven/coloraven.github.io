# VSCODE写HEXO博客时自动插入FrontMatter的实现

## 第一步
首先点`VSCODE`的`文件`->`首选项`->`用户片段`，在弹出来的对话框中选择`markdown.json`。输入以下内容：
```json
{
	"Hexo Front Matter": {
		"prefix": "---", # 触发代码块的输入字符
		"body": [
			"---",
			"title: ${TM_FILENAME_BASE}", # 自动将文件名作为标题
			"date: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE} ${CURRENT_HOUR}:${CURRENT_MINUTE}:${CURRENT_SECOND}", # 自动输入当前时间
			"update: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE} ${CURRENT_HOUR}:${CURRENT_MINUTE}:${CURRENT_SECOND}", # 自动输入当前时间
			"tags:",
			"  - ",
			"  - ",
			"categories:",
			"  - ",
			"  - ",			
			"description: ",
			"cover: ",
			"keywords: ",
			"---\r"
		],
		"description": "Hexo Front Matter"
	}
}
```
## 第二步
然后在VSCODE的设置中添加配置：
```json
"[markdown]": {
        "editor.formatOnSave": true,
        "editor.renderWhitespace": "all",
        "editor.quickSuggestions": {
            "other": true,
            "comments": true,
            "strings": true
        },
        "editor.acceptSuggestionOnEnter": "on"
    }
```
## 第三步
经过以上两个步骤后，用VSCODE写hexo博客，只需要在hexo的source\_post目录下新建markdown文件，并输入文件名，此时在编辑器中输入`---`，VSCODE将弹出自动补全的窗口，选中回车即可输入以下内容,省去了人工输入大量Front Matter信息。
```yml
---
title: VSCODE写HEXO博客时自动插入FrontMatter的实现
date: 2021-08-20 12:47:39
update: 2021-08-20 12:47:39
tags:
  - 
  - 
categories:
  - 
  - 
description: 
cover: 
keywords: 
---
```
## Over

