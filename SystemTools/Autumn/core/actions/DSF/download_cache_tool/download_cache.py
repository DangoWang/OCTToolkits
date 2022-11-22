#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.8
import os
from utils import shotgun_operations
import download_cache_ui
from dayu_widgets import dayu_theme
from pprint import pprint
from utils import fileIO
from dayu_widgets.message import MMessage

sg = shotgun_operations

cache_header = [
    {
        'label': u'资产名字',
        'key': 'asset',
        # 'searchable': True
    },
    {
        'label': u'缓存对象',
        'key': 'object',
        # 'searchable': True
    },
    {
        'label': u'名称空间',
        'key': 'namespace',
        # 'searchable': True
    },
    {
        'label': u'缓存版本',
        'key': 'version',
        # 'searchable': True
    },
    {
        'label': u'缓存路径',
        'key': 'cachePath',
        # 'searchable': True
        },
]


class DownloadCacheFile(object):
    def __init__(self, dict_info=""):
        super(DownloadCacheFile, self).__init__()
        self.dict_info = dict_info
        version_id = self.dict_info["id"]
        cache_info_list = sg.find_shotgun("CustomEntity03", [["sg_shot_version.Version.id", "is", version_id[0]]],
                                          ["sg_namespace", "sg_asset", "sg_obj_list", "sg_version", "sg_cache_path"],
                                          [{'field_name': 'sg_version', 'direction': 'desc'}])
        print cache_info_list
        if cache_info_list:
            table_data = []
            cache_version = cache_info_list[0]["sg_version"]
            for cache in cache_info_list:
                if cache["sg_version"] == cache_version:
                    cache_info = dict()
                    cache_info.update({
                        "asset": cache["sg_asset"],
                        "object": cache["sg_obj_list"],
                        "namespace": cache["sg_namespace"],
                        "version": cache["sg_version"],
                        "cachePath": cache["sg_cache_path"]})
                    table_data.append(cache_info)
                else:
                    break
            self.cache_win = download_cache_ui.DownLoadCache(parent=self.dict_info['widget'])
            dayu_theme.apply(self.cache_win)
            self.cache_win.clear_data()
            self.cache_win.set_header(cache_header)
            self.cache_win.set_data(table_data)
            self.cache_win.data_table.hideColumn(4)
            self.cache_win.download_pb.clicked.connect(lambda: self.get_cache_file(self.cache_win))
            self.cache_win.show()
            self.fetching_copy_thread = fileIO.CopyFile()
            self.fetching_copy_thread.progress.connect(self.get_data)
            self.fetching_copy_thread.finished.connect(self.finish_fetch_data)
        else:
            MMessage.config(2)
            MMessage.error(u'没有相应的缓存信息可以下载!', parent=self.dict_info['widget'])
            return

    def get_data(self, data):
        self.cache_win.set_progress(data[1], data[0])

    def finish_fetch_data(self, finished):
        if finished:
            self.fetching_copy_thread.wait()
            self.fetching_copy_thread.quit()

    def get_cache_file(self, cache_window):
        download_path = cache_window.dir_path_le.text().replace('\\', '/')
        if download_path:
            copy_file_list = self.download_cache_file(download_path, cache_window)
            self.fetching_copy_thread.copy_list = copy_file_list
            self.fetching_copy_thread.start()
            self.cache_win.download_pb.setEnabled(0)
        else:
            MMessage.config(2)
            MMessage.error(u'请先选择路径!', parent=self.dict_info['widget'])
            return

    @staticmethod
    def download_cache_file(download_path, cache_window):
        copy_file_list = []
        rowcount = cache_window.data_model.rowCount()
        for r in range(0, int(rowcount)):
            cache_file = cache_window.data_model.index(r, 4).data()
            cache_path = os.path.split(cache_file)[0]
            file_list = fileIO.get_copy_list(cache_path, cache_path.replace('I:', download_path))
            for file_path in file_list:
                copy_file_list.append(file_path)
        return copy_file_list




