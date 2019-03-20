# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.3.1
# author:fan


import struct
import binascii
import time
from serial import Serial  # 导入模块
t = Serial('com2')  # 创建Serial实例
t.baudrate = 115200  # 设置参数（参数设置请以实际为准）
t.bytesize = 7
t.stopbits = 1
t.parity = 'E'

print('''
            com = %s
      baud_rate = %d
      data_size = %d
         parity = %s
      stop_bits = %d''' % (t.port, t.baudrate, t.bytesize, t.parity, t.stopbits))


def watch_com(read_size=4, write_data='ff', sleep_time=0.1):
    i = 0
    while i < 10:
        i += 1
        if i == 32767:
            i = 0
        time.sleep(sleep_time)
        read_str_hex = t.read(size=read_size)
        if read_str_hex:
            read_str = binascii.b2a_hex(read_str_hex)
            l = read_str[0:4]
            write_str = l + write_data.encode('ascii')
            write_str_hex = binascii.a2b_hex(write_str)
            t.write(write_str_hex)
            print('%5d <-- %s \t(%s)' % (i, read_str, read_str_hex))
            print('%5d --> %s \t(%s)' % (i, write_str, write_str_hex))

if __name__ == '__main__':
    print(t)
    # t.write([0x02, 0x45, 0x37, 0x30, 0x38, 0x30, 0x43, 0x03, 0x35, 0x32])   # Y0 置1
    t.write([2, 69, 55, 48, 49, 48, 67, 3, 53, 51])
    t.write([2, 69, 56, 48, 56, 48, 67, 3, 53, 66])   # Y10 置1
    time.sleep(1)
    t.close()
