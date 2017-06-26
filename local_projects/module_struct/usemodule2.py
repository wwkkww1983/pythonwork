# !/usr/bin/env python
# -*- coding: utf-8 -*-
from struct import unpack, pack

# data1 = [55, 68, 48, 48, 67, 56, 48, 48]
# data = ''
# data_chrs = [chr(i) for i in data1]    # 转为字符列表
# data_bytes = []
# for s in range(len(data_chrs)):
#     if s % 2 == 0:
#         a = int((data_chrs[s] + data_chrs[s + 1]), 16)    # 从下标0元素开始，将相邻两个字符合并成16进制表示并转为int型
#         data_bytes.append(chr(a).encode('utf-8'))              # 将上述元素进一步转为字节码，并组装为一半长度的字节列表
#     else:
#         pass
# print(len(data_bytes), data_bytes, len(b''.join(data_bytes)), b''.join(data_bytes))
# data_shorts = unpack('<L', bytes(b''.join(data_bytes)))

# print(data_shorts)

data2 = [55, 68, 48, 48, 67, 56, 48, 48]
data_chrs = [chr(i) for i in data2]
dword_data = []
for i in range(len(data_chrs)):
    if i % 8 == 0:
        dword_data.append(data_chrs[i+6]+data_chrs[i+7]+data_chrs[i+4]+data_chrs[5]
                          + data_chrs[i+2]+data_chrs[i+3]+data_chrs[i]+data_chrs[i+1])
print(dword_data, int(dword_data[0], 16))

b = b'\x00\x7d\x00\xc8'
dword = unpack('<L', bytes(b))
print(dword)