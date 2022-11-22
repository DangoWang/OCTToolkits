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

from ngSkinTools.ui.basetoolwindow import BaseToolWindow
from maya import cmds
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.components import uiGroup
from ngSkinTools.ui.components.influencesManualMapping import InfluencesManualMapping
from ngSkinTools.ui.components.influencesMappingPreview import InfluencesMappingPreview
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.ui.uiWrappers import FloatField, StoredTextEdit,\
    DropDownField, CheckBoxField, RadioButtonField
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.constants import Constants
from ngSkinTools.utils import Utils
from ngSkinTools.log import getLogger
from ngSkinTools.influenceMapping import InfluenceMapping
from ngSkinTools.mllInterface import MllInterface
from ngSkinTools.orderedDict import OrderedDict


log = getLogger("initTransferWindow")


class CopyWeightsModel(object):
    vertexTransferModes = OrderedDict((
        ("Closest point on surface", "closestPoint"),
        ("UV space", "uvSpace"),
        ("By Vertex ID", "vertexId"),
    ))

    def __init__(self):
        self.parent = None
        self.sourceModel = None
        self.sourceMesh = None
        self.targetMesh = None

    def isEnabled(self):
        def validMesh(mesh):
            return mesh is not None and cmds.objExists(mesh)

        return (self.sourceModel is not None or validMesh(self.sourceMesh)) and validMesh(self.targetMesh)

    def buildInfluenceMappingEngine(self, controls):
        '''
        builds influence transfer mapping, using parameters from UI
        '''

        mapper = self.mapper = InfluenceMapping()
        mapper.mirrorMode = False
        self.mapper.distanceMatchRule.maxThreshold = float(controls.influenceDistanceError.getValue());

        mapper.nameMatchRule.ignoreNamespaces = controls.ignoreNamespaces.getValue() == 1

        mapper.rules = [mapper.distanceMatchRule, mapper.nameMatchRule]
        if self.sourceModel is not None:
            mapper.sourceInfluences = self.sourceModel.influences;
        else:
            mapper.sourceInfluences = MllInterface(mesh=self.sourceMesh).listInfluenceInfo();

        mapper.destinationInfluences = MllInterface(mesh=self.targetMesh).listInfluenceInfo()

        return mapper

    def inputValuesChanged(self):
        self.parent.updateLayoutEnabled()
        self.parent.previewInfluenceMapping()

    def setSourceData(self, model):
        '''
        use LayerData model as source
        '''
        self.sourceModel = model
        self.inputValuesChanged()

    def setSourceMesh(self, mesh):
        self.sourceMesh = mesh
        self.inputValuesChanged()

    def ensureTargetMeshLayers(self):
        targetMll = MllInterface(mesh=self.targetMesh)
        if not targetMll.getLayersAvailable():
            targetMll.initLayers()
            # targetMll.createLayer("weights before import")

    def setDestinationMesh(self, mesh):
        self.targetMesh = mesh
        self.ensureTargetMeshLayers()

        self.inputValuesChanged()

    @Utils.undoable
    def execute(self):
        targetMll = MllInterface(mesh=self.targetMesh)

        self.ensureTargetMeshLayers()

        previousLayerIds = [layer[0] for layer in targetMll.listLayers()]

        sourceMesh = self.sourceMesh
        if self.sourceModel is not None:
            self.sourceModel.saveTo(MllInterface.TARGET_REFERENCE_MESH)
            sourceMesh = MllInterface.TARGET_REFERENCE_MESH

        vertexTransferMode = self.vertexTransferModes[self.parent.controls.transferMode.getSelectedText()]

        sourceMll = MllInterface(mesh=sourceMesh)

        with targetMll.batchUpdateContext():
            sourceMll.transferWeights(self.targetMesh, influencesMapping=self.mapper.mapping,
                                      vertexTransferMode=vertexTransferMode)

            if self.parent.controls.keepExistingLayers.getValue() != 1:
                for layerId in previousLayerIds:
                    targetMll.deleteLayer(layerId)

        LayerDataModel.getInstance().updateLayerAvailability()
        LayerEvents.layerListModified.emit()

