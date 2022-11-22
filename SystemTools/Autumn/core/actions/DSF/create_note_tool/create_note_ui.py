#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import os
from dayu_widgets.message import MMessage
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.qt import *
from utils import shotgun_operations
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from utils import fileIO
from pprint import pprint
sg = shotgun_operations


class CreateNoteUI(QDialog, MFieldMixin):
    def __init__(self, version_info_dict="", parent=None):
        super(CreateNoteUI, self).__init__(parent)
        self.setWindowTitle(u'提交反馈')
        self.resize(500, 460)
        self.version_dict = version_info_dict
        self.project = self.version_dict["project"]
        self.user_name = self.version_dict["user"]
        # self.project = "DSF"
        # self.user_name = "huangna"
        self.artist_list, self.version_info_list = self.get_version_user()
        self.project_id = ""
        self.user_name_id = ""
        self._init_ui()

    def _init_ui(self):
        artist_people = ",".join(self.artist_list)
        self.label_n_1 = MLabel(u"收件人:")
        self.label_n_1.setMinimumWidth(70)
        self.label_people = MLabel(artist_people)
        self.label_n_2 = MLabel(u"*主题:")
        self.label_n_2.setMinimumWidth(70)
        self.line_edit_n2 = MLineEdit().small()
        self.label_n_3 = MLabel(u"*正文:")
        self.label_n_3.setMinimumWidth(70)
        self.text_edit_n1 = MTextEdit()

        self.label_p = MLabel(u"抄送:")
        self.label_p.setMinimumWidth(48)
        code_name_list = self.get_group_name()
        menu2 = MMenu(exclusive=False)
        menu2.set_data(code_name_list)
        self.examiners_combobox = MComboBox()
        self.examiners_combobox.set_menu(menu2)
        # self.bind('button2_selected', self.examiners_combobox, 'value', signal='sig_value_changed')

        self.checkbox_n = MCheckBox("")
        self.label_n_4 = MLabel(u"附件:")
        self.label_n_4.setMinimumWidth(48)
        self.note_file = MLineEdit().folder().small()
        self.note_file.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.submit_note_pb = MPushButton(u'提交').small()

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.checkbox_n)
        layout_1.addWidget(self.label_n_4)

        self.gridLayout_v = QGridLayout()
        self.gridLayout_v.addWidget(self.label_n_1, 0, 0)
        self.gridLayout_v.addWidget(self.label_people, 0, 1)
        self.gridLayout_v.addWidget(self.label_n_2, 1, 0)
        self.gridLayout_v.addWidget(self.line_edit_n2, 1, 1)
        self.gridLayout_v.addWidget(self.label_n_3, 2, 0)
        self.gridLayout_v.addWidget(self.text_edit_n1, 2, 1)
        self.gridLayout_v.addWidget(self.label_p, 3, 0)
        self.gridLayout_v.addWidget(self.examiners_combobox, 3, 1)
        self.gridLayout_v.addLayout(layout_1, 4, 0)
        self.gridLayout_v.addWidget(self.note_file, 4, 1)

        main_lay = QVBoxLayout()
        main_lay.addLayout(self.gridLayout_v)
        main_lay.addWidget(self.submit_note_pb)
        self.setLayout(main_lay)

        # self.project = sg.get_project()
        # self.user_name = sg.get_user()
        self.project_id = sg.find_one_shotgun('Project', [['name', 'is', self.project]], ['id'])
        self.user_name_id = sg.find_one_shotgun("Group", [["sg_login", "is", self.user_name]], ["id", "code"])
        self.checkbox_n.stateChanged.connect(self.show_path)
        self.note_file.setDisabled(True)
        self.submit_note_pb.clicked.connect(self.create_note)
        self.fetching_copy_thread = fileIO.CopyFile()
        self.fetching_copy_thread.finished.connect(self.finish_copy_data)
        self.fetching_oss_copy_thread = fileIO.CopyFTP()
        self.fetching_oss_copy_thread.finished.connect(self.finish_copy_oss_data)
        code_name_list = self.get_version_code()
        self.line_edit_n2.setText(' '.join(code_name_list) + u"--------版本反馈描述")

    def show_path(self):
        if self.checkbox_n.isChecked():
            self.note_file.setDisabled(False)
        else:
            self.note_file.setDisabled(True)

    @property
    def title_text(self):
        return self.line_edit_n2.text()

    @property
    def examiners_people(self):
        return self.examiners_combobox.currentText()

    @property
    def content_text(self):
        return self.text_edit_n1.toPlainText()

    @property
    def folder_path(self):
        # 返回当前文件路径
        return self.note_file.text().replace('\\', '/')

    def get_group_name(self):
        code_info_list = sg.find_shotgun("Group", [["sg_group_project", "name_is", self.project]],
                                         ["code"], [{'field_name': 'sg_login', 'direction': 'asc'}])
        code_name_list = []
        for code_info in code_info_list:
            code_name_list.append(code_info["code"])
        return code_name_list

    def get_version_code(self):
        version_code_list = []
        version_name_list = sg.find_shotgun("Version", [['project', 'name_is', self.project],
                                                        ["id", "in", self.version_dict["id"]]], ["code"])
        for version_name in version_name_list:
            version_code_list.append(version_name["code"])
        return version_code_list

    def create_note(self):
        self.submit_note_pb.setText(u"正在提交...")
        self.submit_note_pb.setDisabled(True)
        attachments_list = []
        if self.checkbox_n.isChecked():
            if not os.path.exists(self.folder_path):
                MMessage.config(2)
                MMessage.warning(u'请先选择正确的附件文件', parent=self)
                self.submit_note_pb.setText(u"提交")
                self.submit_note_pb.setDisabled(False)
                return
        if self.folder_path:
            for root, dirs, files in os.walk(self.folder_path):
                for f in files:
                    file_path = root + "/" + f
                    attachments_list.append(file_path)
        if not self.content_text:
            MMessage.config(2)
            MMessage.warning(u'请先填写必填内容', parent=self)
            self.submit_note_pb.setText(u"提交")
            self.submit_note_pb.setDisabled(False)
            return
        addressing_text = self.label_people.text()
        group_name_list = []
        for group_name in addressing_text.split(","):
            if group_name not in group_name_list:
                group_name_list.append(group_name)
        for cc_name in self.examiners_people.split(","):
            if cc_name not in group_name_list:
                group_name_list.append(cc_name)
        all_addressing_list = sg.find_shotgun("Group", [["code", "in", group_name_list]], ["id", "code"])
        note_links_list = []
        for version_id in self.version_dict["id"]:
            note_links_list.append({"id": version_id, 'type': 'Version'})
        for addressing in all_addressing_list:
            addressing_list = [addressing]
            note_data = {
                "project": self.project_id,
                "subject": self.title_text,
                "sg_proposer": self.user_name_id,
                "addressings_to": addressing_list,
                "content": self.content_text,
                "sg_status_list": "opn",
                "sg_if_read": False,
                "note_links": note_links_list
            }
            note = sg.create_shotgun("Note", note_data)
            note_id = note["id"]
            for file_path in attachments_list:
                file_name = os.path.split(file_path)[-1]
                sg.upload_shotgun("Note", note_id, file_path, field_name="attachments",
                                  display_name=file_name)
        feedback_path_list, oss_path_list = self.get_submit_path()
        copy_list = []
        oss_copy_list = []
        for file_path in attachments_list:
            file_name = os.path.split(file_path)[-1]
            for feedback_path in feedback_path_list:
                file_path_list = [file_path, feedback_path + "/" + file_name]
                copy_list.append(file_path_list)
            for oss_path in oss_path_list:
                oss_file_list = [file_path, oss_path + "/" + file_name]
                oss_copy_list.append(oss_file_list)
        self.fetching_copy_thread.copy_list = copy_list
        self.fetching_copy_thread.start()
        self.fetching_oss_copy_thread.copy_list = oss_copy_list
        self.fetching_oss_copy_thread.start()
        batch_data = []
        for _id in self.version_dict["id"]:
            data = {
                "sg_status_list": "out"
            }
            batch_data.append({"request_type": "update", "entity_type": "Version", "entity_id": _id, "data": data})
        sg.batch_shotgun(batch_data)
        MMessage.config(2)
        MMessage.success(u'提交反馈成功!', parent=self)
        self.submit_note_pb.setText(u"提交成功")

    def get_version_user(self):
        version_info_list = sg.find_shotgun("Version", [['project', 'name_is', self.project],
                                                        ["id", "in", self.version_dict["id"]]],
                                            ["sg_task.Task.entity", "sg_version_type", "sg_task",
                                             "code", "sg_version_number", "sg_task.Task.entity.Asset.sg_asset_type",
                                             "sg_version_number", "user"])
        user_list = []
        for version in version_info_list:
            user = version["user"]["name"]
            user_list.append(user)
        return user_list, version_info_list

    def get_submit_path(self):
        version_type_list = []
        feedback_path_list = []
        oss_path_list = []
        for v in self.version_info_list:
            version_type = v["sg_task.Task.entity"]["type"]
            version_upload_type = v["sg_version_type"]
            if [version_type, version_upload_type] not in version_type_list:
                version_type_list.append([version_type, version_upload_type])
        convention_path_list = self.get_convention_path(version_type_list)
        for version_info in self.version_info_list:
            _task_name = version_info["sg_task"]["name"]
            version_type = version_info["sg_task.Task.entity"]["type"]
            version_upload_type = version_info["sg_version_type"]
            if version_info["sg_version_number"]:
                version = version_info["sg_version_number"]
            else:
                version = None
            if version_type == "Shot":
                scene = version_info["sg_task.Task.entity"]["name"].split("_")[0]
                shot = version_info["sg_task.Task.entity"]["name"].split("_")[-1]
                _code = version_info["sg_task.Task.entity"]["name"]
                classify = None
            elif version_type == "Asset":
                _code = version_info["sg_task.Task.entity"]["name"]
                classify = version_info["sg_task.Task.entity.Asset.sg_asset_type"]
                scene = None
                shot = None
            if version_upload_type == "Dailies":
                date = version_info["code"].split("_")[-1]
            else:
                date = None
            feedback_path_name = version_type + "_" + version_upload_type + "_feedback"
            oss_path_name = version_type + "_" + version_upload_type + "_oss"
            for convention_path in convention_path_list:
                if feedback_path_name == convention_path.keys()[0]:
                    feedback_path = convention_path.values()[0].format(date=date, task_name=_task_name,
                                                                       user=self.user_name, code=_code,
                                                                       classify=classify, scene=scene, shot=shot,
                                                                       version=version)
                    feedback_path_list.append(feedback_path)
                if oss_path_name == convention_path.keys()[0]:
                    oss_path = convention_path.values()[0].format(date=date, task_name=_task_name,
                                                                  user=self.user_name, code=_code,
                                                                  classify=classify, scene=scene, shot=shot,
                                                                  version=version)
                    oss_path_list.append(oss_path)
        return feedback_path_list, oss_path_list

    def finish_copy_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()

    def finish_copy_oss_data(self, finished):
        if finished:
            self.fetching_oss_copy_thread.wait()
            self.fetching_oss_copy_thread.quit()

    @staticmethod
    def get_convention_path(version_type_list):
        convention_path_list = []
        for version_type in version_type_list:
            custom_entity_list = sg.find_one_shotgun('CustomEntity01', [
                ['project', 'name_is', "DSF"], ['sg_type', 'is', version_type[0]],
                ['sg_upload_type', 'is', version_type[1]]],
                                                     ["sg_pattern", "sg_feedback_path", "sg_oss_submit_path"])
            feedback_path_name = version_type[0]+"_"+version_type[1]+"_feedback"
            feedback_dict = {feedback_path_name: custom_entity_list["sg_pattern"]+"/"+custom_entity_list
                             ["sg_feedback_path"]}
            oss_path_name = version_type[0] + "_" + version_type[1] + "_oss"
            oss_dict = {oss_path_name: custom_entity_list["sg_oss_submit_path"] + "/" + custom_entity_list
                        ["sg_feedback_path"]}
            if oss_dict not in convention_path_list:
                convention_path_list.append(oss_dict)
            if feedback_dict not in convention_path_list:
                convention_path_list.append(feedback_dict)
        return convention_path_list


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    version_dict = {"id": [16877, 16852], "type": "Version", "user": "huangan", "project": 'DSF'}
    test = CreateNoteUI(version_dict)
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())

