#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wangdonghao
# time:2019/6/5

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


def flat(list_):
    # 将嵌套列表展开
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return filter(None, res)


def get_assets(group=['CHAR', 'PROP', 'ENV']):
    existed_grp = [each for each in group if mc.objExists(each)]
    all_refs = flat([mc.listRelatives(ref, c=1) for ref in existed_grp])
    all_assets = list(set([ass.split(':')[0]+':high' for ass in all_refs
                  if mc.objExists(ass.split(':')[0]+':high')]))
    assets_info = []
    # [{资产类型：classify, 资产名称空间：namespace, uv信息路径：路径},...]
    for asset in all_assets:
        dict_temp = {}
        try:
            ref_file = mc.referenceQuery(asset, f=1)
            ref_file_name_en = ref_file.split('/')[-1].split('.')[0]
            asset_name = dsf_db.searchTaskInfoDict(ref_file_name_en)['name']
            TEX_name_en = 'dsf_' + asset_name + '_TEX'
            TEX_task_dict = dsf_db.searchTaskInfoDict(TEX_name_en)
            uv_info_path = INFOPATH + TEX_task_dict['path'] + '/' + \
                           TEX_task_dict['name_en'] + '_' + str(TEX_task_dict['pversion']) + '.json'
            dict_temp['classify'] = TEX_task_dict['classify']
            dict_temp['ref_file_name_en'] = ref_file_name_en
            dict_temp['uv_info_path'] = uv_info_path
        except KeyError:
            pass
        assets_info.append(dict_temp)
    return assets_info


def set_UVs(source_data, target_namespace):
    """
    :param source_data:{shape: uv, shape: uv....}
    :param target_namespace:dsf_asset_name_TEX
    :return:
    """
    for k, v in source_data.iteritems():
        target_shape = target_namespace + ':' + k
        pm_node = pm.PyNode(target_shape)
        pm_node.clearUVs()
        yield pm_node.setUVs(v[0], v[1])


def assign_UVs(source_data, target_namespace):
    for k, v in source_data.iteritems():
        target_shape = target_namespace + ':' + k
        pm_node = pm.PyNode(target_shape)
        yield pm_node.assignUVs(v[0], v[1])


class UVLoad(base_class, form_class):
    def __init__(self, parent=getMayaWindow()):
        super(UVLoad, self).__init__(parent=parent)
        self.setupUi(self)
        self.all_assets_dict = get_assets()
        self.progressBar.hide()
        self.progressLabel.hide()
        self.arrange_items()

    def arrange_items(self):
        items_dict = {'CH': 0, 'PROP': 1, 'ENV': 2}
        for each in self.all_assets_dict:
            if not each:
                continue
            item_ref = QtWidgets.QTreeWidgetItem()
            item_ref.setSizeHint(0, QtCore.QSize(10, 20))
            item_ref.setText(0, each["ref_file_name_en"])
            # item_ref.setCheckState(0, QtCore.Qt.Unchecked)
            char_item = self.treeWidget.topLevelItem(items_dict[each['classify']])
            char_item.addChild(item_ref)
            item_ref.setTextColor(0, QtGui.QColor(255, 0, 0))
            each['item'] = item_ref
        return True

    def output_info(self, text):
        txt = self.textBrowser.toPlainText() or u'========信息输出========='
        new_text = '\n'.join([txt, text])
        self.textBrowser.setText(new_text)

    @QtCore.Slot()
    def on_refresh_pb_clicked(self):
        self.all_assets_dict = get_assets()
        self.arrange_items()

    @QtCore.Slot(name='on_import_uv_pb_clicked')
    @undoable
    def on_import_uv_pb_clicked(self):
        self.progressBar.show()
        self.progressLabel.show()
        for each in self.all_assets_dict:
            if not each:
                continue
            if not os.path.isfile(each['uv_info_path']):
                each['item'].setTextColor(0, QtGui.QColor(255, 0, 0))
                print each['uv_info_path']
                self.output_info(u'%s:未发现UV信息，请告知材质通过maya上传并发布文件..' % each['ref_file_name_en'])
                continue
            with open(each['uv_info_path']) as uv_file:
                uv_info_temp = json.load(uv_file)
            uv_info = uv_info_temp['UV_info']
            ass_uv_info = uv_info_temp['ass_UV_info']
            set_uv_iter = set_UVs(uv_info, each['ref_file_name_en'])
            ass_uv_iter = assign_UVs(ass_uv_info, each['ref_file_name_en'])
            percent = 0
            success = 0
            while True:
                try:
                    set_uv_iter.next()
                    ass_uv_iter.next()
                    self.progressBar.setValue((percent*100)/len(uv_info))
                    self.progressLabel.setText(each['ref_file_name_en'])
                    percent += 1
                except StopIteration:
                    success = 1
                    break
                except:
                    self.output_info(u'%s:UV传递错误！请检查拓扑..' % each['ref_file_name_en'])
                    each['item'].setTextColor(0, QtGui.QColor(255, 0, 0))
                    success = 0
                    break
            if success:
                print u'%s:成功导入UV..' % each['ref_file_name_en']
                self.output_info(u'%s:成功导入UV..' % each['ref_file_name_en'])
                each['item'].setTextColor(0, QtGui.QColor(0, 255, 0))
        self.progressBar.hide()
        self.progressLabel.hide()



















