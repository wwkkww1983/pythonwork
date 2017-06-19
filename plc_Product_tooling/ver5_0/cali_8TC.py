# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from calibration import CALIBRATION


def calibration():
    cali = CALIBRATION('8TC')
    readtype = cali.read_board_data('board type')
    if readtype == '8TC':
        if cali.busyflag is None:
            if cali.ispassed is None:
                g = cali.set_7190gain(0)                                   # 设置增益G
                for i in range(1, 9):
                    cali.switch_channel(i)                                 # 切换被测板通道

                    res = cali.board['resistances'][0]
                    cali.switch_res(res)                                   # 切换电阻至'1
                    d = cali.readall_anologue()['ad7190_4_double'][0:3]    # 获取当前基准电阻'1特征电压
                    dres1 = cali.calc_ntc_dres(d[0], d[1], d[2], res, g)   # 获取电阻'1实际值
                    cali.write_board_data(1, dres1)                        # 电阻校准值'1发送到被测板

                    res = cali.board['resistances'][1]
                    cali.switch_res(res)                                   # 切换电阻至'2
                    d = cali.readall_anologue()['ad7190_4_double'][0:3]    # 获取当前基准电阻'2特征电压
                    dres2 = cali.calc_ntc_dres(d[0], d[1], d[2], res, g)   # 获取电阻'2实际值
                    cali.write_board_data(2, dres2)                        # 电阻校准值'2发送到被测板

                    res = cali.board['resistances'][2]
                    cali.switch_res(res)
                    res_checkvalue1 = cali.read_board_data('checkres1')

                    res = cali.board['resistances'][3]
                    cali.switch_res(res)
                    res_checkvalue2 = cali.read_board_data('checkres2')


















if __name__ == '__main__':
    print(cali.board['name'])