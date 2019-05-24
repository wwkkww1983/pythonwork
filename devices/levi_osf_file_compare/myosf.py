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
    print("\n目标productfile.osf路径: ")
    for p in l:
        print(p)
    return l


def compare_all_files_in_osfs(osffile1, osffiles):
    osf1 = MyOsf(osffile1)
    dic1 = osf1.get_files_md5_dic()
    l1 = sorted(dic1.keys())
    for osf in osffiles:
        osf2 = MyOsf(osf)
        dic2 = osf2.get_files_md5_dic()
        print("\n**************** start ****************")
        print("左：{}".format(osffile1))
        print("右：{}".format(osf))
        l2 = sorted(dic2.keys())
        if l1 != l2:
            print("镜像包内文件列表不一致：{}:\n{}\n{}:\n{}".format(osffile1, l1, osf, l2))
        else:
            print("文件名,文件1MD5,文件2MD5,是否一致")
            for k in sorted(dic1.keys()):
                # if k == "defaultproject.zip.u":
                if True:
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


if __name__ == '__main__':
    targetosfs = []
    osfpath = r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用\NUC972_2070_通用_6.4.18_2019-01-23\productfile.osf"
    osfpath1 = r"E:\Redmine2019\LEVIOEM测试\OEM_通用_6.4.18\NUC972_2070S_OEM_6.4.18_2019-01-23\productfile.osf"
    targetosfs.append(osfpath1)
    targetosfs = get_all_osfs(r"\\192.168.11.20\hmi软件镜像\nuc972(V1.0 ~ V1.4)\组态_LEVI\通用")

    compare_all_files_in_osfs(osfpath, targetosfs)
