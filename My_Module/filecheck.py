#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: filecheck
# Author:    fan
# date:      2019/4/23 023
# -----------------------------------------------------------
# 递归计算压缩包或文件夹内文件的MD5值
import hashlib
import os
import logging as log
import rarfile, zipfile

log.basicConfig(level=log.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class FileCheck(object):
    def __init__(self):
        pass

    def calc_md5(self, fileb, nbyte=65535):
        md5 = hashlib.md5()
        while True:
            current_bytes = fileb.read(nbyte)
            if current_bytes:
                md5.update(current_bytes)
            else:
                fileb.close()
                break
        return md5.hexdigest()

    def checkfile(self, filepath:str):
        # 校验类型“文件”
        md5dic = dict()
        try:
            f = open(filepath, "rb")
            md5 = self.calc_md5(f)
            md5dic[filepath] = md5
        except Exception as e:
            log.error("open file fail. -->{}".format(e))
            md5dic[filepath] = "md5错误"
        # print(md5dic)
        return md5dic

    def checkfolder(self, folderpath:str):
        # 校验类型“文件夹”
        md5dic = dict()
        os.chdir(folderpath)
        for root, dirs, files in os.walk(folderpath):
            for i in files:
                fp = os.path.join(root, i)  # 文件绝对路径
                with open(fp, 'rb') as fb:
                    fbmd5 = self.calc_md5(fb)
                fpp = fp[len(folderpath):]  # 截取相对路径作为字典键值
                md5dic[fpp] = fbmd5  # 组装相对路径和文件流为字典
        log.info(md5dic)
        # print(md5dic)
        return md5dic

    def checkzip(self, zippath: str, specialfilenames=None):
        # 校验类型“zip”
        md5dic = dict()
        zip = zipfile.ZipFile(zippath)
        for name in zip.namelist():
            if specialfilenames:
                if name in specialfilenames:  # 只计算压缩包内某些文件的MD5
                    fb = zip.open(name, 'rU')  # f为byte类型
                    md5 = self.calc_md5(fb)
                    md5dic[name.encode('cp437').decode('gbk')] = md5  # 骚操作，先按zip文件名编码方式还原后再用gbk解码
            else:
                fb = zip.open(name, 'rU')  # f为byte类型
                md5 = self.calc_md5(fb)
                md5dic[name.encode('cp437').decode('gbk')] = md5  # 骚操作，先按zip文件名编码方式还原后再用gbk解码
        # print(md5dic)
        return md5dic

    def checkrar(self, rarpath:str, specialfilenames=None):
        # 校验类型“rar”
        md5dic = dict()
        rar = rarfile.RarFile(rarpath)
        for name in rar.namelist():
            if specialfilenames is None:
                fb = rar.open(name, "rU")
                md5 = self.calc_md5(fb)
                md5dic[name.encode('cp437').decode('gbk')] = md5
            else:
                if name in specialfilenames:
                    fb = rar.open(name, "rU")
                    md5 = self.calc_md5(fb)
                    md5dic[name.encode('cp437').decode('gbk')] = md5
        # print(md5dic)
        return md5dic

    def lookfolder(self, folderpath: str):
        # 打开类型“文件夹”,返回所有文件的绝对路径，本函数不需要用到文件流，为了保持接口一致仍返回字典
        name_file_dict = {}
        os.chdir(folderpath)
        for root, dirs, files in os.walk(folderpath):
            for i in files:
                fp = os.path.join(root, i)  # 合成文件绝对路径
                fb = None
                name_file_dict[fp] = fb  # 组装绝对路径和文件流为字典
        log.info(name_file_dict)
        return name_file_dict

    def start_check(self, import_type: str, import_path: str):
        md5s = None
        if not import_type:
            log.error('please select the right import type, then try again.')
        else:
            if import_type is 'string':
                pass
            else:
                if not os.path.exists(import_path):
                    log.error('please select the right file or folder path, then try again.')
                else:
                    if import_type is 'file':
                        md5s = self.checkfile(import_path)
                    elif import_type is 'folder':
                        md5s = self.checkfolder(import_path)
                    elif import_type is 'zip':
                        md5s = self.checkzip(import_path)
                    elif import_type is 'rar':
                        md5s = self.checkrar(import_path)
                    # elif import_type is '7z':    # 暂不支持
                    #     pass
                    else:
                        log.error('the selected file is not supported, please check.')
        # log.info(md5s)
        # print('\n', import_type, path)
        print("\n********************MD5校验结果********************")
        print("模式：{}, 路径：{}".format(import_type, import_path))
        for k in sorted(md5s.keys()):
            # 必须进行排序，使得结果具有一致性。使用字典原因在于用控件换时间。
            print('{},{}'.format(k, md5s[k]))
        print("********************MD5校验结果********************\n")
        return md5s

    def walk_special_package(self, rootpath, filename):
        dic = self.lookfolder(rootpath)
        for k in sorted(dic.keys()):
            p, n = os.path.split(k)
            # for ver in ['6_0_7', '6_0_3']:  # 71Y 6.0.3通用版，6.0.7永康玻璃杯版
            for ver in ['6_0_9']:  # 71Y 6.0.9版本
                # for ver in ['6.4.0', '6_4_0', '6.4_0', '6_4.0']:  # 61Y 6.4.0通用版
                # for ver in ['6.4.18']:  # 61Y 6.4.18通用版
                if ver in p:
                    if n == filename:  # 只针对特定压缩包文件进行读取压缩文件列表计算MD5
                        print('\n', k)
                        self.start_check('zip', k)

if __name__ == '__main__':
    check = FileCheck()
    # check.checkfile(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    # check.start_check("file", r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    # check.checkfolder(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s")
    # check.start_check("folder", r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s")
    # check.checkzip(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    # check.start_check("zip", r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    p1 = r"Z:\MyworkSpace\pythonwork\Temp\OEM镜像对比\OEM_通用-productfile.osf"
    p2 = r"Z:\MyworkSpace\pythonwork\Temp\OEM镜像对比\OEM_科源-productfile.osf"
    logofile = "Z:\MyworkSpace\pythonwork\Temp\OEM镜像对比\logo.NTB"
    codeoemfile = "Z:\MyworkSpace\pythonwork\Temp\OEM镜像对比\codeoem.dat"