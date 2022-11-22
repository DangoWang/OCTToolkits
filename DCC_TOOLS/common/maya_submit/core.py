#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################
import os
import logging
import md5
import md5, StringIO
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from utils.shotgun_operations import *
from utils.common_methods import *
from tools.simple_playblast import spb_main
from PySide2 import QtCore, QtGui, QtWidgets
from pprint import pprint
import json
reload(spb_main)

check_class_dict = dict(mod='CheckModel',
                        rig='CheckRigging',
                        ly='CheckLayout',
                        bk='CheckLayout',
                        an='CheckLayout',
                        tex='CheckMaterial',
                        fur='CheckCFX',
                        cloth='CheckCFX',
                        flo='CheckFl')


def playblast_img(jpg_fullpath):
    return cmds.playblast(fr=cmds.currentTime(q=True), fmt="image", c="jpg", f=jpg_fullpath,
                          os=True, v=True, wh=[960, 540], clearCache=1, forceOverwrite=1, p=100)


def playblast_mov(artist, mov_path):
    path = os.path.dirname(mov_path)
    f = mov_path.replace(path+'/', '').split('.')[0]
    dsf_playblast_win = spb_main.DsfSimplePlayBlast()
    dsf_playblast_win.on_playblast_doit_clicked(artist, f, path)
    return mov_path + "/" + f + ".mov"


def list_current_dir(path, mode='files'):
    files_and_folders = [os.path.join(path, each).replace('\\', '/') for each in os.listdir(path)]
    if mode in ['files']:
        return [file for file in files_and_folders if os.path.isfile(file)]
    elif mode in ['folders']:
        return [folder for folder in files_and_folders if os.path.isdir(folder)]
    elif mode in ['all']:
        return files_and_folders
    return []


def export_fur_mat(export_path):
    yeti_shape_list = cmds.ls(type='pgYetiMaya')
    sg_node_list = []
    for name in yeti_shape_list:
        sg_name = cmds.listConnections(name, d=1, t='shadingEngine')
        if sg_name:
            for s in sg_name:
                if cmds.attributeQuery("pgYetiMaya", node=s, exists=True):
                    yeti_name = cmds.getAttr("{}.pgYetiMaya".format(s))
                    if name not in yeti_name.split(";"):
                        new_yeti_name = yeti_name + ";" + name
                    else:
                        new_yeti_name = yeti_name
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), l=False)
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), new_yeti_name, type="string")
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), l=True)
                else:
                    cmds.addAttr(s, ln="pgYetiMaya", dt="string")
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), e=True, keyable=True)
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), name, type="string")
                    cmds.setAttr("{}.{}".format(s, "pgYetiMaya"), l=True)
                if s not in sg_node_list:
                    sg_node_list.append(s)
    print sg_node_list
    cmds.select(cl=True)
    cmds.select(sg_node_list, r=True, ne=True)
    cmds.file(export_path, options="v=0;", typ="mayaAscii", pr=True, es=True)
    cmds.select(cl=True)
    return export_path


def get_geometry_md5(geometry):
    '''
    '''
    io = StringIO.StringIO()
    dag_path = OpenMaya.MDagPath.getAPathTo(geometry)

    iterator = OpenMaya.MItMeshVertex(dag_path)
    face_list = OpenMaya.MIntArray()
    while not iterator.isDone():
        iterator.getConnectedFaces(face_list)
        io.write('{0} {1}\n'.format(iterator.index(), ' '.join(sorted([str(i) for i in face_list]))))
        iterator.next()

    _md5 = md5.new()
    _md5.update(io.getvalue())
    return _md5.hexdigest()


