# !/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
import time
import sys


def copy_record_files(srcedir, trgtdir, files):
    temp = '{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dirname = temp[:4]+temp[5:7] +temp[8:10]+temp[11:13]+temp[-2:]
    os.chdir(trgtdir)
    os.makedirs(dirname)
    trgtdir = os.path.join(trgtdir, dirname)
    if files:
        for file in files:
            srcefilepath = os.path.join(srcedir, file)
            trgtfilepath = os.path.join(trgtdir, file)
            
            with open(srcefilepath, 'rb') as sorce:
                f = sorce.read()
            with open(trgtfilepath, 'ab') as target:
                target.write(f)
            
if __name__ == '__main__' :
    source_dir = r'C:\Users\fan\AppData\Roaming\11bitstudios\This War Of Mine'
    target_dir = r'C:\Users\fan\Desktop\MyGamerecords'
    file1 = r'config.bin3'
    file2 = r'iPhoneProfiles'
    copy_record_files(source_dir, target_dir, [file1, file2])
    
    
#   格式化成2016-03-20 11:45:39形式
#   print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))