# !/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import logging as log
from crccheck.checksum import Checksum8
from PyQt5.QtWidgets import QWidget

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


def set_com(com_id, com_baudrate):
    """
    :param com_id: 串口号
    :param com_baudrate: 串口波特率
    :return: 串口对象
    """
    com = None
    if com_id and com_baudrate:
        try:
            com = serial.Serial(com_id, com_baudrate)
        except WindowsError as e:
            log.error('WindowsError:{}'.format(e))
        else:
            com.timeout = 0.3
            com.bytesize = 7
            com.parity = 'E'
            com.stopbits = 1
            com.xonxoff

            log.info("串口设置成功: "
                     "串口:{0}, "
                     "波特率:{1}bps, "
                     "数据位:{2},"
                     "校验:{3},"
                     "停止位:{4},"
                     "超时设置:{5}ms.".format(com.port, com.baudrate, com.bytesize,
                                          com.parity, com.stopbits, com.timeout*1000))
    return com


def port_tst(this_port):
    """
    串口测试
    :param this_port:
    :return: 成功或失败
    """
    test_result = 'fail'
    if this_port.is_open:
        for i in range(3):
            try:
                port.write(b'\x05')
            except:
                test_result = 'fail'

            else:
                time.sleep(.1)
                read_bytes = this_port.read(size=1)
                if read_bytes == b'\x06':
                    test_result = 'success'
                    break
                else:
                    test_result = 'fail'
                    time.sleep(.1)
    log.info('com test result: {}'.format(test_result))
    return test_result


def pack_bytes_list(_relative=6000, _word_len=1, _data=None, _read_or_write='read'):
    """
    将数据组装为串口传输用数据
    :param _relative: D0偏移字（内部计算转换成字节数），字
    :param _word_len: read/write数据长度，字
    :param _data: 读取或写入数据，字节 写入用
    :param _read_or_write: 操作类型：read/write
    :return: 待传输字节串
    """
    stx = b'\x02'
    etx = b'\x03'
    # 起始标识，结束标识

    func_code = {'read': b'E00', 'write': b'E10'}[_read_or_write]
    # 读写功能码，3 bytes

    d0_int = 0x4000
    d8000_int = 0x0E00
    start_address_hex = ''
    start_address = b''
    # 读写起始地址，4 bytes
    if _relative in range(6000, 6032):
        start_address_hex = '{:#06X}'.format(_relative * 2 + d0_int)
    if _relative in range(8000, 8255):
        start_address_hex = '{:#06X}'.format((_relative-8000) * 2 + d8000_int)
    start_address = start_address_hex[-4:].encode('ascii')
    lengh = b''
    # 读写长度 2 bytes
    if _word_len in range(1, 32):
        len_hex = '{:#04X}'.format(_word_len * 2)
        lengh = len_hex[-2:].encode('ascii')

    checksum = b''
    # 校验和，1 bytes。功能码、起始地址、数据和结束标识参与校验，起始标识不校验
    check = Checksum8()
    if lengh:
        checksum_int = check.calc(func_code + start_address + lengh + etx)
        checksum_hex = '{:#04X}'.format(checksum_int)
        checksum = checksum_hex[-2:].encode('ascii')

    # 写入数据长度
    if func_code == 'write':
        data = b''   # 格式化数据
    else:
        data = b''

    log.info("the follow parameter packed:"
             "stx: {0}: "
             "function code: {1}; "
             "start address: {2}; "
             "data lengh: {3};"
             "write data: {4}; "
             "etx: {5}; "
             "check sum: {6}".format(stx, func_code, start_address, lengh, _data, etx, checksum))

    # 待发送字节串list
    if _read_or_write == 'read':
        _bytes_list = [stx, func_code, start_address, lengh, etx, checksum]
    else:
        _bytes_list = [stx, func_code, start_address, lengh, data, etx, checksum]
    return _bytes_list


def port_doing(dig_port, bytes_list):
    """
    :param dig_port: 串口对象
    :param bytes_list:
    :return:
    """

    response_size = b''
    ready_bytes = b''
    if bytes_list:
        # 根据读写类型和data长度，计算响应数据size
        if bytes_list[1] == b'E00':
            response_size = 4+2*int(bytes_list[3], 16)

        if bytes_list[1] == b'E10':
            response_size = 1

        for item in bytes_list:
            ready_bytes += item

    log.info('send bytes were ready; {0},'
             'response size will be {1} bytes'.format(ready_bytes, response_size))
    write_flag = 'fail'
    read_flag = 'fail'
    timeout = None
    _response_bytes = b''
    if dig_port.is_open:
        for i in range(3):
            try:
                dig_port.write(ready_bytes)
            except:
                write_flag = 'fail'
            else:
                write_flag = 'success'
                time.sleep(.1)
                _response_bytes = dig_port.read(size=response_size)
                if len(_response_bytes) > 0:
                    read_flag = 'success'
                    break
                else:
                    if i == 2:
                        read_flag = 'fail'
                        timeout = True
    log.info('port writing: {0},'
             'port reading: {1},'
             'response timeout: {2}'.format(write_flag, read_flag, timeout))
    log.info('response data: {}'.format(_response_bytes))
    return {'flag': read_flag, 'read_bytes': _response_bytes}

def bytes_to_data(bytes, datatype):
    """
    :param bytes: 有效数据
    :param datatype:
    :return:
    """


if __name__ == '__main__':
    port = set_com('com1', 115200)
    if port:
        tst = port_tst(port)
        time.sleep(.3)
        if tst == 'success' or 'fail':
            current_bytes = pack_bytes_list(6000, 2, 0, 'read')
            response_bytes = port_doing(port, current_bytes)
            # response_data = response_bytes.
        port.close()
    log.info("串口调试结束")
