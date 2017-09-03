#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by fan on 2017/9/2

import xlrd, xlwt
from os import path


def read_and_write():
    dirpath = r'..\excel'
    xlsname = r'数据表demo.xls'
    readpath = path.join(dirpath, xlsname)

    book = xlrd.open_workbook(readpath)
    table = book.sheets()[0]
    ds = table.col_values(0)
    ds = list(ds)
    begin = ds.index('D1000')
    end = ds.index('D1296')
    data = []
    for i in range(begin, end):
        row_data = table.row_values(i)
        row_data.remove(row_data[0])
        data = data + row_data

    ydata = data
    xdata = list(range(1, len(data)))
    print(xdata)
    print(ydata)

    file = xlwt.Workbook()
    sheet = file.add_sheet('sheet1')
    sheet.write(0, 0, '时间')
    sheet.write(0, 1, '温度')

    for i, x, y in zip(range(1, len(xdata)+1), xdata, ydata):
        sheet.write(i, 0, x)
        sheet.write(i, 1, int(y))
    file.save(r'../excel/数据表3.xls')


def read_data(readpath, begind, endd):
    book = xlrd.open_workbook(readpath)
    table = book.sheets()[0]

    ds = table.col_values(0)
    ds = list(ds)
    begin = ds.index(begind)
    end = ds.index(endd)
    data = []
    for i in range(begin, end):
        row_data = table.row_values(i)
        row_data.remove(row_data[0])
        data = data + row_data

    ydata = data
    xdata = list(range(1, len(data)))

    return xdata, ydata


def write_data(savepath, xdata, ydata, xlabel='时间', ylabel='温度', title='sheet1'):

    file = xlwt.Workbook()
    sheet = file.add_sheet(title)
    sheet.write(0, 0, xlabel)
    sheet.write(0, 1, ylabel)

    for i, x, y in zip(range(1, len(xdata) + 1), xdata, ydata):
        sheet.write(i, 0, x)
        sheet.write(i, 1, int(y))

    try:
        file.save(savepath)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    dir_path = r'..\excel'
    xls_name = r'PLC Editor软元件内存导出表.xls'
    read_path = path.join(dir_path, xls_name)
    save_path = r'..\excel\已处理表格.xls'

    data = read_data(read_path, 'D1000', 'D1296')
    write_data(save_path, data[0], data[1])


