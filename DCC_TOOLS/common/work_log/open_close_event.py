# coding=utf-8

import os
import pyautogui as pag
import maya.OpenMaya as om
import maya.OpenMayaUI as mui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets
import utils.shotgun_operations as sg
import maya.cmds as cmds
import maya.mel as mel
from DCC_TOOLS.common import dcc_utils
import subprocess
import time
from dayu_widgets import label
from dayu_widgets import push_button
from dayu_widgets import combo_box


from dayu_widgets import dayu_theme
from dayu_widgets import menu
import datetime
from functools import partial
from DCC_TOOLS.common.dcc_utils import Timer


_win = "set_task_win_ui"

class task_info:
    user = None
    project = None
    task = None
    name = None
    time = None


class idle_info:
    work = 1
    mouse_t = datetime.datetime.now()
    id = None
    start_time = None
    idle_time = 0
    result = 0


def idle_proc():
    t2_t1 = (datetime.datetime.now() - idle_info.mouse_t).total_seconds()
    if t2_t1 > 300:
        idle_info.result += t2_t1
    if not idle_info.start_time:
        idle_info.start_time = datetime.datetime.now()

def busy_proc():
    if idle_info.start_time:
        idle_info.mouse_t = datetime.datetime.now()
        totalTime = (datetime.datetime.now() - idle_info.start_time).total_seconds()
        idle_info.idle_time += totalTime
        if totalTime > 60:
            idle_info.result += idle_info.idle_time
            idle_info.idle_time = 0
        idle_info.start_time = None

class set_task_win_class(QtWidgets.QMainWindow):
    def __init__(self, parent=dcc_utils.getMayaWindow()):
        super(set_task_win_class, self).__init__(parent)
        self.setWindowTitle("Set Task")
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint)
        self.setObjectName(_win)
        self.resize(300, 66)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # self.pushButton_refresh = push_button.MPusQhButton(parent=self.centralwidget)
        self.pushButton_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_refresh.clicked.connect(self.ref_task)
        self.pushButton_refresh.setText(u"刷新任务")
        self.verticalLayout.addWidget(self.pushButton_refresh)

        label_title = label.MLabel(parent=self.centralwidget)
        label_title.setAlignment(QtCore.Qt.AlignCenter)
        label_title.setText(u"请先选择任务后开始制作")
        self.verticalLayout.addWidget(label_title)

        label_title = label.MLabel(parent=self.centralwidget).secondary()
        label_title.setAlignment(QtCore.Qt.AlignCenter)
        label_title.setText(u"（注：此操作仅用于统计任务用时,set之后窗口自动关闭。）")
        self.verticalLayout.addWidget(label_title)

        # self.comboBox = combo_box.MComboBox(self.centralwidget)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.verticalLayout.addWidget(self.comboBox)
        task_info.task = None
        task_info.user = sg.get_user()
        task_info.project = sg.get_project()
        self.task_list = sg.get_tasks(task_info.project, task_info.user)
        # print self.task_list
        name_task_list = self.task_list.keys()
        name_task_list.sort()
        # self.menu1 = menu.MMenu()
        # self.menu1.set_data(name_task_list)
        # self.comboBox.set_menu(self.menu1)
        self.comboBox.addItem(u"计划任务外")
        self.comboBox.addItems(name_task_list)

        # self.pushButton = push_button.MPushButton(parent=self.centralwidget)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.set_task)
        self.pushButton.setText("Set")
        self.verticalLayout.addWidget(self.pushButton)
        self.setCentralWidget(self.centralwidget)
        # task_info.time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        task_info.time = datetime.datetime.now()
        file_name = cmds.file(q=1, sn=1, shn=1)
        if file_name:
            file_name = file_name.split(".")[0].lower().replace('_', '')
            file_short_name = file_name.split('\\')[-1].split('/')[-1].lower().replace('_', '')
            self.comboBox.setCurrentIndex(0)
            for num, task in enumerate(name_task_list):
                task_lower = task.lower().replace('_', '')
                if task_lower in file_name or file_short_name in task_lower:
                    self.comboBox.setCurrentIndex(num+1)
                    break
            self.set_task()
            print u'已set任务%s'% self.comboBox.currentText()

    def ref_task(self):
        task_info.user = sg.get_user()
        task_info.project = sg.get_project()
        self.task_list = sg.get_tasks(task_info.project, task_info.user)
        name_task_list = self.task_list.keys()
        name_task_list.sort()
        self.comboBox.clear()
        self.comboBox.addItems(name_task_list)
        # self.menu1.set_data(name_task_list)

    def set_task(self):
        sel_task = self.comboBox.currentText()
        task_info.name = sel_task
        idle_info.result = 0
        idle_info.idle_time = 0
        idle_info.start_time =None
        if sel_task == u"计划任务外":
            task_info.task = sel_task
        else:
            task_info.task = self.task_list[sel_task]["id"]
            task_id = self.task_list[sel_task]["id"]
            task_filters = [['id', 'is', task_id]]
            task_fields = ["sg_date"]
            task_sg = sg.find_one_shotgun("Task", task_filters, task_fields)
            if task_sg["sg_date"] == None:
                note_new = {"sg_date": time.strftime('%Y-%m-%d', time.localtime(time.time())),
                            'sg_status_list': 'ip'
                            }
                sg.update_shotgun("Task", task_id, note_new)
        # self.close()


