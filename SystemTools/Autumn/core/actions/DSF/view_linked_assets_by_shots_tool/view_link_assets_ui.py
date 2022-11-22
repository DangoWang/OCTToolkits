#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.10.8
import json
import os
from dayu_widgets.qt import *
from SystemTools.Autumn.gui import autumn_page
import view_link_asset
from dayu_widgets.label import MLabel
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from pprint import pprint
from utils.fileIO import CopyFTP
from utils.fileIO import CopyFile
from utils.fileIO import FormRPCCopy
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.button_group import MCheckBoxGroup
from dayu_widgets.message import MMessage
from SystemTools.Autumn.core.actions.DSF.download_tool import file_download
from utils import shotgun_operations
sg = shotgun_operations
import view_link_asset
reload(view_link_asset)


class WriteDatabase(QThread):
    # 用于创建更新的线程
    write_finished = Signal(bool)

    def __init__(self, parent=None):
        super(WriteDatabase, self).__init__(parent)
        self.data = None

    def run(self, *args, **kwargs):
        for each in self.data:
            print each
            if each:
                if each[0] == 'update':
                    sg.update_shotgun(each[1], each[2], each[3])
                if each[0] == 'create':
                    sg.create_shotgun(each[1], each[2])
        self.write_finished.emit(True)


