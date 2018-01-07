#!/usr/bin/python3

#   8iTC界面所有操作函数——使用函数前需判断debug界面是否打开
#
#   created: Thu Dec 1 9:05:22 2017
#        by:
#
#

import sys
from PyQt5 import QtWidgets
from time import sleep
from PyQt5.QtWidgets import QWidget, QApplication,QMessageBox

from Main_page import Ui_Dialog as Main_Dialog
from Debug_page import Ui_Dialog as Debug_Dialog
from password_dialog import Ui_Dialog as Password_Dialog

class Operation_func(QWidget):
    def __init__(self):
        super().__init__()
        self.M_Dialog=Main_Dialog()
        self.D_Dialog=Debug_Dialog()

        self.mdialog=QWidget()
        self.M_Dialog.setupUi(self.mdialog)
        self.mdialog.showMaximized()
        self.Pass_Dialog=Password_Dialog()
        self.p_dialog=QWidget()
        self.Debug=QWidget()


        self.D_Dialog.setupUi(self.Debug)
        self.Debug.setHidden(True)

        self.Pass_Dialog.setupUi(self.p_dialog)
        self.p_dialog.setHidden(True)

        # self.D_Dialog.setupUi(self.Debug)
        self.setting_click_connect()

    ##按键的点击事件
    def setting_click_connect(self):
        # self.M_Dialog.main_find_device_pushButton.clicked.connect(self.check_device)
        # self.M_Dialog.main_test_byone_pushButton.clicked.connect(self.begin_test)
        self.M_Dialog.main_debug_pyge_toolButton.clicked.connect(self.open_second_window)
        self.Pass_Dialog.buttonBox.accepted.connect(self.p_dialog_ok)
        self.Pass_Dialog.buttonBox.rejected.connect(self.p_dialog_cancel)
        # self.Pass_Dialog.textEdit.setText("123")


    ##按键的点击事件重写<<<
    def open_second_window(self):
        self.Pass_Dialog.textEdit.setText("")
        self.p_dialog.setHidden(False)
        # self.D_Dialog.setupUi(self.Debug)
        # self.Pass_Dialog.setupUi(self.p_dialog)

        # self.Debug.setHidden(False)



        ##     test     <<<<
        # self.D_P3_module_type_choose(6)
        # self.D_P3_channel_choose(1)
        # self.D_P3_gain_choose(3)
        # # self.M_Dialog.close()
        #
        # for i in range(1,9):
        #     j=0
        #     self.D_P2_8_Channel_coldside_T(i, j)
        #     self.D_P2_8_Channel_Sub_Value(i, j)
        #     self.D_P3_8iTC_T_transform_volt(i, j)
        #     self.D_P3_8_Channel_analog_volt(i, j)
        #     self.D_P3_8iTC_transV_sub_Analog_V(i, j)
        #     self.D_P1_volt_current(i,j)
        # self.D_P4_Port_test(2**18-1,1)
        #
        # self.D_P5_debug_info("begin")

        ##    test    >>>>
    def check_device(self):
        self.M_Dialog.main_text_browser.setText("check_device")
    def begin_test(self):
        print("test beginning")
    def p_dialog_ok(self):
        if self.Pass_Dialog.textEdit.text()=="wecon":
            self.p_dialog.close()
            self.Debug.setHidden(False)

        else:
            # QtWidgets.QMessageBox.about(self,"警告","输入密码错误")
            QtWidgets.QMessageBox.warning(self,"警告","输入密码错误",QtWidgets.QMessageBox.Ok)
            self.Pass_Dialog.textEdit.setText("")
    def p_dialog_cancel(self):
        self.p_dialog.close()
    ##>>>

    def M_P_module_type(self, ):
        pass

    ##<Page1> 电压电流显示，index--显示框索引（从左往右，从上往下）、Value--对应的显示值
    def D_P1_volt_current(self, index, Value):
        # dist_VC={1:self.D_Dialog.debug1_5v_v_textBrowser.setText,
        #          2:self.D_Dialog.debug1_5v_a_textBrowser.setText,
        #          3:self.D_Dialog.debug1_f15v_v_textBrowser.setText,
        #          4:self.D_Dialog.debug1_f15v_a_textBrowser.setText,
        #          5:self.D_Dialog.debug1_15v_v_textBrowser.setText,
        #          6:self.D_Dialog.debug1_15v_a_textBrowser.setText,
        #          7:self.D_Dialog.debug1_24v_v_textBrowser.setText,
        #          8:self.D_Dialog.debug1_24v_a_textBrowser.setText}
        # if index in dist_VC:
        #     dist_VC[index](str(Value))
        dist_VC={1:"5v_v",2:"5v_a",3:"f15v_v",4:"f15v_a",5:"15v_v",6:"15v_a",7:"24v_v",8:"24v_a"}
        value=str(Value)
        if index in range(1,9):
            exec("self.D_Dialog.debug1_"+dist_VC[index]+"_textBrowser.setText(value)")
        else:
            ## parameter error
            pass
    ##<Page1> 识别码
    def D_P1_module_ID_code(self, Value):
        self.D_Dialog.debug1_shibiema_textBrowser.setText(str(Value))
    ##<Page1> 掉电保存寄存器
    # def D_P1_BFM_regsiter(self, Value):
    #     self.D_Dialog.debug1_BFM_data_textBrowser.setText(str(Value))

    ##<Page2> 红外模块温度
    def D_P2_Infrared_module_T(self, Value):
        self.D_Dialog.debug2_infrared_data_textBrowser.setText(str(Value))
    ##<Page2> 8通道冷端温度,index--通道、Value--对应通道的值
    def D_P2_8_Channel_coldside_T(self, index, Value):
        # dist_CT={1: self.D_Dialog.debug2_ch1_coldside_T_textBrowser.setText,
        #          2: self.D_Dialog.debug2_ch2_coldside_T_textBrowser.setText,
        #          3: self.D_Dialog.debug2_ch3_coldside_T_textBrowser.setText,
        #          4: self.D_Dialog.debug2_ch4_coldside_T_textBrowser.setText,
        #          5: self.D_Dialog.debug2_ch5_coldside_T_textBrowser.setText,
        #          6: self.D_Dialog.debug2_ch6_coldside_T_textBrowser.setText,
        #          7: self.D_Dialog.debug2_ch7_coldside_T_textBrowser.setText,
        #          8: self.D_Dialog.debug2_ch8_coldside_T_textBrowser.setText}
        # if index in dist_CT:
        #     dist_CT[index](str(Value))
        if index in range(1,9):
            value=str(Value)
            exec("self.D_Dialog.debug2_ch"+str(index)+"_coldside_T_textBrowser.setText(value)")
        else:
            ##index parameter error
            pass
    ##<Page2> 8通道冷端温度与红外测量温度的差值，index--通道、Value--对应的差值
    def D_P2_8_Channel_Sub_Value(self, index, Value):
        # dist_CSV={1: self.D_Dialog.debug2_ch1_Dev_textBrowser.setText,
        #           2: self.D_Dialog.debug2_ch2_Dev_textBrowser.setText,
        #           3: self.D_Dialog.debug2_ch3_Dev_textBrowser.setText,
        #           4: self.D_Dialog.debug2_ch4_Dev_textBrowser.setText,
        #           5: self.D_Dialog.debug2_ch5_Dev_textBrowser.setText,
        #           6: self.D_Dialog.debug2_ch6_Dev_textBrowser.setText,
        #           7: self.D_Dialog.debug2_ch7_Dev_textBrowser.setText,
        #           8: self.D_Dialog.debug2_ch8_Dev_textBrowser.setText}
        # if index in dist_CSV:
        #     dist_CSV[index](str(Value))
        if index in range(1,9):
            value=str(Value)
            exec("self.D_Dialog.debug2_ch"+str(index)+"_Dev_textBrowser.setText(value)")
        else:
            ##index parameter error
            pass

    ##<Page3> 类型选择显示，index--类型选择<1-ADI,2-DAI,3-ADV,4-DAV,5-PT,6-TCV,7-TCR,8-NTC>
    def D_P3_module_type_choose(self, index=6):
        # dist_MTC_C = {1: self.D_Dialog.debug3_type_ADI_radioButton.setChecked,
        #               2: self.D_Dialog.debug3_type_DAI_radioButton.setChecked,
        #               3: self.D_Dialog.debug3_type_ADV_radioButton.setChecked,
        #               4: self.D_Dialog.debug3_type_DAV_radioButton.setChecked,
        #               5: self.D_Dialog.debug3_type_PT_radioButton.setChecked,
        #               6: self.D_Dialog.debug3_type_TCV_radioButton.setChecked,
        #               7: self.D_Dialog.debug3_type_TCR_radioButton.setChecked,
        #               8: self.D_Dialog.debug3_type_NTC_radioButton.setChecked}
        # dist_MTC_D = {1: self.D_Dialog.debug3_type_ADI_radioButton.setCheckable,
        #               2: self.D_Dialog.debug3_type_DAI_radioButton.setCheckable,
        #               3: self.D_Dialog.debug3_type_ADV_radioButton.setCheckable,
        #               4: self.D_Dialog.debug3_type_DAV_radioButton.setCheckable,
        #               5: self.D_Dialog.debug3_type_PT_radioButton.setCheckable,
        #               6: self.D_Dialog.debug3_type_TCV_radioButton.setCheckable,
        #               7: self.D_Dialog.debug3_type_TCR_radioButton.setCheckable,
        #               8: self.D_Dialog.debug3_type_NTC_radioButton.setCheckable}
        # if index in dist_MTC_C:
        #     for i in dist_MTC_C:
        #         dist_MTC_D[i](True)
        #         if index==i:
        #             dist_MTC_C[index](True)
        #             continue
        #         dist_MTC_D[i](False)
            # dist_MTC[index](True)
        value={1:"ADI",2:"DAI",3:"ADV",4:"DAV",5:"PT",6:"TCV",7:"TCR",8:"NTC"}
        if index in range(1,9):
            for i in range(1,9):
                exec("self.D_Dialog.debug3_type_"+value[i]+"_radioButton.setCheckable(True)")
                if index==i:
                    exec("self.D_Dialog.debug3_type_"+value[index]+"_radioButton.setChecked(True)")
                    continue
                exec("self.D_Dialog.debug3_type_"+value[i]+"_radioButton.setCheckable(False)")
        else:
            ##index parameter error
            pass

    ##<Page3> 通道选择显示<1-CH1,2-CH2,3-CH3,4-CH4,5-CH5,6-CH6,7-CH7,8-CH8>
    def D_P3_channel_choose(self, index=1):
        # dist_CC_C = {1: self.D_Dialog.debug3_ch1_radioButton.setChecked,
        #              2: self.D_Dialog.debug3_ch2_radioButton.setChecked,
        #              3: self.D_Dialog.debug3_ch3_radioButton.setChecked,
        #              4: self.D_Dialog.debug3_ch4_radioButton.setChecked,
        #              5: self.D_Dialog.debug3_ch5_radioButton.setChecked,
        #              6: self.D_Dialog.debug3_ch6_radioButton.setChecked,
        #              7: self.D_Dialog.debug3_ch7_radioButton.setChecked,
        #              8: self.D_Dialog.debug3_ch8_radioButton.setChecked}
        # dist_CC_D = {1: self.D_Dialog.debug3_ch1_radioButton.setCheckable,
        #              2: self.D_Dialog.debug3_ch2_radioButton.setCheckable,
        #              3: self.D_Dialog.debug3_ch3_radioButton.setCheckable,
        #              4: self.D_Dialog.debug3_ch4_radioButton.setCheckable,
        #              5: self.D_Dialog.debug3_ch5_radioButton.setCheckable,
        #              6: self.D_Dialog.debug3_ch6_radioButton.setCheckable,
        #              7: self.D_Dialog.debug3_ch7_radioButton.setCheckable,
        #              8: self.D_Dialog.debug3_ch8_radioButton.setCheckable}
        # if index in dist_CC_C:
        #     for i in dist_CC_C:
        #         dist_CC_D[i](True)
        #         if index==i:
        #             dist_CC_C[index](True)
        #             continue
        #         dist_CC_D[i](False)
        if index in range(1,9):
            for i in range(1,9):
                exec("self.D_Dialog.debug3_ch"+str(i)+"_radioButton.setCheckable(True)")
                if index==i:
                    exec("self.D_Dialog.debug3_ch"+str(index)+"_radioButton.setChecked(True)")
                    continue
                exec("self.D_Dialog.debug3_ch"+str(i)+"_radioButton.setCheckable(False)")
                exec('self.D_Dialog.debug3_ch'+str(i)+'_radioButton.update()')
        else:
            ##index parameter error
            pass

    ##<Page3> 增益选择显示<1-1,2-8,3-16,4-32,5-64,6-128>
    def D_P3_gain_choose(self, index=3):
        # dist_GC_C = {1: self.D_Dialog.debug3_gain_1_radioButton.setChecked,
        #              2: self.D_Dialog.debug3_gain_8_radioButton.setChecked,
        #              3: self.D_Dialog.debug3_gain_16_radioButton.setChecked,
        #              4: self.D_Dialog.debug3_gain_32_radioButton.setChecked,
        #              5: self.D_Dialog.debug3_gain_64_radioButton.setChecked,
        #              6: self.D_Dialog.debug3_gain_128_radioButton.setChecked}
        # dist_GC_D = {1: self.D_Dialog.debug3_gain_1_radioButton.setCheckable,
        #              2: self.D_Dialog.debug3_gain_8_radioButton.setCheckable,
        #              3: self.D_Dialog.debug3_gain_16_radioButton.setCheckable,
        #              4: self.D_Dialog.debug3_gain_32_radioButton.setCheckable,
        #              5: self.D_Dialog.debug3_gain_64_radioButton.setCheckable,
        #              6: self.D_Dialog.debug3_gain_128_radioButton.setCheckable}
        # if index in dist_GC_C:
        #     for i in dist_GC_C:
        #         dist_GC_D[i](True)
        #         if index==i:
        #             dist_GC_C[index](True)
        #             continue
        #         dist_GC_D[i](False)
        value={1:"1",2:"8",3:"16",4:"32",5:"64",6:"128"}
        if index in range(1,7):
            for i in range(1,7):
                exec("self.D_Dialog.debug3_gain_"+value[i]+"_radioButton.setCheckable(True)")
                if index==i:
                    exec("self.D_Dialog.debug3_gain_"+value[index]+"_radioButton.setChecked(True)")
                    continue
                exec("self.D_Dialog.debug3_gain_"+value[i]+"_radioButton.setCheckable(False)")
        else:
            ##index parameter error
            pass


    ##<Page3> BFM #27
    def D_P3_write_BFM_27(self, Value):
        self.D_Dialog.debug3_BFM27_textBrowser.setText(str(Value))
    ##<Page3> BFM #67
    def D_P3_write_BFM_67(self, Value):
        self.D_Dialog.debug3_BFM67_textBrowser.setText(str(Value))

    ##<Page3> 8通道模拟模块输出电压，index--通道、Value--通道电压值
    def D_P3_8_Channel_analog_volt(self, index, Value):
        # dist_CAV={1: self.D_Dialog.debug3_ch1_analog_textBrowser.setText,
        #           2: self.D_Dialog.debug3_ch2_analog_textBrowser.setText,
        #           3: self.D_Dialog.debug3_ch3_analog_textBrowser.setText,
        #           4: self.D_Dialog.debug3_ch4_analog_textBrowser.setText,
        #           5: self.D_Dialog.debug3_ch5_analog_textBrowser.setText,
        #           6: self.D_Dialog.debug3_ch6_analog_textBrowser.setText,
        #           7: self.D_Dialog.debug3_ch7_analog_textBrowser.setText,
        #           8: self.D_Dialog.debug3_ch8_analog_textBrowser.setText}
        # if index in dist_CAV:
        #     dist_CAV[index](str(Value))
        if index in range(1,9):
            value=str(Value)
            exec("self.D_Dialog.debug3_ch"+str(index)+"_analog_textBrowser.setText(value)")
        else:
            ##index parameter error
            pass
    ##<Page3> 8iTC 各通道测得温度转换的电压值，index--通道、Value--电压值
    def D_P3_8iTC_T_transform_volt(self, index, Value):
        # dist_T2V={1: self.D_Dialog.debug3_ch1_translate_textBrowser.setText,
        #           2: self.D_Dialog.debug3_ch2_translate_textBrowser.setText,
        #           3: self.D_Dialog.debug3_ch3_translate_textBrowser.setText,
        #           4: self.D_Dialog.debug3_ch4_translate_textBrowser.setText,
        #           5: self.D_Dialog.debug3_ch5_translate_textBrowser.setText,
        #           6: self.D_Dialog.debug3_ch6_translate_textBrowser.setText,
        #           7: self.D_Dialog.debug3_ch7_translate_textBrowser.setText,
        #           8: self.D_Dialog.debug3_ch8_translate_textBrowser.setText}
        # if index in dist_T2V:
        #     dist_T2V[index](str(Value))
        if index in range(1,9):
            value=str(Value)
            exec("self.D_Dialog.debug3_ch"+str(index)+"_translate_textBrowser.setText(value)")
        else:
            ##index parameter error
            pass
    ##<Page3> 各通道模拟模块输出电压与8iTC温度转换电压差值，index--通道、Value--差值
    def D_P3_8iTC_transV_sub_Analog_V(self, index, Value):
        # dist_VSAV={1: self.D_Dialog.debug3_ch1_Dev_textBrowser.setText,
        #            2: self.D_Dialog.debug3_ch2_Dev_textBrowser.setText,
        #            3: self.D_Dialog.debug3_ch3_Dev_textBrowser.setText,
        #            4: self.D_Dialog.debug3_ch4_Dev_textBrowser.setText,
        #            5: self.D_Dialog.debug3_ch5_Dev_textBrowser.setText,
        #            6: self.D_Dialog.debug3_ch6_Dev_textBrowser.setText,
        #            7: self.D_Dialog.debug3_ch7_Dev_textBrowser.setText,
        #            8: self.D_Dialog.debug3_ch8_Dev_textBrowser.setText}
        # if index in dist_VSAV:
        #     dist_VSAV[index](str(Value))
        if index in range(1,9):
            value=str(Value)
            exec("self.D_Dialog.debug3_ch"+str(index)+"_Dev_textBrowser.setText(value)")
        else:
            ##index parameter error
            pass

    ##<Page4> 接线端测试，X_Value--X端子字(位1有效)、Y_Value--Y端子字(位1有效)
    def D_P4_Port_test(self, X_Value,Y_Value):
        value_x=['0' for i in range(18)]
        value_y=['0' for i in range(18)]
        list_x=list(bin(X_Value)[2:])
        list_x=list_x[::-1]
        for i in range(len(list_x)):
            value_x[i]=list_x[i]
        list_y=list(bin(Y_Value)[2:])
        list_y=list_y[::-1]
        for i in range(len(list_y)):
            value_y[i]=list_y[i]

        for i in list(range(8)) + list(range(10,18)):
            # exec("self.D_Dialog.debug4_Y"+str(i)+"_checkBox.setCheckable(True)")
            # if value_y[i]=='1':
            #     exec("self.D_Dialog.debug4_Y"+str(i)+"_checkBox.setChecked(True)")
            exec("self.D_Dialog.debug4_Y" + str(i) + "_checkBox.setHidden(True)")
            #     continue
            # self.D_Dialog.debug4_Y1_checkBox.setHidden()
        for i in list(range(8)) + list(range(10,18)):
            exec("self.D_Dialog.debug4_X"+str(i)+"_checkBox.setHidden(False)")
            if value_x[i]=='1':
                exec("self.D_Dialog.debug4_X"+str(i)+"_checkBox.setChecked(True)")
                continue
            exec("self.D_Dialog.debug4_X" + str(i) + "_checkBox.setHidden(True)")
            # exec("self.D_Dialog.debug4_X"+str(i)+"_checkBox.setCheckable(False)")

    ##<Page5> 调试页面输出
    def D_P5_debug_info(self, log_out):
        self.D_Dialog.debug5_log_textBrowser.append(log_out)
        log_text = self.D_Dialog.debug5_log_textBrowser.toPlainText().splitlines(True)
        if len(log_text) > 255:
            log_text = log_text[-100:]
            self.D_Dialog.debug5_log_textBrowser.setText("".join(log_text))
        # log_buff=""
        # if len(self.LogR)>99:
        #     for i in range(1,10):
        #         self.LogR[i]=self.LogR[i+1]
        #     self.LogR[i+1]=(log_out)
        # else:
        #     self.LogR[len(self.LogR)+1]=(log_out)
        # for i in range(1,len(self.LogR)+1):
        #     log_buff+=self.LogR[i]+"\n"
        # self.D_Dialog.debug5_log_textBrowser.setText(log_buff)
        # for i in self.LogR:
        #     self.D_Dialog.debug5_log_textBrowser.setText()
    ##错误弹窗，title--窗口标题、w--info警告信息
    def warning_widget(self, title, w_info):
        QtWidgets.QMessageBox.warning(self,title,w_info, QtWidgets.QMessageBox.Ok)
    def warning_again_widget(self,w_info):
        chn_wran_flag = QMessageBox.information(self, "错误", w_info,  ####
                                                QMessageBox.Yes | QMessageBox.No)  ####
        return chn_wran_flag








if __name__=='__main__':
    # Oper_func=Operation_func()
    app=QApplication(sys.argv)
    Oper_func=Operation_func()

    sys.exit(app.exec_())
