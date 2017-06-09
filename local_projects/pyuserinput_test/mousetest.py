# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from pymouse import PyMouse as mouse
import time

p1 = (100, 100)
p2 = (100, 200)
p3 = (200, 200)
p4 = (200, 100)
p = (p1, p2, p3, p4)

def mouse_mov():
    mouse.move(0,100, 100)
    time.sleep(1)
    mouse.move(0,100, 200)
    time.sleep(1)
    mouse.move(0,200, 200)
    time.sleep(1)
    mouse.move(0,200, 100)
    time.sleep(1)

mouse_mov()

def mouse_click():
    mouse_mov()


