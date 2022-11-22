#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import datetime
import os

from dayu_widgets.divider import MDivider
from dayu_widgets.message import MMessage
from dayu_widgets import dayu_theme
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.label import MLabel
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.push_button import MPushButton
from dayu_widgets.menu import MMenu
from dayu_widgets.qt import *
from utils import shotgun_operations
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.button_group import MCheckBoxGroup
from dayu_widgets import spin_box
from utils.fileIO import DownloadUrlFile
from dayu_widgets.button_group import MRadioButtonGroup
from pprint import pprint
sg = shotgun_operations


def get_ticket_type(field_name=None):
    field_text = sg.schema_field_read_shotgun("Ticket", field_name)
    ticket_type_list = field_text[field_name]["properties"]["valid_values"]["value"]
    return ticket_type_list


def get_link_type(field_name=None):
    field_text = sg.schema_field_read_shotgun("Ticket", field_name)
    ticket_type_list = field_text[field_name]["properties"]["valid_types"]["value"]
    return ticket_type_list


table_header = [{'label': u'编号', 'key': 'id'},
                {'label': u'审核人员', 'key': 'examiners',},
                {'label': u'反馈描述', 'key': 'describe',},
                {'label': u'附件', 'key': 'file_name'},
                {'label': u'附件编号', 'key': 'file_id'}]


