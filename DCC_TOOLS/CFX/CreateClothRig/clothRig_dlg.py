# -*- coding: utf-8 -*-

# Description:    + 自动创建布料绑定，整理大纲层级
# Author:         + xusheng
# Version:        + v001
# ChangeInfo      +
# Usage:          +



_OCT_UserScriptPath = r'\\192.168.15.242\Plugins\Maya2017\Scripts\CFX'
#本地测试的路径#
#_OCT_UserScriptPath = r'C:\QxsPY\maya2017_py'
_OCT_UserUIFileName = 'clothRig_dlg.ui'
_OCT_clothRig_DLG = None
_OCT_QtUIModule = None

import clothRig
reload(clothRig)
import mayaCommon as macomm
reload(macomm)
try:
    from PySide2 import QtCore, QtWidgets, QtUiTools
    _OCT_QtUIModule = QtWidgets
except:
    from PySide import QtCore, QtGui, QtUiTools
    _OCT_QtUIModule = QtGui


class _OCT_UI_ClothRig_DLG():
    def __init__(self):
        global _OCT_UserScriptPath
        global _OCT_UserUIFileName
        global _OCT_QtUIModule
        self.makeClothRig = clothRig._OCT_CreateClothRig()
        self.oriClothList = []
        self.simClothList = []
        self.colClothList = []

        #界面元素的定义，窗口和按钮以及响应函数，使用了QT designer生成的ui文件保存界面配置信息，在代码中动态加载界面配置#
        ui_file_path = _OCT_UserScriptPath + '/' + _OCT_UserUIFileName
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.theMainWindow = loader.load(ui_file)
        self.theMainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainWin_oriCloth_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "oriCloth_btn")
        self.mainWin_simCloth_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "simCloth_btn")
        self.mainWin_colCloth_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "colCloth_btn")
        self.mainWin_ncloth_chb = self.theMainWindow.findChild(_OCT_QtUIModule.QCheckBox, "ncloth_chb")
        self.mainWin_qualoth_chb = self.theMainWindow.findChild(_OCT_QtUIModule.QCheckBox, "qualoth_chb")
        self.mainWin_autoBind_chb = self.theMainWindow.findChild(_OCT_QtUIModule.QCheckBox, "autoBind_chb")
        self.mainWin_CreateRig_btn = self.theMainWindow.findChild(_OCT_QtUIModule.QPushButton, "createRig_btn")
        self.mainWin_OutMessage_plt = self.theMainWindow.findChild(_OCT_QtUIModule.QPlainTextEdit, "outMessage_plt")

        #按钮和按钮响应函数链接#
        self.mainWin_oriCloth_btn.clicked.connect(self.mainWin_oriCloth_btnClick)
        self.mainWin_simCloth_btn.clicked.connect(self.mainWin_simCloth_btnClick)
        self.mainWin_colCloth_btn.clicked.connect(self.mainWin_colCloth_btnClick)
        self.mainWin_CreateRig_btn.clicked.connect(self.mainWin_CreateRig_btnClick)
        self.mainWin_ncloth_chb.clicked.connect(self.mainWin_ncloth_chbClick)
        self.mainWin_qualoth_chb.clicked.connect(self.mainWin_qualoth_chbClick)


    #以下是所有按钮的点击响应函数#
    def mainWin_ncloth_chbClick(self):
        if self.mainWin_ncloth_chb.isChecked():
            self.mainWin_qualoth_chb.setChecked(False)
        else:
            self.mainWin_qualoth_chb.setChecked(True)

    def mainWin_qualoth_chbClick(self):
        if self.mainWin_qualoth_chb.isChecked():
            self.mainWin_ncloth_chb.setChecked(False)
        else:
            self.mainWin_ncloth_chb.setChecked(True)

    def mainWin_oriCloth_btnClick(self):
        self.oriClothList = self.makeClothRig.getSelObjs()

        if self.oriClothList:
            outMessage = u'您选择的原始布料是：\n' + '\n'.join(self.oriClothList)
            self.outputResult(outMessage)
        #self.makeClothRig.arrangeOriClothGrp(self.oriClothList)
        #just for debug, close these codes in final file
        #macomm.dataToLogFile(self.oriClothList)
        #macomm.openLogFileInTextedit()

    def mainWin_simCloth_btnClick(self):
        self.simClothList = self.makeClothRig.getSelObjs()

        if self.simClothList:
            outMessage = u'您选择的解算布料是：\n' + '\n'.join(self.simClothList)
            self.outputResult(outMessage)
        #self.makeClothRig.arrangeSimClothGrp(self.simClothList)

    def mainWin_colCloth_btnClick(self):
        self.colClothList = self.makeClothRig.getSelObjs()

        if self.colClothList:
            outMessage = u'您选择的碰撞体是：\n' + '\n'.join(self.colClothList)
            self.outputResult(outMessage)
        #self.makeClothRig.arrangeColClothGrp(self.colClothList)

    def mainWin_CreateRig_btnClick(self):
        if self.mainWin_ncloth_chb.isChecked():
            oriMeshList = self.makeClothRig.isObjsFromClothesGrp(self.oriClothList)
            oriMeshList = self.makeClothRig.filterMeshObjsInSelect(oriMeshList)
            simMeshList = self.makeClothRig.filterMeshObjsInSelect(self.simClothList)

            if simMeshList:
                simGrp = self.makeClothRig.getSimGrp()
                simMeshList = self.makeClothRig.putNClothInSimGrp(simGrp, simMeshList)
            colMeshList = self.makeClothRig.filterMeshObjsInSelect(self.colClothList)
            dupOriMeshList = []
            outMessage = u'Rig结果如下：\n'

            if oriMeshList:
                dupOriMeshList = self.makeClothRig.arrangeOriClothGrp(oriMeshList, simGrp)
                outMessage += u'\n进入Rig的原始布料是：\n' + '\n'.join(dupOriMeshList)

                if dupOriMeshList:
                    outMessage += u'\n原始布料组复制：    ' + u'成功!'
                else:
                    outMessage += u'\n原始布料组复制：    ' + u'失败!'

            if dupOriMeshList and simMeshList:
                wrapPairList = self.makeClothRig.createWrap(dupOriMeshList, simMeshList)
                outMessage += u'\n\n复制布料包裹解算布料结果：\n' + '\n'.join(wrapPairList)

            if simMeshList and oriMeshList:
                wrapPairList = self.makeClothRig.createWrap(simMeshList, oriMeshList)
                outMessage += u'\n\n解算布料包裹原始布料结果：\n' + '\n'.join(wrapPairList)

            if simMeshList:
                clothObjList = self.makeClothRig.arrangeSimClothGrp(simMeshList)
                outMessage += u'\n\n进入Rig的解算布料是：\n' + '\n'.join(simMeshList)
                outMessage += u'\n\n创建的解算布料是：\n' + '\n'.join(clothObjList)

            if colMeshList:
                colResultList = [[''], ['']]
                colResultList = self.makeClothRig.arrangeColClothGrp(colMeshList)
                outMessage += u'\n\n进入Rig的碰撞体是：\n' + '\n'.join(colMeshList)
                outMessage += u'\n\n动画模型和碰撞体blendShape结果：\n' + '\n'.join(colResultList[0])
                outMessage += u'\n\n创建的碰撞刚体是：\n' + '\n'.join(colResultList[1])
            self.outputResult(outMessage)
            self.clearUserSelection()
            #self.theMainWindow.close()

    def outputResult(self, message = ''):
        self.mainWin_OutMessage_plt.setPlainText(message)

    def clearUserSelection(self):
        self.oriClothList = []
        self.simClothList = []
        self.colClothList = []



def _OCT_runClothRig_DLG():
    global _OCT_clothRig_DLG
    global _OCT_QtUIModule

    if None != _OCT_QtUIModule:
        _OCT_clothRig_DLG = _OCT_UI_ClothRig_DLG()
        _OCT_clothRig_DLG.theMainWindow.show()