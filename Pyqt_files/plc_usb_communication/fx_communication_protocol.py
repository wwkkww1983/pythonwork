#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     fx_com_protocol
# Description :
#   Author:      fan
#   date:        2017/12/6
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
import logging as log
from crccheck.checksum import Checksum8
import random
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

# 申明（起始）地址类型
COM_ADDRESS = {'Y0': 0x0180,
               'X0': 0x0240,
               'M0': 0x0000,
               'M8000': 0x01C0,
               'C0_B': 0x01E0,
               'T0_B': 0x0200,
               'S0': 0x0280,
               'D0': 0x4000,
               'D8000': 0x0E00,
               'C0_W': 0x0A00,
               'C200_W': 0x0C00,
               'T0_W': 0x1000}

# 申明功能码类型
FUNC_CODE = {'read_words': 0xE00,
             'write_words': 0xE10,
             'read_bit': 0xE8,
             'write_bit': 0xE7,
             'test': 0x05}


class LxPlcCom(object):
    """
    协议对象，包括少数参数和绝大部分协议操作函数
    """
    def __init__(self):
        self.name = None
        self.mode = None
        self.start_add = None
        self.data = None
        self.read_lengh = None
        self.write_lengh = None
        self.stx_bytes = [0x02]
        self.etx_bytes = [0x03]

    def func_code_to_ascii(self, _func):
        """
        功能码转ascii码
        :param _func:
        :return:
        """
        return [ord(letter) for letter in hex(FUNC_CODE[_func]).upper()[2:]]

    def strt_addr_to_ascii(self, _strt_add):
        """
        读或写的起始地址转ascii码
        :param _strt_add:
        :return:
        """
        _type = _strt_add[0]
        _id = int(_strt_add[1:])
        strt_strt_add = None
        strt_addr_fmt = None
        if _type == 'd' or 'D':
            if 0 <= int(_id) <= 7999:
                strt_strt_add = COM_ADDRESS['D0']
            if 8000 <= int(_id) <= 8255:
                strt_strt_add = COM_ADDRESS['D8000']
                _id -= 8000
            strt_add_str = '{:#06X}'.format(_id * 2 + strt_strt_add)
            strt_addr_fmt = [ord(letter) for letter in strt_add_str][2:]
        return strt_addr_fmt

    def lengh_to_ascii(self, _len):
        """
        读或写的长度转ascii码
        :param _len:
        :return:
        """
        lengh_format = []
        # 读写长度 2_bytes list,注意A~F必须是大写的，否则会出错
        if _len in range(1, 33):
            len_str = '{:#04X}'.format(_len * 2)
            lengh_format = [ord(letter) for letter in len_str][2:]
        else:
            log.error('读写长度不能超过32，当前值={}'.format(_len))
        return lengh_format

    def data_value_to_ascii(self, _data):
        """
        写数据转ascii码
        :param _data: 字类型
        :return: 每一个字转为4个ascii字符
        """
        data_format = []
        for x in _data:
            if 0 <= x <= 32767:
                x_str1 = '{0:#06X}'.format(x)
            if -32767 < x < 0:
                x_str1 = '{0:#06X}'.format(x + 65536)
            x_str = x_str1[4:] + x_str1[2:4]
            data_format += [ord(letter) for letter in x_str]
        return data_format

    def checksum_to_ascii(self, *_each_list):
        """
        参与和校验运算的字节
        :param _each_list: stx之后（不包括stx），etx之前（包括etx）
        :return:
        """
        merge_bytes = []
        checksum_int = 0
        checksum_format = []
        for bytes in _each_list:
            merge_bytes += bytes
        checksum_int = Checksum8().calc(merge_bytes)
        checksum_str = '{:#04X}'.format(checksum_int)
        checksum_format = [ord(letter) for letter in checksum_str][2:]
        return checksum_format

    def pack_read_words(self, startadd, lengh):
        func_bytes = self.func_code_to_ascii('read_words')
        startadd_bytes = self.strt_addr_to_ascii(startadd)
        lengh_bytes = self.lengh_to_ascii(lengh)
        check_bytes = self.checksum_to_ascii(func_bytes, startadd_bytes, lengh_bytes, self.etx_bytes)
        return self.stx_bytes + func_bytes + startadd_bytes + lengh_bytes + self.etx_bytes + check_bytes

    def pack_write_words(self, startadd, lengh, data):
        func_bytes = self.func_code_to_ascii('write_words')
        startadd_bytes = self.strt_addr_to_ascii(startadd)
        lengh_bytes = self.lengh_to_ascii(lengh)
        data_bytes = self.data_value_to_ascii(data)
        check_bytes = self.checksum_to_ascii(func_bytes, startadd_bytes, lengh_bytes, data_bytes, self.etx_bytes)
        return self.stx_bytes + func_bytes + startadd_bytes + lengh_bytes + data_bytes + self.etx_bytes + check_bytes

    def unpack_read_return_bytes(self, bytes):
        datavalues = []
        databytes = []
        if 0x02 and 0x03 in bytes:
            databytes = bytes[1:-3]
            if self.checksum_to_ascii(databytes+[0x03]) != bytes[-2:]:
                datavalues = []
            else:
                if len(databytes) % 4 == 0:
                    for i in range(0, len(databytes), 4):
                        tempchr = chr(databytes[i+2]) + chr(databytes[i+3]) + chr(databytes[i]) + chr(databytes[i+1])
                        datavalues.append(int('0x'+tempchr, 16))
                else:
                    datavalues = []
        return datavalues

    def unpack_write_return_bytes(self, bytes):
        """
        判断返回值并处理
        :param bytes:
        :return:
        """
        write_result = False
        if bytes[0] == 0x06:
            write_result = True
        elif bytes[0] == 0x15:
            write_result = False
        else:
            write_result = False
        return write_result
