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
            log.info('hid device closed:{}'.format(self.device.product_name))

    def setcallback(self):
        if self.device:
            self.device.set_raw_data_handler(self.read)

    def read(self, data):
        # print('received={}'.format([hex(item) for item in data[1:]]))
        log.info('received={}'.format([hex(item) for item in data[1:]]))

    def write(self, data):
        result = None
        if self.device:
            result = self.device.send_output_report(data)
        return result

hid_name = 'PLC USB HID VER1'
myhid = MYUSBHID(hid_name)
myhid.start()

def read_hid():
    while myhid.alive:
        myhid.setcallback()

def control_hid():
    # def send_list(data):

    send_list = [0x00 for i in range(65)]
    for i in range(4):
        sleep(0)
        if i == 0:
            send_list[1:16] = [0x05, 0xff, 0x55, 0x53, 0x42, 0x45, 0x41, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        if i == 1:
            send_list[1:16] = [0X01, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        if i == 2:
            send_list[1:16] = [0x0d, 0x00, 0x02, 0x45, 0x30, 0x30, 0x30, 0x45,
                               0x30, 0x32, 0x30, 0x32, 0x03, 0x45, 0x31]
        if i == 3:
            send_list[1:16] = [0x0d, 0x00, 0x02, 0x45, 0x30, 0x30, 0x30, 0x45,
                               0x43, 0x41, 0x30, 0x32, 0x03, 0x30, 0x33]

        log.info('send list: lenth={},data={}'.format(len(send_list), send_list))
        result = myhid.write(send_list)
        log.info('send result={}'.format(result))

threads = []
t1 = threading.Thread(target=read_hid, args=())
threads.append(t1)
t2 = threading.Thread(target=control_hid, args=())
threads.append(t2)

if __name__ == '__main__':
    log.info('usb hid start at {}'.format(ctime()))
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    myhid.stop()
    log.info('usb hid end at {}'.format(ctime()))
