# CSharp from select语法实例


https://bbs.csdn.net/topics/392903084

```csharp
 
private void button1_Click(object sender, EventArgs e)
        {            
            string json = "[{\"Groupid\": \"1\",\"groupnum\": \"9005\",\"groupname\": \"调度中心\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"0\",\"user\": [],\"group\": [{\"Groupid\": \"54\",\"groupnum\": \"66000\",\"groupname\": \"大唐移动\",\"type\": \"0\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": [{\"Groupid\": \"55\",\"groupnum\": \"67000\",\"groupname\": \"大唐移动1\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": []}]        },{\"Groupid\": \"66\",\"groupnum\": \"66000\",\"groupname\": \"大唐联通\",\"type\": \"0\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": [{\"Groupid\": \"67\",\"groupnum\": \"67000\",\"groupname\": \"大唐联通1\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": []}]        }]},{\"Groupid\": \"1\",\"groupnum\": \"9005\",\"groupname\": \"调度中心\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"0\",\"user\": [],\"group\": [{\"Groupid\": \"54\",\"groupnum\": \"66000\",\"groupname\": \"大唐移动\",\"type\": \"0\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": [{\"Groupid\": \"55\",\"groupnum\": \"67000\",\"groupname\": \"大唐移动1\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": []}]        },{\"Groupid\": \"66\",\"groupnum\": \"66000\",\"groupname\": \"大唐联通\",\"type\": \"0\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": [{\"Groupid\": \"67\",\"groupnum\": \"67000\",\"groupname\": \"大唐联通1\",\"type\": \"1\",\"dnsprefix\": \"\",\"islocal\": \"1\",\"canshowall\": \"1\",\"user\": [],\"group\": []}]        }]}]";
            TreeNode nodes = new TreeNode("自定义总节点名称");
            AddChild(nodes, json,"groupname","group");//groupname替换成你的consult_mold_name，group替换成你的son就行了
            treeView1.Nodes.Add(nodes);
        }
 
        public void AddChild(TreeNode nodes,string json,string fatherName,string sonName)
        {
            JArray array = JArray.Parse(json);
            var list = from obj in array.Children()
                        select new { name=obj[fatherName],son= obj[sonName] };
            foreach (var item in list)
            {
                TreeNode node = new TreeNode(item.name.ToString());
                AddChild(node, item.son.ToString(),fatherName,sonName);
                nodes.Nodes.Add(node);
            }                        
        }
```


