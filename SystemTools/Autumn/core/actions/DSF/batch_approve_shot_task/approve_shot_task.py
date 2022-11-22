#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.10
# wechat : 18250844478
###################################################################
import os
# import pprint

from utils import shotgun_operations
from dayu_widgets.qt import *
from utils import fileIO
from pprint import pprint
import approve_shot_task_ui
sg = shotgun_operations


def get_assignees_people(kwargs):
    shot_name_list = []
    task_id = kwargs["id"]
    project_name = kwargs["project"]
    task_info_list = sg.find_shotgun("Task", [["id", "in", task_id], [
                                        "project", "name_is", project_name]], ["entity", "task_assignees", "content"])
    for task_info in task_info_list:
        _type = task_info["entity"]["type"]
        if _type == "Shot":
            shot_name = task_info["entity"]["name"]
            if shot_name not in shot_name_list:
                shot_name_list.append(str(shot_name))
    task_assignees_list = sg.find_shotgun('Task', [['entity', 'type_is', 'Shot'],
                                                   ['project', 'name_is', kwargs['project']],
                                                   ['entity.Shot.code', 'in', shot_name_list]], ['task_assignees'])
    all_assignees_id = []
    for a in task_assignees_list:
        if a["task_assignees"]:
            for one in a["task_assignees"]:
                if one["id"] not in all_assignees_id:
                    all_assignees_id.append(int(one["id"]))
    return all_assignees_id
    # all_assignees_id = [选择的任务对应镜头下所有的分配人员的id]


def get_outsource_shot(all_assignees_id):
    # 获取哪个任务分配给外包，返回任务以及对应得外包人员字典
    outsource_id_list = []
    outsource_name_list = []
    group_list = sg.find_shotgun('Group', [['id', 'in', all_assignees_id]],
                                 ["id", "sg_permission_group", "code"])
    for group in group_list:
        if group["sg_permission_group"] in ['outsource']:
            outsource_id_list.append(group["id"])
            outsource_name_list.append(group["code"])
    # outsource_id_list = [所有外包人员的id列表]
    # outsource_name_list = [所有外包人员名字列表]
    return outsource_id_list, outsource_name_list


def get_latest_version(kwargs, oss_path_template, publish_path_template):
    # 获取任务下面的最新版本，返回任务id对应的最新版本号字典，和最新版本的id号列表
    task_id_list = kwargs["id"]
    project_name = kwargs["project"]
    version_info_list = sg.find_shotgun("Version", [["sg_task.Task.id", "in", task_id_list],
                                                    ['sg_version_type', 'is', 'Publish'],
                                                    ['project', 'name_is', project_name]],
                                        ['code', "sg_path_to_frames", "sg_path_to_movie",
                                         "sg_version_number", "sg_path_to_geometry",
                                         "sg_task.Task.sg_publish_version", "sg_task.Task.id", "entity", "sg_task"])
    version_id_code = {}
    update_code = []
    all_copy_list = []
    for v, version_info in enumerate(version_info_list):
        if version_info["sg_version_number"] == version_info["sg_task.Task.sg_publish_version"]:
            version_id_code[int(version_info["id"])] = version_info["code"]
            task_id = version_info['sg_task.Task.id']
            task_n = version_info['sg_task']['name']
            version_num = version_info['sg_version_number']
            scene = version_info['entity']["name"].split("_")[0]
            shot = version_info['entity']["name"].split("_")[1]
            path_to_frames = version_info['sg_path_to_frames']
            path_to_movie = version_info['sg_path_to_movie']
            path_to_geometry = version_info['sg_path_to_geometry']
            update_code.append(
                ['update', 'Task', task_id, {'sg_approve_version': version_info['sg_version_number'],
                                             }])
            #  更新shotgun上面approve_version 的版本号，便于统计是哪个版本同步给外包

            publish_version_path = publish_path_template.format(task_name=task_n, scene=scene, shot=shot)
            oss_version_path = oss_path_template.format(task_name=task_n, scene=scene, shot=shot,
                                                        version=version_num)
            copy_list = get_inside_copy_list(oss_version_path, publish_version_path,
                                             path_to_frames, path_to_movie, path_to_geometry)
            all_copy_list.extend(copy_list)
    # all_copy_list = [上传阿里云的文件列表]
    # update_code = [shotgun创建更新事件列表]
    # version_id_code = [最新版本id:版本名]
    return all_copy_list, update_code, version_id_code


