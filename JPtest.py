# 테스트 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2

form_test = uic.loadUiType("Fourth.ui")[0]

class TestWindow(QDialog, QWidget, form_test):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def initUI(self):
        self.setupUi(self)

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = TestWindow()
        win.show()
        app.exec_()