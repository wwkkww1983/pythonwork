#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hmi_auto_restart_via_plc
# Author:    fan
# date:      2019/1/5
# 通过hmi串口是否有数据发出，判断hmi是否启动正常，若启动正常则下电hmi延时并重启hmi，继续测试；若hmi未启动则停止测试并报告问题
# -----------------------------------------------------------
from modbus_rtu_master import ModbusRtu
import time
from make_time_formated import nowtimestr
from watchcom import set_port, open_port, close_port, read_correct

print("{} - test started.".format(nowtimestr()))
hmiport = set_port('com9', 115200, 8, 1, 'N')
plcportporp = ("com7", 9600, 8, 1, "N")
plc = ModbusRtu(plcportporp)
plc.write_coil(1, 0xfc00, 1)
print("{} - hmi powered on".format(nowtimestr()))
readbytes = b'\x0201440AM008253\x03' or b'\x02014603R0519081\x03'
i = 0
while i <= 20000:
    i += 1
    x = 0
    try:
        while x < 30:
            try:
                x = read_correct(hmiport, readbytes)
                if x:
                    print("{} - read hmi port success. test times: {}".format(nowtimestr(), i))
                    x = 30  # 跳出循环
            except Exception as e:
                pass
            time.sleep(1)
            x += 1
            print(x)
    except Exception as e:
        print("{} - read hmi port fail. testing stopped.".format(nowtimestr()))
        break
    plc.write_coil(1, 0xfc00, 0)
    print("{} - hmi powered off".format(nowtimestr()))
    time.sleep(5)
    plc.write_coil(1, 0xfc00, 1)
    print("{} - hmi powered on".format(nowtimestr()))
    time.sleep(5)
print("{} - test ended normally.".format(nowtimestr()))

if __name__ == '__main__':
    pass
