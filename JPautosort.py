
# 자동 분류 기능 #

import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from predict_module import do_predict
from cutNresize import cutNresize
import shutil
import cv2
from numpy import dot
from numpy.linalg import norm
import numpy as np

form_categorize = uic.loadUiType("Autosort_window.ui")[0]

class AutosortWindow(QDialog, QWidget, form_categorize):

    def __init__(self):
        super(AutosortWindow, self).__init__()
        self.setupUi(self)
        self.show()

        self.folder_source = ""         # 이미지 있는 폴더
        self.folder_destination = ""    # 이미지 옮길 폴더

        modelName_list = []
        for dirpath, dirname, filenames in os.walk('model'):
            for file in filenames:
                if file.endswith('.txt'):
                    modelName_list.append(Path(file).stem)

        parent = QTreeWidget.invisibleRootItem(self.treeWidget)
        parent2 = QTreeWidget.invisibleRootItem(self.treeWidget_2)
        self.item_base = QTreeWidgetItem()
        self.item_userList = QTreeWidgetItem()
        parent.addChild(self.item_base)
        parent2.addChild(self.item_userList)
        self.item_base.setText(0, '분류 가능 캐릭터 목록')
        self.item_userList.setText(0, '분류 우선순위')
        for d in modelName_list:
            item = self.make_tree_item(d)
            self.item_base.addChild(item)
            self.item_base.sortChildren(0, Qt.SortOrder(0))
        self.buttonDown.clicked.connect(self.move_item)
        self.buttonUP.clicked.connect(self.move_item)
        self.treeWidget.header().setVisible(False)
        self.treeWidget_2.header().setVisible(False)
        self.buttonOK.clicked.connect(self.sort)

        self.BtnFolderSrc.clicked.connect(self.open_Folder)     # 폴더 열기
        self.BtnFolderDest.clicked.connect(self.set_Folder)     # 결과 폴더 지정


    def initUI(self):
        self.setupUi(self)


    def make_tree_item(cls, name: str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        return item

    def move_item(self):
        sender = self.sender()
        if self.buttonDown == sender:
            item = QTreeWidget.currentItem(self.treeWidget)
            self.item_base.removeChild(item)
            self.item_userList.addChild(item)

        else:
            item = QTreeWidget.currentItem(self.treeWidget_2)
            self.item_userList.removeChild(item)
            self.item_base.addChild(item)
            self.item_base.sortChildren(0, Qt.SortOrder(0))


    def sort(self):
        priority = []
        for i in range(0, self.item_userList.childCount()):
            priority.append(self.item_userList.child(i).text(0))

        if len(priority) == 0:
            QMessageBox.about(self, "error", "분류 대상 목록이 비어있습니다.")
        else:
            tmpCropDir = self.folder_destination + '/' + 'tmpCrop'
            img_path = self.folder_source
            crop_list = cutNresize(img_path, tmpCropDir)
            modelDir_list = []
            for k in range(0, len(priority)):
                for dirpath, dirname, filename in os.walk('model'):
                    if priority[k] + ".txt" in filename:
                        modelDir_list.append(dirpath)

            for k in range(0, len(modelDir_list)):
                result = do_predict(modelDir_list[k], crop_list)
                result = set(result)
                result = list(result)
                path = self.folder_destination + '\\' + priority[k]
                if not os.path.exists(path):
                    os.mkdir(path)
                for i in range(0, len(result)):
                    if os.path.isfile(result[i]):
                        shutil.move(result[i], path)
                QMessageBox.about(self, '중간 확인', str(priority[k]) + '의 분류가 완료되었습니다. 분류된 이미지를 확인하십시오.')

            QMessageBox.about(self, '분류 완료', '분류가 전부 완료되었습니다.')

            for file in os.scandir(tmpCropDir):
                os.remove(file.path)
            os.rmdir(tmpCropDir)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AutosortWindow()
    sys.exit(app.exec_())
