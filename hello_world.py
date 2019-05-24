#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hello_world
# Author:    fan
# date:      2019/5/14 014
# -----------------------------------------------------------
import sys


def main(someone):
    print("hello, {}.".format(someone))


if __name__ == '__main__':
    main(sys.argv[1])
