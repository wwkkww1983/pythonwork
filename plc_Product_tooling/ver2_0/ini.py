# !/usr/bin/env python3
# _*_ coding: utf-8 _*_


def config_by_module_type(module_type):
    # 定义配置文件的方式，获取模块设置型号，返回该型号对应的配置参数

    # 初始化
    model_name = ''
    device_type = ''
    show_unit = ''
    tri_state = 0
    channel_num = 0
    measuring_type = ''
    resistance_reference = ()

    # 预定义各项参数的取值范围，可在工装最终确定时进行调整
    MODULES = (u'LX 8PT', u'LX 8TC')
    DEVICE_TYPES = (u'ADI', u'DAI', u'ADV', u'DAV', u'PT', u'TCV', u'TCR', u'NTC')
    CHANNEL_NUMBER = (1, 2, 4, 8)
    MEASURING_TYPES = (u'ADC7190', u'ADS8699_A', u'ADS8699_V', u'DAC8760_A', u'DAC8760_V')
    # ADC7190 电阻测量；ADS8699 电压或电阻测量；DAC8760 给定电压或电流；其他类型需确认
    RESISTANCE_REFERENCES = (0, 100, 200, 300, 400, 500, 600, 700, 800)
    TRI_STATE= (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    SHOW_UNIT = (u'mV', u'mA', u'℃', u'Ω', u'1')

    if module_type == MODULES[0]:
        model_name = MODULES[0]
        device_type = DEVICE_TYPES[4]
        show_unit = SHOW_UNIT[2]
        tri_state = TRI_STATE[15]
        channel_num = CHANNEL_NUMBER[3]
        measuring_type = MEASURING_TYPES[0]
        resistance_reference = (RESISTANCE_REFERENCES[1],)

    module_info = (model_name,
                   device_type,
                   show_unit,
                   channel_num,
                   measuring_type,
                   resistance_reference,
                   tri_state)
    print(
            '\n模块名称(s)：', model_name,
            '\n模块类型(s)：', device_type,
            '\n预设单位(s)：', show_unit,
            '\n通道数量(i)：', channel_num,
            '\n检测芯片(s)：', measuring_type,
            '\n对应电阻(i)：', resistance_reference,
            '\n三态检测(i)：', tri_state
        )
    return module_info

