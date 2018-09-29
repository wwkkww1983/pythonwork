#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: rewritescreenfile
# Author:    fanch
# date:      2018/09/27
# -----------------------------------------------------------

import os.path


def rewritehsc( hscpath, tagname:str, tagstart:int=0, tagfinish:int=99):
    """
    重写hsc画面文件，使用标签或者地址序列替换部件地址
    :param hscpath: hsc画面文件完整路径
    :param tagname: 标签名前缀
    :param tagstart: 标签起始于
    :param tagfinish: 标签结束于
    :return: 无返回
    """
    newf = []
    str1 = 'WordAddr="'
    str2 = '" Fast="0"'
    str3 = 'WriteAddr="'
    str4 = '" KbdScreen="'
    str5 = 'OperateAddr="'
    str6 = '" Fast="0"'
    str7 = 'MonitorAddr="'
    str8 = '" FigureFile="'
    wordtag = [tagname + str(i) for i in range(tagstart, tagfinish+1)]
    bittag = [tagname + str(i) for i in range(tagstart, tagfinish+1)]
    with open(hscpath, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if (str1 in line) and (str2 in line):
                locate1 = line.find(str1)
                locate2 = line.find(str2)
                if (str3 in line) and (str4 in line):
                    locate3 = line.find(str3)
                    locate4 = line.find(str4)
                    wordaddr = line[(locate1 + len(str1)):locate2]
                    print(wordaddr)
                    writeaddr = line[(locate3 + len(str1)):locate4]
                    print(writeaddr)
                    newline = line[0:(locate1 + len(str1))] \
                              + wordtag[0] \
                              + line[locate2:(locate3 + len(str3))] \
                              + wordtag[0] \
                              + line[locate4:]
                    wordtag.remove(wordtag[0])
                    print(newline)
                    newf.append(newline)
            elif (str5 in line) and (str6 in line):
                locate1 = line.find(str5)
                locate2 = line.find(str6)
                if (str7 in line) and (str8 in line):
                    locate3 = line.find(str7)
                    locate4 = line.find(str8)
                    operateaddr = line[(locate1 + len(str5)):locate2]
                    print(operateaddr)
                    monitoraddr = line[(locate3 + len(str5)):locate4]
                    print(monitoraddr)
                    newline = line[0:(locate1 + len(str5))] \
                              + bittag[0] \
                              + line[locate2:(locate3 + len(str7))] \
                              + bittag[0] \
                              + line[locate4:]
                    bittag.remove(bittag[0])
                    print(newline)
                    newf.append(newline)
            else:
                newf.append(line)
    hscdir, hscname = os.path.split(hscpath)
    new = os.path.join(hscdir, 'new')
    if os.path.exists(new):
        pass
    else:
        os.mkdir(new)
    with open(os.path.join(new, hscname), 'w', encoding='utf-8') as f:
        for line in newf:
            f.write(line)


if __name__ == '__main__':
    rewritehsc('0.hsc', 'M', 0, 9)
    rewritehsc('2.hsc', 'D', 0, 10)
