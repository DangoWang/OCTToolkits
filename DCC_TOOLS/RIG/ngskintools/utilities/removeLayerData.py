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

from ngSkinTools import selectionState
from ngSkinTools import utils
from ngSkinTools.layerUtils import LayerUtils
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.ui.events import LayerEvents
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.utils import Utils
from maya import cmds


@Utils.undoable
def removeAllNodes():
    if not LayerUtils.hasCustomNodes():
        utils.confirmDialog(icon='information', title='Info',
                            message='Scene does not contain any custom ngSkinTools nodes.', button=['Ok']);
        return

    message = 'This command deletes all custom ngSkinTools nodes. Skin weights will be preserved, but all layer data will be lost. Do you want to continue?'
    if utils.confirmDialog(
            icon='warning',
            title='Warning',
            message=message,
            button=['Yes', 'No'], defaultButton='No') != 'Yes':
        return

    LayerDataModel.getInstance().cleanCustomNodes()


@Utils.undoable
def removeLayersFromSelection():
    mll = MllInterface()
    target = mll.getTargetInfo()
    if target is None:
        return

    def asList(arg):
        if arg is None:
            return []
        return arg


    # delete any ngSkinTools deformers from the history, and find upstream stuff from given skinCluster.
    mesh,skinCluster = target
    hist = asList(cmds.listHistory(mesh))+asList(cmds.listHistory(skinCluster,future=True,levels=1))

    cmds.delete([i for i in hist if cmds.nodeType(i) in ('ngSkinLayerDisplay','ngSkinLayerData')])

    LayerDataModel.getInstance().updateLayerAvailability()
    selectionState.selectionInfo.dropCache()







