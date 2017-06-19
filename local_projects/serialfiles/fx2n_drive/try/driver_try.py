# !/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import ctypes
import time
from crccheck.checksum import Checksum8
from PyQt5.QtWidgets import QWidget


def set_com(com_id, com_baudrate):
    """
    :param com_id: 串口号
    :param com_baudrate: 串口波特率
    :return: 串口对象
    """
    if com_id and com_baudrate:
        try:
            com = serial.Serial(com_id, com_baudrate)
        except WindowsError as e:
            print('WindowsError: {0}'.format(e))
        else:
            com.timeout = 0.5
            print("""\
        ------------------------------------------------------------
        串口信息：
        串口ID：  {0}
        波特率：  {1}
        数据位：  {2}
        校验  ：  {3}
        停止位：  {4}""".format(com.port, com.baudrate, com.bytesize, com.parity, com.stopbits))
            return com


def port_test(this_port):
    """
    串口测试
    :param this_port:
    :return: 成功或失败
    """
    result = 'fail'
    if this_port.is_open:
        for i in range(5):
            try:
                port.write(b'\x05')
            except:
                print('com test fail')
            else:
                time.sleep(.1)
                read_bytes = this_port.read(size=1)
                if read_bytes == b'\x06':
                    result = 'success'
                    break
                else:
                    result = 'fail'
                    time.sleep(.1)
    print('-'*60, '\nport test result: {}'.format(result))
    return result


def load_port(this_port, relative=6000, word_len=1, data=None, read_or_write='read'):
    """
    执行串口读写操作
    :return:
    :param this_port: 已设定串口
    :param relative: D0偏移字（内部计算转换成字节数），字
    :param word_len: read/write数据长度，字
    :param data: 读取或写入数据，字节 写入用
    :param read_or_write: 操作类型：read/write
    :return: {操作结果标识: , 串口收到数据:}  字节
    """

    response_size = {'read': 4 + word_len * 4, 'write': 1}[read_or_write]  # 返回帧长度，读：数据长度+4，写：1，bytes

    def pack_bytes(_relative=6000, _word_len=1, _data=None, _read_or_write='read'):
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
        func_code = {'read': b'E00', 'write': b'E10'}[_read_or_write]  # 读写功能码，3 bytes

        d0_int = 0x4000  # D0协议地址
        start_address = b''
        if _relative in range(6000, 6032):
            start_address_hex = '{:#06X}'.format(_relative * 2 + d0_int)
            start_address = start_address_hex[-4:].encode('ascii')  # 读写起始地址，4 bytes

        lengh = b''
        if _word_len in range(1, 32):
            len_hex = '{:#04X}'.format(_word_len * 2)
            lengh = len_hex[-2:].encode('ascii')  # 读写长度 2 bytes

        checksum = b''  # 1 bytes
        check = Checksum8()
        if lengh:
            checksum_int = check.calc(func_code + start_address + lengh + etx)
            checksum_hex = '{:#04X}'.format(checksum_int)
            checksum = checksum_hex[-2:].encode('ascii')

        print("""\
        ------------------------------------------------------------
        the follow parameter wpacked
        stx: {0}
        function code: {1}
        start address: {2}
        data lengh: {3}
        operate data: {4}
        etx: {5}check sum: {6}""".format(stx, func_code, start_address, lengh, data, etx, checksum))

        _packed_bytes = b''
        if _read_or_write == 'read':
            _packed_bytes = stx + func_code + start_address + lengh + etx + checksum  # bytes
        return _packed_bytes

    def port_opration(_port, _rerady_bytes, _response_size):
        """
        :param _port: 串口对象
        :param _ready_bytes:
        :param _response_size:
        :return:
        """
        _flag = 'fail'
        _read_bytes = b''

        if _port.is_open:
            for i in range(3):
                try:
                    _port.write(_ready_bytes)
                except:
                    _flag = 'fail'
                    print('send data fail')
                else:
                    time.sleep(.1)
                    _read_bytes = _port.read(size=_response_size)
                    if len(_read_bytes) > 0:
                        _flag = 'success'
                        break
                    else:
                        if  i == 2:
                            _flag = 'fail'
                            print('receive data timeout')
        return {'flag': _flag, 'read_bytes': _read_bytes}

    send_bytes = pack_bytes(relative, word_len, data, read_or_write)
    operation = port_opration(this_port, send_bytes, response_size)
    return operation

if __name__ == '__main__':
    port = set_com('com7', 9600)
    if port:
        test = port_test(port)
        time.sleep(.3)
        if test == 'success':
            port_data = load_port(port, 6000, 1, 0, 'read')
            print('-'*60, ' \n response: {0};\n received bytes: {1}'.format(port_data['flag'], port_data['read_bytes']))
        port.close()
    print('END')
