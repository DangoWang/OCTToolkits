#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
import os
import json
import sys
sys.path.append(os.environ['oct_toolkits_path'])
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])
import datetime
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets.spin_box import MDateEdit
from dayu_widgets.qt import *
import utils.shotgun_operations as sg
from functools import partial
from dayu_widgets import dayu_theme
from PySide import QtCore
from PySide import QtGui
from dayu_widgets.message import MMessage


header_list = [
    # {
    #     'label': 'id',
    #     'key': 'id',
    # },
    {
        'label': u'类型',
        'key': 'sg_type',
        'searchable': True,
        'selectable': True
    },
    {
        'label': u'任务',
        'key': 'entity',
        'searchable': True,
        'selectable': True
    },
    {
        'label': u'时间',
        'searchable': True,
        'key': 'created_at',
    }, {
        'label': u'时长(分钟)',
        'key': 'duration',
        'editable': True,
    } , {
        'label': u'工作内容',
        'key': 'description',
        'editable': True,
    },

]

class WorkLogClass(QMainWindow):
    def __init__(self,parent=None):
        super(WorkLogClass, self).__init__(parent)
        self.user = sg.get_user()
        self.project = sg.get_project()
        self.work_list = self.find_work_log_list()
        self.time_use = 0

        self.task_list = sg.get_tasks(self.project, self.user)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(800, 400)
        self.setWindowTitle(u'Work Log')
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        main_lay = QVBoxLayout(self.centralwidget)

        self.horizontalLayout_title = QHBoxLayout()
        self.pushButton_add = MToolButton().svg('add_line.svg').icon_only()
        self.pushButton_add.clicked.connect(self.add_data)
        self.horizontalLayout_title.addWidget(self.pushButton_add)

        self.toolButton_left = MToolButton().svg('left_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_left)
        self.toolButton_left.clicked.connect(partial(self.time_change, -1))

        self.dateEdit = MDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.today = datetime.date.today()
        self.horizontalLayout_title.addWidget(self.dateEdit)

        self.toolButton_right = MToolButton().svg('right_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_right)
        self.toolButton_right.clicked.connect(partial(self.time_change, 1))

        self.label_title = QLabel()
        self.label_title.setText(u"")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.horizontalLayout_title.addWidget(self.label_title)

        self.lcdNumber = QtGui.QLCDNumber()
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display("00:00:00")
        self.horizontalLayout_title.addWidget(self.lcdNumber)

        # self.btn_time = QtGui.QPushButton(u"开始计时")
        self.btn_time = MToolButton().svg('circle.svg').icon_only()
        self.btn_time.setToolTip(u"点击开始/结束计时")
        self.horizontalLayout_title.addWidget(self.btn_time)

        label_tmp = QtGui.QLabel("        ")
        self.horizontalLayout_title.addWidget(label_tmp)

        self.timer = QtCore.QTimer()
        self.user_time = 0
        self.timer.timeout.connect(self.updateTimerDisplay)
        self.btn_time.clicked.connect(self.btn_time_command)
        # self.timer.start(1000)
        # print self.btn_time.text()

        self.pushButton_min = MToolButton().svg('down_line_dark.svg').icon_only()
        self.pushButton_min.clicked.connect(self.showMinimized)
        self.horizontalLayout_title.addWidget(self.pushButton_min)

        self.toolButton_close = MToolButton().svg('close_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_close)
        self.toolButton_close.clicked.connect(self.close)

        main_lay.addLayout(self.horizontalLayout_title)

        self.model_1 = MTableModel()
        self.model_1.set_header_list(header_list)

        self.model_1.set_data_list(self.work_list)
        self.model_sort = MSortFilterModel()
        self.model_sort.set_header_list(header_list)
        self.model_sort.setSourceModel(self.model_1)

        self.table_small = MTableView(size=dayu_theme.medium, show_row_count=True)
        self.table_small.set_header_list(header_list)
        self.table_small.horizontalHeader().setStretchLastSection(1)
        self.table_small.setShowGrid(True)
        dayu_theme.apply(self.table_small)
        self.table_small.setModel(self.model_sort)
        main_lay.addWidget(self.table_small)

        self.pushButton_save = MPushButton()
        self.pushButton_save.setText(u"保存")
        self.pushButton_save.clicked.connect(self.save_page_info)
        main_lay.addWidget(self.pushButton_save)

        self.pushButton = MPushButton()
        self.pushButton.setText(u"提交")
        self.pushButton.clicked.connect(self.update_work)
        main_lay.addWidget(self.pushButton)
        self.setLayout(main_lay)

        self.show_list = []
        self.dateEdit.dateChanged.connect(self.date_change)
        self.dateEdit.setDateTime(QDateTime(self.today))

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def btn_time_command(self):
        if self.btn_time.styleSheet():
            self.btn_time.setStyleSheet("")
            self.resetTimerDisplay()
        else:
            self.btn_time.setStyleSheet("QToolButton{background-color: #29a19c;}")
            self.startTimerDisplay()

    def startTimerDisplay(self):
        self.timer.start(1000)

    def updateTimerDisplay(self):
        self.user_time += 1
        text = "%02d:%02d:%02d" % (self.user_time/3600, (self.user_time%3600)/60, self.user_time % 60)
        self.lcdNumber.display(text)

    def resetTimerDisplay(self):
        use_minute = self.user_time/60
        self.user_time = 0
        self.lcdNumber.display("00:00:00")
        self.timer.stop()
        if use_minute:
            self.add_data(use_minute)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def time_change(self, num):
        one_day = datetime.timedelta(days=1)
        self.today += one_day * num
        self.dateEdit.setDateTime(QDateTime(self.today))

    def date_change(self):
        self.time_use = 0
        new = self.dateEdit.dateTime().date()
        self.today = datetime.date(new.year(), new.month(), new.day())
        if self.today > datetime.date.today() - datetime.timedelta(days=1) :
            self.toolButton_right.setEnabled(0)
        else:
            self.toolButton_right.setEnabled(1)
        if self.today != datetime.date.today():
            self.pushButton_add.setEnabled(0)
        else:
            self.pushButton_add.setEnabled(1)
        find_word = "{}-{}-{}".format(new.year(), new.month(), new.day())
        self.show_list = []
        for log in self.work_list:
            created_at = log["created_at"]
            if find_word == "{}-{}-{}".format(created_at.year, created_at.month, created_at.day):
                self.show_list.append(log)
                self.time_use += log["duration"]
        self.label_title.setText(u"               当日工作时长： {} 分钟".format(self.time_use))

        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        if os.path.isfile(work_log_info_file) and (self.today == datetime.date.today()):
            file_id = file(work_log_info_file, "r")
            try:
                info_list = json.loads(file_id.read())
                self.show_list.extend(info_list)
            except:
                pass
            file_id.close()
        self.model_1.set_data_list(self.show_list)

    def add_data(self, duration_num=0):
        keys_list = self.task_list.keys()
        keys_list.sort()
        self.show_list.append({'_parent': {'name': 'root'},
                               u'description': u'添加工作说明',
                               u'duration': duration_num,
                               u'created_at': None,
                               u'id': None,
                               u"sg_type": self.sg_type[0],
                               u"sg_type_list": self.sg_type,
                               u"entity": "",
                               u"entity_list": [""] + keys_list,
                               })
        self.model_1.set_data_list(self.show_list)

    def save_page_info(self):
        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        info_dir = []
        keys_list = self.task_list.keys()
        keys_list.sort()
        for row in range(self.model_sort.rowCount()):
            if self.model_1.index(row, 2).data() == "--":
                info_dir.append({'_parent': {'name': 'root'},
                                 "description": self.model_1.index(row, 4).data(),
                                 "duration": int(self.model_1.index(row, 3).data()),
                                 'created_at': None,
                                 'id': None,
                                 "sg_type": self.model_1.index(row, 0).data(),
                                 "sg_type_list": self.sg_type,
                                 "entity": self.model_1.index(row, 1).data(),
                                 "entity_list": [""] + keys_list,
                                 })
        file_id = file(work_log_info_file, "w")
        file_id.write(json.dumps(info_dir))
        file_id.close()
        self.statusbar.showMessage(u"数据保存完成")


    def update_work(self):
        user_filters = [['sg_login', 'is', self.user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        pro_filters = [['name', 'is', self.project]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)

        for row in range(self.model_sort.rowCount()):
            if self.model_1.index(row, 2).data() == "--":
                if not self.tabmodel.index(row, 4).data():
                    MMessage.config(3)
                    MMessage.error(u'请填写描述！', parent=self)
                    return
                log_dict = {'project': pro_sg, "description": self.model_1.index(row, 4).data(),
                            "duration": int(self.model_1.index(row, 3).data()), "sg_group": group_sg,
                            "sg_type": self.model_1.index(row, 0).data()}
                # if self.model_1.index(row, 0).data() == u"计划任务内":
                task_tx = self.model_1.index(row, 1).data()
                if task_tx:
                    task_entity = self.task_list[task_tx]
                    log_dict["entity"] = {"type": "Task", "id":task_entity["id"]}
                    log_dict['sg_type'] = u'计划任务内'
                sg.create_shotgun("TimeLog", log_dict)

        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        file_id = file(work_log_info_file, "w")
        file_id.write("")
        file_id.close()
        self.work_list = self.find_work_log_list()
        self.date_change()
        self.statusbar.showMessage(u"数据上传成功")
        # self.model_1.set_data_list(self.work_list)

        # self.pushButton.setText(u"提交成功")
        # self.pushButton.setEnabled(False)
        # self.close()

    def find_work_log_list(self):
        user_filters = [['sg_login', 'is', self.user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        filters = [['sg_group', 'is', group_sg]]
        fields = ["id", "created_at", "duration", "description", "sg_type", "entity"]
        work_log_list = sg.find_shotgun("TimeLog", filters, fields)

        pro_filters = [['name', 'is', "DSF"]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)
        name_list = sg.schema_field_read_shotgun("TimeLog", "sg_type", pro_sg)
        self.sg_type = name_list["sg_type"]["properties"]["valid_values"]["value"]
        return work_log_list

def main():
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    WorkLogWin = WorkLogClass()
    dayu_theme.apply(WorkLogWin)
    WorkLogWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
