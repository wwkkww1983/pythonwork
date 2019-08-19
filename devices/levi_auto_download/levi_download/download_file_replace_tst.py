#!/usr/bin/python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: levi_downlaod.py
# Author:    fan
# date:      2019/8/14
# -----------------------------------------------------------
# 工程下载时并更新镜像时时屏内镜像文件替换过程随机断电导致重启找不到镜像从而屏启动失败
# 针对此过程建立测试脚本

from devices.levi_auto_download.levi_download.levi_download_cls import LeviDownload
from watchcom import *
import _thread as thread
import random


def get_random_secs(bottom, top):
    value = random.randint(bottom * 1000, top * 1000)
    return value / 1000


def is_hmi_booted_ok():
    port = set_port('com7', 9600, 7, 1, 'N')
    hmi_is_ready = read_correct(port,
                                b'\x01\x03\x00\x00\x00\x01\x04\n')
    return hmi_is_ready


def set_hmi_power_after_delay(flag, delay, state0or1):
    for i in range(5):
        time.sleep(1)
        if flag:
            break
    time.sleep(delay)
    port = set_port('com5', 9600, 7, 1, 'E')
    write_bit(port, "Y0", state0or1)


def loop():
    download = LeviDownload()
    download.open_download(exepth)
    download.config_download()
    while True:
        time.sleep(1)
        # if is_hmi_booted_ok():
        #     # 正常验证下载
        #     download.download_project(fpth)
        # time.sleep(15)  # 正常等待重启
        if is_hmi_booted_ok():
            # 模拟下载过程异常断电
            deylay_sec = 10 + get_random_secs(0, 10)  # 下载开始后多久采取下电操作
            thread.start_new_thread(set_hmi_power_after_delay, (download.downloading, deylay_sec, 0))
            download.download_project(fpth)
        if download.download_error:
            download.close_error_tip_win()
        set_hmi_power_after_delay(1, 0, 0)
        time.sleep(1)
        set_hmi_power_after_delay(1, 0, 1)
        time.sleep(15)


if __name__ == "__main__":
    exepth = r"D:\LeviStudio\Download.exe"
    fpth = r"D:\Levi下载测试\2070.ehmt"
    loop()
    # print(is_hmi_booted_ok())
    # set_hmi_power(1)
