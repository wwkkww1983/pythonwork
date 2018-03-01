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


def get_port(p_name='com2', p_baud=115200, p_bysz=8, p_stpb=1, p_prt='N', tmot=1):
    # 设置串口
    t = Serial(p_name)
    t.baudrate = p_baud
    t.bytesize = p_bysz
    t.stopbits = p_stpb
    t.parity = p_prt
    t.timeout = tmot
    t.close()
    return t


def read_debug_info(port):
    s = []
    if port:
        if not port.is_open:
            port.open()
        else:
            pass
        i = 0
        while i <= 10:
            line = p.readline()
            if not line == b'':
                s.append(line)
    return s


def data_work(data):
    pass


if __name__ == '__main__':
    p = get_port()
    read_debug_info(p)
    p.close()
    print('end')
