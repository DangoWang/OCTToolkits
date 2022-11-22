#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9.3
###################################################################
from PySide.QtCore import *
import datetime
import os
from utils import shotgun_operations
import re
import json
from pprint import pprint

sg = shotgun_operations
reload(sg)


def get_task_info(task_info_dict):
    _content = task_info_dict['content']
    _type = task_info_dict['type']
    _id = task_info_dict['id']
    task_entity_id = {"content": _content, "id": _id, "type": _type}
    return task_entity_id


def copy_daily_file(task_info_dict, group_list):
    _content = task_info_dict['content']
    local_daily_path = task_info_dict['daily_file']
    project_name = task_info_dict['project']
    task_entity_id = get_task_info(task_info_dict)
    # task_info = sg.find_one_shotgun("Task", [['project', 'name_is', project_name],
    #                                                      ["id", "is", task_entity_id["id"]]],
    #                                             ["task_reviewers", 'entity', 'content'])
    task_detail = sg.get_task(sg.get_project(), task_entity_id["id"])
    reviewers_people_list = task_detail["task_reviewers"]
    # entity_task_name = task_info['entity']['name'] + '_' + task_info['content']
    # if entity_task_name not in all_tasks.keys():
    #     return
    # task_detail = all_tasks.get(entity_task_name)
    # user_name = task_info_dict['user']
    # date = datetime.datetime.now().strftime('%Y-%m-%d')
    entity_name = task_info_dict["entity"]
    custom_entity_list = sg.find_one_shotgun('CustomEntity01', [
        ['project', 'name_is', project_name], ['sg_type', 'is', entity_name["type"]],
        ['sg_upload_type', 'is', 'Dailies']], ["sg_pattern", "sg_work_file_name",
                                               "sg_prev_file_name", "sg_oss_submit_path", "sg_attachment_no_version"])
    version_code = custom_entity_list["sg_work_file_name"].format(**task_detail)
    daily_file_name = custom_entity_list["sg_prev_file_name"].format(**task_detail)
    # step_code_name = task_info_dict["step_code"]
    server_inside_path = custom_entity_list["sg_pattern"].format(**task_detail)
    if group_list["sg_permission_group"] == "outsource":
        server_path = custom_entity_list["sg_oss_submit_path"].format(**task_detail)
        server_daily_path = server_path + "/" + daily_file_name + os.path.splitext(local_daily_path)[-1]
    else:
        server_daily_path = server_inside_path + "/" + daily_file_name + os.path.splitext(local_daily_path)[-1]
        try:
            if not os.path.isdir(server_inside_path):
                os.makedirs(server_inside_path)
            if os.path.isfile(server_daily_path):
                os.remove(server_daily_path)
        except Exception as e:
            print e
            return
    copy_file_list = [[local_daily_path, server_daily_path]]
    return_info_list = [copy_file_list, reviewers_people_list, version_code]
    # return_info_list = ["拷贝列表", "审核人列表", "daily版本名" ]
    return return_info_list


