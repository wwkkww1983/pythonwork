#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: modbus_asc_master
# Author:    fan
# date:      2018/12/25
# -----------------------------------------------------------
import minimalmodbus as modbus


def master_init(port, baudrate):
    ins = modbus.Instrument(port, 1, "ascii")
    ins.serial.baudrate = baudrate
    ins.serial.bytesize = 8
    ins.serial.stopbits = 1
    ins.serial.parity = "N"
    ins.serial.timeout = 0.3
    return ins


def read_regs(mst: modbus.Instrument, start: int, count: int):
    return mst.read_registers(start, count)


def write_regs(mst:modbus.Instrument, start: int, data: list):
    mst.write_registers(start, data)

if __name__ == '__main__':
    pt = "COM7"
    baud = 921600
    start_addr = 0
    addr_count = 100
    master = master_init(pt, baud)
    write_regs(master, 0, [40000, 0, 40000, 0, 40000])
    read_data = read_regs(master, start_addr, addr_count)
    print(read_data)
