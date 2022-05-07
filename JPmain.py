import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic #, QtCore
from JPautosort import AutosortWindow
from JPfilter import FilterWindow
from JPlearning import LearningWindow
from JPtest import TestWindow

form_main = uic.loadUiType("Main.ui")[0]

class MainWindow(QMainWindow, QWidget, form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.####버튼 자동 분류####.clicked.connect(self.button_1)
        self.####버튼 중복 처리####.clicked.connect(self.button_2)
        self.####버튼 추가 학습####.clicked.connect(self.button_3)
        self.####버튼 테스트####.clicked.connect(self.button_4)

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

    def button_4(self):
        self.hide()
        self.subwin4 = TestWindow()
        self.subwin4.exec_()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())