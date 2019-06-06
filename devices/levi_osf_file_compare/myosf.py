#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: myosf
# Author:    fan
# date:      2019/5/22 022
# -----------------------------------------------------------

from zipfile import ZipFile
import os
import hashlib
import json


def log(*lines):
    sl = []
    for i in lines:
        si = "{}".format(i)
        sl.append(si)
    print(" ".join(sl))


class MyOsf(ZipFile):

    def do(self, file):
        print(file)

    def get_num_of_files(self):
        return len(self.namelist())

    def get_file_list(self):
        return self.namelist()

    def get_file_md5(self, filename):
        md5 = None
        try:
            fb = self.open(filename, 'rU')
            md5 = self.calc_md5(fb)
        except Exception as e:
            print(e)
        return md5

    def get_files_md5_dic(self):
        md5dic = dict()
        for filename in self.get_file_list():
            md5dic[filename] = self.get_file_md5(filename)
        return md5dic

    def print_files_md5_dic(self):
        dic = self.get_files_md5_dic()
        for i in sorted(dic):
            print(i, dic[i])

    def compare_all_files(self, targetosfpath):
        pass

    def compare_one_file(self, filename, targetfilepath):
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


def get_all_osfs(topdir):
    """
    在目录里获取所有productfile.osf
    :param topdir: 目标文件夹
    :return: productfile.osf路径列表
    """
    l = []
    os.chdir(topdir)
    for dirpath, dirnames, filenames in os.walk(topdir):
        if 'backup' not in dirpath and '串口下载-特殊版' not in dirpath:  # 不处理历史和特殊版本
            for fn in filenames:
                if fn.lower() == "productfile.osf":
                    fp = os.path.join(dirpath, fn)  # 合成文件绝对路径
                    l.append(fp)
    print("目标productfile.osf路径: {}".format(topdir))
    # for p in l:
    #     print(p)
    return l

def compare_special_file_in_osf(srcfile, tgtosf):
    assert os.path.isfile(srcfile)
    assert os.path.isfile(tgtosf)
    filedir, filename = os.path.split(srcfile)
    tgt = MyOsf(tgtosf)
    md5_tgt = tgt.get_file_md5(filename)
    with open(srcfile, 'rb') as f:
        md5_src = tgt.calc_md5(f)
    checksuccess = ""
    print("**************** start ****************")
    print("左：{}".format(srcfile))
    print("右：{}".format(tgtosf))
    if md5_src == md5_tgt:
        checksuccess = "是"
    else:
        checksuccess = "否"
    print("文件名,文件1MD5,文件2MD5,是否一致")
    print("{},{},{},{}".format(filename, md5_src, md5_tgt, checksuccess))
    print("**************** end ****************\n")


def get_path_pairs(mark_strs, dir_src, dir_tgt):
    """
    获取两个对比目录相同型号的路径“对”
    :param mark_str:相同的路径标志，一对路径区分于其他对的字符串
    :param dir_src:源路径
    :param path_tgt:目标路径
    :return: 以mark_str为键的字典
    """
    files_src = get_all_osfs(dir_src)
    files_tgt = get_all_osfs(dir_tgt)
    hmitypes = []
    for i in files_src:
        pa, filename = os.path.split(i)
        unusestr, nuc = os.path.split(pa)
        hmi = '_'.join(nuc.split("_")[:-2])
        if hmi == '':
            hmi = nuc
        hmitypes.append(hmi)
        # log(key_word)
    path_pairs = dict()
    for hmi in hmitypes:
        # print(hmi)
        path_pairs[hmi] = {"source": None, "target": None}
    print("源镜像个数{}".format(len(path_pairs)))
    # log(json.dumps(path_pairs))
    for fns in files_src:
        for hmitype in hmitypes:
            if hmitype in fns:
                path_pairs[hmitype]["source"] = fns
    for fnt in files_tgt:
        for hmitype in hmitypes:
            if hmitype in fnt:
                path_pairs[hmitype]["target"] = fnt
    # log(json.dumps(path_pairs))
    return path_pairs


