#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.label import MLabel
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.push_button import MPushButton
from dayu_widgets.menu import MMenu
from dayu_widgets.qt import *
from utils import shotgun_operations
from dayu_widgets.field_mixin import MFieldMixin
sg = shotgun_operations
from dayu_widgets.message import MMessage

class CreateMessageUI(QDialog, MFieldMixin):
    def __init__(self, parent=None):
        super(CreateMessageUI, self).__init__(parent)
        self.resize(520, 490)
        self.setWindowTitle(u'创建消息')

        self.gridLayout = QGridLayout()
        self.label_title = MLabel(u" 消息标题:")
        self.gridLayout.addWidget(self.label_title, 0, 0)
        self.label_title.setMinimumWidth(70)
        self.line_edit_title = MLineEdit()
        self.gridLayout.addWidget(self.line_edit_title, 0, 1)

        self.label_message = MLabel(u" 消息内容:")
        self.gridLayout.addWidget(self.label_message, 2, 0)
        self.label_message.setMinimumWidth(70)
        self.text_edit_message = MTextEdit(u'')
        self.gridLayout.addWidget(self.text_edit_message, 2, 1)

        self.label_people = MLabel(u" 发送人员:")
        self.gridLayout.addWidget(self.label_people, 3, 0)
        self.label_people.setMinimumWidth(48)
        code_name_list = self.get_group_name()
        self.register_field('button2_selected', [])
        menu2 = MMenu(exclusive=False)
        menu2.set_data(code_name_list)
        self.examiners_combobox = MComboBox()
        self.gridLayout.addWidget(self.examiners_combobox, 3, 1)
        self.examiners_combobox.set_menu(menu2)
        self.bind('button2_selected', self.examiners_combobox, 'value', signal='sig_value_changed')

        layout_1 = QHBoxLayout()
        self.submit_pb = MPushButton(u'提交').small()
        layout_1.addWidget(self.submit_pb)
        self.close_pb = MPushButton(u'关闭').small()
        layout_1.addWidget(self.close_pb)


        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout)
        main_lay.addLayout(layout_1)
        self.setLayout(main_lay)

        self.submit_pb.setDisabled(False)
        self.close_pb.clicked.connect(self.close)
        self.submit_pb.clicked.connect(self.create_ticket_task)

        self.project = parent.project
        self.user_name = parent.user
        self.project_id = sg.find_one_shotgun('Project', [['name', 'is', self.project]], ['id'])
        self.user_name_id = sg.find_one_shotgun("Group", [["sg_login", "is", self.user_name]], ["id", "code"])


    def get_group_name(self):
        code_info_list = sg.find_shotgun("Group", [['sg_permission_group', 'in', ['admin', 'supervisor', 'producer']]
                                                   ],
                                         ["code"], [{'field_name': 'sg_login', 'direction': 'asc'}])
        code_name_list = []
        for code_info in code_info_list:
            code_name_list.append(code_info["code"])
        return code_name_list

    def create_ticket_task(self):
        self.submit_pb.setText(u"正在提交...")
        self.submit_pb.setDisabled(True)

        title_message = self.line_edit_title.text()
        content_message = self.text_edit_message.toPlainText()
        send_people_list = self.examiners_combobox.currentText().split(",")
        for send_people in send_people_list:
            note_dict = dict()
            note_dict["project"] = self.project_id
            note_dict["subject"] = u"{}给你发送了一条消息:\n{}".format(self.user_name_id['code'], title_message)
            note_dict["sg_proposer"] = self.user_name_id
            note_dict["content"] = u"%s" % content_message
            note_dict["addressings_to"] = [sg.find_one_shotgun("Group", [["code", "is", send_people]], ["id", "code"])]
            note_dict["sg_if_read"] = False
            sg.create_shotgun("Note", note_dict)
        MMessage.config(2)
        MMessage.success(u'发送消息成功!', parent=self)
        self.submit_pb.setDisabled(False)
        self.submit_pb.setText(u"提交")