# Docker 搭建Filerun


filerun 官方docker：
https://hub.docker.com/r/afian/filerun/

1、预先搭建好mariadb容器
2、使用以下命令运行filerun容器

```bash
docker run -itd --name filerun \
    --restart=unless-stopped \
    --link=mariadb
    -e FR_DB_HOST=数据库地址 \
    -e FR_DB_PORT=数据库端口 \
    -e FR_DB_NAME=数据库名称（需要先自行建好，filerun初始化时不会建立） \
    -e FR_DB_USER=数据库用户名 \
    -e FR_DB_PASS=数据库密码 \
    -e APACHE_RUN_USER=www-data \
    -e APACHE_RUN_USER_ID=33 \
    -e APACHE_RUN_GROUP=www-data \
    -e APACHE_RUN_GROUP_ID=33 \
    -p 616:80 \
    -v /userdatas/Sandisk/filerun/html:/var/www/html \
    -v /userdatas/Sandisk/filerun/user-files:/user-files \
    afian/filerun
```

filerun默认监听80端口，
默认使用以下两个作为数据持久化的路径：

- /filerun/html:/var/www/html
- /filerun/user-files:/user-files

初始化的用户名密码均为：`superuser`

深色主题：
来源：https://feedback.filerun.com/en/communities/1/topics/501-dark-version-theme
文中提到的`theme_dark.css`

