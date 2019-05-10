#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: ping_server
# Author:    fan
# date:      2019/4/29 029
# -----------------------------------------------------------
import os
import re
import time
from make_time_formated import nowtimestr


if __name__ == '__main__':
    ip = 'mqtt.v-box.net'
    # s = input("请输入ping指令目标ip(默认测试指令为ping {} -n 1):".format(ip))
    print("""
    This is a little tool to monitor network connectivity by running a single "ping" command.
It will log some returned info to a .log file in current folder when started.
    """)
    s = input("Please type the domain or IP address to ping to(default, {}) and press ENTER to start:".format(ip))
    if s == "":
        ping = "ping {} -n 1".format(ip)
    else:
        ping = "ping {} -n 1".format(s)
    with open("{}.log".format(ping), 'w', encoding='utf-8') as f:
        f.write(ping+'\n'+'start time: {}\n'.format(nowtimestr()))
    print('command: {}'.format(ping))
    print('start time: {}'.format(nowtimestr()))
    while True:
        try:
            time.sleep(5)
            file = os.popen(ping)
            log = ""
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line == '请求超时。' or line == 'Request timed out.':
                    log = "{}, 超时".format(nowtimestr()) if line == '请求超时。' else "{}, timed out.".format(nowtimestr())
                    print(log)
                    continue
                elif line.split(' ')[0] == '来自' or line.split(' ')[0] == 'Reply':
                    wordtomatch = r"时间.+ms" if line.split(' ')[0] == '来自' else r"time.+ms"
                    pat = re.compile(wordtomatch)
                    wordmatched = pat.findall(line)
                    # indexmatched = pat.finditer(line)
                    # print(wordmatched, list(indexmatched)[0].span())
                    # splitword = wordmatched[0][2]  # 获取时间数值前面是=或<或>，作为分隔符
                    print("{}, {}".format(nowtimestr(), wordmatched[0]))
                    log = "{}, {}".format(nowtimestr(), wordmatched[0])
                    lines = []
                    continue
                else:
                    continue
            with open("{}.log".format(ping), 'a', encoding='utf-8') as f:
                f.write(log + '\n')
        except Exception as e:
            print(e)

