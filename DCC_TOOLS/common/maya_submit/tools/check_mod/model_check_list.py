#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/11
import os
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import check_utils
import loadUiType
import sys

check_util = check_utils.modCheckToolsUI()
kwRemoveNamespaces = str(os.path.split(os.path.realpath(__file__))[0]).replace("\\", "/") + '/kwRemoveNamespaces.mel'


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
    res = []
    for i in list_:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


def get_meshes_band():
    mc.warning(u'正在分析模型, 请稍等...')
    all_mesh = pm.ls(type='mesh')
    all_mesh_transforms = [each.getParent().name() for each in all_mesh]
    if len(all_mesh_transforms) < 2:
        return
    return_list = list()
    for i in xrange(len(all_mesh_transforms)-1):
        j = i + 1
        while j < len(all_mesh_transforms):
            return_list.append((all_mesh_transforms[i], all_mesh_transforms[j]))
            j += 1
    return return_list


def get_all_mesh_transforms_pm():
    all_mesh = pm.ls(type='mesh')
    all_mesh_transforms = [each.getParent() for each in all_mesh]
    return all_mesh_transforms


def get_all_mesh_transforms_mc():
    all_mesh = pm.ls(type='mesh')
    all_mesh_transforms = [each.getParent().name() for each in all_mesh]
    return all_mesh_transforms


def get_all_meshes_pm():
    return pm.ls(type='mesh')


def get_all_meshes_mc():
    return [each.name() for each in pm.ls(type='mesh')]


def get_all_transforms_pm():
    all_transforms1 = pm.ls(type='transform')
    all_transforms = [each for each in all_transforms1 if not pm.nodeType(each.getShape()) == 'camera']
    return all_transforms


def get_all_transforms_mc():
    all_transforms1 = pm.ls(type='transform')
    all_transforms = [each.name() for each in all_transforms1 if not pm.nodeType(each.getShape()) == 'camera']
    return all_transforms


@undoable
def check_naming_rules_func():
    all_transforms = get_all_transforms_mc()
    all_mesh_transforms = get_all_mesh_transforms_mc()
    all_grps = [each for each in all_transforms if each not in all_mesh_transforms]
    for each_m in all_mesh_transforms:
        extra_str = each_m.split("_Geo")[-1]
        if extra_str:
            if not mc.objExists(extra_str+"_Geo"):
                mc.rename(each_m, each_m.replace("_Geo"+extra_str, extra_str+"_Geo"))
            else:
                mc.rename(each_m, each_m.replace("_Geo" + extra_str, '_' + extra_str + "_Geo"))
    for each_g in all_grps:
        extra_str = each_g.split("_Grp")[-1]
        if extra_str:
            if not mc.objExists(extra_str+"_Grp"):
                mc.rename(each_g, each_g.replace("_Grp" + extra_str, extra_str + "_Grp"))
            else:
                mc.rename(each_g, each_g.replace("_Grp" + extra_str, '_'+extra_str + "_Grp"))
    return None


def fix_naming_rules_func():
    pass


# def check_delete_namespace_func():
#     mel.eval("source %s;" % kwRemoveNamespaces)
#     undeleted_namespaces = mel.eval("kwRemoveNamespaces;")
#     if undeleted_namespaces:
#         return u"以下namespaces未移除！请确认是否是引用节点..." % undeleted_namespaces
#     return None
#
#
# def fix_delete_namespace_func():
#     return u'请手动处理！'


def check_unit_func():
    current_unit = mc.currentUnit(q=True, linear=True)
    if not current_unit == "cm":
        return u"当前单位是%s，设置不正确！" % current_unit
    else:
        return None


def fix_unit_func():
    return u"请手动进设置进行更改！"


def check_blendshape_func():
    blendshape_nodes = mc.ls(type='blendShape')
    if not blendshape_nodes:
        return None
    else:
        return u'存在以下blendshape节点！%s' % blendshape_nodes


def fix_blendshape_func():
    mc.delete(mc.ls(type='blendShape'))
    return None


def check_intersection_func():
    all_intersection_faces = list()
    meshes_band = get_meshes_band()
    if not meshes_band:
        return None
    for each in meshes_band:
        mc.select(each, r=True)
        check_util.meshIntersectTest()
        intersection_faces = mc.ls(sl=True)
        if intersection_faces:
            all_intersection_faces.append(intersection_faces)
    if all_intersection_faces:
        mc.select(flat(all_intersection_faces), r=True)
        return u'发现以下穿插面，请选择在场景中查看%s' % all_intersection_faces
    return None


