import sys
import os

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from JPautosort import AutosortWindow
from JPfilter import FilterWindow
from JPlearning import LearningWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form_main = uic.loadUiType(BASE_DIR +  '/' +"Main.ui")[0]

class MainWindow(QMainWindow, QWidget, form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.button_1)
        self.pushButton_2.clicked.connect(self.button_2)
        self.pushButton_3.clicked.connect(self.button_3)

    def button_1(self):
        self.hide()
        self.subwin1 = AutosortWindow()
        self.subwin1.exec_()
        self.show()

    def button_2(self):
        self.hide()
        self.subwin2 = FilterWindow()
        self.subwin2.exec_()
        self.show()

    def button_3(self):
        self.hide()
        self.subwin3 = LearningWindow()
        self.subwin3.exec_()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())