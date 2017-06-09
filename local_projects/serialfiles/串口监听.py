# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.2.3.1
# author:fan

from serial import Serial
import struct
import time

class com_of_analog(Serial):
    pass

t = com_of_analog('com3', 9600)
print(('\n'
       '      com       = %s\n'
       '      baud_rate = %d\n'
       '      data_size = %d\n'
       '      parity    = %s\n'
       '      stop_bits = %d') % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))


