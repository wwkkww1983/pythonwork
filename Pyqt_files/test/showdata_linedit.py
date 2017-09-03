# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QPushButton,QLabel,QGridLayout,QLineEdit


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        gridtitle = QGridLayout()
        maingrid = QGridLayout()
        maingrid.setSpacing(5)
        j = 0
        pos = []
        names = [i for i in range(32)]
        if len(names) == 32:
            for i in range(4):
                for j in range(8):
                    pos.append((i, j))
            # print(pos)
        for i in names:
            linedit = QLineEdit(str(i))
            grid.addWidget(linedit, *pos[i])
            j += 1
        title_label = QLabel('数据显示')
        gridtitle.addWidget(title_label, 0, 0)
        maingrid.addLayout(gridtitle, 0, 0)
        maingrid.addLayout(grid, 1, 0)

        self.setLayout(maingrid)

        self.setGeometry(300, 100, 500, 600)
        self.setWindowTitle('数据查看')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()