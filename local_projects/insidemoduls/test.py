#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
遍历指定目录下的所有子目录和文件，并返回所有文件的完整文件路径
"""

import os, sys

def get_file_dirs(given_dir):
    """定义函数获取给定目录下的所有文件名（不包含目录名），并添加到列表中"""
    list_of_file_names = []
    list_of_empty_dirs = []
    def findfiles(current_dir):
        """定义函数遍历所有子目录"""
        for each_path in os.listdir(current_dir):
            each_abspath = os.path.join(current_dir, each_path)
            """遍历当前一层目录并组装为绝对路径"""

            if os.path.isfile(each_abspath):
                list_of_file_names.append(each_abspath)
                """如果是文件，添加文件完整路径到列表中"""

            if os.path.isdir(each_abspath):
                    if os.listdir(each_abspath):
                        findfiles(each_abspath)
                    else:
                        list_of_empty_dirs.append(each_abspath)
                    """如果是目录，则调用函数本身"""

    findfiles(given_dir)
    return list_of_file_names, list_of_empty_dirs
test_path = r'C:\Users\fan\OneDrive\pythonwork\local_projects\insidemoduls\osmodulestest'
#test_path = r'C:\Users\fan\Desktop'

l = get_file_dirs(test_path)
print('\n在目录：', test_path, '\n存在的全部文件为：')
for i in l[0]:
    print(i)
print('\n在目录：', test_path, '\n存在的空目录为：')
for k in l[1]:
    print(k)



