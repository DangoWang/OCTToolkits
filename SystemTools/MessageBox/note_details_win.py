#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.12.20
import sys,json, functools
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
from dayu_widgets.avatar import MAvatar
from dayu_widgets.tool_button import MToolButton
import utils.shotgun_operations as sg
from utils import fileIO
from pprint import pprint
import os


class DetailsWin(QWidget):
    def __init__(self, parent=None):
        super(DetailsWin, self).__init__(parent)
        self.image_avatar = MAvatar()
        self.user_login = sg.get_user()
        self.user = sg.find_one_shotgun("Group", [["sg_login", "is", self.user_login]], ["code"])["code"]

        self.label_name = MLabel()
        self.text_edit = MTextEdit()
        self.text_edit.setDisabled(True)
        self.text_edit.setFixedHeight(70)
        # self.text_edit.setFixedWidth(700)
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.button_download = MToolButton()
        self.c_button_reply = MPushButton(u"回复").small().success()
        self.c_button_reply.hide()
        self.file_path = MLineEdit().folder().small()
        self.button_download.hide()
        self.file_path.hide()

        self.splitter_1 = QSplitter()
        self.splitter_1.setOrientation(Qt.Vertical)
        self.splitter_1.setFixedWidth(26)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_download)
        button_layout.addWidget(self.file_path)
        button_layout.addWidget(self.splitter)
        button_layout.addWidget(self.c_button_reply)

        edit_layout = QVBoxLayout()
        edit_layout.addWidget(self.label_name)
        edit_layout.addWidget(self.text_edit)
        edit_layout.addLayout(button_layout)

        self.reply_layout = QHBoxLayout()
        self.reply_layout.addWidget(self.splitter_1)
        self.reply_layout.addWidget(self.image_avatar)
        self.reply_layout.addLayout(edit_layout)

    @property
    def get_text(self):
        return self.text_edit.toPlainText()

    @property
    def get_folder_path(self):
        return self.file_path.text().replace("\\", "/")

    def download_attachment(self, attachments_id):
        try:
            attachment_list = sg.find_shotgun("Attachment", [["id", "in", attachments_id]], ["this_file"])
            for file_url in attachment_list:
                attachment = file_url["this_file"]
                file_name = file_url["this_file"]["name"]
                sg.download_attachment_shotgun(attachment, file_path=u"{}/{}".format(self.get_folder_path, file_name))
            return True
        except Exception as e:
            print e
            return False

    def create_reply(self, note_id):
        try:
            user_name = json.dumps(u"{0}".format(self.user))
            user_name = json.loads(user_name)
            new_reply_content = u"【{}】:{}".format(user_name, self.get_text)
            self.text_edit.setText(new_reply_content)
            reply_dict = {"content": new_reply_content, "entity": {"id": note_id, "type": "Note"}}
            sg.create_shotgun("Reply", reply_dict)
            if self.get_folder_path:
                attachments_list = []
                for root, dirs, files in os.walk(self.get_folder_path):
                    for f in files:
                        file_path = os.path.join(root, f)
                        attachments_list.append(file_path)
                for file_path in attachments_list:
                    file_name = os.path.split(file_path)[-1]
                    sg.upload_shotgun("Note", note_id, file_path, field_name="attachments", display_name=file_name)
            self.text_edit.setDisabled(True)
            return True
        except Exception as e:
            print e
            return False


