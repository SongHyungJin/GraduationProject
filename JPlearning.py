# 추가 학습 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2

form_learning = uic.loadUiType("Third.ui")[0]

class LearningWindow(QDialog, QWidget, form_learning):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def initUI(self):
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LearningWindow()
    win.show()
    app.exec_()