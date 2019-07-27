#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: calc_files_md5s
# Author:    fan
# date:      2018/9/27
# -----------------------------------------------------------
# 递归计算压缩包或文件夹内文件的MD5值
import hashlib
import rarfile, zipfile


def cal_md5(filepath, nbyte=1024):
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            current_bytes = f.read(nbyte)
            if current_bytes:
                md5.update(current_bytes)
            else:
                break
    return md5.hexdigest()


def dezip(zippath):
    zip = zipfile.ZipFile(zippath)
    f = zip.read(zip.namelist()[0])
    print(zip.namelist())
    print(f.decode('utf-8'))

if __name__ == '__main__':
    fp = 'productfile.osf'
    print(cal_md5(fp))
    zp = 'calc_files_md5s.zip'
    dezip(zp)
