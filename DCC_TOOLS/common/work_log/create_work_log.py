# coding=utf-8

from __future__ import unicode_literals
import utils.shotgun_operations as sg
from PySide import QtCore
from PySide import QtGui
import sys
import time
import datetime
from dayu_widgets import label
from dayu_widgets import push_button
from dayu_widgets import text_edit

# print sys.argv

class HJT_ToolTip(QtGui.QMainWindow):
    def __init__(self):
        super(HJT_ToolTip, self).__init__()
        self.setObjectName("HJT_ToolTipUI")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.setCentralWidget(self.centralwidget)

        task_list = sg.get_tasks(sys.argv[-3], sys.argv[-2])
        # print task_list
        # label_task = QtGui.QLabel(self.centralwidget)
        label_task = label.MLabel(parent=self.centralwidget)
        for key, value in task_list.items():
            if value["id"] == int(sys.argv[-1]):
                label_task.setText(u"制作任务: {}".format(key))
                break
        self.verticalLayout.addWidget(label_task)

        label_time = label.MLabel(parent=self.centralwidget)
        self.verticalLayout.addWidget(label_time)
        time_st = sys.argv[-4]
        t_start = "{}/{}/{} {}:{}".format(time_st[0:4], time_st[4:6], time_st[6:8], time_st[8:10], time_st[10:])
        t_end = time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time()))
        label_time.setText(u"制作时间: {} >> {}".format(t_start, t_end))

        # print datetime.datetime.now()
        idle_time = int(float(sys.argv[-5]))
        time_us = ((datetime.datetime.now() - datetime.datetime(int(time_st[0:4]), int(time_st[4:6]), int(time_st[6:8]), int(time_st[8:10]), int(time_st[10:]), 0)).seconds-idle_time) / 3600.0
        label_use = label.MLabel(parent=self.centralwidget)
        self.verticalLayout.addWidget(label_use)
        label_use.setText(u"制作时间: %0.2f小时" % (time_us))

        label_idle = label.MLabel(parent=self.centralwidget)
        self.verticalLayout.addWidget(label_idle)
        label_idle.setText(u"空闲时间: %0.2f小时" % (idle_time/3600.0))

        self.textEdit = text_edit.MTextEdit(parent=self.centralwidget)
        self.verticalLayout.addWidget(self.textEdit)

        self.pushButton = push_button.MPushButton(parent=self.centralwidget)
        self.pushButton.setText(u"上传")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.create_log)
        # name_user = sys.argv[1]
        # name_user = sg.get_user()
        # name_project = sg.get_project()
        # task_list = sg.get_tasks(name_project, name_user)
        self.pushButton.setText( u"上传日志" )

    def create_log(self):
        time_st = sys.argv[-4]
        id_task = sys.argv[-1]
        name_user = sys.argv[-2]
        name_project = sys.argv[-3]

        description = self.textEdit.toPlainText()

        user_filters = [['sg_login', 'is', name_user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        pro_filters = [['name', 'is', name_project]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)

        task_filters = [['id', 'is', int(id_task)]]
        task_fields = []
        task_sg = sg.find_one_shotgun("Task", task_filters, task_fields)
        time_us = (datetime.datetime.now() - datetime.datetime(int(time_st[0:4]), int(time_st[4:6]), int(time_st[6:8]), int(time_st[8:10]), int(time_st[10:]))).seconds/3660.0

        # print time_us
        log_dict = {"entity": task_sg, "description":description, "duration": time_us, "sg_group": group_sg, "project": pro_sg}
        sg.create_shotgun("TimeLog", log_dict)
        sg.update_shotgun('Task', task_sg['id'], {'sg_status_list': 'ip'})
        self.close()
        sys.exit()

app = QtGui.QApplication(sys.argv)
from dayu_widgets import dayu_theme
win = HJT_ToolTip()
dayu_theme.apply(win)
win.show()
sys.exit(app.exec_())