def create_daily_version(task_info_dict, return_info_list):
    copy_file_list = return_info_list[0]
    reviewers_people_list = return_info_list[1]
    version_code = return_info_list[2]
    task_entity_id = get_task_info(task_info_dict)
    project_name = task_info_dict['project']
    project_info = sg.find_one_shotgun('Project', [['name', 'is', project_name]], ['id'])
    describe = task_info_dict['describe']
    server_daily_path = copy_file_list[0][1]
    local_daily_path = copy_file_list[0][0]
    mov_display_name = os.path.split(server_daily_path)[-1]
    user_name = task_info_dict['user']
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code"])
    today_daily_info = sg.find_one_shotgun("Version", [['project', 'name_is', project_name],
                                                       ["sg_task", "is", task_entity_id],
                                                       ["sg_version_type", "is", "Dailies"],
                                                       ["code", "is", version_code]], ["id"])
    if not today_daily_info:
        data = {'project': project_info,
                'sg_path_to_movie': server_daily_path,
                'code': version_code,
                'entity': task_info_dict['entity'],
                'user': group_list,
                'description': describe,
                'sg_task': task_entity_id,
                'sg_version_type': 'Dailies',
                'sg_version_number': 'None',
                'sg_status_list': 'rev',
                }
        version_info = sg.create_shotgun("Version", data)
        version_id = version_info['id']
        version_info_list = [{"id": version_id, "name": version_code, 'type': 'Version'}]
        sg.upload_shotgun("Version", version_id, local_daily_path, field_name="sg_uploaded_movie",
                          display_name=mov_display_name)
        title = u"审核通知:{}".format(version_code)
        content_text = u"{} Daily任务已上传,请审核".format(version_code)
        note_info_dict = {"reviewers_people": reviewers_people_list, "project": project_info,
                          "subject": title, "user": group_list,
                          "version_id_code": version_info_list, "content": content_text}
        create_note(note_info_dict)
    else:
        today_daily_id = today_daily_info["id"]
        data_note = {"description": describe}
        sg.update_shotgun("Version", today_daily_id, data_note)
        sg.upload_shotgun("Version", today_daily_id, local_daily_path, field_name="sg_uploaded_movie",
                          display_name=mov_display_name)
        update_version_id_code = [{"id": today_daily_id, "name": version_code, 'type': 'Version'}]
        title = u"审核通知:{}".format(version_code)
        content_text = u"{} Daily任务已覆盖上传,请审核".format(version_code)
        note_info_dict = {"reviewers_people": reviewers_people_list, "project": project_info,
                          "subject": title, "user": group_list,
                          "version_id_code": update_version_id_code, "content": content_text}
        create_note(note_info_dict)


def create_note(note_info):
    note_data_list = []
    for reviewers in note_info["reviewers_people"]:
        reviewers_list = list()
        reviewers_list.append(reviewers)
        note_data = {
            "project": note_info["project"],
            "subject": note_info["subject"],
            "sg_proposer": note_info["user"],
            "addressings_to": reviewers_list,
            "content": note_info["content"],
            "sg_status_list": "opn",
            "sg_if_read": False,
            "note_links": note_info["version_id_code"]
        }
        note_data_list.append({"request_type": "create", "entity_type": "Note", "data": note_data})
    sg.batch_shotgun(note_data_list)


def get_task_name(task_dict):
    task_id = int(task_dict['id'])
    project_name = task_dict['project']
    find_type = task_dict['type']
    task_info = sg.find_one_shotgun(find_type, [['project', 'name_is', project_name], ["id", "is", task_id]],
                                                ["entity", "content", "id", "Project", "step.Step.code"])
    return task_info


def get_group_list():
    user_name = sg.get_user()
    project = sg.get_project()
    group_list = sg.find_one_shotgun('Group', [['sg_login', 'is', user_name]],
                                     ["id", "code", "sg_permission_group", "sg_login"])
    return group_list, project


