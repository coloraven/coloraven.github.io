# Github Actions 自动部署 Hugo 到 Gitee 同时刷新 Gitee Pages

【转载自：https://segmentfault.com/a/1190000039887159】
> 我的博客使用 GitHub 上的 pages 功能发布的基于 Hugo 生成的静态网站，基本无法正常访问，所以想要同步一份到 gitee 上发布，现在使用 GitHub Actions 提供的计算机资源就可以直接在 GitHub 上进行静态网站的生成，发布，远程刷新 gitee pages，触发条件可以是 push 或者定时等等，可谓十分好用，之后看到可以直接同步到 gitee 仓库，就实现一下试试，以下就是实现步骤，以及踩坑，当然强烈建议看开源代码的官方说明文档。

### 生成公钥和私钥并填入仓库

输入 `ssh-keygen -t rsa -C "user@email.com"`，然后回车几次，会生成 `id_rsa.pub` 文件和 `id_rsa` 文件，分别存放公钥和私钥：

![image](https://segmentfault.com/img/remote/1460000039887161 "image")

#### Gitee 仓库填入公钥

将公钥 `id_rsa.pub` 中的数据填入到 gitee 待备份仓库界面下 settings→Deploy keys→add personal public key

**这里注意:** 要选右上添加 personal public key 才有写入权限

![image](https://segmentfault.com/img/remote/1460000039887162 "image")

#### GitHub 仓库填入私钥

Settings→Secret→New repository secre 用于之后的程序环境配置访问，命名为 GITEE\_RSA\_PRIVATE\_KEY

![image](https://segmentfault.com/img/remote/1460000039887163 "image")

### 生成 GitHub 账号的 personal access token

![image](https://segmentfault.com/img/remote/1460000039887164 "image")

将仓库权限选上就行了，然后将生成的 token，配到私钥配置的地方 仓库→Settings→Secret→New repository secre，命名为 ACCESS\_TOKEN

![image-20210423172942681](https://segmentfault.com/img/remote/1460000039887165 "image-20210423172942681")

### 在仓库 secret 处添加 GITEE\_PASSWORD，放入 gitee 账号密码用于刷新 gitee pages

同之前步骤相同，之后用于环境变量的配置，就是以下 3 条 secret，OSS 的是自动部署到阿里 OSS 的脚本使用的，我是放在一个脚本里运行，需要了解可以看我另一篇文章。

![](https://segmentfault.com/img/remote/1460000039887166)

### 在 GitHub 仓库创建并编写 Actions 脚本！！！

文件名随意从这点开就行，下面有模板，点开后修改也行，创建的文件默认放在`.github/workflows/` 下

也可以用命令创建 `mkdir -p .github/workflows && touch .github/workflows/name.yml`

![image](https://segmentfault.com/img/remote/1460000039887167 "image")

#### 将代码拷入，修改具体变量，比如仓库名等，如果不需要 deploy 直接去掉就行了，不影响：
```yaml
name: deploy blog to gitee
 
on:
  push:
    branches:
      \- main    \# master 分支 push 的时候触发
      
jobs:
  deploy: #执行部署Hugo生成静态代码，默认放在gh-pages分支
    runs-on: ubuntu-18.04
    steps:
      \- uses: actions/checkout@v2
        with:
          submodules: recursive  \# Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    \# Fetch all history for .GitInfo and .Lastmod

      \- name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.81.0'
          extended: true #不需要extended版本就可以注释

      \- name: Build
        run: hugo \--minify

      \- name: Deploypage
        uses: peaceiris/actions-gh-pages@v3
        with:
          personal\_token: ${{ secrets.ACCESS\_TOKEN }}
          external\_repository: JohntunLiu/JohntunLiu.github.io
          publish\_branch: gh-pages  \# default: gh-pages
          publish\_dir: ./public
          
      \- name: Deploygitee
        uses: peaceiris/actions-gh-pages@v3
        with:
          personal\_token: ${{ secrets.ACCESS\_TOKEN }}
          publish\_dir: ./public
                
  
  sync: #同步到gitee仓库
    needs: deploy
    runs-on: ubuntu-latest
    steps:
    \- name: Sync to Gitee
      uses: wearerequired/git-mirror-action@master
      env:
        SSH\_PRIVATE\_KEY: ${{ secrets.GITEE\_RSA\_PRIVATE\_KEY }}
      with:
        \# 来源仓库
        source-repo: "git@github.com:JohntunLiu/myblog.git"
        \# 目标仓库
        destination-repo: "git@gitee.com:JohntunLiu/JohntunLiu.git"
        
  reload-pages:
    needs: sync
    runs-on: ubuntu-latest
    steps:
      \- name: Build Gitee Pages
        uses: yanglbme/gitee-pages-action@main
        with:
          \# 注意替换为你的 Gitee 用户名
          gitee-username: JohntunLiu
          \# 注意在 Settings->Secrets 配置 GITEE\_PASSWORD
          gitee-password: ${{ secrets.GITEE\_PASSWORD }}
          \# 注意替换为你的 Gitee 仓库，仓库名严格区分大小写，请准确填写，否则会出错
          gitee-repo: JohntunLiu/JohntunLiu
          \# 要部署的分支，默认是 master，若是其他分支，则需要指定（指定的分支必须存在）
          branch: gh-pages
```
点击 commit changes 提交运行，之后就看得到运行流程了

![image](https://segmentfault.com/img/remote/1460000039887168 "image")

### 实际效果和流程

如果是部署其他静态网站，修改 deploy 的代码块就行了，我顺便把部署到 GitHub pages 放在了里面：name: Deploypage

如果是 hugo 的话开源人员还提供了缓存机制，可以提高部署速度，可以去开源部分看，具体怎么看就是复制 `- uses: peaceiris/actions-hugo@v2` 后面的部分搜索到 GitHub 中看，比如：`https://github.com/peaceiris/actions-hugo`，readme.md 文档写得相当详实，也会更新说明

![image](https://segmentfault.com/img/remote/1460000039887169 "image")

更多精彩可以关注微信公众号 LiuJohntun，记录并分享我的所见、所学、所想...
