# -*- coding: utf-8 -*-
# from author: orangleliu  date: 2014-11-12
# python3.4 pingIP.py
 
"""
不同平台，实现对所在内网端的ip扫描
有时候需要知道所在局域网的有效ip，但是又不想找特定的工具来扫描。
使用方法 python ip_scaner.py 192.168.1.1
(会扫描192.168.1.1-255的ip)
"""
 
import platform
import sys
import os
import time
import _thread as thread
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


def get_os():
    '''
    get os 类型
    '''
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
     
    flag = False
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >=0:
            flag = True
            break
    if flag:
        print("ip: %s is ok ***"%ip_str)
        log.info('IP: {} is OK'.format(ip_str))


def find_ip():
    return '192.168.22.1'

if __name__ == "__main__":
    print("start time %s" % time.ctime())
    commandargs = sys.argv[1:]
    args = "".join(commandargs)    
     
    ip_prefix = '.'.join(args.split('.')[:-1])
    find_ip()
    print("end time %s"%time.ctime())
