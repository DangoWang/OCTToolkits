#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import sys
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets import dayu_theme
from dayu_widgets.divider import MDivider


class DownLoadCache(QDialog):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, parent=None):
        super(DownLoadCache, self).__init__(parent=parent)
        self.resize(470, 400)
        self.setWindowTitle(u'替换最新资产')

        self.data_table = MTableView(size=dayu_theme.small, show_row_count=True)
        self.data_table.setShowGrid(True)
        self.data_table.set_no_data_text(u'拖拽文件或文件夹到这里')
        self.data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_model = MTableModel()
        self.model_sort = MSortFilterModel()
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.horizontalHeader().setStretchLastSection(1)
        self.model_sort.setSourceModel(self.data_model)
        self.data_table.setModel(self.model_sort)

        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件夹(选填)')

        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        self.download_pb = MPushButton(text=u'下载')

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.progress_label)
        h_layout.addWidget(self.progress)

        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider(u'缓存信息'))
        main_lay.addWidget(self.data_table)
        main_lay.addWidget(MDivider(u'选择保存的路径'))
        main_lay.addWidget(self.dir_path_le)
        main_lay.addLayout(h_layout)
        main_lay.addWidget(self.download_pb)
        self.setLayout(main_lay)

    def set_header(self, header_data):
        """
        :param header_data: 表头
        :return:
        """
        self.data_table.set_header_list(header_data)
        self.data_model.set_header_list(header_data)

    def set_data(self, data):
        """
        :param data: 表格数据
        :return:
        """
        self.data_model.set_data_list(data)

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'完成！')

    def clear_data(self):
        # 清空数据
        self.set_data([])
        self.data_model.clear()


if __name__ == '__main__':
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = DownLoadCache()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


