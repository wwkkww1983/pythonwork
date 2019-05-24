#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: oem_logo_check
# Author:    fan
# date:      2019/5/20 020
# -----------------------------------------------------------
# 第一步，抓取所有厂商的LOGO文件
from imp import reload

from filecheck import FileCheck
from zipfile import ZipFile
import os
import json


def oem_logo_check():
    filecheck = FileCheck()
    LOGOSCALE = {
        "7寸": ["102ML", "700ML", "750ML", "2070", "2070D", "2070S"],
        "4.3寸": ["2043T", "2043E", "2043E-N"],
        "3.5寸": ["2035T"]
    }
    logo_md5s = []
    filename = "logo.NTB"
    path_oem_logos = r"E:\Redmine2019\LEVIOEM测试\logo_OEM"
    path_levi_oem = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\OEM"
    filelist = filecheck.lookfolder(path_levi_oem)  # 获取文件绝对路径
    print(filelist)
    path_temp = r"E:\Redmine2019\LEVIOEM测试\temp"
    oem_logo_dic = dict()
    for fullpath in filelist:  # 穷举OEM目录下所有文件
        path, name = os.path.split(fullpath)  # 分离“productfile.osf”
        if name == "productfile.osf":  # 取productfile.osf文件
            osf = ZipFile(fullpath)
            fileb = osf.open(filename, 'rU')
            md5 = filecheck.calc_md5(fileb)
            p, oeminfostr = os.path.split(path)  # 分离“NUC972_2070S_OEM泉州科源_6.4.18_2019-01-23”
            oeminfo = oeminfostr.split("_")
            if len(oeminfo) >= 4:  # 具有标准命名格式的才进行处理
                hmitype = oeminfo[1]  # 获取2070S
                oemcomp = ''.join(oeminfo[2:-2])  # 获取OEM泉州科源
                if oemcomp not in oem_logo_dic.keys():  # 相同OEM厂家的归类
                    oem_logo_dic[oemcomp] = {"7寸": [], "4.3寸": [], "3.5寸": []}
                for scale in LOGOSCALE.keys():  # 按不同尺寸区分
                    if hmitype in LOGOSCALE[scale]:  # 型号归类
                        if not oem_logo_dic[oemcomp][scale]:  # 若未存MD5值
                            oem_logo_dic[oemcomp][scale].append(md5)
                            depath = os.path.join(path_oem_logos, oemcomp, scale)  # 创建目录logos\OEM泉州科源\7寸
                            if not os.path.exists(depath):
                                os.makedirs(depath)
                            osf.extract(filename, depath)
                        else:  # 已存MD5，但值不一致，说明文件不同。
                            if md5 not in oem_logo_dic[oemcomp][scale]:
                                print("OEM LOGO 文件冲突：{}".format(oeminfostr))  # 同厂家同尺寸屏但LOGO文件不一致
    d = json.dumps(oem_logo_dic)
    print(d)
    with open(os.path.join(path_oem_logos, "{} md5 dict.json".format(filename)), "w") as f:
        f.write(d)

if __name__ == '__main__':
    pass
