# !/usr/bin/python3
# _*_ coding: utf-8_*_

import configparser
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

config = configparser.ConfigParser()
try:
    config.read('boardconfig.ini', encoding='utf-8')
except None:
    log.info('boardconfig.ini file is not found')


def read_inifile_as_dict(sectionname):
    """
    读取ini配置文件为字典数据（C:结构体）
    :param sectionname:
    :return:
    """
    board_dict = {}
    if sectionname not in config.sections():
        log.info('no section named {} in ini file, please check.')
    else:
        section = config[sectionname]
        board_dict = dict(zip([key for key in section], [section[key] for key in section]))
    return board_dict


def board(boardname):
    """
    字典传递及数据字符串类型转其他类型
    :param boardname:
    :return:
    """
    targetboard = read_inifile_as_dict(boardname)
    for key in targetboard.keys():
        if targetboard[key] in ['no', 'No', 'None', 'NO']:
            targetboard[key] = None
        elif targetboard[key] in ['yes', 'Yes', 'True', 'YES', 'OK']:
            targetboard[key] = True

    def todatatype(option_str, type_str):
        """
        某些数据类型需进行转换
        :param option_str: 字典的特定key字符串
        :param type_str: 数据类型描述字符串
        :return:
        """
        if targetboard[option_str]:
            if type_str == 'int':
                targetboard[option_str] = int(targetboard[option_str])
            elif type_str == 'intlist':
                targetboard[option_str] = [int(item) for item in targetboard[option_str].split(',')]
            elif type_str == 'strlist':
                    targetboard[option_str] = [item for item in targetboard[option_str].split(',')]

    todatatype('channel quantity', 'int')
    todatatype('test type', 'strlist')
    todatatype('resistances', 'intlist')
    todatatype('vi limited1 values', 'intlist')
    todatatype('vi limited2 values', 'intlist')
    return targetboard

if __name__ == '__main__':
    board('8TC')
