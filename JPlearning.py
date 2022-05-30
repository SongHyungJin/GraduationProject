# 추가 학습 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from cutNresize import cutNresize
from train import train_module

form_learning = uic.loadUiType("Third.ui")[0]

class LearningWindow(QDialog, QWidget, form_learning):
    def __init__(self):
        super().__init__()

        self.folder_source = ""         # 학습할 이미지가 위치한 폴더
        self.folder_destination = ""    # 학습 데이터 저장할 폴더
        self.chara_name = ""            # 캐릭터 이름 저장해둘 문자열
        self.learning_level = 1

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
        self.BtnRun.clicked.connect(self.start_train)
        
        # 학습 강도 슬라이드바
        self.horizontalSlider.setRange(1, 10)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.valueChanged[int].connect(self.change_slider_value)

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

    def start_train(self):
        if os.path.exists(self.folder_source) and os.path.exists(self.folder_destination) and self.chara_name != "":
            img_path = self.folder_source
            tmpCropDir = self.folder_source + '/' + 'tmpCrop'
            cutNresize(img_path, tmpCropDir)
            char_dir = tmpCropDir + '/' + '0'
            other_dir = tmpCropDir + '/' + '1'
            if not os.path.exists(char_dir):
                os.mkdir(char_dir)
            if not os.path.exists(other_dir):
                os.mkdir(other_dir)
            QMessageBox.about(self, '전처리 완료',
                              tmpCropDir + '\n에 있는 이미지를 폴더에 옮겨 담기 바랍니다.\n대상 캐릭터는 0, 대상 캐릭터 외는 1입니다. \n남는 이미지가 없도록 하십시오.')
            model_path = self.folder_destination + '/' + self.chara_name
            if not os.path.exists(model_path):
                os.mkdir(model_path)
            accuracy_rate = train_module(tmpCropDir, self.learning_level, model_path)
            f = open(model_path + '/' + self.chara_name + '.txt', 'w')
            f.close()
            QMessageBox.about(self, '학습 완료', '학습된 데이터의 학습 셋에 대한 정확도: ' + str(
                accuracy_rate) + '\n학습 데이터의 경로는\n' + model_path + '\n입니다.')
        else:
            QMessageBox.about(self, 'error', '경로와 이름 설정을 다시 한 번 확인해주세요.')

    def change_slider_value(self, value):
        self.learning_level = value
        self.LabelValueSlider.setText(str(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LearningWindow()
    win.show()
    app.exec_()
