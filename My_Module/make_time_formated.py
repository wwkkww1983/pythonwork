#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: make_time_formated
# Author:    fan
# date:      2018/12/26
# -----------------------------------------------------------
import time


def nowtimestr(fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime())


def nowtimestamp():
    return time.mktime(time.localtime())


def timestr2timestamp(timestr, fmt='%Y-%m-%d %H:%M:%S'):
    t_tuple = time.strptime(timestr, fmt)
    timestamp = time.mktime(t_tuple)
    return timestamp


def timestamp2timestr(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    t_tuple = time.localtime(timestamp)
    timestr = time.strftime(fmt, t_tuple)
    return timestr


def timestamp2timevalues(timestamp: float or int):
    tm = time.localtime(timestamp)
    time_values = [tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec]
    return time_values


def timevalues2timestamp(timevalues: list):
    pass


def timestr2timevalues(timestr, fmt='%Y-%m-%d %H:%M:%S'):
    t_tuple = time.strptime(timestr, fmt)
    timestamp = time.mktime(t_tuple)
    tm = time.localtime(timestamp)
    time_values = [tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec]
    return time_values


def timevalues2timestr(timevalues, fmt='%Y-%m-%d %H:%M:%S'):
    pass


if __name__ == '__main__':
    print("now time str: {}".format(nowtimestr(fmt='%Y-%m-%d %H:%M:%S')))
    print("now timestamp: {}".format(nowtimestamp()))
    print("time str to timestamp: {}".format(timestr2timestamp("2018-12-26 15:17:11", fmt='%Y-%m-%d %H:%M:%S')))
    print("timestamp to time str: {}".format(timestamp2timestr(1545808631.0, fmt='%Y-%m-%d %H:%M:%S')))
    print("timestamp to time values: {}".format(timestamp2timevalues(1545808631.0)))
