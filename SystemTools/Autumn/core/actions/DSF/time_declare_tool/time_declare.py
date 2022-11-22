#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dayu_widgets.label import MLabel
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from dayu_widgets.divider import MDivider
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.browser import MDragFileButton, MDragFolderButton
from dayu_widgets.message import MMessage
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.spin_box import MDoubleSpinBox, MDateTimeEdit
from PySide.QtGui import *
from PySide.QtCore import *
from utils import shotgun_operations
from config import GLOBAL
import datetime
import time
import config.GLOBAL
reload(config.GLOBAL)


class TimeDeclare(QWidget, MFieldMixin):
    tableInfo = Signal(dict)

    def __init__(self, task_dic={}, parent=None):
        super(TimeDeclare, self).__init__(parent)
        self.resize(480, 373)
        self.task_dic = task_dic
        self.addUi()

    def addUi(self):
        self.get_task_content = shotgun_operations.get_task(self.task_dic['project'], self.task_dic['id'])

        com = [
            {'label': self.get_task_content['code'], 'value': self.get_task_content['code']},
            {'label': u'任务', 'value': u'任务'},
            {'label': u'会议', 'value': u'会议'},
            {'label': u'请假', 'value': u'请假'},
            {'label': u'其他', 'value': u'其他'},
        ]
        self.declare_type_label = MLabel(u'申报类型：').secondary()
        self.declare_type = MComboBox().small()
        self.declare_type.setMaximumWidth(120)
        self.declare_box = MMenu()
        self.declare_box.set_data(com)
        self.declare_type.set_menu(self.declare_box)
        self.declare_type.setEditText(self.get_task_content['code'])

        self.declare_user_label = MLabel(u'提交用户：').secondary()
        self.declare_user = MLabel()
        self.declare_user.setText(self.task_dic['user'])

        self.declare_date_label = MLabel(u'提交日期：').secondary()
        self.declare_date = MDateTimeEdit(datetime=datetime.datetime.now())
        self.declare_date.setCalendarPopup(True)
        self.declare_date.set_dayu_size(25)
        self.declare_date.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        # self.declare_date.setMaximumWidth(120)

        self.unit = MLabel(u'小时').secondary()
        self.make_time_label = MLabel(u'制作用时：').secondary()
        self.make_time = MDoubleSpinBox()
        self.make_time.set_dayu_size(25)
        self.make_time.setValue(8)

        self.extra_time_label = MLabel(u'额外用时：').secondary()
        self.extra_time = MDoubleSpinBox()
        self.extra_time.set_dayu_size(25)

        self.describe_label = MLabel(u'描述：').secondary()
        self.describe = MTextEdit()

        self.btn_group = QHBoxLayout()
        self.btn_declare = MPushButton(u'提交').small()
        self.btn_closed = MPushButton(u'关闭').small()
        self.btn_declare.setFixedWidth(100)
        self.btn_closed.setFixedWidth(100)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_declare)
        self.btn_group.addWidget(self.btn_closed)
        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.declareInfo_layout = QGridLayout()
        self.declareInfo_layout.addWidget(self.declare_type_label, 0, 0)
        self.declareInfo_layout.addWidget(self.declare_type, 0, 1)
        self.declareInfo_layout.addWidget(self.declare_user_label, 0, 2)
        self.declareInfo_layout.addWidget(self.declare_user, 0, 3)
        # self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.declareInfo_layout.addWidget(self.make_time_label, 1, 0)
        self.declareInfo_layout.addWidget(self.make_time, 1, 1)
        # self.declareInfo_layout.addWidget(self.unit, 2, 2)
        self.declareInfo_layout.addWidget(self.extra_time_label, 1, 2)
        self.declareInfo_layout.addWidget(self.extra_time, 1, 3)
        # self.declareInfo_layout.addWidget(self.extra_time, 2, 5)
        self.declareInfo_layout.addWidget(self.describe_label, 2, 0)
        self.declareInfo_layout.addWidget(self.describe, 2, 1, 3, 3)
        self.declareInfo_layout.addWidget(self.declare_date_label, 5, 0)
        self.declareInfo_layout.addWidget(self.declare_date, 5, 1, 2, 2)


        self.main_lay = QVBoxLayout()
        self.main_lay.addWidget(MDivider(u'提交信息'))
        self.main_lay.addLayout(self.declareInfo_layout)
        self.main_lay.addWidget(MDivider())
        self.main_lay.addLayout(self.btn_group)
        self.main_lay.addStretch()
        self.setLayout(self.main_lay)
        ####connect
        self.btn_declare.clicked.connect(self.declare)
        self.btn_closed.clicked.connect(self.closed)

    @property
    def declare_type_text(self):
        return self.declare_type.currentText()

    @property
    def declare_user_text(self):
        return self.declare_user.text()

    @property
    def make_time_text(self):
        return self.make_time.text()

    @property
    def extra_time_text(self):
        return self.extra_time.text()

    @property
    def declare_date_text(self):
        return self.declare_date.text().split(' ')[0]

    @property
    def declare_time_text(self):
        return self.declare_date.text()

    @property
    def describe_text(self):
        return self.describe.toPlainText()

    def closed(self):
        self.close()

    def declare(self):
        if not self.declare_type_text:
            MMessage.error(u'请填写申报类型', parent=self)
            return
        if len(self.describe_text) < 10:
            MMessage.error(u'描述请不要小于十个字符', parent=self)
            return
        ####写入数据库
        print self.declare_date_text
        print self.declare_time_text
        # print self.declare_type_text
        # print self.declare_user_text
        # print self.make_time_text
        # print self.extra_time_text
        # print self.declare_date_text
        # print self.describe_text
        project_info = shotgun_operations.find_one_shotgun('Project', [['name', 'is', self.task_dic['project']]], ['id'])
        user_info = shotgun_operations.find_one_shotgun('Group', [['code', 'is', self.task_dic['user']]], ['sg_group_project', 'id', 'code'])
        filters_task = [
            ['project', 'name_is', self.task_dic['project']],
            ['id', 'is', self.task_dic['id']]
        ]
        sg_task = shotgun_operations.find_one_shotgun('Task', filters_task, ['id', 'code'])
        create_data = dict(
            project=project_info,
            date=self.declare_date_text,
            # user=user_info,
            updated_by=user_info,
            created_by=user_info,
            sg_group=user_info,
            description=self.describe_text,
            entity=sg_task

        )
        shotgun_operations.create_shotgun('TimeLog', create_data)
        MMessage.success(u'提交成功', parent=self)



def time_declare(task_dic):
    from dayu_widgets import dayu_theme
    global test
    test = TimeDeclare(task_dic)
    dayu_theme.apply(test)
    test.show()


if __name__ == '__main__':
    import sys
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dic = {'id': 15969, 'project': 'DSF', 'type': 'Task', 'user': 'TD_Group'}
    test = TimeDeclare(task_dic)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


