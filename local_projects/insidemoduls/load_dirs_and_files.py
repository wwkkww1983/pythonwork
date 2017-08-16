#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
遍历指定目录下的所有子目录和文件，并返回所有文件的完整文件路径
"""

import os, sys

def get_file_dirs(given_dir):
    list_of_file_names = []
    for each_path in os.listdir(given_dir):
        print(each_path)
        if os.path.isfile(each_path):
            print('step 1')
            file_path = os.path.abspath(each_path)
            print(file_path)
            list_of_file_names.append(file_path)
            print(file_path)
        if os.path.isdir(each_path):
            if os.listdir(each_path):
                get_file_dirs(each_path)
            else:
                pass
        else:
            pass
    print(list_of_file_names)
test_path = r'C:\Users\fan\Desktop'
get_file_dirs(test_path)


