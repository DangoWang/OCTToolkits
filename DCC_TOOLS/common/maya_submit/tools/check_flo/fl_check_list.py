#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/23
import os

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
from utils.common_methods import *
from DCC_TOOLS.common.dcc_utils import *
try:
    from PySide2 import QtWidgets
except ImportError:
    import PySide.QtGui as QtWidgets


legal_grps = ['CHAR', 'PROP', 'ENV', 'CAM', 'LAYOUT_FX', 'persp', 'top', 'front', 'side']
assets_grps = ['CHAR', 'PROP', 'ENV']


def raise_warning_dialog(parent, text):
    return QtWidgets.QMessageBox().warning(parent, u'warning', text, QtWidgets.QMessageBox.Yes)


def parent_tools():
    mel.eval('source "//192.168.15.242/Plugins/Maya2017/Scripts/Layout/dazu.mel";')
    mel.eval('dazumel;')


def check_hierarchy_func(fix=False):
    # 检查最上层大纲层级是否符合规范
    all_main_hierarchys = mc.ls(assemblies=True)
    illegal_assemblies = [ass.encode('utf-8') for ass in all_main_hierarchys if ass not in legal_grps]
    # missing_assemblies = [ms.encode('utf-8') for ms in legal_grps if ms not in all_main_hierarchys]
    if illegal_assemblies:
        if fix:
            mc.select(illegal_assemblies, r=True)
            raise_warning_dialog(None, u'大纲下存在以下非法层级，请检查:\n%s' % illegal_assemblies)
            parent_tools()
        return False
    if not mc.objExists('|CAM'):
        if fix:
            raise_warning_dialog(None, u'缺失CAM组！！')
        return False
    # if missing_assemblies:
    #     if fix:
    #         raise_warning_dialog(None, u'大纲缺失以下层级，请检查:\n%s' % missing_assemblies)
    #         parent_tools()
    #     return False
    illegal_parenting = []
    illegal_assets = []
    # 检查layout_FX下面是否有引用的东西
    # try:
    #     layout_c = mc.listRelatives('LAYOUT_FX', c=1, ad=1, f=1) or []
    #     cam_c = mc.listRelatives('CAM', c=1, ad=1, f=1) or []
    #     for layout_child in layout_c + cam_c:
    #         if mc.referenceQuery(layout_child, inr=True):
    #             if fix:
    #                 mc.select(layout_child, r=True)
    #                 raise_warning_dialog(None, u'LAYOUT_FX层级下不得放入任何资产！请检查:\n%s' % layout_child)
    #                 parent_tools()
    #             return False
    # except TypeError:
    #     pass
    # 检查资产组下面的非法资产和p错的资产
    for asset in assets_grps:
        if not mc.objExists('|' + asset):
            continue
        sub_assets = mc.listRelatives(asset, c=1, f=1) or []
        if not sub_assets:
            continue
        for each in sub_assets:
            if not mc.referenceQuery(each, inr=True):
                illegal_parenting.append(each)
                continue
    if illegal_parenting:
        if fix:
            mc.select(illegal_parenting, r=True)
            raise_warning_dialog(None, u'以下资产放到了错误的层级下，请检查:\n%s' % illegal_parenting)
            parent_tools()
        return False
    if illegal_assets:
        if fix:
            mc.select(illegal_assets, r=True)
            raise_warning_dialog(None, u'以下资产不在资产表中！请检查:\n%s' % illegal_assets)
        return False
    return True


def check_reference_func(fix=False):
    # 检查非法资产
    all_references = dict()
    display_refs = mc.file(q=True, r=True)
    all_ref_nodes = mc.ls(type='reference')
    for ref_node in all_ref_nodes:
        try:
            if mc.referenceQuery(ref_node, f=1) in display_refs:
                all_references[mc.referenceQuery(ref_node, f=1)] = ref_node
        except RuntimeError:
            continue
    unload_refs = []
    illegal_references = []
    wrong_path_references = []
    not_TEX_asset = []
    for ref in display_refs:
        if not mc.referenceQuery(ref, il=True):
            unload_refs.append(ref)
            continue
    if unload_refs:
        if fix:
            raise_warning_dialog(None, u'以下资产未勾选！请检查:\n%s' % unload_refs)
        return False
    if illegal_references:
        if fix:
            raise_warning_dialog(None, u'以下资产不在资产表中！请通报制片:\n%s' % illegal_references)
        return False
    if not_TEX_asset:
        if fix:
            raise_warning_dialog(None, u'以下资产不是材质资产！！:\n%s' % not_TEX_asset)
        return False
    # if wrong_path_references:
    #     if fix:
    #         raise_warning_dialog(None, u'以下资产将被替换为I盘的资产:\n%s' % wrong_path_references)
    #         for each_ref in wrong_path_references:
    #             try:
    #                 ref_nod = all_references[each_ref]
    #                 name_en = each_ref.split('/')[-1].split('.')[0]
    #                 new_ref_path = ''.join(['I:/', dsf_db.searchTaskInfoDict(name_en)['path'], '/', name_en, '.ma'])
    #                 if not os.path.isfile(new_ref_path):
    #                     raise KeyError
    #                 mel.eval('file -loadReference {} -type "mayaAscii" -options "v=0;" {};'.format(ref_nod, new_ref_path))
    #             except KeyError:
    #                 raise_warning_dialog(None, u'该资产在I盘不存在！请通报制片！:\n%s' % each_ref)
    #                 return False
    #     return False
    return True


