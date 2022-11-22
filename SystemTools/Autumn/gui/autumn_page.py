#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import functools
import pprint
import re
from utils import shotgun_operations
from dayu_widgets.item_model import MTableModel, MSortFilterModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.push_button import MPushButton
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.divider import MDivider
from dayu_widgets.message import MMessage
from dayu_widgets.page import MPage
from dayu_widgets.qt import *
from operator import methodcaller
from dayu_widgets import dayu_theme
from dayu_widgets.flow_layout import MFlowLayout
from dayu_widgets.menu import MMenu
from dayu_widgets.label import MLabel
# from dayu_widgets.tag import MTag
import create_table_form
import dayu_widgets.utils as utils
import utils.common_methods as atu
from utils.shotgun_operations import *
import time
import datetime

permission = get_permission(get_user())
admin_group = autumn_design_permissions()
admin_appearance = permission in admin_group


class MFetchDataThread(QThread):
    result_sig = Signal(list)

    def __init__(self, entity_type=None, filters=None, fields=None, order=None, parent=None):
        super(MFetchDataThread, self).__init__(parent)
        self.entity_type = entity_type
        self.filters = filters
        self.fields = fields
        self.order = order


    @staticmethod
    def get_day(num):
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        day = today + one_day*num
        return day

    def deal_filter_type(self, filter_str):
        if not filter_str:
            return filter_str
        new_filter_str = ''
        try:
            new_filter_str = str(filter_str.encode('utf-8'))
        except Exception as e:
            return filter_str
        if '%' in new_filter_str:
            return get_envision(new_filter_str.strip('%'))
        if not isinstance(filter_str, dict):
            if '{' in new_filter_str and '}' in new_filter_str:
                num = int(new_filter_str.strip('{').strip('}'))
                return self.get_day(num)
        return filter_str

    def run(self, *args, **kwargs):
        new_filter = []
        for f in self.filters:
            new_f = [f[0], f[1], self.deal_filter_type(f[2])]
            new_filter.append(new_f)
        try:
            results = shotgun_operations.find_shotgun(self.entity_type, new_filter, self.fields, self.order)
            self.result_sig.emit(results)
        except AttributeError:
            return


