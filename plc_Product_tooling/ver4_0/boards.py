# !/usr/bin/python
# -*- coding: utf-8 -*-

import configparser

BOARDTYPECODE = {'8TC': 0x3F, '未知类型': 0xFFFF}
TESTTYPECODE = dict(
    ADI=0x1, DAI=0x2, ADV=0x3, DAV=0x4, PT=0x4, TCV=0x5, TCR=0x6, NTC=0x7)
config = configparser.ConfigParser()
try:
    config.read('config.ini', encoding='utf-8')
except:
    print('config.ini file is not found')


class TESTEDBOARD(object):
    def __init__(self):
        """
        根据硬件和下位机文档，确定各模块对应属性
        UI显示标签和校准运算过程均以该class下配置的名称为准
        name: 界面显示名称
        board_type: 型号描述的核心字符串
        test_types: 校准类型列表（包含校准的顺序，一个被测板可有多个校准类型）
        unit：显示单位
        channel_quantity: 通道数，校准过程及后台显示使用此参数
        use_resistance: 当前被测板是否使用基准电阻
        resistances: 基准电阻列表（包含顺序）
        remarks: 当前被测板备注信息
        """
        self.name = 'unknow name'
        self.board_type = 'unknow type'
        self.test_types = []
        self.unit = ''
        self.channel_quantity = 0

        self.use_resistance = False
        self.resistances = [0, 0, 0, 0]
        self.remarks = ''
        self.vi_limited1_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.vi_limited2_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.boardlist = config['TOTAL']['BOARDLIST'].split(',')
        self.ready = False
        self.error = ''

    def get_board(self, board_type=''):
        if board_type not in self.boardlist:
            self.error = '"{0}" is not in module list'.format(board_type)
        else:
            section = config[board_type]
            self.name = section['name']
            self.board_type = section['board type']
            self.test_types = section['test type']
            self.unit = section['display unit']
            self.channel_quantity = int(section['channel quantity'])
            self.vi_limited1_values = section['vi limited1 values']
            self.vi_limited2_values = section['vi limited2 values']

            self.use_resistance = section.getboolean('use resistance')
            if self.use_resistance:
                self.resistances = [int(section['resistance1']),
                                    int(section['resistance2']),
                                    int(section['resistance3']),
                                    int(section['resistance4'])]

            self.remarks = section['remarks']

    def get_boardlist(self):

        return self.boardlist

    def print_board_info(self):
        print("""\
                Information of this module:
                name: {0}
                board type: {1}
                test types: {2}
                display unit: {3}
                channel quantity: {4}
                use resistance: {5}
                resistances: {6}
                vi limited1 values: {7}
                vi limited2 values: {8}
                remarks: {9}
                """.format(self.name, self.board_type, self.test_types, self.unit, self.channel_quantity,
                           self.use_resistance, self.resistances, self.vi_limited1_values, self.vi_limited2_values,
                           self.remarks))
        self.print_error()

    def print_error(self):
        print(self.error)


if __name__ == '__main__':
    board = TESTEDBOARD()
    board.get_board('8TC')
    print(board.boardlist)
    board.print_board_info()
