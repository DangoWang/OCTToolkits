# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as OpenMayaUI
import shiboken2
import maya.cmds as cmds
import register
reload(register)
import check_item
reload(check_item)
from functools import partial

def get_maya_window(*argv):
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)

_win_name = "CheckWinUI"

class CheckWinClass(QtWidgets.QMainWindow):
    def __init__(self, step, parent=get_maya_window()):
        super(CheckWinClass, self).__init__(parent)
        self.step = step
        self.delete_old_ui()
        self.resize(366, 566)
        self.setObjectName(_win_name)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.groupBox_up = QtWidgets.QGroupBox(self.splitter)
        self.gridLayout_up = QtWidgets.QGridLayout(self.groupBox_up)
        self.gridLayout_up.setSpacing(2)
        self.gridLayout_up.setContentsMargins(2, 2, 2, 2)

        self.groupBox_select = QtWidgets.QGroupBox(self.groupBox_up)
        # self.groupBox_select.setHidden(1)
        self.gridLayout_up.addWidget(self.groupBox_select, 0, 0, 1, 1)
        self.gridLayout_select = QtWidgets.QGridLayout(self.groupBox_select)
        self.gridLayout_select.setSpacing(2)
        self.gridLayout_select.setContentsMargins(0, 0, 0, 0)
        self.pushButton_all = QtWidgets.QPushButton(self.groupBox_select)
        self.pushButton_all.setText(u"全选")
        self.pushButton_all.clicked.connect(partial(self.select_item, 1))
        self.gridLayout_select.addWidget(self.pushButton_all, 0, 0, 1, 1)
        self.pushButton_none = QtWidgets.QPushButton(self.groupBox_select)
        self.pushButton_none.setText(u"取消全选")
        self.pushButton_none.clicked.connect(partial(self.select_item, 0))
        self.gridLayout_select.addWidget(self.pushButton_none, 0, 1, 1, 1)
        self.pushButton_error = QtWidgets.QPushButton(self.groupBox_select)
        self.pushButton_error.setHidden(1)
        self.pushButton_error.setText("Error")
        self.pushButton_error.clicked.connect(partial(self.select_item, 3))
        self.gridLayout_select.addWidget(self.pushButton_error, 0, 2, 1, 1)
        self.pushButton_invert = QtWidgets.QPushButton(self.groupBox_select)
        self.pushButton_invert.setHidden(1)
        self.pushButton_invert.setText("Invert")
        self.pushButton_invert.clicked.connect(partial(self.select_item, 2))
        self.gridLayout_select.addWidget(self.pushButton_invert, 0, 3, 1, 1)

        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_up)
        self.gridLayout_up.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.pushButton_doit = QtWidgets.QPushButton(self.groupBox_up)
        self.pushButton_doit.setText("DoIt")
        self.pushButton_doit.clicked.connect(self.startCheck)
        self.gridLayout_up.addWidget(self.pushButton_doit, 2, 0, 1, 1)

        self.groupBox_result = QtWidgets.QGroupBox(self.splitter)
        self.gridLayout_result = QtWidgets.QGridLayout(self.groupBox_result)
        self.gridLayout_result.setSpacing(2)
        self.gridLayout_result.setContentsMargins(2, 2, 2, 2)
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_result)
        self.gridLayout_result.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.create_check_tab()
        self.groupBox_result.setHidden(1)

    def delete_old_ui(self):
        maya_window = get_maya_window()
        old_win = maya_window.findChild(QtWidgets.QMainWindow, _win_name)
        if old_win:
            cmds.deleteUI(old_win.objectName(), window=1)

    def select_item(self, mod, *args):
        tab = self.tabWidget.tabText(self.tabWidget.currentIndex())
        if mod == 0:
            for item in self.tab_item_dir[tab]:
                item.checkBox.setChecked(0)
        elif mod == 1:
            for item in self.tab_item_dir[tab]:
                item.checkBox.setChecked(1)
        elif mod == 2:
            for item in self.tab_item_dir[tab]:
                item.checkBox.setChecked(1-item.checkBox.isChecked())
        elif mod == 3:
            for item in self.tab_item_dir[tab]:
                if item.error_list:
                    item.checkBox.setChecked(1)
                else:
                    item.checkBox.setChecked(0)

    def deal_cfg(self):
        cfg_temp = register.check_cfg
        print "cfg_temp", cfg_temp
        cfg_temp[self.step].extend(cfg_temp['common'])
        # print cfg_new
        return {self.step: cfg_temp[self.step]}

    def create_check_tab(self):
        check_list = self.deal_cfg()
        self.tab_proc_dir = {}
        self.tab_item_dir = {}
        for tab, items in check_list.iteritems():
            self.tab_proc_dir[tab] = []
            self.tab_item_dir[tab] = []
            tab_widget = QtWidgets.QWidget()
            self.tabWidget.addTab(tab_widget, tab)
            gridLayout = QtWidgets.QGridLayout(tab_widget)
            scrollArea = QtWidgets.QScrollArea(tab_widget)
            scrollArea.setWidgetResizable(True)
            gridLayout.addWidget(scrollArea)
            scrollAreaWidgetContents = QtWidgets.QWidget()
            scrollArea.setWidget(scrollAreaWidgetContents)
            item_list = QtWidgets.QGridLayout(scrollAreaWidgetContents)
            item_list.setSpacing(2)
            item_list.setContentsMargins(0, 0, 0, 0)
            for num, item in enumerate(items):
                item_new = check_item.CheckItemClass()
                item_new.pushButton_fix.clicked.connect(partial(item["value"], item_new, 1))
                item_new.checkBox.setText(item["label"])
                item_list.addWidget(item_new, num, 0, 1, 1)
                self.tab_item_dir[tab].append(item_new)
                item_new.fix = item["fix"]
                self.tab_proc_dir[tab].append(partial(item["value"], item_new))
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            item_list.addItem(spacerItem, num+1, 0, 1, 1)

    def startCheck(self):
        tab = self.tabWidget.tabText(self.tabWidget.currentIndex())
        self.textBrowser.clear()
        for order in self.tab_proc_dir[tab]:
            order.func(order.args[0])

def main():
    win = CheckWinClass("mod")
    win.show()