class SheetContent(QWidget):
    def __init__(self, parent=None, config=None):
        super(SheetContent, self).__init__(parent=parent)
        # self.setMinimumHeight(970)
        self.__config = {}
        self.set_config(config)
        self.header = []
        self.data = []
        self.actions = {}
        self.svg = None
        self.name = None
        self.msg_parent = atu.get_widget_top_parent(self)
        try:
            self.project = shotgun_operations.get_project()
        except AttributeError:
            self.project = None
        self.user = shotgun_operations.get_user()
        self.action_param = {}  # 用来传递给action的参数
        self.is_load = False  # 切换tab时是否需要刷新数据的标志
        self.show_msg = False
        self.fields_old_index_order = {}
        self.page_fields_order = {}
        # self.tool_bar = MMenuTabWidget()
        # self.search_engine_line_edit = MLineEdit().search_engine().small()
        # self.search_engine_line_edit.setMaximumWidth(300)
        # self.tool_bar.tool_bar_insert_widget(self.search_engine_line_edit)
        self.model = MTableModel()
        self.model_sort = MSortFilterModel()
        self.table = MTableView(size=dayu_theme.small, show_row_count=True)
        # self.table.setMinimumHeight(970)
        self.table.horizontalHeader().setStretchLastSection(1)
        # self.table.header_view.customContextMenuRequested.disconnect(self.table.header_view._slot_context_menu)
        # self.table.header_view.customContextMenuRequested.connect(self._edit_fields)
        self.main_lay = QGridLayout()
        self.model_sort.setSourceModel(self.model)
        self.table.setModel(self.model_sort)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        # self.main_lay.addWidget(self.tool_bar)
        self.main_lay.addWidget(self.table, 0, 0, 1, 1)

        self.page_ctrl = MPage()
        self.page_ctrl.set_total(0)
        self.page_ctrl._change_page_size_button.sig_value_changed.connect(self.set_current_page)
        self.page_ctrl._current_page_spin_box.valueChanged.connect(self.set_current_page)
        self.main_lay.addWidget(self.page_ctrl, 1, 0, 1, 1)

        self.setLayout(self.main_lay)
        self.table.setShowGrid(True)
        self.msg = None

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_menu)
        # self.table.doubleClicked.connect(self.__connect_double_clicked_method)
        #
        # self.table.contextMenu.popup(QCursor.pos())
        # self.table.contextMenu.show()
        # self.table.contextMenu.close()
        #
        self.table.contextMenu = QMenu(self)
        self.action_separator = self.table.contextMenu.addSeparator()
        self.add_action_at = self.table.contextMenu.addAction(u'+')
        self.add_action_win = AddAction(parent=self.msg_parent)
        self.add_action_win.project = self.project
        self.add_action_at.triggered.connect(self.show_action_win)
        self.add_action_win.result_sig.connect(self.add_action)

        self.fetch_data_thread = MFetchDataThread(parent=self)
        self.fetch_data_thread.result_sig.connect(self.get_fetch_result)
        # self.table.horizontalHeader().sectionMoved.connect(self.get_header_moved_result)
        #  如果不是管理员，不允许添加action
        if not admin_appearance:
            self.add_action_at.setVisible(0)
            self.action_separator.setVisible(0)
    # def __connect_double_clicked_method(self):
    #     selected_indexes = self.table.selectedIndexes()
    #     rows = list(set([index.row() for index in selected_indexes]))
    #     self.action_param.update({'id': [int(self.model.index(row, 0).data()) for row in rows]})
    #     self.table.contextMenu.popup(QCursor.pos())
    #     self.table.contextMenu.hide()

    def get_fields_index_order(self, *args):
        result = {}
        for i in range(99):
            header = self.model_sort.headerData(i, Qt.Horizontal)
            if header in result.keys():
                break
            result[header] = i
        return result

    def get_header_moved_result(self, logic_index, old_index, new_index):
        header_data = self.model_sort.headerData(logic_index, Qt.Horizontal)
        if not self.page_fields_order:
            self.page_fields_order = self.fields_old_index_order.copy()
        reverse_dict = {v: k for k, v in self.page_fields_order.iteritems()}
        add_data = 1 if (old_index > new_index) else -1
        for i in range(min(new_index, old_index), max(new_index, old_index)):
            self.page_fields_order[header_data] = new_index
            try:
                if add_data < 0:
                    self.page_fields_order[reverse_dict[i+1]] -= 1
                else:
                    self.page_fields_order[reverse_dict[i]] += 1
            except KeyError:
                pass
        self.__config['page_fields_order'] = self.page_fields_order
        self.__config['page_fields_order'] = self.page_fields_order

    def show_menu(self, *args):
        selected_indexes = self.table.selectedIndexes()
        rows = list(set([index.row() for index in selected_indexes]))
        self.action_param.update({'id': [int(self.model_sort.index(row, 0).data()) for row in rows]})
        self.table.contextMenu.popup(QCursor.pos())
        self.table.contextMenu.show()

    # @Slot(QPoint)
    # def _edit_fields(self, point):
    #     context_menu = MMenu(parent=self)
    #     logical_column = self.table.header_view.logicalIndexAt(point)
    #     model = utils.real_model(self.table.header_view.model())
    #     if logical_column >= 0 and model.header_list[logical_column].get('checkable', False):
    #         action_select_all = context_menu.addAction(self.table.header_view.tr('Select All'))
    #         action_select_none = context_menu.addAction(self.table.header_view.tr('Select None'))
    #         action_select_invert = context_menu.addAction(self.table.header_view.tr('Select Invert'))
    #         self.table.header_view.connect(action_select_all, SIGNAL('triggered()'),
    #                      functools.partial(self.table.header_view._slot_set_select, logical_column, Qt.Checked))
    #         self.table.header_view.connect(action_select_none, SIGNAL('triggered()'),
    #                      functools.partial(self.table.header_view._slot_set_select, logical_column, Qt.Unchecked))
    #         self.table.header_view.connect(action_select_invert, SIGNAL('triggered()'),
    #                      functools.partial(self.table.header_view._slot_set_select, logical_column, None))
    #         context_menu.addSeparator()
    #     fit_action = context_menu.addAction(self.table.header_view.tr('Fit Size'))
    #     fit_action.triggered.connect(functools.partial(self.table.header_view._slot_set_resize_mode, True))
    #     edit_action = context_menu.addAction(self.table.header_view.tr('Edit Fields'))
    #     edit_action.triggered.connect(functools.partial(self.edit_fields, self.__config))
    #     context_menu.addSeparator()
    #     for column in range(self.table.header_view.count()):
    #         action = context_menu.addAction(model.headerData(column, Qt.Horizontal, Qt.DisplayRole))
    #         action.setCheckable(True)
    #         action.setChecked(not self.table.header_view.isSectionHidden(column))
    #         action.toggled.connect(functools.partial(self.table.header_view._slot_set_section_visible, column))
    #     context_menu.exec_(QCursor.pos() + QPoint(10, 10))

    def edit_fields(self, config):
        if not admin_appearance:
            from dayu_widgets.toast import MToast
            MToast.error(parent=self.msg_parent, text=u'您没有权限!')
            return
        edit_fields_win = EditFields(config=config, parent=self.msg_parent)
        edit_fields_win.show()
        edit_fields_win.tableInfo.connect(self.get_edit_fields_results)

    @Slot()
    def get_edit_fields_results(self, edit_results):
        self.__config['page_fields'] = edit_results['page_fields']
        self.parse_config()

    def show_action_win(self, *args):
        page_type = self.__config['page_type']
        self.add_action_win.project = self.project
        self.add_action_win.set_actions_list(page_type)
        self.add_action_win.show()

    @Slot()
    def add_action(self, data):
        self.table.contextMenu.clear()
        self.actions.clear()
        i = 0
        for each in data:
            try:
                label, method, icon, mode = each['label'], each['value'], each['icon'], each['mode']
            except KeyError:
                continue
            if method in self.actions.values():
                continue
            import importlib
            try:
                actions_register = importlib.import_module('SystemTools.Autumn.core.actions.' + self.project + '.actions_register')
            except ImportError:
                raise
            # from SystemTools.Autumn.core.actions import actions_register
            if mode == '0':  # 如果不是右键菜单，就以双击方式启动
                self.table.doubleClicked.connect(lambda i=i, method=method:
                                                 methodcaller(method, self.action_param)(actions_register))
                continue
            self.actions.update({label: method})
            action = self.table.contextMenu.addAction(MIcon(icon, dayu_theme.primary_color), label)
            action.triggered.connect(
                lambda i=i, method=method: methodcaller(method, self.action_param)(actions_register))
            i += 1
        self.__config['page_actions'] = data
        self.action_separator = self.table.contextMenu.addSeparator()
        self.add_action_at = self.table.contextMenu.addAction('+')
        self.add_action_at.triggered.connect(self.show_action_win)
        if not admin_appearance:
            self.add_action_at.setVisible(0)
            self.action_separator.setVisible(0)

    def set_up(self, *args):
        # pass
        # pp.pprint(self.header)
        # pp.pprint(self.data)
        # header = sorted(self.header[:], key=self.page_fields_order)
        new_header = []
        for each_head in self.header:
            if 'order' in each_head.keys():
                if not isinstance(each_head['order'], Qt.SortOrder):
                    del each_head['order']
            new_header.append(each_head)
        self.header = new_header[:]
        self.model.set_header_list(self.header)
        self.model_sort.set_header_list(self.header)
        self.table.set_header_list(self.header)
        #  分页
        # self.model.set_data_list(self.data)
        self.page_ctrl.set_total(len(self.data))
        # self.page_ctrl.set_field('page_size_list',
        #                          [{'label': '25 - Fastest', 'value': 25}, {'label': '50 - Fast', 'value': 50},
        #                           {'label': '75 - Medium', 'value': 75}, {'label': '100 - Slow', 'value': 100},
        #                           {'label': 'All Results', 'value': len(self.data)}])
        self.page_ctrl.set_field('page_size_list',
                                 [
                                  #    {'label': '25 - Fastest', 'value': 25}, {'label': '50 - Fast', 'value': 50},
                                  # {'label': '75 - Medium', 'value': 75}, {'label': '100 - Slow', 'value': 100},
                                  {'label': 'All Results', 'value': len(self.data)}
                                 ])
        self.set_current_page()

    def set_current_page(self, *args):
        num_per_page = int(re.findall('\d+', self.page_ctrl._change_page_size_button.currentText())[0])
        num_page = int(self.page_ctrl._current_page_spin_box.value())
        start = (num_page - 1) * num_per_page
        end = num_page * num_per_page
        # self.model.set_data_list(self.data[start:end])
        self.model.set_data_list(self.data)
        self.fields_old_index_order = self.get_fields_index_order()
        # try:
        #     for each in self.__config['page_fields_order']:
        #         self.table.horizontalHeader().moveSection(each[0], each[1])
        # except Exception as e:
        #     print u'恢复表头顺序出现错误', e
        #     pass

    def set_config(self, config):
        if config:
            self.__config = config

    def update_filters(self, dict_data):
        self.__config.update(dict_data)

    def get_config(self, *args):
        return self.__config

    def get_selected_content(self, *args):
        selected_indexes = self.table.selectedIndexes()
        rows = list(set([index.row() for index in selected_indexes]))
        selected_ids = [int(self.model_sort.index(row, 0).data()) for row in rows]
        result_data = []
        for each_data in self.data:
            if each_data["id"] in selected_ids:
                result_data.append(each_data)
        return result_data

    def parse_config(self, *args):
        self.data = []
        self.header = []
        entity_type = self.__config['page_type']
        filters = self.__config['page_filters']
        order = None
        try:
            order = self.__config['page_order']
        except KeyError:
            pass
        # default_filter = [["project", "name_is", self.project]]
        # default_filter = []
        # for df in default_filter:
        #     if df not in filters:
        #         filters.append(df)
        fields = [f['key'] for f in self.__config['page_fields']]
        # pp.pprint(fields)
        # self.actions = self.__config['page_actions'] or {}
        try:
            self.svg = self.__config['page_svg']
            self.name = self.__config['page_name']
        except KeyError:
            pass
        try:
            self.page_fields_order = self.__config['page_fields_order']
        except KeyError:
            pass
        self.header = [{'label': u'编号', 'key': 'id', 'searchable': True}]
        self.header.extend(self.__config['page_fields'])
        if self.page_fields_order:
            try:
                self.header = sorted(self.header, key=lambda x: int(self.page_fields_order[x['label']]))
            except KeyError:
                pass
        self.fetch_data_thread.entity_type, self.fetch_data_thread.filters, self.fetch_data_thread.fields, \
                                                    self.fetch_data_thread.order = entity_type, filters, fields, order
        if self.show_msg:
            MMessage.config(duration=99)
            if self.msg:
                self.msg.close()
            self.msg = MMessage.loading(u'读取中...', parent=self.msg_parent)
        self.fetch_data_thread.start()

    def get_fetch_result(self, results):
        for each_result in results:
            result_dict = {}
            for field, value in each_result.items():
                field_name = field
                field_value = value
                if type(field_value) == dict:
                    # print field_value
                    value = field_value['name']
                result_dict.update({field_name: value})
            self.data.append(result_dict)  # pass
        self.set_up()
        # 传入调用actions时需要的参数
        self.action_param['project'] = self.project
        self.action_param['user'] = self.user
        self.action_param['type'] = self.__config['page_type']
        self.action_param['widget'] = atu.get_widget_top_parent(self)
        self.action_param['config'] = self.__config
        if self.__config['page_actions']:
            self.add_action(self.__config['page_actions'])
        if self.show_msg:
            MMessage.config(1)
            MMessage.success(u'数据拉取成功！', parent=self.msg_parent)
            self.msg.close()
        self.is_load = True


