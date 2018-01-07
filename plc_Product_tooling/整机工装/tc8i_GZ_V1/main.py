from tc8i import TC8I
import Widget_deal_func,Device_Thread
from PyQt5.QtWidgets import QApplication

import sys


app = QApplication(sys.argv)
ui=Widget_deal_func.Operation_func()
test_8itc = TC8I('PLC USB HID VER1', 'DIGITAL MODULE VER1', 'ANALOG MODULE VER1',all=1)
check_device_name=Device_Thread.Dev_Thread()
warn_flag=0
def info(a):
    ui.D_P5_debug_info(a)

def D2_list(b):
    ui.D_P2_Infrared_module_T(b[0])
    for i in range(1,9):
        ui.D_P2_8_Channel_coldside_T(i,b[i])
        ui.D_P2_8_Channel_Sub_Value(i,b[i+8])

def D1_shibie(c):
    ui.D_P1_module_ID_code(c)

def D3_channel(d):
    ui.D_P3_channel_choose(d)


def D3_BFM(e):
    ui.D_P3_write_BFM_27(str(e[0]))
    ui.D_P3_write_BFM_67(str(e[1]))

def D3_CHn(f):
    for i in range(8):
        ui.D_P3_8_Channel_analog_volt(i+1,f[i])
        ui.D_P3_8iTC_T_transform_volt(i+1,f[i+8])
        ui.D_P3_8iTC_transV_sub_Analog_V(i+1,f[i+16])

def D4_XY(g):
    x=0
    for i in g:
        x+=1<<i
        ui.D_P4_Port_test(x,0)
    pass
def warn_window(h):     #警告窗操作函数
    test_8itc.terminate()
    ui.M_Dialog.label2.setText('检测失败')

    ui.warning_widget(title ='错误',w_info=h)

# def warn_window_again(i):
#     ui.warning_again_widget(i)

def D1_module_v(j):
    for i in range(4):
        ui.D_P1_volt_current(7-2*i,j[i][0])

def check_device(z):
    if z[0]==True:
        ui.D_Dialog.debug1_PLC_check_textBrowser.setText('已连接')
    else:ui.D_Dialog.debug1_PLC_check_textBrowser.setText('连接已断开')
    if z[2]==True:
        ui.D_Dialog.debug1_Amodul_check_textBrowser.setText('已连接')
    else:ui.D_Dialog.debug1_Amodul_check_textBrowser.setText('连接已断开')
    if z[1] == True:
        ui.D_Dialog.debug1_Dmodul_check_textBrowser.setText('已连接')
    else:ui.D_Dialog.debug1_Dmodul_check_textBrowser.setText('连接已断开')

def main_label(t):
    ui.M_Dialog.label2.setText(t)
def main_find_device(y):
    ui.M_Dialog.main_text_browser.setText(y)


def begin_run(test):
    # if test!=True:
    #     test_8itc.start()
    # test_8itc.pause.lock()

    if test>0 and test<9:
        if ui.warning_again_widget("测试错误，是否重试？")!=16384:
            # print(ui.warning_again_widget("测试错误，是否重试？"))
            # test_8itc.pause.unlock()

        # else:
            ui.warning_widget("错误","8ITC-EH%d" % test)

            test_8itc.terminate()
        test_8itc.pause.unlock()

    else:test_8itc.start()


    ui.D_P3_module_type_choose(6)
    ui.D_P3_gain_choose(3)
    ui.D_P4_Port_test(0, 0)



test_8itc._signal_D5_info.connect(info)
test_8itc._signal_D2.connect(D2_list)
test_8itc._signal_D1_shibie.connect(D1_shibie)
test_8itc._signal_D3_channel.connect(D3_channel)
test_8itc._signal_D3_BFM.connect(D3_BFM)
test_8itc._signal_D3_CHn.connect(D3_CHn)
test_8itc._signal_D1_module_v.connect(D1_module_v)
#test_8itc._signal_warn_again_window.connect(warn_window_again)
test_8itc._signal_D4_XY.connect(D4_XY)
test_8itc._signal_warn_window.connect(warn_window)
test_8itc._signal_device_name.connect(main_find_device)
test_8itc._signal_test_again.connect(begin_run)
test_8itc._signal_check_label.connect(main_label)
check_device_name._signal_device_check.connect(check_device)

check_device_name.start()

# time.sleep(2)
# check_device_name.pause.lock()
# time.sleep(2)
# check_device_name.pause.unlock()
ui.M_Dialog.main_test_byone_pushButton.clicked.connect(begin_run)

sys.exit(app.exec_())
