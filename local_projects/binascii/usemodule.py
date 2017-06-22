# !/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii, binhex
import struct
import ctypes

datas = [48, 69, 54, 50]
data = ''
data_str = [chr(i) for i in datas]
data_byte=[]
for s in range(len(data_str)):
    if s % 2 == 0:
        data_byte.append((r'\x'+data_str[s]+data_str[s+1]).encode('ascii'))
    else:
        pass
data_int = struct.unpack('h'*(len(data_byte)//2), bytes(b''.join(data_byte)))

print(data_int)