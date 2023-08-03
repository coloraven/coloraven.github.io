# Aardio语言中Treeview绑定数据格式

```java
winform.treeview.insertItem(
{
	    "text" : '根目录一';
		{
			 "text": '一级目录名',
			{"text": '二级目录名','something':'value'};
			{"text": '二级目录名','something':'value'};
		}
		{
			 "text": '一级目录名',
			{"text": '二级目录名','something':'value'};
			{"text": '二级目录名','something':'value'};
		}
		{
			"text":  '一级节点名','something':'value',
		}
})
winform.treeview.insertItem(
{
	    "text" : '根目录二';
		{
			 "text": '一级目录名',
			{"text": '二级目录名','something':'value'};
			{"text": '二级目录名','something':'value'};
		}
		{
			 "text": '一级目录名',
			{"text": '二级目录名','something':'value'};
			{"text": '二级目录名','something':'value'};
		}
		{
			"text":  '一级节点名','something':'value',
		}
}
)
```




