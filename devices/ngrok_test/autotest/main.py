#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: main
# Author:    fan
# date:      2018/2/23
# -----------------------------------------------------------
import os
from random import shuffle
import logging as log
from get_HMI import open_browser, open_project, check_hmi
from fx_communication_protocol import LxPlcCom
import xlrd
from serial import Serial
import time
import threading
from datetime import datetime as dt

log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')
log.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=log.INFO,
                format='%(asctime)s %(levelname)s: %(message)s')
log.info('hmi checking format: [hmi name] [alive] [date str] [time str] [info]')

def get_hmiurls(xlspath):
    """
    从xls获取HMI地址
    :param xlspath:
    :return:
    """
    hmiinfo_xls = xlrd.open_workbook(xlspath)
    sheet = hmiinfo_xls.sheet_by_name('设备信息')
    hmi_urls = []
    for i in range(2, 19):
        hmi_urls.append(str(sheet.cell_value(i, 5)))
    return hmi_urls


def get_port(p_name='com1', p_baud=9600, p_bysz=8, p_stpb=1, p_prt='N', tmot=1):
    # 设置串口
    t = Serial(p_name)
    t.baudrate = p_baud
    t.bytesize = p_bysz
    t.stopbits = p_stpb
    t.parity = p_prt
    t.timeout = tmot
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


def get_each_hmi_status(browser, hmiurls):
    for url in hmiurls:
        hmitempname = url[-28:-24]
        hmi = open_project(browser, url)
        time.sleep(1)
        hmialive, hmidate, hmitime, checkinfo = check_hmi(hmi)
        log.info((hmitempname, hmialive, hmidate, hmitime, checkinfo))


def set_device_power(port, powercodes):
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
    :param pcode: powered code
    :return: True
    """
    port.open()
    # # 打乱顺序：避免总是相同的设备切换顺序。问题：有时会造前一次的最后一个供电代码与后一次的第一个供电代码相同，设备不会实现切换
    # shuffle(powercodes)

    for y, value in zip(('y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7'), tuple(powercodes)):
        switch(port, y, int(value))
        time.sleep(.1)


def main():
    # 初始化
    powercodes = ['11110000', '11101000', '11100100']
    p = get_port(p_name='com2',
                 p_baud=9600,
                 p_bysz=7,
                 p_stpb=1,
                 p_prt='E')
    close_port(p)
    urls = get_hmiurls('ngrok测试用例设备信息.xls')
    log.info('checking remote hmi status')
    # 开始测试
    open_port(p)
    times = 0
    while True:
        browser = open_browser()
        time.sleep(3)
        # 使前两种方式交替，实现三台设备两两切换12，23，31，32，21，13
        temp = powercodes[0]
        powercodes[0] = powercodes[1]
        powercodes[1] = temp
        t = threading.Thread(target=get_each_hmi_status, args=(browser, urls))
        t.setDaemon(True)
        for powcode in powercodes:
            times += 1
            log.info('当前测试供电代码：'+powcode + ' 总切换次数：' + str(times))
            set_device_power(p, powcode)
            time.sleep(20)
            t.start()
            t.join()
        browser.quit()
        log.info('checking finished')


if __name__ == '__main__':
    main()
