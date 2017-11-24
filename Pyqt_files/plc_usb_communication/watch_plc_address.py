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
import usbhid2 as usbhid
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QDialog, QApplication, QLabel, QLineEdit, \
    QGridLayout, QHBoxLayout


class HidThread(QThread):
    finished_signal = pyqtSignal(tuple)

    def __init__(self, hidname, parent=None):
        super().__init__(parent)
        self.hidname = hidname
        self.startadd = 0
        self.lengh = 1
        self.hid = usbhid.MYUSBHID()
        self.hid.findhiddevice(self.hidname)
        self.hid.start()
        time.sleep(.1)
        self.hid.setcallback()
        # print("write buffer: data={}".format(self.hid.writebuffer))

    def renewset(self, startadd, lengh):
        # 修改D寄存器号时执行1次
        if True:
            self.startadd = startadd
            self.lengh = lengh
            self.hid.updatewritebuffer(self.startadd, self.lengh)

    def run(self):
        # 执行HID读写任务
        if True:
            while True:
                try:
                    self.hid.readbuffer = []
                    result = self.hid.write(self.hid.writebuffer)
                    # print('send result={}'.format(result))
                    time.sleep(0.05)  # 这里必须等待 使hid数据充分被读到
                    if not result:
                        print('hid write error')
                    else:
                        data = self.hid.unpack_read_data(self.hid.readbuffer)
                        self.finished_signal.emit(tuple(data))
                        # print('digit current data ={}'.format(data))
                except Exception as e:
                    print('USB hid Error:', e)
                    break


class DataDialog(QDialog):
    # id_signal = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hidthread = None
        self.hid_name = ''
        self.start_addr = 0
        self.data_lengh = 1
        self.valuelineditarray = []

        self.resize(400, 200)
        self.did_linedit = QLineEdit(self)
        self.did_linedit.setText('D0')
        # self.did_linedit.setGeometry(10, 10, 80, 20)

        self.lengh_lineedit = QLineEdit(self)
        self.lengh_lineedit.setText('1')
        # self.lengh_lineedit.setGeometry()

        self.confirm_button = QPushButton(self)
        self.confirm_button.setText('确定')
        # self.confirm_button.setGeometry(10, 40, 80, 20)

        self.value0_lindedit = QLineEdit(self)
        self.value0_lindedit.setText('')

        hbox = QHBoxLayout()
        for i in range(8):
            self.value_lindedit = QLineEdit(self)
            self.value_lindedit.setObjectName('v'+str(i))
            self.valuelineditarray.append('v'+str(i))
            hbox.addWidget(self.value_lindedit)

        grid = QGridLayout()
        grid.addWidget(self.did_linedit, 0, 0)
        grid.addWidget(self.lengh_lineedit, 0, 1)
        grid.addWidget(self.confirm_button, 1, 0)
        grid.addWidget(self.value0_lindedit, 1, 1)

        maingrid = QGridLayout(self)
        maingrid.addLayout(hbox, 0, 0)
        maingrid.addLayout(grid, 1, 0)

        self.setLayout(maingrid)
    def createhid(self, hidname, startaddr, datalengh):
        self.hidthread = HidThread(hidname)
        self.hidthread.renewset(startaddr, datalengh)
        self.hidthread.finished_signal.connect(self._renew)
        self.hidthread.start()

    def _renew(self, message):
        self.value0_lindedit.setText(str(message[0]))
        for i in range(8):
            linedit = self.findChild(QLineEdit, self.valuelineditarray[i])
            linedit.setText(str(message[i]))

    def _click_to_do_something(self):
        stt = int(self.did_linedit.text()[1:])
        ln = int(self.lengh_lineedit.text())
        self.hidthread.renewset(stt, ln)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DataDialog()
    dialog.show()
    hid_name = 'PLC USB HID VER1'
    start_addr = 0
    data_lengh = 10
    dialog.createhid(hid_name, start_addr, data_lengh)
    dialog.confirm_button.clicked.connect(dialog._click_to_do_something)
    sys.exit(app.exec())

