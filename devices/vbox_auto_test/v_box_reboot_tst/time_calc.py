#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: time_calc
# Author:    fan
# date:      2018/5/25
# -----------------------------------------------------------
import time
debug = 1
timestamp = lambda timestr: int(time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S')))

def get_stamps(boot_log, cnet_log):
    bootstamps = []
    connectedstamps = []
    with open(boot_log, 'r', encoding='gb2312') as f1:
        bootlog = f1.readlines()
        for rec in bootlog:
            recl = rec.split(',')
            if recl[0].isdigit():
                bootstamps.append(int(recl[1]))

        if debug:
            # print(bootlog)
            print(bootstamps)

    with open(cnet_log, 'r', encoding='gb2312') as f2:
        cnetlog = f2.readlines()

        for rec in cnetlog:
            recl = rec.split(' ')
            timestr = recl[0]+' '+recl[1]
            connectedstamps.append(timestamp(timestr))
        if debug:
            # print(cnetlog)
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
    for stamp1 in timestamps1:
        for stamp2 in timestamps2:
            if time_match(stamp1, stamp2):
                print(stamp1, stamp2, stamp2-stamp1)
            else:
                continue


if __name__ == '__main__':
    boot = ['timelog_ethernet.csv', 'timelog_wifi.csv', 'timelog_4g.csv',]
    cnet = ['cnet_ethernet.log', 'cnet_wifi.log', 'cnet_4g.log']
    for b, c in zip(boot, cnet):
        st1, st2 = get_stamps(boot, cnet)
        get_time_interval(st1, st2)
