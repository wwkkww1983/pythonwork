
from fx2n import FX2N
from usbhid_handle import MYUSBHID as myhid
import logging as log
import time
from data_manage import DataOperation
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')
class PLC(object):
    def __init__(self, name):
        self.extended_module_code = {2010: 'LX3V-4AD', 2030: 'LX3V-4TC',2130: 'LX3V-4LTC',2040: 'LX3V-4PT',
                                2038: 'LX3V-8ITC',2048: 'LX3V-4PT',3020: 'LX3V-4DA',5011: 'LX3V-1WT',
                                5012: 'LX3V-2WT',5110: 'LX3V-4PG_BAS',5120: 'LX3V-4PG_ADV'}
        self.bottom_protocol = FX2N()
        self.communicate_protocol_PLC = myhid(name)
        self.data_operation = DataOperation()

        self.communicate_protocol_PLC.start()
        self.communicate_protocol_PLC.setcallback()

    def hid_star(self, name):
        self.communicate_protocol_PLC = myhid(name)
        self.communicate_protocol_PLC.start()
        self.communicate_protocol_PLC.setcallback()
    def get_extended_module(self):
        module_code = self.read_extended_module_BFM(0, 30, 1)
        if len(module_code) == 0:
            return False

        return self.extended_module_code[module_code[0]]


    def write_sof_element(self, start_adds, write_len, write_data):
        '''
        对PLC的软元件写值
        :param start_address: 操作的首地址
        :param operal_word_lengh: 操作的数据长度，字
        :param write_data：要写入的数据，类型列表
        :return: 是否成功写入
        '''
        send_list = self.bottom_protocol.write_wrod_directive_pack(start_adds, write_len, write_data)

        self.communicate_protocol_PLC.write(send_list)
        time.sleep(0.005)
        receive_list = self.communicate_protocol_PLC.unpack_hid_data()
        state = self.bottom_protocol.protocol_data_analysis(receive_list)

        if state == True:
            log.info('write Analog_BFM succeed')
        return state

    def read_sof_element(self,start_adds, write_len):
        '''
        对PLC的软元件读值
        :param start_address: 操作的首地址
        :param operal_word_lengh: 操作的数据长度，字
        :return: 读回的数据
        '''
        send_list = self.bottom_protocol.read_wrod_directive_pack(start_adds, write_len)

        self.communicate_protocol_PLC.write(send_list)
        time.sleep(0.005)
        receive_list = self.communicate_protocol_PLC.unpack_hid_data()
        state = self.bottom_protocol.protocol_data_analysis(receive_list)

        if state == False or state == True:
            log.info('read sof element not succeed')
            return []
        else:
            return state

    def read_extended_module_BFM(self, mod, start_adds, read_len):
        '''
        对PLC的所连接的扩展模块的BFM进行读取
        :param mod :要操作的模块
        :param start_address: 操作的首地址
        :param operal_word_lengh: 操作的数据长度，字
        :return: 读回的数据
        '''
        send_list = self.bottom_protocol.read_extended_module_directive_pack(mod, start_adds, read_len)

        for i in range(3):
            self.communicate_protocol_PLC.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_PLC.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == False or state == True:
                log.info('read extended module BFM not succeed')
            else:
                return state

        return []

    def write_extended_module_BFM(self, mod, start_adds, write_len, write_data):
        send_list = self.bottom_protocol.write_extended_module_directive_pack(mod,start_adds, write_len, write_data)
        for i in range(3):
            self.communicate_protocol_PLC.write(send_list)
            time.sleep(0.01)
            receive_list = self.communicate_protocol_PLC.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == True:
                return state
            else:
                log.info('write extended module BFM NOT succeed')
        return False


if __name__ == "__main__":
    pass
