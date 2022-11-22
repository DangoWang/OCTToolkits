#!/usr/bin/env python
# -*- coding:utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Abc Cache v1.0 
#        BY WangHaoRun
#        2019.03.06
#
#---------------------------------------------------------------

import os
import json
import AbcOutUI2 as oUI2
reload(oUI2)
import AbcCache
reload(AbcCache)
import searchDB
reload(searchDB)
from maya import cmds
from maya import mel
from maya import utils
import maya.OpenMayaUI as omui

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget) 

class outputAbcCacheDialog(QtWidgets.QDialog, oUI2.Ui_Dialog):
    err = False
    ac = AbcCache.AbcCache()

    l_column = {
        u"引用资产":0, 
        u"当前版本":1, 
        u"输出UV":2, 
        u"输出缓存":3, 
        u"输出路径":4, 
        u"提示":5
        }

    l_typ = ["CHAR", "PROP", "ENV", "CAM"]
    ser = ""

    geoGrp = "|Geometry"
    l_obj = ["|Geometry|high"]
    def __init__(self, *args, **kwargs):
        super(outputAbcCacheDialog, self).__init__(*args, **kwargs)
        self.setupUi( self )

        self.setWindowTitle(u"ABC 缓存输出 "+self.ac.version)

        header = QtWidgets.QTreeWidgetItem()
        for i in self.l_column.keys():
            header.setText(self.l_column[i], i)
        self.treeWidget.setHeaderItem(header)

        self.lineEdit_path.setReadOnly(True)

        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)

        self.label_text.setText("")
        self.treeWidget.clear()

        self.comboBox_project.addItems(self.ac.project())

        
        self.treeWidget.setColumnWidth(self.l_column[u"引用资产"], 160)
        self.treeWidget.setColumnHidden(self.l_column[u"输出UV"], True)

        self.comboBox_pathTyp.currentTextChanged.connect(self.on_comboBox_pathTyp_currentTextChanged)
        self.comboBox_project.currentTextChanged.connect(self.on_comboBox_project_currentTextChanged)
        self.pushButton_setstartframe.clicked.connect(self.on_pushButton_setstartframe_clicked)
        self.pushButton_setendframe.clicked.connect(self.on_pushButton_setendframe_clicked)
        self.pushButton_init.clicked.connect(self.on_pushButton_init_clicked)
        self.pushButton_output.clicked.connect(self.on_pushButton_output_clicked)
        self.pushButton_saveInfo.clicked.connect(self.on_pushButton_saveInfo_clicked)
        self.pushButton_setpath.clicked.connect(self.setpath)

        self.ctrl_setcolor(-1)

        pass

    def setpath(self):
        path = cmds.fileDialog2(cap="OutPut Path:", dialogStyle=2, fileMode=3)
        self.lineEdit_path.setText(path[0])
        self.ctrl_setcolor(0)

    def ctrl_setcolor(self, i):
        self.pushButton_init.setStyleSheet("background:#555555")
        self.pushButton_saveInfo.setStyleSheet("background:#555555")
        self.pushButton_output.setStyleSheet("background:#555555")

        if i==0:
            self.pushButton_init.setStyleSheet("background:#444499")
        elif i==1:
            self.pushButton_saveInfo.setStyleSheet("background:#444499")
        elif i==2:
            self.pushButton_output.setStyleSheet("background:#444499")
        elif i==3:
            self.pushButton_saveInfo.setStyleSheet("background:#444499")
            self.pushButton_output.setStyleSheet("background:#444499")
        else:
            pass

        
    def check(self):
        if self.err:
            QtWidgets.QMessageBox.warning(self, u"警告：", u"引用文件的名字空间不正确，名字空间 = 引用的文件名。\n保存配置文件失败。")
            self.ctrl_setcolor(0)
            return False

        '''
        if cmds.file(modified=True, q=True):
            QtWidgets.QMessageBox.warning(self, u"警告：", u"场景有变动，请保存后，重新初始化。")
            self.err = True
            self.setColor()
            return False
            '''

        if self.lineEdit_path.text() == "":
            QtWidgets.QMessageBox.warning(self, u"警告：", u"没有缓存输出路径，请尝试初始化。\n保存配置文件失败。")
            self.ctrl_setcolor(0)
            return False

        return True
    def on_comboBox_pathTyp_currentTextChanged(self, str):
        self.lineEdit_taskname.clear()
        self.lineEdit_taskver.clear()
        self.lineEdit_path.clear()
        
        if self.comboBox_pathTyp.currentIndex() == 1:
            self.pushButton_setpath.setEnabled(True)
            self.lineEdit_path.setReadOnly(True)
        else:
            self.pushButton_setpath.setEnabled(True)
            self.lineEdit_path.setReadOnly(True)

    def on_comboBox_project_currentTextChanged(self, str):
        self.lineEdit_taskname.clear()
        self.lineEdit_taskver.clear()
        self.lineEdit_path.clear()
        self.treeWidget.clear()
        self.ser = self.ac.savepath(self.comboBox_project.currentText())
        self.taskinfo = searchDB.taskInfo(self.comboBox_project.currentText())
        self.ctrl_setcolor(0)
        pass

    def on_pushButton_setstartframe_clicked(self):
        self.spinBox_startframe.setValue(cmds.playbackOptions( q=True, min=True ))
        pass

    def on_pushButton_setendframe_clicked(self):
        self.spinBox_endframe.setValue(cmds.playbackOptions( q=True, max=True ))
        pass

    def on_pushButton_init_clicked(self):
        self.ctrl_close()

        # try:

        self.err = False

        self.progressBar.setValue(0)
        self.label_text.setText(u"提示：正在初始化...")

        if self.comboBox_project.currentText() == "":
            QtWidgets.QMessageBox.critical(self, u"错误：", u"请选择项目。")
            self.label_text.setText(u"错误：请选择项目。")
            self.ctrl_open()
            return

        scene = cmds.file(q=True, sn=True)
        if scene == "":
            QtWidgets.QMessageBox.critical(self, u"错误：", u"场景名称为空，未保存场景。")
            self.label_text.setText(u"错误：场景名称为空，未保存场景。")
            self.ctrl_open()
            return

        filename = QtCore.QFileInfo(scene).baseName()

        if self.comboBox_pathTyp.currentIndex() == 1:
            if self.lineEdit_path.text() == "":
                QtWidgets.QMessageBox.critical(self, u"错误：", u"未指定输出路径。")
                self.label_text.setText(u"错误：未指定输出路径。")
                self.ctrl_open()
                return
        else:
            if not self.lineEdit_taskname.text():
                self.lineEdit_taskname.setText(filename)
            ti = self.taskinfo.searchTaskInfoDict('s'+self.lineEdit_taskname.text().lstrip('dsf_'))
            if not ti:
                ti = self.taskinfo.searchTaskInfoDict(self.lineEdit_taskname.text())
            self.lineEdit_taskver.setText(str(ti["pversion"]))
            self.lineEdit_path.setText(self.ser+"/"+ti["scene"]+"/"+ti["name"]+"/"+ti["group"]+"/"+self.lineEdit_taskver.text())

        self.spinBox_startframe.setValue(70)
        self.spinBox_endframe.setValue(cmds.playbackOptions( q=True, max=True ))

        self.treeWidget.clear()
        for typ in self.l_typ:
            # typ : 'CHAR'
            if cmds.objExists("|"+typ):
                item = QtWidgets.QTreeWidgetItem()
                item.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                item.setText(self.l_column[u"引用资产"], typ)
                self.treeWidget.addTopLevelItem(item)
                if typ in ['CAM']:
                    an_start = cmds.playbackOptions(min=True, query=True)
                    an_end = cmds.playbackOptions(max=True, query=True)
                    path = self.lineEdit_path.text()+'/CAM/' + \
                           self.lineEdit_taskname.text() + '_' + str(int(an_start)) + '_' + str(int(an_end)) + '.abc'
                    item.setCheckState(self.l_column[u"输出缓存"], QtCore.Qt.Checked)
                    item.setText(self.l_column[u"输出路径"], path)
                    print item.text(self.l_column[u"输出路径"])
                    continue
                # typ : 'CHAR'
                l_ref = cmds.listRelatives( "|"+typ, children=True, f=True, pa=True )
                if l_ref != None:
                    for ref in l_ref:
                        ns = cmds.referenceQuery(ref, namespace=True, shortName=True)
                        item_ref = QtWidgets.QTreeWidgetItem()
                        item_ref.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                        item_ref.setText(self.l_column[u"引用资产"], ref.split("|")[-1])
                        item_ref.setToolTip(self.l_column[u"引用资产"], ref)
                        fn_ref = QtCore.QFileInfo(cmds.referenceQuery(ref, filename=True, shortName=True )).baseName()
                        namespace = cmds.referenceQuery(ref, namespace=True )
                        if '_V' in fn_ref and '_V' not in namespace:
                            fn_ref = fn_ref.split('_V')[0]
                        ti_ref = self.taskinfo.searchTaskInfoDict(fn_ref)
                        item_ref.setText(self.l_column[u"当前版本"], str(ti_ref["pversion"]))
                        if not ti_ref["name_en"] in ns:
                            item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.red)
                            item_ref.setText(self.l_column[u"提示"], u"错误：引用文件的名字空间不正确，名字空间=引用的文件名。")
                            self.err = True
                        if ti_ref["classify"] != "":
                            p = self.lineEdit_path.text()+"/"+ti_ref["name"]+"/"+ti_ref["group"]+"/"+ns+"/"+"{datetime}"+".abc"
                            item_ref.setText(self.l_column[u"输出路径"], p)
                        for obj in self.l_obj:
                            high = ref + obj.replace("|", "|"+ns+":")
                            if cmds.objExists(high):
                                item_ref.setCheckState(self.l_column[u"输出缓存"], QtCore.Qt.Checked)
                                item_ref.setCheckState(self.l_column[u"输出UV"], QtCore.Qt.Unchecked)
                                item_hig = QtWidgets.QTreeWidgetItem()
                                item_hig.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                                item_hig.setText(self.l_column[u"引用资产"], high.split('|')[-1][len(ns+":"):])
                                item_hig.setToolTip(self.l_column[u"引用资产"], high)
                                item_ref.addChild(item_hig)
                                obj = ref + obj.replace("|", "|"+ns+":")
                                if cmds.objExists(obj):
                                    children_hi = cmds.listRelatives( obj, children=True, fullPath=True, pa=True  )
                                    for c_hi in children_hi:
                                        item_obj = QtWidgets.QTreeWidgetItem()
                                        item_obj.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                                        item_obj.setText(self.l_column[u"引用资产"], c_hi.split('|')[-1][len(ns+":"):])
                                        item_obj.setToolTip(self.l_column[u"引用资产"], c_hi)
                                        item_hig.addChild(item_obj)
                        geo = ref+self.geoGrp.replace("|", "|"+ns+":")
                        if cmds.objExists(geo):
                            item.addChild(item_ref)
                            item.setExpanded(True)

        if self.check():
            self.ctrl_setcolor(3)
        
        # except:
        #     self.label_text.setText(u"错误：初始化出现未知错误！")
        #     pass

        self.label_text.setText(u"成功：初始化完成！")
        self.ctrl_open()
        pass

    def on_pushButton_output_clicked(self):
        self.ctrl_close()

        # try:
        path = self.lineEdit_path.text()+"/setup.json"
        if self.saveInfo(path):
            self.outputAbc(path)
            self.pushButton_output.setStyleSheet("background:#555555")
        # except:
        #     pass

        self.ctrl_open()

    def outputAbc(self, setup):
        if not cmds.pluginInfo('AbcExport', query=1, loaded=1):
            try:
                cmds.loadPlugin('AbcExport.mll')
            except RuntimeError:
                raise RuntimeError('AbcExport.mll was not found on MAYA_PLUG_IN_PATH')
        self.label_text.setText(u"提示：读取配置文件...")
        l_cmd = self.ac.loadSetup(setup)
        self.progressBar.setMaximum(len(l_cmd))

        self.label_text.setText(u"提示：正在输出...")
        for j in range(0, len(l_cmd)):
            cmd = l_cmd[j]
            self.progressBar.setValue(j)
            utils.processIdleEvents()
            utils.executeInMainThreadWithResult( self.ac.outputAbc, cmd )

        self.progressBar.setValue(self.progressBar.maximum())
        self.label_text.setText(u"提示：缓存输出完成！")

    def saveInfo(self, path):
        if not self.check():
            return False
        else:
            info = {}
            info["project"] = self.comboBox_project.currentText()
            info["start"] = self.spinBox_startframe.value()
            info["end"] = self.spinBox_endframe.value()
            info["scenename"] = self.lineEdit_taskname.text()
            info["version"] = self.lineEdit_taskver.text()
            info_typ = {}
            for i in range(0, self.treeWidget.topLevelItemCount()):
                item_t = self.treeWidget.topLevelItem(i)
                typ = item_t.text(0)
                if typ in ['CAM']:
                    cam_abc_path = item_t.text(self.l_column[u"输出路径"])
                    info_typ[typ] = cam_abc_path
                    continue
                # typ: CHAR
                info_refs = []
                for j in range(0, item_t.childCount()):
                    item_ref = item_t.child(j)
                    #print item_ref.text(0)
                    ns = cmds.referenceQuery(item_ref.text(0), namespace=True, shortName=True)
                    fn_ref = QtCore.QFileInfo(cmds.referenceQuery(item_ref.text(0), filename=True, shortName=True )).baseName()
                    namespace = cmds.referenceQuery(item_ref.text(0), namespace=True)
                    if '_V' in fn_ref and '_V' not in namespace:
                        fn_ref = fn_ref.split('_V')[0]
                    ti_ref = self.taskinfo.searchTaskInfoDict(fn_ref)
                    info_ref = {}
                    info_ref["namespace"] = ns
                    info_ref["name"] = ti_ref["name"]
                    info_ref["name_en"] = ti_ref["name_en"]
                    info_ref["group"] = ti_ref["group"]
                    info_ref["version"] = ti_ref["pversion"]
                    info_ref["output"] = item_ref.text(self.l_column[u"输出路径"])
                    info_ref["isuv"] = int(item_ref.checkState(self.l_column[u"输出UV"]))
                    info_ref["isout"] = int(item_ref.checkState(self.l_column[u"输出缓存"]))
                    if info_ref["output"] != "":
                        info_hig = {}
                        for k in range(0, item_ref.childCount()):
                            item_hig = item_ref.child(k)
                            info_obj = []
                            for l in range(0, item_hig.childCount()):
                                item_obj = item_hig.child(l)
                                info_obj.append(item_obj.toolTip(0))
                            info_hig[item_hig.toolTip(0)] = info_obj
                        info_ref["objects"] = info_hig
                    info_refs.append(info_ref)
                info_typ[typ] = info_refs
                #print typ
                #print info_refs
            info["typ"] = info_typ
            if not os.path.exists(self.lineEdit_path.text()):
                os.makedirs(self.lineEdit_path.text())
            with open(path, 'w') as json_file:
                json.dump(info, json_file, indent=4, ensure_ascii = False)
            pass
            return True
        

    def on_pushButton_saveInfo_clicked(self):
        self.ctrl_close()

        # try:
        if self.saveInfo(self.lineEdit_path.text()+"/setup.json"):
            self.pushButton_saveInfo.setStyleSheet("background:#555555")
        # except:
        #     pass

        self.ctrl_open()

        

    def ctrl_close(self):
        self.pushButton_init.setEnabled(True)
        self.pushButton_saveInfo.setEnabled(True)
        self.pushButton_output.setEnabled(True)

    def ctrl_open(self):
        self.pushButton_init.setEnabled(True)
        self.pushButton_saveInfo.setEnabled(True)
        self.pushButton_output.setEnabled(True)

def main():
    OACD = outputAbcCacheDialog(mayaMainWindow)
    OACD.show()
