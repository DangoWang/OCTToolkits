# -*- coding: utf-8 -*-
"""

    Core functionality for Nightshade UV Editor (NSUV) v2.1.3

    NSUV offers extended utility to Maya's native UV Editor
    Made by Martin (Nightshade) Dahlin - martin.dahlin@live.com - martin.dahlin.net

    Special thanks to:
    Nathan Roberts, Robert Kovach, David Johnson and Viktoras Makauskas on CGTalk, 
    Robert White and Steve Theodore on Tech-Artists.org
    Anton Palmqvist, Malcolm Andrieshyn and my friends Alexander Lilja and Elin Rudén
    for all the feedback, criticism, bug reports and feature ideas. 
    Thank you all!

    Script downloaded from Creative Crash

"""

## Table of Contents
# Initialization
# Classes
# Core Functionality
# Error Codes


## Imports

import pymel.core as pm
import collections
import inspect
import itertools
import math
import operator
import os
import random
import re
import subprocess
import sys
import time


## Initialization

# Vars
mayaVer = pm.optionVar["mayaVer_NSUV"]


# Set icon style of the group toggle icon used by the topBar and visBar
if mayaVer >= 201600:
    barIconClosed = "NS_barIconClosed.png"
    barIconOpen = "NS_barIconOpen.png"
    barIconSmallClosed = "NS_barIconSmallClosed.png"
    barIconSmallOpen = "NS_barIconSmallOpen.png"
else:
    barIconClosed = "NS_barIconClosed_old.png"
    barIconOpen = "NS_barIconOpen_old.png"
    barIconSmallClosed = "NS_barIconSmallClosed_old.png"
    barIconSmallOpen = "NS_barIconSmallOpen_old.png"


# Script jobs
def createScriptJobs(win, scrollList, cBox):

    # Update the compSpace toggle on tool change
    pm.scriptJob(
        event=["ToolChanged", lambda *args: compSpaceToggle(cBox, 2)],
        parent=win,
    )
    
    # Update the uvSetEditor on undo/redo and selection change
    pm.scriptJob(
        event=["SelectionChanged", lambda *args: updateUVSetEditor(scrollList)],
        parent=win,
    )
    pm.scriptJob(
        event=["SelectTypeChanged", lambda *args: updateUVSetEditor(scrollList)],
        parent=win,
    )
    pm.scriptJob(
        event=["SelectModeChanged", lambda *args: updateUVSetEditor(scrollList)],
        parent=win,
    )
    pm.scriptJob(
        event=["Undo", lambda *args: updateUVSetEditor(scrollList)],
        parent=win,
    )
    pm.scriptJob(
        event=["Redo", lambda *args: updateUVSetEditor(scrollList)],
        parent=win,
    )

    # Override the hotkey for Unfold3D brushes
    if mayaVer >= 201600:
        if pm.pluginInfo("Unfold3D", loaded=True, query=True):
            pm.scriptJob(
                event=["ToolChanged", lambda *args: u3dHotkeyOverride()],
                parent=win,
            )            
        pm.scriptJob(
            event=["ToolChanged", lambda *args: selectLastUVBrush()],
            parent=win,
        )


## Classes
 
# 2D Point
class Point2d(object):

    def __init__(self, u, v):
        """ Create a Point2d object using UV coords
        Example: p = Point2d(1,-2) """

        self.u = u
        self.v = v


    def __repr__(self):
        return "Point2d({p.u},{p.v})".format(p=self)


    def __str__(self):
        return "({p.u},{p.v})".format(p=self)


    def inRangeOf(self, other, range):
        """ Calculates the distance to another Point2d object and returns whenever it is in range or not 
        Example: self.rotate(other, 0.01)
        Returns: boolean

        Dependencies: python.math """

        # Calculate U and V distances, then the hypotenuse
        distU = abs(self.u - other.u)
        distV = abs(self.v - other.v)
        dist = math.sqrt(distU**2 + distV**2)

        # Calculate and return
        if range >= dist: return True
        else: return False


    def rotate(self, other, angle):
        """ Rotates a Point2d object around another Point2d object.
        Example: self.rotate(other, 45)

        Dependencies: python.math """

        # Short notation
        oU = other.u
        oV = other.v
        pU = self.u
        pV = self.v

        # Calculate
        angle = angle * math.pi / 180.0 # Radians
        newX = math.cos(angle) * (pU-oU) - math.sin(angle) * (pV-oV) + oU
        newY = math.sin(angle) * (pU-oU) + math.cos(angle) * (pV-oV) + oV

        # Round off and update attributes
        self.u = round(newX, 4)
        self.v = round(newY, 4)

## TEST CLASS REMOVE
# 2D Point
class Point2d2(object):

    def __init__(self, u, v, id):
        """ Create a Point2d object using UV coords
        Example: p = Point2d(1,-2) """

        self.u = u
        self.v = v
        self.id = id


    def __repr__(self):
        return "Point2d({p.u},{p.v},{p.id})".format(p=self)


    def __str__(self):
        return "({p.u},{p.v},{p.id})".format(p=self)


    def inRangeOf(self, other, range):
        """ Calculates the distance to another Point2d object and returns whenever it is in range or not 
        Example: self.rotate(other, 0.01)
        Returns: boolean

        Dependencies: python.math """

        # Calculate U and V distances, then the hypotenuse
        distU = abs(self.u - other.u)
        distV = abs(self.v - other.v)
        dist = math.sqrt(distU**2 + distV**2)

        # Calculate and return
        if range >= dist: return True
        else: return False


    def rotate(self, other, angle):
        """ Rotates a Point2d object around another Point2d object.
        Example: self.rotate(other, 45)

        Dependencies: python.math """

        # Short notation
        oU = other.u
        oV = other.v
        pU = self.u
        pV = self.v

        # Calculate
        angle = angle * math.pi / 180.0 # Radians
        newX = math.cos(angle) * (pU-oU) - math.sin(angle) * (pV-oV) + oU
        newY = math.sin(angle) * (pU-oU) + math.cos(angle) * (pV-oV) + oV

        # Round off and update attributes
        self.u = round(newX, 4)
        self.v = round(newY, 4)
##

# 2D Line
class Line2d(object):

    def __init__(self, pointA, pointB):
        """ Create a Line2d object using two Point2d objects
        Example: l = Line2d(pointA, pointB) """
        
        self.pointA = pointA
        self.pointB = pointB


    def __repr__(self):
        return "Line2d({l.pointA},{l.pointB})".format(l=self)


    def __str__(self):
        return "({l.pointA},{l.pointB})".format(l=self)


    def __iter__(self):
        for coord in (self.pointA, self.pointB):
            yield coord


    # Get angle using arctan
    def getAngle(self):
        """ Gets the arctan angle from the Line2d's two Point2d -objects 
        Example: angle = self.getAngle()
        
        Dependencies: python.math 
        Returns: float """

        # Calc arctangent
        angleVal = calcArctanAngle(self.pointA, self.pointB)
        invertVal = 0

        # Determine how much to rotate. Arctangent range is -90 to +90 degrees
        if angleVal == 0.0000 or angleVal == 90.0000 or angleVal == -90.0000:
            # Type 0 - No rotation
            angleVal = 0

        elif angleVal >= -44.9999 and angleVal <= 44.9999:
            # Type A - Invert
            invertVal = 1

        elif angleVal >= 45.0001 and angleVal <= 89.9999:
            # Type B - Subtract angle from 90
            angleVal = 90 - angleVal
            invertVal = 0

        elif angleVal <= -45.0001 and angleVal >= -89.9999:
            # Type C - Add 45 degrees to angle and invert
            angleVal = 90 + angleVal
            invertVal = 1

        else:
            # Type D - Angle is 45 degrees
            angleVal = 45
            invertVal = 0

        if invertVal == 1:
            angleVal = -angleVal

        # Calculate arctan angle and return it
        return angleVal


# 2D polygon
class Polygon2d(object):

    def __init__(self, lineList):
        """ Create a Polygon2D object using a list of Line2d objects
        Example: l = Polygon2D(list) """
        
        self.lineList = lineList
        self.pos = len(lineList)


    def __repr__(self):
        args = ','.join(['{0!r}'.format(arg) for arg in self])
        return '{cls_name}([{args}])'.format(cls_name=self.__class__.__name__, args=args)


    def __iter__(self):
        for line in self.lineList:
            yield line


    def __len__(self):
        return len(self.lineList)


    def __eq__(self, other):
        # return list(self) == list(other)
        return (self, other)


    # Rotate the polygon
    def rotate(self, other, angle):
        """ Rotates a Polygon2d object around a Point2d object 
        Example: self.rotate(other, 45)
        
        Dependencies: python.math """

        # Get all points in this polygon
        pointList = []
        for line in self:
            for point in line:
                pointList.append(point)
              
        # Remove duplicates
        pointList = list(set(pointList))
        
        # Rotate all points
        for point in pointList:
            point.rotate(other, angle)


    # Calculate the area of the bounding box
    def getBounds(self, mode):
        """ Gets the MAR (minimum-area rectangle) or center of the polygon 
        Example: area = self.getBounds(0); center = self.getBounds(1)
        
        Returns: float for self.getBounds(0) and a tuple for self.getBounds(1) """
        
        self.mode = mode
    
        # Collect all coordinate points
        points = self.getCoords()
    
        # Zip up tuples and get min and max
        xMax, yMax = map(max, zip(*points))
        xMin, yMin = map(min, zip(*points))

        # Calculate and return...
        if self.mode == 0: # MAR
            return (abs(xMax-xMin) * abs(yMax-yMin))
        else: # Center
            cX = 0.5 * (xMin + xMax)
            cY = 0.5 * (yMin + yMax)
            return (cX, cY)  


    # Get the coords of all Point2d objects in the polygon
    def getCoords(self):
        """ Gets all the coordinates for the Point2d objects in the polygon
        Example: coordList = self.getCoords()
        
        Returns: tuple list of floats """
    
        # Loop through all Point2d objects and get the coords, then append to list
        coordList = []
        for line in self:
            for point in line:
                coordList.append((point.u, point.v))
 
        # Remove duplicates and return list
        return list(set(coordList))


    # Get all Line2d objects in the polygon
    def getLines(self):
        """ Gets all the Line2d objects in the polygon
        Example: lineList = self.getLines()
        
        Returns: A list of tuples containing two tuples each """
        
        lineList = []
        for line in self:
            # lineList.append((line.pointA, line.pointB))
            lineList.append(line)
        
        return lineList

    
    # Calculate the rotation for a hull (Polygon2d object) needed to get the MAR (Minimum-Area-Rectangle)
    def getRotation(self):

        # Get the starting area and center as a Point2d object
        areaOld = self.getBounds(0)
        temp = self.getBounds(1)
        center = Point2d(temp[0], temp[1])
        rotateBy = 0
        rotateFinal = 0
        
        # Rotate
        for edge in self:
        
            # Calculate orientation of edge using arcTan
            orientation = edge.getAngle()
            
            # Rotate the convex hull and calculate the bounding box
            self.rotate(center, orientation)
            areaNew = self.getBounds(0)
            
            rotateBy += orientation
            
            # Measure areas
            if areaNew < areaOld:
                areaOld = areaNew
                rotateFinal = rotateBy

        return rotateFinal  


# UV Set Order Manager
class UVSetOrderMan():

    def __init__(self, scrollList):
    
        self.editorScrollList = scrollList
    
        # Class variables
        self.__selObj = None
        self.__uvSetList = []
        self.__uvDict = dict()
        self.uvManScroll = "NSUV_uvManScroll"
        
        # UI dimensions
        self.btnMargin = 2
        self.btnRow = 276
        self.btnWidth = (self.btnRow/2)-8
        self.winHeight = 233
        self.winWidth = 300 # Same as smallWinX
        self.winUvMan = "NSUV_uvManWin" 

        # Create UI
        self.createUI()
        
        # Create script job
        self.scriptJob = pm.scriptJob(
            event=["SelectionChanged", lambda *args: self.uvManCheckSel()], 
            parent=self.winUvMan
        )
        
        # Do initial selection check
        self.uvManCheckSel()


    ## Class functions

    # Check for valid selection and update stuff
    def uvManCheckSel(self):
    
        # Get selection...
        sel = pm.filterExpand(selectionMask=12) # Poly mesh
        
        # Update UI
        if sel != [] and sel != None:
            self.__selObj = pm.ls(selection=True, transforms=True)[0].getShape()
            self.uvManUpdate("draw")
            
        else: # Clear class vars
            self.uvManUpdate("clear")


    # Clear zombie sets
    def uvManClear(self):
    
        # Check selection
        checkSel("mesh")
        
        # Reload Maya scene
        userResponse = pm.confirmDialog(
            button=["Yes", "No"],
            cancelButton="No",
            defaultButton="No",
            dismissString="No",
            message="WARNING: Removing zombie sets requires a scene reload! "\
            "Unsaved changes will be lost! Do you really want to do this?",
            title="WARNING"
        )
        if userResponse == "Yes":
            scene = pm.system.sceneName()
            if scene == "": errorCode(22)
            else: pm.openFile(scene, force=True) # Force reload
                
                
        else: pass # No


    # Moves UV sets
    def uvManMove(self, dir):

        # Check selection
        checkSel("mesh")
        
        # Get index of selected set
        selSet = self.uvManScroll.getSelectItem()[0]
        selSetIndex = 0
        while selSetIndex < len(self.__uvSetList)-1:
            if selSet != self.__uvSetList[selSetIndex]:
                selSetIndex += 1
            else: break
        
        # Check if possible to move the selected set
        if len(self.__uvSetList) == 1:
            return # Only one UV set
        
        if selSetIndex == len(self.__uvSetList)-1 and (dir == "down" or dir == "bottom"):
            return # Already at bottom
        
        if selSetIndex == 0 and (dir == "up" or dir == "top"):    
            return # Already at top
            
        if len(self.__uvSetList) == 2 and selSetIndex == 1 and dir == "down": 
            return # Two sets - already at bottom and trying to move down
            
        if len(self.__uvSetList) == 2 and selSetIndex == 0 and dir == "up":
            return # Two sets - already at top and trying to move up

        # Copy sets
        if dir == "top":
            if selSetIndex == 1:
                self.uvManSwap(0, 1)
            else:
                swapCounter = 1
                while swapCounter != selSetIndex+1:
                    self.uvManSwap(selSetIndex, (selSetIndex-swapCounter))
                    swapCounter += 1

        elif dir == "up":
            self.uvManSwap(selSetIndex, (selSetIndex-1))

        elif dir == "down":
            self.uvManSwap(selSetIndex, (selSetIndex+1))

        else: # "bottom"
            swapCounter = 1
            while swapCounter != len(self.__uvSetList) and (selSetIndex+swapCounter) != len(self.__uvSetList):
                self.uvManSwap(selSetIndex, (selSetIndex+swapCounter))
                swapCounter += 1

        # Update UI and class vars
        self.uvManUpdate("draw")
        
        # Update the UV Set List in the UV Editor
        updateUVSetEditor(self.editorScrollList)
        
        # Reselect uvSet in lists
        self.uvManSelect(selSet)


    # Selects current set in the NSUV UV Set Editor list
    def uvManSelect(self, selSet=[]):    
        if selSet == []:
            selSet = self.uvManScroll.getSelectItem()[0]   
        
        # NSUV UV Set List: Set new active set, deselect all and reselect active set
        self.editorScrollList.deselectAll()
        self.editorScrollList.setSelectItem(selSet)
        setCurrentSet(self.editorScrollList)
        
        # Order Manager List: Deselect all and reslect active set
        self.uvManScroll.deselectAll()
        self.uvManScroll.setSelectItem(selSet)
        
    
    # Swaps the layouts and names of two UV sets
    def uvManSwap(self, set_0, set_1):
        
        # Make a temp UV set that holds a copy of our first set
        tmp_name = self.__uvSetList[set_0] + '_NStmp'
        pm.polyUVSet(
            self.__selObj, 
            copy=True, 
            newUVSet=tmp_name, 
            uvSet=self.__uvSetList[set_0]
            )
        
        # Move the data in our second set, into the first set
        pm.polyUVSet(
            self.__selObj, 
            copy=True, 
            newUVSet=self.__uvSetList[set_0], 
            uvSet=self.__uvSetList[set_1]
            )
        
        # Move the data from our temp set, into our second set
        pm.polyUVSet(
            self.__selObj, 
            copy=True, 
            newUVSet=self.__uvSetList[set_1], 
            uvSet=tmp_name
        )
        
        # Clean up by removing our temp set
        pm.polyUVSet(
            self.__selObj, 
            delete=True, 
            uvSet=tmp_name
        )

        # Swap names
        pm.polyUVSet(
            self.__selObj,
            rename=True,
            newUVSet=self.__uvSetList[set_0]+"_NSnew",
            uvSet=self.__uvSetList[set_0]
        )
        pm.polyUVSet(
            self.__selObj,
            rename=True,
            newUVSet=self.__uvSetList[set_0],
            uvSet=self.__uvSetList[set_1]
        )
        pm.polyUVSet(
            self.__selObj,
            rename=True,
            newUVSet=self.__uvSetList[set_1],
            uvSet=self.__uvSetList[set_0]+"_NSnew"
        )


    # Updates __uvSetList and the UI
    def uvManUpdate(self, mode):
    
        # Clear class vars and scroll list
        if mode == "clear":
            self.__selObj = None
            self.__uvSetList = []
            self.__uvDict = dict()
            self.uvManScroll.removeAll()
            self.uvManScroll.append("Select a Polygon Mesh!")
            return
    
        # Update (clear and re-draw UI)
        else:
        
            # Update class vars and clear scroll list
            uvIndices = pm.polyUVSet(self.__selObj, query=True, allUVSetsIndices=True)
            uvNames = pm.polyUVSet(self.__selObj, query=True, allUVSets=True)            
            self.__uvDict = dict(zip(uvNames, uvIndices)) # Create keypairs
            self.__uvSetList = sorted(self.__uvDict, key=self.__uvDict.get) # Sorted list
            self.uvManScroll.removeAll()
            
            # Get the selected set
            if mode != "draw":
                selectedSet = self.uvManScroll.getSelectItem()[0]
                index = self.uvManScroll.getSelectIndexedItem()[0]
                index -= 1 # one-based to zero-based
                selectedSet = self.uvManScroll.getSelectItem()[0]

            # Modify and set new index for selectedSet
            if mode == "top": index = 0

            if mode == "up": index -= 1

            if mode == "down": index += 1

            if mode == "bottom":
                index = len(self.uvManScroll.getAllItems()) - 1
            
            # Insert set at index if necessary
            if mode == "top" or mode == "up" or mode == "down" or mode == "bottom":
                self.__uvSetList.remove(selectedSet)
                self.__uvSetList.insert(index, selectedSet)

        # Update scroll list
        self.uvManScroll.removeAll()
        for item in self.__uvSetList:
            self.uvManScroll.append(item)
        
        # Select first item in list
        if mode == "draw": self.uvManScroll.setSelectIndexedItem(1)
        else: self.uvManScroll.setSelectItem(selectedSet)


    ## User-interface

    # Close UI
    def closeUI(self):
        pm.deleteUI(self.winUvMan)


    # Create UI
    def createUI(self):

        # Check for window duplicate
        if pm.window( self.winUvMan, exists=True ):
            pm.deleteUI(self.winUvMan)

        # Window
        window = pm.window(
            self.winUvMan,
            height=self.winHeight,
            minimizeButton=False,
            maximizeButton=False,
            resizeToFitChildren=True,
            sizeable=True,
            title="UV Set Order Manager",
            width=self.winWidth 
        )
        
        # Layouts
        frameUVMan = pm.frameLayout(
            collapsable=False, 
            collapse=False, 
            height=self.winHeight, 
            label="Options", 
            marginHeight=10, 
            marginWidth=10, 
            width=self.winWidth 
        )
        
        colUVMan = pm.columnLayout(
            adjustableColumn=False, 
            columnAlign="left", 
            rowSpacing=6,
            width=self.btnRow
        )
        
        textMatchTol = pm.text(
            label="Note:\nChanges takes place on the fly!")        

        formUVMan = pm.formLayout(
            parent=frameUVMan,
            width=self.btnRow
        )

        # UV Sets list
        self.uvManScroll = pm.textScrollList(
            allowMultiSelection=False, 
            deleteKeyCommand="",
            doubleClickCommand="",
            height=116+(5*self.btnMargin),
            parent=formUVMan,
            selectCommand=lambda *args: self.uvManSelect(),
            width=self.btnWidth
        )
        
        # Buttons
        btnTopUVMan = pm.button( 
            command=lambda *args: self.uvManMove("top"),
            label="Make primary", 
            parent=formUVMan,
            width=self.btnWidth,
        )
        btnUpUVMan = pm.button( 
            command=lambda *args: self.uvManMove("up"),
            label="Move up", 
            parent=formUVMan,
            width=self.btnWidth,
        )
        btnDownUVMan = pm.button( 
            command=lambda *args: self.uvManMove("down"),
            label="Move down", 
            parent=formUVMan,
            width=self.btnWidth,
        )
        btnBtmUVMan = pm.button( 
            command=lambda *args: self.uvManMove("bottom"),
            label="Move to bottom", 
            parent=formUVMan,
            width=self.btnWidth,
        )
        btnClrUVMan = pm.button( 
            command=lambda *args: self.uvManClear(),
            label="Clear zombie sets", 
            parent=formUVMan,
            width=self.btnWidth,
        )
        
        # Layout the elements in the formLayout
        pm.formLayout(
            formUVMan, edit=True, 
            attachForm=[
                (self.uvManScroll, "top", 0 ), 
                (self.uvManScroll, "left", 0 ),
                
                (btnTopUVMan, "top", self.btnMargin ),             
                (btnTopUVMan, "right", 0 ), 
                
                (btnUpUVMan, "right", 0 ), 
                
                (btnDownUVMan, "right", 0 ), 
                
                (btnBtmUVMan, "right", 0 ), 
                
                (btnClrUVMan, "right", 0 ), 
            ], 
            attachControl=[           
                (btnTopUVMan, "left", 0, self.uvManScroll),
                
                (btnUpUVMan, "top", self.btnMargin, btnTopUVMan), 
                (btnUpUVMan, "left", 0, self.uvManScroll), 
                
                (btnDownUVMan, "top", self.btnMargin, btnUpUVMan), 
                (btnDownUVMan, "left", 0, self.uvManScroll), 

                (btnBtmUVMan, "top", self.btnMargin, btnDownUVMan), 
                (btnBtmUVMan, "left", 0, self.uvManScroll), 
                
                (btnClrUVMan, "top", self.btnMargin, btnBtmUVMan), 
                (btnClrUVMan, "left", 0, self.uvManScroll), 
            ]
        ) 

        # Buttons
        rowUVMan = pm.rowLayout(
            columnAttach2=["both", "both"], 
            numberOfColumns=2, 
            parent=frameUVMan   
        )
        btnCancelUVMan = pm.button( 
            command=lambda *args: self.closeUI(),
            label="Done", 
            parent=rowUVMan, 
            width=self.btnRow
        )
        
        # Display the window
        pm.showWindow(window)


## Core Functionality

# Absolute/Relative -toggle for the manipulator
def absToggle(state):    
    if state == True: pm.optionVar["absToggle_NSUV"] = True
    else: pm.optionVar["absToggle_NSUV"] = False


# Align shells
def alignShells(action, shellList=None, titleOverride=""):

    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.setToolTo("selectSuperContext")
    
    # Validate UV selection
    checkSel("UV")
    
    # Store the original selection, expand to shell, get bounds
    selOrg = pm.ls(selection=True)
    pm.mel.polySelectBorderShell(0)
    shellBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    
    # Get shells from selection if we have no incomming shells
    if shellList == [] or shellList == None:
        shellList = getShells()

    # Calculate uMin/uMax
    centerU = 0.5 * ( shellBox[0][0] + shellBox[0][1] )
    centerV = 0.5 * ( shellBox[1][0] + shellBox[1][1] )
    
    # Create progress window
    if titleOverride == "":
        createProgWin("Aligning...", len(shellList))
    else:
        createProgWin(titleOverride, len(shellList))
    
    shellsTotal = shellsRemain = len(shellList) # Shell count
    
    # Loop through each shell
    for item in shellList:
    
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True, 
            progress=(shellsTotal - shellsRemain),
            status="Processing shells. %s Shells remaining."%shellsRemain        
        )
        
        # Select the shell and calculate new bounds
        pm.select(item)
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    
        # Move the shell
        if action == "uMax":
            offset = shellBox[0][1] - uvBox[0][1]
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "uMin":
            offset = shellBox[0][0] - uvBox[0][0]
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "uAvg":       
            offset = centerU - ( 0.5 * (uvBox[0][0] + uvBox[0][1]) )
            pm.polyEditUV(relative=True, uValue=offset)
        
        if action == "vMax":
            offset = shellBox[1][1] - uvBox[1][1]
            pm.polyEditUV(relative=True, vValue=offset)
        
        if action == "vMin":
            offset = shellBox[1][0] - uvBox[1][0]
            pm.polyEditUV(relative=True, vValue=offset)
        
        if action == "vAvg":
            offset = centerV - ( 0.5 * (uvBox[1][0] + uvBox[1][1]) )
            pm.polyEditUV(relative=True, vValue=offset)
            
        if action == "center": ## Unused atm
            offsetU = centerU - ( 0.5 * (uvBox[0][0] + uvBox[0][1]) )
            offsetV = centerV - ( 0.5 * (uvBox[1][0] + uvBox[1][1]) )
            pm.polyEditUV(relative=True, uValue=offsetU, vValue=offsetV)
    
        # Decrease the shells remaining -counter
        shellsRemain -= 1
    
    # Close the progress window
    pm.progressWindow(endProgress=True)

    # Reselect the original selection
    pm.select(selOrg)
    
    # Activate the move tool
    pm.setToolTo("moveSuperContext")
    

