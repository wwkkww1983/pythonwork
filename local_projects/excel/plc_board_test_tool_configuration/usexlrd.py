#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by fan on 2017/9/2

import xlrd, time


def read_config(xlspath):
    xlsfile = xlrd.open_workbook(xlspath)
    table = xlsfile.sheets()[0]
    ress = {}
    curs_vals = {}
    com = r'请选择'
    board_code = 0
    cali_type_n = 1
    rows_of_cali_params = []
    cali_params_types = []
    for row_index in range(0, table.nrows):
        if 0 <= row_index <= 7:
            ress[table.cell_value(row_index, 0)] = int(table.cell_value(row_index, 1))
        if 10 <= row_index <= 21:
            k = table.cell_value(row_index, 0)
            l = table.row_values(row_index, 1, 4)
            curs_vals[k] = [int(str(int(l[i]))) for i in range(0, 3)]
        if row_index == 23:
            com = table.cell_value(row_index, 1)
        if row_index == 24:
            board_code = int(str(int(table.cell_value(row_index, 1)))[:2], 16)
        if row_index == 25:
            cali_type_n = int(table.cell_value(row_index, 1))
        if row_index == 26:
            rows_of_cali_params = table.row_values(row_index, 1, cali_type_n+1)
            for i in range(0, len(rows_of_cali_params)):
                rows_of_cali_params[i] = int(str(int(rows_of_cali_params[i])))
        else:
            pass
    for i in range(0, cali_type_n):
        cali_params = {}
        row_index = int(rows_of_cali_params[i])-1
        cali_params[table.cell_value(row_index, 0)] = table.row_values(row_index, 1)
        cali_params_types.append(cali_params)
    d = {}
    for key in curs_vals.keys():
        if '电压' in key:
            d['ch' + key[2]+'val'+'area'] = curs_vals[key]
        if '电流' in key:
            d['ch' + key[2]+'cur'+'area'] = curs_vals[key]
        print(d)

    print("""\
    ress  {0}
    com  {1}
    board_code  {2}
    cali_type_n  {3}
    rows_of_cali_params  {4}
    """.format(ress, com, board_code, cali_type_n, rows_of_cali_params))

    for item in cali_params_types:
        print('   ', item)

if __name__ == '__main__':
    read_config(r'C:\Users\fan\Desktop\PLC工装平台工具\配置文件\Configuration.xls')




