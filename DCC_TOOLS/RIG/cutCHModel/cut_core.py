#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/26

__author__ = 'donghao wang'

import logging
import maya.mel as mel
import maya.cmds as mc
import pymel.core as pm


def create_plane(plane_name, sx=3, sy=3, w=3, h=3):  # 创建刀片
    if mc.objExists(plane_name):
        mc.delete(plane_name)
    pm.polyPlane(sx=sx, sy=sy, w=w, h=h, n=plane_name)
    return plane_name


def cut_model(mesh_name, planeName):  # 切的动作
    mc.select(mesh_name, r=1)
    mel.eval('FillHole;')
    mc.duplicate(mesh_name, name="DuMeshTemp")
    mc.duplicate(planeName, name="DuLaneTemp")
    temp_knife = mc.duplicate(planeName, name="DuLaneTemp_for_single_cut")
    new_name = ["DuMeshTemp", "DuLaneTemp"]
    up_mesh = mc.polyCBoolOp(new_name[0], new_name[1], op=3, ch=1, preserveColor=0, classification=1)[0]
    down_mesh = mc.polyCBoolOp(mesh_name, planeName, op=2, ch=1, preserveColor=0, classification=1)[0]
    mel.eval("DeleteHistory %s" % up_mesh)
    mel.eval("DeleteHistory %s" % down_mesh)
    mc.delete(new_name)
    if mc.objExists(mesh_name):
        mc.delete(mesh_name)
    out_mesh_up = mc.rename(up_mesh, mesh_name)
    out_mesh_down = mc.rename(down_mesh, planeName.replace("_polyPlane", "_Low"))
    mc.rename(temp_knife, planeName)
    return out_mesh_up, out_mesh_down


def build_plane(bone_list):  # 根据骨骼位置创建所有刀片的方法
    if not bone_list:
        logging.error(u" 请先选择骨骼！")
        return False
    plane_list = []
    for each in bone_list:
        if "_L" not in each:
            plane_name = create_plane(each + "_polyPlane")
            constraint_temp = mc.parentConstraint(each, plane_name)
            mc.delete(constraint_temp)
            plane_list.append(plane_name)
    r_grp = [p for p in plane_list if '_R' in p]
    body_grp = [b for b in plane_list if b not in r_grp]
    knives_grp_r = mc.group(r_grp, name='cutting_knives_grp_R')
    knives_grp_body = mc.group(body_grp, name='cutting_knives_grp_body')
    knives_grp = mc.group([knives_grp_r, knives_grp_body], name='cutting_knives_grp')
    mc.select(plane_list, r=1)
    mel.eval('rotate -r -os -fo 0 0 90;FreezeTransformations;')
    for each in (body_grp + r_grp):
        mc.select(each, r=1)
        mel.eval('ReversePolygonNormals;')
    return knives_grp


def boolean_model(bone_root, bone_dict=dict(), model=''):  # 切的执行方法
    for k, v in bone_dict.iteritems():
        if k == bone_root:
            boolean_model(bone_root, v, model)
        else:
            knife_name = k + '_polyPlane'
            print model, knife_name
            mc.select(model, r=1)
            mel.eval('FillHole;')
            cut_model(model, knife_name)
            new_model_name = k + '_Low'
            if isinstance(v, dict):
                if v.items():
                    boolean_model(bone_root, v, new_model_name)


def mirror_knives(grp_name='cutting_knives_grp_R'):
    knives_r_grp = grp_name
    grp_pm_node = pm.PyNode(knives_r_grp)
    grp_pm_node.setPivots((0, 0, 0), worldSpace=1)
    pm.duplicate(knives_r_grp, name='cutting_knives_grp_L')
    mc.setAttr('cutting_knives_grp_L.scaleX', -1)
    for each in mc.listRelatives('cutting_knives_grp_L', c=1, fullPath=1):
        mc.select(each, r=1)
        mel.eval('ReversePolygonNormals;')
        mc.rename(each, each.split('|')[-1].replace('_R', '_L'))
