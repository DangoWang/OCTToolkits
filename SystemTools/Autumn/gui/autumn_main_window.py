#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.9
# wechat : 18250844478
###################################################################
import os
import sys
import codecs
import copy
import getpass
import json
import pprint as pp
from dayu_widgets.line_tab_widget import MLineTabWidget
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.theme import MTheme
from config import GLOBAL
from autumn_page import *
from utils import shotgun_operations
from utils import common_methods as atu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.field_mixin import MFieldMixin
from utils import shotgun_operations as sg
from SystemTools.Autumn.gui import detail_page_ui, detail_page
import utils.common_methods as atu
reload(detail_page_ui)

from pprint import pprint
from color_rules import *


class FilterItem(QWidget):
    def __init__(self, parent=None, filter_content=None):
        super(FilterItem, self).__init__(parent)
        # self.resize(100, 10)
        # self.setMaximumHeight(30)
        self.filter_content = filter_content
        self.main_layout = QHBoxLayout()
        self.delete_item_btn = MToolButton().svg('close_line_dark.svg').small()
        self.filter_content_lb = MLabel()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.delete_item_btn)
        self.main_layout.addWidget(self.filter_content_lb)
        self.set_label(self.filter_content)
        permission = get_permission(get_user())
        admin_group = autumn_design_permissions()
        admin_appearance = permission in admin_group
        if not admin_appearance:
            self.hide()

    def set_label(self, filter_content):
        text = ''
        for each in filter_content:
            new_each = [str(e) for e in each]
            text = ' '.join(new_each) + '\n' + text if text else ' '.join(new_each)
        self.filter_content_lb.setText(text)


class CopyPageWin(QDialog):
    new_page_name_sig = Signal(str)

    def __init__(self, parent=None):
        super(CopyPageWin, self).__init__(parent)
        self.setWindowTitle('Copy A New Page')
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.page_name_le = MLineEdit().small()
        self.page_name_le.setPlaceholderText(u'Input new page name')
        self.main_layout.addWidget(self.page_name_le)
        self.copy_doit_btn = MPushButton('Copy')
        self.cancel_copy_btn = MPushButton('Cancel')
        self.btn_layout.addWidget(self.copy_doit_btn)
        self.btn_layout.addWidget(self.cancel_copy_btn)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)
        self.cancel_copy_btn.clicked.connect(self.close)
        self.copy_doit_btn.clicked.connect(self.copy_doit)

    @property
    def copy_name(self):
        return self.page_name_le.text()

    def copy_doit(self):
        if not self.copy_name:
            MMessage.config(2)
            MMessage.error('Please input a name!', parent=self.parent())
            return
        self.new_page_name_sig.emit(self.copy_name)
        self.close()


class SaveLoadConfig(QDialog):
    cfg_name_sig = Signal(str)

    def __init__(self, parent=None):
        super(SaveLoadConfig, self).__init__(parent)
        self.setWindowTitle(u'保存/加载配置')
        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.cfg_cb = MComboBox()
        self.cfg_menu = MMenu()
        self.cfg_cb.set_menu(self.cfg_menu)
        self.main_layout.addWidget(self.cfg_cb)
        self.save_doit_btn = MPushButton('Save')
        self.cancel_btn = MPushButton('Cancel')
        self.btn_layout.addWidget(self.save_doit_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)
        self.cancel_btn.clicked.connect(self.close)
        self.save_doit_btn.clicked.connect(self.save_doit)

    def set_items(self, data):
        self.cfg_menu.set_data(sorted(data))

    @property
    def save_name(self):
        return self.cfg_cb.currentText()

    def save_doit(self):
        if not self.save_name:
            MMessage.config(2)
            MMessage.error(u'请选择配置名.', parent=atu.get_widget_top_parent(self))
            return
        self.cfg_name_sig.emit(self.save_name)
        self.close()


