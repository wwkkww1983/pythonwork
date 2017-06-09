# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import binascii
import ctypes
import struct
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit


class DriverDataShow(QWidget):
    """
    数字板串口数据读取显示
    """
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)  # 网格布局

        # 需显示的标签，linedit坐标
        positons = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)
            ]

        hex_str = '32 30 30 46 31 39 30 46 37 34 30 43 37 37 30 43 ' \
                  '32 45 30 31 33 38 30 31 34 43 30 41 34 34 30 41 ' \
                  '32 41 30 38 41 41 30 36 41 41 30 37 41 41 30 36 ' \
                  '34 33 30 32 41 39 30 36 37 34 30 36 41 37 30 36 ' \
                  '33 41 35 44 35 43 30 30 33 43 33 43 45 38 46 46 ' \
                  '36 45 43 35 41 30 46 46 34 42 31 33 31 43 30 30 ' \
                  '30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 ' \
                  '30 30 30 30 38 32 36 32 30 31 30 30 30 30 30 30'
        hex_bytes = hex_str.replace(' ', '').encode('ascii')  # 转为16进制字符串
        bytes_list = []
        data_list = []
        for i in range(len(hex_bytes)):
            if i % 8 == 0:
                data_hex = binascii.a2b_hex(hex_bytes[i:i+8])
                data = ((int(data_hex, 16) & 0xff) << 8) + (int(data_hex, 16) >> 8)
                data_c = ctypes.c_int16(data).value  # ctype 有符号整数
                data_list.append(data_c)

        print(bytes_list,data_list)
        #  所有参数转为有符号10进制数显示


        for name, position in zip(range(64), positons):
            if name % 2 == 0:
                label = QLabel(str(name//2))
                grid.addWidget(label, *position)
            else:
                text = 'data'+str(name//2)
                linedit = QLineEdit(str(data_list[name // 2]))  # 转为字符串类型并显示
                linedit.setObjectName(text)
                linedit.set(True)
                grid.addWidget(linedit, *position)

        self.move(300, 150)
        self.setWindowTitle('show data')
        self.show()


    def show_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DriverDataShow()
    sys.exit(app.exec_())
