#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
from time import ctime, sleep
import logging as log
import threading
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class MYUSBHID(object):
    def __init__(self, name):
        self.alive = False
        self.device = None
        self.report = None
        self.name = name

    def start(self):
        _filter = hid.HidDeviceFilter(product_name=self.name)
        hid_device = _filter.get_devices()
        if len(hid_device) > 0:
            self.device = hid_device[0]
            self.device.open()
            self.report = self.device.find_output_reports()
            self.alive = True

    def stop(self):
        self.alive = False
        if self.device:
            self.device.close()

    def setcallback(self):
        if self.device:
            self.device.set_raw_data_handler(self.read)

    def read(self, data):
        print(ctime(),[hex(item).upper() for item in data[1:]])

    def write(self, send_list):
        if self.device:
            if self.report:
                self.report[0].set_raw_data(send_list)
                bytes_num = self.report[0].send()
                return bytes_num

hid_name = 'PLC USB HID VER1'
myhid = MYUSBHID(hid_name)
myhid.start()

# myhid.start()
# if myhid.alive:
#     myhid.setcallback()
#     send_list = [0x00 for i in range(64)]
#     send_list[1:3] = [0X01, 0x00, 0x05]
#     myhid.write(send_list)
#     sleep(2)
#     myhid.stop()


def read_usb():
    while myhid.alive:
        myhid.setcallback()

def control_usb():

    send_list = [0x00 for i in range(64)]
    send_list[1:3] = [0X01, 0x00, 0x05]
    for i in range(100):
        myhid.write(send_list)
        sleep(.01)

threads = []
t1 = threading.Thread(target=read_usb, args=())
threads.append(t1)
t2 = threading.Thread(target=control_usb, args=())
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    myhid.stop()
    print('End at {}'.format(ctime()))



# device = hid.HidDeviceFilter(product_name=hid_name).get_devices()[0]
# log.info(hid.HidDevice)

# def hidusbread(data):
#     try:
#         temp_list = data[1:]
#         print(temp_list)
#         log.info(temp_list)
#     except Exception as e:
#         log.error(e)
#
#
# def read(_data):
#     return([hex(item).upper() for item in _data[1:]])
#
#
# if device:
#     try:
#         device.open()
#         report = device.find_output_reports()
#         liveflag = True
#         while liveflag:
#             temp_list = read()
#
#         device.set_raw_data_handler(hidusbread)
#     except Exception as e:
#         log.info(e)
