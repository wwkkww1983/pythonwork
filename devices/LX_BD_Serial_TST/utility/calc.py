"""this script parse the content of a xml file"""
from math import pow as power
from math import exp as myexp
from ctypes import pointer, c_int, cast, c_float, POINTER


def self_calibration_transform_v(src_data):
    """
    自校准读取的数值转换成为电压（单位：V）
    :param src_data:源数据
    :return dst_data:目标数据
    """
    dst_data = src_data / 262144 * 20.48 - 10.24
    return dst_data


def adv_transform_mv(src_data):
    """
    ADV转换成毫伏电压公式
    :param src_data:源数据
    :return dst_data:目标数据
    """
    dst_data = (78.125 * (src_data - 1) / 1000) - 10240
    return dst_data


def dav_transform_mv(src_data):
    """
    DAV转换成豪伏电压公式
    :param src_data:源数据
    :return dst_data:目标数据
    """
    dst_data = (src_data / 0x40000 * 20.48 - 10.24) * 1000
    return dst_data


def adi_transform_ui(src_data):
    """
    ADI转换成微安电流公式
    :param src_data:源数据,8699上的数字量
    :return dst_data:目标数据
    """
    dst_data = (78.125 * (src_data - 1) / 250) - 40960
    #dst_data = (78.125 * src_data - 10240000) / 250
    return dst_data


def dai_transform_ui(src_data):
    """
    DAI转换成微安电流公式
    :param src_data:源数据
    :return dst_data:目标数据
    """
    dst_data = 1000000 * ((src_data / 0x40000 * 20.48 - 10.24) / 250)
    return dst_data


def tc_transform_mv(src_data):
    """
    tc转换成豪伏电压公式
    :param src_data:源数据
    :return dst_data:目标数据
    """
    dst_data = ((src_data - 2**23) / 3.355) / 1000
    return dst_data


def pt_transform_mo(datum, src_data_a, src_data_b, src_data_c):
    """
    PT转换成毫欧电阻公式
    :param src_data:源数据
    :return dst_data:目标数据
    """
    rfn = 0
    if datum == 1:
        rfn = 68000
    else:
        rfn = 300000
    try:
        dst_data = (src_data_c - 2**23) * rfn / (src_data_b - src_data_a)
    except ZeroDivisionError:
        dst_data = 0
    return dst_data


def hex_split_hight_low_16bit(src_data):
    """
    10进制数据转换成 高8位 和低8位
    :param src_data:源数据
    :return data_hight,data_low:高8位 和低8位
    """
    data_hex = int(hex(int(src_data)), 16)
    data_hight = (data_hex >> 8) & 0xFF
    data_low = data_hex & 0xFF
    return data_hight, data_low


def int_to_float(value):
    """
    十六进制转浮点型数据
    :param value:待转换的数据十进制（int）
    :return : 浮点型数据
    """
    #创建一个int型的指针
    p_int = pointer(c_int(value))
    p_float = cast(p_int, POINTER(c_float))
    float_value = p_float.contents.value
    float_value = round(float_value, 6)
    return float_value


def pt_res_to_temp(res_value):
    """
    pt的电阻转换成温度值
    :param res_value:待转换的电阻值
    :return temp_value: 温度值
    """
    res_value = res_value / 10
    if 6026 < res_value < 10000:
        temp_value = ((
            (res_value) - 10000) / (0.3874 + (10000 - (res_value)) / 397400))
    else:
        rzz = res_value - 10000
        res_value = res_value - 10000
        ree = ((0.0116 * (res_value) * (res_value) + 0.45351 * (res_value)) /
               3056.963)
        res_value = rzz + ree
        ree = ((0.0116 * (res_value) * (res_value) + 0.45351 * (res_value)) /
               3056.963)
        res_value = rzz + ree
        ree = ((0.0116 * (res_value) * (res_value) + 0.45351 * (res_value)) /
               3056.963)
        res_value = rzz + ree
        temp_value = res_value / 0.390958
    return temp_value / 10


def mv_trans_hot_temp(vol_value):
    """
    tc的mv电压换算成热端温度
    :param vol_value:电压值
    :return dst_data:目标数据
    """
    para_below0_k = [
        0.0000000E+00, 2.5173462E+01, -1.1662878E+00, -1.0833638E+00,
        -8.9773540E-01, -3.7342377E-01, -8.6632643E-02, -1.0450598E-02,
        -5.1920577E-04, 0.0000000E+00
    ]
    para_below500_k = [
        0.000000E+00, 2.508355E+01, 7.860106E-02, -2.503131E-01, 8.315270E-02,
        -1.228034E-02, 9.804036E-04, -4.413030E-05, 1.057734E-06, -1.052755E-08
    ]
    para_above500_k = [
        -1.318058E+02, 4.830222E+01, -1.646031E+00, 5.464731E-02,
        -9.650715E-04, 8.802193E-06, -3.110810E-08, 0.000000E+00, 0.000000E+00,
        0.000000E+00
    ]
    p_para = []
    hot_temp = 0
    if -3.852 <= vol_value < 0:
        p_para = para_below0_k
    elif 0 <= vol_value < 20.644:
        p_para = para_below500_k
    elif 20.644 <= vol_value <= 49.202:
        p_para = para_above500_k
    else:
        return 0x7FFF
    for i in range(0, 10):
        hot_temp += p_para[i] * power(vol_value, i)
    hot_temp = hot_temp * 10
    return hot_temp


def __calc_array_value(base, array, count):
    """
    转换公式计算
    :param vol_value:电压值
    :return dst_data:目标数据
    """
    ret_val = 0
    for i in range(0, count):
        ret_val += array[i] * power(base, i)
    return ret_val


def cold_temp_trans_mv(cold_temp):
    """
    tc的冷端温度转毫伏电压
    :param cold_temp:冷端温度
    :return dst_data:目标数据
    """
    cjcbelow_k = [
        0.000000000000E+00, 0.394501280250E-01, 0.236223735980E-04,
        -0.328589067840E-06, -0.499048287770E-08, -0.675090591730E-10,
        -0.574103274280E-12, -0.310888728940E-14, -0.104516093650E-16,
        -0.198892668780E-19, -0.163226974860E-22
    ]
    cjcabove0_k = [
        -0.176004136860E-01, 0.389212049750E-01, 0.185587700320E-04,
        -0.994575928740E-07, 0.318409457190E-09, -0.560728448890E-12,
        0.560750590590E-15, -0.320207200030E-18, 0.971511471520E-22,
        -0.121047212750E-25
    ]
    para_value_a0 = 0.118597600000E+00
    para_value_a1 = -0.118343200000E-03
    para_value_a2 = 0.126968600000E+03
    if -270 <= cold_temp <= 0:
        return __calc_array_value(cold_temp, cjcbelow_k, 10)
    if 0 < cold_temp <= 1372:
        return __calc_array_value(
            cold_temp, cjcabove0_k, 10) + para_value_a0 * myexp(
                para_value_a1 * power(cold_temp - para_value_a2, 2))
    return 0
