#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: print_act
# Author:    fan
# date:      2019/09/06
# -----------------------------------------------------------
import sys
import time


def print_act(s):
    sys.stdout.write("\r")
    sys.stdout.write("程序关闭倒计时：" + s + "（秒），请确认所有数据已正常保存。")
    sys.stdout.flush()
    time.sleep(1)


if __name__ == '__main__':
    i = 10
    while i >= 0:
        print_act(str(i))
        i = i - 1
