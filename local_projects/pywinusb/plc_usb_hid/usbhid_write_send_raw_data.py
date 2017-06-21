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
        print(ctime(),[hex(item) for item in data[1:]])

    def write(self, send_list):
        if self.device:
            if self.report:
                self.report[0].set_raw_data(send_list)
                bytes_num = self.report[0].send()
                return bytes_num


hid_name = 'PLC USB HID VER1'
myhid = MYUSBHID(hid_name)
myhid.start()

def read_hid():
    while myhid.alive:
        myhid.setcallback()

def control_hid():
    send_list = [0x00 for i in range(64)]
    for i in range(1):
        if i == 0 :
        #     send_list[1:3] = [0X01, 0x00, 0x05]
        # elif i == 1 :
            send_list[1:15] = [0x0d,0x00,0x02,0x45,0x30,0x30,0x30,
                               0x45,0x30,0x32,0x30,0x32,0x03,0x45,0x31]
        # elif i == 2:
        #     send_list[1:15] = [0x0d,0x00,0x02,0x45,0x30,0x30,0x30,
        #                        0x45,0x43,0x41,0x30,0x32,0x03,0x30,0x33]
        myhid.write(send_list)
        sleep(2)


threads = []
t1 = threading.Thread(target=read_hid, args=())
threads.append(t1)
t2 = threading.Thread(target=control_hid, args=())
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    myhid.stop()
    print('end at {}'.format(ctime()))
