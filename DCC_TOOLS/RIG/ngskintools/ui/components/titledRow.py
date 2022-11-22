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
from ngSkinTools.ui.uiWrappers import FormLayout
from ngSkinTools.ui.constants import Constants

def createFixed(parent,title):
    '''
    similar to titled row, but not flexible and does not allow inner constructor or multiple elements inside;
    great for numeric fields, drop down fields, other non-stretchy UI elements
    '''
    return create(parent, title, adjustable=False)


def create(parent,title,innerContentConstructor=None,adjustable=True):
    '''
    creates a layout piece with a title and inner content layout
    '''
    
    result = FormLayout(parent=parent)
    
    if innerContentConstructor is None:
        innerContent = cmds.columnLayout(width=1)
        if adjustable:
            cmds.columnLayout(innerContent,e=True,adjustableColumn=1)
    else:  
        innerContent =  innerContentConstructor()
    
    
    result.attachForm(innerContent,0,0,None,Constants.MARGIN_COLUMN2)

    if title!=None:        
        label = cmds.text(parent=result,label=title+':',width=Constants.MARGIN_COLUMN2-Constants.MARGIN_SPACING_HORIZONTAL,align="right")
        result.attachForm(label, 0, None, 0, 0)
    
    if cmds.layout(innerContent,q=True,exists=True):
        cmds.setParent(innerContent)
    
    return result