def close_func(*args):
    if task_info.task:
        # time_st = task_info.time
        id_task = task_info.task
        name_user = task_info.user
        name_project = task_info.project
        task_name = task_info.name

        user_filters = [['sg_login', 'is', name_user]]
        user_fields = []
        group_sg = sg.find_one_shotgun("Group", user_filters, user_fields)

        pro_filters = [['name', 'is', name_project]]
        pro_fields = []
        pro_sg = sg.find_one_shotgun("Project", pro_filters, pro_fields)


        # time_us = ((datetime.datetime.now() - task_info.time).total_seconds() - idle_info.result) / 60.0
        time_us = ((datetime.datetime.now() - task_info.time).total_seconds()) / 60.0

        log_dict = {}
        if id_task == u"计划任务外":
            file_name = cmds.file(q=1, sn=1, shn=1).replace(".ma", "")
            log_dict = {"duration": time_us, "sg_group": group_sg, "project": pro_sg, "description": u'制作:'+file_name, "sg_type": u"计划任务外"}
        else:
            task_filters = [['id', 'is', int(id_task)]]
            task_fields = []
            task_sg = sg.find_one_shotgun("Task", task_filters, task_fields)
            # time_us = (datetime.datetime.now() - datetime.datetime(int(time_st[0:4]), int(time_st[4:6]), int(time_st[6:8]), int(time_st[8:10]), int(time_st[10:]))).seconds/3660.0

            # time_us = ((datetime.datetime.now() - datetime.datetime(int(time_st[0:4]), int(time_st[4:6]), int(time_st[6:8]), int(time_st[8:10]), int(time_st[10:]))).seconds-idle_info.result) / 60.0

            # time_us = (int(time_us)/1440) * 480 + (480 if time_us%1440 > 480 else time_us%1440)
            # print datetime.datetime.now(), time_st
            # print "time_us", time_us, (datetime.datetime.now() - datetime.datetime(int(time_st[0:4]), int(time_st[4:6]), int(time_st[6:8]), int(time_st[8:10]), int(time_st[10:]))).seconds
            # print time_us
            # print task_sg, time_us, group_sg, pro_sg
            log_dict = {"entity": task_sg, "duration": time_us, "sg_group": group_sg, "project": pro_sg, "description": u'制作:'+task_name, "sg_type": u"计划任务内"}
            print u'任务%s当前已用时总计为:%s\n' %(task_name, time_us)
            #  用当前时间 - （当前计时 + 已计时） 早于 早上9 点， 放弃。
            filters1 = [['sg_group.Group.sg_login', 'is', sg.get_user()]]
            fields1 = ["id", "created_at", "duration", "description", "sg_type", "entity"]
            alogs = sg.find_shotgun("TimeLog", filters1, fields1)
            nnow = datetime.datetime.now()
            find_word1 = nnow.strftime("%Y-%m-%d")
            time_all = 0
            for lo in alogs:
                created_at1 = str(lo["created_at"])
                if find_word1 in created_at1:
                    time_all += lo["duration"]
            y, m, d = [int(d) for d in str(datetime.date.today()).split('-')]
            temp = datetime.datetime.now() - datetime.timedelta(float(time_all+time_us) / 60.0 / 24.0)
            print u'当前时间%s\n' % str(temp)
            if temp > datetime.datetime(y, m, d, 9, 0, 0, 0):
                if time_us > 0:
                    if time_us > 480:
                        log_dict['duration'] = time_us - 120.0
                    print u'%s晚于9点， 正常计时\n' % str(temp)
                    sg.create_shotgun("TimeLog", log_dict)
            else:
                print u'%s早于9点， 放弃\n' % str(temp)
        task_info.task = None

    # dir_info = {"entity": {u'type': u'Task', u'id': 16447},
    #             "duration": 60,
    #             "sg_group": {u'type': u'Group', u'id': 117},
    #             "project": {u'type': u'Project', u'id': 89}}
    # sg.create_shotgun("TimeLog", dir_info)
    # path_current = os.path.dirname(os.path.abspath(__file__))
    # if task_info.task:
    #     subprocess.call(r'python {}\create_work_log.py "{}" "{}" "{}" "{}" "{}"'.format(path_current, int(idle_info.result), task_info.time, task_info.project, task_info.user, task_info.task), shell=1)