class ResourcesWin(QDialog):
    edit_result_sig = Signal(str)

    def __init__(self, parent=None):
        super(ResourcesWin, self).__init__(parent)
        self.setWindowTitle('Edit Page Settings')
        self.resize(500, 800)
        self.content_widget = MTextEdit(self).resizeable()
        self.content_widget.setReadOnly(True)
        main_lay = QVBoxLayout()
        main_lay.addWidget(MDivider('Edit Text'))
        main_lay.addWidget(self.content_widget)
        self.setLayout(main_lay)

    def set_text(self, text):
        self.content_widget.setText(text)


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setMaximumHeight(8)
        self.add_button = MToolButton().svg('add_line.svg').icon_only()
        self.add_button.setMaximumHeight(6)
        self.add_button.setMaximumWidth(25)
        self.add_button.hide()
        self.delete_button = MToolButton().svg('close_line.svg').icon_only()
        self.delete_button.setMaximumHeight(6)
        self.delete_button.setMaximumWidth(25)
        self.delete_button.hide()
        self.confirm_button = MToolButton().svg('confirm_line.svg').icon_only()
        self.confirm_button.setMaximumHeight(6)
        self.confirm_button.setMaximumWidth(25)
        self.confirm_button.hide()
        self.data_table = MTableView(size=dayu_theme.small, show_row_count=True)
        self.data_table.setShowGrid(True)
        self.data_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_model = MTableModel()
        self.model_sort = MSortFilterModel()
        self.model_sort.setSourceModel(self.data_model)
        self.data_table.resizeColumnsToContents()
        self.data_table.resizeRowsToContents()
        self.data_table.horizontalHeader().setStretchLastSection(1)
        self.data_table.setModel(self.model_sort)
        # self.data_table.verticalHeader().setDefaultSectionSize(35)
        # self.data_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        the_theme = MTheme(theme='dark')
        the_theme.apply(self)

        layout_2 = QHBoxLayout()
        layout_2.addWidget(self.add_button)
        layout_2.addWidget(self.delete_button)
        layout_2.addWidget(self.confirm_button)
        layout_2.addWidget(self.splitter)

        layout_1 = QGridLayout()
        layout_1.addLayout(layout_2, 0, 0)
        layout_1.addWidget(self.data_table, 1, 0)
        self.setLayout(layout_1)


