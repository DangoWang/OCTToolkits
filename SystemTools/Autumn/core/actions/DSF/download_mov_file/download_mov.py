#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8.26
###################################################################
from utils import shotgun_operations
import os
from dayu_widgets.message import MMessage
sg = shotgun_operations


def get_task_info(download_dict, local_path):
    copy_file_list = []
    _id = download_dict['id']
    project_name = download_dict['project']
    version_dict = download_dict.copy()
    version_dict['id'] = []
    no_version_task = []
    if version_dict['type'] == "Task":
        version_info_list = sg.find_shotgun("Version", [
            ["sg_task.Task.id", "in", _id],
            ['project', 'name_is', project_name]],
                                       ['code', "sg_path_to_movie", "created_at", "entity.Shot.sg_sequence",
                                        "sg_task.Task.id"],
                                       [{'field_name': 'created_at', 'direction': 'desc'}])
        task_id_version = {}
        for task_id in _id:
            for version_info in version_info_list:
                if task_id == version_info["sg_task.Task.id"]:
                    task_id_version[task_id] = version_info
                    break
                else:
                    no_version_task.append(task_id)
        for newest_version in task_id_version.values():
            file_list = get_copy_list(newest_version, local_path)
            copy_file_list.append(file_list)

    elif version_dict['type'] == "Version":
        version_info_list = sg.find_shotgun("Version", [["id", "in", _id], ['project', 'name_is', project_name]],
                                            ['code', "sg_path_to_movie", "created_at", "entity.Shot.sg_sequence"])
        for version_info in version_info_list:
            file_list = get_copy_list(version_info, local_path)
            copy_file_list.append(file_list)

    return copy_file_list, no_version_task


def get_copy_list(version_info, local_path):
    sequence = version_info['entity.Shot.sg_sequence']
    scene = sequence['name'] if sequence else None
    movie_path = version_info['sg_path_to_movie']
    mov_name = os.path.split(movie_path)[-1]
    local_mov_path = local_path + scene + "/" + mov_name
    file_list = [movie_path, local_mov_path]
    return file_list


def get_files(*args):
    window, download_dict = args
    if not window.folder_path:
        MMessage.config(2)
        MMessage.error(u'请先选择路径!', parent=download_dict["widget"])
        return
    copy_file_list, no_version_task = get_task_info(download_dict, window.folder_path)
    if copy_file_list:
        window.get_files_pb.setText(u"正在下载...")
        window.get_files_pb.setDisabled(True)
        window.progress_label.show()
        window.progress.show()
        window.progress_label.setText(u'准备开始...')
        window.progress.setValue(0)
        window.fetching_copy_thread.copy_list = copy_file_list
        window.fetching_copy_thread.start()


def main(download_dict):
    import download_mov_ui
    from dayu_widgets import dayu_theme
    window = download_mov_ui.DownloadWindow(parent=download_dict["widget"])
    dayu_theme.apply(window)
    window.get_files_pb.clicked.connect(lambda: get_files(window, download_dict))
    window.show()
