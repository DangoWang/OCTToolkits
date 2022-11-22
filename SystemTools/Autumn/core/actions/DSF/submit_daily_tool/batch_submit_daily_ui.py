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
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from config import GLOBAL
from utils import fileIO
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets import dayu_theme
from dayu_widgets.progress_bar import MProgressBar
import batch_submit_daily
reload(batch_submit_daily)
image_types = GLOBAL.format_file["picture"]
video_types = GLOBAL.format_file["video"]
daily_filters = image_types+video_types
import batch_submit_daily_qthread
import ssl
from pprint import pprint
ssl._create_default_https_context = ssl._create_unverified_context


batch_submit_header = [
    {
        'label': u'任务编号',
        'key': 'task_id',
        # 'searchable': True
    },
    {
        'label': u'镜头号',
        'key': 'shot',
        # 'searchable': True
    }, {
        'label': u'mov文件路径',
        'key': 'mov',
        # 'searchable': True
    }]


class BatchSubmitDaily(QDialog, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, parent=None):
        super(BatchSubmitDaily, self).__init__(parent)
        self.resize(750, 700)
        self.num = []
        self.all_num = ""
        self.group_list, self.project_name = batch_submit_daily.get_group_list()
        self.setAcceptDrops(True)  # 控制拖拽事件
        user_name = self.group_list["sg_login"]
        self.setWindowTitle(u'提交 Daily')
        self.task_name_layout = QHBoxLayout()
        self.task_name_lb = MLabel(u'任务名称:').secondary()
        self.group_cb = MComboBox()
        self.group_cb.set_placeholder(u'选择环节')
        self.group_cb.setMaximumWidth(100)
        self.group_menu = MMenu()
        groups = ["Ly", "An", "Bk", "Colorkey"]
        self.group_menu.set_data(groups)
        self.group_cb.set_dayu_size(dayu_theme.small)
        self.group_cb.set_menu(self.group_menu)
        self.group_cb.setObjectName('group_cb')
        self.task_name_layout.addWidget(self.task_name_lb)
        self.task_name_layout.addWidget(self.group_cb)
        self.task_name_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout = QHBoxLayout()
        self.user_lb = MLabel(u'提交用户:').secondary()
        self.user_lb.setMaximumWidth(80)
        self.user = MLabel(user_name).secondary()
        self.layout.addWidget(self.user_lb)
        self.layout.addWidget(self.user)
        self.change_time_lb = MLabel(u'提交日期:').secondary()
        self.change_time_lb.setMaximumWidth(80)
        self.date_time_edit = MDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)
        self.date_time_edit.setReadOnly(True)
        self.layout.addWidget(self.change_time_lb)
        self.layout.addWidget(self.date_time_edit)

        self.vertical_layout = QVBoxLayout()
        self.data_table = MTableView(size=dayu_theme.small, show_row_count=True)
        self.data_table.setShowGrid(True)
        self.data_table.set_no_data_text(u'拖拽文件或文件夹到这里')
        self.data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_model = MTableModel()
        self.model_sort = MSortFilterModel()
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.horizontalHeader().setStretchLastSection(1)
        self.model_sort.setSourceModel(self.data_model)
        self.data_table.setModel(self.model_sort)
        self.vertical_layout.addWidget(self.data_table)

        self.describe_te = MTextEdit(u'输入描述...')
        self.describe_te.setMaximumHeight(100)

        self.button_layout = QHBoxLayout()
        self.submit_pb = MPushButton(text=u'提交')
        self.close_pb = MPushButton(text=u'关闭')
        self.button_layout.addWidget(self.submit_pb)
        self.button_layout.addWidget(self.close_pb)

        h_layout = QHBoxLayout()
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        h_layout.addWidget(self.progress_label)
        h_layout.addWidget(self.progress)
        self.progress_label.hide()
        self.progress.hide()

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.task_name_layout)
        main_lay.addLayout(self.layout)
        main_lay.addWidget(MDivider(u'选择视频'))
        main_lay.addWidget(self.data_table)
        main_lay.addWidget(MDivider(u'描述'))
        main_lay.addWidget(self.describe_te)
        main_lay.addLayout(self.button_layout)
        main_lay.addLayout(h_layout)
        self.setLayout(main_lay)

        self.log_dialog = QTextEdit(self)
        self.log_dialog.setReadOnly(True)
        geo = QApplication.desktop().screenGeometry()
        self.log_dialog.setGeometry(geo.width() / 2 - 1000, geo.height() / 2 - 500, geo.width() / 4, geo.height() / 4)
        self.log_dialog.setWindowTitle(self.tr('Log Information'))
        self.log_dialog.setText(self.property('history'))
        self.log_dialog.setWindowFlags(Qt.Dialog)
        self.submit_pb.clicked.connect(self.get_task_info)
        self.close_pb.clicked.connect(self.close)
        self.fetching_copy_thread = fileIO.CopyFTP() if self.group_list["sg_permission_group"] in ['outsource'] \
            else fileIO.CopyFile()
        self.fetching_copy_thread.finished.connect(self.fetching_copy_data)

        self.fetching_batch_submit = batch_submit_daily_qthread.CreateDaily()
        self.fetching_batch_submit.progress.connect(self.finish_one_daily)
        self.fetching_batch_submit.finished.connect(self.submit_daily_finish)

        self.fetching_data_thread = batch_submit_daily.FetchBatchSubmitDailyThread()
        self.fetching_data_thread.fetch_result_sig.connect(self.get_data)
        self.fetching_data_thread.finished_sig.connect(self.finish_fetch_data)
        self.set_header(batch_submit_header)

    def set_header(self, header_data):
        """
        :param header_data: 表头
        :return:
        """
        self.data_model.set_header_list(header_data)
        self.data_table.set_header_list(header_data)

    def set_data(self, data):
        """
        :param data: 表格数据
        :return:
        """
        self.data_model.set_data_list(data)

    @property
    def describe(self):
        # 返回描述
        return self.describe_te.toPlainText()

    @property
    def folder_path(self):
        # 返回当前文件路径
        return self.file_line.text().replace('\\', '/')

    @property
    def group(self):
        # 返回当前环节
        return self.group_cb.currentText()

    def show_log(self):
        # 显示日志窗口
        self.log_dialog.show()

    def append_log(self, txt):
        # 增加一条日志信息
        log = self.log_dialog.toPlainText() or ''
        self.log_dialog.setText(log+'\n'+txt)

    def clear_log(self):
        # 清空日志信息
        self.log_dialog.clear()

    def clear_data(self):
        # 清空数据
        self.set_data([])
        self.data_model.clear()

    def append_data(self, data_dict):
        # 增加一条数据
        self.data_model.append(data_dict)

    @property
    def table_data(self):
        # 返回表格内容
        return self.data_model.get_data_list()

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'上传完成')
            self.submit_pb.setText(u"提交完成...")
            self.submit_pb.setDisabled(False)

    def get_task_info(self):
        self.submit_pb.setText(u"正在提交...")
        self.submit_pb.setDisabled(True)
        self.all_num = len(self.table_data)
        info_list = [self.table_data, self.describe, self.group_list]
        # info_list = ["界面表格信息内容","界面描述窗口内容"，"使用者的id,code,等信息"]
        self.fetching_batch_submit.task_info_list = info_list
        self.fetching_batch_submit.start()

    def get_data(self, data):
        txt = data['msg']
        self.append_log(txt)
        table_info = data['data']
        if table_info:
            self.append_data(dict(table_info.values()[0]))

    def dragEnterEvent(self, event):
        """获取拖拽过来的文件夹+文件"""
        if not self.group:
            MMessage.config(2)
            MMessage.error(u'请先选择环节!', parent=self)
            return
        self.clear_data()
        self.clear_log()
        self.set_progress(0)
        self.submit_pb.setText(u"提交")
        if event.mimeData().hasFormat("text/uri-list"):
            files_list = list(set([url.toLocalFile() for url in event.mimeData().urls()]))
            event.acceptProposedAction()
            self.fetching_data_thread.files_list = {
                'files': files_list,
                'group': self.group,
                'project': self.project_name
            }
            self.fetching_data_thread.start()

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_data_thread.wait()
            self.fetching_data_thread.quit()

    def fetching_copy_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()

    def submit_daily_finish(self, finished):
        if finished:
            self.fetching_batch_submit.wait()
            self.fetching_batch_submit.quit()

    def finish_one_daily(self, data):
        # data = [task_id, return_info_list, create_daily_info]
        # data = [在进行拷贝的任务id，["拷贝列表", "审核人列表", "daily版本名" ]，创建daily版本需要的信息字典]
        # create_daily_info = ["daily_file":mov_path, "id":任务id, "type"：任务类型, "project":project,
        # "user": user_name, "describe": daily_describe, "content"：任务名， "entity":entity]
        self.fetching_copy_thread.copy_list = data[1][0]
        self.fetching_copy_thread.start()
        batch_submit_daily.create_daily_version(data[2], data[1])
        self.num.append(str(data[0]))
        number = (float(len(self.num)) / float(self.all_num)) * 100
        text = u"编号{}的任务上传完成".format(data[0])
        self.set_progress(number, text)


if __name__ == '__main__':
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": [15975], "type": "Task", "user": "huangna", "project": "DSF"}
    test = BatchSubmitDaily()
    test.set_header(batch_submit_header)
    dayu_theme.apply(test)
    test.show()
    test.show_log()
    sys.exit(app.exec_())

