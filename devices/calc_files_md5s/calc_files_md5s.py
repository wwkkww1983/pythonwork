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


def cal_md5(fileb, nbyte=65536):
    # 针对‘file'类型输入
    md5 = hashlib.md5()
    while True:
        current_bytes = fileb.read(nbyte)
        if current_bytes:
            md5.update(current_bytes)
        else:
            fileb.close()
            break
    return md5.hexdigest()


def defile(filepath:str):
    try:
        f = open(filepath, 'rb')
        return {filepath: f}
    except Exception as e:
        log.error(e)
        return {}


def defolder(folderpath:str):
    name_file_dict = {}
    os.chdir(folderpath)
    for root, dirs, files in os.walk(folderpath):
        for i in files:
            fp = os.path.join(root, i)
            fb = open(fp, 'rb')
            fpp = fp[len(folderpath):]    # 截去相对路径
            name_file_dict[fpp] = fb   # 组装相对路径和文件流为字典
    log.info(name_file_dict)
    return name_file_dict


def dezip(zippath:str):
    name_file_dict = {}
    zip = zipfile.ZipFile(zippath)
    for name in zip.namelist():
        fb = zip.open(name, 'rU')    # f为byte类型
        name_file_dict[name.encode('cp437').decode('gbk')] = fb    # 骚操作，先按zip文件名编码方式还原后再用gbk解码
    return name_file_dict


def derar(zippath:str):
    name_file_dict = {}
    rar = rarfile.RarFile(zippath)
    for name in rar.namelist():
        fb = rar.open(name, 'rU')    # f为byte类型
        name_file_dict[name] = fb
    return name_file_dict


def calc_files_md5s(name_file_dic:dict):
    md5s = {}
    for key in name_file_dic:
        md5s[key] = cal_md5(name_file_dic[key])
    # log.info(md5s)
    return md5s


def main(import_type:str, path:str):
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
                    nd = defile(path)
                    md5s = calc_files_md5s(nd)
                elif import_type is 'folder':
                    nd = defolder(path)
                    md5s = calc_files_md5s(nd)
                elif import_type is 'zip':
                    nd = dezip(path)
                    md5s = calc_files_md5s(nd)
                elif import_type is 'rar':
                    nd = derar(path)
                    md5s = calc_files_md5s(nd)
                # elif import_type is '7z':    # 暂不支持
                #     pass
                else:
                    log.error('the selected file is not supported, please check.')
    # log.info(md5s)
    print('\n', import_type, path)
    for k in sorted(md5s.keys()):
        # 必须进行排序，使得结果具有一致性。使用字典原因在于用控件换时间。
        print('{}, {}'.format(k, md5s[k]))
    return md5s

if __name__ == '__main__':
    main('file', 'productfile.osf')
    main('zip', 'calc_files_md5s.zip')
    main('folder', '.')
    main('file', 'G:\STEP7_V54_SP4_Chin_PftW.zip')
    main('zip', 'G:\STEP7_V54_SP4_Chin_PftW.zip')

