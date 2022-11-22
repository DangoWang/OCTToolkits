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

from maya import cmds,mel
from ngSkinTools import selectionState
from ngSkinTools.layerUtils import LayerUtils
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.log import getLogger
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.utilities.weightsClipboard import WeightsClipboard
from ngSkinTools.utils import Utils



class LayerDataModel:
    log = getLogger("layerDataModel")

    # holds instance of singleton object
    __instance = None
    
    @staticmethod
    def getInstance():
        '''
        returns singleton instance of LayerDataModel
        
        :rtype: LayerDataModel
        '''
        return LayerDataModel.__instance

    @classmethod
    def bindAll(cls):
        cls.__instance = LayerDataModel()

        MayaEvents.undoRedoExecuted.addHandler(cls.__instance.updateLayerAvailability)
        MayaEvents.nodeSelectionChanged.addHandler(cls.__instance.updateLayerAvailability)

        cls.__instance.updateLayerAvailability()

    def __init__(self):
        self.layerDataAvailable = None
        self.mll = MllInterface()
        self.clipboard = WeightsClipboard(self.mll)
        

    def setLayerListsUI(self,ui):
        self.layerListsUI = ui
    
    def getLayerListsUI(self):
        '''
        :rtype: LayerListsUI
        '''
        from ngSkinTools.ui import mainwindow
        mainWindow = mainwindow.MainWindow.getInstance()
        if mainWindow is None:
            return None
        return mainWindow.getLayersUI()
        
    def getSelectedLayer(self):
        listsUi = self.getLayerListsUI()
        if listsUi is None:
            return None
        return listsUi.getLayersList().getSelectedID()
    
    def getSelectedLayers(self):
        listsUi = self.getLayerListsUI()
        if listsUi is None:
            return []
        return listsUi.getSelectedLayers()
    
    def getSelectedInfluenceIds(self):
        listsUi = self.getLayerListsUI()
        if listsUi is None:
            return []
        return listsUi.getSelectedInfluenceIds()
    
    def updateLayerAvailability(self):
        '''
        checks if availability of skin layers changed with the 
        current scene selection 
        '''
        self.log.info("updating layer availability")
        

        oldValue = self.layerDataAvailable
        self.layerDataAvailable = self.mll.getLayersAvailable()
        if self.layerDataAvailable!=oldValue:
            LayerEvents.layerAvailabilityChanged.emit()
            
    @Utils.undoable    
    def addLayer(self,name):
        def guessParent():
            currentLayer = self.mll.getCurrentLayer()
            if currentLayer is None:
                return None
            # guess layer's new parent
            parentsByLayerId = dict([(layerId,parentId) for layerId,_,parentId in self.mll.listLayers() if currentLayer in (layerId,parentId)])
            
            # current layer is a parent?
            if currentLayer in parentsByLayerId.values():
                return currentLayer
            
            # current layer has parent
            if currentLayer in parentsByLayerId.keys():
                return parentsByLayerId[currentLayer]
        
        layerId = self.mll.createLayer(name)
        self.mll.setLayerParent(layerId, guessParent())
        
        if layerId is None:
            return None
        
         
        
        
        
        LayerEvents.layerListModified.emit()
        
        self.setCurrentLayer(layerId)
        return layerId
        
    def removeLayer(self,layerId):
        self.mll.deleteLayer(layerId)
        LayerEvents.layerListModified.emit()
        LayerEvents.currentLayerChanged.emit()
        
        
    def setCurrentLayer(self,layerId):
        self.mll.setCurrentLayer(layerId)
        LayerEvents.currentLayerChanged.emit()
        
    def getCurrentLayer(self):
        return self.mll.getCurrentLayer()
        
    def attachLayerData(self):
        self.mll.initLayers()
        with self.mll.batchUpdateContext():
            self.addLayer('Base Weights')

        
        self.updateLayerAvailability()
        selectionState.selectionInfo.dropCache()

        
        
    def cleanCustomNodes(self):
        '''
        removes all custom nodes from current scene
        '''

        # just in case we were in the middle of painting
        cmds.setToolTo('selectSuperContext')

        LayerUtils.deleteCustomNodes()

        # notify the rest of the world
        self.updateLayerAvailability()
        selectionState.selectionInfo.dropCache()

    def getLayerName(self,layerId):
        return mel.eval('ngSkinLayer -id {0} -q -name'.format(int(layerId)))       
    
    def setLayerName(self,layerId,name):
        self.mll.setLayerName(layerId,name)
        LayerEvents.nameChanged.emit()   

    def getLayerOpacity(self,layerId):
        return mel.eval('ngSkinLayer -id {0} -q -opacity'.format(layerId))

    def getLayerEnabled(self,layerId):
        return mel.eval('ngSkinLayer -id {0} -q -enabled'.format(layerId))
    
    def setLayerEnabled(self,layerId,enabled):
        cmds.ngSkinLayer(e=True,id=layerId,enabled=1 if enabled else 0)
        
    def toggleLayerEnabled(self,layerId):
        self.setLayerEnabled(layerId, not self.getLayerEnabled(layerId))
            
    def getLayersCandidateFromSelection(self):
        '''
        for given selection, returns mesh and skin cluster node names where skinLayer data
        is (or can be) attached. 
        '''
        return self.mll.getTargetInfo()

    
    def getLayersAvailable(self):
        self.updateLayerAvailability()
        return self.layerDataAvailable
    
    def isDqMode(self):
        '''
        returns True if current skin cluster is operating in dual quaternion mode
        '''
        target = self.mll.getTargetInfo()
        if not target:
            return False   
        skinCluster = target[1]     
        return cmds.skinCluster(skinCluster,q=True,skinMethod=True)==2    
        