def check_file_path_func(fix=False):
    wrong_nodes = []
    # 检查贴图路径
    all_files_nodes = mc.ls(type='file')
    if all_files_nodes:
        wrong_file_nodes = [fn for fn in all_files_nodes if '%' not in pm.getAttr(fn+'.fileTextureName') and
                            pm.getAttr(fn+'.fileTextureName').split(':')[0] not in ['V', 'I']]
        wrong_nodes.extend(wrong_file_nodes)
        # if fix:
        #     if wrong_file_nodes:
        #         mel.eval('FilePathEditor;')
        #         raise_warning_dialog(None, u'以下贴图路径错误！已为你打开FilePathEditor，请查看:\n%s' % wrong_file_nodes)
        #         return False
        # else:
        #     return False
    # 检查声音路径
    all_audio_nodes = mc.ls(type='audio')
    if all_audio_nodes:
        wrong_audio_nodes = [fn for fn in all_audio_nodes if '%' not in pm.getAttr(fn + '.filename') or
                            pm.getAttr(fn + '.filename').split(':')[0] not in ['V', 'I']]
        wrong_nodes.extend(wrong_audio_nodes)
        # if fix:
        #     if wrong_audio_nodes:
        #         raise_warning_dialog(None, u'以下音频路径错误！已为你打开FilePathEditor，请查看:\n%s' % wrong_audio_nodes)
        #         return False
        # else:
        #     return False
    # 检查缓存路径
    all_cache_nodes = mc.ls(type='gpuCache') or []
    all_abc_nodes = mc.ls(type='AlembicNode') or []
    if all_cache_nodes + all_abc_nodes:
        wrong_cache_nodes = [fn for fn in all_cache_nodes if
                             '%' not in pm.getAttr(fn + '.cacheFileName') or pm.getAttr(fn + '.cacheFileName').split(':')[
                                 0] not in ['V', 'I']]
        wrong_abc_nodes = [a for a in all_abc_nodes if
                             '%' not in pm.getAttr(a + '.abc_File') or pm.getAttr(a + '.abc_File').split(':')[
                                 0] not in ['V', 'I']]
        wrong_nodes.extend(wrong_cache_nodes)
        wrong_nodes.extend(wrong_abc_nodes)
        # if fix:
        #     if wrong_cache_nodes:
        #         raise_warning_dialog(None, u'以下缓存路径错误！已为你打开FilePathEditor，请查看:\n%s' % wrong_cache_nodes)
        #         return False
        # else:
        #     return False
    if fix:
        for each in all_files_nodes:
            old_path = pm.getAttr(each + '.fileTextureName')
            new_path = old_path.replace('V:/', 'I:/')
            new_path = new_path.replace('V:\\', 'I:\\')
            pm.setAttr(each + '.fileTextureName', new_path)
        for each2 in all_audio_nodes:
            old_path = pm.getAttr(each2 + '.filename')
            new_path = old_path.replace('V:/', 'I:/')
            new_path = new_path.replace('V:\\', 'I:\\')
            pm.setAttr(each2 + '.filename', new_path)
        # for each3 in all_cache_nodes:
        #     old_path = pm.getAttr(each3 + '.cacheFileName')
        #     new_path = old_path.replace('V:/', 'I:/')
        #     new_path = new_path.replace('V:\\', 'I:\\')
        #     pm.setAttr(each3 + '.cacheFileName', new_path)
        # for each4 in all_abc_nodes:
        #     old_path = pm.getAttr(each4 + '.abc_File')
        #     new_path = old_path.replace('V:/', 'I:/')
        #     new_path = new_path.replace('V:\\', 'I:\\')
        #     pm.setAttr(each4 + '.abc_File', new_path)
    if wrong_nodes:
        if fix:
            raise_warning_dialog(None, u'以下路径错误！已为你打开FilePathEditor，请查看:\n%s' % wrong_nodes)
            mel.eval('FilePathEditor;')
        return False
    return True


