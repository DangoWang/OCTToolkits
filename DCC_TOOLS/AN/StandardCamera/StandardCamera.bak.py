#!/usr/bin/env python
# -*- coding:utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Standard Camera Tools v1.0 
#        BY WangHaoRun
#        2017.03.22
#        标准摄像机:
#            Create Camera  选择一个摄像机转变为标准摄像机或重建标准摄像机
#            Link Twist     给标准摄像机添加翻转
#            Look At        给自由摄像机添加目标点位置
#            Export         导出摄像机缓存*.abc
#
#
#---------------------------------------------------------------

from PySide import QtCore, QtGui
import os
from maya import cmds
from maya import mel
from PySide.QtCore import * 
from PySide.QtGui import * 
from PySide.QtUiTools import *
from shiboken import wrapInstance
import math
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 

def undoable(function):
    '''A decorator that will make commands undoable in maya'''

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

class StandardCamera(QWidget):
    stdCameraTr = ""
    stdCameraShape = ""
    def __init__(self, *args, **kwargs):
        if cmds.window("StandardCameraUI", exists=True):
            cmds.deleteUI("StandardCameraUI", window=True)
        super(StandardCamera, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags( Qt.Window )
        self.setWindowTitle( "Standard Camera v0.8 By GoodRun" )
        self.setupUi(self)
        if not self.whr_exists():
            QtGui.QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
        
        
    def setupUi(self, StandardCameraUI):
        StandardCameraUI.setObjectName("StandardCameraUI")
        StandardCameraUI.resize(341, 92)
        StandardCameraUI.setMinimumSize(341, 92)
        StandardCameraUI.setMaximumSize(341, 92)
        self.hBoxLayout = QtGui.QHBoxLayout()
        self.hBoxLayout.setContentsMargins(6,6,6,6)
        self.hBoxLayout.setSpacing(3)
        StandardCameraUI.setLayout(self.hBoxLayout)
        self.button1 = QtGui.QPushButton()
        self.button1.setText("Create Camera")
        self.button1.setBaseSize(80,80)
        self.button1.setMinimumSize(80,80)
        self.button1.setMaximumSize(80,80)
        self.button2 = QtGui.QPushButton()
        self.button2.setText("Link Twist")
        self.button2.setBaseSize(80,80)
        self.button2.setMinimumSize(80,80)
        self.button2.setMaximumSize(80,80)
        self.button3 = QtGui.QPushButton()
        self.button3.setText("Look At")
        self.button3.setBaseSize(80,80)
        self.button3.setMinimumSize(80,80)
        self.button3.setMaximumSize(80,80)
        self.button4 = QtGui.QPushButton()
        self.button4.setText("Export")
        self.button4.setBaseSize(80,80)
        self.button4.setMinimumSize(80,80)
        self.button4.setMaximumSize(80,80)
        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        self.hBoxLayout.addWidget(self.button4)

        self.button1.clicked.connect(self.whr_createCamera)
        self.button2.clicked.connect(self.whr_createLinkTwist)
        self.button3.clicked.connect(self.whr_createLookAt)
        self.button4.clicked.connect(self.whr_exportCamera)

    @undoable
    def whr_exists(self):
        self.stdCameraTr = ""
        all_cam = cmds.ls(typ="camera")
        ok = False
        for cam in all_cam:
            tr = cmds.listRelatives( cam, allParents=True )
            if cmds.attributeQuery("StandardCamera", node=tr[0], exists=True):
                self.stdCameraTr = tr[0]
                self.stdCameraShape = cam
                self.button1.setText(self.stdCameraTr)
                ok = True
        print "StandardCamera: ", self.stdCameraTr
        return ok

    @undoable
    def whr_createCamera(self):
        if not self.whr_exists():
            sel = cmds.ls(sl=True)
            transform = ""
            shape = ""
            if len(sel) > 0:
                transform = sel[0]
                shape = cmds.listRelatives(transform, s=True)[0]
                if cmds.nodeType(shape) != "camera":
                    return
            else:
                cameraName = cmds.camera()
                mel.eval("cameraMakeNode 2 \""+cameraName[0]+"\";")
                transform = cameraName[0]
                shape = cameraName[1]

            cmds.setAttr( transform+'.rotateOrder', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateX', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateY', keyable=True )
            cmds.setAttr( transform+'.rotatePivotTranslateZ', keyable=True )
            cmds.setAttr( transform+'.rotatePivotX', keyable=True )
            cmds.setAttr( transform+'.rotatePivotY', keyable=True )
            cmds.setAttr( transform+'.rotatePivotZ', keyable=True )

            cmds.addAttr( transform, nn="0. -------STC-------", ln="StandardCamera", at="enum", en="Main Camera")
            cmds.setAttr( transform+'.StandardCamera', e=True, keyable=True, lock=True)

            cmds.addAttr( transform, ln="focalLength", at="double", dv=35)
            cmds.setAttr( transform+'.focalLength', e=True, keyable=True)
            cmds.setAttr( transform+'.focalLength', cmds.getAttr(shape+'.focalLength'))
            if cmds.connectionInfo(shape+".focalLength", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focalLength", sfd=True), transform+".focalLength")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focalLength", sfd=True), shape+".focalLength")
            cmds.connectAttr(transform+".focalLength", shape+".focalLength")

            cmds.addAttr( transform, nn="1. -------DOF-------", ln="depthOfField", at="enum", en="off:on:")
            cmds.setAttr( transform+'.depthOfField', e=True, keyable=True)
            cmds.setAttr( transform+'.depthOfField', cmds.getAttr(shape+'.depthOfField'))
            cmds.connectAttr(transform+".depthOfField", shape+".depthOfField")

            cmds.addAttr( transform, ln="focusDistance", at="double", dv=6)
            cmds.setAttr( transform+'.focusDistance', e=True, keyable=True)
            cmds.setAttr( transform+'.focusDistance', cmds.getAttr(shape+'.focusDistance'))
            if cmds.connectionInfo(shape+".focusDistance", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focusDistance", sfd=True), transform+".focusDistance")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focusDistance", sfd=True), shape+".focusDistance")
            cmds.connectAttr(transform+".focusDistance", shape+".focusDistance")

            cmds.addAttr( transform, ln="fStop", at="double", dv=5)
            cmds.setAttr( transform+'.fStop', e=True, keyable=True)
            cmds.setAttr( transform+'.fStop', cmds.getAttr(shape+'.fStop'))
            if cmds.connectionInfo(shape+".fStop", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".fStop", sfd=True), transform+".fStop")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".fStop", sfd=True), shape+".fStop")
            cmds.connectAttr(transform+".fStop", shape+".fStop")

            cmds.addAttr( transform, ln="focusRegionScale", at="double", dv=1)
            cmds.setAttr( transform+'.focusRegionScale', e=True, keyable=True)
            cmds.setAttr( transform+'.focusRegionScale', cmds.getAttr(shape+'.focusRegionScale'))
            if cmds.connectionInfo(shape+".focusRegionScale", id=True):
                cmds.connectAttr(cmds.connectionInfo(shape+".focusRegionScale", sfd=True), transform+".focusRegionScale")
                cmds.disconnectAttr(cmds.connectionInfo(shape+".focusRegionScale", sfd=True), shape+".focusRegionScale")
            cmds.connectAttr(transform+".focusRegionScale", shape+".focusRegionScale")

            cmds.addAttr( transform, nn="2. -------AIM-------", ln="AIM", at="enum", en="------------:")

            cmds.setAttr( transform+'.AIM', e=True, keyable=True, lock=True)
            cmds.addAttr( transform, ln="twist", at="doubleAngle", dv=0)
            cmds.setAttr( transform+'.twist', keyable=True )

            cmds.camera(transform, e=True, displaySafeAction=True, displaySafeTitle=True)
            self.button1.setText("Select Camera")
            print "ok"
        else:
            cmds.select(self.stdCameraTr, r=True)
    
    @undoable
    def whr_createLookAt(self):
        if not self.whr_exists():
            QtGui.QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.connectionInfo(self.stdCameraShape+".centerOfInterest", id=True):
            QtGui.QMessageBox.warning(self,"Warning","The standard camera have aim constraint.",QMessageBox.Ok, QMessageBox.Ok)
            cmds.select(self.stdCameraTr, r=True)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotX", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotY", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotZ", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateX", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateY", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateZ", id=True):
            QtGui.QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return

        try:
            sel = cmds.ls(sl=True)
            loc = sel[0]
            key = []
            if cmds.nodeType(loc) == "transform" and cmds.nodeType(cmds.listRelatives(loc, s=True)[0]) == "locator":
                dds = cmds.createNode("distanceDimShape")
                cmds.connectAttr(loc+".worldPosition", dds+".startPoint")
                loc_end = cmds.spaceLocator()[0]
                cmds.setAttr( loc_end+".tx",lock = True)
                cmds.setAttr( loc_end+".ty",lock = True)
                cmds.setAttr( loc_end+".tz",lock = True)
                cmds.setAttr( loc_end+".rx",lock = True)
                cmds.setAttr( loc_end+".ry",lock = True)
                cmds.setAttr( loc_end+".rz",lock = True)
                cmds.parent(loc_end, self.stdCameraTr)
                cmds.connectAttr(loc_end+".worldPosition", dds+".endPoint")

                loc_temp = cmds.spaceLocator()[0]
                cmds.setAttr( loc_temp+".tx",lock = True)
                cmds.setAttr( loc_temp+".ty",lock = True)
                cmds.setAttr( loc_temp+".tz",-5)
                #cmds.setAttr( loc_temp+".tz",lock = True)
                cmds.setAttr( loc_temp+".rx",lock = True)
                cmds.setAttr( loc_temp+".ry",lock = True)
                cmds.setAttr( loc_temp+".rz",lock = True)
                cmds.parent(loc_temp, self.stdCameraTr)

                loc_aim = cmds.spaceLocator(n="look_at")[0]

                tx = cmds.keyframe(loc+".tx", q=True)
                ty = cmds.keyframe(loc+".ty", q=True)
                tz = cmds.keyframe(loc+".tz", q=True)
             
                temp = []
                if not tx is None:
                    temp = temp + tx
                if not ty is None:
                    temp = temp + ty
                if not tz is None:
                    temp = temp + tz
        
                if len(temp) == 0:
                    pass
                else:
                    for t in temp:
                        if not t in key:
                            key.append(t)
                    key.sort()
                    print key

                if len(key) == 0:
                    ta = cmds.xform(loc, t=1,ws=True, q=1)
                    tb = cmds.xform(loc_temp, t=1,ws=True, q=1)
                    tz = cmds.xform(loc_end, t=1,ws=True, q=1)
                    di = cmds.getAttr(dds+".distance")
                    va = om.MVector(ta) - om.MVector(tz)
                    vb = om.MVector(tb) - om.MVector(tz)
                    print va,vb, -di*math.sin(va.angle(vb))
                    cmds.setAttr(loc_temp+".tz", -di*math.cos(vb.angle(va)))
                    cmds.xform(loc_aim,ws=1, t=cmds.xform(loc_temp, t=1,ws=True, q=1))
                    pass
                else:
                    min = int(cmds.playbackOptions(q=True, min=True))
                    max = int(cmds.playbackOptions(q=True, max=True))
                    for k in range(min, max+1):#key
                        cmds.currentTime(k)
                        ta = cmds.xform(loc, t=1,ws=True, q=1)
                        tb = cmds.xform(loc_temp, t=1,ws=True, q=1)
                        tz = cmds.xform(loc_end, t=1,ws=True, q=1)
                        di = cmds.getAttr(dds+".distance")
                        va = om.MVector(ta) - om.MVector(tz)
                        vb = om.MVector(tb) - om.MVector(tz)
                        print va,vb, -di*math.sin(va.angle(vb))
                        cmds.setAttr(loc_temp+".tz", -di*math.cos(vb.angle(va)))
                        cmds.xform(loc_aim,ws=1, t=cmds.xform(loc_temp, t=1,ws=True, q=1))
                        cmds.setKeyframe( loc_aim, attribute='t', t=k )
                        pass

                print self.stdCameraTr
                if cmds.connectionInfo(self.stdCameraTr+".rx", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rx", sfd=True), self.stdCameraTr+".rx")
                if cmds.connectionInfo(self.stdCameraTr+".ry", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".ry", sfd=True), self.stdCameraTr+".ry")
                if cmds.connectionInfo(self.stdCameraTr+".rz", id=True):
                    cmds.disconnectAttr(cmds.connectionInfo(self.stdCameraTr+".rz", sfd=True), self.stdCameraTr+".rz")
                mel.eval("cameraMakeNode 2 \""+self.stdCameraTr+"\";")
                grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)[0]
                print grp
                camera_aim = cmds.listConnections(grp+".target", d=False, s=True)[0]
                print camera_aim, grp
                cmds.parent(loc_aim, grp)
                cmds.parent(camera_aim, loc_aim)
                cmds.setAttr(camera_aim+".tx", 0)
                cmds.setAttr(camera_aim+".ty", 0)
                cmds.setAttr(camera_aim+".tz", 0)
                cmds.delete(loc_end)
                cmds.delete(loc_temp)
            else:
                QtGui.QMessageBox.warning(self,"Warning","Please selection a locator for aim.",QMessageBox.Ok, QMessageBox.Ok)
        except Exception,e:
            QtGui.QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)
       
    @undoable
    def whr_createLinkTwist(self):
        if not self.whr_exists():
            QtGui.QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)
            cmds.connectAttr(self.stdCameraTr+".twist", grp[0]+".twist")
        except Exception,e:
            QtGui.QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)

    @undoable
    def whr_exportCamera(self):
        if not self.whr_exists():
            QtGui.QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        abcpath = ""
        scenepath = ""
        scenepath = cmds.file(q=True, sn=True)
        s = "Z:/DS/Shot/"
        if s in scenepath:
            list_path = scenepath.split("/")
            n = len(list_path)
            for i in range(0, n-3):
                abcpath += list_path[i] + "/"
            list_name = list_path[n-1].split(".")
            if len(list_name) > 2:
                QtGui.QMessageBox.warning(self,"Warning","File name error: '.'",QMessageBox.Ok, QMessageBox.Ok)
                return
            abcpath += "Cache/ABC/Camera/"
            if not os.path.exists(abcpath):
                os.makedirs(abcpath)
            filename = list_name[0]
            list_n = filename.split("_")
            abcpath += filename[0:len(filename)-len(list_n[len(list_n)-1])-1] + ".abc"
            print(filename)
        else:
            multipleFilters = "Abc Files (*.abc)"
            abcpath = cmds.fileDialog2(cap="Export Camera:", fileFilter=multipleFilters, dialogStyle=2)[0]

        print abcpath
    
        min = int(cmds.playbackOptions(q=True, min=True))
        max = int(cmds.playbackOptions(q=True, max=True))
        e = "AbcExport -verbose -j \"-frameRange "+str(min)+" "+str(max)+" -stripNamespaces -worldSpace -dataFormat ogawa -root "+self.stdCameraTr+" -file "+abcpath+"\";"
        if mel.eval(e):
            QtGui.QMessageBox.warning(self,"Warning","Export camera error. \n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
            return
        if not os.path.exists(abcpath):
            QtGui.QMessageBox.warning(self,"Warning","Camera cache not exists.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            QtGui.QMessageBox.information(self,"Final","Export camera final.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
    
def main():
    ui = StandardCamera()
    ui.show()
    return ui

main()