class EditCfgWin(QDialog, MFieldMixin):
    edit_result_sig = Signal(str)

    def __init__(self, parent=None):
        super(EditCfgWin, self).__init__(parent)
        self.resize(870, 700)
        self.tab_page_name = {u'页面过滤': 'page_filters', u'页面动作': 'page_actions',
                              u'页面字段': 'page_fields', u'详情页动作': 'detail_page_actions'}
        self.pages = []
        self.page_setting = {}
        self.project_name = sg.get_project()
        self.splitter = QSplitter()
        self.splitter.setFixedHeight(100)
        self.splitter.setOrientation(Qt.Horizontal)
        self.setWindowTitle('Edit Page Settings')
        self.label_page_name = MLabel(u'页面名字：').secondary()
        self.page_name_le = MLineEdit().small()
        self.label_page_icon = MLabel(u'页面图标：').secondary()
        icon_list = ["alert_fill.svg", "big_view.svg", "calendar_line_dark.svg", "home_fill.svg"]
        icon_menu = MMenu()
        icon_menu.set_data(icon_list)
        self.icon_combobox = MComboBox().small()
        self.icon_combobox.set_menu(icon_menu)
        self.tab_left = MLineTabWidget()
        self.button = MPushButton(text='Finish')

        label_lay1 = QHBoxLayout()
        label_lay1.addWidget(self.label_page_name)
        label_lay1.addWidget(self.page_name_le)
        label_lay1.addWidget(self.splitter)
        label_lay1.addWidget(self.label_page_icon)
        label_lay1.addWidget(self.icon_combobox)
        main_lay = QVBoxLayout()
        main_lay.addLayout(label_lay1)
        main_lay.addWidget(MDivider(u''))
        main_lay.addWidget(self.tab_left)
        main_lay.addWidget(self.button)
        self.setLayout(main_lay)
        self.button.clicked.connect(self.get_table_data)

    @property
    def page_name(self):
        return self.page_name_le.text()

    @property
    def page_icon(self):
        return self.icon_combobox.currentText()

    def set_text(self, cfg):
        import importlib
        self.page_setting.update(page_type=cfg["page_type"])
        actions_function = importlib.import_module('SystemTools.Autumn.core.actions.' + self.project_name + '.actions_register')
        reload(actions_function)
        project_action = actions_function.actions_dict
        self.page_name_le.setText(cfg["page_name"])
        self.register_field('button2_selected', [cfg["page_svg"]])
        self.bind('button2_selected', self.icon_combobox, 'value', signal='sig_value_changed')
        for key, value in self.tab_page_name.items():
            if value == "page_filters":
                header_data = [{'label': u"字段", 'key': "fields", "editable": "True"},
                               {'label': u"关系", 'key': "conditions", "editable": "True"},
                               {'label': u"筛选条件", 'key': "relationship", "editable": "True"}]
                table_data_filters = []
                for data_f in cfg[value]:
                    data_dict = {"fields": data_f[0], "conditions": data_f[1], "relationship": data_f[2]}
                    table_data_filters.append(data_dict)
                self.add_page(key, value, header_data, table_data_filters, mode=1)
            elif value == "page_actions":
                header_data = [{'label': u"动作名称", 'key': "label"},
                               {'label': u"图标", 'key': "icon"},
                               {'label': u"mode", 'key': "mode"},
                               {'label': u"参数", 'key': "value"},
                               {'label': u"是否启用", 'key': "enable", 'checkable': True, 'searchable': False}]
                table_data_actions = []
                actions_dict = project_action.get(self.project_name)
                for actions_data in actions_dict[cfg["page_type"]]:
                    data = actions_data
                    if data in cfg[value]:
                        data["enable_checked"] = 2
                        table_data_actions.append(data)
                    else:
                        data["enable_checked"] = 0
                        table_data_actions.append(data)
                self.add_page(key, value, header_data, table_data_actions)
            elif value == "page_fields":
                header_data = [{'label': u"标签", 'key': "label", "editable": "True"},
                               {'label': u"对应字段", 'key': "key", "editable": "True"},
                               {'label': u"标签顺序", 'key': "order", "editable": "True"},
                               {'label': u"searchable", 'key': "searchable", "editable": "True"},
                               {'label': u"颜色规则", 'key': "color", "editable": "True"}
                               ]
                fields_table_data = []
                for v in cfg[value]:
                    if v["label"] in cfg["page_fields_order"].keys():
                        v["order"] = cfg["page_fields_order"][v["label"]]
                        fields_table_data.append(v)
                    else:
                        v["order"] = ""
                        fields_table_data.append(v)
                self.add_page(key, value, header_data, fields_table_data, mode=1)
            elif value == "detail_page_actions":
                header_data = [{'label': u"动作名称", 'key': "label"},
                               {'label': u"图标", 'key': "icon"},
                               {'label': u"mode", 'key': "mode"},
                               {'label': u"参数", 'key': "value"},
                               {'label': u"是否启用", 'key': "enable", 'checkable': True, 'searchable': False}]
                table_data_actions = []
                try:
                    for actions_data in actions_dict["Version"]:
                        data = actions_data
                        if data in cfg[value]:
                            data["enable_checked"] = 2
                            table_data_actions.append(data)
                        else:
                            data["enable_checked"] = 0
                            table_data_actions.append(data)
                except:
                    for actions_data in actions_dict["Version"]:
                        data = actions_data
                        data["enable_checked"] = 0
                        table_data_actions.append(data)
                self.add_page(key, value, header_data, table_data_actions)

    def add_page(self, p_name, page_name_label, header_data, data, mode=0):
        sheet = TableWidget()
        if mode == 0:
            self.tab_left.add_tab(sheet, {'text': p_name, 'svg': 'calendar_line.svg'})
        if mode == 1:
            self.tab_left.add_tab(sheet, {'text': p_name, 'svg': 'calendar_line.svg'})
            sheet.add_button.show()
            sheet.delete_button.show()
            sheet.add_button.clicked.connect(lambda: self.add_table(header_data))
            sheet.delete_button.clicked.connect(self.delete_table)
        if page_name_label == "page_filters":
            sheet.confirm_button.show()
            sheet.confirm_button.clicked.connect(lambda: self.confirm_data(page_name_label))
        table_info = [sheet, page_name_label]
        self.pages.append(table_info)
        sheet.data_model.set_header_list(header_data)
        sheet.model_sort.set_header_list(header_data)
        sheet.data_table.set_header_list(header_data)
        sheet.data_model.set_data_list(data)

    def get_table_data(self):
        for p in self.pages:
            table_filters_data = p[0].data_model.get_data_list()
            if p[1] == "page_filters":
                filters_data_list = []
                for data_filters in table_filters_data:
                    if data_filters["fields"] and data_filters["conditions"] and data_filters["relationship"]:
                        data_list = [str(data_filters["fields"]), str(data_filters["conditions"]), str(data_filters["relationship"])]
                        filters_data_list.append(data_list)
                self.page_setting["page_filters"] = filters_data_list
            elif p[1] == "page_actions":
                data_actions_list = []
                for data_actions in table_filters_data:
                    data_dict = {}
                    if data_actions["enable_checked"] == 2:
                        data_dict.update(icon=data_actions["icon"], label=data_actions["label"],
                                         mode=data_actions["mode"], value=data_actions["value"])
                        data_actions_list.append(data_dict)
                self.page_setting["page_actions"] = data_actions_list
            elif p[1] == "detail_page_actions":
                data_page_actions_list = []
                for data_actions in table_filters_data:
                    data_dict = {}
                    if data_actions["enable_checked"] == 2:
                        data_dict.update(icon=data_actions["icon"], label=data_actions["label"],
                                         mode=data_actions["mode"], value=data_actions["value"])
                        data_page_actions_list.append(data_dict)
                if data_page_actions_list:
                    self.page_setting["detail_page_actions"] = data_page_actions_list
            elif p[1] == "page_fields":
                fields_order = {}
                data_fields_list = []
                for data_fields in table_filters_data:
                    if data_fields["key"] and data_fields["label"]:
                        fields_dict = {}
                        color_func = data_fields.get("color", None)
                        color_func_name = color_func
                        if color_func and not isinstance(color_func, unicode):
                            color_func_name = color_func.__name__
                        fields_dict.update(key=data_fields["key"], label=data_fields["label"],
                                           searchable=data_fields["searchable"], color=color_func_name)
                        data_fields_list.append(fields_dict)
                        fields_order[data_fields["label"]] = data_fields["order"]
                #  将fields的列表顺序重排
                new_data_fields_list = []
                new_fields_order_temp = zip(fields_order.values(), fields_order.keys())
                new_fields_order = sorted(new_fields_order_temp, key=lambda x: int(x[0] or 0))
                for each_order_tuple in new_fields_order:
                    for each_field in data_fields_list:
                        if each_field['label'] == each_order_tuple[1]:
                            new_data_fields_list.append(each_field)
                            break
                #  重排结束
                self.page_setting["page_fields"] = new_data_fields_list
                self.page_setting["page_fields_order"] = fields_order
        self.page_setting.update(page_name=self.page_name, page_svg=self.page_icon)
        # pprint(self.page_setting)
        text_str = json.dumps(self.page_setting, indent=4)
        self.edit_result_sig.emit(text_str)

    def add_table(self, header_data):
        data_dict = {}
        for h in header_data:
            data_dict[h["key"]] = ""
        self.tab_left.stack_widget.currentWidget().data_model.append(data_dict)

    def delete_table(self):
        selected_indexes = self.tab_left.stack_widget.currentWidget().data_table.selectedIndexes()
        rows = list(set([index.row() for index in selected_indexes]))
        for i in rows:
            self.tab_left.stack_widget.currentWidget().data_model.removeRow(i)

    def confirm_data(self, page_name):
        if page_name == "page_filters":
            relationship_list = []
            valid_dic = sg.valid_operators()
            for key, value in valid_dic.items():
                for v in value:
                    if v not in relationship_list:
                        relationship_list.append(v)
            text_str = json.dumps(relationship_list, indent=4)
            relationship_win = ResourcesWin(self)
            relationship_win.set_text(text_str)
            relationship_win.show()


