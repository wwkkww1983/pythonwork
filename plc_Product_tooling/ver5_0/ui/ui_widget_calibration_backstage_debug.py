# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_calibration_backstage_debug.ui'
#
# Created: Fri Jul  7 18:50:32 2017
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget_Calibration_Backstage(object):
    def setupUi(self, widget_Calibration_Backstage):
        widget_Calibration_Backstage.setObjectName("widget_Calibration_Backstage")
        widget_Calibration_Backstage.resize(818, 369)

        self.retranslateUi(widget_Calibration_Backstage)
        QtCore.QMetaObject.connectSlotsByName(widget_Calibration_Backstage)

    def retranslateUi(self, widget_Calibration_Backstage):
        _translate = QtCore.QCoreApplication.translate
        widget_Calibration_Backstage.setWindowTitle(_translate("widget_Calibration_Backstage", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_Calibration_Backstage = QtWidgets.QWidget()
    ui = Ui_widget_Calibration_Backstage()
    ui.setupUi(widget_Calibration_Backstage)
    widget_Calibration_Backstage.show()
    sys.exit(app.exec_())

