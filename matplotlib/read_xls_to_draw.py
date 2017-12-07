#!/usr/bin/python
# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
from pylab import figure, show, plt
import xlrd


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_data(xlspath, shtindx):
    data = {}
    xls = xlrd.open_workbook(xlspath)
    sheet = xls.sheets()[shtindx]
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
    datasss.update(sheet_name=sheetname)
    # datasss.pop('')
    for key in datasss:
        print(key, '===', datasss[key])

    return datasss


def draw(xls, index, col):

    d = get_data(xls, index)
    xname = ''
    for i in d.keys():
        if '总' in i:
            xname = '采样时间' + i
            xtickvalue = d[i]
    figname = d['sheet_name']
    fig = figure(figsize=(16, 8), dpi=80)

    ax = fig.add_subplot(1, 1, 1)
    x = [i for i in range(500)]
    point = ['b.-', 'r.-', 'g.-', 'k.-', 'c.-']
    for i in range(len(col)):
        y = [n for n in d[col[i]]]
        point[i] = point[i][:2]
        ax.plot(x, y, point[i], label=col[i], linewidth=1)
    ax.set_xlabel(xname)
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    xt = xtickvalue
    ax.set_xticklabels([xt[0], xt[100], xt[200], xt[300], xt[400], xt[499]])
    ax.set_ylabel('当前重量值')
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格


if __name__ == '__main__':
    # xls_path = r"E:\流程17\WE_测试流程-余发荣-2017-09-08 称重模块功能修改测试\测试\ModbusPoll 数据采集\2wt 零点 默认.xlsx"
    # col_name = u'当前平均重量'

    xls_path = r"采集数据整理.xls"

    sheet_index = 2
    col_str = r'跟踪间隔0不启用 跟踪间隔1 跟踪间隔1000 跟踪间隔10000 跟踪间隔20000'
    col_str = r'跟踪范围0 跟踪范围5 跟踪范围20 跟踪范围50 跟踪范围100'
    col_str = r'稳定检查时间0(1) 稳定检查时间1 稳定检查时间200 稳定检查时间500 稳定检查时间1000'
    # col_str = r'检查范围0/1 检查范围5 检查范围20 检查范围50 检查范围100'

    col_name = col_str.split(' ')
    draw(xls_path, sheet_index, col_name)
    show()
