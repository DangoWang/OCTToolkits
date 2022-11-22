#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8.26
###################################################################

from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.qt import *
from dayu_widgets.message import MMessage
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.progress_bar import MProgressBar
import file_download
reload(file_download)
from utils import fileIO
from pprint import pprint
import os


class DownloadWindow(QDialog):

    def __init__(self, download_task_dict="", parent=None):
        super(DownloadWindow, self).__init__(parent)
        self.resize(470, 170)
        self.download_dict = download_task_dict
        self.setWindowTitle(u'下载工具')
        self.copy_file_list = []
        self.send_copy_list = []
        self.splitter = QSplitter()
        self.splitter.setFixedHeight(100)
        self.splitter.setOrientation(Qt.Vertical)
        path_label = MLabel(u'选择路径：').secondary()
        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.dir_path_le.setText(u'E:/Projects/')
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标选择下载路径')
        # self.dir_path_le.setReadOnly(True)
        self.get_files_pb = MPushButton(u'下载').small().primary()
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        path_lay1 = QHBoxLayout()
        path_lay1.addWidget(path_label)
        path_lay1.addWidget(self.dir_path_le)
        path_lay1.addWidget(self.get_files_pb)
        progress_lay1 = QVBoxLayout()
        progress_lay1.addWidget(self.progress)
        progress_lay1.addWidget(self.progress_label)
        path_lay1.addStretch()

        main_lay = QVBoxLayout()
        path_lay1.addWidget(self.splitter)
        main_lay.addLayout(path_lay1)
        main_lay.addLayout(progress_lay1)
        main_lay.addStretch()
        self.setLayout(main_lay)
        self.group_list = file_download.get_group_list(self.download_dict["user"])
        self.get_files_pb.clicked.connect(self.get_files)
        self.fetching_copy_thread = fileIO.CopyFTP() if self.group_list["sg_permission_group"] in ['outsource'] \
            else fileIO.CopyFile()
        self.fetching_copy_thread.progress.connect(self.get_data)
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        existing_txt = self.dir_path_le.text().replace('\\', '/')
        return existing_txt

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(u'正在下载：' + text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'完成！')

    def get_files(self):
        if not self.folder_path:
            MMessage.config(2)
            MMessage.error(u'请先选择路径!', parent=self)
            return
        # else:
        self.get_files_pb.setText(u"正在下载...")
        self.get_files_pb.setDisabled(True)
        self.progress_label.show()
        self.progress.show()
        self.progress_label.setText(u'准备开始...')
        self.progress.setValue(0)
        self.download_dict['local_path'] = self.folder_path
        self.download_dict['identity'] = self.group_list["sg_permission_group"]
        if self.download_dict["type"] == "Version":
            self.copy_file_list = file_download.get_version_info(self.download_dict)
        elif download_win.download_dict["type"] == "Task":
            self.copy_file_list = file_download.get_task_info(self.download_dict)
        if self.copy_file_list:
            self.set_progress(0)
            self.fetching_copy_thread.copy_list = self.copy_file_list
            self.fetching_copy_thread.start()

    def get_data(self, data):
        self.set_progress(data[1], data[0])

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()
            if self.group_list["sg_permission_group"] in ['outsource']:
                fail_file_name = []
                for file_path in self.copy_file_list:
                    if not os.path.isfile(file_path[-1]):
                        fail_file_name.append(os.path.split(file_path[-1])[-1])
                if fail_file_name:
                    MMessage.config(2)
                    MMessage.error(u'{}这些文件下载失败!'.format(fail_file_name), parent=self)
                self.get_files_pb.setText(u"下载完成...")
            else:
                self.get_files_pb.setText(u"下载完成...")


def main(download_dict):
    from dayu_widgets import dayu_theme
    global download_win
    download_win = DownloadWindow(download_dict, parent=download_dict['widget'])
    dayu_theme.apply(download_win)
    download_win.show()



if __name__ == '__main__':
    import sys
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    download_dict = {"task_id": [14608], "type":"Task", "user":"TD", "project": "Demo: Animation"}
    test = DownloadWindow(download_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


