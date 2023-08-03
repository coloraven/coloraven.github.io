# Go语言将Map数据写入EXCEL文件

```go
package main

import (
	"fmt"
	"strconv"
	"time"

	"github.com/xuri/excelize/v2"
)

func main() {

	var Datas []map[string]string
	for i := 0; i < 650000; i++ {
		data := map[string]string{"姓名": "张三", "序号": strconv.Itoa(i), "性别": "男"}
		Datas = append(Datas, data)
	}
	start := time.Now()
	StreamWriter("abc.xlsx", "Sheet1", Datas)
	elapsed := time.Since(start)
	fmt.Printf("Elapsed time: %s\n", elapsed)
}

// 来源http://t.csdn.cn/qv6PS
func StreamAppendWriter(filename, sheet_name string, contents [][]string) {
	//打开工作簿
	file, err := excelize.OpenFile(filename)
	if err != nil {
		return
	}
	// 确保在函数结束时关闭文件
	defer func() {
		if err := file.Close(); err != nil {
			fmt.Println(err)
		}
	}()
	// 获取流式写入器
	streamWriter, _ := file.NewStreamWriter(sheet_name)

	rows_old, _ := file.GetRows(sheet_name) // 按行获取内容
	cols_old, _ := file.GetCols(sheet_name) // 按列获取内容
	fmt.Println("已有内容行数rows:  ", len(rows_old), "已有内容列数cols:  ", len(cols_old))

	// 将源文件内容先写入excel
	for rowid, row_element_old := range rows_old {
		row := make([]interface{}, len(cols_old)) // 每行数据的个数等于列的个数
		// 构造准备写入的每行数据
		for col := 0; col < len(cols_old); col++ {
			if row_element_old == nil {
				row[col] = nil
			} else {
				row[col] = row_element_old[col]
			}
		}
		// 构造写入行的初始位置
		cell_start, _ := excelize.CoordinatesToCellName(1, rowid+1)
		if err := streamWriter.SetRow(cell_start, row); err != nil {
			fmt.Println(err)
		}
	}

	// 将新加contents写进流式写入器
	for rowID := 0; rowID < len(contents); rowID++ {
		row := make([]interface{}, len(contents[0]))
		for colID := 0; colID < len(contents[0]); colID++ {
			row[colID] = contents[rowID][colID]
		}
		// 构造写入行的初始位置
		cell_start, _ := excelize.CoordinatesToCellName(1, rowID+len(rows_old)+1)
		if err := streamWriter.SetRow(cell_start, row); err != nil {
			fmt.Println(err)
		}
	}

	// 结束流式写入过程
	err = streamWriter.Flush()
	if err != nil {
		fmt.Println(err)
	}
	// 保存工作簿
	err = file.SaveAs(filename)
	if err != nil {
		fmt.Println(err)
	}
}

// 来源http://t.csdn.cn/qv6PS
func StreamWriter(filename, sheet_name string, list_of_map []map[string]string) {
	//打开工作簿
	file := excelize.NewFile()
	defer func() {
		if err := file.Close(); err != nil {
			fmt.Println(err)
		}
	}()
	// 获取流式写入器
	streamWriter, _ := file.NewStreamWriter(sheet_name)
	headers := GetKeys(list_of_map[0])
	cell_start, _ := excelize.CoordinatesToCellName(1, 1)
	if err := streamWriter.SetRow(cell_start, headers); err != nil {
		fmt.Println(err)
	}
	// 将contents写进流式写入器
	for index, map_value := range list_of_map {
		row_number := index + 2
		row_of_values := GetValues(map_value, InterfaceToStringSlice(headers)) // 每行数据的个数 = 列的个数 = 切片中元素的个数
		// 构造写入行的初始位置
		cell_start, _ := excelize.CoordinatesToCellName(1, row_number)
		if err := streamWriter.SetRow(cell_start, row_of_values); err != nil {
			fmt.Println(err)
		}
	}

	// 结束流式写入过程
	err := streamWriter.Flush()
	if err != nil {
		fmt.Println(err)
	}
	// 保存工作簿
	err = file.SaveAs(filename)
	if err != nil {
		fmt.Println(err)
	}
}

func GetKeys(map_obj map[string]string) []interface{} {
	// 数组默认长度为map长度,后面append时,不需要重新申请内存和拷贝,效率很高
	keys := make([]interface{}, 0, len(map_obj))
	for k := range map_obj {
		keys = append(keys, k)
	}
	return keys
}

func GetValues(map_obj map[string]string, headers []string) []interface{} {
	values := make([]interface{}, 0, len(map_obj))
	for _, header := range headers {
		value := map_obj[header]
		values = append(values, value)
	}
	return values
}

func InterfaceToStringSlice(ifaceSlice []interface{}) []string {
	strSlice := make([]string, len(ifaceSlice))
	for i, v := range ifaceSlice {
		strSlice[i] = v.(string)
	}
	return strSlice
}

```