# Align UVs
def alignUVs(action):

    # Validate UV selection
    checkSel("UV")
    
    # Original selection
    selOrg = pm.ls(selection=True)
    
    # Poly UVs filter
    selUVs = pm.filterExpand(selectionMask=35)
    if selUVs == []: return # Stop execution without a warning

    # Get bounds
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)

    # Calculate U and V centers
    centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
    centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
   
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.setToolTo("selectSuperContext")
    pm.select(selUVs, replace=True)

    # Align to max U
    if action == "maxU":
        pm.polyEditUV(
            relative=False,
            uValue=uvBox[0][1]
        )
    
    # Align to min U
    if action == "minU":    
        pm.polyEditUV(
            relative=False,
            uValue=uvBox[0][0]
        )
    
    # Align to average U
    if action == "avgU":    
        pm.polyEditUV(
            relative=False,
            uValue=centerU
        )
    
    # Align to max V
    if action == "maxV":
        pm.polyEditUV(
            relative=False,
            vValue=uvBox[1][1]
        )
    
    # Align to min V
    if action == "minV":
        pm.polyEditUV(
            relative=False,
            vValue=uvBox[1][0]
        )
    
    # Align to average V
    if action == "avgV":     
        pm.polyEditUV(
            relative=False,
            vValue=centerV
        )
        
    if action == "singularity":
        pm.polyEditUV(
            relative=False,
            uValue=centerU,
            vValue=centerV,
        )
    
    # Select original selection
    pm.select(selOrg)
    
    # Activate the move tool
    pm.setToolTo("moveSuperContext")


# Auto seams
def autoSeams(win):

    # Check if Unfold3D is loaded
    if pm.pluginInfo("Unfold3D", loaded=True, query=True):

        # Run auto seams
        pm.u3dAutoSeam(
            cutPipes=pm.optionVar["autoSeamPipeCut_NSUV"], 
            select=pm.optionVar["autoSeamOperation_NSUV"],
            splitShells=pm.optionVar["autoSeamSegment_NSUV"],
        )

    else:
        errorCode(16)

    # Close unfold window
    if win != None:
        pm.deleteUI(win)


# Calculate arctangent
def calcArctanAngle(uv1, uv2):
    """ Gets the arctan angle from two UVs or two Point2d -objects 
    Example: angle = self.getAngle()
    
    Dependencies: python.math 
    Returns: float """
    
    # Store coordinates
    if hasattr(uv1, "u"): # Checks if Point2d
        pointA = [uv1.u, uv1.v]
        pointB = [uv2.u, uv2.v]
    else:
        pointA = pm.polyEditUV(uv1, query=True)
        pointB = pm.polyEditUV(uv2, query=True)
    
    # Results can be both positive and negative, so calc both
    if pointA[0] >= pointB[0]:
        distU = (pointA[0] - pointB[0])
        distV = (pointA[1] - pointB[1])
    else:
        distU = (pointB[0] - pointA[0])
        distV = (pointB[1] - pointA[1])
        
    # Use arctangent to calculate angle
    angle = math.degrees( math.atan2(distV, distU) )
    return angle


# Calculate pixel distance between two UVs
def calcPxDist():
    
    # Validate UV selection
    checkSel("UV")
    
    # Get bounds and calculate distances
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    distU = abs(uvBox[0][1] - uvBox[0][0])
    distV = abs(uvBox[1][0] - uvBox[1][1])
    
    # Calculate hypotenuse using trig
    distUV = math.hypot(distU, distV)
    
    # Return distances
    return (distU, distV, distUV)


# Selection checker
def checkSel(selType):
    
    # Check for any selection
    if selType == "any":
        sel = pm.filterExpand(selectionMask=(12, 31, 32, 34, 35))
        if sel == [] or sel == None:
            errorCode(0)

    # Check for valid mesh selection 
    if selType == "mesh":
        sel = pm.filterExpand(selectionMask=12)
        if sel == [] or sel == None:
            errorCode(9)

    # Check for polygon components selections
    if selType == "comps":
        sel = pm.filterExpand(selectionMask=(31, 32, 34, 35))
        if sel == [] or sel == None:
            errorCode(20)
            
    # Check for valid mesh selection 
    if selType == "mesh1":
        sel = pm.filterExpand(selectionMask=12)
        if sel == [] or sel == None or len(sel) > 1:
            errorCode(23)

    # Check for valid face selection
    if selType == "face":
        sel = pm.filterExpand(selectionMask=34)
        if sel == [] or sel == None:
            errorCode(1)

    # Check for valid single face selection
    if selType == "face1": ## Unused atm
        sel = pm.filterExpand(selectionMask=34)
        if sel == [] or sel == None:
            errorCode(19)

    # Check for valid face or mesh selection
    if selType == "faceMesh":
        sel = pm.filterExpand(selectionMask=(12, 34))
        if sel == [] or sel == None:
            errorCode(11)

    # Check for valid face or UV selection
    if selType == "faceUV":
        sel = pm.filterExpand(selectionMask=(34, 35))
        if sel == [] or sel == None:
            errorCode(4)

    # Check for valid edge selection
    if selType == "edge":
        sel = pm.filterExpand(selectionMask=32 )
        if sel == [] or sel == None:
            errorCode(14)

    # Check for valid edge or UV selection
    if selType == "edgeUV":
        sel = pm.filterExpand(selectionMask=(32, 35))
        if sel == [] or sel == None:
            errorCode(3)

    # Check for valid UV selection
    if selType == "UV":
        sel = pm.filterExpand(selectionMask=35)
        if sel == [] or sel == None:
            errorCode(2)

    # Check for valid UV selection (Two points only)
    if selType == "UV2":
        sel = pm.filterExpand(selectionMask=35)
        if len(sel) != 2:
            errorCode(8)

    # Check for valid mesh or UV selection 
    if selType == "meshUV":
        sel = pm.filterExpand(selectionMask=(12, 35))
        if sel == [] or sel == None:
            errorCode(5)

    # Check if selection spans over multiple shells
    if selType == "multi":
    
        # Store original selection and the UVs of it
        selOrg = pm.ls(selection=True)
        selOrgUVs = pm.polyListComponentConversion(toUV=True)
        
        # Expand to entire shells
        shellsAll = pm.polySelectConstraint(
            mode=2,
            shell=1,
            type=0x0010
        )
        pm.polySelectConstraint(disable=True)
        
        # Store all shell(s) UVs
        selUVs = pm.ls(selection=True, flatten=True)
        
        # Get one single UV from selOrgUVs and convert to just ONE shell
        pm.select(selOrgUVs[0])
        shellSingle = pm.polySelectConstraint(
            mode=2, 
            shell=1, 
            type=0x0010
        )
        pm.polySelectConstraint(disable=True)
        
        # This if-statement will only be true if the original selection
        # could be expanded to cover multiple UV shells.
        if shellSingle != shellsAll:
            pm.select(selOrg)
            errorCode(6) 


# Comp space toggle
def compSpaceToggle(cBox, mode):
  
    # Query optVar - not used atm
    if mode == 2:
        return pm.optionVar["compSpace_NSUV"] 
        
    # Check for UV selection (necessary for scriptJob to bypass Maya bug)
    sel = pm.filterExpand(selectionMask=35)
    if sel != [] or sel != None:
    
        # Toggle and update UI component
        pm.texMoveContext(
            "texMoveContext",
            edit=True,
            snapComponentsRelative=mode
        )
        cBox.setValue(mode)
 
        # Update optVar 
        pm.optionVar["compSpace_NSUV"] = mode
        
    else: pass


# Copy/Paste UV's or faces
def copyPasteUV(mode):

    # Selection check
    checkSel("faceUV")
    selType = pm.filterExpand(selectionMask=(34)) # Face check
    
    # Edge/Face?
    if selType == None: # UVs
    
        # Copy/Paste?
        if mode == 0: pm.mel.textureWindowCreateToolBar_uvCopy()
        else: pm.mel.textureWindowCreateToolBar_uvPaste(1,1)

    else: # Faces
        
        # Copy/Paste?
        if mode == 0: pm.mel.polyClipboard(copy=True, uvCoordinates=True)
        else: pm.mel.polyClipboard(paste=True, uvCoordinates=True)
    
    
# Copy UV Set
def copySet(scrollList, copyFrom, copyTo, win=None, lastSettings=False):

    # Increment digits in UV set name string
    def incrementName(uvSet):

        # Split uvSet name string into name and number - increment number by 1 and then concatenate it to the string
        temp = re.split("(\d+$)", uvSet)
        temp[1] = int(temp[1]) + 1
        return temp[0] + str(temp[1])


    # Selection check
    checkSel("any")
    
    # Store original selection
    selOrg = pm.ls(selection=True, flatten=True)
    selOrgSet = set(selOrg) # (used for bool op)
    
    # Get meshes in selection
    mshSel = pm.ls(selection=True, flatten=True, objectsOnly=True)

    # Copy using last settings
    if lastSettings == True:
        copyFrom = pm.optionVar["copyFromSet_NSUV"]
        copyTo = pm.optionVar["copyToSet_NSUV"]
        if copyFrom == None or copyTo == None:
            core.errorCode(28)

    # Copy the UV set for each mesh
    for msh in mshSel:
    
        # Get current UV set on the mesh if copyFrom isn't specified
        if copyFrom == None or copyTo == None:
            copyFrom = pm.polyUVSet(currentUVSet=True, query=True)[0]
        
        # Only true when duplicating a set
        if copyTo == None:
           
            # End with digit?
            if re.search("\d$", copyFrom) != None:
                copyTo = incrementName(copyFrom)

            # Then add digit to name
            else:
                copyTo = copyFrom + str(1)

            # Check if name already exists, and if so increment the number in the name
            uvSets = pm.polyUVSet(
                msh,
                allUVSets=True,
                perInstance=True,
                query=True,
            )            
            for x in range(len(uvSets)):
                if copyTo in uvSets:           
                    copyTo = incrementName(copyTo)
            
        # Create the copyTo -set if it doesn't exist
        uvSets = pm.polyUVSet(msh, query=True, allUVSets=True)
        if copyTo not in uvSets:
            pm.polyUVSet(
                msh,
                create=True,
                uvSet=copyTo,
            )
 
        # Mesh
        sel = pm.filterExpand(selectionMask=12)        
        if sel != [] and sel != None:
            pm.polyUVSet(
                msh,
                copy=True,
                newUVSet=copyTo,
                uvSet=copyFrom,
            )

        else: # Components
            sel = pm.filterExpand(selectionMask=(31, 32, 34, 35))
            if sel != [] and sel != None:
            
                # Get components belonging to current mesh in loop, then copy the UV set
                compsSet = set(pm.ls(pm.polyListComponentConversion(msh, toUV=True), flatten=True))
                intersection = list(set(selOrgSet) & set(compsSet))
                pm.polyCopyUV(
                    intersection,
                    constructionHistory=True,
                    uvSetName=copyTo,
                )

        # Update optVars
        pm.optionVar["copyFromSet_NSUV"] = copyFrom
        pm.optionVar["copyToSet_NSUV"] = copyTo


    # Update the UV set editor
    updateUVSetEditor(scrollList)
    
    # Close the copySetUI window and reselect original selection
    if win != None: pm.deleteUI(win)    
    pm.select(selOrg)


# Compute the convex hull of a set of 2D points using the "Monotone chain convex hull" -algorithm
def createConvexHull(selUVs):
    """ Takes list of UVs, calculates the convex hull and creates a Polygon2d object of the hull.
    Example: hull = createConvexHull(selUVs)
    
    Returns: The hull represented as a Polygon2D object """
  
    # 2D cross product of OA and OB vectors.
    # Returns positive for CCW, negative for CW and 0 if collinear
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
    # Create uvCoordList - tuples with the U and V values
    uvCoordList = []
    for uv in selUVs:
        point = pm.polyEditUV(uv, query=True)
        uvCoordList.append((point[0], point[1]))
 
    # Sort the points and remove duplicates
    points = sorted(set(uvCoordList))

    # Create points in lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
 
    # Create points in upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
 
    # Combine hulls and remove the last points of each list
    hullPoints = lower[:-1] + upper[:-1]
    
    # Create list of points (Point2d)
    pointList = []
    for pair in hullPoints:
        ## NOTE: Rounding the coords might give better results?
        pointList.append(Point2d(pair[0], pair[1]))
        
    # Create list of lines (Line2d)
    lineList = []
    counter = 0
    while counter <= len(pointList)-1:
        if counter != len(pointList)-1:
            line = Line2d(pointList[counter], pointList[counter+1])
        else: # Final line (last to first point)        
            line = Line2d(pointList[counter], pointList[0])

        lineList.append(line)
        counter += 1
        
    # Create polygon object (Polygon2d) for the convex hull, and return it
    return Polygon2d(lineList)


# Progress window template
def createProgWin(titleText, max):
    pm.progressWindow(
        isInterruptable=True,
        maxValue=max,
        minValue=0,
        title=titleText,
        progress=0,
    )


# Create new UV set
def createSet(scrollList, closeWin=None, noClose=False):

    # Selection check
    checkSel("any")

    instVar = False
    unShareVar = False
    
    # Check optVars
    if pm.optionVar["newUVSetShare_NSUV"] > 1:
        instVar = True
        if pm.optionVar["newUVSetShare_NSUV"] == 3:
            unShareVar = True
    
    # Create the UV set
    if instVar == True:
        pm.polyUVSet(
            create=True,
            perInstance=instVar,
            unshared=unShareVar,
            uvSet=pm.optionVar["newUVSet_NSUV"]
        )
    else: # discarding perInstance -flag in order to avoid [0] -suffix
        pm.polyUVSet(
            create=True,
            uvSet=pm.optionVar["newUVSet_NSUV"]
        )

    # Update the UV Set list
    updateUVSetEditor(scrollList)

    # Close the "Create New UV Set" -window if necessary
    if closeWin != None and noClose == False:
        pm.deleteUI(closeWin)


# Create new UV set - store optVars
def createSetOptVars(optVar, ctrlName):

    if optVar == 0: pm.optionVar["newUVSet_NSUV"] = ctrlName.getText()
    else: pm.optionVar["newUVSetShare_NSUV"] = ctrlName.getSelect()-1


# Create NSUV Shelf button
def createShelfBtn():

    # Get Maya version and set icon style
    if mayaVer < 201600: shelfImg = "NSUV_shelf_old.png"
    else: shelfImg = "NSUV_shelf.png"
    
    # Get top shelf as parent
    pm.mel.eval("global string $gShelfTopLevel")
    topShelf = pm.mel.eval("$temp = $gShelfTopLevel")
    currentShelf = pm.tabLayout(topShelf, query=True, selectTab=True)
    pm.setParent(topShelf + "|" + currentShelf)
    
    # Create the button
    pm.shelfButton(
        annotation="Nightshade UV Editor",
        command="python(\"import sys\");"
        "if (`window -ex polyTexturePlacementPanel1Window`){"
        "deleteUI -window polyTexturePlacementPanel1Window;}"
        "if (`window -ex NSUV_mainWin`){"
        "    if (`window -q -iconify NSUV_mainWin`){"
        "        window -e -iconify 0 NSUV_mainWin;"
        "    }else{"
        "        window -e -iconify 1 NSUV_mainWin;}"
        "}else{"
        "    catchQuiet ( `python(\"del sys.modules['NSUV']\")`);"
        "    catchQuiet ( `python(\"del sys.modules['NSUV.UI']\")`);"
        "    catchQuiet ( `python(\"del sys.modules['NSUV.core']\")`);"
        "    python(\"import NSUV\");"
        "}",
        label="NSUV",
        image1=shelfImg,
        sourceType="mel",
    )   
    
    
# Create UV shell from face selection
def createShell():

    # Validate face selection
    checkSel("face")
    
    # Original selection
    selOrg = pm.ls(selection=True)
    
    # Convert to border selection
    selBorders = pm.polyListComponentConversion(
        selOrg,
        border=True,
        fromFace=True,
        toEdge=True,    
    )  

    # Select the borders, cut them up, reselect original selection as UVs
    pm.select(selBorders)    
    pm.polyMapCut()
    pm.select(selOrg)
    newSel = pm.polyListComponentConversion(toUV=True)
    pm.select(newSel)
    
    # Activate the move tool
    pm.setToolTo("moveSuperContext")


# Cut selected UVs or edges
def cutSewUVs(mode):

    selOrg = pm.ls(selection=True)
    selObjs = pm.ls(selection=True, objectsOnly=True)
    objUVs = splitUVsPerMesh(selOrg, selObjs)

    if mode == "cut" or mode == "split":
        for uvs in objUVs:
            pm.polyMapCut(uvs, constructionHistory=True)
    elif mode == "sew":
        for uvs in objUVs:
            pm.polyMapSew(uvs, constructionHistory=True)
    elif mode == "moveSew":
        for uvs in objUVs:
            pm.polyMapSewMove(
                uvs,
                constructionHistory=True,
                limitPieceSize=False,
                numberFaces=10,
            )


# Switches back to the native UV Texture Editor
def defaultEditor(win):

    # Delete NSUV window
    pm.deleteUI(win)
    
    # Restore MEL-callbacks for the texture window scriptedPanelType
    pm.scriptedPanelType(
        "polyTexturePlacementPanel", edit=True,
            addCallback="addTextureWindow",
            createCallback="createTextureWindow",
            removeCallback="removeTextureWindow",
            )
    
    # These rows below is in case you need to source a custom in-house UV Editor.
    # Uncomment the path line below and specify a custom path inside the double quotes
    # If things aren´t working, contact your local Technical Artist

    # path = pm.util.getEnv("MAYA_LOCATION") + "/scripts/others/textureWindowCreateToolBar.mel"

    # Re-source the native toolbar and panels
    pm.mel.source("textureWindowCreateToolBar.mel") # For a custom path, change to pm.mel.source(path)
    pm.mel.source("texturePanel.mel")
    pm.mel.TextureViewWindow()

    # Open up the native UV Texture Editor
    pm.runtime.TextureViewWindow()


# Deletes a UV set from the UV set list
def deleteSet(scrollList):

    # Get UV sets from scrollList
    uvSets = scrollList.getSelectItem()

    # Delete all selected sets from the current mesh selection
    for item in uvSets:
        pm.polyUVSet(
            delete=True,
            uvSet=item,
        )
        
    # Update the UV set editor
    updateUVSetEditor(scrollList)


# Deletes the selected UV's
def deleteUVs():

    selOrg = pm.ls(selection=True)
    selObjs = pm.ls(selection=True, objectsOnly=True)
    objUVs = splitUVsPerMesh(selOrg, selObjs)
    for uvs in objUVs:
        pm.polyMapDel(uvs, constructionHistory=True)


def distributeShells(win=None):

    # Check for UV selection
    checkSel("UV")

    # Function for determining the target shell used for Distribute Shells: Towards Target
    def getTarget(list):
    
        # Vars
        dir = ""
        listA = []
        listB = []

        # Calculate center point and dimensions for the entire selection
        pm.select(list)
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        sizeU = (uvBox[0][1] - uvBox[0][0])
        sizeV = (uvBox[1][1] - uvBox[1][0])

        # Get direction axis
        if sizeU > sizeV or sizeU == sizeV:
            dirAxis = 0
            totalDist = sizeU
        else: 
            dirAxis = 1
            totalDist = sizeV

        # Sort shells into two lists.
        for shell in list:
            pm.select(shell)
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)

            # Add shell to list
            if dirAxis == 0:
                center = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
                if center < centerU:
                    listA.append(shell)
                    dir = 1
                else:
                    listB.append(shell)
                    dir = 2
            else: 
                center = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
                if center < centerV:
                    listA.append(shell)
                    dir = 3
                else:
                    listB.append(shell)
                    dir = 4

        # Get direction and target shell
        if len(listA) == 1:
            targetShell = listA[0]
        else: targetShell = listB[0]

        # Calc distribution distance
        pm.select(targetShell)
        targetBox = pm.polyEvaluate(boundingBoxComponent2d=True)

        if dirAxis == 0:
            targetDist = abs(targetBox[0][1] - targetBox[0][0])            
        else:
            targetDist = abs(targetBox[1][1] - targetBox[1][0])

        dist = (totalDist - targetDist) / (len(shellList)-1)

        # Invert dist if we are distributing towards bottom or the left
        if dir == 2 or dir == 4:
            dist = -dist

        # Place the targetShell on position [0]
        shellList.insert(0, shellList.pop(shellList.index(targetShell)))

        return(targetShell, shellList, dist, dirAxis)


    # Set with shells that have been processed
    excludedSet = set()

    # Read optVars
    spacing = pm.optionVar["distrSpaceVal_NSUV"]
    dir = pm.optionVar["distrDir_NSUV"]
    if dir == 1 or dir == 2:
        dirAxis = 0 # Along U
    else: dirAxis = 1

    if pm.optionVar["distrMethod_NSUV"] == 1: toTarget = False
    else: toTarget = True

    # Store original selection
    selOrg = pm.ls(selection=True) 

    # Get shells from selection
    shellList = getShells()

    # Standard - Sort shells
    if toTarget == False:
        stackShells(shellList)
        if dirAxis == 0: 
            shellList = sortShells(shellList, 0)
        else: 
            shellList = sortShells(shellList, 1)

    # Towards target
    elif toTarget == True:
        pm.select(selOrg)
        targetShell, shellList, dist, dirAxis = getTarget(shellList)
        
        # Exclude the target shell and one start shell
        excludedSet.update(targetShell)
        if targetShell != shellList[0]:
            excludedSet.update(shellList[0])
        else:
            excludedSet.update(shellList[1])

    # Create progress window
    createProgWin("Distributing...", len(shellList))    
    shellsTotal = shellsRemain = len(shellList) # Shell count

    # Start distributing...
    counter = 0
    while counter < len(shellList):

        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break

        # Edit the progress window
        pm.progressWindow(
            edit=True,
            progress=(shellsTotal - shellsRemain),
            status="Processing shells. %s shells remaining."%shellsRemain
        )

        # Get the bounding box info from first shell
        if counter == 0:
            pm.select(shellList[0])

            if toTarget == False:
                if dirAxis == 0: xmaxLast = pm.polyEvaluate(boundingBoxComponent2d=True)[0][1]
                else: ymaxLast = pm.polyEvaluate(boundingBoxComponent2d=True)[1][1]   
                excludedSet.update(shellList[0]) # Add shell to excluded list

        else:
            # Select unprocessed shells
            if counter == 1: pm.select(shellList)
            pm.select(excludedSet, deselect=True)

            if toTarget == False:
                if dirAxis == 0: # Move shell along U
                    xmin = pm.polyEvaluate(boundingBoxComponent2d=True)[0][0]
                    val = abs(xmaxLast - xmin) + spacing
                    if dir == 2: val = -val

                    if xmaxLast > xmin: pm.polyEditUV(uValue=val)
                    else: pm.polyEditUV(uValue=-val)

                    xmaxLast = pm.polyEvaluate(boundingBoxComponent2d=True)[0][1] 

                else: # Move shell along V
                    ymin = pm.polyEvaluate(boundingBoxComponent2d=True)[1][0]
                    val = abs(ymaxLast - ymin) + spacing
                    if dir == 4: val = -val

                    if ymaxLast > ymin: pm.polyEditUV(vValue=val)
                    else: pm.polyEditUV(vValue=-val)

                    ymaxLast = pm.polyEvaluate(boundingBoxComponent2d=True)[1][1]

            else:
                if dirAxis == 0: # Move shell towards target along U
                    if counter != 1: # Skip start shell
                        pm.polyEditUV(uValue=dist)

                else: # Move shell towards target along V
                    if counter != 1: # Skip start shell
                        pm.polyEditUV(vValue=dist)

            # Add current shell to exclusion set
            excludedSet.update(shellList[counter])

        # Modify counters
        shellsRemain -= 1
        counter += 1

    # Close the progress window
    pm.progressWindow(endProgress=True)

    # Reselect the original selection 
    pm.select(selOrg)
    
    # Close distribute window
    if win != None:
        pm.deleteUI(win)


# Cycles edge color
def edgeColor(dir):

    # Display color
    dispCol = pm.displayColor("polyEdge", query=True, active=True)

    # Set the color variable
    if dir == "forward":
        if dispCol == 31: dispCol = 1 # Cycle around
        else: dispCol += 1

    elif dir == "backward":
        if dispCol == 1: dispCol = 31 # Cycle around
        else: dispCol -= 1

    # Change the edge color
    pm.displayColor("polyEdge", dispCol , active=True)


