#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/1/22


__author__ = "dango wang"

import maya.cmds as mc
import pymel.core as pm
import logging


import os
import sys
import loadUiType
import table_widget_methods
import edit_cfg_win
reload(edit_cfg_win)
reload(table_widget_methods)

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType.loadUiType(file_path+'\\reverse_direction.ui')

input_plug_dic = {"translateX": "input2X", "translateY": "input2Y", "translateZ": "input2Z",
                  "rotateX": "input2X", "rotateY": "input2Y", "rotateZ": "input2Z"}
output_plug_dic = {"translate": "output", "translateX": "outputX", "translateY": "outputY", "translateZ": "outputZ",
                   "rotate": "output", "rotateX": "outputX", "rotateY": "outputY", "rotateZ": "outputX"}


def undoable(function):
    '''A decorator that will make commands undoable in maya'''

    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print sys.exc_info()[1]

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode


def get_d_connections(obj, except_node=None):
    if obj is None:
        logging.error("Nothing selected!")
        return False
    all_d_connections = mc.listConnections(obj, d=1, p=1, scn=1)
    all_except_connections = list()
    if not except_node:
        all_except_connections = []
    else:
        for each in except_node:
            if not except_node:
                continue
            all_except_connections.extend(mc.listConnections(each, s=1, scn=1))
    try:
        d_connections = [con for con in all_d_connections if con.split(".")[0] not in all_except_connections]
        return d_connections
    except TypeError:
        return


def get_s_connections(obj=None):
    if obj is None:
        logging.error("Nothing selected!")
        return False
    return mc.listConnections(obj, s=1, p=1, scn=1)


def get_all_connections(obj, filter_list, except_node):
    connections_info = list()
    all_d_connections = get_d_connections(obj, except_node)
    # print all_d_connections
    if not all_d_connections:
        return
    for each in all_d_connections:
        connections = get_s_connections(each)
        for every in filter_list:
            if every not in connections:
                continue
            else:
                connections_info.append((every, each))
    # print connections_info
    return connections_info


def get_all_children(control=None):
    if control is None:
        return ""
    all_shape = mc.listRelatives(control, c=1, ad=1, typ="nurbsCurve")
    if not all_shape:
        raise RuntimeError("no curve selected!")
    all_crv_transform_temp = [mc.listRelatives(a, p=1)[0] for a in all_shape]
    all_crv_transform = list(set(all_crv_transform_temp))
    all_crv_transform.sort(key=all_crv_transform_temp.index)
    return all_crv_transform


def get_point_positions(crv=None):
    if crv is None:
        raise RuntimeError("wrong input!!")
    all_crv_point_pos = list()
    for each_crv in crv:
        point_str = mc.ls("%s.cv[*]" % each_crv)[0]
        if not point_str:
            continue
        start_point = int(point_str.split("[")[1].split(":")[0])
        end_point = int(point_str.split("[")[1].split(":")[1].split("]")[0])
        point_pos_list = list()
        for each_point in range(start_point, end_point+1):
            point_name = "{}.cv[{}]".format(each_crv, each_point)
            point_pos = pm.PyNode(point_name).getPosition(space="world")
            point_pos_list.append((point_name, point_pos))
        if point_pos_list:
            all_crv_point_pos.extend(point_pos_list)
        else:
            continue
    if all_crv_point_pos:
        return all_crv_point_pos
    else:
        return False


def get_con_pos(crv):
    con_pos_list = list()
    for each in crv:
        each_pos = pm.PyNode(each).getTranslation(space="world")
        con_pos_list.append((each, each_pos))
    return con_pos_list


def set_con_pos(con_pos_info):
    for each in con_pos_info:
        pm.PyNode(each[0]).setTranslation(each[1], space="world")
    return True


def create_multiply_node(name, reverse_attr):
    reverse_attr2 = input_plug_dic[reverse_attr]
    mc.shadingNode("multiplyDivide", n=name, asUtility=1)
    mc.setAttr(name+"."+reverse_attr2, -1)
    return name


