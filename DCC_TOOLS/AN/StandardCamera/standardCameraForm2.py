# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'standardCameraForm.ui'
#
# Created: Tue Nov 27 19:16:14 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

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
        standardCameraForm.setWindowTitle(QtWidgets.QApplication.translate("standardCameraForm", "Standard Camera V1.05b by WangHaorun", None, -1))
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

