#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.10.9
import os
from pprint import pprint
from utils import shotgun_operations
from dayu_widgets.qt import *
from utils import fileIO

sg = shotgun_operations


class WriteDatabase(QThread):
    # 用于创建更新的线程
    write_finished = Signal(bool)

    def __init__(self, parent=None):
        super(WriteDatabase, self).__init__(parent)
        self.data = None

    def run(self, *args, **kwargs):
        for each in self.data:
            print each
            if each:
                if each[0] == 'update':
                    sg.update_shotgun(each[1], each[2], each[3])
                if each[0] == 'create':
                    sg.create_shotgun(each[1], each[2])
        self.write_finished.emit(True)


def get_asset_info(task_dict):
    shot_name_list = []
    asset_id_list = []
    task_id = task_dict["id"]
    project_name = task_dict["project"]
    task_info_list = sg.find_shotgun("Task", [["id", "in", task_id], [
                                        "project", "name_is", project_name]], ["entity", "entity.Shot.assets",
                                                                               "task_assignees", "content"])
    for task_info in task_info_list:
        _type = task_info["entity"]["type"]
        if _type == "Shot":
            shot_name = task_info["entity"]["name"]
            if shot_name not in shot_name_list:
                shot_name_list.append(str(shot_name))
        if task_info["entity.Shot.assets"]:
            asset_list = task_info["entity.Shot.assets"]
            for _asset in asset_list:
                asset_id = _asset["id"]
                if asset_id not in asset_id_list:
                    asset_id_list.append(asset_id)
    task_assignees_list = sg.find_shotgun('Task', [['entity', 'type_is', 'Shot'],
                                                   ['project', 'name_is', task_dict['project']],
                                                   ['entity.Shot.code', 'in', shot_name_list]], ['task_assignees'])
    all_assignees_id = []
    for a in task_assignees_list:
        if a["task_assignees"]:
            for one in a["task_assignees"]:
                if one["id"] not in all_assignees_id:
                    all_assignees_id.append(int(one["id"]))
    return shot_name_list, asset_id_list, all_assignees_id
    # shot_name_list = [选择的任务的镜头列表]
    # asset_id_list = [选择的任务链接的资产的id列表]
    # all_assignees_id = [选择的任务对应镜头下所有的分配人员的id]


def get_oss_path(project_name, _type, upload_type):
    # 获取shotgun上面的阿里云，以及publish 路径规范
    custom_entity_list = sg.find_one_shotgun('CustomEntity01', [
                ['project', 'name_is', project_name], ['sg_type', 'is', _type], ['sg_upload_type', 'is', upload_type]],
                                                    ["sg_oss_submit_path", "sg_pattern"])

    oss_path = custom_entity_list["sg_oss_submit_path"]
    copy_path = custom_entity_list["sg_pattern"]
    return oss_path, copy_path


def get_group_list(user_name):
    # 获取使用者是人员信息用于判断是否是外包
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code", "sg_permission_group"])
    return group_list


def get_latest_version(task_id_list, project_name):
    # 获取任务下面的最新版本，返回任务id对应的最新版本号字典，和最新版本的id号列表
    version_info_list = sg.find_shotgun("Version", [["sg_task.Task.id", "in", task_id_list],
                                                    ['sg_version_type', 'is', 'Publish'],
                                                    ['project', 'name_is', project_name]],
                                        ['code', "sg_path_to_frames", "sg_path_to_movie",
                                         "sg_version_number", "sg_path_to_geometry",
                                         "sg_task.Task.sg_publish_version", "sg_task.Task.id"])
    dict_id_version = {}
    version_id_list = []
    print "-------------------------------------"
    for v, version_info in enumerate(version_info_list):
        if version_info["sg_version_number"] == version_info["sg_task.Task.sg_publish_version"]:
            version_id_code = [version_info["sg_version_number"], version_info["code"]]
            dict_id_version[version_info["sg_task.Task.id"]] = version_id_code
            version_id_list.append(int(version_info["id"]))
    # dict_id_version = {"任务id号"：["最新版本号","code"]}
    # version_id_list = [最新版本号id列表]

    return dict_id_version, version_id_list


def get_step_list(project_name):
    # 获取资产类型的流程工序名字，用于界面的上的checkbox,标签的显示
    info_list = sg.find_shotgun("Step", [["sg_project", "name_is", project_name],
                                         ["entity_type", "is", "Asset"]], ["code"])
    step_list = []
    for s in info_list:
        if s["code"] not in step_list:
            step_list.append(s["code"])
    return step_list


