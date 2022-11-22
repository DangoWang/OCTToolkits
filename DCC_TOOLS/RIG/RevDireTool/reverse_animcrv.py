#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/1/25

import maya.cmds as mc
import pymel.core as pm
import loadUiType
import os, logging
import edit_cfg_win
import table_widget_methods
reload(edit_cfg_win)
reload(table_widget_methods)
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide import QtGui as QtWidgets


def get_all_selection():
    selected_obj = mc.ls(sl=True)
    if not selected_obj:
        raise RuntimeError(u"请先选择控制器！")
    return selected_obj


def get_num_keys(ani_crv):
    """
    return type: int
    """
    return pm.PyNode(ani_crv).numKeys()


def get_ani_value(ani_crv):
    """
    [1.24,25.45,3...]
    """
    return [pm.PyNode(ani_crv).getValue(i) for i in xrange(get_num_keys(ani_crv))]


def reverse_ani_crv(attr):
    temp_dict = {"translateX": "inputBX", "translateY": "inputBY", "translateZ": "inputBZ"}
    temp_dict2 = {"rotateX": "inputBX", "rotateY": "inputBY", "rotateZ": "inputBZ"}
    all_crvs = get_all_selection()
    for each_crv in all_crvs:
        ani_crv = each_crv.split(":")[-1] + "_" + attr
        # print ani_crv
        ani_crv2 = mc.ls(ani_crv+"*", type="animCurve")
        ani_crv3 = mc.ls("*:*"+ani_crv+"*", type="animCurve") + mc.ls("*:*:*"+ani_crv+"*", type="animCurve")
        ani_crv4 = list()
        if attr in temp_dict.keys():
            ani_crv4 = mc.ls(each_crv.split(":")[-1]+"_translate_*_"+temp_dict[attr], type="animCurve")
        elif attr in temp_dict2.keys():
            ani_crv4 = mc.ls(each_crv.split(":")[-1]+"_rotate_*_"+temp_dict2[attr], type="animCurve")
        final_crv = ani_crv2 + ani_crv3 + ani_crv4
        final_crv2 = str()
        if isinstance(final_crv, list):
            for each in final_crv:
                ani_crv_namespace = get_ani_crv_namespace(each)
                ctl_namespace = get_selected_namespace([each_crv])[0]
                if ani_crv_namespace != ctl_namespace:
                    continue
                else:
                    final_crv2 = each
                    break
        else:
            final_crv2 = final_crv
        # print final_crv2,final_crv2
        reverse_doit(final_crv2)
    return True


def reverse_doit(ani_crv):
    all_value = get_ani_value(ani_crv)  # float in list
    key_nums = get_num_keys(ani_crv)
    if not key_nums:
        return False
    for num in xrange(key_nums):
        # print num
        pm.PyNode(ani_crv).setValue(num, -all_value[num])
    return True


def get_ani_crv_namespace(ani_crv):
    # print ani_crv
    if pm.referenceQuery(ani_crv, inr=1):
            namespace_ = mc.referenceQuery(ani_crv, ns=True, shn=True)
            return namespace_
    obj = pm.PyNode(ani_crv).listConnections(s=0, d=1, type="transform")
    if obj:
        if pm.referenceQuery(obj[0], inr=1):
            namespace_ = mc.referenceQuery(obj[0].nodeName(), ns=True, shn=True)
            return namespace_
        else:
            get_ani_crv_namespace(obj[0].nodeName())
    else:
        try:
            next_node = pm.PyNode(ani_crv).listConnections(s=0, d=1)[0]
        except:
            return False
        if "RN" in next_node.nodeName():
            return False
            # next_node = next_node.listConnections(s=0, d=1)[0]
        # print next_node.nodeName()
        return get_ani_crv_namespace(next_node)


def get_selected_namespace(selection_list):
    all_namespace = list()
    if not selection_list:
        logging.error(u"请先选择想要反转的角色！")
        return False
    for each_ch in selection_list:
        # print each_ch.split(":")[0]
        all_namespace.append(mc.referenceQuery(each_ch, ns=True, shn=True))
    if all_namespace:
        return all_namespace
    else:
        return False


file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType.loadUiType(file_path+'\\reverse_animcrv.ui')


