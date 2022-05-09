
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

    # 이미지 축소율
    listResize = [100, 250, 500]
    idxResize = 0

    # 코사인 유사도 일치율
    listRate = [0.85, 0.90, 0.95]
    idxRate = 0

    currentFolder = ""

    def __init__(self):
        super(FilterWindow, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)

        # 폴더 열기
        self.BtnOpenFolder.clicked.connect(self.open_Folder)

        # 전체 선택/해제, 선택 파일 제외
        # # #self.BtnSelectAll.clicked.connect(self.)
        # # #self.BtnExclude.clicked.connect(self.)

        # 메인화면으로 돌아가기
        self.BtnMain.clicked.connect(self.R2Main)

        # 확인/취소
        #self.buttonBox.clicked.connect(self.)

        # 이미지 축소율 변경
        self.OpResize_0.toggled.connect(self.setOpResize(self, 0))
        self.OpResize_1.toggled.connect(self.setOpResize(self, 1))
        self.OpResize_2.toggled.connect(self.setOpResize(self, 2))

        # 코사인 유사도 일치율 기준 변경
        self.OpRate_0.toggled.connect(self.setOpRate(self, 0))
        self.OpRate_1.toggled.connect(self.setOpRate(self, 1))
        self.OpRate_2.toggled.connect(self.setOpRate(self, 2))


    def R2Main(self):
        self.close()

    def setOpResize(self, n):
        self.idxResize = n

    def setOpRate(self, n):
        self.idxRate = n

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
            notYETREALNAME_IMAGES = self.load_Image(folder)###############################################################

    # 이미지 로드
    def load_Image(self, folder):
        files = os.listdir(folder)
        images = []
        for file in files:
            if file.endswith(".bmp") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".webp"):
                images.append(file)
        return images

    # 중복 이미지 격리
    #def filter_Image(self, vec_images, folder):
        #for vec_image in vec_images:
            # O(n^2)으로 get_cos_sim
            # 일정 수치(UI에서 RadioBtn으로 고른 수치) 이상일 경우 격리
            # 경로 하위 새 폴더, 파일 이동, 리스트에서 pop

    # 이미지 벡터화
    def vec_Image(self, images):
        for image in images:
            image.flatten()
        return images

    # 이미지 리사이징
    def resize_Image(self, images):
        new_size = self.listResize[self.idxResize]
        new_images = []
        for image in images:
            new_image = cv2.resize(image, (new_size, new_size)) # <- 100, 100 대신 옵션으로 그 때 그 때 지정 가능하게
            new_images.append(new_image)
        return new_images

    # 코사인 유사도 측정
    def get_Cos_Sim(self, vec1, vec2):
        return dot(vec1, vec2)/(norm(a)*norm(b))

    # 이미지 출력 전 해당 이미지들 BGR->RGB 변환
    #def show_Redundancy(self, image):
        #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #......