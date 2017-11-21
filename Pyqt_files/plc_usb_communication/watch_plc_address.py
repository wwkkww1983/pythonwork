#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     watch_plc_address
# Description :
#   Author:      fan
#   date:        2017/11/20
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------



import sys, time
import usbhid
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import  QPushButton, QDialog, QApplication, QLabel, QLineEdit, QGridLayout




class HidThread(QThread):

    finished_signal = pyqtSignal(int)

    def __init__(self, hidname, startadd, parent=None):
        super().__init__(parent)
        self.hidname = hidname
        self.startadd = startadd
        self.hid = usbhid.MYUSBHID(self.hidname, self.startadd)
        self.hid.start()
        time.sleep(.1)
        self.hid.setcallback()
        print("write buffer: data={}".format(self.hid.writebuffer))


    def get_id(self, id):
        # 修改D寄存器号时执行1次
        if True:
        # if id == self.startadd:
        #     pass
        # else:
            self.hid.startadd = id
            self.hid.updatewritebuffer()

    def run(self):
        # 执行HID读写任务
        if True:
            while True:
                try:
                    result = self.hid.write(self.hid.writebuffer)
                    # print('send result={}'.format(result))
                    time.sleep(0.05)  # 这里必须等待 使hid数据充分被读到
                    if not result:
                        print('hid write error')
                    else:
                        data = self.hid.unpack_read_data(self.hid.readbuffer)
                        self.finished_signal.emit(data[0])
                        print('digit current data ={}'.format(data))
                except Exception as e:
                    print('USB hid Error:', e)
                    break


class DataDialog(QDialog):
    id_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        hid_name = 'PLC USB HID VER1'
        startaddr = 0
        self.hidthread = HidThread(hid_name, startaddr)
        self.hidthread.finished_signal.connect(self._renew)
        self.hidthread.start()


        self.resize(400, 200)

        self.did_linedit = QLineEdit(self)
        self.did_linedit.setText('D0')
        self.did_linedit.setGeometry(10, 10, 80, 20)

        self.confirm_button = QPushButton(self)
        self.confirm_button.setText('确定')
        self.confirm_button.setGeometry(10, 40, 80, 20)

        self.value_lindedit = QLineEdit(self)
        self.value_lindedit.setText('')
        self.value_lindedit.setGeometry(10, 70, 80, 20)
        # self.value_lindedit.setDisabled(False)

        layout = QGridLayout(self)

        layout.addWidget(self.did_linedit, 1, 0)
        layout.addWidget(self.confirm_button, 1, 1)
        layout.addWidget(self.value_lindedit, 0, 0)

        self.setLayout(layout)


    def _renew(self, message):
        self.value_lindedit.setText(str(message))



    def _click_to_do_something(self):
        print('按钮按下')
        self.hidthread.get_id(int(self.did_linedit.text()[1:]))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DataDialog()
    dialog.show()

    dialog.confirm_button.clicked.connect(dialog._click_to_do_something)
    sys.exit(app.exec())

