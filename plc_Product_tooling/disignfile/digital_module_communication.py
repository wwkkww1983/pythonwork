# !/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import ctypes
import time
from crccheck.checksum import Checksum8


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
            串口ID：  {0}
            波特率：  {1}
            数据位：  {2}
            校验  ：  {3}
            停止位：  {4}\
            """.format(com.port, com.baudrate, com.bytesize, com.parity, com.stopbits))
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
    print(result)
    return result


def pack_bytes(relative=6000, word_len=2, data=None, pack_type='read'):
    """
    将数据组装为串口传输用数据
    :param relative: D0偏移字（内部计算转换成字节数），字
    :param word_len: read/write数据长度，字
    :param data: 读取或写入数据，字节 写入用
    :param pack_type: 操作类型：read/write
    :return: 待传输字节串
    """
    stx = b'\x02'
    etx = b'\x03'

    func_code = {'read': b'E00', 'write': b'E10'}[pack_type]  # 读写功能码，3 bytes

    d0_int = 0x4000   # D0协议地址
    start_address = b''
    if relative in range(6000, 6032):
        start_address_hex = '{:#06X}'.format(relative * 2 + d0_int)
        start_address = start_address_hex[-4:].encode('ascii')  # 读写起始地址，4 bytes

    lengh = b''
    if word_len in range(1, 32):
        len_hex = '{:#04X}'.format(word_len * 2)
        lengh = len_hex[-2:].encode('ascii')  # 读写长度 2 bytes

    checksum = b''  # 1 bytes
    check = Checksum8()
    if lengh:
        checksum_int = check.calc(func_code+start_address+lengh+etx)
        checksum_hex = '{:#04X}'.format(checksum_int)
        checksum = checksum_hex[-2:].encode('ascii')

    print(stx,func_code,start_address,lengh,etx,checksum)

    return stx+func_code+start_address+lengh+etx+checksum  # bytes


def communication(this_port, prepared_bytes, timeout=0.5):
    """
    执行串口读写操作
    :return:
    :param this_port: 已设定串口
    :param prepared_bytes: 待传输bytes
    :param timeout: 超时
    :return:
    """

    return


if __name__ == '__main__':

    port = set_com('com1', 9600)
    if port:
        port_test(port)
        time.sleep(.3)
        print(pack_bytes(word_len=0x1))
        port.close()

    print('END')


