#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

sys.path.append(os.environ['oct_toolkits_path'])
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])

import json
import datetime
from PySide import QtCore
from PySide import QtGui
from functools import partial


import my_list_model
reload(my_list_model)
import my_task_delegate
reload(my_task_delegate)
import utils.shotgun_operations as sg

from dayu_widgets.tool_button import MToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets.spin_box import MDateEdit
from dayu_widgets import dayu_theme
from dayu_widgets.message import MMessage


class ModelWindowClass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ModelWindowClass, self).__init__(parent)
        self.resize(800, 400)
        self.setWindowTitle(u'Work Log')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        main_lay = QtGui.QVBoxLayout(self.centralwidget)

        self.user = sg.get_user()
        self.project = sg.get_project()

        self.task_list = sg.get_tasks(self.project, self.user)
        # print "self.task_list",  self.task_list

        self.horizontalLayout_title = QtGui.QHBoxLayout()
        self.pushButton_add = MToolButton().svg('add_line.svg').icon_only()
        self.pushButton_add.clicked.connect(self.add_data)
        self.horizontalLayout_title.addWidget(self.pushButton_add)

        self.toolButton_left = MToolButton().svg('left_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_left)
        self.toolButton_left.clicked.connect(partial(self.time_change, -1))

        self.dateEdit = MDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.today = datetime.datetime.today()
        self.horizontalLayout_title.addWidget(self.dateEdit)

        self.toolButton_right = MToolButton().svg('right_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_right)
        self.toolButton_right.clicked.connect(partial(self.time_change, 1))

        self.label_title = QtGui.QLabel()
        self.label_title.setText(u"")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
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
        self.timer_pushbutton = QtCore.QTimer()
        self.timer_pushbutton.timeout.connect(self.set_update_enable)
        self.timer_pushbutton.start(4000)
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
        self.toolButton_close.clicked.connect(self.close_window)

        main_lay.addLayout(self.horizontalLayout_title)

        self.tabview = QtGui.QTableView()
        self.tabview.horizontalHeader().setStretchLastSection(1)
        self.tabview.horizontalHeader().setStretchLastSection(1)
        self.tabview.setStyleSheet('QHeaderView::section, QTableCornerButton::section {color: rgb(200, 200, 200);background-color: rgb(42, 42, 42);}')
        main_lay.addWidget(self.tabview)

        self.tabmodel = my_list_model.TableModel()
        self.tabview.setModel(self.tabmodel)
        self.tabview.setColumnWidth(2, 128)

        pro_filters = [['name', 'is', self.project]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)
        name_list = sg.schema_field_read_shotgun("TimeLog", "sg_type", pro_sg)
        self.sg_type = name_list["sg_type"]["properties"]["valid_values"]["value"]
        try:
            self.sg_type.remove(u"软件自动计时")
        except:
            pass
        self.task_type_delegate = my_task_delegate.TaskDelegate(self.sg_type)
        self.tabview.setItemDelegateForColumn(0, self.task_type_delegate)


        keys_list = self.task_list.keys()
        keys_list.sort()
        self.entity_delegate = my_task_delegate.TaskDelegate(keys_list)
        self.tabview.setItemDelegateForColumn(1, self.entity_delegate)



        self.log_list = self.get_log_list()
        # for log in self.log_list:
        #     dd = datetime.timedelta(hours=4, minutes=55)
        #     print dd.seconds / 3600.0
        #     # datetime.timedelta(minutes=log["duration"]).
        #     # log["duration"] = log["duration"] / 60.0
        #     log["duration"] = datetime.timedelta(minutes=log["duration"]).seconds / 3600.0
        # self.tabmodel.setMyData(self.log_list)

        self.pushButton_save = MPushButton()
        self.pushButton_save.setText(u"保存")
        self.pushButton_save.clicked.connect(self.save_page_info)
        main_lay.addWidget(self.pushButton_save)

        self.pushButton = MPushButton()
        self.pushButton.setText(u"提交")
        self.pushButton.clicked.connect(self.update_work)
        main_lay.addWidget(self.pushButton)
        self.setLayout(main_lay)

        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.dateEdit.dateChanged.connect(self.date_change)
        self.dateEdit.setDateTime(self.today)
        self.pushButton.setText(u"提交  3秒后可操作")
        self.pushButton.setEnabled(0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

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
        use_minute = self.user_time/3600.0
        self.user_time = 0
        self.lcdNumber.display("00:00:00")
        self.timer.stop()
        if use_minute:
            self.add_data(use_minute)

    def time_change(self, num):
        one_day = datetime.timedelta(days=1)
        self.today += one_day * num
        self.dateEdit.setDateTime(QtCore.QDateTime(self.today))

    def set_update_enable(self):
        self.pushButton.setText(u"提交")
        self.timer_pushbutton.stop()
        self.pushButton.setEnabled(1)
        self.date_change()


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
            self.pushButton.setEnabled(0)
        else:
            self.pushButton_add.setEnabled(1)
            self.pushButton.setEnabled(1)
        find_word = "%04d-%02d-%02d"%(new.year(), new.month(), new.day())
        self.show_list = []
        for log in self.log_list:
            created_at = log["date"]
            # print "created_at", created_at, dir(created_at)
            # if find_word == "{}-{}-{}".format(created_at.year, created_at.month, created_at.day):
            if find_word == created_at:
                # print log["duration"]
                # log["duration"] = float("%0.3f" % (float(log["duration"])/60.0))
                if isinstance(log["entity.Task.entity"], dict):
                    log["entity.Task.entity"] = log["entity.Task.entity"]["name"]
                # print "log", log
                self.show_list.append(log)
                self.time_use += log["duration"]
        self.label_title.setText(u"               当日工作时长： {} 小时".format(self.time_use))

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
        self.tabmodel.setMyData(self.show_list)

        for i in range(self.tabmodel.rowCount()):
            self.tabview.openPersistentEditor(self.tabmodel.index(i, 0))
            # self.tabview.openPersistentEditor(self.tabmodel.index(i, 1))
        # if self.time_use > 12:
        #     QtGui.QMessageBox.about(self, u"提示", u"当日工作时长超过12小时，请确认是否扣除休息时间。。。")

    def add_data(self, duration_num=0.0):
        self.tabmodel.insertRow(self.tabmodel.rowCount(), [u'\u8ba1\u5212\u4efb\u52a1\u5916', None, None, duration_num, u""])
        self.tabview.openPersistentEditor(self.tabmodel.index(self.tabmodel.rowCount()-1, 0))


    def save_page_info(self):
        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        info_dir = []
        keys_list = self.task_list.keys()
        keys_list.sort()
        for row in range(self.tabmodel.rowCount()):
            if self.tabmodel.index(row, 2).data() == None:
                info_dir.append({u'description': self.tabmodel.index(row, 4).data(),
                               u'created_at': None,
                               u'entity': self.tabmodel.index(row, 1).data(),
                               u'duration': int(self.tabmodel.index(row, 3).data()),
                               u'sg_type': self.tabmodel.index(row, 0).data(),
                               u'type': u'TimeLog',
                               })
        file_id = file(work_log_info_file, "w")
        file_id.write(json.dumps(info_dir))
        file_id.close()
        self.statusbar.showMessage(u"数据保存完成")

    def get_log_list(self):
        user_filters = [['sg_login', 'is', self.user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        filters = [['sg_group', 'is', group_sg]]
        fields = ["id", "created_at", "duration", "description", "sg_type", "entity", 'entity.Task.entity', "date"]
        work_log_list = sg.find_shotgun("TimeLog", filters, fields)
        for each_log in work_log_list:

            each_log["duration"] = float(each_log["duration"]) / 60.0


        # pro_filters = [['name', 'is', self.project]]
        # pro_fields = []
        # pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)
        # name_list = sg.schema_field_read_shotgun("TimeLog", "sg_type", pro_sg)
        # self.sg_type = name_list["sg_type"]["properties"]["valid_values"]["value"]
        return work_log_list

    def raise_confirm_dialog(self, text):
        confirm_dialog = QtGui.QMessageBox()
        if len(text) > 500:
            text = text[:500] + "..."
        confirm_dialog.setText(text)
        confirm_dialog.setWindowTitle(u"提示")
        confirm_dialog.addButton(u"等等，我再改一下", QtGui.QMessageBox.AcceptRole)  # role 0
        confirm_dialog.addButton(u"没毛病，提交了", QtGui.QMessageBox.RejectRole)  # role 1
        return confirm_dialog.exec_()

    def update_work(self):
        time_update = 0
        for row in range(self.tabmodel.rowCount()):
            time_update += self.tabmodel.index(row, 3).data()
        if time_update >= 12:
            reply = self.raise_confirm_dialog(u'当日工作时长超过12小时，请确认是否已扣除休息时间???\n(参考时间上限：10-11小时)')
            # reply = QtGui.QMessageBox.question(self,
            #                                        u'提交',
            #                                        u'当日工作时长超过12小时，请确认是否扣除休息时间???',
            #                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            #                                        QtGui.QMessageBox.No)

            if reply != 1:
                return
        self.pushButton.setText(u"提交中  3秒后可操作")
        # user_filters = [['sg_login', 'is', self.user]]
        user_filters = [['sg_login', 'is', self.user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        # pro_filters = [['name', 'is', self.project]]
        pro_filters = [['name', 'is', self.project]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)

        for row in range(self.tabmodel.rowCount()):
            # if self.tabmodel.index(row, 2).data() == None:
            if not self.tabmodel.index(row, 4).data():
                MMessage.config(3)
                MMessage.error(u'请填写描述！', parent=self)
                continue
            if self.tabmodel.index(row, 3).data() > 8:
                MMessage.error(u'单条最长时长限制8小时！', parent=self)
                continue
            # print "data", self.tabmodel.index(row, 3).data()
            # print "duration", int(float(self.tabmodel.index(row, 3).data())*60)
            log_dict = {'project': pro_sg, "description": self.tabmodel.index(row, 4).data(),
                        "duration": int(float(self.tabmodel.index(row, 3).data())*60.0), "sg_group": group_sg,
                        # "duration": datetime.timedelta(hours=float(self.tabmodel.index(row, 3).data())).seconds/60.0, "sg_group": group_sg,
                        "sg_type": self.tabmodel.index(row, 0).data()}
            # if self.tabmodel.index(row, 0).data() == u"计划任务内":
            task_tx = self.tabmodel.index(row, 1).data()
            # print "task_tx", task_tx
            if task_tx and (not isinstance(task_tx, dict)) and self.task_list.has_key(task_tx):
                task_entity = self.task_list[task_tx]
                log_dict["entity"] = {"type": "Task", "id":task_entity["id"]}
                log_dict['sg_type'] = u'计划任务内'
            if self.tabmodel.index(row, 2).data() == None:
                sg.create_shotgun("TimeLog", log_dict)
            else:
                sg.update_shotgun("TimeLog", self.show_list[row]["id"], log_dict)
        self.log_list = list()
        self.log_list = self.get_log_list()
        # for each_log in self.log_list:
        #
        #     each_log["duration"] = datetime.timedelta(minutes=each_log["duration"]).seconds/3600.0
        #     # each_log["duration"] = each_log["duration"] / 60.0
        #     # log["duration"] = float("%0.3f" % ((float(log["duration"]))))
        # self.date_change()

        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        try:
            os.remove(work_log_info_file)
        except:
            pass
        # file_id = file(work_log_info_file, "w")
        # file_id.write("")
        # file_id.close()
        self.statusbar.showMessage(u"数据上传成功")
        self.pushButton.setEnabled(0)
        self.timer_pushbutton.start(4000)


    def close_window(self):
        # print "closeEvent"
        tmp_path = os.getenv('TEMP')
        work_log_info_file = os.path.join(tmp_path, "{}-{}-{}.json".format(self.today.year, self.today.month, self.today.day))
        # print work_log_info_file, os.path.isfile(work_log_info_file)
        if os.path.isfile(work_log_info_file):
            qmes = QtGui.QMessageBox.question(self, u"警告", u"有未提交日志，是否提交",
                                              QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                              QtGui.QMessageBox.Yes)
            if qmes == QtGui.QMessageBox.Yes:
                self.update_work()
        self.close()

def main():
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    WorkLogWin = ModelWindowClass()
    dayu_theme.apply(WorkLogWin)
    WorkLogWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