class FetchBatchSubmitDailyThread(QThread):
    """
    拉取数据线程
    """
    fetch_result_sig = Signal(dict)  # 拉取到的当前数据
    finished_sig = Signal(bool)  # 结束信号

    def __init__(self, parent=None):
        super(FetchBatchSubmitDailyThread, self).__init__(parent=parent)
        self.files_list = {}
        self.group = ''
        self.project = ''
        self.files_list = {}
        self.error_list = []  # [没有创建版本的气氛图名,或者不存在的镜头]
        self.shot_path = {}  # {镜头名：[对应的气氛图路径,...]}
        self.all_shot_num = []  # 所有镜头号

    def run(self):
        file_path = []
        if self.files_list and self.files_list['files']:
            self.group = self.files_list['group']
            self.project = self.files_list['project']
            if type(self.files_list['files']) != list:
                file_path.append(self.files_list['files'])
            else:
                file_path = self.files_list['files']
            # 扫描出所有的文件
            all_files = flat([f for f in map(get_files_list, file_path,
                                             ['files'] * len(file_path))])
            self.fetch_result_sig.emit({'msg': u'共扫描到%s个文件' % len(all_files),
                                        'data': {}})
            # 检查文件后缀是否有问题
            wrong_suffix_files = [w for w in all_files if '.' not in w or w.split('.')[-1] not in
                                  ['mov', 'jpg', 'JPG', "png", "jpeg", "PNG", "bmp"]]
            if wrong_suffix_files:
                wrong_suffix_files_name = [n.split('/')[-1] for n in wrong_suffix_files
                                           if n.split('/')[-1] != "Thumbs.db"]
                if wrong_suffix_files_name:
                    self.fetch_result_sig.emit({'msg': u'以下文件后缀名出现问题: %s 已经忽略...' % wrong_suffix_files_name,
                                                'data': {}})
            all_right_files = [r for r in all_files if r not in wrong_suffix_files]
            if self.group == "colorkey":
                table_data_list, error_list = self.get_scene_shot(all_right_files)
                if error_list:
                    self.fetch_result_sig.emit({'msg': u'以下文件名出现问题: %s 已经忽略...' % list(set(error_list)),
                                                'data': {}})
                no_shot_num = []
                for table_data in table_data_list:
                    shot_num = table_data["shot"].replace("s", "")
                    shot_name = table_data["shot"]
                    task_id = get_task_id(self.project, shot_num)
                    if task_id:
                        table_data.update({"task_id": task_id})
                        self.fetch_result_sig.emit({'msg': '', 'data': {shot_name: table_data}})
                    else:
                        if shot_name not in no_shot_num:
                            no_shot_num.append(shot_name)
                self.fetch_result_sig.emit({'msg': u'该文件没有镜头号不存在: %s 已经忽略...' % no_shot_num,
                                                'data': {}})
                self.finished_sig.emit(True)
            else:
                all_mov = [mov for mov in all_right_files if mov.split('.')[-1] in ['mov']]
                data_dict = {}
                for each_mov in all_mov:
                    short_mov = each_mov.split('/')[-1]
                    if not check_file_name_format(short_mov):
                        self.fetch_result_sig.emit({'msg': u'该mov文件命名有问题: %s 已经忽略...' % short_mov, 'data': {}})
                        continue
                    scene, shot, _ = check_file_name_format(short_mov)
                    # 更新字典
                    try:
                        data_dict[scene+'_'+shot] = {'mov': each_mov}
                    except Exception as e:
                        print '文件命名错误', e
                        self.fetch_result_sig.emit({'msg': u'该文件命名有问题: %s 已经忽略...' % short_mov, 'data': {}})
                        continue

                # 开始对字典中的数据进行处理
                for shot, shot_data in data_dict.iteritems():
                    scene_str, name = shot.split('_')
                    scene = scene_str.lstrip('s')
                    # 获取这个镜头的id信息, 这里需要判断任务是否创建
                    shot_name = scene+"_"+name
                    task_id, project_info = get_shot_id(shot_name, self.project, self.group)
                    if not task_id:
                        self.fetch_result_sig.emit({'msg': u'该镜头的任务未创建: %s 已经忽略...'
                                                           % (shot+'_'+self.group), 'data': {}})
                        continue
                    shot_data.update({"task_id": task_id, "shot": shot_name})
                    self.fetch_result_sig.emit({'msg': '', 'data': {shot: shot_data}})
                    # 更新一下字典并发送出去，最终格式：
                    #
                    # ｛‘s01_001’:
                    #           {'task_id': '对应任务id',
                    #           'shot': '对应任务镜头',
                    #           'mov': "本地mov路径"
                    #           }
                    #   ｝
                self.finished_sig.emit(True)

    def get_scene_shot(self, all_right_files):
        # 获取{镜头名：[对应的气氛图路径,...]}字典
        table_data_list = []
        error_list = []
        for colorkey_path in all_right_files:
            file_name = os.path.split(colorkey_path)[-1]

            try:
                scene = file_name.split('_')[0]
                shot = file_name.split('_')[1]
                if re.findall(r'\d+', scene):
                    scene_name = scene.lower()
                    if re.findall(r'\d+', shot):
                        if "-" in shot:
                            shot = shot.split("-")[0]
                        if len(re.findall(r'\d+', shot)[0]) != 3:
                            if len(shot) < 3:
                                shot_num = shot.zfill(3)
                            else:
                                shot_num = shot.zfill(len(shot) + 1)
                        else:
                            shot_num = shot
                        scene_shot = scene_name + "_" + shot_num
                        table_data_list.append({"shot": scene_shot, "mov": colorkey_path})
                else:
                    error_list.append(file_name)
            except Exception as e:
                print u"文件名存在问题", e
                error_list.append(file_name)
        return table_data_list, error_list

