#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################

from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2
import maya.OpenMayaUI as mui


def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class UiDialog(QtWidgets.QDialog):

    def __init__(self, parent=getMayaWindow()):
        super(UiDialog, self).__init__(parent=parent)
        pass

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1100, 700)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.check_pb = QtWidgets.QPushButton(Dialog)
        self.check_pb.setMinimumSize(QtCore.QSize(80, 40))
        self.check_pb.setObjectName("pushButton_check")
        self.horizontalLayout_4.addWidget(self.check_pb)
        self.check_pb.setEnabled(1)
        self.submit_pb = QtWidgets.QPushButton(Dialog)
        self.submit_pb.setEnabled(0)
        self.submit_pb.setMinimumSize(QtCore.QSize(80, 40))
        self.submit_pb.setAutoDefault(False)
        self.submit_pb.setObjectName("pushButton_ok")
        self.horizontalLayout_4.addWidget(self.submit_pb)
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButton_close.setAutoDefault(False)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_4.addWidget(self.pushButton_close)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(Dialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_info = QtWidgets.QWidget(self.splitter)
        self.widget_info.setObjectName("widget_info")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_info)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.project_lb = QtWidgets.QLabel(self.widget_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_lb.sizePolicy().hasHeightForWidth())
        self.project_lb.setSizePolicy(sizePolicy)
        self.project_lb.setMinimumSize(QtCore.QSize(230, 0))
        self.project_lb.setObjectName("comboBox_project")
        self.gridLayout_7.addWidget(self.project_lb, 0, 1, 1, 1)
        self.tasks_cb = QtWidgets.QComboBox(self.widget_info)
        self.tasks_cb.addItem('')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_cb.sizePolicy().hasHeightForWidth())
        self.tasks_cb.setSizePolicy(sizePolicy)
        self.tasks_cb.setMinimumSize(QtCore.QSize(120, 0))
        # self.comboBox_taskname.setEditable(True)
        self.tasks_cb.setObjectName("comboBox_taskname")
        self.gridLayout_7.addWidget(self.tasks_cb, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_info)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 3, 1, 1)

        self.label = QtWidgets.QLabel(self.widget_info)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_info)
        self.label_8.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget_info)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 0, 1, 1, 1)
        self.user_lb = QtWidgets.QLabel(self.widget_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_lb.sizePolicy().hasHeightForWidth())
        self.user_lb.setSizePolicy(sizePolicy)
        self.user_lb.setMinimumSize(QtCore.QSize(0, 23))
        self.user_lb.setObjectName("label_user")
        self.gridLayout_7.addWidget(self.user_lb, 0, 2, 1, 1)
        self.get_task_pb = QtWidgets.QPushButton(self.widget_info)
        self.get_task_pb.setMinimumSize(QtCore.QSize(70, 23))
        self.get_task_pb.setMaximumSize(QtCore.QSize(70, 16777215))
        self.get_task_pb.setObjectName("pushButton_update_task")
        self.gridLayout_7.addWidget(self.get_task_pb, 1, 2, 1, 1)

        self.gridLayout_7.addWidget(QtWidgets.QLabel(u'上一次提交时间: '), 2, 0, 1, 1)
        self.last_update_time_lb = QtWidgets.QLabel()
        self.gridLayout_7.addWidget(self.last_update_time_lb, 2, 1, 1, 1)

        self.version_sb = QtWidgets.QSpinBox(self.widget_info)
        self.version_sb.setMinimumSize(QtCore.QSize(40, 23))
        self.version_sb.setMaximumSize(QtCore.QSize(40, 16777215))
        self.version_sb.setFrame(True)
        self.version_sb.setAlignment(QtCore.Qt.AlignCenter)
        self.version_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.version_sb.setMaximum(999)
        self.version_sb.setObjectName("spinBox_ver")
        self.gridLayout_7.addWidget(self.version_sb, 0, 4, 1, 1)

        # group_label = QtWidgets.QLabel(u'选择环节：')
        # self.gridLayout_7.addWidget(group_label, 2, 0, 1, 1)
        # self.group_cb = QtWidgets.QComboBox()
        # self.group_cb.setMaximumWidth(70)
        # self.gridLayout_7.addWidget(self.group_cb, 2, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_7)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_info)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.project_file_le = QtWidgets.QLineEdit(self.groupBox_3)
        self.project_file_le.setMinimumSize(QtCore.QSize(0, 23))
        self.project_file_le.setMaximumSize(QtCore.QSize(16777215, 23))
        self.project_file_le.setDragEnabled(True)
        self.project_file_le.setProperty("clearButtonEnabled", False)
        self.project_file_le.setObjectName("lineEdit_projectf")
        self.horizontalLayout_6.addWidget(self.project_file_le)
        self.input_file_path_pb = QtWidgets.QPushButton(self.groupBox_3)
        self.input_file_path_pb.setMinimumSize(QtCore.QSize(40, 23))
        self.input_file_path_pb.setMaximumSize(QtCore.QSize(40, 23))
        self.input_file_path_pb.setObjectName("pushButton_view_projectf")
        self.horizontalLayout_6.addWidget(self.input_file_path_pb)
        self.gridLayout_6.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        # self.checkBox_outAD = QtWidgets.QCheckBox(self.groupBox_3)
        # self.checkBox_outAD.setObjectName("checkBox_outAD")
        # self.gridLayout_6.addWidget(self.checkBox_outAD, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.widget_info)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.preview_file_le = QtWidgets.QLineEdit(self.groupBox)
        self.preview_file_le.setMinimumSize(QtCore.QSize(0, 23))
        self.preview_file_le.setMaximumSize(QtCore.QSize(16777215, 23))
        self.preview_file_le.setDragEnabled(True)
        self.preview_file_le.setProperty("clearButtonEnabled", False)
        self.preview_file_le.setObjectName("lineEdit_previewf")
        self.horizontalLayout_5.addWidget(self.preview_file_le)
        self.select_preview_file_pb = QtWidgets.QPushButton(self.groupBox)
        self.select_preview_file_pb.setMinimumSize(QtCore.QSize(40, 23))
        self.select_preview_file_pb.setMaximumSize(QtCore.QSize(40, 23))
        self.select_preview_file_pb.setObjectName("pushButton_view_previewf")
        self.horizontalLayout_5.addWidget(self.select_preview_file_pb)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_8.addWidget(self.label_2)
        self.playblast_img_pb = QtWidgets.QPushButton(self.groupBox)
        self.playblast_img_pb.setMaximumSize(QtCore.QSize(40, 16777215))
        self.playblast_img_pb.setObjectName("pushButton_preview_img")
        self.horizontalLayout_8.addWidget(self.playblast_img_pb)

        self.grab_img_pb = QtWidgets.QPushButton(self.groupBox)
        self.grab_img_pb.setText(u'截图')
        self.grab_img_pb.setMaximumSize(QtCore.QSize(40, 16777215))
        self.grab_img_pb.setObjectName("pushButton_preview_img")
        self.horizontalLayout_8.addWidget(self.grab_img_pb)

        self.playblast_prev_pb = QtWidgets.QPushButton(self.groupBox)
        self.playblast_prev_pb.setMaximumSize(QtCore.QSize(40, 16777215))
        self.playblast_prev_pb.setObjectName("pushButton_preview_mov")
        self.horizontalLayout_8.addWidget(self.playblast_prev_pb)
        spacerItem2 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.gridLayout_4.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.label_4 = QtWidgets.QLabel(self.widget_info)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.describe_te = QtWidgets.QTextEdit(self.widget_info)
        self.describe_te.setObjectName("textEdit_describe")
        self.verticalLayout.addWidget(self.describe_te)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.widget_file = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_file.sizePolicy().hasHeightForWidth())
        self.widget_file.setSizePolicy(sizePolicy)
        self.widget_file.setObjectName("widget_file")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_file)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_file)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.attachment_tw = QtWidgets.QTreeWidget(self.groupBox_2)
        self.attachment_tw.setStyleSheet("QTreeView::item {min-height: 24px; max-height: 24px;}")
        self.attachment_tw.setAlternatingRowColors(True)
        self.attachment_tw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.attachment_tw.setIndentation(0)
        self.attachment_tw.setAllColumnsShowFocus(True)
        self.attachment_tw.setObjectName("treeWidget")
        self.gridLayout_5.addWidget(self.attachment_tw, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        # self.lineEdit_limitDirs = QtWidgets.QLineEdit(self.groupBox_2)
        # self.lineEdit_limitDirs.setObjectName("lineEdit_limitDirs")
        # self.horizontalLayout_3.addWidget(self.lineEdit_limitDirs)
        self.remove_attachment_pb = QtWidgets.QPushButton(self.groupBox_2)
        self.remove_attachment_pb.setMinimumSize(QtCore.QSize(40, 23))
        self.remove_attachment_pb.setMaximumSize(QtCore.QSize(40, 23))
        self.remove_attachment_pb.setObjectName("pushButton_list_remove")
        self.horizontalLayout_3.addWidget(self.remove_attachment_pb)
        self.refresh_attachment_pb = QtWidgets.QPushButton(self.groupBox_2)
        self.refresh_attachment_pb.setMinimumSize(QtCore.QSize(40, 23))
        self.refresh_attachment_pb.setMaximumSize(QtCore.QSize(40, 23))
        self.refresh_attachment_pb.setObjectName("pushButton_update_atta")
        self.horizontalLayout_3.addWidget(self.refresh_attachment_pb)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_13 = QtWidgets.QLabel(self.widget_file)
        self.label_13.setMinimumSize(QtCore.QSize(60, 0))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_10.addWidget(self.label_13)
        self.submit_path_le = QtWidgets.QLineEdit(self.widget_file)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit_path_le.sizePolicy().hasHeightForWidth())
        self.submit_path_le.setSizePolicy(sizePolicy)
        self.submit_path_le.setMinimumSize(QtCore.QSize(110, 23))
        self.submit_path_le.setReadOnly(True)
        self.submit_path_le.setObjectName("lineEdit_sumbitpath")
        self.horizontalLayout_10.addWidget(self.submit_path_le)
        self.pushButton_sumbitpath = QtWidgets.QPushButton(self.widget_file)
        self.pushButton_sumbitpath.setMinimumSize(QtCore.QSize(40, 23))
        self.pushButton_sumbitpath.setMaximumSize(QtCore.QSize(40, 23))
        self.pushButton_sumbitpath.setObjectName("pushButton_sumbitpath")
        self.horizontalLayout_10.addWidget(self.pushButton_sumbitpath)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progress_bar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progress_bar.hide()
        self.progress_bar.setMaximumSize(QtCore.QSize(120, 16777215))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progress_bar)
        self.progress_lb = QtWidgets.QLabel(self.verticalLayoutWidget, text='test')
        self.progress_lb.hide()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_lb.sizePolicy().hasHeightForWidth())
        self.progress_lb.setSizePolicy(sizePolicy)
        self.progress_lb.setObjectName("label_stats")
        self.horizontalLayout_2.addWidget(self.progress_lb)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.log_text_edit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.log_text_edit.setObjectName("textEdit_log")
        self.verticalLayout_3.addWidget(self.log_text_edit)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL("clicked()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.check_pb.setText(QtWidgets.QApplication.translate("Dialog", "检查", None, -1))
        self.submit_pb.setText(QtWidgets.QApplication.translate("Dialog", "提交", None, -1))
        self.pushButton_close.setText(QtWidgets.QApplication.translate("Dialog", "关闭", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "新版本号：", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "任务名称：", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Dialog", "项目名称：", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Dialog", "提交用户：", None, -1))
        self.user_lb.setText(QtWidgets.QApplication.translate("Dialog", "TextLabel", None, -1))
        self.get_task_pb.setText(QtWidgets.QApplication.translate("Dialog", "<<获取任务", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("Dialog", "工程文件：", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", "路径：", None, -1))
        self.input_file_path_pb.setText(QtWidgets.QApplication.translate("Dialog", "<<", None, -1))
        # self.checkBox_outAD.setText(QtWidgets.QApplication.translate("Dialog", "输出 Assembly 文件(内部测试，道具场景专用)", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "预览文件：", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "路径：", None, -1))
        self.select_preview_file_pb.setText(QtWidgets.QApplication.translate("Dialog", "选择", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "创建：", None, -1))
        self.playblast_img_pb.setText(QtWidgets.QApplication.translate("Dialog", "抓图", None, -1))
        self.playblast_prev_pb.setText(QtWidgets.QApplication.translate("Dialog", "拍屏", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "描    述:", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Dialog", "附件目录：", None, -1))
        self.attachment_tw.headerItem().setText(0, u'附件文件列表（仅支持文件夹）')
        # self.attachment_tw.headerItem().setText(1, QtWidgets.QApplication.translate("Dialog", "类型", None, -1))
        # self.attachment_tw.headerItem().setText(2, QtWidgets.QApplication.translate("Dialog", "上传文件列表", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("Dialog", "自动识别附件目录名：", None, -1))
        self.remove_attachment_pb.setText(QtWidgets.QApplication.translate("Dialog", "移除", None, -1))
        self.refresh_attachment_pb.setText(QtWidgets.QApplication.translate("Dialog", "刷新", None, -1))
        self.label_13.setText(QtWidgets.QApplication.translate("Dialog", "存放路径:", None, -1))
        self.pushButton_sumbitpath.setText(QtWidgets.QApplication.translate("Dialog", "查看", None, -1))




if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = UiDialog()
    dialog.setupUi(dialog)
    dialog.show()
    app.exec_()