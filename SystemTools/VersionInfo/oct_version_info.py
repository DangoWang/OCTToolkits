#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
import os
import json
import sys
# sys.path.append(os.environ['oct_toolkits_path'])
# sys.path.append(os.environ['oct_tooltikts_thirdparty'])
# sys.path.append(os.environ['utils_path'])
import datetime
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.qt import *
import utils.shotgun_operations as sg
from PySide import QtCore
from PySide import QtGui


class OCTVersionInfoClass(QMainWindow):
    def __init__(self,version, parent=None):
        super(OCTVersionInfoClass, self).__init__(parent)
        self.version = version
        print self.version
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(566, 366)
        self.setWindowTitle(u'Version List')
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        main_lay = QVBoxLayout(self.centralwidget)

        # self.horizontalLayout_title = QHBoxLayout()
        # self.label_title = QLabel()
        # self.label_title.setText(u"")
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        # self.label_title.setSizePolicy(sizePolicy)
        # self.horizontalLayout_title.addWidget(self.label_title)
        #
        # self.pushButton_min = MToolButton().svg('down_line_dark.svg').icon_only()
        # self.pushButton_min.clicked.connect(self.showMinimized)
        # self.horizontalLayout_title.addWidget(self.pushButton_min)
        #
        # self.toolButton_close = MToolButton().svg('close_line.svg').icon_only()
        # self.horizontalLayout_title.addWidget(self.toolButton_close)
        # self.toolButton_close.clicked.connect(self.close)
        #
        # main_lay.addLayout(self.horizontalLayout_title)

        self.version_text = MTextEdit()
        main_lay.addWidget(self.version_text)

        self.pushButton_save = MPushButton()
        self.pushButton_save.setText(u"请联系管理员更新版本，确认")
        self.pushButton_save.clicked.connect(self.close)
        main_lay.addWidget(self.pushButton_save)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.find_version_list()

    def find_version_list(self):
        ver_filters = []
        ver_fields = ["code", "description"]
        ver_sg = sg.find_shotgun("CustomEntity05", ver_filters, ver_fields)
        for ver in ver_sg:
            if ver["code"] > self.version:
                self.version_text.append(ver["code"])
                self.version_text.append(u"    {}".format(ver["description"]))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


# def main(version="2019-11-27", parent=None):
def main(version, parent=None):
    # from dayu_widgets import dayu_theme
    # from dayu_widgets.qt import QApplication
    # app = QApplication(sys.argv)
    version_win = OCTVersionInfoClass(version, parent)
    return version_win
    # dayu_theme.apply(version_win)
    # WorkLogWin.show()
    # sys.exit(app.exec_())

if __name__ == '__main__':
    main()