def compare_all_files_in_osfs(leftosf, rightosfs):
    osf1 = MyOsf(leftosf)
    dic1 = osf1.get_files_md5_dic()
    l1 = sorted(dic1.keys())
    for osf in rightosfs:
        osf2 = MyOsf(osf)
        dic2 = osf2.get_files_md5_dic()
        print("\n**************** start ****************")
        print("左：{}".format(leftosf))
        print("右：{}".format(osf))
        l2 = sorted(dic2.keys())
        if len(l1) != len(l2):
            print("镜像包内文件列表不一致：{}:\n{}\n{}:\n{}".format(leftosf, l1, osf, l2))
        else:
            print("文件名,文件1MD5,文件2MD5,是否一致")
            for k in sorted(dic1.keys()):
                if True:
                    if k == "os.ents":
                        if k in dic2.keys():
                            if dic1[k] == dic2[k]:
                                comparesuccess = "是,右边是ents"
                            else:
                                comparesuccess = "否,右边是ents"
                            print("{},{},{},{}".format(k, dic1[k], dic2[k], comparesuccess))
                        else:
                            if "os.dnts" in dic2.keys():
                                comparesuccess = "否,右边是dnts"
                                print("{},{},{},{}".format(k, dic1[k], dic2["os.dnts"], comparesuccess))
                            else:
                                print("os文件不存在，请重点检查")
                    else:
                        if dic1[k] == dic2[k]:
                            comparesuccess = "是"
                        else:
                            comparesuccess = "否"
                        if k == "codeoem.dat":
                            dat = osf2.open(k, 'rU')
                            lines = dat.readlines()
                            line1 = lines[0].decode(encoding='utf-8').strip()
                            line2 = lines[1].decode(encoding='utf-8').strip()
                            comparesuccess = ' '.join([comparesuccess, ',右边', line1, line2])
                        print("{},{},{},{}".format(k, dic1[k], dic2[k], comparesuccess))
        print("**************** end ****************")

def mission_compare():
    srcpaths = [normal, oem, unicode, oemunicode, stype]
    tgtpaths = [normal_71y, oem_71y, unicode_71y, oemunicode_71y, stype_71y]
    # get_path_pairs(strs, src, tgt)
    # get_all_osfs(oem)
    for src, tgt in zip(srcpaths, tgtpaths):
        path_pairs = get_path_pairs('', src, tgt)
        for key in path_pairs:
            if path_pairs[key]["target"]:
                target = [path_pairs[key]["target"]]
                compare_all_files_in_osfs(path_pairs[key]["source"], target)


if __name__ == '__main__':
    # targetosfs = []
    # osfpath = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用\NUC972_2070_通用_6.4.18_2019-01-23\productfile.osf"
    # osfpath1 = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_6.4.18\NUC972_2070S_OEM_6.4.18_2019-01-23\productfile.osf"
    # targetosfs.append(osfpath1)
    # targetosfs = get_all_osfs(r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用")
    # compare_all_files_in_osfs(osfpath, targetosfs)
    normal = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用"
    normal_71y = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\通用"
    oem = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\OEM"
    oem_71y = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\OEM"
    unicode = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\Unicode_通用"
    unicode_71y = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\Unicode_通用"
    oemunicode = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\Unicode_OEM"
    oemunicode_71y = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\Unicode_OEM"
    stype = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\标准S机型"
    stype_71y = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\标准S机型"
    srcpaths = [unicode, oemunicode]
    tgtpaths = [unicode_71y, oemunicode_71y]
    # special_file = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\通用\common\os.dnts"
    special_file = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\OEM\common\HMITerm_ARM7.nte"
    special_file = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_NUC972DF71Y_LEVI\Unicode_通用\common\HMITerm_ARM7.nte"
    # for tgtpath in tgtpaths:
    #     osfs = get_all_osfs(tgtpath)
    #     for osf in osfs:
    #         compare_special_file_in_osf(special_file, osf)
    l = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_6.4.18\NUC972_2043T_OEM_6.4.18_2019-01-23\productfile.osf"
    r = r"E:\Redmine2019\LEVIOEM测试\测试 #9312 伟创OEM 2043T镜像测试\NUC972_2043T_OEM伟创_6.4.18_2019-01-23\productfile.osf"
    compare_all_files_in_osfs(l, [r])



