#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Standard Camera Tools v1.0 
#        BY WangHaoRun
#        2017.03.22 v1.0b
#        标准摄像机:
#            Create Camera  选择一个摄像机转变为标准摄像机或重建标准摄像机
#            Link Twist     给标准摄像机添加翻转
#            Look At        给自由摄像机添加目标点位置
#            Export         导出摄像机缓存*.abc
#       
#       2017.04.24 v1.05b
#           1、添加LOOK AT面板和导入导出面板；
#           2、添加导入功能，导入路径对应导出路径自动创建；
#           3、添加LOOK AT的smart back方法，用于优化LOOK AT关键帧；
#           4、添加auto计算方式与manual计算方式
#           5、auto方式通过给定距离，计算出固定距离的目标点
#
#       2017.04.24 v1.1b
#           1、添加选择相机后自动更新名称
#
#       2018.11.01 v1.2b
#           1、添加创建立体相机
#
#       2018.11.27 v1.3b
#           1、添加拍屏功能
#
#       2018.11.29 v1.33b
#           1、添加声音功能
#
#       2018.12.18 v1.35b
#           1、添加相机抖动功能
#
#---------------------------------------------------------------


import maya.cmds as cmds
import maya.mel as mel
import pymel as pm
import os
import math
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.app.stereo.stereoCameraRig
import time

try:
    from PySide2 import QtCore, QtGui, QtWidgets, QtSql
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide import __version__
    from shiboken import wrapInstance 

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow) 

