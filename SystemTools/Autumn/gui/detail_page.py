#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################

from dayu_widgets.qt import *
from utils import shotgun_operations
sg = shotgun_operations
from pprint import pprint
from dayu_widgets.message import MMessage
from config import GLOBAL
image_types = GLOBAL.format_file["picture"]
video_types = GLOBAL.format_file["video"]


class ShowDetailInfo(QThread):
    finished = Signal(bool)
    progress = Signal(list)  # 正在拷贝的文件名和进度

    def __init__(self, task_info_list=''):
        super(ShowDetailInfo, self).__init__()
        self.task_info_list = task_info_list
        self.mute = 0

    def run(self):
        task_id = self.task_info_list["id"][0]
        version_info_list = sg.find_shotgun("Version", [
            ["sg_task.Task.id", "is", task_id], ['project', 'name_is', self.task_info_list["project"]]],
                                            ["code", "description", "sg_status_list", "sg_version_number",
                                             "sg_path_to_frames",
                                             "sg_path_to_movie", "id", "user", "sg_task.Task.sg_latestversion"])
        version_dict = {"_id": "",
                        "user": "",
                        "project_file": "",
                        "preview_file": "",
                        "task_id": "",
                        "config": ""}
        if version_info_list:
            for v, version_info in enumerate(version_info_list):
                if version_info["sg_version_number"] == version_info["sg_task.Task.sg_latestversion"]:
                    version_dict.update({
                        "_id": version_info["id"],
                        "user": (version_info.get("user") or {}).get('name', ''),
                        "project_file": version_info["sg_path_to_frames"],
                        "preview_file": version_info["sg_path_to_movie"],
                        "task_id": task_id,
                        "config": self.task_info_list["config"]
                    })
                    break
        self.progress.emit(version_dict)
        self.finished.emit(True)



