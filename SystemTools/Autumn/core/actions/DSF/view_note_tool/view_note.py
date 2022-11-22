#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
from utils import shotgun_operations
from dayu_widgets.qt import *
sg = shotgun_operations


def get_version__note_dict(task_dict, _type):
    version_name = []
    version_note_list = []
    task_id = task_dict["id"][0]
    version_info_list = sg.find_shotgun("Version", [
        ["sg_task.Task.id", "is", task_id], ['project', 'name_is', task_dict["project"]],
        ["sg_version_type", "is", _type]],
        ["code", "id", "open_notes"])
    if version_info_list:
        for v, version_info in enumerate(version_info_list):
            id_list = []
            version_name.append(version_info["code"])
            note_list = version_info["open_notes"]
            for note in note_list:
                id_list.append(note["id"])
            version_note_dict = {version_info["code"]: id_list}
            version_note_list.append(version_note_dict)
    return version_name, version_note_list


def get_group_list(user_name):
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code", "sg_permission_group"])
    return group_list



