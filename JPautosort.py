
# 자동 분류 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2
from JPcheckAutosort import CheckAutosortWindow
from numpy import dot
from numpy.linalg import norm
import numpy as np

form_categorize = uic.loadUiType("Autosort_window.ui")[0]

class AutosortWindow(QDialog, QWidget, form_categorize):

    def __init__(self):
        super(AutosortWindow, self).__init__()
        self.setupUi(self)

        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.buttonCancel.clicked.connect(self.main)
        self.buttonOK.clicked.connect(self.check)

    def main(self):
        self.close()

    def check(self):
        self.hide()
        self.subwin = CheckAutosortWindow()
        self.subwin.exec_()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AutosortWindow()
    sys.exit(app.exec_())