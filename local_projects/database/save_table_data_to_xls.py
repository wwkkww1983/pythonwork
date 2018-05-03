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
    sheet_name = tables[0]   # 作为sheet name
    sheet_field = tables[1]    # 作为sheet字段
    sheet_data = tables[2]    # 作为sheet数据
    # xls = xlwt.Workbook()
    sheet = xls.add_sheet(sheet_name)
    sheet.write(0, 0, sheet_name)
    for i in range(len(sheet_field)):
        sheet.write(1, i, tables[1][i])

    for i in range(len(sheet_data)):
        for j in range(len(sheet_data[0])):
            sheet.write(i+2, j, sheet_data[i][j])