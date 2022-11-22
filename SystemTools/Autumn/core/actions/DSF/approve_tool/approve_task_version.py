#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.10
# wechat : 18250844478
###################################################################
import os
# import pprint

from utils import shotgun_operations
# from dayu_widgets.qt import *
# from utils import fileIO
import approve_task_version_ui


def check_confirm_state(kwargs, work_mode):
    this_version = shotgun_operations.find_one_shotgun('Version', [['project', 'name_is', kwargs['project']],
                                                               ['id', 'in', kwargs['id']]],
                                                   ['code', 'sg_task.Task.id', 'project', 'sg_path_to_frames',
                                                    'sg_path_to_movie', 'sg_path_to_geometry', 'user', 'entity',
                                                    'sg_task', 'sg_version_type', 'sg_version_number',
                                                    'sg_task.Task.entity.Asset.shots',
                                                    'sg_task.Task.sg_approve_version', 'description'])
    #  现在只有资产才会确认同步
    if this_version['entity']['type'] not in ['Asset']:
        return this_version
    #  不同步给外包的话不需要发送工单
    # if work_mode in ['approve']:
    #     if not this_version['sg_version_type'] == 'Publish':
    #         QMessageBox.critical(kwargs['widget'], u'警告', u'以下版本非Publish版本，无法锁定！\n%s' % this_version['code'],
    #                              QMessageBox.Yes, QMessageBox.Yes)
    #         raise RuntimeError('')
    #     if not this_version['sg_version_number']:
    #         QMessageBox.critical(kwargs['widget'], u'警告', u'以下版本是不带版本号的版本，无法锁定！\n%s' % this_version['code'],
    #                              QMessageBox.Yes, QMessageBox.Yes)
    #         raise RuntimeError('')
    #     return this_version
    # # 去工单里查找该版本是否存在验证请求
    # the_ticket = \
    #     shotgun_operations.find_one_shotgun('Ticket',
    #                                         [['sg_link.Version.code', 'is', this_version['code']]],
    #                                         ['sg_examiners', 'sg_examine_notes']
    #                                         )
    # already_approved = this_version['sg_task.Task.sg_approve_version']
    # if already_approved and already_approved > this_version['sg_version_number']:
    #     QMessageBox.critical(kwargs['widget'], u'警告', u'正在同步的版本必须大于已同步版本！\n%s'% already_approved,
    #                          QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    # if not the_ticket:
    #     QMessageBox.critical(kwargs['widget'], u'警告', u'请先发送工单请求同步该版本！\n%s'% this_version['code'],
    #                       QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    # if not this_version['sg_version_type'] == 'Approved':
    #     QMessageBox.critical(kwargs['widget'], u'警告', u'以下版本非Approved版本，无法同步！\n%s'% this_version['code'],
    #                       QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    # if not this_version['sg_version_number']:
    #     QMessageBox.critical(kwargs['widget'], u'警告', u'以下版本是不带版本号的版本，无法同步！\n%s'% this_version['code'],
    #                       QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    # #  如果工单中指派了验证人，需要验证该验证人是否已经验证
    # unread_notes = []  # 未读notes
    # tested_tester = []  # 已验证的验证人
    # testers = [s['name'] for s in the_ticket['sg_examiners']]  # 所有应该验证的验证人
    # tested_info = the_ticket['sg_examine_notes']  # 所有验证的notes信息
    # for each_note in tested_info:  # 检查下有哪些人没有验证， 或者有哪些note没有读
    #     the_note = shotgun_operations.find_one_shotgun('Note',
    #                                                     [['id', 'is', each_note['id']]],
    #                                                    ['sg_proposer', 'sg_if_read'])
    #     if the_note['sg_proposer']['name'] in testers:
    #         tested_tester.append(the_note['sg_proposer']['name'])
    #     if not the_note['sg_if_read']:
    #         unread_notes.append(the_note['sg_proposer']['name'])
    # untested_tester = [t for t in testers if t not in tested_tester]  # 未验证的验证人的name
    # if untested_tester:
    #     untested_tester = ','.join(untested_tester)
    #     QMessageBox.critical(kwargs['widget'], u'警告',
    #                          u'该版本有以下人员未验证，请通知其验证！\n{}'.format(untested_tester),
    #                          QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    # if unread_notes:
    #     unread_notes = ','.join(unread_notes)
    #     QMessageBox.critical(kwargs['widget'], u'警告',
    #                          u'以下人员给的note未阅读，请前往工单系统确认阅读该消息！\n{}'.format(unread_notes),
    #                          QMessageBox.Yes, QMessageBox.Yes)
    #     raise RuntimeError('')
    return this_version


