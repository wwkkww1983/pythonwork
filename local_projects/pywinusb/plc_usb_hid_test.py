#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
import time


# target_product_name = 'RAPOO GAMEPAD-X (Controller)'
# target_product_id = 0x045e
# target_vendor_id = 0x028e
target_product_name = u'PLC USB HID VER1'
target_product_id = 0x5750
target_vendor_id = 0x0483

def data_list(line_str):
    list_int = []
    for num in line_str.split():
        list_int.append(int(num, 16))
    data_head_16 = list_int
    data_last_49 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data = data_head_16 + data_last_49
    return data

def find_hid(name='', pid=0x0, vid=0x0):
    # 从系统中找到目标设备，通过product_name, product_id, vendor_id
    # all_devices = hid.HidDeviceFilter(product_name=name).get_devices()
    all_devices = hid.HidDeviceFilter(product_id=pid, vendor_id=vid).get_devices()
    # hid设备筛选器通过product_id, vendor_id选中设备

    if not all_devices:
        print(u'未找到USB HID设备(product name = %s, product id = %s, vendor id = %s)' % (name, pid, vid))
    else:
        device = all_devices[0]
        if not device:
            print(u'已找到名为%s的USB HID设备，但无法使用' % target_product_name)
        else:
            return device

def read(data):
    print([hex(item).upper() for item in data[1:]])

if __name__ == '__main__':


    hid_device = find_hid('', target_product_id, target_vendor_id)
    # line_str = '00 01 00 05  00 00 00 00  00 00 00 00  00 00 00 00'
    line = '00 0d 00 02  45 30 30 30  45 30 32 30  32 03 45 31'
    data = data_list(line)
    if hid_device:
        try:
            hid_device.open()
            # hid_device.send_output_report(data)

            # report = hid_device.find_output_reports()
            # report[0].set_raw_data(data)
            # report[0].send()
            write_OK = hid_device.send_output_report(data)
            print(' Write OK = ', write_OK, '\n', 'write data: ', data, '\n', 'length: ', len(data))
            time.sleep(.05)
            hid_device.close()
        except AttributeError:
            print('HID设备打开失败，请确认设备未被占用后重试')

