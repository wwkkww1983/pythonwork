# !/usr/bin/python
# -*- coding: utf-8 -*-

import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')



class MODULE(object):
    def __init__(self):
        """
        根据硬件和下位机文档，确定各模块对应属性
        UI显示标签和校准运算过程均以该对象下配置的名称为准
        """
        self.name = '未知模块'
        self.index = 32767
        self.three_state = 0xf
        self.hardware_type = 'unknown'
        self.used_trip = 'unknown'
        self.use_resistance = False
        self.main_unit = ''
        self.vice_unit = ''
        self.remarks = ''
        self.channel_quantity = 0
        self.ready = False
        self.resistance = [0, 0, 0, 0]
        self.error = ''
        self.modulelist = config['total']['MODULELIST'].split(',')

    def get_module(self, module=''):
        if module not in self.modulelist:
            self.error = '"{0}" is not in module list'.format(module)
        else:
            section = config[module]
            self.name = section['module name']
            self.index = int(section['index'])
            self.three_state = int(section['three state'], 16)
            self.hardware_type = section['hardware type']
            self.used_trip = section['used trip']
            self.use_resistance = section.getboolean('use resistance')
            self.vice_unit = section['vice unit']
            self.remarks = section['remarks']
            self.channel_quantity = int(section['channel quantity'])
            if self.use_resistance:
                self.resistance = [int(section['resistance1']),int(section['resistance2']),
                                   int(section['resistance3']),int(section['resistance4'])]

    def get_modulelist(self):

        return self.modulelist

    def print_module_info(self):
        print("""\
                Information of this module:
                name: %s
                index: %d
                three state: %d
                hardware type: %s
                used trip: %s
                channel quantity: %d
                use resistance %d
                main unit: %s
                vice unit: %s
                remarks: %s
                """ % (self.name,
                       self.index,
                       self.three_state,
                       self.hardware_type,
                       self.used_trip,
                       self.channel_quantity,
                       self.use_resistance,
                       self.main_unit,
                       self.vice_unit,
                       self.remarks))
        self.print_error()

    def print_error(self):
        print(self.error)


if __name__ == '__main__':
    module = MODULE()
    module.get_module('8pt')
    print(module.modulelist)
    module.print_module_info()
