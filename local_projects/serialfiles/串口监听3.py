# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1
# author:fan

from serial import Serial
import struct
import binascii
import time

t = Serial('com3', 9600)
print('''
      com       = %s
      baud_rate = %d
      data_size = %d
      parity    = %s
      stop_bits = %d''' % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))


def watch_com(read_size=4, write_data='ff', sleep_time=0.1):
    i = 0
    while i < 10:
        i += 1
        if i == 32767:
            i = 0
        time.sleep(sleep_time)
        read_str_hex       = t.read(size=read_size)
        if read_str_hex:
            read_str = binascii.b2a_hex(read_str_hex)
            l = read_str[0:4]
            write_str = l + write_data.encode('ascii')
            write_str_hex = binascii.a2b_hex(write_str)
            t.write(write_str_hex)
            print('%5d <-- %s \t(%s)' % (i, read_str, read_str_hex))
            print('%5d --> %s \t(%s)' % (i, write_str, write_str_hex))
#           print(hex(l.decode('ascii')))
watch_com()

class rw_serial(t,Serial):
    