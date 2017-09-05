# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1
# author:fan

import serial
import struct
import binascii
import time


def open_port(portindex, paud):
    ptname = 'com' + str(portindex)
    aport = serial.Serial(ptname, paud)

    print('port: opened; port = %s; baud_rate = %d; data_size = %d; parity = %s; stop_bits = %d'
          % (aport.port, aport.baudrate, aport.bytesize, aport.parity, aport.stopbits))
    time.sleep(.2)
    return aport


def close_port(pt):
    if pt.is_open:
        pt.close()
        print(pt.port, ': closed')


def read_port(pt):
    if pt.readable:
        line = pt.readline()
    print(line)

if __name__ == '__main__':
    p = open_port(3, 9600)
    time.sleep(.5)
    read_port()
    time.sleep(5)
    close_port(p)
