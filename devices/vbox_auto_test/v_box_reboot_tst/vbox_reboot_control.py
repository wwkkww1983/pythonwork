#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: vbox_reboot_control
# Author:    fan
# date:      2018/5/25
# -----------------------------------------------------------
import time
from plc_read_write import set_device_power, get_port, switch, open_port, close_port
import logging as log
import threading as thread

nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
timestamp = lambda timestr: int(time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S')))


log.basicConfig(level=log.info,
                color='FOREGROUND_YELLOW',
                format='%(asctime)s [line:%(lineno)d] %(levelname)s: %(message)s')


def timelog_ethernet(port, n_i=500, offtime=10, ontime=50):
    """
    4G方式必须采用不同方式，因为无法从局域网通过ssh访问盒子主机
    拟采用方式（提前确保电脑和盒子时间同步）：本地脚本只记录电源上电时间和次数，脚本运行结束后单独使用工具
    从4G盒子读取mqttCnet.log的文件内容，两边数据继续比对后组成上电耗时表格
    :return:
    """
    log.info('设置记录文件 timelog_ethernet.csv')
    with open('timelog_ethernet.csv', 'w', encoding='gb2312') as f:
        f.write('{}, {}, {}\n'.format('ip not available', 'ethernet', 'V-BOX上电耗时记录'))
        f.write('序号,上电时间戳（秒）,上电时间\n')
        f.close()
    i = 0
    while i <= n_i:
        switch(port, 'y0', 0)
        log.info('ethernet: v-box powered off')
        time.sleep(offtime)
        switch(port, 'y0', 1)
        log.info('ethernet: v-box powered on')
        i += 1
        powerontime_ethernet = nowtimefmt()
        time_powered_on = int(time.time())
        log.info('ethernet: time_powered_on: {}, time stamp: {}, logging...'.format(powerontime_ethernet, time_powered_on))
        with open('timelog_ethernet.csv', 'a', encoding='gb2312') as f:
            f.write('{}, {}, {}\n'.format(i, time_powered_on,  powerontime_ethernet))
        time.sleep(ontime)
    log.info("ethernet: test finished")


def timelog_wifi(port, n_i=500, offtime=10, ontime=50):
    """
    4G方式必须采用不同方式，因为无法从局域网通过ssh访问盒子主机
    拟采用方式（提前确保电脑和盒子时间同步）：本地脚本只记录电源上电时间和次数，脚本运行结束后单独使用工具
    从4G盒子读取mqttCnet.log的文件内容，两边数据继续比对后组成上电耗时表格
    :return:
    """
    log.info('设置记录文件 timelog_wifi.csv')
    with open('timelog_wifi.csv', 'w', encoding='gb2312') as f:
        f.write('{}, {}, {}\n'.format('ip not available', 'wifi', 'V-BOX上电耗时记录'))
        f.write('序号,上电时间戳（秒）,上电时间\n')
        f.close()
    i = 0
    while i <= n_i:
        switch(port, 'y1', 0)
        log.info('wifi: v-box powered off')
        time.sleep(offtime)
        switch(port, 'y1', 1)
        log.info('wifi: v-box powered on')
        i += 1
        powerontime_wifi = nowtimefmt()
        time_powered_on = int(time.time())
        log.info('wifi: time_powered_on: {}, time stamp: {}, logging...'.format(powerontime_wifi, time_powered_on))
        with open('timelog_wifi.csv', 'a', encoding='gb2312') as f:
            f.write('{}, {}, {}\n'.format(i, time_powered_on,  powerontime_wifi))
        time.sleep(ontime)
    log.info("wifi: test finished")


def timelog_4g(port, n_i=500, offtime=10, ontime=50):
    """
    4G方式必须采用不同方式，因为无法从局域网通过ssh访问盒子主机
    拟采用方式（提前确保电脑和盒子时间同步）：本地脚本只记录电源上电时间和次数，脚本运行结束后单独使用工具
    从4G盒子读取mqttCnet.log的文件内容，两边数据继续比对后组成上电耗时表格
    :return:
    """
    log.info('设置记录文件 timelog_4g.csv')
    with open('timelog_4g.csv', 'w', encoding='gb2312') as f:
        f.write('{}, {}, {}\n'.format('ip not available', '4g', 'V-BOX上电耗时记录'))
        f.write('序号,上电时间戳（秒）,上电时间\n')
    i = 0
    while i <= n_i:
        switch(port, 'y2', 0)
        log.info('4g: v-box powered off')
        time.sleep(offtime)
        switch(port, 'y2', 1)
        log.info('4g: v-box powered on')
        i += 1
        powerontime_4g = nowtimefmt()
        time_powered_on = int(time.time())
        log.info('4g: time_powered_on: {}, time stamp: {}, logging...'.format(powerontime_4g, time_powered_on))
        with open('timelog_4g.csv', 'a', encoding='gb2312') as f:
            f.write('{}, {}, {}\n'.format(i, time_powered_on,  powerontime_4g))
        time.sleep(ontime)
    log.info("4g: test finished")


def main():
    n_i = 500    # 记录次数
    n_offtime = 10    # 下电时长 秒
    n_ontime = 50    # 上电时长 秒
    port = get_port('com6', 9600)
    set_device_power(port, '000000')
    open_port(port)
    threads = []  # 建立线程数组
    t1 = thread.Thread(target=timelog_ethernet, args=(port, n_i, n_offtime, n_ontime))  # 线程1指定函数、参数
    threads.append(t1)  # 装载线程1
    t2 = thread.Thread(target=timelog_wifi, args=(port, n_i, n_offtime, n_ontime))
    threads.append(t2)
    t3 = thread.Thread(target=timelog_4g, args=(port, n_i, n_offtime, n_ontime))
    threads.append(t3)
    # 参数内容以太网和wifi网络方式相同
    for t in threads:  # 循环执行线程数组中的线程
        t.setDaemon(True)  # 将线程声明为守护线程
        t.start()  # 开始线程
    t.join()  # 在子线程执行完成之前，父线程将一直被阻塞
    close_port(port)
    log.info("ethernet/wifi/4g all test finishied.")


if __name__ == '__main__':
    main()