def undoable(function):
    '''A decorator that will make commands undoable in maya'''

    def decoratorCode(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        functionReturn = None
        try: 
            functionReturn = function(*args, **kwargs)
            
        except:
            print sys.exc_info()[1]

        finally:
            cmds.undoInfo(closeChunk=True)
            return functionReturn
            
    return decoratorCode

# UI START

class Ui_standardCameraForm(object):
    def setupUi(self, standardCameraForm):
        standardCameraForm.setObjectName("standardCameraForm")
        standardCameraForm.resize(441, 531)
        self.layoutWidget = QtWidgets.QWidget(standardCameraForm)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 431, 511))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_standardCamera = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_standardCamera.setMinimumSize(QtCore.QSize(421, 121))
        self.groupBox_standardCamera.setMaximumSize(QtCore.QSize(421, 121))
        self.groupBox_standardCamera.setObjectName("groupBox_standardCamera")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_standardCamera)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_createCamera = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_createCamera.sizePolicy().hasHeightForWidth())
        self.pushButton_createCamera.setSizePolicy(sizePolicy)
        self.pushButton_createCamera.setObjectName("pushButton_createCamera")
        self.horizontalLayout_3.addWidget(self.pushButton_createCamera)
        self.pushButton_toStereo = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_toStereo.sizePolicy().hasHeightForWidth())
        self.pushButton_toStereo.setSizePolicy(sizePolicy)
        self.pushButton_toStereo.setObjectName("pushButton_toStereo")
        self.horizontalLayout_3.addWidget(self.pushButton_toStereo)
        self.pushButton_linkTwist = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_linkTwist.sizePolicy().hasHeightForWidth())
        self.pushButton_linkTwist.setSizePolicy(sizePolicy)
        self.pushButton_linkTwist.setObjectName("pushButton_linkTwist")
        self.horizontalLayout_3.addWidget(self.pushButton_linkTwist)
        self.pushButton_lookAt = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_lookAt.sizePolicy().hasHeightForWidth())
        self.pushButton_lookAt.setSizePolicy(sizePolicy)
        self.pushButton_lookAt.setCheckable(True)
        self.pushButton_lookAt.setObjectName("pushButton_lookAt")
        self.horizontalLayout_3.addWidget(self.pushButton_lookAt)
        self.pushButton_playBlast = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_playBlast.sizePolicy().hasHeightForWidth())
        self.pushButton_playBlast.setSizePolicy(sizePolicy)
        self.pushButton_playBlast.setCheckable(True)
        self.pushButton_playBlast.setObjectName("pushButton_playBlast")
        self.horizontalLayout_3.addWidget(self.pushButton_playBlast)
        self.pushButton_importExport = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_importExport.sizePolicy().hasHeightForWidth())
        self.pushButton_importExport.setSizePolicy(sizePolicy)
        self.pushButton_importExport.setCheckable(True)
        self.pushButton_importExport.setObjectName("pushButton_importExport")
        self.horizontalLayout_3.addWidget(self.pushButton_importExport)

        self.sel_to_stdcam = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sel_to_stdcam.sizePolicy().hasHeightForWidth())
        self.sel_to_stdcam.setSizePolicy(sizePolicy)
        # self.sel_to_stdcam.setCheckable(True)
        self.horizontalLayout_3.addWidget(self.sel_to_stdcam)
        self.sel_to_stdcam.setText(u'Sel To \n StdCam')

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_11.addWidget(self.label_3)
        self.label_cameraName = QtWidgets.QLabel(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_cameraName.sizePolicy().hasHeightForWidth())
        self.label_cameraName.setSizePolicy(sizePolicy)
        self.label_cameraName.setText("")
        self.label_cameraName.setObjectName("label_cameraName")
        self.horizontalLayout_11.addWidget(self.label_cameraName)
        self.pushButton_update = QtWidgets.QPushButton(self.groupBox_standardCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout_11.addWidget(self.pushButton_update)
        self.gridLayout.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_standardCamera)
        self.groupBox_lookAtParameter = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_lookAtParameter.setMinimumSize(QtCore.QSize(421, 151))
        self.groupBox_lookAtParameter.setMaximumSize(QtCore.QSize(421, 151))
        self.groupBox_lookAtParameter.setObjectName("groupBox_lookAtParameter")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_lookAtParameter)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(self.groupBox_lookAtParameter)
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 16))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.radioButton_manual = QtWidgets.QRadioButton(self.widget)
        self.radioButton_manual.setChecked(True)
        self.radioButton_manual.setObjectName("radioButton_manual")
        self.horizontalLayout_7.addWidget(self.radioButton_manual)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.radioButton_auto = QtWidgets.QRadioButton(self.widget)
        self.radioButton_auto.setObjectName("radioButton_auto")
        self.horizontalLayout_6.addWidget(self.radioButton_auto)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem3)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_12.addWidget(self.label_7)
        self.doubleSpinBox_distance = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_distance.setMinimum(0.1)
        self.doubleSpinBox_distance.setMaximum(1000.0)
        self.doubleSpinBox_distance.setSingleStep(1.0)
        self.doubleSpinBox_distance.setProperty("value", 5.0)
        self.doubleSpinBox_distance.setObjectName("doubleSpinBox_distance")
        self.horizontalLayout_12.addWidget(self.doubleSpinBox_distance)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.groupBox_lookAtParameter)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setMinimumSize(QtCore.QSize(0, 16))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.radioButton_smartBake = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_smartBake.setChecked(True)
        self.radioButton_smartBake.setObjectName("radioButton_smartBake")
        self.horizontalLayout_10.addWidget(self.radioButton_smartBake)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.doubleSpinBox_tolerance = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.doubleSpinBox_tolerance.setMaximum(1.0)
        self.doubleSpinBox_tolerance.setSingleStep(0.01)
        self.doubleSpinBox_tolerance.setProperty("value", 0.05)
        self.doubleSpinBox_tolerance.setObjectName("doubleSpinBox_tolerance")
        self.horizontalLayout.addWidget(self.doubleSpinBox_tolerance)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem8)
        self.radioButton_framesPerSample = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_framesPerSample.setObjectName("radioButton_framesPerSample")
        self.horizontalLayout_9.addWidget(self.radioButton_framesPerSample)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.widget_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.pushButton_createLookAt = QtWidgets.QPushButton(self.groupBox_lookAtParameter)
        self.pushButton_createLookAt.setObjectName("pushButton_createLookAt")
        self.horizontalLayout_4.addWidget(self.pushButton_createLookAt)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_lookAtParameter)
        self.tabWidget_importExport = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget_importExport.setMinimumSize(QtCore.QSize(422, 101))
        self.tabWidget_importExport.setMaximumSize(QtCore.QSize(422, 101))
        self.tabWidget_importExport.setObjectName("tabWidget_importExport")
        self.tab_import = QtWidgets.QWidget()
        self.tab_import.setObjectName("tab_import")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_import)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_updatePath_import = QtWidgets.QPushButton(self.tab_import)
        self.pushButton_updatePath_import.setMinimumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_import.setMaximumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_import.setObjectName("pushButton_updatePath_import")
        self.horizontalLayout_8.addWidget(self.pushButton_updatePath_import)
        self.label_6 = QtWidgets.QLabel(self.tab_import)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.lineEdit_abcCacheFilePath_import = QtWidgets.QLineEdit(self.tab_import)
        self.lineEdit_abcCacheFilePath_import.setObjectName("lineEdit_abcCacheFilePath_import")
        self.horizontalLayout_8.addWidget(self.lineEdit_abcCacheFilePath_import)
        self.pushButton_abcCacheChoose_import = QtWidgets.QPushButton(self.tab_import)
        self.pushButton_abcCacheChoose_import.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_abcCacheChoose_import.setObjectName("pushButton_abcCacheChoose_import")
        self.horizontalLayout_8.addWidget(self.pushButton_abcCacheChoose_import)
        self.gridLayout_7.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem11)
        self.pushButton_abcCache_import = QtWidgets.QPushButton(self.tab_import)
        self.pushButton_abcCache_import.setObjectName("pushButton_abcCache_import")
        self.horizontalLayout_14.addWidget(self.pushButton_abcCache_import)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem12)
        self.gridLayout_7.addLayout(self.horizontalLayout_14, 1, 0, 1, 1)
        self.tabWidget_importExport.addTab(self.tab_import, "")
        self.tab_export = QtWidgets.QWidget()
        self.tab_export.setObjectName("tab_export")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_export)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_updatePath_export = QtWidgets.QPushButton(self.tab_export)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_updatePath_export.sizePolicy().hasHeightForWidth())
        self.pushButton_updatePath_export.setSizePolicy(sizePolicy)
        self.pushButton_updatePath_export.setMinimumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_export.setMaximumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_export.setObjectName("pushButton_updatePath_export")
        self.horizontalLayout_2.addWidget(self.pushButton_updatePath_export)
        self.label_2 = QtWidgets.QLabel(self.tab_export)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_abcCacheFilePath_export = QtWidgets.QLineEdit(self.tab_export)
        self.lineEdit_abcCacheFilePath_export.setObjectName("lineEdit_abcCacheFilePath_export")
        self.horizontalLayout_2.addWidget(self.lineEdit_abcCacheFilePath_export)
        self.pushButton_abcCacheChoose_export = QtWidgets.QPushButton(self.tab_export)
        self.pushButton_abcCacheChoose_export.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_abcCacheChoose_export.setObjectName("pushButton_abcCacheChoose_export")
        self.horizontalLayout_2.addWidget(self.pushButton_abcCacheChoose_export)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem13)
        self.pushButton_abcCache_export = QtWidgets.QPushButton(self.tab_export)
        self.pushButton_abcCache_export.setObjectName("pushButton_abcCache_export")
        self.horizontalLayout_13.addWidget(self.pushButton_abcCache_export)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem14)
        self.gridLayout_6.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        self.tabWidget_importExport.addTab(self.tab_export, "")
        self.verticalLayout_3.addWidget(self.tabWidget_importExport)
        self.groupBox_playBlast = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_playBlast.setMinimumSize(QtCore.QSize(422, 90))
        self.groupBox_playBlast.setMaximumSize(QtCore.QSize(422, 90))
        self.groupBox_playBlast.setObjectName("groupBox_playBlast")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_playBlast)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.pushButton_updatePath_playBlast = QtWidgets.QPushButton(self.groupBox_playBlast)
        self.pushButton_updatePath_playBlast.setMinimumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_playBlast.setMaximumSize(QtCore.QSize(23, 23))
        self.pushButton_updatePath_playBlast.setObjectName("pushButton_updatePath_playBlast")
        self.horizontalLayout_15.addWidget(self.pushButton_updatePath_playBlast)
        self.label_8 = QtWidgets.QLabel(self.groupBox_playBlast)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_15.addWidget(self.label_8)
        self.lineEdit_playBlast = QtWidgets.QLineEdit(self.groupBox_playBlast)
        self.lineEdit_playBlast.setObjectName("lineEdit_playBlast")
        self.horizontalLayout_15.addWidget(self.lineEdit_playBlast)
        self.pushButton_playBlastChoose = QtWidgets.QPushButton(self.groupBox_playBlast)
        self.pushButton_playBlastChoose.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_playBlastChoose.setObjectName("pushButton_playBlastChoose")
        self.horizontalLayout_15.addWidget(self.pushButton_playBlastChoose)
        self.gridLayout_2.addLayout(self.horizontalLayout_15, 0, 0, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem15)
        self.pushButton_playBlast_go = QtWidgets.QPushButton(self.groupBox_playBlast)
        self.pushButton_playBlast_go.setObjectName("pushButton_playBlast_go")
        self.horizontalLayout_16.addWidget(self.pushButton_playBlast_go)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem16)
        self.gridLayout_2.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_playBlast)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem17)

        self.retranslateUi(standardCameraForm)
        self.tabWidget_importExport.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(standardCameraForm)

    def retranslateUi(self, standardCameraForm):
        standardCameraForm.setWindowTitle(QtWidgets.QApplication.translate("standardCameraForm", "standardCameraForm", None, -1))
        self.groupBox_standardCamera.setTitle(QtWidgets.QApplication.translate("standardCameraForm", "Standard Camera:", None, -1))
        self.pushButton_createCamera.setText(QtWidgets.QApplication.translate("standardCameraForm", "Create", None, -1))
        self.pushButton_toStereo.setText(QtWidgets.QApplication.translate("standardCameraForm", "To\n"
"Stereo", None, -1))
        self.pushButton_linkTwist.setText(QtWidgets.QApplication.translate("standardCameraForm", "Link\n"
"Twist", None, -1))
        self.pushButton_lookAt.setText(QtWidgets.QApplication.translate("standardCameraForm", "Look\n"
"At", None, -1))
        self.pushButton_playBlast.setText(QtWidgets.QApplication.translate("standardCameraForm", "Play\n"
"Blast", None, -1))
        self.pushButton_importExport.setText(QtWidgets.QApplication.translate("standardCameraForm", "Import\n"
"Export", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("standardCameraForm", "Camera Name:", None, -1))
        self.pushButton_update.setText(QtWidgets.QApplication.translate("standardCameraForm", "Update", None, -1))
        self.groupBox_lookAtParameter.setTitle(QtWidgets.QApplication.translate("standardCameraForm", "Look At Parameter:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("standardCameraForm", "Parameter:", None, -1))
        self.radioButton_manual.setText(QtWidgets.QApplication.translate("standardCameraForm", "Manual", None, -1))
        self.radioButton_auto.setText(QtWidgets.QApplication.translate("standardCameraForm", "Auto", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("standardCameraForm", "Distance: ", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("standardCameraForm", "Bake Options:", None, -1))
        self.radioButton_smartBake.setText(QtWidgets.QApplication.translate("standardCameraForm", "Smart Bake", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("standardCameraForm", "Tolerance: ", None, -1))
        self.radioButton_framesPerSample.setText(QtWidgets.QApplication.translate("standardCameraForm", "Frames per Sample", None, -1))
        self.pushButton_createLookAt.setText(QtWidgets.QApplication.translate("standardCameraForm", "Create", None, -1))
        self.pushButton_updatePath_import.setText(QtWidgets.QApplication.translate("standardCameraForm", "U", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("standardCameraForm", "Alembic Path:", None, -1))
        self.pushButton_abcCacheChoose_import.setText(QtWidgets.QApplication.translate("standardCameraForm", "...", None, -1))
        self.pushButton_abcCache_import.setText(QtWidgets.QApplication.translate("standardCameraForm", "Import", None, -1))
        self.tabWidget_importExport.setTabText(self.tabWidget_importExport.indexOf(self.tab_import), QtWidgets.QApplication.translate("standardCameraForm", "Import", None, -1))
        self.pushButton_updatePath_export.setText(QtWidgets.QApplication.translate("standardCameraForm", "U", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("standardCameraForm", "Alembic Path:", None, -1))
        self.pushButton_abcCacheChoose_export.setText(QtWidgets.QApplication.translate("standardCameraForm", "...", None, -1))
        self.pushButton_abcCache_export.setText(QtWidgets.QApplication.translate("standardCameraForm", "Export", None, -1))
        self.tabWidget_importExport.setTabText(self.tabWidget_importExport.indexOf(self.tab_export), QtWidgets.QApplication.translate("standardCameraForm", "Export", None, -1))
        self.groupBox_playBlast.setTitle(QtWidgets.QApplication.translate("standardCameraForm", "Play Blast:", None, -1))
        self.pushButton_updatePath_playBlast.setText(QtWidgets.QApplication.translate("standardCameraForm", "U", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("standardCameraForm", "Out Path:", None, -1))
        self.pushButton_playBlastChoose.setText(QtWidgets.QApplication.translate("standardCameraForm", "...", None, -1))
        self.pushButton_playBlast_go.setText(QtWidgets.QApplication.translate("standardCameraForm", "Go", None, -1))


# UI END

        standardCameraForm.setWindowTitle(QtWidgets.QApplication.translate("standardCameraForm", "Standard Camera V1.35b by WangHaorun", None, -1))

        self.shotDir = "I:/"
        self.localDir = "E:/Projects/"
        self.serverDir = "Cache/ABC/Camera/"

        self.setMinimumSize(QSize(442, 141))
        self.setMaximumSize(QSize(442, 141))

        self.groupBox_playBlast.setHidden(True)
        self.tabWidget_importExport.setHidden(True)
        self.groupBox_lookAtParameter.setHidden(True)

        self.pushButton_update.clicked.connect(self.whr_update)
        self.pushButton_createCamera.clicked.connect(self.whr_createCamera)
        self.pushButton_linkTwist.clicked.connect(self.whr_createLinkTwist)
        self.pushButton_lookAt.clicked.connect(self.whr_groupBox_lookAtParameter_setHidden)
        self.pushButton_playBlast.clicked.connect(self.whr_groupBox_playBlast_setHidden)
        self.pushButton_importExport.clicked.connect(self.whr_tabWidget_importExport_setHidden)
        self.sel_to_stdcam.clicked.connect(self.sel_to_std_cam)

        
        self.pushButton_abcCacheChoose_import.clicked.connect(self.whr_abcCacheChoose_import)
        self.pushButton_abcCacheChoose_export.clicked.connect(self.whr_abcCacheChoose_export)

        self.pushButton_playBlastChoose.clicked.connect(self.whr_playBlastChoose)

        self.pushButton_updatePath_import.clicked.connect(self.whr_updatePath_import)
        self.pushButton_updatePath_export.clicked.connect(self.whr_updatePath_export)

        self.pushButton_updatePath_playBlast.clicked.connect(self.whr_updatePath_playBlast)

        self.pushButton_abcCache_export.clicked.connect(self.whr_cameraCache_export)
        self.pushButton_abcCache_import.clicked.connect(self.whr_cameraCache_import)

        self.pushButton_playBlast_go.clicked.connect(self.whr_doPlayblast)
        

        self.pushButton_createLookAt.clicked.connect(self.whr_createLookAt)

        self.pushButton_toStereo.clicked.connect(self.whr_toStereo)

    def whr_groupBox_lookAtParameter_setHidden(self):
        if self.groupBox_lookAtParameter.isHidden():
            self.groupBox_lookAtParameter.setHidden(False)
        else:
            self.groupBox_lookAtParameter.setHidden(True)
        self.whr_panel_size()

    def whr_groupBox_playBlast_setHidden(self):
        self.whr_updatePath_playBlast()
        if self.groupBox_playBlast.isHidden():
            self.groupBox_playBlast.setHidden(False)
        else:
            self.groupBox_playBlast.setHidden(True)
        self.whr_panel_size()

    def whr_tabWidget_importExport_setHidden(self):
        if self.tabWidget_importExport.isHidden():
            self.tabWidget_importExport.setHidden(False)
        else:
            self.tabWidget_importExport.setHidden(True)
        self.whr_panel_size()

    def whr_panel_size(self):
        h = 141
        if not self.groupBox_lookAtParameter.isHidden():
            h += 161
        if not self.tabWidget_importExport.isHidden():
            h += 111
        if not self.groupBox_playBlast.isHidden():
            h += 100
        self.setMinimumSize(QSize(442, h))
        self.setMaximumSize(QSize(442, h))
        self.resize(442, h)


    @undoable
    def whr_exists(self):
        self.stdCameraTr = ""
        self.stdCameraShape = ""
        self.label_cameraName.setText("")
        self.pushButton_createCamera.setText("Create\nCamera")
        list_cam_tr = mel.eval('listTransforms -cameras')
        print list_cam_tr
        for cam_tr in list_cam_tr:
            if cmds.attributeQuery("StandardCamera", node=cam_tr, exists=True):
                self.stdCameraTr = cam_tr
                self.stdCameraShape = cmds.listRelatives(cam_tr, s=True, f=True)[0]
                self.label_cameraName.setText(self.stdCameraTr)
                self.pushButton_createCamera.setText("Select\nCamera")
                return True
        return False

    def whr_existsStereo(self):
        self.stdCameraStereoTr = ""
        self.stdCameraStereoShape = ""
        self.pushButton_toStereo.setText("To\nStereo")
        list_cam_tr = mel.eval('listTransforms -cameras')
        print list_cam_tr
        for cam_tr in list_cam_tr:
            if cmds.attributeQuery("StandardStereo", node=cam_tr, exists=True):
                self.stdCameraStereoTr = cam_tr
                self.stdCameraStereoShape = cmds.listRelatives(cam_tr, s=True, f=True)[0]
                self.pushButton_toStereo.setText("Select\nStereo")
                return True
        return False

    @undoable
    def whr_createCamera(self):
        filepath = cmds.file(q=True, sn=True)
        fileinfo = QFileInfo(filepath)
        print
        if fileinfo.baseName() == "":
            QMessageBox.warning(self,"Warning","The scene did not save.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if True:
        # if not self.whr_exists():
            sel = cmds.ls(sl=True)
            transform = ""
            shape = ""
            if len(sel) > 0:
                if cmds.objExists(fileinfo.baseName()):
                    QMessageBox.warning(self,"Warning","The current scenario name has been occupied. \nUnable to create a standard camera.",QMessageBox.Ok, QMessageBox.Ok)
                    return
                transform = sel[0]
                if not fileinfo.baseName() == transform:
                    transform = cmds.rename(transform, fileinfo.baseName())
                shape = cmds.rename(cmds.listRelatives(transform, s=True)[0], fileinfo.baseName()+"Shape1")
                if cmds.nodeType(shape) != "camera":
                    return
            else:
                if cmds.objExists(fileinfo.baseName()):
                    QMessageBox.warning(self,"Warning","The current scenario name has been occupied. \nUnable to create a standard camera.",QMessageBox.Ok, QMessageBox.Ok)
                    return
                cameraName = cmds.camera()
                cameraName[0] = cmds.rename(cameraName[0], fileinfo.baseName())
                print cameraName
                mel.eval("cameraMakeNode 2 \""+cameraName[0]+"\";")
                transform = cameraName[0]
                shape = cmds.rename(cmds.listRelatives(transform, s=True)[0], fileinfo.baseName()+"Shape1")

            cmds.setAttr( transform+'.rotateOrder', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateX', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateY', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateZ', keyable=True )
            cmds.setAttr( transform+'.rotatePivotX', keyable=True )
            cmds.setAttr( transform+'.rotatePivotY', keyable=True )
            cmds.setAttr( transform+'.rotatePivotZ', keyable=True )

            cmds.addAttr( transform, nn="0. -------STC-------", ln="StandardCamera", at="enum", en="Main Camera")
            cmds.setAttr( transform+'.StandardCamera', e=True, keyable=True, lock=True)

            cmds.addAttr( transform, ln="focalLength", at="double", dv=35)
            cmds.setAttr( transform+'.focalLength', e=True, keyable=True)
            cmds.setAttr( transform+'.focalLength', cmds.getAttr(shape+'.focalLength'))
            if cmds.connectionInfo(shape+".focalLength", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focalLength", sfd=True), transform+".focalLength")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focalLength", sfd=True), shape+".focalLength")
            cmds.connectAttr(transform+".focalLength", shape+".focalLength")

            cmds.addAttr( transform, nn="1. -------DOF-------", ln="depthOfField", at="enum", en="off:on:")
            cmds.setAttr( transform+'.depthOfField', e=True, keyable=True)
            cmds.setAttr( transform+'.depthOfField', cmds.getAttr(shape+'.depthOfField'))
            cmds.connectAttr(transform+".depthOfField", shape+".depthOfField")

            cmds.addAttr( transform, ln="focusDistance", at="double", dv=6)
            cmds.setAttr( transform+'.focusDistance', e=True, keyable=True)
            cmds.setAttr( transform+'.focusDistance', cmds.getAttr(shape+'.focusDistance'))
            if cmds.connectionInfo(shape+".focusDistance", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focusDistance", sfd=True), transform+".focusDistance")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focusDistance", sfd=True), shape+".focusDistance")
            cmds.connectAttr(transform+".focusDistance", shape+".focusDistance")

            cmds.addAttr( transform, ln="fStop", at="double", dv=5)
            cmds.setAttr( transform+'.fStop', e=True, keyable=True)
            cmds.setAttr( transform+'.fStop', cmds.getAttr(shape+'.fStop'))
            if cmds.connectionInfo(shape+".fStop", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".fStop", sfd=True), transform+".fStop")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".fStop", sfd=True), shape+".fStop")
            cmds.connectAttr(transform+".fStop", shape+".fStop")

            cmds.addAttr( transform, ln="focusRegionScale", at="double", dv=1)
            cmds.setAttr( transform+'.focusRegionScale', e=True, keyable=True)
            cmds.setAttr( transform+'.focusRegionScale', cmds.getAttr(shape+'.focusRegionScale'))
            if cmds.connectionInfo(shape+".focusRegionScale", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focusRegionScale", sfd=True), transform+".focusRegionScale")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focusRegionScale", sfd=True), shape+".focusRegionScale")
            cmds.connectAttr(transform+".focusRegionScale", shape+".focusRegionScale")

            cmds.addAttr( transform, nn="2. -------AIM-------", ln="AIM", at="enum", en="------------:")
            cmds.setAttr( transform+'.AIM', e=True, keyable=True, lock=True)
            cmds.addAttr( transform, ln="twist", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.twist', keyable=True )

            cmds.addAttr( transform, nn="3. -------SHK-------", ln="SHK", at="enum", en="------------:")
            cmds.setAttr( transform+'.SHK', e=True, keyable=True, lock=True)
            cmds.addAttr( transform, ln="rangeX", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.rangeX', keyable=True )
            cmds.addAttr( transform, ln="rangeY", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.rangeY', keyable=True )
            cmds.addAttr( transform, ln="frequencyX", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.frequencyX', keyable=True )
            cmds.addAttr( transform, ln="frequencyY", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.frequencyY', keyable=True )

            cmds.camera(transform, e=True, displaySafeAction=True, displaySafeTitle=True)

            # shk = cmds.createNode( 'transform', n=transform+"_shake")
            # cmds.addAttr(shk, ln="StandardCamera", at="enum", en="Main Camera")
            # cmds.setAttr(shk+".tx", l=True)
            # cmds.setAttr(shk+".ty", l=True)
            # cmds.setAttr(shk+".tz", l=True)
            # cmds.setAttr(shk+".rz", l=True)
            # cmds.setAttr(shk+".sx", l=True)
            # cmds.setAttr(shk+".sy", l=True)
            # cmds.setAttr(shk+".sz", l=True)
            # cmds.setAttr(shk+".v", l=True)
            # ctl = mel.eval("createNode nurbsCurve -n \"CAM_CTLShape\" -p "+transform+";")
            # mel.eval("setAttr -k off \".v\";\n\tsetAttr \".ove\" yes;\n\tsetAttr \".ovc\" 17;\n\tsetAttr \".cc\" -type \"nurbsCurve\" \n\t\t1 27 0 no 3\n\t\t28 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\n\t\t\n\t\t28\n\t\t0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.36014792323112488 -0.0068118572235107422\n\t\t-0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t-0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.29241830110549927 0.36014792323112488 -0.0068118572235107422\n\t\t0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 -0.040136769413948059 -0.0068118572235107422\n\t\t-0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t-0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.29241830110549927 -0.040136769413948059 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t-0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t;\n\tsetAttr \".oclr\" -type \"float3\" 0.065573774 0.065573774 0.065573774 ;")
            # cmds.parent(shape, shk, s=True, add=True)
            # cmds.parent(shape, s=True, rm=True)
            # cmds.parent(shk, transform)
            # newName = transform
            # ctl = cmds.rename(transform, "Camera_Ctrl")
            # cmds.rename(shk, newName)

            print "expression -s \""+transform+".rotateAxisX = noise((time*"+transform+".frequencyX)+0)*"+transform+".rangeX;\\n"+transform+".rotateAxisY = noise((time*"+transform+".frequencyY)+1)*"+transform+".rangeY;\"  -o a -ae 1 -uc all ;"
            mel.eval("expression -s \""+transform+".rotateAxisX = noise((time*"+transform+".frequencyX)+0)*"+transform+".rangeX;\\n"+transform+".rotateAxisY = noise((time*"+transform+".frequencyY)+1)*"+transform+".rangeY;\"  -o a -ae 1 -uc all ;")

            self.whr_exists()
        else:
            cmds.select(self.stdCameraTr, r=True)

    @undoable
    def sel_to_std_cam(self):
        sel = cmds.ls(sl=True)
        transform = ""
        shape = ""
        if len(sel) > 0:
            transform = sel[0]
            shape = cmds.rename(cmds.listRelatives(transform, s=True)[0], transform + "Shape1")
            if cmds.nodeType(shape) != "camera":
                return
        cmds.setAttr(transform + '.rotateOrder', keyable=True)
        cmds.setAttr(transform + '.rotatePivotTranslateX', keyable=True)
        cmds.setAttr(transform + '.rotatePivotTranslateY', keyable=True)
        cmds.setAttr(transform + '.rotatePivotTranslateZ', keyable=True)
        cmds.setAttr(transform + '.rotatePivotX', keyable=True)
        cmds.setAttr(transform + '.rotatePivotY', keyable=True)
        cmds.setAttr(transform + '.rotatePivotZ', keyable=True)

        cmds.addAttr(transform, nn="0. -------STC-------", ln="StandardCamera", at="enum", en="Main Camera")
        cmds.setAttr(transform + '.StandardCamera', e=True, keyable=True, lock=True)

        cmds.addAttr(transform, ln="focalLength", at="double", dv=35)
        cmds.setAttr(transform + '.focalLength', e=True, keyable=True)
        cmds.setAttr(transform + '.focalLength', cmds.getAttr(shape + '.focalLength'))
        if cmds.connectionInfo(shape + ".focalLength", id=True):
            cmds.connectAttr(cmds.connectionInfo(shape + ".focalLength", sfd=True), transform + ".focalLength")
            cmds.disconnectAttr(cmds.connectionInfo(shape + ".focalLength", sfd=True), shape + ".focalLength")
        cmds.connectAttr(transform + ".focalLength", shape + ".focalLength")

        cmds.addAttr(transform, nn="1. -------DOF-------", ln="depthOfField", at="enum", en="off:on:")
        cmds.setAttr(transform + '.depthOfField', e=True, keyable=True)
        cmds.setAttr(transform + '.depthOfField', cmds.getAttr(shape + '.depthOfField'))
        cmds.connectAttr(transform + ".depthOfField", shape + ".depthOfField")

        cmds.addAttr(transform, ln="focusDistance", at="double", dv=6)
        cmds.setAttr(transform + '.focusDistance', e=True, keyable=True)
        cmds.setAttr(transform + '.focusDistance', cmds.getAttr(shape + '.focusDistance'))
        if cmds.connectionInfo(shape + ".focusDistance", id=True):
            cmds.connectAttr(cmds.connectionInfo(shape + ".focusDistance", sfd=True), transform + ".focusDistance")
            cmds.disconnectAttr(cmds.connectionInfo(shape + ".focusDistance", sfd=True), shape + ".focusDistance")
        cmds.connectAttr(transform + ".focusDistance", shape + ".focusDistance")

        cmds.addAttr(transform, ln="fStop", at="double", dv=5)
        cmds.setAttr(transform + '.fStop', e=True, keyable=True)
        cmds.setAttr(transform + '.fStop', cmds.getAttr(shape + '.fStop'))
        if cmds.connectionInfo(shape + ".fStop", id=True):
            cmds.connectAttr(cmds.connectionInfo(shape + ".fStop", sfd=True), transform + ".fStop")
            cmds.disconnectAttr(cmds.connectionInfo(shape + ".fStop", sfd=True), shape + ".fStop")
        cmds.connectAttr(transform + ".fStop", shape + ".fStop")

        cmds.addAttr(transform, ln="focusRegionScale", at="double", dv=1)
        cmds.setAttr(transform + '.focusRegionScale', e=True, keyable=True)
        cmds.setAttr(transform + '.focusRegionScale', cmds.getAttr(shape + '.focusRegionScale'))
        if cmds.connectionInfo(shape + ".focusRegionScale", id=True):
            cmds.connectAttr(cmds.connectionInfo(shape + ".focusRegionScale", sfd=True),
                             transform + ".focusRegionScale")
            cmds.disconnectAttr(cmds.connectionInfo(shape + ".focusRegionScale", sfd=True), shape + ".focusRegionScale")
        cmds.connectAttr(transform + ".focusRegionScale", shape + ".focusRegionScale")

        cmds.addAttr(transform, nn="2. -------AIM-------", ln="AIM", at="enum", en="------------:")
        cmds.setAttr(transform + '.AIM', e=True, keyable=True, lock=True)
        cmds.addAttr(transform, ln="twist", at="doubleAngle", dv=0)
        cmds.setAttr(transform + '.twist', keyable=True)

        cmds.addAttr(transform, nn="3. -------SHK-------", ln="SHK", at="enum", en="------------:")
        cmds.setAttr(transform + '.SHK', e=True, keyable=True, lock=True)
        cmds.addAttr(transform, ln="rangeX", at="doubleAngle", dv=0)
        cmds.setAttr(transform + '.rangeX', keyable=True)
        cmds.addAttr(transform, ln="rangeY", at="doubleAngle", dv=0)
        cmds.setAttr(transform + '.rangeY', keyable=True)
        cmds.addAttr(transform, ln="frequencyX", at="doubleAngle", dv=0)
        cmds.setAttr(transform + '.frequencyX', keyable=True)
        cmds.addAttr(transform, ln="frequencyY", at="doubleAngle", dv=0)
        cmds.setAttr(transform + '.frequencyY', keyable=True)

        cmds.camera(transform, e=True, displaySafeAction=True, displaySafeTitle=True)

        # shk = cmds.createNode( 'transform', n=transform+"_shake")
        # cmds.addAttr(shk, ln="StandardCamera", at="enum", en="Main Camera")
        # cmds.setAttr(shk+".tx", l=True)
        # cmds.setAttr(shk+".ty", l=True)
        # cmds.setAttr(shk+".tz", l=True)
        # cmds.setAttr(shk+".rz", l=True)
        # cmds.setAttr(shk+".sx", l=True)
        # cmds.setAttr(shk+".sy", l=True)
        # cmds.setAttr(shk+".sz", l=True)
        # cmds.setAttr(shk+".v", l=True)
        # ctl = mel.eval("createNode nurbsCurve -n \"CAM_CTLShape\" -p "+transform+";")
        # mel.eval("setAttr -k off \".v\";\n\tsetAttr \".ove\" yes;\n\tsetAttr \".ovc\" 17;\n\tsetAttr \".cc\" -type \"nurbsCurve\" \n\t\t1 27 0 no 3\n\t\t28 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\n\t\t\n\t\t28\n\t\t0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.36014792323112488 -0.0068118572235107422\n\t\t-0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t-0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.29241830110549927 0.36014792323112488 -0.0068118572235107422\n\t\t0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 -0.040136769413948059 -0.0068118572235107422\n\t\t-0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t-0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.38808643817901611 0.54529058933258057 -0.37863010168075562\n\t\t0.38808643817901611 -0.22527951002120972 -0.37863010168075562\n\t\t0.29241830110549927 -0.040136769413948059 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t-0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 1.5120635032653809\n\t\t-0.29241830110549927 -0.26167768239974976 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 -0.0068118572235107422\n\t\t-0.29241830110549927 0.66113805770874023 1.5120635032653809\n\t\t;\n\tsetAttr \".oclr\" -type \"float3\" 0.065573774 0.065573774 0.065573774 ;")
        # cmds.parent(shape, shk, s=True, add=True)
        # cmds.parent(shape, s=True, rm=True)
        # cmds.parent(shk, transform)
        # newName = transform
        # ctl = cmds.rename(transform, "Camera_Ctrl")
        # cmds.rename(shk, newName)

        print "expression -s \"" + transform + ".rotateAxisX = noise((time*" + transform + ".frequencyX)+0)*" + transform + ".rangeX;\\n" + transform + ".rotateAxisY = noise((time*" + transform + ".frequencyY)+1)*" + transform + ".rangeY;\"  -o a -ae 1 -uc all ;"
        mel.eval(
            "expression -s \"" + transform + ".rotateAxisX = noise((time*" + transform + ".frequencyX)+0)*" + transform + ".rangeX;\\n" + transform + ".rotateAxisY = noise((time*" + transform + ".frequencyY)+1)*" + transform + ".rangeY;\"  -o a -ae 1 -uc all ;")


    @undoable
    def whr_createLinkTwist(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)
            cmds.connectAttr(self.stdCameraTr+".twist", grp[0]+".twist")
        except Exception,e:
            QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)

    def whr_abcCacheChoose_import(self):
        multipleFilters = "Abc Files (*.abc)"
        abcpath = cmds.fileDialog2(cap="Import Camera ABC Cache:",okc="Import", fileFilter=multipleFilters, fileMode=1, dialogStyle=2, dir=self.lineEdit_abcCacheFilePath_import.text())
        if not abcpath is None:
            self.lineEdit_abcCacheFilePath_import.setText(abcpath[0])

    def whr_abcCacheChoose_export(self):
        multipleFilters = "Abc Files (*.abc)"
        abcpath = cmds.fileDialog2(cap="Export Camera ABC Cache:",okc="Export", fileFilter=multipleFilters, dialogStyle=2, dir=self.lineEdit_abcCacheFilePath_export.text())
        if not abcpath is None:
            self.lineEdit_abcCacheFilePath_export.setText(abcpath[0])

    def whr_playBlastChoose(self):
        multipleFilters = "Mov Files (*.mov)"
        path = cmds.fileDialog2(cap="Play Blast Out Path:",okc="Ok", fileFilter=multipleFilters, dialogStyle=2, dir=self.lineEdit_playBlast.text())
        if not path is None:
            self.lineEdit_playBlast.setText(path[0])

    def whr_update(self):
        self.whr_exists()
        self.whr_existsStereo()
        #self.whr_updatePath_import()
        #self.whr_updatePath_export()

    def whr_updatePath_playBlast(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        scene = cmds.file(q=True, sn=True)
        filename = QFileInfo(scene).baseName()
        path = QFileInfo(scene).absolutePath()
        self.lineEdit_playBlast.setText(path+"/"+filename+"_pv.mov")

    def whr_updatePath_import(self):
        abcpath = ""
        scenepath = cmds.file(q=True, sn=True)
        scene_filename = QFileInfo(scenepath).baseName()
        if self.shotDir in scenepath:
            list_path = scenepath.split("/")
            n = len(list_path)
            for i in range(0, n-3):
                abcpath += list_path[i] + "/"
            list_name = list_path[n-1].split(".")
            if len(list_name) > 2:
                QMessageBox.warning(self,"Warning","File name error: '.'",QMessageBox.Ok, QMessageBox.Ok)
                return
            abcpath += self.serverDir
            if not os.path.exists(abcpath):
                os.makedirs(abcpath)
            filename = list_name[0]
            list_n = filename.split("_")
            path = abcpath + scene_filename + "_0.abc"
            i=0
            while os.path.exists(path):
                i += 1
                path = abcpath + scene_filename +"_"+ str(i) + ".abc"
            path = abcpath + scene_filename +"_"+ str(i-1) + ".abc"
            self.lineEdit_abcCacheFilePath_import.setText(path)
            self.lineEdit_abcCacheFilePath_import.setToolTip(path)
        else:
            QMessageBox.warning(self,"Warning","Scene file path for errors.\ni.e. "+self.shotDir,QMessageBox.Ok, QMessageBox.Ok)


    def whr_updatePath_export(self):
        scene = cmds.file(q=True, sn=True)
        scene_filename = QFileInfo(scene).completeBaseName()
        scene_path = QFileInfo(scene).absolutePath()
        if self.shotDir in scene_path:
            #+ str(0) 
            path = scene_path.replace(self.shotDir, self.localDir) + "/" + scene_filename +"_"+ ".abc"
            self.lineEdit_abcCacheFilePath_export.setText(path)
            self.lineEdit_abcCacheFilePath_export.setToolTip(path)
        else:
            QMessageBox.warning(self,"Warning","Scene file path for errors.\ni.e. "+self.shotDir,QMessageBox.Ok, QMessageBox.Ok)


    @undoable
    def whr_cameraCache_export(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        abcpath = self.lineEdit_abcCacheFilePath_export.text()
        print abcpath
        if abcpath == "":
            QMessageBox.warning(self,"Warning","Export path is empty.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","File already exists, click U button to update the path.",QMessageBox.Ok, QMessageBox.Ok)
            return
        min = int(cmds.playbackOptions(q=True, min=True))
        max = int(cmds.playbackOptions(q=True, max=True))
        e = "AbcExport -verbose -j \"-frameRange "+str(min)+" "+str(max)+" -stripNamespaces -worldSpace -dataFormat ogawa -root "+self.stdCameraTr+" -file "+abcpath+"\";"
        try:
            mel.eval(e)
        except RuntimeError, e:
            QMessageBox.warning(self,"Warning","Export command execution error. \nCommand: "+e,QMessageBox.Ok, QMessageBox.Ok)
            return
        if not os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","Export the cache does not exist.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            QMessageBox.information(self,"Successful","Successful the export cache.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)

    @undoable
    def whr_cameraCache_import(self):
        abcpath = self.lineEdit_abcCacheFilePath_import.text()
        print abcpath
        if abcpath == "":
            QMessageBox.warning(self,"Warning","Import path is empty.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if not os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","Import the cache does not exist, click U button to update the path.",QMessageBox.Ok, QMessageBox.Ok)
            return
        e = "AbcImport -mode import \""+abcpath+"\";"
        if mel.eval(e):
            QMessageBox.information(self,"Successful","Successful the import cache.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Warning","Import command execution error. \nCommand: "+e,QMessageBox.Ok, QMessageBox.Ok)
            


    def whr_createLookAt_auto(self):
        if self.radioButton_auto.isChecked():
            pass

    def whr_createLookAt_manual(self):
        if self.radioButton_manual.isChecked():
            pass

    def whr_createLookAt_framesPerSample(self):
        if self.radioButton_framesPerSample.isChecked():
            pass

    def whr_createLookAt_smartBake(self):
        if self.radioButton_smartBake.isChecked():
            pass

    def whr_toStereo(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if self.whr_existsStereo():
            cmds.select(self.stdCameraStereoTr, r=True)
            return
        if cmds.nodeType(self.stdCameraShape) == "camera":
            print "camera: ", self.stdCameraTr
            stereo = maya.app.stereo.stereoCameraRig.createStereoCameraRig()
            stereo[0] = cmds.rename(stereo[0], self.stdCameraTr+"_Stereo")
            stereo[1] = cmds.rename(stereo[1], self.stdCameraTr+"_Left")
            stereo[2] = cmds.rename(stereo[2], self.stdCameraTr+"_Right")
            print "stereo: ", stereo
            self.stdCameraStereoTr = stereo[0]
            self.stdCameraStereoShape = cmds.listRelatives(stereo[0])[0]
            cmds.addAttr( self.stdCameraStereoTr, nn="0. -------STS-------", ln="StandardStereo", at="enum", en="Main Stereo")
            cmds.setAttr( self.stdCameraStereoTr+'.StandardStereo', e=True, keyable=True, lock=False)
            print "stereoTr: ",self.stdCameraStereoTr
            print "stereoShape: ",self.stdCameraStereoShape
            cmds.connectAttr( (self.stdCameraTr+'.StandardCamera'), (self.stdCameraStereoTr+'.StandardStereo') )
            cmds.setAttr( self.stdCameraStereoTr+'.StandardStereo', e=True, keyable=True, lock=True)
            cmds.parentConstraint( self.stdCameraTr, self.stdCameraStereoTr, weight=True)
            cmds.connectAttr( (self.stdCameraShape+'.focalLength'), (self.stdCameraStereoShape+'.focalLength') )
            cmds.connectAttr( (self.stdCameraShape+'.horizontalFilmAperture'), (self.stdCameraStereoShape+'.horizontalFilmAperture') )
            cmds.connectAttr( (self.stdCameraShape+'.verticalFilmAperture'), (self.stdCameraStereoShape+'.verticalFilmAperture') )
            cmds.connectAttr( (self.stdCameraShape+'.lensSqueezeRatio'), (self.stdCameraStereoShape+'.lensSqueezeRatio') )
            cmds.connectAttr( (self.stdCameraShape+'.depthOfField'), (self.stdCameraStereoShape+'.depthOfField') )
            cmds.connectAttr( (self.stdCameraShape+'.focusDistance'), (self.stdCameraStereoShape+'.focusDistance') )
            cmds.connectAttr( (self.stdCameraShape+'.fStop'), (self.stdCameraStereoShape+'.fStop') )
            cmds.connectAttr( (self.stdCameraShape+'.focusRegionScale'), (self.stdCameraStereoShape+'.focusRegionScale') )
            cmds.connectAttr( (self.stdCameraShape+'.shakeEnabled'), (self.stdCameraStereoShape+'.shakeEnabled') )
            cmds.connectAttr( (self.stdCameraShape+'.horizontalShake'), (self.stdCameraStereoShape+'.horizontalShake') )
            cmds.connectAttr( (self.stdCameraShape+'.verticalShake'), (self.stdCameraStereoShape+'.verticalShake') )
            cmds.connectAttr( (self.stdCameraShape+'.shakeOverscanEnabled'), (self.stdCameraStereoShape+'.shakeOverscanEnabled') )
            cmds.connectAttr( (self.stdCameraShape+'.shakeOverscan'), (self.stdCameraStereoShape+'.shakeOverscan') )
            for st_cam in stereo:
                st_cam_shapes = cmds.listRelatives(st_cam)
                if cmds.nodeType(st_cam_shapes) == "camera":
                    print "stereoShape: ",st_cam_shapes
                    cmds.connectAttr( (self.stdCameraShape+'.shakeEnabled'), (st_cam_shapes[0]+'.shakeEnabled') )
                    cmds.connectAttr( (self.stdCameraShape+'.horizontalShake'), (st_cam_shapes[0]+'.horizontalShake') )
                    cmds.connectAttr( (self.stdCameraShape+'.verticalShake'), (st_cam_shapes[0]+'.verticalShake') )
                    cmds.connectAttr( (self.stdCameraShape+'.shakeOverscanEnabled'), (st_cam_shapes[0]+'.shakeOverscanEnabled') )
                    cmds.connectAttr( (self.stdCameraShape+'.shakeOverscan'), (st_cam_shapes[0]+'.shakeOverscan') )

    @undoable
    def whr_createLookAt(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.connectionInfo(self.stdCameraShape+".centerOfInterest", id=True):
            QMessageBox.warning(self,"Warning","The standard camera have aim constraint.",QMessageBox.Ok, QMessageBox.Ok)
            cmds.select(self.stdCameraTr, r=True)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotX", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotY", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotZ", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateX", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateY", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateZ", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return

        try:
            min = int(cmds.playbackOptions(q=True, min=True))
            max = int(cmds.playbackOptions(q=True, max=True))
            loc_aim = ""

            cmds.currentTime(min)
            if self.radioButton_auto.isChecked():
                loc_aim = cmds.spaceLocator(n="loc_aim")[0]#look_at
                cmds.parent(loc_aim, self.stdCameraTr)
                cmds.setAttr(loc_aim+".tx", 0)
                cmds.setAttr(loc_aim+".ty", 0)
                cmds.setAttr(loc_aim+".tz", -self.doubleSpinBox_distance.value())
                cmds.setAttr(loc_aim+".rx", 0)
                cmds.setAttr(loc_aim+".ry", 0)
                cmds.setAttr(loc_aim+".rz", 0)
                constraint_temp = cmds.parentConstraint( self.stdCameraTr, loc_aim, mo=True, weight=1)
                cmds.parent(loc_aim, w=True)
                cmds.bakeResults(loc_aim+".t", simulation=True, t=(min, max))
                cmds.delete(constraint_temp)

                print self.stdCameraTr
                if cmds.connectionInfo(self.stdCameraTr+".rx", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rx", sfd=True), self.stdCameraTr+".rx")
                if cmds.connectionInfo(self.stdCameraTr+".ry", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".ry", sfd=True), self.stdCameraTr+".ry")
                if cmds.connectionInfo(self.stdCameraTr+".rz", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rz", sfd=True), self.stdCameraTr+".rz")
                mel.eval("cameraMakeNode 2 \""+self.stdCameraTr+"\";")
                grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)[0]
                print grp
                camera_aim = cmds.listConnections(grp+".target", d=False, s=True)[0]
                print camera_aim, grp
                cmds.parent(loc_aim, grp)
                cmds.parent(camera_aim, loc_aim)
                    
                cmds.setAttr(camera_aim+".tx", 0)
                cmds.setAttr(camera_aim+".ty", 0)
                cmds.setAttr(camera_aim+".tz", 0)

            if self.radioButton_manual.isChecked():
                sel = cmds.ls(sl=True)
                loc = sel[0]
                key = []
                if cmds.nodeType(loc) == "transform" and cmds.nodeType(cmds.listRelatives(loc, s=True)[0]) == "locator":
                    dds = cmds.createNode("distanceDimShape")
                    cmds.connectAttr(loc+".worldPosition", dds+".startPoint")
                    loc_end = cmds.spaceLocator(n="loc_end")[0]
                    cmds.setAttr( loc_end+".tx",lock = True)
                    cmds.setAttr( loc_end+".ty",lock = True)
                    cmds.setAttr( loc_end+".tz",lock = True)
                    cmds.setAttr( loc_end+".rx",lock = True)
                    cmds.setAttr( loc_end+".ry",lock = True)
                    cmds.setAttr( loc_end+".rz",lock = True)
                    cmds.parent(loc_end, self.stdCameraTr)
                    cmds.connectAttr(loc_end+".worldPosition", dds+".endPoint")

                    loc_temp = cmds.spaceLocator(n="loc_temp")[0]
                    cmds.setAttr( loc_temp+".tx",lock = True)
                    cmds.setAttr( loc_temp+".ty",lock = True)
                    cmds.setAttr( loc_temp+".tz",-5)
                    #cmds.setAttr( loc_temp+".tz",lock = True)
                    cmds.setAttr( loc_temp+".rx",lock = True)
                    cmds.setAttr( loc_temp+".ry",lock = True)
                    cmds.setAttr( loc_temp+".rz",lock = True)
                    cmds.parent(loc_temp, self.stdCameraTr)

                    loc_aim = cmds.spaceLocator(n="loc_aim")[0]#look_at

                    tx = cmds.keyframe(loc+".tx", q=True)
                    ty = cmds.keyframe(loc+".ty", q=True)
                    tz = cmds.keyframe(loc+".tz", q=True)
             
                    temp = []
                    if not tx is None:
                        temp = temp + tx
                    if not ty is None:
                        temp = temp + ty
                    if not tz is None:
                        temp = temp + tz
        
                    if len(temp) == 0:
                        pass
                    else:
                        for t in temp:
                            if not t in key:
                                key.append(t)
                        key.sort()
                        print key

                    if len(key) == 0:
                        QMessageBox.critical(self,"Error","The target point is not key animation.",QMessageBox.Ok, QMessageBox.Ok)
                        return
                        '''
                        ta = cmds.xform(loc, t=1,ws=True, q=1)
                        tb = cmds.xform(loc_temp, t=1,ws=True, q=1)
                        tz = cmds.xform(loc_end, t=1,ws=True, q=1)
                        di = cmds.getAttr(dds+".distance")
                        va = om.MVector(ta) - om.MVector(tz)
                        vb = om.MVector(tb) - om.MVector(tz)
                        print va,vb, -di*math.sin(va.angle(vb))
                        cmds.setAttr(loc_temp+".tz", -di*math.cos(vb.angle(va)))
                        cmds.xform(loc_aim,ws=1, t=cmds.xform(loc_temp, t=1,ws=True, q=1))
                        pass
                        '''
                    else:
                        for k in range(min, max+1):#key
                            cmds.currentTime(k)
                            ta = cmds.xform(loc, t=1,ws=True, q=1)
                            tb = cmds.xform(loc_temp, t=1,ws=True, q=1)
                            tz = cmds.xform(loc_end, t=1,ws=True, q=1)
                            di = cmds.getAttr(dds+".distance")
                            print "di:",di
                            va = om.MVector(ta) - om.MVector(tz)
                            vb = om.MVector(tb) - om.MVector(tz)
                            print va,vb, -di*math.sin(va.angle(vb))
                            cmds.setAttr(loc_temp+".tz", -di*math.cos(vb.angle(va)))
                            t = cmds.xform(loc_temp, t=1,ws=True, q=1)
                            cmds.xform(loc_aim,ws=1, t=cmds.xform(loc_temp, t=1,ws=True, q=1))
                            cmds.setKeyframe( loc_aim, attribute='t', t=k )
                            pass

                    print self.stdCameraTr
                    if cmds.connectionInfo(self.stdCameraTr+".rx", id=True):
                        cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rx", sfd=True), self.stdCameraTr+".rx")
                    if cmds.connectionInfo(self.stdCameraTr+".ry", id=True):
                        cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".ry", sfd=True), self.stdCameraTr+".ry")
                    if cmds.connectionInfo(self.stdCameraTr+".rz", id=True):
                        cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rz", sfd=True), self.stdCameraTr+".rz")
                    mel.eval("cameraMakeNode 2 \""+self.stdCameraTr+"\";")
                    grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)[0]
                    print grp
                    camera_aim = cmds.listConnections(grp+".target", d=False, s=True)[0]
                    print camera_aim, grp
                    cmds.parent(loc_aim, grp)
                    cmds.parent(camera_aim, loc_aim)
                    
                    cmds.setAttr(camera_aim+".tx", 0)
                    cmds.setAttr(camera_aim+".ty", 0)
                    cmds.setAttr(camera_aim+".tz", 0)
                    cmds.delete(loc_end)
                    cmds.delete(loc_temp)
                else:
                    QMessageBox.warning(self,"Warning","Please selection a locator for aim.",QMessageBox.Ok, QMessageBox.Ok)

            if self.radioButton_smartBake.isChecked():
                tt = self.doubleSpinBox_tolerance.value()
                cmds.filterCurve( loc_aim+".translateX", loc_aim+".translateY", loc_aim+".translateZ",f = "simplify", timeTolerance = tt )
                    
        except Exception,e:
            QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)

    @undoable
    def whr_doPlayblast(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if self.lineEdit_playBlast.text() == "":
            QMessageBox.critical(self,"Warning","The Out Path is empty.",QMessageBox.Ok, QMessageBox.Ok)
            return
        data = [[(-0.0607322, -0.0201986, -0.119611), (-0.0400222, -0.0201986, -0.119611), (-0.0400222, -0.0228166, -0.119611), (-0.0607322, -0.0228166, -0.119611)],
        [(-0.0607322, -0.0231976, -0.119611), (-0.0400222, -0.0231976, -0.119611), (-0.0400232, -0.0253616, -0.119624), (-0.0607332, -0.0253616, -0.119624)],
        [(-0.0149978, -0.0201986, -0.119611), (0.0131307, -0.0201986, -0.119611), (0.0131307, -0.0228166, -0.119611), (-0.0149978, -0.0228166, -0.119611)],
        [(-0.0149978, -0.0231976, -0.119611), (0.0131307, -0.0231976, -0.119611), (0.0131297, -0.0253616, -0.119624), (-0.0149988, -0.0253616, -0.119624)],
        [(0.0429006, -0.0201986, -0.119611), (0.0605666, -0.0201986, -0.119611), (0.0605666, -0.0228166, -0.119611), (0.0429006, -0.0228166, -0.119611)],
        [(0.0429006, -0.0231976, -0.119611), (0.0605666, -0.0231976, -0.119611), (0.0605666, -0.0253616, -0.119624), (0.0428996, -0.0253616, -0.119624)]
        ]
        shading = cmds.shadingNode("surfaceShader", asShader=True)
        cmds.setAttr(shading+".outColor", 0, 0, 0, type="double3")
        cmds.setAttr(shading+".outTransparency", 0.5, 0.5, 0.5, type="double3")
        cmds.setAttr(shading+".outMatteOpacity", 0, 0, 0, type="double3")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        cmds.connectAttr(shading+".outColor", sg+".surfaceShader", f=True)
        l_polyShape = []
        for point in data:
            poly = cmds.polyCreateFacet(ch=False, p=point )
            cmds.sets(poly, e=True, fe=sg)
            polyShape = cmds.listRelatives(poly)
            l_polyShape.append(polyShape)
            cmds.parent(polyShape[0], self.stdCameraTr, s=True, add=True)
            cmds.delete(poly)
        
        st = cmds.playbackOptions(q=True, min=True)
        et = cmds.playbackOptions(q=True, max=True)
        gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
        sd = cmds.timeControl( gPlayBackSlider, q=True, sound=True )
        if cmds.timeControl(gPlayBackSlider, q=True, rangeVisible=True):
            highlight = cmds.timeControl(gPlayBackSlider, q=True, rangeArray=True)
            st = min=highlight[0]
            et = min=highlight[1]
        cmds.setAttr("hardwareRenderingGlobals.transparencyAlgorithm", 3)
        cmds.setAttr("hardwareRenderingGlobals.transparencyQuality", 1)
        #cam_modelPanel = cmds.modelPanel(cam=self.stdCameraTr)
        #cmds.modelEditor(cam_modelPanel, edit=True, displayAppearance="smoothShaded", fogging=True, displayTextures=True)
        #editorPanelName=cam_modelPanel
        nearClipPlane = cmds.getAttr(self.stdCameraShape+".nearClipPlane")
        cmds.setAttr(self.stdCameraShape+".nearClipPlane", 0.02)
        mel.eval("playbackStateChanged;")
        cmds.playblast(filename=self.lineEdit_playBlast.text(), sound=sd, startTime=st, endTime=et, forceOverwrite=True, format="qt", compression="H.264", sequenceTime=0, clearCache=1, viewer=1, showOrnaments=1, fp=4, percent=100, quality=100, widthHeight=[1024, 429])
        mel.eval("playbackStateChanged;")
        cmds.setAttr(self.stdCameraShape+".nearClipPlane", nearClipPlane)
        for polyShape in l_polyShape:
            cmds.delete(polyShape)
        cmds.delete(shading)
        cmds.delete(sg)
        #cmds.deleteUI(cam_modelPanel,panel=True)
        
class standardCameraDialog(QDialog,Ui_standardCameraForm):
    def __init__(self, *args, **kwargs):
        if cmds.window("standardCameraForm", exists=True):
            cmds.deleteUI("standardCameraForm", window=True)
        super(standardCameraDialog, self).__init__(*args, **kwargs)
        self.setupUi( self )

def show():
    ui = standardCameraDialog(mayaMainWindow)
    ui.whr_update()
    ui.show()

#show()