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

import ngSkinTools.ui.qtCompatibility as qt 
    

def ngLayerPaintCtxInitialize(shape):
    '''
    a wrapper for paint stroke start, feeding in the CTRL/Shift keyboard modifiers 
    for the next brush
    '''
    kargs = {}
    keyboardState = qt.widgets.QApplication.keyboardModifiers()
    kargs['shift'] = bool(keyboardState & qt.QtCore.Qt.ShiftModifier)
    kargs['control'] = bool(keyboardState & qt.QtCore.Qt.ControlModifier)
        
    return cmds.ngLayerPaintCtxInitialize(shape,**kargs)