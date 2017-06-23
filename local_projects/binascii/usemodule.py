# !/usr/bin/env python
# -*- coding: utf-8 -*-


from struct import unpack, pack
datas = [48, 70, 54, 50]
data = ''
data_chrs = [chr(i) for i in datas]    # 转为字符列表
data_bytes=[]
for s in range(len(data_chrs)):
    if s % 2 == 0:
        a = int((data_chrs[s] + data_chrs[s + 1]), 16)    # 从下标0元素开始，将相邻两个字符合并成16进制表示并转为int型
        data_bytes.append(chr(a).encode('ascii'))              # 将上述元素进一步转为字节码，并组装为一半长度的字节列表
    else:
        pass
data_shorts = unpack('<h', bytes(b''.join(data_bytes)))
print(data_shorts)
