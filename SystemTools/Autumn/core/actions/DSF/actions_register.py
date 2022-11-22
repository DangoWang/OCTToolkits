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
            DSF=dict(Shot=[],
                    Asset=[],
                    Version=[{'label': u'下载全部', 'value': 'version_download', 'icon': 'down_fill.svg', 'mode': '1',},
                             {'label': u'RV播放', 'value': 'version_video_player', 'icon': 'media_line.svg', 'mode': '1',},
                             {'label': u'发布该版本', 'value': 'publish_file', 'icon': 'upload_line.svg', 'mode': '1', },
                             {'label': u'修改提交', 'value': 'modify_submit', 'icon': 'edit_fill.svg', 'mode': '1', },
                             # {'label': u'验证通过', 'value': 'confirm_version', 'icon': '', 'mode': '1', },
                             {'label': u'下载缓存', 'value': 'download_cache', 'icon': 'down_fill.svg', 'mode': '1', },
                             {'label': u'锁定版本', 'value': 'lock_version', 'icon': 'success_fill.svg', 'mode': '1',},
                             {'label': u'同步外包', 'value': 'upload_to_outsource', 'icon': 'upload_line.svg', 'mode': '1',},
                             {'label': u'添加反馈', 'value': 'add_note', 'icon': 'upload_line.svg', 'mode': '1',},
                             {'label': u'添加版本描述', 'value': 'add_description', 'icon': 'add_line.svg', 'mode': '1',},
                             {'label': u'下载最新版本mov', 'value': 'download_mov_file', 'icon': 'down_fill.svg', 'mode': '1',},
                             ],
                    Task=[{'label': u'下载最新版本', 'value': 'task_download', 'icon': 'down_fill.svg', 'mode': '1',},
                          {'label': u'RV中打开', 'value': 'task_video_player', 'icon': 'media_line.svg', 'mode': '1',},
                          {'label': u'批量上传', 'value': 'batch_submit', 'icon': 'tree_view.svg', 'mode': '1',},
                          #{'label': u'任务详情', 'value': 'task_details', 'icon': 'detail_line.svg', 'mode': '1',},
                          {'label': u'上传文件', 'value': 'upload_local_file', 'icon': 'cloud_line.svg', 'mode': '1',},
                          {'label': u'批量发布', 'value': 'batch_publish', 'icon': 'upload_line.svg', 'mode': '1',},
                          # {'label': u'提交文件', 'value': 'upload_local_file', 'icon': 'cloud_line.svg', 'mode': '1',},
                          {'label': u'上传Daily', 'value': 'upload_daily', 'icon': 'upload_line.svg', 'mode': '1',},
                          # {'label': u'工时提交', 'value': 'time_declare', 'icon': 'upload_line.svg', 'mode': '1',},
                          {'label': u'导出abc缓存', 'value': 'export_abc', 'icon': 'upload_line.svg', 'mode': '1',},
                          {'label': u'查看反馈', 'value': 'view_note', 'icon': 'tree_view.svg', 'mode': '1',},
                          {'label': u'查看资产连接', 'value': 'view_link_asset', 'icon': 'tree_view.svg', 'mode': '1',},
                          {'label': u'开始制作', 'value': 'start_making', 'icon': 'tree_view.svg', 'mode': '1',},
                          {'label': u'查看制作说明', 'value': 'view_task_description', 'icon': 'tree_view.svg', 'mode': '1',},
                          {'label': u'添加任务描述', 'value': 'add_description', 'icon': 'upload_line.svg', 'mode': '1',},
                          {'label': u'编辑工作日志', 'value': 'edit_work_log', 'icon': 'tree_view.svg', 'mode': '1',},
                          {'label': u'同步镜头文件', 'value': 'upload_shot_task', 'icon': 'upload_line.svg', 'mode': '1',},
                          {'label': u'下载最新版本mov', 'value': 'download_mov_file', 'icon': 'down_fill.svg', 'mode': '1',},
                          {'label': u'批量上传Daily', 'value': 'batch_upload_daily', 'icon': 'upload_line.svg', 'mode': '1',},
                          ],
                    Note=[{'label': u'标为已读', 'value': 'mark_read', 'icon': 'success_line.svg', 'mode': '1',},
                          {'label': u'查看详情', 'value': 'note_details', 'icon': 'success_line.svg', 'mode': '1',}],
                    Ticket=[{'label': u'编辑日志', 'value': 'edit_ticket_log', 'icon': 'success_line.svg', 'mode': '1',},
                            {'label': u'转交工单', 'value': 'assignment_task', 'icon': 'success_line.svg', 'mode': '1',}]
          ))

