#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import sys,os
from dayu_widgets.qt import *
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.message import MMessage
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.item_view import MTableView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets import dayu_theme
import subprocess
from utils import shotgun_operations
sg = shotgun_operations
from OCTLauncher.core.launch_dcc import LaunchDCC


class ExportAbcThread(QThread):
    """
    拷贝文件线程
    """
    finished = Signal(bool)  # 拷贝完成信号
    progress = Signal(list)  # 正在拷贝的文件名和进度

    def __init__(self, cmds=''):
        super(ExportAbcThread, self).__init__()
        self.cmds = cmds
        self.source = ''
        self.dest = ''

    def run(self):
        print self.cmds
        i = 0.0
        for cmd in self.cmds:
            i += 1.0
            launch_batch = LaunchDCC('Maya2017')
            launch_batch.launch_mode = 'back'
            launch_batch.back_launch_cmd = cmd
            launch_batch.launch_dcc()
            # subprocess.check_call(cmd, shell=True)
            progress = int(i * 100 / float(len(self.cmds)))
            self.progress.emit(progress)
        self.finished.emit(True)


def get_latestversion_info(task_info):
    task_id = task_info['id']
    project_name = task_info['project']
    find_type = task_info['type']
    latestversion_mayafile = []
    for t in range(0, len(task_id)):
        version_info_list = sg.find_shotgun("Version", [
            ["sg_task.Task.id", "is", task_id[t]],
            ['project', 'name_is', project_name],
            ["sg_version_type", "is", "Publish"]],
            ["sg_path_to_frames", "sg_version_number", "sg_task.Task.sg_publish_version"])
        if version_info_list:
            for v, version_info in enumerate(version_info_list):
                if version_info["sg_version_number"] == version_info["sg_task.Task.sg_publish_version"]:
                    latestversion_mayafile.append(version_info["sg_path_to_frames"])
                    break
    return latestversion_mayafile


Table_header = [
    {
        'label': u'ma文件路径',
        'key': 'path',
        # 'searchable': True
    }]


class ExportAbc(QDialog):
    fetching_data_sig = Signal(dict)
    submit_data_sig = Signal(list)

    def __init__(self,task_dict="",parent=None):
        super(ExportAbc, self).__init__(parent)
        self.resize(560, 400)
        self.setWindowTitle(u'导出abc')
        self.task_dict = task_dict
        self.maya_file_list = get_latestversion_info(self.task_dict)
        path_label = MLabel(u'选择路径：').secondary()
        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.dir_path_le.setText("C:/Program Files/Autodesk/Maya2017/bin/mayabatch.exe")
        self.data_table = MTableView(size=dayu_theme.small, show_row_count=True)
        self.data_table.setShowGrid(True)
        self.data_table.set_no_data_text(u'')
        self.data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_model = MTableModel()
        self.model_sort = MSortFilterModel()
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.horizontalHeader().setStretchLastSection(1)
        self.data_table.horizontalHeader().hide()
        self.model_sort.setSourceModel(self.data_model)
        self.data_table.setModel(self.model_sort)

        path_lay1 = QHBoxLayout()
        path_lay1.addWidget(path_label)
        path_lay1.addWidget(self.dir_path_le)
        # path_lay1.addWidget(self.get_files_pb)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.data_table)

        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()
        self.export_pb = MPushButton(text=u'输出缓存')

        progress_lay1 = QHBoxLayout()
        progress_lay1.addWidget(self.progress)
        progress_lay1.addWidget(self.progress_label)

        main_lay = QVBoxLayout()
        main_lay.addLayout(path_lay1)
        main_lay.addWidget(MDivider(u'选择文件列表'))
        main_lay.addLayout(self.vertical_layout)
        main_lay.addLayout(progress_lay1)
        main_lay.addWidget(self.export_pb)
        self.setLayout(main_lay)
        self.set_header(Table_header)
        # self.maya_file_list = [r"D:\ww\download\s30_020_Ly_V102.ma"]
        if self.maya_file_list:
            data = []
            for maya_file in self.maya_file_list:
                data_dict = {"path": maya_file}
                data.append(data_dict)
            self.set_data(data)
        else:
            MMessage.config(2)
            MMessage.error(u'没有可以出缓存的文件！', parent=self.task_dict['widget'])
        self.export_pb.clicked.connect(self.export)
        self.fetching_export_thread = ExportAbcThread()
        self.fetching_export_thread.progress.connect(self.get_data_export)
        self.fetching_export_thread.finished.connect(self.finish_fetch_data)

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

    @property
    def table_data(self):
        return self.data_model.get_data_list()

    @property
    def file_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    def clear_data(self):
        # 清空数据
        self.set_data([])
        self.data_model.clear()

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u"完成!")

    def get_data_export(self,data):
        self.set_progress(data)

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_export_thread.wait()
            self.fetching_export_thread.quit()
        self.export_pb.setText(u'缓存输出成功！')

    def export(self):
        if not self.table_data:
            MMessage.config(2)
            MMessage.error(u'没有可以导出缓存的文件', parent=self.task_dict['widget'])
            return
        else:
            cmds =[]
            # currentPath = os.path.dirname(__file__)
            currentPath = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
            publishPath = currentPath + '/core/actions/DSF/export_cache_tool/export_abc.py'  # % currentPath
            melFile = currentPath + '/core/actions/DSF/export_cache_tool/export_abc.mel'  # % currentPath
            for d in self.table_data:
                maya_file = d["path"]
                cmd = '"{mayaBatchPath}" -script "{melFile}" "{publishPath}" "{maPath}" '.format(
                    mayaBatchPath=self.file_path,
                    melFile=melFile,
                    publishPath=publishPath,
                    maPath=maya_file,
                )
                cmds.append(cmd)
            self.fetching_export_thread.cmds = cmds
            self.fetching_export_thread.start()
            self.export_pb.setEnabled(False)
            self.export_pb.setText(u'正在后台输出缓存...')


if __name__ == '__main__':
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    global test
    task_dict = {"id": [14608], "type": "Task", "user": "TD", "project": "Demo: Animation"}
    test = ExportAbc(task_dict)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())




