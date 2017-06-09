from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from ui_window_process import Ui_MainWindow
from ui_untitled import Ui_Form
from ui_widget_setting import Ui_widget_Setting


class Setting(QWidget, Ui_widget_Setting):
    # 定义和构造左侧窗口- 模块选择和串口设置
    def __init__(self):
        super(Setting, self).__init__()
        self.setupUi(self)

        # 初始化各下拉列表默认值 后期改为记忆上一次程序退出时设置的值
        self.ports_setting = ()

class ProcessWindow(QMainWindow, Ui_Form):

    def __init__(self):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)
        self.widget = Setting()

        self.stackedWidget.addWidget(self.widget)
        self.stackedWidget.setCurrentIndex(2)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ProcessWindow()

    # 调用主窗口的show()以及通过主窗口函数child_show调用子窗口的show()
    win.show()
    sys.exit(app.exec_())