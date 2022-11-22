#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
CURRENTPATH = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')
CURRENTSCRIPTPATH = os.path.dirname(__file__).rstrip('config').replace('\\', '/')
RVPATH = 'C:/Program Files/Shotgun/RV-7.0/bin/rv.exe'
OCTLAUNCHERGUIPATH = CURRENTPATH + "/OctLauncher/GUI"
OCTLAUNCHERCFGPATH = CURRENTPATH + "/OctLauncher/config"

format_file = {'frame': ['.ma', '.hip', '.nk'], 'picture': ['.jpg', '.png', '.jpeg', '.tif', '.bmp', '.exr', ], 'video': ['.mov', '.mp4', '.avi']}


