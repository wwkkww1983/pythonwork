# !/usr/bin/python
# -*- coding: utf-8 -*-

import math
import time
import logging as log
from boards import TESTEDBOARD as board

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class CALIBRATION(object):
    def __init__(self):
        """
        提供校准过程实现的方法
        :param tested_board: instance of board
        :return:
        """
        self.expected_board = self.get_board('8TC')  # 这里“8TC”信息由UI设置中获取
        self.bench_resistance = self.get_bench_resistance()
        self.busyflag = None
        self.cominterval = 0.1
        self.check_value = 0
        self.cali_parameter = 0
        self.varify_value = 0


    def get_board(self, slctbdtype):
        """
        获取型号配置信息
        :param slctbdtype:
        :return:
        """
        slctbd = board()
        slctbd.get_board(slctbdtype)
        if slctbd.board_type == 'unknow type':
            log.warning('选择型号不可用，请检查')
            return None
        if slctbd.board_type in slctbd.boardlist:
            log.info('选择型号\'{}\'信息已载入'.format(slctbd.name))
            return slctbd

    def get_bench_resistance(self):
        """
        根据型号选择基准电阻
        :return: 基准电阻列表
        """
        reslist = self.expected_board.resistances.split(',')
        reslist_int = []
        for res in reslist:
            reslist_int.append(int(res))
        log.info('get bench resistance: {}'.format(reslist_int))
        return reslist_int

    def read_board(self):
        pass

    def write_board(self):
        pass

    def set_channel(self):
        pass

    def determinate_res(self):
        """
        检测电阻，可能通过不同方式
        :return:
        """
        initvalue = 0  #res检测初始值
        return initvalue

    def calc_ntc(self):
        """
        ntc校准
        :param chl_num: 通道数
        :param bchmk: 基准参数
        :return: 校准数据，误差，通过标识
        """
        benchress = self.bench_resistance
        initvalue_a = 0
        initvalue_b = 0
        calires_a = benchress[0]
        calires_b = benchress[1]
        caliparam_a = 0
        caliparam_b = 0
        checkres_a = benchress[2]
        checkres_b = benchress[3]
        calierror_a = 0
        calierror_b = 0
        if self.busyflag is not None:
            log.info('校准程序忙')
        else:
            for channel in range(self.expected_board.channel_quantity):
                self.set_channel(channel)
                time.sleep(self.cominterval)
                initvalue_a = self.determinate_res(calierror_a)
                time.sleep(self.cominterval)




    def calc_tcv(self):
        pass

    def calc_tcr(self):
        pass

    def calc_pt(self):
        pass

    def calc_adi(self):
        pass

    def calc_dai(self):
        pass

    def calc_adv(self):
        pass

    def calc_dav(self):
        pass

def main():
    # b = board()
    # b.board_type = '8TC'
    # b.print_board_info()
    c = CALIBRATION()
    log.info('selected board={}'.format(c))



if __name__ == '__main__':
    main()