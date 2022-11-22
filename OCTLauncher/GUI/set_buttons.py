#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtCore import Slot
import os
from OCTLauncher.core import launch_dcc
import config
from config.GLOBAL import *
import datetime

file_path = OCTLAUNCHERGUIPATH
config_path = OCTLAUNCHERCFGPATH

dcc_btn_data = launch_dcc.get_env_config()


class my_listView(QtGui.QListView):

    def __init__(self, parent=None, config=None):
        super(my_listView, self).__init__(parent)
        self.config = config
        self.__last_click_time = None
        self.setAutoScroll(1)
        self.setAutoScrollMargin(0)
        self.clicked.connect(self.click)

    # @Slot(str)
    # def mouseDoubleClickEvent(self, QMouseEvent):
    #     # print self.currentIndex().row()
    #     widget = self.indexWidget(self.currentIndex())
    #     get_launch(widget, self.config)

    # @Slot(str)
    def click(self, *args, **kwargs):
        time_now = int(str(datetime.datetime.now()).replace(' ', '').replace(':', '').replace('-', '').replace('.', ''))
        widget = self.indexWidget(self.currentIndex())
        if not self.__last_click_time:
            self.__last_click_time = time_now
            get_launch(widget, self.config)
            return
        if time_now - self.__last_click_time < 500000:
            return
        self.__last_click_time = time_now
        get_launch(widget, self.config)


def get_launch(qt_object, launch_config=None):
    user, project = launch_config[0].text().encode('unicode-escape').decode('string_escape'), \
                    launch_config[1].currentText().encode('unicode-escape').decode('string_escape')
    try:
        launch_cmd = launch_dcc.LaunchDCC(qt_object.objectName(), parent=qt_object,
                                          extra_env={'oct_user': user, 'oct_project': project})
    except Exception as e:
        print u'启动程序错误', e
        launch_cmd = launch_dcc.LaunchDCC(qt_object, extra_env={'oct_user': user, 'oct_project': project})
    launch_cmd.launch_dcc()


# def launch_app(py_file=None):
#     try:
#         py_file.main()
#     except:
#         pass


def define_item_model_name(prefix):
    return prefix + "_itemModel"


def define_list_view_name(prefix):
    return prefix + "_listView"


def add_launch_buttons(window, group_box, config=None):
    for box in group_box:
        listView = my_listView(config=config)
        # the name will be like DCC_btn_grp_listView
        listView.setObjectName(define_list_view_name(box.objectName()))
        # set to iconMode
        listView.setViewMode(QtGui.QListView.IconMode)
        # hide frame
        listView.setFrameShape(QtGui.QFrame.NoFrame)
        listView.setParent(box)
        listView.setGeometry(10, 20, 310, 100)
        listView.setFixedHeight(box.height())

        slm = QtGui.QStandardItemModel(listView)
        slm.setObjectName(define_item_model_name(box.objectName()))
        slm.setParent(listView)
        listView.setModel(slm)
    button_list = list(dcc_btn_data.keys())
    login_mode = 0
    user_steps = []
    user = ''
    sg = None
    if os.environ['oct_launcher_using_mode'] in ['online']:
        try:
            from utils import shotgun_operations
            sg = shotgun_operations
            user = sg.get_user()
            user_steps = sg.get_step(user)
            login_mode = 1
        except Exception, e:
            print u'可能是离线登陆模式？', e
    for each_button in button_list:
        if not dcc_btn_data[each_button]['GroupBox']:
            continue
        if login_mode:  # 如果不是离线登陆模式，需要对所有的button进行分组筛选
            if_load = 0
            user_permission = sg.get_permission(user)
            if 'Forbidden' in dcc_btn_data[each_button].keys() and user_permission in dcc_btn_data[each_button]['Forbidden']:
                continue
            if 'Groups' in dcc_btn_data[each_button].keys() and dcc_btn_data[each_button]['Groups']:
                for each_user_step in user_steps:
                    if each_user_step in dcc_btn_data[each_button]['Groups']:
                        if_load = 1
                        break
                if not if_load:
                    continue
        else:   # 如果是， 排除掉所有outsource的工具
            if 'Forbidden' in dcc_btn_data[each_button].keys() and 'outsource' in dcc_btn_data[each_button]['Forbidden']:
                continue
        which_group_box = dcc_btn_data[each_button]['GroupBox']
        item_model_name = define_item_model_name(which_group_box)
        list_view_name = define_list_view_name(which_group_box)
        item_model = window.findChild(QtGui.QStandardItemModel, item_model_name)
        list_view = window.findChild(QtGui.QListView, list_view_name)
        # qqq = window.findChild(QtGui.QListView, define_list_view_name(which_group_box))
        # print qqq, item_model
        pix = QtGui.QPixmap(file_path + "/icons/" + each_button + ".png")
        # print icon
        standard_item = QtGui.QStandardItem(QtGui.QIcon(pix), dcc_btn_data[each_button]['Label'].decode('gbk'))
        standard_item.setDragEnabled(0)
        item_model.appendRow(standard_item)
        index = item_model.indexFromItem(standard_item)
        widget_temp = QtGui.QWidget()
        widget_temp.setMaximumSize(0, 0)
        widget_temp.setObjectName(each_button)
        list_view.setIndexWidget(index, widget_temp)
        # dcc_index_dict[each_button] = item_model.indexFromItem(standard_item).row()
        # print item_model.indexFromItem(standard_item).row()
    return

