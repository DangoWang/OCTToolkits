#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################
import os
import shutil
from PySide.QtCore import *
import re
from pprint import pprint
from utils import shotgun_operations
from dayu_widgets.message import MMessage
sg = shotgun_operations


class CopyFile(QThread):
    """
    拷贝文件线程
    """
    finished = Signal(bool)  # 拷贝完成信号
    progress = Signal(list)  # 正在拷贝的文件名和进度

    def __init__(self, copy_list=''):
        super(CopyFile, self).__init__()
        self.copy_list = copy_list
        self.source = ''
        self.dest = ''

    def run(self):
        if not self.copy_list:
            return
        i = 0
        ma_path_list = []
        mov_path_list = []
        version_name_list = []
        entity_shot_list = []
        entity_task_list = []
        for copy_dict in self.copy_list:
            i += 1
            for key, value in copy_dict.items():
                if key == "ma_server_path":
                    ma_path_list.append(copy_dict["ma_server_path"])
                elif key == "mov_server_path":
                    mov_path_list.append(copy_dict["mov_server_path"])
                elif key == "version_name":
                    version_name_list.append(copy_dict["version_name"])
                elif key == "entity_shot":
                    entity_shot_list.append(copy_dict["entity_shot"])
                elif key == "entity_task":
                    entity_task_list.append(copy_dict["entity_task"])
                elif key == "project":
                    project = copy_dict["project"]
                elif key == "description":
                    describe = copy_dict["description"]
                else:
                    self.dest = key
                    self.source = value
                    if os.path.isfile(self.source):  # 如果是文件的话
                        try:
                            dest_path = self.dest.rstrip(self.dest.split('/')[-1].split('\\')[-1])
                            if not os.path.isdir(dest_path):
                                os.makedirs(dest_path)
                            if os.path.isfile(self.dest):
                                os.remove(self.dest)
                            shutil.copyfile(self.source, self.dest)
                        except Exception as e:
                            print e
                            self.finished.emit(False)
                            return
                    elif os.path.isdir(self.source):  # 如果是文件夹的话
                        try:
                            if os.path.isdir(self.dest):
                                shutil.rmtree(self.dest)
                            shutil.copytree(self.source, self.dest)
                        except Exception as e:
                            print e
                            self.finished.emit(False)
                            return
                    else:
                        self.finished.emit(False)
                        return
            self.progress.emit([self.source, (float(i) / float(len(self.copy_list)))*100])
        create_version(ma_path_list, mov_path_list, version_name_list, entity_shot_list, entity_task_list, project, describe)
        self.finished.emit(True)


class FetchBatchSubmitDataThread(QThread):
    """
    拉取数据线程
    """
    fetch_result_sig = Signal(dict)  # 拉取到的当前数据
    finished_sig = Signal(bool)  # 结束信号

    def __init__(self, parent=None):
        super(FetchBatchSubmitDataThread, self).__init__(parent=parent)
        self.files_list = {}
        # self.group = ''

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
            wrong_suffix_files = [w for w in all_files if '.' not in w or w.split('.')[-1] not in ['ma', 'mov']]
            if wrong_suffix_files:
                wrong_suffix_files_name = [n.split('/')[-1] for n in wrong_suffix_files
                                           if n.split('/')[-1] != "Thumbs.db"]
                if wrong_suffix_files_name:
                    self.fetch_result_sig.emit({'msg': u'以下文件后缀名出现问题: %s 已经忽略...' % wrong_suffix_files_name,
                                                'data': {}})
            # 将ma文件和mov文件进行两两组合
            all_right_files = [r for r in all_files if r not in wrong_suffix_files]
            all_ma = [ma for ma in all_right_files if ma.split('.')[-1] in ['ma']]
            all_mov = [mov for mov in all_right_files if mov.split('.')[-1] in ['mov']]
            data_dict = {}
            # 下面将所有的文件组成这样的字典：
            # ｛‘s01_001’:
            #           {'ma': 'ma文件全路径名',
            #           'mov': 'mov文件全路径名',
            #           'version': version}
            #   ｝
            for each_ma in all_ma:
                short_ma = each_ma.split('/')[-1]
                if not check_file_name_format(short_ma):
                    self.fetch_result_sig.emit(
                        {'msg': u'该ma文件命名有问题: %s 已经忽略...' % short_ma, 'data': {}})
                    continue
                scene, shot, _ = check_file_name_format(short_ma)
                # 将文件组成字典形式
                data_dict[scene+'_'+shot] = {'ma': each_ma}
            for each_mov in all_mov:
                short_mov = each_mov.split('/')[-1]
                if not check_file_name_format(short_mov):
                    self.fetch_result_sig.emit({'msg': u'该mov文件命名有问题: %s 已经忽略...' % short_mov, 'data': {}})
                    continue
                scene, shot, _ = check_file_name_format(short_mov)
                # 更新字典
                try:
                    data_dict[scene+'_'+shot].update({'mov': each_mov})
                except Exception as e:
                    print '文件命名错误', e
                    self.fetch_result_sig.emit({'msg': u'该文件命名有问题: %s 已经忽略...' % short_mov, 'data': {}})
                    continue

            # 开始对字典中的数据进行处理
            for shot, shot_data in data_dict.iteritems():
                if not ('ma' in shot_data.keys() and 'mov' in shot_data.keys()):
                    self.fetch_result_sig.emit({'msg': u'该镜头的相关文件命名有问题: %s 已经忽略...' % shot, 'data': {}})
                    continue
                scene_str, name = shot.split('_')
                scene = scene_str.lstrip('s')
                # 获取这个镜头的id信息, 这里需要判断任务是否创建
                shot_name = scene+"_"+name
                shot_id,latestversion,project_info = get_shot_id(shot_name, self.project, self.group)
                if not shot_id:
                    self.fetch_result_sig.emit({'msg': u'该镜头的任务未创建: %s 已经忽略...'
                                                       % (shot+'_'+self.group), 'data': {}})
                    continue
                else:
                    if latestversion:
                        version_number = str(int(re.findall(r'\d+',latestversion)[0])+1).zfill(3)
                    else:
                        version_number = "101"

                shot_data['id'] = ""
                # # 版本信息
                shot_data['version'] = version_number
                file_path = shot_data['ma']
                shot_data['ma_path'] = file_path
                shot_data['ma'] = os.path.split(file_path)[-1]
                mov_path = shot_data['mov']
                shot_data['mov_path'] = mov_path
                shot_data['preview'] = os.path.split(mov_path)[-1]
                del shot_data['mov']
                self.fetch_result_sig.emit({'msg': '', 'data': {shot: shot_data}})
                # 更新一下字典并发送出去，最终格式：
                # ｛‘s01_001’:
                #           {'ma_path': 'ma文件全路径名',
                #           'mov_path': 'mov文件全路径名',
                #           'version': version
                #           'id': _id
                #           'ma':'ma文件名'
                #           'preview':'mov文件名'
                #           }
                #   ｝
            self.finished_sig.emit(True)


