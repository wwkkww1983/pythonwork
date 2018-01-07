
from PyQt5.QtWidgets import  QWidget,QMessageBox
from plc import PLC
from gongzhuang import GongZhuang
import logging as log
from ctypes import *
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

import time
from data_manage import DataOperation
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class TC8I(QThread):
    _signal_D5_info=pyqtSignal(str)     #ui第五页日志
    _signal_D1_shibie=pyqtSignal(int)      #ui第一页识别码
    _signal_D1_module_v=pyqtSignal(list)   #第一页电压值
    _signal_D2=pyqtSignal(list)         #ui第二页全部数据
    _signal_D3_channel=pyqtSignal(int) #ui第三页通道选择
    _signal_D3_BFM=pyqtSignal(list)     #ui第三页BFM
    _signal_D3_CHn=pyqtSignal(list)      #ui第三页电压
    _signal_D4_XY=pyqtSignal(list)      #ui第4页
    _signal_warn_window = pyqtSignal(str)  #警告弹窗
    _signal_device_name=pyqtSignal(str) #首页显示扩展模块识别
    _signal_test_again=pyqtSignal(int) #是否重试
    _signal_check_label=pyqtSignal(str) #首页测试lebal
    pause = QMutex()  ##---##
    def __init__(self, plc_name, digital_name, analog_name,all=1,a=0,b=0,c=0,d=0,e=0):
        super().__init__()      #继承QThreading####
        self.plc_name = plc_name
        self.analog_name = analog_name
        self.digital_name = digital_name

        self.handle_plc = PLC(plc_name)
        self.handle_gongzhuang = GongZhuang(digital_name, analog_name)
        self.data_handle_formula = DataOperation()

        self.all=all
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.e=e
    def run(self):

        if self.all==1:     ####
            self._signal_check_label.emit('检测中....')
            if self.first_step()==True:    ####
                if self.second_setp()==True:    ####
                    if self.third_setp()==True:  ####
                    # if True:
                        if self.fourth_setp()==True:     ####
                            if self.fifth_setp()==True:     ####
                                self._signal_check_label.emit('检测通过')
                            return  True
        # elif self.a==1:   self.first_step()
        # elif self.b==1:   self.second_setp()
        # elif self.c==1:   self.third_setp()
        # elif self.d==1:   self.fourth_setp()
        # elif self.e==1:   self.fifth_setp()
        else: return False  ####
        # self.first_step()
        # self.second_setp()
        # self.third_setp()
        # self.fourth_setp()
        # self.fifth_setp()

    def first_step(self):
        ##上电
        self._signal_D5_info.emit('上电')  ####
        self.handle_gongzhuang.power_up()
        time.sleep(2)
        self.handle_plc.hid_star(self.plc_name)
        time.sleep(1)

        extended_module_code = self.handle_plc.get_extended_module()
        if extended_module_code == False:
            self._signal_warn_window.emit("扩展模块获取失败")
            return False
        self._signal_device_name.emit(extended_module_code)####
        #moudle_name=self.handle_plc.get_extended_module()  #############################
        ##检查供电是否正常
        self._signal_D5_info.emit('开始检查供电是否正常')  ####

        supply_volt_list = self.handle_gongzhuang.get_power_supply()
        if supply_volt_list == False:
            self._signal_warn_window.emit("SYS-EP")
            return False
        # print(supply_volt_list)
        self._signal_D1_module_v.emit(supply_volt_list)
        for i in range(4):
            state = self.data_handle_formula.judge_source_volt(i, supply_volt_list[i][0])
            if state != True:
                self._signal_warn_window.emit(state)  ####
                return False

        ##检查被测模块识别码
        self._signal_D5_info.emit('开始检查被测模块识别码')  ####
        read_data = self.handle_plc.read_extended_module_BFM(0, 30, 1)
        if len(read_data) == 0:
            self._signal_warn_window.emit("MOD-EC0")
            return False
        time.sleep(1)
        if read_data[0] == 2038:
            self._signal_D5_info.emit('被测模块识别码为：2038')  ####
            self._signal_D1_shibie.emit(2038)    ####
            read_data = self.handle_plc.read_extended_module_BFM(1, 0, 1)
            if len(read_data) == 0:
                self._signal_warn_window.emit("MOD-EC1")
                return False
            if read_data[0] ==5012:
                self._signal_D1_shibie.emit(5012)    ####
                self._signal_D5_info.emit('被测模块识别码为：5012')  ####
                return True
            else:
                self._signal_warn_window.emit("MOD-EC1") ####
                print("MOD-EC1")

        elif read_data == False:
            self._signal_warn_window.emit("MOD-EC0") ####
            print("MOD-EC0")

        else:
            self._signal_warn_window.emit("MOD-EM0") ####
            print("MOD-EM0")

    def second_setp(self):
        ##为扩展块BFM写值
        self._signal_D5_info.emit('开始为扩展块BFM写值')  ####
        self.handle_plc.write_extended_module_BFM(0, 27, 1, [0x22, 0x22])
        self.handle_plc.write_extended_module_BFM(0, 67, 1, [0x22, 0x22])

        #下电
        self._signal_D5_info.emit('开始下电')  ####
        self.handle_gongzhuang.power_down()
        time.sleep(3)
        self.handle_gongzhuang.power_up()
        time.sleep(2)
        self.handle_plc.hid_star(self.plc_name)

        time.sleep(2)
        data_27BFM = self.handle_plc.read_extended_module_BFM(0, 27, 1)
        if len(data_27BFM) == 0:
            self._signal_warn_window.emit("MOD-ES0")
            return False
        data_67BFM = self.handle_plc.read_extended_module_BFM(0, 67, 1)
        if len(data_67BFM) == 0:
            self._signal_warn_window.emit("MOD-ES0")
            return False
        self.list_D3_BFM=[0]*2   ####
        self.list_D3_BFM[0],self.list_D3_BFM[1]=str(data_27BFM)[1:-1],str(data_67BFM)[1:-1] ####
        self._signal_D3_BFM.emit(self.list_D3_BFM)   ####
        if data_27BFM[0] == data_67BFM[0] == 0x2222:
            return True
        else:
            self._signal_warn_window.emit("MOD-ES0")  ####
            print("MOD-ES0")

    def third_setp(self):
        ##读取8itc模块内置冷端温度
        self._signal_D5_info.emit('开始读取8iTC模块内置冷端温度')  ####
        list_D2 = [0] * 17  ####
        self.handle_plc.write_extended_module_BFM(0, 26, 2, [0,0,0,0])
        self.handle_plc.write_extended_module_BFM(0, 66, 2, [0,0,0,0])
        code_tem_ch14 = self.handle_plc.read_extended_module_BFM(0, 21, 4)
        if len(code_tem_ch14) == 0:
            self._signal_warn_window.emit("8iTC-EL")
            return False
        code_tem_ch58 = self.handle_plc.read_extended_module_BFM(0, 61, 4)
        if len(code_tem_ch58) == 0:
            self._signal_warn_window.emit("8iTC-EL")
            return False
        code_temperature_8itc = code_tem_ch14 + code_tem_ch58
        code_temperature_8itc = [code_temperature_8itc[i]/10.0 for i in range(8)]
        list_D2[1:9]=code_temperature_8itc  ####
        print(code_temperature_8itc)

        ##读取模拟模块红外温度
        self._signal_D5_info.emit('开始读取模拟模块红外温度')  ####
        temperature_analog_data =self.handle_gongzhuang.read_infrared_temperature(1)
        if len(temperature_analog_data) == 0:
            self._signal_warn_window.emit("8iTC-EL")
            return False
        analog_infrared_temperature_ch1 =temperature_analog_data[0]
        list_D2[0]=analog_infrared_temperature_ch1  ####
        #print(analog_infrared_temperature_ch1)
       # print(list_D2[0])
        for i in range(8):
            list_D2[9+i]=(code_temperature_8itc[i]-analog_infrared_temperature_ch1)   ####
        # analog_infrared_temperature_ch2 = self.hex_to_float(temperature_analog_data[1])
            self._signal_D2.emit(list_D2)        ####
        state = self.__judge_module_coldside_valid(analog_infrared_temperature_ch1, code_temperature_8itc)
        if state == False:
            self._signal_warn_window.emit("8iTC-EL")  ####
            self._signal_D5_info.emit('检测失败，冷端温差过大')

        return state


    def fourth_setp(self):

        list_D3_CHn=[0]*24      ####
        self.handle_plc.write_extended_module_BFM(0, 27, 1, [0x22, 0x22])
        self.handle_plc.write_extended_module_BFM(0, 67, 1, [0x22, 0x22])

        self._signal_D5_info.emit('开始读取BFM27&67的值')  ####
        data_27BFM = self.handle_plc.read_extended_module_BFM(0, 27, 1)
        if len(data_27BFM) == 0:
            self._signal_warn_window.emit("第四步测试错误")
            self._signal_D5_info.emit('检测失败')
            return False
        data_67BFM = self.handle_plc.read_extended_module_BFM(0, 67, 1)
        if len(data_67BFM) == 0:
            self._signal_warn_window.emit("第四步测试错误")
            self._signal_D5_info.emit('检测失败')
            return False
        self.list_D3_BFM[0],self.list_D3_BFM[1]=str(data_27BFM)[1:-1],str(data_67BFM)[1:-1]   ####
        self._signal_D3_BFM.emit(self.list_D3_BFM)   ####

        if data_27BFM[0] == data_67BFM[0] == 0x2222:
            self._signal_D5_info.emit('开始读取热端温度测试')  ####
            for j in range(2):
                set_channel_list = [85, 170]
                read_channel_list = [[9, 11, 49, 51], [10, 12, 50, 52]]
                CHn_select_list=[[1,3,5,7],[2,4,6,8]]

                self.handle_gongzhuang.set_test_channel(set_channel_list[j])

                self.handle_gongzhuang.set_test_type(5)
                self.handle_gongzhuang.set_gain_number(16)
                self.handle_gongzhuang.enabled_volt_output()

                for i in [-5, 20, 40]:
                    self.handle_gongzhuang.set_out_volt(i)
                    time.sleep(4)

                    for m,n in zip(read_channel_list[j],CHn_select_list[j]):
                        Ch_test_flag=True
                        while Ch_test_flag:
                            self._signal_D3_channel.emit(n)  ####
                            analog_ch4_data = self.handle_gongzhuang.get_analog_ch4_volt()
                            if len(analog_ch4_data) == 0:
                                self._signal_warn_window.emit("CH4通道读取失败")
                                self._signal_D5_info.emit('检测失败')
                                return False
                            analog_ch4_volt = self.data_handle_formula.register_volt(analog_ch4_data[0])
                            list_D3_CHn[n-1]=analog_ch4_volt  ####

                            ch_temp = self.handle_plc.read_extended_module_BFM(0,m,1)
                            if len(ch_temp) == 0:
                                self._signal_warn_window.emit("被测通道热端温度读取失败")
                                self._signal_D5_info.emit('检测失败')
                                return False
                            volt_K=self.data_handle_formula.Ktemp2volt(ch_temp[0])
                            list_D3_CHn[n+7]=volt_K ####
                            list_D3_CHn[n+15]=int(analog_ch4_volt-volt_K)   ####
                            self._signal_D3_CHn.emit(list_D3_CHn)    ####

                            state = self.data_handle_formula.judge_volt_validity(i,analog_ch4_volt,volt_K)
                            # Ch_test_flag=False

                            if state ==False:

                                print("8ITC-EH",n)
                                self.handle_gongzhuang.set_test_channel(0)
                                self._signal_test_again.emit(n) ###############
                                self.pause.lock()
                                self.pause.lock()
                                # self._signal_test_again.emit(n) ###############
                                self.pause.unlock()
                                # Ch_test_flag = False

                            else:
                                Ch_test_flag = False
                        # elif state == True:
                        #     flag =False

            self.handle_gongzhuang.set_test_channel(0)
            return True



    def fifth_setp(self):

        self.handle_gongzhuang.power_down()
        error_str = ''
        error_list = self.handle_gongzhuang.control_Yport_sequential_output()
        if error_list == True:
            self._signal_D5_info.emit('测试成功')
            return True
        else:
            self._signal_D4_XY.emit(error_list)
            for i in range(len(error_list)):
                error_str = error_str + str(error_list[i]) + '、'
            error_str ='端子'+ error_str + '连接在一起'
            self._signal_warn_window.emit(error_str)
            self._signal_D5_info.emit('检测失败')
            print('端子', error_list, '连接在一起')
            return False

    ##                                          模拟模块红外温度（度） 8itc获取温度（度）
    def __judge_module_coldside_valid(self, analog_module_readT, coldside_T):
        max_coldside_temp = max(coldside_T)
        min_coldside_temp = min(coldside_T)
        if max_coldside_temp - min_coldside_temp < 0.4:
            if abs(analog_module_readT - max_coldside_temp) < 0.5 and abs(
                            analog_module_readT - min_coldside_temp) < 0.5:
                return True
            else:
                ##log.info
                return False
        else:
            ##log.info
            return False

                            #十进制数
    def hex_to_float(self,value):
        cp = pointer(c_int(value))  # make this into a c integer
        fp = cast(cp, POINTER(c_float))
        return fp.contents.value

if __name__ == "__main__":
    pass
