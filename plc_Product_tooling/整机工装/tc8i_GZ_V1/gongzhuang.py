
from fx2n import FX2N
from usbhid_handle import MYUSBHID as myhid
import logging as log
import time
from data_manage import DataOperation
from ctypes import *
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

class GongZhuang(object):
    def __init__(self, digital_name, analog_name):
        self.bottom_protocol = FX2N()
        self.communicate_protocol_analog = myhid(analog_name)
        self.communicate_protocol_digital = myhid(digital_name)

        self.data_operation = DataOperation()

        self.communicate_protocol_digital.start()
        self.communicate_protocol_digital.setcallback()
        self.communicate_protocol_analog.start()
        self.communicate_protocol_analog.setcallback()

    def analog_hid_stop(self):
        self.communicate_protocol_analog.stop()

    def power_up(self):

        set_state = self.__write_Digital_BFM(6030*2+0x4000, 1, [1,0])
        return set_state

    def power_down(self):

        set_state = self.__write_Digital_BFM(6030*2+0x4000, 1, [0,0])
        return set_state

    def get_power_supply(self):
        power_volt_list =[]
        for i in range(4):
            read_num = self.__read_Digital_BFM((6016+2*i)*2+0x4000, 1)
            if len(read_num)==0:
                return False
            power_volt_list.append(read_num)
            # state = self.data_operation.judge_source_volt(i,read_num[0])

        return power_volt_list

    def set_test_type(self,type = 6):

        state = self.__write_Analog_BFM(0X0018, 1, [type, 0])

        if state == True:
            log.info('set_test_type succeed')

    def set_test_channel(self, channel_number):

        state = self.__write_Analog_BFM(0X001A, 1, [channel_number, 0])

        if state == True:
            log.info('set_test_channel succeed')

    def set_basic_standard(self,basic_standard_num = 6):

        state = self.__write_Analog_BFM(0X001A, 1, [basic_standard_num, 0])

        if state == True:
            log.info('set_basic_standard succeed')

    def set_gain_number(self,gain_number = 16):

        state = self.__write_Analog_BFM(0X001E, 1, [gain_number, 0])

        if state == True:
            log.info('power up succeed')

    def control_Yport_sequential_output(self):

        self.__byte_handle(0,1)

        front_list =[i for i in range(8)] + [-1 for i in range(8)]
        back_list = [-1 for i in range(8)] + [i for i in range(8)]
        connection_port_list = []

        for i in range(16):
            Y_front_8byte = int(2**front_list[i])
            Y_back_8byte  = int(2**back_list[i])
            self.__write_Digital_BFM(6050*2+0x4000,2,[Y_front_8byte,0,Y_back_8byte,0])
            time.sleep(0.2)
            Xport_list =self.__read_Digital_BFM(6052*2+0x4000,2)
            # if len(Xport_list) == 0:
            #     return False
            Xport_front_8byte = Xport_list[0]
            Xport_back_8byte  = Xport_list[1]

            if Xport_front_8byte != Y_front_8byte or Xport_back_8byte != Y_back_8byte:
                for m in range(8):
                    if Xport_front_8byte % 2 == 1:
                        connection_port_list.append(m)
                    if Xport_back_8byte % 2 == 1:
                        connection_port_list.append(m+10)
                    Xport_front_8byte = int(Xport_front_8byte / 2)
                    Xport_back_8byte = int(Xport_back_8byte / 2)
                self.__byte_handle(0, 0)
                return connection_port_list
        self.__byte_handle(0, 0)
        return True




    def read_infrared_temperature(self, channel_number=1):

        code_temp_list = []
        infrared_temperature_list= []

        for i in range(4):
            # code_temperature =self.__read_Analog_BFM(0x0022+2*(i+1)-1, 1) + self.__read_Digital_BFM(0x0022+2*(i), 1)
            code_temperature = self.__read_Analog_BFM(0x22+4*i, 2)
            if len(code_temperature) ==0:
                return []
            if code_temperature[0] <0:
                low16_data = hex(((-code_temperature[0]) ^ 0xffff) + 1)[2:]
                low16_data = low16_data.zfill(4)
            else:
                low16_data = hex(code_temperature[0])[2:]
                low16_data = low16_data.zfill(4)

            if code_temperature[1] <0:
                high16_data = hex(((-code_temperature[1]) ^ 0xffff) + 1)[2:]
            else:
                high16_data = hex(code_temperature[1])[2:]

            code_temperature = high16_data + low16_data
            # code_temp_list.append(int(code_temperature, 16))

            infrared_temperature = self.hex_to_float(int(code_temperature,16))
            infrared_temperature_list.append(infrared_temperature)

        return infrared_temperature_list

    def set_out_volt(self,out_volt):

        #输出电压单位为uV
        dVes = out_volt*10000


        dDes = 65536 * ((1.385*dVes+ 1000000) / 2000000)
        dDes_temp = hex(int(dDes))[2:]
        dDes_temp = dDes_temp.zfill(4)
        dDes_high =int(dDes_temp[:2],16)
        dDes_low =int(dDes_temp[2:],16)

        state = self.__write_Analog_BFM(0x14, 1, [dDes_low, dDes_high])
        return state

        # return dDes
    def enabled_volt_output(self):
        self.__write_Analog_BFM(0x20,1,[1,0])

    def get_analog_ch4_volt(self):
        analog_ch4_data=[]
        high16 = self.__read_Analog_BFM(0xe, 1)
        if len(high16) == 0:
            return []
        low16 = self.__read_Analog_BFM(0xc, 1)
        if len(low16) == 0:
            return []

        value_list = high16 + low16

        high16_data = hex(value_list[0])[2:]
        if value_list[1] < 0:
            low16_data = hex(((-value_list[1]) ^ 0xffff) + 1)[2:]
            low16_data = low16_data.zfill(4)
        else:
            low16_data = hex(value_list[1])[2:]
            low16_data = low16_data.zfill(4)


        temp_value = high16_data+low16_data
        analog_ch4_data.append(int(temp_value, 16))

        # analog_ch4_volt = self.Analog_count_ADC7190_V(analog_ch4_data[0],16)


        return analog_ch4_data

    def Analog_count_ADC7190_V(self,ADC7190_data,G):
        ADC7190_volt = (ADC7190_data - (1<<23))*4.096/(G*(1<<23))
        return ADC7190_volt

    def __write_Analog_BFM(self,start_adds, write_len, write_data):

        send_list = self.bottom_protocol.write_wrod_directive_pack(start_adds, write_len, write_data)
        for i in range(3):
            self.communicate_protocol_analog.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_analog.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == True :
                log.info('write Analog BFM succeed')
                return state
            else:
                log.info('write Analog BFM NOT succeed')
        return False

    def __read_Analog_BFM(self, start_adds, read_len):
        send_list = self.bottom_protocol.read_wrod_directive_pack(start_adds, read_len)

        for i in range(3):

            self.communicate_protocol_analog.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_analog.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == False or state == True:
                log.info('read Analog_BFM not succeed')
            else:
                return state

        return []
    def __write_Digital_BFM(self, start_adds, write_len, write_data):

        send_list = self.bottom_protocol.write_wrod_directive_pack(start_adds, write_len, write_data)

        for i in range(3):

            self.communicate_protocol_digital.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_digital.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == True :
                log.info('write Analog_BFM succeed')
                return state
            else:
                log.info('write Analog BFM NOT succeed')

        return False

    def __read_Digital_BFM(self, start_adds, read_len):
        send_list = self.bottom_protocol.read_wrod_directive_pack(start_adds, read_len)

        for i in  range(3):

            self.communicate_protocol_digital.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_digital.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == False or state == True:
                log.info('read Digital_BFM  not succeed')
            else:
                return state

        return []
    def __byte_handle(self, start_adds, state):
        send_list = self.bottom_protocol.handle_byte_directive_pack(start_adds, state)

        for i in range(3):
            self.communicate_protocol_digital.write(send_list)
            time.sleep(0.005)
            receive_list = self.communicate_protocol_digital.unpack_hid_data()
            state = self.bottom_protocol.protocol_data_analysis(receive_list)

            if state == False:
                log.info(' byte handle not succeed')
            else:
                return state

        return False

    def hex_to_float(self,value):
        cp = pointer(c_int(value))  # make this into a c integer
        fp = cast(cp, POINTER(c_float))
        return fp.contents.value

