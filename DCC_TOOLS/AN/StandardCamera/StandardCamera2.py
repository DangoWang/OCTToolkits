#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Standard Camera Tools v1.0 
#        BY WangHaoRun
#        2017.03.22 v1.0
#        标准摄像机:
#            Create Camera  选择一个摄像机转变为标准摄像机或重建标准摄像机
#            Link Twist     给标准摄像机添加翻转
#            Look At        给自由摄像机添加目标点位置
#            Export         导出摄像机缓存*.abc
#       
#       2017.04.24 v1.35
#           1、添加LOOK AT面板和导入导出面板；
#           2、添加导入功能，导入路径对应导出路径自动创建；
#           3、添加LOOK AT的smart back方法，用于优化LOOK AT关键帧；
#           4、添加auto计算方式与manual计算方式
#           5、auto方式通过给定距离，计算出固定距离的目标点
#
#       2017.04.24 v1.40
#           1、添加选择相机后自动更新名称
#
#
#---------------------------------------------------------------


import maya.cmds as cmds
import maya.mel as mel
import pymel as pm
import os
import math
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui

try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
    import standardCameraForm2 as scf
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide import __version__
    from shiboken import wrapInstance 
    import standardCameraForm as scf

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow) 

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

# UI START

class standardCamera(object):
    def __init__(self):
        self.ui = scf.Ui_standardCameraForm(object)

        self.shotDir = "Z:/DS/Shot/"
        self.cameraDir = "Cache/ABC/Camera/"
        
        self.setMinimumSize(QSize(442, 141))
        self.setMaximumSize(QSize(442, 141))

        self.tabWidget_importExport.setHidden(True)
        self.groupBox_lookAtParameter.setHidden(True)

        self.ui.pushButton_update.clicked.connect(self.whr_update)
        self.pushButton_createCamera.clicked.connect(self.whr_createCamera)
        self.pushButton_linkTwist.clicked.connect(self.whr_createLinkTwist)
        self.pushButton_lookAt.clicked.connect(self.whr_groupBox_lookAtParameter_setHidden)
        self.pushButton_importExport.clicked.connect(self.whr_tabWidget_importExport_setHidden)

        sef
        self.pushButton_abcCacheChoose_import.clicked.connect(self.whr_abcCacheChoose_import)
        self.pushButton_abcCacheChoose_export.clicked.connect(self.whr_abcCacheChoose_export)

        self.pushButton_updatePath_import.clicked.connect(self.whr_updatePath_import)
        self.pushButton_updatePath_export.clicked.connect(self.whr_updatePath_export)

        self.pushButton_abcCache_export.clicked.connect(self.whr_cameraCache_export)
        self.pushButton_abcCache_import.clicked.connect(self.whr_cameraCache_import)

        self.pushButton_createLookAt.clicked.connect(self.whr_createLookAt)

    def whr_groupBox_lookAtParameter_setHidden(self):
        if self.groupBox_lookAtParameter.isHidden():
            self.groupBox_lookAtParameter.setHidden(False)
        else:
            self.groupBox_lookAtParameter.setHidden(True)
        self.whr_panel_size()

    def whr_tabWidget_importExport_setHidden(self):
        if self.tabWidget_importExport.isHidden():
            self.tabWidget_importExport.setHidden(False)
        else:
            self.tabWidget_importExport.setHidden(True)
        self.whr_panel_size()

    def whr_panel_size(self):
        h = 141
        if not self.groupBox_lookAtParameter.isHidden():
            h += 161
        if not self.tabWidget_importExport.isHidden():
            h += 111
        self.setMinimumSize(QSize(442, h))
        self.setMaximumSize(QSize(442, h))
        self.resize(442, h)


    @undoable
    def whr_exists(self):
        self.stdCameraTr = ""
        self.stdCameraShape = ""
        self.label_cameraName.setText("")
        self.pushButton_createCamera.setText("Create Camera")
        list_cam_tr = mel.eval('listTransforms -cameras')
        print list_cam_tr
        for cam_tr in list_cam_tr:
            if cmds.attributeQuery("StandardCamera", node=cam_tr, exists=True):
                self.stdCameraTr = cam_tr
                self.stdCameraShape = cmds.listRelatives(cam_tr, s=True, f=True)[0]
                self.label_cameraName.setText(self.stdCameraTr)
                self.pushButton_createCamera.setText("Select Camera")
                print "SC: ",self.stdCameraTr, self.stdCameraShape
                return True
        return False

    @undoable
    def whr_createCamera(self):
        filepath = cmds.file(q=True, sn=True)
        fileinfo = QFileInfo(filepath)
        print 
        if fileinfo.baseName() == "":
            QMessageBox.warning(self,"Warning","The scene did not save.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if not self.whr_exists():
            sel = cmds.ls(sl=True)
            transform = ""
            shape = ""
            if len(sel) > 0:
                if cmds.objExists(fileinfo.baseName()):
                    QMessageBox.warning(self,"Warning","The current scenario name has been occupied. \nUnable to create a standard camera.",QMessageBox.Ok, QMessageBox.Ok)
                    return
                transform = sel[0]
                if not fileinfo.baseName() == transform:
                    transform = cmds.rename(transform, fileinfo.baseName())
                shape = cmds.rename(cmds.listRelatives(transform, s=True)[0], fileinfo.baseName()+"Shape1")
                if cmds.nodeType(shape) != "camera":
                    return
            else:
                if cmds.objExists(fileinfo.baseName()):
                    QMessageBox.warning(self,"Warning","The current scenario name has been occupied. \nUnable to create a standard camera.",QMessageBox.Ok, QMessageBox.Ok)
                    return
                cameraName = cmds.camera()
                cameraName[0] = cmds.rename(cameraName[0], fileinfo.baseName())
                print cameraName
                mel.eval("cameraMakeNode 2 \""+cameraName[0]+"\";")
                transform = cameraName[0]
                shape = cmds.rename(cmds.listRelatives(transform, s=True)[0], fileinfo.baseName()+"Shape1")

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

            self.whr_exists()
        else:
            cmds.select(self.stdCameraTr, r=True)


    @undoable
    def whr_createLinkTwist(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            grp = cmds.listConnections(self.stdCameraTr+".rx", d=False, s=True)
            cmds.connectAttr(self.stdCameraTr+".twist", grp[0]+".twist")
        except Exception,e:
            QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)

    def whr_abcCacheChoose_import(self):
        multipleFilters = "Abc Files (*.abc)"
        abcpath = cmds.fileDialog2(cap="Import Camera ABC Cache:",okc="Import", fileFilter=multipleFilters, fileMode=1, dialogStyle=2, dir=self.lineEdit_abcCacheFilePath_import.text())
        if not abcpath is None:
            self.lineEdit_abcCacheFilePath_import.setText(abcpath[0])

    def whr_abcCacheChoose_export(self):
        multipleFilters = "Abc Files (*.abc)"
        abcpath = cmds.fileDialog2(cap="Export Camera ABC Cache:",okc="Export", fileFilter=multipleFilters, dialogStyle=2, dir=self.lineEdit_abcCacheFilePath_export.text())
        if not abcpath is None:
            self.lineEdit_abcCacheFilePath_export.setText(abcpath[0])

    def whr_update(self):
        self.whr_exists()
        #self.whr_updatePath_import()
        #self.whr_updatePath_export()

    def whr_updatePath_import(self):
        abcpath = ""
        scenepath = cmds.file(q=True, sn=True)
        scene_filename = QFileInfo(scenepath).baseName()
        if self.shotDir in scenepath:
            list_path = scenepath.split("/")
            n = len(list_path)
            for i in range(0, n-3):
                abcpath += list_path[i] + "/"
            list_name = list_path[n-1].split(".")
            if len(list_name) > 2:
                QMessageBox.warning(self,"Warning","File name error: '.'",QMessageBox.Ok, QMessageBox.Ok)
                return
            abcpath += self.cameraDir
            if not os.path.exists(abcpath):
                os.makedirs(abcpath)
            filename = list_name[0]
            list_n = filename.split("_")
            path = abcpath + scene_filename + "_0.abc"
            i=0
            while os.path.exists(path):
                i += 1
                path = abcpath + scene_filename +"_"+ str(i) + ".abc"
            path = abcpath + scene_filename +"_"+ str(i-1) + ".abc"
            self.lineEdit_abcCacheFilePath_import.setText(path)
            self.lineEdit_abcCacheFilePath_import.setToolTip(path)
        else:
            QMessageBox.warning(self,"Warning","Scene file path for errors.\ni.e. "+self.shotDir,QMessageBox.Ok, QMessageBox.Ok)


    def whr_updatePath_export(self):
        abcpath = ""
        scenepath = cmds.file(q=True, sn=True)
        scene_filename = QFileInfo(scenepath).baseName()
        if self.shotDir in scenepath:
            list_path = scenepath.split("/")
            n = len(list_path)
            for i in range(0, n-3):
                abcpath += list_path[i] + "/"
            list_name = list_path[n-1].split(".")
            if len(list_name) > 2:
                QMessageBox.warning(self,"Warning","File name error: '.'",QMessageBox.Ok, QMessageBox.Ok)
                return
            abcpath += self.cameraDir
            if not os.path.exists(abcpath):
                os.makedirs(abcpath)
            filename = list_name[0]
            list_n = filename.split("_")
            path = abcpath + scene_filename + "_0.abc"
            i=0
            while os.path.exists(path):
                i += 1
                path = abcpath + scene_filename +"_"+ str(i) + ".abc"
            self.lineEdit_abcCacheFilePath_export.setText(path)
            self.lineEdit_abcCacheFilePath_export.setToolTip(path)
        else:
            QMessageBox.warning(self,"Warning","Scene file path for errors.\ni.e. "+self.shotDir,QMessageBox.Ok, QMessageBox.Ok)


    @undoable
    def whr_cameraCache_export(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        abcpath = self.lineEdit_abcCacheFilePath_export.text()
        print abcpath
        if abcpath == "":
            QMessageBox.warning(self,"Warning","Export path is empty.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","File already exists, click U button to update the path.",QMessageBox.Ok, QMessageBox.Ok)
            return
        min = int(cmds.playbackOptions(q=True, min=True))
        max = int(cmds.playbackOptions(q=True, max=True))
        e = "AbcExport -verbose -j \"-frameRange "+str(min)+" "+str(max)+" -stripNamespaces -worldSpace -dataFormat ogawa -root "+self.stdCameraTr+" -file "+abcpath+"\";"
        try:
            mel.eval(e)
        except RuntimeError, e:
            QMessageBox.warning(self,"Warning","Export command execution error. \nCommand: "+e,QMessageBox.Ok, QMessageBox.Ok)
            return
        if not os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","Export the cache does not exist.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            QMessageBox.information(self,"Successful","Successful the export cache.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)

    @undoable
    def whr_cameraCache_import(self):
        abcpath = self.lineEdit_abcCacheFilePath_import.text()
        print abcpath
        if abcpath == "":
            QMessageBox.warning(self,"Warning","Import path is empty.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if not os.path.exists(abcpath):
            QMessageBox.warning(self,"Warning","Import the cache does not exist, click U button to update the path.",QMessageBox.Ok, QMessageBox.Ok)
            return
        e = "AbcImport -mode import \""+abcpath+"\";"
        if mel.eval(e):
            QMessageBox.information(self,"Successful","Successful the import cache.\n"+abcpath,QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Warning","Import command execution error. \nCommand: "+e,QMessageBox.Ok, QMessageBox.Ok)
            


    def whr_createLookAt_auto(self):
        if self.radioButton_auto.isChecked():
            pass

    def whr_createLookAt_manual(self):
        if self.radioButton_manual.isChecked():
            pass

    def whr_createLookAt_framesPerSample(self):
        if self.radioButton_framesPerSample.isChecked():
            pass

    def whr_createLookAt_smartBake(self):
        if self.radioButton_smartBake.isChecked():
            pass

    @undoable
    def whr_createLookAt(self):
        if not self.whr_exists():
            QMessageBox.warning(self,"Warning","No standard camera.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.connectionInfo(self.stdCameraShape+".centerOfInterest", id=True):
            QMessageBox.warning(self,"Warning","The standard camera have aim constraint.",QMessageBox.Ok, QMessageBox.Ok)
            cmds.select(self.stdCameraTr, r=True)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotX", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotY", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotZ", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateX") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateX", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateX"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateY") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateY", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateY"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return
        if cmds.getAttr(self.stdCameraTr+".rotatePivotTranslateZ") != 0 or cmds.connectionInfo(self.stdCameraTr+".rotatePivotTranslateZ", id=True):
            QMessageBox.warning(self,"Warning",self.stdCameraTr+".rotatePivotTranslateZ"+" not's zero or have include animation.",QMessageBox.Ok, QMessageBox.Ok)
            return

        try:
            min = int(cmds.playbackOptions(q=True, min=True))
            max = int(cmds.playbackOptions(q=True, max=True))
            loc_aim = ""

            cmds.currentTime(min)
            if self.radioButton_auto.isChecked():
                loc_aim = cmds.spaceLocator(n="loc_aim")[0]#look_at
                cmds.parent(loc_aim, self.stdCameraTr)
                cmds.setAttr(loc_aim+".tx", 0)
                cmds.setAttr(loc_aim+".ty", 0)
                cmds.setAttr(loc_aim+".tz", -self.doubleSpinBox_distance.value())
                cmds.setAttr(loc_aim+".rx", 0)
                cmds.setAttr(loc_aim+".ry", 0)
                cmds.setAttr(loc_aim+".rz", 0)
                constraint_temp = cmds.parentConstraint( self.stdCameraTr, loc_aim, mo=True, weight=1)
                cmds.parent(loc_aim, w=True)
                cmds.bakeResults(loc_aim+".t", simulation=True, t=(min, max))
                cmds.delete(constraint_temp)

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

            if self.radioButton_manual.isChecked():
                sel = cmds.ls(sl=True)
                loc = sel[0]
                key = []
                if cmds.nodeType(loc) == "transform" and cmds.nodeType(cmds.listRelatives(loc, s=True)[0]) == "locator":
                    dds = cmds.createNode("distanceDimShape")
                    cmds.connectAttr(loc+".worldPosition", dds+".startPoint")
                    loc_end = cmds.spaceLocator(n="loc_end")[0]
                    cmds.setAttr( loc_end+".tx",lock = True)
                    cmds.setAttr( loc_end+".ty",lock = True)
                    cmds.setAttr( loc_end+".tz",lock = True)
                    cmds.setAttr( loc_end+".rx",lock = True)
                    cmds.setAttr( loc_end+".ry",lock = True)
                    cmds.setAttr( loc_end+".rz",lock = True)
                    cmds.parent(loc_end, self.stdCameraTr)
                    cmds.connectAttr(loc_end+".worldPosition", dds+".endPoint")

                    loc_temp = cmds.spaceLocator(n="loc_temp")[0]
                    cmds.setAttr( loc_temp+".tx",lock = True)
                    cmds.setAttr( loc_temp+".ty",lock = True)
                    cmds.setAttr( loc_temp+".tz",-5)
                    #cmds.setAttr( loc_temp+".tz",lock = True)
                    cmds.setAttr( loc_temp+".rx",lock = True)
                    cmds.setAttr( loc_temp+".ry",lock = True)
                    cmds.setAttr( loc_temp+".rz",lock = True)
                    cmds.parent(loc_temp, self.stdCameraTr)

                    loc_aim = cmds.spaceLocator(n="loc_aim")[0]#look_at

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
                        QMessageBox.critical(self,"Error","The target point is not key animation.",QMessageBox.Ok, QMessageBox.Ok)
                        return
                        '''
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
                        '''
                    else:
                        for k in range(min, max+1):#key
                            cmds.currentTime(k)
                            ta = cmds.xform(loc, t=1,ws=True, q=1)
                            tb = cmds.xform(loc_temp, t=1,ws=True, q=1)
                            tz = cmds.xform(loc_end, t=1,ws=True, q=1)
                            di = cmds.getAttr(dds+".distance")
                            print "di:",di
                            va = om.MVector(ta) - om.MVector(tz)
                            vb = om.MVector(tb) - om.MVector(tz)
                            print va,vb, -di*math.sin(va.angle(vb))
                            cmds.setAttr(loc_temp+".tz", -di*math.cos(vb.angle(va)))
                            t = cmds.xform(loc_temp, t=1,ws=True, q=1)
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
                    QMessageBox.warning(self,"Warning","Please selection a locator for aim.",QMessageBox.Ok, QMessageBox.Ok)

            if self.radioButton_smartBake.isChecked():
                tt = self.doubleSpinBox_tolerance.value()
                cmds.filterCurve( loc_aim+".translateX", loc_aim+".translateY", loc_aim+".translateZ",f = "simplify", timeTolerance = tt )
                    
        except Exception,e:
            QMessageBox.critical(self,"Error",str(e),QMessageBox.Ok, QMessageBox.Ok)
        
class standardCameraDialog(QDialog,Ui_standardCameraForm):
    def __init__(self, *args, **kwargs):
        if cmds.window("standardCameraForm", exists=True):
            cmds.deleteUI("standardCameraForm", window=True)
        super(standardCameraDialog, self).__init__(*args, **kwargs)
        self.setupUi( self )

def main():
    ui = standardCameraDialog(mayaMainWindow)

    ui.show()

main()