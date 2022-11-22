# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import os
import maya.OpenMaya as om
import shutil
import logging
from .. import dcc_utils
reload(dcc_utils)
try:
    from PySide2 import QtWidgets
except ImportError:
    import PySide.QtGui as QtWidgets


def check_wrap():
    def wrapper(func):
        def deal_check(item, fix=False):
            if not item.checkBox.isChecked():
                return
            func(item, fix)
            if item.error_list:
                item.setStyleSheet("color: rgb(255, 0, 0);")
                item.pushButton_select.setHidden(0)
                if item.fix:
                    item.pushButton_fix.setHidden(0)
                else:
                    item.pushButton_fix.setHidden(1)
            else:
                item.setStyleSheet("color: rgb(0, 255, 0);")
                item.pushButton_select.setHidden(1)
                item.pushButton_fix.setHidden(1)
        return deal_check
    return wrapper


@check_wrap()
def check_uv(item, fix=False):
    if fix:
        print "fix"
        #  这里需要处理一下item的颜色
        print item.error_list
        return
    allMesh = cmds.ls(type="mesh", fl=1, ni=1)
    item.error_list = []
    for mesh in allMesh:
        uvSets = cmds.polyUVSet(mesh, q=1, auv=1)
        if not uvSets or uvSets != ["map1"]:
            item.error_list.append(mesh)


@check_wrap()
def check_hierarchy_func(item, fix=False):
    legal_grps = ['CHAR', 'PROP', 'ENV', 'CAM', 'LAYOUT_FX', 'persp', 'top', 'front', 'side']

    def parent_tools():
        file_path = '/'.join([dcc_utils.get_dcc_tools_path(), 'AN', 'dazu'])
        mel.eval('source "%s/dazu.mel";' % file_path)
        mel.eval('dazumel;')
    # 检查最上层大纲层级是否符合规范
    all_main_hierarchys = mc.ls(assemblies=True)
    illegal_assemblies = [ass.encode('utf-8') for ass in all_main_hierarchys if ass not in legal_grps]
    missing_assemblies = [ms.encode('utf-8') for ms in legal_grps if ms not in all_main_hierarchys]
    if illegal_assemblies:
        item.error_list.extend(illegal_assemblies)
        if fix:
            mc.select(illegal_assemblies, r=True)
            text = u'大纲下存在以下非法层级，请检查:\n%s' % illegal_assemblies
            dcc_utils.raise_warning_dialog(text)
            parent_tools()
        return False
    if missing_assemblies:
        if fix:
            text = u'大纲缺失以下层级，请检查:\n%s' % missing_assemblies
            dcc_utils.raise_warning_dialog(text)
            parent_tools()
        return False
    # 变色
    # item.setStyleSheet("color: rgb(0, 255, 0);")


@check_wrap()
def check_reference_func(item, fix=False):
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
    if os.environ['oct_launcher_using_mode'] in ['online']:
        from utils import shotgun_operations
        sg = shotgun_operations
        for ref in display_refs:
            #  判断未勾选资产
            if not mc.referenceQuery(ref, il=True):
                unload_refs.append(ref)
                continue
            # 这里需要写判断这个路径是否在shotgun的Version表里， 并且资产必须锁定版本
            project_name = sg.get_project()
            version_info = sg.find_shotgun("Version", [["sg_path_to_frames", "is", ref], [
                'project', 'name_is', project_name], ["sg_version_type", "is", "Publish"]], ["id"])
            if not version_info:
                illegal_references.append(ref)
    if unload_refs:
        if fix:
            text = u'以下资产未勾选！请检查:\n%s' % unload_refs
            dcc_utils.raise_warning_dialog(text)
        return False
    if illegal_references:
        item.error_list.extend(illegal_references)
        if fix:
            text = u'以下资产未锁定！请通知资产部门进行版本锁定:\n%s' % illegal_references
            dcc_utils.raise_warning_dialog(text)
        return False
    # item.setStyleSheet("color: rgb(0, 255, 0);")
    return True


