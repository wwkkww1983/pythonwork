#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: calc_files_md5s
# Author:    fan
# date:      2018/9/27
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
        print(md5dic)
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
        print(md5dic)
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
        print(md5dic)
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
        print(md5dic)
        return md5dic



    def calc_files_md5s(self, name_file_dic: dict):
        md5s = {}
        for key in name_file_dic:
            md5s[key] = self.calc_md5(name_file_dic[key])
        # log.info(md5s)
        return md5s

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

    def start_check(self, import_type:str, path:str):
        md5s = None
        if not import_type:
            log.error('please select the right import type, then try again.')
        else:
            if import_type is 'string':
                pass
            else:
                if not os.path.exists(path):
                    log.error('please select the right file or folder path, then try again.')
                else:
                    if import_type is 'file':
                        nd = self.defile(path)
                        md5s = self.calc_files_md5s(nd)
                    elif import_type is 'folder':
                        # nd = defolder(path)
                        # md5s = calc_files_md5s(nd)
                        md5s = self.defolder(path)
                    elif import_type is 'zip':
                        nd = self.dezip(path)
                        md5s = self.calc_files_md5s(nd)
                    elif import_type is 'rar':
                        nd = self.derar(path)
                        md5s = self.calc_files_md5s(nd)
                    # elif import_type is '7z':    # 暂不支持
                    #     pass
                    else:
                        log.error('the selected file is not supported, please check.')
        # log.info(md5s)
        # print('\n', import_type, path)
        for k in sorted(md5s.keys()):
            # 必须进行排序，使得结果具有一致性。使用字典原因在于用控件换时间。
            print('{},{}'.format(k, md5s[k]))
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

# def cal_md5(fileb, nbyte=65536):
#     # 针对‘file'类型输入
#     md5 = hashlib.md5()
#     while True:
#         current_bytes = fileb.read(nbyte)
#         if current_bytes:
#             md5.update(current_bytes)
#         else:
#             fileb.close()
#             break
#     return md5.hexdigest()
#

# def defile(filepath:str):
#     # 打开类型“文件”
#     try:
#         f = open(filepath, 'rb')
#         return {filepath: f}
#     except Exception as e:
#         log.error(e)
#         return {}
#
#
# def defolder(folderpath:str):
#     # 打开类型“文件夹”
#     name_file_dict = {}
#     os.chdir(folderpath)
#     for root, dirs, files in os.walk(folderpath):
#         for i in files:
#             fp = os.path.join(root, i)
#             with open(fp, 'rb') as fb:
#                 fbmd5 = cal_md5(fb)
#             fpp = fp[len(folderpath):]    # 截取相对路径作为字典键值
#             name_file_dict[fpp] = fbmd5   # 组装相对路径和文件流为字典
#     log.info(name_file_dict)
#     return name_file_dict
#
#
# def dezip(zippath:str):
#     # 打开类型“zip”
#     name_file_dict = {}
#     zip = zipfile.ZipFile(zippath)
#     for name in zip.namelist():
#         # if name == "os.ents":  # 只计算压缩包内某个文件的MD5
#         if True:
#             fb = zip.open(name, 'rU')    # f为byte类型
#             name_file_dict[name.encode('cp437').decode('gbk')] = fb    # 骚操作，先按zip文件名编码方式还原后再用gbk解码
#     return name_file_dict
#
#
# def derar(rarpath:str):
#     # 打开类型“RAR”
#     name_file_dict = {}
#     rar = rarfile.RarFile(rarpath)
#     for name in rar.namelist():
#         fb = rar.open(name, 'rU')    # f为byte类型
#         name_file_dict[name] = fb
#     return name_file_dict
#
#
# def calc_files_md5s(name_file_dic:dict):
#     md5s = {}
#     for key in name_file_dic:
#         md5s[key] = cal_md5(name_file_dic[key])
#     # log.info(md5s)
#     return md5s
#
#
# def lookfolder(folderpath: str):
#     # 打开类型“文件夹”,返回所有文件的绝对路径，本函数不需要用到文件流，为了保持接口一致仍返回字典
#     name_file_dict = {}
#     os.chdir(folderpath)
#     for root, dirs, files in os.walk(folderpath):
#         for i in files:
#             fp = os.path.join(root, i)    # 合成文件绝对路径
#             fb = None
#             name_file_dict[fp] = fb   # 组装绝对路径和文件流为字典
#     log.info(name_file_dict)
#     return name_file_dict