# Flips a UV selection
def flipUVs(direction):

    # Update and get pivot coords
    updateManipCoords()
    manipCoords = pm.optionVar["manipCoords_NSUV"]

    # Flip
    if direction == "U":
        pm.polyEditUV(
            pivotU=manipCoords[0],
            scaleU = -1
        )
    if direction == "V":
        pm.polyEditUV(
            pivotV=manipCoords[1],
            scaleV = -1
        )


# Offset back all shells into the default UV range
def gatherShells():
    
    # Selection check
    checkSel("meshUV")
    
    # Store selection
    selOrg = pm.ls(flatten=True, selection=True)
    selUVs = pm.ls(pm.polyListComponentConversion(toUV=True), flatten=True)
    
    # Progress window
    createProgWin("Gathering...", len(selUVs))
    
    # Go through each UV
    for uvCoord in selUVs:
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break

        move = False
        offsetU = 0.0
        offsetV = 0.0
        position = pm.polyEditUV(uvCoord, query=True)
        
        # Get U offset distance as whole 0-1 -steps
        if position[0] < 0:
            offsetU = 1 - math.trunc(position[0])
            move = True          
        elif position[0] > 1:
            offsetU = 0 - math.trunc(position[0])
            move = True
            
        # Get V offset distance as whole 0-1 -steps
        if position[1] < 0:
            offsetV = 1 - math.trunc(position[1])
            move = True          
        elif position[1] > 1:
            offsetV = 0 - math.trunc(position[1])
            move = True
        
        # Move the shell
        if move == True:
            pm.select(uvCoord, replace=True)
            pm.polyEditUVShell(
                relative=True, 
                uValue=offsetU, 
                vValue=offsetV
            )
            
        # Update the progress window
        pm.progressWindow(edit=True, step=1)
        
    # Close the progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg, replace=True)
    

# Finds the active shader on a mesh
def getActiveShader(txtEditor):

    # Mesh check
    def isMesh(obj):
        if obj == "": return 0        
        return len(pm.polyListComponentConversion(obj, toFace=True))    

    # Get list of active images in the texture editor
    imgNameList = pm.textureWindow(txtEditor, query=True, imageNames=True)
    
    # We will get None if we are in isolate select mode
    if imgNameList == [] or imgNameList == None: 
        return
    
    # Loop through all images - use counter to get the correct GID
    i=0
    for imgName in imgNameList:
        i += 1
        
        # Split image names into object and shader
        buffer = []
        buffer = imgName.split(" ")
        obj = buffer[0]
        shader = buffer[2]
        
        # Skip if not mesh
        if not isMesh(obj): continue
        
        # Now find active Group ID (GID)
        activeGid = pm.getAttr(obj + ".dfgi")
        objGroupList = pm.listConnections((shader + ".dsm"), plugs=True)
        shapes = pm.listConnections((shader + ".dsm"), shapes=True)
        
        # Check all objects
        for objGroup in objGroupList:
            gid =- 99

            # Get the group ID from the current objectGroup (if it exists)
            if pm.objExists(objGroup + ".gid"):
                gid = pm.getAttr(objGroup + ".gid")
            else: continue

            if (gid == activeGid): return i
    return 


# Gets the UV sets from a mesh or component selection. Only fetches the sets from the first mesh.
# Returns tuple with 3 objects: all sets, current set, instanced sets
def getSets():

    # Check for mesh or polygon components
    sel = pm.filterExpand(selectionMask=(12, 31, 32, 34, 35))
    if sel != [] and sel != None:

        # Get only one mesh/shape if we have several selected
        shape = getShapes()

        if len(shape) > 1:
            shape = shape[0]

        # All sets
        varA = pm.polyUVSet(
            shape, query=True,
            allUVSets=True,
            perInstance=True,
        )

        # Current set
        varB = pm.polyUVSet(
            shape, query=True,
            currentUVSet=True,
        )

        return (varA, varB)

    else: return


# Gets all shapes from a selection, returns them as a list
def getShapes():

    shapeList = pm.ls(selection=True, objectsOnly=True)
    shapeList = list(set(shapeList)) # Remove duplicates

    return shapeList


def getShells(inc=None):
    ''' Description: Returns list with each shell in it. Used for lots of things.
        @params: inc (obj) - Components other than UVs (optional).
    '''

    # Get selected UVs (or selection as UVs)
    if inc != None:
        uvList = pm.ls( pm.polyListComponentConversion(inc, toUV=True), flatten=True)
    else:
        uvList = pm.ls(selection=True, flatten=True)

    # Get selected meshes
    objList = pm.ls(uvList, objectsOnly=True, flatten=True)
    objList = list(set(objList))

    # Create list of shells per selected object
    shellsList = []
    for obj in objList:
        shellsDict = collections.defaultdict(list)

        # Create uvShellIds -array
        uvShellIDs, uvShellArray = obj.getUvShellsIds()
        selShellsIDs = set() # Set with selected shells' IDs

        # Get shell IDs for each UV in selection
        for uv in uvList:
            i = int( uv.split('[')[-1].split(']')[0] ) # Get UV index
            selShellsIDs.add(uvShellIDs[i])

        # Get selected shells' UVs as a dictionary
        for i, shellID in enumerate(uvShellIDs):
            if shellID not in selShellsIDs: continue
            else:
                uv = pm.PyNode("%s.map[%s]"%(obj, i))
                shellsDict[shellID].append(uv)

        # Append the shells of the current object
        for value in shellsDict.values():
            shellsList.append(value)

    return shellsList


# Fetch Texel Density off a single face selection
def getTD(field):

    # Calculates the texel density
    def calcTD(face):
        area3D = face.getArea(space="world")
        area2D = face.getUVArea()
        sizeMap = pm.optionVar["tdSize_NSUV"]
        result = (math.sqrt(area2D)/math.sqrt(area3D)) * sizeMap
        return result


    # Check selection
    checkSel("any")
    
    # Store selection
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Convert selection to facess and select it
    selUVs = pm.polyListComponentConversion(toFace=True)
    pm.select(selUVs)

    # Get list of faces
    faceList = pm.ls(selection=True, flatten=True)

    # Calculate average TD by looping through the face list
    tdAverage = 0    
    for face in faceList:
        tdAverage += calcTD(face)        
    result = tdAverage / len(faceList)
    
    # Update field and optVar - then reselct the original seleciton
    field.setValue1(result)
    pm.optionVar["td_NSUV"] = result    
    pm.select(selOrg)


# Splits up a shared edge into two uvEdges - Returns a tuple with the uvEdges
def getUVEdgePairs(selUVs):

    i = 0

    # Find uvEdge pairs by first finding a face that is shared by 2 UVs in selUVs
    while i != 4:
        try:
            uvA_faceList = pm.ls( pm.polyListComponentConversion(selUVs[0], fromUV=True, toFace=True), flatten=True, long=True )
            uvB_faceList = pm.ls( pm.polyListComponentConversion(selUVs[i], fromUV=True, toFace=True), flatten=True, long=True )
        except IndexError: # Will occur if the UVs are not on the same shared edge
            errorCode(19)
        
        # Conv. face lists to sets and get the intersecting face
        intersection = list(set(uvA_faceList) & set(uvB_faceList))
        
        # Might get more than one face. If so, check each face's UVs against selUVs
        if len(intersection) != 1:
            for face in intersection:
                faceUVs = pm.ls( pm.polyListComponentConversion(face, fromFace=True, toUV=True), flatten=True, long=True )
                uvCount = 0
                for uv in faceUVs:
                    if uv in selUVs:
                        uvCount += 1
                if uvCount == 2:
                    intersection = face
                    break

        if intersection != []: 
        
            # Now get the UVs of the intersecting face
            if type(intersection) is list: # as it might be a list 
                faceUVs = pm.ls( pm.polyListComponentConversion(intersection[0], fromFace=True, toUV=True), flatten=True, long=True )
            else:
                faceUVs = pm.ls( pm.polyListComponentConversion(intersection, fromFace=True, toUV=True), flatten=True, long=True )

            # Match the UVs of the intersecting face towards the original UV selection
            j = 0
            removeList = []
            while j != len(faceUVs):
                if faceUVs[j] not in selUVs:
                    removeList.append(faceUVs[j])
                j += 1

            # Remove UVs that weren't found in the original UV selection
            for uv in removeList:
                if uv in faceUVs:
                    faceUVs.remove(uv)

            # Store in logical var, break out...
            uvEdgeA = faceUVs
            break

        else:
            i += 1

    # Get the final uvEdge by exclusion and store in a logical var   
    removeList = []
    for uv in selUVs:
        if uv in uvEdgeA:
            removeList.append(uv)        
    for uv in removeList: 
        selUVs.remove(uv)
    uvEdgeB = selUVs

    # Return the pairs
    uvEdgePairs = (uvEdgeA, uvEdgeB)
    return uvEdgePairs


# Toggles between hardened or softened shell borders
def hardSoftShellBorders():

    # Check selection
    checkSel("mesh")

    # Get selection
    meshList = pm.ls(selection=True, objectsOnly=True)

    # Loop thru every selected mesh
    for subMesh in meshList:

        # Select UV border, convert to contained edges and harden
        pm.select(subMesh)
        pm.runtime.ConvertSelectionToUVs()
        pm.runtime.SelectUVBorder()
        pm.runtime.ConvertSelectionToContainedEdges()
        
        # Get list of edges and check what we have more of: hard or soft edges
        edgeList = pm.ls(selection=True, flatten=True)
        edgeLen = len(edgeList)
        counter = 0
        for edge in edgeList:
            if edge.isSmooth() == True:
                counter += 1
        if counter >= edgeLen / 2: # SOFT
            pm.polySoftEdge(angle=0, constructionHistory=True)
        else: # HARD
            pm.polySoftEdge(angle=180, constructionHistory=True)
            
    # Reselect original
    pm.select(meshList)


# Layout
def layoutUVs(win=None):

    # Vars
    layoutMethodVar = pm.optionVar["layoutMode_NSUV"]
    multiObjVar = pm.optionVar["layoutPackMode_NSUV"]
    place = pm.optionVar["layoutPlace_NSUV"]
    position = pm.optionVar["layoutPlacePres_NSUV"]
    scaleModeVar = pm.optionVar["layoutScaling_NSUV"]
    u3dLoaded = pm.pluginInfo("Unfold3D", loaded=True, query=True)

    # Unfold3D vars
    if mayaVer >= 201650 and u3dLoaded and layoutMethodVar == 1: # 2016 Ext 2 and Unfold3D

        # Placement
        if place == 1: # Pre-defined
            if position == 1: # Default UV range
                packBoxVar = [0.0, 1.0, 0.0, 1.0]

            elif position == 2: # Left half
                packBoxVar = [0.0, 0.5, 0.0, 1.0]

            elif position == 3: # Right half
                packBoxVar = [0.5, 1.0, 0.0, 1.0]

            elif position == 4: # Top half
                packBoxVar = [0.0, 1.0, 0.5, 1.0]

            elif position == 5: # Top left
                packBoxVar = [0.0, 0.5, 0.5, 1.0]

            elif position == 6: # Top right
                packBoxVar = [0.5, 1.0, 0.5, 1.0]

            elif position == 7: # Bottom half
                packBoxVar = [0.0, 1.0, 0.0, 0.5]

            elif position == 8: # Bottom left
                packBoxVar = [0.0, 0.5, 0.0, 0.5]

            elif position == 9: # Bottom right
                packBoxVar = [0.5, 1.0, 0.0, 0.5]

        else: # Custom
            packBoxVar = [
                pm.optionVar["layoutRangeMinU_NSUV"],
                pm.optionVar["layoutRangeMaxU_NSUV"],
                pm.optionVar["layoutRangeMinV_NSUV"],
                pm.optionVar["layoutRangeMaxV_NSUV"],
                ]

        # Pre-scaling
        if pm.optionVar["layoutPreScaling_NSUV"] == 1:
            preScaleVar = 0
        elif pm.optionVar["layoutPreScaling_NSUV"] == 2:
            preScaleVar = 1
        else:
            preScaleVar = pm.optionVar["layoutPreScaling_NSUV"] ## The prescale -flag on the u3dLayout -cmd has nothing on 2 but on 3

        if pm.optionVar["layoutRotate_NSUV"] == True:
            rotStepVal = pm.optionVar["layoutRotStep_NSUV"]
        else: rotStepVal = 0

        preRotVar = pm.optionVar["layoutPreRotation_NSUV"] - 1
        distrVal = pm.optionVar["layoutDistr_NSUV"] - 1

    else: # Legacy vars
        fittingVar = pm.optionVar["layoutFitting_NSUV"] - 1
        layoutVar = pm.optionVar["layoutShell_NSUV"] - 1
        qMethod = pm.optionVar["layoutQuickType_NSUV"]
        rotateVar = pm.optionVar["layoutRotate_NSUV"] - 1
        scaleVar = pm.optionVar["layoutScaling_NSUV"] - 1
        separateVar = pm.optionVar["layoutSepShells_NSUV"] - 1

        if layoutVar == 1: layoutVar = 2
        elif layoutVar == 2: layoutVar = 1

        # Placement
        if layoutMethodVar == 1 or layoutMethodVar == 2: # Legacy: Default cases

            if place == 1: # Pre-defined

                if position == 1: # Default UV range
                    rangeUVar = 1.0
                    rangeVVar = 1.0
                    offsetUVar = 0.0
                    offsetVVar = 0.0
                    
                elif position == 2: # Left half
                    rangeUVar = 0.5
                    rangeVVar = 1.0
                    offsetUVar = 0.0
                    offsetVVar = 0.0
                    
                elif position == 3: # Right half
                    rangeUVar = 0.5
                    rangeVVar = 1.0
                    offsetUVar = 0.5
                    offsetVVar = 0.0
                    
                elif position == 4: # Top half
                    rangeUVar = 1.0
                    rangeVVar = 0.5
                    offsetUVar = 0.0
                    offsetVVar = 0.5
                    
                elif position == 5: # Top left
                    rangeUVar = 0.5
                    rangeVVar = 0.5
                    offsetUVar = 0.0
                    offsetVVar = 0.5
                    
                elif position == 6: # Top right
                    rangeUVar = 0.5
                    rangeVVar = 0.5
                    offsetUVar = 0.5
                    offsetVVar = 0.5
                    
                elif position == 7: # Bottom half
                    rangeUVar = 1.0
                    rangeVVar = 0.5
                    offsetUVar = 0.0
                    offsetVVar = 0.0
                    
                elif position == 8: # Bottom left
                    rangeUVar = 0.5
                    rangeVVar = 0.5
                    offsetUVar = 0.0
                    offsetVVar = 0.0
                    
                elif position == 9: # Bottom right
                    rangeUVar = 0.5
                    rangeVVar = 0.5
                    offsetUVar = 0.5
                    offsetVVar = 0.0

            else: # Custom
                rangeUVar = pm.optionVar["layoutRangeMaxU_NSUV"] - pm.optionVar["layoutRangeMinU_NSUV"]
                rangeVVar = pm.optionVar["layoutRangeMaxV_NSUV"] - pm.optionVar["layoutRangeMinV_NSUV"]
                offsetUVar = pm.optionVar["layoutRangeMinU_NSUV"]
                offsetVVar = pm.optionVar["layoutRangeMinV_NSUV"]

        else: # Legacy: Quick
            if qMethod == 1: 
                layoutVar = 2
                scaleVar = 1
            else: 
                layoutVar = 1
                scaleVar = 0

        # Pre-scaling
        if pm.optionVar["layoutPreScaling_NSUV"] == 1:
            preScaleVar = 0
        elif pm.optionVar["layoutPreScaling_NSUV"] == 2:
            preScaleVar = 1
        else:
            preScaleVar = 2


    # Validate selection
    checkSel("any")

    # Store original selection
    selOrg = pm.ls(selection=True, flatten=True)
    selOrg2 = pm.cmds.ls(selection=True, flatten=True, objectsOnly=True)
    polyLayoutBool = False

    # Setup shells
    shellList = []
    if (u3dLoaded and multiObjVar == 2) or (not u3dLoaded and layoutMethodVar == 2) or layoutMethodVar == 3: # Separatly

        # Comps selection
        if pm.filterExpand(selectionMask=12) == [] or pm.filterExpand(selectionMask=12) == None:

            # Get UV and meshes
            selUVs = pm.ls(pm.polyListComponentConversion(toUV=True), flatten=True)
            pm.mel.toggleSelMode()
            pm.selectMode(object=True)
            selObjs = pm.filterExpand(selectionMask=12)

            # Intersect all selected UVs with the ones in each individual object
            for item in selObjs:
                objUVs = pm.ls(pm.polyListComponentConversion(item, toUV=True), flatten=True)
                intersection = list(set(selUVs) & set(objUVs))
                shellList.append(intersection)

        else: # Mesh selection
            selObjs = pm.ls(selection=True, flatten=True)
            for item in selObjs: # ...get UV's of each mesh
                temp = pm.ls(pm.polyListComponentConversion(item, toUV=True), flatten=True)
                shellList.append(temp)
                
    else: # Together
        temp = pm.ls(pm.polyListComponentConversion(toUV=True), flatten=True)
        shellList.append(temp)

    # Begin layouting
    for item in shellList:

        ## Unfold3D layout
        if mayaVer >= 201650 and u3dLoaded and layoutMethodVar == 1: # 2016 Ext 2

            pm.u3dLayout(
                item,
                layoutScaleMode=scaleModeVar,
                multiObject=multiObjVar,
                mutations=pm.optionVar["layoutItr_NSUV"],
                packBox=packBoxVar,
                preRotateMode=preRotVar,
                preScaleMode=preScaleVar,
                resolution=pm.optionVar["layoutRes_NSUV"],
                rotateMax=pm.optionVar["layoutRotMax_NSUV"],
                rotateMin=pm.optionVar["layoutRotMin_NSUV"],
                rotateStep=rotStepVal, 
                shellSpacing=pm.optionVar["layoutShellPadding_NSUV"],
                tileAssignMode=distrVal,
                tileMargin=pm.optionVar["layoutTilePadding_NSUV"],
                tileU=pm.optionVar["layoutGridUVal_NSUV"],
                tileV=pm.optionVar["layoutGridVVal_NSUV"],
                translate=pm.optionVar["layoutTranslate_NSUV"],
            )

        ## Legacy layout
        elif (mayaVer >= 201650 and u3dLoaded and layoutMethodVar == 2 and multiObjVar == 1) or layoutMethodVar == 1:

            # Unfold
            if mayaVer >= 201600:
                pm.polyMultiLayoutUV(
                    item,
                    flipReversed=pm.optionVar["layoutFlip_NSUV"],
                    gridU=pm.optionVar["layoutGridUVal_NSUV"],
                    gridV=pm.optionVar["layoutGridVVal_NSUV"],
                    layout=layoutVar,
                    layoutMethod=fittingVar,
                    offsetU=offsetUVar,
                    offsetV=offsetVVar,
                    percentageSpace=pm.optionVar["layoutShellPadding_NSUV"],
                    prescale=preScaleVar,
                    rotateForBestFit=rotateVar,
                    scale=scaleVar,
                    sizeU=rangeUVar,
                    sizeV=rangeVVar,
                )
            else:
                pm.polyMultiLayoutUV(
                    item,
                    flipReversed=pm.optionVar["layoutFlip_NSUV"],
                    layout=layoutVar,
                    layoutMethod=fittingVar,
                    offsetU=offsetUVar,
                    offsetV=offsetVVar,
                    percentageSpace=pm.optionVar["layoutShellPadding_NSUV"],
                    prescale=preScaleVar,
                    rotateForBestFit=rotateVar,
                    scale=scaleVar,
                    sizeU=rangeUVar,
                    sizeV=rangeVVar,
                )
                
        elif layoutMethodVar == 2:

            if mayaVer >= 201600:
                polyLayoutBool = True
                pm.polyLayoutUV(
                    item,
                    constructionHistory=True,
                    flipReversed=pm.optionVar["layoutFlip_NSUV"],
                    # frozen=1,
                    gridU=pm.optionVar["layoutGridUVal_NSUV"],
                    gridV=pm.optionVar["layoutGridVVal_NSUV"],
                    layout=layoutVar,
                    layoutMethod=fittingVar,
                    percentageSpace=pm.optionVar["layoutShellPadding_NSUV"],
                    rotateForBestFit=rotateVar,
                    scale=scaleVar,
                    separate=separateVar,
                    )


        ## Quick layout
        else:
            polyLayoutBool = True
            if qMethod:
                pm.polyLayoutUV(
                    item,
                    constructionHistory=True,
                    flipReversed=True,
                    frozen=1,
                    gridU=1,
                    gridV=1,
                    layout=layoutVar,
                    layoutMethod=1,
                    percentageSpace=0.2,
                    rotateForBestFit=1,
                    scale=1,
                    separate=0,
                )

            if qMethod == 3: # Along V

                # Rotate and align shells
                pm.select(item)
                pm.polyEditUV(
                    item,
                    angle=90,
                    pivotU=0.0,
                    pivotV=0.0
                )
                alignShells("uMin")

                # Get selection bounds, calculate distance to U=0 and translate
                uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
                offset = uvBox[0][1] - uvBox[0][0]
                pm.polyEditUV(uValue=offset)

    # Select original selection
    pm.select(selOrg)
    if polyLayoutBool: # Loop through meshes and add to selection if we used polyLayoutUV
        for item in selOrg2:
            if u3dLoaded: # This MEL command requires Unfold3D
                pm.mel.doMenuComponentSelection(item, "meshComponents");

    # Activate the move tool
    pm.setToolTo("moveSuperContext")


# Locks the window size
def lockWindow(win, state):
    if state == 1:
        win.setSizeable(False)
        pm.optionVar["sizeableWin_NSUV"] = True
    else:
        win.setSizeable(True)
        pm.optionVar["sizeableWin_NSUV"] = False


# Update the manipulation field and associated optionVars
def manipField(field, action):

    # Update the optionVar
    pm.optionVar["manipAmt_NSUV"] = field.getValue()

    # Reset to 0
    if action == 0:
        field.setValue(0.0)
        pm.optionVar["manipAmt_NSUV"] = 0.0

    # Reset to 1
    elif action == 1:
        field.setValue(1.0)
        pm.optionVar["manipAmt_NSUV"] = 1.0

    # Get value
    elif action == "get":
        pm.optionVar["manipAmt_NSUV"] = field.getValue()

    # Double value
    elif action == "double":
        newVal = pm.optionVar["manipAmt_NSUV"] = pm.optionVar["manipAmt_NSUV"] * 2
        field.setValue(newVal)

    # Split value
    elif action == "split":
        newVal = pm.optionVar["manipAmt_NSUV"] = pm.optionVar["manipAmt_NSUV"] / 2
        field.setValue(newVal)

    # U-distance
    elif action == "distU":

        # Selection check
        checkSel("UV")

        # Get bounding box coords, and absolute distance between
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newVal = abs(uvBox[0][1] - uvBox[0][0])

        pm.optionVar["manipAmt_NSUV"] = newVal
        field.setValue(newVal)

    # U-distance
    elif action == "distV":

        # Selection check
        checkSel("UV")

        # Get bounding box coords, and absolute distance between
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newVal = abs(uvBox[1][1] - uvBox[1][0])

        pm.optionVar["manipAmt_NSUV"] = newVal
        field.setValue(newVal)

    # Store value into var A
    elif action == "setA":
        newVal = pm.optionVar["manipVarA_NSUV"] = field.getValue()
        pm.optionVar["manipAmt_NSUV"] = newVal

    # Load value from var A
    elif action == "getA":
        newVal = pm.optionVar["manipAmt_NSUV"] = pm.optionVar["manipVarA_NSUV"]
        field.setValue(newVal)

    # Store value into var B
    elif action == "setB":
        newVal = pm.optionVar["manipVarB_NSUV"] = field.getValue()
        pm.optionVar["manipAmt_NSUV"] = newVal

    # Load value from var B
    elif action == "getB":
        newVal = pm.optionVar["manipAmt_NSUV"] = pm.optionVar["manipVarB_NSUV"]
        field.setValue(newVal)

    # Store value into var C
    elif action == "setC":
        newVal = pm.optionVar["manipVarC_NSUV"] = field.getValue()
        pm.optionVar["manipAmt_NSUV"] = newVal

    # Load value from var C
    elif action == "getC":
        newVal = pm.optionVar["manipAmt_NSUV"] = pm.optionVar["manipVarC_NSUV"]
        field.setValue(newVal)

    elif action == "getAngle":

        # Selection check
        checkSel("UV")

        # Check for UV selection?
        sel = pm.ls(selection=True, flatten=True)
        newVal = calcArctanAngle(sel[0], sel[1])
        newVal = abs(newVal)

        # Reduce to angle under 45 degs
        if newVal > 45:
            newVal = 90 - newVal

        # Update field and optionVar
        pm.optionVar["manipAmt_NSUV"] = newVal
        field.setValue(newVal)


