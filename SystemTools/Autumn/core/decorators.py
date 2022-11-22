#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
from dayu_widgets.qt import *
from dayu_widgets import dayu_theme
from dayu_widgets.message import MMessage
from utils.shotgun_operations import *
from dayu_widgets.toast import MToast
from dayu_widgets.label import MLabel

# def toDialog(cls):
#     #  把QWidget装饰成QDialog并添加标题
#     class Dialog(QDialog):
#         def __init__(self, parent=None):
#             super(Dialog, self).__init__(parent)
#             self.widget = cls()
#             self.setWindowTitle('test')
#     return Dialog


class ErrorBox(QMessageBox):
    def __init__(self, parent=None, text=u''):
        super(ErrorBox, self).__init__(parent)
        dayu_theme.apply(self)
        self.main_layout = QHBoxLayout()
        self.main_label = MLabel(text).danger()
        self.main_layout.addWidget(self.main_label)
        self.setLayout(self.main_layout)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


errorWindow = ErrorBox()
user_permission = get_permission(get_user())


def permission_control(allowance=None, forbidden=None):
    def wrapper(func):
        def deal_permission(args):
            # print get_permission(get_user()), allowance, forbidden
            try:
                allow = 1
                if allowance:
                    if user_permission not in allowance:
                        allow = 0
                if forbidden:
                    if user_permission in forbidden:
                        allow = 0
                if allow:
                    return func(args)
                else:
                    MToast.error(parent=errorWindow, text=u'您没有权限!')
                    return
            except Exception as e:
                MToast.error(parent=errorWindow, text=u'发生未知错误!\n%s'%e)
                print e
                return
        return deal_permission
    return wrapper

