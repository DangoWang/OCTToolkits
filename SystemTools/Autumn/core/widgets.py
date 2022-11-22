#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
from dayu_widgets.qt import *
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.drawer import MDrawer
from dayu_widgets.push_button import MPushButton
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.label import MLabel


PADDING = 4


class ADialog(QDialog):

    def __init__(self, parent=None):
        super(ADialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.resize(500, 600)
        self.main_layout = QFormLayout()
        self.minimum_icon = MToolButton().svg('down_line.svg').icon_only()
        self.close_icon = MToolButton().svg('close_line.svg').icon_only()
        self.tool_bar_layout = QHBoxLayout()
        self.tool_bar_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.tool_bar_layout.addWidget(self.minimum_icon)
        self.tool_bar_layout.addWidget(self.close_icon)
        self.main_layout.addRow(self.tool_bar_layout)
        self.setLayout(self.main_layout)
        self.minimum_icon.clicked.connect(self.showMinimized)
        self.close_icon.clicked.connect(self.close)

        self.main_widget = QWidget()
        self.main_layout.addRow(self.main_widget)

        self.SHADOW_WIDTH = 0  # 边框距离
        self.isLeftPressDown = False  # 鼠标左键是否按下
        self.dragPosition = 0  # 拖动时坐标
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7,
                                 NONE=8)  # 枚举参数
        self.dir = self.Numbers.NONE  # 初始鼠标状态
        self.setMouseTracking(True)

    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())
        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        if tl.x() + PADDING >= x >= tl.x() and tl.y() + PADDING >= y >= tl.y():
            # 左上角
            self.dir = self.Numbers.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif rb.x() - PADDING <= x <= rb.x() and rb.y() - PADDING <= y <= rb.y():
            # 右下角
            self.dir = self.Numbers.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif tl.x() + PADDING >= x >= tl.x() and rb.y() - PADDING <= y <= rb.y():
            # 左下角
            self.dir = self.Numbers.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif rb.x() >= x >= rb.x() - PADDING and tl.y() <= y <= tl.y() + PADDING:
            # 右上角
            self.dir = self.Numbers.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif tl.x() + PADDING >= x >= tl.x():
            # 左边
            self.dir = self.Numbers.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif rb.x() >= x >= rb.x() - PADDING:
            # 右边
            self.dir = self.Numbers.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif tl.y() <= y <= tl.y() + PADDING:
            # 上边
            self.dir = self.Numbers.UP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif rb.y() >= y >= rb.y() - PADDING:
            # 下边
            self.dir = self.Numbers.DOWN
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            # 默认
            self.dir = self.Numbers.NONE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = False
            if self.dir != self.Numbers.NONE:
                self.releaseMouse()
                self.setCursor(QCursor(Qt.ArrowCursor))

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
                rmove = QRect(tl, rb)
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

    def set_layout(self, layout):
        self.main_widget.setLayout(layout)


class ADrawer(MDrawer):

    def __init__(self, title, position='right', closable=True, parent=None):
        super(ADrawer, self).__init__(title=title, position=position, closable=closable, parent=parent)
        self.close_btn = MPushButton(u'Close')
        self.copy_tab_pb = MPushButton(u'Copy Tab')
        self.title = title
        self.dialog = QDialog(parent=parent)
        self.add_button(self.copy_tab_pb)
        self.add_button(self.close_btn)
        self.close_btn.clicked.connect(self.close)
        self.copy_tab_pb.clicked.connect(self.copy_tab)

    def copy_tab(self):
        layout = self._main_lay
        self.dialog.setWindowTitle(self.title)
        self.dialog.setLayout(layout)
        self.dialog.show()
        self.close_btn.clicked.connect(self.dialog.close)
        self.dialog.resize(self.size())
        self.dialog.setGeometry(self.geometry())

    def set_widget(self, widget):
        grid_layout = QGridLayout()
        self._scroll_area.setLayout(grid_layout)
        grid_layout.addWidget(widget)


class ProgressWin(QDialog):

    def __init__(self, parent=None):
        super(ProgressWin, self).__init__(parent)
        self.resize(470, 100)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint
                            | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.X11BypassWindowManagerHint)
        self.progress = MProgressBar(status=MProgressBar.SuccessStatus)
        self.progress_label = MLabel('')
        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.progress_layout)
        self.close_pb = MPushButton(u'正在复制...')
        self.main_layout.addWidget(self.close_pb)
        self.close_pb.setEnabled(0)
        self.close_pb.clicked.connect(self.close)

    def set_progress(self, value):
        if value[1] >= 100:
            self.close_pb.setEnabled(1)
            self.progress_label.setText('Success!')
            self.close_pb.setText(u'复制完成！')
        self.progress.setValue(value[1])
        self.progress_label.setText(value[0])


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme

    app = QApplication(sys.argv)
    test = ADrawer()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())




