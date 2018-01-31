# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Wed Jan 31 13:08:21 2018
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(602, 401)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(12, 20, 511, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_quit = QtWidgets.QPushButton(Dialog)
        self.pushButton_quit.setGeometry(QtCore.QRect(480, 360, 89, 23))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(32, 216, 537, 129))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_xls2db = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_xls2db.setGeometry(QtCore.QRect(16, 88, 97, 23))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        self.pushButton_xls2db.setFont(font)
        self.pushButton_xls2db.setObjectName("pushButton_xls2db")
        self.label_txt = QtWidgets.QLabel(self.groupBox_2)
        self.label_txt.setGeometry(QtCore.QRect(16, 24, 169, 16))
        self.label_txt.setObjectName("label_txt")
        self.pushButton_selecxls = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_selecxls.setGeometry(QtCore.QRect(16, 56, 97, 23))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        self.pushButton_selecxls.setFont(font)
        self.pushButton_selecxls.setObjectName("pushButton_selecxls")
        self.lineEdit_xlspath = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_xlspath.setGeometry(QtCore.QRect(120, 56, 401, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.lineEdit_xlspath.setFont(font)
        self.lineEdit_xlspath.setObjectName("lineEdit_xlspath")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(32, 88, 537, 105))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.lineEdit_dbpath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_dbpath.setGeometry(QtCore.QRect(120, 32, 401, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.lineEdit_dbpath.setFont(font)
        self.lineEdit_dbpath.setObjectName("lineEdit_dbpath")
        self.pushButton_selecdb = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_selecdb.setGeometry(QtCore.QRect(16, 33, 97, 23))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        self.pushButton_selecdb.setFont(font)
        self.pushButton_selecdb.setObjectName("pushButton_selecdb")
        self.pushButton_db2xls = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_db2xls.setGeometry(QtCore.QRect(17, 64, 97, 23))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        self.pushButton_db2xls.setFont(font)
        self.pushButton_db2xls.setObjectName("pushButton_db2xls")

        self.retranslateUi(Dialog)
        self.pushButton_quit.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "db2xls and xls2db"))
        self.pushButton_quit.setText(_translate("Dialog", "退出"))
        self.groupBox_2.setTitle(_translate("Dialog", "2. Excel表格导出为.db件或.sjf文件"))
        self.pushButton_xls2db.setText(_translate("Dialog", "导出"))
        self.label_txt.setText(_translate("Dialog", "以sheetname为数据表名字"))
        self.pushButton_selecxls.setText(_translate("Dialog", "选择Excel文件"))
        self.lineEdit_xlspath.setText(_translate("Dialog", "xls文件"))
        self.groupBox.setTitle(_translate("Dialog", "1. db文件或sjf文件导出为Excel表格"))
        self.lineEdit_dbpath.setText(_translate("Dialog", "db文件、sjf文件"))
        self.pushButton_selecdb.setText(_translate("Dialog", "选择数据库文件"))
        self.pushButton_db2xls.setText(_translate("Dialog", "导出"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

