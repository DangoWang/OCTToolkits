#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.push_button import MPushButton
from dayu_widgets.message import MMessage
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
# from dayu_widgets.tag import MTag
from dayu_widgets.flow_layout import MFlowLayout
from dayu_widgets.toast import MToast
from PySide.QtCore import *
from PySide.QtGui import *
from pprint import pprint
# from widgets import ADialog

from utils import shotgun_operations


class TableFormThread(QThread):

    result_data = Signal(list)
    def __init__(self, parent=None):
        super(TableFormThread, self).__init__(parent)
        self.data = ''

    def run(self, *args, **kwargs):
        fields_list = []
        for field in self.data:
            dic = {}
            if self.data[field]['data_type']['value'] in ['entity']:
                children = []
                for child in self.data[field]['properties']['valid_types']['value']:
                    child_dic = {}
                    link_table_fields = shotgun_operations.schema_field_read(child)
                    children_children = []
                    for table_field in link_table_fields:
                        children_children_dic = {}
                        children_children_dic.update({'value': link_table_fields[table_field]['name']['value'],
                                                      'label': link_table_fields[table_field]['name']['value'],
                                                      'shotgun_field': table_field})
                        children_children.append(children_children_dic)
                        # children_children_dic.update({'label':link_table_fields[table_field]['name']['value'], 'value':link_table_fields[table_field]['name']['value'], 'children': children_children})
                    child_dic.update({'label': child, 'value': child, 'children': children_children})
                    children.append(child_dic)
                dic.update({'value': self.data[field]['name']['value'], 'label': self.data[field]['name']['value'], 'children': children, 'shotgun_field': 'entity'})
            else:
                dic.update(
                    {'value': self.data[field]['name']['value'], 'label': self.data[field]['name']['value'], 'shotgun_field': field})

            fields_list.append(dic)
        self.result_data.emit(fields_list)


class CreateTableForm(QDialog):

    tableInfo = Signal(dict)

    def __init__(self, parent=None):
        super(CreateTableForm, self).__init__(parent)
        self.resize(500, 350)
        self.fields_list = []
        self.fields_data = []
        self.tag_color = ''
        self.setWindowTitle('Create Page')
        self.table_form_thread = TableFormThread()
        self.table_form_thread.result_data.connect(self.get_result_data)
        self.addUi()

    def addUi(self):

        self.table_form = QFormLayout()
        self.table_form.setLabelAlignment(Qt.AlignRight)

        self.page_name = MLineEdit()

        self.type_menu = MMenu()
        self.type_menu.set_data(shotgun_operations.type_menu())
        self.type = MComboBox()
        self.type.set_menu(self.type_menu)

        self.fields_menu = MMenu(cascader=True)
        self.fields = MComboBox()
        self.fields._root_menu = self.fields_menu

        self.fields_widget = QWidget()
        self.fields_widget.setMinimumHeight(100)
        self.fields_box = MFlowLayout()
        self.fields_widget.setLayout(self.fields_box)

        self.btn_group = QHBoxLayout()

        self.btn_cancel = MPushButton('Cancel')
        self.btn_create_page = MPushButton('Create Page')

        self.btn_group.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group.addWidget(self.btn_cancel)
        self.btn_group.addWidget(self.btn_create_page)
        # self.btn_group.setLabelAlignment(Qt.AlignRight)

        self.table_form.addRow(MLabel('Create a new Page').h4().secondary().strong())
        self.table_form.addRow(MDivider())
        self.table_form.addRow("Name:", self.page_name)
        self.table_form.addRow("Type:", self.type)

        self.table_form.addRow("Fields:", self.fields)
        self.table_form.addRow("Fields_select:", self.fields_widget)
        self.table_form.addRow(MDivider())
        self.table_form.addRow('', self.btn_group)

        self.fields.set_placeholder("Please select the type first")


        # 设置显示效果
        self.page_name.setEchoMode(MLineEdit.Normal)


        # 把设置的布局加载到窗口
        self.setLayout(self.table_form)

        #connect
        self.type.textChanged.connect(self.get_fields)

        self.btn_create_page.clicked.connect(self.create_page)
        self.btn_cancel.clicked.connect(self.cancel)
        self.fields._root_menu.sig_value_changed.connect(self.give_data)
        # self.fields_box.
    ###将选中的数据放到fields_select中
    def give_data(self, value):
        data = '.'.join(value)
        if data[0] == '.':
            data = data[1:]
        tag = MTag(text=data, parent=self.fields_widget).closeable()
        tag.set_dayu_color(self.tag_color)
        tag.sig_closed.connect(lambda: self.list_pop(tag.text()))
        if data not in self.fields_list:
            self.fields_list.append(data)
            self.fields_box.addWidget(tag)
    ##将删除的数据从列表中删除
    def list_pop(self, tag_text):
        self.fields_list.remove(tag_text)

    ######下面两个函数都是查找shotgun后台真实fields的函数
    def find_entity(self, arg):
        return lambda x: x['value'] == arg

    def assembly_characters(self, choice_fields, all_fields):
        append = {}
        for field in choice_fields:
            pro = field.split('.')
            Isentity = filter(self.find_entity(pro[0]), all_fields)[0]
            # print filter(self.find_entity(pro[0]), all_fields)
            try:
                Isentity_table = filter(self.find_entity(pro[1]), Isentity['children'])[0]
                Isentity_table_field = filter(self.find_entity(pro[2]), Isentity_table['children'])[0]
                append.update({field: field.replace(pro[-1], Isentity_table_field['shotgun_field']).replace(pro[0], 'entity')})
            except Exception as e:
                print(e)
                append.update({field: field.replace(pro[-1], Isentity['shotgun_field'])})
        return append

    def create_page(self):
        page_name_text = self.page_name.text()
        type_text = self.type.currentText()
        fields_text = self.fields_list
        if page_name_text == '':
            MMessage.info(u'请输入页面名', parent=self.parent())
            return
        if not fields_text:
            MMessage.info(u'请选择查看字段', parent=self.parent())
            return
        fields = self.assembly_characters(fields_text, self.fields_data)
        # fields.update({'ID': 'id'})
        fields_true = [{'label': k, 'key': v, 'searchable': True} for k, v in fields.iteritems()]
        self.tableInfo.emit({'page_name': page_name_text,
                             'page_type': type_text,
                             'page_fields': fields_true})
        ##page_fields
        # {u'Updated by.HumanUser.Analytics Truth Finder Onboarded': u'Updated by.HumanUser.analytics_truth_finder_onboarded',
        #     u'Created by.HumanUser.Welcome Page Visited': u'Created by.HumanUser.welcome_page_visited'}
        self.close()

    def cancel(self):
        self.close()
    ####选中type后获取该表的字段
    def get_fields(self):
        # self.fields_list = []
        # for btn in self.fields_widget.children():
        #     if btn != self.fields_box:
        #         btn.deleteLater()
        type_text = self.type.currentText()
        self.table_form_thread.data = shotgun_operations.schema_field_read(type_text)
        self.table_form_thread.start()
        MMessage.config(999)
        self.msg = MMessage.loading(u'正在加载中', parent=self.parent())

    def get_result_data(self, data):
        self.fields_data = data
        self.fields_menu.set_data(data)
        self.msg.close()
        MMessage.config(1)
        MMessage.success(u'加载成功', parent=self.parent())


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication
    from dayu_widgets import dayu_theme
    app = QApplication(sys.argv)
    test = CreateTableForm()

    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())