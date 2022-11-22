#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pprint

from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.browser import MDragFileButton, MDragFolderButton
from dayu_widgets.message import MMessage
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
from PySide.QtGui import *
from PySide.QtCore import *
from utils import fileIO, shotgun_operations
import time
from config import GLOBAL
from utils import common_methods

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


frame_file_formats = GLOBAL.format_file['frame']
picture_file_formats = GLOBAL.format_file['picture']
video_file_formats = GLOBAL.format_file['video']

user = shotgun_operations.get_user()
permission = shotgun_operations.get_permission(user)


class WriteDatabase(QThread):
    write_finished = Signal(bool)

    def __init__(self, data={}, parent=None):
        super(WriteDatabase, self).__init__(parent)
        self.data = data

    def run(self, *args, **kwargs):
        # print self.data['version_code']
        ##写入数据库
        project_info = shotgun_operations.find_one_shotgun('Project', [['name', 'is', self.data['project']]], ['id'])
        filters_entity = [
            ['project', 'name_is', self.data['project']],
            ['code', 'is', self.data['code']]
        ]
        entity = shotgun_operations.find_one_shotgun(self.data['type'], filters_entity, ['id', 'code'])
        filters_task = [
            ['project', 'name_is', self.data['project']],
            ['id', 'is', self.data['id']]
        ]
        sg_task = shotgun_operations.find_one_shotgun('Task', filters_task, ['id', 'code'])
        user_info = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', self.data['user']]], ['sg_group_project', 'id', 'code'])
        create_data = dict(
            project=project_info,
            sg_path_to_frames=self.data['sg_work_file_path'],
            sg_path_to_movie=self.data['sg_prev_file_path'],
            sg_path_to_geometry=self.data['sg_attachment_path'],
            sg_version_number=self.data['new_version'],
            description=self.data['description'],
            user=user_info,
            entity=entity,
            sg_version_type='Submit',
            code=self.data['version_code'],
            sg_task=sg_task,
        )
        # ##创建版本
        version_entity = shotgun_operations.create_shotgun('Version', create_data)
        # ##上传预览图
        # print version_entity['id']
        # print self.data['id']
        shotgun_operations.upload_shotgun("Version", version_entity['id'], self.data['local_prev'], field_name="sg_uploaded_movie",
                                          display_name=self.data['version_code'])
        # ##更新最新版本
        task_entity = shotgun_operations.find_one_shotgun('Task', [['id', 'is', self.data['id'][0]]], ['step.Step.short_name'])
        update_dict = {'sg_latestversion': self.data['new_version']}
        # if not task_entity['step.Step.short_name'] in ['ly', 'bk', 'an']:
        # update_dict.update({'sg_status_list': 'ip'})
        shotgun_operations.update_shotgun('Task', self.data['id'][0], update_dict)

        create_data_no_version = dict(
            project=project_info,
            sg_path_to_frames=self.data['sg_workfile_no_version'],
            sg_path_to_movie=self.data['sg_prevfile_no_version'],
            sg_path_to_geometry=self.data['sg_attachment_no_version'],
            sg_version_number=None,
            description=self.data['description'],
            user=user_info,
            entity=entity,
            sg_version_type='Submit',
            code=self.data['no_version_code'],
            sg_task=sg_task,
        )
        # ##创建版本
        version_id = shotgun_operations.find_shotgun('Version', [['project', 'name_is', 'DSF'], ['code', 'is', self.data['no_version_code']],
                                                                 ['sg_version_type', 'is', 'Submit']], ['id', 'code'])
        if version_id:
            no_version_entity = shotgun_operations.update_shotgun('Version', version_id[0]['id'], create_data_no_version)
        else:
            no_version_entity = shotgun_operations.create_shotgun('Version', create_data_no_version)
        # ##上传预览图
        shotgun_operations.upload_shotgun("Version", no_version_entity['id'], self.data['local_prev'], field_name="sg_uploaded_movie",
                                          display_name=self.data['no_version_code'])
        # # ##更新最新版本
        # shotgun_operations.update_shotgun('Task', self.data['id'], {'sg_latestversion': self.data['new_version']})
        self.write_finished.emit(True)


