#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huang na
# Date  : 2019.7
# wechat : 18250844478
###################################################################
import os
import sys
import time


from PySide.phonon import *
import os
import sys
import time
import functools
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.qt import *
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from SystemTools.Autumn.gui import autumn_page
from config import GLOBAL
from dayu_widgets.radio_button import MRadioButton
from dayu_widgets.loading import MLoadingWrapper

from dayu_widgets import dayu_theme


detail_header_list = [
    {
        'label': u'版本',
        'key': 'version',
        # 'searchable': True
    }, {
        'label': u'状态',
        'key': 'state',
    }, {
        'label': u'描述',
        'key': 'description',
        # 'searchable': True
    }]

image_types = GLOBAL.format_file["picture"]
video_types = GLOBAL.format_file["video"]


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
        # self.videofrom.setFixedSize(470, 280)
        self.videofrom.setFixedHeight(280)

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
        # self.videofrom.setFixedSize(470, 280)
        self.videofrom.setFixedHeight(280)


    def redisplay(self, src_file):
        self.media.setCurrentSource(Phonon.MediaSource(src_file))
        self.media.play()


class DetailPage(QWidget, MFieldMixin):
    approve_sig = Signal(list)
    # publish_sig = Signal(list)

    def __init__(self, task_dict="", parent=None):
        super(DetailPage, self).__init__(parent=parent)
        self.task_dict = task_dict
        if not self.task_dict:
        # mime_dict = detail_page.get_version_dict(self.task_dict)
            self.mime_dict = {}
        self._init_ui()

    def _init_ui(self):
        # self.resize(300, 900)
        self.main_grid = QHBoxLayout()
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.main_grid)

        self.splitter_main = QSplitter(self)
        self.main_grid.addWidget(self.splitter_main)
        self.splitter_main.setOrientation(Qt.Vertical)
        self.mov_path = None
        if self.mime_dict:
            src_file_type = "."+self.mime_dict.get("preview_file").split('.')[-1]
            if src_file_type in image_types:
                self.preview_widget_Video = VideoWidget("")
                self.preview_widget_Image = ImageWidget(self.mime_dict["preview_file"])
                self.preview_widget_Video.videofrom.setVisible(False)
                self.preview_widget_Image.videofrom.setVisible(True)
            elif src_file_type in video_types:
                self.mov_path = self.mime_dict["preview_file"]
                self.preview_widget_Image = ImageWidget("")
                self.preview_widget_Video = VideoWidget(self.mime_dict["preview_file"])
                self.preview_widget_Image.videofrom.setVisible(False)
                self.preview_widget_Video.videofrom.setVisible(True)
                self.preview_widget_Video.media.finished.connect(self.playback)
            else:
                self.preview_widget_Image = ImageWidget("")
                self.preview_widget_Image.custom_widget.setMinimumHeight(250)
                self.preview_widget_Video = VideoWidget("")
                self.preview_widget_Image.custom_widget.setMinimumHeight(0)
                self.preview_widget_Video.videofrom.setVisible(False)
                self.preview_widget_Image.videofrom.setVisible(True)
            self.preview_widget = QWidget()
            vLayout = QVBoxLayout()
            vLayout.setSpacing(0)
            vLayout.setContentsMargins(0, 0, 0, 0)
            vLayout.addWidget(self.preview_widget_Video)
            vLayout.addWidget(self.preview_widget_Image)
            self.preview_widget.setLayout(vLayout)
            self.preview_widget.setFixedHeight(300)
        else:
            self.preview_widget_Image = ImageWidget("")
            self.preview_widget_Image.custom_widget.setMinimumHeight(250)
            self.preview_widget_Video = VideoWidget("")
            self.preview_widget_Image.custom_widget.setMinimumHeight(0)
            self.preview_widget_Video.videofrom.setVisible(False)
            self.preview_widget_Image.videofrom.setVisible(True)
            self.preview_widget = QWidget()
            vLayout = QVBoxLayout()
            vLayout.setSpacing(0)
            vLayout.setContentsMargins(0, 0, 0, 0)
            vLayout.addWidget(self.preview_widget_Image)
            vLayout.addWidget(self.preview_widget_Video)
            self.preview_widget.setLayout(vLayout)

        self.mime_data_layout = QGridLayout()
        self.mime_data_widget = QWidget(self.splitter_main)
        # table
        self.mime_data_table = autumn_page.SheetContent()
        # self.loading_wrapper = MLoadingWrapper(widget=self.mime_data_table.table, loading=False)
        # self.mime_data_table.fetch_data_thread.started.connect(functools.partial(self.loading_wrapper.set_dayu_loading, True))

        # self.mime_data_table.fetch_data_thread.finished.connect(self.stop_circling)
        # self.mime_data_table.fetch_data_thread.finished.connect(
        #     functools.partial(self.loading_wrapper.set_dayu_loading, False))
        # self.mime_data_table.fetch_data_thread.finished.connect(
        #     functools.partial(self.mime_data_table.table.setModel,
        #                       self.mime_data_table.model_sort))
        self.mime_data_table.fetch_data_thread.result_sig.connect(self.set_table)
        self.mime_data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mime_data_table.setMinimumHeight(300)
        # self.mime_data_table.setMinimumWidth(500)
        self.mime_data_layout.addWidget(self.mime_data_table)
        self.mime_data_widget.setLayout(self.mime_data_layout)

        self.mime_text_widget = QWidget()
        self.mime_text_layout = QVBoxLayout()

        self.task_id_layout = QHBoxLayout()
        self.task_id_lb = MLabel(u'编号:').secondary()
        self.task_id = MLabel(u'未发布').secondary()
        self.task_id_layout.addWidget(self.task_id_lb)
        self.task_id_layout.addWidget(self.task_id)
        self.mime_text_layout.addLayout(self.task_id_layout)

        self.file_name_layout = QHBoxLayout()
        self.file_name_lb = MLabel(u'文件名:').secondary()
        self.file_name = MLabel(u'未发布').secondary()
        self.file_name_layout.addWidget(self.file_name_lb)
        self.file_name_layout.addWidget(self.file_name)
        self.mime_text_layout.addLayout(self.file_name_layout)

        self.user_layout = QHBoxLayout()
        self.user_lb = MLabel(u'提交用户:').secondary()
        self.user = MLabel(u'未发布').secondary()
        self.user_layout.addWidget(self.user_lb)
        self.user_layout.addWidget(self.user)
        self.mime_text_layout.addLayout(self.user_layout)

        self.file_size_layout = QHBoxLayout()
        self.file_size_lb = MLabel(u'文件大小:').secondary()
        self.file_size = MLabel(u'未发布').secondary()
        self.file_size_layout.addWidget(self.file_size_lb)
        self.file_size_layout.addWidget(self.file_size)
        self.mime_text_layout.addLayout(self.file_size_layout)

        self.change_time_layout = QHBoxLayout()
        self.change_time_lb = MLabel(u'修改日期:').secondary()
        self.change_time = MLabel(u'未发布').secondary()
        self.change_time_layout.addWidget(self.change_time_lb)
        self.change_time_layout.addWidget(self.change_time)
        self.mime_text_layout.addLayout(self.change_time_layout)

        self.radiobutton_pub = MRadioButton(u"发布/锁定")
        self.radiobutton_sub = MRadioButton(u"提交")
        self.radiobutton_daily = MRadioButton(u"Daily")

        self.radiobutton_layout = QHBoxLayout()
        self.radiobutton_layout.addWidget(self.radiobutton_pub)
        self.radiobutton_layout.addWidget(self.radiobutton_sub)
        self.radiobutton_layout.addWidget(self.radiobutton_daily)

        self.select_version_type_layout = QHBoxLayout()
        self.select_version_type_lb = MLabel()
        self.select_version_type_cb = MComboBox()
        self.select_version_type_menu = MMenu()
        self.select_version_type_cb.set_menu(self.select_version_type_menu)

        self.mime_text_widget.setLayout(self.mime_text_layout)
        self.mime_data_layout.addWidget(self.mime_text_widget)

        window_layout = QGridLayout()
        window_layout.addWidget(self.preview_widget, 0, 0)
        window_layout.addWidget(self.mime_text_widget, 1, 0)
        window_layout.addLayout(self.radiobutton_layout, 2, 0)
        window_layout.addWidget(self.mime_data_widget, 3, 0)
        if self.task_dict:
            task_id = self.task_dict["id"][0]
            self.set_table_info(task_id)

        window_layout.setSpacing(2)
        self.setLayout(window_layout)
        self.mime_data_table.table.clicked.connect(self.change_task_info)
        self.mime_data_table.fetch_data_thread.result_sig.connect(self.hide_column)
        self.radiobutton_pub.clicked.connect(lambda: self.mime_data_table.model_sort.
                                             set_filter_attr_pattern("sg_version_type", "Publish|Approved"))
        self.radiobutton_sub.clicked.connect(lambda: self.mime_data_table.model_sort.
                                             set_filter_attr_pattern("sg_version_type", "Submit"))
        self.radiobutton_daily.clicked.connect(lambda: self.mime_data_table.model_sort.
                                               set_filter_attr_pattern("sg_version_type", "Dailies"))

    # def stop_circling(self):
        # self.loading_wrapper.set_dayu_loading(False)
        # self.mime_data_table.table.setModel(self.mime_data_table.model_sort)

    def set_table_info(self, detail_config):
        task_id = detail_config.get("task_id")
        if not task_id:
            self.mime_data_table.model.clear()
            return
        # functools.partial(self.loading_wrapper.set_dayu_loading, True)
        detail_actions = []
        try:
            detail_actions = detail_config['config']['detail_page_actions']
        except KeyError:
            pass
        color_dict = {'Approved': dayu_theme.green, 'Publish': dayu_theme.yellow, 'Submit': None, 'Dailies': dayu_theme.geekblue}
        self.mime_data_table.set_config({"page_actions": detail_actions,
                                         "page_fields": [{u"label": u"版本", u"key": "sg_version_number"},
                                                         {u"label": u"提交日期", u"key": "created_at"},
                                                         {u"label": u"类型", u"key": "sg_version_type",
                                                          'color': lambda x, y: color_dict[x]},
                                                         {u"label": u"工程文件", u"key": "sg_path_to_frames"},
                                                         {u"label": u"预览文件", u"key": "sg_path_to_movie"},
                                                         {u"label": u"Users", u"key": "user"},
                                                         {u"label": u"描述", u"key": "description"},
                                                         ],
                                         "page_filters": [["sg_task.Task.id", "is", task_id]],
                                         "page_name": "Group",
                                         "page_type": "Version",
                                         "page_svg": "calendar_line.svg",
                                         "page_order": [{'field_name': 'sg_version_number', 'direction': 'desc'}]
                                         })
        self.mime_data_table.parse_config()

    def set_playing_video(self, mov_path):
        if not mov_path:
            # self.preview_widget_Image.src_file = mov_path
            # self.preview_widget_Video.src_file = mov_path
            self.preview_widget_Image.show()
            self.preview_widget_Image.redisplay(u'占位图片')
            # self.preview_widget_Video.redisplay("")
            self.preview_widget_Image.custom_widget.setMinimumHeight(200)
            self.preview_widget_Image.custom_widget.setMinimumHeight(0)
            self.preview_widget_Video.videofrom.setVisible(False)
            self.preview_widget_Image.videofrom.setVisible(True)
        else:
            src_file_type = "." + mov_path.split('.')[-1]
            if src_file_type in image_types:
                self.preview_widget_Image.show()
                self.preview_widget_Image.redisplay(mov_path)
                self.preview_widget_Video.hide()
                self.preview_widget_Image.videofrom.setMinimumHeight(200)
                self.preview_widget_Video.videofrom.setMinimumHeight(0)
                self.preview_widget_Video.videofrom.setVisible(False)
                self.preview_widget_Image.videofrom.setVisible(True)

            if src_file_type in video_types:
                self.preview_widget_Video.show()
                self.preview_widget_Video.redisplay(mov_path)
                self.preview_widget_Image.hide()
                self.preview_widget_Video.videofrom.setVisible(True)
                self.preview_widget_Video.videofrom.setMinimumHeight(200)
                self.preview_widget_Image.videofrom.setMinimumHeight(0)
                self.preview_widget_Image.videofrom.setVisible(False)

    def set_table(self):
        self.radiobutton_pub.setChecked(True)
        self.mime_data_table.model_sort.set_filter_attr_pattern("sg_version_type", "Publish|Approved")

    def hide_column(self):
        self.mime_data_table.table.hideColumn(0)
        self.mime_data_table.table.hideColumn(4)
        self.mime_data_table.table.hideColumn(5)
        self.mime_data_table.table.hideColumn(6)


    def change_task_info(self):
        row = self.mime_data_table.table.currentIndex().row()
        _id = self.mime_data_table.model_sort.index(row, 0).data()
        user_name = self.mime_data_table.model_sort.index(row, 6).data()
        ma_file = self.mime_data_table.model_sort.index(row, 4).data()
        mov_file = self.mime_data_table.model_sort.index(row, 5).data()
        mime_dict = dict()
        mime_dict.update({
            "_id": _id,
            "user": user_name,
            "project_file": ma_file,
            "preview_file": mov_file})
        src_file_type = mime_dict["preview_file"].split('.')[-1]
        if src_file_type in video_types:
            self.mov_path = mime_dict["preview_file"]
        self.set_mime_data(mime_dict)

    def playback(self):
        self.preview_widget_Video.media.setCurrentSource(Phonon.MediaSource(self.mov_path))
        self.preview_widget_Video.media.seek(0)
        self.preview_widget_Video.media.play()

    def pause_mov(self):
        self.media.pause()

    def show_context_menu(self):
        self.mime_data_table.contextMenu = QMenu(self)
        self.mime_data_table.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        self.mime_data_table.contextMenu.show()

    def _set_file_size(self, size):
        self.file_size.setText(size)

    def _set_id(self, _id):
        self.task_id.setText(_id)

    def _set_user(self, user):
        self.user.setText(user)

    def _set_file_name(self, file_name):
        self.file_name.setText(file_name)

    def _set_change_time(self, change_time):
        self.change_time.setText(change_time)

    @staticmethod
    def format_size(bytes_):
        try:
            bytes_ = float(bytes_)
            kb = bytes_ / 1024
        except Exception as e:
            print e
            print(u"传入的字节格式不对")
            return "Error"
        if kb >= 1024:
            M = round(kb / 1024, 2)
            if M >= 1024:
                G = round(M / 1024, 2)
                return "%sG" % G
            else:
                return "%sM" % M
        else:
            return "%skb" % round(kb, 2)

    def get_doc_size(self, file_):
        try:
            size = os.path.getsize(file_)
            return self.format_size(size)
        except Exception as err:
            print(err)

    def set_mime_data(self, data):
        _id = data.get("_id")
        user = data.get("user")
        project_file = data.get("project_file")
        preview_file = data.get("preview_file")
        if project_file and project_file != "--":
            file_name = project_file.replace('\\', '/').split('/')[-1].split('.')[0]
            try:
                file_size = self.get_doc_size(project_file)
            except WindowsError:
                file_size = '--'
            if os.path.isfile(project_file):
                mtime = os.stat(project_file).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                if preview_file:
                    self.mov_path = preview_file
                    self.set_playing_video(preview_file)
                self._set_change_time(file_modify_time)
                self._set_file_name(file_name)
                self._set_file_size(file_size)
                self._set_id(str(_id))
                self._set_user(user)
        else:
            if preview_file:
                self.mov_path = preview_file
                self.set_playing_video(preview_file)
            self._set_id(str(_id))
            self._set_user(user)
            self._set_file_name("")
            self._set_file_size("")
            self._set_change_time("")


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"task_id": [14608], "type": "Task", "user": "TD", "project": 'Demo: Animation'}
    test = DetailPage(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())








