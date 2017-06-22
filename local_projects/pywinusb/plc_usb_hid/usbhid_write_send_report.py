# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
from time import ctime, sleep
import logging as log
import threading
from crccheck.checksum import Checksum8
from struct import unpack, pack
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

class MYUSBHID(object):
    def __init__(self, name):
        self.alive = False
        self.device = None
        self.report = None
        self.name = name
        self.readbuffer = None

    def start(self):
        _filter = hid.HidDeviceFilter(product_name=self.name)
        hid_device = _filter.get_devices()
        if len(hid_device) > 0:
            self.device = hid_device[0]
            self.device.open()
            log.info('hid device opened:{}'.format(self.device.product_name))
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
        self.readbuffer = None
        # print('received={}'.format([hex(item) for item in data[1:]]))
        # data_ = [hex(item) for item in data[1:]]
        log.info('received:lengh={}, data={}'.format(len(data), data))
        self.readbuffer = data
        return data

    def write(self, data):
        result = None
        if self.device:
            result = self.device.send_output_report(data)
        return result

    def pack_data_list(self, _relative=6000, _word_len=1, _data=None, _func='read'):
        """
        将数据组装为usb传输用数据
        :param _relative: D0偏移字（内部计算转换成字节数），字
        :param _word_len: read/write数据长度，字
        :param _data: 读取或写入数据，字节 写入用
        :param _func: 操作类型：read/write
        :return: 待传输字节串
        """
        head = [0x0d, 0x00]
        stx = [0x02]
        etx = [0x03]
        # 起始标识，结束标识

        func_code = {'read': [0x45, 0x30, 0x30], 'write': [0x45, 0x31, 0x30]}[_func]
        # 读写功能码，3 bytes

        d0_int = 0x4000
        d8000_int = 0x0E00
        # 读写起始地址，4_bytes list
        strt_addrs_str = ''
        if _relative in range(6000, 6032):
            strt_addrs_str = '{:#06X}'.format(_relative * 2 + d0_int)
        elif _relative in range(8000, 8255):
            strt_addrs_str = '{:#06X}'.format((_relative - 8000) * 2 + d8000_int)
        start_address = [ord(letter) for letter in strt_addrs_str][2:]

        lengh = []
        # 读写长度 2_bytes list
        if _word_len in range(1, 32):
            len_str = '{:#04X}'.format(_word_len * 2)
            lengh = [ord(letter) for letter in len_str][2:]

        checksum = []
        # 校验和，1 bytes。功能码、起始地址、数据和结束标识参与校验，起始标识不校验
        check = Checksum8()
        if lengh:
            checksum_int = check.calc(func_code + start_address + lengh + etx)
            checksum_str = '{:#04X}'.format(checksum_int)
            checksum = [ord(letter) for letter in checksum_str][2:]

        # 写入数据长度
        data = []
        if func_code == 'write':
            data = []  # 格式化数据
        else:
            data = []

        log.info("the follow parameter packed:"
                 "stx: {0}: "
                 "function code: {1}; "
                 "start address: {2}; "
                 "data lengh: {3};"
                 "write data: {4}; "
                 "etx: {5}; "
                 "check sum: {6}".format(stx, func_code, start_address, lengh, _data, etx, checksum))

        # 待发送数据list
        _data_list = []
        if _func == 'read':
            _data_list = head + stx + func_code + start_address + lengh + etx + checksum
        elif _func == 'write':
            _data_list = head + stx + func_code + start_address + lengh + data + etx + checksum
        return _data_list

    def unpack_data_list(self, _data_list):
        """
        从hid回调数据中获取有效数据并解析。后续读固定长度数据，数字板：64，模拟板：32
        :param _data_list:
        :return:
        """
        lenth = _data_list[1]
        useful_data = _data_list[4: lenth]
        # useful_data = [48, 70, 54, 50]  # 单字的情况+
        data_chr_list = [chr(i) for i in useful_data]
        data_int_list = []
        for s in range(len(data_chr_list)):
            if s % 2 == 0:
                a = int((data_chr_list[s] + data_chr_list[s + 1]), 16)
                data_int_list.append(chr(a).encode('ascii'))
            else:
                pass

        data_int = unpack('<h', bytes(b''.join(data_int_list)))

        print(data_int)
        return data_int

if __name__ == '__main__':
    log.info('usb hid start at {}'.format(ctime()))

    hid_name = 'PLC USB HID VER1'
    # hid_name = 'DIGITAL MODULE VER1'
    # hid_name = 'ANALOG MODULE VER1'


    data1 = [0x05, 0xff, 0x55, 0x53, 0x42, 0x45, 0x41, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    data2 = [0X01, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    data3 = [0x0d, 0x00, 0x02, 0x45, 0x30, 0x30, 0x30, 0x45,
             0x30, 0x32, 0x30, 0x32, 0x03, 0x45, 0x31]
    data4 = [0x0d, 0x00, 0x02, 0x45, 0x30, 0x30, 0x30, 0x45,
             0x43, 0x41, 0x30, 0x32, 0x03, 0x30, 0x33]

    myhid = MYUSBHID(hid_name)
    usb_data = myhid.pack_data_list(_relative=8001)

    # log.info('data={}'.format(data))
    myhid.start()

    def read_hid():
        while myhid.alive:
            myhid.setcallback()

    def control_hid(*useful_data):
        send_list = [0x00 for i in range(65)]
        send_list[1:16] = useful_data
        log.info('send list: lenth={},data={}'.format(len(send_list), send_list))
        result = myhid.write(send_list)
        log.info('send result={}'.format(result))


    threads = []
    t1 = threading.Thread(target=read_hid, args=())
    threads.append(t1)
    t2 = threading.Thread(target=control_hid, args=usb_data)
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    data = myhid.unpack_data_list(_data_list=myhid.readbuffer)
    log.info('unpack data={}'.format(data))
    myhid.stop()
    log.info('usb hid end at {}'.format(ctime()))
