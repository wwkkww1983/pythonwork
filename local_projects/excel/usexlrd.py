#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by fan on 2017/9/2

import xlrd
from os import path

dir_path = r'C:\Users\fan\Desktop\哈巴机实验-范春回\数据-9.1'
file_name = r'7~20mA DA200持续500ms.xls'
file_path = path.join(dir_path, file_name)
book = xlrd.open_workbook(file_path)
table = book.sheets()[0]
ds = table.col_values(0)
ds = list(ds)
begin = ds.index('D1000')
end = ds.index('D3496')
data = []
for i in range(begin, begin+1):
    data = data + table.row_values(152).remove('D1000')

print(data)




if __name__ == '__main__':
    pass