#!/usr/bin/env python
# -*- coding: utf-8 -*-

# open file to output abc and fur cache

import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import time
import os
from utils import shotgun_operations as sg
# from core import shotgun_operations
# sg = shotgun_operations


# get asset id by file path
def get_asset_id(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path],
        ['entity.Asset.sg_asset_type', 'is_not', 'ENV']]
    fields = ["entity.Asset.id"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity.Asset.id"]:
                return version["entity.Asset.id"]
        return None
    else:
        return None

# get asset node by asset id
def get_asset_node(id, *args):
    filters = [
        ['id', 'is', id]]
    fields = []
    asset_list = sg.find_shotgun('Asset', filters, fields)
    if asset_list:
        return asset_list[0]
    else:
        return None

# get task name by file path
def get_task_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["sg_task.Task.content", "entity.Shot.sg_checkbox"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["sg_task.Task.content"]:
                return version
        return None
    else:
        return None

def get_scene_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["entity.Shot.sg_sequence"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity.Shot.sg_sequence"]["name"]:
                return version["entity.Shot.sg_sequence"]["name"]
        return None
    else:
        return None

def get_shot_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["entity"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity"]["name"]:
                return version["entity"]["name"]
        return None
    else:
        return None

def get_shot_version(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = []
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version:
                return version
        return None
    else:
        return None

# get visibility
def is_visibility(obj):
    obj_visibility = cmds.getAttr('{}.visibility'.format(obj))
    if not obj_visibility:
        return obj_visibility
    parent_list = cmds.listRelatives(obj, parent=1, fullPath=1) or []
    if not parent_list:
        return obj_visibility
    else:
        parent_visibility = cmds.getAttr('{}.visibility'.format(parent_list[0]))
        if not parent_visibility:
            return parent_visibility
        else:
            return is_visibility(parent_list[0])

def get_cam(*args):
    cam_list = cmds.ls("CAM")
    if not cam_list.__len__():
        return
    # cam_shape_list = cmds.listRelatives(cam_list[0], ad=1, typ="camera")
    # if cam_shape_list.__len__() != 1:
    #     return
    return cam_list[0]

def get_info_folder(*args):
    if os.path.isdir("E:/"):
        return "E:/"
    elif os.path.isdir("D:/"):
        return "D:/"
    elif os.path.isdir("F:/"):
        return "F:/"
    else:
        return


def abc_out(file_path, *args):
    cmds.file(file_path, f=1, options="v=0;", ignoreVersion=1, typ="mayaAscii", o=1)
    if_yeti = False
    frame_st = cmds.playbackOptions(q=1, animationStartTime=1) -75
    frame_en = cmds.playbackOptions(q=1, animationEndTime=1)
    # log file
    log_file = os.path.join(get_info_folder(), "abc_log.txt")  # r"D:\test\abc_log.txt"
    file_id = file(log_file, "a")
    # get current file name
    current_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    mfile = om.MFileIO()
    current_file = mfile.currentFile()
    file_id.write("=====================================================================================================\n")
    file_id.write("File: {}\n".format(current_file))
    if not cmds.pluginInfo('AbcExport', query=1, loaded=1):
        try:
            cmds.loadPlugin('AbcExport.mll')
        except RuntimeError:
            file_id.write("AbcExport.mll was not found on MAYA_PLUG_IN_PATH\n")
            file_id.close()
            return
    if not current_file:
        return
    # get task name
    task_current = get_task_name(current_file)
    task_name = task_current["sg_task.Task.content"]
    file_id.write("Task Name: {}\n".format(task_name))
    # get scene name
    scene_name = get_scene_name(current_file)
    file_id.write("Scene Name: {}\n".format(scene_name))
    # get shot name
    shot_name = get_shot_name(current_file)
    shot_version = get_shot_version(current_file)
    file_id.write("Shot Name: {}\n".format(shot_name))
    # get reference  node list
    reference_list = cmds.ls(references=1) or []
    file_id.write("Reference List:\n")
    abc_path_convention = sg.find_one_shotgun('CustomEntity01',
                                              [['project', 'name_is', sg.get_project()], ['sg_type', 'is', 'Shot'],
                                               ['sg_upload_type', 'is', 'Publish']], ['sg_cache_path', 'sg_pattern'])
    namespace_list = list()
    for node in reference_list:
        file_id.write("    {} >> ".format(node))
        try:
            # get reference file path
            file_path = cmds.referenceQuery(node, filename=1, unresolvedName=1, withoutCopyNumber=1)
        except Exception as e:
            # print str(e)
            file_id.write("{}".format(str(e)))
            continue
        # get reference namespace
        namespace_long = None
        try:
            namespace_long = cmds.referenceQuery(node, namespace=1)
        except Exception as e:
            file_id.write("{}".format(str(e)))
            continue

        # 取消单层ref限制
        # if namespace.count(":") != 1:
        #     file_id.write("Indirect reference")
        #     continue
        namespace_shot = cmds.referenceQuery(node, namespace=1, shortName=1)
        namespace_tmp = namespace_shot
        namespace_num = 1
        while namespace_shot in namespace_list:
            namespace_shot = namespace_tmp + str(namespace_num)
            namespace_num += 1
        namespace_list.append(namespace_shot)
        # get asset id
        asset_id = get_asset_id(file_path)
        if not asset_id:
            file_id.write("can't find asset id\n")
            continue
        # get asset node
        asset_node = get_asset_node(asset_id)
        if not asset_node:
            file_id.write("can't find asset node\n")
            continue

        yeti_list = []
        try:
            yeti_list = cmds.ls("{}:*".format(namespace_long), type="pgYetiMaya")
        except Exception as e:
            print(str(e))
        if yeti_list:
            if_yeti = True
            # test path
            cache_folder_pattern = ('/'.join(cache_path_pattern.split('/')[:-1])).format(step_code=task_name, scene=scene_name,
                    shot=shot_name[len(scene_name) + 1:], cache_type="fur", namespace=namespace_shot, cache_version=current_time)
            if not os.path.isdir(cache_folder_pattern):
                try:
                    os.makedirs(cache_folder_pattern)
                except Exception as e:
                    file_id.write("can't make folder for fur\n")
                    # print "can't make folder for abc"
                    # print str(e)
                    continue

            file_id.write("        Yeti List:\n")
            for yeti_node in yeti_list:
                fur_path = cache_path_pattern.format(step_code=task_name, scene=scene_name,
                    shot=shot_name[len(scene_name) + 1:], cache_type="fur", namespace=namespace_shot,
                                                     cache_version=current_time, cache_name=yeti_node.split(':')[-1]+'.%04d')
                # fur_full_path = "{}/{}.%04d.fur".format(fur_path, yeti_node.split(':')[-1])
                print( fur_path )
                mel.eval('pgYetiCommand -writeCache "{}" -range {} {} -samples 1 -updateViewport 0 -generatePreview 0 {};'.format(fur_path, frame_st, frame_en, yeti_node))
                file_id.write("            {} >> {}\n".format(yeti_node, fur_path))
                sg.create_shotgun("CustomEntity03", {'code': namespace_shot,
                                                          'sg_cache_type': 'fur',
                                                          'sg_asset': asset_node,
                                                          'sg_namespace': namespace_shot,
                                                          'sg_shot_version': shot_version,
                                                          'sg_version': current_time,
                                                          'project': {u'id': 89, u'type': u'Project'},
                                                          'sg_cache_path': fur_path,
                                                          'sg_obj_list': yeti_node.replace(namespace_long[1:], namespace_shot)})
            continue

        cache_path_pattern = '/'.join([abc_path_convention['sg_pattern'], abc_path_convention['sg_cache_path']])
        abc_path = cache_path_pattern.format(
            step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name)+1:], cache_type="abc",
            namespace=namespace_shot, cache_version=current_time, cache_name=namespace_shot)
        # abc_path = "D:/test/Shot/{task_name}/{scene}/{shot}/cache/{cache_type}/{namespace}/{cache_version}".format(
        #     step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name)+1:], cache_type="abc", namespace=namespace, cache_version=current_time
        # )
        abc_folder = '/'.join(abc_path.split('/')[:-1])
        if not os.path.isdir(abc_folder):
            try:
                os.makedirs(abc_folder)
            except Exception as e:
                file_id.write("can't make folder for abc\n")
                # print "can't make folder for abc"
                # print str(e)
                continue
        # abc_full_path = "{cache_path}/{cache_name}.{cache_type}".format( cache_path=abc_path, cache_name=namespace, cache_type="abc")
        # print "abc_full_path: ", abc_full_path
        high_node = "{}:high".format(namespace_long)
        if not cmds.objExists(high_node):
            file_id.write("can't exists {} for abc\n".format(high_node))
            continue

        obj_list = []
        mesh_list = cmds.listRelatives(high_node, allDescendents=1, type='mesh', fullPath=1)
        tran_list = cmds.listRelatives(mesh_list, parent=1, fullPath=1)
        tran_list = list(set(tran_list))
        for tran in tran_list:
            if is_visibility(tran):
                obj_list.append(tran)
        if not obj_list:
            file_id.write("No objects need to be output cached\n")
            continue
        # print obj_list
        file_id.write("{}\n".format(abc_path))
        abc_job_arg = '-frameRange {} {} -worldSpace -writeVisibility -stripNamespaces -dataFormat ogawa'.format(frame_st, frame_en)
        for obj in obj_list:
            abc_job_arg = '{} -root {}'.format(abc_job_arg, obj)
        abc_job_arg = '{} -file {}'.format(abc_job_arg, abc_path)
        # print abc_full_path
        # cmds.AbcExport(j="-frameRange {} {} -worldSpace -dataFormat ogawa -root {} -file {}".format(frame_st, frame_en, high_node, abc_full_path))
        try:
            cmds.AbcExport(j=abc_job_arg)
            # create shotgun node for cache
            sg.create_shotgun("CustomEntity03", {'code': namespace_shot,
                                            'sg_cache_type': 'abc',
                                            'sg_asset': asset_node,
                                            'sg_namespace': namespace_shot,
                                            'sg_shot_version': shot_version,
                                            'sg_version': current_time,
                                            'project': {u'id': 89, u'type': u'Project'},
                                            'sg_cache_path': abc_path,
                                            'sg_obj_list': ';'.join([obj_shot.replace(namespace_long[1:], namespace_shot) for obj_shot in obj_list])})
        except:
            file_id.write("Can not export abc\n")
    if not if_yeti:
        # camera
        cam = get_cam()
        if cam:
            cam_full_path = '/'.join([abc_path_convention['sg_pattern'], abc_path_convention['sg_cache_path']]).format(
                step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name) + 1:], cache_type="abc",
                namespace="CAM", cache_version=current_time, cache_name="CAM")
            cam_folder = os.path.split(cam_full_path)[0]
            if not os.path.isdir(cam_folder):
                os.makedirs(cam_folder)
            # cam_full_path = "{cache_path}/{cache_name}.{cache_type}".format(cache_path=cam_path, cache_name="CAM",
            #                                                                 cache_type="abc")
            file_id.write("CAM >> {}\n".format(cam_full_path))
            cam_job_arg = '-frameRange {} {} -worldSpace -writeVisibility -stripNamespaces -dataFormat ogawa'.format(frame_st, frame_en)

            cam_job_arg = '{} -root {}'.format(cam_job_arg, cam)
            cam_job_arg = '{} -file {}'.format(cam_job_arg, cam_full_path)
            cmds.AbcExport(j=cam_job_arg)
            sg.create_shotgun("CustomEntity03", {'code': "CAM",
                                            'sg_cache_type': 'abc',
                                            'sg_namespace': "CAM",
                                            'sg_shot_version': shot_version,
                                            'sg_version': current_time,
                                            'project': {u'id': 89, u'type': u'Project'},
                                            'sg_cache_path': cam_full_path,
                                            'sg_obj_list': 'CAM'})

    file_id.close()

    new_info_dict = dict()
    new_info_dict["entity.Shot.sg_checkbox"] = True
    sg.update_shotgun("Version", task_current["id"], new_info_dict)

#abc_out()

