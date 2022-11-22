#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import pprint
import os
import sys
from dayu_widgets.qt import *
from dayu_widgets import label
from dayu_widgets import push_button
from dayu_widgets import line_edit
from dayu_widgets.radio_button import MRadioButton
from dayu_widgets import text_edit
from SystemTools.Autumn.gui import autumn_page
from dayu_widgets.tool_button import MToolButton
from functools import partial
from pprint import pprint
from utils import shotgun_operations
from utils import fileIO
import utils.shotgun_operations as sg
import create_message
reload(create_message)

class UnreadMessageUIClass(QMainWindow):
    def __init__(self, project, user, parent=None):
        super(UnreadMessageUIClass, self).__init__(parent)
        self.resize(1300, 500)
        self.project = project
        self.user = user
        self.this_name = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', self.user]],
                                                                        ['code', 'sg_permission_group'])
        self.identity = self.this_name["sg_permission_group"]
        self.setWindowTitle(u'消息列表')
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.gridLayout_main = QGridLayout(self.central_widget)

        self.project_id = sg.find_one_shotgun('Project', [['name', 'is', self.project]], ['id'])
        self.user_name_id = sg.find_one_shotgun("Group", [["sg_login", "is", self.user]], ["id", "code"])

        # left
        self.frame_left = QFrame(self.central_widget)
        self.gridLayout_main.addWidget(self.frame_left, 0, 0, 1, 1)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_left.sizePolicy().hasHeightForWidth())
        self.frame_left.setSizePolicy(sizePolicy)
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.gridLayout_left = QGridLayout(self.frame_left)


        self.pushButton_add = MToolButton().svg('add_line.svg').icon_only()
        self.pushButton_add.clicked.connect(self.create_ticket)
        self.gridLayout_left.addWidget(self.pushButton_add, 0, 0, 1, 1)

        # 搜索框
        self.line_edit_find = line_edit.MLineEdit(self.frame_left).search().small()
        self.gridLayout_left.addWidget(self.line_edit_find, 0, 1, 1, 1)
        # 弹簧
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_left.addItem(spacerItem, 0, 2, 1, 1)
        # 类型选择
        self.unread_bt = MRadioButton(u"未读")
        self.read_bt = MRadioButton(u"已读")
        self.all_bt = MRadioButton(u"全部")
        self.gridLayout_left.addWidget(self.unread_bt, 0, 3, 1, 1)
        self.gridLayout_left.addWidget(self.read_bt, 0, 4, 1, 1)
        self.gridLayout_left.addWidget(self.all_bt, 0, 5, 1, 1)
        self.unread_bt.setChecked(1)
        self.unread_bt.clicked.connect(partial(self.find_note, 0))
        self.read_bt.clicked.connect(partial(self.find_note, 1))
        self.all_bt.clicked.connect(partial(self.find_note, 2))
        # note 列表
        self.listview = autumn_page.SheetContent()
        self.listview.project = self.project
        self.listview.show_msg = 1
        self.listview.msg_parent = self.listview
        self.listview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listview.setMinimumHeight(300)
        self.listview.setMinimumWidth(666)
        self.gridLayout_left.addWidget(self.listview, 2, 0, 1, 5)
        self.listview.table.clicked.connect(self.show_select_info)
        self.line_edit_find.textChanged.connect(self.listview.model_sort.set_search_pattern)

        # right
        self.frame_right = QFrame(self.central_widget)
        self.gridLayout_main.addWidget(self.frame_right, 0, 1, 1, 1)
        self.frame_right.setFrameShape(QFrame.StyledPanel)
        self.frame_right.setFrameShadow(QFrame.Raised)
        self.gridLayout_right = QGridLayout(self.frame_right)

        label_01 = label.MLabel(parent=self.frame_right)
        label_01.setText(u"链接：")
        self.gridLayout_right.addWidget(label_01, 0, 0, 1, 1)
        self.label_link = label.MLabel(parent=self.frame_right)
        self.gridLayout_right.addWidget(self.label_link, 0, 1, 1, 1)

        label_02 = label.MLabel(parent=self.frame_right)
        label_02.setText(u"标题：")
        self.gridLayout_right.addWidget(label_02, 1, 0, 1, 1)
        self.label_title = label.MLabel(parent=self.frame_right)
        self.gridLayout_right.addWidget(self.label_title, 1, 1, 1, 1)

        label_03 = label.MLabel(parent=self.frame_right)
        label_03.setText(u"描述：")
        label_03.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.gridLayout_right.addWidget(label_03, 2, 0, 1, 1)
        self.description = text_edit.MTextEdit(self.frame_right)
        self.gridLayout_right.addWidget(self.description, 2, 1, 1, 1)

        self.groupBox_path = QGroupBox(self.frame_right)
        self.gridLayout_right.addWidget(self.groupBox_path, 3, 0, 1, 2)

        self.gridLayout_path = QGridLayout(self.groupBox_path)
        label_path = label.MLabel(parent=self.groupBox_path)
        label_path.setText(u"附件：")
        self.gridLayout_path.addWidget(label_path, 0, 0, 1, 1)
        self.lineEdit_path = line_edit.MLineEdit(self.groupBox_path).folder()
        self.lineEdit_path.setPlaceholderText(u'下载路径...')
        self.gridLayout_path.addWidget(self.lineEdit_path, 0, 1, 1, 1)
        self.pushButton_download = push_button.MPushButton(self.groupBox_path)
        self.pushButton_download.setText(u"下载")
        self.pushButton_download.clicked.connect(self.download_file)
        self.gridLayout_path.addWidget(self.pushButton_download, 1, 0, 1, 2)
        self.clean_info()
        self.find_note(0)
        self.note_sg = None
        self.fetching_export_thread = fileIO.FormRPCDownloadUrlFile() if self.identity in ['outsource'] else\
            fileIO.DownloadUrlFile()
        self.fetching_export_thread.finished.connect(self.finish_fetch_data)

    def show_select_info(self):
        self.clean_info()
        self.thread_num = 0
        selected_content = self.listview.get_selected_content()
        if not selected_content:
            return
        note_id = selected_content[0]["id"]
        filters = [["id", "is", note_id]]
        fields = ["subject", "content", "note_links", "attachments", "sg_attachment_path"]
        self.note_sg = shotgun_operations.find_one_shotgun("Note", filters, fields)
        link_name = []
        for li in self.note_sg["note_links"]:
            link_name.append(li["name"])
        self.label_link.setText(";".join(link_name))
        self.label_title.setText(self.note_sg["subject"])
        self.description.setText(self.note_sg["content"])
        if self.note_sg["attachments"] or self.note_sg["sg_attachment_path"]:
            self.groupBox_path.setVisible(1)
        else:
            self.groupBox_path.setVisible(0)
        # make_note_read([note_id])

    def clean_info(self):
        self.label_link.setText("")
        self.label_title.setText("")
        self.description.setText("")
        self.pushButton_download.setText(u'下载')
        self.groupBox_path.setVisible(0)

    def find_note(self, num):
        filters = [["addressings_to", "name_contains", self.this_name['code']]]
        if num == 0:
            filters = [["addressings_to", "name_contains", self.this_name['code']],
                       ["sg_if_read", "is", False]]
        elif num == 1:
            filters = [["addressings_to", "name_contains", self.this_name['code']],
                       ["sg_if_read", "is", True]]

        self.listview.set_config({"page_actions": [{'label': u'标为已读', 'value': 'mark_read', 'icon': 'success_line.svg', 'mode': '1',},
                                                   {'label': u'查看详情', 'value': 'note_details', 'icon': 'info_fill.svg', 'mode': '1',},],
                                  "page_fields": [
                                      {u"label": u"提出者", u"key": "sg_proposer", 'searchable': 1},
                                      {u"label": u"主题", u"key": "subject", 'searchable': 1},
                                                  {u"label": u"创建时间", u"key": "updated_at", 'searchable': 1}],
                                  # "page_filters": [["sg_if_read", "is", True]],
                                  "page_filters": filters,
                                  "page_name": u"消息",
                                  "page_type": "Note",
                                  "page_order": [{'field_name': 'id', 'direction': 'desc'}]
                                 })
        self.listview.parse_config()

    def finish_fetch_data(self, finished):
        if finished:
            self.thread_num += 1
        if self.thread_num == 2:
            # self.fetching_export_thread.wait()
            # self.fetching_export_thread.quit()
            self.pushButton_download.setText(u'下载完成！')
            self.pushButton_download.setEnabled(1)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def download_file(self):
        file_path = self.lineEdit_path.text().replace('\\', '/')
        if not self.note_sg or not file_path:
            return
        if not self.note_sg["attachments"] or not self.note_sg["sg_attachment_path"]:
            self.thread_num += 1
        permission = shotgun_operations.get_permission(self.user)
        file_id_list = []
        # outsource 外包
        if self.note_sg["attachments"]:
            for att in self.note_sg["attachments"]:
                file_id_list.append(att["id"])
            print {file_path: file_id_list}
            self.fetching_export_thread.attachments_dict = {file_path: file_id_list}
            self.fetching_export_thread.start()
            self.pushButton_download.setEnabled(0)
            self.pushButton_download.setText(u'正在下载...')
        if self.note_sg["sg_attachment_path"]:
            copy_thread = fileIO.CopyFile()
            if permission == "outsource":
                copy_thread = fileIO.CopyFTP()
            copy_thread.copy_list = [[self.note_sg["sg_attachment_path"], file_path], ]
            copy_thread.start()
            copy_thread.finished.connect(self.finish_fetch_data)
            self.pushButton_download.setEnabled(0)
            self.pushButton_download.setText(u'正在下载...')
        # this_name = sg.find_one_shotgun('Group', [['sg_login', 'is', user]], ['code'])

    def create_ticket(self):
        create_ticket_win = create_message.CreateMessageUI(parent=self)
        create_ticket_win.show()
        # create_ticket_win.submit_pb.clicked.connect(lambda: self.create_ticket_task(create_ticket_win))



def make_note_read(id_list):
    for id_note in id_list:
        note_new = {"sg_if_read": True}
        shotgun_operations.update_shotgun("Note", id_note, note_new)


def main(project, user, parent):
    win = UnreadMessageUIClass(project, user, parent)
    return win
# if __name__ == '__main__':
#     main()