def get_inside_copy_list(kwargs, oss_path_template, publish_path_template):
    # 获取内部人员上传阿里云的copy_list。
    # kwargs = {"project": self.project_name, "id": version_id_list, "user": ""}
    update_code = []
    all_copy_list = []
    this_version_list = sg.find_shotgun('Version', [['project', 'name_is', kwargs['project']],
                                                    ['id', 'in', kwargs['id']]],
                                        ['code', 'sg_path_to_frames', 'sg_path_to_movie',
                                         'sg_path_to_geometry', 'user', 'entity', 'sg_task',
                                         'sg_version_type', "sg_task.Task.id", 'sg_version_number',
                                         'entity.Asset.sg_asset_type', "sg_task.Task.id"])

    for version_info_dict in this_version_list:
        task_id = version_info_dict['sg_task.Task.id']
        asset_type = version_info_dict['entity.Asset.sg_asset_type']
        asset_name = version_info_dict['entity']['name']
        task_n = version_info_dict['sg_task']['name']
        version_num = version_info_dict['sg_version_number']
        update_code.append(['update', 'Task', task_id, {'sg_approve_version': version_info_dict['sg_version_number'],
                                                        }])
        publish_version_path = publish_path_template.format(classify=asset_type, code=asset_name, task_name=task_n)
        oss_version_path = oss_path_template.format(classify=asset_type, code=asset_name, task_name=task_n,
                                                    version=version_num)
        ma_path = version_info_dict['sg_path_to_frames']
        mov_path = version_info_dict['sg_path_to_movie']
        if ma_path and os.path.exists(ma_path):
            all_copy_list.append([ma_path, ma_path.replace(publish_version_path, oss_version_path)])
        if mov_path and os.path.exists(mov_path):
            all_copy_list.append([mov_path, mov_path.replace(publish_version_path, oss_version_path)])
        geometry_folder = version_info_dict['sg_path_to_geometry']
        if geometry_folder and os.path.exists(geometry_folder):
            if geometry_folder in ma_path or geometry_folder in mov_path:
                for each_f in os.listdir(geometry_folder):
                    f_path = geometry_folder + '/' + each_f
                    f_path = f_path.replace('//', '/')
                    if os.path.isdir(f_path):
                        copy_dirs = fileIO.get_copy_list(f_path, oss_version_path)
                        all_copy_list.extend(copy_dirs)
            else:
                copy_dirs = fileIO.get_copy_list(geometry_folder, oss_version_path)
                all_copy_list.extend(copy_dirs)
    # this_version_list = 最新版本信息列表
    # all_copy_list = 上传阿里云的copy 列表
    # update_code  = 用于shotgun上面创建或者更新的列表信息
    return all_copy_list, update_code


def get_outsource_shot(all_assignees_id):
    # 获取哪个任务分配给外包，返回任务以及对应得外包人员字典
    outsource_id_list = []
    group_list = sg.find_shotgun('Group', [['id', 'in', all_assignees_id]],
                                 ["id", "sg_permission_group", "code"])
    for group in group_list:
        if group["sg_permission_group"] in ['outsource']:
            outsource_id_list.append(group["id"])

    # pprint(outsource_id_list)
    # outsource_id_list = [所有外包人员的id列表]
    return outsource_id_list


def update_sg(kwargs, *args):
    # 用于获取在shotgun上面创建给外包的反馈
    create_note_code = []
    shot_name_list, asset_id_list, outsource_id_list, dict_id_version = args
    proposer = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', kwargs['user']]], ['code', 'sg_login'])
    project = shotgun_operations.find_one_shotgun('Project', [['name', 'is', kwargs['project']]], [])
    link_asset_list = []
    version_code_list = []
    for asset_id in asset_id_list:
        asset_info_dict = {"type": "Asset", "id": asset_id}
        link_asset_list.append(asset_info_dict)
    for info_list in dict_id_version.values():
        if info_list[1] not in version_code_list:
            version_code_list.append(info_list[1])
    shot_name_str = " ".join(shot_name_list)
    subject_tex = u'资产更新通知'
    content_tex = u'以下资产已更新至云:\n{}\n关联镜头为:\n{}\n请及时下载.'.format(version_code_list, shot_name_str)
    for outsource_id in outsource_id_list:
        note_content = {'project': project,
                        'subject': subject_tex,
                        'note_links': link_asset_list,
                        'sg_proposer': proposer,
                        'addressings_to': [{'id': outsource_id, 'type': 'Group'}],
                        'content': content_tex,
                        'sg_if_read': False
                        }
        create_note_code.append(['create', 'Note', note_content])
    return create_note_code
