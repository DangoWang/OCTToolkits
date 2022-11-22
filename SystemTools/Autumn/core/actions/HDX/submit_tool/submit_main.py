# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/12/13
import os
import pprint

import submit_ui
import load_data
from utils import fileIO


class SubmitDoit(submit_ui.HDXSubmit):

    def __init__(self, task_dict, parent=None):
        super(SubmitDoit, self).__init__(task_dict=task_dict, parent=parent)
        self.__task_info = {}
        self.__path_convention = {}
        self.__update_dict = {}
        #  以下为创建daily时， shotgun应该记录的路径：
        self.work_file_oct_path = None
        self.prev_file_oct_path = None
        self.attach_file_oct_path = None
        #  以下为拷贝的目标路径（服务器 or 阿里云）:
        self.work_file_dest_path = None
        self.prev_file_dest_path = None
        self.attach_file_dest_path = None
        #  这个是通知rpc从十月拿取的路径列表
        self.rpc_copy_list = []
        #  这个是版本的code
        self.version_code = None
        #  拷贝文件的线程
        self.copy_thread = None
        self.parse_task_info(task_dict)
        if self.__task_info['user_permission'] in ['outsource']:
            self.fetching_from_rpc_copy = fileIO.FormRPCCopy("download")
            self.fetching_from_rpc_copy.finished.connect(self.finish_from_rpc_copy)

    def parse_task_info(self, task_dict):
        if task_dict:
            self.__task_info = load_data.get_task_info_by_task_dict(task_dict)
            self.version_name_lb.setText('_'.join([self.__task_info['entity']['name'], self.__task_info['task_name'],
                                                   self.__task_info['user'],
                                                  self.__task_info['version']]
                                                  ))
            self.copy_thread = fileIO.CopyFile([]) if self.__task_info['user_permission'] not in ['outsource'] else fileIO.CopyFTP([])
            self.copy_thread.progress.connect(self.__set_progress)
            self.copy_thread.finished.connect(self.__finished_copy)
        return {}

    def __set_progress(self, data):
        self.submit_progress.setValue(data[1])
        self.progress_label.setText(u'正在拷贝至:' + data[0])
        self.append_log('copying: %s' % data[0])

    def submit_doit(self):
        super(SubmitDoit, self).submit_doit()
        #  抓取路径规范， 返回字典
        self.__path_convention = load_data.get_convention(self.__task_info.get('project'),
                                                          self.__task_info.get('entity_type'), 'Dailies', )
        if self.__path_convention and self.__task_info and self.copy_thread:
            #  这里判断是不是外包来获取不同的路径：服务器 or 阿里云
            submit_path_pattern = self.__path_convention['sg_pattern'] \
                                    if self.__task_info['user_permission'] not in ['outsource'] else self.__path_convention['sg_oss_submit_path']
            #  这个时版本的code
            self.version_code = self.__path_convention['sg_work_file_name'] .format(**self.__task_info).split('/')[-1]
            #  根据用户选择来上传不同的文件
            if self.work_file:
                #  以下为创建daily时， shotgun应该记录的路径：
                self.work_file_oct_path = (self.__path_convention['sg_pattern'] + self.__path_convention['sg_work_file_name'])\
                                              .format(**self.__task_info) + self.construction_format
                #  以下为拷贝的目标路径（服务器 or 阿里云）:
                self.work_file_dest_path = (submit_path_pattern + self.__path_convention['sg_work_file_name'])\
                                               .format(**self.__task_info) + self.construction_format
                self.__update_dict['sg_path_to_frames'] = self.work_file_oct_path   # shotgun应该记录十月内部的路径
                self.copy_thread.copy_list.append([self.work_file, self.work_file_dest_path])
                self.rpc_copy_list.append([self.work_file_dest_path, self.work_file_oct_path])  # 让rpc下载的路径
            if self.prev_file:
                #  以下为创建daily时， shotgun应该记录的路径：
                self.prev_file_oct_path = (self.__path_convention['sg_pattern'] + self.__path_convention[
                    'sg_prev_file_name']).format(**self.__task_info) + self.preview_format
                #  以下为拷贝的目标路径（服务器 or 阿里云）:
                self.prev_file_dest_path = (submit_path_pattern + self.__path_convention['sg_prev_file_name'])\
                                               .format(**self.__task_info) + self.preview_format
                self.__update_dict['sg_path_to_movie'] = self.prev_file_oct_path
                self.copy_thread.copy_list.append([self.prev_file, self.prev_file_dest_path])
                self.rpc_copy_list.append([self.prev_file_dest_path, self.prev_file_oct_path])
            if self.attach:
                #  以下为创建daily时， shotgun应该记录的路径：
                self.attach_file_oct_path = (self.__path_convention['sg_pattern'] + self.__path_convention['sg_attachment_path'])\
                                            .format(**self.__task_info)
                #  以下为拷贝的目标路径（服务器 or 阿里云）:
                self.attach_file_dest_path = (submit_path_pattern + self.__path_convention['sg_attachment_path'])\
                                            .format(**self.__task_info)
                self.__update_dict['sg_path_to_geometry'] = self.attach_file_oct_path
                self.copy_thread.copy_list.append([self.attach, self.attach_file_dest_path])
                self.rpc_copy_list.append([self.attach_file_dest_path, self.attach_file_oct_path])
            if not self.__update_dict:  # 如果啥都没选，直接raise
                self.append_log(u'你必须选择文件才能上传！')
                raise RuntimeError
            #  copylist创建完成， 启动拷贝
            if self.__task_info['user_permission'] not in ['outsource']:
                if not os.path.isdir('M:/'):
                    self.append_log(u'未发现M盘！请确认是否已经映射...')
                    raise RuntimeError
            self.copy_thread.start()
        else:
            self.append_log(u'未抓取到路径规范或者任务信息！')
            raise RuntimeError

    def __finished_copy(self, finished):
        #  拷完之后需要进行判断， 如果是外包， 需要通知rpc下载然后创建版本信息。如果是内部则不用。
        if finished:
            self.append_log(u'文件拷贝完成，正在上传数据至shotgun...')
            if self.__task_info['user_permission'] in ['outsource']:
                #  这里通知rpc拿取
                # func(self.rpc_copy_list)
                self.fetching_from_rpc_copy.copy_list = self.rpc_copy_list
                self.fetching_from_rpc_copy.mode = "download"
                self.fetching_from_rpc_copy.start()
            else:
                self.create_version()

    def create_version(self):
        new_version_data = dict(
            project=self.__task_info.get('project_entity'),
            sg_version_number=self.__task_info.get('version_number'),
            description=self.description,
            user=self.__task_info.get('task_assignees'),
            sg_task=self.__task_info.get('sg_task'),
            entity=self.__task_info.get('entity'),
            sg_version_type='Dailies',
            code=self.version_code
        )
        new_version_data.update(self.__update_dict)
        try:
            load_data.create_version(new_version_data)
            self.append_log(u'恭喜你！文件提交完成, 现在你可以关闭窗口了!')
            self.submit_btn.setText(u'上传完成！')
            self.cancel_btn.setEnabled(True)
            return True
        except Exception as e:
            self.append_log(u'写入数据库出现错误：\n%s\n请联系TD解决.'%e)

    def finish_from_rpc_copy(self, finished):
        if finished:
            self.fetching_from_rpc_copy.wait()
            self.fetching_from_rpc_copy.quit()
            self.create_version()
        else:
            self.append_log(u'写入数据库出现错误：\n请联系TD解决.')