```css
.frBtn:hover,
.x-grid3-header {
	background-color: #303030;
}

.x-btn-pressed,
.x-btn-click:hover,
.x-btn-pressed:hover,
.x-btn-icon:hover {
	background-color: #262626;
}

.x-window,
.x-toolbar,
.x-panel-header,
.x-panel-body,
.x-panel-footer,
.x-grid3,
.ext-el-mask,
.x-combo-list-inner,
.x-tab-panel-header,
.x-tab-panel-footer,
.x-form-text,
textarea.x-form-field,
.x-superboxselect-input-field,
.x-menu,
.x-layout-split,
.headerTbar .x-btn-icon:hover,
.targetSelector .backButton:hover,
.targetSelector .closeButton:hover,
.targetSelector .topToolbar,
.targetSelector .x-window-header {
	background-color: #404040;
}

body,
.headerTbar,
.x-menu-item-active,
.tmbItem.typeFolder,
.tmbItem .tmbInner,
.x-superboxselect-item,
.x-tree-node-el:hover,
.fr-btn-default,
.x-grid3-row-over,
.ext-el-mask-msg,
#loadMsg div,
.x-list-over {
	background-color: #262626;
}

.headerTbar .x-btn-icon.x-btn-pressed,
.headerTbar .x-btn-icon.x-btn-click,
.headerTbar .x-btn-icon.x-btn-menu-active {
	background-color: black;
}

.headerTbar .xtb-sep {
	border-color: white;
	opacity: 0.3;
}

.tmbItem.typeFolder,
.tmbItem .tmbInner {
	box-shadow: none;
}

.fr-btn-new,
.fr-btn-primary, .fr-btn-primary:hover,
.x-date-inner .x-date-selected a,
.x-combo-list .x-combo-selected,
.x-list-selected,
.comment.own .text,
.bubbleCount div {
	background-color: #2d61b7;
}

.fr-btn-default,
.fr-btn-default:hover,
.x-color-palette a,
.x-color-palette em,
.x-color-palette a:hover,
.x-color-palette a.x-color-palette-sel,
.x-superboxselect-item {
	border-color: transparent;
}

.x-window,
.x-menu {
	border: 1px solid #262626;
}

.x-tab-strip-bottom,
.x-tab-strip-top,
.x-menu-sep,
.x-toolbar.FR-NavBar,
.x-layout-split,
.x-grid3-header,
.x-grid3-row,
.targetSelector .x-window-body {
	border-color: #262626;
}


.comment.own .text .inner:after,
.comment.own .text .inner:before {
	border-left-color: #2d61b7;
}

.logo3d,
.logo3d a,
.fr-btn-new,
.headerTbar .fa,
.x-btn-icon:hover i,
.x-btn-icon.x-btn-pressed i,
.x-btn-icon.x-btn-click i,
.x-combo-list .x-combo-selected,
.targetSelector .x-list-selected dt,
.targetSelector .x-list-selected .fa,
.frBtn,
a.x-menu-item,
.x-menu-item-active .x-menu-item-the-arrow,
.fr-btn-default:hover {
	color: white;
}

body,
.lang-select,
.x-tree-node a,
.tmbItem .name,
.fa,
.x-form-text,
textarea.x-form-field,
.x-superboxselect-input-field,
.fr-details-fields .field .name,
.x-tool,
.x-grid3-hd-row td,
.FR-NavBar .frBtn span,
.x-tab-strip span.x-tab-strip-text,
.x-fieldset legend,
.footerTextPanel .x-panel-body,
.eventItem .txt .fn,
.targetSelector dt {
	color: #DADCDC;
}
.x-tab-strip-active span.x-tab-strip-text {
	color: white;
}
.x-tree-node .x-tree-ec-icon,
.x-tree-node-el .icons i,
.fa-folder,
.x-tree-node-icon {
	color: #807e7e;
}

.x-tree-selected .x-tree-node-icon,
.x-tree-node-el.x-tree-selected .icons i,
.x-tree-selected .x-tree-ec-icon,
.tmbItemSel .icon i,
.tmbItemSel.typeFolder .iconsHolder i {
	color: #DADCDC;
}

a,
.fr-btn-link,
.fr-details-fields .field.title .value a:hover,
.fr-details-fields .field.title .editIcon:hover i,
.x-superboxselect-btns li:hover,
.x-superboxselect-locked .x-superboxselect-item:hover {
	color: #3FA9F2;
}

.tmbItemSel .tmbInner {
	background-color: transparent;
}
.tmbItem .selOverlay {
	background-color: #262626;
}
.tmbItemSel .tmbInner {
	background-color: transparent;
}
.tmbItem.typeFolder .iconsHolder {
	background-color: transparent;
}

.x-tree-node .x-tree-selected,
.tmbItemSel.typeFolder,
#FR-Grid-Panel .photoMode .tmbItemSel,
.x-grid3-row-selected,
.x-progress-inner,
.ux-progress-cell-background,
.tmbItem .selOverlay,
.tmbItemSel .tmbInner {
	background-color: #2d61b7;
}

.x-tree-node .x-tree-selected a,
.x-grid3-row-selected,
.tmbItemSel .name,
.fr-info-panel .x-tab-strip-active .fa {
	color: white;
}

.x-tab-strip-bottom .x-tab-strip-active .x-tab-right,
.x-tab-strip-top .x-tab-strip-active .x-tab-right {
	border-color: #2d61b7;
}

.tmbItemSel .tmbInner,
.tmbItemSel.typeFolder {
    box-shadow: none;
}

#FR-Grid-Panel .photoMode .tmbItemSel {
	box-shadow: inset 0 0 0 2px #262626 !important;
}

.tmbItem.typeFolder.dragged-over,
.x-tree-node .x-tree-drag-append,
.dragged-over {
	box-shadow: inset 0 0 0 2px #2d61b7 !important;
	background-color: #262626 !important;
}

.tmbItemSel .selOverlay {
	opacity: 0.5;
}

#explorer-shadow {
	display: none;
}

.iconsHolder {
	background-color: #26262626;
}

#FR-Center-Region,
#FR-Info-Region {
	border-left:1px solid #262626;
	box-shadow: none;
}

.x-window.login {
	border: none;
}
.login.transparent {
	background-color: rgba(64, 64, 64, 0.9);
}
.login.transparent .x-panel-footer {
	background-color:transparent;
}
.login.transparent #loginText {
	background-color: rgba(64, 64, 64, 0.3);
}

::-webkit-scrollbar-thumb {
	background-color: dimgray;
}

#FR-AudioPlayer .x-panel-body {
	box-shadow: none;
	border-top: 1px solid #262626;
}

/* Control Panel */
#FR-Tree-Region-xsplit {
	background-color: #404040;
	border-right-color: #262626;
}
#cardDisplayArea {
	box-shadow: none;
}
.sysConfMenuItem {
	background-color: #262626;
}
#gridTab .x-panel-bbar,
#gridTab .x-panel-tbar {
	border-color: #262626;
}
```


