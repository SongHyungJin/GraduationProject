# 추가 학습 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_learning = uic.loadUiType("Third.ui")[0]

class LearningWindow(QDialog, QWidget, form_learning):
    def __init__(self):
        super().__init__()

        self.folder_source = ""         # 학습할 이미지가 위치한 폴더
        self.folder_destination = ""    # 학습 데이터 저장할 폴더
        self.chara_name = ""            # 캐릭터 이름 저장해둘 문자열

        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)

        # 폴더 지정
        self.BtnOpenSrc.clicked.connect(self.open_Folder)
        self.BtnOpenDest.clicked.connect(self.set_Folder)

        # 캐릭터 이름 입력
        self.BtnNameInput.clicked.connect(self.set_Name)

        # 학습 실행
        self.BtnRun.clicked.connect(self.학습 시작)
        
        # 학습 강도 슬라이드바
        self.horizontalSlider.setRange(1, 10)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.valueChanged[int].connect(self.슬라이더바 값 변경)

    def open_Folder(self):
        path = "C:/Users/{}/Pictures".format(os.getlogin())
        folder = QFileDialog.getExistingDirectory(self, "폴더 열기", path)
        if folder:
            self.SrcPath.setText(folder)
            self.folder_source = folder

    def set_Folder(self):
        path = "C:/Users/{}/Pictures".format(os.getlogin())
        folder = QFileDialog.getExistingDirectory(self, "폴더 선택", path)
        if folder:
            self.DestPath.setText(folder)
            self.folder_destination = folder

    def set_Name(self):
        self.chara_name = self.LineNameInput.text()
        self.LabelNameInput.setText(self.chara_name)


    def 학습 시작(self):

    def 슬라이더바 값 변경(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LearningWindow()
    win.show()
    app.exec_()