def check_cam_func(fix=False):
    std_cams = [c for c in mc.ls('*.StandardCamera') if 'Camera_Ctrl' not in c]
    if not std_cams:
        if fix:
            raise_warning_dialog(None, u'未发现标准相机！请检查...')
        return False
    if len(std_cams) > 1:
        if fix:
            mc.select([cam.split('.')[0] for cam in std_cams], r=True)
            raise_warning_dialog(None, u'发现多个标准相机！请检查..\n%s' % std_cams)
        return False
    # if not mc.file(q=True, sn=True):
    #     mel.eval('file -f -save  -options "v=0;";')
    # file_name_en_temp = mc.file(q=True, sn=True, shn=True).split('Ly')
    # file_name_en = ''
    # if len(file_name_en_temp) > 1:
    #     file_name_en = file_name_en_temp[-1]
    # cams = mc.ls(mc.file(q=True, sn=True, shn=True).split('.')[0].strip(file_name_en))
    # if not cams:
    #     if fix:
    #         raise_warning_dialog(None, u'请检查相机名称！！正确格式为：\ns01_001_Ly')
    #     return False
    # if len(cams) > 1:
    #     if fix:
    #         mc.select(cams, r=True)
    #         raise_warning_dialog(None, u'发现多个物体与相机重名！！请检查..\n%s' % cams)
    #     return False
    # shape = pm.PyNode(cams[0]).getShape().name()
    # if mc.getAttr(shape+'.shakeEnabled') or mc.getAttr(shape+'.shakeOverscanEnabled'):
    #     if fix:
    #         mc.select(shape, r=True)
    #         raise_warning_dialog(None, u'相机的shakeEnabled属性和shakeOverscanEnabled被打开！！请检查..\n%s' % shape)
    #     return False
    # if not mc.getAttr(shape+'.cameraAperture') == [(0.864, 0.63)]:
    #     if fix:
    #         mc.select(shape, r=True)
    #         raise_warning_dialog(None, u'相机的Film Gate属性不正确！！请检查..\n%s' % shape)
    #     return False
    # if not std_cams[0].split('.')[0] == mc.file(q=True, sn=True):
    #     mc.select(std_cams, r=True)
    #     raise_warning_dialog(None, u'发现相机与场景名不一致！请检查..\n%s' % std_cams)
    #     return False
    return True


# def check_ch_scaling_func(fix=False):
#     # all_constrain_ctrls = pm.ls('*:Constrain', type='transform')
#     # all_main_ctrls = pm.ls('*:Main', type='transform')
#     if not mc.objExists('CHAR'):
#         if fix:
#             raise_warning_dialog(None, u'未发现组CHAR！请检查...\n')
#         return False
#     chars = pm.listRelatives('CHAR', c=1) or []
#     wrong_scalings = []
#     for each in chars:
#         if not each.getScale() == [1.0, 1.0, 1.0]:
#             wrong_scalings.append(each)
#     if wrong_scalings:
#         if fix:
#             pm.select(wrong_scalings, r=True)
#             sel = mc.ls(sl=True)
#             raise_warning_dialog(None, u'以下角色存在缩放！请检查...\n%s' % sel)
#         return False
#     return True


def check_starting_frame_func(fix=False):
    start_frame = int(mc.playbackOptions(min=True, query=True))
    if not start_frame == 101:
        if fix:
            mc.playbackOptions(min=101)
            return True
        return False
    return True


def check_unknown_nodes_func(fix=False):
    all_unknown_nodes = mc.ls(type='unknown') or []
    expression = mc.ls(type='expression') or []
    all_unknown_nodes.extend(expression)
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


def check_unknown_plugins_func(fix=False):
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


def check_extra_wins_func(fix=False):
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


def check_display_mode_func(fix=False):
    mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    mel.eval('DisplayWireframe;')
    return True


# def check_double_references_func(fix=False):
#     if fix:
#         try:
#             mel.eval('file -f -save  -options "v=0;";')
#         except RuntimeError:
#             raise_warning_dialog(None, u"请先手动另存文件！")
#             return False
#     try:
#         all_chars = mc.listRelatives('CHAR', c=1, pa=1) or []
#         all_props = mc.listRelatives('PROP', c=1, pa=1) or []
#         all_envs = mc.listRelatives('ENV', c=1, pa=1) or []
#     except ValueError:
#         return False
#     all_assets = all_chars + all_props + all_envs
#     if not all_assets:
#         return True
#     wrong_assets = []
#     for each in all_assets:
#         if len(each.split(":")) > 2:
#             wrong_assets.append(each)
#     all_assets_files = [mc.referenceQuery(each, f=1) for each in wrong_assets]
#     all_repeat_file = [f for f in all_assets_files if '{' in f]
#     if wrong_assets:
#         if fix:
#             if all_repeat_file:
#                 raise_warning_dialog(None, u'以下角色重复引用且含有双重名称空间！请先手动导动画处理...\n%s' % all_repeat_file)
#                 return False
#             raise_warning_dialog(None, u"此操作将重新打开该文件。")
#             if not mc.file(q=True, sn=True):
#                 try:
#                     mel.eval('file -f -save  -options "v=0;";')
#                 except RuntimeError:
#                     raise_warning_dialog(None, u"请先手动另存文件！")
#                     return False
#             file_path = mc.file(q=True, sn=True)
#             result = fix_double_namespaces.fix_double_namespaces(file_path)
#             if result:
#                 mel.eval("file -force -open \"%s\";" % file_path)
#             return True
#         return False


