class CreateTicketUI(QDialog, MFieldMixin):
    def __init__(self, parent=None):
        super(CreateTicketUI, self).__init__(parent)
        self.resize(520, 490)
        self.setWindowTitle(u'创建工单')
        self.label_c_1 = MLabel(u"*工单分类:")
        self.label_c_1.setMinimumWidth(70)
        menu_c1 = MMenu()
        ticket_type = get_ticket_type(field_name="sg_ticket_type")
        menu_c1.set_data(ticket_type)
        self.combobox_c = MComboBox().small()
        self.combobox_c.set_menu(menu_c1)
        self.tips = MLabel()
        self.tips.hide()
        self.label_c_2 = MLabel(u"*工单标题:")
        self.label_c_2.setMinimumWidth(70)
        self.line_edit = MLineEdit()
        self.label_c_3 = MLabel(u" 工单描述:")
        self.label_c_3.setMinimumWidth(70)
        self.text_edit_c1 = MTextEdit(u'')
        self.checkbox_c = MCheckBox("")
        self.label_c_4 = MLabel(u"附件:")
        self.label_c_4.setMinimumWidth(48)
        self.line_edit_file = MLineEdit().folder().small()
        self.line_edit_file.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.checkbox_link = MCheckBox("")
        self.checkbox_link.hide()
        link_menu = MMenu()
        link_type = get_link_type(field_name="sg_link")
        link_menu.set_data(link_type)
        self.label_link_type = MLabel(u"链接类型:")
        self.label_link_type.hide()
        self.link_combobox = MComboBox().small()
        self.link_combobox.hide()
        self.link_combobox.set_menu(link_menu)
        self.label_link_id = MLabel(u"类型id:")
        self.label_link_id.hide()
        self.line_edit_link = MLineEdit().small()
        self.line_edit_link.hide()
        self.label_c_5 = MLabel(u"审核人员:")
        self.label_c_5.setMinimumWidth(48)
        self.label_c_5.setVisible(False)
        code_name_list = self.get_group_name()
        self.register_field('button2_selected', [u'王东浩'])
        menu2 = MMenu(exclusive=False)
        menu2.set_data(code_name_list)
        self.examiners_combobox = MComboBox()
        self.examiners_combobox.set_menu(menu2)
        self.bind('button2_selected', self.examiners_combobox, 'value', signal='sig_value_changed')
        self.examiners_combobox.hide()
        self.submit_pb = MPushButton(u'提交').small()
        self.close_pb = MPushButton(u'关闭').small()

        layout_label = QHBoxLayout()
        layout_label.addWidget(self.checkbox_c)
        layout_label.addWidget(self.label_c_4)

        layout_link = QHBoxLayout()
        layout_link.addWidget(self.checkbox_link)
        layout_link.addWidget(self.label_link_type)
        layout_link2 = QHBoxLayout()
        layout_link2.addWidget(self.link_combobox)
        layout_link2.addWidget(self.label_link_id)
        layout_link2.addWidget(self.line_edit_link)

        self.gridLayout_v = QGridLayout()
        self.gridLayout_v.addWidget(self.label_c_1, 0, 0)
        self.gridLayout_v.addWidget(self.combobox_c, 0, 1)
        self.gridLayout_v.addWidget(self.tips, 1, 1)
        self.gridLayout_v.addWidget(self.label_c_2, 2, 0)
        self.gridLayout_v.addWidget(self.line_edit, 2, 1)
        self.gridLayout_v.addWidget(self.label_c_3, 3, 0)
        self.gridLayout_v.addWidget(self.text_edit_c1, 3, 1)
        self.gridLayout_v.addLayout(layout_link, 4, 0)
        self.gridLayout_v.addLayout(layout_link2, 4, 1)
        self.gridLayout_v.addLayout(layout_label, 5, 0)
        self.gridLayout_v.addWidget(self.line_edit_file, 5, 1)
        self.gridLayout_v.addWidget(self.label_c_5, 6, 0)
        self.gridLayout_v.addWidget(self.examiners_combobox, 6, 1)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.submit_pb)
        layout_1.addWidget(self.close_pb)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout_v)
        main_lay.addLayout(layout_1)
        self.setLayout(main_lay)

        self.submit_pb.setDisabled(False)
        self.link_combobox.setDisabled(True)
        self.line_edit_link.setDisabled(True)
        self.close_pb.clicked.connect(self.close)
        self.checkbox_c.stateChanged.connect(self.show_path)
        self.checkbox_link.stateChanged.connect(self.show_link)
        self.line_edit_file.setDisabled(True)
        self.combobox_c.textChanged.connect(self.set_label)

    @property
    def folder_path(self):
        # 返回当前文件路径
        return self.line_edit_file.text().replace('\\', '/')

    @property
    def describe_text(self):
        return self.text_edit_c1.toPlainText()

    @property
    def ticket_type_text(self):
        return self.combobox_c.currentText()

    @property
    def title_text(self):
        return self.line_edit.text()

    @property
    def link_type(self):
        return self.link_combobox.currentText()

    @property
    def type_id(self):
        return self.line_edit_link.text()

    def set_label(self):
        if self.ticket_type_text == u"工具开发":
            self.tips.show()
            self.tips.setText(u"注意：工具开发工单将会抄送给刘总，请详细填写工单描述")
        else:
            self.tips.hide()

    def show_path(self):
        if self.checkbox_c.isChecked():
            self.line_edit_file.setDisabled(False)
        else:
            self.line_edit_file.setDisabled(True)

    def show_link(self):
        if self.checkbox_link.isChecked():
            self.link_combobox.setDisabled(False)
            self.line_edit_link.setDisabled(False)
        else:
            self.link_combobox.setDisabled(True)
            self.line_edit_link.setDisabled(True)

    def get_group_name(self):
        code_info_list = sg.find_shotgun("Group", [['sg_permission_group', 'in', ['admin', 'supervisor', 'producer']]
                                                   ],
                                         ["code"], [{'field_name': 'sg_login', 'direction': 'asc'}])
        code_name_list = []
        for code_info in code_info_list:
            code_name_list.append(code_info["code"])
        return code_name_list


