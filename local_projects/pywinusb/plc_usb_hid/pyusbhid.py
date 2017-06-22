#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
from time import sleep

all_devices = hid.HidDeviceFilter(product_name='PLC USB HID VER1').get_devices()
device = all_devices[0]
sendlist = [0x00 for i in range(64)]
sendlist[1:15] = [0x0d, 0x00, 0x02, 0x45, 0x30, 0x30, 0x30, 0x45, 0x30, 0x32, 0x30, 0x32, 0x03, 0x45, 0x31]
device.open()
sleep(0.5)
reports = device.find_output_reports()
reports[0].set_raw_data(sendlist)
reports[0].send()
device.close()
