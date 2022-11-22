#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/6/27


import os
import getpass
from maya import cmds
import maya.mel as mel
from dango_utils import *
import check_cfg
reload(check_cfg)
import logging
import json
import search_pg_db as sdb
reload(sdb)
import pprint as pp
import pymel.core as pm
try:
    from PySide2 import QtWidgets, QtCore, QtNetwork, QtGui
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore, QtNetwork

file_path = str(os.path.split(os.path.realpath(__file__))[0])
fur_out_form, fur_out_base = loadUiType(file_path + '\\fur_out_ui.ui')
fur_in_form, fur_in_base = loadUiType(file_path + '\\fur_in_ui.ui')
oct_ini_file = QtCore.QSettings(os.path.expanduser("~") + "/settings.ini", QtCore.QSettings.IniFormat)

legal_hierarchies = {'CHAR', 'PROP', 'ENV'}
top_item_dict = {u"名称空间": 0, u"节点名": 1, u"缓存名": 2, u"路径": 3}


def get_top_hierarchy(obj):
    parent = cmds.listRelatives(obj, p=1)
    if parent:
        return get_top_hierarchy(parent[0])
    return obj


def get_all_assemblies():
    return list(set(cmds.ls(assemblies=True)) & legal_hierarchies)


def get_host_name():
    return QtNetwork.QHostInfo().localHostName()


def get_user_tasks_name(db, user):
    all_tasks_dict = db.searchUserTaskInfoList(user)
    return [each['name_en'] for each in all_tasks_dict if each]


def arrange_items(content, tree_widget, checked=['all']):
    # {u'CHAR': {u'dsf_SX_TX_CFX_Fur': [{'cache_name': u'lash',
    #                                    'node_name': u'dsf_SX_TX_CFX_Fur:pgYetiMaya_lashShape',
    #                                    'output_path': u'Z:/DS/Library/TD/Cache/dsf/01/020/Fl/0/
    #                                                   dsf_SX_TX_CFX_Fur/lash/lash.%04d.fur'}],
    #            u'dsf_SX_TX_CFX_Fur1': [{'cache_name': u'lash',
    #                                     'node_name': u'dsf_SX_TX_CFX_Fur1:pgYetiMaya_lashShape',
    #                                     'output_path': u'Z:/DS/Library/TD/Cache/dsf/01/020/Fl/0/
    #                                                   dsf_SX_TX_CFX_Fur1/lash/lash.%04d.fur'}]},
    #  u'PROP': {u'dsf_SX_TX_CFX_Fur2': [{'cache_name': u'lash',
    #                                     'node_name': u'dsf_SX_TX_CFX_Fur2:pgYetiMaya_lashShape',
    #                                     'output_path': u'Z:/DS/Library/TD/Cache/dsf/01/020/Fl/0/
    #                                                    dsf_SX_TX_CFX_Fur2/lash/lash.%04d.fur'}]}}
    if content:
        for group, namespace_dict in content.iteritems():
            group_item = QtWidgets.QTreeWidgetItem()
            group_item.setSizeHint(top_item_dict[u"名称空间"], QtCore.QSize(10, 20))
            group_item.setText(top_item_dict[u"名称空间"], group)
            tree_widget.content_tw.addTopLevelItem(group_item)
            for namespace, fur_list in namespace_dict.iteritems():
                namespace_item = QtWidgets.QTreeWidgetItem()
                namespace_item.setSizeHint(top_item_dict[u"名称空间"], QtCore.QSize(10, 20))
                namespace_item.setText(top_item_dict[u"名称空间"], namespace)
                if not cmds.ls(namespace+':*'):
                    namespace_item.setBackgroundColor(top_item_dict[u"名称空间"], QtGui.QColor(255, 0, 0))
                group_item.addChild(namespace_item)
                for index, each in enumerate(fur_list):
                    node_item = QtWidgets.QTreeWidgetItem()

                    node_item.setSizeHint(top_item_dict[u"节点名"], QtCore.QSize(10, 20))
                    node_item.setText(top_item_dict[u"节点名"], each['node_name'])

                    node_item.setSizeHint(top_item_dict[u"缓存名"], QtCore.QSize(10, 20))
                    node_item.setText(top_item_dict[u"缓存名"], each['cache_name'])
                    if 'all' in checked:
                        node_item.setCheckState(top_item_dict[u"缓存名"], QtCore.Qt.Checked)
                    else:
                        got_it = 0
                        for check in checked:
                            if check in each['cache_name']:
                                node_item.setCheckState(top_item_dict[u"缓存名"], QtCore.Qt.Checked)
                                got_it = 1
                            else:
                                continue
                        if not got_it:
                            node_item.setCheckState(top_item_dict[u"缓存名"], QtCore.Qt.Unchecked)
                    node_item.setSizeHint(top_item_dict[u"路径"], QtCore.QSize(10, 20))
                    node_item.setText(top_item_dict[u"路径"], each['output_path'])
                    
                    if not cmds.objExists(each['node_name']):
                        node_item.setBackgroundColor(top_item_dict[u"节点名"], QtGui.QColor(255, 0, 0))
                    namespace_item.addChild(node_item)
                namespace_item.setExpanded(True)
            group_item.setExpanded(True)


