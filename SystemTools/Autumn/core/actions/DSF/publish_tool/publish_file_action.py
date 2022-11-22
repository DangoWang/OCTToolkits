# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import pprint
import sys
import os
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.message import MMessage
from utils import shotgun_operations, fileIO
import time
import utils.common_methods as atu

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class WriteDatabase(QThread):
    write_finished = Signal(bool)

    def __init__(self, data={}, no_data={}, parent=None):
        super(WriteDatabase, self).__init__(parent)
        self.data = data
        self.no_data = no_data

    def run(self, *args, **kwargs):
        #  pprint.pprint(self.data)
        project_info = shotgun_operations.find_one_shotgun('Project', [['name', 'is', self.data['project']]], ['id'])
        filters_entity = [['project', 'name_is', self.data['project']], ['code', 'is', self.data['code']]]
        entity = shotgun_operations.find_one_shotgun(self.data['type'], filters_entity, ['id', 'code'])
        filters_task = [['project', 'name_is', self.data['project']], ['id', 'is', self.data['task_id']]]
        sg_task = shotgun_operations.find_one_shotgun('Task', filters_task, ['id', 'code', 'step.Step.short_name', 'step.Step.code'])
        user_info = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', self.data['user']]],
                                                        ['sg_group_project', 'id', 'code'])
        create_data = dict(project=project_info, sg_path_to_frames=self.data['sg_path_to_frames'],
                           sg_path_to_movie=self.data['sg_path_to_movie'],
                           sg_path_to_geometry=self.data['sg_path_to_geometry'],
                           sg_version_number=self.data['sg_version_number'], description=self.data['description'],
                           user=user_info, entity=entity, sg_version_type='Publish', code=self.data['version_code'],
                           sg_task=sg_task, )
        #  # # 创建版本
        version_entity = shotgun_operations.create_shotgun('Version', create_data)
        #  # # 上传预览图
        #  print version_entity['id']
        #  print self.data['sg_path_to_movie']
        shotgun_operations.upload_shotgun("Version", version_entity['id'], self.data['local_prev'],
                                          field_name="sg_uploaded_movie", display_name=self.data['sg_path_to_movie'])
        #  #  # # 更新发布版本
        due_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        update_dict = {'sg_publish_version': self.data['sg_version_number']}
        update_dict.update({"sg_date_1": str(due_date)})
        if sg_task["step.Step.short_name"] not in ["bk", "an", "ly"]:
            update_dict.update({"sg_status_list": "apr"})
        shotgun_operations.update_shotgun('Task', self.data['task_id'], update_dict)

        if not self.no_data:
            self.write_finished.emit(True)
            return

        create_data_no_version = dict(project=project_info, sg_path_to_frames=self.no_data['sg_path_to_frames'],
                                      sg_path_to_movie=self.no_data['sg_path_to_movie'],
                                      sg_path_to_geometry=self.no_data['sg_path_to_geometry'], sg_version_number=None,
                                      description=self.data['description'], user=user_info, entity=entity,
                                      sg_version_type='Publish', code=self.no_data['code'], sg_task=sg_task, )
        #  # # 创建版本
        version_id = shotgun_operations.find_shotgun('Version', [['project', 'name_is', 'DSF'],
                                                                 ['code', 'is', self.no_data['code']],
                                                                 ['sg_version_type', 'is', 'Publish']], ['id', 'code'])
        if version_id:
            no_version_entity = shotgun_operations.update_shotgun('Version', version_id[0]['id'],
                                                                  create_data_no_version)
        else:
            no_version_entity = shotgun_operations.create_shotgun('Version', create_data_no_version)
        #  # # 上传预览图
        shotgun_operations.upload_shotgun("Version", no_version_entity['id'], self.no_data['local_prev'],
                                          field_name="sg_uploaded_movie", display_name=self.no_data['code'])
        #  #
        # 发送通知给抄送人
        task_info = shotgun_operations.find_one_shotgun('Task', [['id', 'is', self.data['task_id']]],
                                                        ['entity.Asset.addressings_cc',
                                                        'entity.Shot.addressings_cc',
                                                        'addressings_cc', 'content', 'entity', 'step.Step.short_name']
                                                        )
        asset_adressings = task_info['entity.Asset.addressings_cc'] or []
        shot_adressings = task_info['entity.Shot.addressings_cc'] or []
        task_name_en = task_info['entity'].get('name', 'None') + '_' + task_info['content']
        task_info['addressings_cc'].extend(asset_adressings)
        task_info['addressings_cc'].extend(shot_adressings)
        if task_info.get('step.Step.short_name') in ['rig']:
            anim_groups = shotgun_operations.find_shotgun('Group', [['sg_group_project', 'name_is', shotgun_operations.get_project()],
                                                                    ['sg_department', 'is', u'动画']], ['sg_login'])
            task_info['addressings_cc'].extend(anim_groups)
        note_data = {
            "project": project_info,
            "subject": u'任务上传通知：'+task_name_en,
            "sg_proposer": user_info,
            "addressings_to": task_info['addressings_cc'],
            "content": u"用户{}已发布任务{}。描述为:\n{}".format(user_info.get('code', 'None'), task_name_en, self.data['description']),
            "sg_if_read": False,
        }
        shotgun_operations.create_shotgun('Note', note_data)
        self.write_finished.emit(True)