# UV mapping
def mapping(projection, planarAxis=None, win=None):

    # Vars
    layoutVar, methodVar, optimizeVar, scaleVar = (0,)*4
    selOrg = None
    projList = []
    ssVar = False

    # Method for creating meshFace -groups from a selection containing both meshes and faces
    # Returned list contains meshes on the first index number and meshFace -groups on the second
    def mappingCreateFaceGrpList():

        # Make sure we have faces and not meshes
        pm.mel.ConvertSelectionToFaces()
        selection = pm.ls(selection=True)

        shapes = getShapes()

        # Create main list - populate with null objects. One None per shape node
        mainList = [None] * len(shapes)

        # Loop through every shape node, one index at a time
        for count in range(len(shapes)):
            meshFaceList = []
            for meshFaceGrp in selection:
               
                # Create sub list with all meshFace -groups belonging to each shape node
                if meshFaceGrp.node() == shapes[count]:
                    meshFaceList.append(meshFaceGrp)
                    # selection.remove(meshFaceGrp) # Reduces unneccessary scanning - but breaks script

            # Add meshFace -sub list to main list
            mainList[count] = meshFaceList

        # Return cleaned meshFace -group list
        return mainList


    # Method for setting the projection attribs of an automatic projection
    def mappingSetAttr(meshFaceGrp, projType):

        proj = None

        # Get bounding box, store center points (which is where the manipulator is)
        bounds = pm.exactWorldBoundingBox(meshFaceGrp)
        manipX = (bounds[0] + bounds[3]) / 2.0
        manipY = (bounds[1] + bounds[4]) / 2.0
        manipZ = (bounds[2] + bounds[5]) / 2.0

        # Calculate XYZ distances of the bounding box, and get scale value
        distX = abs(bounds[3] - bounds[0])
        distY = abs(bounds[4] - bounds[1])
        distZ = abs(bounds[5] - bounds[2])
        scaleVal = max(max(distX, distY), distZ)

        # Get shape node and projection node from incomming meshFaceGrp
        if projType == "auto":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyAutoProj")[0]
        elif projType == "cyl":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyCylProj")[0]
        elif projType == "plane":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polyPlanarProj")[0]
        elif projType == "sphere":
            proj = pm.listConnections( meshFaceGrp[0].node() , destination=True, type="polySphProj")[0]

        # Editor projection node
        if projType == "auto":

            # World space
            if pm.optionVar["mapAutoMS2RadGrp_NSUV"] == 1:
                pm.setAttr(proj + ".pivotX", manipX)
                pm.setAttr(proj + ".pivotY", manipY)
                pm.setAttr(proj + ".pivotZ", manipZ)

                pm.setAttr(proj + ".translateX", manipX)
                pm.setAttr(proj + ".translateY", manipY)
                pm.setAttr(proj + ".translateZ", manipZ)

            # Local space
            else: 
                pm.setAttr(proj + ".pivotX", 0.0)
                pm.setAttr(proj + ".pivotY", 0.0)
                pm.setAttr(proj + ".pivotZ", 0.0)

                pm.setAttr(proj + ".translateX", 0.0)
                pm.setAttr(proj + ".translateY", 0.0)
                pm.setAttr(proj + ".translateZ", 0.0)

            pm.setAttr(proj + ".scaleX", scaleVal)
            pm.setAttr(proj + ".scaleY", scaleVal)
            pm.setAttr(proj + ".scaleZ", scaleVal)

            # Add projection node to projList...
            if pm.optionVar["mapAutoMSBox2_NSUV"] == True:
                projList.append(proj)


        elif projType == "cyl":
            pm.setAttr(proj + ".projectionHorizontalSweep", pm.optionVar["mapCylindricalSweep_NSUV"])

            # Add projection node to projList...
            if pm.optionVar["mapCylindricalMS2Box_NSUV"] == True:
                projList.append(proj)


        elif projType == "plane":

            # Add projection node to projList...
            if pm.optionVar["mapPlanarMS3Box_NSUV"] == True:
                projList.append(proj)


        elif projType == "sphere":
            pm.setAttr(proj + ".projectionHorizontalSweep", pm.optionVar["mapSphericalSweep1_NSUV"])
            pm.setAttr(proj + ".projectionVerticalSweep", pm.optionVar["mapSphericalSweep2_NSUV"])

            # Add projection node to projList...
            if pm.optionVar["mapSphericalMS2Box_NSUV"] == True:
                projList.append(proj)

        else:
            print("Unknown projection type sent to core.mapping.mappingSetAttr()")


    # Check for valid face or mesh selection
    checkSel("faceMesh")

    # Store original selection
    selOrg = pm.ls(selection=True)


    ## Automatic projection
    if projection == "auto":

        # Eval optVars
        if pm.optionVar["mapAutoMS1RadGrp_NSUV"] == 2:
            optimizeVar = 1

        if pm.optionVar["mapAutoMS2RadGrp_NSUV"] == 1:
            ssVar = True

        if pm.optionVar["mapAutoLayoutMenu_NSUV"] == "Along U":
            layoutVar = 1
        elif pm.optionVar["mapAutoLayoutMenu_NSUV"] == "Into Square":
            layoutVar = 2
        elif pm.optionVar["mapAutoLayoutMenu_NSUV"] == "Tile":
            layoutVar = 3

        if pm.optionVar["mapAutoLayoutRadGrp1_NSUV"] == 2:
            scaleVar = 1
        elif pm.optionVar["mapAutoLayoutRadGrp1_NSUV"] == 3:
            scaleVar = 3
            
        if pm.optionVar["mapAutoLayoutRadGrp2_NSUV"] == 2:
            methodVar = 1

        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()

        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:

            # Project with custom settings
            if pm.optionVar["mapAutoMethod_NSUV"] == 1:

                # Custom UV set name
                if pm.optionVar["mapAutoSetBox_NSUV"] == True:
                    pm.polyAutoProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapAutoSetBox_NSUV"],
                        layout=layoutVar,
                        layoutMethod=methodVar,
                        optimize=optimizeVar,
                        percentageSpace=pm.optionVar["mapAutoSpaceVal_NSUV"],
                        planes=int(pm.optionVar["mapAutoMSMenu_NSUV"]),
                        scaleMode=scaleVar,
                        uvSetName=pm.optionVar["mapAutoSet_NSUV"],
                        worldSpace=ssVar,
                    )
                else: # No custom UV set name
                    pm.polyAutoProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapAutoSetBox_NSUV"],
                        layout=layoutVar,
                        layoutMethod=methodVar,
                        optimize=optimizeVar,
                        percentageSpace=pm.optionVar["mapAutoSpaceVal_NSUV"],
                        planes=int(pm.optionVar["mapAutoMSMenu_NSUV"]),
                        scaleMode=scaleVar,
                        worldSpace=ssVar,
                    )
                
                # Set projection node attributes
                mappingSetAttr(meshFaceGrp, "auto")
            
                # Normalize results
                if pm.optionVar["mapAutoNormBox_NSUV"] == True:    

                    # Convert to UVs            
                    priorSel = pm.ls(selection=True)     
                    pm.select( pm.polyListComponentConversion(selOrg, toUV=True) )
                    
                    # Normalize
                    normalizeShells(0)
                    
                    # Reselect selection
                    pm.select(priorSel)
                    
                
            # Project with quick settings
            else:            
                pm.polyAutoProjection(
                    selOrg,
                    constructionHistory=True,
                    createNewMap=False,
                    layout=2,
                    layoutMethod=0,
                    optimize=0,
                    percentageSpace=0.2,
                    scaleMode=1,
                    worldSpace=True,
                )
                
        # Select original selection
        pm.select(selOrg)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapAutoMSBox2_NSUV"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")
    
    
    ## Cylindrical projection
    elif projection == "cyl":
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:

            # Custom UV set name
            if pm.optionVar["mapCylindricalSetBox_NSUV"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapCylindricalSetBox_NSUV"],
                    insertBeforeDeformers=pm.optionVar["mapCylindricalMS1Box_NSUV"],
                    smartFit=True,
                    type="cylindrical",
                    uvSetName=pm.optionVar["mapCylindricalSet_NSUV"],
                )
            else: # No custom UV set name
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    insertBeforeDeformers=pm.optionVar["mapCylindricalMS1Box_NSUV"],
                    smartFit=True,
                    type="cylindrical",
                )
                
            # Set projection node attributes
            mappingSetAttr(meshFaceGrp, "cyl")
            
        # Select original selection
        pm.select(selOrg)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapCylindricalMS2Box_NSUV"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")

    
    ## Normal based projection
    elif projection == "normal":
    
        # Vars
        vectorMean = []
        vectorCount = 0

        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
        
            pm.select(meshFaceGrp)
            meshFaceGrpFlat = pm.ls(selection=True, flatten=True)
        
            # Calculate mean vector, then invert it
            for face in meshFaceGrpFlat:
                vectorMean.append( face.getNormal() )

            vectorMean = sum(vectorMean) / len(vectorMean)
            if vectorMean[0] != 0:
                vectorMean[0] = -vectorMean[0]
            if vectorMean[1] != 0:
                vectorMean[1] = -vectorMean[1]
            if vectorMean[2] != 0:
                vectorMean[2] = -vectorMean[2]

            # Create new tempCamera (by cloning the persp camera)
            camTemp = pm.duplicate("persp")
            camTemp = camTemp[0] # list to single object

            # Get current active modelling panel and switch the camera there to camTemp
            panel = pm.getPanel(withFocus=True)
            pm.lookThru(camTemp, panel)

            # Get camera vector and calculate angle between vectors - return as 3 Euler angles
            vectorCam = camTemp.viewDirection(space="world")
            camAngles = pm.angleBetween( euler=True, vector1=vectorCam, vector2=vectorMean )

            # Rotate camera, focus on the selection
            pm.xform(camTemp, relative=True, rotation=[ camAngles[0], camAngles[1], camAngles[2] ])
            pm.viewFit()
        
            # Make projection
            if pm.optionVar["mapNormalSetBox_NSUV"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapNormalSetBox_NSUV"],
                    insertBeforeDeformers=pm.optionVar["mapNormalMS2_NSUV"],
                    keepImageRatio=pm.optionVar["mapNormalMS1_NSUV"],
                    mapDirection="c",
                    type="planar",
                    uvSetName=pm.optionVar["mapNormalSet_NSUV"],
                )
            else:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapNormalSetBox_NSUV"],
                    insertBeforeDeformers=pm.optionVar["mapNormalMS2_NSUV"],
                    keepImageRatio=pm.optionVar["mapNormalMS1_NSUV"],
                    mapDirection="c",
                    type="planar",
                )
            
            # Switch back to perspective camera
            pm.lookThru("persp", panel)
            
            # Remove tempCamera
            pm.delete(camTemp)
            
        # Select original selection as UVs
        pm.select( pm.polyListComponentConversion(selOrg, toUV=True) )
        
        # Orient shell
        orientShells()

        # Do a quick unfold and orient
        unfoldUVs("selected")
        orientShells()
        pm.select(selOrg)


    ## Planar projection
    elif projection == "plane":
    
        # Eval direction var
        if planarAxis == None:
        
            if pm.optionVar["mapPlanarMS1RadGrp_NSUV"] == 1:
                planarAxis = "bestPlane"
                
            else:
                if pm.optionVar["mapPlanarMS2RadGrp_NSUV"] == 1:
                    planarAxis = "x"
                elif pm.optionVar["mapPlanarMS2RadGrp_NSUV"] == 2:
                    planarAxis = "y"
                elif pm.optionVar["mapPlanarMS2RadGrp_NSUV"] == 3:
                    planarAxis = "z"
                elif pm.optionVar["mapPlanarMS2RadGrp_NSUV"] == 4:
                    planarAxis = "c"

        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
    
            # Custom settings
            if pm.optionVar["mapPlanarMethod_NSUV"] == 1:     
            
                # Custom UV set name
                if pm.optionVar["mapPlanarSetBox_NSUV"] == True:
                    pm.polyProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapPlanarSetBox_NSUV"],
                        insertBeforeDeformers=pm.optionVar["mapPlanarMS2Box_NSUV"],
                        keepImageRatio=pm.optionVar["mapPlanarMS1Box_NSUV"],
                        mapDirection=planarAxis,
                        type="planar",
                        uvSetName=pm.optionVar["mapPlanarSet_NSUV"],
                    )
                else: # No custom UV set name
                    pm.polyProjection(
                        meshFaceGrp,
                        constructionHistory=True,
                        createNewMap=pm.optionVar["mapPlanarSetBox_NSUV"],
                        insertBeforeDeformers=pm.optionVar["mapPlanarMS2Box_NSUV"],
                        keepImageRatio=pm.optionVar["mapPlanarMS1Box_NSUV"],
                        mapDirection=planarAxis,
                        type="planar",
                    )
                    
                # Set projection node attributes
                mappingSetAttr(meshFaceGrp, "plane")

            # Quick settings
            else:               
                pm.polyProjection(
                    meshFaceGrp[0],
                    constructionHistory=True,
                    insertBeforeDeformers=True,
                    keepImageRatio=True,
                    mapDirection=planarAxis,
                    type="planar",
                )
                
        # Select original selection
        pm.select(selOrg)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapPlanarMS3Box_NSUV"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")    
        

    ## Spherical projection
    elif projection == "sphere":
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projecting - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
    
            # Custom UV set name
            if pm.optionVar["mapSphericalSetBox_NSUV"] == True:
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    createNewMap=pm.optionVar["mapSphericalSetBox_NSUV"],
                    insertBeforeDeformers=pm.optionVar["mapSphericalMS1Box_NSUV"],
                    smartFit=True,
                    type="spherical",
                    uvSetName=pm.optionVar["mapSphericalSet_NSUV"],
                )
            else: # No custom UV set name
                pm.polyProjection(
                    meshFaceGrp,
                    constructionHistory=True,
                    insertBeforeDeformers=pm.optionVar["mapSphericalMS1Box_NSUV"],
                    smartFit=True,
                    type="spherical",
                )
                
            # Set projection node attributes
            mappingSetAttr(meshFaceGrp, "sphere")

        # Select original selection
        pm.select(selOrg)
        
        # If the user wants the projection manipulators visible...
        if pm.optionVar["mapSphericalMS2Box_NSUV"] == True:
            for item in projList:
                pm.select(item, add=True)
            pm.setToolTo("ShowManips")


    ## Contour Stretch projection
    elif projection == "contour":
    
        # Create meshFace group -list
        meshFaceGrpList = mappingCreateFaceGrpList()
        
        # Start projection - one meshFaceGrp at a time
        for meshFaceGrp in meshFaceGrpList:
        
            # Quick!
            pm.polyContourProjection(
                meshFaceGrp,
                constructionHistory=True,
                insertBeforeDeformers=True,
                method=0, # Walk contours
                userDefinedCorners=False,
            )
        
        # Select original selection
        pm.select(selOrg)    
    
    else:
        print("Incorrect projection type specified for core.mapping()")
    
    # Delete window if necessary
    if win != None:
        pm.deleteUI(win)


# Match UVs
def matchUVs():

    # Check for valid UV selection
    checkSel("UV")

    # Store original selection as flattened list
    selUVs = pm.ls(selection=True, flatten=True)

    # Create Point2d objects as list
    pointList = []
    for uv in selUVs:
        coords = pm.polyEditUV(uv, query=True)
        pointList.append(Point2d2(coords[0], coords[1], uv))

    # Generate list of all possible UV pair comparisons (no duplicates)
    compareList = [x for x in itertools.combinations(pointList, 2)]
    clusterList = []

    # Generate list of point clusters
    for p in pointList:

        # See if the current point has already been added to a cluster...
        if any(p in i for i in clusterList): continue

        cluster = [] # ...else make new cluster
        cluster.append(p)
        for pair in compareList:
            if pair[0] != cluster[0]: continue # Avoids unnecessary lookups
            if pair[0].inRangeOf(pair[1], pm.optionVar["matchTol_NSUV"]): cluster.append(pair[1])
        clusterList.append(cluster)

    # Retrieve meshUV objects from the point2d objects
    uvClusterList = []
    for item in clusterList:
        uvCluster = []
        for p in item: uvCluster.append(p.id)
        uvClusterList.append(uvCluster)

    # Merge clusters into singularities
    for cluster in uvClusterList:
        pm.select(cluster) # Can we get rid of doing this before polyEvaluate?
        uvBox = pm.polyEvaluate(cluster, boundingBoxComponent2d=True)
        centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        pm.polyEditUV(
            cluster,
            relative=False,
            uValue=centerU,
            vValue=centerV,
        )

    # Reselect original selection
    pm.select(selUVs)


# Normalize shells
def normalizeShells(action=0, win=None):

    # Normalizes an individual shell
    def normalize(action):
    
        # Shorthand notation
        dir = pm.optionVar["normDirection_NSUV"]
        
        # Normalize using options from UI/optVars
        if action == 0 and (dir != 2 and dir != 3):

            # Set ratio var (cmd flag is inverted)
            if pm.optionVar["normAspect_NSUV"] == 0:
                ratio = True
            else:
                ratio = False
            
            pm.polyNormalizeUV(
                normalizeType=1,
                preserveAspectRatio=ratio, 
            )
            
        # Normalize U only
        elif action == 3 or dir == 2:
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
            scaleDist = (1 / uvBox[0][1])
            pm.polyEditUV(
                pivotU=0,
                pivotV=0,
                scaleU=scaleDist,
                scaleV=scaleDist
            )
        
        # Normalize V only
        elif action == 4 or dir == 3:
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
            scaleDist = (1 / uvBox[1][1])
            pm.polyEditUV(
                pivotU=0,
                pivotV=0,
                scaleU=scaleDist,
                scaleV=scaleDist
            )


    # Validate selection
    checkSel("any")
    
    # Store original selection
    selOrg = pm.ls(selection=True)
    
    # Create new UV set if the user wanted that
    if pm.optionVar["normSetBox_NSUV"] == True and action == 0:

        # Get active set, clone it and set it to the active set
        currentSet = pm.polyUVSet(currentUVSet=True, query=True)
        copyToName = pm.optionVar["normSet_NSUV"]
        pm.polyCopyUV(
            selOrg,
            createNewMap=True,
            constructionHistory=True,
            uvSetName=copyToName,
        )        
        pm.polyUVSet(
            currentUVSet=True,
            uvSet=copyToName
        )
        pm.select(selOrg)


    # Convert to UV or face selection
    
    # Unitize
    if action == 5 or pm.optionVar["normMethod_NSUV"] == 2:       
        pm.runtime.ConvertSelectionToFaces()
        pm.polyForceUV(unitize=True)
        pm.runtime.ConvertSelectionToUVs()
        
        # Close the normalize window
        if win != None: pm.deleteUI(win)
        return # Early exit
        
    else:
        pm.runtime.ConvertSelectionToUVs()
        
    # Convert selection to shells if we are normalizing individual shells
    if pm.optionVar["normMethod_NSUV"] == 0:
        shellList = []
        shellList.append(selOrg)
    else:
        shellList = getShells() 

        
    # Loop thru shells, snap each to bottom left corner
    for shell in shellList:
        pm.select(shell)
        snapShells(6, ignoreCheck=True)
        normalize(action)
        
    # Reselect original selection
    pm.select(selOrg)
    
    # Close the normalize window
    if win != None: pm.deleteUI(win)


# Gets the path to where the script was executed from
def openManual():
    
    # Get NSUV path
    path = inspect.stack()[0][1]
    path = path[:-20] # Remove the last 20 chars to get the path
    filename = (path+pm.optionVar["manual_NSUV"]) # Add PDF filename
    
    # Open the PDF
    if sys.platform == "win32": # Win
        filename = filename.replace("/", "\\")
        os.startfile(filename)
    elif sys.platform == "darwin": # OSX
        subprocess.call(["open", filename])


# Orient edge
def orientEdge():
    
    # Orients a shell straight based on an edge selection or two selected UVs
    def orient(sel):
    
        # Calculate arctangent (returns degrees) - round down to 4 decimals
        angleVal = round( calcArctanAngle(sel[0], sel[1]), 4)
        invertVal = 0
        
        # Determine how much to rotate. Arctangent range is -90 to +90 degrees
        if angleVal == 0.0000 or angleVal == 90.0000 or angleVal == -90.0000:
            # Type 0 - No rotation
            angleVal = 0
        
        elif angleVal >= -44.9999 and angleVal <= 44.9999:
            # Type A - Invert
            invertVal = 1
            
        elif angleVal >= 45.0001 and angleVal <= 89.9999:
            # Type B - Subtract angle from 90
            angleVal = 90 - angleVal
            invertVal = 0
            
        elif angleVal <= -45.0001 and angleVal >= -89.9999:
            # Type C - Add 45 degrees to angle and invert
            angleVal = 90 + angleVal
            invertVal = 1
            
        else:
            # Type D - Angle is 45 degrees
            angleVal = 45
            invertVal = 0
            
        if invertVal == 1:
            angleVal = -angleVal
            
        # Convert to uv shell
        pm.polySelectConstraint(
            mode=2,
            shell=True,
        )
        pm.polySelectConstraint(
            border=0,
            mode=0,
            shell=False,
        )
        
        # Calculate bounding box pivot (center point) then rotate
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )    
        pm.polyEditUV(
            angle=angleVal,
            pivotU=centerU,
            pivotV=centerV,
        )


    # Validate selection
    checkSel("edgeUV")
    
    # Store selection
    selOrg = pm.ls(selection=True)
    pm.mel.ConvertSelectionToUVs()
    selUVs = pm.ls(selection=True, flatten=True)
    
    # Single UV selection?
    if len(selUVs) == 1:
        errorCode(13)
  
    # Get shells from selection
    shellList = getShells()

    # Create progress window
    createProgWin("Orienting...", len(shellList))
 
    shellsTotal = shellsRemain = len(shellList) # Shell count

    # Loop through each shell
    counter = 0
    while len(shellList) > counter:
    
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True, 
            progress=(shellsTotal - shellsRemain),
            status="Processing shells. %s Shells remaining."%shellsRemain
        )

        # Loop through shell UVs
        shellComps = []
        for uv in selUVs:

            # Create shell components -list
            if uv in shellList[counter]:
                shellComps.append(uv)

                # As we only need two UVs...
                if len(shellComps) <= 2:
                    continue # Move on to next, eventually breaking out

        # Select shell, run orientation method and mod the counters
        pm.select(shellComps)
        orient(shellComps)
        counter += 1
        shellsRemain -= 1

    # Close the progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg)

    # Go to edge selection tool if the original selection was an edge
    if pm.filterExpand(selectionMask=32) != [] and pm.filterExpand(selectionMask=32) != None:
        pm.mel.SelectEdgeMask()


# Orient shells
def orientShells(shellList=None):

    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.setToolTo("selectSuperContext")

    # Validate selection
    checkSel("UV")

    # Store original selection
    selOrg = pm.ls(selection=True)

    # Get shells from selection if we have no incomming shells
    if shellList == None:
        shellList = getShells()

    # Create progress window
    createProgWin("Orienting...", len(shellList))
    shellsTotal = shellsRemain = len(shellList) # Shell count

    # Loop through each shell and orient it
    counter = 0
    while len(shellList) > counter:

        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user")
            break

        # Edit the progress window
        pm.progressWindow(
            edit=True, 
            progress=(shellsTotal - shellsRemain),
            status="Processing shells. %s Shells remaining."%shellsRemain
        )

        # Get current shell and create a Polygon2d -object of the convex hull around the selection
        hull = createConvexHull(shellList[counter])
        center = hull.getBounds(1)

        # Calculate rotation for the hull to get it's MAR - apply rotation to shell
        orientation = hull.getRotation()
        pm.polyEditUV(
            shellList[counter],
            angle=orientation,
            pivotU=center[0],
            pivotV=center[1]
        )

        # Mod the counters and move on...
        counter += 1
        shellsRemain -= 1

    # Close the progress window
    pm.progressWindow(endProgress=True)

    # Reselect original selection
    pm.select(selOrg, replace=True)


# Pins, unpins, clears or inverts UV's - 2016+ only
if mayaVer >= 201600:
    def pinUVs(mode):

        if mode == 0 or mode == 1: # Pin or Unpin
            if pm.selectMode(query=True, component=True) == True:
                pm.runtime.ConvertSelectionToUVs()
                pm.polyPinUV(
                    operation=mode,
                    value=pm.optionVar["polyPinUVVal_NSUV"]
                    )

        elif mode == 2 or mode == 3: # Clear
            if pm.selectMode(query=True, component=True) == True:
                pm.polyPinUV(operation=mode)
        else:
            print("Incorrect argument sent to NSUV.core.pinUVs()")