def get_hierarchy_data(ignore_hide_objects=False):
    '''
    '''
    data = dict()

    model_high_grp = pm.ls('|*|Geometry|high')
    if not model_high_grp:
        return data

    iterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)
    iterator.reset(model_high_grp[0].__apiobject__())

    while not iterator.isDone():
        if OpenMaya.MFnDagNode(iterator.currentItem()).childCount() == 0:
            iterator.next()
            continue

        shape_0 = OpenMaya.MFnDagNode(iterator.currentItem()).child(0)
        if shape_0.apiType() != OpenMaya.MFn.kMesh:
            iterator.next()
            continue

        if ignore_hide_objects and not OpenMaya.MDagPath.getAPathTo(shape_0).isVisible():
            iterator.next()
            continue

        try:
            geo_md5 = get_geometry_md5(iterator.currentItem())
        except:
            geo_md5 = '0' * 32
        data[iterator.fullPathName()] = geo_md5
        iterator.next()

    return data


def comparison_md5(sg_topo_data, file_topo_data):
    #  对比shotgun上的MD5值跟文件的MD5值
    sg_topo_data = json.loads(sg_topo_data)
    no_match_geo = list()
    for geo, topo_value in file_topo_data.iteritems():
        if topo_value != sg_topo_data.get(geo):
            no_match_geo.append(geo)

    return no_match_geo


def check_topo(*args):
    win, task_id, task_type, task_step, task_classify, project = args
    if task_type in ['Shot'] or task_step in ['ani'] or task_classify not in ["CH", "PROP"]:
        return True
    project_info = find_one_shotgun('Project', [['name', 'is', project]], ['id'])
    task_info_list = find_one_shotgun("Task", [["project", "name_is", project], ["id", "is", task_id]],
                                      ["entity", "entity.Asset.sg_md5", "entity.Asset.id"])
    asset_name = task_info_list["entity"]["name"]
    asset_link = task_info_list["entity"]
    asset_task_list = find_shotgun("Task", [["project", "name_is", project], ["entity", "is", task_info_list["entity"]]],
                                   ["task_assignees", "step", "sg_mod5"])

    shotgun_asset_md5 = task_info_list["entity.Asset.sg_md5"]
    asset_id = task_info_list["entity.Asset.id"]
    if task_step == "mod":
        #  查找shotgun上面的md5数值跟文件是否一致
        #  获取文件的MD5值
        file_md5 = get_hierarchy_data(ignore_hide_objects=False)
        if shotgun_asset_md5:
            topology_error = comparison_md5(shotgun_asset_md5, file_md5)
            if topology_error:
                cmds.select(cl=True)
                cmds.select(topology_error)
                g = QtWidgets.QMessageBox.critical(win, u"警告：", u'发现该模型拓扑发生更改', QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
                if g == QtWidgets.QMessageBox.Yes:
                    asset_data = {"sg_md5": json.dumps(file_md5)}
                    update_shotgun("Asset", asset_id, asset_data)
                else:
                    return False
        else:
            asset_data = {"sg_md5": json.dumps(file_md5)}
            update_shotgun("Asset", asset_id, asset_data)  # 把最新的拓扑信息添加到shotgun
        assignees_people = []
        for asset_task in asset_task_list:
            if asset_task["step"] not in ["Model"]:
                for people_info in asset_task["task_assignees"]:
                    if people_info not in assignees_people:
                        assignees_people.append(people_info)
        batch_data = []
        for addressee in assignees_people:
            note_data = {
                "project": project_info,
                "subject": u'资产更新：资产{}的模型任务已上传'.format(asset_name),
                "content": u"资产{}的模型任务已上传, 请知悉。".format(asset_name),
                "addressings_to": [addressee],
                "note_links": [asset_link],
                "sg_status_list": "opn",
                "sg_if_read": False,
            }
            batch_data.append({"request_type": "create", "entity_type": "Note", "data": note_data})
        batch_shotgun(batch_data)
        return True
    else:
        file_md5 = get_hierarchy_data(ignore_hide_objects=True)
        if shotgun_asset_md5:
            topology_error = comparison_md5(shotgun_asset_md5, file_md5)
            if topology_error:
                cmds.select(cl=True)
                cmds.select(topology_error)
                QtWidgets.QMessageBox.critical(win, u"错误：", u'文件与模型拓扑不一样')
                return False
            else:
                return True
        else:
            return True









