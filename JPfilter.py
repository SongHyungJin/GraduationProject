
# 중복 처리 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2
from numpy import dot
from numpy.linalg import norm
import numpy as np

form_filter = uic.loadUiType("Second.ui")[0]


##################

# 딴것도 다 클래스에 QDialog 추가해야됨 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

##################
class FilterWindow(QDialog, QWidget, form_filter):

    OpResize = [100, 250, 500]
    IndexResize = 0
    OpRate = [0.85, 0.90, 0.95]
    IndexRate = 0

    def __init__(self):
        super(FilterWindow, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.BtnOpenFolder.clicked.connect(self.open_Folder)
        #self.BtnSelectAll.clicked.connect(self.)
        #self.BtnExclude.clicked.connect(self.)
        self.BtnMain.clicked.connect(self.R2Main)
        #self.buttonBox.clicked.connect(self.)
        #self.OpResize_0.toggled.connect(self.)
        #self.OpResize_1.toggled.connect(self.)
        #self.OpResize_2.toggled.connect(self.)
        #self.OpRate_0.toggled.connect(self.)
        #self.OpRate_1.toggled.connect(self.)
        #self.OpRate_2.toggled.connect(self.)

    # 프로그램 메인 화면으로 돌아가기
    def R2Main(self):
        self.close()

    #def optionResizing(self):
        #........


    #######################################
    ########################
    ############

    # path : 사용자 사진 폴더, 근데 윈11 가고 나서부턴 원드라이브가 분탕쳐서 생각대로 안 됨
    # getExistingDirectory도 비슷한 모양일 듯 참고 : newbie-developer.tistory.com/122
    # 폴더 선택 안 했을 때 처리용으로 if문 넣는 듯 함. 잘 몰?루

    ######################################
    def open_Folder(self):
        path = "C:/Users/{}/Pictures".format(os.getlogin())
        folder = QFileDialog.getExistingDirectory(self, "폴더 열기", path)
        if folder:
            self.FolderPath.setText(folder)
        return folder

    # 이미지 로드
    # jpeg, bmp 추가해야함
    def load_Image(folder):
        files = os.listdir(folder)
        images = []
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".webp"):
                images.append(file)
        return images

    # 이미지 벡터화
    def vec_Image(images):
        for image in images:
            image.flatten()
        return images

    # 이미지 리사이징
    def resize_Image(images, optionHowMuch):
        new_images = []
        for image in images:
            new_image = cv2.resize(image, (100, 100)) # <- 100, 100 대신 옵션으로 그 때 그 때 지정 가능하게
            new_images.append(new_image)
        return new_images

    # 코사인 유사도 측정
    def get_Cos_Sim(vec1, vec2):
        return dot(vec1, vec2)/(norm(a)*norm(b))

    # 이미지 출력 전 해당 이미지들 BGR->RGB 변환
    #def show_Redundancy(image):
        #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #......

    # 중복 이미지 격리
    #def filter_Image(vec_images, folder):
        #for vec_image in vec_images:
            # O(n^2)으로 get_cos_sim
            # 일정 수치(UI에서 RadioBtn으로 고른 수치) 이상일 경우 격리
            # 경로 하위 새 폴더, 파일 이동, 리스트에서 pop