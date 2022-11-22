#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################
import datetime
import getpass
import importlib
import os
from hashlib import md5
from functools import partial
from operator import methodcaller
import ui
import core
from ..dcc_utils import *
import maya.cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2
from utils import fileIO
from pprint import pprint
import time
import shutil
import tools

reload(ui)
reload(core)


class CopyFileThread(QtCore.QThread):
    result_sig = QtCore.Signal(list)
    finished_sig = QtCore.Signal(bool)

    def __init__(self):
        super(CopyFileThread, self).__init__()
        self.copy_list = []

    def run(self):
        i = 0.0
        copy_len = float(len(self.copy_list))
        copied = []
        for each in self.copy_list:
            source, dest = each
            file_name = os.path.split(source)[1]
            if dest in copied or '.db' in source:
                self.result_sig.emit([file_name, i * 100.0 / copy_len])
                i += 1.0
                continue
            if os.path.isfile(source):
                try:
                    if not os.path.isdir(os.path.dirname(dest)):
                        try:
                            os.makedirs(os.path.dirname(dest))
                        except:
                            os.mkdir(os.path.dirname(dest))
                    # shutil.copy2(source, dest)
                    if os.path.isfile(each[1]):
                        a = time.localtime(os.stat(each[0]).st_mtime)
                        b = time.localtime(os.stat(each[1]).st_mtime)
                        mTimeS = time.strftime('%Y-%m-%d %H:%M:%S', a)
                        mTimeD = time.strftime('%Y-%m-%d %H:%M:%S', b)
                        s_size = os.path.getsize(each[0])
                        d_size = os.path.getsize(each[1])
                        if mTimeS == mTimeD and s_size == d_size:  # 如果修改日期和大小完全一致，不拷贝
                            pass
                        else:
                            shutil.copy2(each[0], each[1])
                    else:
                        shutil.copy2(each[0], each[1])
                    self.result_sig.emit([file_name, i*100.0/copy_len])
                    i += 1.0
                    copied.append(dest)
                except Exception as e:
                    print u'CopyFile ERROR', e
                    pass
        self.finished_sig.emit(True)


