#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: parse
# Author:    fan
# date:      2019/4/16 016
# -----------------------------------------------------------

from bs4 import BeautifulSoup
import xlwt
import glob  # 文件名模式匹配，代替遍历

# with open("Z:\MyworkSpace\pythonwork\Temp\CH_SMP.xml", "r", encoding="utf-8") as f:
#     xml = f.read()
# soup = BeautifulSoup(xml, "xml")
# nmodule = 0
# nsub = 0
# ndlg = 0
# nid = 0
# for module in soup.findChildren("Module"):
#     print(module["Module"])
#     nmodule += 1
#     for sub in module.findChildren("Sub"):
#         nsub += 1
#         print(sub["Sub"])
#         for ids in sub.findChildren("IDS"):
#             print(ids["ID"], ids["String"])
#             nid += 1
#         for dlg in sub.findChildren("Dlg"):
#             ndlg += 1
#             print(dlg["DlgId"])
#             for ids in dlg.findChildren("IDS"):
#                 print(ids["ID"], ids["String"])
#                 nid += 1
#
# print("id 条目：{}".format(nid))

with open("Z:\MyworkSpace\pythonwork\Temp\SP_SMP.xml", "r", encoding="utf-8") as f:
    xml = f.readlines()
xls = xlwt.Workbook()
sheet = xls.add_sheet("ID-Tag table")
sheet.write(0, 0, "ID")
sheet.write(0, 1, "Tag")
i = 1
for line in xml:
    line = line.strip()
    if line[:4] == "<IDS":
        index1 = line.find('ID="')
        l1 = len('ID="')
        index2 = line.find('" String="')
        l2 = len('" String="')
        index3 = line.find('" />')
        print(line[(index1+l1) : index2], line[(index2+l2) :index3])
        sheet.write(i, 0, line[(index1+l1) : index2])
        sheet.write(i, 1, line[(index2+l2) :index3])
        i += 1
xls.save("ID-Tag table.xls")
if __name__ == '__main__':
    pass
