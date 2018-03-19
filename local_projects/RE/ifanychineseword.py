#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: ifanychineseword
# Author:    fan
# date:      2018/3/15
# -----------------------------------------------------------
import re

f = open(r'C:\Users\fan\Desktop\EN_SMP.xml', 'r', encoding='utf-8')
s = []
for line in f.readlines():
    s.append(line)
# zhpattern = re.compile(u'[\u4e00-\u9fa5]+')    # 汉字编码范围
zhpattern = re.compile(u'[\u00ff-\uffff]+')    # AscII码字符范围
for i in s:
    match = zhpattern.search(i)
    if  match:
        # print('包含中文：{}'.format(match.group(0)))
        print('非ascii字符 [{}] 在行[{}]'.format(match.group(0), s.index(i)))

if __name__ == '__main__':
    pass
