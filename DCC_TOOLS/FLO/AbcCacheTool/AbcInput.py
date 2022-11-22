#!/usr/bin/env python
# -*- coding:GBK -*-

# ---------------------------------------------------------------
#
#        OCT Abc Cache v1.0 
#        BY WangHaoRun
#        2019.03.06
#
# ---------------------------------------------------------------

import os
import json
import AbcInUI2 as iUI2

reload(iUI2)
import AbcCache

reload(AbcCache)
import searchDB
import uv_load.main as uvin
reload(uvin)

reload(searchDB)
from maya import cmds
from maya import mel
from maya import utils
import maya.OpenMayaUI as omui

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)


class WHRComboBox(QtWidgets.QComboBox):
    whr_item = None

    def setWHRItem(self, whr_item):
        self.whr_item = whr_item



class inputAbcCacheDialog(QtWidgets.QDialog, iUI2.Ui_Dialog):
    ac = AbcCache.AbcCache()
    ser = ""

    l_column = {u"引用资产": 0,
                u"目标资产": 1,
                u"目标环节": 2,
                u"本地文件": 3,
                u"导入UV": 4,
                u"导入缓存": 5,
                u"缓存来源": 6,
                u"缓存版本": 7,
                u"提示": 8}

    def __init__(self, *args, **kwargs):
        super(inputAbcCacheDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle(u"ABC 缓存加载 " + self.ac.version)

        header = QtWidgets.QTreeWidgetItem()
        for i in self.l_column.keys():
            header.setText(self.l_column[i], i)
        self.treeWidget.setHeaderItem(header)

        self.treeWidget.clear()

        self.comboBox_project.addItems(self.ac.project())

        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)

        self.label_text.setText("")

        self.treeWidget.setColumnWidth(self.l_column[u"引用资产"], 160)
        self.treeWidget.setColumnHidden(self.l_column[u"导入UV"], True)

        self.pushButton_setpath.clicked.connect(self.setpath)

        self.pushButton_loadsetup.setStyleSheet("background:#444499")

        self.pushButton_loadasset.setStyleSheet("background:#555555")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#555555")
        # self.pushButton_loadcache.setEnabled(False)

        self.comboBox_project.currentTextChanged.connect(self.on_comboBox_project_currentTextChanged)
        self.comboBox_scene.currentTextChanged.connect(self.on_comboBox_scene_currentTextChanged)
        self.comboBox_name.currentTextChanged.connect(self.on_comboBox_name_currentTextChanged)
        self.comboBox_fromgroup.currentTextChanged.connect(self.on_comboBox_fromgroup_currentTextChanged)
        self.comboBox_ver.currentTextChanged.connect(self.on_comboBox_ver_currentTextChanged)
        self.pushButton_loadsetup.clicked.connect(self.on_pushButton_loadsetup_clicked)
        self.pushButton_loadasset.clicked.connect(self.on_pushButton_loadasset_clicked)
        self.pushButton_loadcache.clicked.connect(self.on_pushButton_loadcache_clicked)

        self.treeWidget.itemDoubleClicked.connect(self.on_treeWidget_itemDoubleClicked)

        pass

    def setpath(self):
        basicFilter = "setup.json"
        path = cmds.fileDialog2(fileFilter=basicFilter, cap="InPut Path:", dialogStyle=2, fileMode=1)
        self.lineEdit_path.setText(os.path.dirname(path[0]))

    def on_treeWidget_itemDoubleClicked(self, item, column):
        if column == self.l_column[u"目标环节"]:
            pass
        elif column == self.l_column[u"缓存来源"]:
            pass
        elif column == self.l_column[u"缓存版本"]:
            pass

    def dirlist(self, path):
        dir = QtCore.QDir(path)
        if dir.exists():
            dir.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
            return dir.entryList()

    def filelist(self, path):
        dir = QtCore.QDir(path)
        if dir.exists():
            dir.setFilter(QtCore.QDir.Files)
            dir.setSorting(QtCore.QDir.Time)
            return dir.entryList()

    def on_comboBox_project_currentTextChanged(self, str):
        self.comboBox_scene.clear()
        self.comboBox_name.clear()
        self.comboBox_fromgroup.clear()
        self.comboBox_ver.clear()
        self.lineEdit_path.clear()

        project = self.comboBox_project.currentText()
        if project != "":
            self.ser = self.ac.savepath(project)
            self.comboBox_scene.addItem("")
            self.comboBox_scene.addItems(self.dirlist(self.ser))
        pass

    def on_comboBox_scene_currentTextChanged(self, str):
        self.comboBox_name.clear()
        self.comboBox_fromgroup.clear()
        self.comboBox_ver.clear()
        self.lineEdit_path.clear()

        scene = self.comboBox_scene.currentText()
        if scene != "":
            path = self.ser + "/" + scene + "/"
            self.comboBox_name.addItem("")
            self.comboBox_name.addItems(self.dirlist(path))
        pass

    def on_comboBox_name_currentTextChanged(self, str):
        self.comboBox_fromgroup.clear()
        self.comboBox_ver.clear()
        self.lineEdit_path.clear()

        scene = self.comboBox_scene.currentText()
        name = self.comboBox_name.currentText()
        if name != "":
            path = self.ser + "/" + scene + "/" + name + "/"
            self.comboBox_fromgroup.addItem("")
            self.comboBox_fromgroup.addItems(self.dirlist(path))
        pass

    def on_comboBox_fromgroup_currentTextChanged(self, str):
        self.comboBox_ver.clear()
        self.lineEdit_path.clear()
        scene = self.comboBox_scene.currentText()
        name = self.comboBox_name.currentText()
        fromgroup = self.comboBox_fromgroup.currentText()
        if fromgroup != "":
            path = self.ser + "/" + scene + "/" + name + "/" + fromgroup + "/"
            self.comboBox_ver.addItem("")
            self.comboBox_ver.addItems(self.dirlist(path))
        pass

    def on_comboBox_ver_currentTextChanged(self, str):
        self.lineEdit_path.clear()

        scene = self.comboBox_scene.currentText()
        name = self.comboBox_name.currentText()
        fromgroup = self.comboBox_fromgroup.currentText()
        ver = self.comboBox_ver.currentText()
        if ver != "":
            path = self.ser + "/" + scene + "/" + name + "/" + fromgroup + "/" + ver
            if not os.path.exists(path):
                QtWidgets.QMessageBox.critical(self, u"错误：", u"配置文件不存在。")
                return
            self.lineEdit_path.setText(path)
        pass

    def on_pushButton_loadsetup_clicked(self):
        self.pushButton_loadsetup.setStyleSheet("background:#444499")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#555555")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#555555")
        # self.pushButton_loadcache.setEnabled(False)

        self.treeWidget.clear()

        with open(self.lineEdit_path.text() + "/setup.json", 'r') as json_file:
            load_dict = json.load(json_file)
            s = load_dict["start"]
            e = load_dict["end"]

            self.spinBox_startframe.setValue(s)
            self.spinBox_endframe.setValue(e)

            project = load_dict["project"]
            scenename = load_dict["scenename"]
            version = load_dict["version"]
            l_typ = load_dict["typ"]

            self.comboBox_project.blockSignals(True)
            self.comboBox_project.setCurrentText(project)
            self.comboBox_project.blockSignals(False)
            self.taskinfo = searchDB.taskInfo(project)

            for typ in l_typ.keys():
                item_typ = QtWidgets.QTreeWidgetItem(self.treeWidget)
                item_typ.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                item_typ.setText(self.l_column[u"引用资产"], typ)
                item_typ.setExpanded(True)
                self.treeWidget.addTopLevelItem(item_typ)
                if typ in ['CAM']:
                    item_typ.setText(self.l_column[u"缓存来源"], l_typ[typ])
                    continue
                for ref in l_typ[typ]:
                    group = ref["group"]
                    name = ref["name"]
                    namespace = ref["namespace"]
                    objects = ref["objects"]
                    version = ref["version"]
                    output = ref["output"]
                    isout = ref["isout"]
                    name_en = ref["name_en"]
                    l_group = self.dirlist(self.lineEdit_path.text() + "/" + name)

                    item_ref = QtWidgets.QTreeWidgetItem()
                    item_ref.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                    item_ref.setToolTip(self.l_column[u"引用资产"], namespace)
                    item_ref.setWhatsThis(self.l_column[u"引用资产"], name_en)
                    item_ref.setText(self.l_column[u"引用资产"], name)
                    item_ref.setCheckState(self.l_column[u"本地文件"], QtCore.Qt.Unchecked)
                    item_ref.setTextAlignment(self.l_column[u"本地文件"], QtCore.Qt.AlignCenter)

                    '''
                    item_ref.setText(1, group)
                    item_ref.setText(4, group)
                    '''

                    # print "name", name, 'group'
                    l_task = self.taskinfo.searchTaskInfoList("name", name, 'group')
                    # print l_task
                    lt_group = []
                    for task in l_task:
                        if task["pversion"] != None:
                            lt_group.append(task["group"])

                    target = WHRComboBox(self.treeWidget)
                    target.currentTextChanged.connect(self.on_target_currentTextChanged)
                    target.setWHRItem(item_ref)
                    target.addItem("")

                    source = WHRComboBox(self.treeWidget)
                    source.currentTextChanged.connect(self.on_source_currentTextChanged)
                    source.setWHRItem(item_ref)
                    source.addItem("")

                    filever = WHRComboBox(self.treeWidget)
                    filever.setWHRItem(item_ref)
                    filever.addItem("")

                    if lt_group != None:
                        target.addItems(lt_group)

                    if l_group != None:
                        source.addItems(l_group)

                    item_ref.setExpanded(True)
                    item_typ.addChild(item_ref)
                    for obj in objects.keys():
                        item_obj = QtWidgets.QTreeWidgetItem()
                        item_obj.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                        item_obj.setText(self.l_column[u"引用资产"], obj.split('|')[-1][len(namespace + ":"):])
                        item_obj.setToolTip(self.l_column[u"引用资产"], obj)
                        item_obj.setWhatsThis(self.l_column[u"引用资产"], obj)
                        # item_obj.setCheckState(3, QtCore.Qt.Checked)
                        item_obj.setExpanded(True)
                        item_ref.addChild(item_obj)
                        for o in objects[obj]:
                            item_o = QtWidgets.QTreeWidgetItem()
                            item_o.setSizeHint(self.l_column[u"引用资产"], QtCore.QSize(10, 20))
                            item_o.setText(self.l_column[u"引用资产"], o.split('|')[-1][len(namespace + ":"):])
                            item_o.setToolTip(self.l_column[u"引用资产"], o)
                            item_o.setWhatsThis(self.l_column[u"引用资产"], o)
                            item_o.setCheckState(self.l_column[u"导入缓存"], QtCore.Qt.Checked)
                            item_obj.addChild(item_o)
                            utils.processIdleEvents()

                    self.treeWidget.setItemWidget(item_ref, self.l_column[u"目标环节"], target)
                    self.treeWidget.setItemWidget(item_ref, self.l_column[u"目标资产"], QtWidgets.QLineEdit(parent=self))
                    self.treeWidget.setItemWidget(item_ref, self.l_column[u"缓存来源"], source)
                    self.treeWidget.setItemWidget(item_ref, self.l_column[u"缓存版本"], filever)

                    target.setCurrentText(group)
                    source.setCurrentText(group)

                    self.treeWidget.itemWidget(item_ref, self.l_column[u"目标资产"]).setText(item_ref.text(self.l_column[u"引用资产"]))

                    self.on_target_currentTextChanged("")

        self.pushButton_loadsetup.setStyleSheet("background:#555555")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#444499")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#555555")
        # self.pushButton_loadcache.setEnabled(False)

    def on_target_currentTextChanged(self, str):
        '''
        target = WHRComboBox()
        target = self.sender()
        item_ref = QtWidgets.QTreeWidgetItem()
        item_ref = target.whr_item
        name = item_ref.text(0)

        ns = item_ref.toolTip(0)
        group = target.property("prev")
        typ = target.property("typ")

        print ns, group, typ
        if group != None and name != None: 
            ti = self.taskinfo.searchTaskInfoDict_ng(name, group)
            f = "i:/"+ti["path"]+"/"+ti["projectf"]

            objs = cmds.ls("|"+typ+"|"+ns+":*")

            if objs != None:
                rn = cmds.referenceQuery(objs[0], referenceNode=True )
                cmds.file(f, rr=True, rn=rn)

        target.setProperty("prev", target.currentText())
        '''
        pass

    def on_source_currentTextChanged(self, str):
        source = WHRComboBox()
        source = self.sender()
        item_ref = QtWidgets.QTreeWidgetItem()
        item_ref = source.whr_item

        name = item_ref.text(self.l_column[u"引用资产"])
        group = source.currentText()

        filever = WHRComboBox()
        filever = self.treeWidget.itemWidget(item_ref, self.l_column[u"缓存版本"])
        if filever != None:
            filever.clear()
            filever.addItem("")
            item_ref.setCheckState(self.l_column[u"导入UV"], QtCore.Qt.Unchecked)

            ti = self.taskinfo.searchTaskInfoDict_ng(name, group)

            tag_ns = item_ref.toolTip(self.l_column[u"引用资产"])
            name_en = item_ref.whatsThis(self.l_column[u"引用资产"])
            sou_ns = ti["name_en"]

            ns = tag_ns.replace(name_en, sou_ns)

            if group != "":
                l_file = self.filelist(self.lineEdit_path.text() + "/" + name + "/" + group + "/" + ns)

                if l_file != None:
                    try:
                        filever.addItems(l_file)
                        filever.setCurrentText(l_file[0])
                        item_ref.setCheckState(self.l_column[u"导入UV"], QtCore.Qt.Checked)
                    except Exception as e:
                        print e
            pass

    def on_pushButton_loadasset_clicked(self):
        self.pushButton_loadsetup.setStyleSheet("background:#555555")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#444499")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#555555")
        # self.pushButton_loadcache.setEnabled(False)

        self.label_text.setText(u"加载资产...")

        s = self.spinBox_startframe.value()
        e = self.spinBox_endframe.value()
        cmds.playbackOptions(min=s, max=e, ast=s, aet=e)

        num = 0
        for i in range(0, self.treeWidget.topLevelItemCount()):
            item_typ = self.treeWidget.topLevelItem(i)
            for j in range(0, item_typ.childCount()):
                num += item_typ.childCount()

        self.progressBar.setValue(0)
        self.progressBar.setMaximum(num)
        for i in range(0, self.treeWidget.topLevelItemCount()):
            item_typ = self.treeWidget.topLevelItem(i)
            typ = item_typ.text(self.l_column[u"引用资产"])
            if not cmds.objExists("|" + typ):
                if typ not in ['CAM']:
                    cmds.group(em=True, name=typ)
                else:

                    continue

            for j in range(0, item_typ.childCount()):
                # item_typ : CHAR PROP ENV CAM
                self.progressBar.setValue(self.progressBar.value() + 1)
                utils.processIdleEvents()

                item_ref = item_typ.child(j)
                item_ref.setText(self.l_column[u"提示"], "")

                target_asset = self.treeWidget.itemWidget(item_ref, self.l_column[u"目标资产"]).text()
                name = item_ref.text(self.l_column[u"引用资产"]) if not target_asset else target_asset
                target = self.treeWidget.itemWidget(item_ref, self.l_column[u"目标环节"])
                group = target.currentText()
                if group != "":
                    ti = self.taskinfo.searchTaskInfoDict_ng(name, group)
                    f = ""
                    if item_ref.checkState(self.l_column[u"本地文件"]) == QtCore.Qt.Unchecked:
                        f = "i:/" + ti["path"] + "/" + ti["projectf"]
                    else:
                        f = "e:/projects/" + ti["path"] + "/" + ti["projectf"]

                    old_ns = item_ref.toolTip(self.l_column[u"引用资产"]).replace(item_ref.text(self.l_column[u"引用资产"]), name)
                    old_name_en = item_ref.whatsThis(self.l_column[u"引用资产"]).replace(item_ref.text(self.l_column[u"引用资产"]), name)

                    new_name_en = ti["name_en"]
                    new_ns = old_ns.replace(old_name_en, new_name_en)

                    item_ref.setToolTip(self.l_column[u"引用资产"], new_ns)
                    item_ref.setWhatsThis(self.l_column[u"引用资产"], new_name_en)

                    print item_ref.toolTip(self.l_column[u"引用资产"])
                    print item_ref.whatsThis(self.l_column[u"引用资产"])

                    if not cmds.namespace(exists=new_ns):
                        self.label_text.setText(u"加载" + new_ns + "...")
                        if os.path.exists(f):
                            cmds.file(f, r=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
                                      namespace=new_ns, options="v=0;p=17;f=0")
                            l_ref_obj = cmds.ls("|" + new_ns + ":*|")
                            print l_ref_obj
                            for ref in l_ref_obj:
                                if cmds.objExists("|" + ref):
                                    if cmds.objExists("|" + ref):
                                        cmds.parent("|" + ref, "|" + typ)
                                        item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.green)
                                    else:
                                        item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.red)
                                        item_ref.setText(self.l_column[u"提示"], u"错误：资产大组名称不正确!")
                                elif cmds.objExists("|" + typ + "|" + ref):
                                    item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.green)
                                else:
                                    item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.red)
                                    item_ref.setText(self.l_column[u"提示"], u"错误：资产大组名称不正确，找不到大组!")
                        else:
                            item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.red)
                            item_ref.setText(self.l_column[u"提示"], u"错误：文件不存在，无法加载!")

                    else:
                        item_ref.setTextColor(self.l_column[u"引用资产"], QtCore.Qt.green)

                    for i in range(0, item_ref.childCount()):
                        item_obj = QtWidgets.QTreeWidgetItem()
                        item_obj = item_ref.child(i)
                        item_obj.setToolTip(self.l_column[u"引用资产"],
                                            item_obj.whatsThis(self.l_column[u"引用资产"]).replace(old_ns, new_ns))
                        item_obj.setWhatsThis(self.l_column[u"引用资产"], item_obj.toolTip(self.l_column[u"引用资产"]))
                        for j in range(0, item_obj.childCount()):
                            item_o = QtWidgets.QTreeWidgetItem()
                            item_o = item_obj.child(j)
                            item_o.setToolTip(self.l_column[u"引用资产"],
                                              item_o.whatsThis(self.l_column[u"引用资产"]).replace(old_ns, new_ns))
                            item_o.setWhatsThis(self.l_column[u"引用资产"], item_o.toolTip(self.l_column[u"引用资产"]))

        self.progressBar.setValue(num)

        self.label_text.setText(u"资产加载完成！")

        self.pushButton_loadsetup.setStyleSheet("background:#555555")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#555555")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#444499")
        #self.pushButton_loadcache.setEnabled(True)
        pass

    def on_pushButton_loadcache_clicked(self):
        if not cmds.pluginInfo('AbcImport', query=1, loaded=1):
            try:
                cmds.loadPlugin('AbcImport.mll')
            except RuntimeError:
                raise RuntimeError('AbcImport.mll was not found on MAYA_PLUG_IN_PATH')
        self.pushButton_loadsetup.setStyleSheet("background:#555555")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#555555")
        self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#444499")
        # self.pushButton_loadcache.setEnabled(False)

        self.label_text.setText(u"启动缓存导入...")

        num = 0
        for i in range(0, self.treeWidget.topLevelItemCount()):
            item_typ = self.treeWidget.topLevelItem(i)
            for j in range(0, item_typ.childCount()):
                num += item_typ.childCount()

        self.progressBar.setValue(0)
        self.progressBar.setMaximum(num)
        for i in range(0, self.treeWidget.topLevelItemCount()):
            item_typ = self.treeWidget.topLevelItem(i)
            typ = item_typ.text(self.l_column[u"引用资产"])
            if not cmds.objExists("|" + typ):
                if typ not in ['CAM']:
                    cmds.group(em=True, name=typ)
            if typ in ['CAM']:
                path = item_typ.text(self.l_column[u"缓存来源"])
                mel.eval('AbcImport -mode import "%s";' % path)
                continue
            for j in range(0, item_typ.childCount()):
                self.progressBar.setValue(self.progressBar.value() + 1)
                item_ref = item_typ.child(j)
                o_ns = item_ref.toolTip(self.l_column[u"引用资产"])
                name = item_ref.text(self.l_column[u"引用资产"])
                # print 'name:\n', name
                group = self.treeWidget.itemWidget(item_ref, self.l_column[u"缓存来源"]).currentText()
                target_process = self.treeWidget.itemWidget(item_ref, self.l_column[u"目标环节"]).currentText()
                if name not in ['CAM'] and (not group or not target_process):
                    continue
                print "group: ", group
                if group != "":
                    ti = self.taskinfo.searchTaskInfoDict_ng(name, group)

                    tag_ns = item_ref.toolTip(self.l_column[u"引用资产"])
                    name_en = item_ref.whatsThis(self.l_column[u"引用资产"])
                    sou_ns = ti["name_en"]

                    ns = tag_ns.replace(name_en, sou_ns)

                    print ns

                    isUv = item_ref.checkState(self.l_column[u"导入UV"])
                    AbcGrp = self.treeWidget.itemWidget(item_ref, self.l_column[u"缓存来源"]).currentText()
                    if AbcGrp != "":
                        AbcVer = self.treeWidget.itemWidget(item_ref, self.l_column[u"缓存版本"]).currentText()
                        if AbcVer != "":
                            abc = self.lineEdit_path.text() + "/" + name + "/" + AbcGrp + "/" + ns + "/" + AbcVer
                            print abc
                            l_obj = []
                            ct = ""
                            ct2 = ""
                            eft = ""
                            eft2 = ""
                            for k in range(0, item_ref.childCount()):
                                item_obj = item_ref.child(k)
                                ct += item_obj.toolTip(self.l_column[u"引用资产"]) + " "
                                ct2 += item_obj.toolTip(self.l_column[u"引用资产"]).replace(":Geometry", ":sim") + " "
                                for l in range(0, item_obj.childCount()):
                                    item_o = item_obj.child(l)
                                    if item_o.checkState(self.l_column[u"导入缓存"]) == QtCore.Qt.Unchecked:
                                        eft += item_o.text(self.l_column[u"引用资产"]) + " "
                                        eft2 += item_o.text(self.l_column[u"引用资产"]) + " "
                                    # else:
                                    #     eft2 += item_o.text(self.l_column[u"引用资产"]) + " "

                            self.label_text.setText(u"正在导入" + ns + u"的缓存...")
                            utils.processIdleEvents()

                            if not self.if_blend_cb.currentText():
                                QtWidgets.QMessageBox.critical(self, u"错误：", u'请选择缓存融合方式！')
                                return
                            _text = self.treeWidget.itemWidget(item_ref, self.l_column[u"目标资产"]).text()
                            target_asset = _text if _text else name
                            # print target_asset
                            # current_group =
                            ct = ct.replace(name, target_asset).replace('_'+group, '_'+target_process)
                            target_namespace = ct.split('|')[-1].split(":")[0]
                            print target_namespace
                            if self.if_blend_cb.currentText() == 'BlendShape':
                                utils.executeInMainThreadWithResult(self.ac.inputAbc, abc, ct=ct,
                                                                    namespace=target_namespace, bs=1)
                                continue
                            if 'CFX_Cloth' in ct:
                                utils.executeInMainThreadWithResult(self.ac.inputAbc, abc=abc, ct=ct, eft='clothes_Grp ')
                                utils.executeInMainThreadWithResult(self.ac.inputAbc, abc=abc, ct=ct2, eft='body_Grp prop_Grp ')
                                print ct[:-len("|" + ct.split("|")[-1])]
                            else:
                                utils.executeInMainThreadWithResult(self.ac.inputAbc, abc=abc, ct=ct, eft=eft)

        self.progressBar.setValue(num)

        self.label_text.setText(u"缓存导入完成！")

        self.pushButton_loadsetup.setStyleSheet("background:#444499")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadasset.setStyleSheet("background:#555555")
        #self.pushButton_loadasset.setEnabled(True)

        self.pushButton_loadcache.setStyleSheet("background:#555555")
        #self.pushButton_loadcache.setEnabled(True)
        # try:
        #     uvin_window = uvin.UVLoad()
        #     uvin_window.on_import_uv_pb_clicked()
        #     uvin_window.show()
        #     print '成功导入uv..'
        # except:
        #     uvin_window.show()
        pass


def main():
    IACD = inputAbcCacheDialog(mayaMainWindow)
    IACD.show()
