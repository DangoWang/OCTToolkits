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
from ngSkinTools.influenceMapping import InfluenceMapping
from ngSkinTools.ui.SelectHelper import SelectHelper
from ngSkinTools.ui.components import titledRow
from ngSkinTools.ui.components import uiGroup
from ngSkinTools.ui.constants import Constants
from ngSkinTools.ui.events import Signal
from ngSkinTools.ui.uiWrappers import FloatField


class InfluencesListEntry:
    def __init__(self, source=None, destination=None, specialValue=None, automatic=True):
        self.source = source
        self.destination = destination
        self.bidirectional = False
        self.automatic = automatic
        self.targetAndDestinationIsSameMesh = False
        self.specialValue = specialValue

    def asLabel(self):
        if self.specialValue is not None:
            return self.specialValue

        prefix = "[M] " if not self.automatic else ""

        if self.isSelfReference():
            return prefix + shortName(self.source.path) + ": itself"

        if self.source is not None and self.destination is not None:
            mask = "%s -> %s"
            if self.bidirectional:
                mask = "%s <-> %s"
            return prefix + mask % (shortName(self.source.path), shortName(self.destination.path))

        if self.source is not None:
            return prefix + shortName(self.source.path)

        if self.destination is not None:
            return prefix + shortName(self.destination.path)

        return "Could not format item"

    def isSelfReference(self):
        return self.specialValue is None and self.targetAndDestinationIsSameMesh and self.source.path == self.destination.path

    def isConnectedElsewhere(self):
        return self.source is not None and self.destination is not None and self.source.path != self.destination.path

    def highlight(self):
        SelectHelper.replaceHighlight([self.source.path, self.destination.path])

    def __repr__(self):
        return self.asLabel()


def shortName(longName):
    separator = longName.rfind("|")
    if separator >= 0:
        return longName[separator + 1:]
    return longName


def influencesListSort(entry1, entry2):
    # priority for non-automatic entries
    if entry1.automatic != entry2.automatic:
        return 1 if entry1.automatic else -1

    # priority for non-self references
    if entry1.isSelfReference() != entry2.isSelfReference():
        return 1 if entry1.isSelfReference() else -1

    # priority for bidirectional entries
    if entry1.bidirectional != entry2.bidirectional:
        return 1 if not entry1.bidirectional else -1

    if entry1.source is not None and entry2.source is not None:
        return cmp(entry1.source.path, entry2.source.path)

    if entry1.destination is not None and entry2.destination is not None:
        return cmp(entry1.destination.path, entry2.destination.path)

    return 0

class InfluencesMappingPreview(object):
    VAR_PREFIX = "ngSkinToolsInfluenceSourceDestinationPreview"

    def __init__(self):
        self.items = [] # type: list[InfluencesListEntry]
        self.mirrorMode = False

        self.mapper = None # type: InfluenceMapping
        self.currentInfluencesSelection = []

        self.onDelete = Signal("influence mapping preview: onDelete")

    def constructInfluenceList(self):
        self.items = []
        self.currentInfluencesSelection = []


        mapper = self.mapper

        unmatchedSources = mapper.sourceInfluences[:]
        unmatchedDestinations = mapper.destinationInfluences[:]

        sourceInfluencesMap = dict((i.logicalIndex, i) for i in mapper.sourceInfluences)
        destinationInfluencesMap = dict((i.logicalIndex, i) for i in mapper.destinationInfluences)

        def isSourceAutomatic(src):
            return src.logicalIndex not in mapper.manualOverrides.keys()

        for source, destination in mapper.mapping.items():
            source = sourceInfluencesMap[source]
            destination = None if destination is None else destinationInfluencesMap[destination]

            if source is None or destination is None:
                continue

            if source in unmatchedSources:
                unmatchedSources.remove(source)

            if destination in unmatchedDestinations:
                unmatchedDestinations.remove(destination)

            automatic = isSourceAutomatic(source)
            item = None
            if self.mirrorMode and destination is not None:
                item = self.findAssociation(self.items, destination.path, source.path, automatic)
            if item is not None:
                item.bidirectional = True
            else:
                item = InfluencesListEntry()
                item.targetAndDestinationIsSameMesh = self.mirrorMode
                item.source = source
                item.destination = destination
                item.bidirectional = False
                self.items.append(item)
                item.automatic = automatic

        self.items = sorted(self.items, influencesListSort)

        if len(unmatchedSources) > 0 and not self.mirrorMode:
            self.items.append(InfluencesListEntry(specialValue="Unmatched source influences:"))

            for source in unmatchedSources:
                self.items.append(InfluencesListEntry(source=source, automatic=isSourceAutomatic(source)))

        if len(unmatchedDestinations) > 0 and not self.mirrorMode:
            self.items.append(InfluencesListEntry(specialValue="Unmatched destination influences:"))

            for destination in unmatchedDestinations:
                self.items.append(InfluencesListEntry(destination=destination))

        cmds.textScrollList(self.influencesList, e=True, removeAll=True,
                            append=[i.asLabel() for i in self.items])

    @staticmethod
    def findAssociation(itemList, source, destination, automatic):
        for i in itemList:
            if i.automatic != automatic:
                continue

            if i.source.path == source and i.destination.path == destination:
                return i
            if i.bidirectional and i.destination.path == source and i.source.path == destination:
                return i

        return None

    def getSelectedPairs(self):
        selection = cmds.textScrollList(self.influencesList,q=True,sii=True)

        if selection is not None:
            for i in selection:
                yield self.items[i-1]

    # noinspection PyUnusedLocal
    def onInfluenceSelected(self, *args):
        newSelection = list(self.getSelectedPairs())

        newHighlight = []
        for i in newSelection:
            if i.source is not None:
                newHighlight.append(i.source.path)
            if i.destination is not None:
                newHighlight.append(i.destination.path)

        SelectHelper.replaceHighlight(newHighlight)

        # the weird way of forming this currentInfluencesSelection like that
        # is because we want the items to be ordered in first to last selected order
        # when new selection happens, first all items that are not selected anymore
        # are removed from the current selection cache,
        # then all new items that are selected are added at the end.
        for i in self.currentInfluencesSelection[:]:
            if i not in newSelection:
                self.currentInfluencesSelection.remove(i)
        for i in newSelection:
            if i not in self.currentInfluencesSelection:
                self.currentInfluencesSelection.append(i)

    def createUI(self, parent):
        influencesLayout = cmds.columnLayout(parent=parent, adjustableColumn=1,
                                             rowSpacing=Constants.MARGIN_SPACING_VERTICAL)
        cmds.text(parent=influencesLayout, label="Influence mapping to be used:", align='left')
        self.influencesList = cmds.textScrollList(parent=influencesLayout, height=200, numberOfRows=5,
                                                           allowMultiSelection=True,
                                                           selectCommand=self.onInfluenceSelected,
                                                           deleteKeyCommand=lambda
                                                               *args: self.onDelete.emit())


