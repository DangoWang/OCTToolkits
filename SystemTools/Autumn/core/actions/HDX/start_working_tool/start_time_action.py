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
    start_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    batch_data = []
    for _id in task_info_dict["id"]:
        data = {
            "start_date": str(start_time),
            "sg_status_list": "ip"
        }
        batch_data.append({"request_type": "update", "entity_type": "Task", "entity_id": _id, "data": data})
    sg.batch_shotgun(batch_data)
    MMessage.config(2)
    MMessage.success(str(start_time) + u'开始制作，制作状态已改为制作中', parent=task_info_dict["widget"])