def get_shot_id(shot_num, project_name, step):
    # shot_num= "s20_20",project_name = "Demo: Animation",step = "ANI"
    project_info = sg.find_one_shotgun('Project', [['name', 'is', project_name]], ['id'])
    try:
        shot_id = sg.find_shotgun('Shot', [['project', 'is', project_info], ['code', 'is', shot_num]], ['id'])
        shot_id[0]['name'] = shot_num
        latestversion_num = sg.find_shotgun('Task', [
            ['project', 'is', project_info], ['entity', 'is', shot_id[0]], ['step.Step.code', 'is', step]],
            ["sg_latestversion"])[0]['sg_latestversion']
        return shot_id, latestversion_num, project_info
    except Exception as e:
        print u"没有改任务",e
        get_shot_id = None
        latestversion_num = None
        return get_shot_id, latestversion_num, project_info


def create_version(ma_path_list, mov_path_list, version_name_list, entity_shot_list,
                   entity_task_list, project, describe):
    #创建版本
    user_name = sg.get_user()
    #user_name = "TD"
    group_list = sg.find_one_shotgun('Group',
                                     [['sg_login', 'is', user_name]],
                                     ["id", "code"])
    batch_data = []
    for i in range(0, len(mov_path_list)):
        version_num = re.findall(r'\d+', version_name_list[i][0].split("_")[-1])[0]
        data = {"project": project,
                'sg_path_to_movie': mov_path_list[i][0],
                'code': version_name_list[i][0],
                'entity': entity_shot_list[i],
                'sg_path_to_frames': ma_path_list[i][0],
                'user': group_list,
                'sg_version_number': version_num,
                'description': describe,
                'sg_task': entity_task_list[i],
                'sg_version_type': 'Submit'}
        batch_data.append({"request_type": "create", "entity_type": "Version", "data": data})
        task_id = entity_task_list[i]['id']
        data_task = {
            "project": project,
            'sg_latestversion': version_num,
            'sg_status_list': 'ip'
        }
        batch_data.append({"request_type": "update", "entity_type": "Task", "entity_id": task_id, "data": data_task})
        no_version_num_id = find_no_version(project, version_name_list[i][1], entity_shot_list[i])
        if no_version_num_id:
            data_version_num = {
                'sg_path_to_movie': mov_path_list[i][1],
                'sg_path_to_frames': ma_path_list[i][1]}
            batch_data.append(
                {"request_type": "update", "entity_type": "Version", "entity_id": no_version_num_id, "data": data_version_num})
        else:
            data_no_version_num = {"project": project, 'sg_path_to_movie': mov_path_list[i][1],
                                   'code': version_name_list[i][1],
                                   'entity': entity_shot_list[i],
                                   'sg_path_to_frames': ma_path_list[i][1],
                                   'user': group_list,
                                   'sg_version_number': None,
                                   'description': describe,
                                   'sg_task': entity_task_list[i],
                                   'sg_version_type': 'Submit'}
            batch_data.append({"request_type": "create", "entity_type": "Version", "data": data_no_version_num})
    # pprint(batch_data)
    version_info_list = sg.batch_shotgun(batch_data)
    for version_info in version_info_list:
        if version_info["type"] == "Version":
            version_id = version_info['id']
            mov_file = version_info['sg_path_to_movie']
            display_n = os.path.split(mov_file)[-1]
            sg.upload_shotgun("Version", version_id, mov_file, field_name="sg_uploaded_movie", display_name=display_n)


