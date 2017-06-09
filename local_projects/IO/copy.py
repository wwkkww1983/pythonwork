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
      \t Chrome书签备份程序
      根据提示选择操作：
      \t 1 ------ 从OneDrive更新到本机浏览器书签
      \t 2 ------ 将本机浏览器书签备份到OneDrive
      \t quit --- 退出操作""")
      
while True:
    typeNum = input()
    if typeNum == '1':
        sourceFile = os.path.join(oneDriveDir, fileName)
        targetFile = os.path.join(chromeDir, fileName)
        break
    elif typeNum == '2':
        sourceFile = os.path.join(chromeDir, fileName)
        targetFile = os.path.join(oneDriveDir, fileName)
        break
    elif typeNum == 'quit':
        break
    else:
        print('值:', typeNum, '\n输入无效，请重新输入：\n')
        pass
print('sourceFile:\t', sourceFile, '\ntargetFile:\t', targetFile)
fr = open(sourceFile, 'rb')
readFileString = fr.read()
print(readFileString)
fw = open(targetFile, 'wb')
fw.write(readFileString)
fr.close()
fw.close()
