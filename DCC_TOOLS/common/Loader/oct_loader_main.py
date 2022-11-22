# coding=utf-8

import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from DCC_TOOLS.common import dcc_utils
import utils.shotgun_operations as sg
import time
from . import oct_loader_ui
reload(oct_loader_ui)


# 获取脚本路径
def resource_inpath():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))
    return ""


class FetchDataThread(QtCore.QThread):
    find_result = QtCore.Signal(list)
    find_one_result = QtCore.Signal(dict)
    finished = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(FetchDataThread, self).__init__(parent)
        self.mode = ''  # find/find_one
        self.mute = 1
        self.data = []  # [['entity_type', filters, fields], [], ...]

    def run(self, *args, **kwargs):
        for each_data in self.data:
            if self.mute:
                if self.mode in ['find']:
                    result = sg.find_shotgun(*each_data)
                    if result and isinstance(result, list):
                        self.find_result.emit(result)
                elif self.mode in ['find_one']:
                    result = sg.find_one_shotgun(*each_data)
                    if result and isinstance(result, dict):
                        self.find_one_result.emit(result)
            else:
                self.mute = 1
                break
        self.finished.emit(1)


class OCT_Losder_Win_Class(QtWidgets.QMainWindow, oct_loader_ui.Ui_MainWindow_OCT_Loader_UI):
    def __init__(self, parent=dcc_utils.getMayaWindow()):
        super(OCT_Losder_Win_Class, self).__init__(parent)
        self.setupUi(self)
        icon_grid = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_grid_active.png"))
        self.toolButton_grid.setIcon(icon_grid)
        icon_list = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_list.png"))
        self.toolButton_list.setIcon(icon_list)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.scale_change_func()
        self.name_project = sg.get_project()
        self.tabWidget.setTabText(0, u"项目: {}".format(self.name_project))
        self.build_connect()
        self.listWidget_history.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget_history.setIconSize(QtCore.QSize(220, 220))

        self.listWidget_no_version.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget_no_version.setIconSize(QtCore.QSize(220, 220))

        #  多线程
        self.find_asset_tree_thread = FetchDataThread()
        self.find_asset_tree_thread.mode = 'find'
        self.find_asset_tree_thread.find_result.connect(self.arrange_asset_tree_items)

        self.find_shot_tree_thread = FetchDataThread()
        self.find_shot_tree_thread.mode = 'find'
        self.find_shot_tree_thread.find_result.connect(self.arrange_shot_tree_items)

        self.find_version_thread = FetchDataThread()
        self.find_version_thread.mode = 'find'
        self.find_version_thread.find_result.connect(self.arrange_asset_task_img)
        self.find_version_thread.finished.connect(self.finish_arrange_asset_task_img)

        self.listWidget_dir = {}

        self.refresh_asset_tree()

    def build_connect(self):
        self.toolButton_grid.clicked.connect(self.grid_clicked_func)
        self.toolButton_list.clicked.connect(self.list_clicked_func)
        self.toolButton_dateils.clicked.connect(self.show_hide_datelis)
        self.treeWidget_project.itemClicked.connect(self.item_change_func)
        self.horizontalSlider.valueChanged.connect(self.scale_change_func)
        self.listWidget.itemClicked.connect(self.select_task)
        self.lineEdit_find.returnPressed.connect(self.find_asset)
        self.listWidget_history.itemClicked.connect(self.show_update_time0)
        self.listWidget_no_version.itemClicked.connect(self.show_update_time1)

    def grid_clicked_func(self):
        icon_grid = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_grid_active.png"))
        self.toolButton_grid.setIcon(icon_grid)
        self.toolButton_grid.setChecked(1)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.scale_change_func()
        icon_list = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_list.png"))
        self.toolButton_list.setIcon(icon_list)
        self.toolButton_list.setChecked(0)
        self.frame_scale.setVisible(1)

    def list_clicked_func(self):
        icon_grid = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_grid.png"))
        self.toolButton_grid.setIcon(icon_grid)
        self.toolButton_grid.setChecked(0)
        icon_list = QtGui.QIcon(os.path.join(resource_inpath(), "icons/mode_list_active.png"))
        self.toolButton_list.setIcon(icon_list)
        self.toolButton_list.setChecked(1)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.frame_scale.setVisible(0)

    def show_hide_datelis(self):
        if self.groupBox_right.isVisible():
            self.groupBox_right.setVisible(0)
            self.toolButton_dateils.setText("Show Details")
        else:
            self.groupBox_right.setVisible(1)
            self.toolButton_dateils.setText("Hide Details")

    def scale_change_func(self):
        num = self.horizontalSlider.value()
        self.listWidget.setIconSize(QtCore.QSize(num, num))

    def refresh_asset_tree(self):
        self.statusbar.showMessage(u"正在刷新...")
        self.treeWidget_project.clear()
        # asset item
        # get task list
        filters = [["project", "name_is", self.name_project],
                   ["entity", "is_not", None],
                   ["entity.Asset.sg_asset_type", "is_not", None],
                   ["step", "is_not", None],
                   ["sg_status_list", "is_not", "omt"]]
        fields = ["code", "entity.Asset.sg_asset_type", "step", "sg_status_list"]
        # task_asset_list = sg.find_shotgun("Task", filters, fields)
        self.find_asset_tree_thread.data = [["Task", filters, fields]]
        self.find_asset_tree_thread.start()


    def arrange_asset_tree_items(self, tree_data):
        item_asset = QtWidgets.QTreeWidgetItem(self.treeWidget_project)
        item_asset.setText(0, "Asset")
        item_asset.setText(1, "Asset")
        self.type_step_dir = {}
        for task in tree_data:
            task_type = task["entity.Asset.sg_asset_type"]
            task_step = task["step"]["name"]
            if not self.type_step_dir.has_key(task_type):
                self.type_step_dir[task_type] = {"item": None, "steps": []}
                item_type = QtWidgets.QTreeWidgetItem(item_asset)
                icon_item = QtGui.QIcon()
                icon_item.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_{}.png".format(task_type))),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item_type.setIcon(0, icon_item)
                item_type.setText(0, task_type)
                item_type.setText(1, "Asset {}".format(task_type))
                self.type_step_dir[task_type]["item"] = item_type
            if task_step not in self.type_step_dir[task_type]["steps"]:
                item_step = QtWidgets.QTreeWidgetItem(self.type_step_dir[task_type]["item"])
                icon_item = QtGui.QIcon()
                icon_item.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_{}.png".format(task_step))),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item_step.setIcon(0, icon_item)
                item_step.setText(0, task_step)
                item_step.setText(1, "Asset {} {}".format(task_type, task_step))
                self.type_step_dir[task_type]["steps"].append(task_step)
        self.refresh_shot_tree()


    def item_change_func(self, *args):
        self.find_version_thread.mute = 0
        self.find_version_thread.data = []
        self.middle_dir = {}
        self.statusbar.showMessage(u"正在刷新...")
        # self.listWidget.clear()
        self.listWidget_history.clear()
        self.listWidget_no_version.clear()
        item_active = self.treeWidget_project.currentItem()
        if not item_active.text(1):
            return
        item_info = item_active.text(1)
        if item_info.count(" ") != 2:
            self.statusbar.showMessage(u"列表为空...")
            return
        # if not self.middle_dir.has_key(item_info):
        #     self.middle_dir[item_info] = {}
        info_list = item_info.split(" ")
        self.listWidget_dir = {}
        if info_list[0] == "Asset":
            filters_task = [["project", "name_is", self.name_project],
                            ["entity", "is_not", None],
                            ["entity.Asset.sg_asset_type", "is", info_list[1]],
                            ["step", "name_is", info_list[2]],
                            ["sg_status_list", "is_not", "omt"]]
            fields_task = ["sg_publish_version", "content", "entity"]
            task_asset_list = sg.find_shotgun("Task", filters_task, fields_task)
            for task in task_asset_list:
                if not task["sg_publish_version"]:
                    continue
                filters_version = [["project", "name_is", self.name_project],
                                   ["sg_version_number", "is", task["sg_publish_version"]],
                                   ["sg_version_type", "is", "Publish"],
                                   ["sg_task", "is", task],
                                   # ["entity","name_contains", find]
                                   # [find, "in", "entity_name"]
                                   ]
                fields_version = ["sg_path_to_movie", "sg_task.Task.sg_publish_version", 'sg_task.Task.content',
                                  'sg_task.Task.entity', "sg_task.Task.step"
                                  ]
                # task_version = sg.find_one_shotgun("Version", filters_version, fields_version)

                self.find_version_thread.data.append(["Version", filters_version, fields_version])
                # if not task_version:
                #     continue
            self.find_version_thread.mute = 1
            self.listWidget.clear()
            self.find_version_thread.start()
        else:
            self.listWidget.clear()
            filters = [["project", "name_is", self.name_project],
                       ["entity", "is_not", None],
                       ["entity.Shot.sg_sequence", "name_is", info_list[2]],
                       ["step", "name_is", info_list[1]],
                       # [find, "in", "entity.name"]
                       ]
            fields = ["code", "entity"]
            task_shot_list = sg.find_shotgun("Task", filters, fields)
            shot_list = []
            for shot in task_shot_list:
                shot_list.append(shot["entity"]["name"])

            for name  in sorted(shot_list):
                icon_task = QtGui.QIcon()
                icon_task.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_shot.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item = QtWidgets.QListWidgetItem(self.listWidget)
                item.setIcon(icon_task)
                item.setText(name)
            self.statusbar.showMessage(u"刷新完毕...")

    def arrange_asset_task_img(self, version_info_list):
        # print version_info_list
        # print version_info
        #  version_info: {"sg_path_to_movie": sg_path_to_movie, ...}
        #  self.middle_dir: {环节：{资产名： 缩略图}}
        if not version_info_list:
            return
        item_active = self.treeWidget_project.currentItem()
        # print item_active.text(1)
        if not item_active.text(1):
            return
        for version_info in version_info_list:
            if item_active.text(1).split(" ")[-1] == version_info["sg_task.Task.step"]["name"]:
                txt_find = u"%s" % self.lineEdit_find.text()
                if txt_find in version_info["sg_task.Task.entity"]["name"]:

                    # item_info = item_active.text(1)
                    # self.middle_dir[item_info][version_info["sg_task.Task.entity"]["name"]] = version_info["sg_path_to_movie"]
                    # self.middle_dir[version_info["sg_task.Task.entity"]["name"]] = version_info["sg_path_to_movie"]
                    # self.middle_dir[item_info][task["entity"]["name"]] = task_version["sg_path_to_movie"]
                    num_key = 0
                    while self.listWidget_dir.has_key(num_key):
                        num_key += 1
                    self.listWidget_dir[num_key] = [version_info["sg_task.Task.entity"]["name"], version_info["sg_task.Task.content"]]
                    icon_task = QtGui.QIcon()
                    # print version_info["sg_path_to_movie"]
                    icon_task.addPixmap(QtGui.QPixmap(version_info["sg_path_to_movie"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item = QtWidgets.QListWidgetItem(self.listWidget)
                    item.setIcon(icon_task)
                    item.setText("{}_{}".format(version_info["sg_task.Task.entity"]["name"], version_info["sg_task.Task.content"]))

    def finish_arrange_asset_task_img(self, result):
        if result:
            self.statusbar.showMessage(u"刷新完毕...")

    # from DCC_TOOLS.common.Loader import oct_loader_main
    #
    # reload(oct_loader_main)
    #
    # oct_loader_main.main()


    def select_task(self, *args):
        self.listWidget_history.file_dir = {}
        self.listWidget_history.info_dir = {}
        self.listWidget_no_version.file_dir = {}
        self.listWidget_no_version.info_dir = {}
        self.listWidget_history.clear()
        self.listWidget_no_version.clear()
        item = self.treeWidget_project.currentItem().text(1)
        # print self.listWidget.currentIndex().row()
        # print item
        # asset_name, task_name = self.listWidget.currentItem().data(0).split(";")
        asset_name = self.listWidget.currentItem().data(0)
        # print asset_name, task_name
        if item.startswith("Asset"):
            asset_name, task_name = self.listWidget_dir[self.listWidget.currentIndex().row()]
            filters_task = [["project", "name_is", self.name_project],
                       ["entity", "name_is", asset_name],
                       ["entity.Asset.sg_asset_type", "is_not", None],
                       ["step", "name_is", item.split(" ")[-1]],
                       ["content", "is", task_name]
                            ]
            fields_task = ["code", "entity.Asset.sg_asset_type", "step", "sg_note"]
            task_asset = sg.find_one_shotgun("Task", filters_task, fields_task)
            self.label_task_info.setText(task_asset["sg_note"])
            filters_version = [["project", "name_is", self.name_project],
                       ["sg_task", "is", task_asset],
                       ["sg_version_type", "is", "Publish"]]
            fields_version = ["code", "sg_path_to_movie", "sg_path_to_frames", "updated_at", "user", "description"]
            task_version = sg.find_shotgun("Version", filters_version, fields_version)
            if not task_version:
                return
            no_version = sorted(task_version, key=lambda v: v["code"], reverse=1)[-1]
            print no_version["user"]
            if not self.listWidget_no_version.file_dir.has_key(no_version["code"]):
                self.listWidget_no_version.file_dir[no_version["code"]] = None
                self.listWidget_no_version.time_dir[no_version["code"]] = None
                self.listWidget_no_version.info_dir[no_version["code"]] = None
            self.listWidget_no_version.file_dir[no_version["code"]] = no_version["sg_path_to_frames"]
            update_time = no_version["updated_at"]
            self.listWidget_no_version.time_dir[no_version["code"]] = u"{}-{}-{} {}:{}:{}  {}".format(update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute, update_time.second, no_version["user"]["name"])
            self.listWidget_no_version.info_dir[no_version["code"]] = no_version["description"]
            icon_task = QtGui.QIcon()
            icon_task.addPixmap(QtGui.QPixmap(no_version["sg_path_to_movie"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item = QtWidgets.QListWidgetItem(self.listWidget_no_version)
            item.setIcon(icon_task)
            item.setText(no_version["code"])

            for version in sorted(task_version, key=lambda v: v["code"], reverse=1)[0:-1]:
                if not self.listWidget_history.file_dir.has_key(version["code"]):
                    self.listWidget_history.file_dir[version["code"]] = None
                    self.listWidget_history.time_dir[version["code"]] = None
                    self.listWidget_history.info_dir[version["code"]] = None
                self.listWidget_history.file_dir[version["code"]] = version["sg_path_to_frames"]
                update_time = version["updated_at"]
                self.listWidget_history.time_dir[version["code"]] = u"{}-{}-{} {}:{}:{}  {}".format(
                    update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute,
                    update_time.second, version["user"]["name"])
                self.listWidget_history.info_dir[version["code"]] = version["description"]

                # self.listWidget_history.time_dir[version["code"]] = version["updated_at"]
                icon_task = QtGui.QIcon()
                icon_task.addPixmap(QtGui.QPixmap(version["sg_path_to_movie"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item = QtWidgets.QListWidgetItem(self.listWidget_history)
                item.setIcon(icon_task)
                item.setText(version["code"])
        else:
            filters_shot = [["project", "name_is", self.name_project],
                       ["entity", "name_is", asset_name],
                       ["entity.Shot.sg_sequence", "name_is", item.split(" ")[-1]],
                       ["step", "name_is", item.split(" ")[1]]]
            fields_shot = ["code", "entity", "sg_note"]
            task_shot = sg.find_one_shotgun("Task", filters_shot, fields_shot)
            self.label_task_info.setText(task_shot["sg_note"])
            filters_version = [["project", "name_is", self.name_project],
                       ["sg_task", "is", task_shot],
                       ["sg_version_type", "is", "Publish"]]
            fields_version = ["code", "sg_path_to_movie", "sg_path_to_frames", "updated_at", "user", "description"]
            task_version = sg.find_shotgun("Version", filters_version, fields_version)

            no_version = sorted(task_version, key=lambda v: v["code"], reverse=1)[-1]
            if not self.listWidget_no_version.file_dir.has_key(no_version["code"]):
                self.listWidget_no_version.file_dir[no_version["code"]] = None
                self.listWidget_no_version.time_dir[no_version["code"]] = None
                self.listWidget_no_version.info_dir[no_version["code"]] = None
            self.listWidget_no_version.file_dir[no_version["code"]] = no_version["sg_path_to_frames"]
            # self.listWidget_no_version.time_dir[no_version["code"]] = no_version["updated_at"]
            update_time = no_version["updated_at"]
            self.listWidget_no_version.time_dir[no_version["code"]] = u"{}-{}-{} {}:{}:{}  {}".format(update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute, update_time.second, no_version["user"]["name"])
            self.listWidget_no_version.info_dir[no_version["code"]] = no_version["description"]

            txt_find = u"%s" % self.lineEdit_find.text()
            if txt_find in no_version["code"]:
                icon_task = QtGui.QIcon()
                icon_task.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_shot.png")),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item = QtWidgets.QListWidgetItem(self.listWidget_no_version)
                item.setIcon(icon_task)
                item.setText(no_version["code"])

            for version in sorted(task_version, key=lambda v: v["code"], reverse=1)[0:-1]:
                if not self.listWidget_history.file_dir.has_key(version["code"]):
                    self.listWidget_history.file_dir[version["code"]] = None
                    self.listWidget_history.time_dir[version["code"]] = None
                    self.listWidget_history.info_dir[version["code"]] = None
                self.listWidget_history.file_dir[version["code"]] = version["sg_path_to_frames"]
                # self.listWidget_history.time_dir[version["code"]] = version["updated_at"]
                update_time = version["updated_at"]
                self.listWidget_history.time_dir[version["code"]] = u"{}-{}-{} {}:{}:{}  {}".format(
                    update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute,
                    update_time.second, version["user"]["name"])
                self.listWidget_history.info_dir[version["code"]] = version["description"]

                txt_find = u"%s" % self.lineEdit_find.text()
                if txt_find in version["code"]:
                    icon_task = QtGui.QIcon()
                    icon_task.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_shot.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item = QtWidgets.QListWidgetItem(self.listWidget_history)
                    item.setIcon(icon_task)
                    item.setText(version["code"])

    def show_update_time0(self):
        item = self.listWidget_history.currentItem().data(0)
        update_time = self.listWidget_history.time_dir[item]
        # print dir(update_time)
        # self.label_time.setText("{}-{}-{} {}:{}:{}".format(update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute, update_time.second))
        self.label_time.setText(update_time)
        self.label_version_info.setText(self.listWidget_history.info_dir[item])
        # print update_time

    def show_update_time1(self):
        item = self.listWidget_no_version.currentItem().data(0)
        update_time = self.listWidget_no_version.time_dir[item]
        # self.label_time.setText("{}-{}-{} {}:{}:{}".format(update_time.year, update_time.month, update_time.day, update_time.hour, update_time.minute, update_time.second))
        self.label_time.setText(update_time)
        self.label_version_info.setText(self.listWidget_no_version.info_dir[item])
        # print update_time

    def find_asset(self):
        # self.find_asset_tree_thread.mute = 0
        # self.listWidget.clear()
        # find_one_data =
        txt_find = u"%s" % self.lineEdit_find.text()
        self.item_change_func()
        # for i in range(self.listWidget.count()):
        #     item = self.listWidget.item(i)
        #     if txt_find in item.text():
        #         item.setHidden(0)
        #     else:
        #         item.setHidden(1)

    def refresh_shot_tree(self):
        # get task list
        filters = [["project", "name_is", self.name_project],
                   ["entity", "is_not", None],
                   ["entity.Asset.sg_asset_type", "is", None],
                   ["step", "is_not", None]]
        fields = ["code", "step", "entity", "entity.Shot.sg_sequence"]
        # task_shot_list = sg.find_shotgun("Task", filters, fields)
        self.find_shot_tree_thread.data = [["Task", filters, fields]]
        self.find_shot_tree_thread.start()


    def arrange_shot_tree_items(self, tree_data):
        # asset item
        item_shot = QtWidgets.QTreeWidgetItem(self.treeWidget_project)
        item_shot.setText(0, "Shot")
        item_shot.setText(1, "Shot")
        self.step_seq_dir = {}
        for task in tree_data:
            try:
                step = task["step"]["name"]
                sequence = task["entity.Shot.sg_sequence"]["name"]
                if not self.step_seq_dir.has_key(step):
                    self.step_seq_dir[step] = [sequence]
                else:
                    if sequence not in self.step_seq_dir[step]:
                        self.step_seq_dir[step].append(sequence)
            except:
                pass
        for st in sorted(self.step_seq_dir.keys()):
            item_st = QtWidgets.QTreeWidgetItem(item_shot)
            icon_item = QtGui.QIcon()
            icon_item.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_{}.png".format(st))),
                                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item_st.setIcon(0, icon_item)
            item_st.setText(0, st)
            item_st.setText(1, "Shot {}".format(st))
            for sq in sorted(self.step_seq_dir[st]):

                item_sq = QtWidgets.QTreeWidgetItem(item_st)
                icon_item = QtGui.QIcon()
                icon_item.addPixmap(QtGui.QPixmap(os.path.join(resource_inpath(), "icons/icon_{}.png".format("sequence"))),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item_sq.setIcon(0, icon_item)
                item_sq.setText(0, sq)
                item_sq.setText(1, "Shot {} {}".format(st, sq))
        self.statusbar.showMessage(u"刷新完成！")


def takeCode(elem):
    return elem["code"]


def main():
    win = OCT_Losder_Win_Class()
    win.show()
    return win