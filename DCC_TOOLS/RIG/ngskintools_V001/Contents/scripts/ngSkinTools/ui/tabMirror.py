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
from ngSkinTools.ui.basetab import BaseTab
from ngSkinTools.ui.editMirrorInfluencesWindow import EditMirrorInfluencesWindow
from ngSkinTools.ui.uiWrappers import FloatField, CheckBoxField, DropDownField
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.ui.events import LayerEvents, MayaEvents
from ngSkinTools.log import getLogger
from ngSkinTools.orderedDict import OrderedDict
from ngSkinTools.ui.components.influencePrefixSuffixSelector import InfluencePrefixSuffixSelector
from ngSkinTools.ui.components import titledRow, uiGroup
from ngSkinTools.mllInterface import MllInterface, MirrorDirection
from ngSkinTools import selectionState
from ngSkinTools.influenceMapping import InfluenceMapping

log = getLogger("mirror UI")

class TabMirror(BaseTab):
    TOOL_PAINT = 'ngSkinToolsLayerPaintCtx'

    # prefix for environment variables for this tab
    VAR_PREFIX = 'ngSkinToolsMirrorTab_'
    
    
    
    def __init__(self):
        BaseTab.__init__(self)
        
    def executeMirror(self):
        self.influenceMappingConfiguration.updateSelectionsInfluenceMapping()
        
        mirrorDirection = MirrorDirection.DIRECTION_POSITIVETONEGATIVE
        if self.mirroringOptions.mirrorDirection.getValue()==0: # guess
            mirrorDirection = MirrorDirection.DIRECTION_GUESS;
        if self.mirroringOptions.mirrorDirection.getValue()==2: # negative to positive
            mirrorDirection = MirrorDirection.DIRECTION_NEGATIVETOPOSITIVE;
        if self.mirroringOptions.mirrorDirection.getSelectedText()==VertexMirroringOptions.MIRROR_FLIP: 
            mirrorDirection = MirrorDirection.DIRECTION_FLIP;
        
        with LayerDataModel.getInstance().mll.batchUpdateContext():
            for layerId in LayerDataModel.getInstance().layerListsUI.getSelectedLayers():
                LayerDataModel.getInstance().mll.mirrorLayerWeights(layerId,
                        mirrorWidth=self.mirroringOptions.mirrorWidth.getValue(),
                        mirrorLayerWeights=self.mirroringOptions.mirrorWeights.getValue(),
                        mirrorLayerMask=self.mirroringOptions.mirrorMask.getValue(),
                        mirrorDualQuaternion=self.mirroringOptions.mirrorDq.getValue(),
                        mirrorDirection=mirrorDirection
                    )

        # if layer list is filtered, might be handy to refresh influence list now - not that it costs much
        LayerEvents.influenceListChanged.emit()
        
        return True
        
    def createUI(self, parent):
        from ngSkinTools.ui.mainwindow import MainWindow
        
        mainActions = MainWindow.getInstance().actions
        self.setTitle('Mirror')
        
        # base layout
        self.cmdLayout = self.createCommandLayout([
                    ('Mirror Weights', mainActions.mirrorWeights, '')
                    ], SkinToolsDocs.UI_TAB_MIRROR)
        

        self.mirroringOptions = VertexMirroringOptions()
        self.mirroringOptions.createUI(self.cmdLayout.innerLayout)
        
        #configurationGroup = self.createUIGroup(self.cmdLayout.innerLayout, 'Configuration',defaultCollapsed=True)
        self.vertexMappingConfiguration = VertexMappingConfiguration()
        self.vertexMappingConfiguration.createUI(parent=self.cmdLayout.innerLayout)
        self.influenceMappingConfiguration = InfluencesMappingConfiguration()
        self.influenceMappingConfiguration.createUI(parent=self.cmdLayout.innerLayout)

        def update():
            cmds.layout(self.cmdLayout.outerLayout.layout, e=True, enable=selectionState.getLayersAvailable())

        selectionState.selectionInfo.changed.addHandler(update, parent)

        update()

        return self.cmdLayout.outerLayout.layout
    
class VertexMirroringOptions(object):
    VAR_PREFIX = 'ngSkinToolsMirror_mirroringOptions'
    MIRROR_TEXTS = {'x':("Left to right (+X to -X)", "Right to left (-X to +X)"),
                    'y':("Top to bottom (+Y to -Y)", "Bottom to top (-Y to +Y)"),
                    'z':("Front to back (+Z to -Z)", "Back to front (-Z to +Z)"),
                    }
    
    MIRROR_GUESS = 'Guess from stroke'
    MIRROR_FLIP = 'Flip'

    def createUI(self,parent):
        group = self.mirrorOptionsGroup = uiGroup.create(parent, 'Mirroring Options')

        titledRow.createFixed(group, 'Mirror direction')
        self.mirrorDirection = DropDownField(self.VAR_PREFIX + 'mirrorDirection')
        

        def getMirrorSideTexts():
            axis = selectionState.mirrorInfo.get()['axis']
            if axis is None:
                axis = 'x'
            return self.MIRROR_TEXTS[axis]
        
        def rebuildMirrorDirectionDropDown():
            self.mirrorDirection.beginRebuildItems()
            self.mirrorDirection.addOption(self.MIRROR_GUESS)
            for mirrorText in getMirrorSideTexts():
                self.mirrorDirection.addOption(mirrorText)
            self.mirrorDirection.addOption(self.MIRROR_FLIP)
            self.mirrorDirection.endRebuildItems()
        
        selectionState.mirrorInfo.changed.addHandler(rebuildMirrorDirectionDropDown, parent)
            
        def updateEnabled():
            data = LayerDataModel.getInstance()
            self.mirrorDq.setEnabled(data.layerDataAvailable and data.isDqMode())
        MayaEvents.nodeSelectionChanged.addHandler(updateEnabled, parent)


        titledRow.createFixed(group, 'Mirror Seam Width')
        self.mirrorWidth = FloatField(self.VAR_PREFIX + 'mirrorWidth', minValue=0, maxValue=None, step=1.0, defaultValue=0.1, annotation='Defines width of the interpolation from left to right side on the model center line.')
        cmds.setParent(group)
        titledRow.create(group, 'Elements')
        self.mirrorWeights = CheckBoxField(self.VAR_PREFIX + 'MirrorWeights', label="Mirror weights",
                annotation='Check this if mirror operation should be mirroring weights', defaultValue=1)
        self.mirrorMask = CheckBoxField(self.VAR_PREFIX + 'MirrorMask', label="Mirror mask",
                annotation='Check this if mirror operation should be mirroring layer mask', defaultValue=1)
        self.mirrorDq = CheckBoxField(self.VAR_PREFIX + 'MirrorDualQuaternion', label="Mirror dual quaternion weights",
                annotation='Check this if mirror operation should be mirroring dual quaternion weights', defaultValue=1)

        LayerEvents.mirrorConfigurationChanged.addHandler(rebuildMirrorDirectionDropDown, parent)
        rebuildMirrorDirectionDropDown()
        updateEnabled()
    
