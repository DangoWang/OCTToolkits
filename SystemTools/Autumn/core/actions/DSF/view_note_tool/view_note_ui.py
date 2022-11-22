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
from dayu_widgets.message import MMessage
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.line_edit import MLineEdit
from SystemTools.Autumn.gui import autumn_page
import view_note
reload(view_note)
from utils import fileIO
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from utils import common_methods
type_list = ["Publish", "Approved", "Submit", "Dailies"]


class ViewNote(QWidget, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, task_dict=""):
        super(ViewNote, self).__init__()
        self.resize(500, 900)
        self.setWindowTitle(u'替换最新资产')
        self.task_dict = task_dict
        self.table_result = ""
        self.note_id_list = []
        self.user = self.task_dict["user"]
        group_info = view_note.get_group_list(self.user)
        self.identity = group_info["sg_permission_group"]

        self.label_version_type = MLabel(u"版本类型:")
        type_menu = MMenu()
        type_menu.set_data(type_list)
        self.type_combobox = MComboBox().small()
        self.type_combobox.set_menu(type_menu)

        self.label_version = MLabel(u"版本:")
        self.version_menu = MMenu()
        self.version_combobox = MComboBox().small()
        self.version_combobox.set_menu(self.version_menu)

        self.describe_edit = MTextEdit()
        self.describe_edit.setMaximumHeight(200)

        self.note_id_lb = MLabel(u'编号:').secondary()
        self.note_id = MLabel(u'未发布').secondary()
        self.note_id_lb.setMaximumWidth(150)

        self.accept_user_lb = MLabel(u'接受反馈者:').secondary()
        self.accept_user = MLabel(u'未发布').secondary()
        self.accept_user_lb.setMaximumWidth(150)

        self.submit_user_lb = MLabel(u'提交反馈者:').secondary()
        self.submit_user = MLabel(u'未发布').secondary()
        self.submit_user_lb.setMaximumWidth(150)

        self.data_lb = MLabel(u'反馈日期:').secondary()
        self.data = MLabel(u'未发布').secondary()
        self.data_lb.setMaximumWidth(150)

        self.version_lb = MLabel(u'链接的版本:').secondary()
        self.version = MLabel(u'未发布').secondary()
        self.version_lb.setMaximumWidth(150)

        self.attachments_lb = MLabel(u'附件:').secondary()
        self.attachments = MLabel(u'未发布').secondary()
        self.attachments_lb.setMaximumWidth(150)

        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setPlaceholderText(u'输入下载路径')
        self.tips_pb = MPushButton(text=u'下载附件').small()
        self.tips_pb.setMinimumWidth(80)

        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        self.mime_data_table = autumn_page.SheetContent()
        self.mime_data_table.fetch_data_thread.result_sig.connect(self.get_table)
        self.mime_data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mime_data_table.setMaximumHeight(400)
        self.mime_data_table.setMinimumWidth(500)

        layout_version = QHBoxLayout()
        layout_version.addWidget(self.label_version_type)
        layout_version.addWidget(self.type_combobox)
        layout_version.addWidget(self.label_version)
        layout_version.addWidget(self.version_combobox)

        self.note_id_layout = QHBoxLayout()
        self.note_id_layout.addWidget(self.note_id_lb)
        self.note_id_layout.addWidget(self.note_id)

        self.accept_user_layout = QHBoxLayout()
        self.accept_user_layout.addWidget(self.accept_user_lb)
        self.accept_user_layout.addWidget(self.accept_user)

        self.submit_user_layout = QHBoxLayout()
        self.submit_user_layout.addWidget(self.submit_user_lb)
        self.submit_user_layout.addWidget(self.submit_user)

        self.data_lb_layout = QHBoxLayout()
        self.data_lb_layout.addWidget(self.data_lb)
        self.data_lb_layout.addWidget(self.data)

        self.version_lb_layout = QHBoxLayout()
        self.version_lb_layout.addWidget(self.version_lb)
        self.version_lb_layout.addWidget(self.version)

        self.attachments_lb_layout = QHBoxLayout()
        self.attachments_lb_layout.addWidget(self.attachments_lb)
        self.attachments_lb_layout.addWidget(self.attachments)

        self.download_layout = QHBoxLayout()
        self.download_layout.addWidget(self.dir_path_le)
        self.download_layout.addWidget(self.tips_pb)

        self.progress_lay1 = QHBoxLayout()
        self.progress_lay1.addWidget(self.progress)
        self.progress_lay1.addWidget(self.progress_label)

        self.label_layout = QVBoxLayout()
        self.label_layout.addLayout(self.note_id_layout)
        self.label_layout.addLayout(self.accept_user_layout)
        self.label_layout.addLayout(self.submit_user_layout)
        self.label_layout.addLayout(self.data_lb_layout)
        self.label_layout.addLayout(self.version_lb_layout)
        self.label_layout.addLayout(self.attachments_lb_layout)
        self.label_layout.addLayout(self.download_layout)
        self.label_layout.addLayout(self.progress_lay1)

        main_lay = QGridLayout()
        main_lay.addWidget(MDivider(u'选择版本'), 0, 0)
        main_lay.addLayout(layout_version, 1, 0)
        main_lay.addWidget(MDivider(u'反馈描述'), 2, 0)
        main_lay.addWidget(self.describe_edit, 3, 0)
        main_lay.addWidget(MDivider(u'反馈详情'), 4, 0)
        main_lay.addLayout(self.label_layout, 5, 0)
        main_lay.addWidget(self.mime_data_table, 6, 0)
        self.setLayout(main_lay)
        self.mime_data_table.table.clicked.connect(self.change_task_info)
        self.tips_pb.clicked.connect(self.down_load)
        self.type_combobox.textChanged.connect(self.find_version)
        self.version_combobox.textChanged.connect(self.find_note)
        self.fetching_note_thread = fileIO.FormRPCDownloadUrlFile() if self.identity in ['outsource'] else \
            fileIO.DownloadUrlFile()
        self.fetching_note_thread.progress.connect(self.get_data)
        self.fetching_note_thread.finished.connect(self.finish_fetch_data)

    @property
    def version_type(self):
        return self.type_combobox.currentText()

    @property
    def version_name(self):
        return self.version_combobox.currentText()

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    def set_data(self, data):
        """
        :param data: 表格数据
        :return:
        """
        self.mime_data_table.model.set_data_list(data)

    def clear_data(self):
        # 清空数据
        self.set_data([])
        self.mime_data_table.model.clear()

    def find_version(self):
        self.progress_label.hide()
        self.progress.hide()
        self.clear_data()
        self.describe_edit.setText("")
        self.note_id.setText(u"未发布")
        self.submit_user.setText(u"未发布")
        self.accept_user.setText(u"未发布")
        self.version.setText(u"未发布")
        self.data.setText(u"未发布")
        self.version_combobox.clear()
        version_name, note_id_list = view_note.get_version__note_dict(self.task_dict, self.version_type)
        self.version_menu.set_data(version_name)
        self.note_id_list = note_id_list

    def find_note(self):
        for note_id in self.note_id_list:
            if self.version_name == note_id.keys()[0]:
                version_note_id = note_id.values()
                if version_note_id:
                    self.set_table_info(version_note_id)
                else:
                    MMessage.config(2)
                    MMessage.error(u'该任务没有反馈!', parent=self.task_dict['widget'])
                break

    def set_table_info(self, version_note_id):
        self.mime_data_table.set_config({"page_actions": "",
                                         "page_fields": [{u"label": u"接受反馈者", u"key": "addressings_to"},
                                                         {u"label": u"链接资产版本", u"key": "note_links"},
                                                         {u"label": u"附件", u"key": "attachments"},
                                                         {u"label": u"状态", u"key": "sg_status_list"},
                                                         {u"label": u"类型", u"key": "sg_note_type"},
                                                         {u"label": u"反馈时间", u"key": "created_at"},
                                                         {u"label": u"反馈者", u"key": "sg_proposer"},
                                                         {u"label": u"反馈内容", u"key": "content"},
                                                         ],
                                         "page_filters": [["id", "in", version_note_id[0]],
                                                          ["project", "name_is", self.task_dict["project"]]],
                                         "page_name": "Group",
                                         "page_type": "Note",
                                         "page_svg": "calendar_line.svg",
                                         "page_order": [{'field_name': 'created_at', 'direction': 'desc'}]
                                         })
        self.mime_data_table.parse_config()

    def get_table(self, result):
        self.table_result = result
        row = 0
        self.add_label_info(row)

    def add_label_info(self, row):
        content = self.mime_data_table.model_sort.index(row, 8).data()
        self.describe_edit.setText(content)
        _id = self.mime_data_table.model_sort.index(row, 0).data()
        self.note_id.setText(_id)
        submit_user = self.mime_data_table.model_sort.index(row, 7).data()
        self.submit_user.setText(submit_user)
        accept_user = self.mime_data_table.model_sort.index(row, 1).data()
        self.accept_user.setText(accept_user)
        version_lb = self.mime_data_table.model_sort.index(row, 2).data()
        self.version.setText(version_lb)
        data_lb = self.mime_data_table.model_sort.index(row, 6).data()
        self.data.setText(data_lb)
        attachments_lb = self.mime_data_table.model_sort.index(row, 3).data()
        if attachments_lb:
            self.tips_pb.setText(u"带附件")
            self.tips_pb.setDisabled(False)
            self.dir_path_le.setDisabled(False)
        else:
            self.tips_pb.setText(u"没有附件")
            self.tips_pb.setDisabled(True)
            self.dir_path_le.setDisabled(True)
        self.hide_column()

    def hide_column(self):
        self.mime_data_table.table.hideColumn(0)
        self.mime_data_table.table.hideColumn(3)
        self.mime_data_table.table.hideColumn(8)

    def change_task_info(self):
        row = self.mime_data_table.table.currentIndex().row()
        self.add_label_info(row)

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
            self.fetching_note_thread.wait()
            self.fetching_note_thread.quit()

    def down_load(self):
        if not self.folder_path:
            MMessage.config(2)
            MMessage.error(u'请先路径!', parent=self.task_dict['widget'])
            return
        selected_indexes = self.mime_data_table.table.selectedIndexes()
        rows = list(set([index.row() for index in selected_indexes]))
        attachments_id = []
        down_info = {}
        for r in rows:
            note_id = self.mime_data_table.model_sort.index(r, 0).data()
            for t in self.table_result:
                if t["id"] == int(note_id):
                    if t["attachments"]:
                        self.progress_label.show()
                        self.progress.show()
                        for file_id in t["attachments"]:
                            attachments_id.append(file_id["id"])
                        break
                    else:
                        self.progress_label.hide()
                        self.progress.hide()
                        MMessage.config(2)
                        MMessage.error(u'没有附件可以下载！', parent=self.task_dict['widget'])

        if attachments_id:
            self.set_progress(0)
            down_info[self.folder_path] = attachments_id
            self.fetching_note_thread.attachments_dict = down_info
            self.fetching_note_thread.start()
        else:
            self.progress_label.hide()
            self.progress.hide()
            MMessage.config(2)
            MMessage.error(u'没有附件可以下载！', parent=self.task_dict['widget'])


def view_note_drawer(widget, task_dict):
    from ....widgets import ADrawer
    drawer_widget = ADrawer('Note', parent=widget)
    drawer_widget.setMinimumWidth(500)
    drawer_widget.set_dayu_position('right')
    detail_content = ViewNote(task_dict)
    drawer_widget.set_widget(detail_content)
    return drawer_widget


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    dict_info = {"id": [15975], "type": "Task", "user": "TD", "project": "DSF"}
    test = ViewNote(dict_info)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


