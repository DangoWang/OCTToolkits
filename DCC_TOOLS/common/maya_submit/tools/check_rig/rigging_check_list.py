#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/27
import json
import os
from DCC_TOOLS.common.dcc_utils import *
from utils.shotgun_operations import *
import maya.cmds as mc
import pymel.core as pm
from maya import mel

ctrl_top_grp = 'MotionSystem'


def raise_warning_dialog(text):
    warning_win = mc.window(t=u'提示', h=30, s=1)
    mc.columnLayout(adj=1)
    mc.text(text, h=100)
    mc.showWindow(warning_win)


def reformat_list(list_):
    # 将列表进行自动换行
    if len(list_) <= 1:
        return str(list_)
    i = 0
    new_list_str = ''
    for _ in xrange(100):
        if list_[i:(i + 5)]:
            new_list_str += str(list_[i:(i + 5)]) + '\n'
            i = i+5
        else:
            break
    return new_list_str


def get_all_mesh_transform():
    return [each.getParent() for each in pm.ls(type='mesh')]


def check_hierarchy_func(kwargs=None):
    # 检查最上层大纲层级是否符合规范
    camera_grp = {'persp', 'top', 'front', 'side'}
    all_top_grp = mc.ls(assemblies=True)
    asset = list(set(all_top_grp) - camera_grp)
    if len(asset) > 1:
        return u'大纲中发现多个层级！！\n %s' % asset
    return None


def fix_hierarchy_func(*args, **kwargs):
    return u'请手动处理！'


def check_tex_func(*args, **kwargs):
    all_files_nodes = mc.ls(type='file')
    wrong_nodes = []
    if all_files_nodes:
        wrong_file_nodes = [fn for fn in all_files_nodes if
                            pm.getAttr(fn + '.fileTextureName').split(':')[0] not in ['I']]
        wrong_nodes.extend(wrong_file_nodes)
    if wrong_nodes:
        return u'贴图路径不正确！'
    return None
    pass


def fix_tex_func(*args, **kwargs):
    return u'请手动处理！'


def check_unknown_nodes_func(*args, **kwargs):
    all_unknown_nodes = mc.ls(type='unknown')
    if all_unknown_nodes:
        return u'发现以下未知节点，是否删除？\n%s' % all_unknown_nodes
    return None


def fix_unknown_nodes_func(*args, **kwargs):
    extra_nodes_type = ['unknown', 'animLayer']
    all_unknown_nodes = []
    for each_type in extra_nodes_type:
        all_this_type_nodes = pm.ls(type=each_type)
        all_unknown_nodes.extend(all_this_type_nodes)
    wrong_nodes = []
    if all_unknown_nodes:
        for each in all_unknown_nodes:
            try:
                pm.lockNode(each, lock=False)
                pm.delete(each)
            except:
                wrong_nodes.append(each.name())
                continue
    if wrong_nodes:
        return u'以下节点被锁定无法删除！\n%s' % wrong_nodes
    return None


def check_ctrl_renaming_func(*args, **kwargs):
    if not mc.objExists(ctrl_top_grp):
        return False
    all_nurbscrv = pm.listRelatives(ctrl_top_grp, c=1, ad=1, s=1)
    all_ctrls = [ctl.getParent() for ctl in all_nurbscrv if pm.objectType(ctl) == 'nurbsCurve']
    all_renaming_ctrls = [c.name() for c in all_ctrls if "|" in c.name()]
    if all_renaming_ctrls:
        return u'发现以下控制器重复命名！！请手动解决...\n%s' % all_renaming_ctrls
    return None


def fix_ctrl_renaming_func(*args, **kwargs):
    return u'请手动解决！'


def check_ctrl_attr_func(*args, **kwargs):
    if not mc.objExists(ctrl_top_grp):
        return False
    all_nurbscrv = pm.listRelatives(ctrl_top_grp, c=1, ad=1, s=1)
    all_ctrls = [ctl.getTransform() for ctl in all_nurbscrv]
    wrong_ctrls = []
    for each in all_ctrls:
        a = (each.getTranslation().get() == (0.0, 0.0, 0.0)) if pm.getAttr(each.name()+".t", cb=1) else 1
        b = each.getRotation().isZero() if pm.getAttr(each.name()+".r", cb=1) else 1
        c = each.getScale() == [1.0, 1.0, 1.0] if pm.getAttr(each.name()+".s", cb=1) else 1
        if a and b and c:
            continue
        wrong_ctrls.append(each)
    if wrong_ctrls:
        pm.select(wrong_ctrls, r=1)
        return u'发现以下控制器属性栏错误！请检查...\n%s' % wrong_ctrls
    return None


def fix_ctrl_attr_func(*args, **kwargs):
    return u'请手动处理!'


def check_unknown_plugins_func(*args, **kwargs):
    mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    unknown_plugins = mc.unknownPlugin(q=True, list=True)
    if unknown_plugins:
        return u'发现以下未知插件，是否移除？\n%s' % unknown_plugins
    return None


def fix_unknown_plugins_func(*args, **kwargs):
    unknown_plugins = mc.unknownPlugin(q=True, list=True)
    failed_removing = list()
    if unknown_plugins:
        for each in unknown_plugins:
            try:
                mc.unknownPlugin(each, r=True)
            except:
                failed_removing.append(each)
        if failed_removing:
            return u'以下未知插件无法移除！请手动处理..\n%s' % failed_removing
    try:
        mel.eval("delete BaseAnimation;")
    except Exception as e:
        print e
    return None


def check_topology_func(*args, **kwargs):
    mc.select(ado=True)
    for group in mc.ls(sl=True):
        try:
            asset_info = find_shotgun("Asset", [["project", "name_is", "DSF"], ["code", "is", group]], ["sg_md5"])
            break
        except:
            pass
    if not asset_info:
        raise_warning_dialog(u'没有在shotgun上找到该文件对应的资产,请检查大纲命名是否正确！！\n')
        return False
    else:
        mod_shotgun_md5 = asset_info[0].get("sg_md5")
        rig_file_md5 = get_hierarchy_data(ignore_hide_objects=True)
        if mod_shotgun_md5:
            topology_error = comparison_md5(mod_shotgun_md5, rig_file_md5)
            print topology_error
            if topology_error:
                mc.select(cl=True)
                mc.select(topology_error)
                # raise_warning_dialog(u'该文件与最新的模型对比存在拓扑不一致！！\n')
                return u'该文件与最新的模型对比存在拓扑不一致！请手动处理..\n'

def fix_topology_func(*args, **kwargs):
    return u'请手动处理!'



    # mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    # unknown_plugins = mc.unknownPlugin(q=True, list=True)
    # if unknown_plugins:
    #     return u'发现以下未知插件，是否移除？\n%s' % unknown_plugins
    # return None