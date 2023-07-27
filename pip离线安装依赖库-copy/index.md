# pip离线安装依赖库

记录下命令，下载所需依赖库，在不能联网的机器上离线安装。
```bash
# 查看
pip list

# 依赖库信息格式输出
pip freeze > requirements.txt

# 仅下载
pip download -r requirements.txt

# 安装
pip install --no-index --find-links=dir_path -r requirements.txt
```
