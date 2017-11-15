#!/usr/bin/python
# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
from pylab import figure, show, plt
import xlrd


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_data(xlspath, colname):
    data = {}
    xls = xlrd.open_workbook(xlspath)
    sheet = xls.sheets()[0]
    m = sheet.nrows  # 行数
    l = sheet.ncols  # 列数
    sheetname = sheet.cell_value(0, 0)
    names = sheet.row_values(2)
    values = []

    for name in names:
        index = names.index(name)
        value = sheet.col_values(index)[3:]
        values.append(value)
    datasss = dict(zip(names, values))
    datasss.update(sheet_name=sheetname, time=datasss[''])
    datasss.pop('')
    for key in datasss:
        print(key, '===', datasss[key])

    return datasss


def draw(xls, col):

    d = get_data(xls, col)
    figname = d['sheet_name']
    xname = '采样时间40s'
    xtickvalue = d['time']
    dataname = col
    yvalues = [n for n in d[col]]

    fig = figure(figsize=(12, 6), dpi=80)
    ax = fig.add_subplot(1, 1, 1)
    x = [i for i in range(500)]
    y = yvalues

    ax.plot(x, y, 'b.-', label=dataname, linewidth=1)
    ax.set_xlabel(xname)
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    xt = xtickvalue

    ax.set_xticklabels([xt[0], xt[100], xt[200], xt[300], xt[400], xt[499]])

    ax.set_ylabel('目标数据')
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格


if __name__ == '__main__':
    xls_path = r"E:\流程17\WE_测试流程-余发荣-2017-09-08 称重模块功能修改测试\测试\ModbusPoll 数据采集\2wt 零点 默认.xlsx"
    col_name = u'当前平均重量'
    # col_name = '当前重量原始值'
    draw(xls_path, col_name)
    show()