def reverse_direction(scale_obj, scale_attr, con_name, reverse_attr, connections_info):
    """
    :param scale_obj:
    :param reverse_attr: translateX
    :param con_name: Mouth1_Con
    :param scale_attr: scaleX
    :param connections_info:[('Mouth1_Con.translate', u'MouthCon1_follicle_multiply.input1')...]
    :return:
    """
    if mc.getAttr(scale_obj+"."+scale_attr) == -1:
        pass
    else:
        mc.setAttr(scale_obj+"."+scale_attr, lock=0)
        mc.setAttr(scale_obj+"."+scale_attr, -1)
    node_name = con_name+"_rev_multi_node"
    if mc.objExists(node_name):
        mc.delete(node_name)
    multiply_node = create_multiply_node(node_name, reverse_attr)
    mc.connectAttr(con_name+".translate", multiply_node+".input1")
    for each_connection in connections_info:
        # print each_connection
        multiply_node_attr = output_plug_dic[each_connection[0].split(".")[1]]  # outputX
        mc.disconnectAttr(each_connection[0], each_connection[1])
        mc.connectAttr(multiply_node+"."+multiply_node_attr, each_connection[1])
    return True


def restore_shape(point_positions):
    """
    :param point_positions: [("FKShoulder_L.cv[0]",[1.74142514155, 14.5171409258, -1.93783658147])...]
    :return:
    """
    for each in point_positions:
        pm.PyNode(each[0]).setPosition(each[1], space="world")
    return True


def get_pivot(con):
    """
    :param con:
    :return: {each_con:((rotate pivot),(scale pivot))...}
    """
    if not isinstance(con, list):
        raise RuntimeError("not valid list!")
    all_pivot_nifo = dict()
    for each_con in con:
        scale_pivot = pm.PyNode(each_con).getScalePivot(space="world")
        rotate_pivot = pm.PyNode(each_con).getRotatePivot(space="world")
        all_pivot_nifo[each_con] = (rotate_pivot, scale_pivot)
    return all_pivot_nifo


def inverse_pivot_info(cur_format, new_format, reverse_attr, all_pivot_info):
    inverse_dict = {"translateX": (-1, 1, 1), "translateY": (-1, 1, 1), "translateZ": (-1, 1, 1)}
    new_pivot_info = dict()
    for k, v in all_pivot_info.items():
        k = k.replace(cur_format, new_format)
        multi_tup = inverse_dict[reverse_attr]
        new_rotate_pv = (v[0][0] * multi_tup[0], v[0][1] * multi_tup[1], v[0][2] * multi_tup[2])
        new_scale_pv = (v[1][0] * multi_tup[0], v[1][1] * multi_tup[1], v[1][2] * multi_tup[2])
        new_pivot_info[k] = (new_rotate_pv, new_scale_pv)
    return new_pivot_info


def set_pivot(all_pivot_info):
    for k, v in all_pivot_info.items():
        try:
            pm.PyNode(k).setRotatePivot(v[0], space="world")
            pm.PyNode(k).setScalePivot(v[0], space="world")
        except:
            pass
    return True


def all_inverse_obj(cur_format, new_format, con):
    return [each_con.replace(cur_format, new_format) for each_con in con]


def reverse_ik(ik_con, scale_attr):
    children = get_all_children(ik_con)
    for each_child in children:
        scale_con_temp = mc.listRelatives(mc.listRelatives(each_child, p=1)[0], p=1)[0]
        reverse_each_ik(each_child, scale_con_temp, scale_attr)


def reverse_each_ik(ik_con, scale_con, scale_attr):
    children = mc.listRelatives(ik_con, c=1, typ="transform")
    if children:
        mc.select(children, r=True)
        mc.Unparent(children)
    try:
        mc.setAttr(scale_con + "." + scale_attr, lock=0)
        mc.setAttr(scale_con + "." + scale_attr, -1)
    except:
        pass
    if children:
        mc.parent(children, ik_con)
    return True