def get_copy_list(kwargs, this_version):
    #  所有人都验证了，现在开始同步到阿里云.注意，当附件路径为空时，文件名中必须包含版本的code才可以被同步
    all_copy_list = []
    # for version_to_upload in this_version:
    version_id = this_version['id']
    version_info_dict = shotgun_operations.get_version(kwargs['project'], version_id)
    path_convention = shotgun_operations.find_one_shotgun('CustomEntity01',
                                                          [['project', 'name_is', kwargs['project']],
                                                           ['sg_type', 'is', version_info_dict['type']],
                                                           ['sg_upload_type', 'is', 'Publish']
                                                           ],
                                                          ['sg_pattern', 'sg_oss_submit_path']
                                                          )
    publish_version_path = path_convention['sg_pattern'].format(**version_info_dict)
    oss_version_path = path_convention['sg_oss_submit_path'].format(**version_info_dict)
    copy_list = []
    copy_list.append([version_info_dict['sg_path_to_frames'],
                      version_info_dict['sg_path_to_frames'].replace(publish_version_path, oss_version_path)])
    copy_list.append([version_info_dict['sg_path_to_movie'],
                      version_info_dict['sg_path_to_movie'].replace(publish_version_path, oss_version_path)])
    if version_info_dict['sg_path_to_geometry'] in version_info_dict['sg_path_to_frames'] or \
        version_info_dict['sg_path_to_geometry'] in version_info_dict['sg_path_to_movie']:
        if os.path.isdir(version_info_dict['sg_path_to_geometry']):
            for each_f in os.listdir(version_info_dict['sg_path_to_geometry']):
                f_path = version_info_dict['sg_path_to_geometry'] + '/' + each_f
                f_path = f_path.replace('//', '/')
                if os.path.isdir(f_path):
                    copy_list.append([f_path, f_path.replace(publish_version_path, oss_version_path)])
                if os.path.isfile(f_path):
                    if this_version['code'] in f_path:
                        copy_list.append([f_path, f_path.replace(publish_version_path, oss_version_path)])
    else:
        copy_list.append([version_info_dict['sg_path_to_geometry'],
                          version_info_dict['sg_path_to_geometry'].replace(publish_version_path, oss_version_path)])
    all_copy_list.extend(copy_list)
    return all_copy_list


def update_sg(kwargs, this_version, work_mode, users_shots):
    # 写数据库
    # 更新 sg_approve_version
    update_code = []
    task_id = this_version['sg_task.Task.id']
    # shotgun_operations.update_shotgun('Task', task_id,
    #                                   {'sg_approve_version': this_version['sg_version_number']})
    # if work_mode in ['approve']:
    update_code.append(['update', 'Task', task_id, {'sg_approve_version': this_version['sg_version_number'],
                                                    # 'sg_status_list': 'fin'
                                                    }])
    # 把publish改成approve
    # approve_version_dict = this_version.copy()
    # del approve_version_dict['id']
    # del approve_version_dict['sg_task.Task.id']
    # del approve_version_dict['type']
    # approve_version_dict['sg_version_type'] = 'Approved'
    # if_existed = shotgun_operations.find_one_shotgun('Version',
    #                                        [['project', 'name_is', kwargs['project']],
    #                                         ['code', 'is', approve_version_dict['code']],
    #                                         ['sg_version_type', 'is', 'Publish']
    #                                         ], ['code'])
    # if work_mode in ['approve']:
    #     if if_existed:
    #         update_code.append(['update', 'Version', if_existed['id'], approve_version_dict])
    #         # shotgun_operations.update_shotgun('Version', if_existed['id'], approve_version_dict)
    #     else:
    #         QMessageBox.critical(kwargs['widget'], u'警告', u'未发现该Publish版本，无法更新类型，请联系TD！\n{}'.format(if_existed),
    #                              QMessageBox.Yes, QMessageBox.Yes)
    #         return
    #  创建通知
    #  由于发布的是版本信息，所以需要告知版本的user以及版本链接到的任务-->资产-->镜头-->user
    all_related_users, all_related_shots = users_shots
    all_related_shots_str = ','.join(all_related_shots)
    proposer = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', kwargs['user']]], ['code', 'sg_login'])
    project = shotgun_operations.find_one_shotgun('Project', [['name', 'is', kwargs['project']]], [])

    version_info_dict = shotgun_operations.get_version(kwargs['project'], this_version['id'])
    path_convention = shotgun_operations.find_one_shotgun('CustomEntity01', [['project', 'name_is', kwargs['project']],
                                                                             ['sg_type', 'is',
                                                                              version_info_dict['type']],
                                                                             ['sg_upload_type', 'is', 'Publish']],
                                                          ['sg_oss_submit_path'])
    for each_user in all_related_users:
        sg_attachment_path = None
        if work_mode in ['approve']:
            the_note = u'{}已锁定，描述:\n          {}\n关联镜头为：      {}\n请留意.'\
                            .format(this_version['code'], this_version['description'], all_related_shots_str)
        else:
            oss_version_path = path_convention['sg_oss_submit_path'].format(**version_info_dict)
            sg_attachment_path = oss_version_path
            the_note = u'{}已同步至云，描述:\n          {}\n关联镜头为：      {}\n请及时下载.'.format(this_version['code']
                                                                                   , this_version['description'
                                                                                   ], all_related_shots_str)
        note_content = {'project': project,
                        'subject': u'资产更新通知:%s' % this_version['code'],
                        'note_links': [{'id': this_version['id'], 'type': 'Version'}],
                        'sg_proposer': proposer,
                        'addressings_to': [{'id': each_user['id'], 'type': 'Group'}],
                        'content': the_note,
                        'sg_attachment_path': sg_attachment_path,
                        'sg_if_read': False
                        }
        update_code.append(['create', 'Note', note_content])
    return update_code


