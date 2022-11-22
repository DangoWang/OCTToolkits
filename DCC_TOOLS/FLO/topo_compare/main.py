#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wangdonghao
# time:2019/6/6

import os
import sys
import json
from maya import cmds as mc
import pymel.core as pm
import searchDB
from check_cfg import *
from dango_utils import *
try:
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtWidgets, QtCore, QtGui
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import QWidget
    import PySide.QtGui as QtWidgets
    from shiboken import wrapInstance

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path+'\\ui.ui')
dsf_db = searchDB.taskInfo('dsf')


def get_assets(group=['CHAR', 'PROP', 'ENV'], classify=['TEX', 'RIG', 'MOD']):
    existed_grp = [each for each in group if mc.objExists(each)]
    all_refs = flat([mc.listRelatives(ref, c=1) for ref in existed_grp])
    all_assets = list(set([ass.split(':')[0]+':high' for ass in all_refs
                  if mc.objExists(ass.split(':')[0]+':high')]))
    assets_info = []
    # [{资产名：name_en, 材质topo信息路径：TEX_topo_file， 绑定topo信息路径：RIG_topo_file, 模型topo信息路径: MOD_topo_file},...]
    for asset in all_assets:
        dict_temp = {}
        ref_file = mc.referenceQuery(asset, f=1)
        ref_file_name_en = ref_file.split('/')[-1].split('.')[0]
        asset_name = dsf_db.searchTaskInfoDict(ref_file_name_en)['name']
        for c in classify:
            name_en = 'dsf_' + asset_name + '_' + c
            task_dict = dsf_db.searchTaskInfoDict(name_en)
            try:
                topo_info_path = INFOPATH + task_dict['path'] + '/' + \
                                 task_dict['name_en'] + '_' + str(task_dict['pversion']) + '.json'
            except KeyError:
                topo_info_path = None
            dict_temp[c+'_topo_info'] = 'None'
            if c in ['MOD']:
                dict_temp[c + '_topo_info'] = task_dict['pversion']
            else:
                if topo_info_path and os.path.isfile(topo_info_path):
                    with open(topo_info_path) as topo_file:
                        topo_info = json.load(topo_file)
                    dict_temp[c + '_topo_info'] = topo_info['mod_version']
        dict_temp['ref_file_name_en'] = ref_file_name_en
        assets_info.append(dict_temp)
    return assets_info


class TopoCompare(base_class, form_class):
    def __init__(self, parent=getMayaWindow()):
        super(TopoCompare, self).__init__(parent=parent)
        self.setupUi(self)

    @QtCore.Slot()
    def on_pushButton_clicked(self):
        self.treeWidget.clear()
        dict_temp = {'ref_file_name_en': 0,
                     'RIG_topo_info': 1,
                     'TEX_topo_info': 2,
                     'MOD_topo_info': 3
                     }
        all_assets = get_assets()
        # print all_assets
        for each in all_assets:
            item_ref = QtWidgets.QTreeWidgetItem()
            for k, v in dict_temp.iteritems():
                # item_ref.setSizeHint(v, QtCore.QSize(10, 20))
                item_ref.setText(v, str(each[k]))
                if each[k] == 'None':
                    item_ref.setTextColor(v, QtGui.QColor(255, 0, 0))
            self.treeWidget.addTopLevelItem(item_ref)
            # item_ref.setText(1, each["RIG_topo_info"])
            # item_ref.setText(2, each["TEX_topo_info"])
            # item_ref.setText(3, each["MOD_topo_info"])
            # # item_ref.setCheckState(0, QtCore.Qt.Unchecked)
            #
            # item_ref.setTextColor(0, QtGui.QColor(255, 0, 0))
            # each['item'] = item_ref













