#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/27

import os
import sys

from maya import mel

from DCC_TOOLS.common.dcc_utils import *
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
import inspect
import mat_check_list
reload(mat_check_list)


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


def check_func(func_name, label, fix, task_dict):
    result = methodcaller(func_name, fix, task_dict)(mat_check_list)
    if result:
        label.setStyleSheet('background-color: rgb(0, 255, 8);')
    else:
        label.setStyleSheet('background-color: rgb(255, 0, 4);')


def raise_confirm_dialog(text):
    confirm_dialog = QtWidgets.QMessageBox()
    if len(text) > 500:
        text = text[:500] + "..."
    confirm_dialog.setText(text)
    confirm_dialog.setWindowTitle(u"提示")
    confirm_dialog.addButton(u"Yes", QtWidgets.QMessageBox.AcceptRole)  # role 0
    confirm_dialog.addButton(u"No", QtWidgets.QMessageBox.RejectRole)  # role 1
    return confirm_dialog.exec_()


def resource_inpath():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))
    return ""


file_path = os.path.realpath(resource_inpath())
form_class, base_class = loadUiType(file_path+'\\check_material.ui')


class CheckMaterial(base_class, form_class):
    result_signal = QtCore.Signal(int)

    def __init__(self, task_dict=None, parent=None):
        super(CheckMaterial, self).__init__(parent=getMayaWindow())
        self.setupUi(self)
        self.task_dict = task_dict
        self.check_doit.clicked.connect(self.check_mat_doit)
        self.connect_slot()

    def closeEvent(self, event):
        res = raise_confirm_dialog(u'确定已经完成检查了吗？')
        if res:
            self.result_signal.emit(0)
            event.accept()
        else:
            self.result_signal.emit(1)
            event.accept()

    def get_all_checking_items(self):
        all_children = self.checking_items_widget.children()
        all_items = [each for each in all_children if "_cb" in each.objectName()]
        return all_items

    def get_selected_checking_items(self):
        all_items = self.get_all_checking_items()
        checking_items = [each for each in all_items if each.isChecked()]
        return checking_items

    def check_mat_doit(self):
        all_checking_checkboxes = self.get_selected_checking_items()
        gMainProgressBar = mel.eval('$gMainProgressBar=$gMainProgressBar')
        mc.progressBar(gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status=u"正在检查...",
                         maxValue=100)
        for each in all_checking_checkboxes:
            func_name = each.objectName().replace('_cb', '_func')
            label = self.findChild(QtWidgets.QLabel, each.objectName().replace("_cb", "_lb"))
            check_func(func_name, label, False, self.task_dict)
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True, )

    def connect_slot(self):
        for each in self.get_all_checking_items():
            pb = self.findChild(QtWidgets.QPushButton, each.objectName().replace("_cb", "_pb"))
            func_name = each.objectName().replace('_cb', '_func')
            label = self.findChild(QtWidgets.QLabel, each.objectName().replace("_cb", "_lb"))
            pb.clicked.connect(lambda func=func_name, lab=label: check_func(func, lab, True, self.task_dict))


if __name__ == '__main__':
    window1 = CheckMaterial()
    window1.show()
