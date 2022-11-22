#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.7
# wechat : 18250844478
###################################################################
import datetime
import shutil

from dayu_widgets.qt import *
import subprocess
import os
from config import GLOBAL
from functools import wraps
from collections import OrderedDict
import gc
# 将嵌套列表展开
def flat(list_):
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return filter(None, res)


#  更改字典的编码
def change_dict_encoding(input_dict, encoding='gbk'):
    if isinstance(input_dict, dict):
        return {change_dict_encoding(key): change_dict_encoding(value) for key, value in input_dict.iteritems()}
    elif isinstance(input_dict, list):
        return [change_dict_encoding(element) for element in input_dict]
    elif isinstance(input_dict, unicode):
        return input_dict.encode(encoding)
    else:
        return input_dict


#  获取widget的最上层parent控件
def get_widget_top_parent(widget):
    if not widget.parent():
        return widget
    return get_widget_top_parent(widget.parent())


def grab_pic(jpg_fullpath):
    clipboard = QApplication.clipboard()
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    else:
        startupinfo = None
    scrab_exe = GLOBAL.CURRENTPATH+'/bin/capture/PrScrn.dll'
    exe_path = GLOBAL.CURRENTPATH if os.path.isfile(scrab_exe) else GLOBAL.CURRENTSCRIPTPATH
    if not os.path.isfile(scrab_exe):
        scrab_exe = GLOBAL.CURRENTSCRIPTPATH + '/bin/capture/PrScrn.dll'
    try:
        new_scrab_exe = scrab_exe.replace(exe_path, get_documents())
        if not os.path.isdir(os.path.dirname(new_scrab_exe)):
            os.makedirs(os.path.dirname(new_scrab_exe))
        shutil.copyfile(scrab_exe, new_scrab_exe)
        scrab_exe = new_scrab_exe
    except:
        pass
    print 'starting...', scrab_exe
    grab = subprocess.Popen('rundll32.exe '+scrab_exe+' ,PrScrn', startupinfo=startupinfo)
    grab.wait()
    dataImage = clipboard.pixmap()
    dataImage.save(jpg_fullpath)
    if os.path.isfile(jpg_fullpath):
        return jpg_fullpath
    return ''


def get_documents():
    try:
        import ctypes
        from ctypes.wintypes import MAX_PATH
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            return buf.value
        else:
            return 'D:/'
    except:
        return 'D:/'


def func_cache(maxsize=50, memory_time=1):
    '''
    :param maxsize: 最大存储个数
    :param memory_time: 记忆时间
    :return:
    '''
    def cache_decorator(fn):
        _cache = OrderedDict()
        # time_now = datetime.datetime.now()
        #  _cache: {args:{value: result, time: datetime}, ...}
        @wraps(fn)
        def inner(*args, **kwargs):
            n_args = str(args)
            time_now = datetime.datetime.now()
            delta = datetime.timedelta(seconds=memory_time)
            if n_args in _cache.keys() and (time_now-_cache[n_args].get('time') < delta):
                # print 'hit cache!Last result is %s' % _cache[n_args].get('time')
                return _cache.get(n_args).get('value')
            r = fn(*args, **kwargs)
            if len(_cache) >= maxsize:
                _key = _cache.keys()[0]
                del _cache[_key]
                gc.collect()
                # print 'queue is full, del _cache[%s]' % (_key)
            _cache[n_args] = dict(value=r, time=time_now)
            # _cache.setdefault(n_args, dict(value=r, time=time_now))
            return r
        return inner
    return cache_decorator
