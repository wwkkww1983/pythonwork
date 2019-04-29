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
    s = input("请输入ping指令目标ip(默认测试指令为ping {} -n 1):".format(ip))
    if s == "":
        ping = "ping {} -n 1".format(ip)
    else:
        ping = "ping {} -n 1".format(s)
    with open("{}.log".format(ping), 'w', encoding='utf-8') as f:
        f.write(ping+'\n'+'start time: {}\n'.format(nowtimestr()))
    print(ping)
    print('start time: {}'.format(nowtimestr()))
    while True:
        try:
            time.sleep(5)
            file = os.popen(ping)
            log = ""
            lines = file.readlines()
            for line in lines:
                if line == '请求超时。\n':
                    print("{}, 超时".format(nowtimestr()))
                    log = "{}, 超时".format(nowtimestr())
                    continue
                elif line[:2] == '来自':
                    wordtomatch = r"时间.+ms"
                    pat = re.compile(wordtomatch)
                    wordmatched = pat.findall(line)
                    # indexmatched = pat.finditer(line)
                    # print(wordmatched, list(indexmatched)[0].span())
                    splitword = wordmatched[0][2]
                    print("{}, {}".format(nowtimestr(), wordmatched[0].split(splitword)[1]))
                    log = "{}, {}".format(nowtimestr(), wordmatched[0].split(splitword)[1])
                    lines = []
                    continue
                else:
                    continue
            with open("{}.log".format(ping), 'a', encoding='utf-8') as f:
                f.write(log + '\n')
        except Exception as e:
            print(e)

