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
from get_HMI import open_browser, open_project, check_hmi, set_num_value
from fx_communication_protocol import LxPlcCom
import xlrd, xlwt
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


def get_hmiurls(xlspath):
    """
    从xls获取HMI地址
    :param xlspath:
    :return:
    """
    hmiinfo_xls = xlrd.open_workbook(xlspath)
    sheet = hmiinfo_xls.sheet_by_name('设备信息')
    time.sleep(.5)
    s=sheet.cell_value(2, 5)
    n=sheet.nrows
    hmi_urls = []
    for i in range(2, sheet.nrows):
        print(sheet.cell_value(i, 5))
        hmi_urls.append(str(sheet.cell_value(i, 5)))
    if hmi_urls:
        return hmi_urls


def create_report(report_path, urls):
    hmireport_xls = xlwt.Workbook()
    # 必须标记单元格覆盖填写为允许，否则运行报错：Exception: Attempt to overwrite cell
    report_sheet = hmireport_xls.add_sheet('test report', cell_overwrite_ok=True)
    # 定义用于存放数据的表（二维列表）
    data_area = []
    if os.path.exists(report_path):
        # # 如果该报告文件存在，直接删除
        # os.remove('Ngrok问题测试报告.xls')
        # 如果该报告文件存在，在拷贝到内存中，新文件获取该数据并进行初始化
        e_report_xls = xlrd.open_workbook(report_path)
        e_report_sheet = e_report_xls.sheet_by_index(0)
        for i in range(e_report_sheet.nrows):
            if i >= 2:
                data_area.append(e_report_sheet.row_values(i))
            for j in range(e_report_sheet.ncols):
                report_sheet.write(i, j, e_report_sheet.cell_value(i, j))

    else:
        # 如果报告文件不存在，进行配置初始化
        report_sheet.write(0, 0, 'Ngrok问题网络切换PMI连接检测')
        sheet_head = ['ID',
                      'HMI_NAME',
                      'G4router0_SUCS',
                      'G4router0_FAIL',
                      'Router0_SUCS',
                      'Router0_FAIL',
                      'Switch_SUCS',
                      'Switch_FAIL',
                      'TOTAL_n',
                      'FAIL_n',
                      'URL']

        for i in range(len(sheet_head)):
            # 表格头部
            report_sheet.write(1, i, sheet_head[i])
        for hmi_id, hmi_url in zip([nm for nm in range(1, len(urls)+1)], urls):
            # 组装初始数据
            # hmi_name = hmi_url    # 局域网访问
            hmi_name = hmi_url[-28:-24]    # 远程访问
            row_value = [hmi_id, hmi_name, 0, 0, 0, 0, 0, 0, 0, 0, hmi_url]
            data_area.append(row_value)
            for n in range(len(row_value)):
                report_sheet.write(hmi_id+1, n, row_value[n])
    hmireport_xls.save('Ngrok问题测试报告.xls')
    time.sleep(2)
    return hmireport_xls, report_sheet, data_area


def set_report(data, sht, data_area):
    """
    设置数据
    :param data: [curdevice, hmitempname, hmialive,h midate, hmitime, checkinfo]
    :param sht: report_sheet
    :param data_area: data_area
    :return: True
    """
    for i in range(len(data_area)):
        if data[0] == data_area[i][1]:
            # 第8列-总次数；第9列-错误次数
            data_area[i][8] += 1
            if data[1] == 'g4router0':
                if data[2] is True:
                    data_area[i][2] += 1
                if data[2] is False:
                    data_area[i][3] += 1
                    data_area[i][9] += 1
            if data[1] == 'router0':
                if data[2] is True:
                    data_area[i][4] += 1
                if data[2] is False:
                    data_area[i][5] += 1
                    data_area[i][9] += 1
            if data[1] == 'switch0':
                if data[2] is True:
                    data_area[i][6] += 1
                if data[2] is False:
                    data_area[i][7] += 1
                    data_area[i][9] += 1

    for k in range(len(data_area)):
        for j in range(len(data_area[k])):
            if 10 >= j >= 2:
                sht.write(k+2, j, data_area[k][j])


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


def get_each_hmi_status(browser, hmiurls, curdevice, reportsheet, dataarea):
    for url in hmiurls:
        hmitempname = url[-28:-24]
        hmi = open_project(browser, url)
        time.sleep(1)
        if hmi:
            hmialive, hmidate, hmitime, checkinfo = check_hmi(hmi)
            set_report([hmitempname, curdevice, hmialive, hmidate, hmitime, checkinfo],
                       reportsheet,
                       dataarea)
        else:
            hmialive, hmidate, hmitime, checkinfo = [False, None, None, 'url not found']
        log.info('[{}], [{}], [{}], [{}], [{}], [{}]'.format(hmitempname,
                                                             curdevice,
                                                             hmialive,
                                                             hmidate,
                                                             hmitime,
                                                             checkinfo))


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

    for y, value in zip(('y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7'), tuple(pwcd)):
        switch(prt, y, int(value))
        time.sleep(.1)
    time.sleep(.5)
    close_port(prt)


def set_device_power2(proj, powercode):
    num_value = {0: "SPAN_0NUM_24_0"}
    div = proj.find_element_by_xpath('/html/body/div[@id="divfrm0"]/span[@id="{}"]'.format(num_value[0]))
    time.sleep(0.5)
    div.click()
    time.sleep(0.5)
    set_num_value(proj, powercode)