class LinkAsset(QWidget, MFieldMixin):

    def __init__(self, task_dict=""):
        super(LinkAsset, self).__init__()
        self.task_dict = task_dict
        self.project_name = self.task_dict["project"]
        self.resize(600, 760)
        self.setWindowTitle(u'连接的资产信息')
        self.table_step = []
        self.step = view_link_asset.get_step_list(self.project_name)
        self.shot_name = MTextEdit()
        self.shot_name.setMaximumHeight(80)
        self.shot_name.setDisabled(True)
        self.radio_group_b = MCheckBoxGroup()
        self.radio_group_b.sig_checked_changed.connect(self.search_table)
        self.radio_group_b.set_button_list(self.step)

        self.place_holder_label = MLabel(u'请先选择环节↑↑↑').h1().warning()
        self.place_holder_label.setMinimumSize(300, 400)
        self.place_holder_label.setAlignment(Qt.AlignCenter)

        self.mime_data_table = autumn_page.SheetContent()
        self.mime_data_table.fetch_data_thread.result_sig.connect(self.hide_column)
        self.check_box_normal = MCheckBox("")
        self.path_label = MLabel(u'同步路径：').secondary()
        self.dir_path_le = MLineEdit().folder()
        self.dir_path_le.setMinimumWidth(300)
        self.download_select_pb = MPushButton(u'同步所有').small().primary()
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_label.hide()
        self.progress.hide()

        layout_label = QVBoxLayout()
        layout_label.addWidget(self.shot_name)

        layout_path = QHBoxLayout()
        layout_path.addWidget(self.check_box_normal)
        layout_path.addWidget(self.path_label)
        layout_path.addWidget(self.dir_path_le)
        layout_button = QHBoxLayout()
        layout_button.addWidget(self.download_select_pb)

        progress_lay1 = QVBoxLayout()
        progress_lay1.addWidget(self.progress)
        progress_lay1.addWidget(self.progress_label)

        layout = QVBoxLayout()
        layout.addWidget(MDivider(u'镜头号'))
        layout.addLayout(layout_label)
        layout.addWidget(MDivider(u'资产表'))
        layout.addWidget(self.radio_group_b)
        layout.addWidget(self.mime_data_table)
        self.mime_data_table.hide()
        layout.addWidget(self.place_holder_label)
        layout.addLayout(layout_path)
        layout.addLayout(layout_button)
        layout.addLayout(progress_lay1)

        main_lay = QVBoxLayout()
        main_lay.addLayout(layout)
        self.setLayout(main_lay)
        self.user_name = task_dict['user']
        self.group_list = view_link_asset.get_group_list(self.user_name)
        self.oss_path_template, self.copy_path_template = view_link_asset.get_oss_path(self.task_dict["project"],
                                                                                       "Asset", "Publish")
        self.dir_path_le.setPlaceholderText(self.copy_path_template)
        self.shot_name_list, self.asset_id_list, self.all_assignees_id = view_link_asset.get_asset_info(self.task_dict)
        self.shot_name.setText(" ".join(self.shot_name_list))
        if self.asset_id_list:
            self.set_table_info()
        self.download_select_pb.clicked.connect(self.synchronization_all)
        self.fetching_copy_thread = CopyFTP() if self.group_list["sg_permission_group"] in ['outsource'] else CopyFile()
        self.rpc_copy_to_oss = FormRPCCopy('upload')
        self.rpc_copy_to_oss.progress.connect(self.get_data_copy)
        self.rpc_copy_to_oss.finished.connect(self.finish_fetch_data)
        self.fetching_copy_thread.progress.connect(self.get_data_copy)
        self.fetching_copy_thread.finished.connect(self.finish_fetch_data)
        self.check_box_normal.stateChanged.connect(self.show_path)
        self.dir_path_le.setDisabled(True)
        self.write_data_base_thread = WriteDatabase(parent=self)
        self.write_data_base_thread.write_finished.connect(self.finish_writing)

    def set_table_info(self):
        self.mime_data_table.set_config({"page_actions": "",
                                         "page_fields": [{u"label": u"资产名", u"key": "entity.Asset.code"},
                                                         {u"label": u"任务名", u"key": "content"},
                                                         {u"label": u"通过的版本", u"key": "sg_publish_version"},
                                                         {u"label": u"资产类型", u"key": "entity.Asset.sg_asset_type"},
                                                         {u"label": u"本地版本", u"key": "using_version"},
                                                         {u"label": u"环节", u"key": "step"},
                                                         ],
                                         "page_filters": [['entity.Asset.id', 'in', self.asset_id_list]],
                                         "page_name": "Group",
                                         "page_type": "Task",
                                         "page_svg": "calendar_line.svg",
                                         "page_order": [{'field_name': 'entity.Asset.code', 'direction': 'desc'}]
                                         })
        self.mime_data_table.parse_config()

    def search_table(self, texts):
        self.mime_data_table.show()
        self.place_holder_label.hide()
        value = ""
        for t in texts:
            if value:
                value = value + "|"+t
            else:
                value = t
        if not value:
            self.mime_data_table.hide()
            self.place_holder_label.show()
            return
        self.mime_data_table.model_sort.set_filter_attr_pattern("step", value)
        self.table_step = texts

    @property
    def folder_path(self):
        # 返回当前文件夹路径
        return self.dir_path_le.text().replace('\\', '/')

    @property
    def task_name(self):
        return self.combobox.currentText()

    def show_path(self):
        if self.check_box_normal.isChecked():
            self.dir_path_le.setDisabled(False)
        else:
            self.dir_path_le.setDisabled(True)

    def hide_column(self):
        self.mime_data_table.table.hideColumn(0)
        self.mime_data_table.table.hideColumn(4)
        if self.group_list["sg_permission_group"] in ['outsource']:
            self.read_json_file()

    def read_json_file(self):
        get_table_list = self.mime_data_table.data
        cache_path = os.path.dirname(__file__).replace("\\", "/").replace("Autumn/gui/action_ui", "cache/")
        json_file_path = cache_path + "/using_asset_version.json"
        new_table_list = []
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as load_f:
                load_dict = json.load(load_f)
            for table_data in get_table_list:
                try:
                    _id = table_data["id"]
                    table_data["using_version"] = load_dict[str(_id)]
                except:
                    table_data["using_version"] = None
                new_table_list.append(table_data)
            self.mime_data_table.model.set_data_list(new_table_list)

    def write_json(self, step_list):
        cache_path = os.path.dirname(__file__).replace("\\", "/").replace("Autumn/gui/action_ui", "cache/")
        json_file_path = cache_path+"/using_asset_version.json"
        if os.path.exists(json_file_path):
            os.remove(json_file_path)
        get_table_list = self.mime_data_table.data
        version_num_dict = dict()
        for table_data in get_table_list:
            if step_list:
                if table_data["step"] in step_list:
                    _id = table_data["id"]
                    version = table_data["sg_publish_version"]
                    version_num_dict.update({_id: version})
            else:
                _id = table_data["id"]
                version = table_data["sg_publish_version"]
                version_num_dict.update({_id: version})
        with open(json_file_path, "w") as f:
            json.dump(version_num_dict, f)

    def get_selected_rows(self):
        indexes = self.mime_data_table.table.selectedIndexes()
        rows = list(set([index.row() for index in indexes]))
        return rows

    def synchronization_all(self):
        if not self.table_step:
            MMessage.config(2)
            MMessage.warning(u'请先选择环节', parent=self)
            return
        self.download_select_pb.setText(u"正在同步...")
        self.download_select_pb.setDisabled(True)
        self.set_progress(0)
        dict_id_version, version_id_list = self.get_task_id(self.table_step)
        # dict_id_version = {"任务id":["任务下面版本的sg_version_number","版本code"]}
        # version_id_list = 任务下面最新版本的ID
        all_copy_list = None
        rpc_all_copy_list = None
        if self.group_list["sg_permission_group"] not in ['outsource']:  # 内部人员
            if self.folder_path:    # 如果选择了路径就是下载到内部，
                download_dict = {"id": version_id_list, "project": self.project_name,
                                 "local_path": self.folder_path, "type": "Version",
                                 'identity': self.group_list["sg_permission_group"]}
                pprint(download_dict)
                all_copy_list = file_download.get_version_info(download_dict)
            else:   # 上传阿里云
                kwargs = {"project": self.project_name, "id": version_id_list, "user": self.user_name}
                rpc_all_copy_list, update_code = \
                    view_link_asset.get_inside_copy_list(kwargs, self.oss_path_template, self.copy_path_template)
                # all_copy_list 获取上传阿里云的路径列表
                outsource_id_list = view_link_asset.get_outsource_shot(self.all_assignees_id)
                # 获取哪个任务分配给外包，返回任务以及对应得外包人员字典
                create_note_code = view_link_asset.update_sg(kwargs, self.shot_name_list,
                                                             self.asset_id_list, outsource_id_list,
                                                             dict_id_version)
                update_code.extend(create_note_code)
                # print "----------------------update_code-----------------"
                # pprint(update_code)
                self.write_data_base_thread.update_code_list = update_code
        else:   # 外包人员需要从阿里云上拉取资产，并记录json文件
            self.write_json(self.table_step)
            if not self.folder_path:
                folder_path = "I:/"
            else:
                folder_path = self.folder_path
            download_dict = {"id": version_id_list, "project": self.project_name,
                             "local_path": folder_path, "type": "Version",
                             'identity': "outsource"}
            all_copy_list = file_download.get_version_info(download_dict)
        # print "--------------------------all_copy_list---------------------"
        # pprint(all_copy_list)
        if all_copy_list:
            self.fetching_copy_thread.copy_list = all_copy_list
            self.fetching_copy_thread.start()
        if rpc_all_copy_list:
            self.rpc_copy_to_oss.copy_list = rpc_all_copy_list
            self.rpc_copy_to_oss.start()

    def get_task_id(self, step_list=[]):
        task_id_list = []
        for data in self.mime_data_table.data:
            if step_list:
                if data["step"] in step_list:
                    if int(data["id"]) not in task_id_list:
                        task_id_list.append(int(data["id"]))
            else:
                if int(data["id"]) not in task_id_list:
                    task_id_list.append(int(data["id"]))
        print task_id_list
        if task_id_list:
            dict_id_version, version_id_list = view_link_asset.get_latest_version(task_id_list, self.project_name)
            return dict_id_version, version_id_list
            # dict_id_version = {"任务id":["任务下面版本的sg_version_number","版本code"]}
            # version_id_list = 任务下面最新版本的ID
        else:
            return None

    def set_progress(self, number, text=''):
        # 设置进度
        if self.progress_label.isHidden():
            self.progress_label.show()
            self.progress.show()
        self.progress_label.setText(text)
        self.progress.setValue(number)
        if number == 100:
            self.progress_label.setText(u'同步完成！')
            self.download_select_pb.setText(u"同步完成")

    def get_data_copy(self, data):
        self.set_progress(data[1], data[0])

    def finish_fetch_data(self, finished):
        if finished:
            # self.fetching_copy_thread.wait()
            # self.fetching_copy_thread.quit()
            # 只拷贝文件的话就通知外包
            if self.group_list["sg_permission_group"] not in ['outsource'] and not self.folder_path:
                self.progress_label.setText(u'正在写入数据库，请稍后....')
                self.write_data_base_thread.start()

    def finish_writing(self, result):
        if result:
            MMessage.config(2)
            MMessage.success(u'数据库写入成功！', parent=self)
            self.progress_label.setText(u'数据库写入成功！')
            self.submit_progress.setValue(100)


def link_asset_drawer(widget, task_dict):
    from ....widgets import ADrawer
    drawer_widget = ADrawer('LinkAssets', parent=widget)
    drawer_widget.setMinimumWidth(500)
    drawer_widget.set_dayu_position('right')
    detail_content = LinkAsset(task_dict)
    drawer_widget.set_widget(detail_content)
    return drawer_widget


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    version_dict = {"id": [15977], "type": "Task", "user": "huangna", "project": 'DSF'}
    test = LinkAsset(version_dict)
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())

