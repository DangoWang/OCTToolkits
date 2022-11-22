#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dayu_widgets.qt import MIcon
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.push_button import MPushButton
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from dayu_widgets.check_box import MCheckBox
from PySide.QtCore import *
from PySide.QtGui import *
from utils import shotgun_operations
# from widgets import ADialog


class Input(QWidget):

    def __init__(self, fields_box={}, parent=None):
        super(Input, self).__init__(parent)
        self.fields_dict = {}
        self.resize(500, 350)
        self.fields_list = fields_box
        self.addUi()
        self.set_value()

    def addUi(self):
        self.layout = QHBoxLayout()
        self.field_box = MComboBox().small()
        self.field_menu = MMenu()
        self.field_box.lineEdit().setReadOnly(False)

        self.flter_box = MComboBox().small()
        self.filter_menu = MMenu()
        self.flter_box.lineEdit().setReadOnly(False)

        self.keyword = MLineEdit().small()
        self.check_box = MCheckBox()
        self.check_box.setChecked(True)

        self.layout.addWidget(self.check_box)
        self.layout.addWidget(self.field_box)
        self.layout.addWidget(self.flter_box)
        self.layout.addWidget(self.keyword)
        self.setLayout(self.layout)

    def set_value(self):
        self.fields_dict = self.fields_list.copy()
        # for each in self.fields_list:
        #     self.fields_dict[each['label']] = each['key']
        self.field_menu.set_data(self.fields_dict.keys())
        self.field_box.set_menu(self.field_menu)
        valid_operators = shotgun_operations.valid_operators()
        self.filter_menu.set_data(list(set(valid_operators['text'] + valid_operators['entity'] + valid_operators['date'])))
        self.flter_box.set_menu(self.filter_menu)

    def get_value(self):
        return [self.check_box.isChecked(), self.field_box.currentText(), self.flter_box.currentText(), self.keyword.text()]


class FilterWindow(QDialog):

    filterInfo = Signal(list)

    def __init__(self, fields_box={}, parent=None):
        super(FilterWindow, self).__init__(parent)
        self.setWindowTitle('Create Filter')
        self.resize(500, 200)
        self.fields_box = fields_box
        self.classes = []
        self.addUi()

    def addUi(self):

        self.table_form = QFormLayout()
        self.table_form.setLabelAlignment(Qt.AlignRight)

        self.filter_name = MLineEdit()
        self.filter_name.setText('new filter')

        self.filter_operation = QHBoxLayout()
        self.btn_add_conditions = MToolButton().svg('add_line.svg').icon_only()
        # self.btn_del_conditions = MToolButton().svg('trash_line.svg').icon_only()

        self.filter_operation.addWidget(self.btn_add_conditions)
        # self.filter_operation.addWidget(self.btn_del_conditions)
        self.filter_operation.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.filter_tree = QWidget()
        self.out_filter_tree_layout = QVBoxLayout()
        self.filter_tree_layout = QVBoxLayout()
        self.out_filter_tree_layout.addLayout(self.filter_tree_layout)
        self.filter_tree.setLayout(self.out_filter_tree_layout)
        self.out_filter_tree_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.btn_group = QHBoxLayout()
        self.btn_cancel = MPushButton('Cancel')
        self.btn_create_filter = MPushButton('Create Filter')

        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_cancel)
        self.btn_group.addWidget(self.btn_create_filter)

        self.table_form.addRow(MLabel('Setting the following conditions:').h4().secondary().strong())
        # self.table_form.addRow(MDivider())
        # self.table_form.addRow('filter name', self.filter_name)
        # self.table_form.addRow(MDivider())
        self.table_form.addRow(self.filter_operation)
        self.table_form.addRow(self.filter_tree)
        self.table_form.addRow(MDivider())
        self.table_form.addRow('', self.btn_group)

        # 把设置的布局加载到窗口
        self.setLayout(self.table_form)

        ###connect
        self.btn_add_conditions.clicked.connect(self.add_conditions)
        # self.btn_del_conditions.clicked.connect(self.del_conditions)
        self.btn_create_filter.clicked.connect(self.create_filters)
        self.btn_cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def add_conditions(self):
        input = Input(self.fields_box)
        self.filter_tree_layout.addWidget(input)
        self.classes.append(input)

    # def del_conditions(self):
    #     for each in self.classes:
    #         if each.get_value()[0]:
    #             each.close()

    def create_filters(self):
        # choice_list = [['project', 'name_is', shotgun_operations.get_project()]]
        choice_list = []
        for each in self.classes:
            choice_temp = each.get_value()
            if choice_temp[0]:
                try:
                    choice = [self.fields_box[choice_temp[1]], choice_temp[2], choice_temp[3]]
                    if ':' in choice_temp[3]:
                        choice = [self.fields_box[choice_temp[1]], choice_temp[2], eval(choice_temp[3])]
                except KeyError:
                    choice = [choice_temp[1], choice_temp[2], choice_temp[3]]
                    if ':' in choice_temp[3]:
                        choice = [choice_temp[1], choice_temp[2], eval(choice_temp[3])]
                choice_list.append(choice)
        self.filterInfo.emit(choice_list)
        self.close()


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme
    app = QApplication(sys.argv)
    test = FilterWindow()

    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())