#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: mylog
# Author:    fan
# date:      2019/1/28
# -----------------------------------------------------------


def mylog(linedata: str, filename="log.txt", writeway="a"):
    with open(filename, writeway, encoding="utf-8") as f:
        print(linedata)
        f.write(linedata + "\n")


if __name__ == '__main__':
    pass
