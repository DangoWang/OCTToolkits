#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9.03
# wechat : 18250844478
###################################################################
import sys
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.browser import MDragFileButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.spin_box import MDateTimeEdit
from PySide.QtCore import QDateTime
from dayu_widgets.message import MMessage
from dayu_widgets.line_edit import MLineEdit
from config import GLOBAL
from utils import fileIO
from pprint import pprint
import submit_daily
reload(submit_daily)
image_types = GLOBAL.format_file["picture"]
video_types = GLOBAL.format_file["video"]
daily_filters = image_types+video_types
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class SubmitDailyWindow(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, task_dict_info="", parent=None):
        super(SubmitDailyWindow, self).__init__(parent)
        self.resize(470, 520)
        self.rpc_copy_list = []
        self.version_id = ""
        self.path_to_movie = ""
        self.mov_display_name = ""
        self.return_info_list = []
        self.task_dict = task_dict_info
        self.task_info, self.group_list = submit_daily.get_task_name(self.task_dict)
        if self.task_info[0]["entity"]:
            task_name = self.task_info[0]["entity"]["name"] + "_" + self.task_info[0]["content"]
        else:
            task_name = self.task_info[0]["content"]
        user_name = self.task_dict['user']
        self.setWindowTitle(u'提交 Daily')
        self.task_name_layout = QHBoxLayout()
        self.task_name_lb = MLabel(u'任务名称:').secondary()
        self.task_name = MLabel(task_name).secondary()

        self.task_name_layout.addWidget(self.task_name_lb)
        self.task_name_layout.addWidget(self.task_name)
        self.task_name_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout = QHBoxLayout()
        self.user_lb = MLabel(u'提交用户:').secondary()
        self.user = MLabel(user_name).secondary()
        self.layout.addWidget(self.user_lb)
        self.layout.addWidget(self.user)
        self.change_time_lb = MLabel(u'提交日期:').secondary()
        self.date_time_edit = MDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)
        self.date_time_edit.setReadOnly(True)
        self.layout.addWidget(self.change_time_lb)
        self.layout.addWidget(self.date_time_edit)

        self.browser_8 = MDragFileButton(text='Click or drag media file here', multiple=False)
        self.browser_8.set_dayu_svg('media_line.svg')
        self.browser_8.set_dayu_filters(daily_filters)
        self.register_field('current_file', '')
        self.bind('current_file', self.browser_8, 'dayu_path', signal='sig_file_changed')
        self.bind('current_file', self.browser_8, 'text')
        self.label_f = MLabel(u"附件:")
        self.label_f.setMinimumWidth(48)
        self.file_line = MLineEdit().folder()
        self.file_line.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')

        self.describe_te = MTextEdit(u'输入描述...')
        self.describe_te.setMaximumHeight(100)

        self.button_layout = QHBoxLayout()
        self.submit_pb = MPushButton(text=u'提交')
        self.close_pb = MPushButton(text=u'关闭')
        self.button_layout.addWidget(self.submit_pb)
        self.button_layout.addWidget(self.close_pb)

        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.label_f)
        self.path_layout.addWidget(self.file_line)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.task_name_layout)
        main_lay.addLayout(self.layout)
        main_lay.addWidget(MDivider(u'选择视频'))
        main_lay.addWidget(self.browser_8)
        main_lay.addLayout(self.path_layout)
        main_lay.addWidget(MDivider(u'描述'))
        main_lay.addWidget(self.describe_te)
        main_lay.addLayout(self.button_layout)
        self.setLayout(main_lay)

        self.submit_pb.clicked.connect(self.submit_daily)
        self.close_pb.clicked.connect(self.close)
        self.fetching_copy_thread = fileIO.CopyFTP() if self.group_list["sg_permission_group"] in ['outsource'] \
            else fileIO.CopyFile()
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)
        # self.fetching_copy_attachment_thread = fileIO.CopyFile()
        # self.fetching_copy_attachment_thread.finished.connect(self.finish_attachment_data)
        if self.group_list["sg_permission_group"] in ['outsource']:
            self.fetching_from_rpc_copy = fileIO.FormRPCCopy("download")
            self.fetching_from_rpc_copy.finished.connect(self.finish_from_rpc_copy)

    @property
    def describe(self):
        # 返回描述
        return self.describe_te.toPlainText()

    @property
    def folder_path(self):
        # 返回当前文件路径
        return self.file_line.text().replace('\\', '/')

    def submit_daily(self):
        self.submit_pb.setText(u"正在提交daily...")
        self.submit_pb.setDisabled(True)
        file_path = self.field("current_file")
        if not file_path:
            MMessage.config(2)
            MMessage.error(u'请先选择文件!', parent=self.task_dict["widget"])
            return
        self.task_info[0]["daily_file"] = file_path
        self.task_info[0]["project"] = self.task_dict["project"]
        self.task_info[0]["describe"] = self.describe
        self.task_info[0]["user"] = self.task_dict["user"]
        self.task_info[0]["attachment"] = self.folder_path
        self.return_info_list = submit_daily.copy_daily_file(self.task_info[0], self.group_list)
        copy_file_list = self.return_info_list[0]
        self.rpc_copy_list = self.return_info_list[4]
        self.fetching_copy_thread.copy_list = copy_file_list
        self.fetching_copy_thread.start()
        #   daily文件copy

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()
            if self.group_list["sg_permission_group"] in ['outsource']:
                # 如果是外包客户上传的daily，就发送阿里云路径跟下载到本地的路径,通知内部进行下载
                pprint(self.rpc_copy_list)
                self.fetching_from_rpc_copy.copy_list = self.rpc_copy_list
                self.fetching_from_rpc_copy.mode = "download"
                self.fetching_from_rpc_copy.start()
            else:
                self.version_id, self.path_to_movie, self.mov_display_name = \
                    submit_daily.create_daily_version(self.task_info[0], self.return_info_list, self.folder_path)
                submit_daily.upload_mov(self.version_id, self.path_to_movie, self.mov_display_name)
                MMessage.config(2)
                MMessage.success(u'上传daily成功!', parent=self.task_dict["widget"])
                self.submit_pb.setText(u"上传成功")

    def finish_from_rpc_copy(self, finished):
        if finished:
            self.fetching_from_rpc_copy.wait()
            self.fetching_from_rpc_copy.quit()
            self.version_id, self.path_to_movie, self.mov_display_name = \
                submit_daily.create_daily_version(self.task_info[0], self.return_info_list, self.folder_path)
            # print "iiiiiiiiiiiiiiiii", self.version_id, self.path_to_movie, self.mov_display_name
            submit_daily.upload_mov(self.version_id, self.path_to_movie, self.mov_display_name)
            MMessage.config(2)
            MMessage.success(u'上传daily成功!', parent=self.task_dict["widget"])
            self.submit_pb.setText(u"上传成功")
        else:
            MMessage.config(2)
            MMessage.error(u'上传daily失败!', parent=self.task_dict["widget"])

    def finish_attachment_data(self, finished):
        if finished:
            self.fetching_copy_attachment_thread.wait()
            self.fetching_copy_attachment_thread.quit()


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": [15975], "type": "Task", "user": "huangna", "project": "DSF"}
    test = SubmitDailyWindow(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())

