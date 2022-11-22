#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import sys
import os

sys.path.append(os.environ['oct_toolkits_path'])
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])
from config.GLOBAL import *
from gui import autumn_main_window
from utils.shotgun_operations import *
import ssl

try:
    user = get_user()
    permission = get_permission(user)
    admin_group = autumn_design_permissions()
except ssl.SSLEOFError:
    raise RuntimeError(u'网络连接错误！！')

admin_appearance = permission in admin_group


def autumn():
    autumn_window = autumn_main_window.UIMain()
    if not admin_appearance:
        #  隐藏一些管理员才能有的按钮
        for each_widget in [autumn_window.create_page_action,
                            autumn_window.copy_page_action,
                            autumn_window.load_cfg_action,
                            autumn_window.add_filter_pb,
                            autumn_window.edit_config_action,
                            autumn_window.save_page_pb,
                            autumn_window.delete_page_pb]:
            each_widget.setVisible(0)
        #  隐藏done
        cfg = autumn_window.load_user_config(user)
        autumn_window.parse_config(cfg)
    window_title = autumn_window.windowTitle()
    new_window_title = window_title + '      ' + u'登陆用户：' + user + u'         权限：' + permission
    autumn_window.setWindowTitle(new_window_title)
    return autumn_window

def main():
    from thirdparty.dayu_widgets import dayu_theme
    from thirdparty.dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    permission = get_permission(get_user())
    autumn_win = autumn()
    dayu_theme.apply(autumn_win)
    # autumn_win.showMaximized()
    import ctypes
    process_id = 'Autumn Desktop Beta v1.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(process_id)
    autumn_win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

