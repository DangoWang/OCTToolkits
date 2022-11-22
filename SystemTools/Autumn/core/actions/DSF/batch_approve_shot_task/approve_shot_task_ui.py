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
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.line_edit import MLineEdit
from utils import shotgun_operations, fileIO


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


class ApproveShotWin(QDialog):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, parent=None):
        super(ApproveShotWin, self).__init__(parent)
        self.resize(470, 400)
        self.setWindowTitle(u'同步镜头')
        self.publish_task_name = MTextEdit()
        self.publish_task_name.setEnabled(0)
        self.publish_task_name_label = MLabel(u'版本名称：')

        self.addressings_lb = MTextEdit()
        self.addressings_lb.setEnabled(0)
        self.addressings_lb_lb = MLabel(u'通知给：')

        self.btn_group = QHBoxLayout()
        self.btn_submit = MPushButton(u'同步').small()
        self.btn_closed = MPushButton(u'关闭').small()
        self.btn_submit.setFixedWidth(220)
        self.btn_closed.setFixedWidth(220)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_submit)
        self.btn_group.addWidget(self.btn_closed)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.progress_layout = QHBoxLayout()
        self.progress_lb = MLabel()
        self.submit_progress = MProgressBar()
        self.progress_layout.addWidget(self.progress_lb)
        self.progress_layout.addWidget(self.submit_progress)

        info_layout = QGridLayout()
        info_layout.addWidget(self.publish_task_name_label, 0, 0)
        info_layout.addWidget(self.publish_task_name, 0, 1)
        info_layout.addWidget(self.addressings_lb_lb, 1, 0)
        info_layout.addWidget(self.addressings_lb, 1, 1)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'同步信息'))
        main_lay.addLayout(info_layout)
        main_lay.addLayout(self.progress_layout)
        main_lay.addLayout(self.btn_group)
        self.setLayout(main_lay)
        self.file_IO_publish = fileIO.FormRPCCopy('upload')  # fileIO.CopyFTP()
        self.file_IO_publish.finished.connect(self.copy_finished)
        self.file_IO_publish.progress.connect(self.progress)
        self.write_data_base_thread = WriteDatabase(parent=self)
        self.write_data_base_thread.write_finished.connect(self.finish_writing)
        self.btn_closed.clicked.connect(self.close)
        self.btn_submit.clicked.connect(self.approve)

    def approve(self):
        self.btn_submit.setEnabled(False)
        self.btn_submit.setText(u"正在上传...")
        self.btn_closed.setEnabled(False)

    def progress(self, data):
        self.submit_progress.setValue(data[1])
        self.progress_label.setText(u'正在上传：'+ data[0])

    def copy_finished(self):
        self.progress_label.setText(u'拷贝完成！')
        self.btn_submit.setText(u"上传完成！")
        # 只拷贝文件的话就通知外包
        self.progress_label.setText(u'正在写入数据库，请稍后....')
        self.write_data_base_thread.start()

    def finish_writing(self, result):
        if result:
            MMessage.config(2)
            MMessage.success(u'数据库写入成功！', parent=self)
            self.progress_label.setText(u'数据库写入成功！')
            self.submit_progress.setValue(100)


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = ApproveShotWin()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


