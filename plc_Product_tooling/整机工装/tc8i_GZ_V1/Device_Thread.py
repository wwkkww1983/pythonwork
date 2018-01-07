

from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QMutex

from usbhid_handle import MYUSBHID as myhid
import  pywinusb.hid as hid


class Dev_Thread(QtCore.QThread):
    _signal_device_check=pyqtSignal(list)
    def __init__(self,parent=None):
        super(Dev_Thread,self).__init__(parent)

    pause=QMutex()

    def run(self):
        # i=0
        while True:
           # print("123")
           # sleep(1)
           # self.pause.lock()
           #
           # self.pause.unlock()
            PLC_connect_state = self.check_connect_hid_device('PLC USB HID VER1')
            digtal_connect_state = self.check_connect_hid_device('DIGITAL MODULE VER1')
            analog_connect_state = self.check_connect_hid_device('ANALOG MODULE VER1')
            self._signal_device_check.emit([PLC_connect_state,digtal_connect_state,analog_connect_state])
            sleep(1)

    # def device_find(self):
    #     usb_hid_device_name = []
    #     _filter = hid.HidDeviceFilter()
    #     hid_device = _filter.get_devices()
    #     for i in hid_device:
    #         usb_hid_device_name += [i.product_name]
    #     print(usb_hid_device_name)
    #     return usb_hid_device_name


    def check_name(self):  # # # # # 返回pc机所有hid设备名
        usb_hid_device_name = []
        _filter = hid.HidDeviceFilter()
        hid_device = _filter.get_devices()
        for i in hid_device:
            usb_hid_device_name += [i.product_name]
        return usb_hid_device_name

    def check_connect_hid_device(self,name):

        usb_hid_device_name = self.check_name()
        device_num = len(usb_hid_device_name)

        for i in range(device_num):
            if name == usb_hid_device_name[i]:
                return True

        return False


