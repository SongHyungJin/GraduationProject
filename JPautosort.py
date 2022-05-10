# 자동 분류 기능 #
import sys
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QCheckBox, QLabel, QLineEdit, QProgressBar
from PyQt5.QtGui import *
from PyQt5.QtCore import QBasicTimer
from PyQt5 import uic
from JPautosort import AutosortWindow
from JPfilter import FilterWindow
from JPlearning import LearningWindow
from JPtest import TestWindow

form_categorize = uic.loadUiType("Autosort_window.ui")[0]


class AutosortWindow(QAutosortWindow, QWidget, QCheckbox):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.pushButton.clicked.connect()  # 사진 폴더

        # 체크박스
        self.checkBox.stateChanged.connect(self.checkprogressbar)
        self.checkBox_2.stateChanged.connect(self.filemove)
        self.checkBox_3.stateChanged.connecet(self.filecopy)

        # 연결되는거 전체
        self.lineEdit.  # lineEdit에 선택된 폴더명 입력, 구글링해서 추가로 찾아봄
        self.pushButton.clicked.connect() # 폴더 선택 창으로 이동
        self.pushButton_2.clicked.connect(self.label_pic)
        self.pushButton_3.clicked.connect(self.label_pic)
        self.buttonOK.clicked.connect(self.buttonok)
        self.buttonCancel.clicked.connect(self.buttoncancel)

        self.listWidget = QListWidget(self)
        self.listWidget.insertItem(n, QListWidgetItem(""))  # n에는 캐릭터 수, "" 안에는 클래스로 추가 (이름 추가하는 클래스도
        # 만들어야할듯
        self.label_pic()  # 폴더 내의 사진이 표시될 곳

    def checkprogressbar(self):
        n = 500 # 선택된 사진 개수, 일단 대충 때려넣음
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(n)

        def run(self, n):
            for i in range(n):
            time.sleep(0.01)
            self.progressBar.setValue(i+1) # 진행바는 따로 레이어 만들어서 빼도 될듯?

    def filemove(self):
        print("")

    def filecopy(self):
        print("")

    def buttonok(self):
        self.hide()
        self.subwin1 = CheckCategorizing()  # 새로운 파일 추가
        self.subwin1.exec_()
        self.show()

    def buttoncancel(self):
        self.hide()
        self.subwin2 = MainWindow()
        self.subwin2.exec_()
        self.show()

    def labelpic(self):  # 사진 표시될거 만들어야함.

if __name__ == '__Autosort_window__':
    app = QApplication(sys.argv)
    win = AutosortWindow()
    sys.exit(app.exec_())