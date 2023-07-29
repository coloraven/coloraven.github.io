# Hexo引用本地图片


## 引用本地图

参考：[原文链接](https://steflerjiang.github.io/2016/12/20/Hexo%E6%A1%86%E6%9E%B6%E4%B8%8B%E7%BB%99%E5%8D%9A%E5%AE%A2%E6%8F%92%E5%85%A5%E6%9C%AC%E5%9C%B0%E5%9B%BE%E7%89%87/)

首先在`hexo`的配置文件`_config.yml`中增加一句：
```yml
permalink: :title/
```
再在source文件夹中新建images文件夹，插入的图片要保存进此文件夹。
插入语法`html`(可控制图片大小):

```html
<img src="/four heroes.jpg" alt="dota插图" style="zoom:80%;" />
# 或
<img src="/images/four heroes.jpg" width=50% height=50% align=center/>
```
<img src="/four heroes.jpg" alt="dota插图" style="zoom:80%;" />



### label标签彩色文字样例，仅butterfly主题生效
```Markdown
臣亮言：{% label 先帝 %}创业未半，而{% label 中道崩殂 blue %}。今天下三分，{% label 益州疲敝 pink %}，此诚{% label 危急存亡之秋 red %}也！然侍衞之臣，不懈于内；{% label 忠志之士 purple %}，忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气；不宜妄自菲薄，引喻失义，以塞忠谏之路也。
宫中、府中，俱为一体；陟罚臧否，不宜异同。若有{% label 作奸 orange %}、{% label 犯科 green %}，及为忠善者，宜付有司，论其刑赏，以昭陛下平明之治；不宜偏私，使内外异法也。
```
