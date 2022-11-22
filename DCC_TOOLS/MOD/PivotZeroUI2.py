# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PivotZeroUI2.ui'
#
# Created: Mon Feb 18 17:42:52 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(448, 559)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_check = QtWidgets.QPushButton(Dialog)
        self.pushButton_check.setObjectName("pushButton_check")
        self.verticalLayout.addWidget(self.pushButton_check)
        self.pushButton_pivotZero = QtWidgets.QPushButton(Dialog)
        self.pushButton_pivotZero.setObjectName("pushButton_pivotZero")
        self.verticalLayout.addWidget(self.pushButton_pivotZero)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "轴心归零", None, -1))
        self.treeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("Dialog", "物体名称", None, -1))
        self.treeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("Dialog", "归零状态", None, -1))
        self.pushButton_check.setText(QtWidgets.QApplication.translate("Dialog", "检查", None, -1))
        self.pushButton_pivotZero.setText(QtWidgets.QApplication.translate("Dialog", "归零", None, -1))