# def pack_write_data(self, operal_type='read', start_address=0, operal_word_lengh=1, wt_data=None):
#     """
#     将数据组装为串口数据形式
#     :param start_address: D0偏移字（内部计算转换成字节数），字
#     :param operal_word_lengh: read/write数据长度，字
#     :param wt_data: 读取或写入数据，字节 写入用
#     :param operal_type: 操作类型：read/write
#     :return: 待传输字节串
#     """
#     if operal_type == 'read':
#         # 根据读长度要对usb_hid读缓存readbuffer进行区分1~14word, 1条帧；15~30word,2条帧；31、32word,3条帧
#         self.readbuffermaxlen = ((operal_word_lengh + 1) * 4 - 1) // 62 + 1
#     if operal_type == 'write':
#         self.readbuffermaxlen = 1
#
#     stx = [0x02]
#     etx = [0x03]
#     # 起始标识，结束标识
#
#     func_code = {'read': [0x45, 0x30, 0x30], 'write': [0x45, 0x31, 0x30]}[operal_type]
#
#     # 读写功能码，3 bytes
#
#     def pack_strt_addr(strt_addr_):
#         # 读写起始地址，4_bytes list
#         d0_fmt = 0x4000
#         d8000_fmt = 0x0E00
#         strt_addr_str = ''
#         if strt_addr_ in range(0, 8000):
#             strt_addr_str = '{:#06X}'.format(strt_addr_ * 2 + d0_fmt)
#         elif strt_addr_ in range(8000, 8255):
#             strt_addr_str = '{:#06X}'.format((strt_addr_ - 8000) * 2 + d8000_fmt)
#         strt_addr_fmt = [ord(letter) for letter in strt_addr_str][2:]
#         return strt_addr_fmt
#
#     start_address_code = pack_strt_addr(start_address)
#
#     def pack_lengh(len_):
#         lengh = []
#         # 读写长度 2_bytes list,注意A~F必须是大写的，否则会出错
#         if operal_word_lengh in range(1, 33):
#             len_str = '{:#04X}'.format(operal_word_lengh * 2)
#             lengh = [ord(letter) for letter in len_str][2:]
#         return lengh
#
#     lengh_code = pack_lengh(operal_word_lengh)
#
#     # 写指令时的数据（列表类型）组装
#     wt_data_code = []
#     if operal_type == 'read':
#         pass
#     if operal_type == 'write':
#         def pack_wtdata(nums):
#             wt_codes = []
#             for x in nums:
#                 h = 0
#                 b = int(x).to_bytes(2, byteorder='little', signed=True)
#                 l = h.from_bytes(b, 'big', signed=False)
#                 h_str = '{0:#06X}'.format(l)
#                 wt_codes += [ord(letter) for letter in h_str[2:]]
#             return wt_codes
#
#         wt_data_code = pack_wtdata(wt_data)
#
#
#
#     log.info("""
#     "the follow parameter packed:"
#         "stx: {0}: "
#         "function code: {1}; "
#         "start address: {2}; "
#         "data lengh: {3};"
#         "write data: {4}; "
#         "etx: {5}; "
#         "check sum: {6}""".format(
#         stx, func_code, start_address_code, lengh_code, wt_data_code, etx, checksum_code))
#     # 待发送数据list
#     _data_list = []
#     if operal_type == 'read':
#         _data_list = stx + func_code + start_address_code + lengh_code + etx + checksum_code
#     elif operal_type == 'write':
#         _data_list = stx + func_code + start_address_code + lengh_code + wt_data_code + etx + checksum_code
#     return _data_list        w

if __name__ == '__main__':

    s = LxPlcCom()
    # print(s.func_code_to_ascii('read_words'))
    # print(s.strt_addr_to_ascii('d8120'))
    # print(s.checksum_to_ascii([1, 2, 3, 4, 5]))
    # print(s.data_value_to_ascii([0x1234, 0x5678, 0xffff]))
    # l = s.pack_read_words('d8000', 32)
    # print('read words: ', l, '\n', ' '.join([hex(i)[2:] for i in l]))
    randoml = []
    for i in range(32):
        randoml.append(random.randint(-32768, 32767))
    l = s.pack_write_words('d0', 32, randoml)
    print(randoml, '\n', l, '\n', ' '.join([hex(i)[2:] for i in l]))
    print(s.unpack_read_return_bytes([0x2] + l[6:-3] + [0x3] + s.checksum_to_ascii(l[6:-3]+[0x3])))

