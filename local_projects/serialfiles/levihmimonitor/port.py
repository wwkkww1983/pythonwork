# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1, 串口通信例子
# author:fan

import serial
import struct
import binascii
import time
import _thread as thread


def open_port(portnm, paud=115200):
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
    start = 0
    end = 0
    usetime = None
    if not pt.is_open:
        return
    else:
        while pt.is_open:
            data = None
            datab = pt.readline()
            try:
                data = datab.decode('gb2312')
            except:
                data = '无法gb2312解码'.encode('gb2312') + datab
            if data[0] == '\r':
                if data[-2:] == '\r\n':
                    print(data[1:-2])
                    if 'byPCN= 0x1,' in data:
                        start = time.clock()
                    if 'Use time' in data:
                        usetime = data
                    if 'Read Mac' in data:
                        end = time.clock()
                        break
            else:
                print(data)
        print('start at {0}\nend at {1}\n时间差 = {2}\nuse time: {3}'.format(start, end, end-start, usetime))


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
    p = open_port('com3')
    # write_port(p, 'abcdef')
    # thread.start_new_thread(read_port, (p,))
    # 使用子线程通讯，主线程用于处理其他事务
    read_port(p)
    print('aa')
