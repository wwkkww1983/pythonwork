#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: calc_files_md5s
# Author:    fan
# date:      2018/9/27
# -----------------------------------------------------------
# 递归计算压缩包或文件夹内文件的MD5值
# import hashlib
# import os
# import logging as log
# import rarfile
import zipfile
from os import path
from filecheck import FileCheck

HMIINDEX = {
    'LEVI 350T': 16,
    'LEVI 350TV': 18,
    'LEVI 430E': 2,
    'LEVI 430T': 2,
    'LEVI 430TV': 6,
    'LEVI 700E': 10,
    'LEVI 700EM': 17,
    'LEVI 700L': 12,
    'LEVI 700LK': 13,
    'LEVI 777A': 10,
    'LEVI 777T': 1,
    'LEVI 777TV': 5,
    'LEVI 908T': 3,
    'LEVI 908TV': 7,
    'LEVI 910T': 4,
    'LEVI 102A': 11,
    'LEVI 102E': 11,
    'LEVI 102L': 14,
    'LEVI 2070': 30,
    'LEVI 2070_TV': 31,
    'LEVI 700ML': 32,
    'LEVI 700ML_TV': 33,
    'LEVI 2035T': 36,
    'LEVI 2035T_TV': 37,
    'LEVI 2043T': 34,
    'LEVI 2043T_TV': 35,
    'LEVI 2043E': 38,
    'LEVI 2043E_TV': 39,
    'LEVI 2070S': 42,
    'LEVI 102ML': 44,
    'LEVI 102ML_TV': 45,
    'LEVI 750ML': 46,
    'LEVI 750ML_TV': 47,
    'LEVI 2070D': 70,
    'LEVI 2070D_TV': 71
}
OEMINDEX = {
    "OEM泉州科源": "JITOO",
    "OEM万维": "Exibl"
}


def osf_compare(srcpath, oempath, logopath, datpath, cpu="61y"):
    # 对比项目：长度，文件列表，MD5
    tarpath = path.join(oempath, "productfile.osf")
    assert path.isfile(tarpath)

    # 取OEM目录‘NUC972_2070_OEM泉州科源_6.4.18_2019-01-23’解析镜像信息：0-NUC972，1-型号，2-OEM，3-OS版本，4-OS日期
    productinfo = path.split(oempath)[1].split("_")

    if cpu == "61y":  # 2000系列常规型号
        file_list = [
            'BasEngine.nte',
            'HMITerm_ARM7.nte',
            'PLCCommon.nte',
            'PVGEngine.nte',
            'SysSet1.zip.u',
            'bmplib.eblb',
            'codeoem.dat',
            'defaultproject.zip.u',
            'logo.NTB',
            'os.ents',
            'project.zip.u',
            'zk12.bin',
            'zk16.bin',
            'zk8.bin'
        ]
    elif cpu == "71y":  # 2070D
        file_list = [
            'BasEngine.nte',
            'HMITerm_ARM7.nte',
            'PLCCommon.nte',
            'PVGEngine.nte',
            'SysSet1.zip.u',
            'bmplib.eblb',
            'codeoem.dat',
            'defaultproject.zip.u',
            'logo.NTB',
            'os.dnts',
            'project.zip.u',
            'zk12.bin',
            'zk16.bin',
            'zk8.bin'
        ]
    else:
        file_list = []
    dic1 = check.start_check("zip", srcpath)
    dic2 = check.start_check("zip", tarpath)
    if sorted(dic1) != file_list or sorted(dic2) != file_list:
        print("文件列表不相等：\n{}\n{}\n{}".format(file_list, sorted(dic1), sorted(dic2)))
    else:
        for filename in file_list:
            if filename == 'logo.NTB':
                srcmd5 = check.checkfile(logopath)[logopath]
                tarmd5 = dic2[filename]
                try:
                    assert srcmd5 == tarmd5
                    print('success, {}, {}, {}'.format(filename, srcmd5, tarmd5))
                except Exception:
                    print('fail, {}, {}, {}'.format(filename, srcmd5, tarmd5))
            elif filename == 'codeoem.dat':
                f = zipfile.ZipFile(tarpath)
                dat = f.open(filename, 'rU')
                lines = dat.readlines()
                line1 = lines[0].decode(encoding='utf-8')
                line2 = lines[1].decode(encoding='utf-8')
                l1 = line1.split('=')
                l2 = line2.split('=')
                assert l1[0] == 'codeoem'
                assert l2[0] == 'hmitype'
                assert l1[1] == OEMINDEX[productinfo[2]] + '\n'
                assert l2[1] == str(HMIINDEX["LEVI " + productinfo[1]]) + '\n'  # 补上\n
                print("success, {}, {}, OEM={}, hmitype={}".format(
                    filename, dic2[filename], OEMINDEX[productinfo[2]], str(HMIINDEX["LEVI " + productinfo[1]])))
            else:
                try:
                    assert dic1[filename] == dic2[filename]
                    print('success, {}, {}'.format(filename, dic2[filename]))
                except Exception as e:
                    print('fail, {}, {}, {}'.format(filename, dic1[filename], dic2[filename]))

if __name__ == '__main__':
    check = FileCheck()
    generalpath = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_6.4.18\NUC972_2043T_OEM_6.4.18_2019-01-23\productfile.osf"
    # p2 = r"Z:\MyworkSpace\pythonwork\Temp\OEM镜像对比\OEM_科源-productfile.osf"
    oempath = r"E:\Redmine2019\LEVIOEM测试\测试 #9036 万维机电有限公司 生产镜像（700ML 2043T 102ML） 测试\OEM_万维\NUC972_2043T_OEM万维_6.4.18_2019-01-23"
    logofile = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_6.4.18\LOGOS\4.3寸\logo.NTB"
    codeoemfile = r"E:\Redmine2019\LEVIOEM测试\测试 #9036 万维机电有限公司 生产镜像（700ML 2043T 102ML） 测试\OEM_万维\NUC972_2043T_OEM万维_6.4.18_2019-01-23\codeoem.dat"
    # check.start_check("zip", p1)
    # check.start_check("zip", p2)
    osf_compare(generalpath, oempath, logofile, codeoemfile)


