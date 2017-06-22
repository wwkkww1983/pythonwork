# !/usr/bin/env python
# -*- coding: utf-8 -*-


from struct import unpack, pack


datas = [48, 70, 54, 50]
data = ''
data_chr_list = [chr(i) for i in datas]
data_int_list=[]
for s in range(len(data_chr_list)):
    if s % 2 == 0:
        a = int((data_chr_list[s] + data_chr_list[s + 1]), 16)
        data_int_list.append(chr(a).encode('ascii'))
    else:
        pass

data_int = unpack('<h', bytes(b''.join(data_int_list)))

print(data_int)