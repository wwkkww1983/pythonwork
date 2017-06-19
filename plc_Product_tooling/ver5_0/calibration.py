# !/usr/bin/python
# -*- coding: utf-8 -*-

import math
import time
import logging as log
from boardtypes import board

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class CALIBRATION(object):
    def __init__(self, slctboard):
        """
        提供校准过程实现的方法
        :param tested_board: instance of board
        :return:
        """
        self.board = board(slctboard)  # 选择被测板类型后即决定该class下所有函数是否被执行、参数是什么
        self.busyflag = None
        self.ispassed = None
        self.steptime = 0.1
        self.check_value = 0
        self.cali_parameter = 0
        self.varify_value = 0


    # def calibration(self):
    #     cali_results = []
    #     for type in self.board['try type']:
    #         if type == 'NTC':
    #             cali_results.append(self.cali_ntc())
    # 组装校准程序，考虑放到主程序文件中

    def set_7190gain(self, type):
        if type == '8TC':
            portA.write('gain', 0)


    def read_type(self, param):
        if param == 'board type':
            return portA.read('type')

    def write_board(self, params):
        return False

    def switch_channel(self, x):
        pass

    def switch_res(self):
        pass

    def get_res_realvalue(self):
        """
        获取电阻真实值，可能通过不同方式，需要滤波？设置增益，
        :return:
        """
        realvalue = 0  #res检测初始值
        return realvalue

    def get_res_feedbkvalue(self):
        """
        获取电阻检测值，通过board，需要滤波？设置增益
        :return:
        """
        realvalue = 0  #res检测初始值
        return realvalue

    def cali_ntc(self):
        """
        ntc校准,a,b,c,d分别代表4组电阻检测：校准1，校准2，检验1，检验2
        :param chl_num: 通道数
        :param bchmk:
        :return: 校准数据，误差，通过标识
        """
        if self.busyflag is not False:
            log.error('调用函数 {} 时资源使用冲突，请检查'.format(__name__))
            return
        else:
            pass
        channelnum = self.board.channel_quantity
        channellist = list(range(1, 1+channelnum)) # 通道从1开始算
        benchress = self.bench_resistance
        # 存放ntc校准的参数、误差、当前值, 用于显示
        ntc_cali_params = [0] * channelnum  # 最终结果可能是个tuple列表
        ntc_cali_errors = [0] * channelnum
        ntc_current_values = [0] * channelnum
        ntc_calipass = [False] * channelnum

        res_a = benchress[0]
        res_b = benchress[1]
        res_c = benchress[2]
        res_d = benchress[3]
        initvalue_res_a = 0
        initvalue_res_b = 0
        initvalue_res_c = 0
        initvalue_res_d = 0
        realvalue_res_a = 0
        realvalue_res_b = 0
        realvalue_res_c = 0
        realvalue_res_d = 0
        caliparam_a = 0
        caliparam_b = 0
        calierror_c = 0
        calierror_d = 0

        def calc_param(rra,ira,rrb,irb):
            parama = func(rra,ira)
            paramb = func(rrb,irb)
            return parama,paramb

        def calc_error(rrc,irc,rrd,ird):
            return errorfunc(rrc,irc,rrd,ird)

        if self.busyflag is not None:
            log.info('校准程序忙，等待响应...')
        else:
            # 每个通道依次校准，并在一次循环中尽量保留所有信息，数据处理到位。不要多次循环
            for channel in channellist:  # 每个通道依次检测
                self.switch_channel(channel)  # 设定当前通道，一次只能设置1个通道为开

                # 获取校准电阻a,b的真实值、回显值
                time.sleep(self.comintervaltime)  # 操作间隔（硬件切换时间和通讯占用），下同
                realvalue_res_a = self.get_res_realvalue(res_a)
                time.sleep(self.comintervaltime)
                initvalue_res_a = self.get_res_feedbkvalue(res_a)
                time.sleep(self.comintervaltime)
                realvalue_res_b = self.get_res_realvalue(res_b)
                time.sleep(self.comintervaltime)
                initvalue_res_b = self.get_res_feedbkvalue(res_b)

                # 根据4组值，计算校准参数并写入被测板
                if realvalue_res_a & initvalue_res_a & realvalue_res_b & initvalue_res_b is None:
                    log.error('NTC校准过程获取电阻值错误，通道={}, 阻值={}'.format(
                        channel, [realvalue_res_a, initvalue_res_a, realvalue_res_b, initvalue_res_b]))
                    break
                else:
                    params = calc_param(realvalue_res_a,initvalue_res_a,realvalue_res_b,initvalue_res_b)
                    ntc_cali_params[channel-1] = params  # 每个通道将相应校准参数整合到一个列表中
                    writed = self.write_board(*params)
                    time.sleep(self.comintervaltime)
                    if writed is False:
                        log.error('NTC校准过程通讯错误，通道={}, 参数={}'.format(channel, params))
                        break
                    else:
                        pass

                # 获取检验电阻d,c的真实值、回显值
                realvalue_res_c = self.get_res_realvalue(res_c)  # 获取真实值，通过红外模块？下同
                time.sleep(self.comintervaltime)
                initvalue_res_c = self.get_res_feedbkvalue(res_c)  # 获取检测值，通过被测板，下同
                time.sleep(self.comintervaltime)
                realvalue_res_d = self.get_res_realvalue(res_d)
                time.sleep(self.comintervaltime)
                initvalue_res_d = self.get_res_feedbkvalue(res_d)

                # 根据4组值，计算该通道误差，并显示。
                if realvalue_res_c & initvalue_res_c & realvalue_res_d & initvalue_res_d is None:
                    log.error('NTC检验过程获取电阻值错误，通道={}, 阻值={}'.format(
                        channel, [realvalue_res_c, initvalue_res_c, realvalue_res_d, initvalue_res_d]))
                    break
                else:
                    error = calc_error(realvalue_res_c,initvalue_res_c,realvalue_res_d,initvalue_res_d)
                    ntc_cali_errors[channel-1] = error


        if ntc_calipass != [True]*channelnum:
            log.info('NTC 校准失败，通过情况：通道{}=误差{}={}'.format(channellist, ntc_cali_errors, ntc_calipass))
        else:
            log.info('NTC 校准通过，通道{}=误差{}'.format(channellist, ntc_cali_errors))

        return ntc_calipass, ntc_cali_errors



    def cali_tcv(self):
        pass

    def cali_tcr(self):
        pass

    def cali_pt(self):
        pass

    def cali_adi(self):
        pass

    def cali_dai(self):
        pass

    def cali_adv(self):
        pass

    def cali_dav(self):
        pass


def main():
    c = CALIBRATION('8TC')
    log.info('selected board = {}'.format(c.board['name']))



if __name__ == '__main__':
    main()