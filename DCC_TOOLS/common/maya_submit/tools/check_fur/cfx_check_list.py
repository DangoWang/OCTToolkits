#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/23
import json
import os

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.api.OpenMaya as om
from utils.common_methods import *
from DCC_TOOLS.common.dcc_utils import *

try:
    from PySide2 import QtWidgets
except ImportError:
    import PySide.QtGui as QtWidgets

legal_layers = ['defaultLayer', 'defaultRenderLayer', 'BaseAnimation', 'masterLayer']
legal_grps = ['CHAR', 'PROP', 'ENV', 'CAM', 'persp', 'top', 'front', 'side']


def raise_warning_dialog(text):
    warning_win = mc.window(t=u'提示', h=30, s=1)
    mc.columnLayout(adj=1)
    mc.text(text, h=100)
    mc.showWindow(warning_win)


def get_all_mesh_transform():
    return [each.getParent() for each in pm.ls(type='mesh')]


def reformat_list(list):
    # 将列表进行自动换行
    if len(list) <= 1:
        return str(list)
    i = 0
    new_list_str = ''
    for _ in xrange(100):
        if list[i:(i+5)]:
            new_list_str += str(list[i:(i+5)])+'\n'
            i = i+5
        else:
            break
    return new_list_str


def check_hierarchy_func(fix=False, kwargs=None):
    # 检查最上层大纲层级是否符合规范
    pass


def check_lambert_func(fix=False, kwargs=None):
    all_lambert = mc.ls(type='lambert')
    if len(all_lambert) != 1:
        if fix:
            all_lambert.remove('lambert1')
            mc.select(all_lambert, r=1)
            raise_warning_dialog(u'场景中发现多个lambert节点，请检查...\n%s' % reformat_list(all_lambert))
        return False
    if not mc.getAttr(all_lambert[0]+'.color') == [(0.5, 0.5, 0.5)]:
        if fix:
            mc.setAttr(all_lambert[0]+'.color', 0.5, 0.5, 0.5)
            return True
        return False
    return True


def check_layers_func(fix=False, kwargs=None):
    all_layers = mc.ls(type=['displayLayer', 'renderLayer', 'animLayer'])
    if all_layers:
        illegal_layers = [layer for layer in all_layers if layer not in legal_layers]
        if illegal_layers:
            if fix:
                mc.delete(illegal_layers)
                return True
            return False
    return True


def check_lights_func(fix=False, kwargs=None):
    all_lights = mc.ls(type='light')
    if all_lights:
        if fix:
            mc.select(all_lights, r=1)
            mel.eval('pickWalk -d up;doDelete;')
            return True
        return False
    return True


def check_unused_mat_func(fix=False, kwargs=None):
    mel.eval('MLdeleteUnused;')
    return True


def check_unknown_nodes_func(fix=False, kwargs=None):
    all_unknown_nodes = mc.ls(type='unknown')
    wrong_nodes = []
    if all_unknown_nodes:
        if fix:
            for each in all_unknown_nodes:
                try:
                    mc.lockNode(each, lock=False)
                    mc.delete(each)
                except:
                    wrong_nodes.append(each.name())
                    continue
            return True
        return False
    return True


def check_unknown_plugins_func(fix=False, kwargs=None):
    unknown_plugins = mc.unknownPlugin(q=True, list=True)
    failed_removing = list()
    if unknown_plugins:
        if fix:
            for each in unknown_plugins:
                try:
                    mc.unknownPlugin(each, r=True)
                except:
                    failed_removing.append(each)
            return True
        return False
    return True


def check_extra_wins_func(fix=False, kwargs=None):
    maya_window = getMayaWindow().objectName()
    all_windows = pm.lsUI(typ='window')
    window_remove = [maya_window]
    all_extra_windows = [w for w in all_windows if w not in window_remove]
    if all_extra_windows:
        if fix:
            for each in all_extra_windows:
                try:
                    mc.deleteUI(each)
                except:
                    pass
            return True
        return False
    return True


def check_display_mode_func(fix=False, kwargs=None):
    mel.eval('SelectAll;')
    mel.eval('displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;')
    mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    mel.eval('DisplayWireframe;')
    return True

def check_ns_func(fix=False, kwargs=None):
    all_extra_windows = [ns for ns in mc.namespaceInfo(lon=1) if ns not in ["UI", "shared"]]
    if all_extra_windows:
        if fix:
            for each in all_extra_windows:
                try:
                    mc.namespace(mergeNamespaceWithRoot=1, rm=each)
                except:
                    pass
            return True
        return False
    return True


