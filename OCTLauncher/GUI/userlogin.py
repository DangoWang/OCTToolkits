#!/usr/bin/env python
# -*- coding: utf-8 -*-


from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.message import MMessage
from dayu_widgets.stacked_widget import MStackedWidget
from dayu_widgets.divider import MDivider
from dayu_widgets import dayu_theme
from dayu_widgets.qt import *
from PySide.QtCore import *
from PySide.QtGui import *
import functools
import hashlib

class LoginShotgunThread(QThread):

    login_result = Signal(dict)
    # finished_subprocess = Signal(str)

    def __init__(self, parent=None, ):
        super(LoginShotgunThread, self).__init__(parent)
        try:
            from utils import shotgun_operations
            self.sg = shotgun_operations
            self.sg_instance = shotgun_operations.SGOperationThread()
        except Exception as e:
            print e
            self.login_result.emit(u'数据库连接错误')
            return
        self.data = {}
        # {'change_password': 1, 'username': self.name_box.text(), 'password': self.password_box.text(),
        #  'old_password': self.old_password.text(), 'new_password': self.new_password_box.text()}

    def run(self):
        if not self.data['change_password']:
            filters = [['sg_login', 'is', self.data['username']],
                ["sg_password", "is", self.data['password']]
            ]
        else:
            filters = [['sg_login', 'is', self.data['username']], ["sg_password", "is", self.data['old_password']]]
        groups = self.sg.find_shotgun("Group", filters, ['sg_group_project'], sg_instance=self.sg_instance)
        if groups:
            if self.data['change_password']:
                g = groups[0]
                self.sg.update_shotgun('Group', g['id'], {'sg_password': self.data['new_password']}, sg_instance=self.sg_instance)
                pass
            project_list = []
            for group in groups[0]['sg_group_project']:
                project_list.append(group['name'])
            self.login_result.emit({'project': project_list})
        else:
            self.login_result.emit(u'账号或密码错误')
        # self.finished_subprocess.emit('finished')


