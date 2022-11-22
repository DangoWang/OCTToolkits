#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
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
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from utils import shotgun_operations
from dayu_widgets.progress_bar import MProgressBar
import maya.cmds as cmds
import os
import shutil
from utils import fileIO
import maya.mel as mel

sg = shotgun_operations


class ArrangeCachePath(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, attr_node_list="", parent=None):
        super(ArrangeCachePath, self).__init__(parent)
        self.resize(470, 200)
        self.setWindowTitle(u'整理缓存/贴图路径')
        self.attr_node_list = attr_node_list

        self.source_cache_path = MLabel(u'源路径：').secondary()
        self.source_path_le = MLineEdit().folder()

        self.target_cache_path = MLabel(u'目标路径：').secondary()
        self.target_path_le = MLineEdit().folder()

        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        self.submit_pb = MPushButton(text=u'开始')
        self.close_pb = MPushButton(text=u'关闭')

        self.gridLayout_v = QGridLayout()
        self.gridLayout_v.addWidget(self.source_cache_path, 0, 0)
        self.gridLayout_v.addWidget(self.source_path_le, 0, 1)
        self.gridLayout_v.addWidget(self.target_cache_path, 1, 0)
        self.gridLayout_v.addWidget(self.target_path_le, 1, 1)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress)
        self.progress_layout.addWidget(self.progress_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submit_pb)
        self.button_layout.addWidget(self.close_pb)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout_v)
        main_lay.addLayout(self.progress_layout)
        main_lay.addLayout(self.button_layout)
        self.setLayout(main_lay)
        self.project = sg.get_project()
        self.user_name = sg.get_user()
        self.task_dic = sg.get_tasks(self.project, self.user_name)
        self.submit_pb.clicked.connect(self.start_copy_cache)
        self.close_pb.clicked.connect(self.close)
        self.fetching_copy_thread = fileIO.CopyFile()
        self.fetching_copy_thread.progress.connect(self.get_data)
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)

    @property
    def source_folder_path(self):
        # 返回当前文件夹路径
        return self.source_path_le.text().replace('\\', '/')

    @property
    def target_folder_path(self):
        # 返回当前文件夹路径
        return self.target_path_le.text().replace('\\', '/')

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(u'正在拷贝：' + text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'完成！')

    def get_data(self, data):
        self.set_progress(data[1], data[0])

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()
            failed = []
            for attr_node in self.attr_node_list:
                node_attr_path = cmds.getAttr(attr_node).replace("\\", "/")
                new_abc_path = node_attr_path.replace(self.source_folder_path, self.target_folder_path)
                print attr_node, new_abc_path
                try:
                    cmds.setAttr(attr_node, new_abc_path, type="string")
                except:
                    pass
                result_attr = cmds.getAttr(attr_node).replace("\\", "/")
                if result_attr == node_attr_path:
                    failed.append(attr_node)
            self.submit_pb.setText(u"整理完成。")
            if failed:
                QMessageBox.question(self, u"提示",
                                     u"以下属性由于maya自身原因未成功指定，你可以选择重新开启maya重试， 或者在filePathEditor中指定:\n%s" % failed)
                mel.eval('FilePathEditor;')

    def start_copy_cache(self):
        if not self.source_folder_path and not self.target_folder_path:
            MMessage.config(2)
            MMessage.error(u'请正确的路径', parent=self)
            return
        self.submit_pb.setText(u"正在整理。。。")
        self.submit_pb.setDisabled(True)
        self.progress_label.show()
        self.progress.show()
        new_copy_list = []
        for attr_node in self.attr_node_list:
            node_attr_path = cmds.getAttr(attr_node).replace("\\", "/")
            if self.source_folder_path in node_attr_path:
                new_copy_list.append([node_attr_path, node_attr_path.replace(self.source_folder_path, self.target_folder_path)])
        # copy_file_list = fileIO.get_copy_list(self.source_folder_path, self.target_folder_path)
        self.fetching_copy_thread.copy_list = new_copy_list
        self.fetching_copy_thread.start()


def main(attr_node_list, parent_win):
    from dayu_widgets import dayu_theme
    global test
    test = ArrangeCachePath(attr_node_list=attr_node_list, parent=parent_win)
    dayu_theme.apply(test)
    test.show()