def flat(list_):
    # 将嵌套列表展开,例如输入：[1,[2,3,[1,3],4], 5],展开则是[1,2,3,1,3,4,5]
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return filter(None, res)


def get_files_list(file_dir, mode='files'):
    files_full_path = []
    folders_full_path = []
    if os.path.isfile(file_dir):
        if mode in ['files']:
            files_full_path.append(file_dir.replace('\\', '/'))
            return files_full_path
        return []

    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        folders_full_path.extend([(root + '\\' + fl).replace('\\', '/') for fl in dirs])
        files_full_path.extend([(root + '\\' + f).replace('\\', '/') for f in files])
    if mode in ['files']:
        return files_full_path
    if mode in ['folders']:
        return folders_full_path
    else:
        return files_full_path + folders_full_path


def check_file_name_format(fn):
    # 判断文件是否是s01_001_Ly_V001.ma这种命名格式
    try:
        if "." in fn:
            fn = os.path.splitext(fn)[0]
        scene = fn.split('_')[0]
        shot = fn.split('_')[1]
        try:
            version_temp = re.findall(r'\d+', fn)[2]
            version = version_temp
        except IndexError:
            version = '0'
        # version = re.findall(r'\d+', version_temp.split('.')[0])[0]
        if not version:
            return False
        version = version.zfill(3)
        if not (scene[0].lower() == 's' and len(re.findall(r'\d+', scene)[0]) == 2
                and len(re.findall(r'\d+', shot)[0]) == 3):
            return False
        return scene.replace('S', 's'), shot, version
    except Exception, e:
        return False


def get_shot_id(shot_num, project_name, step):
    # shot_num= "s20_20",project_name = "Demo: Animation",step = "ANI"
    project_info = sg.find_one_shotgun('Project', [['name', 'is', project_name]], ['id'])
    try:
        shot_id = sg.find_shotgun('Shot', [['project', 'is', project_info], ['code', 'is', shot_num]], ['id'])
        shot_id[0]['name'] = shot_num
        task_id = sg.find_shotgun('Task', [
            ['project', 'is', project_info], ['entity', 'is', shot_id[0]], ['step.Step.code', 'is', step]],
            ["id"])[0]['id']
        return task_id, project_info
    except Exception as e:
        print u"没有该任务",e
        task_id = None
        return task_id, project_info


def get_task_id(project_name, shot_num):
    # shot_num= "s20_20",project_name = "Demo: Animation",step = "ANI"
    project_info = sg.find_one_shotgun('Project', [['name', 'is', project_name]], ['id'])
    shot_info = sg.find_one_shotgun("Shot", [['project', 'name_is', project_name], ['code', 'is', shot_num]], ['id'])
    if shot_info:
        shot_id = shot_info["id"]
        try:
            task_info = sg.find_one_shotgun("Task", [['project', 'name_is', project_name],
                                                   ['entity.Shot.id', 'is', shot_id],
                                           ["step.Step.short_name", "is", "ck"]], ['id'])
            task_id = task_info["id"]
            # task_entity_id = {"type": "Task", "id": task_id["id"]}
        except Exception as e:
            print u'{}该镜头下没有colorkey任务'.format(shot_num), e
            task_data = {
                "project": project_info,
                "entity": {u'type': u'Shot', u'id': shot_id},
                "content": u'ck',
                "step": {u'type': u'Step', u'id': 143, u'name': u'Colorkey'},
                "sg_status_list": "ip",
            }
            task_info = sg.create_shotgun("Task", task_data)
            task_id = task_info["id"]
        return task_id
    else:
        return None
