#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8.26
###################################################################

import os
from dayu_widgets.message import MMessage
from utils import shotgun_operations
from utils import fileIO
from pprint import pprint

sg = shotgun_operations


def get_path_template(project_name):
    path_template = {}
    custom_entity_list = sg.find_shotgun('CustomEntity01',
                                             [['project', 'name_is', project_name], ['sg_upload_type', 'is', 'Publish']],
                                             ["sg_pattern", "sg_oss_submit_path", "sg_type"])
    for custom_entity in custom_entity_list:
        _type = custom_entity["sg_type"]
        value_list = [custom_entity["sg_oss_submit_path"]]
        path_template[_type] = value_list
    return path_template


def get_version_info(download_dict):
    copy_file_list = []
    download_path = download_dict['local_path']
    version_id = download_dict['id']
    project_name = download_dict['project']
    find_type = download_dict['type']
    identity = download_dict['identity']
    path_template = get_path_template(project_name)
    version_info_list = sg.find_shotgun(find_type, [
        ["id", "in", version_id], ['project', 'name_is', project_name]],
                                   ["code", "sg_path_to_frames", "sg_path_to_movie", "sg_path_to_geometry",
                                    'sg_version_type', 'entity', "entity.Asset.sg_asset_type", "entity.Asset.code",
                                    "sg_task.Task.content", "entity.Shot.sg_sequence", "entity.Shot.code",
                                    "sg_version_number"])
    if identity in ['outsource']:
        for version_info in version_info_list:
            if not version_info['sg_version_type'] in ['Publish', 'Approved']:
                MMessage.config(2)
                MMessage.warning(u'只能下载Publish或Approved类型的版本！', parent=download_dict['widget'])
                raise RuntimeError
            oss_path_template = path_template[version_info["entity"]["type"]][0]
            classify_n = version_info["entity.Asset.sg_asset_type"]
            task_name_n = version_info["sg_task.Task.content"]
            code_n = version_info["entity.Asset.code"]
            scene_n = version_info["entity.Shot.sg_sequence"]
            if scene_n:
                shot_n = version_info["entity.Shot.code"].split("_")[-1]
            else:
                shot_n = ""
            version_num = version_info["sg_version_number"]
            oss_path = oss_path_template.format(classify=classify_n, task_name=task_name_n, code=code_n,
                                                scene=scene_n, shot=shot_n, version=version_num)
            out_local_path = oss_path.replace("oss://oss-oct-sg/", download_path).replace(version_num, "")
            copy_file_list.extend([oss_path, out_local_path])
    else:
        for version_info in version_info_list:
            if not version_info['sg_version_type'] in ['Publish', 'Approved']:
                MMessage.config(2)
                MMessage.warning(u'只能下载Publish或Approved类型的版本！', parent=download_dict['widget'])
                raise RuntimeError
            geometry_folder = version_info["sg_path_to_geometry"]
            ma_path = version_info["sg_path_to_frames"]
            mov_path = version_info["sg_path_to_movie"]
            if geometry_folder and os.path.exists(geometry_folder):
                if geometry_folder in ma_path or geometry_folder in mov_path:
                    for each_f in os.listdir(geometry_folder):
                        f_path = geometry_folder + '/' + each_f
                        f_path = f_path.replace('//', '/')
                        if os.path.isdir(f_path):
                            copy_dirs = fileIO.get_copy_list(f_path, f_path.replace(f_path[0] + ':', download_path))
                            copy_file_list.extend(copy_dirs)
                else:
                    copy_dirs = fileIO.get_copy_list(geometry_folder,
                                                     geometry_folder.replace(geometry_folder[0] + ':', download_path))
                    copy_file_list.extend(copy_dirs)
            if ma_path and os.path.exists(ma_path):
                local_ma_path = ma_path.replace(ma_path.split(':')[0] + ':', download_path)
                ma_file_list = [ma_path, local_ma_path]
                if ma_file_list not in copy_file_list:
                    copy_file_list.append(ma_file_list)
            else:
                MMessage.config(1)
                MMessage.warning(u'工程文件不存在', parent=download_dict['widget'])
            if mov_path and os.path.exists(mov_path):
                local_mov_path = mov_path.replace(mov_path.split(':')[0] + ':', download_path)
                mov_file_list = [mov_path, local_mov_path]
                if mov_file_list not in copy_file_list:
                    copy_file_list.append(mov_file_list)
            else:
                MMessage.config(1)
                MMessage.warning(u'预览文件不存在', parent=download_dict['widget'])
    return copy_file_list


def get_task_info(download_dict):
    # download_path = download_dict['local_path']
    task_id = download_dict['id']
    project_name = download_dict['project']
    version_dict = download_dict.copy()
    version_dict['type'] = 'Version'
    version_dict['id'] = []
    no_publish = []
    for t in range(0, len(task_id)):
        version_info_list = sg.find_shotgun("Version", [
            ["sg_task.Task.id", "is", task_id[t]],
            ['sg_version_type', 'is', 'Publish'],
            ['project', 'name_is', project_name]],
            ['code', "sg_path_to_frames",
             "sg_path_to_movie", "sg_version_number", "sg_path_to_geometry", "sg_task.Task.sg_publish_version"])
        # print "version_info_list",version_info_list
        if version_info_list:
            for v, version_info in enumerate(version_info_list):
                if version_info["sg_task.Task.sg_publish_version"]:
                    if version_info["sg_version_number"] == version_info["sg_task.Task.sg_publish_version"]:
                        version_dict['id'].append(version_info['id'])
                        break
                else:
                    no_publish.append(str(task_id[t]))
        else:
            no_publish.append(str(task_id[t]))
    if no_publish:
        MMessage.config(2)
        MMessage.warning(u'{}任务需要发布之后才能下载！'.format(",".join(no_publish)), parent=download_dict['widget'])
    if version_dict['id']:
        copy_file_list = get_version_info(version_dict)
        return copy_file_list


def get_group_list(user_name):
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code", "sg_permission_group"])
    return group_list
