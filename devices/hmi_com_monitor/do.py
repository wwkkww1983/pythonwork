#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: port
# Author:    fan
# date:      2018/3/1
# -----------------------------------------------------------
from serial import Serial
from time import sleep, clock
from threading import Thread
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_port(p_name='com2', p_baud=115200, p_bysz=8, p_stpb=1, p_prt='N'):
    # 设置串口
    t = Serial(p_name)
    t.baudrate = p_baud
    t.bytesize = p_bysz
    t.stopbits = p_stpb
    t.parity = p_prt
    # t.timeout = tmot
    t.close()
    return t


def read_debug_info(port):
    """
    获取串口调试信息并解析
    :param port: 串口对象
    :param point_num: 采集的行数
    :return:
    """
    global topage, frompage, down_position, up_position
    p_time_seq = []
    down_position_seq = []
    up_position_seq = []
    # from_pages = []
    # to_pages = []
    page_switch_times = []
    if port:
        if not port.is_open:
            port.open()
        else:
            pass
        while (len(page_switch_times) < 20) and (len(down_position_seq) < 200):
            # sleep(0.1)
            line = p.readline()
            if not line == b'':
                if line[-3:] == b'\r\r\n':
                    line = line[:-3]
                    linestr = str(line, encoding='utf-8')
                    # print(linestr)
                    templ = linestr.split(',')
                    templ.append('')  # 防止溢出
                    p_time_seq.append(templ[0][-8:])
                    if templ[1] == 'EventType = ClickDown':
                        down_position = (templ[2][6:], templ[3][:-1])
                        down_position_seq.append(down_position)
                    if templ[1] == 'EventType = ClickUp':
                        up_position = (templ[2][6:], templ[3][:-1])
                        up_position_seq.append(up_position)
                        print('touch point: press{}, release{}'.format(down_position, up_position))
                    if templ[0] == '[MGR]:DelScnNoFromMap':
                        frompage = templ[1][7:]
                        # from_pages.append(frompage)
                    if templ[0] == '[MGR]:AddScnNoToMap':
                        topage = templ[1][7:]
                        # to_pages.append(topage)
                        # print('----------', topage)
                    if templ[0][:8] == '--Screen':
                        page_time = templ[1][7:]
                        page_switch_times.append(frompage + ',' + topage + ',' + page_time)
                        print('page switching time: {} to {}: {}'.format(frompage, topage, page_time))
    return p_time_seq, down_position_seq, up_position_seq, page_switch_times


def get_touch_delay(data):
    """
    触摸延迟时间
    :param data:
    :return:
    """
    time_seq, down_xy, up_xy = [data[0], data[1], data[2]]
    if len(time_seq) == 2 * len(down_xy) == 2 * len(up_xy):
        touch_delay_seq = []
        for i in range(len(time_seq)):
            if i % 2 == 1:
                delay = int(time_seq[i]) - int(time_seq[i - 1])
                touch_delay_seq.append(delay)
        return touch_delay_seq


