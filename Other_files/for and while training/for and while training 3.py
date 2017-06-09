# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# created on 2.17,2017
# author: fan

"""练习
使用for 循环将一个字符串list 组合成一句话的字符串并打印，注意空格
['My','name','is','Han','mei']
"""
l = ['My', 'name', 'is', 'Han', 'mei']
L = ''
for i in range(len(l)):
    if i < len(l):
        L += l[i] + ' '
L += l[-1]
print(L)
