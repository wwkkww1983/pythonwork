"""this script parse the content of a xml file"""
import datetime
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import QMutex, pyqtSignal
from bsp.device.serial.serial_handle import Ser


class ComThread(QtCore.QThread):
    """ Summary of class here.
    串口检测线程
    """
    #串口检测
    signal_main_com_search = pyqtSignal(list)
    signal_main_total_time = pyqtSignal(str)

    def __init__(self, parent=None):
        #super 函数是用于调用父类的一个方法
        super(ComThread, self).__init__(parent)
        self.serial = Ser()

    #QMutex类提供的是线程之间的访问顺序化。
    #QMutex的目的是保护一个对象、数据结构或者代码段，所以同一时间只有一个线程可以访问它
    pause = QMutex()

    def run(self):
        """
        串口检测写入
        """
        #记录起始时间
        total_start_time = datetime.datetime.now()
        found_serial_port = []
        found_serial_port_new = []
        while True:
            #检查可用的串口
            #记录总时间
            total_time = datetime.datetime.now()
            found_serial_port_new = self.serial.search()
            if found_serial_port_new != found_serial_port:
                self.signal_main_com_search.emit(found_serial_port_new)
                found_serial_port = found_serial_port_new
            self.signal_main_total_time.emit(
                str(total_time - total_start_time))
            sleep(0.5)

if __name__ == '__main__':
    pass
