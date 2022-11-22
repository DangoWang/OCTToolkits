#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Dango Wang
# time : 2019/7/9
import shutil

from dango_utils import *
from check_cfg import *
import maya.cmds as cmds
import pymel.core as pm
import os
import check_cfg
import search_pg_db as sdb
from maya import mel
reload(check_cfg)
reload(sdb)


try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    import PySide.QtGui as QtWidgets
    from PySide import QtCore

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path+'\\ui.ui')
oct_ini_file = QtCore.QSettings(os.path.expanduser("~") + "/settings.ini", QtCore.QSettings.IniFormat)


class FlWork(base_class, form_class):
    def __init__(self, parent=None):
        super(FlWork, self).__init__(parent=getMayaWindow())
        self.setupUi(self)
        self._db = None
        self.project_cb.addItem(self._project)

    @property
    def _project(self):
        return oct_ini_file.value("project/name")

    @property
    def _scene(self):
        return self.scene_cb.currentText()

    @property
    def _shot(self):
        return self.shot_cb.currentText()

    @property
    def _target(self):
        return self.target_cb.currentText()

    @QtCore.Slot()
    def on_import_abc_pb_clicked(self):
        from AbcCacheTool import AbcInput
        reload(AbcInput)
        AbcInput.main()

    @QtCore.Slot()
    def on_import_fur_pb_clicked(self):
        from fur_pipe import main as furm
        reload(furm)
        furmWin = furm.FurInWin()
        furmWin.show()

    @QtCore.Slot()
    def on_project_cb_currentIndexChanged(self):
        self._db = sdb.taskInfo('dsf')
        all_scenes = self._db.searchSceneList()
        self.scene_cb.addItems(all_scenes)

    @QtCore.Slot()
    def on_scene_cb_currentIndexChanged(self):
        self._db = sdb.taskInfo(self._project)
        all_shots = self._db.searchShotNameList(self._scene)
        self.shot_cb.addItems(all_shots)

    @QtCore.Slot()
    def on_save_as_pb_clicked(self):
        target_path = '/'.join([DSFLOCALWORKPATH, self._project, 'Shot', self._target, self._scene, self._shot])
        file_name = '_'.join(['s' + self._scene, self._shot, self._target+'.ma'])
        if not os.path.isdir(target_path):
            os.makedirs(target_path)

        all_abc_nodes = cmds.ls(type='AlembicNode') or []
        all_yeti_nodes = cmds.ls(type='pgYetiMaya') or []
        wrong_abc = []
        wrong_yeti = []
        abc_set_up_file = ''
        yeti_set_up_file = ''
        for each_abc in all_abc_nodes:
            abc_path = mel.eval('getAttr %s.abc_File' % each_abc) or ''
            if not abc_path:
                continue
            print abc_path
            if self._shot not in abc_path or self._scene not in abc_path or '.abc' not in abc_path:
                wrong_abc.append(abc_path)
                continue
            str_temp = abc_path.split(CACHEPATH+'/'.join([self._project, self._scene, self._shot])+'/')[-1]
            # str_temp : An/0/SX_TX/RIG/dsf_SX_TX_RIG/20190515_1624.abc
            source_step = str_temp.split('/')[0]
            print source_step
            if source_step not in ['CF_Cloth']:
                wrong_abc.append(abc_path)
                continue
            abc_set_up_file = CACHEPATH + '/'.join([self._project, self._scene, self._shot,
                                                source_step, str_temp.split('/')[1], 'setup.json'])
            break
        for each_yeti in all_yeti_nodes:
            yeti_path = mel.eval('getAttr %s.cacheFileName' % each_yeti) or ''
            if not yeti_path:
                continue
            if self._shot not in yeti_path or self._scene not in yeti_path or '.fur' not in yeti_path:
                wrong_yeti.append(yeti_path)
                continue
            str_temp = yeti_path.split(CACHEPATH+'/'.join([self._project, self._scene, self._shot])+'/')[-1]
            # str_temp : An/0/SX_TX/RIG/dsf_SX_TX_RIG/20190515_1624.fur
            source_step = str_temp.split('/')[0]
            if source_step not in ['CF_Fur']:
                wrong_yeti.append(yeti_path)
                continue
            yeti_set_up_file = CACHEPATH + '/'.join([self._project, self._scene, self._shot,
                                                source_step, str_temp.split('/')[1], 'setup.json'])
            break
        if wrong_abc or wrong_yeti:
            wrong_nodes = wrong_yeti + wrong_abc
            QtWidgets.QMessageBox.critical(self, u"错误：", u'以下节点缓存加载错误！:\n%s' % wrong_nodes)
            return False
        cache_folder = target_path + '/Cache'

        if not os.path.isdir(cache_folder):
            os.mkdir(cache_folder)
        print abc_set_up_file, yeti_set_up_file
        if abc_set_up_file and os.path.isfile(abc_set_up_file):
            shutil.copyfile(abc_set_up_file, cache_folder+'/abc_setup.json')
            pass
        if yeti_set_up_file and os.path.isfile(yeti_set_up_file):
            shutil.copyfile(yeti_set_up_file, cache_folder+'/fur_setup.json')
            pass
        cmds.file(rename='/'.join([target_path, file_name]))
        cmds.file(force=True, type='mayaAscii', save=True)