class VertexMappingConfiguration(object):
    VAR_PREFIX = 'ngSkinToolsMirror_vertexMappingConfiguration'
    vertexTransferModes = OrderedDict((
                    ("Closest point on surface","closestPoint"),
                    ("UV space","uvSpace"),
                    ))
    
    def updateConfiguration(self):
        mll = MllInterface()
        mll.configureVertexMirrorMapping(mirrorAxis=self.mirrorAxis.getSelectedText(),vertexTransferMode=self.vertexTransferModes[self.transferMode.getSelectedText()])
        LayerEvents.mirrorConfigurationChanged.emit()

    def createUI(self,parent):
        group = self.rootGroup = uiGroup.create(parent, 'Vertex Mapping')
        titledRow.createFixed(group, 'Mirror Axis')
        self.mirrorAxis = DropDownField(self.VAR_PREFIX+'mirrorAxis')
        self.mirrorAxis.setItems('X','Y','Z')
        self.mirrorAxis.changeCommand.addHandler(self.updateConfiguration, parent)

        titledRow.create(parent=group, title="Mapping mode")
        cmds.columnLayout()
        self.transferMode = DropDownField(self.VAR_PREFIX+'vertexMirrorMappingMode')
        self.transferMode.setItems(*self.vertexTransferModes.keys())
        self.transferMode.changeCommand.addHandler(self.updateConfiguration, parent)
        
        def update():
            mirrorAxis = selectionState.mirrorInfo.get()['axis']
            if mirrorAxis is not None:
                self.mirrorAxis.setValue(mirrorAxis.upper())
        
        selectionState.mirrorInfo.changed.addHandler(update, parent)

        update()
    
class InfluencesMappingConfiguration(object):
    VAR_PREFIX = 'ngSkinToolsMirror_influencesMappingConfiguration'
    
    def configureMapper(self):
        '''
        :rtype InfluenceMapping
        '''

        mll = selectionState.mll


        mapper = InfluenceMapping()
        mapper.mirrorMode = True
        mapper.manualOverrides = mll.getManualMirrorInfluences()
        mapper.sourceInfluences = mll.listInfluenceInfo()

        axis = mll.getMirrorAxis()

        mapper.distanceMatchRule.mirrorAxis = 0 if axis is None else 'xyz'.index(axis)
        mapper.distanceMatchRule.maxThreshold = float(self.influenceDistanceError.getValue());

        def parseCommaValue(values):
            return [value.strip() for value in values.split(",")]

        if self.influencePrefixSuffixSelector.ignorePrefixes.getValue()==1:
            mapper.nameMatchRule.setPrefixes(*parseCommaValue(self.influencePrefixSuffixSelector.influencePrefixes.getValue()))
        else:
            mapper.nameMatchRule.setSuffixes(*parseCommaValue(self.influencePrefixSuffixSelector.influenceSuffixes.getValue()))

        return mapper

    def updateSelectionsInfluenceMapping(self):
        mapper = self.configureMapper()
        mapper.calculate()
        selectionState.mll.configureInfluencesMirrorMapping(mapper.mapping)

        # for unit-testing traceability
        self.lastMapperUsed = mapper
        selectionState.mirrorInfo.changed.emit()

    def createUI(self,parent):
        
        group = self.mirrorOptionsGroup = uiGroup.create(parent, 'Influences Mapping')

        titledRow.createFixed(group, 'Position Tolerance')
        self.influenceDistanceError = FloatField(self.VAR_PREFIX+'distanceError', minValue=0, maxValue=None, step=0.01, defaultValue=0.001, 
                                    annotation='Defines maximum inaccuracy between left and right influence positions')

        
        self.influencePrefixSuffixSelector = InfluencePrefixSuffixSelector()
        self.influencePrefixSuffixSelector.createUI(group)
        titledRow.createFixed(group, None)

        cmds.button(label = "Edit influence associations...",command=self.showEditInfluencesWindow)


    # noinspection PyUnusedLocal
    def showEditInfluencesWindow(self, *args):
        # type: (object) -> EditMirrorInfluencesWindow
        w = EditMirrorInfluencesWindow.getInstance()
        w.setMapperBuilder(self.configureMapper)
        w.showWindow()
        return w
