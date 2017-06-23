#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRC32 import CRC32
from PyCRC.CRCCCITT import CRCCCITT
from crc_itu import crc16
from crccheck.crc import CrcModbus
from crccheck.checksum import Checksum16
from crccheck.checksum import Checksum8


def data_list(line_str):
    list_int = []
    for num in line_str.split():
        list_int.append(int(num, 16))
    print(list_int)
    return list_int


def get_bytes(hex_str):

    return bytes.fromhex(hex_str)


def string_delspace(data_str):

    hex_str = ''.join(data_str.split(' '))
    print('data without space : {}'.format(hex_str))
    return hex_str


def get_crc(data, how_to):

    def pycrc_crc16(data_str):
        crc = CRC16().calculate(data_str)
        return crc

    def crc_modbus(data_str):
        crc = CrcModbus().calc(data_str)
        return crc

    if how_to == 'pycrc':
        return pycrc_crc16(data)
    if how_to == 'crcmodbus':
        return hex(crc_modbus(data))
    else:
        return 'no crc bytes created'


def get_sum(data, how_to):

    def crccheck_checksum16(data_str):
        checksum = Checksum16.calc(data_str)
        return checksum

    def crccheck_checksum8(data_str):
        checksum = Checksum8.calc(data_str)
        return checksum
    if how_to == 'checksum16':
        return crccheck_checksum16(data)
    if how_to == 'checksum8':
        return crccheck_checksum8(data)

if __name__ == '__main__':

    string = '11 6D 8A 80 51 7D'
    string = '45 30 30 30 45 30 32 30 32'


    print('data : {}'.format(string))
    m = get_bytes(string)

    s = [0, 128, 2, 2, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 3, 52, 51][4:-2]
    m = ''.join([chr(i) for i in s]).encode('ascii')

    print('str_hex(lengh:{}) = {}'.format(len(m), m))

    l = get_crc(m, 'pycrc')
    s = get_crc(m, 'crcmodbus')
    print("\npycrc : {0:#06x}\ncrccheck: {1}".format(l, s))  # crc校验，plc、hmi采用的通讯校验方式一致

    n = get_sum(m, 'checksum8')
    print('\nchecksum: {0:#04x}'.format(n))  # 校验和，与plc串口、usb协议（三菱mc协议）的通讯校验方式一致
