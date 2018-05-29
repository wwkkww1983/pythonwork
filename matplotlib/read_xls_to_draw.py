#!/usr/bin/python
# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
from pylab import figure, show, plt
import xlrd

debug = 1

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_data(xlspath, shtindx=0):
    xls = xlrd.open_workbook(xlspath)
    sheet = xls.sheets()[shtindx]
    m = sheet.nrows  # 行数
    l = sheet.ncols  # 列数
    sheetname = sheet.cell_value(0, 0)
    col_names = sheet.row_values(1)
    print(col_names)
    datasss = {}
    for i in range(len(col_names)):
        # 将字段和对应值组成字典
        datasss[col_names[i]] = sheet.col_values(i)[2:]
    datasss['sheet_name'] = sheetname
    datasss['n_rows'] = m
    datasss['n_cols'] = l
    datasss['col_names'] = sheet.row_values(1)
    for key in datasss:
        if debug:
            print(key, '=', datasss[key])
    return datasss


def draw(data_dic):
    global x
    # d = get_data(xls, index)
    col_names = data_dic['col_names']

    figname = data_dic['sheet_name']
    fig = figure(figsize=(16, 8), dpi=80)

    ax = fig.add_subplot(1, 1, 1)
    # x = [i for i in range(xlen)]
    point = ['b.-', 'r.-', 'g.-', 'k.-', 'c.-', 'm.-', 'y.-', 'b^-']

    xname = col_names[0]
    x = [int(i) for i in data_dic[xname]]
    xlen = len(x)
    for i in range(1, len(col_names)):
        # 排除作为横轴标签的数据列，从第二列开始画图
        y = [n for n in data_dic[col_names[i]]]
        # point[i] = point[i][:2]
        ax.plot(x, y, point[i], label=col_names[i], linewidth=0.1)
    ax.set_xlabel(xname)
    # ax.set_xticks([0, int(0.2*xlen), int(0.4*xlen), int(0.6*xlen), int(0.8*xlen), xlen])
    ax.set_xticks([int(i/10*xlen) for i in range(0, 12, 2)])
    # ax.set_xticklabels([x[0]] + [x[int(i/10*xlen)] for i in range(2, 10, 2)] + [x[-1]+1])
    # ax.set_xticklabels([x[0], x[int(0.2*xlen)], x[int(0.4*xlen)], x[int(0.6*xlen)], x[int(0.8*xlen)], x[xlen-1]])
    ax.set_ylabel('当前重量值')
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格


if __name__ == '__main__':
    # xls_path = r"E:\流程17\WE_测试流程-余发荣-2017-09-08 称重模块功能修改测试\测试\ModbusPoll 数据采集\2wt 零点 默认.xlsx"
    # col_name = u'当前平均重量'
    # xls_path = r"E:\Redmine-任务\四路型BD模块（有壳）测试239\测试\水壶加热测温实验数据8路1.xls"
    # xls_path = r"E:\Redmine\20180503 李为 两路型BD板模块（有壳）LX3V-2PTS-BD_V1.2\PID验证实验\绘图.xls"
    xls_path = r"P:\FAN_SHARED\201805 v-box版本测试遗留问题处理\测试结果\不同方式上电启动耗时_新方式\不同方式上电启动耗时整理.xlsx"
    # sheet_index = 0
    # col_str = r'跟踪间隔0不启用 跟踪间隔1 跟踪间隔1000 跟踪间隔10000 跟踪间隔20000'
    # col_str = r'跟踪范围0 跟踪范围5 跟踪范围20 跟踪范围50 跟踪范围100'
    # col_str = r'稳定检查时间0(1) 稳定检查时间1 稳定检查时间200 稳定检查时间500 稳定检查时间1000'
    # col_str = r'检查范围0/1 检查范围5 检查范围20 检查范围50 检查范围100'
    # col_str = r'2PT2DAV-1	2PT2DAV-2	2PT2ADV-1	2PT2ADV-2	4PT-1	4PT-2	4PT-3	4PT-4'
    d = get_data(xls_path)
    draw(d)
    show()
