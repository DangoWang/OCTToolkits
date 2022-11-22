#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/6/17

import os
from maya import cmds
from DCC_TOOLS.common.dcc_utils import *
import logging
try:
    from PySide2 import QtWidgets, QtCore

except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path+'\\ui.ui')


class NurbsShapeTransfer(base_class, form_class):

    def __init__(self, parent=getMayaWindow()):
        super(NurbsShapeTransfer, self).__init__(parent=parent)
        self.setupUi(self)
        self.load_source_pb.clicked.connect(lambda: self.load_selected(self.source_tw))
        self.load_target_pb.clicked.connect(lambda: self.load_selected(self.target_tw))
        self.source_clear_pb.clicked.connect(lambda: self.clear_items(self.source_tw))
        self.target_clear_pb.clicked.connect(lambda: self.clear_items(self.target_tw))

    @staticmethod
    def get_selected():
        return cmds.ls(sl=1) if cmds.ls(sl=1) else []

    @staticmethod
    def add_item(table_widget, label):
        contents = [table_widget.item(i, 0).text() for i in range(table_widget.rowCount())]
        print contents
        if label in contents:
            return 
        row_count = table_widget.rowCount()
        table_widget.setRowCount(row_count + 1)
        new_item = QtWidgets.QTableWidgetItem(label)
        table_widget.setItem(row_count, 0, new_item)
        return True

    @staticmethod
    def clear_items(item):
        item.setRowCount(0)
        item.clearContents()

    def load_selected(self, tw):
        map(self.add_item, [tw]*len(self.get_selected()), self.get_selected())

    @property
    def world_transfer(self):
        return self.world_rb.isChecked() if self.world_rb.isChecked() else False

    @staticmethod
    @undoable
    def transfer_nurbs(source_obj, target_obj, world=False):
        import pymel.core as pm
        if world:
            s_cvs = pm.PyNode(source_obj).getCVs(space='world')
            pm.PyNode(target_obj).setCVs(s_cvs, space='world')
        else:
            s_cvs = pm.PyNode(source_obj).getCVs()
            pm.PyNode(target_obj).setCVs(s_cvs)

    def transfer_nurbs_batch_doit(self, sources, targets, mod):
        if len(sources) != len(targets):
            logging.error(u'左右两边物体数量不一致！！')
            return False
        map(self.transfer_nurbs, sources, targets, [mod]*len(sources))

    @QtCore.Slot(name='on_doit_all_pb_clicked')
    def on_doit_all_pb_clicked(self):
        sources = [self.source_tw.item(i, 0).text() for i in range(self.source_tw.rowCount())]
        targets = [self.target_tw.item(j, 0).text() for j in range(self.target_tw.rowCount())]
        self.transfer_nurbs_batch_doit(sources, targets, self.world_transfer)

    @QtCore.Slot(name='on_doit_sel_pb_clicked')
    def on_doit_sel_pb_clicked(self):
        sources = [self.source_tw.item(index.row(), 0).text() for index in self.source_tw.selectedIndexes()]
        targets = [self.target_tw.item(index.row(), 0).text() for index in self.target_tw.selectedIndexes()]
        self.transfer_nurbs_batch_doit(sources, targets, self.world_transfer)


if __name__ == '__main__':
    pass


