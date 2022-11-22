#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/26

__author__ = 'donghao wang'

import os
import sys
import maya.cmds as mc
import pymel.core as pm
import logging
import maya.mel as mel
import loadUiType
import cut_core
reload(cut_core)

try:
    from PySide2 import QtCore
except ImportError:
    from PySide import QtCore

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType.loadUiType(file_path+'\\cut_ch_model_ui.ui')
knives_sheet_form, knives_sheet_base = loadUiType.loadUiType(file_path+'\\knives_sheet.ui')
conn_form, conn_base = loadUiType.loadUiType(file_path+'\\simple_connection_editor.ui')


def undoable(function):
    # A decorator that will make commands undoable in maya
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


def tree_to_dict(filter_list, tree_root=['Root_M']):
    # 将根骨骼下的所有在列表中的子物体以字典方式返回（为了生成刀片和递归做布尔运算）
    tree_dict = {}
    for each in tree_root:
        final_children = get_children_in_list(each, filter_list)
        children_temp = mc.listRelatives(each, c=1)
        if not children_temp:
            return each
        tree_dict[each] = tree_to_dict(filter_list, final_children)
    return tree_dict


def get_children_in_list(root, filter_list):
    # 辅助上面那个函数
    children = mc.listRelatives(root, c=1)
    if not children:
        return []
    return_list = []
    for each in children:
        if each not in filter_list:
            return_list.append(get_children_in_list(each, filter_list))
        else:
            return_list.append(each)
    return_list = flat(filter(None, return_list))
    return return_list


def flat(list_):
    # 将嵌套列表展开
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


def get_node_inputs(head_shapes, type, all_bs=None):
    #  追溯给定节点的所有上游节点（指定类型）
    if all_bs is None:
        all_bs = []
    for each in head_shapes:
        a = mc.listConnections(each, s=1, d=0)
        if a:
            b = mc.listConnections(each, s=1, d=0, type=type)
            if b:
                all_bs.extend(b)
            return get_node_inputs(a, type=type, all_bs=all_bs)
    return all_bs


class KnivesSheet(knives_sheet_base, knives_sheet_form):
    # 刀片表
    def __init__(self, parent=None):
        super(KnivesSheet, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)


class ConnectEditor(conn_base, conn_form):
    # 连接编辑器
    def __init__(self, parent=None):
        super(ConnectEditor, self).__init__(parent=parent)
        self.setupUi(self)

    @QtCore.Slot()
    def on_connect_attr_pb_clicked(self):
        selected = mc.ls(sl=1)
        selected_attr_temp = mc.channelBox("mainChannelBox", q=1, selectedMainAttributes=1)
        selected_attr = selected[0] + "." + selected_attr_temp[0] if selected_attr_temp else selected[0]
        self.connect_attr_le.setText(selected_attr)

    @QtCore.Slot()
    def on_connected_obj_pb_clicked(self):
        selected = mc.ls(sl=1)
        text = "\n".join(selected)
        self.connected_obj_te.setText(text)

    @QtCore.Slot()
    def on_connected_attr_pb_clicked(self):
        selected_attr_temp = mc.channelBox("mainChannelBox", q=1, selectedMainAttributes=1)
        if not selected_attr_temp:
            logging.error(u'请手动输入属性！')
            return
        self.connected_attr_le.setText(selected_attr_temp[0])

    @property
    def connect_attr(self):
        return self.connect_attr_le.text()

    @property
    def connected_objs(self):
        return self.connected_obj_te.toPlainText().split()

    @property
    def connected_attr(self):
        return self.connected_attr_le.text()

    @property
    def node_type_to_ls(self):
        return self.ls_type_nodes_le.text()

    @QtCore.Slot()
    def on_ls_type_nodes_pb_clicked(self):
        if not self.node_type_to_ls:
            logging.error(u'请先输入属性！')
            return
        selected = mc.ls(type=self.node_type_to_ls)
        text = "\n".join(selected)
        self.connected_obj_te.setText(text)

    @QtCore.Slot()
    def on_sel_node_mesh_pb_clicked(self):
        selected_nodes = self.connected_obj_te.createMimeDataFromSelection().text().split()
        mc.select(cl=1)
        for each in selected_nodes:
            if mc.objExists(each):
                meshes = mc.listConnections(each, type='mesh') or mc.listConnections(each, type='joint')
                if meshes:
                    mc.select(meshes, add=1)
        # if mc.ls(sl=1):
        #     mel.eval('PickWalkUp;')