# {u'type': u'Task', u'id': 16447} 0.108196721311 {u'type': u'Group', u'id': 117} {u'type': u'Project', u'id': 89}

def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

def open_func(*args):
    if task_info.task:
        close_func()
    if not cmds.file(q=1, sn=1):
        return
    if cmds.window(_win, exists=1):
        cmds.deleteUI(_win)
    win = set_task_win_class()
    # win.show()

    # mel.eval('''source unifiedRenderGlobalsWindow;createRenderSettingsWindow;''')
    # while 1:
    #     if cmds.scriptJob(ex=100):
    #         break
    # 延迟启动设置任务
    # cmds.evalDeferred(add_idle_event, lp=1)
    # idle_timer = Timer(10, add_idle_event, repeat=False)
    # idle_timer.start()

def add_idle_event():
    if task_info.task:
        close_func()
    if not cmds.file(q=1, sn=1):
        return
    # if not idle_info.id:
    #     idle_info.id = cmds.scriptJob(idleEvent=idle_proc)
    #     cmds.scriptJob(ct=["busy", busy_proc])
    #     print "idle_info.id", idle_info.id

    if cmds.window(_win, exists=1):
        cmds.deleteUI(_win)
    win = set_task_win_class()
    # dayu_theme.apply(win)
    win.show()

def main():
    cmds.evalDeferred(add_event, lp=1)
    # mevent = om.MEventMessage()
    # mevent.addEventCallback("SceneOpened", open_func)
    # maya = getMayaWindow()
    # cmds.window(maya.objectName(), e=1, closeCommand=close_func)
    # cmds.scriptJob("oct_idleEvent", idleEvent=idle_proc)
    # cmds.scriptJob("oct_busyEvent", ct=["busy", busy_proc])
    # cmds.scriptJob(ct=["busy", busy_proc])
def get_mouse_position(elapsedTime, lastTime, *args):
    x,y = pag.position()
    # print x, y
    if (idle_info.mouse_x == x) & (idle_info.mouse_y == y):
        if not idle_info.start_time:
            idle_info.start_time = datetime.datetime.now()
    else:
        idle_info.mouse_x = x
        idle_info.mouse_y = y

def add_event():
    # om.MMessage().removeCallback(callbackid)
    mevent = om.MEventMessage()
    mevent.addEventCallback("SceneOpened", open_func)
    maya = getMayaWindow()
    cmds.window(maya.objectName(), e=1, closeCommand=close_func)
    # idle_info.id = cmds.scriptJob(idleEvent=idle_proc)
    # cmds.scriptJob(ct=["busy", busy_proc])
    # print "idle_info.id", idle_info.id