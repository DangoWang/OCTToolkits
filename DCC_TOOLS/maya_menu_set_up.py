#!/usr/bin/env python
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os

if os.environ['oct_launcher_using_mode'] in ['online']:
    import utils.shotgun_operations as sg
    import maya_menu_dict
    oct_tools_menu_register = maya_menu_dict.get_config('online')
    from utils import common_methods
    user = sg.get_user()
    steps = sg.get_step(user)
else:
    import maya_menu_dict
    oct_tools_menu_register = maya_menu_dict.get_config('offline')
    steps = None


def add_p_menu():
    if cmds.menu('oct_user_tools_menu', exists=True):
        cmds.deleteUI('oct_user_tools_menu')
    maya_main_window = mel.eval('$gMainWindow=$gMainWindow')
    p_menu = cmds.menu('oct_user_tools_menu', parent=maya_main_window, tearOff=True, aob=True, label='OCT-ToolBox')
    return p_menu


def get_menus():
    cfgs = oct_tools_menu_register['common']
    existed_func = []
    if steps:
        for s in steps:
            try:
                cfg_one = oct_tools_menu_register[s]
                for menu_list in cfg_one:
                    if 'label' in menu_list.keys() and menu_list['label'] and menu_list['label'] not in existed_func:
                        cfgs.append(menu_list)
                        existed_func.append(menu_list['label'])
            except KeyError:
                pass
    return cfgs


def arrange_menus(menus, p_menu):
    for c_menu in menus:
        if not c_menu['value']:
            cmds.menuItem(divider=True, parent=p_menu, label=c_menu['label'])
            continue
        elif isinstance(c_menu['value'], list):
            cmds.menuItem(c_menu['label'], subMenu=True, aob=1, tearOff=True,
                          parent=p_menu, label=c_menu['label'], image=c_menu['icon'])
            arrange_menus(c_menu['value'], c_menu['label'])
        else:
            cmds.menuItem(parent=p_menu, label=c_menu['label'], image=c_menu['icon'],
                          command='reload(maya_menu_dict);maya_menu_dict.%s()' % c_menu['value'])



