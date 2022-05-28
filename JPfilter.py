
# 중복 처리 기능 #

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PIL import Image
from numpy import dot
from numpy.linalg import norm
import numpy as np

form_filter = uic.loadUiType("Second.ui")[0]

class FilterWindow(QDialog, QWidget, form_filter):

    def __init__(self):
        super(FilterWindow, self).__init__()
        # 이미지 축소율
        self.listResize = [100, 250, 500]
        self.idxResize = 0

        # 코사인 유사도 일치율
        self.listRate = [0.85, 0.90, 0.95]
        self.idxRate = 0

        self.currentFolder = ""

        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)

        # Radiobutton 기본값 설정
        self.OpResize_0.setChecked(True)
        self.OpRate_0.setChecked(True)

        # 폴더 열기
        self.BtnOpenFolder.clicked.connect(self.open_Folder)

        # 전체 선택/해제, 선택 파일 제외
        # # #self.BtnSelectAll.clicked.connect(self.)
        # # #self.BtnExclude.clicked.connect(self.)

        # 중복 처리 작업 실행
        self.BtnRun.clicked.connect(self.filter_Image)

        # 이미지 축소율 변경
        self.OpResize_0.toggled.connect(lambda:self.setOpResize(0))
        self.OpResize_1.toggled.connect(lambda:self.setOpResize(1))
        self.OpResize_2.toggled.connect(lambda:self.setOpResize(2))

        # 코사인 유사도 일치율 기준 변경
        self.OpRate_0.toggled.connect(lambda:self.setOpRate(0))
        self.OpRate_1.toggled.connect(lambda:self.setOpRate(1))
        self.OpRate_2.toggled.connect(lambda:self.setOpRate(2))

    def setOpResize(self, n):
        self.idxResize = n

    def setOpRate(self, n):
        self.idxRate = n

    # 폴더 열기
    def open_Folder(self):
        path = "C:/Users/{}/Pictures".format(os.getlogin())
        folder = QFileDialog.getExistingDirectory(self, "폴더 열기", path)
        if folder:
            self.FolderPath.setText(folder)
            self.currentFolder = folder

    # 이미지 출력
    #def show_Image(self, images):
        #self.qPixmapFileVar = QPixmap()
        #self.qPixmapFileVar.load()
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(100)
        #self.label_pic.setPixmap(self.qPixmapFileVar)
        #for image in images:
            #pixmap = QPixmap(image)
            #self.label_pic.setPixmap(pixmap)

    # 중복 이미지 격리
    def filter_Image(self):
        # 이미지 로드
        folder = self.currentFolder
        vec_imgs = self.load_File(folder)

        # 이미지 벡터들에 대해 코사인 유사도 측정 후 처리
        # loc:유사도를 측정할 다른 한 쪽의 파일의 vec_images 내 위치
        # origin:0~size-1, 여기서 pop된 값을 target으로, 처리가 끝나면 target을 인덱스로 파일 리스트에서 일괄 이동
        # 격리 시 vec_images에서 제거, loc은 유지(loc이 가리키던 파일은 이미 중복으로 판단되었고 다시 판별할 필요 X)
        origin = []
        targets = []
        cnt = 0 # 큰 루프 돈 횟수
        for i in range(0, len(vec_imgs)):
            origin.append(i)
        for vec_img in vec_imgs:
            loc = cnt+1
            if(loc >= len(vec_imgs)):
                break
            while(loc < len(vec_imgs)):
                similarity = self.get_Cos_Sim(vec_img, vec_imgs[loc])
                if(similarity > self.listRate[self.idxRate]):
                    targets.append(origin.pop(loc))
                    del vec_imgs[loc]
                else:
                    loc = loc+1
            cnt = cnt+1

        # 파일 한 번에 이동
        self.relocate_Image(folder, targets)
        # 격리된 이미지 show OR 완료 메시지
        self.fin_filter()

    # 파일 로드 & 전처리
    def load_File(self, folder):
        filenames = os.listdir(folder)
        new_size = self.listResize[self.idxResize]  # 이미지 리사이징 옵션
        vec_imgs = []                               # 이미지 로딩 & 전처리 후 리턴할 결과물
        
        for filename in filenames:  # 아래 확장자에 해당하는 파일만 열기-PIL로 바꾸고 변동 가능성**
            if filename.endswith(".bmp") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):# or filename.endswith(".webp"):
                with open(folder + '/' + filename, "rb") as file:
                    img = Image.open(file)                  # 이미지 파일 열기
                    img = img.convert("RGB")
                    img = img.resize((new_size, new_size))  # 이미지 사이즈 조정
                    vec_img = self.vector_Image(img)        # 이미지 벡터화
                    vec_img = vec_img.astype("float") / 256
                    vec_imgs.append(vec_img)
        return vec_imgs

    # 이미지 벡터화
    def vector_Image(self, img):
        vec = np.asarray(img)   # 배열 형태로 전환
        vec = vec.ravel()       # 3차원 -> 1차원 배열로 변환
        return vec

    # 코사인 유사도 측정
    def get_Cos_Sim(self, vec1, vec2):
        return dot(vec1, vec2)/(norm(vec1)*norm(vec2))

    # 파일 이동
    def relocate_Image(self, folder, targets):
        img_src = folder
        img_dest = folder+'/중복'
        if not os.path.exists(img_dest):
            os.makedirs(img_dest)
        img_list = []
        files = os.listdir(img_src)
        for file in files:
            if file.endswith(".bmp") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                img_list.append(file)
        for target in targets:
            os.replace(img_src+'/'+img_list[target], img_dest+'/'+img_list[target])
            self.label_4.setText(img_dest+'/'+img_list[target])

    # 완료 알림
    def fin_filter(self):
        QMessageBox.about(self, '알림', '작업 완료')