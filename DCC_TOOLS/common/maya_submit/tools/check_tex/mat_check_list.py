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
import hashlib
from DCC_TOOLS.common.dcc_utils import *
from utils.common_methods import *
try:
    from PySide2 import QtWidgets
except ImportError:
    import PySide.QtGui as QtWidgets

legal_sets = ['defaultLightSet', 'defaultObjectSet', 'initialParticleSE', 'initialShadingGroup']
legal_layers = ['defaultLayer', 'defaultRenderLayer', 'BaseAnimation', 'masterLayer']
# file_spec = ['roughness', 'bump', 'normal', 'specular', 'dis', 'metalness',
#              'Roughness', 'Bump', 'Normal', 'Specular', 'Metalness'
#              ]
file_spec = ['basecolor', 'BaseColor', 'clr', 'Clr', 'diffues']

# def raise_warning_dialog(parent, text):
#     return QtWidgets.QMessageBox().warning(parent, u'warning', text, QtWidgets.QMessageBox.Yes)


def raise_warning_dialog(text):
    warning_win = mc.window(t=u'提示', h=30, s=1)
    mc.columnLayout(adj=1)
    mc.text(text, h=100)
    mc.showWindow(warning_win)


def get_all_mesh_transform():
    return [each.getParent() for each in pm.ls(type='mesh')]


def flat(list_):
    # 将嵌套列表展开
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


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


def meshMD5(full_path):
    sl = om.MSelectionList()
    sl.add(full_path)
    mesh_dag = sl.getDagPath(0)
    mesh_mfn = om.MFnMesh(mesh_dag)
    v = mesh_mfn.getVertices()
    v_str0 = '[' + ', '.join([str(i) for i in v[0]]) + ']'
    v_str1 = '[' + ', '.join([str(i) for i in v[1]]) + ']'
    topology = hashlib.md5( v_str0 + ' ' + v_str1).hexdigest()
    return {full_path:topology}


def get_tuopu():
    high_grp = mc.ls('high')
    if not high_grp:
        return {}
    if len(high_grp) != 1:
        raise RuntimeError('high dose not exist or more than one objects named high!!!')
    all_meshes = mc.listRelatives('high', c=1, ad=1, f=1, type='mesh')
    output_dict = {}
    for each in all_meshes:
        output_dict.update(meshMD5(each))
    return output_dict


def check_hierarchy_func(fix=False, kwargs=None):
    # 检查最上层大纲层级是否符合规范
    camera_grp = {'persp', 'top', 'front', 'side'}
    all_top_grp = mc.ls(assemblies=True)
    asset = list(set(all_top_grp) - camera_grp)
    if len(asset) != 1:
        if fix:
            raise_warning_dialog(u'大纲层级数量不正确！！\n %s' % asset)
        return False
    asset_name = asset[0]
    if mc.objExists('blendshape'):
        if fix:
            mc.delete('blendshape')
        else:
            return False
    if len(mc.listRelatives(asset_name, c=1)) != 1 or mc.listRelatives(asset_name, c=1)[0] != 'Geometry':
        raise_warning_dialog(u'大纲层级不正确！请检查...')
        return False
    return True


def check_history_func(fix=False, kwargs=None):
    mel.eval('SelectAll')
    mel.eval('DeleteHistory;')
    return True


def check_hide_mod_func(fix=False, kwargs=None):
    all_hide_meshes = [m for m in get_all_mesh_transform() if not m.v.get()]
    if all_hide_meshes:
        if fix:
            pm.select(all_hide_meshes, r=True)
            raise_warning_dialog(u'已为你选中隐藏的模型\n%s' % reformat_list(all_hide_meshes))
        return False
    return True


def check_set_func(fix=False, kwargs=None):
    all_sets = mc.ls(type='objectSet')
    all_wrong_sets = [s for s in all_sets if s not in legal_sets and 'SG' not in s]
    if all_wrong_sets:
        if fix:
            try:
                mc.delete(all_wrong_sets)
                return True
            except:
                return True
        return False
    return True


def check_no_mat_func(fix=False, kwargs=None):
    all_meshes = mc.ls(type='mesh')
    no_mat_meshes = [each for each in all_meshes if not mc.listConnections(each, type='shadingEngine')]
    if no_mat_meshes:
        if fix:
            mc.select(no_mat_meshes, r=True)
            raise_warning_dialog(u'已为你在场景中选择无材质的模型:\n %s' % reformat_list(no_mat_meshes))
        return False
    return True


