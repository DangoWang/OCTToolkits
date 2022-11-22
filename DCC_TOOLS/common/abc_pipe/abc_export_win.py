# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds
from DCC_TOOLS.common import dcc_utils
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import time
import os
import utils.shotgun_operations as sg

_win = "abc_export_win_ui"

class abc_export_win_class(QtWidgets.QMainWindow):
    def __init__(self, parent=dcc_utils.getMayaWindow()):
        super(abc_export_win_class, self).__init__(parent)
        self.setWindowTitle(u"导出ABC")
        self.setObjectName(_win)
        self.resize(200, 264)

        self.centralwidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.comboBox_task = QtWidgets.QComboBox(self.centralwidget)
        self.gridLayout.addWidget(self.comboBox_task, 0, 0, 1, 1)
        # self.verticalLayout.addWidget(self.comboBox_task)
        user = sg.get_user()
        project = sg.get_project()
        self.task_list = sg.get_tasks(project, user)
        # print self.task_list
        name_task_list = self.task_list.keys()
        name_task_list.sort()
        self.comboBox_task.addItems(name_task_list)

        self.pushButton_task = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_task.clicked.connect(self.set_task)
        self.pushButton_task.setText(u"设置任务")
        self.gridLayout.addWidget(self.pushButton_task, 1, 0, 1, 1)

        # self.label_scene = QtWidgets.QLabel()
        # self.label_scene.setText('场次：')
        # self.gridLayout.addWidget(self.label_scene, 0, 0, 1, 1)
        # self.comboBox_scene = QtWidgets.QComboBox()
        # self.gridLayout.addWidget(self.comboBox_scene, 1, 0, 1, 1)
        #
        # # shot
        # self.label_shot = QtWidgets.QLabel()
        # self.label_shot.setText(u'镜号：')
        # self.gridLayout.addWidget(self.label_shot, 2, 0, 1, 1)
        # self.comboBox_shot = QtWidgets.QComboBox()
        # self.comboBox_shot.setMinimumSize(QtCore.QSize(80, 0))
        # self.gridLayout.addWidget(self.comboBox_shot, 3, 0, 1, 1)
        #
        # self.label_fromgroup = QtWidgets.QLabel()
        # self.label_fromgroup.setText(u'来源环节：')
        # self.gridLayout.addWidget(self.label_fromgroup, 4, 0, 1, 1)
        # self.comboBox_fromgroup = QtWidgets.QComboBox()
        # self.comboBox_fromgroup.setMinimumSize(QtCore.QSize(66, 0))
        # self.comboBox_fromgroup.setObjectName("comboBox_fromgroup")
        # self.gridLayout.addWidget(self.comboBox_fromgroup, 5, 0, 1, 1)

        self.label_ver = QtWidgets.QLabel()
        self.label_ver.setText(u'版本：')
        self.gridLayout.addWidget(self.label_ver, 6, 0, 1, 1)
        self.comboBox_ver = QtWidgets.QComboBox()
        self.comboBox_ver.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBox_ver.setObjectName("comboBox_ver")
        self.gridLayout.addWidget(self.comboBox_ver, 7, 0, 1, 1)



        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.node_list = QtWidgets.QVBoxLayout()
        self.verticalLayout.addLayout(self.node_list)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 8, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText(u"DoIt")
        self.gridLayout.addWidget(self.pushButton, 9, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.refresh_reference_node_list()
        self.pushButton.clicked.connect(self.abc_out)

        # self.comboBox_scene.currentTextChanged.connect(self.refresh_shot_list)
        # self.comboBox_shot.currentTextChanged.connect(self.refresh_task_list)
        # self.comboBox_fromgroup.currentTextChanged.connect(self.refresh_version_list)

        # self.refresh_scene_list()
        # self.refresh_version_list()

    def set_task(self):
        sel_task = self.comboBox_task.currentText()
        task_id = self.task_list[sel_task]["id"]
        self.refresh_version_list(task_id)

    def get_scene_list(self):
        filters = [['project', 'name_is', 'DSF']]
        fields = ['code']
        scene_list = sg.find_shotgun('Sequence', filters, fields) or []
        result = []
        for scene in scene_list:
            result.append(scene['code'])
        return sorted(result)

    def refresh_scene_list(self):
        self.comboBox_scene.clear()
        self.comboBox_scene.addItems(self.get_scene_list())

    def get_shots_by_scene(self, scene_num):
        filters = [['project', 'name_is', 'DSF'],
                   ['sg_sequence', 'name_is', scene_num]]
        fields = ['code']
        shot_list = sg.find_shotgun('Shot', filters, fields) or []
        result = []
        for shot in shot_list:
            result.append(shot['code'])
        return sorted(result)

    def refresh_shot_list(self):
        scene_num = self.comboBox_scene.currentText()
        self.comboBox_shot.clear()
        if scene_num:
            self.comboBox_shot.addItems(self.get_shots_by_scene(scene_num))

    def get_tasks_by_shot(self, shot_num):
        filters = [['project', 'name_is', 'DSF'],
                   ['entity.Shot.code', 'contains', shot_num]]
        fields = ['content']
        task_list = sg.find_shotgun('Task', filters, fields) or []
        result = []
        self.task_dir = {}
        for task in task_list:
            if task['content'] in result:
                continue
            result.append(task['content'])
            self.task_dir[task['content']] = task
        return sorted(result)

    def refresh_task_list(self):
        shot_num = self.comboBox_shot.currentText()
        self.comboBox_fromgroup.clear()
        if shot_num:
            self.comboBox_fromgroup.addItems(self.get_tasks_by_shot(shot_num))

    def get_version_by_task(self, task_name):
        self.version_dir = {}
        task_name = self.comboBox_fromgroup.currentText()
        task = self.task_dir[task_name]
        filters = [['project', 'name_is', 'DSF'],
                   ['sg_task.Task.id', 'is', task['id']]
                   ]#, ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['code', 'sg_task.Task.id']
        self.version_list = sg.find_shotgun('Version', filters, fields) or []
        for version in self.version_list:
            self.version_dir[version["code"]] = version

    def get_version_by_task_id(self, task_id):
        # from DCC_TOOLS.common.work_log import open_close_event
        # task_id = open_close_event.task_info.task
        self.version_dir = {}
        if not task_id:
            return
        filters = [['project', 'name_is', 'DSF'],
                   ['sg_task.Task.id', 'is', task_id]
                   ]#, ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['code', 'sg_task', "entity.Shot.sg_sequence", "entity"]
        self.version_list = sg.find_shotgun('Version', filters, fields) or []
        for version in self.version_list:
            self.version_dir[version["code"]] = version

    def refresh_version_list(self, task_id):
        # task_name = self.comboBox_fromgroup.currentText()
        # self.comboBox_ver.clear()
        # if task_name:
        #     self.get_version_by_task(task_name)
        self.get_version_by_task_id(task_id)
        self.comboBox_ver.clear()
        self.comboBox_ver.addItems(sorted(self.version_dir.keys(), reverse=1))


    def refresh_reference_node_list(self, *args):
        reference_list = cmds.ls(references=1) or []
        self.node_dir = {}
        for node in reference_list:
            print node
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            checkBox.setText(node)
            self.node_list.addWidget(checkBox)
            self.node_dir[node] = checkBox

    def abc_out(self, *args):
        frame_st = cmds.playbackOptions(q=1, animationStartTime=1)
        frame_en = cmds.playbackOptions(q=1, animationEndTime=1)
        ver_name = self.comboBox_ver.currentText()
        if not ver_name:
            return
        shot_version = self.version_dir[ver_name]
        # print shot_version
        # get current file name
        current_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # mfile = om.MFileIO()
        # current_file = mfile.currentFile()
        if not cmds.pluginInfo('AbcExport', query=1, loaded=1):
            try:
                cmds.loadPlugin('AbcExport.mll')
            except RuntimeError:
                return
        # if not current_file:
        #     return
        # get task name
        # task_name = get_task_name(current_file)
        task_name = shot_version["sg_task"]["name"]
        # # get scene name
        # scene_name = get_scene_name(current_file)
        scene_name = shot_version["entity.Shot.sg_sequence"]["name"]
        #
        # # get shot name
        # shot_name = get_shot_name(current_file)
        shot_name = shot_version["entity"]["name"]
        # shot_version = get_shot_version(current_file)

        # get reference  node list
        reference_list = cmds.ls(references=1) or []
        abc_path_convention = sg.find_one_shotgun('CustomEntity01',
                                                  [['project', 'name_is', sg.get_project()], ['sg_type', 'is', 'Shot'],
                                                   ['sg_upload_type', 'is', 'Publish']],
                                                  ['sg_cache_path', 'sg_pattern'])
        cache_path_pattern = '/'.join([abc_path_convention['sg_pattern'], abc_path_convention['sg_cache_path']])

        for node, widget in self.node_dir.items():
            if not widget.isChecked():
                continue
            try:
                # get reference file path
                file_path = cmds.referenceQuery(node, filename=1, unresolvedName=1, withoutCopyNumber=1)
            except Exception as e:
                # print str(e)

                continue
            # get reference namespace
            namespace = cmds.referenceQuery(node, namespace=1)
            if namespace.count(":") != 1:
                continue
            namespace = cmds.referenceQuery(node, namespace=1, shortName=1)
            # get asset id
            asset_id = get_asset_id(file_path)
            print "asset_id", asset_id
            if not asset_id:
                continue
            # get asset node
            asset_node = get_asset_node(asset_id)
            if not asset_node:

                continue

            yeti_list = []
            try:
                yeti_list = cmds.ls("{}:*".format(namespace), type="pgYetiMaya")
            except Exception as e:
                print(str(e))
            if yeti_list:
                # test path
                # fur_path = "D:/test/Shot/{task_name}/{scene}/{shot}/cache/{cache_type}/{namespace}/{cache_version}".format(
                #     step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name)+1:], cache_type="fur", namespace=namespace, cache_version=current_time
                # )
                cache_folder_pattern = ('/'.join(cache_path_pattern.split('/')[:-1])).format(step_code=task_name,
                                                                                             scene=scene_name,
                                                                                             shot=shot_name[
                                                                                                  len(scene_name) + 1:],
                                                                                             cache_type="fur",
                                                                                             namespace=namespace,
                                                                                             cache_version=current_time)

                if not os.path.isdir(cache_folder_pattern):
                    try:
                        os.makedirs(cache_folder_pattern)
                    except Exception as e:

                        # print "can't make folder for abc"
                        # print str(e)
                        continue

                for yeti_node in yeti_list:
                    fur_full_path = cache_path_pattern.format(step_code=task_name, scene=scene_name,
                                                         shot=shot_name[len(scene_name) + 1:], cache_type="fur",
                                                         namespace=namespace,
                                                         cache_version=current_time,
                                                         cache_name=yeti_node.split(':')[-1] + '.%04d')

                    # fur_full_path = "{}/{}.%04d.fur".format(fur_path, yeti_node.split(':')[-1])
                    print( fur_full_path )
                    mel.eval('pgYetiCommand -writeCache "{}" -range {} {} -samples 1 -updateViewport 0 -generatePreview 0 {};'.format(fur_full_path, frame_st, frame_en, yeti_node))

                    sg.create_shotgun("CustomEntity03", {'code': namespace,
                                                              'sg_cache_type': 'fur',
                                                              'sg_asset': asset_node,
                                                              'sg_namespace': namespace,
                                                              'sg_shot_version': shot_version,
                                                              'sg_version': current_time,
                                                              'project': {u'id': 89, u'type': u'Project'},
                                                              'sg_cache_path': fur_full_path,
                                                              'sg_obj_list': yeti_node})
                continue


            abc_full_path = cache_path_pattern.format(
                step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name) + 1:], cache_type="abc",
                namespace=namespace, cache_version=current_time, cache_name=namespace)
            abc_folder = '/'.join(abc_full_path.split('/')[:-1])
            # abc_path = "D:/test/Shot/{task_name}/{scene}/{shot}/cache/{cache_type}/{namespace}/{cache_version}".format(
            #     step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name)+1:], cache_type="abc", namespace=namespace, cache_version=current_time
            # )
            if not os.path.isdir(abc_folder):
                try:
                    os.makedirs(abc_folder)
                except Exception as e:

                    # print "can't make folder for abc"
                    # print str(e)
                    continue
            # abc_full_path = "{cache_path}/{cache_name}.{cache_type}".format( cache_path=abc_path, cache_name=namespace, cache_type="abc")
            # print "abc_full_path: ", abc_full_path
            high_node = None
            high_node_list = cmds.ls("{}:high".format(namespace), long=1) or []
            if high_node_list.__len__() == 1:
                high_node = high_node_list[0]
            else:
                for h_n in high_node_list:
                    if "Geometry" in h_n:
                        high_node = h_n
            # high_node = "{}:high".format(namespace)
            # if not cmds.objExists(high_node):
            #     continue
            if not high_node:
                continue

            obj_list = []
            mesh_list = cmds.listRelatives(high_node, allDescendents=1, type='mesh', fullPath=1)
            tran_list = cmds.listRelatives(mesh_list, parent=1, fullPath=1)
            tran_list = list(set(tran_list))
            for tran in tran_list:
                if is_visibility(tran):
                    obj_list.append(tran)
            if not obj_list:

                continue
            # print obj_list
            frame_st = cmds.playbackOptions(q=1, animationStartTime=1)
            frame_en = cmds.playbackOptions(q=1, animationEndTime=1)

            abc_job_arg = '-frameRange {} {} -worldSpace -writeVisibility -stripNamespaces -dataFormat ogawa'.format(frame_st, frame_en)
            for obj in obj_list:
                abc_job_arg = '{} -root {}'.format(abc_job_arg, obj)
            abc_job_arg = '{} -file {}'.format(abc_job_arg, abc_full_path)
            # print abc_full_path
            # cmds.AbcExport(j="-frameRange {} {} -worldSpace -dataFormat ogawa -root {} -file {}".format(frame_st, frame_en, high_node, abc_full_path))
            cmds.AbcExport(j=abc_job_arg)
            # create shotgun node for cache
            sg.create_shotgun("CustomEntity03", {'code': namespace,
                                            'sg_cache_type': 'abc',
                                            'sg_asset': asset_node,
                                            'sg_namespace': namespace,
                                            'sg_shot_version': shot_version,
                                            'sg_version': current_time,
                                            'project': {u'id': 89, u'type': u'Project'},
                                            'sg_cache_path': abc_full_path,
                                            'sg_obj_list': ';'.join(obj_list)})
            # yeti_list = []
            # try:
            #     yeti_list = cmds.ls("{}:*".format(namespace), type="pgYetiMaya")
            # except Exception as e:
            #     print(str(e))
            # if not yeti_list:
            #     continue
            #
            # # test path
            # # fur_path = "D:/test/Shot/{task_name}/{scene}/{shot}/cache/{cache_type}/{namespace}/{cache_version}".format(
            # #     step_code=task_name, scene=scene_name, shot=shot_name[len(scene_name)+1:], cache_type="fur", namespace=namespace, cache_version=current_time
            # # )
            # cache_folder_pattern = ('/'.join(cache_path_pattern.split('/')[:-1])).format(step_code=task_name,
            #                                                                              scene=scene_name,
            #                                                                              shot=shot_name[
            #                                                                                   len(scene_name) + 1:],
            #                                                                              cache_type="fur",
            #                                                                              namespace=namespace,
            #                                                                              cache_version=current_time)
            #
            # if not os.path.isdir(cache_folder_pattern):
            #     try:
            #         os.makedirs(cache_folder_pattern)
            #     except Exception as e:
            #
            #         # print "can't make folder for abc"
            #         # print str(e)
            #         continue
            #
            # for yeti_node in yeti_list:
            #     fur_full_path = cache_path_pattern.format(step_code=task_name, scene=scene_name,
            #                                          shot=shot_name[len(scene_name) + 1:], cache_type="fur",
            #                                          namespace=namespace,
            #                                          cache_version=current_time,
            #                                          cache_name=yeti_node.split(':')[-1] + '.%04d')
            #
            #     # fur_full_path = "{}/{}.%04d.fur".format(fur_path, yeti_node.split(':')[-1])
            #     print( fur_full_path )
            #     mel.eval('pgYetiCommand -writeCache "{}" -range {} {} -samples 1 -updateViewport 0 -generatePreview 0 {};'.format(fur_full_path, frame_st, frame_en, yeti_node))
            #
            #     sg.create_shotgun("CustomEntity03", {'code': namespace,
            #                                               'sg_cache_type': 'fur',
            #                                               'sg_asset': asset_node,
            #                                               'sg_namespace': namespace,
            #                                               'sg_shot_version': shot_version,
            #                                               'sg_version': current_time,
            #                                               'project': {u'id': 89, u'type': u'Project'},
            #                                               'sg_cache_path': fur_full_path,
            #                                               'sg_obj_list': yeti_node})
            widget.setChecked(0)