def main_no_plc():
    # 初始化
    # 关闭PLC控制电源，4G路由器持续生效
    # p = get_port(p_name='com2',
    #              p_baud=9600,
    #              p_bysz=7,
    #              p_stpb=1,
    #              p_prt='E')
    # close_port(p)
    # 设置HMI监控类型：
    # 远程访问地址
    url_xls = 'ngrok测试用例设备信息.xls'
    urls = get_hmiurls(url_xls)
    """
    # 局域网访问地址
    # urls = ['192.168.35.223', '192.168.35.224', ]
    # for i in range(len(urls)):
    #     urls[i] = 'http://' + urls[i]
    """
    report_path = 'Ngrok问题测试报告.xls'
    rept_xls, rept_sht, dt_ar = create_report(report_path, urls)
    log.info('hmi urls from:'+url_xls)
    log.info('report file:'+report_path)
    log.info('record format: [device] [hmi name] [alive] [date str] [time str] [info]')
    log.info('start checking remote hmi status')
    # 开始测试
    times = 0
    browser = open_browser()
    time.sleep(3)
    powercodes = ['11110000', '11101000', '11100100']
    code_device_map = {'11110000': 'switch0', '11101000': 'g4router0', '11100100': 'router0'}
    while True:
        # 使前两种方式交替，实现三台设备两两切换12，23，31，32，21，13
        # temp = powercodes[0]
        # powercodes[0] = powercodes[1]
        # powercodes[1] = temp
        for powcode in powercodes:
            times += 1
            log.info('current powercode:{}, net swtich times:{}'.format(powcode, times))
            # set_device_power(p, powcode)
            # time.sleep(60)
            t = threading.Thread(target=get_each_hmi_status,
                                 args=(browser, urls, code_device_map[powcode], rept_sht, dt_ar))
            t.setDaemon(True)
            t.start()
            t.join()
        rept_xls.save(report_path)
        time.sleep(1)
        log.info('powercode {} checking finished'.format(powercodes))


def main_4g_onoff():
    # 初始化
    # PLC控制电源，4G路由器重启
    p = get_port(p_name='com2',
                 p_baud=9600,
                 p_bysz=7,
                 p_stpb=1,
                 p_prt='E')
    close_port(p)
    # 设置HMI监控类型：
    # 远程访问地址
    url_xls = 'ngrok测试用例设备信息.xls'
    urls = get_hmiurls(url_xls)
    """
    # 局域网访问地址
    # urls = ['192.168.35.223', '192.168.35.224', ]
    # for i in range(len(urls)):
    #     urls[i] = 'http://' + urls[i]
    """
    report_path = 'Ngrok问题测试报告.xls'
    rept_xls, rept_sht, dt_ar = create_report(report_path, urls)
    log.info('hmi urls from:'+url_xls)
    log.info('report file:'+report_path)
    log.info('record format: [device] [hmi name] [alive] [date str] [time str] [info]')
    log.info('start checking remote hmi status')
    # 开始测试
    times = 0
    browser = open_browser()
    time.sleep(3)
    powercodes = ['11101000']
    code_device_map = {'11110000': 'switch0', '11101000': 'g4router0', '11100100': 'router0'}
    while True:
        for powcode in powercodes:
            times += 1
            log.info('current powercode:{}, net swtich times:{}'.format(powcode, times))
            set_device_power(p, '11100000')
            time.sleep(30)
            set_device_power(p, powcode)
            time.sleep(90)
            t = threading.Thread(target=get_each_hmi_status,
                                 args=(browser, urls, code_device_map[powcode], rept_sht, dt_ar))
            t.setDaemon(True)
            t.start()
            t.join()
        rept_xls.save(report_path)
        time.sleep(1)
        log.info('powercode {} checking finished'.format(powercodes))


def main_switch_onoff():
    # 初始化记录文件
    url_xls = 'ngrok测试用例设备信息.xls'
    urls = get_hmiurls(url_xls)
    report_path = 'Ngrok问题测试报告.xls'
    rept_xls, rept_sht, dt_ar = create_report(report_path, urls)
    log.info('hmi urls from:' + url_xls)
    log.info('report file:' + report_path)
    log.info('record format: [device] [hmi name] [alive] [date str] [time str] [info]')
    log.info('start checking remote hmi status')

    # 开始测试
    proj_control = open_browser()    # 浏览器窗口1：主控HMI监控
    proj_control.set_window_position(x=0, y=0)
    proj_control.set_window_size(width=700, height=800)
    time.sleep(2)
    proj_control.get(r'http://192.168.39.23')
    time.sleep(2)
    times = 0    # 测试次数
    browser = open_browser()    # 浏览器窗口2：HMI监控
    browser.set_window_position(x=720, y=0)
    browser.set_window_size(width=700, height=800)
    time.sleep(3)
    # 重新定义 机器电源码对应设备
    code_device_map = {'01110000': 'switch0', '01011000': 'g4router0', '01010100': 'router0'}
    while times <= 200:
        for powcode in code_device_map.keys():
            times += 1
            log.info('current powercode:{}, net swtich times:{}'.format(powcode, times))
            # set_device_power2(proj_control, '01010000')    # 三个设备下电
            # time.sleep(30)
            try:
                set_device_power2(proj_control, powcode)    # 只有一个设备上电
            except Exception as e:
                print(e)
            time.sleep(180)
            t = threading.Thread(target=get_each_hmi_status,
                                 args=(browser, urls, code_device_map[powcode], rept_sht, dt_ar))
            t.setDaemon(True)
            t.start()
            t.join()
        rept_xls.save(report_path)
        time.sleep(400)
        log.info('powercode {} checking finished'.format('01110000'))


if __name__ == '__main__':
    # data_report()
    # main_4g_onoff()
    # main_no_plc()
    main_switch_onoff()
