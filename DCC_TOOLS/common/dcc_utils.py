#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.8
# wechat : 18250844478
###################################################################

import os
import sys
import maya.cmds as cmds
import pymel.core as pm
import xml.etree.ElementTree as xml
from cStringIO import StringIO
import maya.OpenMayaUI as mui
import maya.OpenMaya as OpenMaya
try:
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    import pyside2uic as uic
except ImportError:
    import PySide.QtGui as QtWidgets
    from shiboken import wrapInstance
    import pysideuic as uic

import threading
import os
import codecs
import shutil

try:
    from maya.utils import executeInMainThreadWithResult
except ImportError:
    executeInMainThreadWithResult = None


def get_current_file_name(full_path=False, dir_path=False):
    if not pm.sceneName().dirname():
        cmds.file(save=1)
    if full_path:
        if dir_path:
            return str(pm.sceneName().dirname())
        return str(pm.sceneName().abspath()).replace('\\', '/')
    return str(pm.sceneName().basename().split(".")[0])


def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
        return form_class, base_class


def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def undoable(function):
    # A decorator that will make commands undoable in maya
    def decoratorCode(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)
        except:
            print(sys.exc_info()[1])
        finally:
            cmds.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode


class Timer(threading.Thread):
    def __init__(self, interval, function, args=[], kwargs={}, repeat=True):
        self.interval = interval
        self.function = function
        self.repeat = repeat
        self.args = args
        self.kwargs = kwargs
        self.event = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        def _mainLoop():
            self.event.wait(self.interval)
            if not self.event.isSet():
                if executeInMainThreadWithResult:
                    executeInMainThreadWithResult(self.function, *self.args, **self.kwargs)
                else:
                    self.function(*self.args, **self.kwargs)

        if self.repeat:
            while not self.event.isSet():
                _mainLoop()
        else:
            _mainLoop()
            self.stop()

    def start(self):
        self.event.clear()
        threading.Thread.start(self)

    def stop(self):
        self.event.set()
        threading.Thread.__init__(self)


def get_dcc_tools_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS.rstrip('common')
    else:
        return os.path.dirname(os.path.abspath(__file__)).rstrip('common')


def raise_warning_dialog(text):
    new_text = text
    if isinstance(text, list):
        new_text = reformat_list(text)
    warning_win = cmds.window(t=u'提示', h=30, s=1)
    cmds.columnLayout(adj=1)
    cmds.text(new_text, h=100)
    cmds.showWindow(warning_win)


def reformat_list(list):
    # 将列表进行自动换行
    if len(list) <= 1:
        return str(list)
    i = 0
    new_list_str = ''
    for _ in xrange(100):
        if list[i:(i+5)]:
            new_list_str += str(list[i:(i+5)])+'\n'
            i = i+5
        else:
            break
    return new_list_str


def get_maya_references(file_path, pattern='rfn[\S\s]*-typ'):
    data = list()
    # str_format = re.compile(pattern)
    with codecs.open(file_path, 'r', 'gbk') as ma:
        for line in ma.readlines():
            if line.count('requires'):
                break
            if ':' in line and 'RN' in line:
            # if str_format.search(line):
                data.append(line.split('-rfn')[1].split("\"")[1])
    return data


def get_double_namespaces(ref_data):
    double_names = [data for data in ref_data if ":" in data]
    double_names_dict = {}
    for each in double_names:
        double_names_dict[each] = each.split(':')[-1]
    return double_names_dict


def fix_double_namespaces(file_path):

    ref_data = get_maya_references(file_path)
    if not ref_data:
        return
    double_data = get_double_namespaces(ref_data)
    print double_data
    if os.path.isfile(file_path):
        with codecs.open(file_path, 'r', encoding='gbk') as (f):
            file_content = f.read()
        file_context = file_content
        for k, v in double_data.iteritems():
            file_context = file_context.replace(k, v)
        old_file_path = file_path.replace('.ma', '_dirty.ma')
        shutil.copy2(file_path, old_file_path)
        with codecs.open(file_path, 'w', encoding='gbk') as nf:
            nf.write(file_context)
    return True


def get_all_mesh_transform():
    return [each.getParent() for each in pm.ls(type='mesh')]


def get_geometry_md5(geometry):
    '''
    '''
    import md5, StringIO

    io = StringIO.StringIO()
    dag_path = OpenMaya.MDagPath.getAPathTo(geometry)

    iterator = OpenMaya.MItMeshVertex(dag_path)
    face_list = OpenMaya.MIntArray()
    while not iterator.isDone():
        iterator.getConnectedFaces(face_list)
        io.write('{0} {1}\n'.format(iterator.index(), ' '.join(sorted([str(i) for i in face_list]))))
        iterator.next()

    _md5 = md5.new()
    _md5.update(io.getvalue())
    return _md5.hexdigest()


def get_hierarchy_data(ignore_hide_objects=False):
    '''
    '''
    data = dict()

    model_high_grp = pm.ls('|*|Geometry|high')
    if not model_high_grp:
        return data

    iterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kTransform)
    iterator.reset(model_high_grp[0].__apiobject__())

    while not iterator.isDone():
        if OpenMaya.MFnDagNode(iterator.currentItem()).childCount() == 0:
            iterator.next()
            continue

        shape_0 = OpenMaya.MFnDagNode(iterator.currentItem()).child(0)
        if shape_0.apiType() != OpenMaya.MFn.kMesh:
            iterator.next()
            continue

        if ignore_hide_objects and not OpenMaya.MDagPath.getAPathTo(shape_0).isVisible():
            iterator.next()
            continue

        try:
            geo_md5 = get_geometry_md5(iterator.currentItem())
        except:
            geo_md5 = '0' * 32
        data[iterator.fullPathName()] = geo_md5
        iterator.next()

    return data


def comparison_md5(sg_topo_data, file_topo_data):
    import json
    #  对比shotgun上的MD5值跟文件的MD5值
    sg_topo_data = json.loads(sg_topo_data)
    no_match_geo = list()
    for geo, topo_value in file_topo_data.iteritems():
        if topo_value != sg_topo_data.get(geo):
            no_match_geo.append(geo)

    return no_match_geo