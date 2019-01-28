#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: com2_watching
# Author:    fan
# date:      2019/1/19
# -----------------------------------------------------------
from modbus_rtu_master import ModbusRtu
import time
from make_time_formated import nowtimestr
from watchcom import set_port, open_port, close_port, read_correct


hmiport = set_port('com9', 115200, 8, 1, 'N')
plcportporp = ("com7", 9600, 8, 1, "N")
plc = ModbusRtu(plcportporp)


flag_offline = b'ngrok-----[19 15:58:54]   ngrok-----' \
               b'err------------' \
               b'socklist.count(mainsock)!=0&&mainsock!=0   ---' \
               b'socklist.size = 0 \r\r\n'
flag_online = b'ngrok-----[19 16:00:12]   ngrok-----' \
              b'FD_ISSET( it1->first, &readSet )&&tempinfo->isconnect==1----' \
              b'tempinfo->istype=3  ---' \
              b'socklist.size = 2 \r\r\n'


def log(file: str, line: str, writeway="a"):
    with open(file, writeway, encoding="utf-8") as f:
        print(line)
        f.write(line + "\n")


def isonline(com: str, flag: bool):
    test_count = 0
    while test_count <= 5000:
        test_count += 1
        try:
            hmiport = set_port(com, 115200, 8, 1, 'N')
            s = hmiport.readline()
            if s:
                if b'ngrok-----' in s:
                    print(s)
                    l = s.strip().split(b"  ")
                    if len(l) == 3:
                        if l[1] == b' ngrok-----FD_ISSET( it1->first, &readSet )&&tempinfo->isconnect==1----' \
                                   b'tempinfo->istype=3':
                            if flag:
                                loginfo = l[0][-12:-1].decode() + " hmi online = True"
                                log(loginfo)
                                return 1
                        if l[1] == b' ngrok-----err------------socklist.count(mainsock)!=0&&mainsock!=0':
                            if not flag:
                                loginfo = l[0][-12:-1].decode() + " hmi online = False"
                                log(loginfo)
                                return 2
        except Exception as e:
            print("{} - read hmi port fail. testing stopped: {}".format(nowtimestr(), e))
            break
    return 0


def test(com, times, logfile):
    log("{} - test started.".format(nowtimestr()), "w")
    count = 0
    plc.write_coil(1, 0xfc00, 1)
    set_port(comid, 115200, 8, 1, 'N')
    while count <= times:
        count += 1
        x = isonline(com, True)
        if x is 1:
            logline = "{} - hmi online success. count = {}".format(nowtimestr(), count)
            log(logfile, logline)
            plc.write_coil(1, 0xfc00, 0)
            print("{} - hmi powered off".format(nowtimestr()))
        if x is 0:
            log("{} hmi online err.".format(nowtimestr()))
            break
        x = isonline(com, False)
        if x is 2:
            logline = "{} - hmi offline success. count = {}".format(nowtimestr(), count)
            log(logline)
            plc.write_coil(1, 0xfc00, 1)
            print("{} - hmi powered on".format(nowtimestr()))
        if x is 0:
            log("{} hmi offline err.".format(nowtimestr()))
            break
    log("{} - test finished.".format(nowtimestr()))

if __name__ == '__main__':
    ran = (20, 28)
    com_list = []
    for i in range(*ran):
        comid = "com" + str(i)
        com_list.append(comid)
    logfile_list = []
    for com in com_list:
        logfile = "log_{}.txt".format(com)
        logfile_list.append(logfile)
    print(com_list)
    print(logfile_list)
