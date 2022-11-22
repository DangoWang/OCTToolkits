#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8.27
###################################################################

import subprocess
import os
from utils import shotgun_operations
from dayu_widgets.message import MMessage
from config import GLOBAL
sg = shotgun_operations


def playing_version(dict_info):
    mov_path = []
    version_id = dict_info['id']
    project_name = dict_info['project']
    find_type = dict_info['type']
    for v in range(0, len(version_id)):
        version_info = sg.find_shotgun(find_type, [
            ["id", 'is', version_id[v]], ['project', 'name_is', project_name]], ['sg_path_to_movie'])
        mov_path.append(version_info[0]['sg_path_to_movie'])
    print mov_path
    if mov_path:
        rv_path = GLOBAL.RVPATH
        if os.path.isfile(rv_path):
            subprocess.Popen(rv_path+' ' + (' '.join(mov_path)))
        else:
            MMessage.config(1)
            MMessage.warning(u'没有找到RV播放器！', parent=dict_info['widget'])
    else:
        MMessage.config(1)
        MMessage.warning(u'没有可以播放的视频文件！', parent=dict_info['widget'])


def playing_task(dict_info):
    mov_path = []
    task_id = dict_info['id']
    project_name = dict_info['project']
    find_type = dict_info['type']
    for t in range(0, len(task_id)):
        version_info_list = sg.find_shotgun("Version",[
            ["sg_task.Task.id", "is", task_id[t]], ['project', 'name_is', project_name]],
            ['sg_path_to_movie', "sg_version_number","sg_task.Task.sg_latestversion"])
        if version_info_list:
            for v, version_info in enumerate(version_info_list):
                if version_info["sg_version_number"] == version_info["sg_task.Task.sg_latestversion"]:
                    mov_path.append(version_info['sg_path_to_movie'])
                    break
    if mov_path:
        rv_path = GLOBAL.RVPATH
        if os.path.isfile(rv_path):
            subprocess.Popen(rv_path+' ' + (' '.join(mov_path)))
        else:
            MMessage.config(1)
            MMessage.warning(u'没有找到RV播放器！', parent=dict_info['widget'])
    else:
        MMessage.config(1)
        MMessage.warning(u'没有可以播放的视频文件！', parent=dict_info['widget'])