class ReverseAniCrv(base_class, form_class):
    def __init__(self):
        super(ReverseAniCrv, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)
        self.edit_cfg_window = edit_cfg_win.RecordAttrWin()
        self.translateX.clicked.connect(lambda: reverse_ani_crv("translateX"))
        self.translateY.clicked.connect(lambda: reverse_ani_crv("translateY"))
        self.translateZ.clicked.connect(lambda: reverse_ani_crv("translateZ"))
        self.rotateX.clicked.connect(lambda: reverse_ani_crv("rotateX"))
        self.rotateY.clicked.connect(lambda: reverse_ani_crv("rotateY"))
        self.rotateZ.clicked.connect(lambda: reverse_ani_crv("rotateZ"))
        self.edit_cfg_window.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.edit_cfg_window.tableWidget.customContextMenuRequested.connect(self.show_reverse_menu)
        self.reverse_pushButton.clicked.connect(self.edit_cfg_window.show)
        self.edit_cfg_window.add_attr_pushButton.setHidden(True)
        self.edit_cfg_window.delete_attr_pushButton.setHidden(True)
        self.edit_cfg_window.clear_pushButton.setHidden(True)
        self.edit_cfg_window.save_cfg_pushButton.setHidden(True)
        self.edit_cfg_window.special_save_cfg_pushButton.setHidden(True)
        self.edit_cfg_window.which_char_le.setHidden(True)
        self.edit_cfg_window.reverse_pushButton.clicked.connect(self.reverse_attr)
        # self.edit_cfg_window.add_attr_win.pushButton_2.clicked.connect(self.input_cfg_attr)

    # def input_cfg_attr(self):
    #     dict_temp = {"tx": "translateX", "ty": "translateY", "tz": "translateZ", "rx": "rotateX", "ry": "rotateY",
    #                     "rz": "rotateZ"}
    #     selected_con = mc.ls(sl=True)
    #     for each in selected_con:
    #         each_con = each
    #         if ":" in each:
    #             each_con = each.split(":")[-1]
    #         selected_attr = dict_temp[mc.channelBox("mainChannelBox", q=1, selectedMainAttributes=1)[0]]
    #         table_widget_methods.add_item(self.edit_cfg_window.add_attr_win.tableWidget, each_con)
    #         self.edit_cfg_window.add_attr_win.lineEdit_3.setText(selected_attr)
    #     return True

    def show_reverse_menu(self, pos):
        menu = QtWidgets.QMenu()
        item = menu.addAction("Reverse!")
        action = menu.exec_(self.edit_cfg_window.tableWidget.mapToGlobal(pos))
        if action == item:
            self.reverse_attr()
        return True

    def reverse_attr(self):
        all_attr = table_widget_methods.get_contents(self.edit_cfg_window.tableWidget)['AnimCrv']
        selected_name = get_selected_namespace(mc.ls(sl=True))
        # print selected_name, 1
        temp_dict = {"_rotateX": "_rotate_*_inputBX", 
                     "_rotateY": "_rotate_*_inputBY", 
                     "_rotateZ": "_rotate_*_inputBZ", 
                     "_translateX": "_translate_*_inputBX",
                     "_translateY": "_translate_*_inputBY",
                     "_translateZ": "_translate_*_inputBZ",
                     }
        if not selected_name:
            return False
        for each in all_attr:
            try:
                # print each
                each2 = each
                for k, v in temp_dict.items():
                    if k in each:
                        each2 = each.replace(k, v)
                # print each, each2
                all_crv = mc.ls("*"+each+"*", type="animCurve") + \
                          mc.ls("*:*"+each+"*", type="animCurve") + \
                          mc.ls("*:*:*"+each+"*", type="animCurve") + \
                          mc.ls("*"+each+"*:*", type="animCurve")
                all_crv2 = mc.ls("*"+each2+"*", type="animCurve") + \
                           mc.ls("*:*"+each2+"*", type="animCurve") + \
                           mc.ls("*:*:*"+each2+"*", type="animCurve") + \
                           mc.ls("*"+each2+"*:*", type="animCurve")
                # print all_crv2
                all_crv.extend(all_crv2)
                all_crv = list(set(all_crv))
                # print all_crv
                for each_crv in all_crv:
                    curve_namespace = get_ani_crv_namespace(each_crv)
                    if curve_namespace:
                        if curve_namespace not in selected_name:
                            print curve_namespace
                            continue
                        print (u"正在反转曲线:" + each_crv)
                        reverse_doit(each_crv)
            except:
                continue
        logging.info(u"反转的角色为：%s" % selected_name)
        return True











