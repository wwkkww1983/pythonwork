#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: levi_file_parser
# Author:    fan
# date:      2019/6/13 013
# -----------------------------------------------------------
import os
from mylog import mylog
from bs4 import BeautifulSoup
import xml.dom.minidom as dom
import json


class LeviFileParser(object):
    def __init__(self, installed_dir):
        self.levi_root = None
        if not os.path.exists(os.path.join(installed_dir, "Editor.exe")):
            mylog("file not found: {}".format(os.path.join(installed_dir, "Editor.exe")))
        else:
            self.levi_root = installed_dir

    def parse_filetype(self):
        filepath = os.path.join(self.levi_root, "FileType.xml")
        if not os.path.exists(filepath):
            mylog(mylog("file not found: {}".format(filepath)))
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                xmlstr = f.read()
            # mylog(xmlstr)
            if 'encoding="gb2312"' in xmlstr:
                xmlstr = xmlstr.replace('encoding="gb2312"', 'encoding="utf-8"', 1)
            soup = BeautifulSoup(xmlstr, "xml")
            set = soup.findChild("FILETYPESET")
            fi = set.findChild("FILE")
            mylog("\n{}\n属性数量,{}\n配置信息如下\n配置项,值,说明".format(filepath, len(fi.attrs)))
            for k in sorted(fi.attrs.keys()):
                mylog("{},{}".format(k, fi.attrs[k]))
            # filetype_dic["ID"] = fi["ID"]
            # filetype_dic["Suffix"] = fi["Suffix"]
            # filetype_dic["Title"] = fi["Title"]
            # filetype_dic["plctype"] = fi["plctype"]
            # filetype_dic["Type"] = fi["Type"]
            # print(soup.prettify())

    def parse_hmitype(self):
        filepath = os.path.join(self.levi_root, "HMIType.hmi")
        if not os.path.exists(filepath):
            mylog(mylog("file not found: {}".format(filepath)))
        else:
            with open(filepath, "r") as f:
                xmlstr = f.read()
            if 'encoding="gb2312"' in xmlstr:
                xmlstr = xmlstr.replace('encoding="gb2312"', 'encoding="utf-8"', 1)
            # mylog(xmlstr)

            soup = BeautifulSoup(xmlstr, "xml")
            set = soup.findChild("HMISet")
            hmis = set.findChildren("Hmi")
            mylog("\n{}\n型号数量 {}\n型号信息如下\n型号,型号索引,对应LEVI型号".format(filepath, len(hmis)))
            for hmi in hmis:
                mylog("{},{}".format(hmi["Type"], hmi["TypeIndex"]))

if __name__ == '__main__':
    directory = r"D:\Program Files\WECONSOFT\中性及OEM\欧华OVAHMI20190612"
    levifiles = LeviFileParser(directory)
    levifiles.parse_filetype()
    levifiles.parse_hmitype()