if __name__ == "__main__":

    from crccheck.checksum import Checksum8
    a=GongZhuang( 'DIGITAL MODULE VER1', 'ANALOG MODULE VER1')

    c = FX2N()

    infrared_list = a.read_infrared_temperature()
    print(infrared_list)

    # def pack_check_sum(check_list):
    #     """
    #         对传入数据进行和LRC校验
    #         :param check_list: 需要校验的数据列表
    #         :return: 校验和结果
    #     """
    #     checksum = []
    #     # print(check_list)
    #     # 校验和，1 bytes。功能码、起始地址、数据和结束标识参与校验，起始标识不校验
    #     check = Checksum8()
    #     if check_list:
    #             checksum_int = check.calc(check_list)
    #             checksum_str = '{:#04X}'.format(checksum_int)
    #             checksum = [ord(letter) for letter in checksum_str][2:]
    #     # else:
    #     #         log.error('chencksum error')
    #     return checksum
    #
    #
    #
    # a = [ 69, 55,56,56, 48, 49, 3]
    # d = pack_check_sum(a)
    # print(d)
    # lengh = []
    # # print(a)
    #
    #
    #
    # # for i in range(4):
    # b = 0x0188
    # len_str = '{:#06X}'.format(b)
    # lengh = lengh + [ord(letter) for letter in len_str][2:]
    # c = chr(lengh[1])
    # # print(len_str)
    # print(lengh)
    # # print(c)

