
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form_categorize = uic.loadUiType(BASE_DIR + '/' + "Check_Autosort.ui")[0]

class CheckAutosortWindow(QDialog, QWidget, form_categorize):

    def __init__(self):
        super(CheckAutosortWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CheckAutosortWindow()
    sys.exit(app.exec_())