def reverse_matrix_ctrl(ctrl, scale_con, scale_attr, reverse_attr):
    try:
        mc.setAttr(scale_con+"."+scale_attr, lock=0)
        mc.setAttr(scale_con+"."+scale_attr, -1)
    except:
        pass
    if not mc.objExists("Fixed"):
        logging.error(u"请检查是否存在Fixed组！")
        return
    if not mc.objExists("Matrix_Reverse"):
        mc.createNode("transform", name="Matrix_Reverse")
        mc.parent("Matrix_Reverse", "Fixed")
    matrix_trans_node = mc.createNode("transform", name=ctrl+"_matrix_reverse")
    mc.parent(matrix_trans_node, "Matrix_Reverse")
    matrix_d_plug = mc.listConnections(ctrl+".matrix", d=1, s=0, p=1)[0]
    # try:
    multiply_node = create_multiply_node("Matrix_Reverse_multiply_node", reverse_attr)
    mc.connectAttr(ctrl+".translate", multiply_node+".input1")
    mc.connectAttr(multiply_node+".output", matrix_trans_node + ".translate")
    mc.connectAttr(matrix_trans_node + ".matrix", matrix_d_plug, f=1)
    return ctrl
    # except:
    #     pass


class ReverseDirection(base_class, form_class):
    def __init__(self):
        super(ReverseDirection, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)
        self.point_pos = None
        self.show_edit_win = edit_cfg_win.RecordAttrWin()
        self.show_edit_win.reverse_pushButton.setHidden(True)
        self.show_edit_win.label.setHidden(True)
        self.show_edit_win.char_label.setHidden(True)
        self.edit_cfg_pushButton.clicked.connect(self.show_edit_win.show)
        self.scale_obj_pushButton.clicked.connect(self.input_scale_obj)
        self.reverse_pushButton.clicked.connect(self.input_reverse_obj)
        self.except_pushButton.clicked.connect(self.input_except_obj)
        self.doit_pushButton.clicked.connect(self.reverse_it)
        self.except_pushButton_2.clicked.connect(lambda: table_widget_methods.delete_items(self.tableWidget))
        self.show_edit_win.add_attr_win.pushButton_2.clicked.connect(
            lambda: self.input_cfg_attr(self.show_edit_win.add_attr_win.tableWidget,
                                        self.show_edit_win.add_attr_win.lineEdit_3))
        self.input_rotate_attr.clicked.connect(
            lambda: self.input_cfg_attr(self.rotate_cons,
                                        self.rotate_attr))
        self.clear_rotate_cons.clicked.connect(self.clear_all_rotate_cons)
        self.reverse_rotation_doit.clicked.connect(self.reverse_rotate_doit)
        self.restore_shape_pushButton.clicked.connect(lambda: restore_shape(self.point_pos))
        self.undo_pushButton.clicked.connect(self.quick_undo)

    def quick_undo(self):
        count = int(self.undo_count_lineEdit.text())
        for _ in range(count):
            mc.Undo()

    def clear_all_rotate_cons(self, tableWidget):
        table_widget_methods.clear_all_items(tableWidget)
        return True

    def input_cfg_attr(self, tableWidget, lineEdit):
        self.clear_all_rotate_cons(tableWidget)
        dict_temp = {"tx": "translateX", "ty": "translateY", "tz": "translateZ",
                     "rx": "rotateX", "ry": "rotateY", "rz": "rotateZ"}
        selected_con = mc.ls(sl=True)
        for each in selected_con:
            each_con = each
            if ":" in each:
                each_con = each.split(":")[-1]
            # print each_con
            selected_attr = ""
            for each_attr in mc.channelBox("mainChannelBox", q=1, selectedMainAttributes=1):
                try:
                    selected_attr = dict_temp[each_attr] + " " + selected_attr
                except KeyError:
                    selected_attr = each_attr + " " + selected_attr
            table_widget_methods.add_item(tableWidget, each_con)
            lineEdit.setText(selected_attr)
        return True

    def input_scale_obj(self):
        sel = mc.ls(sl=True)[0]
        if not sel:
            raise RuntimeError("please select an obj!")
        self.scale_obj_lineEdit.setText(sel)
        return True

    def input_reverse_obj(self):
        sel = mc.ls(sl=True)[0]
        if not sel:
            raise RuntimeError("please select an obj!")
        self.reverse_lineEdit.setText(sel)
        return True

    def input_except_obj(self):
        sel = mc.ls(sl=True)
        if not sel:
            raise RuntimeError("please select an obj!")
        for each in sel:
            table_widget_methods.add_item(self.tableWidget, each)
        return True

    def get_sel_radio_btn(self, attr_list):
        for each in attr_list:
            if eval("self.%s.isChecked()" % each):
                return each
            else:
                continue
        return False

    @undoable
    def reverse_it(self):
        scale_obj = self.scale_obj_lineEdit.text()
        scale_attr = self.get_sel_radio_btn(["scaleX", "scaleY", "scaleZ"])
        reverse_obj = self.reverse_lineEdit.text()
        reverse_attr = self.get_sel_radio_btn(["translateX", "translateY", "translateZ"])
        # ##
        all_reversing_obj = get_all_children(reverse_obj)  # [a, b, c]
        all_shapes_temp = [mc.listRelatives(child, c=1, s=1) for child in all_reversing_obj]
        all_shapes = list()
        current_LR_format = self.l_format_lineEdit.text() if self.l_format_lineEdit.text() else "R"
        inverse_LR_format = self.r_format_lineEdit.text() if self.r_format_lineEdit.text() else "L"
        for each in all_shapes_temp:
            all_shapes.extend(each)
        all_reversing_obj_temp = [each_obj for each_obj in all_reversing_obj if current_LR_format in each_obj]
        print all_reversing_obj_temp
        # 获取所有控制器曲线的点的位置
        all_point_pos = get_point_positions(all_shapes)
        self.point_pos = all_point_pos
        except_node = table_widget_methods.get_contents(self.tableWidget)['AnimCrv']
        # 获取rpv 和 spv 的位置，用来将中心点归到原位
        all_pv_info = get_pivot(all_inverse_obj(current_LR_format, inverse_LR_format, all_reversing_obj_temp))
        inverse_pv_info = inverse_pivot_info(inverse_LR_format, current_LR_format, reverse_attr, all_pv_info)
        # IK 和 极向量 的反转  ##还有FK
        if "IK" in reverse_obj or "Pole" in reverse_obj or "FK" in reverse_obj or "Roll" in reverse_obj:
            reverse_ik(reverse_obj, scale_attr)
            set_pivot(inverse_pv_info)
            restore_shape(all_point_pos)
            return
        if self.is_matrix_checkBox.isChecked():
            reverse_matrix_ctrl(reverse_obj, scale_obj, scale_attr, reverse_attr)
            set_pivot(inverse_pv_info)
            restore_shape(all_point_pos)
            return
        for each_crv in all_reversing_obj:
            connections_info = get_all_connections(each_crv, [each_crv+".translate", each_crv + "." + reverse_attr],
                                                    except_node)
            # print connections_info
            if not connections_info:
                continue
            reverse_direction(scale_obj, scale_attr, each_crv, reverse_attr, connections_info)
        set_pivot(inverse_pv_info)
        restore_shape(all_point_pos)
        logging.info("successfully reversed %s" % all_reversing_obj)

    @staticmethod
    def reverse_rotate(attribute):
        con, attr = attribute.split(".")
        all_rotate_connect = get_all_connections(con, [con+".rotate", con+"."+attr], [])
        rotate_multi = create_multiply_node(con+"rotate_multiply_node_for_reversing"+attr, attr)
        mc.connectAttr(con+".rotate", rotate_multi + ".input1")
        for each_connection in all_rotate_connect:
            # print each_connection
            multiply_node_attr = output_plug_dic[each_connection[0].split(".")[1]]  # outputX
            mc.disconnectAttr(each_connection[0], each_connection[1])
            mc.connectAttr(rotate_multi + "." + multiply_node_attr, each_connection[1])
        return True

    @undoable
    def reverse_rotate_doit(self):
        all_cons = table_widget_methods.get_contents(self.rotate_cons)['AnimCrv']
        attr = self.rotate_attr.text()
        all_attrs = attr.split(" ")
        all_full_attr = list()
        for each_attr in all_attrs:
            if not each_attr:
                continue
            all_full_attr.extend(each_con+"."+each_attr for each_con in all_cons)
        map(self.reverse_rotate, all_full_attr)






