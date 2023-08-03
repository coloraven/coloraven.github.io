# 【ChatGPT】FormCreat生成的vue文件如何使用

## 我提问如下
如何使用下面代码，用中文表达:
```html
<template>
  <div>
    <v-form-render :form-json="formJson" :form-data="formData" :option-data="optionData" ref="vFormRef">
    </v-form-render>
    <el-button type="primary" @click="submitForm">Submit</el-button>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        formJson: {"widgetList":[{"type":"tab","category":"container","icon":"tab","displayType":"border-card","tabs":[{"type":"tab-pane","category":"container","icon":"tab-pane","internal":true,"widgetList":[{"type":"grid","category":"container","icon":"grid","cols":[{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea81387","label":"待查内容","labelAlign":"","rows":5,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":false,"disabled":false,"hidden":false,"required":true,"requiredHint":"","validation":"","validationHint":"","customClass":[],"labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea81387"}],"options":{"name":"gridCol79620","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":""},"id":"grid-col-79620"},{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea113419","label":"查询结果","labelAlign":"","rows":5,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":true,"disabled":false,"hidden":false,"required":false,"requiredHint":"","validation":"","validationHint":"","customClass":"","labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea113419"}],"options":{"name":"gridCol52302","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":[]},"id":"grid-col-52302"}],"options":{"name":"grid114628","hidden":false,"gutter":12,"colHeight":null,"customClass":[]},"id":"grid114628"}],"options":{"name":"tab1","label":"微博手机互查","hidden":false,"active":true,"disabled":false,"customClass":""},"id":"tab-pane-26648"},{"type":"tab-pane","category":"container","icon":"tab-pane","internal":true,"widgetList":[{"type":"grid","category":"container","icon":"grid","cols":[{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea52469","label":"textarea","labelAlign":"","rows":3,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":false,"disabled":false,"hidden":false,"required":false,"requiredHint":"","validation":"","validationHint":"","customClass":"","labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea52469"}],"options":{"name":"gridCol106250","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":""},"id":"grid-col-106250"},{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea71693","label":"textarea","labelAlign":"","rows":3,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":false,"disabled":false,"hidden":false,"required":false,"requiredHint":"","validation":"","validationHint":"","customClass":"","labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea71693"}],"options":{"name":"gridCol9901","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":""},"id":"grid-col-9901"}],"options":{"name":"grid97343","hidden":false,"gutter":12,"colHeight":null,"customClass":[]},"id":"grid97343"}],"options":{"name":"tab-pane-102788","label":"QQ手机互查","hidden":false,"active":false,"disabled":false,"customClass":""},"id":"tab-pane-102788"},{"type":"tab-pane","category":"container","icon":"tab-pane","internal":true,"widgetList":[{"type":"grid","category":"container","icon":"grid","cols":[{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea47336","label":"textarea","labelAlign":"","rows":3,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":false,"disabled":false,"hidden":false,"required":false,"requiredHint":"","validation":"","validationHint":"","customClass":"","labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea47336"}],"options":{"name":"gridCol90005","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":""},"id":"grid-col-90005"},{"type":"grid-col","category":"container","icon":"grid-col","internal":true,"widgetList":[{"type":"textarea","icon":"textarea-field","formItemFlag":true,"options":{"name":"textarea63821","label":"textarea","labelAlign":"","rows":3,"defaultValue":"","placeholder":"","columnWidth":"200px","size":"","labelWidth":null,"labelHidden":false,"readonly":false,"disabled":false,"hidden":false,"required":false,"requiredHint":"","validation":"","validationHint":"","customClass":"","labelIconClass":null,"labelIconPosition":"rear","labelTooltip":null,"minLength":null,"maxLength":null,"showWordLimit":false,"onCreated":"","onMounted":"","onInput":"","onChange":"","onFocus":"","onBlur":"","onValidate":""},"id":"textarea63821"}],"options":{"name":"gridCol60866","hidden":false,"span":12,"offset":0,"push":0,"pull":0,"responsive":false,"md":12,"sm":12,"xs":12,"customClass":""},"id":"grid-col-60866"}],"options":{"name":"grid117325","hidden":false,"gutter":12,"colHeight":null,"customClass":[]},"id":"grid117325"}],"options":{"name":"tab-pane-31920","label":"预留","hidden":false,"active":false,"disabled":false,"customClass":""},"id":"tab-pane-31920"}],"options":{"name":"tab40457","hidden":false,"customClass":[]},"id":"tab40457"}],"formConfig":{"modelName":"formData","refName":"vForm","rulesName":"rules","labelWidth":80,"labelPosition":"left","size":"","labelAlign":"label-left-align","cssCode":"","customClass":"","functions":"","layoutType":"PC","onFormCreated":"","onFormMounted":"","onFormDataChange":""}},
        formData: {},
        optionData: {}
      }
    },
    methods: {
      submitForm() {
        this.$refs.vFormRef.getFormData().then(formData => {
          // Form Validation OK
          alert( JSON.stringify(formData) )
        }).catch(error => {
          // Form Validation failed
          this.$message.error(error)
        })
      }
    }
  }
</script>
```
## 【注释】
上述代码可通过访问http://120.92.142.115/或https://www.vform666.com/，导入下面`json`获得。
```json
{
  "widgetList": [
    {
      "type": "tab",
      "category": "container",
      "icon": "tab",
      "displayType": "border-card",
      "tabs": [
        {
          "type": "tab-pane",
          "category": "container",
          "icon": "tab-pane",
          "internal": true,
          "widgetList": [
            {
              "type": "grid",
              "category": "container",
              "icon": "grid",
              "cols": [
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea81387",
                        "label": "待查内容",
                        "labelAlign": "",
                        "rows": 5,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": false,
                        "disabled": false,
                        "hidden": false,
                        "required": true,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": [],
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea81387"
                    }
                  ],
                  "options": {
                    "name": "gridCol79620",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": ""
                  },
                  "id": "grid-col-79620"
                },
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea113419",
                        "label": "查询结果",
                        "labelAlign": "",
                        "rows": 5,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": true,
                        "disabled": false,
                        "hidden": false,
                        "required": false,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": "",
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea113419"
                    }
                  ],
                  "options": {
                    "name": "gridCol52302",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": []
                  },
                  "id": "grid-col-52302"
                }
              ],
              "options": {
                "name": "grid114628",
                "hidden": false,
                "gutter": 12,
                "colHeight": null,
                "customClass": []
              },
              "id": "grid114628"
            }
          ],
          "options": {
            "name": "tab1",
            "label": "微博手机互查",
            "hidden": false,
            "active": true,
            "disabled": false,
            "customClass": ""
          },
          "id": "tab-pane-26648"
        },
        {
          "type": "tab-pane",
          "category": "container",
          "icon": "tab-pane",
          "internal": true,
          "widgetList": [
            {
              "type": "grid",
              "category": "container",
              "icon": "grid",
              "cols": [
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea52469",
                        "label": "textarea",
                        "labelAlign": "",
                        "rows": 3,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": false,
                        "disabled": false,
                        "hidden": false,
                        "required": false,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": "",
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea52469"
                    }
                  ],
                  "options": {
                    "name": "gridCol106250",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": ""
                  },
                  "id": "grid-col-106250"
                },
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea71693",
                        "label": "textarea",
                        "labelAlign": "",
                        "rows": 3,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": false,
                        "disabled": false,
                        "hidden": false,
                        "required": false,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": "",
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea71693"
                    }
                  ],
                  "options": {
                    "name": "gridCol9901",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": ""
                  },
                  "id": "grid-col-9901"
                }
              ],
              "options": {
                "name": "grid97343",
                "hidden": false,
                "gutter": 12,
                "colHeight": null,
                "customClass": []
              },
              "id": "grid97343"
            }
          ],
          "options": {
            "name": "tab-pane-102788",
            "label": "QQ手机互查",
            "hidden": false,
            "active": false,
            "disabled": false,
            "customClass": ""
          },
          "id": "tab-pane-102788"
        },
        {
          "type": "tab-pane",
          "category": "container",
          "icon": "tab-pane",
          "internal": true,
          "widgetList": [
            {
              "type": "grid",
              "category": "container",
              "icon": "grid",
              "cols": [
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea47336",
                        "label": "textarea",
                        "labelAlign": "",
                        "rows": 3,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": false,
                        "disabled": false,
                        "hidden": false,
                        "required": false,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": "",
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea47336"
                    }
                  ],
                  "options": {
                    "name": "gridCol90005",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": ""
                  },
                  "id": "grid-col-90005"
                },
                {
                  "type": "grid-col",
                  "category": "container",
                  "icon": "grid-col",
                  "internal": true,
                  "widgetList": [
                    {
                      "type": "textarea",
                      "icon": "textarea-field",
                      "formItemFlag": true,
                      "options": {
                        "name": "textarea63821",
                        "label": "textarea",
                        "labelAlign": "",
                        "rows": 3,
                        "defaultValue": "",
                        "placeholder": "",
                        "columnWidth": "200px",
                        "size": "",
                        "labelWidth": null,
                        "labelHidden": false,
                        "readonly": false,
                        "disabled": false,
                        "hidden": false,
                        "required": false,
                        "requiredHint": "",
                        "validation": "",
                        "validationHint": "",
                        "customClass": "",
                        "labelIconClass": null,
                        "labelIconPosition": "rear",
                        "labelTooltip": null,
                        "minLength": null,
                        "maxLength": null,
                        "showWordLimit": false,
                        "onCreated": "",
                        "onMounted": "",
                        "onInput": "",
                        "onChange": "",
                        "onFocus": "",
                        "onBlur": "",
                        "onValidate": ""
                      },
                      "id": "textarea63821"
                    }
                  ],
                  "options": {
                    "name": "gridCol60866",
                    "hidden": false,
                    "span": 12,
                    "offset": 0,
                    "push": 0,
                    "pull": 0,
                    "responsive": false,
                    "md": 12,
                    "sm": 12,
                    "xs": 12,
                    "customClass": ""
                  },
                  "id": "grid-col-60866"
                }
              ],
              "options": {
                "name": "grid117325",
                "hidden": false,
                "gutter": 12,
                "colHeight": null,
                "customClass": []
              },
              "id": "grid117325"
            }
          ],
          "options": {
            "name": "tab-pane-31920",
            "label": "预留",
            "hidden": false,
            "active": false,
            "disabled": false,
            "customClass": ""
          },
          "id": "tab-pane-31920"
        }
      ],
      "options": {
        "name": "tab40457",
        "hidden": false,
        "customClass": []
      },
      "id": "tab40457"
    }
  ],
  "formConfig": {
    "modelName": "formData",
    "refName": "vForm",
    "rulesName": "rules",
    "labelWidth": 80,
    "labelPosition": "left",
    "size": "",
    "labelAlign": "label-left-align",
    "cssCode": "",
    "customClass": "",
    "functions": "",
    "layoutType": "PC",
    "onFormCreated": "",
    "onFormMounted": "",
    "onFormDataChange": ""
  }
}
```
## `ChatGPT`答复如下
这段代码看起来是一个Vue.js组件的模板和脚本部分。
在模板中，它包含了一个v-form-render组件，这个组件使用了三个 prop：form-json、form-data和option-data，并且给了它一个 ref。这个组件后面跟着一个 el-button 组件，这个组件有一个 type 属性为 primary，并且绑定了一个 click 事件处理函数 submitForm。
在脚本中，这个组件定义了一个对象，这个对象有一个 data 函数，这个函数返回了一个对象，这个对象里有一个 formJson 属性，它的值是一个大型的 JSON 对象。
要使用这个组件，你需要在你的 Vue 应用中引入它，然后在某个模板中使用它。例如，你可以在你的应用中定义一个组件：
```html
<template>
  <div>
    <my-form-component :form-json="formJson" :form-data="formData" :option-data="optionData"/>
  </div>
</template>

<script>
import MyFormComponent from './path/to/my-form-component.vue'

export default {
  components: {
    MyFormComponent
  },
  data() {
    return {
      formJson: {...},
      formData: {...},
      optionData: {...}
    }
  }
}
</script>
```
在模板中，你可以使用 my-form-component 组件，并且通过 props 传入相应的数据。
你还可以在脚本中定义一个 submitForm 函数，这个函数会在点击按钮时被调用。你可以通过在组件的 methods 对象中定义这个函数来实现这个功能。
例如：
```html
<template>
  <div>
    <my-form-component :form-json="formJson" :form-data="formData" :option-data="optionData" @submit="submitForm"/>
  </div>
</template>

<script>
import MyFormComponent from './path/to/my-form-component.vue'

export default {
  components: {
    MyFormComponent
  },
  data() {
    return {
      formJson: {...},
      formData: {...},
      optionData: {...}
    }
  },
  methods: {
    submitForm(formData) {
      // 在这里处理提交表单的逻辑
    }
  }
}
</script>
```
在这个例子中，我们在模板中为 my-form-component 绑定了一个 submit 事件，并且在组件的 methods 对象中定义了一个 submitForm 函数。当点击提交按钮时，组件会触发 submit 事件，并且把表单数据作为参数传递给事件处理函数。你可以在事件处理函数中进行相应的逻辑处理。
希望这能帮助你理解这段代码的作用。如果你有其他问题，请随时追问。