class EditFields(create_table_form.CreateTableForm):

    def __init__(self, config, parent=None):
        super(EditFields, self).__init__(parent)
        self.setWindowTitle('Edit Page')
        self.central_widget = QWidget(parent=self)
        self.central_widget.setLayout(self.table_form)
        self.central_widget.hide()
        self.config = config or {}
        # try:
        #     del self.config['page_fields'][u'ID']
        # except KeyError:
        #     pass
        # self.fields_data
        self.page_name.setText(self.config['page_name'])
        self.table_form_new = QFormLayout()
        self.table_form_new.setLabelAlignment(Qt.AlignRight)
        self.table_form_new.addRow(MLabel('Edit This Page:      '+self.config['page_name']).h4().secondary().strong())
        self.table_form_new.addRow(MDivider())
        fields_widget = QWidget()
        self.fields_layout = MFlowLayout()
        fields_widget.setLayout(self.fields_layout)
        self.table_form_new.addRow(MLabel('Existing Fields:'))
        self.table_form_new.addRow(fields_widget)
        self.table_form_new.addRow(self.fields_widget)
        map(self.give_data, [each['label'].split('.') for each in self.config['page_fields']])
        self.tag_color = 'yellow'
        self.table_form_new.addRow(MLabel('Add Fields:'))
        self.get_fields_btn = MPushButton(u'Get Fields>>')
        self.btn_group_3 = QHBoxLayout()
        self.btn_group_3.addWidget(self.get_fields_btn)
        self.btn_group_3.addWidget(self.fields)
        self.table_form_new.addRow('', self.btn_group_3)
        self.table_form_new.addRow(MDivider())
        self.btn_group_2 = QHBoxLayout()
        self.btn_group_2.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_group_2.addWidget(self.btn_cancel)
        self.btn_create_page.setText('Edit')
        self.btn_group_2.addWidget(self.btn_create_page)
        self.table_form_new.addRow('', self.btn_group_2)
        self.setLayout(self.table_form_new)
        self.get_fields_btn.clicked.connect(lambda: self.type.setEditText(self.config['page_type']))
        self.btn_create_page.clicked.disconnect(self.create_page)
        self.btn_create_page.clicked.connect(self.edit_page)

    def edit_page(self, *args):
        try:
            self.create_page()
        except IndexError:
            removed_fields = [each['label'] for each in self.config['page_fields'] if each['label'] not in self.fields_list]
            new_config = self.config['page_fields'][:]
            if removed_fields:
                for f in removed_fields:
                    for p in self.config['page_fields']:
                        if f == p['label']:
                            try:
                                new_config.remove(p)
                            except Exception as e:
                                print '424, remove key error', e
                                continue
            self.config['page_fields'] = new_config[:]
            for each_cfg in self.config['page_fields']:
                if 'reg' in each_cfg.keys():
                    del each_cfg['reg']
        pprint.pprint(self.config['page_fields'])
        self.tableInfo.emit({'page_fields': self.config['page_fields']})
        self.close()


