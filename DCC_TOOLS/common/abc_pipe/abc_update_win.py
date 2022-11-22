# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as OpenMayaUI
import shiboken2
import utils.shotgun_operations as sg
import maya.cmds as cmds
from functools import partial

def getMayaWindow(*argv):
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)

_win = "abc_update_win_ui"

class abc_update_win_class(QtWidgets.QMainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(abc_update_win_class, self).__init__(parent)
        self.setObjectName(_win)
        self.resize(666, 333)
        self.setWindowTitle(u'ABC 更新缓存（十月文化）')
        # main layout
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.header().setVisible(True)
        self.treeWidget.headerItem().setText(0, u'节点')
        self.treeWidget.headerItem().setText(1, u'版本选择')
        self.treeWidget.headerItem().setText(2, u'替换')
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.verticalLayout.addWidget(self.treeWidget)
        self.refresh_abc_list()

    def refresh_abc_list(self):
        abc_list = cmds.ls(type="AlembicNode")
        for abc in abc_list:
            abc_file = cmds.getAttr("{}.abc_File".format(abc))
            filters = [['project', 'name_is', 'DSF'],
                       ['sg_cache_path', 'is', abc_file]
                       ]  # , ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
            fields = ['code', 'sg_namespace', "sg_cache_type", "sg_obj_list"]
            cache_sg_node = sg.find_shotgun('CustomEntity03', filters, fields) or []
            if not cache_sg_node:
                continue
            filters_version = [['project', 'name_is', 'DSF'],
                               ['code', 'is', cache_sg_node[0]["code"]],
                               ['sg_namespace', 'is', cache_sg_node[0]["sg_namespace"]],
                               ['sg_cache_type', 'is', cache_sg_node[0]["sg_cache_type"]],
                               #['sg_obj_list', 'is', cache_sg_node[0]["sg_obj_list"]],
                               ]
            fields_version = ['sg_cache_path', 'sg_version']
            cache_version_list = sg.find_shotgun('CustomEntity03', filters_version, fields_version) or []
            item_abc = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_abc.setText(0, abc)

            comboBox = QtWidgets.QComboBox(self.treeWidget)
            self.treeWidget.setItemWidget(item_abc, 1, comboBox)
            version_list = []
            for v in cache_version_list:
                version_list.append(v['sg_version'])
            comboBox.addItems(sorted(version_list, reverse=1))
            pushBtnBox = QtWidgets.QPushButton(self.treeWidget)
            self.treeWidget.setItemWidget(item_abc, 2, pushBtnBox)
            pushBtnBox.setText(u"替换")
            pushBtnBox.clicked.connect(partial(self.updete_abc, abc, comboBox, cache_version_list))

    def updete_abc(self, node, comboBox, version_list, *args):
        version_num = comboBox.currentText()
        abc_file = None
        for version in version_list:
            if version["sg_version"] == version_num:
                cmds.setAttr("{}.abc_File".format(node), version["sg_cache_path"], type="string")


def main():
    if cmds.window(_win, exists=1):
        cmds.deleteUI(_win)
    win = abc_update_win_class()
    win.show()

if __name__ == "__main__":
    main()
