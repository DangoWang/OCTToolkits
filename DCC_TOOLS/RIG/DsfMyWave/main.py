#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/6/17

import os
import random

from maya import cmds
from DCC_TOOLS.common.dcc_utils import *
from utils.common_methods import *
import maya.mel as mel
import pymel.core as pm
import mel_context
reload(mel_context)
import logging

try:
    from PySide2 import QtWidgets, QtCore

except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore

file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path + '\\ui.ui')


class NMWave(base_class, form_class):

    def __init__(self, parent=getMayaWindow()):
        super(NMWave, self).__init__(parent=parent)
        self.setupUi(self)
        self.load_source_pb.clicked.connect(lambda: self.load_selected(self.source_tw))
        self.load_target_pb.clicked.connect(lambda: self.load_selected(self.target_tw))
        self.source_clear_pb.clicked.connect(lambda: self.clear_items(self.source_tw))
        self.target_clear_pb.clicked.connect(lambda: self.clear_items(self.target_tw))

    @staticmethod
    def get_selected():
        return cmds.ls(sl=1) if cmds.ls(sl=1) else []

    @staticmethod
    def add_item(table_widget, label):
        contents = [table_widget.item(i, 0).text() for i in range(table_widget.rowCount())]
        if label in contents:
            return
        row_count = table_widget.rowCount()
        table_widget.setRowCount(row_count + 1)
        new_item = QtWidgets.QTableWidgetItem(label)
        table_widget.setItem(row_count, 0, new_item)
        return True

    @staticmethod
    def clear_items(item):
        item.setRowCount(0)
        item.clearContents()

    def load_selected(self, tw):
        map(self.add_item, [tw] * len(self.get_selected()), self.get_selected())

    @QtCore.Slot()
    def on_input_main_ctrl_pb_clicked(self):
        sel_obj = self.get_selected()
        if sel_obj:
            self.main_ctrl.setText(sel_obj[0])
        return

    @QtCore.Slot(name='on_doit_pb_clicked')
    @undoable
    def on_doit_pb_clicked(self):
        if not cmds.pluginInfo('DsfMyWave', query=1, loaded=1):
            try:
                cmds.loadPlugin('DsfMyWave.mll')
            except RuntimeError:
                raise RuntimeError('DsfMyWave.mll was not found on MAYA_PLUG_IN_PATH')
        sources = [self.source_tw.item(i, 0).text() for i in range(self.source_tw.rowCount())]
        targets = [self.target_tw.item(j, 0).text() for j in range(self.target_tw.rowCount())]
        main_ctrl = self.main_ctrl.text()
        if len(sources) != len(targets):
            logging.error(u'左右两边物体数量不一致！！')
            return False
        main_ctrl_node = cmds.createNode("DsfMyWave", name=main_ctrl + '_my_wave_node')
        add_str = "addAttr -ln \"t_offset\" -at double -min -100 -max 100 -dv -10 {0};" \
                  "setAttr -e -keyable true {0}.t_offset;" \
                  "addAttr -ln \"s_offset\" -at double -min -100 -max 100 -dv -10 {0};" \
                  "setAttr -e -keyable true {0}.s_offset;" \
                  "addAttr -ln \"t_on_off\" -at bool {0};" \
                  "setAttr -e -keyable true {0}.t_on_off;" \
                  "addAttr -ln \"s_on_off\" -at bool {0};" \
                  "setAttr -e -keyable true {0}.s_on_off;".format(main_ctrl)
        mel.eval(add_str)
        cmds.connectAttr(main_ctrl + '.t_on_off', main_ctrl_node + '.t_on_off')
        cmds.connectAttr(main_ctrl + '.s_on_off', main_ctrl_node + '.s_on_off')
        cmds.connectAttr(main_ctrl + '.t_offset', main_ctrl_node + '.t_offset')
        cmds.connectAttr(main_ctrl + '.s_offset', main_ctrl_node + '.s_offset')
        index = 0
        while index < len(sources):
            mel.eval(mel_context.get_mel_text({'ctrl': sources[index]}))
            ctrl_node = cmds.createNode("DsfMyWave", name=sources[index] + '_my_wave_node')
            cmds.connectAttr('time1.outTime', ctrl_node + '.inputTime')
            for each in ['.tx_amplitude', '.ty_amplitude', '.tz_amplitude', '.sx_amplitude', '.sy_amplitude',
                         '.sz_amplitude', '.s_min', '.t_frequency', '.s_frequency']:
                cmds.connectAttr(sources[index] + each, ctrl_node + each)
            for conn_attr in ['.translateX', '.translateY', '.translateZ', '.scaleX', '.scaleY', '.scaleZ']:
                cmds.connectAttr(ctrl_node + conn_attr, targets[index] + conn_attr)
            cmds.connectAttr(main_ctrl + '.t_on_off', ctrl_node + '.t_on_off')
            cmds.connectAttr(main_ctrl + '.s_on_off', ctrl_node + '.s_on_off')
            cmds.connectAttr(main_ctrl_node + '.t_wave_offset[%s]' % index, ctrl_node + '.t_offset')
            cmds.connectAttr(main_ctrl_node + '.s_wave_offset[%s]' % index, ctrl_node + '.s_offset')
            index += 1

    @QtCore.Slot(name='on_add_offset_doit_pb_clicked')
    @undoable
    def on_add_offset_doit_pb_clicked(self):
        sel = cmds.ls(sl=1)
        if sel:
            for each in sel:
                if not cmds.objExists(each + '.t_offset'):
                    continue
                cmds.addAttr(each, ln='wave_offset', at='double', dv=0)
                cmds.setAttr(each+'.wave_offset', e=1, keyable=1)
                out_wave_node = cmds.listConnections(each, s=0, d=1, type='DsfMyWave')[0]
                cmds.connectAttr(each+'.wave_offset', out_wave_node+'.offset')

    @QtCore.Slot(name='on_add_blink_pb_clicked')
    @undoable
    def on_add_blink_pb_clicked(self):
        self.bn = []
        self.random_blink_on_of = []
        random_seed = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 30, 33, 35, 37, 39, 41, 45, 49, 51, 57, 59]
        random_seed_1 = [0]
        random_seed_2 = [-1, 1]
        random_seed_3 = [0, 0, 1, 0.5]
        sources = [self.source_tw.item(i, 0).text() for i in range(self.source_tw.rowCount())]
        main_ctrl = self.main_ctrl.text()
        if not (sources and main_ctrl):
            logging.error(u'请输入正确信息！')
            return
        if sources:
            for s in sources:
                each = pm.PyNode(s)
                if not cmds.objExists(s+'.close_eye'):
                    continue
                if cmds.objExists(each.name() + '_random_blink_node'):
                    continue
                blink_node = pm.createNode('DsfMyBlink', name=(each.name() + '_random_blink_node'))
                self.bn.append(blink_node)
                pm.PyNode('time1').outTime >> blink_node.in_time

                plus_node = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
                blink_node.blink >> plus_node.input1D[1]
                for anim_crv in pm.listConnections(each.close_eye, s=0, d=1, p=1):
                    plus_node.output1D >> anim_crv
                each.close_eye >> plus_node.input1D[0]
                _str = 'select -r {ctrl};addAttr -ln "random_blink"  -at bool -dv 1  "{ctrl}";'\
                       'setAttr -e -keyable true {ctrl}.random_blink;'.format(**{'ctrl': s})
                mel.eval(_str)
                plus_node_2 = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
                plus_node_temp = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
                pm.setAttr(plus_node_temp.input1D[0], -1)
                each.random_blink >> plus_node_2.input1D[0]
                plus_node_2.output1D >> plus_node_temp.input1D[1]
                plus_node_temp.output1D >> blink_node.envelope
                self.random_blink_on_of.append(plus_node_2)
        if main_ctrl:
            if not cmds.objExists(main_ctrl+'.random_blink'):
                mel.eval(mel_context.blink_attr.format(**{'ctrl': main_ctrl}))
            mctl = pm.PyNode(main_ctrl)
            for a in self.random_blink_on_of:
                mctl.random_blink >> a.input1D[1]
            for b in self.bn:
                random_blink_offset = random_seed[random.randint(0, len(random_seed)-1)] * random_seed_2[
                    random.randint(0, len(random_seed_2)-1)]
                random_blink_speed = random_seed_1[random.randint(0, len(random_seed_1)-1)] * random_seed_2[
                    random.randint(0, len(random_seed_2)-1)]
                random_blink_interval = random_seed_3[random.randint(0, len(random_seed_3)-1)] * random_seed_2[
                    random.randint(0, len(random_seed_2)-1)]
                offset_p = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
                speed_p = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
                interval_p = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))

                mctl.random_blink_offset >> offset_p.input1D[0]
                pm.setAttr(offset_p.input1D[1], random_blink_offset)
                offset_p.output1D >> b.frame_offset

                mctl.random_blink_speed >> speed_p.input1D[0]
                pm.setAttr(speed_p.input1D[1], random_blink_speed)
                speed_p.output1D >> b.speed

                mctl.random_blink_interval >> interval_p.input1D[0]
                pm.setAttr(interval_p.input1D[1], random_blink_interval)
                interval_p.output1D >> b.interval

    @QtCore.Slot(name='on_delete_old_attr_pb_clicked')
    @undoable
    def on_delete_old_attr_pb_clicked(self):
        for each in pm.ls(typ='DsfMyBlink'):
            blink_ctl = list(set(pm.listConnections(each, s=1, d=0, type='transform')))[0]
            plus_node = pm.listConnections(each.blink, s=0, d=1, p=1)
            for p in plus_node:
                blink_ctl.close_eye >> p
            pm.delete(each)
            pm.delete(pm.listConnections(blink_ctl.random_offset, s=0, d=1))
            mel.eval('catch (`deleteAttr -attribute "%s" "%s"`);' % ('random_blink', blink_ctl.name()))
            mel.eval('catch (`deleteAttr -attribute "%s" "%s"`);' % ('random_speed', blink_ctl.name()))
            mel.eval('catch (`deleteAttr -attribute "%s" "%s"`);' % ('random_offset', blink_ctl.name()))
            mel.eval('catch (`deleteAttr -attribute "%s" "%s"`);' % ('random_interval', blink_ctl.name()))

        # sel = pm.ls(sl=1)
        # if sel:
        #     for each in sel:
        #         if not pm.objExists(each.close_eye):
        #             continue
        #         mel.eval(mel_context.blink_attr.format(**{'ctrl': each.name()}))
        #         each.random_blink_offset >> random_num_plus.input1D[0]
        #         blink_node = pm.createNode('DsfMyBlink', name=each.name()+'_random_blink_node')
        #         pm.PyNode('time1').outTime >> blink_node.in_time
        #         each.random_blink >> blink_node.envelope
        #         each.random_blink_speed >> blink_node.speed
        #         random_num_plus.output1D >> blink_node.frame_offset
        #         each.random_blink_interval >> blink_node.interval
        #         plus_node = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
        #         blink_node.blink >> plus_node.input1D[1]
        #         for anim_crv in pm.listConnections(each.close_eye, s=0, d=1, p=1):
        #             plus_node.output1D >> anim_crv
        #         each.close_eye >> plus_node.input1D[0]
        #         # random_num = random.randint(0, 15)
        #         random_num_plus = pm.PyNode(mel.eval('shadingNode -asUtility plusMinusAverage;'))
        #
        #         # pm.setAttr(random_num_plus.input1D[1], random_num)
        # pm.select(sel)


if __name__ == '__main__':
    pass
