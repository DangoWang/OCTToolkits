#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import sys
from dayu_widgets.qt import *
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from utils import shotgun_operations as sg


class AddVersionDesc(QDialog):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, version_info_dict="", parent=None):
        super(AddVersionDesc,  self).__init__(parent)
        self.resize(470, 400)
        self.setWindowTitle(u'添加版本说明')
        self._id = version_info_dict["id"][0]
        self.type = version_info_dict["type"]

        self.desc_edit = MTextEdit()
        self.submit_pb = MPushButton(text=u'提交')
        self.close_pb = MPushButton(text=u'关闭')

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submit_pb)
        self.button_layout.addWidget(self.close_pb)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'添加说明'))
        main_lay.addWidget(self.desc_edit)
        main_lay.addLayout(self.button_layout)
        self.setLayout(main_lay)
        self.close_pb.clicked.connect(self.close)
        self.submit_pb.clicked.connect(self.add_desc)

    @property
    def get_text(self):
        # 返回说明
        return self.desc_edit.toPlainText()

    def add_desc(self):
        self.submit_pb.setText(u"正在提交....")
        self.submit_pb.setDisabled(True)
        if self.type == "Task":
            data = {"sg_description": self.get_text}
        elif self.type == "Version":
            data = {"description": self.get_text}
        sg.update_shotgun(self.type, self._id, data)
        self.submit_pb.setText(u"提交成功")


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = AddVersionDesc()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