def fix_intersection_func():
    return u'请在场景中查看！'


def check_more_faces_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"0\",\"0\",\"1\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\","
             "\"0\",\"1e-005\",\"0\",\"-1\",\"0\",\"0\" };")
    all_more_faces = mc.ls(sl=True)
    if all_more_faces:
        return u"发现以下面多于四个边：\n%s" % all_more_faces
    else:
        return None


def fix_more_faces_func():
    return u'请选择在场景中查看！'


def check_more_cvs_func():
    all_more_cvs = list()
    meshes_band = get_meshes_band()
    if not meshes_band:
        return None
    for each in meshes_band:
        mc.select(each, r=True)
        check_util.selectUnqualVertex()
        more_cvs = mc.ls(sl=True)
        if more_cvs:
            all_more_cvs.append(more_cvs)
    if all_more_cvs:
        mc.select(flat(all_more_cvs), r=True)
        return u'发现以下非四边点，请选择在场景中查看%s' % all_more_cvs
    return None


def fix_more_cvs_func():
    return u'请选择在场景中查看！'


def check_lamina_faces_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\","
             "\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"1\",\"0\" };")
    all_lamina_faces = mc.ls(sl=True)
    if all_lamina_faces:
        return u"发现以下重合面%s" % all_lamina_faces
    else:
        return None


def fix_lamina_faces_func():
    return u"请在场景中查看！"


def check_nonmanifold_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\","
             "\"1e-005\",\"0\",\"1e-005\",\"0\",\"1\",\"0\",\"0\" };")
    all_nonmanifold_faces = mc.ls(sl=True)
    if all_nonmanifold_faces:
        return u"发现以下非歧义面%s" % all_nonmanifold_faces
    else:
        return None
    
    
def fix_nonmanifold_func():
    return u"请在场景中查看！"


def check_nonplanar_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"1\",\"0\",\"0\",\"0\",\"0\",\"1\",\"0\",\"1e-005\",\"0\","
             "\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\",\"0\" };")
    all_nonplanar_faces = mc.ls(sl=True)
    if all_nonplanar_faces:
        return u"发现以下不平的面%s" % all_nonplanar_faces
    else:
        return None


def fix_nonplanar_func():
    return u"请在场景中查看！"


def check_holes_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"1\",\"0\",\"0\",\"0\",\"1\",\"0\",\"0\",\"1e-005\",\"0\","
             "\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\",\"0\" };")
    all_holes_faces = mc.ls(sl=True)
    if all_holes_faces:
        return u"发现以下带洞的面%s" % all_holes_faces
    else:
        return None


def fix_holes_func():
    return u"请在场景中查看！"


def check_concave_func():
    mc.select(cl=1)
    mel.eval("polyCleanupArgList 4 { \"1\",\"2\",\"1\",\"0\",\"0\",\"1\",\"0\",\"0\",\"0\",\"1e-005\",\"0\","
             "\"1e-005\",\"0\",\"1e-005\",\"0\",\"-1\",\"0\",\"0\" };")
    all_concave_faces = mc.ls(sl=True)
    if all_concave_faces:
        return u"发现以下凹面%s" % all_concave_faces
    else:
        return None


def fix_concave_func():
    return u"请在场景中查看！"


def check_nouv_faces_func():
    all_meshes = get_all_meshes_pm()
    all_meshes_with_no_uvs = list()
    for each in all_meshes:
        uv = each.numUVs()
        if not uv:
            all_meshes_with_no_uvs.append(each.name())
    if all_meshes_with_no_uvs:
        mc.select(all_meshes_with_no_uvs, r=True)
        return u"发现以下模型没有UV，请在场景中查看:\n%s" % all_meshes_with_no_uvs
    else:
        return None


def fix_nouv_faces_func():
    return u"请在场景中查看！"


def check_render_stats_func():
    check_dict = {'.castsShadows': 1, '.receiveShadows': 1, '.holdOut': 0, '.motionBlur': 1, '.primaryVisibility': 1,
                  '.smoothShading': 1, '.visibleInReflections': 1, '.visibleInRefractions': 1, '.doubleSided': 1,
                  '.geometryAntialiasingOverride': 0, '.shadingSamplesOverride': 0}
    all_meshes = get_all_meshes_mc()
    all_meshes_with_wrong_render_stats = list()
    for each_mesh in all_meshes:
        for k, v in check_dict.iteritems():
            if mc.getAttr(each_mesh+k) != v:
                all_meshes_with_wrong_render_stats.append(each_mesh)
    if all_meshes_with_wrong_render_stats:
        mc.select(all_meshes_with_wrong_render_stats, r=True)
        return u"发现以下模型的渲染属性不正确，是否设置成正确？\n%s" % all_meshes_with_wrong_render_stats
    else:
        return None


