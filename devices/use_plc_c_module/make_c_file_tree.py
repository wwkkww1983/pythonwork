#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: make_c_file_tree
# Author:    fan
# date:      2018/3/14
# -----------------------------------------------------------
import os
import shutil


def make_c_file_tree():
    c_dir = r'E:\Redmine\_20180123 PLC CModule\提交\编译器\CBlock_测试代码\c_struc'
    pkg_dir = r'E:\Redmine\_20180123 PLC CModule\提交\编译器\CBlock_测试代码\topack'
    os.chdir(c_dir)
    fun_dirs = []
    for name in os.listdir(c_dir):
        if os.path.isfile(name) and (name[-2:] in ['.c']):
            tempdirname = os.path.splitext(name)[0]
            if tempdirname not in fun_dirs:
                fun_dirs.append(tempdirname)
                target_dir = os.path.join(pkg_dir, tempdirname)
                os.mkdir(target_dir)
                source_path = os.path.join(c_dir, name)
                shutil.copy(source_path, target_dir)
if __name__ == '__main__':
    pass
