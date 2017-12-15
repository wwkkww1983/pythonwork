#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     communication_via_serial
# Description :
#   Author:      fan
#   date:        2017/12/13
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

from serial import Serial as ser
from fx_communication_protocol import LxPlcCom
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class FxCommSerial(object):
    def __init__(self, comid):
        self.com = None
        try:
            self.com = ser(comid)
        except:
            log.error('serial port {0} can\'t be used'.format(self.com.name))

    def reconfig(self, baud=9600, bytes=8, stops=1, parity='1', timeout=None):
        if self.com.is_open:
            try:
                self.com.baudrate = baud
                self.com.bytesize = bytes
                self.com.stopbits = stops
                self.com.parity = parity
                self.com.timeout = timeout
            except:
                log.error('config serial {} fail'.format(self.com.name))

    def write(self, data):
        if self.com.is_open:
            self.com.write(self, data)

    def read(self, datalengh):
        if self.com.is_open:
            self.com.read(self, size=datalengh)


if __name__ == '__main__':
    com = FxCommSerial('com1')
    com.reconfig(baud=115200, bytes=8, stops=1, parity='N', timeout=1)
    print(com.com)