class CutChModel(base_class, form_class):
    knives_sheet_dialog = KnivesSheet()

    def __init__(self):
        super(CutChModel, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)
        self.connection_editor = ConnectEditor(parent=self)
        self.open_knives_sheet_pb.clicked.connect(self.knives_sheet_dialog.show)
        self.conn_editor_pb.clicked.connect(self.connection_editor.show)
        self.connection_editor.connect_pb.clicked.connect(self.connect_all_attr)
        self.connection_editor.reverse_connect_pb.clicked.connect(self.reverse_connect_all_attr)
        self.constraints_list = []

    @undoable
    def connect_all_attr(self):
        # 连接属性
        connect_attr = self.connection_editor.connect_attr
        for each in self.connection_editor.connected_objs:
            connected_attr = each + '.' + self.connection_editor.connected_attr
            try:
                mc.connectAttr(connect_attr, connected_attr, f=1)
            except:
                pass

    @undoable
    def reverse_connect_all_attr(self):
        # 反向连接属性
        connect_attr = self.connection_editor.connect_attr
        for each in self.connection_editor.connected_objs:
            connected_attr = each + '.' + self.connection_editor.connected_attr
            try:
                self.reverse_connect_attr(connect_attr, [connected_attr])
            except:
                pass

    @property
    def joints_to_create(self):
        # 所有要创建的骨骼
        all_children = self.knives_sheet_dialog.children()
        all_textbrowser = [each for each in all_children if '_tb' in each.objectName()]
        all_jnts = []
        for every in all_textbrowser:
            the_text = every.toPlainText().split()
            all_jnts.extend(the_text)
        left_jnts = [jnt.replace('_R', "_L") for jnt in all_jnts]
        all_jnts.extend(left_jnts)
        all_jnts = list(set(all_jnts))
        return all_jnts

    @property
    def get_root(self):
        # 根骨骼
        return self.knives_sheet_dialog.root_jnt_cb.toPlainText().split()[0]

    @property
    def joints_dict_to_create(self):
        # 把要创建的骨骼列表变成字典形式
        return tree_to_dict(self.joints_to_create, [self.get_root])

    @QtCore.Slot(name='on_create_knives_pb_clicked')
    @undoable
    def on_create_knives_pb_clicked(self):
        wrong_jnts = []
        for each in self.joints_to_create:
            if not mc.objExists(each):
                wrong_jnts.append(each)
        if wrong_jnts:
            logging.error(u'以下骨骼不存在！请处理...\n%s' % wrong_jnts)
            return
        return cut_core.build_plane(self.joints_to_create)

    @property
    def selected_model(self):
        selection = mc.ls(sl=1)
        if not selection:
            logging.error(u'请先选择要切割的模型！')
            return
        # if not selection[0] == 'body_Low':
        #     logging.error(u'请将身体模型命名为body_Low')
        #     return
        return selection[0]

    @QtCore.Slot(name='on_mirror_knives_pb_clicked')
    @undoable
    def on_mirror_knives_pb_clicked(self):
        cut_core.mirror_knives()

    @QtCore.Slot(name='on_boolean_doit_pb_clicked')
    @undoable
    def on_boolean_doit_pb_clicked(self):
        selected = self.selected_model
        new_name = mc.rename(selected, self.get_root+'_Low')
        # mc.duplicate(selected, name=selected+"_for_single_cut")
        if selected:
            cut_core.boolean_model(self.get_root, self.joints_dict_to_create, new_name)

    @QtCore.Slot(name='on_rename_body_pb_clicked')
    @undoable
    def on_rename_body_pb_clicked(self):
        if not mc.ls(sl=True):
            logging.error(u'请先选择模型！')
            return
        for each in mc.ls(sl=True):
            if 'body_' not in each:
                mc.rename(each, 'body_' + each)

    @QtCore.Slot(name='on_rename_clothes_pb_clicked')
    @undoable
    def on_rename_clothes_pb_clicked(self):
        if not mc.ls(sl=True):
            logging.error(u'请先选择模型！')
            return
        for each in mc.ls(sl=True):
            if 'clothes_' not in each:
                mc.rename(each, 'clothes_' + each)

    @QtCore.Slot(name='on_add_constraint_pb_clicked')
    @undoable
    def on_add_constraint_pb_clicked(self):
        # if mc.objExists('body_body_Low'):
        #     body_cons_1 = mc.parentConstraint(self.get_root, 'body_body_Low', mo=1)
        #     self.constraints_list.append(body_cons_1)
        # if mc.objExists('clothes_body_Low'):
        #     body_cons_2 = mc.parentConstraint(self.get_root, 'clothes_body_Low', mo=1)
        #     self.constraints_list.append(body_cons_2)
        for each in self.joints_to_create:
            mesh_name1 = 'body_' + each + '_Low'
            mesh_name2 = 'clothes_' + each + '_Low'
            if mc.objExists(mesh_name1):
                body_cons = mc.parentConstraint(each, mesh_name1, mo=1)
                self.constraints_list.append(body_cons)
            if mc.objExists(mesh_name2):
                clothes_cons = mc.parentConstraint(each, mesh_name2, mo=1)
                self.constraints_list.append(clothes_cons)
        return self.constraints_list

    # @QtCore.Slot(name='on_generate_a_plane_pb_clicked')
    # def on_generate_a_plane_pb_clicked(self):
    #     if not mc.ls(sl=True):
    #         logging.error(u'请先选择骨骼！')
    #         return
    #     joint_=mc.ls(sl=True)[0]
    #     knife = cut_core.create_plane(joint_+'_polyPlane')
    #     cons_temp = mc.parentConstraint(joint_, knife)
    #     mc.delete(cons_temp)

    # @QtCore.Slot(name='on_reverse_normal_pb_clicked')
    # def on_reverse_normal_pb_clicked(self):
    #     if not mc.ls(sl=True):
    #         logging.error(u'请先选择面片！')
    #         return
    #     mel.eval('ReversePolygonNormals;')

    @QtCore.Slot(name='on_boolean_once_doit_clicked')
    @undoable
    def on_boolean_once_doit_clicked(self):
        if not mc.ls(sl=True):
            logging.error(u'请先选择面片+模型！')
            return
        knife, model = mc.ls(sl=True)
        cut_core.cut_model(model, knife)

    # @QtCore.Slot(name='on_reverse_L_normal_pb_clicked')
    # @undoable
    # def on_reverse_L_normal_pb_clicked(self):
    #     L_grp = 'cutting_knives_grp_L'
    #     all_l_planes = mc.listRelatives(L_grp, c=1)
    #     for each in all_l_planes:
    #         mc.select(each, r=1)
    #         mel.eval('ReversePolygonNormals;')

    # @QtCore.Slot(name='on_reverse_R_normal_pb_clicked')
    # @undoable
    # def on_reverse_R_normal_pb_clicked(self):
    #     R_grp = 'cutting_knives_grp_R'
    #     all_R_planes = mc.listRelatives(R_grp, c=1)
    #     for each in all_R_planes:
    #         mc.select(each, r=1)
    #         mel.eval('ReversePolygonNormals;')
    #
    # @QtCore.Slot(name='on_reverse_body_normal_pb_clicked')
    # @undoable
    # def on_reverse_body_normal_pb_clicked(self):
    #     body_grp = 'cutting_knives_grp_body'
    #     all_b_planes = mc.listRelatives(body_grp, c=1)
    #     for each in all_b_planes:
    #         mc.select(each, r=1)
    #         mel.eval('ReversePolygonNormals;')

    @QtCore.Slot(name='on_rename_as_body_pb_clicked')
    @undoable
    def on_rename_as_body_pb_clicked(self):
        selected = pm.ls(sl=1)
        if not len(selected) == 2 or not mc.nodeType(selected[1].getShape().name()) == 'mesh' \
                                  or not mc.nodeType(selected[0].name()) == 'joint':
            logging.error(u'请选择骨骼+模型！')
            return False
        if 'body_' not in selected[1]:
            pm.rename(selected[1], 'body_' + selected[0] + '_Low')

    @QtCore.Slot(name='on_rename_as_cloth_pb_clicked')
    @undoable
    def on_rename_as_cloth_pb_clicked(self):
        selected = pm.ls(sl=1)
        if not len(selected) == 2 or not mc.nodeType(selected[1].getShape().name()) == 'mesh' \
                or not mc.nodeType(selected[0].name()) == 'joint':
            logging.error(u'请选择骨骼+模型！')
            return False
        if 'clothes_' not in selected[1]:
            pm.rename(selected[1], 'clothes_' + selected[0] + '_Low')

    @staticmethod
    def get_all_heavy_nodes():
        all_heavy_nodes = mc.ls(type='skinCluster') + mc.ls(type='blendShape')
        all_needed_heavy_nodes = [each for each in all_heavy_nodes if mc.getAttr(each + '.envelope') == 1]
        return all_needed_heavy_nodes

    @staticmethod
    def get_all_head_bs_skin_nodes(head_name):
        shape = pm.PyNode(head_name).getShape().name()
        all_head_sources = mc.listConnections(shape, s=1, d=0)
        all_envelope_nodes = [each for each in all_head_sources if mc.objExists(each+'.envelope')]
        return all_envelope_nodes

    # def get_all_body_bs_skin_nodes(self):
    #     all_heavy_nodes = self.get_all_heavy_nodes()

    # @property
    # def get_all_adv_constraints(self):
    #     if not mc.objExists('ConstraintSystem'):
    #         logging.error(u'未发现组ConstraintSystem！！请确保层级正确！')
    #         return
    #     all_adv_cons = mc.listRelatives('ConstraintSystem', c=1)
    #     return all_adv_cons

    @property
    def get_all_fixed_constraints(self):
        if not mc.objExists('Fixed'):
            logging.error(u'Fixed！！请确保层级正确！')
            return
        all_fixed_constraints = mc.listRelatives('Fixed', c=1, ad=1, type='constraint')
        return all_fixed_constraints

    @staticmethod
    def reverse_connect_attr(attr_a, attr_list):
        multi = mc.shadingNode("multiplyDivide", name="switch_multi", asUtility=1)
        plus = mc.shadingNode("plusMinusAverage", name="switch_plus", asUtility=1)
        mc.connectAttr(attr_a, multi + '.input1X', f=1)
        mc.setAttr(multi + '.input2X', -1)
        mc.connectAttr(multi + '.outputX', plus + '.input1D[0]', f=1)
        mc.setAttr(plus + '.input1D[1]', 1)
        for attr_b in attr_list:
            mc.connectAttr(plus + '.output1D', attr_b, f=1)
        return

    @QtCore.Slot(name='on_add_attr_pb_clicked')
    @undoable
    def on_add_attr_pb_clicked(self):
        grp_list = ['high', 'low']
        # grp_list = ['high', 'low', 'body_Low', 'head_Hi', 'head_Low', 'head_Hi_Geo', 'head_Low_Geo']
        # eye_balls = ['eye_01_R_Geo', 'eye_02_R_Geo', 'eye_01_L_Geo', 'eye_02_L_Geo']
        selected_ctl = mc.ls(sl=True)
        if not selected_ctl:
            logging.error(u'请先选择控制器！')
            return
        for g in grp_list:
            if not mc.objExists(g):
                logging.error(u'请确保已经正确创建了%s' % grp_list)
                return False
        # for eye in eye_balls:
        #     if not mc.objExists(eye):
        #         logging.error(u'眼球命名不正确！正确的应为：\n%s' % eye_balls)
        #         return False
        # head_Hi_Geo_shape = pm.PyNode('head_Hi_Geo').getShape().name()
        # if not get_node_inputs(head_Hi_Geo_shape, 'blendShape') \
        #         or not get_node_inputs(head_Hi_Geo_shape, 'skinCluster'):
        #     logging.error(u'请先对head_Hi_Geo进行蒙皮和blendShape！')
        #     return
        #  增加属性
        mc.addAttr(selected_ctl[0], ln='switch_body', en="low:high:", sn='SWB', k=0, at='enum')
        mc.addAttr(selected_ctl[0], ln='switch_head', en="low:high:", sn='SWH', k=0, at='enum')
        mc.setAttr("Constrain.switch_body", cb=1)
        mc.setAttr("Constrain.switch_head", cb=1)
        #  找出节点
        all_heavy_nodes = mc.ls(type='skinCluster') + mc.ls(type='blendShape')
        all_needed_heavy_nodes = [each for each in all_heavy_nodes if mc.getAttr(each + '.envelope') == 1]

        #  =============身体的================
        # 打断蒙皮和blend
        for each in all_needed_heavy_nodes:
            mc.connectAttr(selected_ctl[0]+'.switch_body', each + '.envelope', f=1)
        # 约束节点开关
        constraints_list = mc.listRelatives('low', c=1, ad=1, type='constraint')
        if constraints_list:
            for c in constraints_list:
                mc.connectAttr(selected_ctl[0] + '.switch_body', c + '.nodeState', f=1)
        # 连接显示
        mc.connectAttr(selected_ctl[0] + '.switch_body', 'high.visibility', f=1)
        self.reverse_connect_attr(selected_ctl[0] + '.switch_body', ['low.visibility'])
        #  =============头的=================
        # head_high_skin_blend = get_node_inputs(head_Hi_Geo_shape, 'blendShape') + \
        #                        get_node_inputs(head_Hi_Geo_shape, 'skinCluster')
        # for every in head_high_skin_blend:
        #     mc.connectAttr(selected_ctl[0] + '.switch_head', every + '.envelope', f=1)
        # mc.connectAttr(selected_ctl[0] + '.switch_head', 'head_Hi_Geo.visibility', f=1)
        # self.reverse_connect_attr(selected_ctl[0] + '.switch_head', ['head_Low_Geo.visibility'])
        # 乘除节点和加减节点
        # all_multi_plus_nodes = mc.ls(type='multiplyDivide') + mc.ls(type='plusMinusAverage')
        # # 动画曲线
        # all_ani_curve = mc.ls(type='animCurve')
        # 多余的约束 + 以上
        # all_node_stats_nodes = self.get_all_fixed_constraints
        # all_node_stats_nodes_attr = [attr+'.nodeState' for attr in all_node_stats_nodes]
        # 反向连接
        # self.reverse_connect_attr(selected_ctl[0] + '.switch_head', all_node_stats_nodes_attr)
        # if not self.constraints_list:
        #     logging.error(u"请先给low模增加约束！")
        #     return
        # print self.get_all_adv_constraints
        # self.constraints_list.extend(self.get_all_adv_constraints)
        # needed_cons = self.constraints_list
        # all_constraints = mc.ls(type='constraint')
        # all_cons_need_closed = [each for each in all_constraints if each not in needed_cons]
        # for c in all_cons_need_closed:
        #     self.reverse_connect_attr(selected_ctl[0] + '.switchModel', c+'.nodeState')
        # return True