class UIMain(QMainWindow):

    def __init__(self, parent=None):
        super(UIMain, self).__init__(parent)
        self.resize(1500, 800)
        # self.setMinimumSize(1500, 1000)
        self.setWindowIcon(MIcon(os.environ['oct_toolkits_path']+'/icons/autumn.svg', dayu_theme.primary_color))
        self.config = {}
        self.pages = []
        self.page_names = []
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle('Autumn v1.0 Beta')
        self.central_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.central_widget)

        self.tool_bar = QToolBar(parent=self)
        self.tool_bar.setFloatable(False)
        self.tool_bar.setMovable(False)
        self.addToolBar(self.tool_bar)
        self.create_page_action = \
            self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/add_line_dark.svg', dayu_theme.primary_color), u'Create')
        self.copy_page_action = \
            self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/float_dark.svg', dayu_theme.primary_color), u'Copy')
        self.load_cfg_action = \
            self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/down_line_dark.svg', dayu_theme.primary_color), u'Load')
        self.refresh_action = self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/refresh_line.svg', dayu_theme.primary_color),
                                                   u'Refresh')
        self.edit_config_action = self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/edit_line.svg', dayu_theme.primary_color),
                                                      u'Edit')
        self.help_action = \
            self.tool_bar.addAction(MIcon(os.environ['oct_toolkits_path']+'/icons/confirm_line_dark.svg', dayu_theme.primary_color), u'Help')
        # 主界面， splitter
        self.h_layout_2 = QHBoxLayout()
        self.splitter_main = QSplitter()
        self.splitter_main.setOrientation(Qt.Horizontal)
        self.filters_widget = QWidget(self.splitter_main)
        self.filters_main_layout = QVBoxLayout()
        self.filters_layout_out = QVBoxLayout()
        self.filters_layout_in = QVBoxLayout()
        self.filters_layout_out.addLayout(self.filters_layout_in)

        #  这个控件用于翻页filter page
        self.filter_st = QStackedWidget(self)
        self.filters_layout_in.addWidget(self.filter_st)
        self.add_filter_pb = MPushButton(u'+').small()
        add_filter_pb_layout = QHBoxLayout()
        add_filter_pb_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        add_filter_pb_layout.addWidget(self.add_filter_pb)
        add_filter_pb_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.filters_layout_in.addLayout(add_filter_pb_layout)

        self.add_filter_pb.setMaximumWidth(30)
        self.filters_layout_in.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.pb_layout = QHBoxLayout()
        self.save_page_pb = MToolButton().svg('detail_line.svg').text_beside_icon()
        self.save_page_pb.setText('Save')
        self.save_page_pb.setStyleSheet('background-color: rgb(91, 173, 90);')
        self.delete_page_pb = MToolButton().svg('trash_line.svg').text_beside_icon()
        self.delete_page_pb.setText('Delete')
        self.delete_page_pb.setStyleSheet('background-color: rgb(157, 90, 90);')
        self.pb_layout.addWidget(self.save_page_pb)
        self.pb_layout.addWidget(self.delete_page_pb)
        self.filters_widget.setLayout(self.filters_main_layout)
        self.filters_main_layout.addWidget(MDivider('Filters Editor'))
        self.filters_main_layout.addLayout(self.filters_layout_out)
        self.filters_layout_out.addLayout(self.pb_layout)
        self.filters_widget.resize(70, 99)
        #  增加tab
        sheet_widget = QWidget(self.splitter_main)
        sheet_widget.resize(1000, 900)
        sheet_layout = QHBoxLayout()
        sheet_widget.setLayout(sheet_layout)
        self.sheet_tab = MLineTabWidget()
        sheet_layout.addWidget(self.sheet_tab)
        #  增加详情页
        self.detail_page = detail_page_ui.DetailPage(parent=self.splitter_main, task_dict={})
        self.h_layout_2.addWidget(self.splitter_main)
        self.grid_layout.addLayout(self.h_layout_2, 2, 0)
        self.setCentralWidget(self.central_widget)

        #  connecting to slots

        self.add_filter_pb.clicked.connect(self.add_filter)  # 增加过滤条件
        self.sheet_tab.stack_widget.currentChanged.connect(self.change_current_page)  # 当前页面发生变更时需要切换filter页面
        self.create_page_action.triggered.connect(self.create_new_page)  # 新建页面
        self.copy_page_action.triggered.connect(self.copy_page)
        self.refresh_action.triggered.connect(self.refresh_current_page)
        self.edit_config_action.triggered.connect(self.edit_current_page_cfg)
        self.load_cfg_action.triggered.connect(self.load_cfg)
        self.save_page_pb.clicked.connect(self.save_config)  # 保存配置
        self.delete_page_pb.clicked.connect(self.delete_page)

        self.fetching_batch_show = detail_page.ShowDetailInfo()
        self.fetching_batch_show.progress.connect(self.get_data)
        self.fetching_batch_show.finished.connect(self.finish)


    def edit_current_page_cfg(self):
        if not self.current_page:
            return
        edit_cfg_win = EditCfgWin(parent=self)
        cfg = self.current_page.get_config().copy()
        edit_cfg_win.set_text(cfg)
        edit_cfg_win.edit_result_sig.connect(self.get_edit_cfg_result)
        edit_cfg_win.show()
        pass

    def get_edit_cfg_result(self, cfg):
        # cfg = cfg.replace("'", '"')
        self.current_page.set_config(json.loads(cfg))
        self.current_page.parse_config()

    def refresh_current_page(self):
        if not self.current_page:
            return
        self.current_page.parse_config()

    def create_new_page(self):
        from create_table_form import CreateTableForm
        create_window = CreateTableForm(parent=self)
        create_window.tableInfo.connect(self.get_fields)
        create_window.show()

    def load_cfg(self):
        load_win = SaveLoadConfig(parent=self)
        load_win.save_doit_btn.setText('Load')
        cfg_list = shotgun_operations.get_autumn_config_codes(self.project)
        load_win.set_items(cfg_list)
        load_win.cfg_name_sig.connect(self.load_code_cfg)
        load_win.show()

    def load_code_cfg(self, cfg_name):
        cfg = shotgun_operations.get_autumn_config(cfg_name)
        self.parse_config(cfg)

    def copy_page(self):
        if not self.current_page:
            return
        copy_page_window = CopyPageWin(parent=self)
        copy_page_window.show()
        copy_page_window.new_page_name_sig.connect(self.get_copy_page_name)
        pass

    def get_copy_page_name(self, name):
        if name in self.page_names:
            MMessage.config(2)
            MMessage.error(u'Page existed!! Please input another name!', parent=self)
            return
        config = self.current_page.get_config().copy()
        config['page_name'] = name
        copied_page = self.add_sheet(config)
        copied_page.parse_config()
        self.sheet_tab.tool_button_group.set_dayu_checked(self.sheet_tab.stack_widget.count() - 1)

    def add_filter(self):
        #  该函数用于唤起filter窗口
        if not self.current_page:
            return
        from filter_form import FilterWindow
        page_fields = self.current_page.get_config()['page_fields']
        page_fields_dict = {}
        for each in page_fields:
            page_fields_dict[each['label']] = each['key']
        filter_win = FilterWindow(fields_box=page_fields_dict, parent=self)
        filter_win.show()
        filter_win.filterInfo.connect(self.get_filters)

    def delete_filters(self, filter_item):
        # self.current_page.clear()
        left_filters = [f for f in self.current_page.get_config()['page_filters'] if
                        f not in filter_item.filter_content]
        filter_item.hide()
        self.current_page.update_filters(
            {'page_filters': left_filters})
        self.current_page.parse_config()

    def get_filters(self, filters):
        # 槽，filters
        if not self.current_page:
            return
        useful_filters = [f for f in filters if f not in self.current_page.get_config()['page_filters']]
        if not useful_filters:
            # self.current_page.update_filters(self.current_page.get_config()['page_filters'])
            # self.current_page.parse_config()
            return
        filter_item = FilterItem(filter_content=useful_filters)
        self.filter_st.currentWidget().current_layout.addWidget(filter_item)
        filter_item.delete_item_btn.clicked.connect(functools.partial(self.delete_filters, filter_item))
        self.current_page.update_filters({'page_filters': (useful_filters+self.current_page.get_config()['page_filters'])})
        self.current_page.parse_config()

    def add_sheet(self, config):
        #  新建filter页面
        filter_widget = QWidget(parent=self.filter_st)
        filter_layout_out = QVBoxLayout()
        filter_layout = QVBoxLayout()
        filter_layout_out.addLayout(filter_layout)
        filter_layout_out.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        filter_widget.setLayout(filter_layout_out)
        self.filter_st.addWidget(filter_widget)
        filter_widget.current_layout = filter_layout
        #  增加搜索框
        search_le = MLineEdit().search().small()
        filter_layout.addWidget(search_le)
        #  建立page
        sheet = SheetContent(self)
        sheet.show_msg = True
        # sheet.table.setFixedHeight(970)
        sheet.table.clicked.connect(self.get_table_data)
        sheet.project = self.project
        sheet.user = self.user
        sheet.set_config(config)
        self.sheet_tab.add_tab(sheet, {'text': config['page_name'], 'svg': config['page_svg']})
        # self.sheet_tab.tool_button_group.set_dayu_checked(self.sheet_tab.stack_widget.count() - 1)
        # search_le.textChanged.connect(sheet.model_sort.set_search_pattern)
        search_le.editingFinished.connect(functools.partial(self.set_sheet_data, sheet, search_le))
        self.pages.append(sheet)
        self.page_names.append(sheet.name)
        return sheet

    def get_table_data(self):
        action_param = {}
        table_data = self.sheet_tab.stack_widget.currentWidget()
        row = table_data.table.currentIndex().row()
        task_id = table_data.model_sort.index(row, 0).data()
        action_param['id'] = [int(task_id)]
        action_param['project'] = shotgun_operations.get_project()
        action_param['user'] = shotgun_operations.get_user()
        action_param['type'] = "Task"
        action_param['widget'] = atu.get_widget_top_parent(self)
        action_param['config'] = table_data.get_config()
        self.fetching_batch_show.task_info_list = action_param
        if self.fetching_batch_show.mute != 1:
            self.finish(finished=True)
        self.fetching_batch_show.start()

    def get_data(self, data):
        # if not data["_id"]:
        #     MMessage.config(1)
        #     MMessage.error(u'没有最新版本的信息！', parent=self)
        mov_path = data["preview_file"]
        self.detail_page.set_playing_video(mov_path)
        self.detail_page.preview_widget_Video.media.finished.connect(self.detail_page.playback)
        self.detail_page.set_table_info(data)
        self.detail_page.mime_data_table.fetch_data_thread.result_sig.connect(self.detail_page.set_table)
        self.detail_page.set_mime_data(data)
      # self.fetching_batch_show.mute = 0 # 表示线程启动

    def finish(self, finished):
        if finished:
            self.fetching_batch_show.wait()
            self.fetching_batch_show.quit()
            self.fetching_batch_show.mute = 1

    def set_sheet_data(self, sheet, search_le):
        if sheet.data:
            sheet.model_sort.set_search_pattern(search_le.text())
            # sheet.model.set_data_list(sheet.data)

    def change_current_page(self, index):
        self.filter_st.setCurrentIndex(index)
        if self.current_page and not self.current_page.is_load:
            self.current_page.parse_config()
            for each in self.current_page.get_config()['page_filters']:
                filter_item = FilterItem(filter_content=[each])
                self.filter_st.currentWidget().current_layout.addWidget(filter_item)
                filter_item.delete_item_btn.clicked.connect(functools.partial(self.delete_filters, filter_item))

    @property
    def user(self):
        # return 'TD_Group'
        return shotgun_operations.get_user()

    @property
    def project(self):
        # return 'Demo: Animation'  #
        return shotgun_operations.get_project()

    @property
    def current_page(self):
        return self.sheet_tab.stack_widget.currentWidget()

    def get_fields(self, field_dict):
        #  槽，获取fields
        if field_dict['page_name'] in self.page_names:
            MMessage.config(3)
            MMessage.error(u'已经存在该页面，无法重复创建！', parent=self)
            return
        self.page_names.append(field_dict['page_name'])
        field_dict.update({'page_svg': 'calendar_line.svg', 'page_filters': [], 'page_actions': None})
        self.add_sheet(field_dict)
        self.sheet_tab.tool_button_group.set_dayu_checked(self.sheet_tab.stack_widget.count() - 1)
        self.filter_st.setCurrentIndex(self.sheet_tab.stack_widget.currentIndex())
        self.current_page.parse_config()

    def save_config(self):
        save_win = SaveLoadConfig(parent=self)
        cfg_list = shotgun_operations.get_autumn_config_codes(self.project)
        save_win.set_items(cfg_list)
        save_win.cfg_name_sig.connect(self.save_cfg_doit)
        save_win.show()
        # with codecs.open(filename=config_path, mode='w', encoding='utf-8') as config:
        #     json.dump(self.config, config, ensure_ascii=False, indent=4)

    def deal_recursion(self, input_dict, dealed_strs=None):
        if dealed_strs is None:
            dealed_strs = ['_parent', 'reg']
        if isinstance(input_dict, dict):
            new_dict = {}
            for k, v in input_dict.iteritems():
                if k not in dealed_strs:
                    new_dict[k] = v
            return {nk: self.deal_recursion(nv, dealed_strs=dealed_strs) for nk, nv in new_dict.iteritems()}
        elif isinstance(input_dict, list):
            return [self.deal_recursion(element, dealed_strs=dealed_strs) for element in input_dict]
        elif isinstance(input_dict, unicode):
            return input_dict
        elif 'function' in str(type(input_dict)):
            return input_dict.__name__
        else:
            return input_dict

    def save_cfg_doit(self, cfg_code):
        config_temp = dict()
        list_temp = []
        for each in self.pages:
            # if not each.isHidden():
            cfg_temp_1 = each.get_config().copy()
            # for ff in cfg_temp['page_fields']:
            #     if 'reg' in ff.keys():
            #         del ff['reg']
            cfg_temp = self.deal_recursion(cfg_temp_1)
            cfg_temp_key = cfg_temp['page_name'][:]
            cfg_temp_value = copy.deepcopy(cfg_temp)
            list_temp.append({cfg_temp_key: cfg_temp_value})
        config_temp['autumn_config'] = list_temp
        standard_cfg = self.deal_recursion(config_temp)
        config_str = json.dumps(standard_cfg)
        self.config = standard_cfg.copy()
        shotgun_operations.set_autumn_config(cfg_code, config_str)
        MMessage.config(2)
        MMessage.success(u'保存配置成功！', parent=self)

    def load_user_config(self, user):
        temp_config = {'autumn_config': []}
        config_list = shotgun_operations.get_user_autumn_config(user)
        if not config_list:
            MMessage.config(2)
            MMessage.error(u'该账户没有查看权限！请联系TD..', parent=atu.get_widget_top_parent(self))
            return
        final_cfg = {}
        page_name_list = []
        for each_cfg_str in config_list:
            each_cfg = json.loads(each_cfg_str)
            for each_autumn_cfg in each_cfg.values()[0]:
                page_name, page_cfg = each_autumn_cfg.keys()[0], each_autumn_cfg.values()[0]
                if page_name not in page_name_list:
                    page_name_list.append(page_name)
                # for page_name, page_cfg in each_cfg.items():
                if page_name not in final_cfg.keys():
                    final_cfg[page_name] = page_cfg
                else:
                    existed_fields = final_cfg[page_name]['page_fields'] or []
                    new_fields = page_cfg['page_fields'] or []
                    final_fields = []
                    for field in existed_fields + new_fields:
                        if field not in final_fields:
                            final_fields.append(field)
                    final_cfg[page_name]['page_fields'] = final_fields

                    existed_filters = final_cfg[page_name]['page_filters'] or []
                    new_filters = page_cfg['page_filters'] or []
                    final_filter = []
                    for filters in existed_filters + new_filters:
                        if filters not in final_filter:
                            final_filter.append(filters)
                    final_cfg[page_name]['page_filters'] = final_filter

                    existed_actions = final_cfg[page_name]['page_actions'] or []
                    new_actions = page_cfg['page_actions'] or []
                    final_actions = []
                    for action in existed_actions + new_actions:
                        if action not in final_actions:
                            final_actions.append(action)
                    final_cfg[page_name]['page_actions'] = final_actions
                # self.config['autumn_config'].append({page_name: final_cfg[page_name]})
        for p_name in page_name_list:
            pcfg = final_cfg.get(p_name)
            temp_config['autumn_config'].append({p_name: pcfg})
        # for pn, pcfg in final_cfg.items():
        #     temp_config['autumn_config'].append({pn: pcfg})
        self.config = self.deal_recursion(temp_config)
        return self.config
        # self.config = final_cfg

    def parse_config(self, config):
        if config:
            # print self.config
            #  把unicode转成json字典
            config_temp = config
            if isinstance(config, unicode):
                config_temp = json.loads(config)
            # 处理颜色问题， 把字典中字符串的值转为函数对象
            new_config = config_temp.values()[0]
            for each_cfg in new_config:
                page_name = each_cfg.keys()[0]
                page_cfg = each_cfg.values()[0]
                new_fields = []
                for field in page_cfg.get('page_fields', []):
                    if 'color' in field.keys():
                        color_str = field.get('color', None)
                        # print color_str
                        if color_str:
                            field.update({'color': eval(color_str)})
                    new_fields.append(field)
                page_cfg.update({'page_fields': new_fields})
                self.page_names.append(page_cfg)
                #  转完直接添加这个页面
                self.add_sheet(page_cfg)
            # self.page_names = list(new_config.keys())
            # for page_name, page_config in new_config.items():
            #     self.add_sheet(page_config)
            #  设置当前页面为第一个页面
            self.sheet_tab.tool_button_group.set_dayu_checked(0)

    def delete_page(self):
        if self.current_page.name in self.page_names:
            self.page_names.remove(self.current_page.name)
        if self.current_page in self.pages:
            self.pages.remove(self.current_page)
        if self.current_page.name in self.config.keys():
            del self.config[self.current_page.name]  # 删掉config中的这一个页面
        for each in self.sheet_tab.tool_button_group.children():
            try:
                if each.text() == self.current_page.name:
                    each.hide()
            except Exception as e:
                print(e)
                pass
        self.filter_st.currentWidget().hide()
        self.current_page.hide()
        if self.sheet_tab.stack_widget.count():
            self.sheet_tab.tool_button_group.set_dayu_checked(0)


if __name__ == '__main__':
    import sys
    os.path.dirname(__file__) in sys.path or sys.path.append(os.path.dirname(__file__))
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = UIMain()
    dayu_theme.apply(test)
    import ctypes
    process_id = 'Autumn Desktop'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(process_id)
    # test.get_filters({})
    # pp.pprint(test.config)
    # print test.current_page.name
    # test.current_page.add_action('version_download', u'下载')
    test.show()
    # test.load_user_config()
    sys.exit(app.exec_())