#  kwargs:{
#            'id': list,
#            'type': str,
#            'user': str,
#            'project': str,
#  }


@permission_control()
def modify_submit(kwargs):
    from modify_submit_tool import main as modify_submit_win
    win = modify_submit_win.ModifySubmit(parent=kwargs['widget'])
    win.parse_data(kwargs)
    win.show()


@permission_control()
def version_download(kwargs):
    import download_tool.file_download_ui
    reload(download_tool.file_download_ui)
    download_tool.file_download_ui.main(kwargs)


# @permission_control()
def task_download(kwargs):
    import download_tool.file_download_ui as win
    reload(win)
    win.main(kwargs)


@permission_control()
def version_video_player(kwargs):
    import open_in_rv_tool.video_player as aavp
    reload(aavp)
    aavp.playing_version(kwargs)


@permission_control()
def task_video_player(kwargs):
    import open_in_rv_tool.video_player as acav
    reload(acav)
    acav.playing_task(kwargs)


@permission_control(forbidden=['outsource'])
def batch_submit(kwargs):
    batch_submit_header = [
        {
            'label': u'ma文件',
            'key': 'ma'}, {'label': u'预览文件', 'key': 'preview'},
        {'label': u'版本', 'key': 'version'}, {'label': u'ma文件路径', 'key': 'ma_path'},
        {'label': u'mov文件路径', 'key': 'mov_path'}]
    import batch_submit_tool.batch_submit_ui as agab
    reload(agab)
    batch_submit_win = agab.BatchSubmitWindow(parent=kwargs['widget'])
    batch_submit_win.set_header(batch_submit_header)
    batch_submit_win.show()
    batch_submit_win.show_log()


# @permission_control()
# # def task_details(kwargs):
# #     import detail_page_tool.detail_page_ui
# #     reload(detail_page_tool.detail_page_ui)
# #     drawer = detail_page_tool.detail_page_ui.task_detail_drawer(kwargs['widget'], kwargs)
# #     drawer.setMinimumWidth(500)
# #     drawer.show()


@permission_control(allowance=['artist', 'admin', 'supervisor', 'outsource', 'producer'])
def upload_local_file(kwargs):
    import submit_tool.upload_file_local_action as submit
    reload(submit)
    submit.upload_local_file(kwargs)


@permission_control(allowance=['artist', 'admin', 'supervisor'])
def time_declare(kwargs):
    import time_declare_tool.time_declare as time_declare
    reload(time_declare)
    time_declare.time_declare(kwargs)


# @permission_control(allowance=['artist', 'admin', 'supervisor', 'producer'])
def upload_daily(kwargs):
    from submit_daily_tool import submit_daily_ui
    reload(submit_daily_ui)
    window = submit_daily_ui.SubmitDailyWindow(task_dict_info=kwargs, parent=kwargs["widget"])
    window.show()


@permission_control(allowance=['artist', 'admin', 'supervisor', 'producer'])
def batch_upload_daily(kwargs):
    from submit_daily_tool import batch_submit_daily_ui
    reload(batch_submit_daily_ui)
    window = batch_submit_daily_ui.BatchSubmitDaily(parent=kwargs["widget"])
    window.show()
    window.show_log()


@permission_control(allowance=['artist', 'admin', 'supervisor', 'producer'])
def publish_file(kwargs):
    import publish_tool.publish_file_action as publish_file_action
    reload(publish_file_action)
    publish_file_action.publish_file(kwargs)


