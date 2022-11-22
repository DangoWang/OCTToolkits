# -*- coding: utf-8 -*-

# Description:    + 常用函数
# Author:         + xusheng
# Version:        + v001
# ChangeInfo      +
# Usage:          +


_OCT_TempLogPath = r'C:\Users\qiuxusheng\Desktop\log.txt'

import json
import subprocess as sp

def dataToLogFile(*args, **kwargs):
    if args:
        try:
            f = open(_OCT_TempLogPath, 'w')
            kwargs['args'] = args
            json.dump(kwargs, f, indent=4)
            f.flush()
            f.close()
        except:
            raise

def openLogFileInTextedit(filePath = ''):
    global _OCT_TempLogPath

    if filePath:
        _OCT_TempLogPath = filePath

    try:
        sp.Popen(['notepad++.exe', _OCT_TempLogPath])
    except:
        sp.Popen(['notepad.exe', _OCT_TempLogPath])