# Cycles the manipulator around the corners of the selection bounding box or UV range bounds
def pivotCycle(cycleType, dir):

    # Original selection
    selOrg = pm.ls(selection=True)

    # Check for component selection
    checkSel("comps")

    # Get mesh name from component
    mesh = selOrg[0]
    mesh = re.findall("([^.]+)[.]", str(mesh) )[0]

    # Get current tool
    cTool = pm.currentCtx()

    if cTool == "moveSuperContext":
        posCurrent = pm.texMoveContext( "texMoveContext", query=True, position=True ) 

    elif cTool == "RotateSuperContext":
        posCurrent = pm.texRotateContext( "texRotateContext", query=True, position=True ) 

    elif cTool == "scaleSuperContext":
        posCurrent = pm.texScaleContext( "texScaleContext", query=True, position=True )

    elif cTool == "ModelingToolkitSuperCtx":
        posCurrent = pm.texWinToolCtx( "ModelingToolkitSuperCtx", query=True, position=True )

    # Cycle UV range bounds
    if cycleType == 0:
        if dir == 0: # Bottom left
            pm.setAttr(mesh+".uvPivot", 0.0, 0.0)
        elif dir == 1: # Top right
            pm.setAttr(mesh+".uvPivot", 1.0, 1.0)
        elif dir == 2: # Top left
            pm.setAttr(mesh+".uvPivot", 0.0, 1.0)
        elif dir == 3: # Bottom right
            pm.setAttr(mesh+".uvPivot", 1.0, 0.0)

    # Cycle bounding box bounds
    else:
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)

        if dir == 0: # Bottom left
            pm.setAttr(mesh+".uvPivot", uvBox[0][0], uvBox[1][0])
        elif dir == 1: # Top right          
            pm.setAttr(mesh+".uvPivot", uvBox[0][1], uvBox[1][1])
        elif dir == 2: # Top left
            pm.setAttr(mesh+".uvPivot", uvBox[0][0], uvBox[1][1])
        elif dir == 3: # Bottom right
            pm.setAttr(mesh+".uvPivot", uvBox[0][1], uvBox[1][0])


# Rounds a value to the power of two
def powerOfTwo(val):
    
    nextSize = 1
    newSize, prevSize = (0,)*2
    
    while nextSize < val:
        prevSize = nextSize
        nextSize = nextSize * 2
    
    if (val - prevSize) < (nextSize - val):
        newSize = prevSize
    else:
        newSize = nextSize
        
    return newSize


# Propagate UV set
def propagateSets(scrollList):

    # Selection check
    checkSel("mesh")

    # Get all shapes in the selection
    shapes = getShapes()

    # Can't propagate with a single mesh only
    if len(shapes) < 2:
        errorCode(12)

    # Get active UV set
    setName = pm.polyUVSet(
        shapes[0],
        currentUVSet=True,
        query=True,
    )

    # Go through each set/object and propagate accordingly
    for mesh in shapes:
        baseSetName = str(setName[0])
        perInstance = False
        setExists = False

        # If the name ends with the suffix (*) where * is a digit between 0-99...
        if re.match("^[a-z]+?\([0-9]{1,2}\)$", baseSetName, re.IGNORECASE):

            # ...remove said suffix from the baseSetName, set bool
            baseSetName = re.findall("([^.]+)[(]", baseSetName, re.IGNORECASE )[0]
            perInstance = True

        # Get all sets from mesh object and check for a match
        uvSets = pm.polyUVSet(
            mesh,
            allUVSets=True,
            perInstance=True,
            query=True,
        )
        if baseSetName in uvSets:
            setExists = True

        # If we have a per-instance case
        if perInstance == True:

            # Set exists...
            if setExists == True:

                # ..but does it exist on this instance?
                perInstanceExists = pm.polyUVSet(
                    mesh,
                    perInstance=True,
                    query=True,
                    uvSet=baseSetName,
                )

                if perInstanceExists == None or perInstanceExists == []:
                    meshParent = pm.listRelatives(
                        mesh,
                        parent=True,
                        path=True,
                    )
                    newSet = pm.polyUVSet(
                        mesh,
                        create=True,
                        perInstance=True,
                        uvSet=baseSetName,                
                    )
                    pm.polyUVSet(
                        meshParent[0],
                        currentUVSet=True,
                        uvSet=newSet[0],
                    )
            
            # Set doesn't exist at all   
            else: 
                pm.polyUVSet(
                    mesh, 
                    create=True,
                    perInstance=True,
                    uvSet=baseSetName
                )
                pm.polyUVSet(
                    mesh,
                    currentUVSet=True,
                    uvSet=baseSetName,
                ) 
 
        # Set does not exist and is not per-instance
        elif (setExists == False): 

            pm.polyUVSet(
                mesh,
                create=True,
                uvSet=baseSetName,            
            )
            pm.polyUVSet(
                mesh,
                currentUVSet=True,
                uvSet=baseSetName,            
            )        

        else: # Set exists already, do nothing!
            pass

    # Update the editor
    updateUVSetEditor(scrollList)


# Method for randomizing a single shell
def randomize(shell):
    
    # optVars to short notation vars
    boxTU = pm.optionVar["randTBox1_NSUV"]
    boxTV = pm.optionVar["randTBox2_NSUV"]
    boxRCW = pm.optionVar["randRBox1_NSUV"]
    boxRCCW = pm.optionVar["randRBox2_NSUV"]
    boxSU = pm.optionVar["randSBox1_NSUV"]
    boxSD = pm.optionVar["randSBox2_NSUV"]
    
    # Translation
    if boxTU == 1 or boxTV == 1:
        valT = pm.optionVar["randT_NSUV"]
        
        # Along U
        if boxTU == 1:
            translateVal = random.uniform(-valT, valT)
            pm.polyEditUV(uValue=translateVal)
        
        # Along V
        if boxTV == 1:
            translateVal = random.uniform(-valT, valT)
            pm.polyEditUV(vValue=translateVal)

        
    # Rotation
    if boxRCW == 1 or boxRCCW == 1:
        valR = pm.optionVar["randR_NSUV"]
    
        # Both directions
        if boxRCW and boxRCCW:
            rotateVal = random.uniform(-valR, valR)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )
    
        # Clockwise
        elif boxRCW == 1:
            rotateVal = random.uniform(0, valR)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )
        
        # Counter-clockwise
        elif boxRCCW == 1:
            rotateVal = random.uniform(-valR, 0)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], angle=rotateVal )

    
    # Scaling
    if boxSU == 1 or boxSD == 1:
    
        valS = float(pm.optionVar["randS_NSUV"])
        
        # Both up and down
        if boxSU == 1 and boxSD == 1:

            # Convert percentage to decimal number
            tempUp = valS/100 + 1
            tempDown = 1 - valS/100            
            scaleVal = random.uniform(tempDown, tempUp)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )
        
        # Up
        elif boxSU == 1:

            # Convert percentage to decimal number
            tempUp = (valS/100) + 1            
            scaleVal = random.uniform(1.0, tempUp)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )
            
        # Down
        elif boxSD == 1:

            # Convert percentage to decimal number
            tempDown = 1 - (valS/100)            
            scaleVal = random.uniform(tempDown, 1.0)
            updateManipCoords()
            manipCoords = pm.optionVar["manipCoords_NSUV"]
            pm.polyEditUV( pivotU=manipCoords[0], pivotV=manipCoords[1], scaleU=scaleVal, scaleV=scaleVal )


# Randomize UVs
def randomizeShells():

    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.setToolTo("selectSuperContext")
    
    # Check the selection
    checkSel("UV")
    
    # Get the selection
    selOrg = pm.ls(selection=True)
    
    # Convert the selection to individual shells; store in a list
    shellList = getShells()
    
    # Count shells
    countShells = len(shellList)
    
    # Create progress window
    createProgWin("Randomizing...", countShells)
    
    progCount = 0
    
    # Randomization loop
    for shell in shellList:
    
        progCount += 1
        
        # Break if cancelled by user
        if pm.progressWindow(query=True, isCancelled=True) == True:
            pm.warning("Interupted by user\n")
            break
        
        # Edit the progress window
        pm.progressWindow(
            edit=True,
            progress=(progCount),
            status=("Randomizing shell %s / %s")%(progCount, countShells)
        )
        
        # Select shell and run randomize
        pm.select(shellList[progCount-1], replace=True)
        pm.setToolTo("moveSuperContext")
        randomize(shell)
        
    # End progress window and reselect original selection
    pm.progressWindow(endProgress=True)
    pm.select(selOrg, replace=True)


# Relax UVs
def relaxUVs(win=None):

    # Vars
    methodVar = 1
    pinVar = False
    pinUnselVar = False
    selOrg = None

    # Manage optVars
    if pm.optionVar["relaxEdge_NSUV"] == 1:
        relaxType = "uniform"
    else:
        relaxType = "harmonic"

    if pm.optionVar["relaxPin_NSUV"]:
        if pm.optionVar["relaxPinType_NSUV"] == 1:
            pinVar = True
            pinUnselVar = False
        else:
            pinVar = False
            pinUnselVar = True

    # Check for Unfold3D plugin and set correct value for methodVar
    if pm.pluginInfo("Unfold3D", loaded=True, query=True):
        methodVar = pm.optionVar["relaxMethod_NSUV"]
    else:
        if pm.optionVar["relaxMethod_NSUV"] == 1:
            methodVar = 2
        elif pm.optionVar["relaxMethod_NSUV"] == 2:
            methodVar = 3

    # Validate selection
    checkSel("UV")

    # Store selection
    selOrg = pm.ls(selection=True)
    selObjs = pm.ls(selection=True, objectsOnly=True)


    ## Unfold3D optimize

    # Method: Unfold3D
    if methodVar == 1:
        if mayaVer >= 201650: # New command
            pm.u3dOptimize(
                selOrg,
                borderintersection=pm.optionVar["relaxBorder_NSUV"],
                iterations=pm.optionVar["relaxItr_NSUV"],
                mapsize=pm.optionVar["relaxSize_NSUV"],
                power=pm.optionVar["relaxPower_NSUV"],
                roomspace=pm.optionVar["relaxSpacing_NSUV"],
                surfangle=pm.optionVar["relaxAngle_NSUV"],
                triangleflip=pm.optionVar["relaxFlips_NSUV"],
            )
        else:
            pm.Unfold3D( # Old command
                selOrg,
                borderintersection=pm.optionVar["relaxBorder_NSUV"],
                iterations=pm.optionVar["relaxItr_NSUV"],
                mapsize=pm.optionVar["relaxSize_NSUV"],
                optimize=True,
                power=pm.optionVar["relaxPower_NSUV"],
                roomspace=pm.optionVar["relaxSpacing_NSUV"],
                surfangle=pm.optionVar["relaxAngle_NSUV"],
                triangleflip=pm.optionVar["relaxFlips_NSUV"],
            )

        # Close relax window
        if win != None:
            pm.deleteUI(win)


    ## Legacy optimize

    if methodVar == 2: # Legacy optimize (relax)
        pm.untangleUV(
            relax=relaxType,
            pinBorder=pm.optionVar["relaxPinBorder_NSUV"],
            pinSelected=pinVar,
            pinUnselected=pinUnselVar,
            relaxTolerance=0,
            maxRelaxIterations=pm.optionVar["relaxMaxItr_NSUV"], 
        )

    elif methodVar == 3: # Legacy optimize (relax) - Quick
        pm.untangleUV(
            relax=relaxType,
            pinBorder=False,
            pinSelected=False,
            pinUnselected=True,
            relaxTolerance=0.0,
            maxRelaxIterations=5,
        )

    # Reselect original selection
    pm.select(selOrg)

    # Close relax window
    if win != None:
        pm.deleteUI(win)


# Rename UV set
def renameSet(scrollList, renameField, renameUI):

    # Perform selection check
    checkSel("mesh1")
    
    # Get UV Set names
    nameNew = renameField.getText()
    nameOld = scrollList.getSelectItem()[0]
    
    # Check for identical names
    if nameNew == nameOld:
        errorCode(24)
        
    # Check if UV name starts with a letter
    if nameNew == "": errorCode(25)
    elif nameNew == False or nameNew[0].isalpha() == False:
        errorCode(25)
    
    # Rename UV Set and set it to the current set
    pm.polyUVSet(
        newUVSet=nameNew,
        rename=True,
        uvSet=str(nameOld),
    )
    pm.polyUVSet(
        currentUVSet=True,
        uvSet=nameNew
    )
    
    # Update UV Set list
    updateUVSetEditor(scrollList)
    
    # Select the correct set
    scrollList.setSelectItem(nameNew)
    
    # Close down the rename UV Set window. Eval at runtime.
    pm.evalDeferred(lambda: pm.deleteUI(renameUI))


# Rotates a UV selectio
def rotateUVs(dir, local=False):
    
    manipAmt = pm.optionVar["manipAmt_NSUV"]
    
    # Global rotate
    if local == False:
    
        # Update coords
        updateManipCoords()
        manipCoords = pm.optionVar["manipCoords_NSUV"]
    
        if dir == "90":
            pm.polyEditUV(
                angle=90,
                pivotU=manipCoords[0],
                pivotV=manipCoords[1]
            )        
        elif dir == "-90":
            pm.polyEditUV(
                angle = -90,
                pivotU=manipCoords[0],
                pivotV=manipCoords[1]
            )    
        elif dir == "180":
            pm.polyEditUV(
                angle=180,
                pivotU=manipCoords[0],
                pivotV=manipCoords[1]
            )
        elif dir == "CW":
            pm.polyEditUV(
                angle=(manipAmt * -1),
                pivotU=manipCoords[0],
                pivotV=manipCoords[1]
            )        
        elif dir == "CCW":
            pm.polyEditUV(
                angle=manipAmt,
                pivotU=manipCoords[0],
                pivotV=manipCoords[1]
            )

    # Local rotate
    else:
    
        # Save original selection and create shell list
        selOrg = pm.ls(selection=True)
        shellList = getShells()
    
        # Create progress window
        createProgWin("Rotating...", len(shellList))
        
        shellsTotal = shellsRemain = len(shellList) # Shell count
        
        # Start rotating
        counter = 0
        while counter < len(shellList):
        
            # Break if cancelled by user
            if pm.progressWindow(query=True, isCancelled=True) == True:
                pm.warning("Interupted by user")
                break
                
            # Edit the progress window
            pm.progressWindow(
                edit=True, 
                progress=(shellsTotal - shellsRemain),
                status="Processing shells. %s shells remaining."%shellsRemain        
            )
            
            # Calculate pivot then rotate current shell
            pm.select(shellList[counter])
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
            centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
            centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
            
            if dir == "90":
                pm.polyEditUV(
                    angle=90,
                    pivotU=centerU,
                    pivotV=centerV
                )        
            elif dir == "-90":
                pm.polyEditUV(
                    angle = -90,
                    pivotU=centerU,
                    pivotV=centerV
                )    
            elif dir == "180":
                pm.polyEditUV(
                    angle=180,
                    pivotU=centerU,
                    pivotV=centerV
                )
            elif dir == "CW":
                pm.polyEditUV(
                    angle=(manipAmt * -1),
                    pivotU=centerU,
                    pivotV=centerV
                )        
            elif dir == "CCW":
                pm.polyEditUV(
                    angle=manipAmt,
                    pivotU=centerU,
                    pivotV=centerV
                )
                
            # Modify counters
            shellsRemain -= 1            
            counter += 1
            
        # Close the progress window
        pm.progressWindow(endProgress=True)
        
        # Reselect original selection
        pm.select(selOrg)


# Scales a UV selection
def scaleUVs(scaleType, local=False):

    manipAmt = pm.optionVar["manipAmt_NSUV"]

    # Global scale
    if local == False:
    
        # Update coords
        updateManipCoords()
        manipCoords = pm.optionVar["manipCoords_NSUV"]
        
        # Scale
        if scaleType == "U":   
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleU=manipAmt
            )        
        if scaleType == "V":
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleV=manipAmt
            )        
        if scaleType == "UV":
            pm.polyEditUV(
            pivotU=manipCoords[0],
            pivotV=manipCoords[1],
            scaleU=manipAmt,
            scaleV=manipAmt
            )
    
    # Local (relative) scale
    else: 
       
        # Save original selection and create shell list
        selOrg = pm.ls(selection=True)
        shellList = getShells()
        
        # Create progress bar
        createProgWin("Scaling...", len(shellList))
        
        shellsTotal = shellsRemain = len(shellList) # Shell count
        
        # Start scaling
        counter = 0
        while counter < len(shellList):

            # Break if cancelled by user
            if pm.progressWindow(query=True, isCancelled=True) == True:
                pm.warning("Interupted by user")
                break
                
            # Edit the progress window
            pm.progressWindow(
                edit=True, 
                progress=(shellsTotal - shellsRemain),
                status="Processing shells. %s shells remaining."%shellsRemain        
            )
        
            # Calculate pivot then scale current shell
            pm.select(shellList[counter])
            uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
            centerU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
            centerV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
            
            if scaleType == "U":
                pm.polyEditUV(
                pivotU=centerU,
                pivotV=centerV,
                scaleU=manipAmt
                ) 
            
            elif scaleType == "V":
                pm.polyEditUV(
                pivotU=centerU,
                pivotV=centerV,
                scaleV=manipAmt
                ) 
            
            else: # scaleType == "UV"
                pm.polyEditUV(
                pivotU=centerU,
                pivotV=centerV,
                scaleU=manipAmt,
                scaleV=manipAmt
                )

            # Modify counters
            shellsRemain -= 1
            counter += 1
        
        # Close the progress window
        pm.progressWindow(endProgress=True)
        
        # Reselect original selection
        pm.select(selOrg)

        
# Converts selection modes
def selectTypeChange(toType, txtEditor=None):

    # Changes selection mode to components
    pm.mel.changeSelectMode("-component")
    
    if toType == 1: # Face
        pm.selectType(facet=True) # Because selectType is a bugged command
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(objectComponent=True, facet=True)

    elif toType == 2: # Edge
        pm.selectType(edge=True)
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(objectComponent=True, edge=True)

    elif toType == 3: # Vertex
        pm.selectType(vertex=True, latticePoint=True)
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(objectComponent=True, vertex=True)

    elif toType == 4: # UV
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(allComponents=False)
        pm.selectType(polymeshUV=True)

    elif toType == 5: # Shell
        pm.mel.changeSelectMode("-component") # Repeated because of some bug
        pm.selectType(facet=True)
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(meshUVShell=True)

    elif toType == 6: # Mesh
        pm.mel.changeSelectMode("-object")
        pm.selectType(meshComponents=False)
        pm.selectType(objectComponent=True, allComponents=False)
        pm.selectType(polymesh=True)


# Converts a selection
def selectConvert(toType, txtEditor=None):

    # Vars
    converted = []
    
    # # To contained or connected faces
    if toType == 5 or toType == 6:

        # Update the UV editor, selection and selection type
        selOrg = pm.ls(selection=True, flatten=True)
        if toType == 5: # To contained faces
            pm.textureWindow(txtEditor, edit=True, selectInternalFaces=True)
        else: # To connected faces
            pm.textureWindow(txtEditor, edit=True, selectRelatedFaces=True)
        pm.select(selOrg, deselect=True)
        newSel = pm.ls(selection=True, flatten=True)
        pm.selectType(facet=True)
        pm.select(newSel)
        return

    # To Face
    elif toType == 1:
        converted = pm.polyListComponentConversion(internal=True, 
                    fromEdge=True, fromUV=True, fromVertex=True, fromVertexFace=True, 
                    toFace=True,
                    )
        selectTypeChange(1)

    # To Edge
    elif toType == 2:
        converted = pm.polyListComponentConversion(
                    fromFace=True, fromUV=True, fromVertex=True, fromVertexFace=True, 
                    toEdge=True,
                    )
        selectTypeChange(2)

    # To Vertex
    elif toType == 3:
        converted = pm.polyListComponentConversion(
                    fromEdge=True,fromFace=True, fromUV=True, fromVertexFace=True, 
                    toVertex=True,
                    )
        selectTypeChange(3)
 
    # To UV
    elif toType == 4:
        converted = pm.polyListComponentConversion(
                    fromEdge=True, fromFace=True, fromVertex=True, fromVertexFace=True,
                    toUV=True,
                    )
        selectTypeChange(4)

    pm.select(converted)


# Select last used Unfold3d -brush
def selectLastUVBrush():

    # Get current tool
    cTool = pm.currentCtx()

    # Only run if we have context active
    if pm.contextInfo(cTool, exists=True):
        brushMode = None

        # Get current context class and query the brush mode
        ctx = pm.contextInfo(cTool, c=True)
        if ctx == "texSculptCacheContext":
            brushMode = pm.texSculptCacheContext(cTool, query=True, mode=True)

        elif ctx == "texCutContext":
            brushMode = pm.texCutContext(cTool, query=True, mode=True)

        elif ctx == "Unfold3DBrush":
            brushMode = pm.cmds.Unfold3DContext(cTool, query=True, unfold=True)
            temp = int(brushMode) # Unfold or Optimize?
            if temp: brushMode="Unfold"
            else: brushMode="Optimize"

        elif ctx == "SymmetrizeUVBrush":
            brushMode = "Symmetrize"

        # Overwrite optVar for last brush mode with the current mode
        if pm.optionVar["uvBrushMode_NSUV"] != brushMode:
            pm.optionVar["uvBrushLastMode_NSUV"] = pm.optionVar["uvBrushMode_NSUV"]
            pm.optionVar["uvBrushMode_NSUV"] = brushMode


# Select unmapped faces
def selectUnmapped():

    # Store original selection
    selOrg = pm.ls(selection=True, flatten=True)

    # Validate selection
    if selOrg == [] or selOrg == None:
        errorCode(9)

    # Select unmapped face
    else:
        pm.polySelectConstraint( mode=3, type=0x0008, textured=2 )
        unmappedSel = pm.ls(selection=True)

        # Restore selection constraint
        pm.polySelectConstraint(disable=True)

        # Select mesh or the unmapped face
        if unmappedSel == [] or unmappedSel == None: 
            pm.select(selOrg)
            errorCode(21)
        else:
            pm.select(unmappedSel)


# Loads and Stores a selection into an option variable
def selectionVar(mode, var):
    
    # Load
    if mode == "load":
    
        # Early exits if trying to load empty list
        if pm.optionVar["storedSelA_NSUV"] == [] and var == "A": return
        if pm.optionVar["storedSelB_NSUV"] == [] and var == "B": return
    
        # Get string list from optVar
        if var == "A": 
            strList = pm.optionVar["storedSelA_NSUV"]
        elif var == "B":
            if pm.optionVar["storedSelB_NSUV"] == []: return
            strList = pm.optionVar["storedSelB_NSUV"]
            
        # Create nodes from string list
        objList = []
        for item in strList:
            if item != None and item != "":
                
                # In case the mesh or component don't exist
                try: 
                    objList.append(pm.PyNode(item))
                except pm.MayaNodeError:
                    errorCode(26)
                except pm.MayaAttributeError:
                    errorCode(27)

        # Switch selection type to what was in the selection previously
        if pm.filterExpand(objList[0], selectionMask=34) != None: selectTypeChange(1) # Face
        elif pm.filterExpand(objList[0], selectionMask=32) != None: selectTypeChange(2) # Edge
        elif pm.filterExpand(objList[0], selectionMask=31) != None: selectTypeChange(3) # Vertex
        elif pm.filterExpand(objList[0], selectionMask=35) != None: selectTypeChange(4) # UV
        elif pm.filterExpand(objList[0], selectionMask=12) != None: selectTypeChange(6) # Mesh

        pm.select(objList, replace=True)


    elif mode == "save":

        # Get selection
        sel = pm.ls(sl=1, fl=1)
        strList = []
        objList = []

        # Convert MeshUV list to str list
        for item in sel: 
            strList.append(str(item))
        
        if len(strList) == 1: strList.append("") ## Because single-element lists causes error on load

        # Store in optVar
        if var == "A":
            pm.optionVar["storedSelA_NSUV"] = strList
        elif var == "B":
            pm.optionVar["storedSelB_NSUV"] = strList


# Set the selected UV set to the current
def setCurrentSet(scrollList=None, uvSetName=None):

    # Special case for the menuItems on the UV set menu
    if scrollList == None:
        scrollList = pm.ui.PyUI("uvSetScrollList_NSUV")
        scrollList.setSelectItem(uvSetName)

    # Save original selection
    selOrg = pm.ls(selection=True, flatten=True)

    # Get UV sets from scrollList and change currentUVSet, then reselect
    setCurrentSet = scrollList.getSelectItem()
    pm.polyUVSet(
        currentUVSet=True,
        uvSet=str(setCurrentSet[0])
    )
    time.sleep(0.25) # Else setCurrentSet() overrides the doubleClickCommand on the scrollList
    pm.select(selOrg)


# Method for setting working units via the setWorkingUnits -UI
def setUnits(menu, deleteWin):
    newUnit = menu.getValue() # Read value
    pm.currentUnit(linear=newUnit) # Set working units

    # Reload grid
    currentGridSpacing = pm.grid(query=True, spacing=True)
    currentGridSize = pm.grid(query=True, size=True)
    if currentGridSize < 1.0:
        currentGridSize = 1.0
    pm.grid(spacing=currentGridSpacing, size=currentGridSize)
    
    pm.deleteUI(deleteWin)


# Set texel density
def setTD(field1, field2):
    
    # Check selection
    checkSel("any")
    
    # Store selection
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Convert to UVs then to list of individual shells
    selUVs = pm.polyListComponentConversion(toUV=True)
    pm.select(selUVs)
    shellList = getShells()
    
    # Read TD and map size values from fields
    tdVal = pm.optionVar["td_NSUV"] = field1.getValue1()
    mapVal = pm.optionVar["tdSize_NSUV"] = field2.getValue1()
    
    # Calculate scalar
    scalar = tdVal / mapVal
  
    # Run unfold on every shell
    for shell in shellList:
        pm.unfold(
            shell,
            globalBlend=0, 
            globalMethodBlend=1, 
            iterations=0, 
            optimizeAxis=0, 
            pinSelected=0, 
            pinUvBorder=0, 
            scale=scalar,
            stoppingThreshold=0.001, 
            useScale=True,
        )
        
    # Re-center the manipulator and reselect the original selection
    pm.setToolTo("moveSuperContext")
    pm.select(selOrg)
    

