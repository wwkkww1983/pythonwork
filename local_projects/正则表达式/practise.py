#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: practise
# Author:    fan
# date:      2018/3/9
# -----------------------------------------------------------
import re
s = r'Wecon PLC Editor  E:\Redmine\_20180123 PLC CModule\测试\测试工程\1-32000-0-0-100-10.pwcp   - 梯形图（写入）'
r = r"(?<=Wecon PLC Editor).+"
pattern1 = re.compile(r)
matcher1 = re.search(pattern1, s)
print(matcher1.group(0))
if __name__ == '__main__':
    pass
