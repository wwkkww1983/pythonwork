#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: time_calc
# Author:    fan
# date:      2018/5/25
# -----------------------------------------------------------
import time
import os.path as path
debug = 0
timestamp = lambda timestr: int(time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S')))


def get_stamps(boot_log, cnet_log):
    print('处理{}和{}'.format(boot_log, cnet_log))
    bootstamps = []
    connectedstamps = []
    with open(boot_log, 'r', encoding='gb2312') as f1:
        bootlog = f1.readlines()
        for rec in bootlog:
            recl = rec.split(',')
            if recl[0].isdigit():
                bootstamps.append(int(recl[1]))

        if debug:
            print(bootlog)
            print(bootstamps)

    with open(cnet_log, 'r', encoding='gb2312') as f2:
        cnetlog = f2.readlines()

        for rec in cnetlog:
            recl = rec.split(' ')
            timestr = recl[0]+' '+recl[1]
            connectedstamps.append(timestamp(timestr))
        if debug:
            print(cnetlog)
            print(connectedstamps)
    return bootstamps, connectedstamps


def time_match(stamp1, stamp2):
    if stamp1 < stamp2:
        if stamp2 - stamp1 < 50:
            return 1
        else:
            return 0
    else:
        return 0


def get_time_interval(timestamps1, timestamps2):
    data = []
    lenth = len(timestamps1) - len(timestamps2)
    if lenth == 0:
        print('时间记录未丢失')
    elif lenth > 0:
        print('Cnet 文件时间记录丢了{}个'.format(lenth))
    else:
        print('timelog 文件时间记录丢了{}个'.format(lenth))
    for stamp1 in timestamps1:
        for stamp2 in timestamps2:
            if time_match(stamp1, stamp2):
                # print(stamp1, stamp2, stamp2-stamp1)
                data.append([stamp1, stamp2, stamp2-stamp1])
            else:
                continue
    return data


if __name__ == '__main__':
    filedir = r"P:\FAN_SHARED\201805 v-box版本测试遗留问题处理\测试结果\不同方式上电启动耗时_新方式"
    boot = ['timelog_ethernet.csv', 'timelog_wifi.csv', 'timelog_4g.csv',]
    cnet = ['cnet_ethernet.log', 'cnet_wifi.log', 'cnet_4g.log']
    csv = ['ethernet.csv', 'wifi.csv', '4g.csv']
    for b, c, t in zip(boot, cnet, csv):
        b = path.join(filedir, b)
        c = path.join(filedir, c)
        t = path.join(filedir, t)
        st1, st2 = get_stamps(b, c)
        ti = get_time_interval(st1, st2)
        with open(t, 'w', encoding='gb2312') as f:
            ti = [','.join([str(x) for x in i] + ['\n']) for i in ti]
            # ti = [str(i) for i in ti] + ['\n']
            # print(ti)
            f.writelines(ti)
