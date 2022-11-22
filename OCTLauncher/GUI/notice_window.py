# -*- coding: utf-8 -*-

import os
import sys
from dayu_widgets.qt import *
import HJT_Python_Mods
import json
# print dir(HJT_Python_Mods)


class NoticeWindow(QMainWindow):
    def __init__(self, parent=None, data=''):
        super(NoticeWindow, self).__init__(parent)
        self.resize(240, 280)
        self.setMaximumWidth(250)
        self.message = data
        self.url = None
        try:
            data = json.loads(data)
            self.message, self.url = [data.get('message').replace('\n', '<br>'), data.get('url')]
        except (ValueError, AttributeError):
            pass
        self.setStyleSheet("""QMainWindow{
                                color: rgb(6, 150, 215);
                                background-color: rgb(68, 68, 68);
                            }
                            
                            QTextBrowser{
                                color: rgb(255, 255, 255);
                            }
                            
                            
                            QToolButton{
                                border-radius:4px;
                                color: rgb(255, 255, 255);
                                background-color: rgb(6, 150, 215);
                            }""")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.X11BypassWindowManagerHint)
        self.setWindowTitle(u'消息')

        self.centralwidget = QWidget(self)
        self.main_layout = QVBoxLayout(self.centralwidget)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.label = QLabel(self.centralwidget)
        pix = QPixmap(os.path.join(os.path.dirname(__file__).replace("\\", "/"),"icons/sound.png")).scaled(22, 22)
        self.label.setPixmap(pix)
        # self.label.setStyleSheet("color: rgb(6, 150, 215);background-color: rgb(68, 68, 68);")
        # self.label.setText(u"通知")
        # font = QFont()
        # font.setFamily("Consolas")
        # font.setPointSize(16)
        # font.setWeight(75)
        # font.setBold(True)
        # self.label.setFont(font)
        self.main_layout.addWidget(self.label)

        self.main_layout.addWidget(QLabel())


        # self.textBrowser = QTextBrowser(self.centralwidget)
        # self.textBrowser.setFrameShape(QFrame.NoFrame)
        # self.textBrowser.setPlainText(meassage)
        # self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 3)

        self.text_label = QLabel(self.centralwidget)
        self.text_label.setStyleSheet('font: 87 9pt "Arial Black";color: rgb(255, 162, 47);')
        final_message = self.message
        if self.url:
            final_message += u'<br><br> 点此查看链接：<a href="%s">%s</a>' % (self.url, self.url)
            pass
        self.text_label.setText(final_message)
        self.text_label.setOpenExternalLinks(True)
        self.text_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.main_layout.addWidget(self.text_label)

        label_1 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(label_1)

        # self.toolButton_details = QToolButton(self.centralwidget)
        # self.toolButton_details.setMinimumSize(QSize(0, 22))
        # self.toolButton_details.setText(u"查看")
        # sizePolicy.setHeightForWidth(self.toolButton_details.sizePolicy().hasHeightForWidth())
        # self.toolButton_details.setSizePolicy(sizePolicy)
        # self.gridLayout.addWidget(self.toolButton_details, 2, 1, 1, 1)
        # self.toolButton_read = QToolButton(self.centralwidget)
        # self.toolButton_read.setMinimumSize(QSize(0, 25))
        # self.toolButton_read.setText(u"已读")
        # sizePolicy.setHeightForWidth(self.toolButton_read.sizePolicy().hasHeightForWidth())
        # self.toolButton_read.setSizePolicy(sizePolicy)
        # self.gridLayout.addWidget(self.toolButton_read, 2, 1, 1, 1)
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        self.button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.toolButton_close = QToolButton(self.centralwidget)
        self.toolButton_close.setMinimumSize(QSize(0, 22))
        self.toolButton_close.setText(u"关闭")
        self.toolButton_close.clicked.connect(self.close)
        sizePolicy.setHeightForWidth(self.toolButton_close.sizePolicy().hasHeightForWidth())
        self.toolButton_close.setSizePolicy(sizePolicy)
        self.button_layout.addWidget(self.toolButton_close)
        self.setCentralWidget(self.centralwidget)

        self.move((HJT_Python_Mods.get_desktop_width() - self.width()),
                  HJT_Python_Mods.get_desktop_hight())  # 初始化位置到右下角

    def show_animation(self):
        # 显示弹出框动画
        self.show()
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setEasingCurve(QEasingCurve.OutElastic)
        self.animation.setDuration(1500)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        h = (HJT_Python_Mods.get_desktop_hight() - self.height()-10)  # 往上
        w = HJT_Python_Mods.get_desktop_width() - self.width() - 10   # 往左
        self.animation.setEndValue(QPoint(w, h))
        self.animation.start()


