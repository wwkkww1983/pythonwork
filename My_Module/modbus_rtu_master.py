#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: modbus_rtu_master
# Author:    fan
# date:      2018/11/26
# -----------------------------------------------------------
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from watchcom import set_port, open_port, close_port
import logging
import time


def log(*info):
    logger = logging.getLogger('LOG')
    i = ' '.join(info)
    logger.info(i)


class ModbusRtu(object):
    def __init__(self, portprop):
        self._port = set_port(*portprop)    # "COMx", 9600, 8, 1, "N"
        self.master = modbus_rtu.RtuMaster(self._port)
        self.master.set_timeout(5.0)
        self.master.set_verbose(True)
        self.slave_stations = list(range(1, 255))

    def reset_buffer(self):
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()

    def write_coil(self, slv_station, coil_id, status):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            self.master.execute(slv_station, cst.WRITE_SINGLE_COIL, coil_id, output_value=status)

    def write_coils(self, slv_station, coils_start_id, status_list):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            self.master.execute(slv_station, cst.WRITE_MULTIPLE_COILS, coils_start_id, output_value=status_list)

    def read_coil(self, slv_station, coil_id, lenth=1):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            return self.master.execute(slv_station, cst.READ_COILS, coil_id, lenth)

    def read_coils(self, slv_station, coils_start_id, lenth):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            return self.master.execute(slv_station, cst.READ_COILS, coils_start_id, lenth)

    def write_register(self, slv_station, register_id, data):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            self.master.execute(slv_station, cst.WRITE_SINGLE_REGISTER, register_id, output_value=data)

    def write_registers(self, slv_station, register_start_id, data_list):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            self.master.execute(slv_station, cst.WRITE_MULTIPLE_REGISTERS, register_start_id, output_value=data_list)

    def read_register(self, slv_station, register_id, lenth=1):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            return self.master.execute(slv_station, cst.READ_HOLDING_REGISTERS, register_id, lenth)

    def read_registers(self, slv_station, register_id, lenth):
        if slv_station in self.slave_stations:
            self.reset_buffer()
            return self.master.execute(slv_station, cst.READ_HOLDING_REGISTERS, register_id, lenth)


if __name__ == '__main__':
    port_property = ("com7", 9600, 8, 1, "N")

    # master = ModbusRtu(port_property)
    # station_id = 3
    # statuses = [0] * 10
    # values = [500] * 10
    # master.write_coils(station_id, 0x0000, statuses)
    # master.write_coil(station_id, 0x0000, 0)
    # master.write_register(station_id, 0x0000, 100)
    # master.write_registers(station_id, 0x0000, values)
    # print("read coil:", master.read_coil(station_id, 0x0000))
    # print("read coils:", master.read_coils(station_id, 0x0000, 10))
    # print("read register:", master.read_register(station_id, 0x0000))
    # print("read registers:", master.read_registers(station_id, 0x0000, 10))

    def loop_write(portp):
        master = ModbusRtu(portp)
        i = 0
        while 8 - i:
            master.write_coil(1, 0xfc00 + i, 0)
            print("1")
            i += 1
            time.sleep(1)
    # def write(portp):
    #     _port = set_port(*portp)
    #     status = 1
    #     _port.timeout = 2
    #     master = modbus_rtu.RtuMaster(_port)
    #     master.set_timeout(1)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc00, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc01, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc02, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc03, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc04, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc05, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc06, status)
    #     master.execute(3, cst.WRITE_SINGLE_COIL, 0xfc07, status)
    loop_write(port_property)
    # write(port_property)