class FurOutWin(fur_out_base, fur_out_form):

    def __init__(self, parent=getMayaWindow()):
        super(FurOutWin, self).__init__(parent=parent)
        self.setupUi(self)
        self._user = oct_ini_file.value(get_host_name() + "/name")
        self._project = oct_ini_file.value("project/name")
        self._current_task = ''
        self._db = sdb.taskInfo(self._project)
        self._task_version = ''
        self._task_dict = {}
        self._output_path = ''
        self._out_nodes = []
        self._scene_name = QtCore.QFileInfo(cmds.file(q=True, sn=True)).baseName()
        self.__init_ui()

    def __init_ui(self):
        self.current_proj_cb.addItem(self._project)
        self.user_le.setText(self._user)
        self.on_input_end_f_pb_clicked()
        self.on_input_start_f_pb_clicked()
        self.output_lb.hide()
        self.output_prb.hide()

    @QtCore.Slot()
    def on_current_proj_cb_currentIndexChanged(self):
        self.task_cb.clear()
        self._project = self.current_proj_cb.currentText()
        if not self._project:
            return
        self._db = sdb.taskInfo(self._project)
        for i, task_name in enumerate(get_user_tasks_name(self._db, self._user)):
            if not task_name:
                continue
            if task_name in self._scene_name or self._scene_name in task_name:
                self._current_task = task_name
            self.task_cb.addItem(task_name)
            self.task_cb.setItemData(i, task_name, QtCore.Qt.UserRole + 1)
        if self._current_task:
            ind = self.task_cb.findText(self._current_task, QtCore.Qt.MatchExactly)
            if ind > 0:
                self.task_cb.setCurrentIndex(ind)
        return True

    @QtCore.Slot()
    def on_task_cb_currentIndexChanged(self):
        self.task_ver_le.setText('')
        self.output_dir_le.setText('')
        if self.task_cb.currentText():
            self._current_task = self.task_cb.currentText()
            self._task_dict = self._db.searchTaskInfoDict(self._current_task)
            task_version = str(self._task_dict['version'] or '0')
            self._task_version = task_version
            self.task_ver_le.setText(self._task_version)
        else:
            return
        self._output_path = check_cfg.CACHEPATH + '/'.join(
            [self._project, self._task_dict["scene"], self._task_dict["name"], self._task_dict["group"],
             self._task_version]
            )
        self.output_dir_le.setText(self._output_path)
        return True

    @QtCore.Slot()
    def on_input_start_f_pb_clicked(self):
        self.start_f_le.setText(str(int(cmds.playbackOptions(q=1, min=1))))

    @QtCore.Slot()
    def on_input_end_f_pb_clicked(self):
        self.end_f_le.setText(str(int(cmds.playbackOptions(q=1, max=1))))

    def _get_content_dict(self, out=False):
        all_yeti_nodes = cmds.ls(type='pgYetiMaya')
        if not all_yeti_nodes:
            return
        content_dict = {}
        for each_yeti_node in all_yeti_nodes:
            if out and each_yeti_node not in self._out_nodes:
                continue
            top_hiechy = get_top_hierarchy(each_yeti_node)
            namespace = each_yeti_node.split(':')[0]
            yeti_node_name = pm.PyNode(each_yeti_node).getParent().name().split(':')[-1].split('_')[-1]
            output_path = '/'.join([self._output_path, namespace, yeti_node_name, yeti_node_name+'.%04d.fur'])
            dict_temp = dict(node_name=each_yeti_node, cache_name=yeti_node_name, output_path=output_path)
            if top_hiechy not in content_dict.keys():
                content_dict[top_hiechy] = {}
            if namespace not in content_dict[top_hiechy].keys():
                content_dict[top_hiechy][namespace] = []
            content_dict[top_hiechy][namespace].append(dict_temp)
            # self._output_list.append(dict_temp)
        return content_dict

    @QtCore.Slot()
    def on_output_dir_le_editingFinished(self):
        self.output_dir_le.setText(self.output_dir_le.text().replace('\\', '/'))
        self._output_path = self.output_dir_le.text()
        self.on_load_content_pb_clicked()

    @QtCore.Slot()
    def on_load_content_pb_clicked(self):
        self.content_tw.clear()
        self.output_lb.show()
        if not self._output_path:
            logging.error(u'请选择正确的任务或者填入正确的路径！！')
            return
        content = self._get_content_dict()
        arrange_items(content, self, checked=['all'])

    @property
    def _output_list(self):
        node_dict = []
        for top_item_index in range(self.content_tw.topLevelItemCount()):
            top_item = self.content_tw.topLevelItem(top_item_index)
            for namespace_item_index in range(0, top_item.childCount()):
                namespace_item = top_item.child(namespace_item_index)
                for node_index in range(0, namespace_item.childCount()):
                    node_item = namespace_item.child(node_index)
                    if node_item.checkState(top_item_dict[u"缓存名"]) == QtCore.Qt.Checked:
                        node_dict.append(dict(node_name=node_item.text(top_item_dict[u"节点名"]),
                                              cache_name=node_item.text(top_item_dict[u"缓存名"]),
                                              output_path=node_item.text(top_item_dict[u"路径"]),
                                              ))
                        self._out_nodes.append(node_item.text(top_item_dict[u"节点名"]))
        return node_dict

    @QtCore.Slot()
    def on_output_doit_pb_clicked(self):
        if self._output_list:
            try:
                for i, each in enumerate(self._output_list):
                    try:
                        if not os.path.isdir(each['output_path']):
                            os.makedirs(each['output_path'].rstrip(each['output_path'].split('/')[-1]))
                    except WindowsError:
                        pass
                    # self.output_lb.show()
                    self.output_prb.show()
                    self.output_lb.setText(each['node_name'])
                    self.output_prb.setValue(100*i/len(self._output_list))
                    mel.eval('pgYetiCommand '
                             '-writeCache "{0}" -range {1} {2} -samples 1 -updateViewport 0 -generatePreview 0 {3};'
                             .format(each['output_path'], self.start_f_le.text(), self.end_f_le.text(), each['node_name']))
                    logging.info(u'成功导出：%s\n' % each['output_path'])
                # self.output_lb.hide()
                self.output_prb.hide()
                self.output_lb.setText(u'Success！')
                self.mk_json_file()
            except Exception as e:
                print e
                self.output_prb.hide()
                self.output_lb.setText(u'Failed！')

    def mk_json_file(self):
        json_path = self._output_path + '/setup.json'
        json_dict = dict(scenename=self._current_task, start=self.start_f_le.text(), end=self.end_f_le.text(),
                         project=self._project, typ=self._get_content_dict(out=True))
        with open(json_path, 'w') as js:
            json.dump(json_dict, js, indent=4, ensure_ascii=False)


