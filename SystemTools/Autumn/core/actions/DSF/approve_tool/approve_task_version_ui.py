#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import config.GLOBAL
import time
import utils.common_methods as atu
reload(config.GLOBAL)
image_types = config.GLOBAL.format_file["picture"]
video_types = config.GLOBAL.format_file["video"]
daily_filters = image_types+video_types

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class WriteDatabase(QThread):

    write_finished = Signal(bool)

    def __init__(self, parent=None):
        super(WriteDatabase, self).__init__(parent)
        self.data = None

    def run(self, *args, **kwargs):
        for each in self.data:
            print each
            if each:
                if each[0] == 'update':
                    shotgun_operations.update_shotgun(each[1], each[2], each[3])
                if each[0] == 'create':
                    shotgun_operations.create_shotgun(each[1], each[2])
        self.write_finished.emit(True)


class ApprovedFileAction(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, parent=None):
        super(ApprovedFileAction, self).__init__(parent)
        self.addressings_lb = MLabel('')
        self.progress_layout = QVBoxLayout()
        self.submitInfo_layout = QGridLayout()
        self.des_lb = MLabel()
        self.publishd_task_name = MLabel()
        self.publishd_task_name_label = MLabel(u'版本名称：')
        self.setWindowTitle(u'同步资产')
        self.resize(565, 300)
        self.mute_lock = 0
        self.copy_info = []
        self.work_mode = 'approve'  # 2019.10.21新增需求，需要将拷贝文件和approve动作分开
        self.file_IO_publish = fileIO.FormRPCCopy('upload')  # fileIO.CopyFTP()
        self.file_IO_publish.finished.connect(self.copy_finished)
        self.file_IO_publish.progress.connect(self.progress)
        self.write_data_base_thread = WriteDatabase(parent=self)
        self.write_data_base_thread.write_finished.connect(self.finish_writing)
        self.addUi()

    def addUi(self):
        publishd_task_name_layout = QHBoxLayout()
        publishd_task_name_layout.addWidget(self.publishd_task_name_label)
        publishd_task_name_layout.addWidget(self.publishd_task_name)

        des_layout = QHBoxLayout()
        _label = MLabel(u'版本描述：')
        des_layout.addWidget(_label)
        des_layout.addWidget(self.des_lb)

        # self.description_label = MLabel(u'发布描述：')
        # self.description = MTextEdit()

        self.submitInfo_layout.addLayout(publishd_task_name_layout, 0, 0)
        self.submitInfo_layout.addLayout(des_layout, 1, 0)
        # self.submitInfo_layout.addWidget(self.publishd_task_name_label, 0, 0)
        # self.submitInfo_layout.addWidget(self.publishd_task_name, 0, 1)
        # self.submitInfo_layout.addWidget(self.description_label, 4, 0)
        # self.submitInfo_layout.addWidget(self.description, 4, 2)
        # self.submitInfo_layout.addItem(QSpacerItem(5, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.submit_progress = MProgressBar()
        self.progress_label = MLabel()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.submit_progress)

        self.addressings_lb_lb = MLabel(u'通知给：')
        self.addressings_layout = QHBoxLayout()
        self.addressings_layout.addWidget(self.addressings_lb_lb)
        self.addressings_layout.addWidget(self.addressings_lb)

        self.btn_group = QHBoxLayout()
        self.btn_submit = MPushButton(u'同步').small()
        self.btn_closed = MPushButton(u'关闭').small()
        self.btn_submit.setFixedWidth(100)
        self.btn_closed.setFixedWidth(100)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_submit)
        self.btn_group.addWidget(self.btn_closed)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(MDivider(u'提交信息'))
        self.main_layout.addLayout(self.submitInfo_layout)
        self.main_layout.addLayout(self.addressings_layout)
        self.main_layout.addWidget(MDivider())
        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.addLayout(self.btn_group)
        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.main_layout)
        # self.submit_progress.hide()
        # self.progress_label.hide()
        ####connect
        self.btn_closed.clicked.connect(self.close)
        self.btn_submit.clicked.connect(self.publishd)

    def publishd(self):
        self.btn_submit.setEnabled(False)
        self.btn_closed.setEnabled(False)
        self.submit_progress.show()
        self.progress_label.show()
        MMessage.config(999)
        if self.work_mode in ['approve']:  # 如果只是approve锁定版本，那就不拷贝文件
            self.progress_label.setText(u'正在写入数据库，请稍后....')
            self.write_data_base_thread.start()
            return
        elif self.work_mode in ['upload']:
            self.copy_msg = MMessage.loading(u'正在上传文件，请勿操作', parent=atu.get_widget_top_parent(self))
            self.file_IO_publish.start()

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
        self.copy_msg.close()
        self.progress_label.setText(u'拷贝完成！')
        # 只拷贝文件的话就通知外包
        self.progress_label.setText(u'正在写入数据库，请稍后....')
        self.write_data_base_thread.start()

    def finish_writing(self, result):
        if result:
            MMessage.config(2)
            MMessage.success(u'数据库写入成功！', parent=atu.get_widget_top_parent(self))
            self.progress_label.setText(u'数据库写入成功！')
            self.submit_progress.setValue(100)


if __name__ == '__main__':
    from thirdparty.dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": 13020, "type": "Version", "user": "TD_Group", "project": "DSF"}
    test = ApprovedFileAction()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