# def main(import_type:str, path:str):
#     md5s = None
#     if not import_type:
#         log.error('please select the right import type, then try again.')
#     else:
#         if import_type is 'string':
#             pass
#         else:
#             if not os.path.exists(path):
#                 log.error('please select the right file or folder path, then try again.')
#             else:
#                 if import_type is 'file':
#                     nd = defile(path)
#                     md5s = calc_files_md5s(nd)
#                 elif import_type is 'folder':
#                     # nd = defolder(path)
#                     # md5s = calc_files_md5s(nd)
#                     md5s = defolder(path)
#                 elif import_type is 'zip':
#                     nd = dezip(path)
#                     md5s = calc_files_md5s(nd)
#                 elif import_type is 'rar':
#                     nd = derar(path)
#                     md5s = calc_files_md5s(nd)
#                 # elif import_type is '7z':    # 暂不支持
#                 #     pass
#                 else:
#                     log.error('the selected file is not supported, please check.')
#     # log.info(md5s)
#     # print('\n', import_type, path)
#     for k in sorted(md5s.keys()):
#         # 必须进行排序，使得结果具有一致性。使用字典原因在于用控件换时间。
#         print('{},{}'.format(k, md5s[k]))
#     return md5s
#
#
# def walk_special_package(rootpath, filename):
#     dic = lookfolder(rootpath)
#     for k in sorted(dic.keys()):
#         p, n = os.path.split(k)
#         # for ver in ['6_0_7', '6_0_3']:  # 71Y 6.0.3通用版，6.0.7永康玻璃杯版
#         for ver in ['6_0_9']:  # 71Y 6.0.9版本
#         # for ver in ['6.4.0', '6_4_0', '6.4_0', '6_4.0']:  # 61Y 6.4.0通用版
#         # for ver in ['6.4.18']:  # 61Y 6.4.18通用版
#
#             if ver in p:
#                 if n == filename:  # 只针对特定压缩包文件进行读取压缩文件列表计算MD5
#                     print('\n', k)
#                     main('zip', k)

if __name__ == '__main__':
    # main('file', 'productfile.osf')
    # main('zip', r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用\NUC972_700ML_通用_6.3.96_2018-09-30\productfile.osf")
    check = FileCheck()
    check.checkfile(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    check.checkfolder(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s")
    check.checkzip(r"E:\MyWorkPlace\pythonwork\devices\calc_files_md5s\calc_files_md5s.zip")
    # check.checkrar(r"E:\免安装程序~\excutor.rar")  # 报错未解决

    #check.start_check('folder', r'D:\Program Files\WECONSOFT\LeviStudio\20190314发布测试2')
    # main('file', 'G:\STEP7_V54_SP4_Chin_PftW.zip')
    # main('zip', 'G:\STEP7_V54_SP4_Chin_PftW.zip')
    # while True:
    #     # 循环输入zip路径，打印zip内文件MD5
    #     p = input('输入文件路径，按回车开始校验：')
    #     if not p:
    #         continue
    #     else:
    #         if p[0] == '"':
    #             p = p[1:]
    #         if p[-1] == '"':
    #             p = p[:-1]
    #         if not os.path.exists(p):
    #             continue
    #         else:
    #             main('zip', p)
    # 61Y（64M存储版本生产镜像路径）
    # roots = [
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\OEM',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\Unicode_通用',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\Unicode_OEM'
    # ]
    # 71Y（128M存储版本生产镜像路径）
    # roots = [
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\通用',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\OEM',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\Unicode_通用',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\Unicode_OEM',
    #     r'\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\标准S机型\永康玻璃杯'
    # ]
    # name = 'productfile.osf'
    # for root in roots:
    #     print("\n", root)
    #     walk_special_package(root, name)

