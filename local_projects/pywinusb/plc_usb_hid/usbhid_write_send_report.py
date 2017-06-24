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

        # print('received={}'.format([hex(item) for item in data[1:]]))
        # data_ = [hex(item) for item in data[1:]]
        #
        self.readbuffer.append(data)
        log.info('received:lengh={}, data={}'.format(len(self.readbuffer), self.readbuffer))
        return self.readbuffer

    def write(self, data):
        result = None
        if self.device:
            result = self.device.send_output_report(data)
        return result

    def pack_write_data(self, _relative=6000, _word_len=1, _data=None, _func='read'):
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
        if _relative in range(6000, 6032) or range(0, 14):
            strt_addrs_str = '{:#06X}'.format(_relative * 2 + d0_int)
        elif _relative in range(8000, 8255):
            strt_addrs_str = '{:#06X}'.format((_relative - 8000) * 2 + d8000_int)
        start_address = [ord(letter) for letter in strt_addrs_str][2:]

        lengh = []
        # 读写长度 2_bytes list
        if _word_len in range(1, 33):
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
            _data_list = stx + func_code + start_address + lengh + etx + checksum
        elif _func == 'write':
            _data_list = stx + func_code + start_address + lengh + data + etx + checksum
        return _data_list

    def unpack_data_list(self, data_buffer):
        """
        从hid回调数据中获取有效数据并解析。后续读固定长度数据，
        :param _data_list: 无符号整型列表
        :param data_from: 数字板：64，模拟板：32
        :return:
        """

        buffer = data_buffer
        newdata = [0 for i in range(3)]
        newlen = 0

        # hid读回数据处理 ： 00
        for n in range(len(buffer)):
            newlen += buffer[n][1]
            newdata += buffer[n][3:buffer[n][1] + 3]
        newdata[:3] = [0, newlen, 2]
        log.info('new hid data: lengh={}, data={}'.format(newlen, newdata))
        # return newdata   # 获取hid数据
        digit_current_data = {}
        def get_digit_current_data(new_hid_data):
            if len(new_hid_data) == 135:
                used_data = new_hid_data[4:-3]
                data_chr_list = [chr(i) for i in used_data]
                data_int_list = []
                unpack_lengh = 128
                for s in range(unpack_lengh):
                    # if s % 2 == 0:
                    #     a = int((data_chr_list[s] + data_chr_list[s + 1]), 16)
                    #     data_int_list.append(chr(a).encode('ascii'))
                    if s % 4 == 0:
                        a = data_chr_list[s+2]+data_chr_list[s+3]+data_chr_list[s]+data_chr_list[s+1]
                        data_int_list.append(int(a, 16))
                    else:
                        pass
                # data_unsigned_int = unpack('<' + 'h' * (unpack_lengh//4), bytes(b''.join(data_int_list)))
                data_unsigned_int = data_int_list
                print(data_unsigned_int)
                return data_unsigned_int
        return get_digit_current_data(newdata)
        # return {'adc_8_data_dword': [0, 0, 0, 0, 0, 0, 0, 0],
        #         'test_point_value_int': [0, 0, 0, 0, 0, 0, 0, 0],
        #         # 'ch1_v24_int': 0,
        #         # 'ch1_i24_int': 0,
        #         # 'ch2_v15_int': 0,
        #         # 'ch2_i15_int': 0,
        #         # 'ch3_v-15_int': 0,
        #         # 'ch3_i-15_int': 0,
        #         # 'ch4_v5/7_int': 0,
        #         # 'ch4_i5/7_int': 0,
        #         'cali_param_int': [0, 0, 0, 0],
        #         'board_type_word': [0, 0],
        #         'power_up_flag_word': 0,
        #         'frame_ready_flag_word': 0
        #         }

if __name__ == '__main__':
    # hid_name = 'PLC USB HID VER1'
    hid_name = 'DIGITAL MODULE VER1'
    # hid_name = 'ANALOG MODULE VER1'
    myhid = MYUSBHID(hid_name)
    hid_send_data = myhid.pack_write_data(_relative=6000, _word_len=32)

    log.info('usb hid start at {}'.format(ctime()))
    myhid.start()

    def read_hid():
        while myhid.alive:
            myhid.setcallback()

    def control_hid(*write_data):
        # write_buffer = [0x00 for i in range(65)]
        # write_buffer[1:16] = write_data
        write_buffer = [0, 0xd, 0] + list(write_data) + [0x00 for i in range(49)]
        log.info('send list: lenth={},data={}'.format(len(write_buffer), write_buffer))
        myhid.readbuffer = []
        result = myhid.write(write_buffer)
        log.info('send result={}'.format(result))
        sleep(.05)  # 这里必须等待 使hid数据充分被读到
        receivedata = myhid.unpack_data_list(myhid.readbuffer)
        log.info('received new hid data={}'.format(receivedata))

    threads = []
    t1 = threading.Thread(target=control_hid, args=hid_send_data)
    threads.append(t1)
    t2 = threading.Thread(target=read_hid, args=())
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()
    sleep(2)
    myhid.stop()
    t.join()
    # data = myhid.unpack_data_list(_data_list=myhid.readbuffer)
    # log.info('unpack data={}'.format(data))
    log.info('usb hid end at {}'.format(ctime()))
