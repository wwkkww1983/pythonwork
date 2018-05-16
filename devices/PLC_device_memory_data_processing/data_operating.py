#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by fan on 2017/9/2

import xlrd, xlwt
import os
from getfiles import get_files


def read_and_write(dirpath, d_start, d_end, x_label, y_label, save_path):
    files = get_files(dirpath)
    xlss = []
    for filename in files:
        # 找到目标文件夹下的xls文件
        if filename[-4:] == '.xls':
            xlss.append(filename)
        else:
            pass

    tarketbook = xlwt.Workbook()
    # 设置目标xls文件，处理后表格放这里

    for xlsfile in xlss:
        book = xlrd.open_workbook(os.path.join(dirpath, xlsfile))
        # 读取工作表文件
        table = book.sheets()[0]
        # 读取表格
        ds = table.col_values(0)
        ds = list(ds)
        start = ds.index(d_start[0])
        end = ds.index(d_end[0])
        data = []
        for i in range(start, end):
            # 读取数据时，D1000之类的寄存器名称不需要
            row_data = table.row_values(i)
            row_data.remove(row_data[0])
            data = data + row_data
        ydata = data
        xdata = list(range(0, len(data)-1))

        sheet = tarketbook.add_sheet(xlsfile[:31])
        # 新建sheet来保存每一个xls文件整理的数据
        sheet.write(0, 0, xlsfile[:-4])
        sheet.write(1, 0, x_label)
        sheet.write(1, 1, y_label)
        # 第一行横轴时间，竖轴温度

        for i, x, y in zip(range(2, len(xdata)+2), xdata, ydata):
            # 数据写入sheet,注意表头部写标题和标签，不要覆盖
            # if y and y != '0':
            sheet.write(i, 0, x)
            sheet.write(i, 1, int(y))

    tarketbook.save(save_path)


# def read_data(readpath, begind, endd):
#     book = xlrd.open_workbook(readpath)
#     table = book.sheets()[0]
#
#     ds = table.col_values(0)
#     ds = list(ds)
#     begin = ds.index(begind)
#     end = ds.index(endd)
#     data = []
#     for i in range(begin, end):
#         row_data = table.row_values(i)
#         row_data.remove(row_data[0])
#         data = data + row_data
#
#     ydata = data
#     xdata = list(range(1, len(data)))
#
#     return xdata, ydata


def write_data(savepath, xdata, ydata, xlabel='时间/?s', ylabel='温度/0.1℃', title='sheet1'):

    file = xlwt.Workbook()
    sheet = file.add_sheet(title[10:])
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
    dir_path = r'E:\MyWorkPlace\pythonwork\devices\PLC_device_memory_data_processing\xlses'
    sav_pth = r"E:\MyWorkPlace\pythonwork\devices\PLC_device_memory_data_processing\已处理表格.xls"
    # Dxxxx只能是出现在软元件内存文件中索引的D地址
    stt = ['D1000']
    ed = ['D7000']
    x_lab = '采样周期/*ms'
    y_lab = '温度/*℃'
    read_and_write(dir_path, stt, ed, x_lab, y_lab, sav_pth)
