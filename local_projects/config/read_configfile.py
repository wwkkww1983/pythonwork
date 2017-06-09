#! /usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
default = 'DEFAULT'
# config = configparser.ConfigParser()
# config.read('example.ini', encoding='gb2312')
# all_sections = config.sections()
# age = config[default]['a ge']
# is_student = config[default].getboolean('is student')


# print(all_sections)
# age = int(age.split(',')[0])
# print(age)
# print(is_student)

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
all_sections = config.sections()

module = '8pt'


class MODULE(object):
    def __init__(self, name, index, three_state, hardware_type, used_trip, channel_quantity,
                 use_resistance, resistance1, resistance2, resistance3, resistance4,
                 main_unit, vice_unit, remarks):
        self.name = name
        self.index = index
        self.three_state = three_state
        self.hardware_type = hardware_type
        self.used_trip = used_trip
        self.channel_quantity = channel_quantity
        self.use_resistance = use_resistance
        self.resistance1 = resistance1
        self.resistance2 = resistance2
        self.resistance3 = resistance3
        self.resistance4 = resistance4
        self.main_unit = main_unit
        self.vice_unit = vice_unit
        self.remarks = remarks

    def print_info(self):
        print("""\
        Information of this module:
        name: %s
        index: %d
        three state: %d
        hardware type: %s
        used trip: %s
        channel quantity: %d
        use resistance %d
        resistance1: %d
        resistance2: %d
        resistance3: %d
        resistance4: %d
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
               self.resistance1,
               self.resistance2,
               self.resistance3,
               self.resistance4,
               self.main_unit,
               self.vice_unit,
               self.remarks))

if __name__ == '__main__':
    section = config[module]
    this_module = MODULE(section['name'],
                         int(section['index']),
                         int(section['three state'], 16),
                         section['hardware type'],
                         section['used trip'],
                         int(section['channel quantity']),
                         section.getboolean('use resistance'),
                         int(section['resistance1']),
                         int(section['resistance2']),
                         int(section['resistance3']),
                         int(section['resistance4']),
                         section['main unit'],
                         section['vice unit'],
                         section['remarks'])

    this_module.print_info()
