#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################

from dayu_widgets.qt import *
from utils import shotgun_operations
sg = shotgun_operations
import batch_submit_daily
from pprint import pprint


class CreateDaily(QThread):
    finished = Signal(bool)
    progress = Signal(list)  # 正在拷贝的文件名和进度

    def __init__(self, task_info_list=''):
        super(CreateDaily, self).__init__()
        self.task_info_list = task_info_list

    def run(self):
        if self.task_info_list:
            project_name = sg.get_project()
            daily_describe = self.task_info_list[1]
            user_name = self.task_info_list[2]["sg_login"]
            for table_info in self.task_info_list[0]:
                task_id = int(table_info["task_id"])
                mov_path = table_info["mov"]
                create_daily_info = {"daily_file": mov_path, "id": task_id, "type": "Task",
                                     "project": project_name, "user": user_name, "describe": daily_describe}
                task_info = batch_submit_daily.get_task_name(create_daily_info)
                task_content = task_info["content"]
                task_entity = task_info["entity"]
                task_step_code = task_info["step.Step.code"]
                create_daily_info.update({"content": task_content, "entity": task_entity, "step_code": task_step_code})
                return_info_list = batch_submit_daily.copy_daily_file(create_daily_info, self.task_info_list[2])
                # return_info_list = ["拷贝列表", "审核人列表", "daily版本名" ]
                self.progress.emit([task_id, return_info_list, create_daily_info])
                # create_daily_info = ["daily_file":mov_path, "id":任务id, "type"：任务类型, "project":project,
                # "user": user_name, "describe": daily_describe, "content"：任务名， "entity":entity]
            self.finished.emit(True)

