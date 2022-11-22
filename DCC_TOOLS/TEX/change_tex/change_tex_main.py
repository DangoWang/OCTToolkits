#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/5/15

import xml.etree.ElementTree as xml
from cStringIO import StringIO
import maya.OpenMayaUI as mui
import os
import sys
from maya import mel
import maya.cmds as mc
import pymel.core as pm
try:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
    import pyside2uic as uic
except ImportError:
    import PySide.QtGui as QtWidgets
    from PySide import QtCore
    from shiboken import wrapInstance
    import pysideuic as uic

size_list = ['512', '1024', '2048', '4096']


def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
        return form_class, base_class


def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


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


file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType(file_path+'\\change_tex_ui.ui')


def get_node_connections(nodes, type, result=None):
    #  追溯给定节点的所有上游节点（指定类型）
    if result is None:
        result = []
    for each in nodes:
        a = mc.listConnections(each, s=1, d=0)
        if a:
            b = mc.listConnections(each, s=1, d=0, type=type)
            if b:
                result.extend(b)
            get_node_connections(a, type=type, result=result)
    return result


def get_SG(sel):
    sgs = []
    sel = [mc.listRelatives(each, c=1, ad=1, type='mesh') for each in sel]
    sel = list(set(flat(sel)))
    for each_mesh in sel:
        each_sg = mc.listConnections(each_mesh, s=0, d=1, type='shadingEngine') or []
        sgs.extend(each_sg)
    return sgs


def flat(list_):
    # 将嵌套列表展开
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


class ChangeTex(base_class, form_class):
    result_signal = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(ChangeTex, self).__init__(parent=getMayaWindow())
        self.setupUi(self)
        self.script_job = int()
        self.changeto_512.clicked.connect(lambda: self.change_tex_doit('512'))
        self.changeto_1024.clicked.connect(lambda: self.change_tex_doit('1024'))
        self.changeto_2048.clicked.connect(lambda: self.change_tex_doit('2048'))
        self.changeto_4096.clicked.connect(lambda: self.change_tex_doit('4096'))
        self.add_script_job()

    @undoable
    def change_tex_doit(self, new_size):
        if not mc.ls(sl=1):
            raise RuntimeError(u'请先选择模型！')
        all_files_nodes = get_node_connections(get_SG(mc.ls(sl=1)), 'file')
        for each in all_files_nodes:
            old_path = pm.getAttr(each + '.fileTextureName')
            for size in size_list:
                if size in old_path:
                    base_name = os.path.basename(old_path)
                    old_path = old_path.rstrip(base_name)
                    new_path = old_path.replace(size, new_size, 1) + base_name
                    pm.setAttr(each + '.fileTextureName', new_path)
                    break
        self.update_file_path()
        return True

    def closeEvent(self, event):
        mc.scriptJob(kill=self.script_job, force=True)
        event.accept()

    def add_script_job(self):
        self.script_job = mc.scriptJob(parent=self.objectName(), event=["SelectionChanged", self.update_file_path])
        return self.script_job

    def update_file_path(self):
        if not mc.ls(sl=1):
            return
        result = []
        all_files_nodes = get_node_connections(get_SG(mc.ls(sl=1)), 'file')
        for each in all_files_nodes:
            path = pm.getAttr(each + '.fileTextureName')
            dir = path.rstrip(os.path.basename(path))
            result.append(dir)
        result_text = '\n'.join(list(set(result)))
        self.textBrowser.setText(result_text)

