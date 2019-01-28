"""this script parse the content of a xml file"""
import binascii
from PyCRC.CRC16 import CRC16


def __crc16_check(check_list):
    """
    CRC校验
    :param check_list: 待校验的列表
    :return:CRC校验值 2*8位 （list）
    """
    check_byte = b''
    check_len = len(check_list)

    # 将列表中的值提取出来组成一串新的位串
    for i in range(check_len):
        temporary_var = check_list[i]
        # 转换成相同的字符串即'0x11'
        temporary_var = hex(temporary_var)
        # 截取掉'0x'
        temporary_var = "{:0>2s}".format(temporary_var[2:])
        temporary_var = binascii.a2b_hex(temporary_var)
        check_byte += temporary_var

    # 调用CRC16校验库函数进行校验
    check_num = hex(CRC16(modbus_flag=True).calculate(check_byte))
    check_num_list = []
    check_num = "{:0>4s}".format(check_num[2:])
    check_num_list.append(int(check_num[0:2], 16))
    check_num_list.append(int(check_num[2:4], 16))

    return check_num_list


def add_crc16_check(check_list):
    """
    以大端模式把校验码加到传入列表后面
    :param check_list: 待校验的列表
    :return:带CRC校验码的数据串
    """
    check_num_list = __crc16_check(check_list)

    check_list.append(check_num_list[1])
    check_list.append(check_num_list[0])
    # 以大端方式加到传进来的列表返回
    return check_list


if __name__ == '__main__':
    pass
