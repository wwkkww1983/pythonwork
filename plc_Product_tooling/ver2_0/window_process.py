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
from ui_window_process import Ui_MainWindow
from ui_widget_setting import Ui_widget_Setting
from ui_widget_calibration_backstage import Ui_widget_Calibration_Backstage
from ui_widget_result import Ui_widget_Result_Show
from ui_widget_calibration import Ui_widget_Calibration
import ini
# 导入模块配置文件


class Setting(QWidget, Ui_widget_Setting):
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

        # print(self.ports_setting)


# class Calibration(QWidget, Ui_widget_Calibration_Lx8pt):
#     """定义和构造右侧顶部窗口- 当前选择的模块校准窗口，默认8pt"""
#     def __init__(self):
#         super(Calibration, self).__init__()
#         self.setupUi(self)
#         self.setDisabled(True)
# 作为后台画面使用，每个模块对应不同的标签名、数值显示、标题等
class Calibration(QWidget, Ui_widget_Calibration):
    """定义和构造校准主窗口类对象 - 根据选择模块配置相关的显示内容，提供缺省值"""
    def __init__(self):
        super(Calibration, self).__init__()
        self.setupUi(self)
        self.setDisabled(True)


class CalibrationBackstage(QWidget, Ui_widget_Calibration_Backstage):
    """定义和构造校准后台后台窗口类对象 - 根据选择模块配置相关的显示内容，提供缺省值"""
    def __init__(self):
        super(CalibrationBackstage, self).__init__()
        self.setupUi(self)
        self.setDisabled(True)


class Result(QWidget, Ui_widget_Result_Show):
    """定义和构造右侧底部窗口- 显示校准结果和控制按钮"""

    def __init__(self):
        super(Result, self).__init__()
        self.setupUi(self)

        palette = QtGui.QPalette()
        color = QtGui.QColor(197, 215, 187)
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

        self.setDisabled(True)


class ProcessWindow(QMainWindow, Ui_MainWindow):
    """程序主窗口 - 包含左侧、右侧顶部、右侧底部三个子窗口"""

    def __init__(self):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)



        # 移除窗口标题栏
        # self.setWindowFlags(Qt.FramelessWindowHint)

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


        self.module_selected = ''
        self.comboBox_Select_Module.setCurrentIndex(0)

        # 实例化设置界面
        self.child_left = Setting()

        # 实例化校准界面 根据设置窗口的选择进行配置
        self.child_middle = Calibration()

        # 实例化结果界面
        self.child_buttom = Result()

    def select_module(self):
        self.module_selected = self.comboBox_Select_Module.currentText()

    def child_show(self):
        # 显示三个子窗口的内容
        self.gridLayout_left.addWidget(self.child_left)
        self.child_left.show()

        self.gridLayout_middle.addWidget(self.child_middle)
        self.child_middle.show()

        self.gridLayout_buttom.addWidget(self.child_buttom)
        self.child_buttom.show()

    def child_remove(self):
        self.gridLayout_middle.removeWidget(self.child_middle)

    def show_setting(self):
        self.label.setText(str(self.module_selected) +
                           str(self.child_left.ports_setting))

    def module_confirm(self):
        # 获取当前设置的型号，获取检测到的型号进行比较，确定是否正确
        set_module_type = self.comboBox_Select_Module.currentText()
        set_module_configuration = ini.config_by_module_type(set_module_type)
        self.child_middle.label_Module_Type.setText(set_module_configuration[0])
        self.child_middle.label_Object_Type.setText(set_module_configuration[1])
        self.child_middle.label_Hard_Detection_Code.setText(str(hex(set_module_configuration[6])))



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ProcessWindow()

    # 调用主窗口的show()以及通过主窗口函数child_show调用子窗口的show()
    win.show()

    def show_setting():
        # 串口操作按钮根据操作，第一次按下把当前设置信息传给主程序，并禁用设置项；
        # 第二次按下启用设置项，依次循环
        # print(win.child_left.pushButton_Open_Ports.text())
        if win.child_left.pushButton_Open_Ports.text() == u'关闭串口':
            win.groupBox_1.setEnabled(True)
            win.child_left.groupBox_2.setEnabled(True)
            win.child_left.groupBox_3.setEnabled(True)
            win.child_left.groupBox_4.setEnabled(True)
            win.child_middle.setDisabled(True)
            win.child_buttom.setDisabled(True)
            win.child_left.pushButton_Open_Ports.setText(u'打开串口')

        else:
            win.select_module()
            win.child_left.open_port()
            win.show_setting()
            win.module_confirm()

            win.groupBox_1.setDisabled(True)
            win.child_left.groupBox_2.setDisabled(True)
            win.child_left.groupBox_3.setDisabled(True)
            win.child_left.groupBox_4.setDisabled(True)
            win.child_middle.setEnabled(True)
            win.child_buttom.setEnabled(True)
            win.child_left.pushButton_Open_Ports.setText(u'关闭串口')

    def show_backstage():
        if win.pushButton_Go_Backstage.text() == u'查看详细信息':
            win.child_remove()
            win.child_middle = CalibrationBackstage()
            win.pushButton_Go_Backstage.setText(u'查看概览信息')

        else:
            win.child_remove()
            win.child_middle = Calibration()
            win.pushButton_Go_Backstage.setText(u'查看详细信息')
        win.child_show()

    win.child_left.pushButton_Open_Ports.clicked.connect(show_setting)
    win.pushButton_Go_Backstage.clicked.connect(show_backstage)
    sys.exit(app.exec_())