class TransferWeightsTab(BaseTab):
    log = getLogger("Transfer Weights Tab")
    VAR_PREFIX = 'ngSkinToolsTransferTab_'
    
    axisValues = ('X','Y','Z')
    
    def __init__(self):
        BaseTab.__init__(self)
        self.dataModel = CopyWeightsModel()
        self.dataModel.parent = self
        self.currentSelection = None

        self.influenceMappingPreview = InfluencesMappingPreview()
        self.influencesManualMapping = InfluencesManualMapping()

    def createUI(self, parent):
        buttons = [
            ('Done', self.execContinue,''),
            ('Cancel', self.closeWindow,'')
        ]

        self.cmdLayout = self.createCommandLayout(buttons,SkinToolsDocs.INITWEIGHTTRANSFER_INTERFACE)
        
        self.createTransferOptionsGroup()
        self.createInfluenceMappingGroup()

        LayerEvents.layerAvailabilityChanged.addHandler(self.updateLayoutEnabled,self.cmdLayout.outerLayout)
        MayaEvents.nodeSelectionChanged.addHandler(self.updateUIValues, self.cmdLayout.outerLayout)

        self.updateLayoutEnabled()
        self.updateUIValues()
        self.updatePreferedValues()
        
    def releaseUI(self):
        LayerEvents.layerAvailabilityChanged.removeHandler(self.updateLayoutEnabled)
        MayaEvents.nodeSelectionChanged.removeHandler(self.updateUIValues)
        
    def updatePreferedValues(self):
        self.influencesManualMapping.manualOverrides = {}

    def updateUIValues(self):
        # when selection changes between update UI calls, overwrite UI with preferred values in the mesh
        selection = cmds.ls(sl=True)
        if selection!=self.currentSelection:
            self.updatePreferedValues()
        self.currentSelection = selection
        self.previewInfluenceMapping()
        
    def createTransferOptionsGroup(self):
        group = self.createUIGroup(self.cmdLayout.innerLayout, 'Transfer Options')
        self.createTitledRow(parent=group, title="Vertex Transfer Mode")
        self.controls.transferMode = DropDownField(self.VAR_PREFIX+'vertexTransferMode')
        
        for opt in CopyWeightsModel.vertexTransferModes.keys():
            self.controls.transferMode.addOption(opt)
        
        self.createTitledRow(parent=group, title=None)
        self.controls.keepExistingLayers = CheckBoxField(self.VAR_PREFIX+'KeepExistingLayers',label="Keep existing layers",
                annotation='when unselected, will delete existing layers in destination',defaultValue=1)
        
    def createInfluenceMappingGroup(self):
        group = self.createUIGroup(self.cmdLayout.innerLayout, 'Influence Mapping')

        self.createFixedTitledRow(group, 'Infl. Distance Error')
        self.controls.influenceDistanceError = FloatField(self.VAR_PREFIX+'distanceError', minValue=0, maxValue=None, step=0.01, defaultValue=0.001,
                                    annotation='Defines maximum inaccuracy between left and right influence positions')
        self.controls.influenceDistanceError.changeCommand.addHandler(self.previewInfluenceMapping, group)

        self.createTitledRow(parent=group, title="Namespaces")
        self.controls.ignoreNamespaces = CheckBoxField(self.VAR_PREFIX+'IgnoreNamespaces',label="Ignore",
                annotation='ignore influence namespaces when matching by name',defaultValue=1)
        self.controls.ignoreNamespaces.changeCommand.addHandler(self.previewInfluenceMapping,ownerUI=group)


        self.influenceMappingPreview.mirrorMode = False
        self.influenceMappingPreview.createUI(parent=group)
        self.influenceMappingPreview.onDelete.addHandler(self.influencesManualMapping.removeSelectedManualMappings,group)


        manualGroup = uiGroup.create(self.cmdLayout.innerLayout, 'Manual influence mapping')
        self.influencesManualMapping.mirrorMode = False
        self.influencesManualMapping.createUI(parent=manualGroup)
        self.influencesManualMapping.getSelectedInfluences = lambda: self.influenceMappingPreview.currentInfluencesSelection
        self.influencesManualMapping.manualOverridesChanged.addHandler(self.previewInfluenceMapping, group)


        cmds.setParent(group)

    def closeWindow(self,*args):
        self.parentWindow.closeWindow()
        
    def buildInfluenceMappingEngine(self):
        '''
        :rtype: InfluenceMapping
        '''
        result = self.dataModel.buildInfluenceMappingEngine(self.controls)
        result.manualOverrides = self.influencesManualMapping.manualOverrides
        return result
    
    def previewInfluenceMapping(self):
        if not self.dataModel.isEnabled():
            return
        engine = self.buildInfluenceMappingEngine()
        engine.calculate()
        self.influenceMappingPreview.mapper = engine
        self.influenceMappingPreview.constructInfluenceList()

    def execContinue(self,*args):
        self.previewInfluenceMapping()
        self.dataModel.execute()
        self.closeWindow()

    def updateLayoutEnabled(self):
        '''
        updates UI enabled/disabled flag based on layer data availability
        '''
        enabled = self.dataModel.isEnabled()
        cmds.layout(self.cmdLayout.innerLayout,e=True,enable=enabled)
        cmds.layout(self.cmdLayout.buttonForm,e=True,enable=enabled)
    
class TransferWeightsWindow(BaseToolWindow):
    def __init__(self, windowName):
        BaseToolWindow.__init__(self, windowName)
        self.useUserPrefSize = False
        self.windowTitle = 'Transfer Weights'
        self.sizeable = True
        self.defaultHeight = 600
        self.defaultWidth = 450
        self.content = TransferWeightsTab()
        self.content.parentWindow = self
        self.content.mirrorMode = False

    @staticmethod
    def getInstance():
        return BaseToolWindow.rebuildWindow('TransferWeightsWindow', TransferWeightsWindow)

    def createWindow(self):
        BaseToolWindow.createWindow(self)

        self.content.createUI(self.windowName)

    def onWindowDeleted(self):
        self.content.releaseUI()
        return BaseToolWindow.onWindowDeleted(self)
