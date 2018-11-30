#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: serial_read_and_write.py
# Author:    fan
# date:      2018/10/11
# -----------------------------------------------------------
# 一个串口开关、读取数据以及wecon PLC Y读写的小模块
import serial
import time
from fx_communication_protocol import LxPlcCom


def set_port(portnm: str, paud: int, bytesize: int, stopbits: int, parity: str):
    """
    set a port and open it
    :param portnm: com1,com2, ...
    :param paud: default 9600
    :param bytesize:
    :param stopbits:
    :param parity:
    :return:
    """
    t = serial.Serial(portnm)
    t.baudrate = paud
    t.bytesize = bytesize
    t.stopbits = stopbits
    t.parity = parity
    t.timeout = 0.3
    # print('port opened at port = %s; baud_rate = %d; data_size = %d; parity = %s; stop_bits = %d'
    #       % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))
    time.sleep(.2)
    return t


def close_port(pt: serial.Serial):
    """
    close the port
    :param pt:
    :return:
    """
    if pt.is_open:
        pt.close()
        print(pt.port, ': closed')


def open_port(pt: serial.Serial):
    """
    open the port
    :param pt:
    :return:
    """
    if not pt.is_open:
        pt.open()
        print(pt.port, ': opened')


def read_correct(pt: serial.Serial):
    """
    if port is alive, keep reading data with readline mode
    :param pt:
    :return:
    """
    res = None
    if not pt.is_open:
        res = False
    else:
        try:
            time.sleep(0.01)
            for i in range(20):
                datab = pt.readline(15)
                if datab == b'\x02014407M008047\x03':
                    print('the read bytes is: {}'.format(datab))
                    res = True
                    break
        except Exception as e:
            print(e)
            res = False
    return res


def write_bit(port, bit, value):
    # 设置输出状态，vlaue=0:复位； value=1:置位
    l = LxPlcCom()
    data = l.pack_write_bit(bit, value)
    for i in range(5):
        port.write(data)
        time.sleep(0.05)
    # port.close()


if __name__ == '__main__':
    # port_hmi = set_port('com2', 115200, 7, 1, 'E')
    # a = read_correct(port_hmi)
    # print('HMI port read ok? {}'.format(a))
    port_plc = set_port('com7', 9600, 7, 1, 'E')
    write_bit(port_plc, 'Y0', 0)