class UploadFileLocalAction(QDialog, MFieldMixin):

    def __init__(self, task_dic={}, parent=None):
        super(UploadFileLocalAction, self).__init__(parent)
        # self.resize(470, 520)
        self.task_dic = task_dic
        self.setMinimumWidth(660)
        self.copy_thread = fileIO.CopyFTP() if permission in ['outsource'] else fileIO.CopyFile()
        self.copy_thread.finished.connect(self.copy_finished)
        self.copy_thread.progress.connect(self.progress)
        self.mute_lock = 0
        self.copy_info = []
        self.write_database = WriteDatabase()
        self.write_database.write_finished.connect(self.write_finished)
        self.__work_file = ''
        self.__prev_file = ''
        self.__attach = None
        self.sg_attachment_path = None
        self.addUi()


    def addUi(self):

        self.label_task_name = MLabel(u'任务名称：').secondary()
        self.task_name = MLabel()

        self.label_submit_user = MLabel(u'提交用户：').secondary()
        self.submit_user = MLabel()

        self.label_submit_version = MLabel(u'提交版本：').secondary()
        self.submit_version = MLabel()

        self.label_submit_path = MLabel(u'提交路径：').secondary()
        self.submit_path = MLabel()

        self.label_description = MLabel(u'描述：').secondary()
        self.description = MTextEdit()
        self.description.setMaximumHeight(80)

        # self.file_explain_label = MLabel(u'文件上传后，将自动根据任务名称对文件更名处理。').secondary()
        # self.dir_explain_label = MLabel(u'文件夹上传后，不会对文件名进行更改，会存放到当前任务的工程文件和预览文件同级目录下。').secondary()

        self.submitInfo_layout = QGridLayout()
        self.submitInfo_layout.addWidget(self.label_task_name, 0, 0)
        self.submitInfo_layout.addWidget(self.task_name, 0, 1)
        self.submitInfo_layout.addWidget(self.label_submit_user, 0, 3)
        self.submitInfo_layout.addWidget(self.submit_user, 0, 4)
        self.submitInfo_layout.addWidget(self.label_submit_version, 0, 6)
        self.submitInfo_layout.addWidget(self.submit_version, 0, 7)
        self.submitInfo_layout.addWidget(self.label_submit_path, 1, 0)
        self.submitInfo_layout.addWidget(self.submit_path, 1, 1)
        self.submitInfo_layout.addWidget(self.label_description, 2, 0)
        self.submitInfo_layout.addWidget(self.description, 3, 0, 8, 8)

        self.construction_file = MDragFileButton(text='Click or drag file here')
        self.construction_file.set_dayu_svg('upload_line.svg')
        self.construction_file.set_dayu_filters(frame_file_formats)
        # self.__construction_path = MLabel()
        # self.__construction_path.set_elide_mode(Qt.ElideMiddle)
        self.construction_file.sig_file_changed.connect(self.construction_path)

        self.preview_file = MDragFileButton(text='Click or drag media file here', multiple=False)
        self.preview_file.set_dayu_svg('media_line.svg')
        self.preview_file.set_dayu_filters(picture_file_formats+video_file_formats)
        # self.__preview_path = MLabel()
        # self.__preview_path.set_elide_mode(Qt.ElideRight)
        self.preview_file.sig_file_changed.connect(self.preview_path)

        self.geometry_file = MDragFolderButton()
        # self.__external_path = MLabel()
        # self.__external_path.set_elide_mode(Qt.ElideRight)
        self.geometry_file.sig_folder_changed.connect(self.external_path)

        self.file_layout = QGridLayout()
        self.file_layout.addWidget(self.construction_file, 2, 0)
        self.file_layout.addWidget(self.preview_file, 2, 1)
        # self.file_layout.addWidget(self.__construction_path, 3, 0)
        # self.file_layout.addWidget(self.__preview_path, 3, 1)

        self.btn_group = QHBoxLayout()
        self.btn_submit = MPushButton(u'提交').small()
        self.btn_closed = MPushButton(u'关闭').small()
        self.btn_submit.setFixedWidth(100)
        self.btn_closed.setFixedWidth(100)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_submit)
        self.btn_group.addWidget(self.btn_closed)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.progress_layout = QVBoxLayout()
        self.submit_progress = MProgressBar()
        self.progress_label = MLabel()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.submit_progress)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'提交信息'))
        main_lay.addLayout(self.submitInfo_layout)
        main_lay.addWidget(MDivider(u'工程文件/预览文件'))
        # main_lay.addWidget(self.file_explain_label)
        main_lay.addLayout(self.file_layout)
        main_lay.addWidget(MDivider(u'附件'))
        # main_lay.addWidget(self.dir_explain_label)
        main_lay.addWidget(self.geometry_file)
        # main_lay.addWidget(self.__external_path)
        main_lay.addWidget(MDivider())
        main_lay.addLayout(self.progress_layout)
        main_lay.addLayout(self.btn_group)
        main_lay.addStretch()
        self.setLayout(main_lay)
        ##connect
        self.btn_submit.clicked.connect(self.submit)
        self.btn_closed.clicked.connect(self.close)
        self.disposal_data()
        self.submit_progress.hide()
        self.progress_label.hide()
        if permission in ['outsource']:
            self.fetching_from_rpc_copy = fileIO.FormRPCCopy("download")
            self.fetching_from_rpc_copy.finished.connect(self.finish_from_rpc_copy)

    def construction_path(self, text):
        if not text:
            return 
        if self.file_format(text) not in frame_file_formats:
            MMessage.error(u'请放入maya文件，格式为：' + str(frame_file_formats), parent=common_methods.get_widget_top_parent(self))
            return
        self.construction_file.setText(text)
        self.construction_file.set_dayu_svg('app-maya.png')
        self.__work_file = text

    def preview_path(self, text):
        if not text:
            self.__prev_file = ''
            return
        if self.file_format(text) not in picture_file_formats+video_file_formats:
            MMessage.error(u'请放入预览文件，格式为' + str(picture_file_formats+video_file_formats), parent=common_methods.get_widget_top_parent(self))
            return
        self.preview_file.setText(text)
        self.preview_file.set_dayu_svg('../../icons/autumn_video.png')
        self.__prev_file = text

    def external_path(self, text):
        if not text:
            self.__attach = ''
            return 
        self.geometry_file.setText(text)
        self.geometry_file.set_dayu_svg('../../icons/autumn_dir.png')
        self.__attach = text

    def disposal_data(self):
        # 获取shotgun中task字段
        self.get_task_id_content = shotgun_operations.get_task(self.task_dic['project'], self.task_dic['id'])
        # 获取上传文件路径
        self.path_file_dic = shotgun_operations.get_path_convention(self.task_dic['project'], self.get_task_id_content['type'], 'Submit')
        self.file_path = self.path_file_dic['sg_pattern'].format(**self.get_task_id_content) \
                            if permission not in ['outsource'] else self.path_file_dic['sg_oss_submit_path'].format(**self.get_task_id_content)
        self.sg_pattern_path = self.path_file_dic['sg_pattern'].format(**self.get_task_id_content)
        # 获取工程文件路径
        self.sg_work_file_path = self.file_path + '/' + self.path_file_dic['sg_work_file_name'].format(**self.get_task_id_content)
        # 获取无版本工程文件路径
        self.sg_workfile_no_version = self.file_path+'/'+self.path_file_dic['sg_workfile_no_version'].format(**self.get_task_id_content)
        # 获取预览文件路径
        self.sg_prev_file_path = self.file_path + '/' + self.path_file_dic['sg_prev_file_name'].format(**self.get_task_id_content)
        # 获取无版本预览文件路径
        self.sg_prevfile_no_version = self.file_path+'/'+self.path_file_dic['sg_prevfile_no_version'].format(**self.get_task_id_content)
        # 获取附件文件路径
        self.sg_attachment_path = self.file_path+'/'+self.path_file_dic['sg_attachment_path'].format(**self.get_task_id_content)
        # 获取附件无版本文件路径
        self.sg_attachment_no_version = self.file_path+'/'+self.path_file_dic['sg_attachment_no_version'].format(**self.get_task_id_content)
        # 获取附件文件夹名字
        self.attachment_file_name = self.path_file_dic['sg_attachment_path'].format(**self.get_task_id_content)
        self.task_name.setText(self.path_file_dic['sg_work_file_name'].format(**self.get_task_id_content))
        self.submit_path.setText(self.file_path.replace('/', '\\'))
        self.submit_user.setText(self.task_dic['user'])
        self.submit_version.setText(self.get_task_id_content['version'])
        # self.type = self.get_task_id_content['type']

    def file_format(self, filename):
        return '.'+filename.split('.')[-1]

    def submit(self):
        if len(self.description.toPlainText()) < 10:
            MMessage.error(u'描述不能少于十个字符', parent=common_methods.get_widget_top_parent(self))
            return
        if self.construction_file.text() == 'Click or drag media file here':
            self.__work_file = None
            # MMessage.error(u'请上传工程文件', parent=common_methods.get_widget_top_parent(self))
            # return
        if self.preview_file.text() == 'Click or drag media file here':
            MMessage.error(u'请上传预览文件', parent=common_methods.get_widget_top_parent(self))
            return
        self.btn_submit.setEnabled(False)
        self.btn_closed.setEnabled(False)
        self.submit_progress.show()
        self.progress_label.show()
        try:
            attach = fileIO.get_copy_list(self.__attach, self.sg_attachment_path+'/'+self.__attach.split('/')[-1])
            attach_no_version = fileIO.get_copy_list(self.__attach, self.sg_attachment_no_version+'/'+self.__attach.split('/')[-1])
        except:
            attach = []
            attach_no_version = []
        copy_list = []
        if self.__work_file:
            copy_list.extend([
                [self.__work_file, self.sg_work_file_path + self.file_format(self.construction_file.text())],
                [self.__work_file, self.sg_workfile_no_version+self.file_format(self.construction_file.text())]
            ])
        if self.__prev_file:
            copy_list.extend([
                [self.__prev_file, self.sg_prev_file_path + self.file_format(self.preview_file.text())],
                [self.__prev_file, self.sg_prevfile_no_version+self.file_format(self.preview_file.text())]
            ])
        copy_list.extend(attach)
        copy_list.extend(attach_no_version)
        if permission in ['outsource']:
            self.rpc_copy_list = [self.file_path, self.sg_pattern_path]  # 通知内部从阿里云下载的路径列表
        self.copy_thread.copy_list = copy_list
        self.copy_thread.start()
        MMessage.config(999)
        self.copy_msg = MMessage.loading(u'正在上传文件，请勿操作', parent=common_methods.get_widget_top_parent(self))

    def progress(self, data):
        if not self.mute_lock:
            self.mute_lock = 1
            self.submit_progress.setValue(data[1])
            self.progress_label.setText(u'正在上传：'+ data[0])
            self.mute_lock = 0
        else:
            self.copy_info.append(data)

    def copy_finished(self, data):
        if self.copy_info:
            for cp in self.copy_info:
                self.submit_progress.setValue(cp[1])
                self.progress_label.setText(cp[0])
        self.progress_label.setText(u'正在写入数据库，请稍后....')
        if permission in ['outsource']:
            self.fetching_from_rpc_copy.copy_list = self.rpc_copy_list
            self.fetching_from_rpc_copy.mode = "download"
            self.fetching_from_rpc_copy.start()
        else:
            self.write_to_shotgun()

    def write_to_shotgun(self):
        self.copy_msg.close()
        self.copy_thread.quit()
        sg_work_file_path = self.sg_pattern_path + '/' + self.path_file_dic['sg_work_file_name'].format(
            **self.get_task_id_content) + self.file_format(self.construction_file.text())
        sg_workfile_no_version = self.sg_pattern_path + '/' + self.path_file_dic['sg_workfile_no_version'].format(
            **self.get_task_id_content) + self.file_format(self.construction_file.text())
        sg_prev_file_path = self.sg_pattern_path + '/' + self.path_file_dic['sg_prev_file_name'].format(
            **self.get_task_id_content) + self.file_format(self.preview_file.text())
        sg_prevfile_no_version = self.sg_pattern_path + '/' + self.path_file_dic['sg_prevfile_no_version'].format(
            **self.get_task_id_content) + self.file_format(self.preview_file.text())
        sg_attachment_path = self.sg_pattern_path + '/' + self.path_file_dic['sg_attachment_path'].format(
            **self.get_task_id_content)
        sg_attachment_no_version = self.sg_pattern_path + '/' + self.path_file_dic[
            'sg_attachment_no_version'].format(**self.get_task_id_content)
        self.write_msg = MMessage.loading(u'正在写入数据库，请勿操作', parent=common_methods.get_widget_top_parent(self))
        self.write_database.data = {
            'project': self.task_dic['project'],
            'type': self.get_task_id_content['type'],
            'user': self.task_dic['user'],
            'code': self.get_task_id_content['code'],
            'id': self.task_dic['id'],
            'task_name': self.get_task_id_content['task_name'],
            'new_version': self.get_task_id_content['version'].zfill(3),
            'description': self.description.toPlainText(),
            'sg_work_file_path': sg_work_file_path,
            'sg_workfile_no_version': sg_workfile_no_version,
            'sg_prev_file_path': sg_prev_file_path,
            'sg_prevfile_no_version': sg_prevfile_no_version,
            'sg_attachment_path': sg_attachment_path,
            'sg_attachment_no_version': sg_attachment_no_version,
            'version_code': self.path_file_dic['sg_work_file_name'].format(**self.get_task_id_content),
            'no_version_code': self.path_file_dic['sg_workfile_no_version'].format(**self.get_task_id_content),
            'local_prev': self.preview_file.text()
        }
        self.write_database.start()

    def finish_from_rpc_copy(self, finished):
        if finished:
             self.write_to_shotgun()
        else:
             MMessage.config(1)
             MMessage.error(u'上传失败！', parent=common_methods.get_widget_top_parent(self))

    def write_finished(self, data):
        if data:
            self.write_msg.close()
            MMessage.config(1)
            MMessage.success(u'写入成功', parent=common_methods.get_widget_top_parent(self))
            self.submit_progress.setValue(100)
            self.submit_progress.set_status(MProgressBar.SuccessStatus)
            self.progress_label.setText(u'任务上传完成!')
            self.write_database.quit()
            self.btn_closed.setEnabled(True)


def upload_local_file(task_dict):
    test = UploadFileLocalAction(task_dict, parent=task_dict['widget'])
    test.show()

if __name__ == '__main__':
    import sys
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": 15969, "type": "Version", "user": "TD_Group", "project": "DSF"}
    test = UploadFileLocalAction(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
