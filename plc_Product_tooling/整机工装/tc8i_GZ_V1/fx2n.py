# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from crccheck.checksum import Checksum8
import time


class FX2N(object):

    def __init__(self):
        pass

    def read_wrod_directive_pack(self,start_address=0, operal_word_lengh=1):
        """
            将数据组装为FX2N协议规定数据形式
            :param start_address: D0偏移字（内部计算转换成字节数），字
            :param operal_word_lengh: 读取数据长度，字
            :return: 待传输字节串
        """
        stx = [0x02]
        etx = [0x03]
        func_dec = [0x45, 0x30, 0x30]
        start_address_ascii = self.__data_to_ascii([start_address], 4)
        lengh_ascii = self.__data_to_ascii([operal_word_lengh*2])

        #对数据进行和校验
        data_for_check = func_dec + start_address_ascii + lengh_ascii + etx
        check_value = self.__pack_check_sum(data_for_check)

        protocol_data = stx + data_for_check + check_value

        return protocol_data

    def write_wrod_directive_pack(self, start_address=0, operal_word_lengh=32, write_data=[] ):
        """
            将数据组装为FX2N协议规定数据形式
            :param start_address: D0偏移字（内部计算转换成字节数），字
            :param operal_word_lengh: 读取数据长度，字
            :param write_data：要写入的数据，类型列表
            :return: 待传输字节串
        """
        stx = [0x02]
        etx = [0x03]
        func_dec = [0x45, 0x31, 0x30]
        start_address_ascii = self.__data_to_ascii([start_address],4)
        lengh_ascii = self.__data_to_ascii([operal_word_lengh * 2])
        write_data_ascii = self.__data_to_ascii(write_data)
        # 对数据进行和校验
        data_for_check = func_dec + start_address_ascii + lengh_ascii + write_data_ascii + etx
        check_value = self.__pack_check_sum(data_for_check)

        protocol_data = stx + data_for_check + check_value
        return protocol_data

    def read_extended_module_directive_pack(self, mod=0, start_address=0, operal_word_lengh=1):
        """
           读取扩展模块BFM的指令，将数据组装为FX2N协议规定数据形式
           :param start_address: D0偏移字（内部计算转换成字节数），字
           :param operal_word_lengh: 读取数据长度，字
           :return: 待传输字节串
       """
        stx = [0x02]
        etx = [0x03]
        func_dec = [0x46, 0x30]

        mod_ascii = self.__data_to_ascii([mod], 1)
        start_address_ascii = self.__data_to_ascii([start_address], 4)
        lengh_ascii = self.__data_to_ascii([operal_word_lengh * 2])

        # 对数据进行和校验
        data_for_check = func_dec + mod_ascii + start_address_ascii + lengh_ascii + etx
        check_value = self.__pack_check_sum(data_for_check)

        protocol_data = stx + data_for_check + check_value

        return protocol_data
    def write_extended_module_directive_pack(self, mod=0, start_address=0, operal_word_lengh=32, write_data=[] ):
        """
            读扩展模块的BFM指令，以FX2N协议规定数据形式打包
            :param mod: 要操作第几个模块
            :param start_address: 要操作的BFM起始地址
            :param operal_word_lengh: 操作的长度
            :param write_data：要写入的数据，类型列表
            :return: 待传输指令数据
        """
        stx = [0x02]
        etx = [0x03]
        func_dec = [0x46, 0x31]

        mod_ascii = self.__data_to_ascii([mod], 1)
        start_address_ascii = self.__data_to_ascii([start_address],4)
        lengh_ascii = self.__data_to_ascii([operal_word_lengh * 2])
        write_data_ascii = self.__data_to_ascii(write_data,2)
        # 对数据进行和校验
        data_for_check = func_dec + mod_ascii + start_address_ascii + lengh_ascii + write_data_ascii + etx
        check_value = self.__pack_check_sum(data_for_check)

        protocol_data = stx + data_for_check + check_value
        return protocol_data


    def handle_byte_directive_pack(self,start_address,state):
        """
            将数据组装为FX2N协议规定数据形式
            :param start_address: 要操作的位地址
            :param state: 置位或者复位 1/0
            :return: 待传输指令数据
        """
        stx = [0x02]
        etx = [0x03]
        func_dec_on = [0x45, 0x37]
        func_dec_off = [0x45, 0x38]

        start_address_ascii = self.__data_to_ascii([start_address], 4)
        # 对数据进行和校验
        if state == 0:
            func_dec = func_dec_off
        else:
            func_dec = func_dec_on

        data_for_check = func_dec + start_address_ascii + etx
        check_value = self.__pack_check_sum(data_for_check)

        protocol_data = stx + data_for_check + check_value
        return protocol_data


    def protocol_data_analysis(self, receive_data):
        """
            将获取的FX2N协议相关数据进行判断是否操作成功提取返回所需内容
            :param receive_data: 获取的协议相关数据，
            :return: 操作状态或者读到的信息
        """
        receive_data_chr = []
        read_data = []

        if len(receive_data) == 1:
            if receive_data[0] == 0x06: #06是写成功返回码
                return True
            elif receive_data[0] == 0x15:#15响应失败返回码
                return False

        if len(receive_data) > 2:
            # print(receive_data[0], receive_data[-3])
            if receive_data[0] == 2 and receive_data[-3] == 3:
                receive_check_value = []
                receive_check_value = [receive_data[-2]]+[receive_data[-1]]
                data_for_check = receive_data[1:-2]
                cal_check_value = self.__pack_check_sum(data_for_check)

                if cal_check_value == receive_check_value:  # 和校验
                    useful_data = receive_data[1:-3]
                    for i in useful_data:
                        receive_data_chr = receive_data_chr + [chr(i)]
                    receive_data_len = len(receive_data_chr)
                    if receive_data_len % 4 == 0:
                        for s in range(receive_data_len):
                            if s % 4 == 0:
                                temp_data = receive_data_chr[s + 2] + receive_data_chr[s + 3] + receive_data_chr[s] + \
                                    receive_data_chr[s + 1]
                                if int(receive_data_chr[s+2], 16) < 8:
                                    read_data.append(int(temp_data, 16))
                                else:
                                    temp_data = int(temp_data, 16)
                                    temp_data = -((temp_data ^ 0xffff)+1)
                                    read_data.append(temp_data)

                            else:
                                pass

                        return read_data

        return False

    def __data_to_ascii(self, data_needtotransform, word_len= 2):
        """
               将传入的数据转为ASCII码表示以十进制输出
               :param data_needtotransform:需要转换的数据，类型 列表
               :return: 以十进制表示的ASCII码数据
        """
        lengh = []
        for n in data_needtotransform:
            # print(ord(n))
            if word_len == 1:
                len_str = '{:#02X}'.format(n)
            elif word_len == 2:
                len_str = '{:#04X}'.format(n)
            elif word_len == 4:
                len_str = '{:#06X}'.format(n)
            lengh=lengh+[ord(letter) for letter in len_str][2:]
            # print(lengh)
        return lengh

    # def startaddr_to_ascii(self, strt_addr_):
    #     """
    #         将起始地址转为ASCII码以十进制输出
    #         :param strt_addr_:要控制的首地址
    #         :return: 转换后的首地址
    #     """
    #     d0_fmt = 0x4000
    #     d8000_fmt = 0x0E00
    #     strt_addr_str = ''
    #     if strt_addr_ in range(6000, 6032) or range(0, 14):
    #         strt_addr_str = '{:#06X}'.format(strt_addr_ * 2 + d0_fmt)
    #     elif strt_addr_ in range(8000, 8255):
    #         strt_addr_str = '{:#06X}'.format((strt_addr_ - 8000) * 2 + d8000_fmt)
    #     strt_addr_fmt = [ord(letter) for letter in strt_addr_str][2:]
    #     print(strt_addr_fmt)
    #     return strt_addr_fmt
    #
    # def handlelengh_to_ascii(self,len_):
    #     lengh = []
    #     # 读写长度 2_bytes list
    #     if len_ in range(1, 33):
    #         len_str = '{:#04X}'.format(len_ * 2)
    #         lengh = [ord(letter) for letter in len_str][2:]
    #         print(lengh)
    #     return lengh
    def __pack_check_sum(self, check_list):
        """
            对传入数据进行和LRC校验
            :param check_list: 需要校验的数据列表
            :return: 校验和结果
        """
        checksum = []
        # print(check_list)
        # 校验和，1 bytes。功能码、起始地址、数据和结束标识参与校验，起始标识不校验
        check = Checksum8()
        if check_list:
                checksum_int = check.calc(check_list)
                checksum_str = '{:#04X}'.format(checksum_int)
                checksum = [ord(letter) for letter in checksum_str][2:]
        # else:
        #         log.error('chencksum error')
        return checksum

if __name__ == "__main__":
    newdata = [2,1,3]
    read_data1 = newdata[1:-1]
    # print(newdata[0])
    a = FX2N()
    c = a.write_wrod_directive_pack(6030,1,[1,0])
    # print(c)

    # print(c)
    # receive_data_chr = []
    # receive_data = [48, 48, 50, 51, 49, 48, 53, 54, 52, 51, 48, 48]
    # for i in receive_data:
    #     receive_data_chr =receive_data_chr+[chr(i)]
    # print(receive_data_chr[3])
    #
    # data_int_list = []
    # unpack_lengh = len(receive_data_chr)
    # for s in range(unpack_lengh):
    #     if -1 < s < 128:
    #         if s % 4 == 0:
    #             a = receive_data_chr[s+2] + receive_data_chr[s+3] + receive_data_chr[s] + receive_data_chr[s+1]
    #             data_int_list.append(int(a, 16))
    #         else:
    #             pass
    # print(data_int_list)
