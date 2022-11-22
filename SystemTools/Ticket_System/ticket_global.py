#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__)).replace("\\", "/"))
import ticket_function


def get_ticket_config(user_name):
    all_ticket_complete = {"page_title": u'未完成的工单', "page_icon": "calendar_line.svg",
                           "filters": [["sg_status_list", "is_not", "res"],
                                       ['sg_proposer', 'name_not_contains', u'刘总'],
                                       ['sg_proposer', 'name_not_contains', u'林总'],
                                       ['sg_proposer', 'name_not_contains', u'阎总'],
                                       ['project', 'name_not_contains', 'Demo: Game']
                                       ]}

    all_ticket_unfinished = {"page_title": u'已完成的工单', "page_icon": "calendar_line.svg",
                             "filters": [["sg_status_list", "is", "res"],
                                         ['sg_proposer', 'name_not_contains', u'刘总'],
                                         ['sg_proposer', 'name_not_contains', u'林总'],
                                         ['sg_proposer', 'name_not_contains', u'阎总'],
                                         ['project', 'name_not_contains', 'Demo: Game']
                                         ]}

    my_ticket_complete = {"page_title": u'未完成的工单', "page_icon": "calendar_line.svg",
                          "filters": [["sg_status_list", "is_not", "res"],
                                      ["sg_proposer.Group.sg_login", "is", user_name],
                                      ['project', 'name_not_contains', 'Demo: Game']]}
    my_ticket_unfinished = {"page_title": u'已完成的工单', "page_icon": "calendar_line.svg",
                            "filters": [["sg_status_list", "is", "res"], ['project', 'name_not_contains', 'Demo: Game'],
                                        ["sg_proposer.Group.sg_login", "is", user_name]]}
    return all_ticket_complete, all_ticket_unfinished, my_ticket_complete, my_ticket_unfinished


def get_examine_config(project_name, user_name_code):
    examine_complete_id, examine_unfinished_id = ticket_function.get_examiners_type(project_name, user_name_code)
    if examine_complete_id:
        my_examine_complete = {"page_title": u'已审核的工单', "page_icon": "calendar_line.svg",
                               "filters": [["id", "in", examine_complete_id]]}
    else:
        my_examine_complete = {"page_title": u'已审核的工单', "page_icon": "calendar_line.svg",
                               "filters": [["sg_proposer", "name_is", "False"]]}
    if examine_unfinished_id:
        my_examine_unfinished = {"page_title": u'未审核的工单', "page_icon": "calendar_line.svg",
                                 "filters": [["id", "in", examine_unfinished_id]]}

    else:
        my_examine_unfinished = {"page_title": u'未审核的工单', "page_icon": "calendar_line.svg",
                                 "filters": [["sg_proposer", "name_is", "False"]]}
    return my_examine_complete, my_examine_unfinished

