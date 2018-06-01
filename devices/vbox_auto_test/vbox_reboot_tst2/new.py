
#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: new
# Author:    fan
# date:      2018/6/1
# -----------------------------------------------------------
import win32api


def set_scrn_resol(width, height):
    # 利用win32api库修改屏幕分辨率
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsHeight = width
    dm.PelsWidth = height
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)

if __name__ == '__main__':
    set_scrn_resol(1366,768)
