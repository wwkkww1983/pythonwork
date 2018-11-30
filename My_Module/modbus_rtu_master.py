#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: modbus_rtu_master
# Author:    fan
# date:      2018/11/26
# -----------------------------------------------------------
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from watchcom import set_port, open_port, close_port
import logging


def log(*info):
    logger = logging.getLogger('LOG')
    i = ' '.join(info)
    logger.info(i)


class ModbusRtu(object):
    def __init__(self, port):
        self.master = modbus_rtu.RtuMaster(port)
        self.master.set_timeout(5.0)
        self.master.set_verbose(True)
        self.slave_station = [0, 1]

    def write_coil(self, slv_station, coil_id, status):
        if slv_station in self.slave_station:
            self.master.execute(slv_station, cst.WRITE_SINGLE_COIL, coil_id, output_value=status)

    def write_coils(self, slv_station, coils_start_id, status_list):
        if slv_station in self.slave_station:
            self.master.execute(slv_station, cst.WRITE_MULTIPLE_COILS, coils_start_id, output_value=status_list)

    def write_register(self, slv_station, register_id, data):
        if slv_station in self.slave_station:
            self.master.execute(slv_station, cst.WRITE_SINGLE_REGISTER, register_id, output_value=data)

    def write_registers(self, slv_station, register_start_id, data_list):
        if slv_station in self.slave_station:
            self.master.execute(slv_station, cst.WRITE_MULTIPLE_REGISTERS, register_start_id, output_value=data_list)

    def read_coil(self, slv_station, coil_id, lenth=1):
        if slv_station in self.slave_station:
            return self.master.execute(slv_station, cst.READ_COILS, coil_id, lenth)

    def read_coils(self, slv_station, coils_start_id, lenth):
        if slv_station in self.slave_station:
            return self.master.execute(slv_station, cst.READ_COILS, coils_start_id, lenth)


if __name__ == '__main__':
    port = set_port("com50", 9600, 8, 1, "N")
    station_id = 1
    master = ModbusRtu(port)
    # master.write_coils(station_id, 0x0000, [1, 0, 0, 0, 0, 0, 0, 1])
    # master.write_coil(station_id, 0x0000, 0)
    # master.write_register(station_id, 0x0000, 100)
    # master.write_registers(station_id, 0x0000, [5200, 200])
    print(master.read_coil(1, 0x0000))
    print(master.read_coils(1, 0x0000, 10))