def get_users(kwargs, version_info, work_mode):
    all_users = []
    this_user = shotgun_operations.find_one_shotgun('Group', [['id', 'is', version_info['user']['id']]], ['code', 'sg_login'])
    all_users.append(this_user)
    all_related_shots = version_info['sg_task.Task.entity.Asset.shots']
    all_shots_names = [s['name'] for s in all_related_shots]
    all_groups = shotgun_operations.find_shotgun('Group', [['sg_group_project', 'name_contains', kwargs['project']]],
                                                ['sg_permission_group', 'code'])
    for each_user in all_groups:
        if each_user['code'] == this_user['code'] or not each_user['sg_permission_group']:
            continue
        if each_user['sg_permission_group'] in ['outsource']:
            if work_mode not in ['approve']:
                related_task = shotgun_operations.find_one_shotgun('Task', [['project', 'name_is', kwargs['project']],
                                                                            ['task_assignees', 'name_contains', each_user['code']],
                                                                            ['entity', 'in', all_related_shots]], [])
                if related_task:
                    all_users.append(each_user)
        else:
            if work_mode in ['approve']:
                related_task = shotgun_operations.find_one_shotgun('Task', [['project', 'name_is', kwargs['project']],
                                                                            ['task_assignees', 'name_contains', each_user['code']],
                                                                            ['entity', 'in', all_related_shots]], [])
                if related_task:
                    all_users.append(each_user)
    # dealed_users = []
    # if all_related_shots:
    #     for each in all_related_shots:
    #         shot_tasks = shotgun_operations.find_shotgun('Task', [['project', 'name_is', kwargs['project']],
    #                                                           ['entity', 'is', each]], ['task_assignees'])
    #         for each_task in shot_tasks:
    #             for task_assignees in each_task['task_assignees']:
    #                 if task_assignees in dealed_users:
    #                     continue
    #                 dealed_users.append(task_assignees)
    #                 task_assignees_permission = shotgun_operations.get_permission(task_assignees['id'])
    #                 if task_assignees['id'] != this_user['id'] and task_assignees not in all_users:
    #                     if task_assignees_permission in ['outsource']:  # 如果是外包， 只有在同步文件（不是锁定文件）的情况下才通知
    #                         if work_mode not in ['approve']:
    #                             all_users.append(task_assignees)
    #                     else:
    #                         if work_mode in ['approve']:
    #                             all_users.append(task_assignees)
    return all_users, all_shots_names


def main(kwargs, work_mode):
    version_info = check_confirm_state(kwargs, work_mode)
    all_copy_list = get_copy_list(kwargs, version_info)
    users_shots = get_users(kwargs, version_info, work_mode)
    update_code = update_sg(kwargs, version_info, work_mode, users_shots)
    related_users = [user['code'] for user in get_users(kwargs, version_info, work_mode)[0]]
    # 拷贝文件
    window = approve_task_version_ui.ApprovedFileAction(parent=kwargs['widget'])
    window.work_mode = work_mode
    window.publishd_task_name_label.setText(version_info['code'])
    window.des_lb.setText(version_info['description'])
    users_text = ','.join(related_users[:5]) + ',\n' + ','.join(related_users[5:])
    window.addressings_lb.setText(users_text)
    window.file_IO_publish.copy_list = all_copy_list
    window.write_data_base_thread.data = update_code
    window.show()