class OctMayaSubmit(ui.UiDialog):

    def __init__(self):
        super(OctMayaSubmit, self).__init__()
        self.setupUi(self)
        self.setParent(getMayaWindow())
        self.setWindowTitle(u'oct maya 提交工具2.0  2019.8.22')
        self.copied = []
        self.__copy_progress = 1
        self.project_lb.setText(self.project)  # 设置项目
        self.user_lb.setText(self.user)  # 设置用户
        # self.set_file_path()  # 设置当前工作目录
        self.tasks_cb.currentIndexChanged.connect(self.change_current_task)  # 当前任务变更
        self.input_file_path_pb.clicked.connect(self.set_file_path)  # 输入文件路径
        self.playblast_img_pb.clicked.connect(self.playblast_img)  # 拍图
        self.grab_img_pb.clicked.connect(self.grab_img)  # 截图
        self.playblast_prev_pb.clicked.connect(self.play_blast)
        self.select_preview_file_pb.clicked.connect(self.select_preview_file)  # 选择预览文件
        self.get_task_pb.clicked.connect(self.arrange_tasks_items)  # 获取任务
        self.remove_attachment_pb.clicked.connect(self.delete_attachment)  # 移除选中的附件
        self.refresh_attachment_pb.clicked.connect(self.refresh_attachment)  # 刷新附件
        self.check_pb.clicked.connect(self.raise_check_window)  # 唤起质检窗口
        self.submit_pb.clicked.connect(self.submit_files)  # 提交文件
        self.tasks_dict = {}
        self.sg_task = None
        self.copy_file_thread = CopyFileThread()
        self.copy_file_thread.result_sig.connect(self.get_copy_progress)
        self.copy_file_thread.finished_sig.connect(self.finished_copy)
        self.log_text_edit.setReadOnly(True)

    @property
    def user(self):
        return core.get_user()

    @property
    def project(self):
        return core.get_project()

    @property
    def task_code(self):
        # NH_XiZ或者01_001
        return self.tasks_dict[self.task_name_en]['code']

    @property
    def task_name_en(self):
        # NH_XiZ_RIG或者01_001_Ly
        return self.tasks_cb.currentText()

    @property
    def new_version(self):
        return int(self.version_sb.value())

    @property
    def task_id(self):
        return self.tasks_dict[self.task_name_en]['id']

    @property
    def task_type(self):
        return self.tasks_dict[self.task_name_en]['type']

    @property
    def task_name(self):
        return self.tasks_dict[self.task_name_en]['task_name']

    @property
    def task_step(self):
        return self.tasks_dict[self.task_name_en]['step']

    @property
    def task_classify(self):
        return self.tasks_dict[self.task_name_en]['classify']

    @property
    def task_scene(self):
        return self.tasks_dict[self.task_name_en]['scene']

    @property
    def task_shot(self):
        return self.tasks_dict[self.task_name_en]['shot']

    @property
    def task_version(self):
        if self.tasks_dict[self.task_name_en]['version']:
            if int(self.tasks_dict[self.task_name_en]['version']) > 100:
                return int(self.tasks_dict[self.task_name_en]['version'])
        return 101

    @property
    def project_file(self):
        return self.project_file_le.text()

    @property
    def preview_file(self):
        return self.preview_file_le.text()

    @property
    def prev_file_type(self):
        return '.' + self.preview_file.split('.')[-1]

    @property
    def current_folder(self):
        return core.os.path.dirname(self.project_file)

    @property
    def convention(self):
        return core.get_path_convention(self.project, self.task_type, 'Submit')

    @property
    def submit_path(self):
        return self.convention['sg_pattern'].format(**self.tasks_dict[self.task_name_en])

    @property
    def attach_path(self):
        return '/'.join(
            [self.submit_path, self.convention['sg_attachment_path'].format(**self.tasks_dict[self.task_name_en])])

    @property
    def attach_no_version(self):
        return '/'.join([self.submit_path,
                         self.convention['sg_attachment_no_version'].format(**self.tasks_dict[self.task_name_en])])

    @property
    def attachments(self):
        attach_folders = []
        for i in range(0, self.attachment_tw.topLevelItemCount()):
            item = self.attachment_tw.topLevelItem(i)
            attach_folders.append(item.text(0))
        return attach_folders

    @property
    def describe(self):
        return self.describe_te.toPlainText()

    def get_task_dict(self):
        self.tasks_dict = core.get_tasks(self.project, self.user)
        for task_whole_name, task_info in self.tasks_dict.items():
            self.tasks_dict[task_whole_name]['version'] = str(int(task_info['version']) + 1).zfill(3)
        return self.tasks_dict

    def set_new_version(self):
        self.version_sb.setValue(self.task_version)

    def file_name(self, with_version=False, form='.ma'):
        if with_version:
            if form in ['.ma']:
                return self.convention['sg_work_file_name'].format(**self.tasks_dict[self.task_name_en]) + form
            return self.convention['sg_prev_file_name'].format(**self.tasks_dict[self.task_name_en]) + form
        if form in ['.ma']:
            return self.convention['sg_workfile_no_version'].format(**self.tasks_dict[self.task_name_en]) + form
        return self.convention['sg_prevfile_no_version'].format(**self.tasks_dict[self.task_name_en]) + form

    def change_current_task(self):
        if not self.task_name_en:
            return
        # if self.tasks_dict[self.task_name_en]['version']:
        #     self.tasks_dict[self.task_name_en]['version'] = '101'
        # else:
        #
        # self.tasks_dict[self.task_name_en]['version'] = str(int(self.tasks_dict[self.task_name_en]['version'])+1).zfill(3)
        self.sg_task = core.find_shotgun('Task',
                                         [['project', 'name_is', self.project], ['id', 'is', self.task_id]],
                                         ['id', 'code', 'updated_at', 'addressings_cc',
                                          'entity.Asset.addressings_cc', 'entity.Shot.addressings_cc',
                                          ])[0]
        self.last_update_time_lb.setText(self.sg_task['updated_at'].strftime('%Y-%m-%d %H:%M:%S'))
        if self.check_asset_naming():
            self.set_new_version()
        self.set_submit_path()
        if self.task_type not in ['Asset'] or self.task_step in ['ani']:
            return True
        find_asset = False
        for ass in cmds.ls(assemblies=True):
            if ass in self.task_name_en:
                find_asset = True
                break
        if not find_asset:
            QtWidgets.QMessageBox.warning(self, u"警告：", u'发现大纲层级与任务名不匹配！请确认大纲层级正确???')
        find_high = False
        for ass1 in cmds.ls(assemblies=True):
            if cmds.objExists('|%s|Geometry|high' % ass1):
                find_high = True
                break
        if not find_high:
            QtWidgets.QMessageBox.warning(self, u"警告：", u'high层级不正确！请确认Geometry和high的拼写是否正确？')

    def select_preview_file(self):
        uwd_temp = cmds.file(q=1, sn=1).decode('utf-8')
        uwd = uwd_temp if uwd_temp else ''
        try:
            selected_path_temp = cmds.fileDialog2(dialogStyle=1, fileMode=1, dir=uwd)
            selected_path = selected_path_temp[0] if selected_path_temp else ''
            self.preview_file_le.setText(selected_path)
            if selected_path.endswith('.mov'):
                a = time.localtime(os.stat(selected_path).st_mtime)
                mTimeS = time.strftime('%Y-%m-%d %H:%M:%S', a).split()[0]
                today = str(datetime.datetime.now()).split()[0]
                if not mTimeS == today:
                    QtWidgets.QMessageBox.warning(self, u"警告：", u'拍屏必须是今天的！你选的拍屏日期是%s' % mTimeS)
                    return False
                # if os.
            return selected_path
        except IndexError:
            return ""

    def arrange_tasks_items(self):
        if not self.user or not self.project:
            QtWidgets.QMessageBox.critical(self, u"错误：", u'未登陆或当前账号未分配项目！ ')
            return
        self.progress_lb.show()
        self.progress_bar.show()
        self.set_progress(0, u'正在获取任务...')
        self.get_task_dict()
        all_tasks = sorted(list(self.tasks_dict.keys()))
        self.tasks_cb.clear()
        self.tasks_cb.addItem('')
        self.tasks_cb.addItems(all_tasks)
        self.set_progress(100, u'成功拉取任务！')

    def append_log(self, text):
        self.log_text_edit.append('\n' + text)

    def set_progress(self, value, text=''):
        # 设置当前进度以及进度的label
        self.progress_bar.setValue(value)
        self.progress_lb.setText(text)

    def clear_attachments(self):
        self.attachment_tw.clear()

    def append_attachment(self, attachment_path):
        # 根据路径来添加附件
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, attachment_path)
        self.attachment_tw.addTopLevelItem(item)

    def delete_attachment(self):
        # 删除选中的item
        for item in self.attachment_tw.selectedItems():
            shiboken2.delete(item)

    def refresh_attachment(self):
        # 可以根据当前工作路径扫描出所有的附件文件夹， 并添加到附件列表
        # 配合self.append_attachment使用
        self.clear_attachments()
        if not self.current_folder or not core.os.path.isdir(self.current_folder):
            QtWidgets.QMessageBox.critical(self, u"错误：", u'请先输入正确的工作路径 ')
            return
        all_attachments = core.list_current_dir(self.current_folder, mode='folders')
        for each in all_attachments:
            self.append_attachment(each)
        if all_attachments:
            QtWidgets.QMessageBox.information(self, u"提示：", u'附件列表已更新，请留意。 ')
        pass

    def check_asset_naming(self):
        task_obj = self.task_code
        # if self.task_type in ['Asset']:
        #     if self.task_step not in ['ani']:
        #         if not cmds.objExists(task_obj):
        #             QtWidgets.QMessageBox.critical(self, u"错误：", u'资产命名有误！请检查文件命名规范！正确应为:\n%s'
        #                                            % task_obj)
        #             self.splitter.setEnabled(0)
        #             self.check_pb.setEnabled(0)
        #             return False
        return True

    def raise_check_window(self):
        process = self.task_step or ''
        check_class_dict = core.check_class_dict

        def dynamic_import(module):
            return importlib.import_module('DCC_TOOLS.common.maya_submit.tools.' + module + '.' + module)

        def make_push_button_enabled(signal):
            if signal:
                self.submit_pb.setEnabled(1)
            else:
                self.submit_pb.setEnabled(0)
            return

        check_process = 'check_' + process
        try:
            check_class = dynamic_import(check_process)
            reload(check_class)
            check_win = methodcaller(check_class_dict[process])(check_class)
            check_win.result_signal.connect(make_push_button_enabled)
            check_win.show()
        except ImportError:
            QtWidgets.QMessageBox.critical(self, u'警告', u'当前环节缺少质检工具！', QtWidgets.QMessageBox.Yes)
            make_push_button_enabled(1)

    def set_file_path(self):
        try:
            current_file = get_current_file_name(full_path=True, dir_path=False)
            if not current_file.endswith('.ma'):
                QtWidgets.QMessageBox.critical(self, u"错误：", u'文件格式不正确！必须是ma格式.')
                return
            self.project_file_le.setText(current_file)
            if not self.tasks_cb.currentText():
                if not self.tasks_dict:
                    self.arrange_tasks_items()
                if self.tasks_dict:
                    for k, v in self.tasks_dict.items():
                        if k in current_file:
                            task_index = self.tasks_cb.findText(k)
                            self.tasks_cb.setCurrentIndex(task_index)
                            # self.tasks_cb.setEditText(k)
                            # self.change_current_task()
            else:
                print self.tasks_cb.currentText(), current_file
                if current_file and self.tasks_cb.currentText() not in current_file:
                    QtWidgets.QMessageBox.warning(self, u"警告：", u'当前任务名称不在文件名中，请确认所选的任务没错？')
            # self.refresh_attachment()
        except Exception, e:
            print u'发生错误:', e
            QtWidgets.QMessageBox.critical(self, u"错误：", u'文件未保存或文件路径中含有中文！')
            return

    def playblast_img(self):
        preview_file_name = self.file_name(with_version=True, form='.jpg')
        if preview_file_name:
            jpg_path = '/'.join([self.current_folder, preview_file_name.replace('.jpg', '')])
            new_name = core.playblast_img(jpg_path).replace('#', '0')
            self.preview_file_le.setText(new_name)
        pass

    def grab_img(self):
        preview_file_name = self.file_name(with_version=True, form='.jpg')
        if preview_file_name:
            jpg_path = '/'.join([self.current_folder, preview_file_name])
            core.grab_pic(jpg_path)
            self.preview_file_le.setText(jpg_path)

    def play_blast(self):
        preview_file_name = self.file_name(with_version=True, form='.mov')
        if preview_file_name:
            prev_path = '/'.join([self.current_folder, preview_file_name])
            result = core.playblast_mov(getpass.getuser(), prev_path)
            if result:
                self.preview_file_le.setText(prev_path)

    def set_submit_path(self):
        self.submit_path_le.setText(self.submit_path)

        pass

    def submit_files(self):
        assert core.check_topo(*[self, self.task_id, self.task_type, self.task_step, self.task_classify, self.project]), \
               'Checking topo error !'
        self.append_log(u'正在保存...')
        self.submit_pb.setEnabled(0)
        cmds.file(rename=self.project_file)
        cmds.file(save=1, f=1, type='mayaAscii')
        self.append_log(u'正在后台上传, 请不要关闭此窗口...')
        self.set_progress(0, 'ready...\n')
        ma_target_file = '/'.join([self.submit_path, self.file_name(with_version=False, form='.ma')])
        prev_target_file = '/'.join([self.submit_path, self.file_name(with_version=False, form=self.prev_file_type)])
        ma_target_file_with_version = '/'.join([self.submit_path, self.file_name(with_version=True, form='.ma')])
        prev_target_file_with_version = '/'.join(
            [self.submit_path, self.file_name(with_version=True, form=self.prev_file_type)])
        file_copy_list = [[self.project_file, ma_target_file],
                          [self.preview_file, prev_target_file],
                          [self.project_file, ma_target_file_with_version],
                          [self.preview_file, prev_target_file_with_version]
                          ]
        if self.task_step == 'fur':
            mat_local_file = self.project_file.replace('.ma', '_mat.ma')
            mat_target_file = '/'.join([self.submit_path, 'attachment',
                                        self.file_name(with_version=False, form='.ma').replace('.ma', '_mat.ma')])
            mat_target_file_with_version = '/'.join([self.submit_path, 'attachment',
                                                     self.file_name(with_version=True, form='.ma').replace('.ma',
                                                                                                           '_mat.ma')])
            export_mat_path = core.export_fur_mat(mat_local_file)
            file_copy_list.append([export_mat_path, mat_target_file])
            file_copy_list.append([export_mat_path, mat_target_file_with_version])
        folder_copy_list = [[att, self.attach_path + '/' + att.split('/')[-1]] for att in self.attachments]
        folder_copy_list.extend([[att, self.attach_no_version + '/' + att.split('/')[-1]] for att in self.attachments])
        for each in file_copy_list + folder_copy_list:
            if not each[0] or not each[1]:
                QtWidgets.QMessageBox.critical(self, u"错误：",
                                               u'信息不完整！请检查信息...')
                return
        for fld in folder_copy_list:
            file_copy_list.extend(fileIO.get_copy_list(fld[0], fld[1]))
        self.get_copy_tuples(file_copy_list)

    def get_copy_tuples(self, file_copy_list):#得到无重复的copy文件列表
        copy_tuples = []
        for ct in file_copy_list:
            if os.path.isdir(ct[0]):
                copy_tuples.extend(fileIO.get_copy_list(ct[0], ct[1]))
            if os.path.isfile(ct[0]):
                copy_tuples.append([ct[0], ct[1]])
        copy_tuples = [f for f in copy_tuples if '.db' not in f[0]]
        for i, each in enumerate(copy_tuples):
            if each[1] in self.copied:
                continue
            self.copied.append(each[1])
        self.copy_file_thread.copy_list = copy_tuples
        self.copy_file_thread.start()
        # copy = CopyFileThread(copy_tuples)
        # copy.signal.connect(self.get_copy_progress)
        # copy.finished.connect(self.finished_copy)
        # copy.start()

    def get_copy_progress(self, progress_data):
        #  progress_data: text, value
        if progress_data:
            # file_name = progress_data
            # copy_progress_num = self.__copy_progress * 100 / float(len(self.copied))
            # self.__copy_progress += 1
            # if copy_progress_num == 100:
            #     self.finished_copy(True)
            # else:
            self.set_progress(progress_data[1], progress_data[0])
            self.append_log(u'正在上传: %s' % progress_data[0])
            self.pushButton_close.setEnabled(False)

    def finished_copy(self, result):
        if result:
            self.set_progress(100, u'上传完成！正在写入shotgun...')
            self.append_log(u'文件全部拷贝完成，正在写入数据库...')
            try:
                result = self.create_version()
                if result:
                    self.set_progress(100, u'上传完成！数据写入完成！')
                    self.append_log(u'数据写入完成！现在你可以关闭窗口了。')
                    self.pushButton_close.setEnabled(True)
            except Exception as e:
                print 'error:', e
                self.set_progress(99, u'数据库写入出现问题！请联系TD！')
                self.append_log(u'数据库写入出现问题！请联系TD！')
            finally:
                self.check_pb.setEnabled(False)
                self.submit_pb.setEnabled(False)

    # def copy_file(self, source_file, target_file):
    #     QtCore.QCoreApplication.processEvents()
    #     target_dir = os.path.dirname(target_file)
    #     # print target_dir
    #     if not os.path.exists(source_file):
    #         print "Not exists: " + source_file
    #         return
    #     if not os.path.exists(target_dir):
    #         os.makedirs(target_dir)
    #     if not os.path.exists(target_file) or (
    #             os.path.exists(target_file) and (os.path.getsize(target_file) != os.path.getsize(source_file))):
    #         self.progress_lb.setText(source_file)
    #         g_s = open(source_file, 'rb')
    #         g = g_s.read()
    #         md5_source = md5(g).hexdigest()
    #         md5_target = None
    #         g_s.close()
    #         checking_time = 50
    #         # print source_file
    #         while not (md5_source == md5_target and checking_time > 0):
    #             with open(source_file, 'rb') as s:
    #                 with open(target_file, 'wb') as fd:
    #                     record_size = 10048576
    #                     size = int(os.path.getsize(os.path.abspath(source_file)) / record_size)
    #                     records = iter(partial(s.read, record_size), b'')
    #                     self.progress_bar.setValue(0)
    #                     self.append_log(u'Copy: %s to \n%s' % (source_file, target_file))
    #                     for i, data in enumerate(records):
    #                         fd.write(data)
    #                         if size:
    #                             self.progress_bar.setValue((i * 100) / size)
    #             with open(target_file, 'rb') as h_s:
    #                 h = h_s.read()
    #                 md5_target = md5(h).hexdigest()
    #             checking_time -= 10

    # def get_copy_list(self, source_dir, target_dir):
    #     if not source_dir:
    #         return []
    #     files = []
    #     for f in os.listdir(source_dir):
    #         source_file = source_dir + '/' + f
    #         target_file = target_dir + '/' + f
    #         if os.path.isfile(source_file):
    #             files.append([source_file, target_file])
    #         if os.path.isdir(source_file):
    #             files.extend(self.get_copy_list(source_file, target_file))
    #     return files

    def create_version(self):
        project_info = core.find_one_shotgun('Project', [['name', 'is', self.project]], ['id'])
        user_info = core.find_shotgun("Group",
                                      [["sg_login", "is", self.user]],
                                      ['sg_group_project', 'id', 'code'])[0]
        entity = core.find_shotgun(self.task_type,
                                   [['project', 'name_is', self.project], ['code', 'is', self.task_code]],
                                   ['code', 'id'])[0]
        sg_task = self.sg_task
        version_data = dict(project=project_info,
                            sg_path_to_movie=self.submit_path + '/' + self.file_name(with_version=True,
                                                                                     form=self.prev_file_type),
                            sg_path_to_frames=self.submit_path + '/' + self.file_name(with_version=True, form='.ma'),
                            sg_path_to_geometry=self.attach_path,
                            sg_version_number=str(self.new_version).zfill(3),
                            description=self.describe,
                            user=user_info,
                            entity=entity,
                            sg_version_type='Submit',
                            code=self.file_name(with_version=True, form='.ma').replace('.ma', ''),
                            sg_task=sg_task,
                            )
        no_num_version = version_data.copy()
        no_num_version['code'] = self.file_name(with_version=False, form='.ma').replace('.ma', '')
        no_num_version['sg_path_to_movie'] = self.submit_path + '/' + self.file_name(with_version=False,
                                                                                     form=self.prev_file_type)
        no_num_version['sg_path_to_frames'] = self.submit_path + '/' + self.file_name(with_version=False, form='.ma')
        no_num_version['sg_path_to_geometry'] = self.attach_no_version
        no_num_version['sg_version_number'] = None
        # 创建版本
        version_entity = core.create_shotgun('Version', version_data)
        no_num_version_entity_id = core.find_shotgun('Version', [['project', 'name_is', self.project],
                                                                 ['code', 'is', no_num_version['code']],
                                                                 ['sg_version_type', 'is', 'Submit']
                                                                 ],
                                                     ['id', 'code'])
        if no_num_version_entity_id:
            no_num_version_entity = core.update_shotgun('Version', no_num_version_entity_id[0]['id'], no_num_version)
        else:
            no_num_version_entity = core.create_shotgun('Version', no_num_version)
        # 上传预览图
        core.upload_shotgun("Version", version_entity['id'], self.preview_file, field_name="sg_uploaded_movie",
                            display_name=self.task_code)
        core.upload_shotgun("Version", no_num_version_entity['id'], self.preview_file, field_name="sg_uploaded_movie",
                            display_name=self.task_code)
        # 更新最新版本
        update_dict = {'sg_latestversion': str(self.new_version).zfill(3)}
        # if not self.task_step in ['ly', 'bk', 'an']:
        # update_dict.update({'sg_status_list': 'ip'})
        core.update_shotgun('Task', self.task_id, update_dict)
        # 发送通知给抄送人
        asset_adressings = self.sg_task['entity.Asset.addressings_cc'] or []
        shot_adressings = self.sg_task['entity.Shot.addressings_cc'] or []
        self.sg_task['addressings_cc'].extend(asset_adressings)
        self.sg_task['addressings_cc'].extend(shot_adressings)
        note_data = {
            "project": project_info,
            "subject": u'任务上传通知：'+self.task_name_en,
            "sg_proposer": user_info,
            "addressings_to": self.sg_task['addressings_cc'],
            "content": "用户{}已上传任务{}, 请知悉。".format(self.user, self.task_name_en),
            "sg_if_read": False,
        }
        core.create_shotgun('Note', note_data)
        return True


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = OctMayaSubmit()
    dialog.append_attachment('test')
    dialog.show()
    app.exec_()

