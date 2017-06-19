# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from calibration import CALIBRATION

def readall_digit():
    """
    监控数字板数据
    :return:
    """
    return

def readall_anologue():
    """
    监控模拟板数据
    :return:
    """
    return

def readall_board():
    """
    监控被测板数据
    :return:
    """

def calibration():
    cali = CALIBRATION('8TC')
    readtype = cali.read_type('board type')
    if readtype == '8TC':
        cali.set_7190gain('8TC')
        if cali.busyflag == None:
            if cali.ispassed == None:
                for i in range(1, 9):
                    cali.switch_channel(i)
                    cali.switch_res(cali.board['resistances'][0])
                    v1 = cali.get_res_realvalue()
                    cali.switch_res(cali.board['resistances'][1])
                    v2 = cali.get_res_realvalue()

















if __name__ == '__main__':
    print(cali.board['name'])