def graph_delay_time(fig_tags, delay_seq):
    fig = Figure(figsize=(12, 6), dpi=80)
    canvas = FigureCanvas(fig)
    figname = fig_tags['figname']
    title = fig_tags['plot1']['title']
    xlabel = fig_tags['plot1']['xlabel']
    ylabel = fig_tags['plot1']['ylabel']
    dataname = fig_tags['plot1']['dataname']
    # xtickvalue =
    yvalues = [n for n in delay_seq]
    ax = fig.add_subplot(2, 2, 1)
    x = [i for i in range(len(delay_seq))]
    y = yvalues
    ax.plot(x, y, 'b.-', label=dataname, linewidth=1)
    ax.set_xlabel(xlabel)
    ax.set_xticks([i for i in range(0, len(delay_seq), len(delay_seq) // 10)])
    # xt = xtickvalue
    # ax.set_xticklabels(['a', 'b', 'c', 'd', 'e'])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格
    canvas.print_figure('demo.jpg')


def graph_click_position(fig_tags, xy_seq):
    fig = Figure(figsize=(12, 8), dpi=80)
    fig.suptitle(fig_tags['title'])
    canvas = FigureCanvas(fig)
    for i in range(0, 4):
        ax = fig.add_subplot(2, 2, i + 1)
        # ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
        # ax.invert_yaxis()
        axname = fig_tags['plot' + str(i)]['axname']
        axname = axname
        xlabel = fig_tags['plot' + str(i)]['xlabel']
        ylabel = fig_tags['plot' + str(i)]['ylabel']
        ax.set_xlim(fig_tags['plot' + str(i)]['xlim'])
        ax.set_ylim(fig_tags['plot' + str(i)]['ylim'])
        dataname = fig_tags['plot' + str(i)]['dataname1']
        seq = xy_seq[i]
        x = [int(n[0]) for n in seq]
        y = [int(n[1]) for n in seq]
        ax.plot(x, y, 'b.', label=dataname, linewidth=2)
        ax.set_xlabel(xlabel, labelpad=2)
        ax.set_ylabel(ylabel)
        ax.set_title(axname)
        ax.legend()  # 图例
        ax.grid()  # 网格
    canvas.print_figure('demo1.png')

    def get_page_switch_time():
        pass


def do_graph_click_3102():
        pos_lim = {'pi3102': {'左上': [(0, 100), (10, 80)],
                              '右上': [(700, 800), (0, 80)],
                              '右下': [(700, 800), (400, 480)],
                              '左下': [(0, 100), (400, 480)]}}
        figtags = {'title': '触摸点击测试',
                   'plot0': {'axname': '',
                             'xlabel': '左上  x - 坐标',
                             'ylabel': 'y - 坐标',
                             'dataname1': 'press(x,y)',
                             'xlim': (0, 100),
                             'ylim': (0, 80)},
                   'plot1': {'axname': '',
                             'xlabel': '右上  x - 坐标',
                             'ylabel': 'y - 坐标',
                             'dataname1': 'press(x,y)',
                             'xlim': (700, 800),
                             'ylim': (0, 80)},
                   'plot2': {'axname': '',
                             'xlabel': '右下  x - 坐标',
                             'ylabel': 'y - 坐标',
                             'dataname1': 'press(x,y)',
                             'xlim': (700, 800),
                             'ylim': (400, 480)},
                   'plot3': {'axname': '',
                             'xlabel': '左下  x - 坐标',
                             'ylabel': 'y - 坐标',
                             'dataname1': 'press(x,y)',
                             'xlim': (0, 100),
                             'ylim': (400, 480)}}
        direct = ['左上', '右上', '右下', '左下']
        l_4 = []
        for i, dt in zip(range(4), direct):
            print('请点击HMI屏幕 {} 角 300 次'.format(dt))
            l = read_debug_info(p)
            l_4.append(l[1])
        graph_click_position(figtags, l_4)


def do_graph_click_3102h():
    pos_lim = {'pi3102': {'左上': [(0, 128), (0, 100)],
                          '右上': [(896, 1024), (0, 128)],
                          '右下': [(896, 1024), (500, 600)],
                          '左下': [(0, 128), (500, 600)]}}
    figtags = {'title': '触摸点击测试',
               'plot0': {'axname': '',
                         'xlabel': '左上  x - 坐标',
                         'ylabel': 'y - 坐标',
                         'dataname1': 'press(x,y)',
                         'xlim': (0, 128),
                         'ylim': (0, 100)},
               'plot1': {'axname': '',
                         'xlabel': '右上  x - 坐标',
                         'ylabel': 'y - 坐标',
                         'dataname1': 'press(x,y)',
                         'xlim': (896, 1024),
                         'ylim': (0, 100)},
               'plot2': {'axname': '',
                         'xlabel': '右下  x - 坐标',
                         'ylabel': 'y - 坐标',
                         'dataname1': 'press(x,y)',
                         'xlim': (896, 1024),
                         'ylim': (500, 600)},
               'plot3': {'axname': '',
                         'xlabel': '左下  x - 坐标',
                         'ylabel': 'y - 坐标',
                         'dataname1': 'press(x,y)',
                         'xlim': (0, 128),
                         'ylim': (500, 600)}}
    direct = ['左上', '右上', '右下', '左下']
    l_4 = []
    for i, dt in zip(range(4), direct):
        print('请点击HMI屏幕 {} 角 300 次'.format(dt))
        l = read_debug_info(p)
        l_4.append(l[1])
    graph_click_position(figtags, l_4)
    for i in l_4:
        print(l_4.index(i), i)
        for j in i:
            print(i)

if __name__ == '__main__':
    p = get_port()
    do_graph_click_3102h()
    print('end')
    p.close()
