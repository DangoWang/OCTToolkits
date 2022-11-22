#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/11/6

import os
import sys
import time
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.browser import MDragFileButton, MDragFolderButton
from dayu_widgets.message import MMessage
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
from PySide.QtGui import *
from PySide.QtCore import *
from utils import fileIO, shotgun_operations
from config import GLOBAL
from utils import common_methods

frame_file_formats = GLOBAL.format_file['frame']
picture_file_formats = GLOBAL.format_file['picture']
video_file_formats = GLOBAL.format_file['video']


class DealCopy(QThread):
    copy_sig = Signal(list)

    def __init__(self, copy_list=None, parent=None):
        super(DealCopy, self).__init__(parent=parent)
        self.copy_list = copy_list
        #  __copy_list: [[s, d], [s, d] ...]

    def run(self, *args, **kwargs):
        final_result = []
        for each in self.copy_list:
            if os.path.isfile(each[1]):
                a = time.localtime(os.stat(each[0]).st_mtime)
                b = time.localtime(os.stat(each[1]).st_mtime)
                mTimeS = time.strftime('%Y-%m-%d %H:%M:%S', a)
                mTimeD = time.strftime('%Y-%m-%d %H:%M:%S', b)
                s_size = os.path.getsize(each[0])
                d_size = os.path.getsize(each[1])
                if mTimeS == mTimeD and s_size == d_size:
                    continue
            final_result.append(each)
        if final_result:
            self.copy_sig.emit(final_result)


