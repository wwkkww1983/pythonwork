#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     setup.py
# Description :
#   Author:      fan
#   date:        2018/1/8
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from distutils.core import setup
import py2exe
import sys
# this allows to run it with a simple double click.

# setup(console=['ui_dialog.py'])
setup(windows=[{"helloworkd.py"}], options={"py2exe":{"includes":["sip"]}})


if __name__ == '__main__':
    pass
