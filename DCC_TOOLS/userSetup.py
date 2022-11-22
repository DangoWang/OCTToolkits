import maya.cmds as cmds
import maya.OpenMaya as openMaya
import maya.utils as utils
import os
utils.executeDeferred('import maya_menu_set_up; import maya_menu_dict;maya_menu_set_up.arrange_menus(maya_menu_set_up.get_menus(), maya_menu_set_up.add_p_menu())')
# if os.environ['oct_launcher_using_mode'] in ['online']:
#     utils.executeDeferred('from DCC_TOOLS.common.work_log import open_close_event;open_close_event.main()')


# import DCC_TOOLS.maya_menu_set_up as maya_menu_set_up
# import DCC_TOOLS.maya_menu_dict as maya_menu_dict
# maya_menu_set_up.arrange_menus(maya_menu_set_up.get_menus(), maya_menu_set_up.add_p_menu())
# from DCC_TOOLS.common.work_log import open_close_event
# open_close_event.main()
