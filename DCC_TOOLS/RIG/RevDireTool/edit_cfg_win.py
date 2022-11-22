#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/1/22

__author__ = "dango wang"

import loadUiType
import os
import maya.cmds as mc
import table_widget_methods
reload(table_widget_methods)
import yaml
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore


file_path = str(os.path.split(os.path.realpath(__file__))[0])
record_form, record_base = loadUiType.loadUiType(file_path+'\\record_reversing_attr.ui')
add_attr_record, add_record = loadUiType.loadUiType(file_path+'\\add_attr_dialog.ui')
special_save_form, special_save_base = loadUiType.loadUiType(file_path+'\\special_save.ui')
cfg_path = file_path + "\\config\\reverse_attr_cfg.yaml"


class RecordAttrWin(record_base, record_form):
    def __init__(self):
        super(RecordAttrWin, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)
        self.add_attr_win = AddAttrDialog()
        self.special_save = SpecialSave(self)
        # self.add_attr_win.setParent(self)
        self.add_attr_win.pushButton.clicked.connect(self.add_item)
        self.add_attr_pushButton.clicked.connect(self.add_attr_win.show)
        self.load_attr_pushButton.clicked.connect(self.arrange_items)
        self.delete_attr_pushButton.clicked.connect(self.delete_item)
        self.clear_pushButton.clicked.connect(self.clear_items)
        self.save_cfg_pushButton.clicked.connect(self.save_cfg)
        self.special_save.special_save_pb.clicked.connect(self.special_save_cfg)
        self.special_save_cfg_pushButton.clicked.connect(self.special_save.show)
        self.arrange_items()
        self.add_script_job()

    def add_item(self):
        ctrl_name = table_widget_methods.get_contents(self.add_attr_win.tableWidget)['AnimCrv']
        existing_attr_name = table_widget_methods.get_contents(self.tableWidget)['AnimCrv']
        attr_name = self.add_attr_win.lineEdit_3.text().strip(" ")
        all_attr_name = attr_name.split(" ")
        for each_attr_name in all_attr_name:
            if not (ctrl_name and each_attr_name):
                raise RuntimeError("Plz fill all info needed!")
            for each_ctrl in ctrl_name:
                item_label = each_ctrl + "_" + each_attr_name
                if item_label not in existing_attr_name:
                    table_widget_methods.add_item(self.tableWidget, item_label)
        return True

    def add_script_job(self):
        mc.scriptJob(parent=self.objectName(), event=["SelectionChanged", self.arrange_items])

    def arrange_items(self):
        which_char = self.which_char_le.text()
        if which_char:
            cfg_path_temp = file_path + "\\config\\"+which_char+"\\reverse_attr_cfg.yaml"
            with open(cfg_path_temp, 'r') as f:
                data = yaml.load(f)
            data_sorted = list(set(data['AnimCrv']))
            table_widget_methods.clear_all_items(self.tableWidget)
            table_widget_methods.set_all_items(self.tableWidget, data_sorted)
            return
        selected_char_temp = mc.ls(sl=True)
        selected_char = str()
        if selected_char_temp:
            selected_char = selected_char_temp[0]
        cfg_path2 = cfg_path
        self.char_label.setText(u"通用")
        if selected_char and mc.referenceQuery(selected_char, inr=1):
            file_ = mc.referenceQuery(selected_char, f=1)
            char_name = file_.split("/")[-1].rstrip(".ma")
            cfg_path2 = file_path + "\\config\\"+char_name+"\\reverse_attr_cfg.yaml"
            self.char_label.setText(char_name)
            if not os.path.isfile(cfg_path2):
                cfg_path2 = cfg_path
                self.char_label.setText(u"通用")
        with open(cfg_path2, 'r') as f:
            data = yaml.load(f)
        data_sorted = list(set(data['AnimCrv']))
        table_widget_methods.clear_all_items(self.tableWidget)
        table_widget_methods.set_all_items(self.tableWidget, data_sorted)
        # print data['AnimCrv'][0]
        return True

    def delete_item(self):
        table_widget_methods.delete_items(self.tableWidget)
        return True

    def clear_items(self):
        table_widget_methods.clear_all_items(self.tableWidget)
        return True

    def save_cfg(self):
        cfg_info = table_widget_methods.get_contents(self.tableWidget)['AnimCrv']
        cfg_sorted = list(set(cfg_info))
        cfg_sorted.sort(key=cfg_info.index)
        table_widget_methods.save_cfg({'AnimCrv': cfg_sorted}, cfg_path)
        return True

    def special_save_cfg(self):
        cfg_info = table_widget_methods.get_contents(self.tableWidget)['AnimCrv']
        cfg_sorted = list(set(cfg_info))
        cfg_sorted.sort(key=cfg_info.index)
        char_name = self.special_save.special_save_le.text()
        char_cfg_dir = file_path + "\\config\\"+char_name
        if not os.path.isdir(char_cfg_dir):
            os.mkdir(char_cfg_dir)
        table_widget_methods.save_cfg({'AnimCrv': cfg_sorted}, char_cfg_dir + "\\reverse_attr_cfg.yaml")
        return True


class AddAttrDialog(add_record, add_attr_record):
    def __init__(self, parent=None):
        super(AddAttrDialog, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)
        # table_widget_methods.clear_all_items(self.tableWidget)
        self.clear_pushButton.clicked.connect(self.clear_contents)

    def clear_contents(self):
        table_widget_methods.clear_all_items(self.tableWidget)
        return True


class SpecialSave(special_save_base, special_save_form):
    def __init__(self, parent=None):
        super(SpecialSave, self).__init__(parent=parent)
        self.setupUi(self)