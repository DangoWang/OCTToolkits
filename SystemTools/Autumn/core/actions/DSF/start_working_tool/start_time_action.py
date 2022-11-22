#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.10.8
import time
from dayu_widgets.message import MMessage
from utils import shotgun_operations
sg = shotgun_operations


def get_start_time(task_info_dict):
    batch_data = []
    not_start_task = []
    start_task = []
    start_time_int = time.strftime('%Y%m%d', time.localtime(time.time()))
    start_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    task_info_list = sg.find_shotgun("Task", [["id", "in", task_info_dict["id"]],
                                              ["project", "name_is", task_info_dict["project"]]], ["start_date"])
    for task_info in task_info_list:
        if task_info["start_date"]:
            shotgun_start_data = task_info["start_date"].replace("-", "")
            print shotgun_start_data
            if int(start_time_int) >= int(shotgun_start_data):
                data = {"sg_date": str(start_time),
                        "sg_status_list": "ip"}
                batch_data.append({"request_type": "update", "entity_type": "Task",
                                   "entity_id": task_info["id"], "data": data})
                start_task.append(task_info["id"])
            else:
                not_start_task.append(task_info["id"])
        else:
            data = {"sg_date": str(start_time),
                    "sg_status_list": "ip"}
            batch_data.append({"request_type": "update", "entity_type": "Task",
                               "entity_id": task_info["id"], "data": data})
            start_task.append(task_info["id"])
    if not_start_task:
        MMessage.config(5)
        MMessage.warning(u"编号为{}的任务没到可以开始时间，暂时不能开始".format(not_start_task),
                         parent=task_info_dict["widget"])
    if start_task:
        sg.batch_shotgun(batch_data)
        MMessage.config(3)
        MMessage.success(u'编号为{}的开始制作，制作状态已改为制作中'.format(start_task), parent=task_info_dict["widget"])
   