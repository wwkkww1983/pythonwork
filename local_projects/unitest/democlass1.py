#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: democlass1
# Author:    fan
# date:      2018/10/17
# -----------------------------------------------------------


class Demo(object):
    def __init__(self):
        # self.result = None
        pass

    def addstr(self, in1, in2, in3):
        if (type(in1) is str) and (type(in2) is str) and (type(in3) is str):
            # self.result = in1 + in2 + in3
            return in1 + in2 + in3

if __name__ == '__main__':
    inputs = ["input", "input2", "input3"]
    demo = Demo()
    # print(demo.addstr(*inputs))