# Smart stack
def smartStack():

    # Validate UV selection
    checkSel("UV")

    # Store selection
    selOrg = pm.ls(selection=True, flatten=True)

    # Create shells
    shellList = getShells()
    
    pm.select(selOrg)
    
    # Stack
    stackShells(shellList)
    
    # Orient
    orientShells(shellList)    


# Snap point A to point B
def snapPoints(snapSel):
    
    # Validate selection (only two UVs)
    checkSel("UV2")
    
    # Store original selection as flattened list
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Get U and V distances
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
    distU = abs(uvBox[0][1] - uvBox[0][0])
    distV = abs(uvBox[1][1] - uvBox[1][0])

    # Store coordinate info
    pointA = pm.polyEditUV(selOrg[0], query=True)
    pointB = pm.polyEditUV(selOrg[1], query=True)

    # Snap A to B
    if snapSel == 0:

        # Shell position correction
        if pointA[1] > pointB[1]:
            distV = -distV
        if pointA[0] > pointB[0]:
            distU = -distU

        # Select UV from first shell
        pm.select(selOrg[0])

    # Snap B to A 
    elif snapSel == 1:

        # Shell position correction
        if pointA[0] < pointB[0]:
            distU = -distU
        if pointA[1] < pointB[1]:
            distV = -distV

        # Select UV from second shell
        pm.select(selOrg[1])

    else: # Error
        print("Error: Invalid snapSel -arg passed to snapPointS() - expected 0 or 1")

    # Expand selection to entire shell, then move the shell
    pm.runtime.SelectUVShell()
    pm.polyEditUV(
        uValue=distU,
        vValue=distV
    )


# Snap shells
def snapShells(dir, ignoreCheck=False):

    # Validate UV selection
    if ignoreCheck == False:
        checkSel("UV")

    # Get bounding box
    uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)

    # Calc distances
    distCenterU = 0.5 - (uvBox[0][0] + uvBox[0][1]) * 0.5
    distCenterV = 0.5 - (uvBox[1][0] + uvBox[1][1]) * 0.5
    distRight = 1 - uvBox[0][1]
    distLeft = -uvBox[0][0]
    distBottom = -uvBox[1][0]
    distTop = 1 - uvBox[1][1]

    # Center
    if dir == 0:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distCenterV
        )

    # Top left
    elif dir == 1:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distTop
        )

    # Top
    elif dir == 2:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distTop
        )

    # Top right
    elif dir == 3:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distTop
        )
    
    # Left
    elif dir == 4:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distCenterV
        )
    
    # Right
    elif dir == 5:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distCenterV
        )
    
    # Bottom left
    elif dir == 6:
        pm.polyEditUV(
            uValue=distLeft,
            vValue=distBottom
        )
    
    # Bottom
    elif dir == 7:
        pm.polyEditUV(
            uValue=distCenterU,
            vValue=distBottom
        )
    
    # Bottom right
    elif dir == 8:
        pm.polyEditUV(
            uValue=distRight,
            vValue=distBottom
        )
        
    # Activate the move tool
    pm.setToolTo("moveSuperContext")
    

# Sorts the shell list by size
def sortShells(list, mode):

    # Get bounding box info of each shell
    tempList = []
    for shell in list:
        pm.select(shell)
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        
        # Calc bounding box
        if mode == 0: size = abs(uvBox[0][1] - uvBox[0][0]) # U
        elif mode == 1: size = abs(uvBox[1][0] - uvBox[1][1]) # V
        tempList.append((size, shell)) 
        
    # Sort list based on first element in tuples
    sortedList = sorted(tempList, key=operator.itemgetter(0))

    # Convert list of tuples to list of uv shells. Exclude the size-part of the tuples.
    finalList = []
    for t in sortedList:
        finalList.append(t[1])
        
    # Reverse and return
    finalList = finalList[::-1]
    return finalList


# Splits a multi-mesh UV-selection into one list of UV's per object
def splitUVsPerMesh(uvList, meshList):

    objUVs = []
    for mesh in meshList:
        meshUVs = []
        for uvRange in uvList:
            if str(uvRange).startswith(str(mesh)):
                meshUVs.append(uvRange)

        objUVs.append(meshUVs)

    return objUVs


# Spread out shells
def spreadOutShells():
    
    # Validate selection
    checkSel("any")
    
    # Save original selection
    selOrg = pm.ls(selection=True)
    
    # Go to mesh selection mode
    pm.mel.toggleSelMode()
    pm.selectMode(object=True)
    
    # Spread out for every shell...
    meshList = pm.filterExpand(selectionMask=12) # Convert selection to mesh    
    for item in meshList:

        # Select mesh, convert selection to UVs
        pm.select(item)
        selOrgUV = pm.polyListComponentConversion(toUV=True)
        pm.select(selOrgUV)
        
        # Calculate center point from UV bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        oldCenterU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        oldCenterV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        
        # Layout/(order) UV shells
        pm.polyLayoutUV(
            flipReversed=True,
            layout=2,
            layoutMethod=1,
            percentageSpace=0.2,
            rotateForBestFit=True,
            scale=0,
            separate=False,
        )
        
        # Calculate new center point from UV bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        newCenterU = 0.5 * ( uvBox[0][0] + uvBox[0][1] )
        newCenterV = 0.5 * ( uvBox[1][0] + uvBox[1][1] )
        
        # Get proper translation distance, then move back the shell package
        distU = oldCenterU - newCenterU
        distV = oldCenterV - newCenterV
        
        if oldCenterU <= newCenterU:        
            pm.polyEditUV(
                uValue=distU,
                vValue=distV
            )

        else:
            pm.polyEditUV(
                uValue=distU,
                vValue=distV
            )
        
    # Select the original selection
    pm.select(selOrg)


# UV Snapshot: Take snapshot
def ssTakeShot(win=None, multiTile=False):

    # Method vars
    imfExt = ".iff"
    imfKey = "iff"
    
    # Check for valid mesh selection
    checkSel("mesh")
  
    # Get file format from control, insert into optVar
    format = pm.optionVar["shotUVformat_NSUV"]
    
    # Get ff names (keyword and extensions) if OS is macintosh
    if pm.about(macOS=True):
        extList = ["iff", "jpg", "pntg", "ps", "png", "pict", "qtif", "sgi", "tga", "tif", "bmp"]
        imfKey = extList[format-1]
        imfExt = "." + extList[format-1]
        
    else: # Else get for Windows
        if format != "Maya IFF":
            imfKey = pm.imfPlugins(format, query=True, keyword=True)
            imfExt = pm.imfPlugins(format, query=True, extension=True)
    
    # Read optVars, store in convenient vars
    rgb = pm.optionVar["shotUVcolor_NSUV"]
    sizeX = pm.optionVar["shotUVxSize_NSUV"]
    sizeY = pm.optionVar["shotUVySize_NSUV"]
    
    # Check if file path is blank - execution is halted
    path = pm.optionVar["shotUVpath_NSUV"]
    if path == "":
        errorCode(10)

    # Fix extension
    path = re.split("([.])\w+$", path)[0] + imfExt

    # Check if file already exists
    if multiTile == False:
        if os.path.isfile(path) == True:

            # Warn the user about it
            result = pm.confirmDialog(
                button=["Yes", "Cancel"],
                cancelButton="Cancel",
                defaultButton="Cancel",
                dismissString="Cancel",
                message="File exists. Overwrite?",
                title="Warning!",
            )

    # Double all the backslashes in case we have an NT-like path
    path = path.replace("\\", "\\\\")
    
    # Custom range: Read radioButton from radioCollection and set optVar
    if pm.optionVar["shotUVrange_NSUV"] == 2:
    
        # Do the xform
        rangeType = pm.optionVar["shotUVtype_NSUV"]
        
        if rangeType == 1:
            ssXform(0)
        
        elif rangeType == 2:
            ssXform(2)
        
        elif rangeType == 3:
            ssXform(4)
        
        elif rangeType == 4:
            ssXform(6)
        
        elif rangeType == 5:
            ssXform(8)
        
        elif rangeType == 6:
            ssXform(10)

    # Run snapshot command
    pm.uvSnapshot(
        antiAliased=pm.optionVar["shotUVaa_NSUV"],
        entireUVRange=False,
        fileFormat=imfKey,
        name=path,
        overwrite=True,
        redColor=(rgb[0] * 255),
        greenColor=(rgb[1] * 255),
        blueColor=(rgb[2] * 255),
        xResolution=sizeX,
        yResolution=sizeY,
    )
    
    # Custom range: Then move back shells to original position
    if pm.optionVar["shotUVrange_NSUV"] == 2:
    
        # Do the xform
        rangeType = pm.optionVar["shotUVtype_NSUV"]
        
        if rangeType == 1:
            ssXform(1)
        
        elif rangeType == 2:
            ssXform(3)
        
        elif rangeType == 3:
            ssXform(5)
        
        elif rangeType == 4:
            ssXform(7)
        
        elif rangeType == 5:
            ssXform(9)
        
        elif rangeType == 6:
            ssXform(11)  
            
    # Delete window if necessary
    if win != None:
        pm.deleteUI(win)

    if multiTile == False:
        pm.confirmDialog(
            button=["Okay"],
            cancelButton="Okay",
            defaultButton="Okay",
            dismissString="Okay",
            message="Snapshot(s) complete!",
            title="Done!",
        )


# UV Snapshot: Transforms shells into 0->1 range
def ssXform(action, uPos=None, vPos=None):

    # Convert mesh to UV selection and store in list
    selOrg = pm.ls(selection=True)
    selOrgUVs = pm.polyListComponentConversion(toUV=True)

    # Transformation switch below

    # Lying rectangle
    if action == 0:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=0,
            pivotV=0,
            scaleV=2
        )

    # Lying rectangle - undo
    elif action == 1:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=0,
            pivotV=0,
            scaleV=0.5
        )

    # Standing rectangle
    elif action == 2:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=0,
            pivotV=0,
            scaleU=2
        )

    # Standing rectangle - undo
    elif action == 3:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=0,
            pivotV=0,
            scaleU=0.5
        )

    # -1 to 1
    elif action == 4:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            scaleU=0.5,
            scaleV=0.5
        )

    # -1 to 1 - undo
    elif action == 5:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            scaleU=2,
            scaleV=2
        )

    # Second quadrant
    elif action == 6:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            uValue=1
        )

    # Second quadrant - undo
    elif action == 7:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            uValue=-1
        )

    # Third quadrant
    elif action == 8:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            uValue=1,
            vValue=1
        )

    # Third quadrant - undo
    elif action == 9:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            uValue=-1,
            vValue=-1
        )

    # Fourth quadrant
    elif action == 10:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            vValue=1
        )

    # Fourth quadrant - undo
    elif action == 11:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            vValue=-1
        )

    # Custom quadrant - Used by multi-tile/UDIM
    elif action == 12:
        pm.polyEditUV(
            selOrgUVs,
            pivotU=1,
            pivotV=1,
            uValue=uPos,
            vValue=vPos,
        )


# UV Snapshot with the multi-tile/UDIM option on
def ssMultiShot(win=None):

    # Calculate prefix
    def getPrefix(u, v):
        val = 1000 + (u + 1) + (v * 10)
        if val >= 10000:
            val = str(val)[1:]
        else: val = str(val)
        val = ("_"+val)
        return val

    # Read optVars, prepare vars
    oldPath = pm.optionVar["shotUVpath_NSUV"]
    uMax = pm.optionVar["snapshotGridUVal_NSUV"]
    vMax = pm.optionVar["snapshotGridVVal_NSUV"]
    tilesMax = uMax * vMax

    # Loop through and take snapshots
    offsetU, offsetV, offsetTotalU, offsetTotalV, uVal, vVal = (0,)*6
    for x in range(tilesMax):

        # Calculate u and v coordinates
        if uVal == uMax - 1:
            vVal += 1 # Up the vVal pointer
        uVal = x % uMax # Modulus uMax to get U position

        # Get tile prefix, set path and translate UV's
        prefix = getPrefix(uVal, vVal)
        path = re.split("([.])\w+$", oldPath)[0]
        path = path+prefix
        if x == 0: pass
        else:
            if uVal == 0: 
                offsetU = uMax-1
                offsetV = -1
                offsetTotalU -= offsetU
                offsetTotalV -= offsetV
            else: 
                offsetU = -1
                offsetV = 0
                offsetTotalU -= offsetU
                offsetTotalV -= offsetV

            ssXform(12, offsetU, offsetV)

        # Snapshot
        pm.optionVar["shotUVpath_NSUV"] = path
        ssTakeShot(win, True)

    offsetTotalU = offsetTotalU
    offsetTotalV = offsetTotalV

    # Offset everything back to it's original position and restore path
    ssXform(12, offsetTotalU, offsetTotalV)
    pm.optionVar["shotUVpath_NSUV"] = oldPath
    
    pm.confirmDialog(
        button=["Okay"],
        cancelButton="Okay",
        defaultButton="Okay",
        dismissString="Okay",
        message="Snapshot(s) complete!",
        title="Done!",
    )


# Stack shells
def stackShells(shellList=None):

    # Validate selection
    checkSel("faceUV")
    
    selOrg = pm.ls(selection=True, flatten=False)
    
    # Convert to UVs if we have faces
    selUVs = pm.filterExpand(selectionMask=35)
    if selUVs == [] or selUVs == None:
        pm.runtime.ConvertSelectionToUVs()
    
    # Removes the "WARNING: some items cannot be moved in the 3d view" -error message
    pm.setToolTo("moveSuperContext")
    
    # Create shells from selection if we have no incomming shells
    if shellList == [] or shellList == None:
        shellList = getShells()
    
    # Run shell alignment
    alignShells("center", shellList, "Stacking...")
    
    # Expand select original selection, then expand selection to entire shell
    pm.select(selOrg)
    pm.runtime.SelectUVShell()


# Stitch edges - moving, rotating and scaling the connected UV shells 
def stitchTogether(order=0):

    # Vars
    selUVs = None
    uvEdgeA = []
    uvEdgeB = []
    
    # Add a shell to another in the shells list
    def addShellToShell(shells, a, b):

        # Add a to b (element by element) and remove a from shells list
        i = shells.index(b)
        shells[i] = tuple(map(operator.add, a, b))
        shells.remove(a)


    # Validate selection
    checkSel("edgeUV")

    # Get original selection (+as mesh)
    selOrg = pm.ls(selection=True, flatten=True)
    selObj = pm.ls(selection=True, objectsOnly=True)[0]

    # Convert to edges if we have a UV selection
    if pm.filterExpand(selectionMask=35) != None:
        pm.mel.PolySelectConvert(3) # Verts
        pm.mel.PolySelectConvert(20) # Contained edges
        edgeSet = set(pm.ls(selection=True, flatten=True))
    else: edgeSet = set(selOrg)

    # Filter out non-boundary edges
    edgeList = []
    for edge in edgeSet:
        edgeUVs = pm.ls( pm.polyListComponentConversion(edge, fromEdge=True, toUV=True), flatten=True)
        if len(edgeUVs) == 4: # Open edge
           edgeList.append(edge) 

    # Get all shells belonging to the mesh we are stitching on
    shells = getShells(selOrg)

    # Get the size of each shell
    tempList = []
    for shell in shells:
        faces = pm.ls( pm.polyListComponentConversion(shell, fromUV=True, toFace=True), flatten=True)
        area = 0
        for face in faces:
            area += face.getUVArea()
            
        tempList.append((shell, area))

    # Sort list based on second element in tuples, in descending order
    shells = sorted(tempList, key=operator.itemgetter(1), reverse=True)


    # Start stitching
    for edge in edgeList:

        # Get UV edge -pairs
        temp = pm.ls( pm.polyListComponentConversion(edge, fromEdge=True, toUV=True), flatten=True )
        uvEdgePairs = getUVEdgePairs(temp)

        # Loop over shells, comparing ownership of the uvEdgePair towards them
        shellA = []
        shellB = []
        for x in range(0, len(shells)):

            # if uvEdgePairs[0][0] in shells[x][0]:
            if uvEdgePairs[0][0] in shells[x][0] or uvEdgePairs[0][1] in shells[x][0]:
                shellA = shells[x]
                x += 1 # Advance to next shell

            elif uvEdgePairs[1][0] in shells[x][0] or uvEdgePairs[1][1] in shells[x][0]:
                shellB = shells[x]

            if shellA != [] and shellB != []: break # Shells have been found


        # Happens if we try and stitch an edge/UVedge that belongs to one shell only
        if shellB == []: continue

        # Set shell order for the stitching
        if shellA[1] < shellB[1]:
            if order == 0:
                order = 1
                addShellToShell(shells, shellA, shellB)
            else:
                order = 0
                addShellToShell(shells, shellB, shellA)
        else:
            if order == 0:
                addShellToShell(shells, shellB, shellA)
            else:
                addShellToShell(shells, shellA, shellB)

        if order == 0:
            uvEdgeA = uvEdgePairs[0]
            uvEdgeB = uvEdgePairs[1]
        elif order == 1:
            uvEdgeA = uvEdgePairs[1]
            uvEdgeB = uvEdgePairs[0]

        # Create vectors and calculate angles, offset and ratio between the uvEdge pairs
        targetP0 = pm.polyEditUV(uvEdgeA[0], query=True)
        try: targetP1 = pm.polyEditUV(uvEdgeA[1], query=True)
        except IndexError: 
            continue

        sourceP0 = pm.polyEditUV(uvEdgeB[0], query=True)
        try: sourceP1 = pm.polyEditUV(uvEdgeB[1], query=True)
        except IndexError: 
            continue
        
        # Calculate midpoints for the offset vector, and pivot position for 
        targetMid = []
        targetMid.append((targetP0[0] + targetP1[0]) / 2)
        targetMid.append((targetP0[1] + targetP1[1]) / 2)
        sourceMid = []
        sourceMid.append((sourceP0[0] + sourceP1[0]) / 2)
        sourceMid.append((sourceP0[1] + sourceP1[1]) / 2)
        pivotRotate = pm.datatypes.Point(sourceMid)
        pivotScale = pm.datatypes.Point(targetMid)
        
        # Calculate vectors
        offsetVector = pm.datatypes.Vector(targetMid[0] - sourceMid[0], targetMid[1] - sourceMid[1], 0.0)
        sourceVector = pm.datatypes.Vector(sourceP1[0] - sourceP0[0], sourceP1[1] - sourceP0[1], 0.0)
        targetVector = pm.datatypes.Vector(targetP0[0] - targetP1[0], targetP0[1] - targetP1[1], 0.0)

        # Get edge length ratio
        ratio = targetVector.length() / sourceVector.length()

        temp = sourceVector.cross(targetVector)

        # Set sign for the angular rotation
        if temp[2] > 0: # Same
            sign = 1
        elif temp[2] < 0: # Opposite
            sign = -1
            # sourceVector = -sourceVector

        else: # Perpendicular
            sign = 0

        angle = math.degrees(sourceVector.angle(targetVector)) * sign # Calculate signed angle in degrees

        if temp < 0:
            pm.select(uvEdgeB[0]) ## WARN: Might wanna do something about these selects in the future
        else:
            pm.select(uvEdgeB[1]) ##
        pm.runtime.SelectUVShell() ##
        sourceShell = pm.filterExpand(selectionMask=35, expand=0, fullPath=1)

        # Rotate
        pm.polyEditUV(
            sourceShell,
                angle=angle,
                pivotU=(pivotRotate.x),
                pivotV=(pivotRotate.y),
                relative=True,
        )

        # Move
        pm.polyEditUV(
            sourceShell,
                relative=True,
                uValue=(offsetVector.x),
                vValue=(offsetVector.y),
        )

        # Scale
        pm.polyEditUV(
            sourceShell,
                pivotU=(pivotScale.x),
                pivotV=(pivotScale.y),
                relative=True,
                scaleU=ratio,
                scaleV=ratio,
        )

    # Sew
    pm.select(edgeList)
    pm.runtime.ConvertSelectionToContainedEdges()
    pm.polyMapSewMove()


# Straighten shell
def strShell():
    
    # Validate selection
    checkSel("edgeUV")
    
    # Store original selection in various formats
    selOrg = pm.ls(selection=True)
    pm.select( pm.polyListComponentConversion(toUV=True) ) # selOrg as UVs
    selOrgUVs = pm.ls(selection=True, flatten=True) # selOrg as UVs (flattened)
    
    # Check if selection spans multiple shells
    checkSel("multi")
    
    # Get border UVs selection
    selBorderUVs = pm.polySelectConstraint(
        border=1, 
        mode=2, 
        shell=0, 
        type=0x0010
    )
    pm.polySelectConstraint(disable=True)
    selBorderUVs = pm.ls(selection=True, flatten=True)
    
    # Loops for counting border UVs in the original UV selection
    countUV = 0
    counter1 = 0

    while counter1 < len(selOrgUVs):
        counter2 = 0
        
        # Check for match against every border UV - count matching UVs
        while counter2 < len(selBorderUVs):
            if selOrgUVs[counter1] == selBorderUVs[counter2]:
                countUV += 1
            counter2 += 1    
        counter1 += 1 
    
    # Border edge UV count collected. Select original UV selection
    pm.select(selOrgUVs)
    
    # Selection contains only border UVs
    if len(selOrgUVs) == countUV:

        # Straighten map border
        pm.polyStraightenUVBorder(
            blendOriginal=0.0,
            curvature=0.0,
            gapTolerance=5,
            preserveLength=1.0
        )
        
        # Unfold unselected UVs
        unfoldUVs("unselected")
    
    # Selection contains two border UVs
    elif countUV == 2:
        
        # Convert to contained edges, cut, convert back, straighten
        pm.select( pm.polyListComponentConversion(toEdge=True, internal=True) )
        pm.polyMapCut()
        pm.select( pm.polyListComponentConversion(toUV=True) )
        pm.polyStraightenUVBorder(
            blendOriginal=0.0,
            curvature=0.0,
            gapTolerance=5,
            preserveLength=1.0
        )
 
        # Convert to contained edges, sew, convert back    
        pm.select( pm.polyListComponentConversion(toEdge=True, internal=True) )
        pm.polyMapSewMove(
            constructionHistory=True,
            limitPieceSize=False,
            numberFaces=10
        )    
        pm.select(selOrgUVs) # Because the sew command deselects
        
        # Unfold unselected UVs
        unfoldUVs("unselected")
        
    # Faulty UV selection. This one should never execute actually
    else:
        errorCode(7)
    
    # Time to straighten the shell!
    # Select two random UVs. Since they are all on a line now, it doesn't matter
    pm.select(selOrgUVs[0])
    pm.select(selOrgUVs[1], add=True)
    
    # Orient straight
    orientEdge()
    
    # Find shell direction by calculating arctangent. It's either 0 or 90
    angleVal = int( round( calcArctanAngle(selOrgUVs[0], selOrgUVs[1]) ) )
    
    # Unfold
    if angleVal == 0:
        unfoldUVs("U")
    else:
        unfoldUVs("V")
    
    pm.select(selOrg)