class AddAction(QDialog, MFieldMixin):
    result_sig = Signal(list)

    def __init__(self, parent=None):
        super(AddAction, self).__init__(parent)
        self.setWindowTitle(u'Add Actions')
        self.resize(300, 500)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(MDivider('Add Actions'))
        self.action_table = MTableView(size=dayu_theme.small, show_row_count=False)
        self.action_table.horizontalHeader().setStretchLastSection(1)
        self.action_table.setShowGrid(False)
        self.add_pb = MPushButton(u'Add')
        self.main_layout.addWidget(self.action_table)
        self.main_layout.addWidget(self.add_pb)
        self.actions_header = [{'label': u'Actions', 'key': 'label'},
                               {'label': u'Method', 'key': 'value'},
                               {'label': u'Mode', 'key': 'mode'},
                               {'label': u'Icon', 'key': 'icon', 'icon': lambda x, y: x}, ]
        self.actions_list = []
        self.action_model = MTableModel()
        self.action_model.set_header_list(self.actions_header)
        self.model_sort = MSortFilterModel()
        self.model_sort.setSourceModel(self.action_model)
        self.action_table.setModel(self.model_sort)
        self.model_sort.set_header_list(self.actions_header)
        self.action_table.set_header_list(self.actions_header)
        # self.action_table.hideColumn(1)
        # self.action_table.hideColumn(2)
        # self.action_table.hideColumn(3)
        self.add_pb.clicked.connect(self.get_result)
        self.project = None

    def set_actions_list(self, page_type):
        if page_type:
            import importlib
            actions_register = importlib.import_module('SystemTools.Autumn.core.actions.' + self.project + '.actions_register')
            # from SystemTools.Autumn.core.actions import actions_register
            self.actions_list = actions_register.actions_dict[self.project][page_type]
            self.action_model.set_data_list(self.actions_list)

    def get_result(self, *args):
        selected_action = []
        rows = list(set([index.row() for index in self.action_table.selectedIndexes()]))
        selected_action.extend([{'label': self.model_sort.index(row, 0).data(),
                                 'value': self.model_sort.index(row, 1).data(),
                                 'mode': self.model_sort.index(row, 2).data(),
                                 'icon': self.model_sort.index(row, 3).data(),
                                 }
                                for row in rows])
        self.result_sig.emit(selected_action)
        self.close()


