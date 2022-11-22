#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import os
import sys
from dayu_widgets.message import MMessage
from dayu_widgets.line_edit import MLineEdit
from SystemTools.Autumn.gui import autumn_page
from dayu_widgets.label import MLabel
from dayu_widgets.line_tab_widget import MLineTabWidget
from dayu_widgets.tab_widget import MTabWidget
from dayu_widgets.qt import *
from utils import shotgun_operations
from dayu_widgets.tool_button import MToolButton
from pprint import pprint
sg = shotgun_operations
# sys.path.append(os.path.abspath(os.path.dirname(__file__)).replace("\\", "/"))
import ticket_function
reload(ticket_function)
import ticket_global
reload(ticket_global)


class TicketMainUI(QDialog):
    def __init__(self, parent=None):
        super(TicketMainUI, self).__init__(parent)
        self.resize(1000, 700)
        self.setWindowTitle(u'提交工单工具 v2019.10.18')
        self.project = ""
        self.user_name = ""
        self.project_id = ""
        self.user_name_id = ""
        self.user_name_code = ""
        self.pages = []
        self.page_names = []
        self._init_ui()

    def _init_ui(self):
        if not os.environ['oct_launcher_using_mode'] in ['online']:
            return
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.create_button = MToolButton().svg('add_line.svg').icon_only()
        self.refresh_bp = MToolButton().svg('refresh_line.svg').icon_only()
        self.create_button.setMaximumWidth(45)
        self.refresh_bp.setMaximumWidth(45)
        self.tab_card = MTabWidget()
        #全部工单的布局
        self.all_ticket_widget = QWidget()
        self.label = MLabel(u"搜索:")
        self.search_line_edit = MLineEdit().search().small()
        self.search_line_edit.setMaximumWidth(170)
        self.splitter_1 = QSplitter()
        self.splitter_1.setOrientation(Qt.Horizontal)
        self.all_tab_center = MLineTabWidget()
        self.gridLayout_1 = QGridLayout(self.all_ticket_widget)
        layout_all = QHBoxLayout()
        layout_all.addWidget(self.label)
        layout_all.addWidget(self.search_line_edit)
        layout_all.addWidget(self.splitter_1)
        layout_all_1 = QVBoxLayout()
        layout_all_1.addLayout(layout_all)
        layout_all_1.addWidget(self.all_tab_center)
        self.gridLayout_1.addLayout(layout_all_1, 0, 0, 1, 1)

        # 我的工单的布局
        self.my_ticket_widget = QWidget()
        self.my_label = MLabel(u"搜索:")
        self.search_line_edit2 = MLineEdit().search().small()
        self.search_line_edit2.setMaximumWidth(170)
        self.splitter_2 = QSplitter()
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.my_tab_center = MLineTabWidget()
        self.gridLayout_2 = QGridLayout(self.my_ticket_widget)
        my_layout_all = QHBoxLayout()
        my_layout_all.addWidget(self.my_label)
        my_layout_all.addWidget(self.search_line_edit2)
        my_layout_all.addWidget(self.splitter_2)
        my_layout_all_1 = QVBoxLayout()
        my_layout_all_1.addLayout(my_layout_all)
        my_layout_all_1.addWidget(self.my_tab_center)
        self.gridLayout_2.addLayout(my_layout_all_1, 0, 0, 1, 1)

        # 我的审核的布局
        self.my_examine_widget = QWidget()
        self.examine_label = MLabel(u"搜索:")
        self.search_line_edit3 = MLineEdit().search().small()
        self.search_line_edit3.setMaximumWidth(170)
        self.splitter_3 = QSplitter()
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.examine_tab_center = MLineTabWidget()
        self.gridLayout_3 = QGridLayout(self.my_examine_widget)
        examine_layout_1 = QHBoxLayout()
        examine_layout_1.addWidget(self.examine_label)
        examine_layout_1.addWidget(self.search_line_edit3)
        examine_layout_1.addWidget(self.splitter_3)
        examine_layout_2 = QVBoxLayout()
        examine_layout_2.addLayout(examine_layout_1)
        examine_layout_2.addWidget(self.examine_tab_center)
        self.gridLayout_3.addLayout(examine_layout_2, 0, 0, 1, 1)

        my_layout_all_2 = QHBoxLayout()
        my_layout_all_2.addWidget(self.create_button)
        my_layout_all_2.addWidget(self.refresh_bp)
        my_layout_all_2.addWidget(self.splitter)

        self.tab_card.addTab(self.all_ticket_widget, u'全部工单')
        self.tab_card.addTab(self.my_ticket_widget, u'我的工单')
        self.tab_card.addTab(self.my_examine_widget, u'我的审核')

        main_lay = QVBoxLayout()
        main_lay.addLayout(my_layout_all_2)
        main_lay.addWidget(self.tab_card)
        self.setLayout(main_lay)
        self.project = sg.get_project()
        self.user_name = sg.get_user()
        self.project_id = sg.find_one_shotgun('Project', [['name', 'is', self.project]], ['id'])
        self.user_name_id = sg.find_one_shotgun("Group", [["sg_login", "is", self.user_name]], ["id", "code"])
        self.user_name_code = self.user_name_id["code"]
        self.create_button.clicked.connect(self.create_ticket)
        self.refresh_bp.clicked.connect(self.refresh_ticket)
        self.tab_card.currentChanged.connect(self.set_my_ticket_page)
        self.set_page_add()

    def set_page_add(self):
        if not self.user_name_code:
            return
        all_ticket_complete, all_ticket_unfinished, my_ticket_complete, \
            my_ticket_unfinished = ticket_global.get_ticket_config(self.user_name)
        self.add_page(self.get_config_data(all_ticket_complete), "all")
        self.add_page(self.get_config_data(all_ticket_unfinished), "all")
        self.add_page(self.get_config_data(my_ticket_complete), "my")
        self.add_page(self.get_config_data(my_ticket_unfinished), "my")
        my_examine_complete, my_examine_unfinished = \
            ticket_global.get_examine_config(self.project, self.user_name_code)
        self.add_page(self.get_config_data(my_examine_complete))
        self.add_page(self.get_config_data(my_examine_unfinished))

    @staticmethod
    def get_config_data(config_data):
        config = {"page_actions": [{'label': u'编辑日志', 'value': 'edit_ticket_log', 'icon': 'success_line.svg', 'mode': '1',},
                                   {'label': u'分配任务', 'value': 'assignment_task', 'icon': 'success_line.svg', 'mode': '1',}],
                  "page_fields": [{u"label": u"提出者", u"key": "sg_proposer", 'searchable': 1},
                                  {u"label": u"分配给", u"key": "sg_examiners", 'searchable': 1},
                                  {u"label": u"工单类型", u"key": "sg_ticket_type", 'searchable': 1},
                                  {u"label": u"工单标题", u"key": "title", 'searchable': 1},
                                  {u"label": u"工单描述", u"key": "description", 'searchable': 1},
                                  {u"label": u"状态", u"key": "sg_status_list", 'searchable': 1},
                                  {u"label": u"用时", u"key": "time_logs_sum", 'searchable': 1},
                                  {u"label": u"附件", u"key": "attachments"},
                                  {u"label": u"提交时间", u"key": "created_at", 'searchable': 1},
                                  {u"label": u"完成时间", u"key": "sg_due_date", 'searchable': 1},
                                  {u"label": u"项目", u"key": "project", 'searchable': 1},
                                  ],
                  "page_filters": config_data["filters"],
                  "page_name": config_data["page_title"],
                  "page_type": "Ticket",
                  "page_svg": config_data["page_icon"],
                  "page_order": [{'field_name': 'updated_at', 'direction': 'desc'}]}
        return config

    def create_ticket(self):
        create_ticket_win = ticket_function.CreateTicketUI(parent=self)
        create_ticket_win.show()
        create_ticket_win.submit_pb.clicked.connect(lambda: self.create_ticket_task(create_ticket_win))

    def create_ticket_task(self, create_win):
        create_win.submit_pb.setText(u"正在提交...")
        create_win.submit_pb.setDisabled(True)
        attachments_list = []
        folder_path = ""
        if create_win.checkbox_c.isChecked():
            if os.path.exists(create_win.folder_path):
                folder_path = create_win.folder_path
            else:
                MMessage.config(2)
                MMessage.warning(u'请先选择正确的附件文件', parent=self)
                create_win.submit_pb.setText(u"提交")
                create_win.submit_pb.setDisabled(False)
                return
        if folder_path:
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    attachments_list.append(file_path)
            # big_size_file = ticket_function.check_file_size(attachments_list)
            # if big_size_file:
            #     MMessage.config(2)
            #     MMessage.warning(u'请检查附件大小不要超过500MB!', parent=self)
            #     return
        if not create_win.ticket_type_text or not create_win.title_text:
            MMessage.config(2)
            MMessage.warning(u'请先填写必填内容', parent= self)
            create_win.submit_pb.setText(u"提交")
            create_win.submit_pb.setDisabled(False)
            return
        _id = create_win.type_id
        _type = create_win.link_type
        if _id and _type:
            if _type != "Group":
                find_id = sg.find_one_shotgun(_type, [['project', 'name_is', self.project],
                                                      ['id', "is", int(_id)]], ["id"])
            else:
                find_id = sg.find_one_shotgun(_type, [['sg_group_project', 'name_is', self.project],
                                                      ['id', "is", int(_id)]], ["id"])
            if not find_id:
                MMessage.config(2)
                MMessage.warning(u'请检查id编号是否正确!', parent=self)
                create_win.submit_pb.setText(u"提交")
                create_win.submit_pb.setDisabled(False)
                return
            link_dict = {u'id': int(_id), u"type": _type}
        else:
            link_dict = None
        group_name_text = create_win.examiners_combobox.currentText()
        group_name_list = []
        for group_name in group_name_text.split(","):
            group_name_list.append(group_name)
        examiners_list = sg.find_shotgun("Group", [["code", "in", group_name_list]], ["id", "code"])
        # important_human_list = [
        #                        {"type": "HumanUser", "id": 115},
        #                        {"type": "HumanUser", "id": 118},
        #                         ]
        # 刘总114, 林总115, 金爷118
        ticket_data = {
            "project": self.project_id,
            "description": create_win.describe_text,
            "sg_proposer": self.user_name_id,
            "sg_ticket_type": create_win.ticket_type_text,
            "title": create_win.title_text,
            "sg_status_list": "rev",
            # "addressings_cc": important_human_list,
            "sg_examiners": examiners_list,
            "sg_link": link_dict
        }
        ticket_id = sg.create_shotgun("Ticket", ticket_data)["id"]
        # for each in important_human_list:
        #     sg.follow_shotgun(each, {"type": "Ticket", "id": ticket_id})
        for file_path in attachments_list:
            file_name = os.path.split(file_path)[-1]
            sg.upload_shotgun("Ticket", ticket_id, file_path, field_name="attachments", display_name=file_name)
        # examiners_list.extend(important_human_list)
        if create_win.ticket_type_text == u"工具开发":
            # add_perople = [{"type": "HumanUser", "id": 114}]  # 刘总114, 林总115, 金爷118
            examiners_list.append({"type": "HumanUser", "id": 114})
        batch_data = []
        for addressee in examiners_list:
            addressee_list = [addressee]
            note_data = {
                "project": self.project_id,
                "subject": u'工单请求：'+create_win.title_text,
                "sg_proposer": self.user_name_id,
                "addressings_to": addressee_list,
                "content": create_win.describe_text,
                "sg_status_list": "opn",
                "sg_if_read": False,
            }
            batch_data.append({"request_type": "create", "entity_type": "Note", "data": note_data})
        note_info_list = sg.batch_shotgun(batch_data)
        for note_info in note_info_list:
            for file_path in attachments_list:
                file_name = os.path.split(file_path)[-1]
                sg.upload_shotgun("Note", note_info["id"], file_path, field_name="attachments",
                                  display_name=file_name)

        self.all_tab_center.stack_widget.currentWidget().parse_config()
        MMessage.config(2)
        MMessage.success(u'提交工单成功!', parent=self)
        create_win.submit_pb.setDisabled(False)
        create_win.submit_pb.setText(u"提交")
        create_win.close()

    def refresh_ticket(self):
        if self.tab_card.currentIndex() == 0:
            self.all_tab_center.stack_widget.currentWidget().parse_config()
        if self.tab_card.currentIndex() == 1:
            self.my_tab_center.stack_widget.currentWidget().parse_config()
        if self.tab_card.currentIndex() == 2:
            my_examine_complete, my_examine_unfinished = \
                ticket_global.get_examine_config(self.project, self.user_name_code)
            if self.examine_tab_center.stack_widget.currentIndex() == 0:
                config = self.get_config_data(my_examine_complete)
            else:
                config = self.get_config_data(my_examine_unfinished)
            self.examine_tab_center.stack_widget.currentWidget().set_config(config)
            self.examine_tab_center.stack_widget.currentWidget().parse_config()

    def view_ticket(self):
        if self.tab_card.currentIndex() == 0:
            table_name = self.all_tab_center.stack_widget.currentWidget()
            ticket_id, _type, title, describe, attachments, proposer = self.get_table_data(table_name)
        elif self.tab_card.currentIndex() == 1:
            table_name = self.my_tab_center.stack_widget.currentWidget()
            ticket_id, _type, title, describe, attachments, proposer = self.get_table_data(table_name)
        elif self.tab_card.currentIndex() == 2:
            table_name = self.examine_tab_center.stack_widget.currentWidget()
            ticket_id, _type, title, describe, attachments, proposer = self.get_table_data(table_name)
        view_ticket_win = ticket_function.ViewTicketUI(int(ticket_id), proposer, parent=self)
        table_data_list = ticket_function.get_notes(int(ticket_id), self.project, self.user_name_code)
        view_ticket_win.set_data(table_data_list)
        view_ticket_win.data_table.hideColumn(0)
        view_ticket_win.data_table.hideColumn(4)
        view_ticket_win.line_edit_v1.setText(_type)
        view_ticket_win.line_edit_v1.setReadOnly(True)
        view_ticket_win.line_edit_v2.setText(title)
        view_ticket_win.line_edit_v2.setReadOnly(True)
        view_ticket_win.text_edit_v1.setText(describe)
        view_ticket_win.text_edit_v1.setReadOnly(True)
        # print my_note, self.tab_card.currentIndex()
        if self.tab_card.currentIndex() == 2:
            if self.examine_tab_center.stack_widget.currentIndex() == 1:
                view_ticket_win.splitter.show()
                view_ticket_win.button_note.show()
        if attachments and attachments != "--":
            view_ticket_win.dir_path_le.setDisabled(False)
            view_ticket_win.submit_pb_v1.setDisabled(False)
        else:
            view_ticket_win.dir_path_le.setDisabled(True)
            view_ticket_win.submit_pb_v1.setDisabled(True)
        view_ticket_win.show()

    @staticmethod
    def get_table_data(table_name):
        row = table_name.table.currentIndex().row()
        ticket_id = table_name.model_sort.index(row, 0).data()
        _type = table_name.model_sort.index(row, 3).data()  # 工单类型
        title = table_name.model_sort.index(row, 4).data()  # 工单标题
        describe = table_name.model_sort.index(row, 5).data()  # 工单描述
        attachments = table_name.model_sort.index(row, 7).data()  # 附件
        proposer = table_name.model_sort.index(row, 1).data()  # 提出者
        return ticket_id, _type, title, describe, attachments, proposer

    def add_page(self, config, _type=None):
        sheet = autumn_page.SheetContent()
        sheet.table.doubleClicked.connect(self.view_ticket)
        sheet.fetch_data_thread.result_sig.connect(lambda: self.hide_column(sheet))
        sheet.show_msg = True
        if _type == "all":
            sheet.set_config(config)
            self.all_tab_center.add_tab(sheet, {'text': config['page_name'], 'svg': config['page_svg']})
            self.all_tab_center.stack_widget.currentChanged.connect(lambda: self.set_my_ticket_page(0))
            self.all_tab_center.tool_button_group.set_dayu_checked(0)
            self.set_my_ticket_page(0)
        elif _type == "my":
            sheet.set_config(config)
            self.my_tab_center.add_tab(sheet, {'text': config['page_name'], 'svg': config['page_svg']})
            self.my_tab_center.stack_widget.currentChanged.connect(lambda: self.set_my_ticket_page(1))
            self.my_tab_center.tool_button_group.set_dayu_checked(0)
        else:
            sheet.set_config(config)
            self.examine_tab_center.add_tab(sheet, {'text': config['page_name'], 'svg': config['page_svg']})
            self.examine_tab_center.stack_widget.currentChanged.connect(lambda: self.set_my_ticket_page(2))
            self.examine_tab_center.tool_button_group.set_dayu_checked(0)
        self.pages.append(sheet)
        self.page_names.append(sheet.name)
        return sheet

    @staticmethod
    def hide_column(table_name):
        table_name.table.hideColumn(0)
        # table_name.table.hideColumn(8)

    def set_my_ticket_page(self, index):
        if not self.user_name_code:
            return
        if index == 0:
            self.search_line_edit.textChanged.connect(
                self.all_tab_center.stack_widget.currentWidget().model_sort.set_search_pattern)
            if not self.all_tab_center.stack_widget.currentWidget().is_load:
                self.all_tab_center.stack_widget.currentWidget().parse_config()
                self.all_tab_center.stack_widget.currentWidget().is_load = 1
        elif index == 1:
            self.search_line_edit2.textChanged.connect(
                self.my_tab_center.stack_widget.currentWidget().model_sort.set_search_pattern)
            if not self.my_tab_center.stack_widget.currentWidget().is_load:
                self.my_tab_center.stack_widget.currentWidget().parse_config()
                self.my_tab_center.stack_widget.currentWidget().is_load = 1
        elif index == 2:
            self.search_line_edit3.textChanged.connect(
                self.examine_tab_center.stack_widget.currentWidget().model_sort.set_search_pattern)
            if not self.examine_tab_center.stack_widget.currentWidget().is_load:
                self.examine_tab_center.stack_widget.currentWidget().parse_config()
                self.examine_tab_center.stack_widget.currentWidget().is_load = 1


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    test = TicketMainUI()
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())

