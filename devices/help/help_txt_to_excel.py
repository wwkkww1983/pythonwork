#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: help_txt_to_excel
# Author:    fan
# date:      2019/5/23 023
# -----------------------------------------------------------
import xlwt


name = 'levi'
xls = xlwt.Workbook()
sheet = xls.add_sheet(name)

with open(r"E:\Redmine2019\功能清单列写\功能清单-匹配帮助文档\{}.txt".format(name), 'r', encoding='utf-8') as f:
    txt = f.readlines()
level1 = []
level2 = []
level3 = []
level4 = []
level = []
for line in txt:
    print(line.rstrip())
    if line[:3] == "  [":  # 帮助标题
        char = line.strip().split(' ')[-1]
        level.append(char)
        sheet.write(len(level), 0, char)
    if line[:6] == ''.join([' '] * 5) + '[':  # 第一级
        char = line.strip().split(' ')[-1]
        level.append(char)
        sheet.write(len(level)-1, 1, char)
    if line[:9] == ' ' * 8 + '[':  # 第二级
        char = line.strip().split(' ')[-1]
        level.append(char)
        sheet.write(len(level)-2, 2, char)
    if line[:12] == ' ' * 11 + '[':  # 第三级
        char = line.strip().split(' ')[-1]
        level.append(char)
        sheet.write(len(level)-3, 3, char)
    if line[:15] == ' ' * 14 + '[':  # 第四级
        char = line.strip().split(' ')[-1]
        level.append(char)
        sheet.write(len(level)-4, 4, char)
# print(level1)
# print(level2)
# print(level3)
# print(level4)
print(level4)
xls.save(r'E:\Redmine2019\功能清单列写\功能清单-匹配帮助文档\{}（多余空行记得删掉）.xls'.format(name))

if __name__ == '__main__':
    pass