@permission_control(forbidden=['outsource'])
def export_abc(kwargs):
    import export_cache_tool.export_abc_ui
    reload(export_cache_tool.export_abc_ui)
    export_cache_tool.export_abc_ui.ExportAbc(task_dict=kwargs, parent=kwargs['widget']).show()


@permission_control(forbidden=['outsource'])
def view_note(kwargs):
    import view_note_tool.view_note_ui as view_note_t
    reload(view_note_t)
    drawer = view_note_t.view_note_drawer(kwargs['widget'], kwargs)
    drawer.setMinimumWidth(500)
    drawer.show()


@permission_control(forbidden=['outsource'])
def download_cache(kwargs):
    import download_cache_tool.download_cache
    reload(download_cache_tool.download_cache)
    download_cache_tool.download_cache.DownloadCacheFile(kwargs)


# @permission_control(forbidden=['outsource'])
# def confirm_version(kwargs):
#     import approve_tool
#     approve_tool.confirm_version_doit(kwargs)

@permission_control(allowance=['producer', 'admin'])
def upload_to_outsource(kwargs):
    import approve_tool.approve_task_version
    reload(approve_tool.approve_task_version)
    approve_tool.approve_task_version.main(kwargs, work_mode='upload')


@permission_control(allowance=['producer', 'admin'])
def add_note(kwargs):
    import create_note_tool.create_note_ui
    reload(create_note_tool.create_note_ui)
    create_note_tool.create_note_ui.CreateNoteUI(version_info_dict=kwargs, parent=kwargs['widget']).show()


@permission_control()
def add_description(kwargs):
    import add_description.add_desc
    reload(add_description.add_desc)
    add_description.add_desc.AddVersionDesc(version_info_dict=kwargs, parent=kwargs['widget']).show()


@permission_control(allowance=['admin', 'supervisor'])
def lock_version(kwargs):
    import approve_tool.approve_task_version as atv
    reload(atv)
    atv.main(kwargs, work_mode='approve')


@permission_control()
def view_link_asset(kwargs):
    import view_linked_assets_by_shots_tool.view_link_assets_ui as view_link_assets_ui
    reload(view_link_assets_ui)
    drawer = view_link_assets_ui.link_asset_drawer(kwargs['widget'], kwargs)
    drawer.setMinimumWidth(500)
    drawer.show()


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
    from SystemTools.MessageBox import note_details_win
    reload(note_details_win)
    note_details_win.main(kwargs)


@permission_control()
def view_task_description(kwargs):
    import view_task_description_tool.view_task_description as view_description
    reload(view_description)
    view_description.ViewProduction(task_dict=kwargs, parent=kwargs['widget']).show()


@permission_control(forbidden=['outsource'])
def batch_publish(kwargs):
    import batch_publish.batch_publish_main as bp
    reload(bp)
    win = bp.BatchPublish(kwargs=kwargs, parent=kwargs['widget'])
    win.show()


@permission_control()
def edit_work_log(kwargs):
    from work_log_tool import work_log_ui
    reload(work_log_ui)
    win = work_log_ui.WorkLogClass(task_dict=kwargs, parent=kwargs['widget'])
    win.show()


@permission_control()
def edit_ticket_log(kwargs):
    from work_log_tool import ticket_work_log
    reload(ticket_work_log)
    win = ticket_work_log.WorkLogClass(task_dict=kwargs, parent=kwargs['widget'])
    win.show()


@permission_control()
def upload_shot_task(kwargs):
    from batch_approve_shot_task import approve_shot_task
    reload(approve_shot_task)
    approve_shot_task.main(kwargs)


@permission_control()
def download_mov_file(kwargs):
    from download_mov_file import download_mov
    reload(download_mov)
    download_mov.main(kwargs)


@permission_control()
def assignment_task(kwargs):
    import SystemTools.Ticket_System.ticket_function as ticket_win
    reload(ticket_win)
    win = ticket_win.AssignmentTask(kwargs, parent=kwargs['widget'])
    win.show()
