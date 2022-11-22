#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/10


__author__ = "dango wang"

import maya.OpenMayaUI as mui
try:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
except ImportError:
    import PySide.QtGui as QtWidgets
    from PySide import QtCore
    from shiboken import wrapInstance


def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class PlayBlastDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PlayBlastDialog, self).__init__(parent=getMayaWindow())

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 150)
        # Dialog.setMinimumSize(QtCore.QSize(350, 150))
        # Dialog.setMaximumSize(QtCore.QSize(350, 150))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 54, 12))
        self.label.setObjectName("label")
        self.artist_le = QtWidgets.QLineEdit(Dialog)
        self.artist_le.setGeometry(QtCore.QRect(50, 30, 101, 21))
        self.artist_le.setObjectName("artist_le")
        self.file_path_le = QtWidgets.QLineEdit(Dialog)
        self.file_path_le.setGeometry(QtCore.QRect(20, 70, 161, 21))
        self.file_path_le.setObjectName("file_path_le")
        self.input_file_path_pb = QtWidgets.QPushButton(Dialog)
        self.input_file_path_pb.setGeometry(QtCore.QRect(190, 70, 41, 21))
        self.input_file_path_pb.setObjectName("input_file_path_pb")
        self.select_file_path_pb = QtWidgets.QPushButton(Dialog)
        self.select_file_path_pb.setGeometry(QtCore.QRect(240, 70, 51, 21))
        self.select_file_path_pb.setObjectName("select_file_path_pb")
        self.playblast_doit = QtWidgets.QPushButton(Dialog)
        self.playblast_doit.setGeometry(QtCore.QRect(200, 110, 101, 30))
        self.playblast_doit.setObjectName("playblast_doit")
        self.playblast_doit.setStyleSheet('background-color: rgb(59, 149, 73);')
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 30, 31, 16))
        self.mov_name_le = QtWidgets.QLineEdit(Dialog)
        self.mov_name_le.setGeometry(QtCore.QRect(200, 30, 75, 21))
        self.mov_name_le.setObjectName("mov_name_le")
        self.input_mov_name_pb = QtWidgets.QPushButton(Dialog)
        self.input_mov_name_pb.setGeometry(QtCore.QRect(280, 30, 31, 21))
        self.input_mov_name_pb.setObjectName("input_mov_name_pb")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(320, 30, 31, 16))
        self.label_3.setText("cam:")
        self.cam_name_le = QtWidgets.QLineEdit(Dialog)
        self.cam_name_le.setGeometry(QtCore.QRect(350, 30, 75, 21))
        self.cam_name_le.setObjectName("cam_name_le")
        self.input_cam_name_pb = QtWidgets.QPushButton(Dialog)
        self.input_cam_name_pb.setGeometry(QtCore.QRect(430, 30, 31, 21))
        self.input_cam_name_pb.setObjectName("input_cam_name_pb")
        self.input_cam_name_pb.setText(u"《《")

        self.draw_hud_cb = QtWidgets.QCheckBox(Dialog)
        self.draw_hud_cb.setGeometry(QtCore.QRect(350, 70, 50, 21))
        self.draw_hud_cb.setText(u'hud')
        self.draw_hud_cb.setChecked(1)
        self.setWindowTitle(u'dsf简易拍屏工具 by wangdonghao')
        self.label.setText(u"artist：")
        self.input_file_path_pb.setText(u"《《")
        self.select_file_path_pb.setText(u"select")
        self.playblast_doit.setText(u"playblast")
        self.label_2.setText(u"mov：")
        self.input_mov_name_pb.setText(u"《《")
        QtCore.QMetaObject.connectSlotsByName(Dialog)
