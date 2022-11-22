#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import sys
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.progress_bar import MProgressBar
from utils import fileIO
from utils import shotgun_operations
from dayu_widgets.message import MMessage
sg = shotgun_operations


class ViewProduction(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, task_dict="", parent=None):
        super(ViewProduction, self).__init__(parent)
        self.resize(470, 400)
        self.setWindowTitle(u'查看制作说明')
        self.task_dict = task_dict
        self.user = self.task_dict["user"]
        group_info = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', self.user]],
                                                         ['code', "sg_permission_group"])
        self.identity = group_info["sg_permission_group"]
        self.d_test, self.file_id = self.get_task_describe()
        self.text_describe = MTextEdit()
        self.text_describe.setText(self.d_test)
        path_label = MLabel(u'选择路径：').secondary()
        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.submit_pb = MPushButton(text=u'下载')

        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        path_lay1 = QHBoxLayout()
        path_lay1.addWidget(path_label)
        path_lay1.addWidget(self.dir_path_le)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress)
        self.progress_layout.addWidget(self.progress_label)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'制作说明'))
        main_lay.addWidget(self.text_describe)
        main_lay.addWidget(MDivider(u'下载附件'))
        main_lay.addLayout(path_lay1)
        main_lay.addWidget(self.submit_pb)
        main_lay.addLayout(self.progress_layout)
        self.setLayout(main_lay)

        self.submit_pb.clicked.connect(self.download_file)
        self.fetching_download_thread = fileIO.FormRPCDownloadUrlFile() if self.identity in ['outsource'] else \
            fileIO.DownloadUrlFile()
        self.fetching_download_thread.progress.connect(self.get_data)
        self.fetching_download_thread.finished.connect(self.finish_fetch_data)

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    def get_task_describe(self):
        file_id = []
        task_info = sg.find_shotgun("Task", [['project', 'name_is', self.task_dict["project"]],
                                             ["id", "is", self.task_dict["id"]]], ["sg_description", "sg_multi_entity"])
        d_text = task_info[0]["sg_description"]
        for file_info in task_info[0]["sg_multi_entity"]:
            file_id.append(file_info['id'])
        return d_text, file_id

    def download_file(self):
        self.submit_pb.setText(u"正在下载...")
        self.submit_pb.setDisabled(True)
        if not self.folder_path:
            MMessage.config(2)
            MMessage.error(u'请先路径!', parent=self)
            self.submit_pb.setText(u"下载")
            self.submit_pb.setDisabled(False)
            return
        if self.file_id:
            download_dict = {self.folder_path: self.file_id}
            self.set_progress(0)
            self.fetching_download_thread.attachments_dict = download_dict
            self.fetching_download_thread.start()
        else:
            MMessage.config(2)
            MMessage.error(u'没有可以下载的附件!', parent=self)
            self.submit_pb.setText(u"下载")
            self.submit_pb.setDisabled(False)

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'完成!')

    def get_data(self, data):
        self.set_progress(data)

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_download_thread.wait()
            self.fetching_download_thread.quit()
            self.submit_pb.setText(u"下载完成")


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = ViewProduction()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


