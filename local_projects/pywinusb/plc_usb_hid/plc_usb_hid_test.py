#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
import time
import logging as log

log.basicConfig(level=log.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# target_product_name = 'RAPOO GAMEPAD-X (Controller)'
# target_product_id = 0x045e
# target_vendor_id = 0x028e
target_product_name = u'PLC USB HID VER1'
target_product_id = 0x5750
target_vendor_id = 0x0483

def raw_data(line_one):
    data = []
    if len(line_one) !=16:
        log.error('data lengh(current value {}) must be 16'.format(len(line_one)))
    else:
        data_head_16 = line_one
        data_last_49 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        data = data_head_16 + data_last_49
        log.info('data:{}'.format(data))
        return data

def find_hid(name=u'PLC USB HID VER1'):
    all_devices = hid.HidDeviceFilter(target_product_name=name).get_devices()
    if not all_devices:
        log.error('no hid decice {} was found'.format(name))
    else:
        device = all_devices[0]
        if not device:
            print(u'已找到名为%s的USB HID设备，但无法使用' % target_product_name)
        else:
            return device

def read(data):
    print([hex(item).upper() for item in data[1:]])

if __name__ == '__main__':
    hid_device = find_hid()
    line = [0x00, 0x0d, 0x00, 0x02,  0x45, 0x30, 0x30, 0x30, 0x45, 0x30, 0x32, 0x30,  0x32, 0x03, 0x45, 0x31]
    data = raw_data(line)
    if hid_device:
        try:
            hid_device.open()
            # hid_device.send_output_report(data)

            # report = hid_device.find_output_reports()
            # report[0].set_raw_data(data)
            # report[0].send()
            write_result = hid_device.send_output_report(data)
            log.info('write result={0} lengh={1} data={2}'.format(write_result,len(data),data))
            print(' Write OK = ', write_result, '\n', 'write data: ', data, '\n', 'length: ', len(data))
            time.sleep(.05)
            hid_device.close()
        except AttributeError:
            print('HID设备打开失败，请确认设备未被占用后重试')