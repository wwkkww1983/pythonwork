#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# @File Name: cmd_print
# @Author:    Fan
# @Date:      2020/2/9 0009 15:40
# @Content:   在命令行当前页面输出和刷新（区别于逐行输出）
# -----------------------------------------------------------

import time
import os
import sys
from curses import *


def single_line_refresh1(ind):
    if ind == 99:
        print("\r Loaded", end="\n")
    else:
        print("\r Now loading... {}%".format(str(ind)), end="")


def single_line_refresh2(ind):
    if ind == 99:
        sys.stdout.write("\rLoaded.\n")
        sys.stdout.flush()
    else:
        sys.stdout.write("\rNow loading... {}%".format(str(ind)))
        sys.stdout.flush()


def multi_lines_refresh():
    stdscr = initscr()

    stdscr.keypad(True)
    stdscr.box()
    time.sleep(5)


    stdscr.keypad(False)



if __name__ == '__main__':
    # h = ['|', '/', '-', '\\']
    # for i in range(100):
    #     time.sleep(0.2)
    #     single_line_refresh2(i)
    multi_lines_refresh()
