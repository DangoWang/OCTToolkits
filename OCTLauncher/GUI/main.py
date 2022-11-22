# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dango_repo\OctLauncher\GUI\main.ui'
#
# Created: Tue Sep 24 14:04:37 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_MagisianDesktop(object):
    def setupUi(self, MagisianDesktop):
        MagisianDesktop.setObjectName("MagisianDesktop")
        MagisianDesktop.resize(350, 657)
        MagisianDesktop.setMinimumSize(QtCore.QSize(350, 500))
        MagisianDesktop.setMaximumSize(QtCore.QSize(350, 16777215))
        MagisianDesktop.setCursor(QtCore.Qt.ArrowCursor)
        MagisianDesktop.setWindowOpacity(1.0)
        MagisianDesktop.setStyleSheet("font-family:\"Leelawadee UI\";\n"
                                      "font-size: 12px;\n"
                                      "background: url(:/icons/bg.png) no-repeat;\n"
                                      "\n"
                                      "")
        MagisianDesktop.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout_2 = QtGui.QGridLayout(MagisianDesktop)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 15)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(96)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.title_bar_grp = QtGui.QGroupBox(MagisianDesktop)
        self.title_bar_grp.setMinimumSize(QtCore.QSize(0, 26))
        self.title_bar_grp.setMaximumSize(QtCore.QSize(16777215, 26))
        self.title_bar_grp.setStyleSheet("border:none;\n"
                                         "padding:3px;\n"
                                         "margin:0;\n"
                                         "background-image: url();")
        self.title_bar_grp.setObjectName("title_bar_grp")
        self.titile_bar_layout = QtGui.QHBoxLayout(self.title_bar_grp)
        self.titile_bar_layout.setSpacing(0)
        self.titile_bar_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.titile_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.titile_bar_layout.setObjectName("titile_bar_layout")
        self.oct_logo_btn = QtGui.QToolButton(self.title_bar_grp)
        self.oct_logo_btn.setMinimumSize(QtCore.QSize(25, 25))
        self.oct_logo_btn.setMaximumSize(QtCore.QSize(25, 25))
        self.oct_logo_btn.setStyleSheet("QToolButton#oct_logo_btn\n"
                                        "{\n"
                                        "    image: url(:/icons/oct.ico);\n"
                                        "    height: 20px;\n"
                                        "    width: 20px;\n"
                                        "    border: none;\n"
                                        "}\n"
                                        "QToolButton#oct_logo_btn::hover\n"
                                        "{\n"
                                        "    image: url(:/icons/oct.ico);\n"
                                        "    background-color: rgb(240, 255, 254);\n"
                                        "}")
        self.oct_logo_btn.setText("")
        self.oct_logo_btn.setIconSize(QtCore.QSize(16, 16))
        self.oct_logo_btn.setObjectName("oct_logo_btn")
        self.titile_bar_layout.addWidget(self.oct_logo_btn)
        self.title_label = QtGui.QLabel(self.title_bar_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.title_label.setObjectName("title_label")
        self.titile_bar_layout.addWidget(self.title_label)
        self.close_btn = QtGui.QToolButton(self.title_bar_grp)
        self.close_btn.setMinimumSize(QtCore.QSize(25, 25))
        self.close_btn.setMaximumSize(QtCore.QSize(25, 25))
        self.close_btn.setStyleSheet("QToolButton#close_btn\n"
                                     "{\n"
                                     "    image: url(:/icons/close.png);\n"
                                     "    height: 20px;\n"
                                     "    width: 20px;\n"
                                     "    border: none;\n"
                                     "}\n"
                                     "QToolButton#close_btn::hover\n"
                                     "{\n"
                                     "    image: url(:/icons/close.png);\n"
                                     "    background-color: rgb(156, 199, 255);\n"
                                     "}")
        self.close_btn.setText("")
        self.close_btn.setObjectName("close_btn")
        self.titile_bar_layout.addWidget(self.close_btn)
        self.gridLayout_2.addWidget(self.title_bar_grp, 0, 0, 1, 1)
        self.main_widget = QtGui.QWidget(MagisianDesktop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMaximumSize(QtCore.QSize(999, 999))
        self.main_widget.setStyleSheet("background-image: url();")
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.main_widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.toolbar_grp = QtGui.QGroupBox(self.main_widget)
        self.toolbar_grp.setMinimumSize(QtCore.QSize(0, 30))
        self.toolbar_grp.setMaximumSize(QtCore.QSize(16777215, 35))
        self.toolbar_grp.setStyleSheet("background-color: rgb(125, 103, 52);\n"
                                       "padding:0px;\n"
                                       "border-top-left-radius:0px;\n"
                                       "border-top-right-radius:0px;\n"
                                       "border-bottom-right-radius:2px;\n"
                                       "border-bottom-left-radius:2px;")
        self.toolbar_grp.setTitle("")
        self.toolbar_grp.setObjectName("toolbar_grp")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.toolbar_grp)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.menu_layout_2 = QtGui.QHBoxLayout()
        self.menu_layout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.menu_layout_2.setObjectName("menu_layout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.toolbar_grp)
        self.label.setStyleSheet("margin-right:8px;\n"
                                 "color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.toolbar_grp)
        self.comboBox.setStyleSheet("QComboBox{\n"
                                    "    color: #fff;\n"
                                    "}\n"
                                    "QComboBox::drop-down {\n"
                                    "    subcontrol-origin: padding;\n"
                                    "    subcontrol-position: top right;\n"
                                    "    width: 20px;\n"
                                    "    border-left-width: 0px;\n"
                                    "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                    "    border-bottom-right-radius: 3px;\n"
                                    "}\n"
                                    "QAbstractItemView{\n"
                                    "    color: #fff;\n"
                                    "    border: none;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar:vertical\n"
                                    "{\n"
                                    "    width:8px;\n"
                                    "    background:rgba(0,0,0,0%);\n"
                                    "    margin:0px,0px,0px,0px;\n"
                                    "    padding-top:9px;  \n"
                                    "    padding-bottom:9px;\n"
                                    "}\n"
                                    "QScrollBar::handle:vertical\n"
                                    "{\n"
                                    "    width:8px;\n"
                                    "    background:rgba(0,0,0,25%);\n"
                                    "    border-radius:4px;  \n"
                                    "    min-height:20;\n"
                                    "}\n"
                                    "QScrollBar::handle:vertical:hover\n"
                                    "{\n"
                                    "    width:8px;\n"
                                    "    background:rgba(0,0,0,50%);   \n"
                                    "    border-radius:4px;\n"
                                    "    min-height:20;\n"
                                    "}\n"
                                    "QScrollBar::add-line:vertical   \n"
                                    "{\n"
                                    "    height:9px;width:8px;\n"
                                    "    border-image:url(:/images/a/3.png);\n"
                                    "    subcontrol-position:bottom;\n"
                                    "}\n"
                                    "QScrollBar::sub-line:vertical \n"
                                    "{\n"
                                    "    height:9px;width:8px;\n"
                                    "    border-image:url(:/images/a/1.png);\n"
                                    "    subcontrol-position:top;\n"
                                    "}\n"
                                    "QScrollBar::add-line:vertical:hover  \n"
                                    "{\n"
                                    "    height:9px;width:8px;\n"
                                    "    border-image:url(:/images/a/4.png);\n"
                                    "    subcontrol-position:bottom;\n"
                                    "}\n"
                                    "QScrollBar::sub-line:vertical:hover\n"
                                    "{\n"
                                    "    height:9px;width:8px;\n"
                                    "    border-image:url(:/images/a/2.png);\n"
                                    "    subcontrol-position:top;\n"
                                    "}\n"
                                    "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical \n"
                                    "{\n"
                                    "    background:rgba(0,0,0,10%);\n"
                                    "    border-radius:4px;\n"
                                    "}\n"
                                    "")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.toolbar_grp)
        self.label_2.setStyleSheet("margin-right:8px;\n"
                                   "color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.user = QtGui.QLineEdit(self.toolbar_grp)
        self.user.setReadOnly(True)
        self.user.setObjectName("user")
        self.horizontalLayout_3.addWidget(self.user)
        self.menu_layout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.menu_layout_2)
        self.verticalLayout_4.addWidget(self.toolbar_grp)
        self.work_area_grp = QtGui.QGroupBox(self.main_widget)
        self.work_area_grp.setStyleSheet("background-color: #ffffff;")
        self.work_area_grp.setTitle("")
        self.work_area_grp.setFlat(False)
        self.work_area_grp.setObjectName("work_area_grp")
        self.gridLayout = QtGui.QGridLayout(self.work_area_grp)
        self.gridLayout.setObjectName("gridLayout")
        self.DCC_btn_grp = QtGui.QGroupBox(self.work_area_grp)
        self.DCC_btn_grp.setMinimumSize(QtCore.QSize(300, 200))
        self.DCC_btn_grp.setMaximumSize(QtCore.QSize(16777215, 300))
        self.DCC_btn_grp.setObjectName("DCC_btn_grp")
        self.gridLayout.addWidget(self.DCC_btn_grp, 0, 0, 1, 1)
        self.pipe_btn_grp = QtGui.QGroupBox(self.work_area_grp)
        self.pipe_btn_grp.setMinimumSize(QtCore.QSize(300, 100))
        self.pipe_btn_grp.setMaximumSize(QtCore.QSize(16777215, 150))
        self.pipe_btn_grp.setObjectName("pipe_btn_grp")
        self.gridLayout.addWidget(self.pipe_btn_grp, 1, 0, 1, 1)
        self.other_btn_grp = QtGui.QGroupBox(self.work_area_grp)
        self.other_btn_grp.setMinimumSize(QtCore.QSize(0, 150))
        self.other_btn_grp.setMaximumSize(QtCore.QSize(16777215, 200))
        self.other_btn_grp.setObjectName("other_btn_grp")
        self.gridLayout.addWidget(self.other_btn_grp, 2, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.work_area_grp)
        self.gridLayout_2.addWidget(self.main_widget, 1, 0, 1, 1)

        self.retranslateUi(MagisianDesktop)
        QtCore.QMetaObject.connectSlotsByName(MagisianDesktop)
        MagisianDesktop.setTabOrder(self.oct_logo_btn, self.close_btn)

    def retranslateUi(self, MagisianDesktop):
        MagisianDesktop.setWindowTitle(
            QtGui.QApplication.translate("MagisianDesktop", "oct_launcher v1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("MagisianDesktop", "   OctLauncher  v2.1", None,
                                                              QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("MagisianDesktop", "选择项目: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("MagisianDesktop", "当前用户：", None, QtGui.QApplication.UnicodeUTF8))
        self.DCC_btn_grp.setTitle(
            QtGui.QApplication.translate("MagisianDesktop", "制作软件", None, QtGui.QApplication.UnicodeUTF8))
        self.pipe_btn_grp.setTitle(
            QtGui.QApplication.translate("MagisianDesktop", "流程软件", None, QtGui.QApplication.UnicodeUTF8))
        self.other_btn_grp.setTitle(
            QtGui.QApplication.translate("MagisianDesktop", "其他", None, QtGui.QApplication.UnicodeUTF8))


from qrc import *