def find_no_version(project_info, code_name, entity_is):
    try:
        no_version_id = sg.find_one_shotgun("Version", [['project', 'is', project_info],
                                   ['code', 'is', code_name], ["entity", "is", entity_is],
                                                        ["sg_version_type", "is", "Submit"]], ["id"])["id"]
        return no_version_id
    except Exception as e:
        print u"不存在该版本", e, code_name
        return None


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


def get_copy_file_list(win, table_data, project, group, describe):
    #收集要copy的文件转换成字典，以及创建版本所需要的路径，版本号，和版本名
    copy_list = []
    for t in range(0, len(table_data)):
        copy_dict = {}
        ma_path = table_data[t]['ma_path']
        mov_path = table_data[t]['mov_path']
        ma_file_name = os.path.split(ma_path)[-1]
        scene, shot, _ = check_file_name_format(ma_file_name)
        seq = scene.lstrip('s')
        shot_name = seq + "_" + shot
        ma_suffix = os.path.splitext(ma_path)[-1]
        mov_suffix = os.path.splitext(mov_path)[-1]
        shot_id, latestversion_num, project_info = get_shot_id(shot_name, project, group)
        if latestversion_num:
            version_num = str(int(re.findall(r'\d+', latestversion_num)[0]) + 1).zfill(3)
        else:
            version_num = "101"
        task_name_id = sg.find_shotgun('Task',
                                       [['project', 'is', project_info], ['entity', 'is', shot_id[0]],
                                        ['step.Step.short_name', 'is', group]],
                                       ["id", 'content'])
        pprint(task_name_id)
        if not task_name_id:
            MMessage.config(2)
            MMessage.error(u'未找到相关任务，请检查shotgun对应镜头是否存在该任务!', parent=win)
            return
        dic_value = {'scene': seq,
                     'shot': shot,
                     'code': shot_id[0]["name"],
                     'type': "Shot",
                     'task_name': task_name_id[0]["content"],
                     'step_code': group,
                     'version': version_num, }
        customentity_list = sg.find_one_shotgun('CustomEntity01', [
            ['project', 'name_is', "DSF"], ['sg_type', 'is', "Shot"], ['sg_upload_type', 'is', 'Submit']],
            ["sg_pattern", "sg_workfile_no_version", "sg_work_file_name", "sg_prev_file_name",
             "sg_prevfile_no_version"])
        server_path = customentity_list["sg_pattern"].format(**dic_value)
        workfile_no_version = customentity_list["sg_workfile_no_version"].format(**dic_value)
        workfile_name = customentity_list["sg_work_file_name"].format(**dic_value)
        prevfile_name = customentity_list["sg_prev_file_name"].format(**dic_value)
        prevfile_no_version = customentity_list["sg_prevfile_no_version"].format(**dic_value)
        copy_dict[server_path + "/" + workfile_name + ma_suffix] = ma_path
        copy_dict[server_path + "/" + prevfile_name + mov_suffix] = mov_path
        copy_dict[server_path + "/" + workfile_no_version + ma_suffix] = ma_path
        copy_dict[server_path + "/" + prevfile_no_version+mov_suffix] = mov_path
        ma_server_path_list = [server_path + "/" + workfile_name + ma_suffix, server_path + "/" +
                               workfile_no_version + ma_suffix]
        mov_server_path_list = [server_path + "/" + prevfile_name + mov_suffix, server_path + "/" +
                                prevfile_no_version+mov_suffix]
        version_name_list = [workfile_name, workfile_no_version]
        copy_dict.update(entity_task=task_name_id[0], entity_shot=shot_id[0], 
                         ma_server_path=ma_server_path_list,
                         mov_server_path=mov_server_path_list, version_name=version_name_list,
                         project=project_info, description=describe)
        # copy_dict ={服务器上带版本的maya文件路径：本地maya文件，
        #             服务器上带版本的MOV文件路径：本地MOV文件，
        #             服务器上不带版本的maya文件路径：本地maya文件，
        #             服务器上不带版本的MOV文件路径：本地MOV文件，
        #             "ma_server_path":[服务器上带版本的maya文件路径, 服务器上不带版本的maya文件路径],
        #             "mov_server_path":[服务器上带版本的MOV文件路径, 服务器上不带版本的MOV文件路径]
        #             "version_name"：[带版本名，不带版本号的名字]
        #             "project":项目，
        #             "step":部门组名，
        #             "description":描述
        # }
        copy_list.append(copy_dict)
    return copy_list


def check_file_name_format(fn):
    # 判断文件是否是s01_001_Ly_V001.ma这种命名格式
    try:
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


def flat(list_):
    # 将嵌套列表展开,例如输入：[1,[2,3,[1,3],4], 5],展开则是[1,2,3,1,3,4,5]
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return filter(None, res)
