#!/usr/bin/env python
# -*- coding:utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Asset Library v1.0 
#        BY WangHaoRun
#        2018.05.06
#
#---------------------------------------------------------------
import os
from PySide2 import QtCore, QtGui, QtWidgets, QtSql
from shiboken2 import wrapInstance 

from PySide2.QtCore import * 

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
import sqlite3

mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QMainWindow) 

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

class Ui_assetLibraryDialog(object):
    def setupUi(self, assetLibraryDialog):
        assetLibraryDialog.setObjectName("assetLibraryDialog")
        assetLibraryDialog.resize(751, 630)
        self.gridLayout = QtWidgets.QGridLayout(assetLibraryDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(assetLibraryDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(assetLibraryDialog)
        self.comboBox.setMinimumSize(QtCore.QSize(120, 23))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.hasAD_cb = QtWidgets.QCheckBox(assetLibraryDialog)
        self.hasAD_cb.setObjectName("hasAD_cb")
        self.hasAD_cb.setText(u'AD')
        self.horizontalLayout.addWidget(self.hasAD_cb)
        self.hasAD_cb.hide()

        self.label_2 = QtWidgets.QLabel(assetLibraryDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_assetName = QtWidgets.QLineEdit(assetLibraryDialog)
        self.lineEdit_assetName.setObjectName("lineEdit_assetName")
        self.horizontalLayout.addWidget(self.lineEdit_assetName)
        self.pushButton_update = QtWidgets.QPushButton(assetLibraryDialog)
        self.pushButton_update.setMinimumSize(QtCore.QSize(45, 23))
        self.pushButton_update.setMaximumSize(QtCore.QSize(45, 16777215))
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(assetLibraryDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeWidget_outliner = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_outliner.setObjectName("treeWidget_outliner")
        self.treeWidget_assetlist = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_assetlist.setObjectName("treeWidget_assetlist")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.progress_lable = QtWidgets.QLabel(assetLibraryDialog)
        self.horizontalLayout_2.addWidget(self.progress_lable)
        self.progress_lable.setText(u'正在读取...')
        self.progress_lable.hide()

        self.progressBar = QtWidgets.QProgressBar(assetLibraryDialog)
        self.progressBar.setMaximumSize(QtCore.QSize(120, 16777215))
        # self.progressBar.setGeometry(20, 50, 0, 0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.progressBar.hide()
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        # self.spacer_temp = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_2.addItem(self.spacer_temp)

        # self.pushButton_close = QtWidgets.QPushButton(assetLibraryDialog)
        # self.pushButton_close.setObjectName("pushButton_close")
        # self.horizontalLayout_2.addWidget(self.pushButton_close)
        # spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(assetLibraryDialog)
        QtCore.QMetaObject.connectSlotsByName(assetLibraryDialog)

    def retranslateUi(self, assetLibraryDialog):
        assetLibraryDialog.setWindowTitle(QtWidgets.QApplication.translate("assetLibraryDialog", "Asset Library V1.0beta by wanghaorun", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Project Name:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Asset Name:", None, -1))
        self.pushButton_update.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Search", None, -1))
        self.treeWidget_outliner.headerItem().setText(0, QtWidgets.QApplication.translate("assetLibraryDialog", "Outliner", None, -1))
        self.treeWidget_assetlist.headerItem().setText(0, QtWidgets.QApplication.translate("assetLibraryDialog", "Thumbnail", None, -1))
        self.treeWidget_assetlist.headerItem().setText(1, QtWidgets.QApplication.translate("assetLibraryDialog", "Name", None, -1))
        self.treeWidget_assetlist.headerItem().setText(2, QtWidgets.QApplication.translate("assetLibraryDialog", "Chinese", None, -1))
        self.treeWidget_assetlist.headerItem().setText(3, QtWidgets.QApplication.translate("assetLibraryDialog", "Ver(Pub/All)", None, -1))
        self.treeWidget_assetlist.headerItem().setText(4, QtWidgets.QApplication.translate("assetLibraryDialog", "Describe", None, -1))
        # self.treeWidget_assetlist.headerItem().setText(5, QtWidgets.QApplication.translate("assetLibraryDialog",
        #                                                                                    "hasAD", None, -1))
        # self.pushButton_close.setText(QtWidgets.QApplication.translate("assetLibraryDialog", "Close", None, -1))


# UI END
        
        self.pushButton_update.clicked.connect(self.update_assetlist)
        # self.pushButton_close.clicked.connect(self.close)
        self.treeWidget_outliner.itemClicked.connect(self.on_treeWidget_outliner_iClicked)
        self.treeWidget_assetlist.itemClicked.connect(self.on_treeWidget_assetlist_iClicked)
        self.treeWidget_assetlist.itemDoubleClicked.connect(self.on_treeWidget_assetlist_iDoubleClicked)
        self.treeWidget_assetlist.customContextMenuRequested.connect(self.on_treeWidget_assetlist_cContextMenuRequested)
        self.lineEdit_assetName.returnPressed.connect(self.update_assetlist)
        self.hasAD_cb.stateChanged.connect(self.update_assetlist)
        
        self.treeWidget_assetlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_assetlist.setIndentation(0)
        self.treeWidget_assetlist.setIconSize(QtCore.QSize(100, 70))
        
        sizes = [120, 450]
        self.splitter.setSizes(sizes)

        self.pubPath = "I:/"
        self.systemPath = "//192.168.15.253/projects/"
        self.projects = ["dsf", "dstv", "dsns"]
        self.comboBox.addItems(self.projects)
        self.comboBox.setCurrentText("dsf")

        self.db_project_path = self.systemPath+"Daily_DB/"+self.comboBox.currentText()+"/DATA.s3db"
        self.db_system_path = self.systemPath+"Daily_DB/"+self.comboBox.currentText()+"/SYSTEM.s3db"

    def connectdb(self):
        pass

    def update_outliner(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.db_project_path)
        ok = db.open()
        model =  QtSql.QSqlQueryModel()
        model.setQuery("SELECT DISTINCT [classify] from [tasks] WHERE [big]='Asset' ORDER BY [classify]", db)
        for i in range(0, model.rowCount()):
#            print model.record(i).value(0)
            data_c = [model.record(i).value("classify")]
            item_c = QtWidgets.QTreeWidgetItem(data_c)
            item_c.setSizeHint(0, QtCore.QSize(25,25))
            model_g =  QtSql.QSqlQueryModel()
            model_g.setQuery("SELECT DISTINCT [group] from [tasks] WHERE [big]='Asset' AND [classify] = '"+model.record(i).value("classify")+"' ORDER BY [group]", db)
            while(model_g.canFetchMore()):
                model_g.fetchMore()
            for j in range(0, model_g.rowCount()):
#                print model_g.record(j).value(0)
                data_g = [model_g.record(j).value("group")]
                item_g = QtWidgets.QTreeWidgetItem(data_g)
                item_g.setData(0, QtCore.Qt.UserRole+1, "[big] = 'Asset' And [classify] = '"+model.record(i).value("classify")+"' AND [group] = '"+model_g.record(j).value("group")+"' ORDER BY [name_en]")
                item_g.setSizeHint(0, QtCore.QSize(25,25))
                item_c.addChild(item_g)
            self.treeWidget_outliner.addTopLevelItem(item_c)

    def on_treeWidget_outliner_iClicked(self, item, column, filter='' ):
        self.progressBar.show()
        self.progress_lable.show()
        self.treeWidget_assetlist.clear()
        sql = item.data(0, QtCore.Qt.UserRole+1)
        progress_value = 0
        if not sql is None:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.db_project_path)
            ok = db.open()
            model = QtSql.QSqlQueryModel()
            model.setQuery("SELECT * from [tasks] WHERE "+sql, db)
            for i in range(0, model.rowCount()):
    #            print model.record(i).value(0)
                data = ["", model.record(i).value("name_en"), model.record(i).value("name_zn"),  str(model.record(i).value("pversion"))+"/"+str(model.record(i).value("version")), model.record(i).value("describe")]
                if filter and (filter not in data[1]+data[2]):
                    continue
                self.hasAD_cb.hide()
                if 'MOD' in model.record(i).value("name_en"):
                    self.hasAD_cb.show()
                if self.hasAD_cb.isChecked():
                    if not model.record(i).value("hasAD"):
                        continue
                self.progressBar.setValue(progress_value)
                progress_value += 1
                item = QtWidgets.QTreeWidgetItem(data)
                if not model.record(i).value("previewf") is "":
                    item.setData(0, QtCore.Qt.UserRole+1, self.pubPath+model.record(i).value("path")+"/"+model.record(i).value("projectf"))
                    item.setData(0, QtCore.Qt.UserRole+2, self.pubPath+model.record(i).value("path")+"/"+model.record(i).value("previewf"))
                    pix = QtGui.QPixmap(self.pubPath+model.record(i).value("path")+"/"+model.record(i).value("previewf"))
                    item.setIcon(0, QtGui.QIcon(pix))
                item.setTextAlignment(0, QtCore.Qt.AlignCenter)
                item.setTextAlignment(1, QtCore.Qt.AlignCenter)
                item.setTextAlignment(2, QtCore.Qt.AlignCenter)
                item.setTextAlignment(3, QtCore.Qt.AlignCenter)
                item.setSizeHint(0, QtCore.QSize(70,70))                
                self.treeWidget_assetlist.addTopLevelItem(item)
        self.progressBar.hide()
        self.progress_lable.hide()

    def update_assetlist(self):
        item = self.treeWidget_outliner.currentItem()
        filt = self.lineEdit_assetName.text()
        self.on_treeWidget_outliner_iClicked(item, 0, filter=filt)
        pass

    def on_treeWidget_assetlist_iClicked(self, item, column ):
        if column == 0:
            icon_p = item.data(0, QtCore.Qt.UserRole+2)
            if not icon_p is "":
                pix = QtGui.QPixmap(icon_p)
                self.button = QtWidgets.QPushButton(self.treeWidget_assetlist)
                self.button.setIcon(QtGui.QIcon(pix))
                self.button.setGeometry(0,0,self.treeWidget_assetlist.width(),self.treeWidget_assetlist.height())
                self.button.setIconSize(QtCore.QSize(self.treeWidget_assetlist.width(),self.treeWidget_assetlist.height()))
                self.button.clicked.connect(self.button.close)
                self.button.show()
                print icon_p

    def on_treeWidget_assetlist_iDoubleClicked(self, item, column ):
        if column == 0:
            icon_p = item.data(0, QtCore.Qt.UserRole+2)
            #print icon_p

    def on_treeWidget_assetlist_cContextMenuRequested(self, pos):
        menu = QtWidgets.QMenu()

        im = QtWidgets.QAction("Import File", menu)
        im.triggered.connect(self.on_imTriggered)


        op = QtWidgets.QAction("Create Assembly Reference", menu)
        op.triggered.connect(self.on_carTriggered)

        cr = QtWidgets.QAction("Create Reference...", menu)
        cr.triggered.connect(self.on_crTriggered)

        rr = QtWidgets.QAction("Replace Reference...", menu)
        rr.triggered.connect(self.on_rrTriggered)

        
        menu.addAction(cr)
        menu.addAction(rr)
        menu.addSeparator()
        menu.addAction(im)
        menu.addAction(op)

        menu.exec_(QtGui.QCursor.pos())

    def on_imTriggered(self):
        si = self.treeWidget_assetlist.selectedItems()
        for item in si:
            cmds.file(item.data(0, QtCore.Qt.UserRole + 1), i=True, ignoreVersion=True)
        pass

    def on_carTriggered(self):
        item = self.treeWidget_assetlist.currentItem()
        path = item.data(0, QtCore.Qt.UserRole+1)
        assembly_path = path.replace(os.path.basename(path), 'Assembly/'+os.path.basename(path).replace('MOD', 'AD'))
        if QtCore.QFileInfo(assembly_path).exists:
            if not cmds.pluginInfo('sceneAssembly', query=1, loaded=1):
                try:
                    cmds.loadPlugin('sceneAssembly.mll')
                except RuntimeError:
                    raise RuntimeError('sceneAssembly.mll was not found on MAYA_PLUG_IN_PATH')
            ar_node = cmds.assembly(type='assemblyReference')
            cmds.setAttr(ar_node+'.definition', assembly_path, type='string')
            print os.path.basename(path)
            ar_node_name = os.path.basename(path).replace('.ma', '')
            if cmds.objExists(ar_node_name):
                cmds.delete(ar_node_name)
            cmds.rename(ar_node, ar_node_name)
        pass

    def on_crTriggered(self):
        si = self.treeWidget_assetlist.selectedItems()
        for item in si:
            #file -r  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace \""+name+"\" -options \"v=0;p=17;f=0\" \""+path+"\";
            cmds.file(item.data(0, QtCore.Qt.UserRole+1), r=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False, namespace=item.text(1), options="v=0;p=17;f=0")
        pass

    def on_rrTriggered(self):
        #file -loadReference "dsf_NH_FangJ_MODRN" -options "v=0;" "C:/Users/Administrator/Documents/maya/projects/default/scenes/bb.mb";
        item = self.treeWidget_assetlist.currentItem()
        path = item.data(0, QtCore.Qt.UserRole+1)
        if QtCore.QFileInfo(path).exists:
            objs = cmds.ls(sl=True)
            ns = cmds.referenceQuery(objs , referenceNode=True)
            if ns != "":
                cmds.file(path, loadReference = ns, options="v=0;")
            else:
                cmds.file(path, r=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False, namespace=item.text(1), options="v=0;p=17;f=0")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Warning:")
            msgBox.setInformativeText("File not found.\n"+path)
            yesButton = msgBox.addButton(QMessageBox.Yes)
            noButton = msgBox.addButton(QMessageBox.No)
            msgBox.exec_()
            if msgBox.clickedButton() == yesButton:
                cmds.delete(list_object)
        pass

class assetLibraryDialog(QtWidgets.QDialog,Ui_assetLibraryDialog):
    def __init__(self, *args, **kwargs):
        if cmds.window("assetLibraryDialog", exists=True):
            cmds.deleteUI("assetLibraryDialog", window=True)
        super(assetLibraryDialog, self).__init__(*args, **kwargs)
        self.setupUi( self )

def show():
    ui = assetLibraryDialog(mayaMainWindow)
    ui.connectdb()
    ui.update_outliner()
    ui.show()
