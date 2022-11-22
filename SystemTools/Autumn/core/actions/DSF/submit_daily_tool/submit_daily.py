#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9.3
###################################################################
from PySide.QtCore import *
import datetime
import os
from utils import shotgun_operations
from utils import fileIO


sg = shotgun_operations


def get_task_info(task_info_dict):
    _content = task_info_dict['content']
    _type = task_info_dict['type']
    _id = task_info_dict['id']
    task_entity_id = {"content": _content, "id": _id, "type": _type}
    return task_entity_id


def copy_daily_file(task_info_dict, group_list):
    permission = group_list["sg_permission_group"]
    _content = task_info_dict['content']
    local_daily_path = task_info_dict['daily_file']
    project_name = task_info_dict['project']
    local_attachment_path = task_info_dict['attachment']
    task_entity_id = get_task_info(task_info_dict)
    task_info = sg.find_one_shotgun("Task", [['project', 'name_is', project_name],
                                                         ["id", "is", task_entity_id["id"]]],
                                                ["task_reviewers", 'entity', 'content'])
    entity_task_name = task_info['entity']['name'] + '_' + task_info['content']
    all_tasks = sg.get_tasks(sg.get_project(), sg.get_user())
    if entity_task_name not in all_tasks.keys():
        return
    task_detail = all_tasks.get(entity_task_name)
    reviewers_people_list = task_info["task_reviewers"]
    # user_name = task_info_dict['user']
    entity_name = task_info_dict["entity"]
    custom_entity_list = sg.find_one_shotgun('CustomEntity01', [
        ['project', 'name_is', project_name], ['sg_type', 'is', entity_name["type"]],
        ['sg_upload_type', 'is', 'Dailies']], ["sg_pattern", "sg_work_file_name",
                                               "sg_prev_file_name", "sg_oss_submit_path", "sg_attachment_no_version"])
    step_code_name = task_info_dict["step.Step.code"]
    version_code = custom_entity_list["sg_work_file_name"].format(**task_detail)
    # daily_file_name = 无版本号的预览文件名
    daily_file_name = custom_entity_list["sg_prev_file_name"].format(**task_detail)

    # server_path = 如果是外包就是阿里云daily路径， 否则就是十月内部服务器daily路径
    server_path = custom_entity_list['sg_pattern'].format(**task_detail) if \
        permission not in ['outsource'] else \
        custom_entity_list["sg_oss_submit_path"].format(**task_detail)

    # sg_pattern_path = 十月服务器上daily
    sg_pattern_path = custom_entity_list['sg_pattern'].format(**task_detail)

    server_daily_path = server_path + "/" + daily_file_name + os.path.splitext(local_daily_path)[-1]
    #  server_daily_path = 如果是外包就是阿里云daily路径， 否则就是十月内部服务器daily路径

    path_to_mov = sg_pattern_path + "/" + daily_file_name + os.path.splitext(local_daily_path)[-1]
    # shotgun 上面sg_path_to_movie 显示的路径
    if local_attachment_path:
        attachment_file_path = server_path + "/" + custom_entity_list["sg_attachment_no_version"]
        #   服务器上daily附件路径
    else:
        attachment_file_path = ""

    #  如果人员是外包 server_daily_path 是阿里云对应的daily路径
    copy_file_list = [[local_daily_path, server_daily_path]]
    copy_attachment_list = fileIO.get_copy_list(local_attachment_path, attachment_file_path)
    copy_file_list.extend(copy_attachment_list)   # 工程文件与附件列表
    # copy_file_list = [[本地路径， 服务器路径（如果是外包就是阿里云路径）]]
    if permission in ['outsource']:
        rpc_copy_list = [[server_path, sg_pattern_path]]
    else:
        rpc_copy_list = []
    # rpc_copy_list = 发送给十月的路径列表[[阿里云路径， 十月内部提交daily的服务器路径]，
    # [阿里云附件路径， 十月内部附件路径]]

    return_info_list = [copy_file_list, reviewers_people_list, version_code,
                        attachment_file_path, rpc_copy_list, path_to_mov]
    return return_info_list


