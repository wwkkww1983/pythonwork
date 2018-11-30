#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: everymd5s.py
# Author:    FanNote
# date:      2018/10/01
# -----------------------------------------------------------
import zipfile, rarfile
import os
import hashlib
import logging as log


class EveryMd5s(object):
    def __init__(self):
        self.md5value = None
        self.name_file_dict = None
        self.allfilesabspaths = None
        self.name_md5_dic = None

    def cal_md5(self, fileb, nbyte=65536):
        # 针对‘file'类型输入,返回单个文件的md5值
        md5 = hashlib.md5()
        while True:
            current_bytes = fileb.read(nbyte)
            if current_bytes:
                md5.update(current_bytes)
            else:
                fileb.close()
                break
        log.info(md5)
        self.md5value = md5.hexdigest()
        return self.md5value

    def defile(self, filepath: str):
        # 打开类型“文件”，单文件
        try:
            f = open(filepath, 'rb')
            name_file_dict = {filepath: f}
        except Exception as e:
            log.error(e)
            name_file_dict = {}
        log.info(name_file_dict)
        self.name_file_dict = name_file_dict
        return self.name_file_dict

    def defolder(self, folderpath: str):
        # 打开类型“文件夹”
        name_file_dict = {}
        os.chdir(folderpath)
        for root, dirs, files in os.walk(folderpath):
            for i in files:
                fp = os.path.join(root, i)
                fb = open(fp, 'rb')
                fpp = fp[len(folderpath):]  # 截取相对路径作为字典键值
                name_file_dict[fpp] = fb  # 组装相对路径和文件流为字典
        log.info(name_file_dict)
        self.name_file_dict = name_file_dict
        return name_file_dict

    def dezip(self, zippath: str):
        # 打开类型“zip”
        name_file_dict = {}
        zip = zipfile.ZipFile(zippath)
        for name in zip.namelist():
            fb = zip.open(name, 'rU')  # f为byte类型
            name_file_dict[name.encode('cp437').decode('gbk')] = fb  # 骚操作，先按zip文件名编码方式还原后再用gbk解码
        log.info(name_file_dict)
        self.name_file_dict = name_file_dict
        return name_file_dict

    def derar(self, zippath: str):
        # 打开类型“RAR”
        name_file_dict = {}
        rar = rarfile.RarFile(zippath)
        for name in rar.namelist():
            fb = rar.open(name, 'rU')  # f为byte类型
            name_file_dict[name] = fb
        log.info(name_file_dict)
        self.name_file_dict = name_file_dict
        return name_file_dict

    def get_all_files_abspaths_in_dir(self, dir: str):
        # 打开类型“文件夹”,返回所有文件的绝对路径
        name_file_list = []
        os.chdir(dir)
        for root, dirs, files in os.walk(dir):
            for i in files:
                fp = os.path.join(root, i)  # 合成文件绝对路径
                name_file_list.append(fp)  # 绝对路径
        log.info(name_file_list)
        self.allfilesabspaths = name_file_list
        return self.allfilesabspaths

    def calc_files_md5s(self, name_file_dic: dict):
        md5s = {}
        for key in name_file_dic:
            md5s[key] = self.cal_md5(name_file_dic[key])
        log.info(md5s)
        self.name_md5_dic = md5s
        return self.name_md5_dic


if __name__ == "__main__":
    this = EveryMd5s()
    this.get_all_files_abspaths_in_dir(r'..\vbox_auto_test')
    for file in this.allfilesabspaths:
        print(file)