# get asset id by file path
def get_asset_id(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path],
        ['entity.Asset.sg_asset_type', 'is_not', 'ENV']]
    fields = ["entity.Asset.id"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity.Asset.id"]:
                return version["entity.Asset.id"]
        return None
    else:
        return None

# get asset node by asset id
def get_asset_node(id, *args):
    filters = [
        ['id', 'is', id]]
    fields = []
    asset_list = sg.find_shotgun('Asset', filters, fields)
    if asset_list:
        return asset_list[0]
    else:
        return None

# get task name by file path
def get_task_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["sg_task.Task.content"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["sg_task.Task.content"]:
                return version["sg_task.Task.content"]
        return None
    else:
        return None

def get_scene_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["entity.Shot.sg_sequence"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity.Shot.sg_sequence"]["name"]:
                return version["entity.Shot.sg_sequence"]["name"]
        return None
    else:
        return None

def get_shot_name(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = ["entity"]
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version["entity"]["name"]:
                return version["entity"]["name"]
        return None
    else:
        return None

def get_shot_version(file_path, *args):
    filters = [
        ['sg_path_to_frames', 'is', file_path]]
    fields = []
    version_list = sg.find_shotgun('Version', filters, fields)
    if version_list:
        for version in version_list:
            if version:
                return version
        return None
    else:
        return None

# get visibility
def is_visibility(obj):
    obj_visibility = cmds.getAttr('{}.visibility'.format(obj))
    if not obj_visibility:
        return obj_visibility
    parent_list = cmds.listRelatives(obj, parent=1, fullPath=1) or []
    if not parent_list:
        return obj_visibility
    else:
        parent_visibility = cmds.getAttr('{}.visibility'.format(parent_list[0]))
        if not parent_visibility:
            return parent_visibility
        else:
            return is_visibility(parent_list[0])

def get_cam(*args):
    cam_list = cmds.ls("CAM")
    if cam_list.__len__() != 1:
        return
    cam_shape_list = cmds.listRelatives(ad=1, typ="camera")
    if cam_shape_list.__len__() != 1:
        return
    return cam_list[0]






def main():
    if cmds.window(_win, exists=1):
        cmds.deleteUI(_win)
    win = abc_export_win_class()
    win.show()

if __name__ == "__main__":
    main()
