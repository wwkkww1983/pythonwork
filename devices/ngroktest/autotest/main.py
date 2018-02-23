#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: main
# Author:    fan
# date:      2018/2/23
# -----------------------------------------------------------
from get_HMI import open_browser, open_project, check_hmi
from fx_communication_protocol import LxPlcCom
import xlrd
from serial import Serial
import time
import threading


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


def get_each_hmi_status(browser, hmiurls):
    for url in hmiurls:
        hmitempname = url[-28:-24]
        hmi = open_project(browser, url)
        time.sleep(1)
        hmialive, hmidate, hmitime = check_hmi(hmi)
        print('hmi:{} alive is {}, hmi current time: {} {}'.format(hmitempname, hmialive, hmidate, hmitime))
        time.sleep(1)


def main():
    urls = get_hmiurls('ngrok测试用例设备信息.xls')
    print('checking remote hmi status')
    browser = open_browser()
    t = threading.Thread(target=get_each_hmi_status, args=(browser, urls))
    t.setDaemon(True)
    t.start()
    t.join()
    browser.quit()
    print('checking finished')


if __name__ == '__main__':
    main()
