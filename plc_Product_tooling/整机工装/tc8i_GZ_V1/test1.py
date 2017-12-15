import  Widget_deal_func
from tc8i import TC8I
import Widget_deal_func
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread,pyqtSignal
import sys


app = QApplication(sys.argv)
ui_111=Widget_deal_func.Operation_func()
ui_111.warning_widget('')
sys.exit(app.exec_())