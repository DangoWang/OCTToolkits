# -*- coding: utf-8 -*-

import os
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

def win():
    _win_name = "add_proxy_switch_ui"
    if cmds.window(_win_name, exists=1):
        cmds.deleteUI(_win_name)
    _win_name = cmds.window(_win_name, title=u"添加代理")
    lay_main = cmds.columnLayout(adj=1, rowSpacing=6)

    cmds.button(l=u"加载插件", command=load_mll)
    text_btn = cmds.textFieldButtonGrp(label=u'路径:', buttonLabel=' .. ', cw3=[30, 100, 20], adj=2)
    cmds.textFieldButtonGrp(text_btn, e=1, bc=partial(get_abc_path, text_btn), cc=partial(record_path, text_btn))
    if cmds.optionVar( ex='ProxySwitchPath' ):
        cmds.textFieldButtonGrp(text_btn, e=1, tx=cmds.optionVar( q='ProxySwitchPath' ))
    add_btn =  cmds.button(label=u"输出缓存", command=partial(export_abc, text_btn))
    ref_btn = cmds.button(l=u"切换", command = switch_proxy)
    ref_btn = cmds.button(l=u"切换GPU", command=partial(switch_proxy_gpu, text_btn))
    cmds.showWindow()

def load_mll(*args):
    if not cmds.pluginInfo('AbcImport', query=1, loaded=1):
        try:
            cmds.loadPlugin('AbcImport.mll')
        except RuntimeError:
            return

def get_abc_path(bt, *args):
    txt = cmds.fileDialog2(dialogStyle=2, fm=3)
    if txt:
        cmds.textFieldButtonGrp( bt, e=1, tx=txt[0] )
        record_path(bt)

def record_path(bt, *args):
    cmds.optionVar(sv=('ProxySwitchPath', cmds.textFieldButtonGrp(bt, q=1, tx=1)))

def get_sel_rn(*args):
    sel_list = cmds.ls(sl=1, long=1)
    rn_list = {}
    for sel in sel_list:
        try:
            rn = cmds.referenceQuery(sel, rfn=1)
            ns = cmds.referenceQuery(sel, ns=1)
            if not rn_list.has_key(rn):
                rn_list[rn] = ns
        except:
            continue
    return rn_list

def export_abc(btn, *args):
    rn_list = get_sel_rn()
    frame_st = cmds.playbackOptions(q=1, animationStartTime=1)
    frame_en = cmds.playbackOptions(q=1, animationEndTime=1)
    abc_pth = cmds.textFieldButtonGrp(btn, q=1, tx=1)
    for rn, ns in rn_list.items():
        pm = cmds.listConnections(rn, type="proxyManager") or []
        print pm
        obj = "{}:Geometry".format(ns)
        if not cmds.objExists(obj):
            continue
        # abc_job = '-frameRange {} {} -worldSpace -writeVisibility -dataFormat ogawa -root {}'.format(frame_st, frame_en, obj)
        cmds.gpuCache(obj, startTime=frame_st, endTime=frame_en, optimize=1, optimizationThreshold=40000,
                      writeMaterials=0, dataFormat="ogawa", directory=abc_pth, fileName=rn, writeUVs=1)
        abc_fle = os.path.join(abc_pth, "{}.abc".format(rn))
        # abc_job = '{} -file {}'.format(abc_job, abc_fle)
        # cmds.AbcExport(j=abc_job)
        if not pm:
            mel.eval('proxyAdd "{}" "{}" "";'.format(rn, abc_fle.replace("\\", "/")))

def switch_proxy(*args):
    sel_list = cmds.ls(sl=1)
    rn_fle = {}
    for sel in sel_list:
        rn = cmds.referenceQuery(sel, rfn=1)
        if not rn_fle.has_key(rn):
            rn_fle[rn] = cmds.referenceQuery(rn, filename=1)
    for rn, fle in rn_fle.items():
        pm = cmds.listConnections(rn, type="proxyManager") or []
        if not pm:
            continue
        active = cmds.listConnections("{}.activeProxy".format(pm[0]), plugs=1)[0]
        rn_node = cmds.listConnections(active)[0]
        # file_name = cmds.referenceQuery(rn, filename=1)
        # cmds.file(file_name, unloadReference=rn_node)
        new = active.replace(active[-2], str(1-int(active[-2])))
        new_node = cmds.listConnections(new)[0]
        mel.eval("proxySwitch {}".format(new_node))

def switch_proxy_gpu(btn, *args):
    abc_pth = cmds.textFieldButtonGrp(btn, q=1, tx=1)
    sel_list = cmds.ls(sl=1)
    rn_fle = {}
    for sel in sel_list:
        shape_sel = cmds.listRelatives(sel, shapes=1)[0]
        if cmds.nodeType(shape_sel) == "gpuCache":
            cmds.delete(sel)
            pm = cmds.listConnections(sel[0:-4], type="proxyManager") or []
            active = cmds.listConnections("{}.activeProxy".format(pm[0]), plugs=1)[0]
            activeRN = cmds.listConnections(active)[0]
            print activeRN
            cmds.file(loadReference=activeRN)
        else:
            rn = cmds.referenceQuery(sel, rfn=1)
            pm = cmds.listConnections(rn, type="proxyManager") or []
            if not pm:
                continue
            if not rn_fle.has_key(rn):
                rn_fle[rn] = cmds.referenceQuery(rn, filename=1)
                active = cmds.listConnections("{}.activeProxy".format(pm[0]), plugs=1)[0]
                activeRN = cmds.listConnections(active)[0]
                cmds.file(unloadReference=activeRN)
                RIG = cmds.listConnections("{}.proxyList".format(pm[0]))[0]
                cmds.createNode("gpuCache", name="{}_GPUShape".format(RIG))
                cmds.setAttr("{}_GPUShape.cacheFileName".format(RIG), os.path.join(abc_pth, "{}.abc".format(RIG)), type="string")
