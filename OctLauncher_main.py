# -*- coding: utf-8 -*-

from config.GLOBAL import *
import sys
import os
import json
os.environ['utils_path'] = sys.argv[0] or ''
os.environ['oct_tooltikts_thirdparty'] = CURRENTPATH + '/thirdparty'
os.environ['oct_toolkits_path'] = CURRENTPATH
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])
from dayu_widgets.qt import *
from OCTLauncher.GUI import userlogin
reload(userlogin)
from OCTLauncher.GUI import launcher_main
from OCTLauncher.GUI import HJT_Python_Mods
from utils import common_methods


my_documents_folder = common_methods.get_documents() or 'D:/'


class MainApp(QSystemTrayIcon):

    def __init__(self):
        super(MainApp, self).__init__()
        self.main_window = launcher_main.MainWindow()
        self.menu = QMenu()
        # self.blink_thread = BlinkWidget(self)
        self.quit_action = QAction('&Exit', self.menu)  # 直接退出可以用qApp.quit
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)
        self.activated.connect(self.act)
        self.login_info = {}
        self.setIcon(QIcon(QPixmap(CURRENTPATH + "/icons/oct_monkey.ico")))
        # self.main_window.message_thread.new_messages_sig.connect(self.receive_new_msgs)
        # self.messageClicked.connect(self.main_window.show_note_list)
        self.login_file = my_documents_folder + "/oct_launcher_login_info.json"
        if os.path.isfile(self.login_file):
            with open(self.login_file, "r") as f:
                try:
                    self.login_info = json.load(f)
                except ValueError:
                    pass
            # if self.login_info:
            #     self.get_login_info(self.login_info)
        self.main_window.change_login_btn.clicked.connect(self.change_login_user)

    # def receive_new_msgs(self, txt):
    #
    #     self.showMessage(u'消息提示', txt)

        # if count > 0:
        #     try:
        #         self.showMessage(u'十月文化', u'有{}条未读消息'.format(count))
        #     except Exception as e:
        #         pass

    def setup_main_window(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(CURRENTPATH + "/icons/oct_monkey.ico"))
        self.main_window.arrange_launch_btns()
        self.main_window.setWindowIcon(icon)
        desktop = QApplication.desktop()
        # self.main_window.move(1000, 100)
        self.main_window.resize(100, desktop.height()*4/7)
        # self.main_window.move(1500, 200)
        self.main_window.move(HJT_Python_Mods.get_desktop_width() - self.main_window.size().width(),
                              (HJT_Python_Mods.get_desktop_hight() - self.main_window.size().height()) / 2)
        # if desktop.height() * 2 < desktop.width():
        #     self.main_window.move(desktop.width()/2 - self.main_window.width()/2 - 50,
        #                           desktop.height() - self.main_window.height() - 50)
        # else:
        #     self.main_window.move(2*desktop.width()/2 - self.main_window.width() - 50,
        #                           desktop.height() - self.main_window.height() - 50)
        self.main_window.setAutoFillBackground(True)

    def quit_app(self):
        self.main_window.hide()
        self.hide()
        os._exit(0)
        # exit()

    def act(self, reason):
        if reason == 2:
            self.main_window.show()

    def change_login_user(self):
        if os.path.isfile(self.login_file):
            os.remove(self.login_file)
        self.quit_app()

    def get_login_info(self, login_info):
        if login_info:
            with open(self.login_file, "w") as f:
                json.dump(login_info, f)
            os.environ['oct_launcher_using_mode'] = 'offline'
            if not login_info == 'offline':
                self.login_info = login_info
                self.main_window.login_info = login_info
                user, projects_temp = self.login_info['username'], self.login_info['project']
                os.environ['oct_user'] = str(user)
                os.environ['oct_launcher_using_mode'] = 'online'
                projects = [each.decode('utf-8') for each in projects_temp]
                self.main_window.comboBox.addItems(projects)
                self.main_window.user.setText(user)
            self.setup_main_window()
            self.act(2)
            self.show()
            if os.environ['oct_launcher_using_mode'] in ['online']:
                self.main_window.parse_message()
            self.showMessage(u'十月文化', u'启动工具，双击或右键使用', icon=QSystemTrayIcon.Information)
        else:
            confirm_dialog = QMessageBox()
            confirm_dialog.setText(u'shotgun连接失败，是否以离线形式使用？')
            confirm_dialog.setWindowTitle(u"提示")
            confirm_dialog.addButton(u"是", QMessageBox.AcceptRole)  # role 0
            confirm_dialog.addButton(u"否，联系TD", QMessageBox.RejectRole)  # role 1
            answer = confirm_dialog.exec_()
            if answer == 0:
                os.environ['oct_launcher_using_mode'] = 'offline'
                self.setup_main_window()
                self.act(2)
                self.show()
                self.showMessage(u'十月文化', u'启动工具，双击或右键使用', icon=QSystemTrayIcon.Information)


def main():
    import ctypes
    myappid = 'oct.octLauncher.subproduct.20190820'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    launch_app = MainApp()
    login_window = userlogin.UserLogin()
    dayu_theme.apply(login_window)
    # login_window.setWindowIcon(MIcon('./GUI/icons/oct.svg', dayu_theme.primary_color))
    login_window.userInfo.connect(launch_app.get_login_info)
    login_window.show()
    if launch_app.login_info:
        if launch_app.login_info == 'offline' or 'password' not in launch_app.login_info.keys():  # 为了兼容旧模式
            login_window.hide()
            launch_app.get_login_info(launch_app.login_info)
        else:
            login_window.name_box.setEnabled(False)
            login_window.password_box.setEnabled(False)
            login_window.name_box.setText(launch_app.login_info['username'])
            login_window.password_box.setText(launch_app.login_info['password'])
            login_window.submit_login()
    # launch_app.setup_main_window()
    # launch_app.act(2)
    # launch_app.show()
    # launch_app.showMessage(u'十月文化', u'启动工具，双击或右键使用', icon=QSystemTrayIcon.Information)
    # print os.environ['oct_tooltikts_thirdparty']
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
