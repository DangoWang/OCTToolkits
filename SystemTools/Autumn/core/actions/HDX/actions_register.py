#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################

from ...decorators import *

# 这里用来存放所有的action入口函数

#  mode的0是双击，1是右键
actions_dict = dict(
            HDX=dict(Shot=[],
                    Asset=[],
                    Version=[],
                    Task=[
                          {'label': u'上传文件', 'value': 'submit_dailies', 'icon': 'cloud_line.svg', 'mode': '1',},
                        {'label': u'开始制作', 'value': 'start_making', 'icon': 'tree_view.svg', 'mode': '1', },
                    ],
                    Note=[{'label': u'标为已读', 'value': 'mark_read', 'icon': 'success_line.svg', 'mode': '1',},
                          {'label': u'查看详情', 'value': 'note_details', 'icon': 'success_line.svg', 'mode': '1',}
                          ],
                     Ticket=[{'label': u'编辑日志', 'value': 'edit_ticket_log', 'icon': 'success_line.svg', 'mode': '1', },
                             {'label': u'转交工单', 'value': 'assignment_task', 'icon': 'success_line.svg', 'mode': '1', }]
          ))

#  kwargs:{
#            'id': list,
#            'type': str,
#            'user': str,
#            'project': str,
#  }


# @permission_control(allowance=['artist', 'admin', 'supervisor', 'outsource'])
def submit_dailies(kwargs):
    from submit_tool import submit_main
    reload(submit_main)
    submit_win = submit_main.SubmitDoit(kwargs, parent=kwargs['widget'])
    submit_win.show()


@permission_control()
def mark_read(kwargs):
    id_note_list = kwargs['id']
    from SystemTools.MessageBox import unread_message_ui
    unread_message_ui.make_note_read(id_note_list)


@permission_control()
def start_making(kwargs):
    import start_working_tool.start_time_action as start_working
    reload(start_working)
    start_working.get_start_time(kwargs)


@permission_control()
def mark_read(kwargs):
    id_note_list = kwargs['id']
    from SystemTools.MessageBox import unread_message_ui
    unread_message_ui.make_note_read(id_note_list)


@permission_control()
def note_details(kwargs):
    id_note_list = kwargs['id']
    from SystemTools.MessageBox import note_details_win
    note_details_win.NoteDetailsMainWin(kwargs, kwargs['widget'])


@permission_control()
def edit_ticket_log(kwargs):
    from ..DSF.work_log_tool import ticket_work_log
    reload(ticket_work_log)
    win = ticket_work_log.WorkLogClass(task_dict=kwargs, parent=kwargs['widget'])
    win.show()


@permission_control()
def assignment_task(kwargs):
    import SystemTools.Ticket_System.ticket_function as ticket_win
    reload(ticket_win)
    win = ticket_win.AssignmentTask(kwargs, parent=kwargs['widget'])
    win.show()