if __name__ == '__main__':
    import sys
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    page = SheetContent()
    # page = EditFields({"page_actions": {u'播放': 'task_video_player'},
    #                   "page_fields": {"Updated by.ApiUser.Maintainer": "entity.ApiUser.email", "Users": "users",
    #                                   "Created by.HumanUser.Tags": "entity.HumanUser.tags", u"编号": "id",
    #                                   "Group Name": "code",
    #                                   "Created by.HumanUser.First Name": "entity.HumanUser.firstname"},
    #                   "page_filters": [],
    #                   "page_name": "Group",
    #                   "page_type": "Task",
    #                   "page_svg": "calendar_line.svg"})

    page.set_config({"page_actions": [],
                      "page_fields": {"Updated by.ApiUser.Maintainer": "entity.ApiUser.email", "Users": "users",
                                      "Created by.HumanUser.Tags": "entity.HumanUser.tags", u"编号": "id",
                                      "Group Name": "code",
                                      "Created by.HumanUser.First Name": "entity.HumanUser.firstname"},
                      "page_filters": [],
                      "page_name": "Group",
                      "page_type": "Group",
                      "page_svg": "calendar_line.svg"})
    page.show()
    # page.parse_config()
    dayu_theme.apply(page)
    sys.exit(app.exec_())
