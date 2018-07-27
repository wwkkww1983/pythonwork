#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: set
# Author:    fan
# date:      2018/7/25
# -----------------------------------------------------------
# 在 C:\Python34\Lib\site-packages\MY_MODULE_PATH.pth 文件中添加当前目录即可在所有项目中自由引用
import os, sys
pth_file = ""
sys.path =    ['E:\\MyWorkPlace\\pythonwork\\My_Module',
               'C:\\Windows\\system32\\python34.zip',
               'C:\\Python34\\DLLs',
               'C:\\Python34\\lib',
               'C:\\Python34',
               'C:\\Python34\\lib\\site-packages',
               'C:\\Python34\\lib\\site-packages\\win32',
               'C:\\Python34\\lib\\site-packages\\win32\\lib',
               'C:\\Python34\\lib\\site-packages\\Pythonwin']
self_module_path = os.path.abspath(".")
if self_module_path not in sys.path:
    sys.path.append(self_module_path)
else:
    pass
if __name__ == '__main__':
    print(sys.path)
