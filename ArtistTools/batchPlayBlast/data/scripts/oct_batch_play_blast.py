#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import getpass
from qt import *
import spb_main as spb
import maya.cmds as cmds
import maya.OpenMayaUI as omu


class PlayBlastUi(QWidget):
    def __init__(self, exe_file="", parent=None):
        super(PlayBlastUi, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.exe_file = exe_file
        self.resize(450, 547)
        self.listWidget = QListWidget()
        self.pushButton_2 = QPushButton(u"Select save path")
        self.lineEdit_2 = QLineEdit()
        self.pushButton_3 = QPushButton(u"PlayBlast")
        self.pushButton_4 = QPushButton(u"Select maya file")
        self.pushButton_5 = QPushButton(u"Remove maya file")
        self.label = QLabel(u"Progress")
        self.progressBar = QProgressBar()
        self.progressBar.setProperty("value", 0)
        
        self.Layout_2 = QVBoxLayout()
        self.Layout_2.addWidget(self.pushButton_4)
        self.Layout_2.addWidget(self.pushButton_5)
        
        self.Layout_1 = QHBoxLayout()
        self.Layout_1.addWidget(self.listWidget)
        self.Layout_1.addLayout(self.Layout_2)
        
        self.Layout_3 = QHBoxLayout()
        self.Layout_3.addWidget(self.lineEdit_2)
        self.Layout_3.addWidget(self.pushButton_2)
        
        self.Layout_4 = QHBoxLayout()
        self.Layout_4.addWidget(self.label)
        self.Layout_4.addWidget(self.progressBar)
        
        main_lay = QVBoxLayout()
        main_lay.addLayout(self.Layout_1)
        main_lay.addLayout(self.Layout_3)
        main_lay.addWidget(self.pushButton_3)
        main_lay.addLayout(self.Layout_4)
        self.setLayout(main_lay)
        
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.pushButton_2.clicked.connect(self.select_save_path)
        self.pushButton_4.clicked.connect(self.select_maya_file)
        self.pushButton_3.clicked.connect(self.run)
        self.pushButton_5.clicked.connect(self.remove)
        self.progressBar.setValue(0)

    def select_maya_file(self):
        self.listWidget.clear()
        maya_folder_path = QFileDialog.getExistingDirectory(self, "choose directory")
        for dir_path,subpaths,files in os.walk(maya_folder_path):
            for file_name in files:
                if file_name.endswith(".ma"):
                    maya_file_path = dir_path.replace('\\', '/')+"/" + file_name
                    self.listWidget.addItem(maya_file_path)

    def select_save_path(self):
        save_path = QFileDialog.getExistingDirectory(self, "choose directory")
        self.lineEdit_2.setText(save_path)

    @property
    def save_path(self):
        return self.lineEdit_2.text().replace('\\', '/')

    def remove(self):
        for i in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(i))

    def run(self):
        self.pushButton_3.setEnabled(0)
        self.pushButton_3.setText(u'Begin playblast')
        mafilelist = []
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        print "currentPath", current_path
        count = self.listWidget.count()
        for ii in xrange(count):
            maya_file = self.listWidget.item(ii).text()
            mafilelist.append(maya_file)
        playblast_list = []
        for ma_file in mafilelist:
            suffix = os.path.splitext(ma_file)[-1]
            mov_path = self.save_path + "/" + os.path.split(ma_file)[-1].replace(suffix, "")
            maya_file = {ma_file: mov_path}
            playblast_list.append(maya_file)
        self.play_blast(playblast_list)
        return True

    def play_blast(self,playblast_list):
        i = 0.0
        for file_path in playblast_list:
            i += 1.0
            artist = getpass.getuser()
            for k, v in file_path.items():
                mayafile_path = k
                cmds.file(mayafile_path, o=1, f=1)
                videosname = os.path.basename(mayafile_path).split(".")[0]
                mov_path = v
                playblast_n = spb.DsfSimplePlayBlast(self.exe_file)
                m3dview = omu.M3dView()
                c3dview = m3dview.active3dView()
                c3dview.setDisplayStyle(1)
                playblast_n.play_blast(artist, videosname, mov_path)
                progress = int(i * 100 / float(len(playblast_list)))
                self.progressBar.setValue(progress)
                if progress == 100:
                    self.pushButton_3.setText("Playblastend")
                    self.pushButton_3.setEnabled(1)
                    QMessageBox.information(self, u"Message", u"Success!", QMessageBox.Yes)


def main(exe_file):
    #app = QApplication(sys.argv)
    global win
    win = PlayBlastUi(exe_file)
    win.show()
    #sys.exit(app.exec_())

if __name__ == '__main__':
    import sys
    #app = QApplication(sys.argv)
    test = PlayBlastUi()
    test.show()
    #sys.exit(app.exec_())



