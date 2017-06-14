# !/usr/bin/python
# -*- coding: utf-8 -*-

import math
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
        self.channel = 0
        self.testtypes = 'unknow type'
        self.check_value = 0
        self.cali_parameter = 0
        self.varify_value = 0
        self.tested_board = 'abc'
        self.tested_board = self.get_selected_board('8TC')
        # 这里“8TC”信息由UI设置中获取

    def get_selected_board(self, slctbdtype):
        slctbd = board()
        slctbd.get_board(slctbdtype)
        if slctbd.board_type == 'unknow type':
            log.warning('选择型号不可用，请检查')
            return None
        if slctbd.board_type in slctbd.boardlist:
            log.info('选择型号{} 信息已载入'.format(slctbd.name))
            return slctbd

    def select_benchmark(self):
        """
        根据型号选择基准对象
        :return:
        """
        pass

    def read_board(self):
        pass

    def write_board(self):
        pass

    def calc_ntc(self, chl_num, *bchmk):
        """
        ntc校准
        :param chl_num: 通道数
        :param bchmk: 基准参数
        :return: 校准数据，误差，通过标识
        """
        pass

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
    log.info('selected board={}'.format(c.get_selected_board('8TC')))



if __name__ == '__main__':
    main()