class ApprovedFileAction(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, version_dict={}, parent=None):
        super(ApprovedFileAction, self).__init__(parent)
        self.resize(565, 450)
        self.mute_lock = 0
        self.copy_info = []
        self.version_dict = []
        self.file_IO_publish = fileIO.CopyFile()
        self.file_IO_publish.finished.connect(self.copy_finished)
        self.file_IO_publish.progress.connect(self.progress)
        self.write_database = WriteDatabase()
        self.write_database.write_finished.connect(self.write_finished)
        self.set_version_info(version_dict)

    def set_version_info(self, version_info):
        if not version_info:
            return
        self.version_dict = version_info.copy()
        self.version_dict['id'] = version_info['id'][0]
        self.version_info()
        self.addUi()

    def version_info(self):
        self.version = shotgun_operations.get_version(self.version_dict["project"], self.version_dict['id'])
        # self.version['code'] = self.version['entity_code']
        path_con = shotgun_operations.get_path_convention(self.version_dict['project'], self.version['type'], 'Submit')
        self.no_version = shotgun_operations.get_no_version(self.version_dict["project"],
                                                            path_con['sg_workfile_no_version'].format(**self.version))
        self.publishd_path_dict = shotgun_operations.get_path_convention(self.version_dict['project'],
                                                                         self.version['type'], 'Publish')

        self.file_path = self.publishd_path_dict['sg_pattern'].format(**self.version)
        # # # 获取工程文件路径
        self.sg_work_file_path = self.file_path + '/' + self.publishd_path_dict['sg_work_file_name'].format(
            **self.version)
        # # # 获取无版本工程文件路径
        self.sg_workfile_no_version = self.file_path + '/' + self.publishd_path_dict['sg_workfile_no_version'].format(
            **self.version)
        # #  获取预览文件路径
        self.sg_prev_file_path = self.file_path + '/' + self.publishd_path_dict['sg_prev_file_name'].format(
            **self.version)
        # #  获取无版本预览文件路径
        self.sg_prevfile_no_version = self.file_path + '/' + self.publishd_path_dict['sg_prevfile_no_version'].format(
            **self.version)
        # # # 获取附件文件路径
        self.sg_attachment_path = self.file_path + '/' + self.publishd_path_dict['sg_attachment_path'].format(
            **self.version)
        # # 获取附件无版本文件路径
        self.sg_attachment_no_version = self.file_path + '/' + self.publishd_path_dict[
            'sg_attachment_no_version'].format(**self.version)

    def addUi(self):
        self.publishd_task_name_label = MLabel(u'文件名：')
        self.publishd_task_name = MLabel()
        self.publishd_task_name.setText(self.version['code'])

        self.publishd_user_label = MLabel(u'发布用户：')
        self.publishd_user = MLabel()
        self.publishd_user.setText(self.version_dict['user'])

        self.publishd_version_label = MLabel(u'发布版本：')
        self.publishd_version = MLabel()
        self.publishd_version.setText(self.version['sg_version_number'])

        self.publishd_path_label = MLabel(u'发布路径：')
        self.publishd_path = MLabel()
        self.publishd_path.setText(self.file_path)

        self.description_label = MLabel(u'描述：')
        self.description = MTextEdit()

        self.submitInfo_layout = QGridLayout()
        self.submitInfo_layout.addWidget(self.publishd_task_name_label, 0, 0)
        self.submitInfo_layout.addWidget(self.publishd_task_name, 0, 1)
        self.submitInfo_layout.addWidget(self.publishd_user_label, 1, 0)
        self.submitInfo_layout.addWidget(self.publishd_user, 1, 1)
        self.submitInfo_layout.addWidget(self.publishd_version_label, 2, 0)
        self.submitInfo_layout.addWidget(self.publishd_version, 2, 1)
        self.submitInfo_layout.addWidget(self.publishd_path_label, 3, 0)
        self.submitInfo_layout.addWidget(self.publishd_path, 3, 1)
        self.submitInfo_layout.addWidget(self.description_label, 4, 0)
        self.submitInfo_layout.addWidget(self.description, 4, 1, 4, 4)

        self.progress_layout = QVBoxLayout()
        self.submit_progress = MProgressBar()
        self.progress_label = MLabel()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.submit_progress)

        self.btn_group = QHBoxLayout()
        self.btn_submit = MPushButton(u'发布').small()
        self.btn_closed = MPushButton(u'关闭').small()
        self.btn_submit.setFixedWidth(100)
        self.btn_closed.setFixedWidth(100)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_submit)
        self.btn_group.addWidget(self.btn_closed)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(MDivider(u'信息'))
        self.main_layout.addLayout(self.submitInfo_layout)
        self.main_layout.addWidget(MDivider())
        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.addLayout(self.btn_group)
        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.main_layout)
        self.submit_progress.hide()
        self.progress_label.hide()
        # # # # connect
        self.btn_closed.clicked.connect(self.closed)
        self.btn_submit.clicked.connect(self.publishd)
        self.description.setText(self.version['description'])

    @property
    def description_text(self):
        return self.description.toPlainText()

    def file_format(self, filename):
        return '.' + filename.split('.')[-1]

    def closed(self):
        self.close()

    def publishd(self):
        MMessage.config(3)
        if len(self.description_text) < 10:
            MMessage.error(u'描述不能少于十个字符！', parent=atu.get_widget_top_parent(self))
            return u'描述不能少于十个字符！'
            # raise RuntimeError
        # if self.version['sg_version_type'] != 'Submit':
        #     MMessage.error(u'已发布版本不能重复发布。', parent=atu.get_widget_top_parent(self))
        #     return u'已发布版本不能重复发布。'
            # raise RuntimeError
        # if self.version['sg_publish_version'] and self.version['sg_publish_version'] >= self.version['version']:
        #     MMessage.error(u'正在发布版本低于已发布版本！', parent=atu.get_widget_top_parent(self))
        #     return u'正在发布版本低于已发布版本！'
            # raise RuntimeError
        self.btn_submit.setEnabled(False)
        self.btn_closed.setEnabled(False)

        self.submit_progress.show()
        self.progress_label.show()
        # try:
        # try:
        #     attach = fileIO.get_copy_list(self.version['sg_path_to_geometry'], self.sg_attachment_path)
        # except Exception, e:
        #     attach = []
        # try:
        #     attach_no_version = fileIO.get_copy_list(self.no_version['sg_path_to_geometry'],
        #                                            self.sg_attachment_no_version)
        # except Exception, e:
        #     attach_no_version = []
        attach = [[self.version['sg_path_to_geometry'], self.sg_attachment_path]] if self.version['sg_path_to_geometry'] else []
        attach_no_version = [[self.no_version['sg_path_to_geometry'], self.sg_attachment_no_version]] if self.no_version['sg_path_to_geometry'] else []
        copy_list = [[self.version['sg_path_to_frames'],
                      self.sg_work_file_path + self.file_format(self.version['sg_path_to_frames'])],
                     [self.no_version['sg_path_to_frames'],
                      self.sg_workfile_no_version + self.file_format(self.no_version['sg_path_to_frames'])],

                     [self.version['sg_path_to_movie'],
                      self.sg_prev_file_path + self.file_format(self.version['sg_path_to_movie'])],
                     [self.no_version['sg_path_to_movie'],
                      self.sg_prevfile_no_version + self.file_format(self.no_version['sg_path_to_movie'])], ]
        copy_list.extend(attach)
        copy_list.extend(attach_no_version)
        self.file_IO_publish.copy_list = copy_list
        self.file_IO_publish.start()
        MMessage.config(9999)
        self.copy_msg = MMessage.loading(u'正在上传文件，请勿操作', parent=atu.get_widget_top_parent(self))
        return True
        # except Exception, e:
        #     print u'发生未知错误:', e
        #     return u'发生未知错误:', e

    def progress(self, data):
        if not self.mute_lock:
            self.mute_lock = 1
            self.submit_progress.setValue(data[1])
            self.progress_label.setText(u'正在上传：' + data[0])
            self.mute_lock = 0
        else:
            self.copy_info.append(data)

    def copy_finished(self, data):
        if self.copy_info:
            for cp in self.copy_info:
                self.submit_progress.setValue(cp[1])
                self.progress_label.setText(cp[0])
        self.progress_label.setText(u'正在写入数据库，请稍后....')
        if data:
            self.copy_msg.close()
            self.file_IO_publish.quit()
            self.write_msg = MMessage.loading(u'正在写入数据库，请勿操作', parent=atu.get_widget_top_parent(self))
            self.write_database.data = {'project': self.version_dict["project"],
                                        'sg_path_to_frames': self.sg_work_file_path + self.file_format(
                                            self.version['sg_path_to_frames']),
                                        'sg_path_to_movie': self.sg_prev_file_path + self.file_format(
                                            self.version['sg_path_to_movie']),
                                        'sg_path_to_geometry': self.sg_attachment_path,
                                        'description': self.description_text, 'user': self.version_dict['user'],
                                        'version_code': self.publishd_path_dict['sg_work_file_name'].format(
                                            **self.version), 'code': self.version['code'], 'type': self.version['type'],
                                        'task_id': self.version['task_id'],
                                        'sg_version_number': self.version['sg_version_number'],
                                        'local_prev': self.version['sg_path_to_movie'], }
            try:
                self.write_database.no_data = {'sg_path_to_frames': self.sg_workfile_no_version + self.file_format(
                    self.no_version['sg_path_to_frames']),
                                               'sg_path_to_movie': self.sg_prevfile_no_version + self.file_format(
                                                   self.no_version['sg_path_to_movie']),
                                               'sg_path_to_geometry': self.sg_attachment_no_version,
                                               'local_prev': self.no_version['sg_path_to_movie'],
                                               'code': self.no_version['code'], 'type': self.no_version['type'], }
            except:
                self.write_database.no_data = None
            self.write_database.start()
            self.submit_progress.setValue(50)

    def write_finished(self, data):
        if data:
            self.submit_progress.setValue(100)
            self.write_msg.close()
            MMessage.config(1)
            MMessage.success(u'写入成功', parent=atu.get_widget_top_parent(self))
            self.submit_progress.setValue(100)
            self.submit_progress.set_status(MProgressBar.SuccessStatus)
            self.progress_label.setText(u'任务发布完成!')
            self.write_database.quit()
            self.btn_closed.setEnabled(True)


def publish_file(version_dict):
    from dayu_widgets import dayu_theme
    global test
    test = ApprovedFileAction(version_dict, parent=version_dict['widget'])
    dayu_theme.apply(test)
    test.show()


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    global test
    task_dict = {"id": 7071, "type": "Version", "user": "TD_Group", "project": "DSF"}
    test = ApprovedFileAction(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