# Straighten UV selection
def strUVs():

    # Check the selection
    checkSel("UV")

    # Store selection
    selOrg = pm.ls(selection=True, flatten=True)
    
    # Create shell list
    shellList = getShells()
    
    # Read optionVars
    rotAngleTol = pm.optionVar["strUVsAngle_NSUV"]
    strType = pm.optionVar["strUVsType_NSUV"]
    
    # Create progress bar
    if len(shellList) >= 3: # Needs to be 3 - else we get all white windows
        createProgWin("Straightening...", len(shellList))
    
    shellsTotal = shellsRemain = len(shellList) # Shell count
    
    # Perform straighten for every individual shell
    for shell in shellList:
    
        # Break if cancelled by user
        if len(shellList) >= 3:
            if pm.progressWindow(query=True, isCancelled=True) == True:
                pm.warning("Interupted by user")
                break
 
            # Edit the progress window
            pm.progressWindow(
                edit=True, 
                progress=(shellsTotal - shellsRemain),
                status="Processing shells. %s shells remaining."%shellsRemain
            )

        edgeList = []
        uvEdgeListU = []
        uvEdgeListV = []
        shellUVList = []
        
        # Collect the shell UVs into a list
        for uv in shell:
            if uv not in shellUVList:
                shellUVList.append(uv)

        # Convert selection to edges
        if len(selOrg) < len(shellUVList):
            edgeList = pm.polyListComponentConversion(selOrg, toEdge=True)
        else:
            edgeList = pm.polyListComponentConversion(shellUVList, toEdge=True)

        # Make sure the list is flattened
        edgeList = pm.ls(edgeList, flatten=True)

        # Divide edges into two straighten groups (horizontal and vertical)
        for edge in edgeList:

            # Convert edge to UVs and flatten
            edgeToUV = pm.polyListComponentConversion(edge, toUV=True)
            edgeToUV = pm.ls(edgeToUV, flatten=True)

            # Check if the UVs of the uvEdge belong to selOrg AND the current UV shell
            uvEdge = []
            for uvCoord in edgeToUV:

                # Add UV to list - Need this because an edge can be on two shells
                if uvCoord in selOrg and uvCoord in shellUVList:
                    uvEdge.insert(0, uvCoord)

            # Check uv count in uvEdge. 1 = single coord, 2 = uvEdge, 4 = shared edge
            uvEdgePairs = []
            if len(uvEdge) == 4:
                uvEdgePairs = getUVEdgePairs(edgeToUV)
            elif len(uvEdge) == 2:
                uvEdgePairs = []
                uvEdgePairs.append(uvEdge)

            # Insert the uvEdgePair(s) into either the uvEdgeListU/V by checking its arctan angle
            for uvEdge in uvEdgePairs:
                # Get absolute value of the uvEdge angle (to nearest 90 deg)
                rotAngle = math.fabs( calcArctanAngle(uvEdge[0], uvEdge[1]) )

                # Determine where to insert the uvEdge (U or V list)
                if rotAngle >= 0 and rotAngle <= rotAngleTol:

                    # Create uvEdge tuple and insert into V list
                    uvEdgeTuple = (uvEdge[0], uvEdge[1])
                    uvEdgeListU.insert(0, uvEdgeTuple)

                elif rotAngle <= 90 and rotAngle >= (90 - rotAngleTol):

                    # Create uvEdge tuple and insert into U list
                    uvEdgeTuple = (uvEdge[0], uvEdge[1])
                    uvEdgeListV.insert(0, uvEdgeTuple)

                else:
                    pass # uvEdge is already straight

        # Straighten edges: edge loops along U
        if strType == 0 or strType == 1:

            while len(uvEdgeListU) != 0:

                # Clear lists and get coords from first edgeUV. Use as start for edge loop
                edgeLoop = []
                removeList = []
                scannedEdges = []
                stopLoop = False
                edgeLoop.insert(0, uvEdgeListU[0][0])
                edgeLoop.insert(1, uvEdgeListU[0][1])
                removeList.insert(0, uvEdgeListU[0])
                startingEdge = uvEdgeListU[0] 

                # Keep running the upcomming for-loop until no more components are added
                # to the current edgeLoop. When that happens, exit and straighten.
                while stopLoop == False:
                    compAdded = False

                    # Scan all uvEdges (tuples) and look for connections forming the edgeLoop
                    for x in range(len(uvEdgeListU)):

                        # Check if we've worked on the current tuple
                        if uvEdgeListU[x] not in scannedEdges:

                            # Split up the current tuple into a list with it's edgeUV components
                            singleEdge = []
                            singleEdge.append(uvEdgeListU[x][0])
                            singleEdge.append(uvEdgeListU[x][1])

                            # Check if the edgeUV exist in the edgeLoop list
                            if singleEdge[0] in edgeLoop or singleEdge[1] in edgeLoop:

                                # Check every individual UV component of the current uvEdge
                                for uv in singleEdge:
                                    if uv not in edgeLoop:

                                        # Add components to lists
                                        compAdded = True
                                        edgeLoop.append(uv)
                                        scannedEdges.append(uvEdgeListU[x])
                                        removeList.append(uvEdgeListU[x])

                            else:
                                pass # It doesn't exist in the edgeLoop

                        else:
                            pass # uvEdge has been scanned already

                    # Entire edgeLoop gathered. Stop the while-loop running the for-loop scanner
                    if compAdded == False:
                        stopLoop = True

                # Remove processed edgeUVs (tuples)
                for item in removeList:
                    if item in uvEdgeListU:
                        uvEdgeListU.remove(item)

                # Select the edgeLoop and straighten it
                pm.select(edgeLoop)
                alignUVs("avgV")

        # Straighten edges: edge loops along V
        if strType == 0 or strType == 2:

            while len(uvEdgeListV) != 0:

                # Clear lists and get coords from first edgeUV. Use as start for edge loop
                edgeLoop = []
                removeList = []
                scannedEdges = []
                stopLoop = False
                edgeLoop.insert(0, uvEdgeListV[0][0])
                edgeLoop.insert(1, uvEdgeListV[0][1])
                removeList.insert(0, uvEdgeListV[0])            
                startingEdge = uvEdgeListV[0] 
                
                # Keep running the upcomming for-loop until no more components are added
                # to the current edgeLoop. When that happens, exit and straighten.
                while stopLoop == False:
                
                    compAdded = False
                
                    # Scan all uvEdges (tuples) and look for connections forming the edgeLoop
                    for x in range(len(uvEdgeListV)):
                        
                        # Check if we've worked on the current tuple
                        if uvEdgeListV[x] not in scannedEdges:

                            # Split up the current tuple into a list with it's edgeUV components
                            singleEdge = []
                            singleEdge.append(uvEdgeListV[x][0])
                            singleEdge.append(uvEdgeListV[x][1])
          
                            # Check if the edgeUV exist in the edgeLoop list
                            if singleEdge[0] in edgeLoop or singleEdge[1] in edgeLoop:
                                
                                # Check every individual UV component of the current uvEdge
                                for uv in singleEdge:
                                    if uv not in edgeLoop:

                                        # Add components to lists
                                        compAdded = True
                                        edgeLoop.append(uv)
                                        scannedEdges.append(uvEdgeListV[x])
                                        removeList.append(uvEdgeListV[x])

                            else:
                                pass # It doesn't exist in the edgeLoop
                                
                        else:
                            pass # uvEdge has been scanned already
                            
                    # Entire edgeLoop gathered. Stop the while-loop running the for-loop scanner
                    if compAdded == False:
                        stopLoop = True
                    
                # Remove processed edgeUVs (tuples)
                for item in removeList:
                    if item in uvEdgeListV:
                        uvEdgeListV.remove(item)

                # Select the edgeLoop and straighten it
                pm.select(edgeLoop)
                alignUVs("avgU")
                
        # Decrease the shells remaining -counter
        shellsRemain -= 1

    # Close the progress window
    if len(shellList) >= 3:
        pm.progressWindow(endProgress=True)

    # Select the original selection
    pm.select(selOrg)


# Load/Store field values to a variable
def tdVar(mode, field1, field2=None):

    if mode == "getA":
        varTD = pm.optionVar["manipVarTDA1_NSUV"]
        varMap = pm.optionVar["manipVarTDA2_NSUV"]
        field1.setValue1(varTD)
        field2.setValue1(varMap)
    
    if mode == "getB":
        varTD = pm.optionVar["manipVarTDB1_NSUV"]
        varMap = pm.optionVar["manipVarTDB2_NSUV"]
        field1.setValue1(varTD)
        field2.setValue1(varMap)
    
    if mode == "setA":
        varTD = field1.getValue1()
        varMap = field2.getValue1()
        pm.optionVar["manipVarTDA1_NSUV"] = varTD
        pm.optionVar["manipVarTDA2_NSUV"] = varMap
    
    if mode == "setB":
        varTD = field1.getValue1()
        varMap = field2.getValue1()
        pm.optionVar["manipVarTDB1_NSUV"] = varTD
        pm.optionVar["manipVarTDB2_NSUV"] = varMap
        
    if mode == "updateTD":
        pm.optionVar["td_NSUV"] = field1.getValue1()
    
    if mode == "updateSize":
        pm.optionVar["tdSize_NSUV"] = field1.getValue1()


# Function for selecting an image for display in the texture window
def selectImage(shaderIndex, txtEditor):
    
    # Get list of active images in the texture editor
    imgNameList = pm.textureWindow(txtEditor, query=True, imageNames=True)
    
    # Early exit
    if imgNameList == [] or imgNameList == None:
        return 
    
    # Split up imgNameList
    buffer = []
    buffer = imgNameList[shaderIndex].split(" ")
    
    # Early exit
    if len(buffer) == 0:
        return 
    
    # Get shading group. None found? Early exit
    shader = buffer[2]    
    if shader == "":
        return 
        
    # Find shapes via instObjGroups -> dagSetMembers (dsm)
    objGroupList = pm.listConnections((shader + ".dsm"), plugs=True)
    shapes = pm.listConnections((shader + ".dsm"), shapes=True)
        
    # Check all objects
    for objGroup in objGroupList:
        gid =- 99
    
        # Get the group ID from the current objectGroup (if it exists)
        if pm.objExists(objGroup + ".gid"):
            gid = pm.getAttr(objGroup + ".gid")
        else: continue
        
        # Skip to next objectGroup if the nodeType isn't mesh
        if pm.nodeType(shapes[j]) != "mesh": continue            
        if gid != -99: pm.setAttr((shapes[j] + ".dfgi"), gid)

    # Set image in the editor
    pm.textureWindow(
        txtEditor, edit=True, 
            imageNumber=shaderIndex
            )


