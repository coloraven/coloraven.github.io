# Butterfly主题折腾

## 自己打磨
### chrome浏览网页，检查并试图修改元素看变化，如果自己要的效果变了就是自己要找的元素，再以此为关键字用sublime text去搜索主题目录及其子目录文件。
### 修改首页卡片高度
修改文件`\themes\butterfly\source\css\_page\homepage.styl`
```css
  & > .recent-post-item
    display: flex
    flex-direction: row
    align-items: center
    height: 20em # 修改此处，可在chrome先边修改边预览，再改此处
    border-radius: 12px 8px 8px 12px
    background: var(--card-bg)
    box-shadow: var(--card-box-shadow)
    transition: all .3s
```

### 修改首页卡片背景颜色
修改文件`themes\butterfly\source\css\var.styl`
```css
// Global color & SVG
$light-blue = $theme-color
$dark-black = #000000
$light-grey = #EEEEEE
$grey = #858585
$white = #FFFFFF # 修改此处，可在chrome先边修改边预览，再改此处
$whitesmoke = #f5f5f5
$font-black = #4C4948
$card-bg = $white
$text-highlight-color = $font-color
$text-hover = $theme-color
$text-bg-hover = $theme-color
```

更好的卡片背景色（文章文字等的颜色同样适用）修改方法，
将上面文件中的`$card-bg`改为如下式样：
```css
$card-bg = $themeColorEnable && hexo-config('theme_color.card-bg_color') ? alpha(convert(hexo-config('theme_color.card-bg_color')), .1) : $card-green
```
然后再主题配置文件的`theme_color`块
```yml
# 美化/特效
# 自定義主題色
# 顏色值必須被雙引號包裹，就像"#000"而不是#000。否則將會在構建的時候報錯！
theme_color:
  enable: true
  main: "#49B1F5"
  paginator: "#00c4b6"
  button_hover: "#FF7242"
  text_selection: "#00c4b6"
  link_color: "#99a9bf"
  meta_color: "#858585"
  hr_color: "#A4D8FA"
  code_foreground: "#F47466"
  code_background: "rgba(27, 31, 35, .05)"
  toc_color: "#00c4b6"
  blockquote_padding_color: "#49b1f5"
  blockquote_background_color: "#49b1f5"
  card-bg_color: "#3D3D11" #卡片背景 备选，海蓝色#00ffe0d1
```
#### 修改正文字体颜色
`themes\butterfly\source\css\_global\index.styl`
```css
:root
  --global-font-size: $font-size
  --global-bg: $body-bg
  // --font-color: $font-black
  --font-color: #ffffff
```

### 修改导航栏高度
修改`themes\butterfly\source\css\_layout\head.styl`
```css
#nav
  position: absolute
  top: 0
  z-index: 90
  display: flex
  flex-wrap: wrap
  align-items: center
  padding: 0 36px
  width: 100%
// 修改此处
  height: 60px 
  font-size: 1.3em
  opacity: 0
  transition: all .5s
```
好看主题：https://ethant.top/
其图片地址：https://cdn.jsdelivr.net/gh/tzy13755126023/BLOG_SOURCE/theme_f/main.jpg

## CSS 修改
来源：https://butterfly.lete114.top/article/Butterfly-config.html

新建 `Hexo-Butterfly\themes\Butterfly-Master\source\css\Lete.css`(css 文件名自定义)

### 手机端显示

```css
/*移动端优化：去除归档、标签、最新文章、公告、、只保留网站统计*/

@media screen and (max-width: 800px) {
    #aside_content div:not(:last-child) {
        display: none;
        font-size: 13px;
    }
}
```
### 滚动条
```css
/* 滚动条 */

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-thumb {
    background-color: #e58a8a;
    background-image: -webkit-linear-gradient( 45deg, rgba(255, 255, 255, 0.4) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.4) 50%, rgba(255, 255, 255, 0.4) 75%, transparent 75%, transparent);
    border-radius: 2em;
}

::-webkit-scrollbar-corner {
    background-color: transparent;
}

::-moz-selection {
    color: #fff;
    background-color: #e58a8a;
}
```

## 进阶修改
来源：https://ouoholly.github.io/post/my-custom-config-on-hexo-butterfly-theme/
主題顏色
如果想進階修改主題顏色的話，可到以下文件修改參數：

`.\themes\Butterfly\source\css\var.styl`


### 主頁文章：不顯示圖片cover

1.  在 `.\themes\Butterfly\_config.yml` 設定 `index_post_cover: none`
2.  在 `.\themes\Butterfly\source\css\_layout\page.styl` , 
    * 2.1 -  把 `.recent-post-info` 設定 `width: 100%`
    * 2.2 -  在描述 `index_post_cover` 那裡添加下面三行：
```styl
else if hexo-config('index_post_cover') == 'none'
  .post_cover
      display: none
```
### 右下角按鈕：改為默認顯示，按才隱藏
右下角的 `黑夜模式`、`繁簡轉換` 、`字體大小` 按鈕原本是默認隱藏的，要按那個轉轉的設置按鈕才會彈出來。  
我想把這些功能按鈕改成默認顯示，按那個轉轉設置按鈕就收起來，再按再彈出來這樣和原本反過來的效果。  
於是把 `.\themes\Butterfly\source\css\_layout\rightside.styl` 裡改成下面這樣：
```css
#rightside
  position: fixed
  right: -38px
  bottom: 40px
  opacity: 0
  transition: all .5s

  #rightside-config-hide
    transform: translate(0, 0)

  .rightside-in
    animation: rightsideIn .3s

  .rightside-out
    animation: rightsideOut .3s
    transform: translate(30px, 0) !important

  & > div
    & > i,
    & > a,
    & > div
      display: block
      margin-bottom: 2px
      width: 30px
      height: 30px
      background-color: $light-blue
      color: $white
      text-align: center
      text-decoration: none
      font-size: 16px
      line-height: 29px
      cursor: pointer

      &:hover
        background-color: $ruby

  #rightside_config
    i
      animation: avatar_turn_around 2s linear infinite

  #mobile-toc-button
    display: none

@media screen and (max-width: $bg)
  #rightside
    #mobile-toc-button
      display: block

@keyframes rightsideOut
  0%
    transform: translate(0, 0)

  100%
    transform: translate(30px, 0)

@keyframes rightsideIn
  0%
    transform: translate(30px, 0)

  100%
    transform: translate(0, 0)
```

