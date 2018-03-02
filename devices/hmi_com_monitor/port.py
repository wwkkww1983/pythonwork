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
    line_str_seq = []
    p_time_seq = []
    down_position_seq = []
    up_position_seq = []
    if port:
        if not port.is_open:
            port.open()
        else:
            pass
        for i in range(20):
            sleep(0.1)
            line = p.readline()
            if not line == b'':
                if line[-3:] == b'\r\r\n':
                    line = line[:-3]
                    linestr = str(line, encoding='utf-8')
                    print(linestr)
                    templ = linestr.split(',')
                    p_time_seq.append(templ[0][-8:])
                    if templ[1] == 'EventType = ClickDown':
                        down_position_seq.append((templ[2][6:], templ[3][:-2]))
                    if templ[1] == 'EventType = ClickUp':
                        up_position_seq.append((templ[2][6:], templ[3][:-2]))
    return p_time_seq, down_position_seq, up_position_seq


def get_touch_delay(data):
    time_seq, down_xy, up_xy = [data[0], data[1], data[2]]

    if len(time_seq) == 2 * len(down_xy) == 2 * len(up_xy):
        touch_delay_seq = []
        for i in range(len(time_seq)):
            if i%2 == 1:
                delay = int(time_seq[i]) - int(time_seq[i-1])
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

    ax = fig.add_subplot(1, 1, 1)
    x = [i for i in range(len(delay_seq))]
    y = yvalues
    ax.plot(x, y, 'b.-', label=dataname, linewidth=1)
    ax.set_xlabel(xlabel)
    ax.set_xticks([i for i in range(0, len(delay_seq), len(delay_seq)//10)])
    # xt = xtickvalue
    # ax.set_xticklabels(['a', 'b', 'c', 'd', 'e'])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格
    canvas.print_figure('demo.jpg')

if __name__ == '__main__':
    p = get_port()
    l = read_debug_info(p)
    print(l)
    p.close()
    delay_seq = get_touch_delay(l)
    print(delay_seq)
    print('end')
    fig_tags = {'figname': 'a',
                'plot1': {'title': 'b',
                          'xlabel': 'c',
                          'ylabel': 'd',
                          'dataname': 'e',
                          'xticklabels': None,
                          'xtickvalues': None},
                'plot2': {'figname': None}}
    graph_delay_time(fig_tags, delay_seq)
    # print(l)
    # p.close()
    # print('end')
