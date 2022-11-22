#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import os
import shutil
import subprocess
import sys
import json
from PySide import QtGui, QtCore
from PySide.QtCore import Qt
from dayu_widgets.qt import *
import xml.etree.ElementTree as xml
from cStringIO import StringIO
import PySide.QtGui as QtWidgets
import pysideuic as uic
from config.GLOBAL import *
from PySide import QtGui
from dayu_widgets.badge import MBadge
from dayu_widgets.tool_button import MToolButton
from dayu_widgets import dayu_theme
from dayu_widgets.theme import MTheme
import time
from utils import common_methods
from utils import shotgun_operations
from utils import fileIO
import pika
file_path = OCTLAUNCHERGUIPATH
import notice_window

# 获取脚本路径
def resource_inpath():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))
    return ""

def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        sys.path.append(os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/')+'/OCTLauncher/GUI/qrc')
        exec pyc in frame
        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
        return form_class, base_class


# def compile_qrc():
#     qrc_path = os.path.join(file_path, 'qrc')
#     sys.path.append(qrc_path)
#     import_grp = list()
#     for qrc in os.listdir(qrc_path):
#         if qrc.endswith('.qrc'):
#             py_name = qrc_path + "/" + qrc.split('.')[0] + "_rc.py"
#             if not os.path.isfile(py_name):
#                 import_name = qrc.split('.')[0]+'_rc'
#                 qrc_name = qrc_path + "/" + qrc
#                 subprocess.Popen("C:/Python27/Lib/site-packages/PySide/pyside-rcc.exe -o {0} {1}".format(py_name, qrc_name))
#                 import_grp.append(import_name)
#     return import_grp
#
#
# compile_qrc()

from OCTLauncher.GUI import set_buttons

MainWindowForm, MainWindowBase = loadUiType(file_path + '/main.ui')
PADDING = 20


class MessageThread(QThread):
    new_messages_sig = Signal(basestring)
    cmd_sig = Signal(basestring)

    def __init__(self, parent=None):
        super(MessageThread, self).__init__(parent)
        # self.user_info = None
        self.user = None
        # import utils.shotgun_operations as shotgun_operations
        # self.sg = shotgun_operations
        # self.sg_instance = shotgun_operations.SGOperationThread()
        credentials = pika.PlainCredentials('admin', '123456')  # mq用户名和密码
        self.shotgun_connection = pika.BlockingConnection(pika.ConnectionParameters(host='mq.ds.com',
                                                                       port=5672,
                                                                       virtual_host='/shotgun',
                                                                       credentials=credentials))

    def get_message_from_mq(self, ch, method, properties, body):
        if body:
            self.new_messages_sig.emit(body.decode('utf-8'))

    def get_cmd_msg_from_mq(self, ch, method, properties, body):
        if body:
            self.cmd_sig.emit(body)

    def run(self):
        try:
            self.channel = self.shotgun_connection.channel()
            # self.channel.exchange_declare(exchange='notice', exchange_type='direct')
            # self.channel.exchange_declare(exchange='update', exchange_type='fanout')
            notice_result = self.channel.queue_declare(queue=self.user+'_notice', exclusive=False)
            update_result = self.channel.queue_declare(queue=self.user+'_update', exclusive=False)
            self.channel.queue_bind(exchange='notice', queue=notice_result.method.queue)
            self.channel.queue_bind(exchange='update', queue=update_result.method.queue)
            # self.channel.queue_declare(queue=self.user)
            self.channel.basic_consume(queue=notice_result.method.queue, on_message_callback=self.get_message_from_mq, auto_ack=True)
            self.channel.basic_consume(queue=update_result.method.queue, on_message_callback=self.get_cmd_msg_from_mq, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            pass

    # def run(self, *args, **kwargs):
    #     import utils.shotgun_operations as sg
    #     if not self.user_info:
    #         return
    #     # while 1:
    #     filters = [["sg_if_read", "is", False], ["addressings_to", "name_contains", self.user_info['code']]]
    #     fields = ["sg_if_read", "addressings_to"]
    #     note_sg = self.sg.find_shotgun("Note", filters, fields, sg_instance=self.sg_instance)
    #     if note_sg:
    #         # self.blink_thread.blink = 1
    #         # self.news_btn_grp.setVisible(1)
    #         self.new_messages_sig.emit(note_sg.__len__())
    #     else:
    #         self.new_messages_sig.emit(0)  # self.blink_thread.blink = 0  # self.news_btn_grp.setVisible(1)
    #         # time.sleep(60)  # 容易导致并发错误，所以设置成50s刷新一次


class MyVersionThread(QThread):
    btn_show = Signal(int)
    ver_num = Signal(str)
    def __init__(self, btn):
        super(MyVersionThread, self).__init__()
        import utils.shotgun_operations as shotgun_operations
        self.sg = shotgun_operations
        self.sg_instance = shotgun_operations.SGOperationThread()
        self.btn = btn

    def run(self):
        try:
            version_file = os.path.join(resource_inpath(), "version.txt")
            file_id= file(version_file, "r")
            version_info = file_id.readline().replace("\n", "").replace("\r", "")
            file_id.close()
            ver_filters = []
            ver_fields = ["code", "description"]
            ver_sg = self.sg.find_shotgun("CustomEntity05", ver_filters, ver_fields, sg_instance=self.sg_instance)
            for ver in ver_sg:
                if ver["code"] > version_info:
                    self.btn_show.emit(1)
                    self.ver_num.emit(version_info)
                    break
        except:
            pass


class CmdThread(QThread):
    finish_sig = Signal(bool)

    def __init__(self, parent):
        super(CmdThread, self).__init__(parent=parent)
        self.cmd = ''

    def run(self, *args, **kwargs):
        try:
            subprocess.Popen(self.cmd, shell=True)
            self.finish_sig.emit(True)
        except Exception as e:
            print u'执行命令%s出现错误：%s' % (self.cmd, e)
            pass


class MainWindow(MainWindowBase, MainWindowForm):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #  necessary params
        self.login_info = {}
        self.message_thread = MessageThread()
        self.cmd_thread = CmdThread(self)
        self.cmd_thread.finish_sig.connect(self.finish_update)
        self.message_thread.new_messages_sig.connect(self.receive_new_msgs)
        self.message_thread.cmd_sig.connect(self.run_cmd)
        # ---end
        # self.m_Position = None
        self.oct_logo_btn.clicked.connect(self.read_web)
        # self.arrange_launch_btns()
        # self.setAttribute(Qt.WA_NoSystemBackground, True)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.ToolTip)
        self.SHADOW_WIDTH = 0  # 边框距离
        self.isLeftPressDown = False  # 鼠标左键是否按下
        self.dragPosition = 0  # 拖动时坐标
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7,
                                 NONE=8)  # 枚举参数
        self.dir = self.Numbers.NONE  # 初始鼠标状态
        self.setMouseTracking(True)
        self.close_btn.clicked.connect(self.hide)
        self.ver_num = None
        # 消息
        self.msg_count = 0
        # 消息提醒框
        self.new_group()
        # self.blink_thread.start()
        self.copy_task = fileIO.CopyFile()
        self.create_local_cache()
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.message_thread.run)
        # self.timer.start(50000)
        # self.ver_thread = MyVersionThread(self.toolButton_ver)
        # self.ver_thread.start()
        # self.ver_thread.btn_show.connect(self.show_ver_btn)
        # self.ver_thread.ver_num.connect(self.set_ver_num)

    def close(self, event):
        self.hide()
        event.ignore()

    def new_group(self):
        self.news_btn_grp = QtGui.QFrame(self.work_area_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.news_btn_grp.sizePolicy().hasHeightForWidth())
        self.news_btn_grp.setSizePolicy(sizePolicy)
        gridLayout = QtGui.QGridLayout(self.news_btn_grp)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)
        button_alert = MToolButton().svg('alert_fill.svg').large()
        button_alert.setToolTip(u'打开消息盒子')
        self.toolButton_news = MBadge.dot(True, widget=button_alert)
        self.toolButton_news.set_dayu_count(999)
        gridLayout.addWidget(self.toolButton_news, 0, 0, 1, 1)

        button_ver = MToolButton().svg('up_line.svg').large()
        # button_ver.setToolTip(u'打开消息盒子')
        self.toolButton_ver = MBadge.dot(True, widget=button_ver)
        # self.toolButton_ver = MBadge.dot(True, widget=button_ver)
        self.toolButton_ver.set_dayu_text("new")
        # self.toolButton_ver = MToolButton().svg('up_line.svg').icon_only()
        gridLayout.addWidget(self.toolButton_ver, 0, 1, 1, 1)
        self.toolButton_ver.setHidden(1)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.news_btn_grp, 3, 0, 1, 1)
        dayu_theme_ = MTheme('light', primary_color=MTheme.orange)
        dayu_theme_.apply(self.news_btn_grp)
        # self.news_btn_grp.setVisible(0)
        button_alert.clicked.connect(self.show_note_list)
        button_ver.clicked.connect(self.show_version_list)

        self.toolButton_news.set_dayu_count(0)

    def create_local_cache(self):
        #  拷贝maya的plugin
        maya_module = CURRENTPATH + '/DCC_TOOLS/maya_module'
        plug_in_fld = CURRENTPATH + '/DCC_TOOLS/maya_plugins/2017'
        plug_in_fld_maya_2019 = CURRENTPATH + '/DCC_TOOLS/maya_plugins/2019'
        my_document = common_methods.get_documents() or 'D:/'
        local_plug_ins_fld = my_document + '/maya/2017/plug-ins'
        local_plug_ins_fld_maya_2019 = my_document + '/maya/2019/plug-ins'
        local_module = my_document + '/maya/2017/modules'

        self.copy_task.copy_list = [[maya_module, local_module], [plug_in_fld, local_plug_ins_fld],
                                    [plug_in_fld_maya_2019, local_plug_ins_fld_maya_2019]
                                    ]
        self.copy_task.start()
        # if not os.path.isdir(local_plug_ins_fld):
        #     os.makedirs(local_plug_ins_fld)
        # if not os.path.isdir(local_module):
        #     os.makedirs(local_module)
        # for each in os.listdir(plug_in_fld):
        #     try:
        #         shutil.copyfile(plug_in_fld + '/' + each, local_plug_ins_fld + '/' + each)
        #     except (WindowsError, IOError):
        #         return

    def parse_message(self):
        if os.environ['oct_launcher_using_mode'] in ['online']:
            import utils.shotgun_operations as sg
            user = self.login_info['username']
            self.message_thread.user = user
            # self.message_thread.user_info = sg.find_one_shotgun('Group', [['sg_login', 'is', user]], ['code'])
            self.message_thread.start()
            # self.message_thread.start()

    def receive_new_msgs(self, msg):
        notice_win = notice_window.NoticeWindow(self, msg)
        notice_win.show_animation()
        self.msg_count += 1
        self.toolButton_news.set_dayu_count(self.msg_count)

    def run_cmd(self, cmd_sig):
        print 'got command : %s' % cmd_sig
        self.cmd_thread.cmd = cmd_sig
        self.cmd_thread.start()

    def finish_update(self, finish):
        if finish:
            print 'updating finished'

    def show_ver_btn(self, count):
        try:
            self.toolButton_ver.setHidden(1-count)
        except Exception, e:
            pass

    def set_ver_num(self, ver_num):
        try:
            self.ver_num = ver_num
        except Exception, e:
            pass

    def show_note_list(self):
        self.msg_count = 0
        self.toolButton_news.set_dayu_count(0)
        if os.environ['oct_launcher_using_mode'] in ['online']:
            from SystemTools.MessageBox import unread_message_ui
            # reload(unread_message_ui)
            message_window = unread_message_ui.main(self.comboBox.currentText(),
                                                    self.user.text(), parent=self)
            this_theme = MTheme('dark', primary_color=MTheme.orange)
            this_theme.apply(message_window)
            message_window.show()

    def show_version_list(self):
        if os.environ['oct_launcher_using_mode'] in ['online']:
            from SystemTools.VersionInfo import oct_version_info
            # reload(unread_message_ui)
            ver_window = oct_version_info.main(self.ver_num, parent=self)
            this_theme = MTheme('dark', primary_color=MTheme.orange)
            this_theme.apply(ver_window)
            ver_window.show()

    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点 
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())
        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        # if tl.x() + PADDING >= x >= tl.x() and tl.y() + PADDING >= y >= tl.y():
        #     # 左上角
        #     self.dir = self.Numbers.LEFTTOP
        #     self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        # elif rb.x() - PADDING <= x <= rb.x() and rb.y() - PADDING <= y <= rb.y():
        #     # 右下角
        #     self.dir = self.Numbers.RIGHTBOTTOM
        #     self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))
        # elif tl.x() + PADDING >= x >= tl.x() and rb.y() - PADDING <= y <= rb.y():
        #     # 左下角
        #     self.dir = self.Numbers.LEFTBOTTOM
        #     self.setCursor(QtGui.QCursor(Qt.SizeBDiagCursor))
        # elif rb.x() >= x >= rb.x() - PADDING and tl.y() <= y <= tl.y() + PADDING:
        #     # 右上角
        #     self.dir = self.Numbers.RIGHTTOP
        #     self.setCursor(QtGui.QCursor(Qt.SizeBDiagCursor))
        # elif tl.x() + PADDING >= x >= tl.x():
        #     # 左边
        #     self.dir = self.Numbers.LEFT
        #     self.setCursor(QtGui.QCursor(Qt.SizeHorCursor))
        # elif rb.x() >= x >= rb.x() - PADDING:
        #     # 右边
        #     self.dir = self.Numbers.RIGHT
        #     self.setCursor(QtGui.QCursor(Qt.SizeHorCursor))
        # elif tl.y() <= y <= tl.y() + PADDING:
        #     # 上边
        #     self.dir = self.Numbers.UP
        #     self.setCursor(QtGui.QCursor(Qt.SizeVerCursor))
        if rb.y() >= y >= rb.y() - PADDING:
            # 下边 
            self.dir = self.Numbers.DOWN
            # self.setCursor(QtGui.QCursor(Qt.SizeVerCursor))
        else:
            # 默认 
            self.dir = self.Numbers.NONE
            self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = False
            if self.dir != self.Numbers.NONE:
                self.releaseMouse()
                self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = True
            if self.dir != self.Numbers.NONE:
                self.mouseGrabber()
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if not self.isLeftPressDown:
            self.region(gloPoint)
        else:
            if self.dir != self.Numbers.NONE:
                rmove = QtCore.QRect(tl, rb)
                if self.dir == self.Numbers.LEFT:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                elif self.dir == self.Numbers.RIGHT:
                    rmove.setWidth(gloPoint.x() - tl.x())
                elif self.dir == self.Numbers.UP:
                    if rb.y() - gloPoint.y() <= self.minimumHeight():
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif self.dir == self.Numbers.DOWN:
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif self.dir == self.Numbers.LEFTTOP:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if rb.y() - gloPoint.y() <= self.minimumHeight():
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif self.dir == self.Numbers.RIGHTTOP:
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif self.dir == self.Numbers.LEFTBOTTOM:
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif self.dir == self.Numbers.RIGHTBOTTOM:
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass
                self.setGeometry(rmove)
            else:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    @staticmethod
    def read_web():
        import webbrowser
        url = 'http://www.octmedia.com/'
        webbrowser.open(url, new=0, autoraise=True)

    def arrange_launch_btns(self):
        set_buttons.add_launch_buttons(self, [self.DCC_btn_grp, self.pipe_btn_grp, self.other_btn_grp],
                                       config=[self.user, self.comboBox])
        return True


def main():
    app = None
    if not app:
        app = QtGui.QApplication([])
    window = MainWindow()
    window.move(1500, 200)
    # window.setAutoFillBackground(True)
    window.raise_()
    window.show()
    if app:
        app.exec_()


if __name__ == '__main__':
    main()
