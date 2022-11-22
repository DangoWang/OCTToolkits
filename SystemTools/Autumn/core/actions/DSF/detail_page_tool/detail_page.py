#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huang na
# Date  : 2019.7
# wechat : 18250844478
###################################################################
import os

from utils import shotgun_operations
from dayu_widgets.qt import *
from PySide.phonon import *
from dayu_widgets.message import MMessage
from pprint import pprint
sg = shotgun_operations


def get_version_dict(task_dict):
    task_id = task_dict["id"][0]
    version_info_list = sg.find_shotgun("Version",[
        ["sg_task.Task.id", "is", task_id], ['project', 'name_is', task_dict["project"]]],
        ["code", "description", "sg_status_list", "sg_version_number", "sg_path_to_frames",
         "sg_path_to_movie", "id", "user", "sg_task.Task.sg_latestversion"])
    if version_info_list:
        version_dict = {}
        for v, version_info in enumerate(version_info_list):
            if version_info["sg_version_number"] == version_info["sg_task.Task.sg_latestversion"]:
                version_dict.update({
                    "_id": version_info["id"],
                    "user": (version_info.get("user") or {}).get('name', ''),
                    "project_file": version_info["sg_path_to_frames"],
                    "preview_file": version_info["sg_path_to_movie"]
                })
                break
        if not version_dict:
            MMessage.config(2)
            MMessage.error(u'没有最新版本的信息！', parent=task_dict['widget'])
        return version_dict


class ImageWidget(QWidget):
    def __init__(self, src_file=""):
        super(ImageWidget, self).__init__()
        self.src_file = src_file
        self.videofrom = QWidget()
        self.custom_widget = QLabel()
        self.custom_widget.setStyleSheet("background-color:black;")
        self.custom_widget.setPixmap(QPixmap(self.src_file))
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.custom_widget)
        self.videofrom.setLayout(self.vLayout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.videofrom, 1)
        window_layout.setSpacing(2)
        self.setLayout(window_layout)
        self.videofrom.setFixedSize(470, 280)

    def redisplay(self, src_file):
        if not src_file:
            return
        img = QImage(src_file)
        w, h = img.width(), img.height()
        for _ in xrange(999):
            if w <= 400:
                break
            w = w * 0.9
            h = h * 0.9
        size = QSize(w, h)
        pic = QPixmap(img.scaled(size, Qt.IgnoreAspectRatio))
        self.custom_widget.setPixmap(QPixmap(pic))


class VideoWidget(QWidget):
    def __init__(self, src_file=""):
        super(VideoWidget, self).__init__()
        self.videofrom = QWidget()
        self.media = Phonon.MediaObject()
        vwidget = Phonon.VideoWidget(self.videofrom)
        Phonon.createPath(self.media, vwidget)
        vwidget.setAspectRatio(Phonon.VideoWidget.AspectRatioAuto)
        aOutput = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.media, aOutput)
        self.media.setCurrentSource(Phonon.MediaSource(src_file))

        layout_1 = QVBoxLayout()
        layout_1.addWidget(vwidget)
        self.videofrom.setLayout(layout_1)
        self.media.play()
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.videofrom, 1)
        window_layout.setSpacing(2)
        self.setLayout(window_layout)
        self.videofrom.setFixedSize(470, 280)

    def redisplay(self, src_file):
        self.media.setCurrentSource(Phonon.MediaSource(src_file))
        self.media.play()


if __name__ == '__main__':
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme
    import sys
    app = QApplication(sys.argv)
    global test
    # task_dict = {"task_id": [15969], "type": "Task", "user": "TD", "project": "Demo: Animation"}
    mov_path = ""
    test = ImageWidget(mov_path)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())