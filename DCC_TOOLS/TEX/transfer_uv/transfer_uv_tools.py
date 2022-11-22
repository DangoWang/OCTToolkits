import sys
import pymel.core as pm
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
import transfer_uv_tools_ui
import uv_function
reload(transfer_uv_tools_ui)
reload(uv_function)
class MainWindow(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = transfer_uv_tools_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.group_teans_uv_button.clicked.connect(self.groupTransferUV)
        self.ui.anylize_group_button.clicked.connect(self.anylizeGroup)
        self.ui.select_same_in_group_button.clicked.connect(self.selectSameTopu)
        self.ui.transfer_uv_group_button.clicked.connect(self.transferSameTopu)
        self.ui.look_objects_by_topu_button.clicked.connect(self.lookObjectsByTopu)
        self.ui.transfer_uv_by_object_button.clicked.connect(self.transferUvByObject)
        self.mode_a_dict = {}
        self.mode_b_list = []
        self.mode_b_source = ''
    def groupTransferUV(self):
        #print "let\'s transfer uv throgh groups"
        uv_function.groupTransUV()

    def anylizeGroup(self):
        grp = pm.ls(sl = 1,type="transform")[0]
        if grp:
            group_name = grp.name()
            self.ui.group_groupName.setText(group_name)
        else:
            group_name = 'master'
        self.mode_a_dict = uv_function.anylizeGroup(group_name)
        self.selectSameTopu()

    def selectSameTopu(self):
        #print "this func select same topu objects!"
        pm.select(cl=1)
        for key in self.mode_a_dict.keys():
            pm.select(self.mode_a_dict[key][0],tgl = 1)

    def transferSameTopu(self):
        #print "let us transfer same topu objects!"
        for key in self.mode_a_dict.keys():
            if len(self.mode_a_dict[key])>1:
                for tga in self.mode_a_dict[key][1:]:
                    pm.polyTransfer(tga,uv=1,ao=self.mode_a_dict[key][0])
                    print "transfer uv from %s to---> %s"%(self.mode_a_dict[key][0],tga)
    def lookObjectsByTopu(self):
        #print "select objects from one mesh"
        select_obj = pm.ls(sl=1)
        self.mode_b_source = select_obj[0].getShape()
        self.mode_b_list = uv_function.matchTopu(select_obj,self.ui.groupName)
        pm.select(self.mode_b_list)
        print self.mode_b_list
        print self.mode_b_source
    def transferUvByObject(self):

        for tga in self.mode_b_list:
            pm.polyTransfer(tga,uv=1,ao=self.mode_b_source)
            print "transfer uv from %s to---> %s"%(self.mode_b_source,tga)
        #print "transfer uv to objects from one mesh"
def showWindow():
    global window
    window = MainWindow()
    window.show()
    return window
