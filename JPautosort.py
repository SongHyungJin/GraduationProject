
# 자동 분류 기능 #

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

form_categorize = uic.loadUiType("Autosort_window.ui")[0]

class AutosortWindow(QDialog, QWidget, form_categorize):

    def __init__(self):
        super(AutosortWindow, self).__init__()
        self.setupUi(self)
        self.show()
        data = ["Apple", "Banana", "Tomato", "Cherry"]

        parent = QTreeWidget.invisibleRootItem(self.treeWidget)
        for d in data:
            item = self.make_tree_item(d)
            parent.addChild(item)
        self.buttonDown.clicked.connect(self.move_item)
        self.buttonUP.clicked.connect(self.move_item)
        self.treeWidget.header().setVisible(False)
        self.treeWidget_2.header().setVisible(False)
        self.buttonOK.clicked.connect(self.sort)
        self.pushButton.clicked.connect(self.open_Folder)


    def initUI(self):
        self.setupUi(self)


    def make_tree_item(cls, name: str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        return item

    def move_item(self):
        sender = self.sender()
        if self.buttonDown == sender:
            source = self.treeWidget
            target = self.treeWidget_2

        else:
            source = self.treeWidget_2
            target = self.treeWidget

        item = QTreeWidget.invisibleRootItem(source).takeChild(source.currentIndex().row())
        QTreeWidget.invisibleRootItem(target).addChild(item)

    def sort(self):
        QMessageBox.about(self, "about title", "about message")

    def open_Folder(self):
        path = "C:/Users/{}/Pictures".format(os.getlogin())
        folder = QFileDialog.getExistingDirectory(self, "폴더 열기", path)
        if folder:
            self.FolderPath.setText(folder)
            self.currentFolder = folder


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AutosortWindow()
    sys.exit(app.exec_())