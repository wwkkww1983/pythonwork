# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1, 串口通信例子
# author:fan

import serial
import struct
import binascii
import time
import _thread as thread


def open_port(portnm, paud=9600):
    """
    set a port and open it
    :param portnm: com1,com2, ...
    :param paud: default 9600
    :return: port which was opened
    """
    aport = serial.Serial(portnm, paud)
    print('port: opened; port = %s; baud_rate = %d; data_size = %d; parity = %s; stop_bits = %d'
          % (aport.port, aport.baudrate, aport.bytesize, aport.parity, aport.stopbits))
    time.sleep(.2)
    return aport


def close_port(pt):
    """
    close the port
    :param pt:
    :return:
    """
    if pt.is_open:
        pt.close()
        print(pt.port, ': closed')


def read_port(pt):
    """
    if port is alive, keep reading data with readline mode
    :param pt:
    :return:
    """
    if not pt.is_open:
        return
    else:
        while pt.is_open:
            data = pt.readline()
            print(data)


def write_port(pt, data='hello world'):
    """
    write something
    :param pt: port
    :param data: str which is ready to be writen to port
    :return:
    """
    bdata = data.encode()
    pt.write(bdata)


if __name__ == '__main__':
    p = open_port('com5')
    write_port(p, 'abcdef')
    thread.start_new_thread(read_port, (p,))
    # 使用子线程通讯，主线程用于处理其他事务
    time.sleep(5)
    print('aa')