def check_lambert_func(fix=False, kwargs=None):
    all_lambert = mc.ls(type='lambert')
    all_lambert.remove('lambert1')
    if len(all_lambert) != 1:
        if fix:
            mc.select(all_lambert, r=1)
            raise_warning_dialog(u'场景中发现多个lambert节点，请检查...\n%s' % reformat_list(all_lambert))
        return False
    if not mc.getAttr(all_lambert[0]+'.color') == [(0.5, 0.5, 0.5)]:
        if fix:
            try:
                mc.setAttr(all_lambert[0]+'.color', 0.5, 0.5, 0.5)
            except RuntimeError:
                pass
            return True
        return False
    return True


def check_face_mat_func(fix=False, kwargs=None):
    all_meshes = mc.ls(type='mesh')
    all_wrong_meshes = []
    for each in all_meshes:
        try:
            all_se = list(set(mc.listConnections(each, type='shadingEngine')))
        except TypeError:
            continue
        all_sg = [sg for sg in all_se if 'SG' in sg]
        if len(all_sg) > 1:
            all_wrong_meshes.append(each)
    if all_wrong_meshes:
        if fix:
            mc.select(all_wrong_meshes, r=True)
            raise_warning_dialog(u'已为你选中带有面材质的模型：\n %s' % reformat_list(all_wrong_meshes))
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
    # all_se = mc.ls(type='shadingEngine')
    # all_needed_materials_temp = [mc.listConnections(each, s=1, d=0) for each in all_se]
    # all_needed_materials = list(set(flat(all_needed_materials_temp)))
    # all_materials = mc.ls(mat=1)
    # all_useless_materials = [every for every in all_materials if every not in all_needed_materials]
    # if all_useless_materials:
    #     if fix:
    #         mc.delete(all_useless_materials)
    #         return True
    #     return False
    return True


def check_samp_func(fix=False, kwargs=None):
    # 检查samplerInfo
    si = mc.ls(type='samplerInfo')
    if len(si) > 1:
        if fix:
            mc.select(si, r=1)
            raise_warning_dialog(u'场景中存在多个samplerInfo节点，请检查\n %s' % reformat_list(si))
            return False
    return True


def check_merge_mat_func(fix=False, kwargs=None):
    # 检查重复的file节点
    mc.select(cl=1)
    fn = mc.ls(type='file')
    fn_dict = {}
    wrong_fn = []
    for each in fn:
        ftn = mc.getAttr(each + '.fileTextureName')
        try:
            if not fn_dict[ftn] in wrong_fn:
                wrong_fn.append(fn_dict[ftn])
            wrong_fn.append(each)
        except KeyError:
            fn_dict[ftn] = each
    if wrong_fn:
        if fix:
            mc.select(wrong_fn, r=1)
            raise_warning_dialog(u'以下节点指向了同一个路径贴图，请检查是否可合并：\n%s' % reformat_list(wrong_fn))
        return False
    return True


def check_file_node_func(fix=False, kwargs=None):
    fn = mc.ls(type='file')
    wrong_attr = str()
    mc.select(cl=1)
    for each in fn:
        f_name = mc.getAttr(each + '.fileTextureName')
        if f_name.split('_')[-1].split('.')[0] not in file_spec:
            if not mc.getAttr(each + '.colorSpace') == 'Raw':
                wrong_attr = wrong_attr + each + '-->' + u'Color Space不是Raw\n'
                mc.select(each, add=1)
            if not mc.getAttr(each + '.ignoreColorSpaceFileRules') == 1:
                wrong_attr = wrong_attr + each + '-->' + u'Ignore CS File Rules未勾选\n'
                mc.select(each, add=1)
            if not mc.getAttr(each + '.alphaIsLuminance') == 1:
                wrong_attr = wrong_attr + each + '-->' + u'Alpha Is Luminance未勾选\n'
                mc.select(each, add=1)
    if wrong_attr:
        if fix:
            raise_warning_dialog(u'以下file节点相应属性存在问题：\n %s' % wrong_attr)
        return False
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
                    wrong_nodes.append(each)
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

def check_transform_attr_func(fix=False, kwargs=None):
    node_list = mc.ls(typ="transform", long=1)
    if not node_list:
        return False
    for node in node_list:
        mesh_list = mc.ls(node, dag=1, type="mesh")
        if not mesh_list:
            continue
        attr_rotate = mc.getAttr("{}.rotate".format(node))
        if attr_rotate!= [(0, 0, 0)]:
            if fix:
                cmds.setAttr("{}.rotate".format(node), 0, 0, 0)
                continue
            return False
    return True