@check_wrap()
def check_locked_reference_func(item, fix=False):
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
    if os.environ['oct_launcher_using_mode'] in ['online']:
        from utils import shotgun_operations
        sg = shotgun_operations
        unlocked_reference = []
        project_name = sg.get_project()
        for ref in display_refs:
            version_info = sg.find_shotgun("Version", [["sg_path_to_frames", "is", ref], [
                'project', 'name_is', project_name], ["sg_version_type", "is", "Publish"]],
                ["sg_version_number", "sg_task.Task.sg_publish_version", "sg_task.Task.id", "entity"])
            if version_info:
                if version_info[0]["sg_version_number"] != version_info[0]["sg_task.Task.sg_publish_version"]:
                    unlocked_reference_dict = {}  # 初始化字典
                    unlocked_reference_dict.setdefault(ref, []).append(version_info[0]["sg_task.Task.sg_publish_version"])  # 格式化字典
                    unlocked_reference_dict.setdefault(ref, []).append(version_info[0]["sg_task.Task.id"])
                    unlocked_reference.append(unlocked_reference_dict)
        if unlocked_reference:
            item.error_list.extend(unlocked_reference)
            if fix:
                mfile = om.MFileIO()
                current_file = mfile.currentFile()
                file_path = os.path.split(current_file)[0]
                suffix = os.path.splitext(current_file)[-1]
                file_name = os.path.split(current_file)[-1]
                old_file_path = file_path + "/" + file_name.replace(suffix, "") + "_old.ma"
                try:
                    shutil.copyfile(current_file, old_file_path)
                except Exception as e:
                    print e
                for reference in unlocked_reference:
                    for k, v in reference.items():
                        ref = k
                        latestversion = v[0]
                        _id = v[1]
                        frames_path = sg.find_one_shotgun("Version", [['project', 'name_is', project_name], [
                            "sg_version_type", "is", "Publish"], ['sg_task.Task.id', "is", _id],
                             ["sg_version_number", "is", latestversion]], ["sg_path_to_frames"])
                        new_reference_path = ''
                        if frames_path:
                            new_reference_path = frames_path["sg_path_to_frames"]
                        reference_node = all_references[ref]
                        mc.file(new_reference_path, loadReference=reference_node, type="mayaAscii", options="v=0;")
                mc.file(save=True)
            return False
    else:
        if fix:
            logging.error(u'当前为离线模式，无法检查是否是锁定资产！')
            # raise RuntimeError(u'当前为离线模式，无法检查是否是锁定资产！')
        return False
    item.setStyleSheet("color: rgb(0, 255, 0);")
    return True


@check_wrap()
def check_file_path_func(item, fix=False):
    wrong_nodes = []
    # 检查贴图路径
    all_files_nodes = mc.ls(type='file')
    if all_files_nodes:
        wrong_file_nodes = [fn for fn in all_files_nodes if '%' not in pm.getAttr(fn+'.fileTextureName') and
                            pm.getAttr(fn+'.fileTextureName').split(':')[0] not in ['V', 'I']]
        wrong_nodes.extend(wrong_file_nodes)
        item.error_list.extend(wrong_file_nodes)
    # 检查声音路径
    all_audio_nodes = mc.ls(type='audio')
    if all_audio_nodes:
        wrong_audio_nodes = [fn for fn in all_audio_nodes if '%' not in pm.getAttr(fn + '.filename') or
                            pm.getAttr(fn + '.filename').split(':')[0] not in ['V', 'I']]
        wrong_nodes.extend(wrong_audio_nodes)
        item.error_list.extend(wrong_audio_nodes)
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
        item.error_list.extend(wrong_cache_nodes)
        item.error_list.extend(wrong_abc_nodes)
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
        for each3 in all_cache_nodes:
            old_path = pm.getAttr(each3 + '.cacheFileName')
            new_path = old_path.replace('V:/', 'I:/')
            new_path = new_path.replace('V:\\', 'I:\\')
            pm.setAttr(each3 + '.cacheFileName', new_path)
        for each4 in all_abc_nodes:
            old_path = pm.getAttr(each4 + '.abc_File')
            new_path = old_path.replace('V:/', 'I:/')
            new_path = new_path.replace('V:\\', 'I:\\')
            pm.setAttr(each4 + '.abc_File', new_path)
    if wrong_nodes:
        if fix:
            text = u'以下路径错误！已为你打开FilePathEditor，请查看:\n%s' % wrong_nodes
            dcc_utils.raise_warning_dialog(text)
            mel.eval('FilePathEditor;')
        return False
    # item.setStyleSheet("color: rgb(0, 255, 0);")
    return True


