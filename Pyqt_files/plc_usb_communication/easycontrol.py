# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1
# author:fan

from serial import Serial
import struct
import binascii
import time
from fx_communication_protocol import LxPlcCom    # 用来组装串口数据


def get_port(p_name='com1', p_baud=9600, p_bysz=8, p_stpb=1, p_prt='N', tmot=1):
    # 设置串口
    t = Serial(p_name)
    t.baudrate = p_baud
    t.bytesize = p_bysz
    t.stopbits = p_stpb
    t.parity = p_prt
    t.timeout = tmot
    return t


def write(port, y, value):
    #
    l = LxPlcCom()
    data = l.pack_write_bit(y, value)
    for i in range(3):
        port.write(data)
        time.sleep(0.01)


def close_port(port):
    port.close()


if __name__ == '__main__':
    t = get_port(p_name='com2',
                 p_baud=115200,
                 p_bysz=7,
                 p_stpb=1,
                 p_prt='E')
    print(t)
    for y in ['Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7']:
        for v in [0, 0, 1, 0, 1, 0, 0]:
            write(t, y, v)
            time.sleep(.1)
    time.sleep(1)
    for y in ['Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7']:
        write(t, y, 1)
        time.sleep(.1)

    time.sleep(1)
    for y in ['Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7']:
        write(t, y, 0)
        time.sleep(.1)
    t.close()
