# !/usr/bin/python3
# _*_ coding: utf-8_*_

import configparser
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


def read_config_file(filename):
    config = configparser.ConfigParser()
    try:
        config.read(filename, encoding='utf-8')
    except None:
        log.info('boardconfig.ini file is not found')
    return config


def read_section_as_dict(sectionname):
    """
    读取ini配置文件为字典数据（C:结构体）
    :param sectionname:
    :return:
    """
    config = read_config_file()
    board_dict = {}
    sec = config.sections()
    if sectionname not in sec:
        log.info('no section named={} in ini file, please check.'.format(sectionname))
    else:
        section = config[sectionname]
        board_dict = dict(zip([key for key in section], [section[key] for key in section]))
    return board_dict


def get_board(boardname):
    """
    字典传递及数据字符串类型转其他类型
    :param boardname:
    :return:
    """
    targetboard = read_section_as_dict(boardname)
    for key in targetboard.keys():
        if targetboard[key] in ['0', 'no', 'No', 'None', 'NO']:
            targetboard[key] = None
        elif targetboard[key] in ['1', 'yes', 'Yes', 'True', 'YES', 'OK']:
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
    if boardname != 'DEFAULT' and boardname != 'boards':
        todatatype('channel quantity', 'int')
        todatatype('test type', 'strlist')
        todatatype('resistances', 'intlist')
        todatatype('vi limited1 values', 'intlist')
        todatatype('vi limited2 values', 'intlist')
    return targetboard


def get_board_list(sec='boards'):
    """
    从.ini文件获取模块信息
    :return:
    """
    boards = read_section_as_dict(sec)
    board_list = boards.get('name list')
    return board_list

if __name__ == '__main__':
    read_config_file('boardconfig.ini')
    log.info(get_board('8TC'))
    log.info(get_board_list('boards'))
