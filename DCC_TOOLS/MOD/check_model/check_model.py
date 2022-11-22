#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/1/7
import os
import sys
import logging
import loadUiType
from PySide2.QtCore import Slot
from operator import methodcaller
try:
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import QWidget
    import PySide.QtGui as QtWidgets
    from shiboken import wrapInstance
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui
import model_check_list
reload(model_check_list)


file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType.loadUiType(file_path+'\\check_model.ui')
my_maya_document_path = cmds.internalVar(userAppDir=True) + "model_check_items.json"
config_path = file_path + '\\config\\'

legal_assemblies = ['persp', 'top', 'front', 'side']
except_grp_names = ["high", "low", "fx", "cfx", "Geometry", "blendshape"]
env_grp = {"Geometry":
               ["high",
                "low",
                ]}

char_grp = {"Geometry":
               ["blendshape",
                {"high":
                    [{"body_Grp": [
                            {"eye_Grp": [
                                "eye_L_Grp",
                                "eye_R_Grp"]},
                            "mouthcavity_Grp",
                            "fingernail_Grp"]},
                        "prop_Grp",
                        "clothes_Grp"]},
                "low",
                "temp"]}

ch_uncheck = ['check_intersection_cb', 'check_more_cvs_cb', 'check_nonmanifold_cb', 'check_nonplanar_cb',
              'check_concave_cb', 'check_nouv_faces_cb']
env_uncheck = ["check_lamina_faces_cb", "check_nonmanifold_cb", "check_more_faces_cb", "check_more_cvs_cb",
               "check_intersection_cb", "check_pivot_cb", "check_freeze_cb", "check_nonplanar_cb", "check_concave_cb",
               "check_holes_cb"]