# --------------------------------------
@check_wrap()
def check_cam_func(item, fix=False):
    std_cams = [c for c in mc.ls('*.StandardCamera') if 'Camera_Ctrl' not in c]
    if not std_cams:
        if fix:
            text = u'未发现标准相机！请检查...'
            dcc_utils.raise_warning_dialog(text)
        return False
    if len(std_cams) > 1:
        if fix:
            mc.select([cam.split('.')[0] for cam in std_cams], r=True)
            text = u'发现多个标准相机！请检查..\n%s' % std_cams
            dcc_utils.raise_warning_dialog(text)
        return False
    if not mc.file(q=True, sn=True):
        mel.eval('file -f -save  -options "v=0;";')
    file_name_en_temp = mc.file(q=True, sn=True, shn=True).split('An')
    file_name_en = ''
    if len(file_name_en_temp) > 1:
        file_name_en = file_name_en_temp[-1]
    cams = mc.ls(mc.file(q=True, sn=True, shn=True).split('.')[0].strip(file_name_en))
    if not cams:
        if fix:
            text = u'请检查相机名称！！正确格式为：\ns01_001_An'
            dcc_utils.raise_warning_dialog(text)
        return False
    if len(cams) > 1:
        if fix:
            mc.select(cams, r=True)
            text = u'发现多个物体与相机重名！！请检查..\n%s' % cams
            dcc_utils.raise_warning_dialog(text)
        return False
    shape = pm.PyNode(cams[0]).getShape().name()
    if mc.getAttr(shape+'.shakeEnabled') or mc.getAttr(shape+'.shakeOverscanEnabled'):
        if fix:
            mc.select(shape, r=True)
            text = u'相机的shakeEnabled属性和shakeOverscanEnabled被打开！！请检查..\n%s' % shape
            dcc_utils.raise_warning_dialog(text)
        return False
    if not mc.getAttr(shape+'.cameraAperture') == [(0.864, 0.63)]:
        if fix:
            mc.select(shape, r=True)
            text = u'相机的Film Gate属性不正确！！请检查..\n%s' % shape
            dcc_utils.raise_warning_dialog(text)
        return False
    return True


@check_wrap()
def check_ch_scaling_func(item, fix=False):
    if not mc.objExists('CHAR'):
        if fix:
            text = u'未发现组CHAR！请检查...\n'
            dcc_utils.raise_warning_dialog(text)
        return False
    chars = pm.listRelatives('CHAR', c=1) or []
    wrong_scalings = []
    for each in chars:
        if not each.getScale() == [1.0, 1.0, 1.0]:
            wrong_scalings.append(each)
            item.error_list.extend(wrong_scalings)
    if wrong_scalings:
        if fix:
            pm.select(wrong_scalings, r=True)
            sel = mc.ls(sl=True)
            text = u'以下角色存在缩放！请检查...\n%s' % sel
            dcc_utils.raise_warning_dialog(text)
            item.error_list.extend(sel)
        return False
    return True


# --------------------------------------
@check_wrap()
def check_starting_frame_func(item, fix=False):
    start_frame = int(mc.playbackOptions(min=True, query=True))
    if not start_frame == 101:
        if fix:
            mc.playbackOptions(min=101)
            return True
        return False
    return True


# --------------------------------------
@check_wrap()
def check_unknown_nodes_func(item, fix=False):
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


# --------------------------------------
@check_wrap()
def check_unknown_plugins_func(item, fix=False):
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


@check_wrap()
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


@check_wrap()
def check_display_mode_func(fix=False):
    mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    mel.eval('DisplayWireframe;')
    return True


@check_wrap()
def check_double_references_func(item, fix=False):
    if fix:
        try:
            mel.eval('file -f -save  -options "v=0;";')
        except RuntimeError:
            text = u"请先手动另存文件！"
            dcc_utils.raise_warning_dialog(text)
            return False
    try:
        all_chars = mc.listRelatives('CHAR', c=1, pa=1) or []
        all_props = mc.listRelatives('PROP', c=1, pa=1) or []
        all_envs = mc.listRelatives('ENV', c=1, pa=1) or []
    except ValueError:
        return False
    all_assets = all_chars + all_props + all_envs
    if not all_assets:
        return True
    wrong_assets = []
    for each in all_assets:
        if len(each.split(":")) > 2:
            wrong_assets.append(each)
    all_assets_files = [mc.referenceQuery(each, f=1) for each in wrong_assets]
    all_repeat_file = [f for f in all_assets_files if '{' in f]
    if wrong_assets:
        if fix:
            if all_repeat_file:
                item.error_list.extend(all_repeat_file)
                text = u'以下角色重复引用且含有双重名称空间！请先手动导动画处理...\n%s' % all_repeat_file
                dcc_utils.raise_warning_dialog(text)
                return False
            text = u"此操作将重新打开该文件。"
            dcc_utils.raise_warning_dialog(text)
            if not mc.file(q=True, sn=True):
                try:
                    mel.eval('file -f -save  -options "v=0;";')
                except RuntimeError:
                    text = u"请先手动另存文件！"
                    dcc_utils.raise_warning_dialog(text)
                    return False
            file_path = mc.file(q=True, sn=True)
            result = dcc_utils.fix_double_namespaces(file_path)
            if result:
                mel.eval("file -force -open \"%s\";" % file_path)
            return True
        return False


