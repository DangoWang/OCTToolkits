# -*- coding: utf-8 -*-
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from functools import partial
import maya.cmds as cmds
import os
import shutil

class ImgCopyThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(ImgCopyThread, self).__init__(parent)
        self.copy_path = ""

    def run(self, *args, **kwargs):
        cur_dir = get_current_dir()
        if not cur_dir:
            return
        for root, dirs, files in os.walk(self.copy_path):
            for img in files:
                source_path = os.path.join(root, img)
                dst_full = source_path.replace("I:/", cur_dir)
                if not os.path.isdir(os.path.dirname(dst_full)):
                    os.makedirs(os.path.dirname(dst_full))
                print "copy {}  \n>>>>>> {}".format(source_path, dst_full)
                shutil.copy(source_path, dst_full)
        self.wait()
        self.quit()


class MenuListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(MenuListWidget, self).__init__()
        self.setIconSize(QtCore.QSize(100, 100))

        self.file_dir = {}
        self.time_dir = {}
        self.info_dir = {}
        self.rightClickMenu()
        self.copy_thread = ImgCopyThread()

    def rightClickMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QtWidgets.QMenu(self)
        download_file = self.contextMenu.addAction(u"下载")
        download_file.triggered.connect(partial(self.open_file, 3))
        open_file = self.contextMenu.addAction(u"下载并打开")
        open_file.triggered.connect(partial(self.open_file, 0))
        create_ref = self.contextMenu.addAction(u"Reference")
        create_ref.triggered.connect(partial(self.open_file, 1))
        reload_ref = self.contextMenu.addAction(u"替换Reference")
        reload_ref.triggered.connect(partial(self.open_file, 2))

    def open_file(self, mod):
        item = self.currentItem().data(0)
        file_path = self.file_dir[item]
        if not os.path.isfile(file_path):
            print u"文件不存在",
            return
        if mod==0 or mod==3:
            cur_dir = get_current_dir()
            if not cur_dir:
                print u"请联系TD添加下载路径盘",
                return
            if not file_path.startswith("I:/"):
                print u"文件不是I盘文件，",
                return
            new_file_path = file_path.replace("I:/", cur_dir)
            new_path = os.path.split(new_file_path)[0]
            if not os.path.isdir(new_path):
                try:
                    os.makedirs(new_path)
                except:
                    print u"没有权限创建下载路径",
                    return
            if os.path.isfile(new_file_path):
                os.remove(new_file_path)
            shutil.copy(file_path, new_file_path)
            # 拷贝视频
            file_folder, file_name = os.path.split(file_path)
            mov_name = file_name[0:-3] + "_pv"
            for mo in os.listdir(file_folder):
                if mov_name in mo:
                    shutil.copy(os.path.join(file_folder, mo), os.path.join(file_folder, mo).replace("I:/", cur_dir))
            im_path = os.path.join(os.path.dirname(file_path), "sourceimages")
            if os.path.isdir(im_path):
                copy_img = cmds.confirmDialog(t=u"拷贝提示",
                                         m=u"<font color=red size=6>是否拷贝贴图到本地？</font><br><br><font color=yellow size=5>-拷贝,请按Yes.<br>-取消,请按Cancel.</font>",
                                         b=["Yes", "Cancel"], db="Cancel")
                if copy_img == "Yes":
                    print u"开始拷贝，请耐心等待。。。"
                    dst_path = os.path.join(os.path.dirname(new_file_path), "sourceimages")
                    self.copy_thread.copy_path = im_path
                    self.copy_thread.start()
                    print u"开始复制贴图到本地。。。"
                    # for root, dirs, files in os.walk(im_path):
                    #     for img in files:
                    #         source_path = os.path.join(root, img)
                    #         dst_full = source_path.replace("I:/", cur_dir)
                    #         if not os.path.isdir(os.path.dirname(dst_full)):
                    #             os.makedirs(os.path.dirname(dst_full))
                    #         shutil.copy(source_path, dst_full)
            if mod==3:
                return
            cfm = cmds.confirmDialog(t="Warning", m=u"<font color=red size=6>为了避免文件丢失,请手动保存文件.</font><br><br><font color=yellow size=5>-强制打开新文件,请按Yes.<br>-取消,请按Cancel.</font>",
                                     b=["Yes", "Cancel"], db="Cancel")
            if cfm == "Yes":
                cmds.file(new_file_path, options="v=0;", ignoreVersion=1, o=1, f=1)
            #
            # try:
            #     cmds.file(new_file_path, options="v=0;", ignoreVersion=1, o=1)
            # except:
            #     print u"请先清空文件后再打开文件",
        elif mod == 1:
            cmds.file(file_path, r=1, namespace="", ignoreVersion=1, gl=1, mergeNamespacesOnClash=0, options="v=0;")
        elif mod ==2:
            sel_list = cmds.ls(sl=1, long=1)
            rn_list = {}
            rn = None
            try:
                rn = cmds.referenceQuery(sel_list[0], rfn=1)
                cmds.file(file_path, loadReference=rn, options="v=0;p=17;f=0")
            except:
                pass

    def showContextMenu(self, pos):
        parent = self.currentItem()
        if parent:
            self.contextMenu.exec_(QtGui.QCursor.pos())

def get_current_dir():
    if os.path.isdir("E:/"):
        if not os.path.isdir("E:/Projects/"):
            try:
                os.makedirs("E:/Projects/")
            except:
                return
        return "E:/Projects/"
    elif os.path.isdir("D:/"):
        if not os.path.isdir("D:/Projects/"):
            try:
                os.makedirs("D:/Projects/")
            except:
                return
        return "D:/Projects/"
    elif os.path.isdir("F:/"):
        if not os.path.isdir("F:/Projects/"):
            try:
                os.makedirs("F:/Projects/")
            except:
                return
        return "F:/Projects/"
    else:
        return