#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/1/28

try:
	from PySide2 import QtWidgets
except ImportError:
	from PySide import QtGui as QtWidgets
import yaml
import logging


def add_item(table_widget, label):
	if ":" in label:
		logging.error(u"控制器名中不能有名称空间（namespace）")
		return False
	row_count = table_widget.rowCount()
	# print row_count
	table_widget.setRowCount(row_count + 1)
	new_item = QtWidgets.QTableWidgetItem(label)
	table_widget.setItem(row_count, 0, new_item)
	# table_widget.removeRow(row_count)
	return True


def clear_all_items(table_widget):
	table_widget.setRowCount(0)
	return table_widget.clearContents()


def set_all_items(table_widget, item_label):
	# items_count = len(item_label)
	# if not items_count:
	# 	return False
	# table_widget.setRowCount(items_count)
	for each_label in item_label:
		add_item(table_widget, each_label)
	return True


def delete_items(table_widget):
	selected_items = table_widget.selectedItems()
	if not selected_items:
		raise RuntimeError("Plz select at least one item First!!")
	for i in selected_items:
		row = table_widget.indexFromItem(i).row()
		table_widget.removeRow(row)
	return True


def save_cfg(cfg_info, cfg_path):
	with open(cfg_path, 'w') as f:
		yaml.dump(cfg_info, f)
	logging.info("Successfully saved in %s" % cfg_path)
	return True


def get_contents(table_widget):
	row_count = table_widget.rowCount()
	ani_crv_contents = list()
	ani_crv = dict()
	for i in xrange(row_count):
		ani_crv_contents.append(table_widget.item(i, 0).text())
	ani_crv['AnimCrv'] = ani_crv_contents
	return ani_crv
