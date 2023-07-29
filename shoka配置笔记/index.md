# shoka配置笔记

shoka主题的魔改笔记
## 首页卡片
`shoka\source\css\_mixins.styl`
```stylus mark:4
  shadow-box(border = true, radius = .5rem) {
  border-radius: radius;
  border: .0625rem solid var(--grey-2) if border == true;
  box-shadow: 0 .625rem 1.875rem -.9375rem var(--box-bg-shadow);
}
```
0 0.1rem 1.9rem -0.1rem #191717

## 右侧滚动条颜色
`themes\shoka\source\css\_common\scaffolding\scrollbar.styl`
```stylus mark:4
  ::-webkit-scrollbar {
  width: .3125rem;
  height: .3125rem;
  background: 0 FIREBRICK;
}
```

## 首页卡片鼠标滑过时边框阴影-249行
`themes\shoka\source\css\_common\components\pages\home.styl`
```stylus mark:8
    +mobile() {
      flex-direction: column;
      height: fit-content;
      max-height: fit-content;
    }

    &:hover {
      box-shadow: 0 0 2rem #000;// var(--box-bg-shadow);
```

## 标签后台时显示的文字
`themes\shoka\languages\zh-CN.yml`
```yaml mark:4-5
---
name: 简体中文
favicon:
  show: （●´3｀●）やれやれだぜ
  hide: (´Д｀)大変だ！
```
