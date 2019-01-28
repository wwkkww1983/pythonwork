#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hmi_rtc_check.py
# Author:    fan
# date:      2018/12/26
# -----------------------------------------------------------
import requests as req
from make_time_formated import nowtimestamp, nowtimestr, timestamp2timestr, timestr2timestamp, timestamp2timevalues
from modbus_rtu_master import ModbusRtu
from time import sleep
import threading as thread
debug = False


def get_beijing_timestamp():
    """
    获取标准北京时间
    """
    url = "http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
    # get方法返回数据格式：
    # {'ret': ['SUCCESS::接口调用成功'], 'v': '*', 'api': 'mtop.common.getTimestamp', 'data': {'t': '1545807646734'}}
    bj_timestamp = 0
    try:

        get_data = req.get(url).json()
        if get_data["ret"][0] == "SUCCESS::接口调用成功":
            bj_timestamp = get_data["data"]["t"]
            bj_timestamp = float(bj_timestamp[:10]+"."+bj_timestamp[-3:])  # 注意，web获取的时间戳单位为毫秒
        else:
            pass
    except Exception as e:
        print(nowtimestr())
        print("error, get beijing time fail from url({}). detail: {}".format(url, e))
    if debug:
        print("get the beijing timestamp:", bj_timestamp)
    return bj_timestamp


def read_device_time_values(mst: ModbusRtu, station=1):
    # communicate with device to get device time
    dev_time_values = ()
    try:
        dev_time_values = mst.read_registers(station, 0, 6)
    except Exception as e:
        print("error: modbus read registers fail. detail: {}".format(e))
    if debug:
        print("read time values from device: {}".format(dev_time_values))
    return list(dev_time_values)


def get_device_timestamp(timevalues: list):
    dev_timestamp = 0
    if len(timevalues) == 6:
        dev_time = "{}-{}-{} {}:{}:{}".format(*timevalues)
        dev_timestamp = timestr2timestamp(dev_time)
    if debug:
        print("get the device timestamp:", dev_timestamp)
    return dev_timestamp


def write_beijing_time_to_device(mst, station=1):
    beijing_timestamp = get_beijing_timestamp()
    timevalues = timestamp2timevalues(beijing_timestamp)
    mst.write_registers(station, 10, list(timevalues))
    sleep(0.01)
    mst.write_coil(station, 10000, 1)


def main(mstplc, msthmi, station):
    err_count = 0
    j = 0
    while j <= 20000:
        j += 1
        beijing_timestamp = get_beijing_timestamp()
        # 北京时间写入hmi
        timevalues = timestamp2timevalues(beijing_timestamp)

        device_timevalues = [0] + [0] * 5
        beijing_timestamp = 0
        try:
            msthmi.write_registers(station, 10, list(timevalues))
            sleep(0.1)
            msthmi.write_coil(station, 10000, 1)
            sleep(5)
            mstplc.write_coil(1, 0xfc00, 0)
            sleep(5)
            mstplc.write_coil(1, 0xfc00, 1)
            sleep(10)
            # 读回对比
            beijing_timestamp = get_beijing_timestamp()  # 需要重新获取北京时间
            device_timevalues = read_device_time_values(msthmi, station)
        except Exception as e:
            print(e)

        beijing_timestr = timestamp2timestr(beijing_timestamp)
        device_timestamp = get_device_timestamp(device_timevalues)
        device_timestr = timestamp2timestr(device_timestamp)
        err = device_timestamp - beijing_timestamp
        if err >= 5 or err <= -5:
            is_err = True
        else:
            is_err = False
        if is_err:
            err_count += 1
        fmt_log = [nowtimestr(),
                   beijing_timestr,
                   str(beijing_timestamp),
                   device_timestr,
                   str(device_timestamp),
                   str(err),
                   str(is_err),
                   str(err_count),
                   str(j)]
        log = ", ".join(fmt_log)
        log = "".join([log, "\n"])
        # print(""
        #       "北京时间：{}  -- 时间戳：{}\n"
        #       "设备时间：{}  -- 时间戳：{}"
        #       "".format(beijing_timestr, beijing_timestamp, device_timestr, device_timestamp))
        with open("hmi rtc test log.csv".format(station), "a", encoding="utf-8") as f:
            f.write(log)
        print(log)


def start_tst():
    portpplc = ("COM9", 9600, 8, 1, "O")
    portphmi = ("COM7", 9600, 8, 1, "O")
    masterplc = ModbusRtu(portpplc)
    masterhmi = ModbusRtu(portphmi)
    station_id = 1
    head = "{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(
        "logtime",
        "bj_time",
        "bj_timestamp",
        "dev_time",
        "dev_timestamp",
        "error(sec.dev-bj)",
        "is_error?",
        "err_count",
        "total_count")
    with open("hmi rtc test log.csv", "w", encoding="utf-8") as f:
         f.write("{} slave {} test log\n".format(nowtimestr(), station_id))
         print("start logging")
         f.write(head)
         print(head)
    masterplc.write_coils(1, 0xfc00, [1, 1])

    main(masterplc, masterhmi, station_id)


if __name__ == '__main__':
    # time_values = [2018, 12, 26, 16, 42, 11]
    # get_beijing_timestamp()
    # get_device_timestamp(time_values)
    # portp = ("COM7", 9600, 8, 1, "N")
    # master = ModbusRtu(portp)
    # write_beijing_time_to_device()
    # sleep(0.1)
    # main(master, 1)
    start_tst()
    # for k in range(5):
    #     sleep(1)
    #     pass