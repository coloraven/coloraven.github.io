# CSharp中TreeView绑定JSON数据


JSON数据

```json
{
    "accepttime": 1600966807,
    "certificate": "",
    "completetext": "",
    "completetime": 1601010419,
    "createtime": 1600966807,
    "deleteflag": 0,
    "endtimestr": "12:00",
    "gid": 42,
    "netbarCameraList": [{
        "account": "admin",
        "address": "172.16.36.17",
        "cameraid": 21,
        "gid": 42,
        "name": "36",
        "password": "52358",
        "port": 554
    }],
    "netbarname": "长沙",
    "uniacid": 6,
    "userid": 66
}
```

代码：

```csharp
/// <summary>
        /// 绑定树形控件
        /// </summary>
        /// <param name="treeView"></param>
        /// <param name="strJson"></param>
        public void BindTreeView(TreeView treeView, string strJson)
        {
            treeView.Nodes.Clear();
            if (IsJsonObject(strJson))//判断是否字典类型
            {
                JObject jo = (JObject)JsonConvert.DeserializeObject(strJson);
                foreach (var item in jo)
                {
                    TreeNode tree;
                    if (item.Value.GetType() == typeof(JObject))//判断是否为字典类型
                    {
                        tree = new TreeNode(item.Key);//以字典的键为节点名
                        AddTreeChildNode(ref tree, item.Value.ToString());
                        treeView.Nodes.Add(tree);
                    }
                    else if (item.Value.GetType() == typeof(JArray))
                    {
                        tree = new TreeNode(item.Key);
                        AddTreeChildNode(ref tree, item.Value.ToString());
                        treeView.Nodes.Add(tree);
                    }
                    else
                    {
                        tree = new TreeNode(item.Key + ":" + item.Value.ToString());
                        treeView.Nodes.Add(tree);
                    }
                }
            }
            if (IsArray(strJson))//判断是否为列表类型
            {
                JArray ja = (JArray)JsonConvert.DeserializeObject(strJson);
                int i = 0;
                foreach (JObject item in ja)
                {
                    TreeNode tree = new TreeNode();
                    foreach (var itemOb in item)
                    {
                        TreeNode treeOb;
                        if (itemOb.Value.GetType() == typeof(JObject))
                        {
                            treeOb = new TreeNode(itemOb.Key);
                            AddTreeChildNode(ref treeOb, itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                        else if (itemOb.Value.GetType() == typeof(JArray))
                        {
                            treeOb = new TreeNode(itemOb.Key);
                            AddTreeChildNode(ref treeOb, itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                        else
                        {
                            treeOb = new TreeNode(itemOb.Key + ":" + itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                    }
                    treeView.Nodes.Add(tree);
                }
            }
            treeView.ExpandAll();
        }
        /// <summary>
        /// 添加子节点
        /// </summary>
        /// <param name="parantNode"></param>
        /// <param name="value"></param>
        public void AddTreeChildNode(ref TreeNode parantNode, string value)
        {
            if (IsJsonObject(value))
            {
                JObject jo = (JObject)JsonConvert.DeserializeObject(value);
                foreach (var item in jo)
                {
                    TreeNode tree;
                    if (item.Value.GetType() == typeof(JObject))
                    {
                        tree = new TreeNode(item.Key);
                        AddTreeChildNode(ref tree, item.Value.ToString());
                        parantNode.Nodes.Add(tree);
                    }
                    else if (item.Value.GetType() == typeof(JArray))
                    {
                        tree = new TreeNode(item.Key);
                        AddTreeChildNode(ref tree, item.Value.ToString());
                        parantNode.Nodes.Add(tree);
                    }
                    else
                    {
                        tree = new TreeNode(item.Key + ":" + item.Value.ToString());
                        parantNode.Nodes.Add(tree);
                    }
                }
            }
            if (IsArray(value))
            {
                JArray ja = (JArray)JsonConvert.DeserializeObject(value);
                int i = 0;
                foreach (JObject item in ja)
                {
                    TreeNode tree = new TreeNode();
                    parantNode.Nodes.Add(tree);
                    foreach (var itemOb in item)
                    {
                        TreeNode treeOb;
                        if (itemOb.Value.GetType() == typeof(JObject))
                        {
                            treeOb = new TreeNode(itemOb.Key);
                            AddTreeChildNode(ref treeOb, itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                        else if (itemOb.Value.GetType() == typeof(JArray))
                        {
                            treeOb = new TreeNode(itemOb.Key);
                            AddTreeChildNode(ref treeOb, itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                        else
                        {
                            treeOb = new TreeNode(itemOb.Key + ":" + itemOb.Value.ToString());
                            tree.Nodes.Add(treeOb);
                        }
                    }
                }
            }
        }
        /// <summary>
        ///  判断是否JOjbect类型
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public bool IsJsonObject(string value)
        {
            try
            {
                JObject ja = JObject.Parse(value);
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }
        /// <summary>
        /// 判断是否JArray类型
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public bool IsArray(string value)
        {
            try
            {
                JArray ja = JArray.Parse(value);
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }
```

效果：
<img src="2622728873.png" alt="2021-07-19T02:57:58.png" style="zoom:80%;" />