def undoable(function):
    # A decorator that will make commands undoable in maya
    def decoratorCode(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print sys.exc_info()[1]

        finally:
            cmds.undoInfo(closeChunk=True)
            return functionReturn
    return decoratorCode


def get_all_mesh_shape():
    """
    get all mesh_shapes
    :return: mesh shapes
    """
    return cmds.ls(type="mesh", sn=1)


def get_mesh_transform(mesh_shape):
    """
    :param mesh_shape:
    :return:list of all mesh transforms
    """
    mesh_parent = cmds.listRelatives(mesh_shape, ap=1, type="transform")
    return mesh_parent


def get_all_mesh_transforms(shapes):
    """
    :param shapes: []
    :return: [[],[],[]...]
    """
    return map(get_mesh_transform, shapes)


def get_all_spec_nodes(node_type="transform", except_node_type='camera'):
    all_spec_nodes = cmds.ls(type=node_type, sn=1)
    all_except_nodes = cmds.ls(type=except_node_type, sn=1)
    return [each for each in all_spec_nodes if each not in
            [cmds.listRelatives(each_cam, p=1)[0] for each_cam in all_except_nodes]]


def get_error_transforms(transform_list):
    """
    :param transform_list: [a,[],[]...]
    :return:
    """
    return [etl for etl in transform_list if len(etl) > 1]


def get_right_transforms(transform_list):
    """
    :param transform_list: [[],[],...]
    :return:
    """
    transforms = list()
    for each in transform_list:
        if isinstance(each, list):
            transforms.extend(each)
        else:
            return False
    return transforms


def get_all_grps(node_type, mesh_transforms):
    all_nodes = get_all_spec_nodes(node_type)
    # print all_nodes
    return [each_grp for each_grp in all_nodes if each_grp not in mesh_transforms]


def get_repeating_transforms(str_list):
    """
    :param str_list: right transforms
    :return:
    """
    repeating_list = list()
    for each in str_list:
        if "|" in each:
            repeating_list.append(each.encode("utf-8"))
    if repeating_list:
        return repeating_list
    else:
        return False


def rename_grp(grp_str):
    if "_Grp" not in grp_str:
        # print grp_str
        renamed_str = str()
        if "_Low" not in grp_str:
            renamed_str = grp_str+"_Grp"
        else:
            renamed_str = grp_str.replace("_Low", "_Grp")
        cmds.rename(grp_str, renamed_str)
        return grp_str.encode("utf-8"), renamed_str.encode("utf-8")
    else:
        return str()


def rename_mesh_transform(mesh_transform):
    if "_Geo" not in mesh_transform:
        renamed_str = str()
        if "_Low" not in mesh_transform:
            renamed_str = mesh_transform + "_Geo"
        else:
            renamed_str = mesh_transform.replace("_Low", "_Geo")
        cmds.rename(mesh_transform, renamed_str)
        return mesh_transform.encode("utf-8"), renamed_str.encode("utf-8")
    else:
        return str()


def rename_low_name(mesh_transform):
    if "_Geo" not in mesh_transform and "_Low" not in mesh_transform:
        cmds.rename(mesh_transform, mesh_transform + "_Low")
    elif "_Geo" in mesh_transform:
        cmds.rename(mesh_transform, mesh_transform.replace("_Geo", "_Low"))
    return True


def get_selection():
    selection_list = cmds.ls(sl=True)
    if not selection_list:
        return False
    else:
        return selection_list


def get_all_selection_children(selection_list):
    return_list = list()
    for each in selection_list:
        all_children = cmds.listRelatives(each, c=1, ad=1, type='transform')
        if all_children:
            return_list.extend(all_children)
    return_list.extend(selection_list)
    return return_list


def create_grp(grp_type, parent_grp="Geometry"):
    for k, v in grp_type.items():
        if k == "Geometry":
            if not cmds.objExists(k):
                cmds.createNode("transform", name=k)
        else:
            if not cmds.objExists(k):
                cmds.createNode("transform", name=k, parent=parent_grp)
        for each in v:
            if isinstance(each, str):
                if not cmds.objExists(each):
                    cmds.createNode("transform", name=each, parent=k)
            elif isinstance(each, dict):
                create_grp(each, parent_grp=k)


def rename_obj(selection_list):
    if not selection_list:
        return False
    mesh_transform_list = list()
    all_transforms_list = selection_list
    for each in selection_list:
        all_mesh = cmds.listRelatives(each, c=1, ad=1, type="mesh")
        all_transforms = cmds.listRelatives(each, c=1, ad=1, type="transform")
        if all_mesh:
            for e in all_mesh:
                mesh_transform_list.extend(cmds.listRelatives(e, ap=1, type="transform"))
        if all_transforms:
            all_transforms_list.extend(all_transforms)
    all_grp_list = list(set(list(filter(None, [grp for grp in all_transforms_list if grp not in mesh_transform_list]))))
    mesh_transform_list = list(set(mesh_transform_list))
    map(rename_grp, all_grp_list)
    map(rename_mesh_transform, mesh_transform_list)


def raise_confirm_dialog(text):
    confirm_dialog = QtWidgets.QMessageBox()
    if len(text) > 500:
        text = text[:500] + "..."
    confirm_dialog.setText(text)
    confirm_dialog.setWindowTitle(u"提示")
    confirm_dialog.addButton(u"自动处理", QtWidgets.QMessageBox.AcceptRole)  # role 0
    confirm_dialog.addButton(u"场景查看", QtWidgets.QMessageBox.RejectRole)  # role 1
    confirm_dialog.addButton(u"忽略", QtWidgets.QMessageBox.DestructiveRole)  # role 2
    return confirm_dialog.exec_()


def raise_warning_dialog(parent, text):
    return QtWidgets.QMessageBox().warning(parent, u'warning', text, QtWidgets.QMessageBox.Yes)


class CheckModel(base_class, form_class):
    result_signal = QtCore.Signal(int)

    def __init__(self, task_dict=None, parent=None):
        super(CheckModel, self).__init__(parent=loadUiType.getMayaWindow())
        if task_dict is None:
            task_dict = {}
        self.setupUi(self)
        self.task_dict = task_dict
        # cmds.OutlinerWindow()
        # self._outliner = None
        # self._out_parent = None
        # self._outliner_panel = mel.eval("outlinerPanel -menuBarVisible true -label `localizedPanelLabel(\"Outliner\")`;")
        # self.setup_outliner_panel()
        self.connect_signals()
        self.check_char.clicked.connect(self.on_check_model_clicked)
        # self.set_selecting_items()
        self.check_all.stateChanged.connect(self.check_all_items)
        self.tabWidget.currentChanged.connect(self.set_selecting_items)

    def check_all_items(self):
        needed_checks = [self.check_unknown_nodes_cb, self.check_unknown_plugins_cb, self.check_history_cb,
                         self.check_extra_wins_cb, self.check_display_mode_cb, self.check_hierarchy,
                         self.check_renaming, self.check_instance]
        all_check_items = self.checking_items_widget.children()
        all_check_items.remove(self.check_all)
        all_check_items.remove(self.line_8)
        for cb in needed_checks:
            all_check_items.remove(cb)
        if self.check_all.isChecked():
            for each in all_check_items:
                try:
                    each.setChecked(1)
                except AttributeError:
                    continue
        else:
            for each in all_check_items:
                try:
                    if self.tabWidget.currentIndex() == 0:
                        each.setChecked(0)
                        # self.set_selecting_items()
                    else:
                        each.setChecked(1)
                        if each.objectName() in ch_uncheck:
                            each.setChecked(0)
                except AttributeError:
                    continue
        return True

    def reset_settings(self):
        needed_checks = [self.check_unknown_nodes_cb, self.check_unknown_plugins_cb,
                         self.check_history_cb, self.check_extra_wins_cb,
                         self.check_display_mode_cb, self.check_hierarchy, self.check_instance, self.check_namespace_cb]
        all_check_items = self.checking_items_widget.children()
        all_check_items.remove(self.check_all)
        all_check_items.remove(self.line_8)
        for cb in needed_checks:
            all_check_items.remove(cb)
        for each in all_check_items:
            try:
                each.setChecked(1)
                if self.tabWidget.currentIndex() == 1:
                    if each.objectName() in ch_uncheck:
                        each.setChecked(0)
                    # else:
                    #     each.setEnabled(0)
            except AttributeError:
                continue

    def set_selecting_items(self):
        # self.reset_settings()
        if self.tabWidget.currentIndex() == 1:
            self.reset_settings()
        # current_type = 'env' if current_tab == 0 else ''
        # if not current_type:
        #     return
        # settings = env_uncheck
        # for each in settings:
        #     cb = self.findChild(QtWidgets.QCheckBox, each)
        #     if cb:
        #         cb.setChecked(0)
        #         cb.setEnabled(0)
        return True

    # def closeEvent(self, event):
        # self.save_selected_items()
    #     event.accept()

    # def save_selected_items(self):
    #     all_check_items = self.get_checking_items()
    #     all_check_items.extend([self.check_instance, self.check_renaming])
    #     checking_cfg = list()
    #     for each in all_check_items:
    #         if not each.isChecked():
    #             checking_cfg.append(each.objectName())
    #     with open(my_maya_document_path, 'w') as f:
    #         json.dump(checking_cfg, f)
    #     return True

    def setup_outliner_panel(self):
        outliner_panel = omui.MQtUtil.findControl(self._outliner_panel)
        outliner_widget = wrapInstance(long(outliner_panel), QWidget)
        self._outliner = outliner_widget.parent().parent()
        self._out_parent = outliner_widget.parent().parent().parent()
        self._outliner.setMinimumSize(290, 640)
        self.outliner_grid_layout.addWidget(self._out_parent)

    def connect_button_signal(self, button_widget):
        # print 2
        button_name = button_widget.objectName()
        if "low_pb" in button_name:
            return
        grp_name = button_name.replace("_env_pb", "").replace("_pb", "")
        button_widget.clicked.connect(lambda: self.parent_to_grp(grp_name))

    @undoable
    def parent_to_grp(self, grp_name):
        selection = get_selection()
        if cmds.objExists(grp_name):
            cmds.parent(selection, grp_name)
            selection_children = get_all_selection_children(selection)
            self.check_repeating_names_func()
            rename_obj(selection_children)
            # map(rename_mesh_transform, selection)
        else:
            logging.error(u"未发现组%s，请确保已经正确创建了层级！！\n" % grp_name)
            return False
        return True

    def get_all_buttons(self):
        all_env_children_widget = self.env_tab.children()
        all_ch_children_widget = self.ch_tab.children()
        all_env_children_widget.extend(all_ch_children_widget)
        all_pb = [pb for pb in all_env_children_widget if "_pb" in pb.objectName()]
        return all_pb

    def connect_signals(self):
        all_buttons = self.get_all_buttons()
        map(self.connect_button_signal, all_buttons)

    def get_current_text(self):
        return self.textBrowser.toPlainText()

    def set_current_text(self, text):
        current_text = self.get_current_text()
        self.textBrowser.setText(current_text + text)

    @staticmethod
    def create_top_grp(grp_name):
        if not cmds.objExists(grp_name):
            cmds.createNode("transform", name=grp_name)
        return True

    @staticmethod
    def check_instance_copy():
        all_shapes = get_all_mesh_shape()
        all_mesh_transforms = get_all_mesh_transforms(all_shapes)
        all_error_transforms = get_error_transforms(all_mesh_transforms)
        if all_error_transforms:
            select_str = list()
            for each in all_error_transforms:
                select_str.extend(each)
            cmds.select(select_str, replace=True)
            return u"以下节点instance copy未处理！\n%s\n" % all_error_transforms
        return None

    @staticmethod
    def fix_instance_copy():
        return u"请在场景中手动处理！"

    @staticmethod
    def check_repeating_names():
        all_transforms = get_all_spec_nodes("transform")
        repeating_transforms = get_repeating_transforms(all_transforms)
        if repeating_transforms:
            cmds.select(repeating_transforms, r=True)
            return u"以下节点名称存在重复！请处理...\n%s\n" % repeating_transforms
        return None

    @staticmethod
    @undoable
    def fix_repeating_names():
        all_transforms = get_all_spec_nodes("transform")
        repeating_transforms = get_repeating_transforms(all_transforms)
        all_repeating_names = list(set([e.split('|')[-1] for e in repeating_transforms]))
        for each in all_repeating_names:
            repeating_objs = cmds.ls(each)
            i = 0
            while len(repeating_objs) > 1:
                cmds.rename(repeating_objs[0], each+str(i))
                i += 1
                repeating_objs = cmds.ls(each)
        return

    @staticmethod
    @undoable
    def create_rename_grps(grp_name, grp_type):
        # all_shapes = get_all_mesh_shape()
        # all_mesh_transforms = get_all_mesh_transforms(all_shapes)
        # all_right_transforms = get_right_transforms(all_mesh_transforms)
        # all_grps_temp = get_all_grps("transform", all_right_transforms)
        # all_grps = [each_grp for each_grp in all_grps_temp if each_grp not in except_grp_names]
        # renamed_grp = map(rename_grp, all_grps)
        # renamed_transform = map(rename_mesh_transform, all_right_transforms)
        # renamed_grp.extend(renamed_transform)
        # renamed_grp = list(filter(None, renamed_grp))
        # logging.info(u"已完成以下重命名：%s\n" % renamed_grp)
        if not cmds.objExists("Geometry"):
            create_grp(grp_type)
            cmds.parent("Geometry", grp_name)
            logging.info(u"已为您创建组Geometry\n")
        else:
            logging.error(u"组Geometry已经存在！！无法重复创建...\n")
        return True

    @Slot(name="on_rename_model_clicked")
    def on_rename_model_clicked(self):
        # check instance copy error
        env_name = self.env_name.text()
        if not env_name:
            logging.error(u"请输入场景名！！\n")
            return
        self.create_top_grp(env_name)
        which_quality = 'high' if not self.high_env_rb.isChecked() else 'low'
        env_grp_final = env_grp
        env_grp_final['Geometry'].remove(which_quality)
        self.create_rename_grps(env_name, env_grp_final)
        env_grp_final['Geometry'].append(which_quality)
        return True

    @Slot(name="on_rename_char_clicked")
    def on_rename_char_clicked(self):
        char_name = self.char_name.text()
        if not char_name:
            logging.error(u"请输入角色名！！\n")
            return
        self.check_instance_copy()
        self.check_repeating_names()
        self.create_top_grp(char_name)
        self.create_rename_grps(char_name, char_grp)
        return True

    # @Slot(name="on_low_env_pb_clicked")
    # def on_low_env_pb_clicked(self):
    #     selection = get_selection()
    #     if selection:
    #         if cmds.objExists("low"):
    #             cmds.parent(selection, "low")
    #             map(rename_obj, selection)
    #         else:
    #             logging.error(u"未发现组low，请确保已经正确创建了层级！！\n")
    #             return False
    #     return True

    @Slot(name="on_low_pb_clicked")
    def on_low_pb_clicked(self):
        selection = get_selection()
        if selection:
            if cmds.objExists("low"):
                cmds.parent(selection, "low")
                map(rename_low_name, selection)
            else:
                logging.error(u"未发现组low，请确保已经正确创建了层级！！\n")
                return False
        return True

    def check_instance_func(self):
        if self.check_instance.isChecked():
            label = self.findChild(QtWidgets.QLabel, self.check_instance.objectName() + "_lb")
            message = self.check_instance_copy()
            if message:
                label.setStyleSheet('background-color: rgb(255, 0, 4);')
                dlg = raise_confirm_dialog(message)
                if dlg == 0:
                    warning_text = self.fix_instance_copy()
                    if warning_text:
                        raise_warning_dialog(self, warning_text)
                        return False
                elif dlg == 2:
                    return True
                return False
            else:
                label.setStyleSheet('background-color: rgb(0, 255, 8);')
        return True

    def check_repeating_names_func(self):
        if self.check_renaming.isChecked():
            label = self.findChild(QtWidgets.QLabel, self.check_renaming.objectName() + "_lb")
            message = self.check_repeating_names()
            if message:
                label.setStyleSheet('background-color: rgb(255, 0, 4);')
                dlg = raise_confirm_dialog(message)
                if dlg == 0:
                    warning_text = self.fix_repeating_names()
                    if warning_text:
                        raise_warning_dialog(self, warning_text)
                    else:
                        return True
                elif dlg == 2:
                    return True
                return False
            else:
                label.setStyleSheet('background-color: rgb(0, 255, 8);')
        return True

    def get_checking_items(self):
        all_items = self.checking_items_widget.children()
        all_cb = [cb for cb in all_items if "_cb" in cb.objectName()]
        return all_cb

    def check_geometry(self):
        camera_grp = {'persp', 'top', 'front', 'side'}
        all_top_grp = cmds.ls(assemblies=True)
        model = list(set(all_top_grp) - camera_grp)
        if len(model) > 1:
            return u'大纲中发现多个层级！！\n %s' % model
        # if self.task_dict:
        #     if not model[0] != self.task_dict['name']:
        #         return u'资产命名不正确！！请检查\n%s ' % model[0]
        if not cmds.objExists('Geometry'):
            return u'未发现组Geometry！请检查...'
        if self.tabWidget.currentIndex() == 0:
            child1 = cmds.listRelatives(model[0], c=1)
            child2 = cmds.listRelatives(child1[0], c=1)
            if len(child1) > 1 or len(child2) > 1 or child1[0] != 'Geometry' or child2[0] not in ['high', 'low']:
                return u'以下层级可能不正确！请核对标准。。。\n%s' % [child1, child2]
        else:
            all_ch_children_widget = self.ch_tab.children()
            all_allowed_grp = [pb.objectName().replace('_pb', '')
                               for pb in all_ch_children_widget if "_pb" in pb.objectName()]
            missing_grps = []
            allowed_missing_grps = ['eye_Grp', 'eye_L_Grp',
                                    'eye_R_Grp', 'mouthcavity_Grp', 'fingernail_Grp']
            for each in all_allowed_grp:
                if each not in allowed_missing_grps:
                    if not cmds.objExists(each):
                        missing_grps.append(each)
            if missing_grps:
                return u'以下层级未发现,请检查：%s\n' % missing_grps
        return None

    @Slot(name="on_check_model_clicked")
    def on_check_model_clicked(self):
        if self.check_hierarchy.isChecked():
            geometry_wrong = self.check_geometry()
            if geometry_wrong:
                self.check_hypergraph_lb.setStyleSheet('background-color: rgb(255, 0, 4);')
                answer = raise_confirm_dialog(geometry_wrong)
                if answer != 2:
                    raise_warning_dialog(self, u'请手动处理！')
                    return
            else:
                self.check_hypergraph_lb.setStyleSheet('background-color: rgb(0, 255, 8);')

        check_repeating_names = self.check_repeating_names_func()
        if not check_repeating_names:
            return False

        check_instance_copy = self.check_instance_func()
        if not check_instance_copy:
            return False

        all_checking_checkboxes = self.get_checking_items()
        for each_cb in all_checking_checkboxes:
            each_label = self.findChild(QtWidgets.QLabel, each_cb.objectName().replace("_cb", "_lb"))
            if each_cb.isChecked():
                check_func_name = each_cb.objectName().replace("_cb", "_func")
                fix_func_name = check_func_name.replace("check", "fix")
                check_result = methodcaller(check_func_name)(model_check_list)
                if check_result:
                    each_label.setStyleSheet('background-color: rgb(255, 0, 4);')
                    check_answer = raise_confirm_dialog(check_result)
                    if check_answer == 0:
                        fix_result = methodcaller(fix_func_name)(model_check_list)
                        if fix_result:
                            raise_warning_dialog(self, fix_result)
                            return False
                        each_label.setStyleSheet('background-color: rgb(0, 255, 8);')
                    elif check_answer == 1:
                        return False
                    else:
                        continue
                else:
                    each_label.setStyleSheet('background-color: rgb(0, 255, 8);')
        if_checking_dialog = QtWidgets.QMessageBox()
        if_checking_dialog.setText(u'确定已经完成所有的检测项吗？')
        if_checking_dialog.setWindowTitle(u"提示")
        if_checking_dialog.addButton(u"是的，可以确认提交了", QtWidgets.QMessageBox.AcceptRole)  # role 0
        if_checking_dialog.addButton(u"等等，我再看看", QtWidgets.QMessageBox.RejectRole)  # role 1
        if_checking_finished = if_checking_dialog.exec_()
        if not if_checking_finished:
            self.result_signal.emit(1)
            return True
        else:
            self.result_signal.emit(0)
            return False

    # @Slot(name="on_check_char_clicked")
    # def on_check_char_clicked(self):
    #     # print 2
    #     a = self.check_instance_copy()
    #     b = self.check_repeating_names()
    #     # if a and b:
    #     #     logging.info(u"未发现instance复制和重命名...\n")

