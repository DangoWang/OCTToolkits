#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
import pprint
import sys,os
import functools

from dayu_widgets import dayu_theme
from dayu_widgets.divider import MDivider
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.loading import MLoadingWrapper
from dayu_widgets.push_button import MPushButton
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.qt import *
import utils.shotgun_operations as sg


header_list = [
    {
        'label': 'id',
        'key': 'id',
    }, {
        'label': u'日期',
        'key': 'created_at',
        # 'searchable': True,
        # 'selectable': True,
    }, {
        'label': u'说明',
        'key': 'description',
        # 'width': 90,
        # 'searchable': True,
        'editable': True,
    }, {
        'label': u'时长(分钟)',
        'key': 'duration',
        'selectable': True,
        # 'searchable': True,
        # 'exclusive': False,
        # 'width': 120,
    }
]

class WorkLogClass(QDialog):
    def __init__(self,task_dict="",parent=None):
        super(WorkLogClass, self).__init__(parent)
        self.task_id = task_dict["id"][0]
        self.project = task_dict["project"]
        self.user = task_dict["user"]
        self.resize(560, 400)
        self.setWindowTitle(u'Work Log')
        main_lay = QVBoxLayout()

        self.horizontalLayout_title = QHBoxLayout()
        self.pushButton_add = MToolButton().svg('add_line.svg').icon_only()
        self.pushButton_add.clicked.connect(self.add_data)
        self.horizontalLayout_title.addWidget(self.pushButton_add)
        # self.pushButton_del = MToolButton().svg('close_line.svg').icon_only()
        # self.pushButton_del.clicked.connect(self.del_data)
        # self.horizontalLayout_title.addWidget(self.pushButton_del)
        label_title = QLabel()
        label_title.setText(u"")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label_title.sizePolicy().hasHeightForWidth())
        label_title.setSizePolicy(sizePolicy)
        self.horizontalLayout_title.addWidget(label_title)

        main_lay.addLayout(self.horizontalLayout_title)

        self.model_1 = MTableModel()
        self.model_1.set_header_list(header_list)
        self.work_list = self.find_work_log_list()
        # print self.work_list
        self.del_list  = []
        self.model_1.set_data_list(self.work_list)
        self.model_sort = MSortFilterModel()
        self.model_sort.setSourceModel(self.model_1)

        self.table_small = MTableView(size=dayu_theme.medium, show_row_count=True)
        self.table_small.setShowGrid(True)
        dayu_theme.apply(self.table_small)
        # self.table_small.DoubleClicked.connect(self.update_work)
        self.table_small.setModel(self.model_sort)
        main_lay.addWidget(self.table_small)

        self.pushButton = MPushButton()
        self.pushButton.setText(u"提交")
        self.pushButton.clicked.connect(self.update_work)
        main_lay.addWidget(self.pushButton)
        self.setLayout(main_lay)

    def del_row(self):
        reply = QMessageBox.question(self, '确认', '确定删除数据?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            r = self.player_tabview.currentIndex().row()
            # item = self.player_model.index(r, 0)
            self.table_small.beginRemoveRows(QModelIndex(),0, r)
            self.table_small.endRemoveRows()

    def del_data(self):
        # print self.table_small.currentIndex().row()
        # print self.model_sort.rowCount()
        reply = QMessageBox.question(self, u'确认', u'确定删除数据?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            r = self.table_small.currentIndex().row()
            # self.model_sort.beginRemoveRows(r)
            # self.model_sort.beginRemoveRows(QModelIndex(),r, r)
            self.del_list.append(self.work_list[r])
            self.work_list.remove(self.work_list[r])
            self.model_1.set_data_list(self.work_list)
            # self.model_sort.endRemoveRows()

    def add_data(self):
        self.work_list.append({'_parent': {'name': 'root'}, u'description': u'New Time Log', u'duration': 0, u'created_at': None, u'id': None})
        self.model_1.set_data_list(self.work_list)

    def update_work(self):
        # print self.model_sort.rowCount()
        user_filters = [['sg_login', 'is', self.user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        pro_filters = [['name', 'is', sg.get_project()]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)

        for row in range(self.model_sort.rowCount()):
            if self.model_1.index(row, 0).data() == "--":
                log_dict = {"entity": self.task_sg, "description": self.model_1.index(row, 2).data(), "duration": int(self.model_1.index(row, 3).data()), "sg_group": group_sg,
                            "project": pro_sg}
                sg.create_shotgun("TimeLog", log_dict)

                # print "new:",self.model_1.index(row, 0).data(),self.model_1.index(row, 2).data(),self.model_1.index(row, 3).data()
        #     else:
        #         new_info = {"description": self.model_1.index(row, 2).data(), "duration": int(self.model_1.index(row, 3).data())}
        #         sg.update_shotgun("TimeLog", int(self.model_1.index(row, 0).data()), new_info)
        # for del_sg in self.del_list:
        #     if del_sg["id"]:
        #         sg.delete_one_shotgun("TimeLog", del_sg["id"])
                # print "update:", self.model_1.index(row, 0).data(),self.model_1.index(row, 2).data(),self.model_1.index(row, 3).data()
        # for row in range(self.model_sort.rowCount()):
        #     print self.model_sort.data(row)
        # print self.work_list
        # print self.del_list
        self.pushButton.setText(u"提交成功")
        self.pushButton.setEnabled(False)

    def find_work_log_list(self):
        task_filters = [['id', 'is', int(self.task_id)]]
        task_fields = []
        self.task_sg = sg.find_one_shotgun("Task", task_filters, task_fields)

        filters = [['entity', 'is', self.task_sg]]
        fields = ["id", "created_at", "duration", "description"]
        work_log_list = sg.find_shotgun("TimeLog", filters, fields)
        return work_log_list

if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": [16447], "type": "Task", "user": "hanjuntai", "project": "DSF"}
    test = WorkLogClass(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())