def get_oss_path(kwargs, _type, upload_type):
    # 获取shotgun上面的阿里云，以及publish 路径规范
    project_name = kwargs["project"]
    custom_entity_list = sg.find_one_shotgun('CustomEntity01', [
                ['project', 'name_is', project_name], ['sg_type', 'is', _type], ['sg_upload_type', 'is', upload_type]],
                                                    ["sg_oss_submit_path", "sg_pattern"])

    oss_path = custom_entity_list["sg_oss_submit_path"]
    copy_path = custom_entity_list["sg_pattern"]
    return oss_path, copy_path


def get_inside_copy_list(*args):
    # 获取内部人员上传阿里云的copy_list。
    copy_list = []
    oss_version_path, publish_version_path, path_to_frames, path_to_movie, path_to_geometry = args
    copy_list.append([path_to_frames, path_to_frames.replace(publish_version_path, oss_version_path)])
    copy_list.append([path_to_movie, path_to_movie.replace(publish_version_path, oss_version_path)])
    if path_to_geometry in path_to_frames or path_to_geometry in path_to_movie:
        if os.path.isdir(path_to_geometry):
            for each_f in os.listdir(path_to_geometry):
                f_path = path_to_geometry + '/' + each_f
                f_path = f_path.replace('//', '/')
                if os.path.isdir(f_path):
                    copy_list.append([f_path, f_path.replace(publish_version_path, oss_version_path)])
    else:
        copy_list.append([path_to_geometry,
                          path_to_geometry.replace(publish_version_path, oss_version_path)])

    return copy_list


def update_sg(kwargs, *args):
    # 用于获取在shotgun上面创建给外包的反馈
    create_note_code = []
    link_version_list = []
    outsource_id_list, version_id_code = args
    proposer = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', kwargs['user']]], ['code', 'sg_login'])
    project = shotgun_operations.find_one_shotgun('Project', [['name', 'is', kwargs['project']]], [])
    subject_tex = u'镜头任务更新通知'
    content_tex = u'以下镜头任务已更新至云:\n{}\n请及时下载.'.format(version_id_code.values())
    for i in version_id_code.keys():
        link_version_list.append({"type": "Version", "id": i})

    for outsource_id in outsource_id_list:
        note_content = {'project': project,
                        'subject': subject_tex,
                        'note_links': link_version_list,
                        'sg_proposer': proposer,
                        'addressings_to': [{'id': outsource_id, 'type': 'Group'}],
                        'content': content_tex,
                        'sg_if_read': False
                        }
        create_note_code.append(['create', 'Note', note_content])
    return create_note_code


def main(kwargs):
    # 拷贝文件

    all_assignees_id = get_assignees_people(kwargs)
    outsource_id_list, outsource_name_list = get_outsource_shot(all_assignees_id)
    oss_path, copy_path = get_oss_path(kwargs, "Shot", "Publish")
    all_copy_list, shotgun_event, version_id_code = get_latest_version(kwargs, oss_path, copy_path)
    create_note_code = update_sg(kwargs, outsource_id_list, version_id_code)
    shotgun_event.extend(create_note_code)
    window = approve_shot_task_ui.ApproveShotWin(parent=kwargs['widget'])
    window.show()
    window.addressings_lb.setText(",".join(outsource_name_list))
    window.publish_task_name.setText(",".join(version_id_code.values()))
    print "-------------------------all_copy_list---------------"
    pprint(all_copy_list)
    print "-------------------------shotgun_event---------------"
    pprint(shotgun_event)
    window.file_IO_publish.copy_list = all_copy_list
    window.write_data_base_thread.data = shotgun_event

