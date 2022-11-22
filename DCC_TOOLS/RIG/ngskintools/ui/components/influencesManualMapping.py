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
from ngSkinTools.ui.events import Signal


class InfluencesManualMapping(object):
    VAR_PREFIX = "ngSkinToolsInfluencesManualMapping"

    def __init__(self):
        self.mirrorMode = False
        self.getSelectedInfluences = lambda: None
        self.manualOverrides = {}
        self.manualOverridesChanged = Signal("influences manual mapping: manual overrides changed")

    def createUI(self, parent):
        cmds.rowLayout(parent=parent,nc=3)
        buttonWidth = 110
        cmds.button('Disconnect link',width=buttonWidth,command=lambda *args: self.doDisconnectMapping(),annotation='Disconnect two associated influences, and make each influence point to itself')
        if self.mirrorMode:
            cmds.button('Link, both ways',width=buttonWidth,command=lambda *args: self.doConnectMapping(bidirectional=True),annotation='Connect two selected influences and link them both ways')
        cmds.button('Link, one way' if self.mirrorMode else "Link",width=buttonWidth,command=lambda *args: self.doConnectMapping(bidirectional=False),annotation='Connect two selected influences and link on source to destination')
        cmds.rowLayout(parent=parent,nc=2)
        cmds.button('Remove manual rule',width=buttonWidth,command=lambda *args: self.removeSelectedManualMappings(),annotation='Remove manual rule; influence will be a subject to automatic matching')

    def addManualInfluenceMapping(self,source,destination):
        self.manualOverrides[source.logicalIndex] = None if destination is None else destination.logicalIndex

    def doDisconnectMapping(self):
        for mapping in self.getSelectedInfluences():
            if mapping.source is None:
                continue

            if mapping.destination is None:
                continue

            if mapping.source == mapping.destination:
                continue

            # for both source and destination, create a mapping for just itself
            self.addManualInfluenceMapping(mapping.source,
                                           mapping.source if mapping.targetAndDestinationIsSameMesh else None)
            if mapping.bidirectional:
                self.addManualInfluenceMapping(mapping.destination, mapping.destination)

        self.manualOverridesChanged.emit()


    def doConnectMapping(self, bidirectional=True):
        selection = self.getSelectedInfluences()
        if len(selection) < 2:
            return

        if bidirectional and len(selection) != 2:
            return

        validSources = []

        for item in selection[:-1]:
            if item.isConnectedElsewhere() or item.source is None:
                continue
            validSources.append(item)

        # second selected list item
        destinationItem = selection[-1]
        if destinationItem.isConnectedElsewhere():
            return

        destination = destinationItem.destination if destinationItem.destination is not None else destinationItem.source
        if destination is None:
            return

        destination = destination.logicalIndex
        for sourceItem in validSources:
            source = sourceItem.source.logicalIndex
            self.manualOverrides[source] = destination
            if bidirectional:
                self.manualOverrides[destination] = source

        self.manualOverridesChanged.emit()


    def removeSelectedManualMappings(self):
        selection = self.getSelectedInfluences()
        for item in selection:
            if item.source.logicalIndex in self.manualOverrides:
                del self.manualOverrides[item.source.logicalIndex]
            if item.bidirectional and item.destination.logicalIndex in self.manualOverrides:
                del self.manualOverrides[item.destination.logicalIndex]
        self.manualOverridesChanged.emit()
