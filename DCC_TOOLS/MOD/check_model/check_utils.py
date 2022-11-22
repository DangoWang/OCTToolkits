# -*- coding: utf-8 -*-
####################################################
# Copyright 2016 October Media. All rights reserved.
# Model Check Tools
# Author: Gao Lei
####################################################

try:
    from PySide.QtCore import Qt
    import PySide.QtGui as QtWidgets
    import shiboken
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2 import QtWidgets, QtCore
    import shiboken2 as shiboken

import sys
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as mc


# print dir(PySide2.QtGui)
# A decorator that will make commands undoable in maya
def undoable(function):
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


# get maya main window pointer
def mayaMainWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = shiboken.wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)
    return mayaMainWindow


class modCheckToolsUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(modCheckToolsUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setObjectName('oct_mod_check_tools')
        self.setWindowTitle('Model Check Tools')
        self.setStyleSheet('QWidget { font-family: "Microsoft YaHei"; }')
        self.setMinimumWidth(200)

        self.meshIntersectBtn = QtWidgets.QPushButton(u'穿插面检查')
        self.selectIntersectBtn = QtWidgets.QPushButton(u'选择穿插面')
        self.unqualVertexBtn = QtWidgets.QPushButton(u'选择非四边点')
        self.unqualFaceBtn = QtWidgets.QPushButton(u'选择非四边面')
        self.progressBar = QtWidgets.QProgressBar()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.meshIntersectBtn)
        self.mainLayout.addWidget(self.selectIntersectBtn)
        self.mainLayout.addWidget(self.unqualVertexBtn)
        self.mainLayout.addWidget(self.unqualFaceBtn)
        self.mainLayout.addWidget(self.progressBar)
        self.setLayout(self.mainLayout)

        self.meshIntersectBtn.clicked.connect(self.meshIntersectTest)
        self.selectIntersectBtn.clicked.connect(self.selectMeshIntersect)
        self.unqualVertexBtn.clicked.connect(self.selectUnqualVertex)
        self.unqualFaceBtn.clicked.connect(self.selectUnqualFace)

        self.meshIntersectList = []

    def deleteOldUI(self):
        for c in mayaMainWindow().findChildren(QtWidgets.QWidget, 'oct_mod_check_tools'):
            if c != self:
                c.deleteLater()

    def getIntersectFaces(self, mesh1, mesh2):
        fnMesh1 = om.MFnMesh(mesh1)
        fnMesh2 = om.MFnMesh(mesh2)

        edgeList = []
        edgeUtil = om.MScriptUtil()
        edgePtr = edgeUtil.asInt2Ptr()
        preUtil = om.MScriptUtil()
        prePtr = preUtil.asIntPtr()
        for i in xrange(fnMesh2.numEdges()):
            fnMesh2.getEdgeVertices(i, edgePtr)
            x = edgeUtil.getInt2ArrayItem(edgePtr, 0, 0)
            y = edgeUtil.getInt2ArrayItem(edgePtr, 0, 1)

            mItVtx = om.MItMeshVertex(mesh2)
            mItVtx.setIndex(x, prePtr)
            raySource = om.MFloatPoint(mItVtx.position(om.MSpace.kWorld))

            mItVtx.setIndex(y, prePtr)
            rayDir = om.MFloatPoint(mItVtx.position(om.MSpace.kWorld)) - raySource

            resultPoint = om.MFloatPoint()
            hitFaceUtil = om.MScriptUtil(-1)
            hitFacePtr = hitFaceUtil.asIntPtr()
            fnMesh1.closestIntersection(raySource, rayDir, None,  # faceIds
                                        None,  # triIds
                                        False,  # idsSorted
                                        om.MSpace.kWorld, 1,  # maxParam,
                                        False,  # testBothDirections,
                                        None,  # accelParams
                                        resultPoint, None,  # hitRayParam
                                        hitFacePtr,  # hitFace
                                        None,  # hitTris
                                        None,  # hitBarys1
                                        None,  # hitBarys2
                                        )
            hitFace = hitFaceUtil.getInt(hitFacePtr)
            # edgeId = '%s.e[%d]' % (mesh2.fullPathName(),i)
            if hitFace >= 0 and not i in edgeList:
                edgeList.append(i)

        faceList = []
        faceArr = om.MIntArray()
        edgeIt = om.MItMeshEdge(mesh2)
        for i in edgeList:
            edgeIt.setIndex(i, prePtr)
            faceArr.clear()
            edgeIt.getConnectedFaces(faceArr)
            for j in xrange(faceArr.length()):
                faceId = '%s.f[%d]' % (mesh2.fullPathName(), faceArr[j])
                if not faceId in faceList:
                    faceList.append(faceId)
        return faceList

    @undoable
    def meshIntersectTest(self):
        slist = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(slist)
        mesh1 = om.MDagPath()
        slist.getDagPath(0, mesh1)
        bbox1 = om.MFnTransform(mesh1).boundingBox()
        mesh1.extendToShape()

        self.meshIntersectList = []
        self.progressBar.reset()
        self.progressBar.setValue(0)
        num = slist.length() - 1
        for i in xrange(1, slist.length()):
            mesh2 = om.MDagPath()
            slist.getDagPath(i, mesh2)
            bbox2 = om.MFnTransform(mesh2).boundingBox()
            if bbox1.intersects(bbox2):
                # print mesh2.fullPathName()
                mesh2.extendToShape()
                faceList = self.getIntersectFaces(mesh1, mesh2)
                self.meshIntersectList.extend(faceList)
            self.progressBar.setValue(i * 100.0 / num)
        self.progressBar.setValue(100)
        if self.meshIntersectList:
            mc.select(self.meshIntersectList)

    @undoable
    def selectMeshIntersect(self):
        if self.meshIntersectList:
            mc.select(self.meshIntersectList)

    @undoable
    def selectUnqualVertex(self):
        self.progressBar.reset()
        slist = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(slist)
        mesh = om.MDagPath()
        slist.getDagPath(0, mesh)
        mesh.extendToShape()

        numUtil = om.MScriptUtil()
        numPtr = numUtil.asIntPtr()
        itMesh = om.MItMeshVertex(mesh)
        vlist = []
        dagName = mesh.fullPathName()
        while not itMesh.isDone():
            itMesh.numConnectedEdges(numPtr)
            if numUtil.getInt(numPtr) != 4:
                vlist.append('%s.vtx[%d]' % (dagName, itMesh.index()))
            itMesh.next()
        mc.select(vlist)

    @undoable
    def selectUnqualFace(self):
        self.progressBar.reset()
        slist = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(slist)
        mesh = om.MDagPath()
        slist.getDagPath(0, mesh)
        mesh.extendToShape()

        itMesh = om.MItMeshPolygon(mesh)
        flist = []
        dagName = mesh.fullPathName()
        edgeArr = om.MIntArray()
        while not itMesh.isDone():
            edgeArr.clear()
            itMesh.getEdges(edgeArr)
            if len(edgeArr) != 4:
                flist.append('%s.f[%d]' % (dagName, itMesh.index()))
            itMesh.next()
        mc.select(flist)


class modCheckTools():
    def __init__(self, *arg):
        self._command()

    def _command(self):
        for c in mayaMainWindow().findChildren(QtWidgets.QWidget, 'oct_mod_check_tools'):
            c.showNormal()
            c.raise_()
            return
        self.mod_check_tool = modCheckToolsUI()
        self.mod_check_tool.showNormal()
        self.mod_check_tool.raise_()