class NoteDetailsMainWin(QDialog, MFieldMixin):
    def __init__(self, note_info_dict ="", parent=None):
        super(NoteDetailsMainWin, self).__init__(parent)
        self.resize(600, 800)
        self.setWindowTitle(u'通知详情')
        self.note_info_dict = note_info_dict
        self.project = self.note_info_dict["project"]
        self.note_id = self.note_info_dict["id"][0]
        note_info, reply_detail_info = self.get_note_info()
        title = note_info["subject"]

        self.button_refresh = MToolButton()
        self.button_refresh.svg('refresh_line.svg').text_beside_icon()
        self.button_refresh.setText(u'刷新')

        path_label = MLabel(title).h3()
        detail_lay = QVBoxLayout()

        for c in range(0, len(reply_detail_info)+1):
            reply_win = DetailsWin()
            reply_win.splitter_1.setFixedHeight(20)
            reply_win.image_avatar.set_dayu_size(40)
            if c == 0:
                content = reply_detail_info[c]
                reply_win.splitter_1.hide()
                reply_win.image_avatar.set_dayu_size(60)
                reply_win.label_name.setText(content[1])
                reply_win.text_edit.setText(content[0])
                if content[2]:
                    reply_win.button_download.show()
                    reply_win.file_path.show()
                    reply_win.button_download.svg('down_fill.svg').text_beside_icon()
                    reply_win.button_download.setText(u'下载附件')
                    reply_win.button_download.clicked.connect(functools.partial(self.download_attachment,
                                                                                reply_win, content[2]))
            elif c == len(reply_detail_info):
                reply_win.button_download.show()
                reply_win.file_path.show()
                reply_win.c_button_reply.show()
                # reply_win.button_download
                reply_win.button_download.setText(u'上传附件')
                reply_win.text_edit.setDisabled(False)
                reply_win.c_button_reply.clicked.connect(lambda: self.upload_reply(reply_win))
            else:
                content = reply_detail_info[c]
                reply_win.label_name.setText(content[1])
                reply_win.text_edit.setText(content[0])
                if content[2]:
                    reply_win.button_download.show()
                    reply_win.file_path.show()
                    reply_win.button_download.svg('down_fill.svg').text_beside_icon()
                    reply_win.button_download.setText(u'下载附件')
                reply_win.button_download.clicked.connect(functools.partial(self.download_attachment,
                                                                            reply_win, content[2]))
            detail_lay.addLayout(reply_win.reply_layout)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'通知标题'))
        main_lay.addWidget(path_label)
        main_lay.addWidget(MDivider(u'通知详情'))
        main_lay.addLayout(detail_lay)

        main_lay.addStretch()
        self.setLayout(main_lay)

    def get_note_info(self):
        reply_detail_info = []
        note_info = sg.find_one_shotgun("Note", [['project', 'name_is', self.project], ["id", "is", self.note_id]],
                                                ["subject", "content", "sg_proposer", "attachments"])
        proposer = note_info["sg_proposer"]
        note_content = note_info["content"]
        if not proposer:
            proposer_name = ""
        else:
            proposer_name = proposer["name"]
        if not note_content:
            note_content = note_info["subject"]
        note_detail_info = [note_content, proposer_name]
        reply_info_list = sg.note_thread_read_shotgun(self.note_id)
        for i in range(0, len(reply_info_list)):
            attachments_id = []
            if i != len(reply_info_list)-1:
                if reply_info_list[i]["type"] == "Note":
                    if reply_info_list[i+1]["type"] == "Attachment":
                        for k in range(i+1, len(reply_info_list)):
                            if reply_info_list[k]["type"] != "Attachment":
                                break
                            else:
                                attachments_id.append(reply_info_list[k]["id"])
                    note_detail_info.append(attachments_id)
                    reply_detail_info.append(note_detail_info)
                if reply_info_list[i]["type"] == "Reply":
                    if reply_info_list[i+1]["type"] == "Attachment":
                        reply_people = reply_info_list[i]["user"]["name"]
                        for k in range(i + 1, len(reply_info_list)):
                            if reply_info_list[k]["type"] != "Attachment":
                                break
                            else:
                                attachments_id.append(reply_info_list[k]["id"])
                        reply_detail_list = [reply_info_list[i]["content"], reply_people, attachments_id]
                        reply_detail_info.append(reply_detail_list)
                    else:
                        reply_people = reply_info_list[i]["user"]["name"]
                        reply_detail_list = [reply_info_list[i]["content"], reply_people, attachments_id]
                        reply_detail_info.append(reply_detail_list)
            else:
                if reply_info_list[i]["type"] == "Reply":
                    reply_people = reply_info_list[i]["user"]["name"]
                    reply_detail_list = [reply_info_list[i]["content"], reply_people, attachments_id]
                    reply_detail_info.append(reply_detail_list)
                elif reply_info_list[i]["type"] == "Note":
                    note_detail_info.append(attachments_id)
                    reply_detail_info.append(note_detail_info)
        return note_info, reply_detail_info

    def download_attachment(self, weight, attachment_id_list):
        if not weight.get_folder_path:
            MMessage.config(2)
            MMessage.warning(u'请先选择存放文件的路径！', parent=self)
            return
        weight.button_download.setText(u'正在下载')
        value = weight.download_attachment(attachment_id_list)
        if value:
            MMessage.config(2)
            MMessage.success(u'下载成功！', parent=self)
            weight.button_download.setText(u'下载完成')
        else:
            MMessage.config(2)
            MMessage.success(u'下载失败！', parent=self)
            weight.button_download.setText(u'下载失败')

    def upload_reply(self, weight):
        weight.c_button_reply.setText(u"正在上传")
        value = weight.create_reply(self.note_id)
        if value:
            MMessage.config(2)
            MMessage.success(u'上传成功！', parent=self)
            weight.c_button_reply.setText(u'上传完成')
        else:
            MMessage.config(2)
            MMessage.success(u'上传失败！', parent=self)
            weight.c_button_reply.setText(u'上传失败')


def main(note_info_dict):
    from dayu_widgets import dayu_theme
    window = NoteDetailsMainWin(note_info_dict, parent=note_info_dict["widget"])
    dayu_theme.apply(window)
    window.show()


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    note_info_dict = {'project': "DSF", "id": 8052}
    test = NoteDetailsMainWin(note_info_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())