class FurInWin(fur_in_base, fur_in_form):

    def __init__(self, parent=getMayaWindow()):
        super(FurInWin, self).__init__(parent=parent)
        self.setupUi(self)
        self._db = None
        self._init_ui()

    def _init_ui(self):
        current_proj = self._project
        self.current_proj_cb.addItem(current_proj)
        self.input_lb.hide()
        self.input_prb.hide()

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
    def _cache_ver(self):
        return self.cache_ver_cb.currentText()

    @property
    def _source(self):
        return self.source_cb.currentText()

    @property
    def _source_asset(self):
        return self.source_asset_cb.currentText()

    @property
    def _target(self):
        return self.target_cb.currentText()

    @property
    def _input_path(self):
        return self.input_dir_le.text()

    @property
    def _output_list(self):
        node_dict = []
        for top_item_index in range(self.content_tw.topLevelItemCount()):
            top_item = self.content_tw.topLevelItem(top_item_index)
            for namespace_item_index in range(0, top_item.childCount()):
                namespace_item = top_item.child(namespace_item_index)
                for node_index in range(0, namespace_item.childCount()):
                    node_item = namespace_item.child(node_index)
                    if node_item.checkState(top_item_dict[u"缓存名"]) == QtCore.Qt.Checked:
                        node_dict.append(dict(node_name=node_item.text(top_item_dict[u"节点名"]),
                                              cache_name=node_item.text(top_item_dict[u"缓存名"]),
                                              output_path=node_item.text(top_item_dict[u"路径"]), ))
        return node_dict

    @QtCore.Slot()
    def on_current_proj_cb_currentIndexChanged(self):
        self._db = sdb.taskInfo('dsf')
        all_scenes = self._db.searchSceneList()
        self.scene_cb.addItems(all_scenes)

    @QtCore.Slot()
    def on_scene_cb_currentIndexChanged(self):
        self._db = sdb.taskInfo(self._project)
        all_shots = self._db.searchShotNameList(self._scene)
        self.shot_cb.addItems(all_shots)

    @QtCore.Slot()
    def on_shot_cb_currentIndexChanged(self):
        fur_cache_path_ver = check_cfg.CACHEPATH + '/'.join(
            [self._project, self._scene, self._shot, self._source])
        if os.path.isdir(fur_cache_path_ver):
            folder_list = [each for each in cmds.getFileList(folder=fur_cache_path_ver) if '.' not in each]
            self.cache_ver_cb.addItems(folder_list)

    @QtCore.Slot()
    def on_cache_ver_cb_currentIndexChanged(self):
        if self._cache_ver:
            self.input_dir_le.setText(check_cfg.CACHEPATH + '/'.join(
                [self._project, self._scene, self._shot, self._source, self._cache_ver]))

    @QtCore.Slot()
    def on_load_content_pb_clicked(self):
        print 'loading...'
        json_file = self._input_path + '/setup.json'
        with open(json_file, 'r') as f:
            contents = json.load(f)
        # print contents
        content = contents['typ']
        new_content_temp = dict_replace(content, self._source_asset, self._target)
        new_content = dict_replace(new_content_temp, self._target+'/', self._source_asset+'/')
        # print new_content
        arrange_items(new_content, self, checked=['all'])

    def input_cache(self, node_dict):
        progress_v = self.input_prb.value()
        node_name = node_dict['node_name'].replace(':', '_')
        if not cmds.objExists(node_name):
            mel.eval('pgYetiEnsurePluginLoaded();')
            yeti_node = pm.PyNode(mel.eval('pgYetiCreate();'))
            pm.rename(yeti_node.getParent(), node_name)
            node_name = pm.PyNode(node_name).getShape().name()
            if not mc.objExists('|Yeti_Cache'):
                mc.createNode('transform', name='|Yeti_Cache')
            pm.PyNode(node_name).getParent().setParent('|Yeti_Cache')
        cmds.setAttr(node_name+'.cacheFileName', node_dict['output_path'], type='string')
        cmds.setAttr(node_name+'.fileMode', 1)
        logging.info(u'导入：%s\n' % [node_name, u'===>', node_dict['output_path']])
        self.input_prb.setValue(progress_v+10)
        # else:
        #     logging.info(u'该节点不存在：%s\n' % node_name)
        #     return

    @QtCore.Slot()
    def on_input_doit_pb_clicked(self):
        print 'importing...'
        print self._output_list
        self.input_lb.show()
        self.input_prb.show()
        self.input_prb.setValue(0)
        map(self.input_cache, self._output_list)
        self.input_prb.setValue(100)
        self.input_lb.setText(u'缓存导入完成！')







