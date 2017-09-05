#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by fan on 2017/9/2

import xlrd
import os

def read_config(xlspath):
    xlsfile = xlrd.open_workbook(xlspath)
    table = xlsfile.sheets()[0]
    ress = {}
    curs = {}
    com = '请选择'
    board_code = 0
    cali_type_n = 1
    rows_of_cali_params = []
    cali_params = {}
    for row_index in range(0, table.nrows):
        if 0 <= row_index <= 7:
            ress[table.cell_value(row_index, 0)] = table.cell_value(row_index, 1)
        if 10 <= row_index <= 21:
            curs[table.cell_value(row_index, 0)] = table.row_values(row_index, 1, 4)
        if row_index == 23:
            com = table.cell_value(row_index, 1)
        if row_index == 24:
            board_code = int('0x'+str(table.cell_value(row_index, 1))[:2], 16)
        if row_index == 25:
            cali_type_n = int(table.cell_value(row_index, 1))
        if row_index == 26:
            rows_of_cali_params = table.row_values(row_index, 1, cali_type_n+1)
        else:
            pass
    for i in range(0, cali_type_n):
        row_index = int(rows_of_cali_params[i])-1
        cali_params[table.cell_value(row_index, 0)] = table.row_values(row_index, 1)

    print("""\
    com  {0}
    board_code  {1}
    cali_type_n  {2}
    rows_of_cali_params  {3}
    cali_params  {4}
    """.format(com, board_code, cali_type_n, rows_of_cali_params, cali_params))



if __name__ == '__main__':
     read_config( r'C:\Users\fan\Desktop\PLC工装平台工具\配置文件\Configuration.xls'
)




