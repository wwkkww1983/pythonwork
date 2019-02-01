#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hmi_powered_down_save_auto_tst
# Author:    fan
# date:      2019/1/28
# -----------------------------------------------------------
# 问题：测试hmi掉电保存.
# 方案：通过脚本控制plc给hmi下电和上电，给hmi掉电保存区域赋值以及从该区域读回进行对比。通讯均通过串口Modbus rtu实现.
# 注意写完要保持3s才能确保正常掉电保存。
from modbus_rtu_master import ModbusRtu
import time
from random import randrange
from mylog import mylog
from make_time_formated import nowtimestr
from watchcom import set_port, open_port, close_port, read_correct

plc_port = ("com7", 9600, 8, 1, "N")
hmi_port = ("com9", 9600, 8, 1, "N")
plc = ModbusRtu(plc_port)
hmi = ModbusRtu(hmi_port)


def data_generator():
    return [randrange(0, 65535), randrange(0, 65535), randrange(0, 65535)]


def write(data):
    # print([data[0]] * 100)
    # print([data[1]] * 100)
    # print([data[2]] * 100)
    hmi.write_registers(1, 5000 - 3500, [data[0]] * 100)
    hmi.write_registers(1, 5100 - 3500, [data[1]] * 100)
    hmi.write_registers(1, 5200 - 3500, [data[2]] * 100)
    time.sleep(0.5)
    hmi.write_registers(1, 2, [1])


def read():
    read1 = hmi.read_registers(1, 4000 - 3500, 100)
    read2 = hmi.read_registers(1, 4100 - 3500, 100)
    read3 = hmi.read_registers(1, 4200 - 3500, 100)
    # print(read1)
    # print(read2)
    # print(read3)
    return [list(read1), list(read2), list(read3)]


def compare(data, read_data):
    for i, j in zip(data, read_data):
        print(i)
        print(j)
    if data == read_data:
        return True
    else:
        return False


def set_power(x):
    # if type(x) == bool:
        plc.write_coil(1, 0xfc00, x)


def start():
    testcount = 0
    errcount = 0
    excepcount = 0
    while testcount <= 10000:
        try:
            testcount += 1
            hmi.write_register(1, 0, testcount)
            hmi.write_register(1, 1, errcount)
            data = data_generator()
            write(data)
            writedata = [[data[0]] * 100, [data[1]] * 100, [data[2]] * 100]
            time.sleep(5)
            set_power(0)
            time.sleep(5)
            set_power(1)
            time.sleep(10)
            readdata = read()
            result = compare(writedata, readdata)
            if result is True:
                pass
            else:
                errcount += 1
            print("{} - test result: {}. {} times error in {} times test. exception count={}".format(
                nowtimestr(), result, errcount, testcount, excepcount))
        except Exception as e:
            print("exception happens. {}".format(e))
            excepcount += 1
            continue


if __name__ == '__main__':
    start()
    # readdata = read()
    # for i in readdata:
    #     x = i[0]
    #     for j in i:
    #         if j != x:
    #             print("error")
    #             break

