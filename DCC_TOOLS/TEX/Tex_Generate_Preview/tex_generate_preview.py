#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import sys, os
from dayu_widgets.qt import *
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.item_view import MListView
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MTableModel, MSortFilterModel
import maya.cmds as cmds
import maya.OpenMaya as openMaya
import maya.mel as mel

header_list = [
    {
        'label': 'Name',
        'key': 'name',
    }]


class GeneratePreview(QWidget, MFieldMixin):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self):
        super(GeneratePreview, self).__init__()
        self.resize(470, 400)
        self.setWindowTitle(u'显示材质窗口')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.table_default = MListView()
        self.model_1 = MTableModel()
        self.model_1.set_header_list(header_list)
        self.model_sort = MSortFilterModel()
        self.model_sort.setSourceModel(self.model_1)
        self.table_default.setModel(self.model_sort)
        self.show_pb = MPushButton(text=u"show")
        self.close_pb = MPushButton(text=u"close")

        lay = QHBoxLayout()
        lay.addWidget(self.show_pb)
        lay.addWidget(self.close_pb)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'选择的物体'))
        main_lay.addWidget(self.table_default)
        main_lay.addLayout(lay)
        self.setLayout(main_lay)
        self.get_select_list()
        self.show_pb.clicked.connect(self.generate_preview)

        self.selection_callback = openMaya.MEventMessage.addEventCallback("SelectionChanged", self.select_change_func)
        self.close_pb.clicked.connect(self.close_func)

    def get_select_list(self):
        data_list = []
        select_list = cmds.ls(sl=True)
        for s in select_list:
            if cmds.nodeType(s) == "mesh":
                name_dict = {"name": s}
            else:
                mesh = cmds.listRelatives(s)
                name_dict = {"name": mesh}
            data_list.append(name_dict)
        self.model_1.set_data_list(data_list)

    def select_change_func(self, *arges, **kwargs):
        self.model_1.set_data_list([])
        self.model_1.clear()
        data_list = []
        select_list = cmds.ls(sl=True)
        for s in select_list:
            if cmds.nodeType(s) == "mesh":
                name_dict = {"name": s}
            else:
                mesh = cmds.listRelatives(s)
                name_dict = {"name": mesh}
            data_list.append(name_dict)
        self.model_1.set_data_list(data_list)

    def generate_preview(self):
        select_mesh_list = []
        list_data = self.model_1.get_data_list()
        for data in list_data:
            select_mesh_list.append(data["name"][0])
        for mesh in select_mesh_list:
            sg = cmds.listConnections(mesh, d=1, t='shadingEngine')  # 获取mesh的下一个类型为shadingEngin
            material_name = cmds.listConnections("{}.surfaceShader".format(sg[0]))
            file_node_list = cmds.listConnections(material_name, d=1, t='file')
            if file_node_list:
                for file_node in file_node_list:
                    if cmds.getAttr("{}.uvTilingMode".format(file_node)) == 3:
                        material_path = cmds.getAttr("{}.fileTextureName".format(file_node))
                        material_name = os.path.split(material_path)[-1]
                        if "_basecolor" in material_name.split(".")[0]:
                            mel.eval('generateUvTilePreview %s;' % (file_node))
                            cmds.select(file_node)

    def close_func(self):
        openMaya.MMessage.removeCallback(self.selection_callback)
        self.close()


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = GeneratePreview()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())



