# -*- coding: utf-8 -*-

import hou
from PySide2 import QtCore, QtGui, QtWidgets
import utils.shotgun_operations as sg
from functools import partial

_win = "abc_input_win_ui"

class abc_input_win_class(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(abc_input_win_class, self).__init__(parent)
        self.setObjectName(_win)
        self.resize(666, 333)
        self.setWindowTitle(u'ABC 缓存加载（十月文化）')
        # main layout
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout_01 = QtWidgets.QHBoxLayout()

        # scene
        self.label_scene = QtWidgets.QLabel()
        self.label_scene.setText('场次：')
        self.horizontalLayout_01.addWidget(self.label_scene)
        self.comboBox_scene = QtWidgets.QComboBox()
        self.horizontalLayout_01.addWidget(self.comboBox_scene)

        # shot
        self.label_shot = QtWidgets.QLabel()
        self.label_shot.setText(u'镜号：')
        self.horizontalLayout_01.addWidget(self.label_shot)
        self.comboBox_shot = QtWidgets.QComboBox()
        self.comboBox_shot.setMinimumSize(QtCore.QSize(80, 0))
        self.horizontalLayout_01.addWidget(self.comboBox_shot)

        self.label_fromgroup = QtWidgets.QLabel()
        self.label_fromgroup.setText(u'来源环节：')
        self.horizontalLayout_01.addWidget(self.label_fromgroup)
        self.comboBox_fromgroup = QtWidgets.QComboBox()
        self.comboBox_fromgroup.setMinimumSize(QtCore.QSize(66, 0))
        self.comboBox_fromgroup.setObjectName("comboBox_fromgroup")
        self.horizontalLayout_01.addWidget(self.comboBox_fromgroup)

        self.label_ver = QtWidgets.QLabel()
        self.label_ver.setText(u'版本：')
        self.horizontalLayout_01.addWidget(self.label_ver)
        self.comboBox_ver = QtWidgets.QComboBox()
        self.comboBox_ver.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBox_ver.setObjectName("comboBox_ver")
        self.horizontalLayout_01.addWidget(self.comboBox_ver)
        spacerItem_02 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_01.addItem(spacerItem_02)
        self.verticalLayout.addLayout(self.horizontalLayout_01)

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.header().setVisible(True)
        self.treeWidget.headerItem().setText(0, u'资产名字')
        self.treeWidget.headerItem().setText(1, u'名字空间')
        self.treeWidget.headerItem().setText(2, u'目标任务')
        self.treeWidget.headerItem().setText(3, u'导入缓存')
        self.treeWidget.headerItem().setText(4, u'缓存版本')
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.verticalLayout.addWidget(self.treeWidget)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText('assemble')
        self.verticalLayout.addWidget(self.pushButton)

        # self.progressBar = QtWidgets.QProgressBar()
        # self.progressBar.setProperty("value", 0)
        # self.verticalLayout.addWidget(self.progressBar)
        self.comboBox_scene.currentTextChanged.connect(self.refresh_shot_list)
        self.comboBox_shot.currentTextChanged.connect(self.refresh_task_list)
        self.comboBox_fromgroup.currentTextChanged.connect(self.refresh_version_list)
        self.comboBox_ver.currentTextChanged.connect(self.refresh_cache_list)
        self.pushButton.clicked.connect(self.todo_input_abc)
        self.task_dir = {}
        self.version_list = []
        self.version_dir = {}
        self.refresh_scene_list()

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
        version_id_list = []
        for version in self.version_list:
            version_id_list.append(version['id'])
        if not version_id_list:
            return
        filters = [['project', 'name_is', 'DSF'],
                   ['sg_shot_version.Version.id', 'in', version_id_list]
                   ]#, ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['code', 'sg_shot_version']
        cache_list = sg.find_shotgun('CustomEntity03', filters, fields) or []
        if not cache_list:
            return
        for cache in cache_list:
            if cache['sg_shot_version']['name'] not in self.version_dir.keys():
                self.version_dir[cache['sg_shot_version']['name']] = []
            self.version_dir[cache['sg_shot_version']['name']].append(cache['id'])

    def refresh_version_list(self):
        task_name = self.comboBox_fromgroup.currentText()
        self.comboBox_ver.clear()
        if task_name:
            self.get_version_by_task(task_name)
        self.comboBox_ver.addItems(sorted(self.version_dir.keys(), reverse=1))
        # self.comboBox_ver.addItems(self.get_version_by_task(from_num))

    def refresh_cache_list(self):
        self.treeWidget.clear()
        version_num = self.comboBox_ver.currentText()
        if not version_num:
            return
        filters = [['project', 'name_is', 'DSF'],
                   ['id', 'in', self.version_dir[version_num]],
                   # ["sg_cache_type", "is", "abc"],
                   ["sg_cache_type", "is", "abc"]
                   ]#, ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['sg_namespace', 'sg_version', 'sg_asset', "sg_cache_type"]
        cache_list = sg.find_shotgun('CustomEntity03', filters, fields) or []
        if not cache_list:
            return
        reference_dir = {}
        for cache in cache_list:
            if not reference_dir.has_key(cache['sg_namespace']):
                reference_dir[cache['sg_namespace']] = cache
            else:
                if cache['sg_version'] > reference_dir[cache['sg_namespace']]['sg_version']:
                    reference_dir[cache['sg_namespace']] = cache
        self.create_reference_list(reference_dir)

    def create_reference_list(self, reference_dir):
        for key, value in reference_dir.items():
            # print key, value
            # 资产名字 名字空间 目标任务 导入缓存 缓存版本 目标 导入 id
            item_ref = QtWidgets.QTreeWidgetItem(self.treeWidget)

            # 资产名字
            cam = 0
            try:
                item_ref.setText(0, value['sg_asset']['name'])
            except:
                item_ref.setText(0, "CAM")

            # 名字空间
            item_ref.setText(1, key)

            # 目标资产
            # comboBox = QtWidgets.QComboBox(self.treeWidget)
            # self.treeWidget.setItemWidget(item_ref, 2, comboBox)
            # task_list = sg.find_shotgun('Task', [['project', 'name_is', 'DSF'], ['entity.Asset.code', 'is', value['sg_asset']['name']]], ['content'])
            # if task_list:
            #     item_ref.setText(5, task_list[0]['content'])
            # for task in task_list:
            #     comboBox.addItem(task['content'])
            # comboBox.currentTextChanged.connect(partial(self.combo_box_change, comboBox, item_ref))

            # 判断导入
            checkBox = QtWidgets.QCheckBox(self.treeWidget)
            checkBox.setChecked(1)
            checkBox.clicked.connect(partial(self.check_box_cick, checkBox, item_ref))
            self.treeWidget.setItemWidget(item_ref, 3, checkBox)
            item_ref.setText(6, '1')

            # 版本信息
            version = QtWidgets.QLabel(self.treeWidget)
            version.setText(value['sg_version'])
            self.treeWidget.setItemWidget(item_ref,4, version)

            # 缓存id
            item_ref.setText(7, str(value['id']))

            item_ref.setText(8, value["sg_cache_type"])

    def check_box_cick(self, box, item, *args):
        if box.isChecked():
            item.setText(6, '1')
        else:
            item.setText(6, '')

    def combo_box_change(self, box, item, *args):
        current = box.currentText()
        item.setText(5, current)

    def todo_input_abc(self):
        ref_num = self.treeWidget.topLevelItemCount()
        if not ref_num:
            return
        input_cam = 1
        cache_dir = {}
        for i in range(ref_num):
            # 是否导入
            if self.treeWidget.topLevelItem(i).text(6):
                cache_type = self.treeWidget.topLevelItem(i).text(8)
                namespace = self.treeWidget.topLevelItem(i).text(1)
                cache_id = int(self.treeWidget.topLevelItem(i).text(7))
                cache_path = self.get_cache_path_by_cache_id(cache_id)
                # print cache_type, namespace, cache_id,cache_path
                if cache_type == "fur":
                    continue
                elif cache_type=="abc":
                    # print cache_path
                    cache_dir[namespace] = cache_path
        num = 0
        if not cache_dir:
            return
        node_obj = hou.node("/obj")
        node_geo = node_obj.createNode("geo", "loader", run_init_scripts=False)
        node_merge = node_geo.createNode("merge")
        for name_node, cache_path in cache_dir.items():
            node_abc = node_geo.createNode('alembic')
            node_abc.parm('fileName').set(cache_path)
            node_abc.setName(name_node)
            node_abc.moveToGoodPosition()
            node_merge.setInput(num, node_abc, 0)
            num += 1
        node_merge.moveToGoodPosition()
        print u"Import finished, please continue"


    def get_fur_mat_by_asset_name(self, asset_name, *args):
        filters = [['project', 'name_is', 'DSF'],
                   ['entity.Asset.code', 'is', asset_name],
                   ['step', 'name_is', 'Fur']]
        fields = []
        task_list = sg.find_shotgun('Task', filters, fields)
        if not task_list:
            return
        return task_list[0]

    def get_fur_cahce_by_id(self, cache_id):
        fur_filters = [['project', 'name_is', 'DSF'],
                       ['id', 'is', cache_id]]
        new_fields = ['sg_namespace', "sg_cache_path", "sg_obj_list"]
        fur_cache = sg.find_one_shotgun('CustomEntity03', fur_filters, new_fields)
        return fur_cache

    def get_cam_by_abc(self, cache_id):
        filters = [['project', 'name_is', 'DSF'],
            ['id', 'is', cache_id]
            ]
        fields = ['sg_version', "sg_shot_version", "project"]
        abc_cache = sg.find_shotgun('CustomEntity03', filters, fields)[0]

        fur_filters = [['project', 'name_is', 'DSF'],
                       ["sg_cache_type", "is", "abc"],
                       ['sg_version', 'is', abc_cache['sg_version']],
                       ['sg_shot_version', 'is', abc_cache['sg_shot_version']],
                       ['sg_obj_list', 'is', 'CAM'],
                       ['sg_namespace', 'is', 'CAM'],
                       ['code', 'is', 'CAM']
                       ]
        new_fields = ["sg_cache_path"]
        fur_cache = sg.find_shotgun('CustomEntity03', fur_filters, new_fields)
        return fur_cache

    def get_fur_list_by_abc(self, cache_id):
        filters = [['project', 'name_is', 'DSF'],
            ['id', 'is', cache_id]
            ]
        fields = ['sg_version', "sg_asset", "sg_shot_version", "project"]
        abc_cache = sg.find_shotgun('CustomEntity03', filters, fields)[0]

        fur_filters = [['project', 'name_is', 'DSF'],
                       ["sg_cache_type", "is", "fur"],
                       ['sg_version', 'is', abc_cache['sg_version']],
                       ['sg_asset', 'is', abc_cache['sg_asset']],
                       ['sg_shot_version', 'is', abc_cache['sg_shot_version']]
                       ]
        new_fields = ['sg_namespace', "sg_cache_path", "sg_obj_list"]
        fur_cache = sg.find_shotgun('CustomEntity03', fur_filters, new_fields)
        return fur_cache

    def get_cache_path_by_cache_id(self, cache_id):
        filters = [['project', 'name_is', 'DSF'],
                   ['id', 'is', cache_id]
                   ]  # , ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['sg_cache_path']
        cache_path = sg.find_shotgun('CustomEntity03', filters, fields)[0]
        return cache_path['sg_cache_path']

    def get_obj_list_by_cache_id(self, cache_id):
        filters = [['project', 'name_is', 'DSF'],
                   ['id', 'is', cache_id]
                   ]  # , ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['sg_obj_list']
        obj_list = sg.find_shotgun('CustomEntity03', filters, fields)[0]
        return obj_list['sg_obj_list'].split(';')

    def get_file_by_cache_id(self, cache_id, task_name, *args):
        filters = [['project', 'name_is', 'DSF'],
                   ['id', 'is', cache_id]
                   ]  # , ['sg_version_type', 'is', 'Publish']['entity.Task.id', 'is', task['id']
        fields = ['sg_namespace', 'sg_version', 'sg_asset']
        cache = sg.find_shotgun('CustomEntity03', filters, fields)[0]
        asset = cache['sg_asset']
        task_list = sg.find_shotgun('Task', [['project', 'name_is', 'DSF'], ['entity.Asset.id', 'is', asset['id']]], ['content'])
        # 获取任务ID
        task_id = None
        for task in task_list:
            if task['content'] == task_name:
                task_id = task['id']
                break
        latest_version = self.get_latest_version('DSF', task_id)
        reference_path = self.get_path_to_frames('DSF', task_id, latest_version)
        return reference_path

    def get_latest_version(self, project_name, task_id):
        filters = [
            ['project', 'name_is', project_name],
            ['id', 'is', task_id]
        ]
        fields = ['sg_publish_version']
        taskdetail = sg.find_shotgun('Task', filters, fields)
        if taskdetail:
            if taskdetail[0]['sg_publish_version']:
                return taskdetail[0]['sg_publish_version']
            else:
                return 0
        else:
            return 0

    def get_path_to_frames(self, project_name, task_id, version):
        filters = [
            ['project', 'name_is', project_name],
            ['sg_task.Task.id', 'is', task_id],
            ['sg_version_number', 'is', version],
            ['sg_version_type', 'is', 'Publish']]
        fields = ["sg_path_to_frames"]
        taskdetail = sg.find_shotgun('Version', filters, fields)
        if taskdetail:
            if taskdetail[0]['sg_path_to_frames']:
                return taskdetail[0]['sg_path_to_frames']
            else:
                return ""
        else:
            return ""


def main():
    win = abc_input_win_class()
    win.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    win.show()
