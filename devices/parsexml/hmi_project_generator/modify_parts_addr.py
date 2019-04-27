#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: modify_parts_addr
# Author:    fan
# date:      2019/4/24 024
# -----------------------------------------------------------
from bs4 import BeautifulSoup
import re


def replace_something(tarstr: str, oldstr: str):
    # 用星号*替换特殊字符，为后续解析做准备
    pat = re.compile(oldstr)
    matchstrs = pat.findall(tarstr)
    matchs = list(pat.finditer(tarstr))
    print(len(matchstrs))
    print(len(matchs))
    tarl = list(tarstr)

    if len(matchstrs) == len(matchs):
        for i in range(len(matchstrs)):
            span = matchs[i].span()
            tarl[span[0]:span[1]] = len(matchstrs[i]) * ["*"]
    outputstr = ''.join(tarl)
    # print(outputstr)
    with open('0 - copy - replace.hsc', 'w', encoding="utf-8") as f:
        f.write(outputstr)
    return [outputstr, matchstrs]


def parse_xml(xmlstr: str):
    # 解析xml并修改节点属性
    xml = BeautifulSoup(xmlstr, "xml")
    for scr in xml.findChildren("ScrInfo"):
        for part in scr.findChildren("PartInfo"):
            for gen in part.findChildren("General"):
                gen["WordAddr"] = "HDW10000"
    xmlstr = xml.prettify()  # 将soup对象格式化输出（xml文件）
    with open("xml generated.hsc", 'w', encoding="utf-8") as f:
        f.write(xmlstr)
    return xmlstr


def recover_something(tar: list, oldstr: str):
    # 将特殊字符还原
    pat = re.compile(oldstr)
    matchstrs = tar[1]  # 待还原的文本
    matchs = list(pat.finditer(tar[0]))  # 匹配星号的索引位置
    print(len(matchstrs))
    print(len(matchs))
    tarl = list(tar[0])
    if len(matchstrs) == len(matchs):
        for i in range(len(matchstrs)):
            span = matchs[i].span()
            tarl[span[0]:span[1]] = matchstrs[i]
    outputstr = ''.join(tarl)
    # print(outputstr)
    with open('0 - copy - replace - recover.hsc', 'w', encoding="utf-8") as f:
        f.write(outputstr)

if __name__ == '__main__':
    with open(r"Z:\MyworkSpace\pythonwork\Temp\HMIProject-画面部件地址修改\screens\0 - copy.hsc",
              "r",
              encoding="utf-8") as xml:
        xmlstr = xml.read()
    replaceold = r'[0-9]+[\x02].+[\x02][0-9]+'  # 正则匹配 CharSize="14\x0214\x0214\x0214\x0214\x0214\x0214\x0214"
    recover = r'\*\*+\*\*'
    replaced = replace_something(xmlstr, replaceold)
    addrswitched = parse_xml(replaced[0])
    replaced[0] = addrswitched
    recover_something(replaced, recover)