def fix_render_stats_func():
    check_dict = {'.castsShadows': 1, '.receiveShadows': 1, '.holdOut': 0, '.motionBlur': 1, '.primaryVisibility': 1,
                  '.smoothShading': 1, '.visibleInReflections': 1, '.visibleInRefractions': 1, '.doubleSided': 1,
                  '.geometryAntialiasingOverride': 0, '.shadingSamplesOverride': 0}
    all_meshes = get_all_meshes_mc()
    for each_mesh in all_meshes:
        for k, v in check_dict.iteritems():
            mc.setAttr(each_mesh + k, v)
    return None


def check_normal_func():
    all_transforms = get_all_meshes_mc()
    if not all_transforms:
        return None
    mc.select(all_transforms, r=True)
    mel.eval('polyNormalPerVertex -ufn true;')
    return None


def fix_normal_func():
    pass


def check_freeze_func():
    attr_dict = ['.t', '.r', '.s']
    all_transforms = get_all_transforms_mc()
    wrong_transforms = list()
    for each in all_transforms:
        sum_ = 0
        for attr in attr_dict:
            sum_ += sum(mc.getAttr(each+attr)[0])
        if sum_ != 3.0:
            wrong_transforms.append(each)
    if wrong_transforms:
        mc.select(wrong_transforms, r=True)
        return u"发现以下模型未Freeze，是否Freeze？\n%s" % wrong_transforms
    return None


def fix_freeze_func():
    mel.eval('SelectAll;')
    mel.eval('FreezeTransformations;')
    return None


def check_anicrv_func():
    all_anicrvs = mc.ls(type='animCurve')
    hardware_anicrv = []
    if all_anicrvs:
        for each in all_anicrvs:
            if 'hardware' not in each:
                try:
                    mc.delete(each)
                    print u"删除了动画曲线: %s" % each
                except:
                    continue
            else:
                hardware_anicrv.append(each)
    if hardware_anicrv:
        return u'发现以下硬件雾关键帧！请导出文件再继续执行检查...\n %s ' % hardware_anicrv
    return None


def fix_anicrv_func():
    return u'请导出文件再继续操作！'


def check_pivot_func():
    all_transforms = get_all_transforms_pm()
    all_wrong_pivots = list()
    for each in all_transforms:
        pivot = each.getPivots(worldSpace=1)
        sum_ = sum(pivot[0]) + sum(pivot[1])
        if sum_:
            all_wrong_pivots.append(each.name())
    if all_wrong_pivots:
        mc.select(all_wrong_pivots, r=True)
        return u"发现以下节点轴心点未放到原点，是否处理？\n%s" % all_wrong_pivots
    return None


def fix_pivot_func():
    all_transforms = get_all_transforms_pm()
    for each in all_transforms:
        each.setPivots((0, 0, 0), worldSpace=1)
    return None


def check_lock_hide_func():
    keyable_attr = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.visibility']
    all_transforms = get_all_transforms_mc()
    wrong_transforms = list()
    for each in all_transforms:
        multi_temp = 1
        for attr in keyable_attr:
            multi_temp *= mc.getAttr(each+attr, k=True)
            multi_temp *= mc.getAttr(each+attr, se=True)
        if not multi_temp:
            wrong_transforms.append(each)
    if wrong_transforms:
        mc.select(wrong_transforms, r=True)
        return u"发现以下物体属性栏属性错误，是否修正？\n%s" % wrong_transforms
    return None


def fix_lock_hide_func():
    keyable_attr = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.visibility']
    all_transforms = get_all_transforms_mc()
    for each in all_transforms:
        for attr in keyable_attr:
            mc.setAttr(each + attr, keyable=1)
            mc.setAttr(each + attr, lock=0)
    return None


def check_namespace_func():
    all_transforms = get_all_transforms_mc()
    all_meshes = get_all_meshes_mc()
    all_transforms.extend(all_meshes)
    wrong_names = list()
    for each in all_transforms:
        if ":" in each:
            wrong_names.append(each)
    if wrong_names:
        mc.select(wrong_names, r=True)
        return u'发现以下名称命名含有namespace，是否删除namespace？！\n%s' % wrong_names
    return None


