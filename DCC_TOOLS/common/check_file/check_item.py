# -*- coding: utf-8 -*-

import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds

def resource_inpath():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))
    return ""

class CheckItemClass(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CheckItemClass, self).__init__(parent)
        self.fix = 0
        self.error_list = []
        self.setStyleSheet("color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.gridLayout_item = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_item.setSpacing(2)
        self.gridLayout_item.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setChecked(1)
        self.checkBox.setMinimumSize(0, 29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.gridLayout_item.addWidget(self.checkBox, 0, 0, 1, 1)
        # self.pushButton_fix = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_fix = QtWidgets.QToolButton(self.groupBox)
        self.pushButton_fix.setAutoRaise(True)
        self.pushButton_fix.setIconSize(QtCore.QSize(23, 23))
        self.pushButton_fix.setFixedSize(23, 23)
        self.pushButton_fix.setIcon(QtGui.QIcon(os.path.join(resource_inpath(),"icon_fix.svg")))
        self.pushButton_fix.setHidden(1)
        self.gridLayout_item.addWidget(self.pushButton_fix, 0, 1, 1, 1)
        # self.pushButton_select = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_select = QtWidgets.QToolButton(self.groupBox)
        self.pushButton_select.setAutoRaise(True)
        self.pushButton_select.setIconSize(QtCore.QSize(23, 23))
        self.pushButton_select.setFixedSize(23, 23)
        self.pushButton_select.setIcon(QtGui.QIcon(os.path.join(resource_inpath(),"icon_select.svg")))
        self.pushButton_select.clicked.connect(self.select_error)
        self.pushButton_select.setHidden(1)
        self.gridLayout_item.addWidget(self.pushButton_select, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

    def select_error(self):
        try:
            cmds.select(self.error_list, r=1)
        except:
            return