# Popup menu buttons for the sidebar
def popupAlignShellsU(btn, parent, img, warn=False):

    # Get UV Selection
    sel = pm.filterExpand(selectionMask=35)

    if btn == 0:

        # Update parent command and image
        parent.setCommand(lambda *args: popupAlignShellsU(0, parent, img, True))
        parent.setImage1(img)
        
        # Also run command if we have a selection and not executing popupAlignShellsU via popupMenu change
        if warn == True and sel != [] or sel != None: alignShells("uMin")

    elif btn == 1:
        parent.setCommand(lambda *args: popupAlignShellsU(1, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignShells("uAvg")

    elif btn == 2:
        parent.setCommand(lambda *args: popupAlignShellsU(2, parent, img, True))
        parent.setImage1(img)        
        if warn == True and sel != [] or sel != None: alignShells("uMax")


def popupAlignShellsV(btn, parent, img, warn=False):
    sel = pm.filterExpand(selectionMask=35)

    if btn == 0:
        parent.setCommand(lambda *args: popupAlignShellsV(0, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignShells("vMax")

    elif btn == 1:
        parent.setCommand(lambda *args: popupAlignShellsV(1, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignShells("vAvg")

    elif btn == 2:
        parent.setCommand(lambda *args: popupAlignShellsV(2, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignShells("vMin")


def popupAlignUVsU(btn, parent, img, warn=False):

    # Get UV Selection
    sel = pm.filterExpand(selectionMask=35)

    if btn == 0:

        # Update parent command and image
        parent.setCommand(lambda *args: popupAlignUVsU(0, parent, img, True))
        parent.setImage1(img)

        # Also run command if we have a selection
        if warn == True and sel != [] or sel != None: alignUVs("minU")

    elif btn == 1:
        parent.setCommand(lambda *args: popupAlignUVsU(1, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignUVs("avgU")

    elif btn == 2:
        parent.setCommand(lambda *args: popupAlignUVsU(2, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignUVs("maxU")

        
def popupAlignUVsV(btn, parent, img, warn=False):
    sel = pm.filterExpand(selectionMask=35)

    if btn == 0:
        parent.setCommand(lambda *args: popupAlignUVsV(0, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignUVs("maxV")
    elif btn == 1:
        parent.setCommand(lambda *args: popupAlignUVsV(1, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignUVs("avgV")
    elif btn == 2:
        parent.setCommand(lambda *args: popupAlignUVsV(2, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: alignUVs("minV")


def popupCalculate(btn, parent, img, field, cbObject=None, warn=False):

    # Get UV Selection
    sel = pm.filterExpand(selectionMask=35)

    if btn == 0:

        # Update parent command and image
        parent.setCommand(lambda *args: popupCalculate(0, parent, img, field, None, True))
        parent.setImage1(img)

        # Also run command if we have a selection
        if warn == True and sel != [] or sel != None: manipField(field, "distU")

    elif btn == 1:
        parent.setCommand(lambda *args: popupCalculate(1, parent, img, field, None, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: manipField(field, "distV")

    elif btn == 2:
        parent.setCommand(lambda *args: popupCalculate(2, parent, img, field, cbObject, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: cbObject() # Opens calcPxDistUI

    elif btn == 3:
        parent.setCommand(lambda *args: popupCalculate(3, parent, img, field, None, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: manipField(field, "getAngle")


def popupCyclePivot(btn, parent, img, warn=False):

    # Get UV Selection
    sel = pm.filterExpand(selectionMask=35)

    # Top left UV bounds
    if btn == 0:
    
        # Update parent command and image
        parent.setCommand(lambda *args: popupCyclePivot(0, parent, img, True))
        parent.setImage1(img)
        
        # Also run command if we have a selection
        if warn == True and sel != [] or sel != None: pivotCycle(0, 2)

    elif btn == 1:
        parent.setCommand(lambda *args: popupCyclePivot(1, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(0, 1)

    elif btn == 2:
        parent.setCommand(lambda *args: popupCyclePivot(2, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(0, 0)

    elif btn == 3:
        parent.setCommand(lambda *args: popupCyclePivot(3, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(0, 3)

    # Top left selection bounds
    elif btn == 4:
        parent.setCommand(lambda *args: popupCyclePivot(4, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(1, 2)

    elif btn == 5:
        parent.setCommand(lambda *args: popupCyclePivot(5, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(1, 1)

    elif btn == 6:
        parent.setCommand(lambda *args: popupCyclePivot(6, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(1, 0)

    elif btn == 7:
        parent.setCommand(lambda *args: popupCyclePivot(7, parent, img, True))
        parent.setImage1(img)
        if warn == True and sel != [] or sel != None: pivotCycle(1, 3)


## WARN: In the future, merge with visBarToggle()
# Toggles the visibility of the topBar groups
def topBarToggle(incVar, toggleBtn, elements, parLayout):

    widthVar = 0
    
    if incVar == 1:
        widthVar = 205
    elif incVar == 2:
        widthVar = 124
    elif incVar == 3:
        widthVar = 205
    elif incVar == 4:
        widthVar = 125
    elif incVar == 5:
        widthVar = 97
    else: pm.error("Wrong arg (incVar) sent to NSUV.core.topBarToggle - Valid args are 1, 2, 3, 4 and 5")

    if elements[0].getVisible() == True:
        toggleBtn.setImage1(barIconClosed)
        for i in elements:
            i.setVisible(False)
        parLayout.setWidth(10)

    else:
        toggleBtn.setImage1(barIconOpen)
        for i in elements:
            i.setVisible(True)        
        parLayout.setWidth(widthVar)


# Translates a UV selection    
def translateUVs(dir):
    
    # Update coords and read from optVars
    updateManipCoords()
    manipAmt = pm.optionVar["manipAmt_NSUV"]
    
    # If the absolute toggle is active
    if pm.optionVar["absToggle_NSUV"] == True:
    
        # Get bounding box
        uvBox = pm.polyEvaluate(boundingBoxComponent2d=True)
        
        # Calc distances
        distCenterU = 0.5 * (uvBox[0][0] + uvBox[0][1])
        distCenterV = 0.5 * (uvBox[1][0] + uvBox[1][1])
        distU = distCenterU - manipAmt
        distV = distCenterV - manipAmt

        # Get proper translation distance
        if distU < 0:
            distU = math.fabs(distU)
            distV = math.fabs(distV)
        else:
            distU = -distU
            distV = -distV
    
    # Move switch
    if dir == "left" or dir == "upLeft" or dir == "downLeft":
        if pm.optionVar["absToggle_NSUV"] == False:
            pm.polyEditUV(
                uValue=(manipAmt * -1),
                vValue=0
            )
        else: # Absolute position
            pm.polyEditUV(
                uValue=distU
            )
    
    if dir == "right" or dir == "upRight" or dir == "downRight":
        if pm.optionVar["absToggle_NSUV"] == False:
            pm.polyEditUV(
                uValue=manipAmt,
                vValue=0
            )
        else: # Absolute position
            pm.polyEditUV(
                uValue=distU
            )
    
    if dir == "up" or dir == "upRight" or dir == "upLeft":
        if pm.optionVar["absToggle_NSUV"] == False:
            pm.polyEditUV(
                uValue=0,
                vValue=manipAmt
            )
        else: # Absolute position
            pm.polyEditUV(
                vValue=distV
            )
    
    if dir == "down" or dir == "downRight" or dir == "downLeft":
        if pm.optionVar["absToggle_NSUV"] == False:
            pm.polyEditUV(
                uValue=0,
                vValue=(manipAmt * -1)
            )
        else: # Absolute position
            pm.polyEditUV(
                vValue=distV
            )


# Override the hotkey for the Unfold3D brushes
def u3dHotkeyOverride():

    # Get current tool
    cTool = pm.currentCtx()

    # Only run if we have a context active
    if pm.contextInfo(cTool, exists=True):

        # Get context type and update it
        ctxType = pm.contextInfo(cTool, c=True)
        if ctxType == "Unfold3DBrush":

            # Override brush size, set to 0
            if pm.optionVar["unfoldBrushSizeOverride_NSUV"]:
                pm.cmds.Unfold3DContext(
                    cTool, edit=True,
                        sizeuv=pm.optionVar["unfoldBrushSizeOrg_NSUV"],
                )
                pm.optionVar["unfoldBrushSizeOverride_NSUV"] = False;

        else: # Update both current context and texUnfoldUVContext
            if (ctxType == "texSculptCacheContext"):
                pm.optionVar["unfoldBrushSizeOrg_NSUV"] = pm.cmds.Unfold3DContext("texUnfoldUVContext", query=True, sizeuv=True)
                sizeNew = pm.texSculptCacheContext(cTool, query=True, size=True)

                # Edit Unfold3d contexts
                pm.cmds.Unfold3DContext(
                    cTool, edit=True,
                    sizeuv=sizeNew,
                )
                pm.cmds.Unfold3DContext( 
                    "texUnfoldUVContext", edit=True,
                        optimize=True,
                )
                pm.optionVar["unfoldBrushSizeOverride_NSUV"] = True


# Unfolds UVs
def unfoldUVs(unfoldType="both", win=None):

    # Vars
    methodVar = 1
    selOrg = None

    # Manage optVars
    if pm.optionVar["unfoldPin_NSUV"] == True and pm.optionVar["unfoldPinType_NSUV"] == 1:
        pinVar = True
    else:
        pinVar = False

    # Check for Unfold3D plugin and set correct value for methodVar
    if pm.pluginInfo("Unfold3D", loaded=True, query=True):
        methodVar = pm.optionVar["unfoldMethod_NSUV"]
    else:
        if pm.optionVar["unfoldMethod_NSUV"] == 1:
            methodVar = 2
        elif pm.optionVar["unfoldMethod_NSUV"] == 2:
            methodVar = 3

    # Validate selection
    checkSel("UV")

    # Store selection
    selOrg = pm.ls(selection=True)
    selObjs = pm.ls(selection=True, objectsOnly=True)


    ## Unfold3D unfold

    if unfoldType == "both" and methodVar == 1:
        if mayaVer >= 201650: # New command
            pm.u3dUnfold(
                selOrg,
                iterations=pm.optionVar["unfoldItr_NSUV"],
                pack=pm.optionVar["unfoldPack_NSUV"],
                borderintersection=pm.optionVar["unfoldBorder_NSUV"],
                triangleflip=pm.optionVar["unfoldFlips_NSUV"],
                mapsize=pm.optionVar["unfoldSize_NSUV"],
                roomspace=pm.optionVar["unfoldSpaceVal_NSUV"],
            )
        else:
            pm.Unfold3D( # Old command
                selOrg,
                unfold=True,
                iterations=pm.optionVar["unfoldItr_NSUV"],
                pack=pm.optionVar["unfoldPack_NSUV"],
                borderintersection=pm.optionVar["unfoldBorder_NSUV"],
                triangleflip=pm.optionVar["unfoldFlips_NSUV"],
                mapsize=pm.optionVar["unfoldSize_NSUV"],
                roomspace=pm.optionVar["unfoldSpaceVal_NSUV"],
            )

        # Close unfold window and return
        if win != None:
            pm.deleteUI(win)
        return


    ## Legacy unfold

    # Split up selection into one list of UV's per mesh
    objUVs = splitUVsPerMesh(selOrg, selObjs)

    if unfoldType == "both":
        if methodVar == 2: # Legacy unfold - Both directions
            for uvs in objUVs:
                pm.polyOptUvs( # Local solver
                    uvs,
                    constructionHistory=pm.optionVar["unfoldHist_NSUV"],
                    globalBlend=pm.optionVar["unfoldSolver_NSUV"],
                    globalMethodBlend=pm.optionVar["unfoldOtO_NSUV"],
                    iterations=pm.optionVar["unfoldMaxItr_NSUV"],
                    optimizeAxis=(pm.optionVar["unfoldConst_NSUV"]-1), # 1-based to 0-based
                    pinSelected=pinVar,
                    pinUvBorder=pm.optionVar["unfoldPinBorder_NSUV"],
                    scale=pm.optionVar["unfoldSFact_NSUV"],
                    stoppingThreshold=pm.optionVar["unfoldStop_NSUV"],
                    useScale=pm.optionVar["unfoldRescale_NSUV"],
                )

        else: # Legacy unfold - Quick
            for uvs in objUVs:
                pm.polyOptUvs( # Local solver
                    uvs,
                    constructionHistory=True,
                    globalBlend=0.0,
                    globalMethodBlend=1.0,
                    iterations=25,
                    optimizeAxis=0,
                    pinSelected=False,
                    stoppingThreshold=0.001,
                    useScale=False,
                )


    ## Legacy unfold - special cases

    elif unfoldType == "unselected": # Legacy unfold - Unselected. Used by strShell()
        for uvs in objUVs:
            pm.polyOptUvs( # Local solver
                uvs,
                constructionHistory=True,
                globalBlend=0.0,
                globalMethodBlend=1.0,
                iterations=25,
                optimizeAxis=0,
                pinSelected=True,
                stoppingThreshold=0.001,
                useScale=False,
            )

    elif unfoldType == "selected": # Legacy unfold - Selected. Used by mapping()
        for uvs in objUVs:
            pm.polyOptUvs(
                uvs,
                constructionHistory=False,
                globalBlend=0.0,
                globalMethodBlend=0.5,
                iterations=5000,
                optimizeAxis=0,
                pinSelected=False,
                stoppingThreshold=0.0010,
                useScale=False,
            )

    
    elif unfoldType == "U": # Legacy unfold - Direction U
        for uvs in objUVs:
            pm.polyOptUvs(
                uvs,
                constructionHistory=False,
                globalBlend=0.0,
                globalMethodBlend=0.5,
                iterations=pm.optionVar["unfoldMaxItr_NSUV"],
                optimizeAxis=2,
                pinSelected=pinVar,
                pinUvBorder=False, ##
                stoppingThreshold=pm.optionVar["unfoldStop_NSUV"],
                useScale=False,
            )

    elif unfoldType == "V": # Legacy unfold - Direction V
        for uvs in objUVs:
            pm.polyOptUvs(
                uvs,
                constructionHistory=False,
                globalBlend=0.0,
                globalMethodBlend=0.5,
                iterations=pm.optionVar["unfoldMaxItr_NSUV"],
                optimizeAxis=1,
                pinSelected=pinVar,
                stoppingThreshold=pm.optionVar["unfoldStop_NSUV"], 
                useScale=False,
            )


    # Reselect original selection
    pm.select(selOrg)

    # Close unfold window
    if win != None:
        pm.deleteUI(win)


# Update the textureWindow displays and all the menues/MM related to the displays
# Not sending any args to this func will result in everything being refreshed
def updateDisplay(mode=(-1), update=(-1), tBarCBox=None):

    # Vars
    color = 1.0
    
    # Get UV editor panel name
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]
    
    # Image display
    if mode == -1 or mode == 0:
    
        # Get option var
        state = pm.optionVar["imgDisp_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0

        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["imgDisp_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, imageDisplay=state)
        pm.menuItem("menuDisplayTxt_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayTxt_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn1").setValue(state)


    # Dimming
    if mode == -1 or mode == 1:
    
        # Get option var
        state = pm.optionVar["imgDim_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: 
                state = 1
                color = 0.5
            else: 
                state = 0
                color = 1.0
    
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["imgDim_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, imageBaseColor=[color, color, color])
        pm.menuItem("menuDisplayDim_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayDim_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn2").setValue(state)


    # Shell shading
    if mode == -1 or mode == 2:
        
        # Get option var
        state = pm.optionVar["shellShade_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["shellShade_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, displaySolidMap=state)
        pm.menuItem("menuDisplayShade_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayShade_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn3").setValue(state)        


    # Shell (texture) borders
    if mode == -1 or mode == 3:

        # Get option var and flip it
        state = pm.optionVar["shellBorder_NSUV"]
        if update != -1:
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["shellBorder_NSUV"] = state
        pm.polyOptions(displayMapBorder=state)
        pm.polyOptions(sizeBorder=3)
        pm.menuItem("menuDisplayBorder_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayBorder_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn4").setValue(state)


    # Shell distortion
    if mayaVer >= 201600:
        if mode == -1 or mode == 4:

            # Get option var
            state = pm.optionVar["shellDist_NSUV"]
            
            # ...and flip it
            if update != -1:
                if state == 0: state = 1
                else: state = 0
            
            # Update optVar, editor, menu, marking menu and button on the visibility bar
            pm.optionVar["shellDist_NSUV"] = state
            pm.textureWindow(txtEditor, edit=True, displayDistortion=state)
            pm.menuItem("menuDisplayDist_NSUV", edit=True, checkBox=state)
            pm.menuItem("menuDisplayDist_MM_NSUV", edit=True, checkBox=state)
            pm.ui.PyUI("visBtn5").setValue(state)


    # Checkers
    if mayaVer >= 201500:
        if mode == -1 or mode == 5:

            # Get option var
            state = pm.optionVar["checkers_NSUV"]
            
            # ...and flip it
            if update != -1:
                if state == 0: state = 1
                else: state = 0
                
            # Update optVar, editor, menu, marking menu and button on the visibility bar
            pm.optionVar["checkers_NSUV"] = state
            pm.textureWindow(txtEditor, edit=True, displayCheckered=state)
            pm.menuItem("menuDisplayCheckers_NSUV", edit=True, checkBox=state)
            pm.menuItem("menuDisplayCheckers_MM_NSUV", edit=True, checkBox=state)
            pm.ui.PyUI("visBtn7").setValue(state)


    # Filtering
    if mode == -1 or mode == 6:
        
        # Get option var 
        state = pm.optionVar["imgFilter_NSUV"]
        stateInv = not state
        
        if update != -1: # ...and flip it
            if state == 0: 
                state = 1
                stateInv = 0
            else: 
                state = 0
                stateInv = 1
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["imgFilter_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, imageUnfiltered=stateInv) # Inverted because UNfiltered, not filtered
        pm.menuItem("menuDisplayFilter_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayFilter_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn8").setValue(state)


    # RGBA
    if mode == -1 or mode == 7:
        rgbaMode = "color"
        
        # Get option var
        if update == 0: # RGB
            pm.optionVar["imgRGBA_NSUV"] = False
        elif update == 1: # A
            pm.optionVar["imgRGBA_NSUV"] = True
            rgbaMode = "mask"
        elif update == -1: # Just read
            if pm.optionVar["imgRGBA_NSUV"] == True: rgbaMode = "mask"
            
        # Update editor
        pm.textureWindow(txtEditor, edit=True, displayStyle=rgbaMode)


    # Grid
    if mode == -1 or mode == 8:

        # Get option var
        state = pm.optionVar["gridDisp_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0

        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["gridDisp_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, toggle=state)
        pm.menuItem("menuDisplayGrid_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayGrid_MM_NSUV", edit=True, checkBox=state)  
        pm.ui.PyUI("visBtn11").setValue(state) 


    # Pixel snap
    if mode == -1 or mode == 9:
    
        # Get option var
        state = pm.optionVar["pxSnap_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["pxSnap_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, imagePixelSnap=state)
        pm.menuItem("menuDisplayPxSnap_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayPxSnap_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn13").setValue(state)


    # Texture editor baking
    if mode == -1 or mode == 10:

        # Get option var
        state = pm.optionVar["editorBaking_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["editorBaking_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, viewPortImage=state)
        pm.menuItem("menuDisplayBaking_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayBaking_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn14").setValue(state)


    # Image ratio
    if mode == -1 or mode == 11:

        # Get option var
        state = pm.optionVar["imgRatio_NSUV"]
        
        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.textureWindow(txtEditor, edit=True, imageRatio=state)
        pm.menuItem("menuDisplayImgRatio_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuDisplayImgRatio_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("visBtn17").setValue(state)
        pm.optionVar["imgRatio_NSUV"] = state


    # Color management
    if mayaVer >= 201600:
        if mode == -1 or mode == 12:
        
            # Get option var
            state = pm.optionVar["colorMan_NSUV"]
            
            if update != -1: # ...and flip it
                if state == 0: state = 1
                else: state = 0
                
            # Update optVar, editor and button on the visibility bar
            try: # Necessary since all code is processed
                pm.optionVar["colorMan_NSUV"] = state
                pm.textureWindow(txtEditor, edit=True, cmEnabled=state)
                pm.ui.PyUI("visBtn17").setValue(state)
            except: pass            


    # Isolate select
    if mode == -1 or mode == 13:
    
        # Get option var and flip it
        state = pm.optionVar["isoSelect_NSUV"]

        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0

        # Update optVar, editor, menu, marking menu and button on the top bar
        pm.textureWindow(txtEditor, edit=True, useFaceGroup=state)
        pm.menuItem("menuViewIsoSelect_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuViewIsoSelect_MM_NSUV", edit=True, checkBox=state)
        pm.ui.PyUI("topBtnIso").setValue(state)
        pm.optionVar["isoSelect_NSUV"] = state

        # Turn off contained, connected faces view, "view faces of selected images"
        if state == 1:
        
            # Update optVars, editor, menues and marking menues 
            pm.optionVar["containedFaces_NSUV"] = not state
            pm.optionVar["connectedFaces_NSUV"] = not state
            pm.optionVar["viewFaces_NSUV"] = not state
            
            pm.textureWindow(txtEditor, edit=True, internalFaces=(not state))
            pm.textureWindow(txtEditor, edit=True, relatedFaces=(not state))
            
            pm.menuItem("menuViewContainedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewContainedFaces_MM_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_MM_NSUV", edit=True, checkBox=(not state))  
            pm.menuItem("menuViewFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewFaces_MM_NSUV", edit=True, checkBox=(not state))   


    # Tile labels
    if mayaVer >= 201500:
        if mode == -1 or mode == 14:
        
            # Get option var and flip it
            state = pm.optionVar["tileLabels_NSUV"]

            if update != -1: # ...and flip it
                if state == 0: state = 1
                else: state = 0
            
            # Update optVar, editor, menu, marking menu and button on the visibility bar
            pm.optionVar["tileLabels_NSUV"] = state
            pm.textureWindow(txtEditor, edit=True, tileLabels=state)
            pm.menuItem("menuDisplayLabels_NSUV", edit=True, checkBox=state)
            pm.menuItem("menuDisplayLabels_MM_NSUV", edit=True, checkBox=state)
            

    # Contained faces
    if mode == -1 or mode == 15:
        
        # Get option var and flip it
        state = pm.optionVar["containedFaces_NSUV"]

        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu and marking menu
        pm.optionVar["containedFaces_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, internalFaces=state)
        pm.menuItem("menuViewContainedFaces_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuViewContainedFaces_MM_NSUV", edit=True, checkBox=state)
        
        # Turn off isolate select, connected faces, "view faces of selected images"
        if state == 1:
        
            # Update optVars, editor, menues and marking menues 
            pm.optionVar["isoSelect_NSUV"] = not state
            pm.optionVar["connectedFaces_NSUV"] = not state
            pm.optionVar["viewFaces_NSUV"] = not state
            
            pm.textureWindow(txtEditor, edit=True, relatedFaces=(not state))
            pm.textureWindow(txtEditor, edit=True, useFaceGroup=(not state))
            
            pm.menuItem("menuViewIsoSelect_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewIsoSelect_MM_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_MM_NSUV", edit=True, checkBox=(not state))  
            pm.menuItem("menuViewFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewFaces_MM_NSUV", edit=True, checkBox=(not state))


    # Connected faces
    if mode == -1 or mode == 16:

        # Get option var and flip it
        state = pm.optionVar["connectedFaces_NSUV"]

        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu and marking menu
        pm.optionVar["connectedFaces_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, relatedFaces=state)
        pm.menuItem("menuViewConnectedFaces_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuViewConnectedFaces_MM_NSUV", edit=True, checkBox=state)

        # Turn off isolate select, contained faces, "view faces of selected images"
        if state == 1:
        
            # Update optVars, editor, menues and marking menues 
            pm.optionVar["isoSelect_NSUV"] = not state
            pm.optionVar["containedFaces_NSUV"] = not state
            pm.optionVar["viewFaces_NSUV"] = not state
            
            pm.textureWindow(txtEditor, edit=True, relatedFaces=(not state))
            pm.textureWindow(txtEditor, edit=True, useFaceGroup=(not state))
            
            pm.menuItem("menuViewIsoSelect_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewIsoSelect_MM_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewContainedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewContainedFaces_MM_NSUV", edit=True, checkBox=(not state))  
            pm.menuItem("menuViewFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewFaces_MM_NSUV", edit=True, checkBox=(not state))


    # View faces of selected images
    if mode == -1 or mode == 17:

        # Get option var and flip it
        state = pm.optionVar["viewFaces_NSUV"]

        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu and marking menu
        pm.optionVar["viewFaces_NSUV"] = state
        pm.textureWindow(txtEditor, edit=True, useFaceGroup=state)
        pm.menuItem("menuViewFaces_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuViewFaces_MM_NSUV", edit=True, checkBox=state)
        
        # Turn off contained, connected faces view, isolate select
        if state == 1:
        
            # Update optVars, editor, menues and marking menues 
            pm.optionVar["containedFaces_NSUV"] = not state
            pm.optionVar["connectedFaces_NSUV"] = not state
            pm.optionVar["isoSelect_NSUV"] = not state
            
            pm.textureWindow(txtEditor, edit=True, internalFaces=(not state))
            pm.textureWindow(txtEditor, edit=True, relatedFaces=(not state))
            
            pm.menuItem("menuViewContainedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewContainedFaces_MM_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewConnectedFaces_MM_NSUV", edit=True, checkBox=(not state))  
            pm.menuItem("menuViewIsoSelect_NSUV", edit=True, checkBox=(not state))
            pm.menuItem("menuViewIsoSelect_MM_NSUV", edit=True, checkBox=(not state))


    # Front face RGBA
    if mode == -1 or mode == 18:

        # Get option vars, create float4
        stateRGB = pm.optionVar["frontColor_NSUV"]
        stateAlpha = pm.optionVar["frontAlpha_NSUV"]
        val = stateRGB + (stateAlpha,)
        
        # Update editor
        pm.textureWindow(txtEditor, edit=True, frontFacingColor=val)
    
    # Back face RGBA
    if mode == -1 or mode == 19:

        # Get option vars, create float4
        stateRGB = pm.optionVar["backColor_NSUV"]
        stateAlpha = pm.optionVar["backAlpha_NSUV"]
        val = stateRGB + (stateAlpha,)
        
        # Update editor
        pm.textureWindow(txtEditor, edit=True, backFacingColor=val)
        
        
    # Toolbar
    if mode == -1 or mode == 20:

        # Get option var and flip it
        state = pm.optionVar["toolbarState_NSUV"]

        if update != -1: # ...and flip it
            if state == 0: state = 1
            else: state = 0
        
        # Update optVar, editor, menu, marking menu and button on the visibility bar
        pm.optionVar["toolbarState_NSUV"] = state
        pm.frameLayout("frameToolbar_NSUV", edit=True, collapse=(not state))
        pm.menuItem("menuViewToolbar_NSUV", edit=True, checkBox=state)
        pm.menuItem("menuViewToolbar_MM_NSUV", edit=True, checkBox=state)
    

# Update the exposure or gamma fields or the optionMenu for the texture window color management
def updateExpGam(mode, control, toggle=False):

    # Get UV editor panel name
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]

    if mode == -1: # Update exposure and gamma from optVars
        
        if pm.optionVar["expToggle_NSUV"] == True:
            pm.textureWindow(txtEditor, edit=True, exposure=pm.optionVar["expField_NSUV"])
            control[0].setValue(pm.optionVar["expField_NSUV"])
            control[1].setValue(True)
        else:
            control[0].setValue(0.00)
            control[1].setValue(False)
            
        if pm.optionVar["gamToggle_NSUV"] == True:
            pm.textureWindow(txtEditor, edit=True, gamma=pm.optionVar["gamField_NSUV"])
            control[2].setValue(pm.optionVar["gamField_NSUV"])
            control[3].setValue(True)
        else:
            control[3].setValue(1.00)
            control[3].setValue(False)            

    elif mode == 0: # Update exposure   
        expVar = pm.optionVar["expField_NSUV"] = control.getValue()
        if pm.textureWindow(txtEditor, query=True, exposure=True) != 0.00:
            pm.textureWindow(txtEditor, edit=True, exposure=expVar)
        
    elif mode == 1: # Update gamma
        gamVar = pm.optionVar["gamField_NSUV"] = control.getValue()
        if pm.textureWindow(txtEditor, query=True, gamma=True) != 1.00:
            pm.textureWindow(txtEditor, edit=True, gamma=gamVar)

    elif mode == 2: # Toggle exposure
        if toggle == True:
            expVar = pm.optionVar["expField_NSUV"]
            pm.optionVar["expToggle_NSUV"] = True
        else:
            expVar = 0.00
            pm.optionVar["expToggle_NSUV"] = False
        control.setValue(expVar)
        pm.textureWindow(txtEditor, edit=True, exposure=expVar)
        
    elif mode == 3: # Toggle gamma
        if toggle == True:
            gamVar = pm.optionVar["gamField_NSUV"]
            pm.optionVar["gamToggle_NSUV"] = True
        else:
            gamVar = 1.00
            pm.optionVar["gamToggle_NSUV"] = False
        control.setValue(gamVar)
        pm.textureWindow(txtEditor, edit=True, gamma=gamVar)
        
    elif mode == 4: # OptionMenu
        newVT = control.getValue()
        currentVT = pm.textureWindow(txtEditor, query=True, viewTransformName=True)
        
        try: # Change VT to the one selected in the optionMenu
            pm.textureWindow(txtEditor, edit=True, viewTransformName=newVT)
            pm.optionVar["vtName_NSUV"] = newVT

        except RuntimeError: # ...or just edit the optionMenu
            control.setValue(currentVT)
            pm.optionVar["vtName_NSUV"] = currentVT

            
# Saves the state of the frames into optVars
def updateFrame(frame, state):

    if frame == 1:
        pm.optionVar["frame1_NSUV"] = state
    elif frame == 2:
        pm.optionVar["frame2_NSUV"] = state
    elif frame == 3:
        pm.optionVar["frame3_NSUV"] = state
    elif frame == 4:
        pm.optionVar["frame4_NSUV"] = state
    elif frame == 5:
        pm.optionVar["frame5_NSUV"] = state
    elif frame == 6:
        pm.optionVar["frame6_NSUV"] = state
    elif frame == 7:
        pm.optionVar["frame7_NSUV"] = state
    elif frame == 8:
        pm.optionVar["frame8_NSUV"] = state


# Updates the pivot of the move/rotate/scale -contexts
def updateManipCoords():

    # Get current tool
    cTool = pm.currentCtx()

    if cTool == "moveSuperContext":
        pm.optionVar["manipCoords_NSUV"] = pm.texMoveContext( "texMoveContext", query=True, position=True ) 
    
    elif cTool == "RotateSuperContext":
        pm.optionVar["manipCoords_NSUV"] = pm.texRotateContext( "texRotateContext", query=True, position=True ) 
    
    elif cTool == "scaleSuperContext":
        pm.optionVar["manipCoords_NSUV"] = pm.texScaleContext( "texScaleContext", query=True, position=True )
        
    elif cTool == "ModelingToolkitSuperCtx":
        pm.optionVar["manipCoords_NSUV"] = pm.texWinToolCtx( "ModelingToolkitSuperCtx", query=True, position=True )
    
    else: # Some other tool - pass
        pass


# Updates the UV set editor
def updateUVSetEditor(scrollList):

    # Since the menubar is created by a scripted panel -callback (addTextureWindow) command before createUI()
    # draws the window, scrollList will point to the empty list that is defined at the top inside NSUV.UI 
    # Solution: We will fetch the scroll list by its string name instead. Hacky but works!
    if type(scrollList) is list:
        scrollList = pm.ui.PyUI("uvSetScrollList_NSUV")

    # Clear the UV set editor
    scrollList.removeAll()
    
    # Mesh or components selected?
    sel = pm.filterExpand(selectionMask=(12, 31, 32, 34, 35))
    if sel != [] and sel != None:

        # Get UV sets
        uvSetsAll, uvSetCurrent = getSets()

        if uvSetsAll != [] and uvSetsAll != None:

            # Rebuild the textScrollList
            for item in uvSetsAll:
            
                # Check UV set for instance identifiers
                uvSetPerInst = pm.polyUVSet(
                    sel, query=True,
                    perInstance=True,
                    uvSet=item,
                )
                
                # If instance identifier was found, continue to next uv-set in the loop
                if uvSetPerInst == None: continue
                else: uvSetInst = uvSetPerInst[0]
                    
                # Add UV set to list
                scrollList.append(uvSetInst) 
        
        # ...and highlight it in the editor
        scrollList.setSelectItem(uvSetCurrent)
        
        # Also highlight it in the native UV set editor if it's open
        if pm.window("uvSetEditor", exists=True):
            pm.textScrollList(
                "uvSetList", edit=True,
                selectItem=uvSetCurrent
            )

    else:
        # No selection on the UI - clear the list
        scrollList.deselectAll()
        scrollList.removeAll()


# Activates a Unfold3D or other UV tool context, such as the Cut tool or the Unfold tool
def uvContextTool(contextType, toolType, options=False):

    # Set context type
    if contextType == 0: tool = "texLatticeDeformSuperContext"
    elif contextType == 1: tool = "texSmudgeUVSuperContext"
    elif contextType == 2: tool = "texMoveUVShellSuperContext"
    elif contextType == 3: tool = "texSmoothSuperContext"
    elif contextType == 4: tool = "texTweakSuperContext"
    elif contextType == 5: tool = "texUnfoldUVContext"
    elif contextType == 6: tool = "texCutUVContext"
    elif contextType == 7: tool = "texSculptCacheContextObj"
    elif contextType == 8: tool = "texSymmetrizeUVContext"

    # Execute context type
    if toolType == "unfold": pm.cmds.Unfold3DContext(tool, edit=True, unfold=True)
    elif toolType == "optimize": pm.cmds.Unfold3DContext(tool, edit=True, optimize=True)
    elif toolType == "symmetrize": pm.SymmetrizeUVContext(tool, edit=True)
    elif toolType == "cut": pm.texCutContext(tool, edit=True, mode="Cut")
    elif toolType == "sew": pm.texCutContext(tool, edit=True, mode="Sew")
    elif toolType == "grab": pm.texSculptCacheContext(tool, edit=True, mode="Grab")
    elif toolType == "pinch": pm.texSculptCacheContext(tool, edit=True, mode="Pinch")
    elif toolType == "smear": pm.texSculptCacheContext(tool, edit=True, mode="Smear")
    elif toolType == "freeze": pm.texSculptCacheContext(tool, edit=True, mode="Freeze")

    # Activate tool and select mode
    pm.setToolTo(tool)

    # Popup the tool settings panel
    if options == True: pm.toolPropertyWindow()


# Toggles visibility of the visBar groups
def visBarToggle(incVar, toggleBtn, elements, parLayout):

    widthVar = 0

    if incVar == 1:
        if mayaVer <= 201400:
            widthVar = 173
        elif mayaVer <= 201500:
            widthVar = 211
        else:
            widthVar = 211
    elif incVar == 2:
        widthVar = 77
    elif incVar == 3:
        widthVar = 96
    elif incVar == 4:
        widthVar = 306
    elif incVar == 5:
        widthVar = 155
    else: pm.error("Wrong arg (incVar) sent to NSUV.core.visBarToggle - Valid args are 1, 2, 3 and 4")

    if elements[0].getVisible() == True:
        toggleBtn.setImage1(barIconSmallClosed)
        for i in elements:
            i.setVisible(False)
        parLayout.setWidth(10)

    else:
        toggleBtn.setImage1(barIconSmallOpen)
        for i in elements:
            i.setVisible(True)
        parLayout.setWidth(widthVar)


## Error Codes

def errorCode(code):
    
    # No selection at all
    if code == 0:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select something before performing this operation.",
            title="Error!"
        )
        pm.error("You must select something before performing this operation.")
    
    # No valid face selection
    elif code == 1:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some faces before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some faces before performing this operation.")
    
    # No valid UV selection
    elif code == 2:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some UVs before performing this operation.")
    
    # No valid edge or UV selection
    elif code == 3:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some edges or UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some edges or UVs before performing this operation.")
            
    # No valid face or UV selection
    elif code == 4:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some faces or UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some faces or UVs before performing this operation.")
        
    # No valid mesh or UV selection
    elif code == 5:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select a mesh or some UVs before performing this operation.",
            title="Error!"
        )
        pm.error("You must select a mesh or some UVs before performing this operation.")
        
    # Selection spans over multiple shells
    elif code == 6:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="This tool doesn't work if the selection spans over multiple UV shells.",
            title="Error!"
        )
        pm.error("This tool doesn't work if the selection spans over multiple UV shells.")
        
    # Straighten UV shell failed
    elif code == 7:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("The straighten shell -tool only works on -one- UV shell and only on -one- "
                 "edge loop -or- edge ring at a time. Center or shell border selection does "
                 "not matter."),
            title="Error!"
        )
        pm.error("Incorrect selection for the straighten shell tool")
        
    # Didn't select exactly two UVs
    elif code == 8:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select exactly two UVs before performing this operation."),
            title="Error!"
        )
        pm.error("You must select exactly two UVs before performing this operation.")  
        
    # No valid mesh selection
    elif code == 9:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select a mesh before performing this operation."),
            title="Error!"
        )
        pm.error("You must select a mesh before performing this operation.")  
        
    # File path is blank
    elif code == 10:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must enter a file path."),
            title="Error!"
        )
        pm.error("You must enter a file path.")  
        
    # No valid face or mesh selection
    elif code == 11:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("You must select some face(s) or a mesh before performing this operation."),
            title="Error!"
        )
        pm.error("You must select some face(s) or a mesh before performing this operation.")  
    
    # Invalid selection for UV Set: Propagate
    elif code == 12:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("Propagate requires more than one object to be selected."),
            title="Error!"
        )
        pm.error("Propagate requires more than one object to be selected.")  
    
    # Didn't select TWO UV's or ONE edge
    elif code == 13:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("This operation requires at least 2 UVs or an edge."),
            title="Error!"
        )
        pm.error("You must select exactly two UVs or one edge before performing this operation.")  

    # No valid edge selection
    elif code == 14:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("This operation requires an edge selection."),
            title="Error!"
        )
        pm.error("This operation requires an edge selection.")  

    ## WARN: UNUSED - Previously: # Didn't select TWO UV's
    elif code == 15:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("Using this feature on a UV selection requires exactly 2 UVs!"),
            title="Using this feature on a UV selection requires exactly 2 UVs!"
        )
        pm.error("Using this feature on a UV selection requires exactly 2 UVs!")

    # Unfold3D plugin not loaded
    elif code == 16:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("The Unfold3D plugin needs to be loaded before running this!"),
            title="The Unfold3D plugin needs to be loaded before running this!"
        )
        pm.error("The Unfold3D plugin needs to be loaded before running this!")

    # UDIM U-value exceeded
    elif code == 17:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("UDIM has a limitation of 10 UV tiles in the U-dimension. Setting field to 10!"),
            title="Error!"
        )
        pm.error("UDIM has a limitation of 10 UV tiles in the U-dimension. Setting field to 10!")

    # UDIM V-value exceeded
    elif code == 18:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("UDIM has a limitation of 1000 UV tiles in the V-dimension. Setting field to 1000!"),
            title="Error!"
        )
        pm.error("UDIM has a limitation of 1000 UV tiles in the V-dimension. Setting field to 1000!")
        
    # Two UV's who are not shared by same edge
    elif code == 19:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("The selected UVs are not located on the same shared edge."),
            title="Error!"
        )
        pm.error("The selected UVs are not located on the same shared edge.")
        
    # No valid selection for copying UVs/UV sets)
    elif code == 20:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must select some polygon components before performing this operation.",
            title="Error!"
        )
        pm.error("You must select some polygon components before performing this operation.")
        
    # No unmapped faces found
    elif code == 21:
        pm.confirmDialog(
            button="Ok",
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message=("No unmapped faces was found on the selected mesh."),
            title="Error!"
        )   
    
    # Scene needs to be saved (UV Set Order Manager > Clear Zombie Sets)
    elif code == 22:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You need to save the scene before performing a reload!", 
            title="Error!"
        )
        
    # Only a single mesh
    elif code == 23:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="You must have exactly one mesh selected before performing a UV set rename!", 
            title="Error!"
        )
        pm.error("You must have exactly one mesh selected before performing a UV set rename!")
        
    # UV names are identical
    elif code == 24:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="Cannot rename UV set to an existing UV set name!", 
            title="Error!"
        )
        pm.error("Cannot rename UV set to an existing UV set name!")
        
    # Invalid UV set name
    elif code == 25:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="UV set names cannot be blank or start with a digit or a symbol!", 
            title="Error!"
        )
        pm.error("UV set names cannot be blank or start with a digit or a symbol!")

    # Loaded mesh doesn't exist
    elif code == 26:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="Attempting to load a mesh that no longer exists - aborting!", 
            title="Error!"
        )
        pm.error("Attempting to load a mesh that no longer exists - aborting!")
        
    # Loaded components doesn't exist
    elif code == 27:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="Attempting to load components that no longer exists - aborting!", 
            title="Error!"
        )
        pm.error("Attempting to load components that no longer exists - aborting!")

    # Copying UV sets with last known options failed
    elif code == 28:
        pm.confirmDialog(
            button=["Ok"],
            cancelButton="Ok",
            defaultButton="Ok",
            dismissString="Ok",
            message="One or both of the UV sets used in the last copy no longer exists - aborting!", 
            title="Error!"
        )
        pm.error("One or both of the UV sets used in the last copy no longer exists - aborting!")