#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: xmldomparsing
# Author:    fanch
# date:      2018/09/27
# -----------------------------------------------------------
from xml.dom.minidom import parse
import xml.dom.minidom
from time import sleep

newf = []
# with open('0.hsc', 'r') as f:
#     for line in f.readlines():
#         if not (('CharSize="' in line) and ('" WordAddr' in line)):
#             newf.append(line)
#         else:
#             locate1 = line.find('CharSize="')
#             locate2 = line.find('" WordAddr')
#             stx = line[(locate1+len('CharSize="')):locate2]
#             newline = line[0:(locate1+len('CharSize="'))] + 'iamfont' + line[locate2:]
#             # print(newline)
#             newf.append(newline)
# with open('0_.hsc', 'w') as f:
#     for line in newf:
#         f.write(line)


# DOMTree = xml.dom.minidom.parse('0_.hsc')
# collection = DOMTree.documentElement
# if collection.hasAttribute('ScreenNo'):
#     print('画面号：{}'.format(collection.getAttribute('ScreenNo')))
# parts = collection.getElementsByTagName("General")
# for part in parts:
#     if part.hasAttribute('WordAddr'):
#         part.set('WordAddr', 'D0')
#         print(part.getAttribute('WordAddr'))
#     if part.hasAttribute('WriteAddr'):
#         print(part.getAttribute('WriteAddr'))
#
# if __name__ == '__main__':
#     pass
