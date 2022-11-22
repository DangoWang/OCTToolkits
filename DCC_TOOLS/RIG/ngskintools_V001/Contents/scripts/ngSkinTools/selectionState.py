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

'''
Cached information about current selection
'''
from ngSkinTools.log import getLogger
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.stateStore import CachedValue
from ngSkinTools.ui.events import Signal, LayerEvents, MayaEvents

log = getLogger('selectionState')

mll = MllInterface()

# container for mirror related state
mirrorInfo = CachedValue('mirrorInfo', lambda: {
    'axis': mll.getMirrorAxis(),
})

# container for primary selection data
selectionInfo = CachedValue('selectionInfo', lambda: {
    'target': mll.getTargetInfo(),
    'layersAvailable': mll.getLayersAvailable(),
})


def getLayersAvailable():
    return selectionInfo.get()['layersAvailable']


def bind(signals, values):
    for signal in signals:
        for value in values:
            signal.addHandler(value.dropCache)


def bindAll():
    log.info("adding handlers to signals")
    bind(
        signals=[MayaEvents.nodeSelectionChanged, MayaEvents.undoRedoExecuted, LayerEvents.layerAvailabilityChanged],
        values=[selectionInfo, mirrorInfo])
    bind(
        signals=[LayerEvents.mirrorConfigurationChanged],
        values=[mirrorInfo])
