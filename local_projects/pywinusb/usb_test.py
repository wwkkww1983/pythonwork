#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试pywinusb模块，连接LX 3VP验证USB HID协议帧格式
# 参考http://www.bkjia.com/Pythonjc/991533.html

import sys
import pywinusb.hid as hid

target_product_name = 'RAPOO GAMEPAD-X (Controller)'
target_product_id = 0x045e
target_vendor_id = 0x028e
# 雷柏X-Box手柄UID设备


def find_hid(name='', pid=0x0, vid=0x0):
    # 从系统中找到目标设备，通过product_name, product_id, vendor_id
    all_devices = hid.HidDeviceFilter(product_name=name).get_devices()
    # all_devices = hid.HidDeviceFilter(product_id=pid, vendor_id=vid).get_devices()
    # hid设备筛选器通过product_id, vendor_id选中设备

    if not all_devices:
        error = '未找到HID设备(name={0}, pid={0}, vid={1})'.format(name, pid, vid)
        print(error)
    else:
        device = all_devices[0]
        if not device:
            print(u'已找到名为%s的USB HID设备，但无法使用' % target_product_name)
        else:
            print(device)
            return device

device = find_hid(target_product_name, target_product_id, target_vendor_id)


def read(data):
    print([hex(item).upper() for item in data[1:]])

if device:
    while not input('\n'):
        device.set_raw_data_handler(read)

