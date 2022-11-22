#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.11.6
# wechat : 18250844478
import os
import sys
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.message import MMessage
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets.progress_bar import MProgressBar
from thirdparty.PIL import Image


class ChangeSize(QThread):
    """
    更改贴图尺寸线程
    """
    finished = Signal(bool)  # 拷贝完成信号
    progress = Signal(list)  # 正在拷贝的文件名和进度

    def __init__(self, change_list=''):
        super(ChangeSize, self).__init__()
        self.change_list = change_list
        #  attachments_dict:{下载路径： 附件id列表}
        #self.change_list:[[保存路径, 尺寸],[贴图路径，...],]

    def run(self):
        if not self.change_list:
            return
        save_path = self.change_list[0][0]
        size = self.change_list[0][1]
        i = 1
        for tex in self.change_list[1]:
            try:
                img_switch = Image.open(tex)  # 读取图片
                img_deal = img_switch.resize((int(size), int(size)))  # 转化图片
                file_name = os.path.split(tex)[1]
                tex_save_path = save_path + "/" + file_name
                img_deal.save(tex_save_path)
                self.progress.emit([file_name, (float(i) / float(len(self.change_list[1]))) * 100])
                i += 1
            except Exception as e:
                self.progress.emit([u'以下文件转换尺寸出现错误：%s' % tex + ': ' + str(e), (float(i) / float(len(self.change_list[1]))) * 100])
        self.finished.emit(True)


class ChangeTexSize(QWidget, MFieldMixin):

    def __init__(self):
        super(ChangeTexSize, self).__init__()
        self.resize(700, 520)
        self.setWindowTitle(u'更改贴图尺寸')

        path_label = MLabel(u'选择路径：').secondary()
        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        browser_7 = MDragFolderButton()
        browser_7.sig_folder_changed.connect(self.dir_path_le.setText)

        save_path_label = MLabel(u'选择保存路径：').secondary()
        self.save_path_le = MLineEdit().folder()
        self.save_path_le.setMinimumWidth(300)
        self.save_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')

        size_label = MLabel(u'填写尺寸：').secondary()
        self.size_le = MLineEdit()
        self.size_le.setMinimumWidth(50)
        self.submit_pb = MPushButton(text=u'开始')
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        path_lay1 = QHBoxLayout()
        path_lay1.addWidget(path_label)
        path_lay1.addWidget(self.dir_path_le)

        path_lay2 = QHBoxLayout()
        path_lay2.addWidget(size_label)
        path_lay2.addWidget(self.size_le)
        path_lay2.addWidget(save_path_label)
        path_lay2.addWidget(self.save_path_le)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.progress_label)
        h_layout.addWidget(self.progress)

        main_lay = QVBoxLayout()
        main_lay.addLayout(path_lay1)
        main_lay.addWidget(MDivider(u'拖拽文件夹'))
        main_lay.addWidget(browser_7)
        main_lay.addWidget(MDivider(u'选择保存路径'))
        main_lay.addLayout(path_lay2)
        main_lay.addWidget(self.submit_pb)
        main_lay.addLayout(h_layout)
        self.setLayout(main_lay)

        self.log_dialog = QTextEdit(self)
        self.log_dialog.setReadOnly(True)
        geo = QApplication.desktop().screenGeometry()
        self.log_dialog.setGeometry(geo.width() / 2 - 1000, geo.height() / 2 - 500, geo.width() / 4, geo.height() / 4)
        self.log_dialog.setWindowTitle(self.tr('Log Information'))
        self.log_dialog.setText(self.property('history'))
        self.log_dialog.setWindowFlags(Qt.Dialog)

        self.setAcceptDrops(True)

        self.submit_pb.clicked.connect(self.change_texture)
        self.fetching_data_thread = ChangeSize()
        self.fetching_data_thread.progress.connect(self.get_data)
        self.fetching_data_thread.finished.connect(self.finish_fetch_data)

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    @property
    def save_folder_path(self):
        # 返回保存的路径
        return self.save_path_le.text().replace('\\', '/')

    @property
    def get_size(self):
        # 返回填写的尺寸
        return self.size_le.text()

    def show_log(self):
        # 显示日志窗口
        self.log_dialog.show()

    def append_log(self, txt):
        # 增加一条日志信息
        log = self.log_dialog.toPlainText() or ''
        self.log_dialog.setText(log+'\n'+txt)

    def clear_log(self):
        # 清空日志信息
        self.log_dialog.clear()

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'更改尺寸完成！')

    def get_data(self, data):
        txt = data[0]
        if u'错误' in txt:
            self.append_log(txt)
        else:
            self.set_progress(data[1], data[0])

    def change_texture(self):
        if not self.folder_path or not self.save_folder_path:
            MMessage.config(2)
            MMessage.error(u'请先选择路径!', parent=self)
            return
        if not self.get_size:
            MMessage.config(2)
            MMessage.error(u'请先填写尺寸!', parent=self)
            return
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.submit_pb.setText(u"开始更改贴图尺寸...")
        self.submit_pb.setDisabled(True)
        change_tex_list = [[self.save_folder_path, self.get_size]]
        tex_list = []
        for home, dirs, files in os.walk(self.folder_path):
            for f in files:
                if os.path.splitext(f)[1] in ['.tif']:
                    file_path = home + "/" + f
                    tex_list.append(file_path)
        change_tex_list.append(tex_list)
        self.fetching_data_thread.change_list = change_tex_list
        self.fetching_data_thread.start()

    def finish_fetch_data(self, finished):
        if finished:
            self.progress_label.setText(u'转换完成！')
            self.progress.setValue(100)
            self.submit_pb.setText(u"更改贴图尺寸完成...")
            self.fetching_data_thread.wait()
            self.fetching_data_thread.quit()
            MMessage.config(1)
            MMessage.success(u'更改贴图尺寸完成!', parent=self)


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = ChangeTexSize()
    dayu_theme.apply(test)
    test.show()
    test.show_log()
    sys.exit(app.exec_())


