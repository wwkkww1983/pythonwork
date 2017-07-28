# -*- coding: utf-8 -*-

import logging as log
from time import sleep
from ctypes import windll
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QMainWindow, QGridLayout, QLineEdit, QLabel)
import board
import calibrate
from usb_hid import MYUSBHID as myhid
from ui import ui_window_process, ui_widget_calibration_backstage_debug,\
    ui_widget_result, ui_widget_calibration, ui_widget_download, ui_widget_setting_usb

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

# 获取模块列表 - > UI模块列表
MODULELIST = board.get_board_list()
log.info('MODULIST = {}'.format(MODULELIST))


class HidThreads(QThread):
    hidreadSignal = pyqtSignal(list)

    def __init__(self, _hid, parent=None):
        super(HidThreads, self).__init__(parent)
        self.hid1 = _hid
        self.flag = False

    def run(self):
        self.hid1.setcallback()
        hid = self.hid1
        write_buffer = hid.writebuffer
        log.info('write buffer: lenth={},data={}'.format(len(write_buffer), write_buffer))
        while True:
            try:
                result = hid.write(write_buffer)
                log.info('send result={}'.format(result))
                sleep(.1)  # 这里必须等待 使hid数据充分被读到
                if not result:
                    log.info('hid write error')
                else:
                    digit_current_data = hid.unpack_read_data(hid.readbuffer)
                    self.hidreadSignal.emit(digit_current_data)
                    log.info('digit current data ={}'.format(digit_current_data))
            except Exception as e:
                log.error('USB hid Error:', e)


class Setting(QWidget, ui_widget_setting_usb.Ui_widget_Setting):
    # 定义和构造左侧窗口- 模块选择和串口设置
    def __init__(self):
        super(Setting, self).__init__()
        self.setupUi(self)
        # 初始化各下拉列表默认值 后期改为记忆上一次程序退出时设置的值
        self.ports_setting = ()


class Calibration(QWidget, ui_widget_calibration.Ui_widget_Calibration):
    """定义和构造校准主窗口类对象 - 根据选择模块配置相关的显示内容，提供缺省值"""
    def __init__(self):
        super(Calibration, self).__init__()
        self.setupUi(self)


class CalibrationBackstage(QWidget, ui_widget_calibration_backstage_debug.Ui_widget_Calibration_Backstage):
    """定义和构造校准后台后台窗口类对象 - 根据选择模块配置相关的显示内容，提供缺省值"""
    def __init__(self):
        super(CalibrationBackstage, self).__init__()
        self.setupUi(self)


class Download(QWidget, ui_widget_download.Ui_widget_Download):
    """定义下载窗口"""
    def __init__(self):
        super(Download, self).__init__()
        self.setupUi(self)


class Result(QWidget, ui_widget_result.Ui_widget_Result_Show):
    """定义和构造右侧底部窗口- 显示校准结果和控制按钮"""

    def __init__(self):
        super(Result, self).__init__()
        self.setupUi(self)

        palette = QtGui.QPalette()
        color = QtGui.QColor(197, 215, 187)
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

        self.setDisabled(True)


