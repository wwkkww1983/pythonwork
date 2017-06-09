# -*- coding: utf-8 -*-

# 一些网上的UI教学
# 图标下载 http://www.easyicon.net/505471-tool_icon.html
# 窗体嵌套：http://blog.csdn.net/a359680405/article/details/45172155
# 设置背景图片等 http://www.cnblogs.com/dcb3688/p/4237204.html
# 窗体风格https://jingyan.baidu.com/article/ac6a9a5e7a79312b653eacc0.html
# 样式表：http://blog.csdn.net/yansmile1/article/details/52882965
# 关于串口的调试 https://my.oschina.net/u/2306127/blog/616002
# qss属性大全 http://www.cnblogs.com/laihuayan/archive/2012/07/27/2611111.html


from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt
import configparser
from calc import modules
from ui import ui_window_process, ui_widget_setting, ui_widget_calibration_backstage,\
    ui_widget_result, ui_widget_calibration, ui_widget_download

# 获取模块列表用于显示UI文本
config = configparser.ConfigParser()
config.read('calc\config.ini', encoding='utf-8')
MODULELIST = config['total']['MODULELIST'].split(',')


class Setting(QWidget, ui_widget_setting.Ui_widget_Setting):
    # 定义和构造左侧窗口- 模块选择和串口设置
    def __init__(self):
        super(Setting, self).__init__()
        self.setupUi(self)



        # 初始化各下拉列表默认值 后期改为记忆上一次程序退出时设置的值
        self.ports_setting = ()

        self.comboBox_PortA_Id.setCurrentIndex(0)
        self.comboBox_PortA_Paudrate.setCurrentIndex(4)
        self.comboBox_PortB_Id.setCurrentIndex(1)
        self.comboBox_PortB_Paudrate.setCurrentIndex(4)
        self.comboBox_PortC_Id.setCurrentIndex(2)
        self.comboBox_PortC_Paudrate.setCurrentIndex(4)

    def open_port(self):
        porta_id = self.comboBox_PortA_Id.currentText()
        porta_paudrate = self.comboBox_PortA_Paudrate.currentText()
        portb_id = self.comboBox_PortB_Id.currentText()
        portb_paudrate = self.comboBox_PortB_Paudrate.currentText()
        portc_id = self.comboBox_PortC_Id.currentText()
        portc_paudrate = self.comboBox_PortC_Paudrate.currentText()

        self.ports_setting = ((porta_id, porta_paudrate), (portb_id, portb_paudrate),
                              (portc_id, portc_paudrate))


class Calibration(QWidget, ui_widget_calibration.Ui_widget_Calibration):
    """定义和构造校准主窗口类对象 - 根据选择模块配置相关的显示内容，提供缺省值"""
    def __init__(self):
        super(Calibration, self).__init__()
        self.setupUi(self)


class CalibrationBackstage(QWidget, ui_widget_calibration_backstage.Ui_widget_Calibration_Backstage):
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
    """程序主窗口 - 包含5个子窗口，其中右侧中间窗口切换为校准、后台、下载三种界面"""

    def __init__(self):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)

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
        self.stackedWidget_2.setCurrentIndex(2)
        self.comboBox_Select_page.currentIndexChanged.connect(self.changepage)

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
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        # 设置背景
        palette = QtGui.QPalette()
        picture = QtGui.QPixmap('../ver2_0/source/background_1920_1200px.jpg')
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(picture))
        self.setPalette(palette)

        # 设置默认模块
        self.module_selected = ''
        self.comboBox_Select_Module.setCurrentIndex(0)


    def changepage(self):
        self.stackedWidget_2.setCurrentIndex(self.comboBox_Select_page.currentIndex()+2)

    def select_module(self):
        self.module_selected = self.comboBox_Select_Module.currentText()

    def show_setting(self):
        self.label.setText(str(self.module_selected) +
                           str(self.child_left.ports_setting))

    def module_confirm(self):
        pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ProcessWindow()
    win.show()
    sys.exit(app.exec_())