class ModifySubmit(QDialog, MFieldMixin):

    def __init__(self, parent=None):
        super(ModifySubmit, self).__init__(parent=parent)
        self.version_detail = []
        self.__work_file = None
        self.__prev_file = None
        self.__attach = None
        self.version_id = None
        self.project = None
        self.__deal_copy_thread = DealCopy(parent=self)
        self.__deal_copy_thread.copy_sig.connect(self.__get_dealed_copy_result)
        self.copy_thread = fileIO.CopyFile()
        self.copy_thread.progress.connect(self.__set_progress)
        self.copy_thread.finished.connect(self.__finished_copy)
        self._init_ui()

    def _init_ui(self):
        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(MDivider(u'覆盖上传'))

        version_name_layout = QHBoxLayout()
        self.__version_name_lb = MLabel()
        version_name_layout.addWidget(MLabel(u'版本名称:'))
        version_name_layout.addWidget(self.__version_name_lb)
        version_name_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__main_layout.addLayout(version_name_layout)

        self.__main_layout.addWidget(MDivider(u'工程文件'))
        self.construction_file = MDragFileButton(text='')
        self.construction_file.setFixedHeight(70)
        self.construction_file.set_dayu_svg('upload_line.svg')
        self.construction_file.sig_file_changed.connect(self.__construction_path)
        self.__main_layout.addWidget(self.construction_file)
        self.__main_layout.addWidget(MDivider(u'预览文件'))
        self.preview_file = MDragFileButton(text='', multiple=False)
        self.preview_file.setFixedHeight(70)
        self.preview_file.set_dayu_svg('media_line.svg')
        self.preview_file.sig_file_changed.connect(self.__preview_path)
        self.__main_layout.addWidget(self.preview_file)
        self.__main_layout.addWidget(MDivider(u'附件(文件夹, 例如 D:/aaa/sourceimages )'))
        self.attach = MDragFolderButton()
        self.attach.setFixedHeight(70)
        self.attach.setText('')
        self.__main_layout.addWidget(self.attach)
        self.attach.sig_folder_changed.connect(self.__external_path)

        self.__main_layout.addWidget(MDivider(u'追加描述'))
        self.desc_edit = MTextEdit()
        self.desc_edit.setMinimumHeight(100)
        self.__main_layout.addWidget(self.desc_edit)

        __doit_button_layout = QHBoxLayout()
        self.__submit_btn = MPushButton(u'上传').small()
        self.__cancel_btn = MPushButton(u'取消').small()
        __doit_button_layout.addWidget(self.__submit_btn)
        __doit_button_layout.addWidget(self.__cancel_btn)
        self.__cancel_btn.clicked.connect(self.close)
        self.__main_layout.addLayout(__doit_button_layout)

        self.__log_edit = MTextEdit()
        self.__log_edit.setMinimumHeight(200)
        self.__log_edit.setReadOnly(True)
        self.__log_edit.hide()
        self.__main_layout.addWidget(self.__log_edit)

        self.progress_layout = QVBoxLayout()
        self.submit_progress = MProgressBar()
        self.submit_progress.hide()
        self.progress_label = MLabel()
        self.progress_label.hide()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.submit_progress)
        self.__main_layout.addLayout(self.progress_layout)

        self.__submit_btn.clicked.connect(self.__submit_doit)

        self.setLayout(self.__main_layout)
        self.setMinimumWidth(500)

    def parse_data(self, version_info=None):
        if version_info:
            self.version_id = version_info['id'][0]
            self.project = version_info['project']
            version_detail = shotgun_operations.find_one_shotgun('Version',
                                                                 [['id', 'is', int(self.version_id)], ['project', 'name_is', self.project]],
                                                                 ['code', 'sg_path_to_movie', 'sg_version_type',
                                                                  'sg_path_to_geometry', 'sg_path_to_frames']
                                                                 )
            no_version = shotgun_operations.find_one_shotgun('Version',
                                                                 [['project', 'name_is', version_info['project']],
                                                                 ['sg_version_type', 'is', version_detail['sg_version_type']],
                                                                  ['sg_version_number', 'is', None],
                                                                  ['code', 'is', version_detail['code'][:-5]]
                                                                  ],
                                                                 ['code', 'sg_path_to_movie',
                                                                  'sg_path_to_geometry', 'sg_path_to_frames']
                                                                 )
            self.version_detail.append(version_detail)
            self.version_detail.append(no_version)
            self.__version_name_lb.setText(version_detail['code'])

    @staticmethod
    def __file_format(filename):
        return '.'+filename.split('.')[-1]

    def __construction_path(self, text):
        if self.__file_format(text) not in frame_file_formats:
            MMessage.error(u'请放入maya文件，格式为：' + str(frame_file_formats),
                           parent=common_methods.get_widget_top_parent(self))
            return
        self.construction_file.setText(text)
        self.__work_file = text

    def __preview_path(self, text):
        if self.__file_format(text) not in picture_file_formats + video_file_formats:
            MMessage.error(u'请放入预览文件，格式为' + str(picture_file_formats + video_file_formats),
                           parent=common_methods.get_widget_top_parent(self))
            return
        self.preview_file.setText(text)
        self.__prev_file = text

    def __external_path(self, text):
        self.attach.setText(text)
        self.__attach = text

    def __submit_doit(self):
        self.__log_edit.show()
        self.__append_log(u'开始处理需要更新的文件...')
        try:
            att_files = []
            for each in self.version_detail:
                att_files.extend(fileIO.get_copy_list(self.__attach,
                                                      each['sg_path_to_geometry']+'/'+self.__attach.split('/')[-1]))
        except:
            att_files = []
        copy_list = []
        if self.__work_file:
            for wv in self.version_detail:
                copy_list.append([self.__work_file, wv['sg_path_to_frames']])
        if self.__prev_file:
            for pv in self.version_detail:
                copy_list.append([self.__prev_file, pv['sg_path_to_movie']])
        copy_list.extend(att_files)
        self.__deal_copy_thread.copy_list = copy_list
        print copy_list
        self.__deal_copy_thread.start()

    def __append_log(self, text):
        self.__log_edit.append('\n' + text)

    def __get_dealed_copy_result(self, dealed_result):
        all_files_need_update = [aa[1].split('/')[-1].split('\\')[-1] for aa in dealed_result]
        self.__append_log(u'共扫描到以下文件需要更新：\n%s' % ('\n'.join(all_files_need_update)))
        self.__append_log(u'开始上传...')
        self.submit_progress.show()
        self.progress_label.show()
        self.copy_thread.copy_list = dealed_result
        self.copy_thread.start()
        return

    def __set_progress(self, data):
        self.submit_progress.setValue(data[1])
        self.progress_label.setText(u'正在拷贝至:'+data[0])
        self.__append_log('copying: %s' % data[0])

    def __finished_copy(self, finished):
        if finished:
            self.__append_log(u'正在写入描述...')
            if self.version_id:
                if self.desc_edit.toPlainText():
                    version_modify = shotgun_operations.find_one_shotgun('Version', [['project', 'name_is', self.project],
                                                                                   ['id', 'is', self.version_id]],
                                                                       ['description', 'code', 'sg_task', "user"])
                    existed_desc_txt = version_modify['description'] or ''
                    desc = self.desc_edit.toPlainText() or ''
                    new_desc = existed_desc_txt + '\n' + desc
                    shotgun_operations.update_shotgun('Version', self.version_id, {'description': new_desc})
                    if self.__prev_file:
                        shotgun_operations.upload_shotgun("Version", version_modify['id'], self.__prev_file,
                                                          field_name="sg_uploaded_movie",
                                                          display_name=version_modify['code'])


                    # 发送通知给抄送人
                    project_node = shotgun_operations.find_one_shotgun('Project', [['name', 'is', self.project]], [])
                    # version_modify = shotgun_operations.find_one_shotgun('Version', [['id', 'is', self.version_id]],
                    #                                                      ['sg_task', "user"])
                    task_info = shotgun_operations.find_one_shotgun('Task',
                                                                    [['id', 'is', version_modify["sg_task"]["id"]]],
                                                                    ['entity.Asset.addressings_cc',
                                                                     'entity.Shot.addressings_cc',
                                                                     'addressings_cc', 'content', 'entity']
                                                                    )
                    asset_adressings = task_info['entity.Asset.addressings_cc'] or []
                    shot_adressings = task_info['entity.Shot.addressings_cc'] or []
                    task_name_en = task_info['entity'].get('name', 'None') + '_' + task_info['content']
                    task_info['addressings_cc'].extend(asset_adressings)
                    task_info['addressings_cc'].extend(shot_adressings)
                    note_data = {
                        "project": project_node,
                        "subject": u'修改提交通知：' + task_name_en,
                        "sg_proposer": version_modify["user"],
                        "addressings_to": task_info['addressings_cc'],
                        "content": u"用户{}提交了任务修改{}。描述为:\n{}".format(version_modify["user"].get('name', 'None'),
                                                                    task_name_en,
                                                                    new_desc),
                        "sg_if_read": False,
                    }
                    shotgun_operations.create_shotgun('Note', note_data)


            self.__append_log(u'上传成功！现在你可以关闭窗口了。')
            self.submit_progress.setValue(100)
            self.progress_label.setText(u'上传完成！')
            self.__submit_btn.setEnabled(False)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    from dayu_widgets.theme import MTheme
    window = ModifySubmit()
    this_theme = MTheme('dark')
    this_theme.apply(window)
    window.show()
    sys.exit(app.exec_())

