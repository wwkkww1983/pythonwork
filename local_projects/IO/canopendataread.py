# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @author fan
# @version 2010-09-25 14:57
# 这是一个USB-CAN保存数据的解析程序，可以将原始数据解析为CANOpen格式，将各部分数据分别显示

import os
import sys

fileName = r'C:\Users\fan\OneDrive\pythonwork\local_projects\IO\canOpenAnal.txt'
#fileName = r'C:\Users\fan\OneDrive\pythonwork\local_projects\IO\CANMessage.txt'

def readUsbCanDataFile(fPath):
    file_read = open(fPath, 'r', -1, 'gbk')
    f = file_read.readlines()
    head_info = []
    head_label = []
    data_table = []
    data_num = 0
    for line_id in range(len(f)):
        f[line_id] = f[line_id].rstrip()
        if 1 <= line_id <= 5:
            head_info.append(f[line_id])
        if  line_id == 8:
            head_label = f[line_id].split(maxsplit=8)
        if line_id >= 9:
            data_num += 1
            data_id = f[line_id].split(maxsplit=8)
            data_table.append(data_id)
    for i in head_info:
        print(i)
    print(head_label)
    for k in data_table:
        print(k)
        file_read.close()
    return(head_info, head_label, data_table, data_num)
ff = readUsbCanDataFile(fileName)


