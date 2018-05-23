#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: ssh.py
# Author:    fan
# date:      2018/5/18
# -----------------------------------------------------------
import paramiko
from plc_read_write import set_device_power, get_port, switch, open_port, close_port    # 导入控制PLCY点的函数(com6, '101010')
import time
import logging as log
import os
import threading as thread

log.basicConfig(level=log.INFO,
                color='FOREGROUND_YELLOW',
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

nowtimefmt = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 格式化当前时间
timestamp = lambda timestr: int(time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S')))



class Ssh(object):
    """
    ssh类，基于局域网IP建立shell链接，通过Linux终端执行远程命令或采集远程主机信息
    """
    def __init__(self):
        self.ssh = paramiko.SSHClient()

    def login(self, ip_, usrname_, password_):
        """
        远程主机登录
        :param ip_:
        :param usrname_:
        :param password_:
        :return: ssh已登录对象
        """
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过是否接收保存密码信息
        self.ssh.connect(ip_, 22, usrname_, password_)  # 用户登录

    def do_cmd(self, cmd):
        """
        远程主机执行命令
        :param cmd: 命令内容
        :return: 返回屏显结果
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=1)
        # din = stdin.readlines()
        # err = stderr.redlines()
        out = stdout.readlines()
        out_strlist = []
        # print(out)
        for line in out:
            out_strlist.append(line)
            # print(line[:-1])
        return out_strlist


def timelog_ethernet(port, n_i, offtime, ontime):
    client1 = Ssh()
    ip1 = '192.168.39.123'
    usrname = 'root'
    password = 'weconily'
    cmd = 'tail -n 2 /wecon/run/project/mqttCnet.log'
    timelog_ethernet = open('timelog_ethernet.csv', 'a', encoding='gb2312')
    timelog_ethernet.write('{}, {}, {}\n'.format(ip1, 'Ethernet', 'V-BOX上电耗时记录'))
    timelog_ethernet.write('序号,上电耗时（秒）,出错次数\n')
    timelog_ethernet.close()
    i = 0
    n_errs1 = 0
    while i <= n_i:
        timelog_ethernet = open('timelog_ethernet.csv', 'a', encoding='gb2312')
        time.sleep(.2)
        switch(port, 'y0', 0)
        time.sleep(offtime)
        switch(port, 'y0', 1)
        i += 1
        log.info('ethernet: time_powered_on: {}'.format(nowtimefmt()))
        time_powered_on = int(time.time())
        log.info('ethernet: time stamp: {}'.format(time_powered_on))
        time.sleep(ontime)
        try:
            client1.login(ip1, usrname, password)
            cnetloglist = client1.do_cmd(cmd)
            log.info('ethernet: 读文件cnetloglist: {}'.format(cnetloglist))
            if 'connect success!' in cnetloglist[-1]:
                time_reboot_end = cnetloglist[-1].split(' ')[0] + ' ' + cnetloglist[-1].split(' ')[1]
                log.info('ethernet: time_reboot_end: {}'.format(time_reboot_end))
                time_reboot_end = timestamp(time_reboot_end)
                log.info('ethernet: time stamp: {}'.format(time_reboot_end))
                timelog_ethernet.write(
                    '{}, {}, {}\n'.format(str(i), str(time_reboot_end - time_powered_on), str(n_errs1)))
                timelog_ethernet.close()
        except Exception as e:
            n_errs1 += 1
            timelog_ethernet.write('{}, {}, {}\n'.format(str(i), ' ', str(n_errs1)))
            log.error('ethernet: ')
            log.error(e)
            timelog_ethernet.close()
            time.sleep(1)


def timelog_wifi(port, n_i, offtime, ontime):
    client2 = Ssh()
    ip2 = '192.168.33.173'
    usrname = 'root'
    password = 'weconily'
    cmd = 'tail -n 2 /wecon/run/project/mqttCnet.log'
    timelog_wifi = open('timelog_wifi.csv', 'a', encoding='gb2312')
    timelog_wifi.write('{}, {}, {}\n'.format(ip2, 'WIFI', 'V-BOX上电耗时记录'))
    timelog_wifi.write('序号,上电耗时（秒）,出错次数\n')
    timelog_wifi.close()
    i = 0
    n_errs2 = 0
    while i <= n_i:
        timelog_wifi = open('timelog_wifi.csv', 'a', encoding='gb2312')
        time.sleep(.5)
        switch(port, 'y1', 0)
        time.sleep(offtime)
        switch(port, 'y1', 1)
        i += 1
        log.info('wifi: time_powered_on: {}'.format(nowtimefmt()))
        time_powered_on = int(time.time())
        log.info('wifi: time stamp: {}'.format(time_powered_on))
        time.sleep(ontime)
        try:
            client2.login(ip2, usrname, password)
            cnetloglist2 = client2.do_cmd(cmd)
            log.info('wifi: 读文件cnetloglist2: {}'.format(cnetloglist2))
            if 'connect success!' in cnetloglist2[-1]:
                time_reboot_end2 = cnetloglist2[-1].split(' ')[0] + ' ' + cnetloglist2[-1].split(' ')[1]
                log.info('wifi: time_reboot_end: {}'.format(time_reboot_end2))
                time_reboot_end2 = timestamp(time_reboot_end2)
                log.info('wifi: time stamp: {}'.format(time_reboot_end2))
                timelog_wifi.write(
                    '{}, {}, {}\n'.format(str(i), str(time_reboot_end2 - time_powered_on), str(n_errs2)))
                timelog_wifi.close()
        except Exception as e:
            n_errs2 += 1
            timelog_wifi.write('{}, {}, {}\n'.format(str(i), ' ', str(n_errs2)))
            log.error('wifi: ')
            log.error(e)
            timelog_wifi.close()
            time.sleep(1)
            continue


def timelog_4g(port, n_i, offtime, ontime):
    """
    4G方式必须采用不同方式，因为无法从局域网通过ssh访问盒子主机
    拟采用方式（提前确保电脑和盒子时间同步）：本地脚本只记录电源上电时间和次数，脚本运行结束后单独使用工具
    从4G盒子读取mqttCnet.log的文件内容，两边数据继续比对后组成上电耗时表格
    :return:
    """
    timelog_4g = open('timelog_4g.csv', 'a', encoding='gb2312')
    timelog_4g.write('{}, {}, {}\n'.format('ip not available', '4g', 'V-BOX上电耗时记录'))
    timelog_4g.write('序号,上电时间戳（秒）,出错次数\n')
    timelog_4g.close()
    i = 0
    n_errs3 = 0
    while i <= n_i:
        timelog_4g = open('timelog_4g.csv', 'a', encoding='gb2312')
        switch(port, 'y2', 0)
        time.sleep(offtime)
        switch(port, 'y2', 1)
        i += 1
        powerontime_4g = nowtimefmt()
        log.info('4g: time_powered_on: {}'.format(powerontime_4g))
        time_powered_on = int(time.time())
        log.info('4g: time stamp: {}'.format(time_powered_on))
        time.sleep(ontime)
        try:
            timelog_4g.write('{}, {}, {}, {}\n'.format(i, time_powered_on, n_errs3, powerontime_4g))
            timelog_4g.close()
        except Exception as e:
            n_errs3 += 1
            timelog_4g.write('{}, {}, {}\n'.format(i, ' ', n_errs3))
            log.error('4g: ')
            log.error(e)
            timelog_4g.close()
            time.sleep(1)


def main():
    port = get_port('com6', 9600)
    set_device_power(port, '000000')
    open_port(port)
    threads = []  # 建立线程数组
    t1 = thread.Thread(target=timelog_ethernet, args=(port, 1000, 10, 30))  # 线程1指定函数、参数
    threads.append(t1)  # 装载线程1
    t2 = thread.Thread(target=timelog_wifi, args=(port, 1000, 10, 40))
    threads.append(t2)
    t3 = thread.Thread(target=timelog_4g, args=(port, 1000, 10, 40))
    threads.append(t3)
    # 参数内容以太网和wifi网络方式相同
    for t in threads:  # 循环执行线程数组中的线程
        t.setDaemon(True)  # 将线程声明为守护线程
        t.start()  # 开始线程
    t.join()  # 在子线程执行完成之前，父线程将一直被阻塞
    close_port(port)
    print("all over")
if __name__ == '__main__':
    main()
