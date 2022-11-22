#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pprint as pp
# import yaml
# import codecs
# import json
import subprocess, os
from OCTLauncher.config import software_launch_env
from PySide import QtGui
from config.GLOBAL import *
from dayu_widgets.message import MMessage
import json
# config_path = OCTLAUNCHERCFGPATH


def change_encoding(input_dict, encoding='gbk'):
    if isinstance(input_dict, dict):
        return {change_encoding(key): change_encoding(value) for key, value in input_dict.iteritems()}
    elif isinstance(input_dict, list):
        return [change_encoding(element) for element in input_dict]
    elif isinstance(input_dict, unicode):
        return input_dict.encode(encoding)
    else:
        return input_dict


def get_env_config(env_config_path=None):
    reload(software_launch_env)
    # if not env_config_path:
    #     env_config_path = config_path
    data = software_launch_env.launch_env
    # with codecs.open(os.path.join(env_config_path, 'software_launch_env.py'), 'r') as f:
    #     data = json.load(f)
    data = change_encoding(data)
    if data:
        return data
    else:
        raise RuntimeError("Reading env_config failed!")


def deal_ch(txt):
    return json.loads(json.dumps(txt, encoding='gbk'))


def get_os_env():
    return os.environ.copy()  # - ENV_NAME:ENV_VALUE


class LaunchDCC(object):
    def __init__(self, dcc, parent=None, extra_env=None):
        self.parent = parent
        self.extra_env = extra_env
        self._dcc = str(dcc)
        self.launch_mode = 'front'
        self.back_launch_cmd = ''
        self._env_config = get_env_config()
        self._os_env = get_os_env()

    def edit_env(self):
        _env = self._os_env
        all_env = self._env_config[self._dcc]['Env']
        if not all_env:
            return _env
        for e in all_env:
            if e['mode'] == 'over':
                _env[e['name']] = e['value']
            elif e['mode'] == 'pre':
                _env[e['name']] = e['value'] + ";" + os.environ.get(e['name'], '')
            elif e['mode'] == 'post':
                _env[e['name']] = os.environ.get(e['name'], '') + ";" + e['value']
            else:
                pass
        # print dcc_name, _env
        return _env

    def launch_dcc(self):
        # print self.edit_env()
        # print self.extra_env
        reload(software_launch_env)
        if self.extra_env:
            self.edit_env().update(self.extra_env)
        _env = self.edit_env()
        try:
            _env['oct_tooltikts_thirdparty'] = os.environ['oct_tooltikts_thirdparty']
            _env['oct_toolkits_path'] = os.environ['oct_toolkits_path']
            if self.launch_mode == 'front':
                MMessage.config(5)
                MMessage.loading(u'正在开启%s, 请稍等...'% deal_ch(self._env_config[self._dcc]['Label']),
                                 parent=self.parent)
                exe_str = deal_ch(self._env_config[self._dcc]['Exec'])
                if 'python' not in exe_str and '--' not in exe_str and not os.path.isfile(exe_str):
                    raise RuntimeError
                if '.bat' in str(exe_str):
                    subprocess.Popen(exe_str, env=_env, shell=False)
                else:
                    try:
                        subprocess.Popen(exe_str.encode('utf-8'), env=_env, shell=True)
                    except Exception, e:
                        print e
                        raise RuntimeError(e)
            else:
                if self.back_launch_cmd:
                    _env['PYTHONPATH'] = ';'.join([_env['PYTHONPATH'],  os.environ['oct_tooltikts_thirdparty'],
                                                   os.environ['oct_toolkits_path']
                                                   ])
                    subprocess.check_call(self.back_launch_cmd, env=_env, shell=False)
        except:
            QtGui.QMessageBox.question(self.parent, u"提示", u"未发现{},请确保已经安装了该版本软件！\n默认在以下路径：{}"
                                       .format(deal_ch(self._dcc),
                                               deal_ch(self._env_config[self._dcc]['Exec'])
                                               ),
                                        QtGui.QMessageBox.Ok)





