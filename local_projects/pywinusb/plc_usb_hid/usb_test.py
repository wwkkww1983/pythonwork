#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试pywinusb模块，连接LX 3VP验证USB HID协议帧格式
# 参考http://www.bkjia.com/Pythonjc/991533.html

import sys
import pywinusb.hid as hid

target_product_name = 'PLC USB HID VER1'
target_product_id = 0x5750
target_vendor_id = 0x0483
digit_link_name = 'DIGITAL MODULE VER1'
analog_link_name = 'ANALOG MODULE VER1'
plc_link_name = 'PLC USB HID VER1'
# 维控USB HID

def find_hids(pid=0x0, vid=0x0):
    # 从系统中找到目标设备，通过product_name, product_id, vendor_id
    all_devices = hid.HidDeviceFilter(product_id=pid, target_vendor_id=vid).get_devices()
    # all_devices = hid.HidDeviceFilter(product_id=pid, vendor_id=vid).get_devices()
    # hid设备筛选器通过product_id, vendor_id选中设备
    devices = []
    if not all_devices:
        error = '未找到HID设备(pid={0}, vid={1})'.format(pid, vid)
        print(error)
    else:
        for device in all_devices:
            if device.product_name == digit_link_name:
                digit_board = device
            elif device.product_name == analog_link_name:
                analog_board = device
            else:
                common_plc = device
        return {'digit board': digit_board, 'anolog board': analog_board, 'common plc': common_plc}

hid_devices = find_hids(target_product_id, target_vendor_id)



if __name__ == '__main__':
    for name in hid_devices:
        print('找到设备{0}:\n {1}'.format(name, hid_devices[name]))

