# !/usr/bin/python
# -*- coding: utf-8 -*-


class PlcBoardTestTool(object):
    def __init__(self):
        self.poweron = False
        self.digital_board_ch_id = 0x0
        self.v24_ch1_switch = False
        self.n15_ch2_switch = False
        self.p15_ch3_switch = False
        self.v5_ch4_switch = False
        self.v_ch5_switch = False
        self.v_ch6_switch = False
        self.v_ch7_switch = False
        self.v_ch8_switch = False

