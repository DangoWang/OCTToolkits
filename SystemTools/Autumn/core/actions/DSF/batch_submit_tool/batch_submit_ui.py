#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
###################################################################

from config import GLOBAL
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.qt import *
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.message import MMessage
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets import dayu_theme
import batch_submit
reload(batch_submit)
import utils.shotgun_operations
reload(utils.shotgun_operations)
sg = utils.shotgun_operations
batch_submit_header = [
    {
        'label': u'ma文件',
        'key': 'ma',
        # 'searchable': True
    }, {
        'label': u'预览文件',
        'key': 'preview',
        # 'searchable': True
    }, {
        'label': u'版本',
        'key': 'version',
        # 'searchable': True
    }, {
        'label': u'ma文件路径',
        'key': 'ma_path',
        # 'searchable': True
    }, {
        'label': u'mov文件路径',
        'key': 'mov_path',
        # 'searchable': True
    }
]


class BatchSubmitWindow(QMainWindow):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self, parent=None):
        super(BatchSubmitWindow, self).__init__(parent=parent)
        self.resize(1000, 700)
        self.setWindowTitle(u'oct 批量上传工具 v2019.8.5')
        # self.layout = QGridLayout()
        # self.layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        # self.layout.addWidget(self.main_widget, 0, 0)
        self.main_widget.setMinimumSize(530, 700)
        self.main_layout = QGridLayout()
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        # 选择环节，选择上传路径
        self.widget_1 = QWidget(self.splitter)
        self.widget_1.setMaximumHeight(80)
        self.horizontal_layout_1 = QHBoxLayout()
        self.vertical_layout_1 = QVBoxLayout()
        self.vertical_layout_1.addLayout(self.horizontal_layout_1)
        self.widget_1.setLayout(self.vertical_layout_1)

        self.horizontal_layout_1.addWidget(MLabel(u'项目名：').secondary())
        self.project_cb = MLineEdit()
        self.project_cb.setMaximumWidth(130)
        self.project_cb.set_dayu_size(dayu_theme.small)
        self.project_cb.setObjectName('group_cb')
        self.horizontal_layout_1.addWidget(self.project_cb)

        self.horizontal_layout_1.addWidget(MLabel(u'选择环节：').secondary())
        self.group_cb = MComboBox()
        self.group_cb.set_placeholder(u'选择环节')
        self.group_cb.setMaximumWidth(100)
        self.group_menu = MMenu()
        self.group_cb.set_dayu_size(dayu_theme.small)
        self.group_cb.set_menu(self.group_menu)
        self.group_cb.setObjectName('group_cb')
        self.horizontal_layout_1.addWidget(self.group_cb)

        self.horizontal_layout_1.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.addWidget(MLabel(u'选择路径：').secondary())
        self.dir_path_le = MLineEdit().folder().small()
        self.dir_path_le.setPlaceholderText(u'输入路径或点击右侧文件夹图标浏览文件(选填)')
        self.get_files_pb = MPushButton(u'获取').small().primary()
        horizontal_layout_2.addWidget(self.dir_path_le)
        horizontal_layout_2.addWidget(self.get_files_pb)
        self.vertical_layout_1.addLayout(horizontal_layout_2)

        self.widget_2 = QWidget(self.splitter)
        self.vertical_layout = QVBoxLayout()
        self.widget_2.setLayout(self.vertical_layout)
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
        self.vertical_layout.addWidget(self.data_table)

        self.describe_te = MTextEdit(u'输入描述...')
        self.describe_te.setMaximumHeight(50)
        self.vertical_layout.addWidget(self.describe_te)

        h_layout = QHBoxLayout()
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        h_layout.addWidget(self.progress_label)
        h_layout.addWidget(self.progress)
        self.progress_label.hide()
        self.progress.hide()
        self.vertical_layout.addLayout(h_layout)

        self.submit_pb = MPushButton(text=u'提交')
        self.vertical_layout.addWidget(self.submit_pb)

        self.main_layout.addWidget(self.splitter, 0, 0)
        self.main_widget.setLayout(self.main_layout)

        self.log_dialog = QTextEdit(self)
        self.log_dialog.setReadOnly(True)
        geo = QApplication.desktop().screenGeometry()
        self.log_dialog.setGeometry(geo.width() / 2 - 1000, geo.height() / 2-500, geo.width() / 4, geo.height() / 4)
        self.log_dialog.setWindowTitle(self.tr('Log Information'))
        self.log_dialog.setText(self.property('history'))
        self.log_dialog.setWindowFlags(Qt.Dialog)

        self.setAcceptDrops(True)

        self.files_list = []
        self.submit_data = []
        self.get_files_pb.clicked.connect(self.get_files)
        self.submit_pb.clicked.connect(self.copy_files)
        self.msg = QWidget()
        #user_list = read_shotgun_shot.project_list()[0]
        #self.set_project(user_list)
        # groups = GLOBAL.SHOTTASKNAME
        groups = ["Ly", "An", "Bk", "Flo"]
        self.set_groups(groups)
        self.fetching_data_thread = batch_submit.FetchBatchSubmitDataThread()
        self.fetching_data_thread.fetch_result_sig.connect(self.get_data)
        self.fetching_data_thread.finished_sig.connect(self.finish_fetch_data)
        self.fetching_copy_thread = batch_submit.CopyFile()
        self.fetching_copy_thread.progress.connect(self.get_data_copy)
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)
        self.set_project()

    def set_header(self, header_data):
        """
        :param header_data: 表头
        :return:
        """
        self.data_model.set_header_list(header_data)
        self.data_table.set_header_list(header_data)

    def set_data(self, data):
        """
        :param data: 表格数据
        :return:
        """
        self.data_model.set_data_list(data)

    def set_project(self):
        # 设置当前用户
        project = sg.get_project()
        # project = "Demo: Animation"
        self.project_cb.setText(project)

    def set_groups(self, groups):
        # 设置当前环节
        self.group_menu.set_data(groups)

    @property
    def get_project(self):
        # 返回当前用户
        return self.project_cb.text()

    @property
    def group(self):
        # 返回当前环节
        return self.group_cb.currentText()

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    @property
    def table_data(self):
        return self.data_model.get_data_list()

    @property
    def describe(self):
        # 返回描述
        return self.describe_te.toPlainText()

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

    def clear_data(self):
        # 清空数据
        self.set_data([])
        self.data_model.clear()

    def append_data(self, data_dict):
        # 增加一条数据
        self.data_model.append(data_dict)

    def get_files(self):
        # 发送路径信号
        self.clear_data()
        self.clear_log()
        self.set_progress(0)
        if not self.group:
            MMessage.config(2)
            MMessage.error(u'请先选择环节!', parent=self)
            return
        if self.folder_path:
            self.fetching_data_thread.files_list = {
                                         'files': self.folder_path,
                                         'group': self.group,
                                         'project': self.get_project
                                         }
            self.fetching_data_thread.start()

    def copy_files(self):
        if not self.table_data:
            MMessage.config(2)
            MMessage.error(u'请先选择上传的文件!', parent=self)
            return
        else:
            self.submit_pb.setText(u"正在提交...")
            self.submit_pb.setDisabled(True)
            project = self.get_project
            copy_list = batch_submit.get_copy_file_list(self,self.table_data, project, self.group, self.describe)
            self.fetching_copy_thread.copy_list = copy_list
            self.fetching_copy_thread.start()

    def get_data(self, data):
        txt = data['msg']
        self.append_log(txt)
        table_info = data['data']
        if table_info:
            self.append_data(dict(table_info.values()[0]))

    def get_data_copy(self, data):
        self.set_progress(data[1])

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_data_thread.wait()
            self.fetching_data_thread.quit()

    def finish_copy_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'拷贝文件完成！')
            self.submit_pb.setText(u"提交完成...")
            self.submit_pb.setDisabled(False)

    def dragEnterEvent(self, event):
        """获取拖拽过来的文件夹+文件"""
        self.clear_data()
        self.clear_log()
        self.set_progress(0)
        if not self.group:
            MMessage.config(2)
            MMessage.error(u'请先选择环节!', parent=self)
            return
        if event.mimeData().hasFormat("text/uri-list"):
            self.clear_log()
            self.files_list = list(set([url.toLocalFile() for url in event.mimeData().urls()]))
            event.acceptProposedAction()
            self.fetching_data_thread.files_list = {
                'files': self.files_list,
                'group': self.group,
                'project': self.get_project
            }

    def dropEvent(self, event):
        """获取拖拽过来的文件夹"""
        self.fetching_data_thread.start()
        # folder_list = [url.toLocalFile() for url in event.mimeData().urls() if os.path.isdir(url.toLocalFile())]
        # return folder_list


def main():
    from dayu_widgets import dayu_theme
    global test
    test = BatchSubmitWindow()
    test.set_header(batch_submit_header)
    dayu_theme.apply(test)
    test.show_log()
    test.show()


if __name__ == '__main__':
    import sys
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    test = BatchSubmitWindow()
    test.set_header(batch_submit_header)
    dayu_theme.apply(test)
    test.show_log()
    test.show()

    sys.exit(app.exec_())
