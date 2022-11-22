# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# author: wangdonghao
from dayu_widgets.qt import *
from dayu_widgets.push_button import MPushButton
from dayu_widgets.divider import MDivider
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.message import MMessage
import utils.common_methods as atu
from utils import shotgun_operations
from dayu_widgets.label import MLabel
from dayu_widgets.progress_bar import MProgressBar
from ..publish_tool.publish_file_action import ApprovedFileAction


class BatchPublish(QDialog):
    def __init__(self, kwargs, parent=None):
        super(BatchPublish, self).__init__(parent)
        self.__task_info = kwargs.copy()
        self.__version_info = kwargs.copy()
        self.__version_info['page_type'] = 'Version'
        self.__version_info['id'] = []
        self.__copy_progress = 0.0
        self.setWindowTitle(u'批量发布工具')
        self.resize(500, 500)
        self._init_ui()

    def _init_ui(self):
        self.main_lay = QVBoxLayout()
        self.label = MLabel()
        self.main_lay.addWidget(self.label)
        self.main_lay.addWidget(MDivider(u'输入发布描述'))
        self.description = MTextEdit(self)
        self.error_log = MTextEdit(self)
        self.main_lay.addWidget(self.description)
        self.doit_pb = MPushButton(u'发布').primary()
        self.main_lay.addWidget(self.doit_pb)
        self.main_lay.addWidget(self.error_log)
        self.progress = MProgressBar()
        self.main_lay.addWidget(self.progress)
        self.error_log.setReadOnly(True)
        self.error_log.setText(u'正在发布...\n')
        self.error_log.hide()
        self.doit_pb.clicked.connect(self.batch_publish_doit)
        self.setLayout(self.main_lay)
        if self.__task_info:
            self.label.setText(u'将发布选中的 %s 个任务.' % len(self.__task_info['id']))
        # self.publish_action = ApprovedFileAction(parent=self)
        # self.publish_action.write_database.write_finished.connect(self.get_publish_result)

    def append_log(self, txt):
        etxt = self.error_log.toPlainText()
        self.error_log.setText(etxt + '\n' + txt)

    def get_submit_version(self):
        try:
            wrong_tasks = []
            for each in self.__task_info['id']:
                latest_version_info = shotgun_operations.find_one_shotgun('Task', [['id', 'is', each],
                                                                                   ['project', 'name_is', self.__version_info['project']]],
                                                                          ['sg_latestversion'])
                latest_version_num = latest_version_info['sg_latestversion']
                latest_version = shotgun_operations.find_one_shotgun('Version',
                                                                     [
                                                                         ['project', 'name_is', self.__version_info['project']],
                                                                         ['sg_version_number', 'is', str(latest_version_num)],
                                                                         ['sg_version_type', 'is', 'Submit'],
                                                                         ['sg_task', 'is', latest_version_info]
                                                                     ], ['id']
                                                                     )
                if not latest_version:
                    wrong_tasks.append(each)
                    continue
                self.__version_info['id'].append([latest_version['id']])
            if wrong_tasks:
                self.append_log(u'查询以下任务时出现问题，请确保文件信息已正确上传至shotgun: %s' % wrong_tasks)
                raise RuntimeError
        except:
            return

    def batch_publish_doit(self):
        if len(self.description.toPlainText()) < 10:
            MMessage.error(u'描述不能少于十个字符！', parent=atu.get_widget_top_parent(self))
            raise RuntimeError
        self.doit_pb.setText(u'正在后台发布， 请勿关闭窗口...')
        self.doit_pb.setEnabled(False)
        self.error_log.show()
        self.get_submit_version()
        if not self.__version_info['id']:
            return
        self.append_log(u'共有%s个文件需要发布...' % len(self.__version_info['id']))
        for version_id in self.__version_info['id']:
            version_info = self.__version_info.copy()
            version_info['id'] = version_id
            publish_action = ApprovedFileAction(version_info, parent=self)
            publish_action.description.setText(self.description.toPlainText())
            publish_result = publish_action.publishd()
            publish_action.write_database.write_finished.connect(self.get_publish_result)
            if publish_result is not True:
                self.append_log(u'发布版本编号{}时出现问题：{};请检查是否正常提交.'.format(version_id, publish_result))

    def get_publish_result(self):
        self.__copy_progress += 1.0
        self.progress.setValue(self.__copy_progress*100.0/len(self.__version_info['id']))
        if self.progress.value() >= 100:
            self.doit_pb.setText(u'任务全部发布完成！')
            self.append_log(u'全部发布完成！现在你可以关闭此窗口了.')


if __name__ == '__main__':
    pass
    # import sys
    # from dayu_widgets.qt import QApplication
    # from dayu_widgets import dayu_theme
    # app = QApplication(sys.argv)
    # test = BatchPublish(None)
    # dayu_theme.apply(test)
    # test.show()
    # sys.exit(app.exec_())