# -*- coding: utf-8 -*-

# Description:    + 移除或者添加晶格影响
# Author:         + xusheng
# Version:        + v001
# ChangeInfo      +
# Usage:          +



_OCT_UserScriptPath = r'\\192.168.15.242\Plugins\Maya2017\Plug-ins\latticeToMesh'
#本地测试的路径#
#_OCT_UserScriptPath = r'C:\QxsCode\maya2017_py'
_OCT_UserUIFileName = 'latticeToMesh_dlg.ui'
_OCT_latticeToMesh_DLG = None
_OCT_QtUIModule = None


try:
    from PySide2 import QtCore, QtWidgets, QtUiTools
    _OCT_QtUIModule = QtWidgets
except:
    from PySide import QtCore, QtGui, QtUiTools
    _OCT_QtUIModule = QtGui
import latticeToMesh as lame
reload(lame)


class _OCT_UI_latticeToMesh_DLG():
    def __init__(self):
        global _OCT_UserScriptPath
        global _OCT_UserUIFileName
        global _OCT_QtUIModule

        #界面元素的定义，窗口和按钮以及响应函数，使用了QT designer生成的ui文件保存界面配置信息，在代码中动态加载界面配置#
        ui_file_path = _OCT_UserScriptPath + "/" + _OCT_UserUIFileName
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.objList = []
        self.theMainWindow = loader.load(ui_file)
        self.theMainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainWin_addLattice_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "addLattice_btn")
        self.mainWin_rmLattice_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "rmLattice_btn")
        self.mainWin_disConn_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "disConn_btn")

        #按钮和按钮响应函数链接#
        self.mainWin_addLattice_btn.clicked.connect(self.mainWin_addLattice_btnClick)
        self.mainWin_rmLattice_btn.clicked.connect(self.mainWin_rmLattice_btnClick)
        self.mainWin_disConn_btn.clicked.connect(self.mainWin_disConn_btnClick)

    #以下是所有按钮的点击响应函数#
    def mainWin_addLattice_btnClick(self):
        objList = lame.getSelObjs()
        lame.addLatticeToObjs(objList)
        self.newList = []


    def mainWin_rmLattice_btnClick(self):
        objList = lame.getSelObjs()
        self.newList = lame.rmLatticeFromObjs(objList)

    def mainWin_disConn_btnClick(self):
        lame.disconnFFDWithMesh(self.newList)


def _OCT_runLatticeToMesh_DLG():
    global _OCT_latticeToMesh_DLG
    global _OCT_QtUIModule

    if None != _OCT_QtUIModule:
        _OCT_latticeToMesh_DLG = _OCT_UI_latticeToMesh_DLG()
        _OCT_latticeToMesh_DLG.theMainWindow.show()