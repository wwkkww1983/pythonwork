# !/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @author fan
# @version 2010-09-25 14:57

import os
import sys
import time

oneDriveDir = r""
chromeDir = r''
fileName = 'Bookmarks'
typeNum = ''
print("""\
********** Chrome书签备份程序 **********

请根据提示选择操作：

           1    > 从OneDrive更新到本机浏览器书签
          ------------------------------------------
           2    > 将本机浏览器书签备份到OneDrive
          ------------------------------------------
           3    > 退出操作
          ------------------------------------------""")
      
def fullDir(oneDir, chrDir, file):
    while True:
        typeNum = input()
        fuDir = []
        if typeNum == '1':
            source = os.path.join(oneDir, file)
            target = os.path.join(chrDir, file)
            fuDir = [source, target]
            return fuDir
        elif typeNum == '2':
            source = os.path.join(chrDir, file)
            target = os.path.join(oneDir, file)
            fuDir = [source, target]
            return fuDir
        elif typeNum == '3':
            fuDir = []
            return fuDir
        else:
            print('值:', typeNum, '\n输入无效，请重新输入：\n')
            pass
            
            
listPath = fullDir(oneDriveDir, chromeDir, fileName)    
if listPath:
    print('备份源:\t', listPath[0], '备份目标:\t', listPath[1])
    fr = open(listPath[0], 'rb')
    readFileString = fr.read()
    fw = open(listPath[1], 'wb')
    fw.write(readFileString)
    fr.close()
    fw.close()
