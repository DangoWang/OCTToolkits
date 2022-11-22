#-*- coding: utf-8 -*-
####################################################
# Copyright 2016 October Media. All rights reserved.
# Transfer UVs (without undo)
# Author: Gao Lei
####################################################
try:
    from PySide.QtCore import Qt
    from PySide.QtGui import *
    import shiboken
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import *
    import shiboken2 as shiboken

import maya.api.OpenMaya as new_om
import maya.OpenMayaUI as omui
import maya.cmds as mc

# get maya main window pointer
def mayaMainWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = shiboken.wrapInstance(long(mayaMainWindowPtr), QWidget)
    return mayaMainWindow

class apiTransUVsUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(apiTransUVsUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setObjectName('api_trans_uvs')
        self.setWindowTitle('Transfer UVs')
        self.setStyleSheet('QWidget { font-family: "Microsoft YaHei"; }')
        self.setMinimumWidth(200)

        self.srcBtn = QPushButton(u'选择来源物体')
        self.desBtn = QPushButton(u'传给目标物体')
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.srcBtn)
        self.mainLayout.addWidget(self.desBtn)
        self.setLayout(self.mainLayout)
        self.srcBtn.clicked.connect(self.getSrcList)
        self.desBtn.clicked.connect(self.toDesList)

        self.srcList = []
        self.desList = []

    def getSrcList(self):
        self.srcList = mc.ls(sl=1)

    def toDesList(self):
        self.desList = mc.ls(sl=1)
        for i in range(len(self.srcList)):
            src = self.srcList[i]
            des = self.desList[i]
            slist = new_om.MSelectionList()
            slist.add(src)
            slist.add(des)
            src = slist.getDagPath(0)
            des = slist.getDagPath(1)
            src = src.extendToShape()
            des = des.extendToShape()
            srcFn = new_om.MFnMesh(src)
            desFn = new_om.MFnMesh(des)
            uArr, vArr = srcFn.getUVs()
            uvCounts,uvIds = srcFn.getAssignedUVs()
            desFn.clearUVs()
            desFn.setUVs(uArr, vArr)
            desFn.assignUVs(uvCounts,uvIds)

class apiTransUVs():
    def __init__(self, *arg):
        self._command()
    def _command(self):
        for c in mayaMainWindow().findChildren(QWidget,'api_trans_uvs'):
            c.showNormal()
            c.raise_()
            return
        self.api_trans_uvs = apiTransUVsUI()
        self.api_trans_uvs.showNormal()
        self.api_trans_uvs.raise_()