class ProcessWindow(QMainWindow, ui_window_process.Ui_MainWindow):
    """程序主窗口"""
    def __init__(self):
        super(ProcessWindow, self).__init__()
        # 构造主窗口
        self.setupUi(self)
        self.digit_hid = myhid('DIGITAL MODULE VER1')
        self.digit_hid.start()
        self.thread = HidThreads(self.digit_hid)

        self.board = None

        # 窗口导入
        self.setting = Setting()
        self.downloadpage = Download()
        self.calibrationpage = Calibration()
        self.calibrationbackstagepage = CalibrationBackstage()
        self.result = Result()

        # 设置、结果界面设置
        self.stackedWidget.addWidget(self.setting)  # page index 2
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget_3.addWidget(self.result)  # page index 2
        self.stackedWidget_3.setCurrentIndex(2)

        # 主界面设置
        self.stackedWidget_2.addWidget(self.downloadpage)   # page index 2
        self.stackedWidget_2.addWidget(self.calibrationpage)  # page index 3
        self.stackedWidget_2.addWidget(self.calibrationbackstagepage)  # page index 4
        self.comboBox_Select_page.currentIndexChanged.connect(self.change_page)

        # 移除窗口标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 移除最小化，最大化按钮，保留关闭按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 设置窗口样式（按部件分类设置），应用样式表
        self.style = """
                        # QPushButton{background-color:rgb(230, 231, 220);color:rgb(51, 51, 51)}
                        # QComboBox{background-color:rgb(145, 191, 36);color:#005050;}
                        # QLabel{background-color:rgb(136, 136, 136);color:rgb(51, 51, 51)}
                        # QGroupBox{background-color:rgb(145, 191, 36)}
                     """
        self.setStyleSheet(self.style)

        # 设置窗口标题、标题图标
        self.setWindowTitle(u'LX模拟量模块出厂检测程序')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ver2_0/source/window_24px.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # 设置任务栏图标
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        # 设置背景
        palette = QtGui.QPalette()
        picture = QtGui.QPixmap('../ver2_0/source/background_1920_1200px.jpg')
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(picture))
        self.setPalette(palette)

        # 初始化模块列表，提供默认模块
        self.board = ''
        for types in ['']+MODULELIST:
            self.comboBox_Select_Board.addItem(types)
        self.comboBox_Select_Board.setCurrentIndex(0)
        self.comboBox_Select_page.setCurrentIndex(3)

        self.digit_data = [0] * 32


        self.backstage_config()
        self.setting.pushButton_Link_Digit_Board.clicked.connect(self.hid_link)

    def hid_link(self):
        """
        获取系统当前usb hid设备中符合条件的对象
        :return:
        """
        button = self.setting.pushButton_Link_Digit_Board
        if button.text() == '连接数字板':
            self.thread.hidreadSignal.connect(self.backstage_renew)
            self.thread.start()
            button.setText('取消连接数字板')
        elif button.text() == '取消连接数字板':
            self.thread.terminate()
            self.thread.wait()
            button.setText('连接数字板')
        else:
            pass



    # def get_hid_buffer(self, _hid):
    #     """
    #     监视hid 数据，放到线程中全程进行hid通讯，直到结束本次工装使用或手动断开
    #     :return:
    #     """
    #     if (self.digit_hid.alive or self.anolog_hid.alive) is not True:
    #         log.info('工装板 {} USB连接不正确，请检查'.format(self.digit_hid.name+'\\'+self.anolog_hid.name))
    #     else:
    #         pass
    #
    # def getdata(self, data):
    #     pass

    def backstage_config(self):
        sleep(.1)
        grid = QGridLayout()
        pos = []
        data = self.digit_data
        self.linedit_group = []
        if len(data) == 32:
            for i in range(4):
                for j in range(8):
                    pos.append((i, j))
            for k,i in zip(data,range(32)):
                linedit = QLineEdit('linedit_'+str(k))
                linedit.setText(str(k))
                grid.addWidget(linedit, *pos[i])
                self.linedit_group.append(linedit)
        self.calibrationbackstagepage.setLayout(grid)

    def backstage_renew(self, data):
        for i, j in zip(data, self.linedit_group):
            j.setText(str(i))

    def change_page(self):
        self.stackedWidget_2.setCurrentIndex(self.comboBox_Select_page.currentIndex()+2)

    def select_module(self):
        self.board = self.comboBox_Select_Board.currentText()

    def show_setting(self):
        self.label.setText(str(self.board) + str(self.child_left.ports_setting))

    def module_confirm(self):
        pass


def cali_8tc():
    pass

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ProcessWindow()
    win.show()
    sys.exit(app.exec_())
