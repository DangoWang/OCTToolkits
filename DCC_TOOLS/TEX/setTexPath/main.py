#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/6/20

import os
from maya import cmds
import maya.mel as mel
from DCC_TOOLS.common.dcc_utils import *
import logging
from utils import shotgun_operations
import pymel.core as pm

try:
    from PySide2 import QtWidgets, QtCore

except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path+'\\ui.ui')

server_path = 'I:/'
local_path = 'E:/Projects/'


def change_tex_path(dest_path):
    all_files_nodes = cmds.ls(type=['file'])
    for each in all_files_nodes:
        mel.eval('setAttr -l false { "%s.ftn" };' % each)
        old_path = cmds.getAttr(each + '.fileTextureName')
        path_temp = old_path.split('sourceimages')[-1]
        new_path = dest_path + '/sourceimages' + path_temp
        mel.eval("setAttr -type \"string\" {}.fileTextureName \"\";".format(each))
        mel.eval("setAttr -type \"string\" {}.fileTextureName \"{}\";".format(each, new_path))
        mel.eval('setAttr -l true { "%s.ftn" };' % each)
    pass


class SetTexPath(base_class, form_class):

    def __init__(self, parent=getMayaWindow()):
        super(SetTexPath, self).__init__(parent=parent)
        self.setupUi(self)
        # self.mod_rb.toggled.connect(self.set_img_path)
        # self.rig_rb.toggled.connect(self.set_img_path)
        # self.tex_rb.toggled.connect(self.set_img_path)
        # self.server_rb.toggled.connect(self.set_img_path)
        # self.local_rb.toggled.connect(self.set_img_path)
        self.comboBox.currentIndexChanged.connect(self.set_img_path)
        # self.cfx_fur_rb.toggled.connect(self.set_img_path)
        self.asset_name_le.editingFinished.connect(self.set_img_path)
        self.asset_name_le.setText(self.get_asset_name())
        self.asset_name_le.setEnabled(0)
        self.task_names_rb = []
        self.set_img_path()

    @staticmethod
    def get_asset_name():
        default_assemblies = ['persp', 'top', 'front', 'side']
        asset_name = [a for a in cmds.ls(assemblies=True) if a not in default_assemblies]
        return asset_name[0] if asset_name else ''

    def process(self):
        for each in self.task_names_rb:
            if each.isChecked():
                return each.text()

    @QtCore.Slot()
    def on_input_asset_name_pb_clicked(self):
        if not cmds.ls(sl=1):
            logging.error(u'请先选择物体！')
            return
        asset = cmds.ls(sl=1)[0]
        self.asset_name_le.setText(asset)
        self.set_img_path()

    def set_img_path(self):
        asset_name = self.asset_name_le.text()
        #  检查下资产是否存在
        name = shotgun_operations.find_one_shotgun('Asset', [['project', 'name_is', 'DSF'], ['code', 'is', asset_name]],
                                                   ['sg_asset_type']
                                                   )
        if not name:
            self.img_path_lb.setText(u'该资产不存在！请检查资产名...')
            return False
        tasks = shotgun_operations.find_shotgun('Task', [['project', 'name_is', 'DSF'], ['entity', 'name_is', asset_name]],
                                                   ['content']
                                                   )
        task_names = [each_t['content'] for each_t in tasks]
        if not self.task_names_rb:
            for each_task_name in task_names:
                rb = QtWidgets.QRadioButton()
                rb.setText(each_task_name)
                rb.toggled.connect(self.set_img_path)
                self.horizontalLayout_4.addWidget(rb)
                self.task_names_rb.append(rb)
        dest_path = server_path if not self.comboBox.currentIndex() else local_path
        if self.process():
            path = '/'.join(['dsf', 'Asset', name['sg_asset_type'], asset_name, self.process()])
            # path = path_temp.rstrip(path_temp.split('/')[-1]) + self.process
            repath_dest = dest_path + path
            self.img_path_lb.setText(repath_dest)
            return repath_dest

    @QtCore.Slot()
    def on_change_doit_pb_clicked(self):
        dest_path = self.img_path_lb.text()
        if ":" not in dest_path:
            logging.error(u'请输入正确的资产名！')
            return False
        change_tex_path(dest_path)
        all_files_nodes = cmds.ls(type=['file'])
        for each in all_files_nodes:
            old_path = cmds.getAttr(each + '.fileTextureName')
            if server_path not in old_path:
                self.img_path_lb.setText(u'失败！')
                logging.error(u'由于maya原因重定向失败！请重开maya后打开文件重试！')
                return
        self.img_path_lb.setText(u'重定向成功！')