class CreateNoteUI(QDialog, MFieldMixin):
    def __init__(self, parent=None):
        super(CreateNoteUI, self).__init__(parent)
        self.setWindowTitle(u'提交反馈')
        self.examine_info = {}
        self.resize(430, 460)
        self.label_n_1 = MLabel(u"*收件人:")
        self.label_n_1.setMinimumWidth(70)
        self.line_edit_n = MLineEdit().small()
        self.label_n_2 = MLabel(u"*主题:")
        self.label_n_2.setMinimumWidth(70)
        self.line_edit_n2 = MLineEdit().small()
        self.label_n_3 = MLabel(u"*正文:")
        self.label_n_3.setMinimumWidth(70)
        self.text_edit_n1 = MTextEdit()

        self.label_time = MLabel(u"*用时:")
        self.label_time.setMinimumWidth(70)
        self.spin_time = spin_box.MSpinBox()
        self.spin_time.setMaximum(999999)
        layout_time = QHBoxLayout()
        layout_time.addWidget(self.label_time)
        layout_time.addWidget(self.spin_time)

        self.checkbox_n = MCheckBox("")
        self.label_n_4 = MLabel(u"附件:")
        self.label_n_4.setMinimumWidth(48)
        self.note_file = MLineEdit().folder().small()
        self.note_file.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.submit_note_pb = MPushButton(u'提交').primary().small()
        self.close_button = MPushButton(u'关闭').primary().small()

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.submit_note_pb)
        layout_button.addWidget(self.close_button)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.checkbox_n)
        layout_1.addWidget(self.label_n_4)

        self.gridLayout_v = QGridLayout()
        self.gridLayout_v.addWidget(self.label_n_1, 0, 0)
        self.gridLayout_v.addWidget(self.line_edit_n, 0, 1)
        self.gridLayout_v.addWidget(self.label_n_2, 1, 0)
        self.gridLayout_v.addWidget(self.line_edit_n2, 1, 1)
        self.gridLayout_v.addWidget(self.label_n_3, 2, 0)
        self.gridLayout_v.addWidget(self.text_edit_n1, 2, 1)
        self.gridLayout_v.addWidget(self.label_time, 3, 0)
        self.gridLayout_v.addWidget(self.spin_time, 3, 1)
        self.gridLayout_v.addLayout(layout_1, 4, 0)
        self.gridLayout_v.addWidget(self.note_file, 4, 1)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout_v)
        main_lay.addLayout(layout_button)
        self.setLayout(main_lay)
        self.close_button.clicked.connect(self.close)
        self.line_edit_n.setText(self.parent().proposer)
        self.line_edit_n.setReadOnly(True)
        self.checkbox_n.stateChanged.connect(self.show_path)
        self.note_file.setDisabled(True)
        self.submit_note_pb.clicked.connect(self.create_note)


    def show_path(self):
        if self.checkbox_n.isChecked():
            self.note_file.setDisabled(False)
        else:
            self.note_file.setDisabled(True)

    @property
    def addressing(self):
        return self.line_edit_n.text()

    @property
    def title_text(self):
        return self.line_edit_n2.text()

    @property
    def content_text(self):
        return self.text_edit_n1.toPlainText()

    @property
    def folder_path(self):
        # 返回当前文件路径
        return self.note_file.text().replace('\\', '/')

    def create_note(self):
        self.submit_note_pb.setText(u"正在提交...")
        self.submit_note_pb.setDisabled(True)
        attachments_list = []
        if self.checkbox_n.isChecked():
            if not os.path.exists(self.folder_path):
                MMessage.config(2)
                MMessage.warning(u'请先选择正确的附件文件', parent=self.parent().parent())
                self.submit_note_pb.setText(u"提交")
                self.submit_note_pb.setDisabled(False)
                return
        if self.folder_path:
            for root, dirs, files in os.walk(self.folder_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    attachments_list.append(file_path)
            # big_size_file = check_file_size(attachments_list)
            # if big_size_file:
            #     MMessage.config(2)
            #     MMessage.warning(u'请检查附件大小不要超过500MB!', parent=self.parent().parent())
            #     return
        if not self.title_text or not self.content_text or not self.spin_time.value() > 0:
            MMessage.config(2)
            MMessage.warning(u'请先填写必填内容', parent=self.parent().parent())
            self.submit_note_pb.setText(u"提交")
            self.submit_note_pb.setDisabled(False)
            return

        addressing_id_list = []
        if self.addressing:
            addressing_id = sg.find_one_shotgun('Group', [['code', 'is', self.addressing]], ['id', 'code'])
            addressing_id_list.append(addressing_id)
        note_data = {
            "project": self.parent().project_id,
            "subject": u'工单回复：'+self.title_text,
            "sg_proposer": self.parent().user_name_id,
            "addressings_to": addressing_id_list,
            "content": self.content_text,
            "sg_status_list": "opn",
            "sg_if_read": False,
        }
        note = sg.create_shotgun("Note", note_data)
        note_id = note["id"]
        note_subject = note["subject"]
        note_file_list = []
        note_file_id_list = []
        for file_path in attachments_list:
            file_name = os.path.split(file_path)[-1]
            note_file_list.append(file_name)
            note_file_id = sg.upload_shotgun("Note", note_id, file_path, field_name="attachments",
                                             display_name=file_name)
            note_file_id_list.append(note_file_id)
        link_notes_list = sg.find_one_shotgun("Ticket", [["id", "is", int(self.parent().ticket_id)]],
                                              ["sg_examine_notes"])["sg_examine_notes"]
        examine_notes = {u"id": note_id, u"name": note_subject, u"type": u'Note'}
        link_notes_list.append(examine_notes)
        data_ticket = {"sg_examine_notes": link_notes_list}
        sg.update_shotgun("Ticket", int(self.parent().ticket_id), data_ticket)
        update_ticket_status(self.parent().project_name, int(self.parent().ticket_id))
        self.examine_info = {"id": note_id, "examiners": self.parent().user_name_code, "describe": self.title_text,
                             "file_name": note_file_list, "file_id": note_file_id_list}
        MMessage.config(2)
        MMessage.success(u'提交反馈成功!', parent=self.parent().parent())
        self.parent().append_data(self.examine_info)
        self.parent().parent().refresh_ticket()
        self.submit_note_pb.setText(u"提交")
        self.submit_note_pb.setDisabled(False)

        # 创建timelog
        link_note = sg.find_one_shotgun("Ticket", [["id", "is", int(self.parent().ticket_id)]], [])
        pro_filters = [['name', 'is', self.parent().project_name]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)

        log_dict = {"entity": link_note, "description": self.content_text, "duration": self.spin_time.value(), "sg_group": self.parent().user_name_id, "project": pro_sg}
        sg.create_shotgun("TimeLog", log_dict)

        self.close()


class ViewTicketUI(QDialog):
    def __init__(self, ticket_id="", proposer="", parent=None):
        super(ViewTicketUI, self).__init__(parent)
        self.setWindowTitle(u'查看工单反馈')
        self.ticket_id = ticket_id
        self.proposer = proposer
        self.user_name_code = self.parent().user_name_code
        self.user_name_id = self.parent().user_name_id
        self.project_name = self.parent().project
        self.project_id = self.parent().project_id
        self.resize(730, 420)
        self.label_v_1 = MLabel(u"工单类别:")
        self.label_v_1.setMinimumWidth(70)
        self.line_edit_v1 = MLineEdit().small()
        self.label_v_2 = MLabel(u"工单标题:")
        self.label_v_2.setMinimumWidth(70)
        self.line_edit_v2 = MLineEdit().small()
        self.label_v_3 = MLabel(u"工单描述:")
        self.label_v_3.setMinimumWidth(70)
        self.text_edit_v1 = MTextEdit()
        self.label_c_4 = MLabel(u"附件:")
        self.label_c_4.setMinimumWidth(70)
        self.dir_path_le = MLineEdit().folder().small()
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.submit_pb_v1 = MPushButton(u'下载', MIcon('down_fill.svg')).small()
        self.submit_pb_v1.setDisabled(False)
        self.divider = MDivider().vertical()

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
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.button_note = MPushButton(u'创建反馈').primary().small()
        self.splitter.hide()
        self.button_note.hide()
        self.label_file = MLabel(u"附件:")
        self.label_file.setMinimumWidth(70)
        self.down_path_le = MLineEdit().folder().small()
        self.down_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.submit_pb_v2 = MPushButton(u'下载', MIcon('down_fill.svg')).small()
        self.submit_pb_v2.setDisabled(False)

        self.layout_1 = QHBoxLayout()
        self.layout_1.addWidget(self.dir_path_le)
        self.layout_1.addWidget(self.submit_pb_v1)
        self.layout_2 = QHBoxLayout()
        self.layout_2.addWidget(self.label_file)
        self.layout_2.addWidget(self.down_path_le)
        self.layout_2.addWidget(self.submit_pb_v2)

        self.layout_3 = QHBoxLayout()
        self.layout_3.addWidget(self.button_note)
        self.layout_3.addWidget(self.splitter)

        self.gridLayout_v = QGridLayout()
        self.gridLayout_v.addWidget(self.label_v_1, 0, 0)
        self.gridLayout_v.addWidget(self.line_edit_v1, 0, 1)
        self.gridLayout_v.addWidget(self.label_v_2, 1, 0)
        self.gridLayout_v.addWidget(self.line_edit_v2, 1, 1)
        self.gridLayout_v.addWidget(self.label_v_3, 2, 0)
        self.gridLayout_v.addWidget(self.text_edit_v1, 2, 1)
        self.gridLayout_v.addWidget(self.label_c_4, 3, 0)
        self.gridLayout_v.addLayout(self.layout_1, 3, 1)

        self.gridLayout_v1 = QGridLayout()
        self.gridLayout_v1.addWidget(self.data_table, 0, 0)
        self.gridLayout_v1.addLayout(self.layout_2, 1, 0)

        layout_v1 = QVBoxLayout()
        layout_v1.addWidget(MDivider(u"工单详情"))
        layout_v1.addLayout(self.gridLayout_v)

        layout_v2 = QVBoxLayout()
        layout_v2.addWidget(MDivider(u"反馈详情"))
        layout_v2.addLayout(self.layout_3)
        layout_v2.addLayout(self.gridLayout_v1)

        main_lay = QHBoxLayout()
        main_lay.addLayout(layout_v1)
        main_lay.addWidget(self.divider)
        main_lay.addLayout(layout_v2)
        self.setLayout(main_lay)
        self.set_header(table_header)
        self.set_data([])
        self.submit_pb_v2.clicked.connect(self.download_note_file)
        self.submit_pb_v1.clicked.connect(self.download_ticket_file)
        self.fetching_note_thread = DownloadUrlFile()
        self.fetching_note_thread.progress.connect(self.get_data)
        self.fetching_note_thread.finished.connect(self.finish_fetch_data)
        self.button_note.clicked.connect(self.show_create_note)

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

    def append_data(self, data_dict):
        # 增加一条数据
        self.data_model.append(data_dict)

    @property
    def folder_note_path(self):
        # 返回当前文件路径
        return self.down_path_le.text().replace('\\', '/')

    @property
    def folder_ticket_path(self):
        # 返回当前文件路径
        return self.dir_path_le.text().replace('\\', '/')

    def download_ticket_file(self):
        self.submit_pb_v1.setText(u"正在下载...")
        self.submit_pb_v1.setDisabled(True)
        down_ticket_info = {}
        if not self.folder_ticket_path:
            MMessage.config(2)
            MMessage.warning(u'请先选择存放文件的路径！', parent=self.parent())
            self.submit_pb_v1.setText(u"下载")
            self.submit_pb_v1.setDisabled(False)
            return
        id_list = self.get_attachments_id()
        if not id_list:
            MMessage.config(2)
            MMessage.warning(u'没有附件可以下载！', parent=self.parent())
            self.submit_pb_v1.setText(u"下载")
            self.submit_pb_v1.setDisabled(False)
            return
        down_ticket_info[self.folder_ticket_path] = id_list
        self.fetching_note_thread.attachments_dict = down_ticket_info
        self.fetching_note_thread.start()

    def get_attachments_id(self):
        attachments_list = sg.find_one_shotgun("Ticket", [["id", "is", int(self.ticket_id)]], ["attachments"])["attachments"]
        if attachments_list:
            id_list = []
            for attachment in attachments_list:
                id_list.append(attachment["id"])
        return id_list

    def download_note_file(self):
        self.submit_pb_v2.setText(u"正在下载...")
        self.submit_pb_v2.setDisabled(True)
        down_info = {}
        file_id_list = []
        if not self.folder_note_path:
            MMessage.config(2)
            MMessage.warning(u'请先选择存放文件的路径！', parent=self.parent())
            self.submit_pb_v2.setText(u"下载")
            self.submit_pb_v2.setDisabled(False)
            return
        indexes = self.data_table.selectedIndexes()
        if not indexes:
            MMessage.config(2)
            MMessage.warning(u'没有可以下载的文件！', parent=self.parent())
            self.submit_pb_v2.setText(u"下载")
            self.submit_pb_v2.setDisabled(False)
            return
        rows = list(set([index.row() for index in indexes]))
        for r in rows:
            file_id = self.data_model.index(r, 4).data()
            for i in file_id.split(","):
                file_id_list.append(int(i))
        down_info[self.folder_note_path] = file_id_list
        self.fetching_note_thread.attachments_dict = down_info
        self.fetching_note_thread.start()

    def get_data(self, data):
        pass

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_note_thread.wait()
            self.fetching_note_thread.quit()
            self.submit_pb_v2.setText(u"下载")
            self.submit_pb_v2.setDisabled(False)
            self.submit_pb_v1.setText(u"下载")
            self.submit_pb_v1.setDisabled(False)

    def show_create_note(self):
        create_note_win = CreateNoteUI(parent=self)
        create_note_win.show()


class AssignmentTask(QDialog, MFieldMixin):
    def __init__(self, ticket_info="", parent=None):
        super(AssignmentTask, self).__init__(parent)
        self.setWindowTitle(u'分配任务')
        self.select_people_list = []
        self.select_project = ""
        self.ticket_info = ticket_info
        all_projects = shotgun_operations.find_shotgun('Project', [['sg_status', 'is', 'active']], ['name'])
        all_projects_names = [p['name'] for p in all_projects]
        # self.project_list = [self.ticket_info["project"], "OCT MNG"]
        self.project_list = all_projects_names
        self.resize(500, 250)
        self.label_people = MLabel(u"分配:")
        self.checkbox_group_b = MCheckBoxGroup()
        self.checkbox_group_b.sig_checked_changed.connect(self.get_select_people)

        self.label_project = MLabel(u"项目:")
        self.radio_group_project = MRadioButtonGroup()
        self.radio_group_project.set_button_list(self.project_list)
        self.radio_group_project.sig_checked_changed.connect(self.get_project)
        self.radio_group_project.set_dayu_checked(0)

        self.label_keyword = MLabel(u"关键字:")
        self.register_field('button1_selected', [u'其他'])
        menu2 = MMenu()
        menu2.set_data(get_ticket_type("sg_key_words"))
        self.keyword_combobox = MComboBox()
        self.keyword_combobox.set_menu(menu2)
        self.bind('button1_selected', self.keyword_combobox, 'value', signal='sig_value_changed')
        self.keyword_combobox.lineEdit().setReadOnly(False)

        self.submit_note_pb = MPushButton(u'提交').primary().small()
        self.close_button = MPushButton(u'关闭').primary().small()

        self.gridLayout_a = QGridLayout()
        self.gridLayout_a.addWidget(self.label_people, 0, 0)
        self.gridLayout_a.addWidget(self.checkbox_group_b, 0, 1)
        self.gridLayout_a.addWidget(self.label_project, 1, 0)
        self.gridLayout_a.addWidget(self.radio_group_project, 1, 1)
        self.gridLayout_a.addWidget(self.label_keyword, 2, 0)
        self.gridLayout_a.addWidget(self.keyword_combobox, 2, 1)

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.submit_note_pb)
        layout_button.addWidget(self.close_button)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout_a )
        # main_lay.addWidget(self.radio_group_project)
        main_lay.addLayout(layout_button)
        self.setLayout(main_lay)
        admin_people_name, code_info_list = self.get_admin_people()
        self.data_list = admin_people_name
        self.checkbox_group_b.set_button_list(self.data_list)

        self.admin_people_info = code_info_list
        self.submit_note_pb.clicked.connect(self.assignment_task)
        self.close_button.clicked.connect(self.close)

    @staticmethod
    def get_admin_people():
        admin_people_name = []
        code_info_list = sg.find_shotgun("Group", [['sg_permission_group', 'in', ['admin']]],
                                         ["code"], [{'field_name': 'sg_login', 'direction': 'asc'}])
        for code in code_info_list:
            if code["id"] != 63:  # 把TD组过滤掉
                admin_people_name.append(code["code"])
        return admin_people_name, code_info_list

    def get_keyword(self):
        return self.keyword_combobox.currentText()

    def get_project(self, data):
        self.select_project = self.project_list[data]

    def get_select_people(self, data):
        self.select_people_list = data

    def assignment_task(self):
        self.submit_note_pb.setText(u"正在提交")
        self.submit_note_pb.setDisabled(True)
        people_info_list = []
        batch_data = []
        people_id = {}
        # project_info = sg.find_one_shotgun('Project', [['name', 'is', self.ticket_info["project"]]], ['id'])
        user_name_id = sg.find_one_shotgun("Group", [["sg_login", "is", self.ticket_info["user"]]], ["id", "code"])
        for name in self.admin_people_info:
            people_id[name["id"]] = name["code"]
        for name in self.select_people_list:
            for k, v in people_id.items():
                if v == name:
                    name_id = k
                    break
                else:
                    name_id = None
            if name_id:
                people_info = {"id": name_id, "type": "Group"}
                people_info_list.append(people_info)
            else:
                MMessage.config(2)
                MMessage.warning(u'不存在该人员', parent=self)
        keyword = self.get_keyword()
        project_info = sg.find_one_shotgun('Project', [['name', 'is', self.select_project]], ['id'])
        ticket_data = {"sg_examiners": people_info_list, "project": project_info, "sg_key_words": keyword}
        for ticket_id in self.ticket_info["id"]:
            link_ticket_id = {"id": ticket_id, "type": "Ticket"}
            batch_data.append({"request_type": "update", "entity_type": "Ticket",
                               "entity_id": ticket_id, "data": ticket_data})
            ticket_info = sg.find_one_shotgun('Ticket', [['id', 'is', ticket_id]],
                                                         ['title', "description"])
            ticket_title = ticket_info["title"]
            ticket_desc = ticket_info["description"]
            for addressings_info in people_info_list:
                note_data = {
                    "project": project_info,
                    "subject": u'任务分配：'+ticket_title,
                    "sg_proposer": user_name_id,
                    "content": ticket_desc,
                    "addressings_to": [addressings_info],
                    "note_links": [link_ticket_id],
                    "sg_status_list": "opn",
                    "sg_if_read": False,
                }
                batch_data.append({"request_type": "create", "entity_type": "Note", "data": note_data})
        sg.batch_shotgun(batch_data)
        self.submit_note_pb.setText(u"提交完成")
        MMessage.config(2)
        MMessage.warning(u'提交完成', parent=self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    test = AssignmentTask()
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


def update_ticket_status(project_name, ticket_id):
    ticket_examiners_list = []
    notes_id_list = []
    note_examiners_list = []
    ticket_list = sg.find_one_shotgun("Ticket", [['id', "is", ticket_id]],
                                      ["sg_examine_notes", "sg_examiners"])
    for note_info in ticket_list["sg_examine_notes"]:
        if note_info["id"] not in notes_id_list:
            notes_id_list.append(note_info["id"])
    for examiner in ticket_list["sg_examiners"]:
        if examiner["name"] not in ticket_examiners_list:
            ticket_examiners_list.append(examiner["name"])
    if notes_id_list:
        note_info_list = sg.find_shotgun("Note", [["id", "in", notes_id_list]], ["id", "sg_proposer"])
        for note_info in note_info_list:
            if note_info["sg_proposer"]["name"] not in note_examiners_list:
                note_examiners_list.append(note_info["sg_proposer"]["name"])
    if len(ticket_examiners_list) == len(note_examiners_list):
        data = {"sg_status_list": "res", 'sg_due_date': datetime.datetime.now()}
        sg.update_shotgun("Ticket", ticket_id, data)


def get_examiners_type(project_name, user_name):
    ticket_list = sg.find_shotgun("Ticket", [["sg_examiners", "name_contains", user_name],
                                             # ['sg_status_list', 'is_not', 'rev']
                                             ],
                                  ["sg_examine_notes", "sg_status_list"])
    no_notes_ticket_list = []#没有审核过的id列表
    notes_ticket_list = []#已经审核过的id列表
    for notes_list in ticket_list:
        if notes_list["sg_status_list"] == "res":
            notes_ticket_list.append(notes_list["id"])
        else:
            notes_id_list = []
            for notes in notes_list["sg_examine_notes"]:
                notes_id_list.append(notes["id"])
            if notes_id_list:
                note_info = sg.find_shotgun("Note", [["id", "in", notes_id_list],
                                                     ["sg_proposer", "name_is", user_name]], ["id"])
            else:
                note_info = []
            if not note_info:
                no_notes_ticket_list.append(notes_list["id"])
            else:
                notes_ticket_list.append(notes_list["id"])
    return notes_ticket_list, no_notes_ticket_list


def get_notes(ticket_id, project_name, user_name):
    # my_note = False
    notes_list = sg.find_one_shotgun("Ticket", [["id", "is", ticket_id]],
                                     ["sg_examine_notes"])["sg_examine_notes"]
    notes_id_list = []
    table_data_list = []
    for notes in notes_list:
        notes_id_list.append(notes["id"])
    if notes_id_list:
        notes_info_list = sg.find_shotgun("Note", [["id", "in", notes_id_list]],
                                          ["subject", "sg_proposer", "attachments", "id"])
        for notes_info in notes_info_list:
            file_name_list = []
            file_id_list = []
            if notes_info["attachments"]:
                for attachment in notes_info["attachments"]:
                    file_name_list.append(attachment["name"])
                    file_id_list.append(attachment["id"])
            else:
                file_name_list = ""
                file_id_list = ""
            # if user_name == notes_info["sg_proposer"]["name"]:
            #     my_note = True
            table_data_dict = {"id": notes_info["id"],
                               "examiners": notes_info["sg_proposer"]["name"],
                               "describe": notes_info["subject"],
                               "file_name": file_name_list,
                               "file_id": file_id_list}
            table_data_list.append(table_data_dict)
    # return table_data_list, my_note
    return table_data_list


def check_file_size(file_path_list):
    big_size = []
    for file_path in file_path_list:
        f_size = os.path.getsize(file_path)
        f_size = f_size/float(1024 * 1024)
        if round(f_size, 2) > 50:
            big_size.append(file_path)
    return big_size

