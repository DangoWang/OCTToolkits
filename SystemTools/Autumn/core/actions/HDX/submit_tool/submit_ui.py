# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/12/13

import os
import sys
import time
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.browser import MDragFileButton, MDragFolderButton
from dayu_widgets.message import MMessage
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.check_box import MCheckBox
from PySide.QtGui import *
import functools
from PySide.QtCore import *
from utils import fileIO, shotgun_operations
from config import GLOBAL
from utils import common_methods


class HDXSubmit(QDialog, MFieldMixin):

    def __init__(self, task_dict, parent=None):
        super(HDXSubmit, self).__init__(parent=parent)
        self.work_file = None
        self.prev_file = None
        self.attach = None
        self._init_ui()

    def _init_ui(self):
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(MDivider(u'提交文件'))

        version_name_layout = QHBoxLayout()
        self.version_name_lb = MLabel()
        version_name_layout.addWidget(MLabel(u'即将创建新版本:'))
        version_name_layout.addWidget(self.version_name_lb)
        version_name_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__main_layout.addLayout(version_name_layout)

        self.__main_layout.addWidget(MDivider(u'工程文件'))
        self.construction_file_cb = MCheckBox(u'<< 若需要上传工程文件请点击')
        self.construction_file_cb.setStyleSheet('color: #467947;')
        construction_file_layout = QHBoxLayout()
        construction_file_layout.addWidget(self.construction_file_cb)
        self.construction_file_btn = MDragFileButton(text='')
        self.construction_file_btn.setFixedHeight(70)
        self.construction_file_btn.set_dayu_svg('upload_line.svg')
        self.construction_file_btn.setVisible(False)
        construction_file_layout.addWidget(self.construction_file_btn)
        self.construction_file_cb.stateChanged.connect(self.__change_upload_construction_files_state)
        self.construction_file_btn.sig_file_changed.connect(self.__construction_path)
        self.__main_layout.addLayout(construction_file_layout)

        self.__main_layout.addWidget(MDivider(u'预览文件'))
        self.preview_file_cb = MCheckBox(u'<< 若需要上传预览文件请点击')
        self.preview_file_cb.setStyleSheet('color: #467947;')
        preview_file_layout = QHBoxLayout()
        preview_file_layout.addWidget(self.preview_file_cb)
        self.preview_file_btn = MDragFileButton(text='')
        self.preview_file_btn.setFixedHeight(70)
        self.preview_file_btn.set_dayu_svg('media_line.svg')
        self.preview_file_btn.setVisible(False)
        preview_file_layout.addWidget(self.preview_file_btn)
        self.preview_file_cb.stateChanged.connect(self.__change_upload_preview_files_state)
        self.preview_file_btn.sig_file_changed.connect(self.__preview_path)
        self.__main_layout.addLayout(preview_file_layout)

        self.__main_layout.addWidget(MDivider(u'附件(文件夹)'))
        self.attach_cb = MCheckBox(u'<< 若需要上传附件请点击')
        self.attach_cb.setStyleSheet('color: #467947;')
        attach_layout = QHBoxLayout()
        attach_layout.addWidget(self.attach_cb)
        self.attach_btn = MDragFolderButton()
        self.attach_btn.setText('')
        self.attach_btn.setFixedHeight(70)
        self.attach_btn.setVisible(False)
        attach_layout.addWidget(self.attach_btn)
        self.attach_cb.stateChanged.connect(self.__change_upload_attach_state)
        self.attach_btn.sig_folder_changed.connect(self.__attach_path)
        self.__main_layout.addLayout(attach_layout)

        self.__main_layout.addWidget(MDivider(u'描述'))
        self.desc_edit = MTextEdit()
        self.desc_edit.setMinimumHeight(50)
        self.desc_edit.setFixedHeight(70)
        self.__main_layout.addWidget(self.desc_edit)

        __doit_button_layout = QHBoxLayout()
        self.submit_btn = MPushButton(u'上传').small()
        self.cancel_btn = MPushButton(u'取消').small()
        __doit_button_layout.addWidget(self.submit_btn)
        __doit_button_layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.close)
        self.__main_layout.addLayout(__doit_button_layout)

        self.__log_edit = MTextEdit()
        self.__log_edit.setMinimumHeight(200)
        self.__log_edit.setReadOnly(True)
        self.__log_edit.hide()
        self.__main_layout.addWidget(self.__log_edit)

        self.progress_layout = QVBoxLayout()
        self.submit_progress = MProgressBar()
        self.submit_progress.hide()
        self.progress_label = MLabel()
        self.progress_label.hide()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.submit_progress)
        self.__main_layout.addLayout(self.progress_layout)

        self.submit_btn.clicked.connect(self.submit_doit)

        self.setLayout(self.__main_layout)
        self.setMinimumWidth(500)

    def __change_upload_construction_files_state(self):
        if self.construction_file_cb.isChecked():
            self.construction_file_btn.setVisible(True)
            self.construction_file_cb.setText(u'点击选择或拖拽文件 >>')
            return
        self.construction_file_btn.setVisible(False)
        self.construction_file_cb.setText(u'<< 若需要上传工程文件请点击')

    def __change_upload_preview_files_state(self):
        if self.preview_file_cb.isChecked():
            self.preview_file_btn.setVisible(True)
            self.preview_file_cb.setText(u'点击选择或拖拽文件 >>')
            return
        self.preview_file_btn.setVisible(False)
        self.preview_file_cb.setText(u'<< 若需要上传预览文件请点击')

    def __change_upload_attach_state(self):
        if self.attach_cb.isChecked():
            self.attach_btn.setVisible(True)
            self.attach_cb.setText(u'点击选择或拖拽文件夹 >>')
            return
        self.attach_btn.setVisible(False)
        self.attach_cb.setText(u'<< 若需要上传附件请点击')

    def __construction_path(self, text):
        self.construction_file_btn.setText(text)
        self.construction_file_btn.set_dayu_svg('')
        self.work_file = text

    @property
    def construction_format(self):
        if self.work_file:
            return '.' + self.work_file.split('.')[-1]

    @property
    def preview_format(self):
        if self.prev_file:
            return '.' + self.prev_file.split('.')[-1]

    @property
    def description(self):
        return self.desc_edit.toPlainText()

    def __preview_path(self, text):
        self.preview_file_btn.setText(text)
        self.preview_file_btn.set_dayu_svg('')
        self.prev_file = text

    def __attach_path(self, text):
        self.attach_btn.setText(text)
        self.attach_btn.set_dayu_svg('')
        self.attach = text

    def append_log(self, text):
        self.__log_edit.append('\n' + text)

    def submit_doit(self):
        self.construction_file_btn.setEnabled(False)
        self.construction_file_cb.setEnabled(False)
        self.preview_file_btn.setEnabled(False)
        self.preview_file_cb.setEnabled(False)
        self.attach_btn.setEnabled(False)
        self.attach_cb.setEnabled(False)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setText(u'正在上传...')
        self.cancel_btn.setEnabled(False)
        self.__log_edit.setVisible(True)
        self.append_log(u'开始上传文件， 请在允许你关闭窗口之前不要关闭此窗口...')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from dayu_widgets.theme import MTheme
    window = HDXSubmit({})
    this_theme = MTheme('dark')
    this_theme.apply(window)
    window.show()
    sys.exit(app.exec_())