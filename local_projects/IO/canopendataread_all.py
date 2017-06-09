# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @author fan
# @version 2010-09-25 14:57
# 这是一个USB-CAN保存数据的解析程序，可以将原始数据解析为CANOpen格式，将各部分数据分别显示

import os
import sys

fileName = r'D:\OneDrive\pythonwork\local_projects\IO\canOpenAnal.txt'
file_read = open(fileName,'r',-1,'gbk')
f = file_read.read()
#for line in f:
#   print(line.rstrip())

        
file_read.close()