def fix_namespace_func():
    try:
        mel.eval("source \"%s\";" % kwRemoveNamespaces)
        undeleted_namespaces = mel.eval("kwRemoveNamespaces;")
    except RuntimeError:
        return None
    if undeleted_namespaces:
        return u"以下namespaces未移除！请确认是否是引用节点...\n%s" % undeleted_namespaces
    return None


# def check_namespace_func():
#     all_transforms = get_all_transforms_mc()
#     all_meshes = get_all_meshes_mc()
#     all_transforms.extend(all_meshes)
#     wrong_names = list()
#     for each in all_transforms:
#         if ":" in each:
#             wrong_names.append(each)
#     if wrong_names:
#         mc.select(wrong_names, r=True)
#         return u'发现以下名称命名含有namespace，是否删除namespace？！\n%s' % wrong_names
#     return None
#
#
# def fix_namespace_func():
#     all_transforms = get_all_transforms_mc()
#     all_meshes = get_all_meshes_mc()
#     all_transforms.extend(all_meshes)
#     for each in all_transforms:
#         if ":" in each:
#             new_name = each.split(":")[-1]
#             mc.rename(each, new_name)
#     return None


def check_shape_name_func():
    all_transforms = get_all_transforms_pm()
    wrong_shape_names = list()
    for each in all_transforms:
        try:
            shape_name = each.getShape().name()
        except AttributeError:
            continue
        if not shape_name == each.name()+'Shape':
            wrong_shape_names.append(shape_name)
    if wrong_shape_names:
        mc.select(wrong_shape_names, r=True)
        return u'发现以下shape命名不正确！是否修改为正确？\n%s' % wrong_shape_names
    return None


def fix_shape_name_func():
    all_transforms = get_all_transforms_pm()
    for each in all_transforms:
        try:
            shape_name = each.getShape().name()
        except AttributeError:
            continue
        if not shape_name == each.name()+'Shape':
            mc.rename(shape_name, each.name()+'Shape')
    return None


def get_material_func():
    all_se = mc.ls(type='shadingEngine')
    all_needed_meterials_temp = [mc.listConnections(each, s=1, d=0) for each in all_se]
    all_needed_meterials = list(set(flat(all_needed_meterials_temp)))
    all_materials = mc.ls(mat=1)
    all_useless_materials = [every for every in all_materials if every not in all_needed_meterials]
    if all_useless_materials:
        return all_useless_materials
    return None


def check_material_func():
    all_useless_materials = get_material_func()
    if all_useless_materials:
        return u'发现以下没用的材质，是否删除？\n %s' % all_useless_materials
    return None


def fix_material_func():
    all_useless_materials = get_material_func()
    if all_useless_materials:
        try:
            mc.delete(all_useless_materials)
        except:
            pass
    return None


def check_unknown_nodes_func():
    extra_nodes_type = ['unknown', 'constraint', 'joint', 'nurbsCurve', 'locator', 'cluster', 'lattice', 'wrap',
                        'expression']
    all_unknown_nodes = []
    for each_type in extra_nodes_type:
        all_this_type_nodes = pm.ls(type=each_type)
        all_unknown_nodes.extend(all_this_type_nodes)
    if all_unknown_nodes:
        return u'发现以下未知节点，是否删除？\n%s' % all_unknown_nodes
    return None


def fix_unknown_nodes_func():
    extra_nodes_type = ['unknown', 'constraint', 'joint', 'nurbsCurve',
                        'locator', 'cluster', 'lattice', 'wrap', 'expression']
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


def check_unknown_plugins_func():
    unknown_plugins = mc.unknownPlugin(q=True, list=True)
    if unknown_plugins:
        return u'发现以下未知插件，是否移除？\n%s' % unknown_plugins
    return None


def fix_unknown_plugins_func():
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
    return None


def check_history_func():
    mel.eval('SelectAll')
    mel.eval('DeleteHistory;')
    return None


def fix_history_func():
    pass


def check_extra_wins_func():
    maya_window = loadUiType.getMayaWindow().objectName()
    all_windows = pm.lsUI(typ='window')
    window_remove = [maya_window]
    all_extra_windows = [w for w in all_windows if w not in window_remove]
    for each in all_extra_windows:
        try:
            mc.deleteUI(each)
        except:
            pass
    return None


def fix_extra_wins_func():
    pass


def check_display_mode_func():
    mel.eval('DisplayWireframe;')
    mel.eval('$gUseSaveScenePanelConfig = false; file -uc false;$gUseScenePanelConfig = false;file -uc false;')
    return None


def fix_display_mode_func():
    pass