# --------------------------------------
@check_wrap()
def check_tex_hierarchy_func(item, fix=False):
    # 检查最上层大纲层级是否符合规范
    camera_grp = {'persp', 'top', 'front', 'side'}
    all_top_grp = mc.ls(assemblies=True)
    asset = list(set(all_top_grp) - camera_grp)
    if len(asset) != 1:
        if fix:
            text = u'大纲层级数量不正确！！\n %s' % asset
            dcc_utils.raise_warning_dialog(text)
        return False
    asset_name = asset[0]
    if mc.objExists('blendshape'):
        if fix:
            mc.delete('blendshape')
        else:
            return False
    if len(mc.listRelatives(asset_name, c=1)) != 1 or mc.listRelatives(asset_name, c=1)[0] != 'Geometry':
        text = u'大纲层级不正确！请检查...'
        dcc_utils.raise_warning_dialog(text)
        return False
    return True


# ----------------------
@check_wrap()
def check_history_func(item, fix=False, kwargs=None):
    mel.eval('SelectAll')
    mel.eval('DeleteHistory;')
    return True


# ----------------------
@check_wrap()
def check_hide_mod_func(item, fix=False, kwargs=None):
    all_hide_meshes = [m for m in dcc_utils.get_all_mesh_transform() if not m.v.get()]
    if all_hide_meshes:
        if fix:
            pm.select(all_hide_meshes, r=True)
            text = u'已为你选中隐藏的模型\n%s' % reformat_list(all_hide_meshes)
            dcc_utils.raise_warning_dialog(text)
        return False
    return True


check_cfg = {
            'common': [],
            'mod': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},
                    {'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},
                    ],
            'rig': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},

                    ],
            'tex': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},

                    ],
            'ly': [{'label': u"检查层级", "value": check_hierarchy_func, "fix": 1, "icon": ""},
                   {'label': u"检查Reference", "value": check_reference_func, "fix": 1, "icon": ""},
                   {'label': u"检查贴图，缓存，声音路径", "value": check_file_path_func, "fix": 1, "icon": ""},
                   {'label': u"检查相机", "value": check_cam_func, "fix": 1, "icon": ""},
                   {'label': u"检查角色缩放", "value": check_ch_scaling_func, "fix": 1, "icon": ""},
                   {'label': u"检查开始帧", "value": check_starting_frame_func, "fix": 1, "icon": ""},
                   {'label': u"检查未知节点", "value": check_unknown_nodes_func, "fix": 1, "icon": ""},
                   {'label': u"检查未知插件", "value": check_unknown_plugins_func, "fix": 1, "icon": ""},
                   {'label': u"关闭多余窗口", "value": check_extra_wins_func, "fix": 1, "icon": ""},
                   {'label': u"更改显示模式", "value": check_display_mode_func, "fix": 1, "icon": ""},
                   {'label': u"检查双重引用", "value": check_double_references_func, "fix": 1, "icon": ""},

                   ],
            'an': [{'label': u"检查层级", "value": check_hierarchy_func, "fix": 1, "icon": ""},
                   {'label': u"检查Reference", "value": check_reference_func, "fix": 1, "icon": ""},
                   {'label': u"锁定最新版本资产", "value": check_locked_reference_func, "fix": 1, "icon": ""},
                   {'label': u"检查贴图，缓存，声音路径", "value": check_file_path_func, "fix": 1, "icon": ""},
                   {'label': u"检查相机", "value": check_cam_func, "fix": 1, "icon": ""},
                   {'label': u"检查角色缩放", "value": check_ch_scaling_func, "fix": 1, "icon": ""},
                   {'label': u"检查开始帧", "value": check_starting_frame_func, "fix": 1, "icon": ""},
                   {'label': u"检查未知节点", "value": check_unknown_nodes_func, "fix": 1, "icon": ""},
                   {'label': u"检查未知插件", "value": check_unknown_plugins_func, "fix": 1, "icon": ""},
                   {'label': u"关闭多余窗口", "value": check_extra_wins_func, "fix": 1, "icon": ""},
                   {'label': u"更改显示模式", "value": check_display_mode_func, "fix": 1, "icon": ""},
                   {'label': u"检查双重引用", "value": check_double_references_func, "fix": 1, "icon": ""},
                   ],
            'fur': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},

                    ],
            'cloth': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},

                      ],
            'flo': [{'label': u"测试", "value": check_uv, "fix": 1, "icon": ""},

                    ]
            }