def create_daily_version(task_info_dict, return_info_list, attachment_file):
    reviewers_people_list = return_info_list[1]
    version_code = return_info_list[2]
    if attachment_file:
        attachment_file_path = return_info_list[3]
    else:
        attachment_file_path = ""
    task_entity_id = get_task_info(task_info_dict)
    project_name = task_info_dict['project']
    project_info = sg.find_one_shotgun('Project', [['name', 'is', project_name]], ['id'])
    describe = task_info_dict['describe']
    path_to_movie = return_info_list[-1]
    mov_display_name = os.path.split(path_to_movie)[-1]
    user_name = task_info_dict['user']
    group_list = get_group_list(user_name)
    del group_list["sg_permission_group"]
    today_daily_info = sg.find_one_shotgun("Version", [['project', 'name_is', project_name],
                                                       ["sg_task", "is", task_entity_id],
                                                       ["sg_version_type", "is", "Dailies"],
                                                       ["code", "is", version_code]], ["id"])
    if not today_daily_info:
        data = {'project': project_info,
                'sg_path_to_movie': path_to_movie,
                'code': version_code,
                'entity': task_info_dict['entity'],
                'user': group_list,
                'description': describe,
                'sg_task': task_entity_id,
                'sg_version_type': 'Dailies',
                'sg_version_number': 'None',
                'sg_status_list': 'rev',
                'sg_path_to_geometry': attachment_file_path
                }
        version_info = sg.create_shotgun("Version", data)
        version_id = version_info['id']
        version_info_list = [{"id": version_id, "name": version_code, 'type': 'Version'}]
        title = u"审核通知:{}".format(version_code)
        content_text = u"{} Daily任务已上传,请审核".format(version_code)
        note_info_dict = {"reviewers_people": reviewers_people_list, "project": project_info,
                          "subject": title, "user": group_list,
                          "version_id_code": version_info_list, "content": content_text}
        create_note(note_info_dict)
        return version_id, path_to_movie, mov_display_name
    else:
        version_id = today_daily_info["id"]
        data_note = {"description": describe}
        sg.update_shotgun("Version", version_id, data_note)
        update_version_id_code = [{"id": version_id, "name": version_code, 'type': 'Version'}]
        title = u"审核通知:{}".format(version_code)
        content_text = u"{} Daily任务已覆盖上传,请审核".format(version_code)
        note_info_dict = {"reviewers_people": reviewers_people_list, "project": project_info,
                          "subject": title, "user": group_list,
                          "version_id_code": update_version_id_code, "content": content_text}
        create_note(note_info_dict)
        return version_id, path_to_movie, mov_display_name


def upload_mov(*args):
    version_id, daily_path, mov_display_name = args
    sg.upload_shotgun("Version", version_id, daily_path, field_name="sg_uploaded_movie",
                      display_name=mov_display_name)


def create_note(note_info):
    note_data_list = []
    for reviewers in note_info["reviewers_people"]:
        reviewers_list = list()
        reviewers_list.append(reviewers)
        note_data = {
            "project": note_info["project"],
            "subject": note_info["subject"],
            "sg_proposer": note_info["user"],
            "addressings_to": reviewers_list,
            "content": note_info["content"],
            "sg_status_list": "opn",
            "sg_if_read": False,
            "note_links": note_info["version_id_code"]
        }
        note_data_list.append({"request_type": "create", "entity_type": "Note", "data": note_data})
    sg.batch_shotgun(note_data_list)


def get_task_name(task_dict):
    task_id = task_dict['id']
    project_name = task_dict['project']
    find_type = task_dict['type']
    user_name = task_dict['user']
    task_info = sg.find_shotgun("Task",
                                [['project', 'name_is', project_name], ["id", "is", task_id[0]]],
                                ["entity", "content", "id", "Project", "step.Step.code"])
    group_list = get_group_list(user_name)
    return task_info, group_list


def get_group_list(user_name):
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code", "sg_permission_group"])
    return group_list
