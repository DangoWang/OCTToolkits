#
#    ngSkinTools
#    Copyright (c) 2009-2017 Viktoras Makauskas.
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by EULA.
#         
#    A copy of EULA can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from maya import cmds
from ngSkinTools.ui import uiWrappers
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.options import Options

def create(parent,title,defaultCollapsed=False):
    '''
    creates collapsable UI group
    '''
    cmds.setParent(parent)
    
    optionName = "ngSkinTools_group%s_collapse" % title.replace(" ", "") 
    
    def saveState():
        Options.saveOption(optionName, cmds.frameLayout(group,q=True,collapse = True))
    
    
    group = uiWrappers.frameLayout(label=title, marginWidth=Constants.MARGIN_SPACING_HORIZONTAL,marginHeight=Constants.MARGIN_SPACING_VERTICAL, collapsable=True,
                             expandCommand=saveState,collapseCommand=saveState)
    
    cmds.frameLayout(group,e=True,collapse = Options.loadOption(optionName, 1 if defaultCollapsed else 0))
    return cmds.columnLayout(adjustableColumn=1,rowSpacing=Constants.MARGIN_SPACING_VERTICAL)
    

