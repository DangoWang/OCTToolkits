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
from utils import fileIO


class DownloadWindow(QDialog):

    def __init__(self, parent=None):
        super(DownloadWindow, self).__init__(parent)
        self.resize(470, 170)
        self.setWindowTitle(u'下载工具')

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

        # self.get_files_pb.clicked.connect(self.get_files)
        self.fetching_copy_thread = fileIO.CopyFile()
        self.fetching_copy_thread.progress.connect(self.get_data)
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)
        self.copy_file_list = []

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        existing_txt = self.dir_path_le.text().replace('\\', '/') + '/'
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

    def get_data(self, data):
        self.set_progress(data[1], data[0])

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()
            self.get_files_pb.setText(u"下载完成...")


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
