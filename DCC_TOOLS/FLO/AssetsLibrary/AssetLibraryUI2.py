# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AssetLibrary.ui'
#
# Created: Mon May 06 11:23:47 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_assetLibraryDialog(object):
    def setupUi(self, assetLibraryDialog):
        assetLibraryDialog.setObjectName("assetLibraryDialog")
        assetLibraryDialog.resize(751, 630)
        self.gridLayout = QtWidgets.QGridLayout(assetLibraryDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(assetLibraryDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(assetLibraryDialog)
        self.comboBox.setMinimumSize(QtCore.QSize(120, 23))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(assetLibraryDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_assetName = QtWidgets.QLineEdit(assetLibraryDialog)
        self.lineEdit_assetName.setObjectName("lineEdit_assetName")
        self.horizontalLayout.addWidget(self.lineEdit_assetName)
        self.pushButton_update = QtWidgets.QPushButton(assetLibraryDialog)
        self.pushButton_update.setMinimumSize(QtCore.QSize(45, 23))
        self.pushButton_update.setMaximumSize(QtCore.QSize(45, 16777215))
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(assetLibraryDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeWidget_outliner = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_outliner.setObjectName("treeWidget_outliner")
        self.treeWidget_assetlist = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_assetlist.setObjectName("treeWidget_assetlist")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_close = QtWidgets.QPushButton(assetLibraryDialog)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_2.addWidget(self.pushButton_close)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(assetLibraryDialog)
        QtCore.QMetaObject.connectSlotsByName(assetLibraryDialog)

    def retranslateUi(self, assetLibraryDialog):
        assetLibraryDialog.setWindowTitle(QtWidgets.QApplication.translate("assetLibraryDialog", "Asset Library V1.0beta by wanghaorun", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Project Name:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Asset Name:", None, -1))
        self.pushButton_update.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Update", None, -1))
        self.treeWidget_outliner.headerItem().setText(0, QtWidgets.QApplication.translate("assetLibraryDialog", "Outliner", None, -1))
        self.treeWidget_assetlist.headerItem().setText(0, QtWidgets.QApplication.translate("assetLibraryDialog", "Thumbnail", None, -1))
        self.treeWidget_assetlist.headerItem().setText(1, QtWidgets.QApplication.translate("assetLibraryDialog", "Name", None, -1))
        self.treeWidget_assetlist.headerItem().setText(2, QtWidgets.QApplication.translate("assetLibraryDialog", "Chinese", None, -1))
        self.treeWidget_assetlist.headerItem().setText(3, QtWidgets.QApplication.translate("assetLibraryDialog", "Ver(Pub/All)", None, -1))
        self.treeWidget_assetlist.headerItem().setText(4, QtWidgets.QApplication.translate("assetLibraryDialog", "Describe", None, -1))
        self.pushButton_close.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Close", None, -1))