class UserLogin(QWidget):
    userInfo = Signal(dict)

    def __init__(self, parent=None):
        super(UserLogin, self).__init__(parent)
        self.setWindowTitle(u'OctLauncher | 登录')
        self.resize(300, 200)
        self.setWindowIcon(MIcon('./GUI/icons/oct.svg', dayu_theme.primary_color))
        self.login_shotgun = LoginShotgunThread()
        self.login_shotgun.login_result.connect(self.get_result_data)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.login_shotgun.finished_subprocess.connect(self.finished_subprocess)
        self._init_ui()

    def _init_ui(self):
        self.main_out_layout = QGridLayout()
        self.stack_widget = MStackedWidget(parent=self)
        self.main_out_layout.addWidget(self.stack_widget)
        login_widget = QWidget()
        self.stack_widget.addWidget(login_widget)
        self.main_layout = QHBoxLayout()
        login_widget.setLayout(self.main_layout)
        self._layout = QVBoxLayout()
        self.btn_group = QHBoxLayout()

        self.fill_widget = QWidget()
        # self.fill_widget.setFixedWidth(100)

        self.name_box = MLineEdit()
        tool_btn_name = MLabel(text=u'账户').mark().secondary()
        tool_btn_name.setAlignment(Qt.AlignCenter)
        tool_btn_name.setFixedWidth(60)
        # tool_btn_name.setFixedWidth(50)
        self.name_box.set_prefix_widget(tool_btn_name)

        self.password_box = MLineEdit()
        self.password_box.setEchoMode(QLineEdit.Password)
        tool_btn_password = MLabel(text=u'密码').mark().secondary()
        tool_btn_password.setAlignment(Qt.AlignCenter)
        tool_btn_password.setFixedWidth(60)
        # tool_btn_password.setFixedWidth(50)
        self.password_box.set_prefix_widget(tool_btn_password)

        self.btn_submit_login = MPushButton(u'登录')

        self.offline_using = MPushButton(u'离线使用')

        self.change_password_btn = MPushButton(u'修改密码')
        self.change_password_btn.setFixedWidth(80)
        self.change_password_btn.setEnabled(0)

        self.btn_group.addWidget(self.btn_submit_login)
        self.btn_group.addWidget(self.change_password_btn)
        self.btn_group.addWidget(self.offline_using)

        # self._layout.addWidget(self.fill_widget)
        self._layout.addWidget(self.name_box)
        self._layout.addWidget(self.password_box)
        self._layout.addWidget(MDivider())
        self._layout.addLayout(self.btn_group)
        # self._layout.addWidget(self.fill_widget)
        self.main_layout.addWidget(self.fill_widget)
        self.main_layout.addLayout(self._layout)
        self.main_layout.addWidget(self.fill_widget)

        self.setLayout(self.main_out_layout)

        # 修改密码界面
        change_password_widget = QWidget()
        change_password_layout = QVBoxLayout()
        change_password_widget.setLayout(change_password_layout)
        self.old_password = MLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        old_ps_btn_name = MLabel(text=u'旧密码').mark().secondary()
        old_ps_btn_name.setAlignment(Qt.AlignCenter)
        old_ps_btn_name.setFixedWidth(80)
        # tool_btn_name.setFixedWidth(50)
        self.old_password.set_prefix_widget(old_ps_btn_name)
        change_password_layout.addWidget(self.old_password)

        self.new_password_box = MLineEdit()
        self.new_password_box.setEchoMode(QLineEdit.Password)
        new_password_lb = MLabel(text=u'新密码').mark().secondary()
        new_password_lb.setAlignment(Qt.AlignCenter)
        new_password_lb.setFixedWidth(80)
        # tool_btn_password.setFixedWidth(50)
        self.new_password_box.set_prefix_widget(new_password_lb)
        change_password_layout.addWidget(self.new_password_box)

        self.ensure_new_password_box = MLineEdit()
        self.ensure_new_password_box.setEchoMode(QLineEdit.Password)
        ensure_new_password_box_lb = MLabel(text=u'确认新密码').mark().secondary()
        ensure_new_password_box_lb.setAlignment(Qt.AlignCenter)
        ensure_new_password_box_lb.setFixedWidth(80)
        # tool_btn_password.setFixedWidth(50)
        self.ensure_new_password_box.set_prefix_widget(ensure_new_password_box_lb)
        change_password_layout.addWidget(self.ensure_new_password_box)

        change_password_layout.addWidget(MDivider())

        self.change_ps_btn_group = QHBoxLayout()
        self.change_ps_btn = MPushButton(u'确认并登陆')
        self.cancel_change_btn = MPushButton(u'取消')
        self.change_ps_btn_group.addWidget(self.change_ps_btn)
        self.change_ps_btn_group.addWidget(self.cancel_change_btn)
        change_password_layout.addLayout(self.change_ps_btn_group)

        self.stack_widget.addWidget(change_password_widget)

        self.offline_using.clicked.connect(self.off_line_use)
        self.btn_submit_login.clicked.connect(self.submit_login)
        self.password_box.returnPressed.connect(self.submit_login)
        self.change_password_btn.clicked.connect(
            functools.partial(self.stack_widget.setCurrentIndex, 1))
        self.cancel_change_btn.clicked.connect(
            functools.partial(self.stack_widget.setCurrentIndex, 0))
        self.name_box.textChanged.connect(self.enable_change_ps_btn)
        self.change_ps_btn.clicked.connect(self.change_password_login)

    def enable_change_ps_btn(self, text):
        self.change_password_btn.setEnabled(1)

    def submit_login(self):
        pass_word = hashlib.md5(self.password_box.text()).hexdigest()
        self.login_shotgun.data = {'change_password': 0,
                                   'username': self.name_box.text(), 'password': pass_word}
        if not self.name_box.text() or not self.password_box.text():
            MMessage.error(u'请先输入账户密码！', parent=self)
            return
        if self.password_box.text() == '123':
            self.stack_widget.setCurrentIndex(1)
            return
        self.btn_submit_login.setText(u'正在登录...')
        self.btn_submit_login.setEnabled(0)
        self.login_shotgun.start()

    def change_password_login(self):
        if not self.old_password.text() or not self.new_password_box.text() or not self.ensure_new_password_box.text():
            MMessage.error(u'请先输入密码！', parent=self)
            return
        if self.old_password.text() == self.new_password_box.text():
            MMessage.error(u'新旧密码不能一样！', parent=self)
            return
        if self.new_password_box.text() == '123':
            MMessage.error(u'密码不能为初始密码！', parent=self)
            return
        if not self.new_password_box.text() == self.ensure_new_password_box.text():
            MMessage.error(u'两次输入的新密码不一致！', parent=self)
            return
        old_pass_word = hashlib.md5(self.old_password.text()).hexdigest()
        new_pass_word = hashlib.md5(self.new_password_box.text()).hexdigest()
        self.login_shotgun.data = {'change_password': 1, 'username': self.name_box.text(),
                                   'password': self.password_box.text(), 'old_password': old_pass_word,
                                   'new_password': new_pass_word}
        self.change_ps_btn.setEnabled(0)
        self.change_ps_btn.setText(u'正在登录...')
        self.login_shotgun.start()
    pass

    def get_result_data(self, data):
        if data == u'数据库连接错误':
            MMessage.info(data, parent=self)
            self.userInfo.emit({})
            self.btn_submit_login.setEnabled(1)
            self.change_ps_btn.setEnabled(1)
            self.change_ps_btn.setText(u'确认并登陆')
            # self.close()
        elif data == u'账号或密码错误':
            MMessage.error(data, parent=self)
            self.btn_submit_login.setEnabled(1)
            self.change_ps_btn.setEnabled(1)
            self.change_ps_btn.setText(u'确认并登陆')
            # self.userInfo.emit({})
            # self.close()
        else:
            if self.login_shotgun.data['change_password'] != 1:
                self.userInfo.emit({'username': self.name_box.text(), 'password': self.password_box.text(), 'project': data['project']})
            else:
                self.userInfo.emit({'username': self.name_box.text(), 'password': self.new_password_box.text(),
                                    'project': data['project']})
            # MMessage.success('登录成功', parent=self)
            # self.btn_submit_login.setText(u'登录')
            self.close()
        self.btn_submit_login.setText(u'登录')
        self.login_shotgun.quit()

    # def finished_subprocess(self, data):
    #     if data == 'finished':
    #         self.btn_submit_login.setText(u'登录成功')

    def off_line_use(self):
        self.userInfo.emit('offline')
        self.close()


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme
    app = QApplication(sys.argv)
    test = UserLogin()

    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
