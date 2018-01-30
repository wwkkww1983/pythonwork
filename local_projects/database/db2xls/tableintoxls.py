#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: soft
# Author:    fan
# date:      2018/1/24
# -----------------------------------------------------------


def add_to_xls(xls, tables):
    """
    将表格信息按照一定格式（表格名_str，字段_tuple，数据_tuple(tuple)）记录到指定xls文件当中
    """
    table_name = tables[0]
    table_firstline = tables[1]
    table_data = tables[2]
    # xls = xlwt.Workbook()
    sheet = xls.add_sheet(table_name)
    sheet.write(0, 0, table_name)
    for i in range(len(table_firstline)):
        sheet.write(1, i, tables[1][i])

    for i in range(len(table_data)):
        for j in range(len(table_data[0])):
            sheet.write(i+2, j, table_data[i][j])