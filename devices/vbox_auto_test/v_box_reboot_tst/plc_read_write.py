#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: plc_readand_write
# Author:    fan
# date:      2018/5/22
# -----------------------------------------------------------

from fx_communication_protocol import LxPlcCom
import time
from serial import Serial

def get_port(p_name='com1', p_baud=9600, p_bysz=8, p_stpb=1, p_prt='N', tmot=1):
    # 设置串口
    t = Serial(p_name)
    t.baudrate = p_baud
    t.bytesize = p_bysz
    t.stopbits = p_stpb
    t.parity = p_prt
    t.timeout = tmot
    t.close()
    return t


def switch(port, y, value):
    # 设置输出状态，vlaue=0:复位； value=1:置位
    l = LxPlcCom()
    data = l.pack_write_bit(y, value)
    for i in range(3):
        port.write(data)
        time.sleep(0.01)


def close_port(port):
    # 关闭串口
    port.close()


def open_port(port):
    port.open()


def set_device_power(prt, pwcd):
    """
    代码说明：二进制0、1组成的字符串。
             设备供电代码，一共8位，0表示电源断开，1表示电源接通。定义如下：
             位0，Y0, 不使用
             位1，Y1, HMI 电源
             位2，Y2, 离HMI最近的交换机电源
             位3，Y3, 连接方式 交换机电源
             位4，Y4, 连接方式 4G路由器电源
             位5，Y5, 连接方式 网口路由器电源
             位6，Y6, 预留，不使用
             位7，Y7, 预留，不使用
    :param pwcd:
    :param prt:
    :return: True
    """
    open_port(prt)
    # # 打乱顺序：避免总是相同的设备切换顺序。问题：有时会造前一次的最后一个供电代码与后一次的第一个供电代码相同，设备不会实现切换
    # shuffle(powercodes)

    for y, value in zip(('y0', 'y1', 'y2', 'y3', 'y4', 'y5'), tuple(pwcd)):
        switch(prt, y, int(value))
        time.sleep(.1)
    time.sleep(.5)
    close_port(prt)

if __name__ == '__main__':
    pass
