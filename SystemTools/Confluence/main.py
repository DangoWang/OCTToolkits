#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################

import sys
import os
sys.path.append(os.environ['oct_toolkits_path'])
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])
from dayu_widgets.qt import *
from dayu_widgets.tool_button import MToolButton
from PySide import QtWebKit
from PySide import QtCore
import webbrowser


class OCTWiki(QMainWindow):
    def __init__(self, parent=None):
        super(OCTWiki, self).__init__(parent)
        self.resize(888, 666)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        main_lay = QVBoxLayout(self.centralwidget)
        self.horizontalLayout_title = QHBoxLayout()
        self.horizontalLayout_title.addItem(QSpacerItem(40, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.pushButton_min = MToolButton().svg('down_line_dark.svg').icon_only()
        self.pushButton_min.clicked.connect(self.showMinimized)
        self.horizontalLayout_title.addWidget(self.pushButton_min)
        self.toolButton_close = MToolButton().svg('close_line.svg').icon_only()
        self.horizontalLayout_title.addWidget(self.toolButton_close)
        self.toolButton_close.clicked.connect(self.close)
        main_lay.addLayout(self.horizontalLayout_title)
        self.web_view = QtWebKit.QWebView()
        main_lay.addWidget(self.web_view)
        self.web_view.setUrl('http://wiki.ds.com/pages/viewpage.action?pageId=8618280')
        self.setLayout(main_lay)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

def main():
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication
    app = QApplication(sys.argv)
    wiki_win = OCTWiki()
    dayu_theme.apply(wiki_win)
    wiki_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    webbrowser.open("http://wiki.ds.com/pages/viewpage.action?pageId=8618280", new=0, autoraise=True)
