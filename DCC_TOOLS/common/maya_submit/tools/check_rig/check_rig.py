#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/27

import os
import sys
import logging
from DCC_TOOLS.common.dcc_utils import *
from PySide2.QtCore import Slot
from operator import methodcaller
try:
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import QWidget
    import PySide.QtGui as QtWidgets
    from shiboken import wrapInstance
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMayaUI as omui
import inspect
import rigging_check_list
reload(rigging_check_list)


def undoable(function):
    # A decorator that will make commands undoable in maya
    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print sys.exc_info()[1]

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn
    return decoratorCode


def raise_confirm_dialog(text):
    confirm_dialog = QtWidgets.QMessageBox()
    if len(text) > 500:
        text = text[:500] + "..."
    confirm_dialog.setText(text)
    confirm_dialog.setWindowTitle(u"提示")
    confirm_dialog.addButton(u"自动处理", QtWidgets.QMessageBox.AcceptRole)  # role 0
    confirm_dialog.addButton(u"场景查看", QtWidgets.QMessageBox.RejectRole)  # role 1
    confirm_dialog.addButton(u"忽略", QtWidgets.QMessageBox.DestructiveRole)  # role 2
    return confirm_dialog.exec_()


def raise_warning_dialog(parent, text):
    return QtWidgets.QMessageBox().warning(parent, u'warning', text, QtWidgets.QMessageBox.Yes)


def resource_inpath():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))
    return ""


file_path = os.path.realpath(resource_inpath())
form_class, base_class = loadUiType(file_path+'\\check_rigging.ui')


class CheckRigging(base_class, form_class):
    result_signal = QtCore.Signal(int)

    def __init__(self, task_dict=None, parent=None):
        super(CheckRigging, self).__init__(parent=getMayaWindow())
        self.setupUi(self)

        self.task_dict = task_dict
        print self.task_dict
        self.select_all.stateChanged.connect(self.check_all_items)
        self.check_doit.clicked.connect(self.check_rigging_doit)

    def check_all_items(self):
        all_items = self.get_all_checking_items()
        for item in all_items:
            item.setChecked(1) if self.select_all.isChecked() else item.setChecked(0)
        return

    def get_all_checking_items(self):
        all_children = self.children()
        all_items = [each for each in all_children if "_cb" in each.objectName()]
        return all_items

    def get_selected_checking_items(self):
        all_items = self.get_all_checking_items()
        checking_items = [each for each in all_items if each.isChecked()]
        return checking_items

    def check_rigging_doit(self):
        all_checking_checkboxes = self.get_all_checking_items()
        for each_cb in all_checking_checkboxes:
            each_label = self.findChild(QtWidgets.QLabel, each_cb.objectName().replace("_cb", "_lb"))
            if each_cb.isChecked():
                check_func_name = each_cb.objectName().replace("_cb", "_func")
                fix_func_name = check_func_name.replace("check", "fix")
                check_result = methodcaller(check_func_name, self.task_dict)(rigging_check_list)
                if check_result:
                    each_label.setStyleSheet('background-color: rgb(255, 0, 4);')
                    check_answer = raise_confirm_dialog(check_result)
                    if check_answer == 0:
                        fix_result = methodcaller(fix_func_name, self.task_dict)(rigging_check_list)
                        if fix_result:
                            raise_warning_dialog(self, fix_result)
                            return False
                        each_label.setStyleSheet('background-color: rgb(0, 255, 8);')
                    elif check_answer == 1:
                        return False
                    else:
                        continue
                else:
                    each_label.setStyleSheet('background-color: rgb(0, 255, 8);')
        if_checking_dialog = QtWidgets.QMessageBox()
        if_checking_dialog.setText(u'确定已经完成所有的检测项吗？')
        if_checking_dialog.setWindowTitle(u"提示")
        if_checking_dialog.addButton(u"是的，可以确认提交了", QtWidgets.QMessageBox.AcceptRole)  # role 0
        if_checking_dialog.addButton(u"等等，我再看看", QtWidgets.QMessageBox.RejectRole)  # role 1
        if_checking_finished = if_checking_dialog.exec_()
        if not if_checking_finished:
            self.result_signal.emit(1)
            return True
        else:
            self.result_signal.emit(0)
            return False


if __name__ == '__main__':
    import sys
    sys.path.append(r'D:\dango_repo\check_rigging')
    import checking_rigging
    reload(checking_rigging)
    window1 = checking_rigging.CheckRigging()
    window1.show()
