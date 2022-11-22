# -*- coding: utf-8 -*-
"""

    Main user-interface for Nightshade UV Editor (NSUV) v2.1.3

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

## Table of contents
# Initialization
# Texture Windows
# Main Window
# Toolbar
# Menubar
# Menubar: Menues
# Radial Menues
# Popup Menues
# Auxiliary Windows


## Imports

import pymel.core as pm
from functools import partial
import re
import core as core
import optVars as vars


## Initialization

# Vars
NSUV_title = pm.optionVar["editorTitle_NSUV"]
scrollListUVSet = []

# UI Margins
gapA = 4 # Misc custom margins
gapB = 5

sBarB = 8 # Sidebar margins. Bottom, horizontal, left, top
sBarH = 3
sBarL = 1
sBarT = 1

tBarH = 1 # Topbar margins. Horizontal, left, right, top
tBarL = 9
tBarR = 8
tBarT = 0

vBarH = 0 # Visbar margins. Bottom, horizontal, left, right, top
vBarL = 3
vBarR = 8
vBarT = 2


# Main window
mainWinX = 977
mainWinY = 900


# Auxiliary windows
largeWinX = 470 # Large window template
largeWinY = 460 
smallWinX = 300 # Small window template

aboutWinY = 190
autoSeamsWinY = 150
buyWinY = 176
calcPxCellX = (smallWinX/4)-5
calcPxCellY = 17
calcPxWinY = 189
copySetWinY = 94
createSetWinY = 156
distributeWinY = 312
dispSettingsWinY = 321
layoutWinY = 711
matchTolWinY = 139
mapAutoWinY = 581
mapCylindricalWinY = 169
mapNormalWinY = 261
mapPlanarWinY = 304
mapSphericalWinY = 191
normalizeWinY = 261
randWinY = 241
relaxWinY = 355
renameSetWinY = 94
snapshotWinY = 433
strUVWinY = 188
submitWinY = 190
totdWinY = 354
unfoldWinY = 335
workUnitsWinY = 139


# UI dimensions
btnLeft = 12 # Snapshot and layout predef button/radBtn margins
btnTop = 20
radLeft = 2
radTop = 50

dispCol1 = 30 # Display settings
dispCol2 = 65
dispCol3 = 210
dispCol4 = 74
dispCol5 = 95
dispCol6 = 103
dispCol7 = 54

frameMainX = 119 # Side panel frame
frameMargin = 10 # Frame margin for large and small window templates
frameX = largeWinX - 26 # Large window frame (About, Workflow, Tricks)

iconSmall = 18 # Snapping and translation icons
iconTop = 26 # Topbar icons

layoutCol1 = 120

mappingCol1 = 170 # Mapping/Projection columns
mappingCol2 = 110
mappingCol3 = 150

renameCol1 = 110 # Rename UV set columns
renameCol2 = 110

setListY = 64 # UV Set list
sepSpace = 5 # Separators height
sepSpace2 = 10

largeCol1 = 170 # Columns for large windows
largeCol2 = 70
largeCol3 = 130
smallCol1 = 100 # Columns for small windows
smallCol2 = 175

totdCol1 = 120 # Columns for the Tip of the Day -window
totdCol2 = 350

vBarFieldY = 16 # Visbar fields
vBarFieldX = 40


# UI names
menuDimImage, menuEditorBaking, menuGrid, menuImageDisplay, \
menuImageRatio, menuMapOverlay, menuPixelSnap, menuUnfiltered = ("",)*8
panelUV = "NSUV_panel"
txtWinFlow = "NSUV_textureWindowFlow"
txtWinFrame = "NSUV_textureWindowFrame"

visBtn1 = "visBtn1"
visBtn2 = "visBtn2"
visBtn3 = "visBtn3"
visBtn4 = "visBtn4"
visBtn5 = "visBtn5"
visBtn6 = "visBtn6"
visBtn7 = "visBtn7"
visBtn8 = "visBtn8"
visBtn9 = "visBtn9"
visBtn10 = "visBtn10"
visBtn11 = "visBtn11"
visBtn12 = "visBtn12"
visBtn13 = "visBtn13"
visBtn14 = "visBtn14"
visBtn15 = "visBtn15"
visBtn16 = "visBtn16"
visBtn17 = "visBtn17"
topBtnIso = "topBtnIso"

winMain = "NSUV_mainWin"
winAbout = "NSUV_aboutWin"
winAutoSeam = "NSUV_autoSeamsWin" 
winBuy = "NSUV_buyWin"
winCalcPx = "NSUV_calcPxWin"
winCopyNewUVSet = "NSUV_copyNewUVSetWin"
winDispSettings = "NSUV_displaySettingsWin"
winDistr = "NSUV_distributeWin"
winFAQ = "NSUV_faqWin"
winLayout = "NSUV_layoutWin"
winMatchTol = "NSUV_matchTolWin"
winMapAuto = "NSUV_mapAutoWin"
winMapCamera = "NSUV_mapCameraWin"
winMapCylindrical = "NSUV_mapCylindricalWin"
winMapNormal = "NSUV_mapNormalWin"
winMapPlanar = "NSUV_mapPlanarWin"
winMapSpherical = "NSUV_mapSphericalWin"
winNewUVSet = "NSUV_newUVSetWin"
winNormalize = "NSUV_normalizeWin"
winRnd = "NSUV_rndWin"
winRelax = "NSUV_relaxWin"
winRenameUVSet = "NSUV_renameUVSetWin"
winSS = "NSUV_snapshotWin"
winStrUVs = "NSUV_straightenUVsWin"
winSubmit = "NSUV_submitWin"
winUnits = "NSUV_workingUnitsWin"
winTotd = "NSUV_tipOfDayWin"
winTricks = "NSUV_tricksWin"
winUnfold = "NSUV_unfoldWin"
winUpdate = "NSUV_updateWin"
winWelcome = "NSUV_welcomeWin"
winWorkflow = "NSUV_workflowWin"


# Icon dictionary
iconDict = {
    "barIconSmallOpen": "NS_barIconSmallOpen.png",
    "barIconSmallClosed": "NS_barIconSmallClosed.png",
    "barIconOpen": "NS_barIconOpen.png",
    "barIconClosed": "NS_barIconClosed.png",
    "faq": "NSUV_faq.png",
    "title": "NSUV_title.png",
    "tricks": "NSUV_tricks.png",
    "workflow": "NSUV_workflow.png",

    "scaleUV": "NS_manipScaleUV.png", 
    "scaleU": "NS_manipScaleU.png",
    "scaleV": "NS_manipScaleV.png",
    "flip": "NS_manipFlip.png",
    "rotate90CCW": "NS_manipRot90CCW.png",
    "rotateCCW": "NS_manipRotCCW.png",
    "rotate90CW": "NS_manipRot90CW.png",
    "rotateCW": "NS_manipRotCW.png",
    "moveUpLeft": "NS_manipMoveUpLeft.png",
    "moveUp": "NS_manipMoveUp.png",
    "moveUpRight": "NS_manipMoveUpRight.png",
    "moveLeft": "NS_manipMoveLeft.png",
    "moveRight": "NS_manipMoveRight.png",
    "moveDownLeft": "NS_manipMoveDownLeft.png",
    "moveDown": "NS_manipMoveDown.png",
    "moveDownRight": "NS_manipMoveDownRight.png",
    "absRelOff": "NS_absRelToggleOff.png",
    "absRelOn": "NS_absRelToggleOn.png",
    "calcAngle": "NS_calcAngle.png",
    
    "cycleSel1": "NS_cyclePivotSel1.png",
    "cycleSel2": "NS_cyclePivotSel2.png",
    "cycleSel3": "NS_cyclePivotSel3.png",
    "cycleSel4": "NS_cyclePivotSel4.png",
    "cycleUV1": "NS_cyclePivotUV1.png",
    "cycleUV2": "NS_cyclePivotUV2.png",
    "cycleUV3": "NS_cyclePivotUV3.png",
    "cycleUV4": "NS_cyclePivotUV4.png",
    
    "double": "NS_manipVal2.png",
    "reset": "NS_manipValReset.png",
    "distU": "NS_manipCalcDistU.png",
    "distV": "NS_manipCalcDistV.png",
    "distPx": "NS_calcPixelDist.png",
    "manipVarA": "NS_manipVarA.png",
    "manipVarB": "NS_manipVarB.png",
    "manipVarC": "NS_manipVarC.png",
    
    "projAuto": "NS_projAuto.png",
    "projCyl": "NS_projCyl.png",
    "projPlane": "NS_projPlane.png",
    "projPlaneX": "NS_projPlaneX.png",
    "projPlaneY": "NS_projPlaneY.png",
    "projPlaneZ": "NS_projPlaneZ.png",
    "projSphere": "NS_projSphere.png",
    "projCam": "NS_projCam.png",
    "projNormal": "NS_projNormal.png",
    "projContour": "NS_projContour.png",
    "projFind": "NS_projFind.png",
    
    "cutTool": "NS_cutUVTool.png",
    "sewTool": "NS_sewUVTool.png",
    "unfoldTool": "NS_unfoldUVTool.png",
    "optimizeTool": "NS_optimizeUVTool.png",
    "cut": "NS_cutUVs.png",
    "sew": "NS_sewUVs.png",
    "unfold": "NS_unfold.png",
    "optimize": "NS_optimizeUVs.png",
    "split": "NS_splitUVs.png",
    "moveSew": "NS_moveSewUVs.png",
    "unfoldU": "NS_unfoldU.png",
    "strShell": "NS_straightenShell.png",
    "createShell": "NS_createShell.png",
    "stitch": "NS_stitch.png",
    "smoothTool": "NS_smoothUVTool.png",
    "strSel": "NS_straightenSel.png",
    
    "orient": "NS_orientShells.png",
    "orientEdge": "NS_orientEdge.png",
    "stack": "NS_stackShells.png",
    "match": "NS_matchUVs.png",
    "layout": "NS_layoutShells.png",
    "layoutStrip": "NS_layoutShellsUStrip.png",
    "spreadOut": "NS_spreadOutShells.png",
    "gather": "NS_gatherShells.png",
    "randomize": "NS_randomizeUV.png",
    "distribute": "NS_distribute.png",
    
    "alignShellsTop": "NS_alignShellsTop.png",    
    "alignShellsLeft": "NS_alignShellsLeft.png",
    "alignVMax": "NS_alignVmax.png",
    "alignUMin": "NS_alignUmin.png",
    "alignShellsMidV": "NS_alignShellsMidV.png",
    "alignShellsMidU": "NS_alignShellsMidU.png",
    "alignVMid": "NS_alignVmid.png",
    "alignUMid": "NS_alignUmid.png",
    "alignShellsBottom": "NS_alignShellsBottom.png",
    "alignShellsRight": "NS_alignShellsRight.png",
    "alignVMin": "NS_alignVmin.png",
    "alignUMax": "NS_alignUmax.png",
    "normalize": "NS_normalize.png",
    "normalizeUV": "NS_normalizeUV.png",
    "unitize": "NS_unitize.png",
    "snapAB": "NS_snapAtoB.png",
    "snapTopLeft": "NS_snapTopLeft.png",
    "snapTop": "NS_snapTop.png",
    "snapTopRight": "NS_snapTopRight.png",
    "snapLeft": "NS_snapLeft.png",
    "snapCenter": "NS_snapCenter.png",
    "snapRight": "NS_snapRight.png",
    "snapBottomLeft": "NS_snapBottomLeft.png",
    "snapBottom": "NS_snapBottom.png",
    "snapBottomRight": "NS_snapBottomRight.png",
    
    "uvSetNew": "NS_uvSetNew.png",
    "uvSetCopy": "NS_uvSetCopy.png",
    "uvSetDupe": "NS_uvSetDupe.png",
    "uvSetProp": "NS_uvSetPropagate.png",
    "uvSetOrderMan": "NS_uvSetOrderMan.png",
    "uvSetShareInst": "NS_uvSetShareInst.png",
    "uvSetSelInst": "NS_uvSetSelInst.png",
    "uvSetSnapshot": "NS_uvSnapshot.png",
    
    "tdVarA": "NS_tdVarA.png",
    "tdVarB": "NS_tdVarB.png",
    "tdSet": "NS_tdSet.png",
    "tdGet": "NS_tdGet.png",
    
    "imgDisp": "NS_imageDisplay.png",
    "dimTexture": "NS_dimTexture.png",
    "shadeShells": "NS_shadeShells.png",
    "shellBorders": "NS_shellBorders.png",
    "distToggle": "NS_distortionToggle.png",
    "edgeColors": "NS_edgeColorToggle.png",
    "checker": "NS_checkerTiles.png",
    "filtered": "NS_filteredMode.png",
    "dispColor": "NS_displayColor.png",
    "dispAlpha": "NS_displayAlpha.png",
    
    "gridDisp": "NS_gridDisplay.png",
    "gridSnap": "NS_snapToGrid.png",
    "pxSnap": "NS_pixelSnap.png",
    
    "swapBG": "NS_swapBG.png",
    "updatePSD": "NS_updatePSD.png",
    "bakeEditor": "NS_bakeEditor.png",
    "imgRatio": "NS_imageRatio.png",
    
    "expControl": "NS_expControl.png",
    "gammaControl": "NS_gammaControl.png",
    "vtOn": "NS_transformToggleOn.png",
    "vtOff": "NS_transformToggleOff.png",
    "winLockOn": "NS_winLockOn.png",
    "winLockOff": "NS_winLockOff.png",
    
    "uvRangeA": "NS_uvRange_a.png",
    "uvRangeB": "NS_uvRange_b.png",
    "uvRangeC": "NS_uvRange_c.png",
    "uvRangeD": "NS_uvRange_d.png",
    "uvRangeE": "NS_uvRange_e.png",
    "uvRangeF": "NS_uvRange_f.png",
    "uvRangeG": "NS_uvRange_g.png",
    "uvRangeH": "NS_uvRange_h.png",
    "uvRangeI": "NS_uvRange_i.png",
    "uvRangeJ": "NS_uvRange_j.png",
    "uvRangeK": "NS_uvRange_k.png",
    "uvRangeL": "NS_uvRange_l.png",
    "uvRangeM": "NS_uvRange_m.png",
    "uvRangeN": "NS_uvRange_n.png",
    
    "latticeTool": "NS_latticeTool.png", 
    "smudgeTool": "NS_smudgeUVTool.png", 
    "smearTool": "NS_smearUVTool.png", 
    "moveTool": "NS_moveUVShellTool.png", 
    "grabTool": "NS_grabUVTool.png", 
    "pinchTool": "NS_pinchUVTool.png", 
    "tweakTool": "NS_tweakUVTool.png", 
    "pinTool": "NS_pinUVTool.png", 
    "symmetrizeTool": "NS_symmetrizeUVTool.png", 
    "pin": "NS_pinUVs.png", 
    "unpin": "NS_unpinUVs.png", 
    "unpinAll": "NS_unpinAllUVs.png", 
    "pathTool": "NS_shortestPathTool.png", 
    "shell": "NS_selShell.png", 
    "border": "NS_selBorder.png", 
    "softhard": "NS_softHardBorder.png", 
    "grow": "NS_selGrow.png", 
    "shrink": "NS_selShrink.png", 
    "invert": "NS_selInvert.png", 
    "selectA" : "NS_saveSelA.png",
    "selectB" : "NS_saveSelB.png",
    "isoToggle": "NS_isoSelToggle.png", 
    "isoAdd": "NS_isoSelAdd.png", 
    "isoSub": "NS_isoSelSubtract.png", 
    "isoReset": "NS_isoSelReset.png", 
    "copyUV": "NS_copyUV.png", 
    "pasteUV": "NS_pasteUV.png", 
    "delUV": "NS_deleteUV.png",
    
    "qLayoutA": "NS_qLayout_a.png",
    "qLayoutB": "NS_qLayout_b.png",
    "qLayoutC": "NS_qLayout_c.png",
    
    "distr2Target": "NS_distributeTT.png"
}

# Tip of the Day -image dictionary
totdImageDict = {
    1 : "NS_totd_01.png",
    2 : "NS_totd_02.png",
    3 : "NS_totd_03.png",
    4 : "NS_totd_04.png",
    5 : "NS_totd_05.png",
    6 : "NS_totd_06.png",
    7 : "NS_totd_07.png",
    8 : "NS_totd_08.png",
    9 : "NS_totd_09.png",
    10 : "NS_totd_10.png",
    11 : "NS_totd_11.png",
    12 : "NS_totd_12.png",
    13 : "NS_totd_13.png",
    14 : "NS_totd_14.png",
    15 : "NS_totd_15.png",
    16 : "NS_totd_16.png",
    17 : "NS_totd_17.png",
    18 : "NS_totd_18.png",
    19 : "NS_totd_19.png",
    20 : "NS_totd_20.png",
}

# Tip of the Day -texts dictionary
totdTextDict = {
    1 : "Many buttons in NSUV have secondary functionality on the right mouse button. For "\
"instance: Flip UV's flips a selection along U on left click, but along V if you right click it.",
    2 : "If you are new to UV-unwrapping be sure to check out the \"Basic workflow\" guide "\
"under the NSUV -menu.",
    3 : "If you are a more advanced user, check out the \"Tips and Tricks\" section under the NSUV -menu.",
    4 : "Some icons are collected under a shared popup menu accessable via right-click. "\
"Examples: Align Shells, Copy UV's and Cycle Pivot.",
    5 : "All options windows  - such as the ones for the UV projections or Layout UV's - are "\
"accessable via the right mouse button.",
    6 : "You can scale and rotate shells relative to their own individual pivot points by right"\
"-clicking the rotate or scale buttons.",
    7 : "All UV display options are shared under an options window. You will find it under"\
" \"Display\" > \"Settings\" in the menu above the top bar.",
    8 : "The ABC-buttons at the manipulator can be used to store a value. Use left click to"\
" read a value and left click to store. The value is saved between Maya sessions.",
    9 : "Stitch UV's is a powerful sewing tool used for moving, rotating AND scaling UV-shells"\
" before sewing them together.",
    10 : "You can measure the unit or pixel distance between two UV's - or the angle between"\
" then - via the measure tools located in the manipulator. Very handy for making sure you have"\
" enough padding around your shells in order to avoid texture bleeding.",
    11 : "Use the Straighten Shell tool in order to make a shell straight. Useful for things such as pipes.",
    12 : "Use Stack Shells in combination with Match UV's to make sure that several identical"\
" shells gets precisely the same texture coordinates.",
    13 : "You can retrieve a Texel Density value from a face or a selection of several faces"\
" by using \"Get Texel Density\"",
    14 : "You can orient shells so that the edges you've selected run parallell to the U or V"\
" axis. Select some edges on some shells and click \"Orient Edge\".",
    15 : "If you need to override the internal UV set order index you can use the UV Set Order Manager.",
    16 : "You can use Multi-tile (UDIM) when Laying out UV's and performing UV Snapshots. The"\
" snapshots will recieve the prefix _1001 for the first tile, _1002 for the second and so on -"\
" all according to UDIM standards!",
    17 : "You can snap two UV shells together by a selection of UV's on both shells.",
    18 : "Use \"Duplicate UV Set\" in order to quickly make a copy of the active UV set, using"\
" the last know settings used by \"Copy UV Set\".",
    19 : "You can switch between relative and absolute positioning when translating shells by"\
" clicking the x-icon in the middle.",
    20 : "The frames on the side bar can be collapsed - as can the groups on the top bar and bottom bar!",
}


# Get Maya version
mayaVer = pm.optionVar["mayaVer_NSUV"]

# Maya 2015 or earlier? Change to 2015-style icons
if mayaVer <= 201599:
    for k, v in iconDict.iteritems():
        iconDict[k] = iconDict[k][:-4] + "_old.png"

    for k, v in totdImageDict.iteritems():
        totdImageDict[k] = totdImageDict[k][:-4] + "_old.png"


## Texture Window

# Add the texture window and menues to the panel
def addTextureWindow():

    # Get UV editor panel name
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]

    # Vars for the popup menu items
    ctrlShiftMenu = (txtEditor + "ToolOptionsPop")
    shiftMenu = (txtEditor + "popupMenusShift")
    ctrlMenu = (txtEditor + "popupMenusCtl")
    
    # Create Unfold3D context and initialize texSculptCacheContextObj
    if mayaVer >= 201600:
        pm.mel.initUVSculptTool()
    
    # Create the menu bar
    createMenubar(txtEditor)
    
    # Main layout
    txtWinLayout = pm.formLayout()
    
    # Frame layout
    pm.frameLayout(
        "frameToolbar_NSUV",
        borderVisible=False, 
        collapsable=True, 
        collapse=(not pm.optionVar["toolbarState_NSUV"]),
        labelVisible=False, 
        visible=True, 
        )
        
    # Create flowLayout then create toolbar
    txtWinFlow = pm.flowLayout(visible=True)
    createToolbar(txtWinFlow)
    pm.setParent('..') # Set default parent to one step up
    pm.setParent('..') # ...and another step
    
    # Attach the actual textureWindow to the main layout
    pm.textureWindow(
        txtEditor, edit=True, 
            parent=txtWinLayout
        )
        
    # Main popup menu
    txtEditorControl = pm.textureWindow(txtEditor, query=True, control=True)    
    
    # Create popup menu
    pm.popupMenu(
        (txtEditor + "popupMenus"), 
            allowOptionBoxes=True,
            button=3, 
            markingMenu=True, 
            parent=txtEditorControl, 
        )
        
    # Create the marking menu and menubar
    createRadialMenu(txtEditor, 0)
    createRadialMenubar(txtEditor)
    pm.setParent( '..', menu=True ) # Set default parent to one step up
    
    # Shift-modifier popup menu
    if not pm.popupMenu(shiftMenu, exists=True):
        pm.popupMenu(
            shiftMenu, 
                allowOptionBoxes=True,
                button=3, 
                ctrlModifier=False, 
                markingMenu=True, 
                parent=txtEditorControl, 
                postMenuCommand=lambda *args: createRadialContextMenu(shiftMenu),
                shiftModifier=True,
            )        
    pm.setParent( '..', menu=True ) # Set default parent to one step up
    
    # Ctrl-modifier popup menu (used for converting selections to other types)
    pm.popupMenu(
        ctrlMenu, 
            allowOptionBoxes=True,
            button=3, 
            ctrlModifier=True, 
            markingMenu=True, 
            parent=txtEditorControl, 
        )

    # Selection conversion menu
    createRadialConvertMenu(txtEditor)
    pm.setParent( '..', menu=True ) # Set default parent to one step up
    
    # Layout formLayout
    pm.formLayout(
        txtWinLayout, edit=True,
        attachForm=[
            ("frameToolbar_NSUV", "top", 0), 
            ("frameToolbar_NSUV", "right", 0), 
            ("frameToolbar_NSUV", "left", 0), 
            (txtEditor, "top", 0), 
            (txtEditor, "right", 0), 
            (txtEditor, "left", 0)
        ],
        attachControl=(txtEditor, "top", 0, "frameToolbar_NSUV"),
        attachPosition=(txtEditor, "bottom", 0, 100), # Percent, not pixels
    )

    # Ctrl+Shift-modifier popup menu
    if not pm.popupMenu(ctrlShiftMenu, exists=True):    
        pm.popupMenu(
            ctrlShiftMenu,
                allowOptionBoxes=True,
                button=3, 
                ctrlModifier=True, 
                markingMenu=True, 
                parent=txtEditorControl, 
                postMenuCommand=lambda *args: pm.mel.buildToolOptionsMM(ctrlShiftMenu),
                shiftModifier=True,
            )
        
    # Call native MEL-scripts and create optVars
    if pm.mel.exists("performTextureViewGridOptions"): # Grid
        pm.mel.performTextureViewGridOptions(0)
        
    if pm.mel.exists("performTextureViewImageRangeOptions"): # Image range
        pm.mel.performTextureViewImageRangeOptions(0)
        
    if pm.mel.exists("performTextureViewBakeTextureOptions"): # Texture bake
        pm.mel.performTextureViewBakeTextureOptions(0)
      
    # Texture display optVar    
    if pm.optionVar["imgDisp_NSUV"] == 1:
        pm.textureWindow(
            txtEditor, edit=True, 
                viewPortImage=False,
        )
    else:
        pm.textureWindow(
            txtEditor, edit=True, 
                viewPortImage=True,
        )


# Creates a textureWindow
def createTextureWindow():

    # Get UV editor panel name
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]
    pm.textureWindow(txtEditor, unParent=True)


# Remove texture editor window
def removeTextureWindow():

    # Get UV editor panel name
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]
    pm.textureWindow(txtEditor, edit=True, unParent=True)


## Main Window

def createUI():

    # Check for window duplicate
    if pm.window( winMain, exists=True ):
        pm.deleteUI(winMain)

    # Sizeable window check
    if pm.optionVar["sizeableWin_NSUV"] == True:
        sizeVar = False
    else:
        sizeVar = True

    # Main window
    window = pm.window(
        winMain,
        maximizeButton=True,
        minimizeButton=True,
        resizeToFitChildren=True,
        sizeable=sizeVar,
        title=NSUV_title,
        widthHeight=(mainWinX, mainWinY)
    )


    ## Left container

    # Main pane layout
    paneMain = pm.paneLayout(
        configuration="vertical2",
        paneSize=([1, 5, 100], [2, 95, 100]),
        separatorThickness=4,
        staticWidthPane=1
    )

    # formMain = pm.formLayout(height=1)
    formMain = pm.formLayout(parent=paneMain, height=1)

    ## FRAME 1: Manipulator
    frame1 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame1_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(1, True),
        expandCommand=lambda *args: core.updateFrame(1, False),
        label="Manipulator",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form1 = pm.formLayout()

    # Scale
    btn1frame1 = pm.iconTextButton(
        annotation="Scale the Selected UVs (Left Click) --- Scale the Selected Shells Relatively (Right Click)",
        command=lambda *args: core.scaleUVs("UV"),
        commandRepeatable=True,
        image1=iconDict["scaleUV"],
        label="Scale the Selected UVs (Left Click) --- Scale the Selected Shells Relatively (Right Click)",
    )
    btn1frame1Pop = pm.popupMenu(
        button=3,
        parent=btn1frame1,
        postMenuCommand=lambda *args: core.scaleUVs("UV", True),
    )
    btn2frame1 = pm.iconTextButton(
        annotation="Scale the Selected UVs Along U Only (Left Click) --- Scale the Selected Shells Relatively Along U Only (Right Click)",
        command=lambda *args: core.scaleUVs("U"),
        commandRepeatable=True,
        image1=iconDict["scaleU"],
        label="Scale the Selected UVs Along U Only (Left Click) --- Scale the Selected Shells Relatively Along U Only (Right Click)",
    )
    btn2frame1Pop = pm.popupMenu(
        button=3,
        parent=btn2frame1,
        postMenuCommand=lambda *args: core.scaleUVs("U", True),
    )

    btn3frame1 = pm.iconTextButton(
        annotation="Scale the Selected UVs Along V Only (Left Click) --- Scale the Selected Shells Relatively Along V Only (Right Click)",
        command=lambda *args: core.scaleUVs("V"),
        commandRepeatable=True,
        image1=iconDict["scaleV"], 
        label="Scale the Selected UVs Along V Only (Left Click) --- Scale the Selected Shells Relatively Along V Only (Right Click)",
    )
    btn3frame1Pop = pm.popupMenu(
        button=3,
        parent=btn3frame1,
        postMenuCommand=lambda *args: core.scaleUVs("V", True),
    )

    # Flip
    btn4frame1 = pm.iconTextButton(
        annotation="Flip the Selected UVs Along U (Left Click) - Flip the Selected UVs Along V (Right Click)",
        command=lambda *args: core.flipUVs("U"),
        commandRepeatable=True,
        image1=iconDict["flip"],
        label="Flip the Selected UVs Along U (Left Click) - Flip the Selected UVs Along V (Right Click)"
    )
    btn4frame1Pop = pm.popupMenu(
        button=3,
        parent=btn4frame1,
        postMenuCommand=lambda *args: core.flipUVs("V"),
    )

    # Rotate
    btn5frame1 = pm.iconTextButton(
        annotation="Rotate the Selected UVs 90 Degrees CCW (Left Click) - Rotate the Selected Shells Relatively 90 Degrees CCW (Right Click)",
        command=lambda *args: core.rotateUVs("90"),
        commandRepeatable=True,
        image1=iconDict["rotate90CCW"],
        label="Rotate the Selected UVs 90 Degrees CCW (Left Click) - Rotate the Selected Shells Relatively 90 Degrees CCW (Right Click)",
    )
    btn5frame1Pop = pm.popupMenu(
        button=3,
        parent=btn5frame1,
        postMenuCommand=lambda *args: core.rotateUVs("90", True),
    )
    btn6frame1 = pm.iconTextButton(
        annotation="Rotate the Selected UVs 90 Degrees CW (Left Click) - Rotate the Selected Shells Relatively 90 Degrees CW (Right Click)",
        command=lambda *args: core.rotateUVs("-90"),
        commandRepeatable=True,
        image1=iconDict["rotate90CW"],
        label="Rotate the Selected UVs 90 Degrees CW (Left Click) - Rotate the Selected Shells Relatively 90 Degrees CW (Right Click)",
    )
    btn6frame1Pop = pm.popupMenu(
        button=3,
        parent=btn6frame1,
        postMenuCommand=lambda *args: core.rotateUVs("-90", True),
    )
    btn7frame1 = pm.iconTextButton(
        annotation="Rotate the Selected UVs CCW (Left Click) - Rotate the Selected Shells Relatively CCW (Right Click)",
        command=lambda *args: core.rotateUVs("CCW"),
        commandRepeatable=True,
        image1=iconDict["rotateCCW"],
        label="Rotate the Selected UVs CCW (Left Click) - Rotate the Selected Shells Relatively CCW (Right Click) ",
    )
    btn7frame1Pop = pm.popupMenu(
        button=3,
        parent=btn7frame1,
        postMenuCommand=lambda *args: core.rotateUVs("CCW", True),
    )
    btn8frame1 = pm.iconTextButton(
        annotation="Rotate the Selected UVs CW (Left Click) - Rotate the Selected Shells Relatively CW (Right Click)",
        command=lambda *args: core.rotateUVs("CW"),
        commandRepeatable=True,
        image1=iconDict["rotateCW"],
        label="Rotate the Selected UVs CW (Left Click) - Rotate the Selected Shells Relatively CW (Right Click)",
    )
    btn8frame1Pop = pm.popupMenu(
        button=3,
        parent=btn8frame1,
        postMenuCommand=lambda *args: core.rotateUVs("CW", True),
    )

    # Translate
    btnMoveUpLeft = pm.iconTextButton(
        annotation="Move the Selected UVs Up and to the Left",
        command=lambda *args: core.translateUVs("upLeft"),
        commandRepeatable=True,
        image1=iconDict["moveUpLeft"],
        label="Move the Selected UVs Up and to the Left"
    )
    btnMoveUp = pm.iconTextButton(
        annotation="Move the Selected UVs Up",
        command=lambda *args: core.translateUVs("up"),
        commandRepeatable=True,
        image1=iconDict["moveUp"],
        label="Move the Selected UVs Up"
    )
    btnMoveUpRight = pm.iconTextButton(
        annotation="Move the Selected UVs Up and to the Right",
        command=lambda *args: core.translateUVs("upRight"),
        commandRepeatable=True,
        image1=iconDict["moveUpRight"],
        label="Move the Selected UVs up and to the right"
    )
    btnMoveDownLeft = pm.iconTextButton(
        annotation="Move the Selected UVs Down and to the Left",
        command=lambda *args: core.translateUVs("downLeft"),
        commandRepeatable=True,
        image1=iconDict["moveDownLeft"],
        label="Move the Selected UVs Down and to the Left"
    )
    btnMoveDown = pm.iconTextButton(
        annotation="Move the Selected UVs Down",
        command=lambda *args: core.translateUVs("down"),
        commandRepeatable=True,
        image1=iconDict["moveDown"],
        label="Move the Selected UVs Down"
    )
    btnMoveDownRight = pm.iconTextButton(
        annotation="Move the Selected UVs Down and to the Right",
        command=lambda *args: core.translateUVs("downRight"),
        commandRepeatable=True,
        image1=iconDict["moveDownRight"],
        label="Move the Selected UVs Down and to the Right",
    )
    btnMoveRight = pm.iconTextButton(
        annotation="Move the Selected UVs to the Right",
        command=lambda *args: core.translateUVs("right"),
        commandRepeatable=True,
        image1=iconDict["moveRight"],
        label="Move the Selected UVs to the Right",
    )
    btnMoveLeft = pm.iconTextButton(
        annotation="Move the Selected UVs to the Left",
        command=lambda *args: core.translateUVs("left"),
        commandRepeatable=True,
        image1=iconDict["moveLeft"],
        label="Move the Selected UVs to the Left",
    )
    btnAbsolute = pm.iconTextCheckBox(
        annotation="Toggle Between Absolute and Relative Translation",
        disabledImage=iconDict["absRelOff"],
        image=iconDict["absRelOff"],
        label="Toggle Between Absolute and Relative Translation",
        offCommand=lambda *args: core.absToggle(False),
        onCommand=lambda *args: core.absToggle(True),
        selectionImage=iconDict["absRelOn"],
        value=pm.optionVar["absToggle_NSUV"],
    )

    # Pivot cycling
    btn9frame1 = pm.iconTextButton(
        annotation="Cycle the Pivot Through the Corners of the UV Range or the Current Selection Bounds --- Options (Right Click and Hold)",
        command=lambda *args: core.pivotCycle(0, 0),
        commandRepeatable=True,
        image1=iconDict["cycleUV1"],
        label="Cycle the Pivot Through the Corners of the UV Range or the Current Selection Bounds --- Options (Right Click and Hold)",
        visible=True,
    )
    btn9frame1Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn9frame1,
        postMenuCommand=lambda *args: createPopupCyclePivot(btn9frame1Pop, btn9frame1)
    )

    # Text field
    fieldManip = pm.floatField(
        annotation="Enter Manipulation Value",
        changeCommand=lambda *args: core.manipField(fieldManip, "get"),
        editable=True,
        precision=4,
        value=pm.optionVar["manipAmt_NSUV"],
        width=56
    )

    # Field value buttons
    btn10frame1 = pm.iconTextButton(
        annotation="Reset the Manipulation Field To 0* (Left Click) --- *1 (Right Click)",
        command=lambda *args: core.manipField(fieldManip, 0),
        commandRepeatable=True,
        image1=iconDict["reset"],
        label="Reset the Manipulation Field To 0* (Left Click) --- *1 (Right Click)",
    )
    btn10frame1Pop = pm.popupMenu(
        button=3,
        parent=btn10frame1,
        postMenuCommand=lambda *args: core.manipField(fieldManip, 1)
    )
    
    # Calculate UV or pixel distance, or angle between two UV's (arctangent calculation)
    btn11frame1 = pm.iconTextButton(
        annotation="Calculate Distance or Angle Between Two Selected UVs --- Options (Right Click and Hold)",
        command=lambda *args: core.manipField(fieldManip, "distU"),
        commandRepeatable=True,
        image1=iconDict["distU"],
        label="Calculate Distance or Angle Between Two Selected UVs --- Options (Right Click and Hold)",
        visible=True,
    )
    btn11frame1Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn11frame1,
        postMenuCommand=lambda *args: createPopupCalculate(btn11frame1Pop, btn11frame1, fieldManip)
    )
    
    # Field value variables
    btn12frame1 = pm.iconTextButton(
        annotation="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        command=lambda *args: core.manipField(fieldManip, "getA"),
        commandRepeatable=True,
        image1=iconDict["manipVarA"],
        label="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        visible=True,
    )
    btn12frame1Pop = pm.popupMenu(
        button=3,
        parent=btn12frame1,
        postMenuCommand=lambda *args: core.manipField(fieldManip, "setA")
    )
    btn13frame1 = pm.iconTextButton(
        annotation="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        command=lambda *args: core.manipField( fieldManip, "getB" ),
        commandRepeatable=True,
        image1=iconDict["manipVarB"],
        label="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        visible=True,
    )
    btn13frame1Pop = pm.popupMenu(
        button=3,
        parent=btn13frame1,
        postMenuCommand=lambda *args: core.manipField(fieldManip, "setB")
    )
    btn14frame1 = pm.iconTextButton(
        annotation="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        command=lambda *args: core.manipField( fieldManip, "getC" ),
        commandRepeatable=True,
        image1=iconDict["manipVarC"],
        label="Load* Value to the Manipulation Field (Left Click) --- *Save Value from (Right Click)",
        )
    btn14frame1Pop = pm.popupMenu(
        button=3,
        parent=btn14frame1,
        postMenuCommand=lambda *args: core.manipField(fieldManip, "setC")
    )
    btn15frame1 = pm.iconTextButton(
        annotation="Multiply* the Manipulation Value By Two (Left Click) --- *Divide (Right Click)",
        command=lambda *args: core.manipField( fieldManip, "double" ),
        commandRepeatable=True,
        image1=iconDict["double"],
        label="Multiply* the Manipulation Value By Two (Left Click) --- *Divide (Right Click)",
        visible=True,
    )
    btn15frame1Pop = pm.popupMenu(
        button=3,
        parent=btn15frame1,
        postMenuCommand=lambda *args: core.manipField(fieldManip, "split")
    )

    # Comp space checkbox
    sep2 = pm.separator(
        height=1,
        horizontal=True,
        style="in",
        width=121
    )
    cBoxCSpace = pm.checkBox(
        align="left",
        annotation="Retain Component Spacing of UVs and Shells",
        label="Ret. Comp. Space",
        offCommand=lambda *args: core.compSpaceToggle(cBoxCSpace, 0),
        onCommand=lambda *args: core.compSpaceToggle(cBoxCSpace, 1),
        value=pm.optionVar["compSpace_NSUV"]
    )

    # Layout the elements in the formLayout
    pm.formLayout(
        form1, edit=True,
        attachForm=[
            (btn1frame1, "top", sBarT ),
            (btn1frame1, "left", sBarL ),
            (btn2frame1, "top", sBarT ),
            (btn3frame1, "top", sBarT ),
            (btn4frame1, "top", sBarT ),

            (btn5frame1, "left", sBarL),

            (btn7frame1, "left", sBarL),

            (btn9frame1, "left", sBarL),

            (btn11frame1, "left", sBarL),

            (sep2, "left", 0),
            (cBoxCSpace, "left", sBarH),
            (cBoxCSpace, "bottom", sBarB),
        ],
        attachControl=[
            (btn2frame1, "left", sBarH, btn1frame1),
            (btn3frame1, "left", sBarH, btn2frame1),
            (btn4frame1, "left", sBarH, btn3frame1),

            (btn5frame1, "top", sBarT, btn1frame1),

            (btn6frame1, "top", sBarT, btn3frame1),
            (btn6frame1, "left", sBarH, btnMoveUpRight),
            (btn7frame1, "top", sBarT, btn5frame1),
            (btn8frame1, "top", sBarT, btn6frame1),
            (btn8frame1, "left", sBarH, btnMoveDownRight),

            (btnMoveUpLeft, "top", 0, btn3frame1),
            (btnMoveUpLeft, "left", sBarH, btn5frame1),
            (btnMoveUp, "top", 0, btn3frame1),
            (btnMoveUp, "left", 0, btnMoveUpLeft),
            (btnMoveUpRight, "top", 0, btn2frame1),
            (btnMoveUpRight, "left", 0, btnMoveUp),
            (btnMoveLeft, "top", 0, btnMoveUp),
            (btnMoveLeft, "left", sBarH, btn7frame1),
            (btnAbsolute, "top", 0, btnMoveUp),
            (btnAbsolute, "left", 0, btnMoveLeft),
            (btnMoveRight, "top", 0, btnMoveUp),
            (btnMoveRight, "left", 0, btnAbsolute),
            (btnMoveDownLeft, "top", 0, btnAbsolute),
            (btnMoveDownLeft, "left", sBarH, btn5frame1),
            (btnMoveDown, "top", 0, btnAbsolute),
            (btnMoveDown, "left", 0, btnMoveDownLeft),
            (btnMoveDownRight, "top", 0, btnAbsolute),
            (btnMoveDownRight, "left", 0, btnMoveDown),

            (btn9frame1, "top", sBarT, btn7frame1),
            (fieldManip, "top", gapA, btnMoveDown),
            (fieldManip, "left", sBarH, btn9frame1),
            (btn10frame1, "top", 0, btn8frame1),
            (btn10frame1, "left", gapA, fieldManip),

            (btn11frame1, "top", 0, btn9frame1),
            (btn12frame1, "top", sBarH, fieldManip),
            (btn12frame1, "left", sBarL, btn11frame1),
            (btn13frame1, "top", sBarH, fieldManip),
            (btn13frame1, "left", sBarL, btn12frame1),
            (btn14frame1, "top", sBarH, fieldManip),
            (btn14frame1, "left", sBarL, btn13frame1),
            (btn15frame1, "top", 0, btn10frame1),
            (btn15frame1, "left", sBarL, btn14frame1),

            (sep2, "top", sBarT, btn15frame1),
            (cBoxCSpace, "top", sBarT, sep2),
        ]
    )


    ## FRAME 2: UV mapping
    frame2 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame2_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(2, True),
        expandCommand=lambda *args: core.updateFrame(2, False),
        label="Project UVs",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form2 = pm.formLayout()

    btn1frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) Using Automatic Mapping (Left Click) --- Automatic Mapping Using Last Known Options (Right Click)",
        command=lambda *args: core.mapping("auto"),
        commandRepeatable=True,
        image1=iconDict["projAuto"],
        label="Project the Selected Mesh(es) or Face(es) Using Automatic Mapping (Left Click) --- Automatic Mapping Using Last Known Options (Right Click)",
    )    
    btn1frame2Pop = pm.popupMenu(
        button=3,
        parent=btn1frame2,
        postMenuCommand=lambda *args: mapAutoUI(),
    )
    btn2frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) using Cylindrical Mapping (Left Click) --- Cylindrical Mapping Using Last Known Options (Right Click)",
        command=lambda *args: core.mapping("cyl"),
        commandRepeatable=True,
        image1=iconDict["projCyl"],
        label="Project the Selected Mesh(es) or Face(es) using Cylindrical Mapping (Left Click) --- Cylindrical Mapping Using Last Known Options (Right Click)",
    )
    btn2frame2Pop = pm.popupMenu(
        button=3,
        parent=btn2frame2,
        postMenuCommand=lambda *args: mapCylindricalUI(),
    )
    btn3frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) using Planar Mapping --- Options (Right Click and Hold)",
        command=lambda *args: core.mapping("plane"),
        image1=iconDict["projPlane"],
        label="Project the Selected Mesh(es) or Face(es) using Planar Mapping --- Options (Right Click and Hold)",
    )
    btn3frame2Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn3frame2,
        postMenuCommand=lambda *args: createPopupPlanarMap(btn3frame2Pop)
        )
    btn4frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) using Spherical Mapping (Left Click) --- Spherical Mapping Using Last Known Options (Right Click)",
        command=lambda *args: core.mapping("sphere"),
        commandRepeatable=True,
        image1=iconDict["projSphere"],
        label="Project the Selected Mesh(es) or Face(es) using Spherical Mapping (Left Click) --- Spherical Mapping Using Last Known Options (Right Click)",
    )
    btn4frame2Pop = pm.popupMenu(
        button=3,
        parent=btn4frame2,
        postMenuCommand=lambda *args: mapSphericalUI(),
    )
    btn5frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) using Planar Mapping: From Camera (Left Click) --- Planar Mapping Using Last Known Options (Right Click)",
        command=lambda *args: core.mapping("plane", "c"),
        commandRepeatable=True,
        image1=iconDict["projCam"],
        label="Project the Selected Mesh(es) or Face(es) using Planar Mapping: From Camera (Left Click) --- Planar Mapping Using Last Known Options (Right Click)",
    )
    btn5frame2Pop = pm.popupMenu(
        button=3,
        parent=btn5frame2,
        postMenuCommand=lambda *args: mapPlanarUI("cam"),
    )
    btn6frame2 = pm.iconTextButton(
        annotation="Project the Selected Mesh(es) or Face(es) using Normal-Based Mapping (Left Click) --- Normal-Based Mapping Using Last Known Options (Right Click)",
        command=lambda *args: core.mapping("normal"),
        commandRepeatable=True,
        image1=iconDict["projNormal"],
        label="Project the Selected Mesh(es) or Face(es) using Normal-Based Mapping (Left Click) --- Normal-Based Mapping Using Last Known Options (Right Click)",
    )
    btn6frame2Pop = pm.popupMenu(
        button=3,
        parent=btn6frame2,
        postMenuCommand=lambda *args: mapNormalUI(),
    )    
    if mayaVer >= 201600:
        btn7frame2 = pm.iconTextButton(
            annotation="Project the Selected Mesh(es) or Face(es) using Contour Stretch Mapping (Left Click) --- Contour Stretch Mapping Using Last Known Options (Right Click)",
            command=lambda *args: core.mapping("contour"),
            commandRepeatable=True,
            image1=iconDict["projContour"],
            label="Project the Selected Mesh(es) or Face(es) using Contour Stretch Mapping (Left Click) --- Contour Stretch Mapping Using Last Known Options (Right Click)",
        )
        btn7frame2Pop = pm.popupMenu(
            button=3,
            parent=btn7frame2,
            postMenuCommand=lambda *args: pm.mel.ContourProjectionOptions(),
        )
    btn8frame2 = pm.iconTextButton(
        annotation="Find and Select Unmapped Faces on the Selection (Left Click) --- Quick Automatic Mapping Projection Using Last Known Options (Right Click)",
        command=lambda *args: core.selectUnmapped(),
        commandRepeatable=True,
        image1=iconDict["projFind"],
        label="Find and Select Unmapped Faces on the Selection (Left Click) --- Quick Automatic Mapping Projection Using Last Known Options (Right Click)",
    )
    btn8frame2Pop = pm.popupMenu(
        button=3,
        parent=btn8frame2,
        postMenuCommand=lambda *args: core.mapping("auto")
    )

    # Layout the elements in the formLayout
    if mayaVer >= 201600:
        pm.formLayout(
            form2, edit=True,
            attachForm=[
                (btn1frame2, "top", sBarT),
                (btn1frame2, "left", sBarL),
                (btn2frame2, "top", sBarT),
                (btn3frame2, "top", sBarT),
                (btn4frame2, "top", sBarT),

                (btn5frame2, "left", sBarL),
                (btn5frame2, "bottom", sBarB),
            ],
            attachControl=[
                (btn2frame2, "left", sBarH, btn1frame2),
                (btn3frame2, "left", sBarH, btn2frame2),
                (btn4frame2, "left", sBarH, btn3frame2),

                (btn5frame2, "top", sBarT, btn1frame2),
                (btn6frame2, "top", sBarT, btn2frame2),
                (btn6frame2, "left", sBarH, btn5frame2),
                (btn7frame2, "top", sBarT, btn4frame2),
                (btn7frame2, "left", sBarH, btn6frame2),
                (btn8frame2, "top", sBarT, btn4frame2),
                (btn8frame2, "left", sBarH, btn7frame2),
            ]
        )
    else:
        pm.formLayout(
            form2, edit=True,
            attachForm=[
                (btn1frame2, "top", sBarT),
                (btn1frame2, "left", sBarL),
                (btn2frame2, "top", sBarT),
                (btn3frame2, "top", sBarT),
                (btn4frame2, "top", sBarT),

                (btn5frame2, "left", sBarL+sBarB),
                (btn5frame2, "bottom", sBarB),
            ],
            attachControl=[
                (btn2frame2, "left", sBarH, btn1frame2),
                (btn3frame2, "left", sBarH, btn2frame2),
                (btn4frame2, "left", sBarH, btn3frame2),

                (btn5frame2, "top", sBarT, btn1frame2),
                (btn6frame2, "top", sBarT, btn2frame2),
                (btn6frame2, "left", sBarH+sBarB, btn5frame2),
                (btn8frame2, "top", sBarT, btn3frame2),
                (btn8frame2, "left", sBarH+sBarB, btn6frame2),
            ]
        )


    ## FRAME 3: Cut/Sew
    frame3 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame3_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(3, True),
        expandCommand=lambda *args: core.updateFrame(3, False),
        label="Cut/Sew",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form3 = pm.formLayout()

    ## Tools added in Maya 2016
    if mayaVer >= 201600:
        btn1frame3 = pm.iconTextButton(
            annotation="Cut UV Tool",
            ## command=lambda *args: core.cutSewTool(0),
            command=lambda *args: core.uvContextTool(6, "cut"),
            commandRepeatable=True,
            image1=iconDict["cutTool"],
            label="Cut UV Tool",
        )
        btn1frame3Pop = pm.popupMenu(
            button=3,
            parent=btn1frame3,
            postMenuCommand=lambda *args: core.uvContextTool(6, "cut", True),
        )
        btn5frame3 = pm.iconTextButton(
            annotation="Sew UV Tool",
            command=lambda *args: core.uvContextTool(6, "sew"),
            commandRepeatable=True,
            image1=iconDict["sewTool"],
            label="Sew UV Tool",
        )
        btn5frame3Pop = pm.popupMenu(
            button=3,
            parent=btn5frame3,
            postMenuCommand=lambda *args: core.uvContextTool(6, "sew", True),
        )
    
    # Standard cut/sew utilities
    btn2frame3 = pm.iconTextButton(
        annotation="Cut the Selected Edge(s) or UV(s)",
        command=lambda *args: core.cutSewUVs("cut"),
        commandRepeatable=True,
        image1=iconDict["cut"],
        label="Cut the Selected Edge(s) or UV(s)",
    )
    btn3frame3 = pm.iconTextButton(
        annotation="Split the Selected UV(s)",
        command=lambda *args: core.cutSewUVs("split"),
        commandRepeatable=True,
        image1=iconDict["split"],
        label="Split the Selected UV()s)",
    )
    btn4frame3 = pm.iconTextButton(
        annotation="Tear Off the Selected Faces and Create a New UV shell",
        command=lambda *args: core.createShell(),
        commandRepeatable=True,
        image1=iconDict["createShell"],
        label="Tear Off the Selected Faces and Create a New UV shell",
    ) 
    btn6frame3 = pm.iconTextButton(
        annotation="Sew Together the Selected Edge(s) or UV(s)",
        command=lambda *args: core.cutSewUVs("sew"),
        commandRepeatable=True,
        image1=iconDict["sew"],
        label="Sew Together the Selected Edge(s) or UV(s)",
    )
    btn7frame3 = pm.iconTextButton(
        annotation="Move and Sew Together the Selected Edge(s) or UV(s)",
        command=lambda *args: core.cutSewUVs("moveSew"),
        commandRepeatable=True,
        image1=iconDict["moveSew"],
        label="Move and Sew Together the Selected Edge(s) or UV(s)",
    )
    btn8frame3 = pm.iconTextButton(
        annotation="Stitch Together the Selected Edge/UV Pair, A to B* (Left Click) --- *B to A (Right Click) ",
        command=lambda *args: core.stitchTogether(0),
        commandRepeatable=True,
        image1=iconDict["stitch"],
        label="Stitch Together the Selected Edge/UV pair"
    )
    btn8frame3Pop = pm.popupMenu(
        button=3,
        parent=btn8frame3,
        postMenuCommand=lambda *args: core.stitchTogether(1),
    )

    # Layout the elements in the formLayout
    if mayaVer >= 201600:
        pm.formLayout(
            form3, edit=True,
            attachForm=[
                (btn1frame3, "top", sBarT),
                (btn1frame3, "left", sBarL),
                (btn2frame3, "top", sBarT),
                (btn3frame3, "top", sBarT),
                (btn4frame3, "top", sBarT),

                (btn5frame3, "left", sBarL),
                (btn5frame3, "bottom", sBarB),
            ],
            attachControl=[
                (btn2frame3, "left", sBarH, btn1frame3),
                (btn3frame3, "left", sBarH, btn2frame3),
                (btn4frame3, "left", sBarH, btn3frame3),

                (btn5frame3, "top", sBarT, btn1frame3),
                (btn6frame3, "top", sBarT, btn2frame3),
                (btn6frame3, "left", sBarH, btn5frame3),
                (btn7frame3, "top", sBarT, btn3frame3),
                (btn7frame3, "left", sBarH, btn6frame3),
                (btn8frame3, "top", sBarT, btn4frame3),                
                (btn8frame3, "left", sBarH, btn7frame3),
            ]
        )
    else:
        pm.formLayout(
            form3, edit=True,
            attachForm=[
                (btn2frame3, "top", sBarT),
                (btn2frame3, "left", sBarT+sBarB),
                (btn3frame3, "top", sBarT),
                (btn4frame3, "top", sBarT),

                (btn6frame3, "left", sBarL+sBarB),
                (btn6frame3, "bottom", sBarB),
            ],
            attachControl=[
                (btn3frame3, "left", sBarH+sBarB, btn2frame3),
                (btn4frame3, "left", sBarH+sBarB, btn3frame3),

                (btn6frame3, "top", sBarT, btn2frame3),
                (btn7frame3, "top", sBarT, btn3frame3),
                (btn7frame3, "left", sBarT+sBarB, btn6frame3),
                (btn8frame3, "top", sBarT, btn4frame3),                
                (btn8frame3, "left", sBarH+sBarB, btn7frame3),
            ]
        )


    ## FRAME 4: Unfold
    frame4 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame4_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(4, True),
        expandCommand=lambda *args: core.updateFrame(4, False),
        label="Unfold",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form4 = pm.formLayout()

    ## Tools added in Maya 2016
    if mayaVer >= 201600:
        btn1frame4 = pm.iconTextButton(
            annotation="Unfold UV Tool",
            command=lambda *args: core.uvContextTool(5, "unfold"),
            commandRepeatable=True,
            image1=iconDict["unfoldTool"],
            label="Unfold UV Tool",
        )
        btn1frame4Pop = pm.popupMenu(
            button=3,
            parent=btn1frame4,
            postMenuCommand=lambda *args: core.uvContextTool(5, "unfold", True),
        )
        btn5frame4 = pm.iconTextButton(
            annotation="Optimize UV Tool",
            command=lambda *args: core.uvContextTool(5, "optimize"),
            commandRepeatable=True,
            image1=iconDict["optimizeTool"],
            label="Optimize UV Tool"
        )
        btn5frame4Pop = pm.popupMenu(
            button=3,
            parent=btn5frame4,
            postMenuCommand=lambda *args: core.uvContextTool(5, "optimize", True),
        )

    # Standard unfold utilities
    btn2frame4 = pm.iconTextButton(
        annotation="Unfold the Selected UVs (Left Click) --- Unfold Using Last Known Options (Right Click)",
        command=lambda *args: core.unfoldUVs(),
        commandRepeatable=True,
        image1=iconDict["unfold"],
        label="Unfold the Selected UVs (Left Click) --- Unfold Using Last Known Options (Right Click)",
    )
    btn2frame4Pop = pm.popupMenu(
        button=3,
        parent=btn2frame4,
        postMenuCommand=lambda *args: unfoldUI(),
    )
    btn3frame4 = pm.iconTextButton(
        annotation="Unfold the Selected UVs Along U* Only (Left Click) --- *V (Right Click)",
        command=lambda *args: core.unfoldUVs("U"),
        commandRepeatable=True,
        image1=iconDict["unfoldU"],
        label="Unfold the Selected UVs Along U* Only (Left Click) --- *V (Right Click)",
    )
    btn3frame4Pop = pm.popupMenu(
        button=3,
        parent=btn3frame4,
        postMenuCommand=lambda *args: core.unfoldUVs("V"),
    )
    btn4frame4 = pm.iconTextButton(
        annotation="Smooth UV Tool",
        command=lambda *args: core.uvContextTool(3, "smooth"),
        commandRepeatable=True,
        image1=iconDict["smoothTool"],
        label="Smooth UV Tool"
    )
    btn4frame4Pop = pm.popupMenu(
        button=3,
        parent=btn4frame4,
        postMenuCommand=lambda *args: core.uvContextTool(3, "smooth", True),
    )    
    btn6frame4 = pm.iconTextButton(
        annotation="Relax/Optimize the Selected UVs (Left Click) --- Relax/Optimize Using Last Known Options (Right Click)",
        command=lambda *args: core.relaxUVs(),
        commandRepeatable=True,
        image1=iconDict["optimize"],
        label="Relax/Optimize the Selected UVs (Left Click) --- Relax/Optimize Using Last Known Options (Right Click)",
    )
    btn6frame4Pop = pm.popupMenu(
        button=3,
        parent=btn6frame4,
        postMenuCommand=lambda *args: relaxUI(),
    )     
    btn7frame4 = pm.iconTextButton(
        annotation="Straighten the Selected Loop/Ring and Unfold the UV shell",
        command=lambda *args: core.strShell(),
        commandRepeatable=True,
        image1=iconDict["strShell"],
        label="Straighten the Selected Loop/Ring and Unfold the UV shell"
    )
    btn8frame4 = pm.iconTextButton(
        annotation="Straighten the Selected UVs (Left Click) --- Straighten UVs Using Last Known Options (Right Click)",
        command=lambda *args: core.strUVs(),
        commandRepeatable=True,
        image1=iconDict["strSel"],
        label="Straighten the Selected UVs (Left Click) --- Straighten UVs Using Last Known Options (Right Click)",
    )
    btn8frame4Pop = pm.popupMenu(
        button=3,
        parent=btn8frame4,
        postMenuCommand=lambda *args: strUVsUI(),
    )  

    # Layout the elements in the formLayout
    if mayaVer >= 201600:
        pm.formLayout(
            form4, edit=True,
            attachForm=[
                (btn1frame4, "top", sBarT),
                (btn1frame4, "left", sBarL),
                (btn2frame4, "top", sBarT),
                (btn3frame4, "top", sBarT),
                (btn4frame4, "top", sBarT),

                (btn5frame4, "left", sBarL),
                (btn5frame4, "bottom", sBarB),
            ],
            attachControl=[
                (btn2frame4, "left", sBarH, btn1frame4),
                (btn3frame4, "left", sBarH, btn2frame4),
                (btn4frame4, "left", sBarH, btn3frame4),

                (btn5frame4, "top", sBarT, btn1frame4),
                (btn6frame4, "top", sBarT, btn2frame4),
                (btn6frame4, "left", sBarH, btn5frame4),
                (btn7frame4, "top", sBarT, btn3frame4),
                (btn7frame4, "left", sBarH, btn6frame4),
                (btn8frame4, "top", sBarT, btn4frame4),                
                (btn8frame4, "left", sBarH, btn7frame4),
            ]
        )
    else:
        pm.formLayout(
            form4, edit=True,
            attachForm=[
                (btn2frame4, "top", sBarT),
                (btn2frame4, "left", sBarT+sBarB),
                (btn3frame4, "top", sBarT),
                (btn4frame4, "top", sBarT),

                (btn6frame4, "left", sBarL+sBarB),
                (btn6frame4, "bottom", sBarB),
            ],
            attachControl=[
                (btn3frame4, "left", sBarH+sBarB, btn2frame4),
                (btn4frame4, "left", sBarH+sBarB, btn3frame4),

                (btn6frame4, "top", sBarT, btn2frame4),
                (btn7frame4, "top", sBarT, btn3frame4),
                (btn7frame4, "left", sBarT+sBarB, btn6frame4),
                (btn8frame4, "top", sBarT, btn4frame4),                
                (btn8frame4, "left", sBarH+sBarB, btn7frame4),
            ]
        )


    ## FRAME 5: Arrange
    frame5 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame5_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(5, True),
        expandCommand=lambda *args: core.updateFrame(5, False),
        label="Arrange",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form5 = pm.formLayout()

    # Child elements
    btn1frame5 = pm.iconTextButton(
        annotation="Orient the Selected UV Shell(s)",
        command=lambda *args: core.orientShells(),
        commandRepeatable=True,
        image1=iconDict["orient"],
        label="Orient the Selected UV Shell(s)",
    )
    btn2frame5 = pm.iconTextButton(
        annotation="Layout the Selected UV Shells (Left Click) --- Layout UVs Using Last Known Options (Right Click)",
        command=lambda *args: core.layoutUVs(),
        commandRepeatable=True,
        image1=iconDict["layout"],
        label="Layout the Selected UV Shells (Left Click) --- Layout UVs Using Last Known Options (Right Click)",
    )
    btn2frame5Pop = pm.popupMenu(
        button=3,
        parent=btn2frame5,
        postMenuCommand=lambda *args: layoutUI(),
    )
    btn3frame5 = pm.iconTextButton(
        annotation="Stack the Selected UV Shells (Left Click) --- Stack and Rotate the Selected UV Shells (Right Click)",
        command=lambda *args: core.stackShells(),
        commandRepeatable=True,
        image1=iconDict["stack"],
        label="Stack the Selected UV Shells (Left Click) --- Stack and Rotate the Selected UV Shells (Right Click)",
    )
    btn3frame5Pop = pm.popupMenu(
        button=3,
        parent=btn3frame5,
        postMenuCommand=lambda *args: core.smartStack(),
    )
    btn4frame5 = pm.iconTextButton(
        annotation="Distribute the Selected Shells (Left Click) --- Distribute Shells Using Last Known Options (Right Click)",
        command=lambda *args: core.distributeShells(),
        commandRepeatable=True,
        image1=iconDict["distribute"],
        label="Distribute the Selected Shells (Left Click) --- Distribute Shells Using Last Known Options (Right Click)",
    )
    btn4frame5Pop = pm.popupMenu(
        button=3,
        parent=btn4frame5,
        postMenuCommand=lambda *args: distributeUI(),
    )
    btn5frame5 = pm.iconTextButton(
        annotation="Orient Shells to the Selected Edge(s)",
        command=lambda *args: core.orientEdge(),
        commandRepeatable=True,
        image1=iconDict["orientEdge"],
        label="Orient Shells to the Selected Edge(s)"
    )   
    btn6frame5 = pm.iconTextButton(
        annotation="Randomize the Selected UV Shells (Left Click) --- Randomize UVs Using Last Known Options (Right Click)",
        command=lambda *args: core.randomizeShells(),
        commandRepeatable=True,
        image1=iconDict["randomize"],
        label="Randomize the Selected UV Shells"
    )
    btn6frame5Pop = pm.popupMenu(
        button=3,
        parent=btn6frame5,
        postMenuCommand=lambda *args: randomizeUI(),

    )
    btn7frame5 = pm.iconTextButton(
        annotation="Spread Out and Bring all UV Shells Together",
        command=lambda *args: core.spreadOutShells(),
        commandRepeatable=True,
        image1=iconDict["spreadOut"],
        label="Spread Out and Bring all UV Shells Together"
    )
    btn8frame5 = pm.iconTextButton(
        annotation="Gather Shells: Offset Shells Back to the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.gatherShells(),
        commandRepeatable=True,
        image1=iconDict["gather"],
        label="Gather Shells: Offset Shells Back to the Default UV Range (0.0 -> 1.0)"
    )
    """
    btn8frame5Pop = pm.popupMenu( ##: NOTE - future feature: need "offset stacked UV shells"
        button=3,
        parent=btn8frame5,
        postMenuCommand=lambda *args: mapNormalUI()
    )"""

    # Layout the elements in the formLayout
    pm.formLayout(
        form5, edit=True,
        attachForm=[
            (btn1frame5, "top", sBarT),
            (btn1frame5, "left", sBarL),
            (btn2frame5, "top", sBarT),
            (btn3frame5, "top", sBarT),
            (btn4frame5, "top", sBarT),

            (btn5frame5, "left", sBarL),
            (btn5frame5, "bottom", sBarB),
        ],
        attachControl=[
            (btn2frame5, "left", sBarH, btn1frame5),
            (btn3frame5, "left", sBarH, btn2frame5),
            (btn4frame5, "left", sBarH, btn3frame5),

            (btn5frame5, "top", sBarT, btn1frame5),
            (btn6frame5, "top", sBarT, btn2frame5),
            (btn6frame5, "left", sBarH, btn5frame5),
            (btn7frame5, "top", sBarT, btn3frame5),
            (btn7frame5, "left", sBarH, btn6frame5),
            (btn8frame5, "top", sBarT, btn4frame5),
            (btn8frame5, "left", sBarH, btn7frame5),
        ]
    )


    ## FRAME 6: Align
    frame6 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame6_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(6, True),
        expandCommand=lambda *args: core.updateFrame(6, False),
        label="Align/Snap",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form6 = pm.formLayout()

    # Align shells and UVs
    btn1frame6 = pm.iconTextButton(
        annotation="Align the Selected Shells Along U --- Options (Right Click and Hold)",
        command=lambda *args: core.alignShells("uAvg"),
        commandRepeatable=True,
        image1=iconDict["alignShellsMidU"],
        label="Align the Selected Shells Along U",
    )
    btn1frame6Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn1frame6,
        postMenuCommand=lambda *args: createPopupAlignShellsU(btn1frame6Pop, btn1frame6)
    )
    btn2frame6 = pm.iconTextButton(
        annotation="Align the Selected Shells Along V --- Options (Right Click and Hold)",
        command=lambda *args: core.alignShells("vAvg"),
        commandRepeatable=True,
        image1=iconDict["alignShellsMidV"],
        label="Align the Selected Shells Along V",
    )
    btn2frame6Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn2frame6,
        postMenuCommand=lambda *args: createPopupAlignShellsV(btn2frame6Pop, btn2frame6)
    )
    btn3frame6 = pm.iconTextButton(
        annotation="Align the Selected UVs Along U --- Options (Right Click and Hold)",
        command=lambda *args: core.alignUVs("avgU"),
        commandRepeatable=True,
        image1=iconDict["alignUMid"],
        label="Align the Selected UVs Along U",
    )
    btn3frame6Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn3frame6,
        postMenuCommand=lambda *args: createPopupAlignUVsU(btn3frame6Pop, btn3frame6)
    )
    btn4frame6 = pm.iconTextButton(
        annotation="Align the Selected UVs Along V --- Options (Right Click and Hold)",
        command=lambda *args: core.alignUVs("avgV"),
        commandRepeatable=True,
        image1=iconDict["alignVMid"],
        label="Align the Selected UVs Along V",
    )
    btn4frame6Pop = pm.popupMenu(
        button=3,
        markingMenu=True,
        parent=btn4frame6,
        postMenuCommand=lambda *args: createPopupAlignUVsV(btn4frame6Pop, btn4frame6)
    )

    
    # Normalize
    btn14frame6 = pm.iconTextButton(
        annotation="Normalize the Selected Shells (Left Click) --- Normalize Using Last Known Options (Right Click)",
        command=lambda *args: core.normalizeShells(0),
        commandRepeatable=True,
        image1=iconDict["normalize"],
        label="Normalize the Selected Shells (Left Click) --- Normalize Using Last Known Options (Right Click)",
    )
    btn14frame6Pop = pm.popupMenu(
        button=3,
        parent=btn14frame6,
        postMenuCommand=lambda *args: normalizeUI(),
    )
    btn15frame6 = pm.iconTextButton(
        annotation="Normalize the Selected Shells Along U* Only (Left Click) --- *V (Right Click)",
        command=lambda *args: core.normalizeShells(3),
        commandRepeatable=True,
        image1=iconDict["normalizeUV"],
        label="Normalize the Selected Shells Along U* Only (Left Click) --- *V (Right Click)",
    )
    btn15frame6Pop = pm.popupMenu(
        button=3,
        parent=btn15frame6,
        postMenuCommand=lambda *args: core.normalizeShells(4),
    )
    
    btn16frame6 = pm.iconTextButton(
        annotation="Snap Two Shells Together via Two Selected UVs, A to B (Left Click) --- B to A (Right Click)",
        command=lambda *args: core.snapPoints(0),
        commandRepeatable=True,
        image1=iconDict["snapAB"],
        label="Snap Two Shells Together via Two Selected UVs, A to B (Left Click) --- B to A (Right Click)",
    )
    btn16frame6Pop = pm.popupMenu(
        button=3,
        parent=btn16frame6,
        postMenuCommand=lambda *args: core.snapPoints(1),
    )

    # Shell snapping
    btn13frame6 = pm.iconTextButton(
        annotation="Match the Selected UVs to their Neighbors (Left Click) --- Match UVs Using Last Known Options (Right Click)",
        # command=lambda *args: core.matchUVs(),
        command=lambda *args: core.matchUVs(),
        commandRepeatable=True,
        image1=iconDict["match"],
        label="Match the Selected UVs to their Neighbors (Left Click) --- Match UVs Using Last Known Options (Right Click)",
    )
    btn13frame6Pop = pm.popupMenu(
        button=3,
        parent=btn13frame6,
        postMenuCommand=lambda *args: matchTolUI(),
    )
    btnSnapTopLeft = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Top Left Corner of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(1),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapTopLeft"],
        label="Snap the Selected Shells to the Top Left Corner of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapTop = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Top Border of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(2),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapTop"],
        label="Snap the Selected Shells to the Top Border of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapTopRight = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Top Right Corner of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(3),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapTopRight"],
        label="Snap the Selected Shells to the Top Right Corner of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapLeft = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Left Border of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(4),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapLeft"],
        label="Snap the Selected Shells to the Left Border of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapCenter = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Center of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(0),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapCenter"],
        label="Snap the Selected Shells to the Center of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapRight = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Right Border of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(5),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapRight"],
        label="Snap the Selected Shells to the Right Border of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapBottomLeft = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Bottom Left Corner of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(6),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapBottomLeft"],
        label="Snap the Selected Shells to the Bottom Left Corner of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )
    btnSnapBottom = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Bottom Border of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(7),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapBottom"],
        label="Snap the Selected Shells to the Bottom Border of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall
    )
    btnSnapBottomRight = pm.iconTextButton(
        annotation="Snap the Selected Shells to the Bottom Right Corner of the Default UV Range (0.0 -> 1.0)",
        command=lambda *args: core.snapShells(8),
        commandRepeatable=True,
        height=iconSmall,
        image1=iconDict["snapBottomRight"],
        label="Snap the Selected Shells to the Bottom Right Corner of the Default UV Range (0.0 -> 1.0)",
        width=iconSmall,
    )

    # Layout the elements in the formLayout
    pm.formLayout(
        form6, edit=True,
        attachForm=[
            (btn1frame6, "top", sBarT),
            (btn1frame6, "left", sBarL),
            (btn2frame6, "top", sBarT),
            (btn3frame6, "top", sBarT),
            (btn4frame6, "top", sBarT),
            
            (btnSnapTopLeft, "left", sBarL),
            (btnSnapLeft, "left", sBarL),
            (btnSnapBottomLeft, "left", sBarL),

            (btn15frame6, "bottom", sBarB),
        ],
        attachControl=[
            (btn2frame6, "left", sBarH, btn1frame6),
            (btn3frame6, "left", sBarH, btn2frame6),
            (btn4frame6, "left", sBarH, btn3frame6),

            (btnSnapTopLeft, "top", sBarT, btn1frame6),
            (btnSnapTop, "top", sBarT, btn1frame6),
            (btnSnapTop, "left", 0, btnSnapTopLeft),
            (btnSnapTopRight, "top", sBarT, btn1frame6),
            (btnSnapTopRight, "left", 0, btnSnapTop),

            (btnSnapLeft, "top", 0, btnSnapTopLeft),
            (btnSnapCenter, "top", 0, btnSnapTop),
            (btnSnapCenter, "left", 0, btnSnapLeft),
            (btnSnapRight, "top", 0, btnSnapTopRight),
            (btnSnapRight, "left", 0, btnSnapCenter),

            (btnSnapBottomLeft, "top", 0, btnSnapLeft),
            (btnSnapBottom, "top", 0, btnSnapCenter),
            (btnSnapBottom, "left", 0, btnSnapBottomLeft),
            (btnSnapBottomRight, "top", 0, btnSnapRight),
            (btnSnapBottomRight, "left", 0, btnSnapBottom),

            (btn14frame6, "top", sBarT, btn4frame6),
            (btn14frame6, "left", gapB, btnSnapTopRight),
            (btn15frame6, "top", sBarT, btn14frame6),
            (btn15frame6, "left", gapB, btnSnapTopRight),
            (btn16frame6, "top", sBarT, btn14frame6),
            (btn16frame6, "left", gapB-1, btn15frame6),
            
            (btn13frame6, "top", sBarT, btn4frame6),
            (btn13frame6, "left", gapB-1, btn15frame6),
        ]
    )


    ## FRAME 7: UV sets
    frame7 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame7_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(7, True),
        expandCommand=lambda *args: core.updateFrame(7, False),
        label="UV Sets",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form7 = pm.formLayout()

    btn1frame7 = pm.iconTextButton(
        annotation="Create New UV Set (Left Click) --- Create New UV Set Using Last Known Options (Right Click)",
        command=lambda *args: core.createSet(scrollListUVSet),
        commandRepeatable=True,
        image1=iconDict["uvSetNew"],
        label="Create New UV Set (Left Click) --- Create New UV Set Using Last Known Options (Right Click)",
    )
    btn1frame7Pop = pm.popupMenu(
        button=3,
        parent=btn1frame7,
        postMenuCommand=lambda *args: createSetUI(),
    )
    btn2frame7 = pm.iconTextButton(
        annotation="Copy the Selected UV Set or Selected Parts to Another UV Set (Right Click and Hold) --- Copy Between the Sets Used in the Last Operation (Left Click)",
        command=lambda *args: core.copySet(scrollListUVSet, None, None, None, True),
        image1=iconDict["uvSetCopy"],
        label="Copy the Selected UV Set or Selected Parts to Another UV Set (Right Click and Hold) --- Copy Between the Sets Used in the Last Operation (Left Click)",
    )
    btn2frame7Pop = pm.popupMenu(
        button=3,
        parent=btn2frame7,
        postMenuCommand=lambda *args: createPopupCopySet(btn2frame7Pop)
    )
    btn3frame7 = pm.iconTextButton(
        annotation="Duplicate the Selected UV Set",
        command=lambda *args: core.copySet(scrollListUVSet, None, None),
        commandRepeatable=True,
        image1=iconDict["uvSetDupe"],
        label="Duplicate the Selected UV Set",
    )
    btn4frame7 = pm.iconTextButton(
        annotation="Propagate: If the Selected UV Set does not Exist on all Selected Meshes, Copy it to said Meshes",
        command=lambda *args: core.propagateSets(scrollListUVSet),
        commandRepeatable=True,
        image1=iconDict["uvSetProp"],
        label="Propagate: If the Selected UV Set does not Exist on all Selected Meshes, Copy it to said Meshes"
    )
    btn5frame7 = pm.iconTextButton(
        annotation="UV Set Order Manager",
        command=lambda *args: core.UVSetOrderMan(scrollListUVSet),
        commandRepeatable=True,
        image1=iconDict["uvSetOrderMan"],
        label="UV Set Order Manager",
    )
    btn6frame7 = pm.iconTextButton(
        annotation="Share Instances",
        command=lambda *args: pm.runtime.ShareUVInstances(),
        commandRepeatable=True,
        image1=iconDict["uvSetShareInst"],
        label="Share Instances"
    )
    btn7frame7 = pm.iconTextButton(
        annotation="Select Shared Instances",
        command=lambda *args: pm.runtime.SelectSharedUVInstances(),
        commandRepeatable=True,
        image1=iconDict["uvSetSelInst"],
        label="Select Shared Instances"
    )
    btn8frame7 = pm.iconTextButton(
        annotation="UV Snapshot Options (Left Click) --- UV Snapshot Using Last Known Options (Right Click)",
        command=lambda *args: core.ssTakeShot(),
        commandRepeatable=True,
        image1=iconDict["uvSetSnapshot"],
        label="UV Snapshot Options (Left Click) --- UV Snapshot Using Last Known Options (Right Click)",
    )
    btn8frame7Pop = pm.popupMenu(
        button=3,
        parent=btn8frame7,
        postMenuCommand=lambda *args: snapshotUI(),
    )

    # UV Sets list
    scrollListUVSet = pm.textScrollList(
        "uvSetScrollList_NSUV",
        allowMultiSelection=True,
        deleteKeyCommand=lambda *args: core.deleteSet(scrollListUVSet),
        doubleClickCommand=lambda *args: renameSetUI(scrollListUVSet), # Necessary to pass arg on the fly
        selectCommand=lambda *args: core.setCurrentSet(scrollListUVSet),
        height=setListY,
        width=frameMainX-2
    )
    
    # Save the scroll list in an optVar (so we can easily reach it in panel.mel)
    pm.optionVar["scrollList_NSUV"] = scrollListUVSet

    # Layout the elements in the formLayout
    pm.formLayout(
        form7, edit=True,
        attachForm=[
            (btn1frame7, "top", sBarT),
            (btn1frame7, "left", sBarL),
            (btn2frame7, "top", sBarT),
            (btn3frame7, "top", sBarT),
            (btn4frame7, "top", sBarT),

            (btn5frame7, "left", sBarL),

            (scrollListUVSet, "left", 0),
            (scrollListUVSet, "bottom", sBarB),
        ],
        attachControl=[
            (btn2frame7, "left", sBarH, btn1frame7),
            (btn3frame7, "left", sBarH, btn2frame7),
            (btn4frame7, "left", sBarH, btn3frame7),

            (btn5frame7, "top", sBarT, btn1frame7),
            (btn6frame7, "top", sBarT, btn2frame7),
            (btn6frame7, "left", sBarH, btn5frame7),
            (btn7frame7, "top", sBarT, btn3frame7),
            (btn7frame7, "left", sBarH, btn6frame7),
            (btn8frame7, "top", sBarT, btn4frame7),
            (btn8frame7, "left", sBarH, btn7frame7),

            (scrollListUVSet, "top", sBarH, btn5frame7),
        ]
    )


    ## FRAME 8: TD
    frame8 = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["frame8_NSUV"],
        collapseCommand=lambda *args: core.updateFrame(8, True),
        expandCommand=lambda *args: core.updateFrame(8, False),
        label="Texel Density",
        parent=formMain,
        width=frameMainX
    )

    # Formlayout for the child elements
    form8 = pm.formLayout()

    fieldGrpTD = pm.floatFieldGrp(
        changeCommand=lambda *args: core.tdVar("updateTD", fieldGrpTD),
        columnAlign=[1, "left"],
        columnWidth2=[70, 42],
        label="TD (px/unit)",
        numberOfFields=1,
        precision=2,
        value1=pm.optionVar["td_NSUV"],
        width=frameMainX
    )
    fieldGrpSize = pm.intFieldGrp(
        changeCommand=lambda *args: core.tdVar("updateSize", fieldGrpSize),
        columnAlign=[1, "left"],
        columnWidth2=[70, 42],
        label="Map size (px)",
        numberOfFields=1,
        value1=pm.optionVar["tdSize_NSUV"],
        width=frameMainX
    )
    btn1frame8 = pm.iconTextButton(
        annotation="Load* Values to the Texel Density Fields (Left Click) --- *Save Values from (Right Click)",
        command=lambda *args: core.tdVar("getA", fieldGrpTD, fieldGrpSize),
        commandRepeatable=True,
        image1=iconDict["tdVarA"],
        label="Load* Values to the Texel Density Fields (Left Click) --- *Save Values from (Right Click)",
    )
    btn1frame8Pop = pm.popupMenu(
        button=3,
        parent=btn1frame8,
        postMenuCommand=lambda *args: core.tdVar("setA", fieldGrpTD, fieldGrpSize),
    )
    btn2frame8 = pm.iconTextButton(
        annotation="Load* Values to the Texel Density Fields (Left Click) --- *Save Values from (Right Click)",
        command=lambda *args: core.tdVar("getB", fieldGrpTD, fieldGrpSize),
        commandRepeatable=True,
        image1=iconDict["tdVarB"],
        label="Load* Values to the Texel Density Fields (Left Click) --- *Save Values from (Right Click)",
    )
    btn2frame8Pop = pm.popupMenu(
        button=3,
        parent=btn2frame8,
        postMenuCommand=lambda *args: core.tdVar("setB", fieldGrpTD, fieldGrpSize),
    )
    btn3frame8 = pm.iconTextButton(
        annotation="Get Texel Density - The average texel density is fetched from the faces in a selection.",
        command=lambda *args: core.getTD(fieldGrpTD),
        commandRepeatable=True,
        image1=iconDict["tdGet"],
        label="Get Texel Density - The average texel density is fetched from the faces a selection.",
    )
    btn4frame8 = pm.iconTextButton(
        annotation="Set Texel Density - Shells are scaled till they match the specified TD",
        command=lambda *args: core.setTD(fieldGrpTD, fieldGrpSize),
        commandRepeatable=True,
        image1=iconDict["tdSet"],
        label="Set Texel Density - Shells are scaled till they match the specified TD"
    )
    btn4frame8Pop = pm.popupMenu(
        button=3,
        parent=btn4frame8,
        postMenuCommand=lambda *args: workingUnitsUI(),
    )

    # Layout the elements in the formLayout
    pm.formLayout(
        form8, edit=True,
        attachForm=[
            (fieldGrpTD, "top", sBarT),
            (fieldGrpTD, "left", sBarL),
            (fieldGrpSize, "left", sBarL),

            (btn1frame8, "left", sBarL),
            (btn1frame8, "bottom", sBarB),
        ],
        attachControl=[
            (fieldGrpSize, "top", sBarT, fieldGrpTD),

            (btn1frame8, "top", sBarH, fieldGrpSize),
            (btn2frame8, "top", sBarH, fieldGrpSize),
            (btn2frame8, "left", sBarH, btn1frame8),
            (btn3frame8, "top", sBarH, fieldGrpSize),
            (btn3frame8, "left", sBarH, btn2frame8),
            (btn4frame8, "top", sBarH, fieldGrpSize),
            (btn4frame8, "left", sBarH, btn3frame8),
        ]
    )

    # Layout the frames inside the main formLayout
    pm.formLayout(
        formMain, edit=True,
        attachForm=[
            (frame1, "top", 0),
            (frame1, "left", 0),
            (frame2, "left", 0),
            (frame3, "left", 0),
            (frame4, "left", 0),
            (frame5, "left", 0),
            (frame6, "left", 0),
            (frame7, "left", 0),
            (frame8, "left", 0),
        ],
        attachControl=[
            (frame2, "top", 0, frame1),
            (frame3, "top", 0, frame2),
            (frame4, "top", 0, frame3),
            (frame5, "top", 0, frame4),
            (frame6, "top", 0, frame5),
            (frame7, "top", 0, frame6),
            (frame8, "top", 0, frame7),
        ]
    )


    ## Right container - Work area

    # Create second paneLayout. Holds the UV editor modelPanel + top and bottom bars
    paneUV = pm.paneLayout(
        configuration="horizontal2",
        paneSize=([1, 100, 99], [2, 100, 1]),
        parent=paneMain,
        separatorThickness=4,
        staticWidthPane=1
    )

    # Get all panels, delete duplicate entries of the NSUV panel
    panelList = pm.getPanel(allPanels=True)
    for p in panelList:
        if p.getLabel() == NSUV_title:
            pm.deleteUI(p, panel=True)

    # Create new model panel
    panelUV = pm.modelPanel(
        label=NSUV_title,
        parent=paneUV
    )

    # Get UV editor panel name, replace it with new one
    txtEditor = pm.getPanel(scriptType="polyTexturePlacementPanel")[0]
    pm.scriptedPanel(
        txtEditor, edit=True,
            replacePanel=panelUV,
    )


    ## Visibility bar

    # Container for the visBar groups
    formVis = pm.formLayout(parent=paneUV, width=1)

    # Group 1 form (Display)
    grp1Layout = pm.formLayout(parent=formVis)

    # Group 1 elements list +toggle
    grp1Elements = []    
    grp1Toggle = pm.iconTextButton(
        command=lambda *args: core.visBarToggle(1, grp1Toggle, grp1Elements, grp1Layout),
        image1=iconDict["barIconSmallOpen"],
        parent=grp1Layout,
        visible=True,
    )

    # Group 1 icons
    grp1btn1 = pm.iconTextCheckBox(
        visBtn1,
        annotation="Toggle Texture Display",
        changeCommand=lambda *args: core.updateDisplay(0, 0),
        image1=iconDict["imgDisp"],
        label="Toggle Texture Display",
        parent=grp1Layout,
        value=pm.optionVar["imgDisp_NSUV"],
    )
    grp1btn2 = pm.iconTextCheckBox(
        visBtn2,
        annotation="Toggle Texture Dimming",
        changeCommand=lambda *args: core.updateDisplay(1, 0),
        image1=iconDict["dimTexture"],
        label="Toggle Texture Dimming",
        parent=grp1Layout,
        value=pm.optionVar["imgDim_NSUV"],
    )
    grp1btn3 = pm.iconTextCheckBox(
        visBtn3,
        annotation="Toggle Shaded UV Display",
        changeCommand=lambda *args: core.updateDisplay(2, 0),
        image1=iconDict["shadeShells"],
        label="Toggle Shaded UV Display",
        parent=grp1Layout,
        value=pm.optionVar["shellShade_NSUV"],
    )
    grp1btn4 = pm.iconTextCheckBox(
        visBtn4,
        annotation="Toggle Shell Borders",
        changeCommand=lambda *args: core.updateDisplay(3, 0),
        image1=iconDict["shellBorders"],
        label="Toggle Shell Borders",
        parent=grp1Layout,
        value=pm.optionVar["shellBorder_NSUV"],
    )
    if mayaVer >= 201500:
        grp1btn5 = pm.iconTextCheckBox(
            visBtn5,
            annotation="Toggle UV Distortion Display",
            changeCommand=lambda *args: core.updateDisplay(4, 0),
            image1=iconDict["distToggle"],
            label="Toggle UV Distortion Display",
            parent=grp1Layout,
            value=pm.optionVar["shellDist_NSUV"],
        )
    grp1btn6 = pm.iconTextButton(
        visBtn6,
        annotation="Cycle Forwards* Between Edge Colors (Left Click) --- *Backwards (Right Click)",
        command=lambda *args: core.edgeColor("forward"),
        commandRepeatable=True,
        image1=iconDict["edgeColors"],
        label="Cycle Forwards* Between Edge Colors (Left Click) --- *Backwards (Right Click)",
        parent=grp1Layout,
    )
    grp1btn6Popup = pm.popupMenu(
        button=3,
        parent=grp1btn6,
        postMenuCommand=lambda *args: core.edgeColor("backward"),
    )
    if mayaVer >= 201500:
        grp1btn7 = pm.iconTextCheckBox(
            visBtn7,
            annotation="Toggle Checkered Tiles",
            changeCommand=lambda *args: core.updateDisplay(5, 0),
            image1=iconDict["checker"],
            label="Toggle Checkered Tiles",
            parent=grp1Layout,
            value=pm.optionVar["checkers_NSUV"],
        )
    grp1btn8 = pm.iconTextCheckBox(
        visBtn8,
        annotation="Toggle Filtered Display",
        changeCommand=lambda *args: core.updateDisplay(6, 0),
        image1=iconDict["filtered"],
        label="Toggle Filtered Display",
        parent=grp1Layout,
        value=pm.optionVar["imgFilter_NSUV"],
    )
    grp1btn9 = pm.iconTextButton(
        visBtn9,
        annotation="Toggle RGB Channels Display",
        command=lambda *args: core.updateDisplay(7, 0),
        commandRepeatable=True,
        image1=iconDict["dispColor"],
        label="Toggle RGB Channel Display",
        parent=grp1Layout,
    )
    grp1btn10 = pm.iconTextButton(
        visBtn10,
        annotation="Toggle Alpha Channel Display",
        command=lambda *args: core.updateDisplay(7, 1),
        commandRepeatable=True,
        image1=iconDict["dispAlpha"],
        label="Toggle Alpha Channel Display",
        parent=grp1Layout,
    )
    
    # Build list of elements in group 1
    if mayaVer >= 201500:
        grp1Elements = [grp1btn1, grp1btn2, grp1btn3, grp1btn4, grp1btn5, grp1btn6, grp1btn7, grp1btn8, grp1btn9, grp1btn10]
    else:
        grp1Elements = [grp1btn1, grp1btn2, grp1btn3, grp1btn4, grp1btn6, grp1btn8, grp1btn9, grp1btn10]

    # Layout the icons inside grp1Layout
    if mayaVer >= 201500:
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1Toggle, "top", vBarT),
                (grp1Toggle, "left", 1),
                (grp1btn1, "top", vBarT),
                (grp1btn2, "top", vBarT),
                (grp1btn3, "top", vBarT),
                (grp1btn4, "top", vBarT),
                (grp1btn5, "top", vBarT),
                (grp1btn6, "top", vBarT),
                (grp1btn7, "top", vBarT),
                (grp1btn8, "top", vBarT),
                (grp1btn9, "top", vBarT),
                (grp1btn10, "top", vBarT),
                (grp1btn10, "right", vBarR),
            ],
            attachControl=[
                (grp1btn1, "left", vBarL, grp1Toggle),
                (grp1btn2, "left", vBarH, grp1btn1),
                (grp1btn3, "left", vBarH, grp1btn2),
                (grp1btn4, "left", vBarH, grp1btn3),
                (grp1btn5, "left", vBarH, grp1btn4),
                (grp1btn6, "left", vBarH, grp1btn5),
                (grp1btn7, "left", vBarH, grp1btn6),
                (grp1btn8, "left", vBarH, grp1btn7),
                (grp1btn9, "left", vBarH, grp1btn8),
                (grp1btn10, "left", vBarH, grp1btn9),
            ]
        )
    else:
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1Toggle, "top", vBarT),
                (grp1Toggle, "left", 1),
                (grp1btn1, "top", vBarT),
                (grp1btn2, "top", vBarT),
                (grp1btn3, "top", vBarT),
                (grp1btn4, "top", vBarT),
                (grp1btn6, "top", vBarT),
                (grp1btn8, "top", vBarT),
                (grp1btn9, "top", vBarT),
                (grp1btn10, "top", vBarT),
                (grp1btn10, "right", vBarR),
            ],
            attachControl=[
                (grp1btn1, "left", vBarL, grp1Toggle),
                (grp1btn2, "left", vBarH, grp1btn1),
                (grp1btn3, "left", vBarH, grp1btn2),
                (grp1btn4, "left", vBarH, grp1btn3),
                (grp1btn6, "left", vBarH, grp1btn4),
                (grp1btn8, "left", vBarH, grp1btn6),
                (grp1btn9, "left", vBarH, grp1btn8),
                (grp1btn10, "left", vBarH, grp1btn9),
            ]
        )


    
    # Group 2 form (Grid/Snap)
    grp2Layout = pm.formLayout(parent=formVis)

    # Group 2 elements list +toggle
    grp2Elements = []
    grp2Toggle = pm.iconTextButton(
        command=lambda *args: core.visBarToggle(2, grp2Toggle, grp2Elements, grp2Layout),
        image1=iconDict["barIconSmallOpen"],
        parent=grp2Layout,
        visible=True,
        )   

    # Group 2 icons
    grp2btn1 = pm.iconTextCheckBox(
        visBtn11,
        annotation="Toggle UV Grid Display",
        changeCommand=lambda *args: core.updateDisplay(8, 0),
        image1=iconDict["gridDisp"],
        label="Toggle UV Grid Display",
        parent=grp2Layout,
        value=pm.optionVar["gridDisp_NSUV"],
    )
    grp2btn2 = pm.iconTextButton(
        visBtn12,
        annotation="Snap the selected UVs to the user specified grid",
        command=lambda *args: pm.mel.performPolyGridUV(0),
        commandRepeatable=True,
        image1=iconDict["gridSnap"],
        label="Snap to Grid",
        parent=grp2Layout,
    )
    grp2btn3 = pm.iconTextCheckBox(
        visBtn13,
        annotation="Toggle Image Pixel Snapping",
        changeCommand=lambda *args: core.updateDisplay(9, 0),
        image1=iconDict["pxSnap"],
        label="Toggle Image Pixel Snapping",
        parent=grp2Layout,
        value=pm.optionVar["pxSnap_NSUV"]
    )

    # Build list of elements in group 2
    grp2Elements = [grp2btn1, grp2btn2, grp2btn3]

    # Layout the icons inside grp2Layout
    pm.formLayout(
        grp2Layout, edit=True,
        attachForm=[
            (grp2Toggle, "top", vBarT),
            (grp2Toggle, "left", 0),
            (grp2btn1, "top", vBarT),
            (grp2btn2, "top", vBarT),
            (grp2btn3, "top", vBarT),
            (grp2btn3, "right", vBarR),
        ],
        attachControl=[
            (grp2btn1, "left", vBarL, grp2Toggle),
            (grp2btn2, "left", vBarH, grp2btn1),
            (grp2btn3, "left", vBarH, grp2btn2),
        ]
    )


    # Group 3 form (PSD networks)
    grp3Layout = pm.formLayout(parent=formVis)

    # Group 3 elements list +toggle
    grp3Elements = []
    grp3Toggle = pm.iconTextButton(
        command=lambda *args: core.visBarToggle(3, grp3Toggle, grp3Elements, grp3Layout),
        image1=iconDict["barIconSmallOpen"],
        parent=grp3Layout,
        visible=True,
        )        

    # Group 3 icons
    grp3btn1 = pm.iconTextCheckBox(
        visBtn14,
        annotation="Toggle UV Editor Baking",
        changeCommand=lambda *args: core.updateDisplay(10, 0),
        image1=iconDict["swapBG"],
        label="Toggle UV Editor Baking",
        parent=grp3Layout,
        value=pm.optionVar["editorBaking_NSUV"],
    )
    grp3btn2 = pm.iconTextButton(
        visBtn15,
        annotation="Update PSD networks",
        command=lambda *args: pm.mel.textureWindowBakeEditorImage(),
        commandRepeatable=True,
        image1=iconDict["updatePSD"],
        label="Update PSD networks",
        parent=grp3Layout,
    )
    grp3btn3 = pm.iconTextButton(
        visBtn16,
        annotation="Force UV Editor Texture Rebake",
        command=lambda *args: pm.mel.psdUpdateTextures(),
        commandRepeatable=True,
        image1=iconDict["bakeEditor"],
        label="Force UV Editor Texture Rebake",
        parent=grp3Layout,
    )
    grp3btn4 = pm.iconTextCheckBox(
        visBtn17,
        annotation="Toggle Texture Ratio",
        changeCommand=lambda *args: core.updateDisplay(11, 0),
        image1=iconDict["imgRatio"],
        label="Toggle Texture Ratio",
        parent=grp3Layout,
        value=pm.optionVar["imgRatio_NSUV"],
    )

    # Build list of elements in group 3
    grp3Elements = [grp3btn1, grp3btn2, grp3btn3, grp3btn4]

    # Layout the icons inside grp3Layout
    pm.formLayout(
        grp3Layout, edit=True,
        attachForm=[
            (grp3Toggle, "top", vBarT),
            (grp3Toggle, "left", 0),
            (grp3btn1, "top", vBarT),
            (grp3btn2, "top", vBarT),
            (grp3btn3, "top", vBarT),
            (grp3btn4, "top", vBarT),
            (grp3btn4, "right", vBarR),
        ],
        attachControl=[
            (grp3btn1, "left", vBarL, grp3Toggle),
            (grp3btn2, "left", vBarH, grp3btn1),
            (grp3btn3, "left", vBarH, grp3btn2),
            (grp3btn4, "left", vBarH, grp3btn3),            
        ]
    )
    
    ## Maya 2016 -only layout (View Transform/Color Management)
    if mayaVer >= 201600:
    
        # Group 4 form (View Transform)
        grp4Layout = pm.formLayout(parent=formVis)

        # Group 4 elements list +toggle
        grp4Elements = []
        grp4Toggle = pm.iconTextButton(
            command=lambda *args: core.visBarToggle(4, grp4Toggle, grp4Elements, grp4Layout),
            image1=iconDict["barIconSmallOpen"],
            parent=grp4Layout,
            visible=True,
            )

        # Group 4 icons
            
        # Exposure control
        fieldExp = pm.floatField(
            changeCommand=lambda *args: core.updateExpGam(0, fieldExp),
            dragCommand=lambda *args: core.updateExpGam(0, fieldExp),
            height=vBarFieldY,
            parent=grp4Layout,
            precision=2,
            step=0.1,
            value=pm.optionVar["expField_NSUV"],
            width=vBarFieldX,
        )
        btnExp = pm.iconTextCheckBox(
            annotation="Toggle the Brightness (Exposure) Adjustment for the Display",
            offCommand=lambda *args: core.updateExpGam(2, fieldExp, False),
            onCommand=lambda *args: core.updateExpGam(2, fieldExp, True),
            image1=iconDict["expControl"],
            label="Toggle the Brightness (Exposure) Adjustment for the Display",
            parent=grp4Layout,
            version="2016",
            value=pm.optionVar["expToggle_NSUV"],
        )    

        # Gamma control
        fieldGamma = pm.floatField(
            changeCommand=lambda *args: core.updateExpGam(1, fieldGamma),
            dragCommand=lambda *args: core.updateExpGam(1, fieldGamma),
            height=vBarFieldY,
            min=0.0,
            parent=grp4Layout,
            precision=2,
            step=0.1,
            value=pm.optionVar["gamField_NSUV"],
            width=vBarFieldX,
        )
        btnGamma = pm.iconTextCheckBox(
            annotation="Toggle the Gamma Adjustment for the Display",
            offCommand=lambda *args: core.updateExpGam(3, fieldGamma, False),
            onCommand=lambda *args: core.updateExpGam(3, fieldGamma, True),
            image1=iconDict["gammaControl"],
            label="Toggle the Gamma Adjustment for the Display",
            parent=grp4Layout,
            version="2016",
            value=pm.optionVar["gamToggle_NSUV"],
        )

        # View transform
        cBoxVT = pm.symbolCheckBox(
            annotation="Toggles On/Off View Transform/Color Management in the UV Editor",
            changeCommand=lambda *args: core.updateDisplay(12, 0),
            onImage=iconDict["vtOn"],
            offImage=iconDict["vtOff"],
            parent=grp4Layout,
            value=pm.optionVar["colorMan_NSUV"],
        )
        optGrpVT = pm.optionMenu(
            changeCommand=lambda *args: core.updateExpGam(4, optGrpVT),
            height=19,
            parent=grp4Layout,
        )
        vtNames = pm.colorManagementPrefs(viewTransformNames=True, query=True)
        for name in vtNames:
            pm.menuItem(label=name)
        optGrpVT.setValue(pm.optionVar["vtName_NSUV"])

        # Build list of dynamic elements in group 4
        grp4Elements = [btnExp, fieldExp, btnGamma, fieldGamma, cBoxVT, optGrpVT]

        # Layout the icons inside grp4Layout
        pm.formLayout(
            grp4Layout, edit=True,
            attachForm=[
                (grp4Toggle, "top", vBarT),
                (grp4Toggle, "left", vBarT),
                (btnExp, "top", vBarT),
                (fieldExp, "top", vBarT),
                (btnGamma, "top", vBarT),
                (fieldGamma, "top", vBarT),
                (cBoxVT, "top", vBarT),            
                (optGrpVT, "top", vBarT),
                (optGrpVT, "right", vBarR),
            ],
            attachControl=[
                (btnExp, "left", vBarL, grp4Toggle),
                (fieldExp, "left", vBarH+1, btnExp),
                (btnGamma, "left", vBarH+2, fieldExp),
                (fieldGamma, "left", vBarH+1, btnGamma),            
                (cBoxVT, "left", vBarH+2, fieldGamma),
                (optGrpVT, "left", vBarH+1, cBoxVT),
            ]
        ) ## End of Maya 2016 -only layout    
    
    # Group 5 form (Editor)
    grp5Layout = pm.formLayout(parent=formVis)

    # Group 5 elements list +toggle
    grp5Elements = []
    grp5Toggle = pm.iconTextButton(
        command=lambda *args: core.visBarToggle(5, grp5Toggle, grp5Elements, grp5Layout),
        image1=iconDict["barIconSmallOpen"],
        parent=grp5Layout,
        visible=True,
        )

    # Group 5 icons
    btnDef = pm.button(
        annotation="Revert to the Default UV Editor", 
        backgroundColor=[0.33, 0.33, 0.33], 
        command=lambda *args: core.defaultEditor(window),
        height=vBarFieldY+2,
        label="Default UV Editor", 
        parent=grp5Layout, 
        width=110,
    )
    btnLock = pm.symbolCheckBox(
        annotation="Lock NSUV Window Size", 
        backgroundColor=[0.33, 0.33, 0.33], 
        onCommand=lambda *args: core.lockWindow(window, 1), 
        offCommand=lambda *args: core.lockWindow(window, 0), 
        height=vBarFieldY+2,
        onImage=iconDict["winLockOn"],
        offImage=iconDict["winLockOff"],
        parent=grp5Layout,
        value=pm.optionVar["sizeableWin_NSUV"],
    )
    
    # Build list of dynamic elements in group 5
    grp5Elements = [btnDef, btnLock]
    
    # Layout the icons inside grp5Layout
    pm.formLayout(
        grp5Layout, edit=True,
        attachForm=[
            (grp5Toggle, "top", vBarT),
            (grp5Toggle, "left", vBarT),
            (btnDef, "top", vBarT),
            (btnLock, "top", vBarT),
            (btnLock, "right", vBarR),
        ],
        attachControl=[
            (btnDef, "left", vBarL, grp5Toggle),
            (btnLock, "left", vBarL+5, btnDef),
        ]
    )

    # Layout the visBar layout
    if mayaVer >= 201600:
        pm.formLayout(
            formVis, edit=True,
            attachForm=[
                (grp1Layout, "top", 0),
                (grp1Layout, "left", 0),
                (grp2Layout, "top", 0),
                (grp3Layout, "top", 0),
                (grp4Layout, "top", 0),
                (grp5Layout, "top", 0),
            ],
            attachControl=[
                (grp2Layout, "left", 0, grp1Layout),
                (grp3Layout, "left", 0, grp2Layout),
                (grp4Layout, "left", 0, grp3Layout),
                (grp5Layout, "left", 0, grp4Layout),
            ]
        )
    else:
        pm.formLayout(
            formVis, edit=True,
            attachForm=[
                (grp1Layout, "top", 0),
                (grp1Layout, "left", 0),
                (grp2Layout, "top", 0),
                (grp3Layout, "top", 0),
                (grp5Layout, "top", 0),
            ],
            attachControl=[
                (grp2Layout, "left", 0, grp1Layout),
                (grp3Layout, "left", 0, grp2Layout),
                (grp5Layout, "left", 0, grp3Layout),
            ]
        )    
    
    # Replace pane
    paneUV.setPane([formVis, 2])

    # Display the window
    pm.showWindow(window)

    # Create script jobs
    core.createScriptJobs(window, scrollListUVSet, cBoxCSpace)

    # Update the UV set editor (else it is blank)
    core.updateUVSetEditor(scrollListUVSet)

    # Turn on/off toggles for the editor display and refresh icon and top menu checkboxes
    core.updateDisplay()

    # Needed because the isolate select button fails otherwise
    core.updateDisplay(13)

    # Update exposure and gamma
    if mayaVer >= 201600:
        elements = [fieldExp, btnExp, fieldGamma, btnGamma, cBoxVT, optGrpVT]
        core.updateExpGam(-1, elements)

    # Delete the Panels -menu from the menu bar. This is a lazy hack because I couldn't
    # find what calls buildPanelPopupMenu() - Luckily Panels is a hardcoded name
    pm.deleteUI("Panels", menu=True)


## Toolbar

def createToolbar(flow):

    # Template for all the toolbar push buttons
    if pm.uiTemplate("toolbarBtnTemplate", exists=True):
        pm.deleteUI("toolbarBtnTemplate", uiTemplate=True)

    pm.uiTemplate("toolbarBtnTemplate")
    pm.iconTextButton(
        commandRepeatable=True,
        defineTemplate="toolbarBtnTemplate",
        height=iconTop,
        width=iconTop,
    )

    ## WARN: This last one isn't really needed as a uiTemplate as the btn type only occurs once
    # Template for all the toolbar checkbox icon buttons
    if pm.uiTemplate("toolbarCboxTemplate", exists=True):
        pm.deleteUI("toolbarCboxTemplate", uiTemplate=True)

    pm.uiTemplate("toolbarCboxTemplate")
    pm.iconTextButton(
        defineTemplate="toolbarCboxTemplate",
        height=iconTop,
        width=iconTop,
    )

    # Group 1 form (Tools)
    grp1Layout = pm.formLayout()
    
    # Group 1 elements list +toggle
    grp1Elements = []
    grp1Toggle = pm.iconTextButton(
        annotation="Show/Hide the Tools Icons",
        command=lambda *args: core.topBarToggle(1, grp1Toggle, grp1Elements, grp1Layout),
        image1=iconDict["barIconOpen"],
        parent=grp1Layout,
        visible=True,
        )
    
    # Push template into stack for the icon btns
    pm.setUITemplate("toolbarBtnTemplate", pushTemplate=True)
    
    # Group 1 icons
    grp1btn1 = pm.iconTextButton(
        annotation="UV Lattice Tool",
        command=lambda *args: core.uvContextTool(0, "lattice"),
        image1=iconDict["latticeTool"],
        label="UV Lattice Tool",
        parent=grp1Layout,
    )
    grp1btn1Pop = pm.popupMenu(
        button=3,
        parent=grp1btn1,
        postMenuCommand=lambda *args: core.uvContextTool(0, "lattice", True),
    )
    grp1btn2 = pm.iconTextButton(
        annotation="Smudge UV Tool",
        command=lambda *args: core.uvContextTool(1, "smudge"),
        image1=iconDict["smudgeTool"],
        label="Smudge UV Tool",
        parent=grp1Layout,
    )
    grp1btn2Pop = pm.popupMenu(
        button=3,
        parent=grp1btn2,
        postMenuCommand=lambda *args: core.uvContextTool(1, "smudge", True),
    )
    grp1btn3 = pm.iconTextButton(
        annotation="Smear UV Tool",
        command=lambda *args: core.uvContextTool(7, "smear"),
        image1=iconDict["smearTool"],
        label="Smear UV Tool",
        parent=grp1Layout,
    )
    grp1btn3Pop = pm.popupMenu(
        button=3,
        parent=grp1btn3,
        postMenuCommand=lambda *args: core.uvContextTool(7, "smear", True),
    )
    grp1btn4 = pm.iconTextButton(   
        annotation="Move UV Shell Tool",
        command=lambda *args: core.uvContextTool(2, "move"),
        image1=iconDict["moveTool"],
        label="Move UV Shell Tool",
        parent=grp1Layout,
    )
    grp1btn4Pop = pm.popupMenu(
        button=3,
        parent=grp1btn4,
        postMenuCommand=lambda *args: core.uvContextTool(2, "move", True),
    )
    if mayaVer >= 201400:
        grp1btn7 = pm.iconTextButton(
            annotation="Tweak UV Tool",
            command=lambda *args: core.uvContextTool(4, "tweak"),
            image1=iconDict["tweakTool"],
            label="Tweak UV -tool", 
            parent=grp1Layout,
        )
        grp1btn7Pop = pm.popupMenu(
            button=3,
            parent=grp1btn7,
            postMenuCommand=lambda *args: core.uvContextTool(4, "tweak", True),
        )
    if mayaVer >= 201600:
        grp1btn5 = pm.iconTextButton(
            annotation="Grab UV Tool",
            # command=lambda *args: [ pm.texSculptCacheContext("texSculptCacheContextObj", edit=True, mode="Grab"), pm.setToolTo("texSculptCacheContextObj") ],
            command=lambda *args: core.uvContextTool(7, "grab"),
            image1=iconDict["grabTool"],
            label="Grab UV Tool",
        parent=grp1Layout,
        )
        grp1btn5Pop = pm.popupMenu(
            button=3,
            parent=grp1btn5,
            postMenuCommand=lambda *args: core.uvContextTool(7, "grab", True),
        )
        grp1btn6 = pm.iconTextButton(
            annotation="Pinch UV Tool",
            command=lambda *args: core.uvContextTool(7, "pinch"),
            image1=iconDict["pinchTool"],
            label="Pinch UV Tool",
            parent=grp1Layout,
        )
        grp1btn6Pop = pm.popupMenu(
            button=3,
            parent=grp1btn6,
            postMenuCommand=lambda *args: core.uvContextTool(7, "pinch", True),
        )
    if mayaVer >= 201650:
        grp1btn8 = pm.iconTextButton(
            annotation="Symmetrize UV Tool",
            command=lambda *args: core.uvContextTool(8, "symmetrize"),
            image1=iconDict["symmetrizeTool"],
            label="Symmetrize UV Tool", 
            parent=grp1Layout,
            version=2017,
        )
        grp1btn8Pop = pm.popupMenu(
            button=3,
            parent=grp1btn8,
            postMenuCommand=lambda *args: core.uvContextTool(8, "symmetrize", True),
        )

    # Pop template from stack
    pm.setUITemplate(popTemplate=True)

    # Build list of elements in group 1
    if mayaVer >= 201600:
        grp1Elements = [grp1btn1, grp1btn2, grp1btn3, grp1btn4, grp1btn5, grp1btn6, grp1btn7]
    elif mayaVer >= 201400:
        grp1Elements = [grp1btn1, grp1btn2, grp1btn3, grp1btn4, grp1btn7]
    else:
        grp1Elements = [grp1btn1, grp1btn2, grp1btn3, grp1btn4]

    # Layout the icons in grp1Layout
    if mayaVer >= 201650:
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1btn1, "top", tBarT),
                (grp1btn1, "left", tBarL),
                (grp1btn2, "top", tBarT),
                (grp1btn3, "top", tBarT),
                (grp1btn4, "top", tBarT),
                (grp1btn5, "top", tBarT),
                (grp1btn6, "top", tBarT),
                (grp1btn7, "top", tBarT),
                (grp1btn8, "top", tBarT),
                (grp1btn8, "right", tBarR),
            ],
            attachControl=[
                (grp1btn2, "left", tBarH, grp1btn1),
                (grp1btn3, "left", tBarH, grp1btn2),
                (grp1btn4, "left", tBarH, grp1btn3),
                (grp1btn5, "left", tBarH, grp1btn4),
                (grp1btn6, "left", tBarH, grp1btn5),
                (grp1btn7, "left", tBarH, grp1btn6),
                (grp1btn8, "left", tBarH, grp1btn7),
            ]
        )

    elif mayaVer >= 201600:
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1btn1, "top", tBarT),
                (grp1btn1, "left", tBarL),
                (grp1btn2, "top", tBarT),
                (grp1btn3, "top", tBarT),
                (grp1btn4, "top", tBarT),
                (grp1btn5, "top", tBarT),
                (grp1btn6, "top", tBarT),
                (grp1btn7, "top", tBarT),
                (grp1btn7, "right", tBarR),
            ],
            attachControl=[
                (grp1btn2, "left", tBarH, grp1btn1),
                (grp1btn3, "left", tBarH, grp1btn2),
                (grp1btn4, "left", tBarH, grp1btn3),
                (grp1btn5, "left", tBarH, grp1btn4),
                (grp1btn6, "left", tBarH, grp1btn5),
                (grp1btn7, "left", tBarH, grp1btn6),
            ]
        )

    elif mayaVer >= 201400:
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1btn1, "top", tBarT),
                (grp1btn1, "left", tBarL),
                (grp1btn2, "top", tBarT),
                (grp1btn3, "top", tBarT),
                (grp1btn4, "top", tBarT),
                (grp1btn7, "top", tBarT),
                (grp1btn7, "right", tBarR),
            ],
            attachControl=[
                (grp1btn2, "left", tBarH, grp1btn1),
                (grp1btn3, "left", tBarH, grp1btn2),
                (grp1btn4, "left", tBarH, grp1btn3),
                (grp1btn7, "left", tBarH, grp1btn4),
            ]
        )

    else: # Maya 2013 and below
        pm.formLayout(
            grp1Layout, edit=True,
            attachForm=[
                (grp1btn1, "top", tBarT),
                (grp1btn1, "left", tBarL),
                (grp1btn2, "top", tBarT),
                (grp1btn3, "top", tBarT),
                (grp1btn4, "top", tBarT),
                (grp1btn4, "right", tBarR),
            ],
            attachControl=[
                (grp1btn2, "left", tBarH, grp1btn1),
                (grp1btn3, "left", tBarH, grp1btn2),
                (grp1btn4, "left", tBarH, grp1btn3),
            ]
        )


    ## Pinning group
    
    # Version check - exclude pinning group if not 2016+. Put args in var.
    if mayaVer >= 201600:
        pm.setParent('..') # Set default parent to one step up

        # Group 2 form (Pinning)
        grp2Layout = pm.formLayout()
        
        # Group 2 elements list +toggle
        grp2Elements = []
        grp2Toggle = pm.iconTextButton(
            annotation="Show/Hide the Pinning Icons",
            command=lambda *args: core.topBarToggle(2, grp2Toggle, grp2Elements, grp2Layout),
            image1=iconDict["barIconOpen"],
            parent=grp2Layout,
            visible=True,
        )
        
        # Push template into stack for the icon btns
        pm.setUITemplate("toolbarBtnTemplate", pushTemplate=True)

        # Group 2 icons        
        grp2btn1 = pm.iconTextButton(
            annotation="Pin UV Tool",
            command=lambda *args: core.uvContextTool(7, "freeze"),
            image1=iconDict["pinTool"],
            label="Pin UV Tool",
            parent=grp2Layout,
        )
        grp2btn1Pop = pm.popupMenu(
            button=3,
            parent=grp2btn1,
            postMenuCommand=lambda *args: core.uvContextTool(7, "freeze", True),
        )
        grp2btn2 = pm.iconTextButton(
            annotation="Pin Selected UVs",
            command=lambda *args: core.pinUVs(0),
            image1=iconDict["pin"],
            label="Pin Selected UVs",
            parent=grp2Layout,
        )
        grp2btn3 = pm.iconTextButton(
            annotation="Unpin Selected UVs",
            command=lambda *args: core.pinUVs(1),
            image1=iconDict["unpin"],
            label="Unpin Selected UVs",
            parent=grp2Layout,
        )
        grp2btn4 = pm.iconTextButton(
            annotation="Unpin All UVs (Left Click) --- Invert All Pins (Right Click)",
            command=lambda *args: core.pinUVs(2),
            image1=iconDict["unpinAll"],
            label="Unpin All UVs (Left Click) --- Invert All Pins (Right Click)",
            parent=grp2Layout,
        )
        grp2btn4Pop = pm.popupMenu( # Invert
            button=3,
            parent=grp2btn4,
            postMenuCommand=lambda *args: core.pinUVs(3),
        )

        # Pop template from stack
        pm.setUITemplate(popTemplate=True)
        
        # Build list of elements in group 2
        grp2Elements = [grp2btn1, grp2btn2, grp2btn3, grp2btn4]
        
        # Layout the icons in grp2Layout
        pm.formLayout(
            grp2Layout, edit=True,
            attachForm=[
                (grp2btn1, "top", tBarT),
                (grp2btn1, "left", tBarL),
                (grp2btn2, "top", tBarT),
                (grp2btn3, "top", tBarT),
                (grp2btn4, "top", tBarT),
                (grp2btn4, "right", tBarR),
            ],
            attachControl=[
                (grp2btn2, "left", tBarH, grp2btn1),
                (grp2btn3, "left", tBarH, grp2btn2),
                (grp2btn4, "left", tBarH, grp2btn3),
            ]
        )


    ## Selections group 
    
    pm.setParent('..') # Set default parent to one step up
    
    # Group 3 form (Selections)
    grp3Layout = pm.formLayout()
    
    # Group 3 elements list +toggle
    grp3Elements = []
    grp3Toggle = pm.iconTextButton(
        annotation="Show/Hide the Selection Icons",
        command=lambda *args: core.topBarToggle(3, grp3Toggle, grp3Elements, grp3Layout),
        image1=iconDict["barIconOpen"],
        parent=grp3Layout,
        visible=True,
    )
    
    # Push template into stack for the icon btns
    pm.setUITemplate("toolbarBtnTemplate", pushTemplate=True)
    
    # Group 3 icons
    grp3btn1 = pm.iconTextButton(
        annotation="Select Shortest Edge Path Tool",
        command=lambda *args: pm.setToolTo("polyShortestEdgePathContext"),
        commandRepeatable=True,
        image1=iconDict["pathTool"],
        label="Select Shortest Edge Path Tool",
        parent=grp3Layout,
    )
    grp3btn2 = pm.iconTextButton(
        annotation="Expand the Active Selection to Entire Shell(s)",
        command=lambda *args: pm.runtime.SelectUVShell(),
        commandRepeatable=True,
        image1=iconDict["shell"],
        label=("Expand the Active Selection to Entire Shell(s)"), 
        parent=grp3Layout,
    )
    grp3btn3 = pm.iconTextButton(
        annotation="Convert UV Selection to Border UVs",
        command=lambda *args: [ pm.runtime.ConvertSelectionToUVs(), pm.runtime.SelectUVBorder() ],
        commandRepeatable=True,
        image1=iconDict["border"],
        label="Convert UV Selection to Border UVs",
        parent=grp3Layout,
    )
    grp3btn4 = pm.iconTextButton(
        annotation="Harden/Soften all Shell Borders",
        command=lambda *args: core.hardSoftShellBorders(),
        commandRepeatable=True,
        image1=iconDict["softhard"],
        label="Harden/Soften all Shell Borders",
        parent=grp3Layout,
    )
    grp3btn5 = pm.iconTextButton(
        annotation="Grow Selection",
        command=lambda *args: pm.runtime.GrowPolygonSelectionRegion(),
        commandRepeatable=True,
        image1=iconDict["grow"],
        label="Grow Selection",
        parent=grp3Layout,
    )
    grp3btn6 = pm.iconTextButton(
        annotation="Shrink Selection",
        command=lambda *args: pm.runtime.ShrinkPolygonSelectionRegion(),
        commandRepeatable=True,
        image1=iconDict["shrink"],
        label="Shrink Selection",
        parent=grp3Layout,
    )
    grp3btn7 = pm.iconTextButton(
        annotation="Invert Selection",
        command=lambda *args: pm.runtime.InvertSelection(),
        commandRepeatable=True,
        image1=iconDict["invert"],
        label="Invert Selection",
        parent=grp3Layout,
    )
    grp3btn8 = pm.iconTextButton(
        annotation="Load* Selection (Left Click) --- *Save (Right Click)", 
        command=lambda *args: core.selectionVar("load", "A"),
        commandRepeatable=True,
        image1=iconDict["selectA"],
        label="Load Selection (Variable A)",
    )
    grp3btn8Pop = pm.popupMenu(
        button=3,
        postMenuCommand=lambda *args: core.selectionVar("save", "A"),
        parent=grp3btn8,
    )
    grp3btn9 = pm.iconTextButton(
        annotation="Load* Selection (Left Click) --- *Save (Right Click)", 
        command=lambda *args: core.selectionVar("load", "B"),
        commandRepeatable=True,
        image1=iconDict["selectB"],
        label="Save Selection (Variable A)",
    )
    grp3btn9Pop = pm.popupMenu(
        button=3,
        postMenuCommand=lambda *args: core.selectionVar("save", "B"),
        parent=grp3btn9,
    )

    # Pop template from stack
    pm.setUITemplate(popTemplate=True)
    
    # Build list of elements in group 3
    grp3Elements = [grp3btn1, grp3btn2, grp3btn3, grp3btn4]
    
    # Layout the icons in grp3Layout
    pm.formLayout(
        grp3Layout, edit=True,
        attachForm=[
            (grp3btn1, "top", tBarT),
            (grp3btn1, "left", tBarL),
            (grp3btn2, "top", tBarT),
            (grp3btn3, "top", tBarT),
            (grp3btn4, "top", tBarT),
            (grp3btn5, "top", tBarT),
            (grp3btn6, "top", tBarT),
            (grp3btn7, "top", tBarT),
            (grp3btn8, "top", tBarT),
            (grp3btn9, "top", tBarT),
            (grp3btn9, "right", tBarR),
        ],
        attachControl=[
            (grp3btn2, "left", tBarH, grp3btn1),
            (grp3btn3, "left", tBarH, grp3btn2),
            (grp3btn4, "left", tBarH, grp3btn3),
            (grp3btn5, "left", tBarH, grp3btn4),
            (grp3btn6, "left", tBarH, grp3btn5),
            (grp3btn7, "left", tBarH, grp3btn6),
            (grp3btn8, "left", tBarH, grp3btn7),
            (grp3btn9, "left", tBarH, grp3btn8),
        ]
    )

    
    ## Isolate select group
    
    pm.setParent('..') # Set default parent to one step up

    # Group 4 form (Isolate select)
    grp4Layout = pm.formLayout()
    
    # Group 4 elements list +toggle
    grp4Elements = []
    grp4Toggle = pm.iconTextButton(
        annotation="Show/Hide the Isolate Selection Icons",
        command=lambda *args: core.topBarToggle(4, grp4Toggle, grp4Elements, grp4Layout),
        image1=iconDict["barIconOpen"],
        parent=grp4Layout,
        visible=True,
    )

    # Group 4 icons
    grp4btn1 = pm.iconTextCheckBox(
        topBtnIso, 
        annotation="Toggle Isolate Select Mode",
        changeCommand=lambda *args: core.updateDisplay(13, 0, grp4btn1),
        image1=iconDict["isoToggle"],
        label="Toggle Isolate Select Mode",
        parent=grp4Layout,
    )

    # Push template into stack for the icon btns
    pm.setUITemplate("toolbarBtnTemplate", pushTemplate=True)

    grp4btn2 = pm.iconTextButton(
        annotation="Add the Selected UVs to the Isolate Select Set",
        ## command=lambda *args: core.isoSelectUVs(1),
        command=lambda *args: [core.checkSel("comps"), pm.mel.textureEditorIsolateSelect(1)],
        image1=iconDict["isoAdd"],
        label="Add the Selected UVs to the Isolate Select Set",
        parent=grp4Layout,
    )    
    grp4btn3 = pm.iconTextButton(
        annotation="Remove the Selected UVs from the Isolate Select Set",
        ## command=lambda *args: core.isoSelectUVs(2),
        command=lambda *args: [core.checkSel("comps"), pm.mel.textureEditorIsolateSelect(2)],
        image1=iconDict["isoSub"],
        label="Remove Selected UVs from the Isolate Select Set",
        parent=grp4Layout, 
    )
    grp4btn4 = pm.iconTextButton(
        annotation="Remove all UVs from the Isolate Select Set",
        ## command=lambda *args: core.isoSelectUVs(0),
        command=lambda *args: pm.mel.textureEditorIsolateSelect(0), 
        image1=iconDict["isoReset"],
        label="Remove all UVs from the Isolate Select Set",
        parent=grp4Layout,
    )
    
    # Pop template from stack
    pm.setUITemplate(popTemplate=True)
    
    # Build list of elements in group 3
    grp4Elements = [grp4btn1, grp4btn2, grp4btn3, grp4btn4]
    
    # Layout the icons in grp4Layout
    pm.formLayout(
        grp4Layout, edit=True,
        attachForm=[
            (grp4btn1, "top", tBarT),
            (grp4btn1, "left", tBarL),
            (grp4btn2, "top", tBarT),
            (grp4btn3, "top", tBarT),
            (grp4btn4, "top", tBarT),
            (grp4btn4, "right", tBarR),
        ],
        attachControl=[
            (grp4btn2, "left", tBarH, grp4btn1),
            (grp4btn3, "left", tBarH, grp4btn2),
            (grp4btn4, "left", tBarH, grp4btn3),
        ]
    )


    ## Copy/Paste/Del group

    pm.setParent('..') # Set default parent to one step up

    # Group 5 form (Copy/Paste/Delete UVs)
    grp5Layout = pm.formLayout()

    # Group 5 elements list +toggle
    grp5Elements = []
    grp5Toggle = pm.iconTextButton(
        annotation="Show/Hide the Copy/Paste/Delete UV Icons",
        command=lambda *args: core.topBarToggle(5, grp5Toggle, grp5Elements, grp5Layout),
        image1=iconDict["barIconOpen"],
        parent=grp5Layout,
        visible=True,
    )
    
    # Push template into stack for the icon btns
    pm.setUITemplate("toolbarBtnTemplate", pushTemplate=True)
    
    # Group 5 icons
    grp5btn1 = pm.iconTextButton(
        annotation="Copy Coordinate(s) of the Selected UV or Face",
        command=lambda *args: core.copyPasteUV(0),
        commandRepeatable=True,
        image1=iconDict["copyUV"],
        label="Copy Coordinate(s) of the Selected UV or Face",
        parent=grp5Layout,
    )    
    grp5btn2 = pm.iconTextButton(
        annotation="Paste Coordinate(s) of the Selected UV or Face",
        command=lambda *args: core.copyPasteUV(1),
        commandRepeatable=True,
        image1=iconDict["pasteUV"],
        label="Paste Coordinate(s) of the Selected UV or Face",
        parent=grp5Layout,
    )        
    grp5btn3 = pm.iconTextButton(
        annotation="Delete Selected UVs from the Active UV Set",
        command=lambda *args: core.deleteUVs(),
        commandRepeatable=True,
        image1=iconDict["delUV"],
        label="Delete Selected UVs from the Active UV Set",
        parent=grp5Layout,
    )
    
    # Pop template from stack
    pm.setUITemplate(popTemplate=True)
    
    # Build list of elements in group 5
    grp5Elements = [grp5btn1, grp5btn2, grp5btn3]
    
    # Layout the icons in grp5Layout
    pm.formLayout(
        grp5Layout, edit=True,
        attachForm=[
            (grp5btn1, "top", tBarT),
            (grp5btn1, "left", tBarL),
            (grp5btn2, "top", tBarT),
            (grp5btn3, "top", tBarT),
            (grp5btn3, "right", tBarR),
        ],
        attachControl=[
            (grp5btn2, "left", tBarH, grp5btn1),
            (grp5btn3, "left", tBarH, grp5btn2),
        ]
    )
  

## Menubar

# Creates the menu bar
def createMenubar(txtEditor):
    
    # Create the Polygons sub menu.
    pm.menu(
        (txtEditor + "EditMenu"), 
            allowOptionBoxes=True,
            familyImage="menuIconEdit.png", 
            label="Polygons", 
            tearOff=True, 
        )
    createEditMenu((txtEditor + "EditMenu"), True)

    # Create the View sub menu.
    pm.menu(
        (txtEditor + "ViewMenu"),
            allowOptionBoxes=True,
            familyImage="menuIconView.png",
            label="View",
            tearOff=True,
        )  
    createViewMenu((txtEditor + "ViewMenu"), True)
    
    # Create the Select sub menu
    pm.menu(
        (txtEditor + "SelectMenu"), 
            allowOptionBoxes=True,
            familyImage="menuIconSelect.png", 
            label="Select", 
            tearOff=True, 
        )
    createSelectMenu((txtEditor + "SelectMenu"), txtEditor, True)
    
    # Create the Tool sub menu
    pm.menu(
        (txtEditor + "ToolMenu"), 
            allowOptionBoxes=True,
            label="Tool",
            tearOff=True, 
        )
    createToolMenu((txtEditor + "ToolMenu"), True)
    
    # Create the Image sub menu
    pm.menu(
        (txtEditor + "DisplayMenu"), 
            allowOptionBoxes=True,
            familyImage="menuIconImages.png", 
            label="Display", 
            tearOff=True, 
        )
    createDisplayMenu((txtEditor + "DisplayMenu"), txtEditor, True)
    
    # Create the Textures sub menu
    pm.menu(
        (txtEditor + "TexturesMenu"), 
            allowOptionBoxes=False,
            label="Textures", 
            tearOff=True, 
        )
    pm.menu(
        (txtEditor + "TexturesMenu"), edit=True, 
            postMenuCommand=lambda *args: createTexturesMenu((txtEditor + "TexturesMenu"), txtEditor, True)
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    # Create UV set sub menu
    pm.menu(
        (txtEditor + "UVSetsMenu"), 
            allowOptionBoxes=False,
            label="UV Sets", 
            tearOff=True, 
        )        
    pm.menu(
        (txtEditor + "UVSetsMenu"), edit=True, 
            postMenuCommand=lambda *args: createUVSetsMenu((txtEditor + "UVSetsMenu"), txtEditor, True)
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    # Create the NSUV sub menu
    pm.menu(
        (txtEditor + "NSUVMenu"), 
            allowOptionBoxes=False,
            label="NSUV", 
            tearOff=True, 
        )
    createNSUVMenu((txtEditor + "NSUVMenu"), True)
    
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


## Menubar: Menues

# Creates the Polygons menu
def createEditMenu(parentMenu, menuBar):

    pm.setParent(parentMenu, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"
    
    # Create menu items
    
    # Copy/Paste/Del UVs
    pm.menuItem(
        ("menuEditCopyUVs" + suffix), 
            annotation="Copy Coordinate(s) of the Selected UV or Face",
            command=lambda *args: core.copyPasteUV(0),
            enableCommandRepeat=True,
            image=iconDict["copyUV"],
            label="Copy UVs",
        )
    pm.menuItem(
        ("menuEditPasteUVs" + suffix), 
            annotation="Paste Coordinate(s) of the Selected UV or Face",
            command=lambda *args: core.copyPasteUV(1),
            enableCommandRepeat=True,
            image=iconDict["pasteUV"],
            label="Paste UVs",
        )
    pm.menuItem(
        ("menuEditDelUVs" + suffix), 
            annotation="Delete Selected UVs from the Active UV Set",
            command=lambda *args: core.deleteUVs(),
            enableCommandRepeat=True,
            image=iconDict["delUV"],
            label="Delete UVs",
        )
        
    pm.menuItem(divider=True)
    
    # UV Sets
    pm.menuItem(
        ("menuEditCreateSet" + suffix), 
            annotation="Create Empty UV Set",
            command=lambda *args: core.createSet(scrollListUVSet),
            enableCommandRepeat=True, 
            image=iconDict["uvSetNew"],
            label="Create Empty UV Set",
        )
    pm.menuItem(
        ("menuEditCopySet" + suffix), 
            annotation="Copy the selected UVs to another UV set", 
            label="Copy UVs to UV Set", 
            image=iconDict["uvSetCopy"],
            subMenu=True, 
            tearOff=True, 
        )
    pm.menu(
        ("menuEditCopySet" + suffix), edit=True, 
            postMenuCommand=lambda *args: createPopupCopySet(("menuEditCopySet" + suffix)),
        )    
    
    pm.setParent(parentMenu, menu=True) # Parent up submenu

    pm.menuItem(
        ("menuEditSetSet" + suffix), 
            annotation="Set the current UV set on selected objects", 
            command=lambda *args: core.setCurrentSet(scrollListUVSet), 
            enableCommandRepeat=True, 
            image="polySetCurrentUVSet.png", 
            label="Set Current UV Set...",
        )
    pm.menuItem(
        ("menuEditRenameSet" + suffix), 
            annotation="Rename the current UV set on selected objects", 
            command=lambda *args: renameSetUI(scrollListUVSet), 
            enableCommandRepeat=True, 
            image="polyRenameUVSet.png", 
            label="Rename Current UV Set...",
        )
    pm.menuItem(
        ("menuEditDelSet" + suffix), 
            annotation="Delete the current UV set on selected objects", 
            command=lambda *args: core.deleteSet(scrollListUVSet), 
            enableCommandRepeat=True, 
            image="polyDeleteUVSet.png", 
            label="Delete Current UV Set",
        )
        
    pm.menuItem(divider=True)
    
    # Normalize UVs
    pm.menuItem(
        ("menuEditNormalize" + suffix), 
            annotation="Normalize the Selected Shells (Left Click) --- Normalize Options (Right Click)",
            command=lambda *args: core.normalizeShells(0),
            enableCommandRepeat=True, 
            image=iconDict["normalize"],
            label="Normalize",
        )
    pm.menuItem(
        ("menuEditNormalizeOpt" + suffix), 
            annotation="Normalize (Options)",
            command=lambda *args: normalizeUI(),
            enableCommandRepeat=False, 
            optionBox=True, 
        )
    pm.menuItem(
        ("menuEditUnitize" + suffix), 
            annotation="Unitize the Selected Shells. All selected faces will be moved to fit into the default 0 -> 1 UV range.",
            command=lambda *args: core.normalizeShells(5),
            image="polyUnitizeUVs.png",
            enableCommandRepeat=True, 
            label="Unitize",
        )
    pm.menuItem(
        ("menuEditUnitizeOpt" + suffix), 
            annotation="Normalize (Options)",
            command=lambda *args: normalizeUI(), 
            enableCommandRepeat=False, 
            optionBox=True, 
        )
        
    # Layout rectangle
    pm.menuItem(
        ("menuEditLayoutRect" + suffix), 
            annotation="Layout the rectangle of polys bounded by two vertices with unitized UVs",
            command=lambda *args: pm.Runtime.LayoutUVRectangle(),
            enableCommandRepeat=True, 
            image="polyUVRectangle.png", 
            label="Layout rectangle", 
        )
        
    pm.menuItem(divider=True)
    
    # UV cycling
    pm.menuItem(
        ("menuEditCycleUV" + suffix), 
            annotation="Cycles the UVs of the selected face counter clockwise", 
            command=lambda *args: pm.mel.polyRotateUVsByVertex(), 
            enableCommandRepeat=True, 
            image="cycleUVs.png", 
            label="Cycle UVs",
        )
        
    # Best plane projection
    pm.menuItem(
        ("menuEditBestPlane" + suffix), 
            annotation="Create UVs by computing the best fitting plane", 
            command=lambda *args: pm.setToolTo("polyBestPlaneTexturingContext"), 
            enableCommandRepeat=True, 
            image="bestPlaneTxt.png", 
            label="Best Plane Texturing Tool",
        )
        
    pm.menuItem(divider=True)
    
    # Grid
    pm.menuItem(
        ("menuEditGrid" + suffix), 
            annotation="Snap the selected UVs to the user specified grid",
            command=lambda *args: core.snapToUserGrid(),
            image=iconDict["gridSnap"],
            label="Snap to Grid",
        )
    pm.menuItem(
        ("menuEditGridOpt" + suffix), 
            command=lambda *args: gridOptions(),
            optionBox=True, 
        )
        
    # Warp texture editor image
    pm.menuItem(
        ("menuEditWarpImage" + suffix), 
            annotation="Warp selected poly object",
            command=lambda *args: pm.mel.performPolyWarpImage(0), 
            echoCommand=True,
            image="polyWarpImage.png", 
            label="Warp Image", 
        )
    pm.menuItem(
        ("menuEditWarpImageOpt" + suffix), 
            annotation="Warp image options",
            command=lambda *args: pm.mel.performPolyWarpImage(1), 
            image="polyWarpImage.png", 
            optionBox=True, 
        )
        
    pm.menuItem(divider=True)
    
    # Map/Straighten UV border
    pm.menuItem(
        ("menuEditMapBorder" + suffix), 
            annotation="Map the texture border indicated by selected UV to specified shape", 
            command=lambda *args: pm.mel.performPolyUntangleUV("map", 0), 
            enableCommandRepeat=True, 
            image="polyMapUVBorder.png", 
            label="Map UV Border",
        )
        
    pm.menuItem(
        ("menuEditMapBorderOpt" + suffix), 
            annotation="Map UV border options", 
            command=lambda *args: pm.mel.performPolyUntangleUV("map", 1), 
            enableCommandRepeat=False, 
            image="polyMapUVBorder.png",
            optionBox=True, 
        )
        
    pm.menuItem(
        ("menuEditStrUVBorder" + suffix), 
            annotation="Select 2 consecutive UVs and a third one to define the border to be straightened", 
            command=lambda *args: pm.mel.performPolyStraightenUV(0), 
            image="polyStraightenUVBorder.png", 
            label="Straighten UV Border",
        )
        
    pm.menuItem(
        ("menuEditStrUVBorderOpt" + suffix), 
            annotation="Straighten UV border options", 
            command=lambda *args: pm.mel.performPolyStraightenUV(1), 
            enableCommandRepeat=False, 
            image="polyStraightenUVBorder.png",
            optionBox=True, 
        )

    pm.menuItem(divider=True)
    
    # Optimize/Relax
    pm.menuItem(
        ("menuEditOptimize" + suffix), 
            annotation="Automatically move UVs for better texture space distribution",
            command=lambda *args: core.relaxUVs(),
            enableCommandRepeat=True, 
            image=iconDict["optimize"],
            label="Relax/Optimize", 
        )
    pm.menuItem(
        ("menuEditOptimizeOpt" + suffix), 
            annotation="Optimize UVs options", 
            command=lambda *args: relaxUI(),
            enableCommandRepeat=False, 
            image="polyRelaxUVShell.png",
            optionBox=True, 
        )
        
    # Unfold
    pm.menuItem(
        ("menuEditUnfold" + suffix), 
            annotation="Select a poly object or UVs to be unfolded",
            command=lambda *args: core.unfoldUVs(),
            image=iconDict["unfold"],
            label="Unfold", 
        )
    pm.menuItem(
        ("menuEditUnfoldOpt" + suffix), 
            annotation="Unfold options",
            command=lambda *args: unfoldUI(),
            enableCommandRepeat=False,
            optionBox=True, 
        )

    # Layout
    if mayaVer == 201650: # Duplicate entry only to highlight the new layout UV features in Maya 2016 EXT2 - Flag also bugs in 2015
        pm.menuItem(
            ("menuEditLayout" + suffix),
                annotation="Select faces to be moved in UV space", 
                command=lambda *args: core.layoutUVs(),
                image=iconDict["layout"],
                label="Layout",
                version=2017,
            )
    else:
        pm.menuItem(
            ("menuEditLayout" + suffix), 
                annotation="Select faces to be moved in UV space", 
                command=lambda *args: core.layoutUVs(),
                image=iconDict["layout"],
                label="Layout",
            )
    pm.menuItem(
        ("menuEditLayoutOpt" + suffix), 
            annotation="Layout options", 
            command=lambda *args: layoutUI(),
            enableCommandRepeat=False, 
            optionBox=True, 
        )
        
    pm.menuItem(divider=True)
    
    # Pinning
    if mayaVer >= 201600:
        pm.menuItem(
            ("menuEditUnpinAll" + suffix), 
                annotation="Unpin all pinned UVs",
                command=lambda *args: core.pinUVs(2),
                enableCommandRepeat=True,
                image=iconDict["unpinAll"],
                label="Unpin All",
                version="2016",
            )
        pm.menuItem(
            ("menuEditInvertPin" + suffix), 
                annotation="Unpin all pinned UVs, and pin previously unpinned UVs",
                command=lambda *args: core.pinUVs(3),
                enableCommandRepeat=True,
                label="Invert Pin",
                version="2016",
            )
        pm.menuItem(
            ("menuEditPin" + suffix), 
                annotation="Pin selection's UVs", 
                command=lambda *args: core.pinUVs(0),
                enableCommandRepeat=True, 
                image=iconDict["pin"],
                label="Pin Selection",
                version="2016", 
            )
        pm.menuItem(
            ("menuEditUnpin" + suffix), 
                annotation="Unpin selection's UVs", 
                command=lambda *args: core.pinUVs(1),
                enableCommandRepeat=True, 
                image=iconDict["unpin"],
                label="Unpin Selection",
                version="2016", 
            )

        pm.menuItem(divider=True)
    if mayaVer >= 201650:
        pm.menuItem(
            ("menuEditAutoSeam" + suffix), 
                annotation="Auto Seams", 
                command=lambda *args: core.autoSeams(),
                enableCommandRepeat=True,
                # image="polyAutoSeams.png",
                label="Auto Seams",
                version=2017,
            )
        pm.menuItem(
            ("menuEditAutoSeamOpt" + suffix), 
                annotation="Auto Seams options", 
                command=lambda *args: autoSeamsUI(),
                enableCommandRepeat=False, 
                optionBox=True, 
            )

    pm.menuItem(
        ("menuEditCut" + suffix), 
            annotation="Separate the UVs along the selected edges", 
            command=lambda *args: core.cutSewUVs("cut"),
            enableCommandRepeat=True, 
            image=iconDict["cut"],
            label="Cut UV Edges",
        )
    # Cut and sew
    pm.menuItem(
        ("menuEditSplit" + suffix), 
            annotation="Separate the selected UV into one for each connected edge", 
            command=lambda *args: core.cutSewUVs("split"),
            enableCommandRepeat=True, 
            image=iconDict["split"],
            label="Split UVs",
    )
    
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuEditCreateShell" + suffix), 
                annotation="Create UV shell along the selection border",
                command=lambda *args: core.createShell(),
                enableCommandRepeat=True, 
                image=iconDict["createShell"],
                label="Create UV Shell", 
                version="2015", 
            )
        
    pm.menuItem(
        ("menuEditSew" + suffix), 
            annotation="Sew the UVs together along the selected edges", 
            command=lambda *args: core.cutSewUVs("sew"),
            enableCommandRepeat=True, 
            image=iconDict["sew"],
            label="Sew UV Edges",
        )
    pm.menuItem(
        ("menuEditMoveSew" + suffix), 
            annotation="Select edges to be moved and merged", 
            command=lambda *args: core.cutSewUVs("moveSew"),
            image=iconDict["moveSew"],
            label="Move and Sew UV Edges",
        )
    pm.menuItem(
        ("menuEditMerge" + suffix), 
            annotation="Select UVs to be merged", 
            command=lambda *args: pm.mel.performPolyMergeUV(0), 
            image="polyMergeUV.png", 
            label="Merge UVs",
        )
    pm.menuItem(
        ("menuEditMergeOpt" + suffix), 
            annotation="Merge UVs options", 
            command=lambda *args: pm.mel.performPolyMergeUV(1), 
            enableCommandRepeat=False, 
            image="polyMergeUV.png",
            optionBox=True, 
        )

    pm.menuItem(divider=True)
    
    # Snapshot
    pm.menuItem(
        ("menuEditSnapshot" + suffix), 
            annotation="Draws the UVs into an image", 
            command=lambda *args: snapshotUI(), 
            image=iconDict["uvSetSnapshot"],
            label="UV Snapshot...",
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the View menu
def createViewMenu(parentMenu, menuBar):    
    
    pm.setParent(parentMenu, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    # Create menuItems 
    pm.menuItem(
        ("menuViewContainedFaces" + suffix), 
            checkBox=pm.optionVar["containedFaces_NSUV"], 
            command=lambda *args: core.updateDisplay(15, 0), 
            label="View Contained Faces",
        )
    pm.menuItem(
        ("menuViewConnectedFaces" + suffix), 
            checkBox=pm.optionVar["connectedFaces_NSUV"] , 
            command=lambda *args: core.updateDisplay(16, 0), 
            label="View Connected Faces",
        )
    pm.menuItem(
        ("menuViewFaces" + suffix), 
            checkBox=pm.optionVar["viewFaces_NSUV"], 
            command=lambda *args: core.updateDisplay(17, 0), 
            label="View Faces of Selected Images",
        )
    pm.menuItem(
        ("menuViewIso" + suffix), 
            label="Isolate Select",
            subMenu=True, 
            tearOff=True, 
        )
    pm.menuItem(
        ("menuViewIsoSelect" + suffix), 
            annotation="Toggle Isolate Select Mode", 
            checkBox=pm.optionVar["isoSelect_NSUV"], 
            command=lambda *args: core.updateDisplay(13, 0), 
            label="View Set",
        )
    pm.menuItem(
        ("menuViewIsoAdd" + suffix), 
            annotation="Add the Selected UVs to the Isolate Select Set", 
            ## command=lambda *args: core.isoSelectUVs(1),
            command=lambda *args: [core.checkSel("comps"), pm.mel.textureEditorIsolateSelect(1)],
            label="Add Selected",
        )
    pm.menuItem(
        ("menuViewIsoRemove" + suffix), 
            annotation="Remove the Selected UVs from the Isolate Select Set", 
            ## command=lambda *args: core.isoSelectUVs(2),
            command=lambda *args: [core.checkSel("comps"), pm.mel.textureEditorIsolateSelect(2)],
            label="Remove Selected",
        )
    pm.menuItem(
        ("menuViewIsoReset" + suffix), 
            annotation="Remove all UVs from the Isolate Select Set", 
            ## command=lambda *args: core.isoSelectUVs(0),
            command=lambda *args: pm.mel.textureEditorIsolateSelect(0), 
            label="Remove All",
        )        
    pm.setParent(parentMenu, menu=True) # Parent up submenu
    
    pm.menuItem(divider=True) # Menu divider
    
    pm.menuItem(
        ("menuViewToolbar" + suffix), 
            annotation="Toggle the display of the toolbar", 
            checkBox=pm.optionVar["toolbarState_NSUV"], 
            command=lambda *args: core.updateDisplay(20, 0), 
            enableCommandRepeat=False,
            label="Toolbar",
        )
    
    pm.menuItem(divider=True) # Menu divider
    
    # Frame options
    pm.menuItem(
        ("menuViewFrameAll" + suffix), 
            command=lambda *args: pm.runtime.FrameAll(), 
            label="Frame All",
        )
    pm.menuItem(
        ("menuViewFrameSel" + suffix), 
            command=lambda *args: pm.runtime.FrameSelected(), 
            label="Frame Selection",
        )
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the selection menu
def createSelectMenu(parentMenu, txtEditor, menuBar):
    
    pm.setParent(parentMenu, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    # Create menu items
    pm.menuItem(
        ("menuEditSelVarALoad" + suffix), 
            annotation="Load Selection (Variable A)", 
            command=lambda *args: core.selectionVar("load", "A"),
            enableCommandRepeat=True, 
            label="Load Selection (Variable A)",
        )
    pm.menuItem(
        ("menuEditSelVarBLoad" + suffix), 
            annotation="Load Selection (Variable B)", 
            command=lambda *args: core.selectionVar("load", "B"),
            enableCommandRepeat=True, 
            label="Load Selection (Variable B)",
        )
    pm.menuItem(
        ("menuEditSelVarASave" + suffix), 
            annotation="Save Selection (Variable A)", 
            command=lambda *args: core.selectionVar("save", "A"),
            enableCommandRepeat=True, 
            label="Save Selection (Variable A)",
        )
    pm.menuItem(
        ("menuEditSelVarBSave" + suffix), 
            annotation="Save Selection (Variable B)", 
            command=lambda *args: core.selectionVar("save", "B"),
            enableCommandRepeat=True, 
            label="Save Selection (Variable B)",
        )

    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuSelConvertToContEdges" + suffix), 
            command=lambda *args: pm.mel.PolySelectConvert(20), 
            label="Convert to Contained Edges",
        )
    pm.menuItem(
        ("menuSelConvertToEdges" + suffix), 
            command=lambda *args: pm.mel.PolySelectConvert(2), 
            label="Convert to Edges",
        )
    pm.menuItem(
        ("menuSelConvertToEdgeLoop" + suffix), 
            command=lambda *args: pm.polySelectSp(loop=True), 
            label="Convert to Edge Loop",
        )  
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuSelConvertToEdgePerim" + suffix), 
                version="2015", 
                command=lambda *args: pm.runtime.ConvertSelectionToEdgePerimeter(), 
                label="Convert to Edge Perimeter",
            )
    pm.menuItem(
        ("menuSelConvertToEdgeRing" + suffix), 
            command=lambda *args: pm.polySelectSp(ring=True), 
            label="Convert to Edge Ring",
        ) 
            
    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuSelConvertToContFaces" + suffix), 
            # command=lambda *args: pm.textureWindow(txtEditor, edit=True, selectInternalFaces=True),
            command=lambda *args: core.selectConvert(5, txtEditor),
            label="Convert to Contained Faces",
        )
    pm.menuItem(
        ("menuSelConvertToConnFaces" + suffix), 
            # command=lambda *args: pm.textureWindow(txtEditor, edit=True, selectRelatedFaces=True),
            command=lambda *args: core.selectConvert(6, txtEditor),
            label="Convert to Connected Faces",
        )
    pm.menuItem(
        ("menuSelConvertToFaces" + suffix), 
            command=lambda *args: pm.mel.PolySelectConvert(1), 
            label="Convert to Faces",
        )
    pm.menuItem(
        ("menuSelConvertToFacePath" + suffix), 
            command=lambda *args: pm.runtime.SelectFacePath(), 
            label="Convert to Face Path",
        ) 
        
    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuSelConvertToUVs" + suffix), 
            command=lambda *args: pm.mel.PolySelectConvert(4), 
            label="Convert to UVs",
        )       
    pm.menuItem(
        ("menuSelConvertToUVEdgeLoop" + suffix), 
            command=lambda *args: pm.mel.polySelectEdges("edgeUVLoopOrBorder"), 
            label="Convert to UV Edge Loop",
        )
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuSelConvertToUVPerim" + suffix), 
                version="2015", 
                command=lambda *args: pm.runtime.ConvertSelectionToUVPerimeter(), 
                label="Convert to UV Perimeter",
            ) 
    pm.menuItem(
        ("menuSelShell" + suffix), 
            annotation="Select UV shell(s) for active UV(s)",
            command=lambda *args: pm.runtime.SelectUVShell(), 
            label="Convert to UV Shell",
        )
    pm.menuItem(
        ("menuSelShellBorder" + suffix), 
            annotation="Select UV border(s) for active UV(s)", 
            command=lambda *args: pm.runtime.SelectUVBorder(), 
            label="Convert to UV Shell Border",
        )
        
    pm.menuItem(divider=True)
        
    pm.menuItem(
        ("menuSelConvertToVerts" + suffix), 
            command=lambda *args: pm.mel.PolySelectConvert(3), 
            label="Convert to Vertices",
        )
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuSelConvertToVertPerim" + suffix), 
                version="2015", 
                command=lambda *args: pm.runtime.ConvertSelectionToVertexPerimeter(), 
                label="Convert to Vertex Perimeter",
            )
            
    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuSelShortEdge" + suffix), 
            annotation="Shortest Edge Path Tool", 
            command=lambda *args: pm.setToolTo("polyShortestEdgePathContext"),
            label="Select Shortest Edge Path Tool",
        )

    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the tool menu
def createToolMenu(parentMenu, menuBar):

    pm.setParent(parentMenu, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    # Create menuItems    
    pm.menuItem(
        ("menuToolLattice" + suffix), 
            annotation="UV Lattice Tool", 
            command=lambda *args: core.uvContextTool(0, "lattice"),
            label="UV Lattice Tool",
        )         
    pm.menuItem(
        ("menuToolLatticeOpt" + suffix), 
            command=lambda *args: core.uvContextTool(0, "lattice", True),
            optionBox=True, 
        )
    pm.menuItem(
        ("menuToolSmudge" + suffix), 
            annotation="UV Smudge Tool", 
            command=lambda *args: core.uvContextTool(1, "smudge"),
            label="UV smudge tool",
        )
    pm.menuItem(
        ("menuToolSmudgeOpt" + suffix), 
            command=lambda *args: core.uvContextTool(1, "smudge", True),
            optionBox=True, 
        )
    pm.menuItem(
        ("menuToolMoveShell" + suffix), 
            annotation="Move UV Shell Tool", 
            command=lambda *args: core.uvContextTool(2, "move"),
            label="Move UV Shell Tool",
        )
    pm.menuItem(
        ("menuToolMoveShellOpt" + suffix), 
            command=lambda *args: core.uvContextTool(2, "move", True),
            label="Move UV Shell Tool Options",
            optionBox=True, 
        )
    pm.menuItem(
        ("menuToolSmooth" + suffix), 
            annotation="UV Smoothing Tool", 
            command=lambda *args: core.uvContextTool(3, "smooth"),
            label="Smooth UV Tool",
        )
    pm.menuItem(
        ("menuToolSmoothOpt" + suffix), 
            command=lambda *args: core.uvContextTool(3, "smooth", True),
            label="Smooth UV Tool Options",
            optionBox=True, 
        )
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuToolTweak" + suffix), 
                annotation="Tweak UV tool", 
                command=lambda *args: core.uvContextTool(4, "tweak"),
                label="Tweak UV tool",
                version="2015", 
            )
        pm.menuItem(
            ("menuToolTweakOpt" + suffix), 
                command=lambda *args: core.uvContextTool(4, "tweak", True),
                label="Tweak UV Tool Options",
                optionBox=True, 
                version="2015",
            )
        
    if mayaVer >= 201600:
        pm.menuItem(divider=True)        
        if pm.pluginInfo("Unfold3D", query=True, loaded=True):
            pm.menuItem(
                ("menuToolUnfold" + suffix), 
                    annotation="Unfold UV Tool: Unwrap a UV mesh", 
                    command=lambda *args: core.uvContextTool(5, "unfold"),
                    label="Unfold UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolUnfoldOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(5, "unfold", True),        
                    label="Unfold UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolOptimize" + suffix), 
                    annotation="Optimize UV Tool: Even out spacing between UVs", 
                    command=lambda *args: core.uvContextTool(5, "optimize"),
                    label="Optimize UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolOptimizeOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(5, "optimize", True),  
                    label="Optimize UV Tool Options",
                    optionBox=True, 
                )

    if mayaVer >= 201650:
        if pm.pluginInfo("modelingToolkit", query=True, loaded=True):
            pm.menuItem(
                ("menuToolSymmetrize" + suffix), 
                    annotation="Symmetrize UV Tool: Mirror UVs Across an Axis", 
                    command=lambda *args: core.uvContextTool(8, "symmetrize"),
                    label="Symmetrize UV Tool",
                    version="2017", 
                )
            pm.menuItem(
                ("menuToolSymmetrizeOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(8, "symmetrize", True),        
                    label="Symmetrize UV Tool Options",
                    optionBox=True, 
                )

    if mayaVer >= 201600:      
        if pm.pluginInfo("Unfold3D", query=True, loaded=True):
            pm.menuItem(
                ("menuToolCut" + suffix), 
                    annotation="Cut UV Tool: Cut UV edges", 
                    command=lambda *args: core.uvContextTool(6, "cut"),
                    label="Cut UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolCutOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(6, "cut", True),
                    label="Cut UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolSew" + suffix), 
                    annotation="Sew UV Tool: Sew UV edges", 
                    command=lambda *args: core.uvContextTool(6, "sew"),
                    label="Sew UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolSewOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(6, "sew", True),
                    label="Sew UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolGrab" + suffix), 
                    annotation="Grab UV Tool: Move UVs along a shell in any direction", 
                    command=lambda *args: core.uvContextTool(7, "grab"),
                    label="Grab UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolGrabOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(7, "grab", True),
                    label="Grab UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolPinch" + suffix), 
                    annotation="Pinch UV Tool: Sharpen soft UV edges", 
                    command=lambda *args: core.uvContextTool(7, "pinch"),
                    label="Pinch UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolPinchOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(7, "pinch", True),
                    label="Pinch UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolSmear" + suffix), 
                    annotation="Smear UV Tool: Pull the surface in the directon of your stroke", 
                    command=lambda *args: core.uvContextTool(7, "smear"),
                    label="Smear UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolSmearOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(7, "smear", True),
                    label="Smear UV Tool Options",
                    optionBox=True, 
                )
            pm.menuItem(
                ("menuToolPin" + suffix), 
                    annotation="Pin UV Tool: Paint areas of a surface to prevent further modification", 
                    command=lambda *args: core.uvContextTool(7, "pin"),
                    label="Pin UV Tool",
                    version="2016", 
                )
            pm.menuItem(
                ("menuToolPinOpt" + suffix), 
                    command=lambda *args: core.uvContextTool(7, "pin", True),
                    label="Pin UV Tool Options",
                    optionBox=True, 
                )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the display menu
def createDisplayMenu(parentMenu, txtEditor, menuBar):
    
    pm.setParent(parentMenu, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    # Create menuItems 
    pm.menuItem(
        ("menuDisplaySettings" + suffix), 
            command=lambda *args: dispSettingsUI(),
            label="Settings",
        )  
    pm.menuItem(divider=True)
    pm.menuItem(
        ("menuDisplayTxt" + suffix), 
            checkBox=pm.optionVar["imgDisp_NSUV"],
            command=lambda *args: core.updateDisplay(0, 0), 
            label="Texture",
        )
    pm.menuItem(
        ("menuDisplayDim" + suffix), 
            checkBox=pm.optionVar["imgDim_NSUV"],
            command=lambda *args: core.updateDisplay(1, 0), 
            label="Dim Texture",
        )
    pm.menuItem(
        ("menuDisplayShade" + suffix), 
            checkBox=pm.optionVar["shellShade_NSUV"],
            command=lambda *args: core.updateDisplay(2, 0), 
            label="Shaded UVs",
        )     
    pm.menuItem(
        ("menuDisplayBorder" + suffix), 
            checkBox=pm.optionVar["shellBorder_NSUV"],
            command=lambda *args: core.updateDisplay(3, 0), 
            label="Shell Borders",
        )
    pm.menuItem(
        ("menuDisplayDist" + suffix), 
            checkBox=pm.optionVar["shellDist_NSUV"],
            command=lambda *args: core.updateDisplay(4, 0), 
            label="Distortion",
        )
    pm.menuItem(
        ("menuDisplayCheckers" + suffix), 
            checkBox=pm.optionVar["checkers_NSUV"],
            command=lambda *args: core.updateDisplay(5, 0), 
            label="Checkers",
        )
    if mayaVer >= 201500:
        pm.menuItem(
            ("menuDisplayLabels" + suffix), 
                annotation="Show texture tile labels on/off", 
                checkBox=pm.optionVar["tileLabels_NSUV"], 
                command=lambda *args: core.updateDisplay(14, 0), 
                label="Tile Labels",
                version="2015", 
        )
    pm.menuItem(
        ("menuDisplayFilter" + suffix), 
            checkBox=pm.optionVar["imgFilter_NSUV"],
            command=lambda *args: core.updateDisplay(6, 0), 
            label="Filtered",
        )

    pm.menuItem(divider=True)
    
    pm.menuItem(
        ("menuDisplayRGB" + suffix), 
            command=lambda *args: core.updateDisplay(7, 0), 
            label="RGB Channels",
        )
    pm.menuItem(
        ("menuDisplayA" + suffix), 
            command=lambda *args: core.updateDisplay(7, 1), 
            label="Alpha Channel",
        )
    pm.menuItem(divider=True)
    
    pm.menuItem(
        ("menuDisplayGrid" + suffix), 
            annotation="Show grid on/off", 
            checkBox=pm.optionVar["gridDisp_NSUV"], 
            command=lambda *args: core.updateDisplay(8, 0), 
            label="Grid",
        )
    pm.menuItem(
        ("menuDisplayGridOpt" + suffix), 
            annotation="Grid options",
            command=lambda *args: pm.mel.performTextureViewGridOptions(1), 
            enableCommandRepeat=False,
            optionBox=True, 
        )
        
    pm.menuItem(divider=True) # Menu divider
        
    pm.menuItem(
        ("menuDisplayPxSnap" + suffix), 
            checkBox=pm.optionVar["pxSnap_NSUV"], 
            command=lambda *args: core.updateDisplay(9, 0), 
            label="Image Pixel Snap",
        )
    pm.menuItem(
        ("menuDisplayPxSnapOpt" + suffix), 
            optionBox=True, 
            command=lambda *args: pm.mel.performPixelSnapOptions(True),
        )
    pm.menuItem(
        ("menuDisplayImgRange" + suffix), 
            label="Image Range",
        )
    pm.menuItem(
        ("menuDisplayImgRangeOpt" + suffix), 
            optionBox=True, 
            command=lambda *args: pm.mel.performTextureViewImageRangeOptions(1),
        )
    pm.menuItem(
        ("menuDisplayBaking" + suffix), 
            annotation="UV Texture Editor baking on/off", 
            checkBox=pm.optionVar["editorBaking_NSUV"], 
            command=lambda *args: core.updateDisplay(10, 0), 
            label="UV Texture Editor Baking",
        )
    pm.menuItem(
        ("menuDisplayBakingOpt" + suffix), 
            command=lambda *args: pm.mel.performTextureViewBakeTextureOptions(True),
            optionBox=True, 
        )
    pm.menuItem(
        ("menuDisplayImgRatio" + suffix), 
            checkBox=pm.optionVar["imgRatio_NSUV"], 
            command=lambda *args: core.updateDisplay(11, 0), 
            label="Use Texture Ratio",
        )
    pm.menuItem(divider=True)
    
    pm.menuItem(
        ("menuDisplayCreatePSD" + suffix), 
            command=lambda *args: pm.mel.photoShopPaintTex(), 
            label="Create PSD Network...",
        )
    pm.menuItem(
        ("menuDisplayUpdatePSD" + suffix), 
            command=lambda *args: pm.mel.psdUpdateTextures(), 
            label="Update PSD Networks",
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the textures menu
def createTexturesMenu(parentMenu, txtEditor, menuBar):

    # Create vars from the editor settings
    numImages = pm.textureWindow(txtEditor, query=True, numberOfImages=1)
    selectedImg = pm.textureWindow(txtEditor, query=True, imageNumber=1)
    menuNames = pm.textureWindow(txtEditor, query=True, imageNames=1)
    selIndex = 0
    
    pm.setParent(parentMenu, menu=True) # Parent up
 
    # Add marking menu (MM) suffix if necessary
    suffix=""
    if menuBar == True: suffix = "_MM"
    
    # Rebuilding the menu so clear old content
    pm.menu(parentMenu, edit=True, deleteAllItems=True)
    
    # Get active shader
    if pm.optionVar["isoSelect_NSUV"] == True:
        selIndex = core.getActiveShader(txtEditor)
        if selIndex != None: 
            selIndex -= 1 # Set index
    else: selIndex = selectedImg
    
    # Default menuItem when we have no selection or textures
    if numImages == 0:        
        pm.menuItem(
            ("menuTextureNone" + suffix),
                enable=False, 
                enableCommandRepeat=False, 
                label="No object selected.",
                )

    # Loop through and create menuItem for each image
    i = 0
    for i in range(0, numImages):
        cBoxVar = False
        
        # Check the active image on the list
        if i == selIndex:
            cBoxVar = True # Set the current image number
        
        # Create
        pm.menuItem(
            ("menuTexture" + str(i) + suffix), 
                checkBox=cBoxVar, 
                command=pm.Callback(core.selectImage, i, txtEditor),
                enableCommandRepeat=False, 
                label=menuNames[i],
            )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Creates the UV sets menu
def createUVSetsMenu(parentMenu, txtEditor, menuBar):

    pm.setParent(parentMenu, menu=True) # Parent up

    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    uvSetCurrent = None

    def createMenuItemCmd(uvSet, uvSetIndex=uvSetCurrent):
    
        isCurrent = False # Check if the current item (uvSetIndex) is equal to the active set    
        if uvSetIndex == pm.polyUVSet(currentUVSet=True, query=True)[0]:
            isCurrent = True
    
        pm.menuItem(
            ("menuUVSets" + uvSetIndex + suffix), # necessary?
                checkBox=isCurrent,
                command=lambda *args: core.setCurrentSet(None, uvSet),
                label=uvSet,
                parent=parentMenu,
        )

        
    # Delete popup menu contents
    pm.menu(parentMenu, edit=True, deleteAllItems=True)

    # Mesh or components selected?
    sel = pm.filterExpand(selectionMask=(12, 31, 32, 34, 35))    
    if sel != [] and sel != None:

        # Get UV sets
        uvSetsAll, uvSetCurrent = core.getSets()
        if uvSetsAll != [] and uvSetsAll != None:
        
            # List of funcion commands and checkbox states
            menuItemList = []

            # Create list of partials
            for item in uvSetsAll: 
            
                # Check UV set for instance identifiers
                uvSetPerInst = pm.polyUVSet(
                    sel, query=True,
                        perInstance=True,
                        uvSet=item,
                )
                
                # If instance identifier was found, continue to next uv-set in the loop
                if uvSetPerInst == None:
                    continue
                else:
                    uvSetInst = uvSetPerInst[0]           
             
                # Append to list of function commands
                menuItemList.append(partial(createMenuItemCmd, uvSetInst))
            
            # Create the actual menu items
            for x,uvSetCurrent in enumerate(menuItemList): uvSetCurrent(uvSetsAll[x])

    else: # No uv sets found
        pm.menuItem(
            ("menuUVSetsNone" + suffix), 
                enable=False, 
                enableCommandRepeat=False, 
                label="No object selected.",
            )        
        pm.setParent( '..' , menu=True ) # Set default parent to one step up
        return 
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up 


# Creates the NSUV menu
def createNSUVMenu(parent, menuBar):

    pm.setParent(parent, menu=True) # Parent up
    
    # Add marking menu (MM) suffix if necessary
    suffix="_NSUV"
    if menuBar == True: suffix = "_MM_NSUV"

    # Create menuItems
    pm.menuItem(
        ("menuNSUVAbout" + suffix), 
            annotation="About", 
            command=lambda *args: aboutUI(), 
            label="About",
        )

    pm.menuItem(
        ("menuNSUVBuy" + suffix),
            annotation="Buy NSUV",
            command=lambda *args: buyUI(),
            label="Buy NSUV",
        )

    pm.menuItem(
        ("menuNSUVFAQ" + suffix),
            annotation="FAQ",
            command=lambda *args: faqUI(),
            label="FAQ",
        )
    pm.menuItem(
        ("menuNSUVManual" + suffix),
            annotation="Manual",
            command=lambda *args: core.openManual(),
            label="Manual",
        )
    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuNSUVWorkflow" + suffix),
            command=lambda *args: workflowUI(),
            annotation="Basic Workflow",
            label="Basic Workflow",
        )
    pm.menuItem(
        ("menuNSUVTricks" + suffix),
            command=lambda *args: tricksUI(),
            annotation="Tips And Tricks",
            label="Tips And Tricks",
        )
    pm.menuItem(
        ("menuNSUVUpdate" + suffix),
            command=lambda *args: updateUI(),
            annotation="Look For Update",
            label="Look For Update",
        )
    pm.menuItem(
        ("menuNSUVReport" + suffix),
            command=lambda *args: submitUI(),
            annotation="Submit Feedback",
            label="Submit Feedback",
        )
    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuNSUVTip" + suffix),
            command=lambda *args: totdUI(),
            annotation="Tip of the Day",
            label="Tip of the Day",
        )

    pm.menuItem(
        ("menuNSUVWelcome" + suffix),
            command=lambda *args: welcomeUI(),
            annotation="Welcome screen",
            label="Welcome screen",
        )

    pm.menuItem(
        ("menuNSUVShelfBtn" + suffix),
            command=lambda *args: core.createShelfBtn(),
            annotation="Create Shelf Button",
            label="Create Shelf Button",
        )

    pm.menuItem(divider=True)

    pm.menuItem(
        ("menuNSUVReset" + suffix),
            command=lambda *args: vars.reset(),
            annotation="Reset NSUV Settings",
            label="Reset NSUV Settings",
        )

    pm.setParent( '..' , menu=True ) # Set default parent to one step up


## Radial Menues

# Creates the radial selection conversion marking menu
def createRadialMenu(txtEditor, popupType):
    
    # Update optVar with new popupType
    pm.optionVar["popupType_NSUV"] = popupType
    
    # Create marking menu
    if popupType == 0:
    
        # Polygons
        pm.menuItem(
            (txtEditor + "Face"), 
                command=lambda *args: core.selectTypeChange(1),
                label="Face",
                radialPosition="S",
                )
        pm.menuItem(
            (txtEditor + "Edge"), 
                command=lambda *args: core.selectTypeChange(2),
                label="Edge",
                radialPosition="N",
                )
        pm.menuItem(
            (txtEditor + "UV"), 
                command=lambda *args: core.selectTypeChange(4),
                label="UV",
                radialPosition="E",
            )
        pm.menuItem(
            (txtEditor + "Vertex"), 
                command=lambda *args: core.selectTypeChange(3),
                label="Vertex",
                radialPosition="W",
            )
        
        if mayaVer >= 201500:
            pm.menuItem(
                (txtEditor + "Shell"), 
                    command=lambda *args: core.selectTypeChange(5),
                    label="Shell",
                    radialPosition="NW",
                    version="2015",
                )


    # Unfold3D
    elif popupType == 3:
        pm.mel.texSculptCacheContextOptionsPopup()     


# Create the radial marking menu -version of the menubar
def createRadialMenubar(txtEditor):

    # Create the Polygons sub menu
    pm.menuItem(
        (txtEditor + "EditMenuPop"), 
            allowOptionBoxes=True,
            label="Polygons", 
            subMenu=True, 
            tearOff=True, 
        )        
    createEditMenu((txtEditor + "EditMenuPop"), False)
    
    # Create the View sub menu
    pm.menuItem(
        (txtEditor + "ViewMenuPop"), 
            allowOptionBoxes=True,
            label="View", 
            subMenu=True, 
            tearOff=True, 
        )        
    createViewMenu((txtEditor + "ViewMenuPop"), False)
    
    # Create the Select sub menu
    pm.menuItem(
        (txtEditor + "SelectMenuPop"), 
            allowOptionBoxes=True,
            label="Select", 
            subMenu=True, 
            tearOff=True, 
        )        
    createSelectMenu((txtEditor + "SelectMenuPop"), txtEditor, False)
    
    # Create the Tool sub menu
    pm.menuItem(
        (txtEditor + "ToolMenuPop"), 
            allowOptionBoxes=True,
            label="Tool", 
            subMenu=True, 
            tearOff=True, 
        )        
    createToolMenu((txtEditor + "ToolMenuPop"), False)
    
    # Create the Display sub menu
    pm.menuItem(
        (txtEditor + "DisplayMenuPop"), 
            allowOptionBoxes=True,
            label="Display", 
            subMenu=True, 
            tearOff=True, 
        )        
    createDisplayMenu((txtEditor + "DisplayMenuPop"), txtEditor, False)
        
    # Create the Textures marking menu
    pm.menuItem(
        (txtEditor + "TexturesMenuPop"), 
            allowOptionBoxes=False,
            label="Textures", 
            subMenu=True, 
            tearOff=False, 
        )        
    pm.menu(
        (txtEditor + "TexturesMenuPop"), edit=True, 
            postMenuCommand=lambda *args: createTexturesMenu((txtEditor + "TexturesMenuPop"), txtEditor, False),
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    # Create UV set sub menu
    pm.menuItem(
        (txtEditor + "UVSetsMenuPop"), 
            allowOptionBoxes=False,
            label="UV Sets", 
            subMenu=True, 
            tearOff=False, 
        )        
    pm.menu(
        (txtEditor + "UVSetsMenuPop"), edit=True, 
            postMenuCommand=lambda *args: createUVSetsMenu((txtEditor + "UVSetsMenuPop"), txtEditor, False)
        )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
        
    # Create the NSUV sub menu
    pm.menuItem(
        (txtEditor + "NSUVMenuPop"), 
            allowOptionBoxes=True,
            label=("NSUV"), 
            subMenu=True, 
            tearOff=True, 
        )        
    createNSUVMenu((txtEditor + "NSUVMenuPop"), False)

    pm.setParent( '..' , menu=True ) # Set default parent to one step up


# Create radial marking menu for selection conversion
def createRadialConvertMenu(txtEditor):
   
    pm.menuItem(
        (txtEditor + "ToFace"), 
            command=lambda *args: core.selectConvert(1), 
            label="To Face",
            radialPosition="S", 
        )
        
    pm.menuItem(
        label="To Edge",
        radialPosition="N", 
        subMenu=True, 
        )
    pm.menuItem(
        (txtEditor + "ToEdge"), 
            command=lambda *args: core.selectConvert(2), 
            label="To Edge",
            radialPosition="N", 
        )
    if mayaVer >= 201500:
        pm.menuItem(
            command=lambda *args: pm.runtime.ConvertSelectionToEdgePerimeter(), 
            label="To Edge Perimeter",
            radialPosition="S", 
            version="2015", 
            )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    pm.menuItem(
        label="To UV",
        radialPosition="E", 
        subMenu=True, 
        )        
    pm.menuItem(
        (txtEditor + "ToUV"), 
            command=lambda *args: core.selectConvert(4), 
            label="To UV",
            radialPosition="E", 
        )
    if mayaVer >= 201500:
        pm.menuItem(
            command=lambda *args: pm.runtime.ConvertSelectionToUVPerimeter(), 
            label="To UV Perimeter",
            radialPosition="W", 
            version="2015", 
            )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    pm.menuItem(
        label="To Vertex",
        radialPosition="W", 
        subMenu=True, 
        )
    pm.menuItem(
        (txtEditor + "ToVertex"), 
            command=lambda *args: core.selectConvert(3), 
            label="To Vertex",
            radialPosition="W", 
        )
    if mayaVer >= 201500:
        pm.menuItem(
            command=lambda *args: pm.runtime.ConvertSelectionToVertexPerimeter(), 
            label="To Vertex Perimeter",
            radialPosition="E", 
            version="2015", 
            )
        
    pm.setParent( '..' , menu=True ) # Set default parent to one step up
    
    pm.menuItem(
        (txtEditor + "ToShell"), 
            command=lambda *args: pm.mel.polySelectBorderShell(0), 
            label="To Shell",
            radialPosition="NE", 
        )
    pm.menuItem(
        (txtEditor + "ToBorder"), 
            command=lambda *args: pm.mel.polySelectBorderShell(1), 
            label="To Shell Border",
            radialPosition="NW", 
        )

    pm.menuItem(
        (txtEditor + "ToEdgeLoop"), 
            command=lambda *args: pm.runtime.SelectEdgeLoop(), 
            label="To Edge Loop",
            radialPosition="SE", 
        )
    pm.menuItem(
        (txtEditor + "SelectShellBorder"), 
            command=lambda *args: pm.mel.polySelectEdges('edgeUVLoopOrBorder'), 
            label="To UV Edge Loop",
            radialPosition="SW", 
        )


# Create radial marking menu for context sensitive tools
def createRadialContextMenu(parent):
   
    selFirst = []
    selFirstShape = []
    selFirstShapeNodeType="unknown"
    
    # Get first selected component or object with a shape
    selFirst = pm.ls(selection=True, head=True)
    if selFirst != [] and selFirst != None:
        selFirstShape = pm.listRelatives(selFirst[0], shapes=True)

    if selFirstShape != [] and selFirstShape != None:
        selFirstShapeNodeType = pm.nodeType(selFirstShape[0])

    # Create popupMenu
    if pm.popupMenu(parent, query=True, exists=True):
    
        # Selection check
        if selFirst == [] or selFirst == None: selFirstStr = ""
        else: selFirstStr = str(selFirst[0]) # Convert to string for the regex
    
        pm.popupMenu(
                parent, edit=True, 
                deleteAllItems=True,
            )
            
        pm.setParent(parent, menu=True) # Parent up
        
        # Create the bottom menu on the marking menu
        pm.menuItem(
            annotation="Toggle Texture Borders", 
            command=lambda *args: core.updateDisplay(3, 0), 
            label="Toggle Texture Borders",
            )
        pm.menuItem(
            annotation="Toggle Texture Display", 
            command=lambda *args: core.updateDisplay(0, 0), 
            label="Toggle Texture Display",
            )
        pm.menuItem(
            annotation="Toggle Shaded UV Display", 
            command=lambda *args: core.updateDisplay(2, 0), 
            label="Toggle Shaded UV Display",
            )
        if mayaVer >= 201500:
            pm.menuItem(
                annotation="Toggle Shell Borders",
                command=lambda *args: core.updateDisplay(3, 0),
                label="Toggle Shell Borders",
                version="2015", 
                )
            pm.menuItem(
                annotation="Toggle UV Distortion Display", 
                command=lambda *args: core.updateDisplay(4, 0), 
                label="Toggle UV Distortion Display",
                version="2015", 
                )

        # Create menu items for the UV context
        if re.search("\.map", selFirstStr):
            pm.menuItem(
                annotation="Unfold/Relax", 
                label="Unfold/Relax",
                radialPosition="N", 
                subMenu=True, 
                )
            pm.menuItem(
                annotation="Unfold", 
                command=lambda *args: core.unfoldUVs(), 
                enableCommandRepeat=True, 
                label="Unfold",
                radialPosition="N", 
                )
            pm.menuItem(
                annotation="Unfold Options", 
                command=lambda *args: unfoldUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="N",
                )
            pm.menuItem(
                annotation="Unfold along U", 
                command=lambda *args: core.unfoldUVs("U"), 
                enableCommandRepeat=True, 
                label="Unfold along U",
                radialPosition="NW", 
                )
            pm.menuItem(
                annotation="Unfold along V", 
                command=lambda *args: core.unfoldUVs("V"), 
                enableCommandRepeat=True, 
                label="Unfold along V",
                radialPosition="NE", 
                )
            pm.menuItem(
                annotation="Relax (Optimize)", 
                command=lambda *args: core.relaxUVs(), 
                enableCommandRepeat=True, 
                label="Relax (Optimize)",
                radialPosition="S", 
                )
            pm.menuItem(
                annotation="Relax Options", 
                command=lambda *args: relaxUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="S",
                )
            pm.setParent( '..' , menu=True ) # Set default parent to one step up
            
            pm.menuItem(
                annotation=("Flip UVs along U"), 
                command=lambda *args: core.flipUVs("U"), 
                enableCommandRepeat=True, 
                label=("Flip UVs along U"),
                radialPosition="NW", 
                )
            pm.menuItem(
                annotation=("Flip UVs along V"), 
                command=lambda *args: core.flipUVs("V"), 
                enableCommandRepeat=True, 
                label=("Flip UVs along V"),
                radialPosition="NE", 
                )
            pm.menuItem(
                annotation=("Rotate UVs 90 deg CCW"), 
                command=lambda *args: core.rotateUVs("90"), 
                enableCommandRepeat=True, 
                label=("Rotate UVs 90 deg CCW"),
                radialPosition="W", 
                )
            pm.menuItem(
                annotation=("Rotate UVs 90 deg CW"), 
                command=lambda *args: core.rotateUVs("-90"), 
                enableCommandRepeat=True, 
                label=("Rotate UVs 90 deg CW"),
                radialPosition="E", 
                )
            pm.menuItem(
                annotation="Align UVs", 
                label="Align UVs",
                radialPosition="SW", 
                subMenu=True, 
                )
            pm.menuItem(
                annotation="Align UVs: Average U", 
                command=lambda *args: core.alignUVs("avgU"), 
                enableCommandRepeat=True, 
                label="Align UVs: Avg. U",
                radialPosition="NW", 
                )
            pm.menuItem(
                annotation="Align UVs: Max V", 
                command=lambda *args: core.alignUVs("maxV"), 
                enableCommandRepeat=True, 
                label="Align UVs: Max V",
                radialPosition="N", 
                )
            pm.menuItem(
                annotation="Align UVs: Min U", 
                command=lambda *args: core.alignUVs("minU"), 
                enableCommandRepeat=True, 
                label="Align UVs: Min U",
                radialPosition="W", 
                )
            pm.menuItem(
                annotation="Align UVs: Max U", 
                command=lambda *args: core.alignUVs("maxU"), 
                enableCommandRepeat=True, 
                label="Align UVs: Max U",
                radialPosition="E", 
                )
            pm.menuItem(
                annotation="Align UVs: Min V", 
                command=lambda *args: core.alignUVs("minV"), 
                enableCommandRepeat=True, 
                label="Align UVs: Min V",
                radialPosition="S", 
                )
            pm.menuItem(
                annotation="Align UVs: Average V", 
                command=lambda *args: core.alignUVs("avgV"), 
                enableCommandRepeat=True, 
                label="Align UVs: Average V",
                radialPosition="SE", 
                )
                
            pm.setParent( '..' , menu=True ) # Set default parent to one step up
            
            pm.menuItem(
                annotation="Smooth UV Tool", 
                command=lambda *args: pm.setToolTo("texSmoothSuperContext"), 
                label="Smooth UV Tool",
                radialPosition="S", 
                )
            pm.menuItem(
                annotation="Smooth UV Tool Options", 
                command=lambda *args: pm.mel.performTextureSmoothOptions(1), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="S",
                )
            pm.menuItem(
                annotation="Arrange", 
                label="Stack/Orient",
                radialPosition="SE", 
                subMenu=True, 
                )
            pm.menuItem(
                annotation="Match UVs", 
                command=lambda *args: core.matchUVs(), 
                enableCommandRepeat=True, 
                label="Match UVs",
                radialPosition="N", 
                )
            pm.menuItem(
                annotation="Match UVs Options", 
                command=lambda *args: matchTolUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="N",
                )
            pm.menuItem(
                annotation="Straighten UV Shell", 
                command=lambda *args: core.strShell(), 
                enableCommandRepeat=True, 
                label="Straighten UV Shell",
                radialPosition="NW", 
                )
            pm.menuItem(
                annotation="Orient Edge", 
                command=lambda *args: core.orientEdge(), 
                enableCommandRepeat=True, 
                label="Orient Edge",
                radialPosition="NE", 
                )
            pm.menuItem(
                annotation="Straighten UVs", 
                command=lambda *args: core.strUVs(), 
                enableCommandRepeat=True, 
                label="Straighten UVs",
                radialPosition="W", 
                )
            pm.menuItem(
                annotation="Straighten UVs", 
                command=lambda *args: strUVsUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="W",
                )
            pm.menuItem(
                annotation="Orient Shells", 
                command=lambda *args: core.orientShells(), 
                enableCommandRepeat=True, 
                label="Orient Shells",
                radialPosition="E", 
                )
            pm.menuItem(
                annotation="Orient Shells Options", 
                command=lambda *args: orientShellsUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="E",
                )
            pm.menuItem(
                annotation="Stack Shells", 
                command=lambda *args: core.stackShells(), 
                enableCommandRepeat=True, 
                label="Stack Shells",
                radialPosition="SE", 
                )
            pm.menuItem(
                annotation="Straighten UV Border", 
                command=lambda *args: pm.mel.performPolyStraightenUV(0), 
                enableCommandRepeat=True, 
                label="Straighten UV Border",
                radialPosition="SW", 
                )
            pm.menuItem(
                annotation="Straighten UV Border Options", 
                command=lambda *args: pm.mel.performPolyStraightenUV(1), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="SW",
                )
                
            pm.setParent( '..' , menu=True ) # Set default parent to one step up
            
            if mayaVer >= 201500:
                pm.menuItem(
                    command=lambda *args: CreateUVShellAlongBorder(), 
                    enableCommandRepeat=True, 
                    label="Create UV Shell",
                    version="2015", 
                    )
                
           # Allows user to define a proc with additional menu items
            if pm.mel.exists("contextUVToolsUVUserMM"): pm.mel.contextUVToolsUVUserMM(parent)

        # Create menu items for the vertex context
        elif re.search("\.vtx", selFirstStr):
            if mayaVer >= 201500:
                pm.menuItem(
                    command=lambda *args: pm.runtime.CreateUVShellAlongBorder(), 
                    enableCommandRepeat=True, 
                    label="Create UV Shell",
                    radialPosition="SE", 
                    version="2015", 
                    )
                
            # Allows user to define a proc with additional menu items
            if pm.mel.exists("contextUVToolsVertexUserMM"): pm.mel.contextUVToolsVertexUserMM(parent)

        # Create menu items for the face context
        elif re.search("\.f", selFirstStr):
            pm.menuItem(
                command=lambda *args: core.mapping("plane"), 
                enableCommandRepeat=True, 
                label="Planar Map",
                radialPosition="N", 
                )
            pm.menuItem(
                annotation="Planar Mapping (Options)", 
                command=lambda *args: mapPlanarUI("x"), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="N",
                )                
                
            pm.menuItem(
                annotation="Automatic Map", 
                command=lambda *args: core.mapping(auto), 
                enableCommandRepeat=True, 
                label="Automatic Map",
                radialPosition="NW", 
                )
            pm.menuItem(
                annotation="Automatic Mapping (Options)", 
                command=lambda *args: mapAutoUI, 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="NW",
                )
                
            pm.menuItem(
                annotation="Normal-based Map", 
                command=lambda *args: core.mapping(normal), 
                enableCommandRepeat=True, 
                label="Normal-based Map",
                radialPosition="NE", 
                )
            pm.menuItem(
                annotation="Automatic Mapping (Options)", 
                command=lambda *args: mapNormalUI, 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="NE",
                )
                
            pm.menuItem(
                annotation="Normalize the Selected Shells (Left Click) --- Normalize Options (Right Click)", 
                command=lambda *args: core.normalizeShells(0), 
                enableCommandRepeat=True, 
                label="Normalize UVs",
                radialPosition="E", 
                )
            pm.menuItem(
                annotation="Normalize UVs (Options)", 
                command=lambda *args: normalizeUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="E",
                )
                
            pm.menuItem(
                annotation="Unitize the Selected Shells. All selected faces will be moved to fit into the default 0 -> 1 UV range.", 
                command=lambda *args: core.normalizeShells(5), 
                enableCommandRepeat=True, 
                label="Unitize UVs",
                radialPosition="W", 
                )
            pm.menuItem(
                annotation="Normalize UVs (Options)", 
                command=lambda *args: normalizeUI(), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="W",
                )
                
            if mayaVer >= 201500:
                pm.menuItem(
                    "tweakShellButton", 
                        annotation="Tweak component's UV positions", 
                        command=lambda *args: pm.setToolTo("texTweakSuperContext"), 
                        label="Tweak UV Tool",
                        radialPosition="S", 
                        version="2015", 
                    )

            pm.menuItem(enableCommandRepeat=True, 
                command=lambda *args: core.layoutUVs(), 
                annotation="Select faces to be moved in UV space", 
                radialPosition="SW", 
                label="Layout UVs",
                )
            pm.menuItem(enableCommandRepeat=True, 
                optionBox=True, 
                command=lambda *args: layoutUI(), 
                annotation="Layout UVs options", 
                radialPosition="SW",
                )

            pm.menuItem(enableCommandRepeat=True, 
                version="2015", 
                command=lambda *args: core.createShell(), 
                radialPosition="SE", 
                label="Create UV Shell",
                )
                
            # Allows user to define a proc with additional menu items
            if pm.mel.exists("contextUVToolsFaceUserMM"):
                pm.mel.contextUVToolsFaceUserMM(parent)
          
        # Create menu items for the edge context
        elif re.search("\.e", selFirstStr):
            pm.menuItem(
                annotation="Move and Sew UV Edge(s)", 
                command=lambda *args: pm.mel.performPolyMapSewMove(0), 
                enableCommandRepeat=True, 
                label="Move and Sew UV Edge(s)",
                radialPosition="N", 
                )
            pm.menuItem(
                annotation="Move and Sew UV Edge(s)", 
                command=lambda *args: pm.mel.performPolyMapSewMove(1), 
                enableCommandRepeat=True, 
                optionBox=True, 
                radialPosition="N",
                )
                
            if mayaVer == 201600:
                pm.menuItem(
                    annotation="Cut UV Tool", 
                    command=lambda *args: [ pm.setToolTo("texCutUVContext"), texCutContext("texCutUVContext", edit=True, mode="Cut") ], 
                    enableCommandRepeat=True, 
                    label="Cut UV Tool", 
                    radialPosition="NW",
                    version=2016, 
                    )
                pm.menuItem(
                    annotation="Sew UV Tool", 
                    command=lambda *args: [ pm.setToolTo("texCutUVContext"), texCutContext("texCutUVContext", edit=True, mode="Sew") ], 
                    enableCommandRepeat=True, 
                    label="Sew UV Tool", 
                    radialPosition="NE",
                    version=2016, 
                    )
                
            pm.menuItem(
                annotation="Cut UV Edge(s)", 
                command=lambda *args: pm.mel.polyPerformAction("polyMapCut", "e", 0), 
                enableCommandRepeat=True, 
                label="Cut",
                radialPosition="W", 
                )
            pm.menuItem(
                annotation="Sew UV Edge(s)", 
                command=lambda *args: pm.mel.polyPerformAction("polyMapSew", "e", 0), 
                enableCommandRepeat=True, 
                label="Sew",
                radialPosition="E", 
                )

            if mayaVer >= 201500:
                pm.menuItem(
                    "tweakShellButton", 
                        annotation="Tweak component's UV positions", 
                        command=lambda *args: pm.setToolTo("texTweakSuperContext"), 
                        label="Tweak UV Tool",
                        radialPosition="S", 
                        version="2015", 
                    )
                pm.menuItem(
                    command=lambda *args: pm.runtime.CreateUVShellAlongBorder(), 
                    enableCommandRepeat=True, 
                    label="Create UV Shell",
                    radialPosition="SE", 
                    version="2015", 
                    )

            # Allows user to define a proc with additional menu items
            if pm.mel.exists("contextUVToolsEdgeUserMM"):
                pm.mel.contextUVToolsEdgeUserMM(parent)

        # Create menu items for the polygon mesh context
        elif selFirstShapeNodeType == "mesh":
            if mayaVer >= 201500:
                pm.menuItem(
                    "tweakShellButton", 
                        annotation="Tweak component's UV positions", 
                        command=lambda *args: pm.setToolTo("texTweakSuperContext"), 
                        label="Tweak UV Tool",
                        radialPosition="S", 
                        version="2015", 
                    )

            # Allows user to define a proc with additional menu items
            if pm.mel.exists("contextUVToolsObjectUserMM"):
                pm.mel.contextUVToolsObjectUserMM(parent)

                
        # Create menu items for the default context - Currently N/A
            
        # Allows user to define a proc with additional menu items
        elif pm.mel.exists("contextUVToolsDefaultUserMM"):
            pm.mel.contextUVToolsDefaultUserMM(parent)    


## Popup Menues

# Create popup menu for Aligning Shells along U
def createPopupAlignShellsU(menu, parent):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    alignShellsVTopItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsU(0, parent, iconDict["alignShellsLeft"], False),
        image=iconDict["alignShellsLeft"],
        label="Align to the Left",
        parent=menu,
    )
    alignShellsVMidItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsU(1, parent, iconDict["alignShellsMidU"], False),
        image=iconDict["alignShellsMidU"],
        label="Align to the Center",
        parent=menu,
    )
    alignShellsVBottomItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsU(2, parent, iconDict["alignShellsRight"], False),
        image=iconDict["alignShellsRight"],
        label="Align to the Right",
        parent=menu,
    )


# Create popup menu for Aligning Shells along V
def createPopupAlignShellsV(menu, parent):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    alignShellsVTopItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsV(0, parent, iconDict["alignShellsTop"], False),
        image=iconDict["alignShellsTop"],
        label="Align to the Top",
        parent=menu,
    )
    alignShellsVMidItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsV(1, parent, iconDict["alignShellsMidV"], False),
        image=iconDict["alignShellsMidV"],
        label="Align to the Center",
        parent=menu,
    )
    alignShellsVBottomItem = pm.menuItem(
        command=lambda *args: core.popupAlignShellsV(2, parent, iconDict["alignShellsBottom"], False),
        image=iconDict["alignShellsBottom"],
        label="Align to the Bottom",
        parent=menu,
    )


# Create popup menu for Aligning UVs along U
def createPopupAlignUVsU(menu, parent):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    alignUVsUTopItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsU(0, parent, iconDict["alignUMin"], False),
        image=iconDict["alignUMin"],
        label="Align to the Left",
        parent=menu,
    )
    alignUVsUVMidItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsU(1, parent, iconDict["alignUMid"], False),
        image=iconDict["alignUMid"],
        label="Align to the Center",
        parent=menu,
    )
    alignUVsUBottomItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsU(2, parent, iconDict["alignUMax"], False),
        image=iconDict["alignUMax"],
        label="Align to the Right",
        parent=menu,
    )
    

# Create popup menu for Aligning UVs along V
def createPopupAlignUVsV(menu, parent):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    alignUVsVTopItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsV(0, parent, iconDict["alignVMax"], False),
        image=iconDict["alignVMax"],
        label="Align to the Top",
        parent=menu,
    )
    alignUVsVMidItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsV(1, parent, iconDict["alignVMid"], False),
        image=iconDict["alignVMid"],
        label="Align to the Center",
        parent=menu,
    )
    alignUVsVBottomItem = pm.menuItem(
        command=lambda *args: core.popupAlignUVsV(2, parent, iconDict["alignVMin"], False),
        image=iconDict["alignVMin"],
        label="Align to the Bottom",
        parent=menu,
    )


# Create popup menu for Calculating distances or angle
def createPopupCalculate(menu, parent, field):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()
    
    # Create callback object for UI.calcPxDistUI - used by core.popupCalculate()
    cbObject = pm.Callback(calcPxDistUI,)

    calculateDistUItem = pm.menuItem(
        command=lambda *args: core.popupCalculate(0, parent, iconDict["distU"], field, False),
        image=iconDict["distU"],
        label="Horizontal UV Distance",
        parent=menu,
    )
    calculateDistVItem = pm.menuItem(
        command=lambda *args: core.popupCalculate(1, parent, iconDict["distV"], field, False),
        image=iconDict["distV"],
        label="Vertical UV Distance",
        parent=menu,
    )
    calculateDistPxItem = pm.menuItem(
        command=lambda *args: core.popupCalculate(2, parent, iconDict["distPx"], field, cbObject, False),
        image=iconDict["distPx"],
        label="Pixel Distance",
        parent=menu,
    )
    calculateAngleItem = pm.menuItem(
        command=lambda *args: core.popupCalculate(3, parent, iconDict["calcAngle"], field, False),
        image=iconDict["calcAngle"],
        label="Angle Between",
        parent=menu,
    )


# Menu listing all UV sets the user can copy to
def createPopupCopySet(parentList):

    uvSetCurrent = None

    # Internal func used by functools.partial for creating menu items
    def createMenuItemCmd(copyTo, copyFrom=uvSetCurrent):    
        pm.menuItem(
            command=lambda *args: core.copySet(scrollListUVSet, copyFrom, copyTo),
            label=copyTo,
            parent=parentList,
        )

    # Delete popup menu contents, as we need to rebuild...
    pm.menu(parentList, edit=True, deleteAllItems=True)

    # Mesh or components selected?
    sel = pm.filterExpand(selectionMask=(12, 31, 32, 34, 35))
    if sel != [] and sel != None:

        # Get UV sets
        uvSetsAll, uvSetCurrent = core.getSets()
        if uvSetsAll != [] and uvSetsAll != None:

            # List of funcion commands
            menuItemList = []

            # Create list of partials
            for item in uvSetsAll: 

                # Check UV set for instance identifiers
                uvSetPerInst = pm.polyUVSet(
                    sel, query=True,
                        perInstance=True,
                        uvSet=item,
                )

                # If instance identifier was found, continue to next uv-set in the loop
                if uvSetPerInst == None:
                    continue
                else:
                    uvSetInst = uvSetPerInst[0]

                # Append to list of function commands
                menuItemList.append(partial(createMenuItemCmd, uvSetInst))

            # Create the actual menu items
            for x,uvSetCurrent in enumerate(menuItemList): uvSetCurrent(uvSetsAll[x])

        # Create default button
        pm.menuItem(
            command=lambda *args: copySetUI(),
            label="Copy into New UV set",
            parent=parentList
        )

    else: # No mesh is selected
        pm.menuItem(
            enable=False,
            label="No Mesh Selected",
            parent=parentList
        )


# Create popup menu for Cycling the Pivot
def createPopupCyclePivot(menu, parent):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    cycleUVTopLeftItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(0, parent, iconDict["cycleUV1"], False),
        image=iconDict["cycleUV1"],
        label="UV Bounds: Top Left",
        parent=menu,
    )
    cycleUVTopRightItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(1, parent, iconDict["cycleUV2"], False),
        image=iconDict["cycleUV2"],
        label="UV Bounds: Top Right",
        parent=menu,
    )
    cycleUVBottomLeftItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(2, parent, iconDict["cycleUV3"], False),
        image=iconDict["cycleUV3"],
        label="UV Bounds: Bottom Left",
        parent=menu,
    )
    cycleUVBottomRightItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(3, parent, iconDict["cycleUV4"], False),
        image=iconDict["cycleUV4"],
        label="UV Bounds: Bottom Right",
        parent=menu,
    )
    cycleSelTopLeftItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(4, parent, iconDict["cycleSel1"], False),
        image=iconDict["cycleSel1"],
        label="Selection: Top Left",
        parent=menu,
    )
    cycleSelTopRightItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(5, parent, iconDict["cycleSel2"], False),
        image=iconDict["cycleSel2"],
        label="Selection: Top Right",
        parent=menu,
    )
    cycleSelBottomLeftItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(6, parent, iconDict["cycleSel3"], False),
        image=iconDict["cycleSel3"],
        label="Selection: Bottom Left",
        parent=menu,
    )
    cycleSelBottomRightItem = pm.menuItem(
        command=lambda *args: core.popupCyclePivot(7, parent, iconDict["cycleSel4"], False),
        image=iconDict["cycleSel4"],
        label="Selection: Bottom Right",
        parent=menu,
    )


# Menu listing all planar mapping directions
def createPopupPlanarMap(menu):

    # Delete popup menu contents, as we need to rebuild...
    menu.deleteAllItems()

    planarXItem = pm.menuItem(
        command=lambda *args: core.mapping("plane", "x"),
        image=iconDict["projPlaneX"],
        label="Planar Mapping: X",
        parent=menu,
    )
    planarXItemOpt = pm.menuItem(
        command=lambda *args: mapPlanarUI("x"),
        label="Planar Mapping: X - Options",
        parent=menu,
        optionBox=True,
    )
    
    planarYItem = pm.menuItem(
        command=lambda *args: core.mapping("plane", "y"),
        image=iconDict["projPlaneY"],
        label="Planar Mapping: Y",
        parent=menu,
    )
    planarYItemOpt = pm.menuItem(
        command=lambda *args: mapPlanarUI("y"),
        label="Planar Mapping: Y - Options",
        parent=menu,
        optionBox=True,
    )
    
    planarZItem = pm.menuItem(
        command=lambda *args: core.mapping("plane", "z"),
        image=iconDict["projPlaneZ"],
        label="Planar Mapping: Z",
        parent=menu,
    )
    planarZItemOpt = pm.menuItem(
        command=lambda *args: mapPlanarUI("z"),
        label="Planar Mapping: Z - Options",
        parent=menu,
        optionBox=True,
    )


## Auxiliary Windows

# About NSUV UI
def aboutUI():

    # Check for window duplicate
    if pm.window( winAbout, exists=True ):
        pm.deleteUI(winAbout)

    # Window
    window = pm.window(
        winAbout,
        height=aboutWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="About NSUV",
        width=largeWinX
    )
    
    # Main column
    colMainAbout = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=largeWinX,
    )
    
    # Title image
    imageNSUV = pm.image(
        image=iconDict["title"],
        parent=colMainAbout,
    )
    
    # Information
    frameInfoAbout = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Information",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainAbout,
        width=largeWinX,
    )
    colInfoAbout = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameInfoAbout
    )
    text1About = pm.text(
        label="Version: \n" + NSUV_title + "\n\nAuthor: \nMartin Dahlin",
        parent=colInfoAbout,
    )
    text2About = pm.text(
        hyperlink=True,
        label="http://www.martin.dahlin.net/",
        parent=colInfoAbout,
    )
    text3About = pm.text(
        label="\nContact: \nmartin.dahlin@live.com",
        parent=colInfoAbout,
    )

    # Description
    frameDescAbout = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Description",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainAbout,
        width=largeWinX,
    )
    text5About = pm.text(
        align="left",
        label="Nightshade UV Editor (NSUV) extends the \
default functionality of Maya's native UV editor by adding \
scripts and tools that greatly speed up the time it takes \
to do UV-related work.",
        parent=frameDescAbout,
        width=frameX,
        wordWrap=True,
    )

    # Special thanks
    frameThanksAbout = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Special Thanks To",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainAbout,
        width=largeWinX,
    )
    text6About = pm.text(
        align="left",
        label="Nathan Roberts, Robert Kovach, David Johnson and Viktoras Makauskas on CGTalk. \
\nRobert White and Steve Theodore on tech-artists.org \n\nAlso: Anton Palmqvist, Malcolm Andrieshyn \
and my friends and former coworkers Alexander Lilja and Elin Rud\xe9n, for all the feedback, \
criticism, bug reports and feature ideas. \n\nThank you all!",
        parent=frameThanksAbout,
        width=frameX,
        wordWrap=True,
    )

    # Button
    btnCloseAbout = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainAbout,
        width=largeWinX,
    )

    # Display the window
    pm.showWindow(window)


# Auto Seams UI
def autoSeamsUI():
    
    # Reset UI
    def autoSeamUIReset():

        # Reset UI controls
        radGrpCutAutoSeam.setSelect(1)
        sliderSplitAutoSeams.setValue(0.0)
        cBoxHolesAutoSeam.setValue1(True)
        
        # Reset optVars
        pm.optionVar["autoSeamOperation_NSUV"] = 1
        pm.optionVar["autoSeamSegment_NSUV"] = 0.0
        pm.optionVar["autoSeamPipeCut_NSUV"] = True

    # Update optVar
    def autoSeamOptVar(varType):

        if varType == 0:
            pm.optionVar["autoSeamOperation_NSUV"] = radGrpCutAutoSeam.getSelect()

        elif varType == 1:
            pm.optionVar["autoSeamSegment_NSUV"] = sliderSplitAutoSeams.getValue()

        elif varType == 2:
            pm.optionVar["autoSeamPipeCut_NSUV"] = cBoxHolesAutoSeam.getValue1()

    
    # Check for window duplicate
    if pm.window( winAutoSeam, exists=True ):
        pm.deleteUI(winAutoSeam)

    # Window
    window = pm.window(
        winAutoSeam,
        height=autoSeamsWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Auto Seams",
        width=largeWinX
    )

    # Create layouts
    form1AutoSeam = pm.formLayout()
    scrollAutoSeam = pm.scrollLayout( childResizable=True )
    form2AutoSeam = pm.formLayout( parent=scrollAutoSeam )

    # Frame and column
    frameAutoSeam = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Auto Seam Options",
        parent=form2AutoSeam
    )
    colAutoSeam = pm.columnLayout(
        parent=frameAutoSeam,
    )

    # Elements
    radGrpCutAutoSeam = pm.radioButtonGrp(
        changeCommand=lambda *args: autoSeamOptVar(0),
        columnWidth=[1, layoutCol1],
        label1="Cut",
        label2="Select",
        label="Seams: ",
        numberOfRadioButtons=2,
        select=pm.optionVar["autoSeamPipeCut_NSUV"],
        vertical=True,
    )
    sliderSplitAutoSeams = pm.floatSliderGrp(
        changeCommand=lambda *args: autoSeamOptVar(1),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=1.0,
        fieldMinValue=0.0,
        label="Stopping threshold: ",
        maxValue=1.0,
        minValue=0.0,
        precision=4,
        value=pm.optionVar["autoSeamSegment_NSUV"]
    )
    cBoxHolesAutoSeam = pm.checkBoxGrp(
        changeCommand=lambda *args: autoSeamOptVar(2),
        columnWidth2=[layoutCol1, largeCol2],
        label="",
        label1="Connect Holes",
        value1=pm.optionVar["autoSeamOperation_NSUV"],
    )

    # Buttons
    btnApplyCloseAutoSeam = pm.button(
        command=lambda *args: core.autoSeams(winAutoSeam),
        label="Confirm",
        parent=form1AutoSeam,
    )
    btnApplyAutoSeam = pm.button(
        command=lambda *args: core.autoSeams(),
        label="Apply",
        parent=form1AutoSeam,
    )
    btnResetAutoSeam = pm.button(
        command=lambda *args: autoSeamUIReset(),
        label="Reset",
        parent=form1AutoSeam,
    )
    btnCloseAutoSeam = pm.button(
        command=lambda *args: pm.deleteUI(winAutoSeam),
        label="Close",
        parent=form1AutoSeam,
    )

    # Layout frame
    pm.formLayout(
        form2AutoSeam, edit=True,
        attachForm=[
            (frameAutoSeam, "top", 0),
            (frameAutoSeam, "left", 0),
            (frameAutoSeam, "right", 0),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1AutoSeam, edit=True,
        attachForm=[
            (scrollAutoSeam, "top", 0),
            (scrollAutoSeam, "left", 0),
            (scrollAutoSeam, "right", 0),

            (btnApplyCloseAutoSeam, "left", 5),
            (btnApplyCloseAutoSeam, "bottom", 5),
            (btnApplyAutoSeam, "bottom", 5),
            (btnResetAutoSeam, "bottom", 5),
            (btnCloseAutoSeam, "right", 5),
            (btnCloseAutoSeam, "bottom", 5),
        ],
        attachControl=[
            (scrollAutoSeam, "bottom", 0, btnApplyCloseAutoSeam),
        ],
        attachPosition=[
            (btnApplyCloseAutoSeam, "right", 3, 25),
            (btnApplyAutoSeam, "left", 2, 25),
            (btnApplyAutoSeam, "right", 3, 50),
            (btnResetAutoSeam, "right", 3, 75),
            (btnResetAutoSeam, "left", 2, 50),
            (btnCloseAutoSeam, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseAutoSeam, "top"),
            (btnApplyAutoSeam, "top"),
            (btnResetAutoSeam, "top"),
            (btnCloseAutoSeam, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for reporting a bug or requesting a feature
def buyUI():

    # Check for window duplicate
    if pm.window( winBuy, exists=True ):
        pm.deleteUI(winBuy)

    # Window
    window = pm.window(
        winBuy,
        height=buyWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Buy NSUV Pro",
        width=largeWinX
    )

    # Main column
    colMainBuy = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=largeWinX,
    )

    # Submission info
    frameBuy = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="License Information",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainBuy,
        width=largeWinX,
    )
    colBuy = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameBuy
    )
    textBuy = pm.text(
        label="Nightshade UV Editor (NSUV) is free to use for all non-commercial purposes. However, if you "\
"are using NSUV in a production environment and/or for making profit, you are considered a professional and "\
"are required to buy the pro version (NSUV Pro).\n\nFor more information about the license please "\
"click the button below to visit the NSUV page on Creative Crash.\n",
        font="boldLabelFont",
        parent=colBuy,
        width=frameX,
        wordWrap=True,
    )
    btnSubmitBuy = pm.button(
        command=lambda *args: pm.launch(web="http://www.creativecrash.com/maya/script/nightshade-uv-editor-pro"),
        label="Go to Creative Crash",
        parent=colBuy,
        width=(largeWinX/2)
    )
    
    # Button
    btnCloseBuy = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainBuy,
        width=largeWinX,
    )

    # Display the window
    pm.showWindow(window)


# UI for calculating pixel distance between two UVs
def calcPxDistUI():

    # Vars
    c1 = 0.3
    c2 = 0.45
    c3 = 0.25
    c4 = 0.39
    c5 = c3
    c6 = c2
    c7 = 0.37
    c8 = 0.32
    c9 = 0.5

    # Get values
    distU, distV, distUV = core.calcPxDist()

    # Check for window duplicate
    if pm.window( winCalcPx, exists=True ):
        pm.deleteUI(winCalcPx)

    # Calculate pixel distances
    # U
    distU4096 = "%.2f" % ( 4096*distU )
    distU2048 = "%.2f" % ( float(distU4096) / 2 )
    distU1024 = "%.2f" % ( float(distU4096) / 4 )
    distU512 = "%.2f" % ( float(distU4096) / 8 )
    distU256 = "%.2f" % ( float(distU4096) / 16 )
    distU128 = "%.2f" % ( float(distU4096) / 32 )

    # V
    distV4096 = "%.2f" % ( 4096*distV )
    distV2048 = "%.2f" % ( float(distV4096) / 2 )
    distV1024 = "%.2f" % ( float(distV4096) / 4 )
    distV512 = "%.2f" % ( float(distV4096) / 8 )
    distV256 = "%.2f" % ( float(distV4096) / 16 )
    distV128 = "%.2f" % ( float(distV4096) / 32 )

    # Diagonal
    distUV4096 = "%.2f" % ( 4096*distUV )
    distUV2048 = "%.2f" % ( float(distUV4096) / 2 )
    distUV1024 = "%.2f" % ( float(distUV4096) / 4 )
    distUV512 = "%.2f" % ( float(distUV4096) / 8 )
    distUV256 = "%.2f" % ( float(distUV4096) / 16 )
    distUV128 = "%.2f" % ( float(distUV4096) / 32 )

    # Construct result strings
    # U
    distU4096L = str(distU4096) + " px"
    distU2048L = str(distU2048) + " px"
    distU1024L = str(distU1024) + " px"
    distU512L = str(distU512) + " px"
    distU256L = str(distU256) + " px"
    distU128L = str(distU128) + " px"

    # V
    distV4096L = str(distV4096) + " px"
    distV2048L = str(distV2048) + " px"
    distV1024L = str(distV1024) + " px"
    distV512L = str(distV512) + " px"
    distV256L = str(distV256) + " px"
    distV128L = str(distV128) + " px"

    # Diagonal
    distUV4096L = str(distUV4096) + " px"
    distUV2048L = str(distUV2048) + " px"
    distUV1024L = str(distUV1024) + " px"
    distUV512L = str(distUV512) + " px"
    distUV256L = str(distUV256) + " px"
    distUV128L = str(distUV128) + " px"

    # Create window
    window = pm.window(
        winCalcPx,
        height=calcPxWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Pixel Distance",
    )

    # Create layouts 
    form1CalcPx = pm.formLayout()
    form2CalcPx = pm.formLayout( parent=form1CalcPx )
    frameCalcPx = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Results",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2CalcPx,
        width=smallWinX,
        )

    gridCalcPx = pm.gridLayout(
        backgroundColor=[0.16, 0.16, 0.16], # Colors the top cells
        cellHeight=calcPxCellY,
        cellWidth=calcPxCellX,
        numberOfRowsColumns=[7,4],
        parent=frameCalcPx,
    )
    pm.text(
        align="center",
        font="boldLabelFont",
        height=calcPxCellY,
        label="Map size",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        font="boldLabelFont",
        height=calcPxCellY,
        label="U Distance",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        font="boldLabelFont",
        height=calcPxCellY,
        label="V Distance",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        font="boldLabelFont",
        height=calcPxCellY,
        label="Distance",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c1, c1, c1],
        height=calcPxCellY,
        label="4096 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c3, c3],
        height=calcPxCellY,
        label=distU4096L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c3, c3, c2],
        height=calcPxCellY,
        label=distV4096L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c4, c5, c6],
        height=calcPxCellY,
        label=distUV4096L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c7, c7, c7],
        height=calcPxCellY,
        label="2048 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c9, c8, c8],
        height=calcPxCellY,
        label=distU2048L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c8, c8, c9],
        height=calcPxCellY,
        label=distV2048L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c8, c9],
        height=calcPxCellY,
        label=distUV2048L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c1, c1, c1],
        height=calcPxCellY,
        label="1024 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c3, c3],
        height=calcPxCellY,
        label=distU1024L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c3, c3, c2],
        height=calcPxCellY,
        label=distV1024L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c4, c5, c6],
        height=calcPxCellY,
        label=distUV1024L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c7, c7, c7],
        height=calcPxCellY,
        label="512 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c9, c8, c8],
        height=calcPxCellY,
        label=distU512L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c8, c8, c9],
        height=calcPxCellY,
        label=distV512L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c8, c9],
        height=calcPxCellY,
        label=distUV512L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c1, c1, c1],
        height=calcPxCellY,
        label="256 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c3, c3],
        height=calcPxCellY,
        label=distU256L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c3, c3, c2],
        height=calcPxCellY,
        label=distV256L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c4, c5, c6],
        height=calcPxCellY,
        label=distUV256L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c7, c7, c7],
        height=calcPxCellY,
        label="128 px",
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c9, c8, c8],
        height=calcPxCellY,
        label=distU128L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c8, c8, c9],
        height=calcPxCellY,
        label=distV128L,
        width=calcPxCellX
    )
    pm.text(
        align="center",
        backgroundColor=[c2, c8, c9],
        height=calcPxCellY,
        label=distUV128L,
        width=calcPxCellX
    )

    pm.setParent('..') # Set default parent to one step up
    
    # Buttons
    btnOkCalcPx = pm.button(
        command=lambda *args: calcPxDistUI(),
        label="Recalculate",
        parent=form1CalcPx,
    )
    btnCloseCalcPx = pm.button(
        command=lambda *args: pm.deleteUI(winCalcPx),
        label="Close",
        parent=form1CalcPx,
    )
    
    # Layout frame
    pm.formLayout(
        form2CalcPx, edit=True,
        attachForm=[
            (frameCalcPx, "top", 0),
            (frameCalcPx, "left", 0),
            (frameCalcPx, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1CalcPx, edit=True,
        attachForm=[
            (form2CalcPx, "top", 0),
            (form2CalcPx, "left", 0),
            (form2CalcPx, "right", 0),
        
            (btnOkCalcPx, "left", 5),
            (btnOkCalcPx, "bottom", 5),
            (btnCloseCalcPx, "right", 5),
            (btnCloseCalcPx, "bottom", 5),
        ],
        attachControl=[
            (form2CalcPx, "bottom", 0, btnCloseCalcPx),
        ],
        attachPosition=[
            (btnOkCalcPx, "right", 2, 50),
            (btnCloseCalcPx, "left", 1, 50),
        ],
        attachNone=[
            (btnOkCalcPx, "top"),
            (btnCloseCalcPx, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)        


# UI for copying to a new UV set
def copySetUI():

    def copySetOptVar(): # Updates optVar
        pm.optionVar["copyNewUVSet_NSUV"] = fieldCopyNewUVSet.getText()


    # Check for window duplicate
    if pm.window( winCopyNewUVSet, exists=True ):
        pm.deleteUI(winCopyNewUVSet)

    # Window
    window = pm.window(
        winCopyNewUVSet,
        height=copySetWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Copy to new UV Set",
    )

    # Layouts
    form1CopyNewUVSet = pm.formLayout()
    form2CopyNewUVSet = pm.formLayout( parent=form1CopyNewUVSet )
    frameCopyNewUVSet = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Copy UV Set Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2CopyNewUVSet,
        width=smallWinX,
    )
    colCopyNewUVSet = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameCopyNewUVSet
    )

    # Text field
    if mayaVer == 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldCopyNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: copySetOptVar(),
            columnAlign=[1, "right"],
            columnWidth2=[smallCol1, smallCol2],
            forceChangeCommand=True,
            insertionPosition=0,
            label="New UV set name: ",
            parent=colCopyNewUVSet,
            text=pm.optionVar["copyNewUVSet_NSUV"],
        )
    else:
        fieldCopyNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: copySetOptVar(),
            columnAlign=[1, "right"],
            columnWidth2=[smallCol1, smallCol2],
            forceChangeCommand=True,
            insertionPosition=0,
            label="New UV set name: ",
            parent=colCopyNewUVSet,
            text=pm.optionVar["copyNewUVSet_NSUV"],
            textChangedCommand=lambda *args: copySetOptVar(), # Added in 2013
        )

    # Buttons
    btnCreateCopyNewUVSet = pm.button(
        command=lambda *args: core.copySet(scrollListUVSet, None, pm.optionVar["copyNewUVSet_NSUV"], winCopyNewUVSet),
        label="Create",
        parent=form1CopyNewUVSet,
    )
    
    btnCloseCopyNewUVSet = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1CopyNewUVSet,
    )
    
    # Layout frame
    pm.formLayout(
        form2CopyNewUVSet, edit=True,
        attachForm=[
            (frameCopyNewUVSet, "top", 0),
            (frameCopyNewUVSet, "left", 0),
            (frameCopyNewUVSet, "right", 0),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1CopyNewUVSet, edit=True,
        attachForm=[
            (form2CopyNewUVSet, "top", 0),
            (form2CopyNewUVSet, "left", 0),
            (form2CopyNewUVSet, "right", 0),
        
            (btnCreateCopyNewUVSet, "left", 5),
            (btnCreateCopyNewUVSet, "bottom", 5),
            (btnCloseCopyNewUVSet, "right", 5),
            (btnCloseCopyNewUVSet, "bottom", 5),
        ],
        attachControl=[
            (form2CopyNewUVSet, "bottom", 0, btnCloseCopyNewUVSet),
        ],
        attachPosition=[
            (btnCreateCopyNewUVSet, "right", 2, 50),
            (btnCloseCopyNewUVSet, "left", 1, 50),
        ],
        attachNone=[
            (btnCreateCopyNewUVSet, "top"),
            (btnCloseCopyNewUVSet, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for creating a new UV set
def createSetUI():

    def createSetOptVar(varType): # Updates optVars

        if varType == 0:
            pm.optionVar["newUVSet_NSUV"] = fieldNewUVSet.getText()

        elif varType == 1:
            pm.optionVar["newUVSetShare_NSUV"] = radGrpNewUVSet.getSelect()

        else: print("Error. Wrong variable passed to createSetOptVar()")


    # Check for window duplicate
    if pm.window( winNewUVSet, exists=True ):
        pm.deleteUI(winNewUVSet)

    # Window
    window = pm.window(
        winNewUVSet,
        height=createSetWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Create New UV Set",
    )

    # Layouts
    form1NewUVSet = pm.formLayout()
    form2NewUVSet = pm.formLayout( parent=form1NewUVSet )
    frameNewUVSet = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Create UV Set Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2NewUVSet,
        width=smallWinX,
    )
    colNewUVSet = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameNewUVSet,
    )

    # Text field
    if mayaVer == 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: createSetOptVar(0),
            columnAlign=[1, "right"],
            columnWidth2=[smallCol1, smallCol2],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV Set name: ",
            parent=colNewUVSet,
            text=pm.optionVar["newUVSet_NSUV"],
        )
    else:
        fieldNewUVSet = pm.textFieldGrp(
            changeCommand=lambda *args: createSetOptVar(0),
            columnAlign=[1, "right"],
            columnWidth2=[smallCol1, smallCol2],
            forceChangeCommand=True,
            insertionPosition=0,
            label="UV set name: ",
            parent=colNewUVSet,
            text=pm.optionVar["newUVSet_NSUV"],
            textChangedCommand=lambda *args: createSetOptVar(0),
        )

    # Radio collection and radio buttons
    radGrpNewUVSet = pm.radioButtonGrp(
        changeCommand=lambda *args: createSetOptVar(1),
        columnAlign=[1, "right"],
        columnWidth2=[smallCol1, smallCol2],
        label1="Shared (default)",
        label2="Per Instance Shared",
        label3="Per Instance Unshared",
        label="UV set sharing: ",
        numberOfRadioButtons=3,
        parent=colNewUVSet,
        vertical=True,
    )

    # Edit the radio collection and select item
    radGrpNewUVSet.setSelect( pm.optionVar["newUVSetShare_NSUV"] )

    # Buttons    
    btnCreateNewUVSet = pm.button(
        command=lambda *args: core.createSet(scrollListUVSet, winNewUVSet, False),
        label="Create",
        parent=form1NewUVSet,
    )
    btnApplyNewUVSet = pm.button(
        command=lambda *args: core.createSet(scrollListUVSet, winNewUVSet, True),
        label="Apply",
        parent=form1NewUVSet,
    )
    btnCloseNewUVSet = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1NewUVSet,
    )

    # Layout frame
    pm.formLayout(
        form2NewUVSet, edit=True,
        attachForm=[
            (frameNewUVSet, "top", 0),
            (frameNewUVSet, "left", 0),
            (frameNewUVSet, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1NewUVSet, edit=True,
        attachForm=[
            (form2NewUVSet, "top", 0),
            (form2NewUVSet, "left", 0),
            (form2NewUVSet, "right", 0),
        
            (btnCreateNewUVSet, "left", 5),
            (btnCreateNewUVSet, "bottom", 5),
            (btnApplyNewUVSet, "bottom", 5),
            (btnCloseNewUVSet, "right", 5),
            (btnCloseNewUVSet, "bottom", 5),
        ],
        attachControl=[
            (form2NewUVSet, "bottom", 0, btnCloseNewUVSet),
        ],
        attachPosition=[
            (btnCreateNewUVSet, "right", 3, 33),
            (btnApplyNewUVSet, "left", 2, 33),
            (btnApplyNewUVSet, "right", 3, 66),
            (btnCloseNewUVSet, "left", 2, 66),
        ],
        attachNone=[
            (btnCreateNewUVSet, "top"),
            (btnApplyNewUVSet, "top"),
            (btnCloseNewUVSet, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for changing the straighten UVs options
def dispSettingsUI():

    # Reset UI
    def dispSettingsReset():

        # Update UI controls
        cBox1DispSettings.setValue1(True)
        cBox2DispSettings.setValue1(False)
        cBox3DispSettings.setValue1(True)
        cBox4DispSettings.setValue1(False)
        cBox5DispSettings.setValue1(True)
        cBox6DispSettings.setValue1(False)
        cBox7DispSettings.setValue1(True)
        radGrpDispSettings.setSelect(False)
        cBox8DispSettings.setValue1(True)
        cBox9DispSettings.setValue1(False)     
        cBox10DispSettings.setValue1(False)
        color1DispSettings.setRgbValue([0.0, 0.0, 1.0])
        alpha1DispSettings.setValue(0.25)
        color2DispSettings.setRgbValue([1.0, 0.0, 0.0])
        alpha2DispSettings.setValue(0.25)
        
        # Update optVars
        pm.optionVar["imgDisp_NSUV"] = True
        pm.optionVar["imgDim_NSUV"] = False
        pm.optionVar["imgFilter_NSUV"] = True
        pm.optionVar["imgRatio_NSUV"] = False
        pm.optionVar["editorBaking_NSUV"] = True
        pm.optionVar["checkers_NSUV"] = False
        pm.optionVar["tileLabels_NSUV"] = True
        pm.optionVar["imgRGBA_NSUV"] = False
        pm.optionVar["shellShade_NSUV"] = True
        pm.optionVar["shellBorder_NSUV"] = False
        pm.optionVar["shellDist_NSUV"] = False
        pm.optionVar["frontColor_NSUV"] = [0.0, 0.0, 1.0]
        pm.optionVar["frontAlpha_NSUV"] = 0.25
        pm.optionVar["backColor_NSUV"] = [1.0, 0.0, 0.0]
        pm.optionVar["backAlpha_NSUV"] = 0.25
        
        # Update display
        core.updateDisplay()
        

    # Apply settings
    def dispSettingsApply(win=None):
    
        # Set optVars
        pm.optionVar["imgDisp_NSUV"] = cBox1DispSettings.getValue1()
        pm.optionVar["imgDim_NSUV"] = cBox2DispSettings.getValue1()
        pm.optionVar["imgFilter_NSUV"] = cBox3DispSettings.getValue1()
        pm.optionVar["imgRatio_NSUV"] = cBox4DispSettings.getValue1()
        pm.optionVar["editorBaking_NSUV"] = cBox5DispSettings.getValue1()
        pm.optionVar["checkers_NSUV"] = cBox6DispSettings.getValue1()
        pm.optionVar["tileLabels_NSUV"] = cBox7DispSettings.getValue1()
        pm.optionVar["imgRGBA_NSUV"] = (radGrpDispSettings.getSelect() - 1) # 1 to 0-based index
        pm.optionVar["shellShade_NSUV"] = cBox8DispSettings.getValue1()
        pm.optionVar["shellBorder_NSUV"] = cBox9DispSettings.getValue1()     
        pm.optionVar["shellDist_NSUV"] = cBox10DispSettings.getValue1()
        pm.optionVar["frontColor_NSUV"] = color1DispSettings.getRgbValue()
        pm.optionVar["frontAlpha_NSUV"] = alpha1DispSettings.getValue()
        pm.optionVar["backColor_NSUV"] = color2DispSettings.getRgbValue()
        pm.optionVar["backAlpha_NSUV"] = alpha2DispSettings.getValue()

        # Update display
        core.updateDisplay()
        
        # Close display settings window
        if win != None:
            pm.deleteUI(win)


    # Check for window duplicate
    if pm.window( winDispSettings, exists=True ):
        pm.deleteUI(winDispSettings)

    # Window
    window = pm.window(
        winDispSettings,
        height=dispSettingsWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Editor Display",
        width=largeWinX
    )

    # Create layouts
    form1DispSettings = pm.formLayout()
    scrollDispSettings = pm.scrollLayout( childResizable=True )
    form2DispSettings = pm.formLayout(parent=scrollDispSettings)
    
    frameDispSettings = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Image Display",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2DispSettings,
    )
    row1DispSettings = pm.rowLayout(
        columnAttach2=["left", "left"],
        columnWidth2=[230, 100],
        numberOfColumns=2,
        parent=frameDispSettings,
        rowAttach=[2, "top", 0],
    )
    col1DispSettings = pm.columnLayout(
        columnAlign="left",
        parent=row1DispSettings,
    )

    # Image Display: Elements
    cBox1DispSettings = pm.checkBoxGrp(
        columnWidth2=[(dispCol1+dispCol2), dispCol3],
        label="Texture: ",
        label1="Display",
        value1=pm.optionVar["imgDisp_NSUV"],
    )
    cBox2DispSettings = pm.checkBoxGrp(
        columnWidth2=[(dispCol1+dispCol2), dispCol3],
        label="",
        label1="Dimming",
        value1=pm.optionVar["imgDim_NSUV"],
    )
    cBox3DispSettings = pm.checkBoxGrp(
        columnWidth2=[(dispCol1+dispCol2), dispCol3],
        label="",
        label1="Filtering",
        value1=pm.optionVar["imgFilter_NSUV"],
    )
    cBox4DispSettings = pm.checkBoxGrp(
        columnWidth2=[(dispCol1+dispCol2), dispCol3],
        label="",
        label1="Ratio",
        value1=pm.optionVar["imgRatio_NSUV"],
    )
    sep1DispSettings = pm.separator(
        height=sepSpace2,
        horizontal=True,
        style="none",
        visible=True,
    )
    cBox5DispSettings = pm.checkBoxGrp(
        columnWidth2=[(dispCol1+dispCol2), dispCol3],
        label="UV Editor: ",
        label1="Baking",
        value1=pm.optionVar["editorBaking_NSUV"],
    )
    sep2DispSettings = pm.separator(
        height=sepSpace2,
        horizontal=True,
        style="none",
        visible=True,
    )

    col2DispSettings = pm.columnLayout(
        columnAlign="left",
        parent=row1DispSettings,
    )

    cBox6DispSettings = pm.checkBoxGrp(
        columnWidth2=[dispCol4, dispCol3],
        label="Tile: ",
        label1="Checkers",
        value1=pm.optionVar["checkers_NSUV"],
    )
    cBox7DispSettings = pm.checkBoxGrp(
        columnWidth2=[dispCol4, dispCol6],
        label="",
        label1="Labels",
        value1=pm.optionVar["tileLabels_NSUV"],
    )
    sep3DispSettings = pm.separator(
        height=sepSpace2,
        horizontal=True,
        style="none",
        visible=True,
    )
    radGrpDispSettings = pm.radioButtonGrp(
        columnWidth2=[dispCol4, dispCol6],
        label1="RGB",
        label2="Alpha",
        label="Channels: ",
        numberOfRadioButtons=2,
        select=pm.optionVar["imgRGBA_NSUV"],
        vertical=True,
    )
    
    # Projection: Frame and column
    frameShellDispSettings = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Shell Display",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2DispSettings,
    )
    row2DispSettings = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
        parent=frameShellDispSettings,
        rowAttach=[2, "top", 0],
    )
    col3DispSettings = pm.columnLayout(
        columnAlign="left",
        parent=row2DispSettings,
    )

    # Shell Display: UI elements
    color1DispSettings = pm.colorSliderGrp(
        columnWidth3=[ dispCol5, (dispCol2-25), (dispCol6) ],
        label="Front Color: ", 
        rgb=pm.optionVar["frontColor_NSUV"],
        )
    alpha1DispSettings = pm.floatSliderGrp(
        columnWidth3=[ dispCol5, (dispCol2-25), (dispCol6) ],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=1.00,
        label="Front Alpha: ",
        minValue=0.00,
        maxValue=1.00,
        precision=2,
        step=0.01,
        value=pm.optionVar["frontAlpha_NSUV"],
    )
    color2DispSettings = pm.colorSliderGrp(
        columnWidth3=[ dispCol5, (dispCol2-25), (dispCol6) ],
        label="Back Color: ", 
        rgb=pm.optionVar["backColor_NSUV"],
    )
    alpha2DispSettings = pm.floatSliderGrp(
        columnWidth3=[ dispCol5, (dispCol2-25), (dispCol6) ],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=1.00,
        label="Back Alpha: ",
        minValue=0.00,
        maxValue=1.00,
        precision=2,
        step=0.01,
        value=pm.optionVar["backAlpha_NSUV"],
    )

    col4DispSettings = pm.columnLayout(
        columnAlign="left",
        parent=row2DispSettings,
    )

    cBox8DispSettings = pm.checkBoxGrp(
        columnWidth2=[dispCol7, dispCol3],
        label="Shell: ",
        label1="Shading",
        value1=pm.optionVar["shellShade_NSUV"],
    )
    cBox9DispSettings = pm.checkBoxGrp(
        columnWidth2=[dispCol7, dispCol3],
        label="",
        label1="Borders",
        value1=pm.optionVar["shellBorder_NSUV"],
    )
    cBox10DispSettings = pm.checkBoxGrp(
        columnWidth2=[dispCol7, dispCol3],
        label="",
        label1="Distortion",
        value1=pm.optionVar["shellDist_NSUV"],
    )

    # Buttons    
    btnApplyCloseDispSettings = pm.button(
        command=lambda *args: dispSettingsApply(winDispSettings),
        label="Confirm",
        parent=form1DispSettings,
    )
    btnApplyDispSettings = pm.button(
        command=lambda *args: dispSettingsApply(),
        label="Apply",
        parent=form1DispSettings,
    )
    btnReseDispSettings = pm.button(
        command=lambda *args: dispSettingsReset(),
        label="Reset",
        parent=form1DispSettings,
    )
    btnCloseDispSettings = pm.button(
        command=lambda *args: pm.deleteUI(winDispSettings),
        label="Close",
        parent=form1DispSettings,
    )
    
    # Layout frames
    pm.formLayout(
        form2DispSettings, edit=True,
        attachForm=[
            (frameDispSettings, "top", 0),
            (frameDispSettings, "left", 0),
            (frameDispSettings, "right", 0),

            (frameShellDispSettings, "left", 0),
            (frameShellDispSettings, "right", 0),
        ],
        attachControl=[
            (frameShellDispSettings, "top", 0, frameDispSettings),
        ],
        attachNone=[
            (frameDispSettings, "bottom"),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1DispSettings, edit=True,
        attachForm=[
            (scrollDispSettings, "top", 0),
            (scrollDispSettings, "left", 0),
            (scrollDispSettings, "right", 0),

            (btnApplyCloseDispSettings, "left", 5),
            (btnApplyCloseDispSettings, "bottom", 5),
            (btnApplyDispSettings, "bottom", 5),
            (btnReseDispSettings, "bottom", 5),
            (btnCloseDispSettings, "right", 5),
            (btnCloseDispSettings, "bottom", 5),
        ],
        attachControl=[
            (scrollDispSettings, "bottom", 0, btnApplyCloseDispSettings),
        ],
        attachPosition=[
            (btnApplyCloseDispSettings, "right", 3, 25),
            (btnApplyDispSettings, "left", 2, 25),
            (btnApplyDispSettings, "right", 3, 50),
            (btnReseDispSettings, "right", 3, 75),
            (btnReseDispSettings, "left", 2, 50),
            (btnCloseDispSettings, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseDispSettings, "top"),
            (btnApplyDispSettings, "top"),
            (btnReseDispSettings, "top"),
            (btnCloseDispSettings, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)
    

# UI for distributing shells
def distributeUI():

    # Vars
    visState1, visState2 = (True,)*2

    # Switch distribution method
    def distrSwitch():
    
        # Standard. Hide towards target -controls
        if radGrpDistr.getSelect() == 1:
            frameSettingsDistr.setVisible(True)            
            textTTDistr.setVisible(False)
            imgTTDistr.setVisible(False)

        # Towards target. Hide standard frames.
        else:
            frameMainDistr.setVisible(True)
            frameSettingsDistr.setVisible(False)            
            textTTDistr.setVisible(True)
            imgTTDistr.setVisible(True)

        # Save optVar
        pm.optionVar["distrMethod_NSUV"] = radGrpDistr.getSelect()


    # Reset UI
    def distrUIReset():

        # Update UI controls
        radGrpDistr.setSelect(1)
        menuSettingsDistr.setSelect(1)
        cBoxSpaceDistr.setValue1(True)
        fieldGrpDistr.setValue1(0.0000)
        fieldGrpDistr.setEnable(True)
        btnSpaceDistr.setEnable(True)
        textSpaceDistr.setEnable(True)

        # Reset optVars
        pm.optionVar["distrMethod_NSUV"] = 1
        pm.optionVar["distrDir_NSUV"] = 1
        pm.optionVar["distrSpacing_NSUV"] = True
        pm.optionVar["distrSpaceVal_NSUV"] = 0.0000
        
        # Switch to the correct layouts
        distrSwitch()
    

    # Update optVar
    def distrOptVar(varType, control=None, control2=None):

        if varType == 0:
            pm.optionVar["distrDir_NSUV"] = menuSettingsDistr.getSelect()

        elif varType == 1:
            pm.optionVar["distrSpacing_NSUV"] = status = cBoxSpaceDistr.getValue1()

            # Enable/Disable controls
            if status == True:
                btnSpaceDistr.setEnable(True)
                textSpaceDistr.setEnable(True)
                fieldGrpDistr.setEnable(True)
            else:
                btnSpaceDistr.setEnable(False)
                textSpaceDistr.setEnable(False)
                fieldGrpDistr.setEnable(False)

        elif varType == 2:
            val = pm.optionVar["manipAmt_NSUV"]
            pm.optionVar["distrSpaceVal_NSUV"] = val
            fieldGrpDistr.setValue1(val)

        elif varType == 3:
            pm.optionVar["distrSpaceVal_NSUV"] = fieldGrpDistr.getValue1()


    # Check for window duplicate
    if pm.window( winDistr, exists=True ):
        pm.deleteUI(winDistr)

    # Read UI control optVars - Set visibility states
    if pm.optionVar["distrSpacing_NSUV"] == False:
        visState1 = False
        visState2 = False

    # Window
    window = pm.window(
        winDistr,
        height=distributeWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Distribute Shells",
        width=largeWinX
    )

    # Create layouts
    form1Distr = pm.formLayout()
    scrollDistr = pm.scrollLayout( childResizable=True )
    form2Distr = pm.formLayout( parent=scrollDistr )

    frameMainDistr = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Distribute Options",
        parent=form2Distr
    )

    # Method radioBtnGrp
    radGrpDistr = pm.radioButtonGrp(
        changeCommand=lambda *args: distrSwitch(),
        columnWidth2=[largeCol1, largeCol2+30],
        label="Method: ",
        labelArray2=["Standard", "Towards target"],
        numberOfRadioButtons=2,
        parent=frameMainDistr,
        select=pm.optionVar["distrMethod_NSUV"],
        vertical=True,
    )


    ## Standard

    # Standard: Settings frame and column
    frameSettingsDistr = pm.frameLayout(
        label="Settings",
        parent=form2Distr
    )
    colSettingsDistr = pm.columnLayout(
        parent=frameSettingsDistr
    )

    # Create direction layout
    form3Distr = pm.formLayout( parent=colSettingsDistr )

    # Create direction elements  
    menuSettingsDistr = pm.optionMenuGrp(
        changeCommand=lambda *args: distrOptVar(0),
        columnWidth2=[largeCol1, largeCol2],
        label="Direction: ",
        parent=form3Distr,
    )

    itemRight = pm.menuItem(label="Right")
    itemLeft = pm.menuItem(label="Left")    
    itemTop = pm.menuItem(label="Top")
    itemBottom = pm.menuItem(label="Bottom")

    menuSettingsDistr.setSelect(pm.optionVar["distrDir_NSUV"])
  
    cBoxSpaceDistr = pm.checkBoxGrp(
        changeCommand=lambda *args: distrOptVar(1),
        columnWidth2=[largeCol1, largeCol2],
        label="Shell spacing: ",
        label1="",
        value1=pm.optionVar["distrSpacing_NSUV"],
    )
    fieldGrpDistr = pm.floatFieldGrp(
        changeCommand=lambda *args: distrOptVar(3),
        columnWidth2=[largeCol1, largeCol2],
        enable=visState2,
        label="Shell padding (Units): ",
        precision=4,
        value1=pm.optionVar["distrSpaceVal_NSUV"],
    )    
    btnSpaceDistr = pm.button(
        command=lambda *args: distrOptVar(2),
        enable=visState1,
        label="Copy from field*",
    )
    textSpaceDistr = pm.text(
        enable=visState1,
        label="* The NSUV manipulator field",
    )


    # Layout direction frame
    pm.formLayout(
        form3Distr, edit=True,
        attachForm=[
            (menuSettingsDistr, "top", 0),
            (menuSettingsDistr, "left", 0),
            
            (cBoxSpaceDistr, "left", 0),

            (fieldGrpDistr, "left", 0),

            (textSpaceDistr, "left", 110),
        ],
        attachControl=[            
            (cBoxSpaceDistr, "top", 10, menuSettingsDistr),
            
            (fieldGrpDistr, "top", 0, cBoxSpaceDistr),
            
            (btnSpaceDistr, "top", 0, cBoxSpaceDistr),
            (btnSpaceDistr, "left", 0, fieldGrpDistr),
            
            (textSpaceDistr, "top", 10, btnSpaceDistr),            
        ],
    )


    ## Towards target
    
    textTTDistr = pm.text(
        label="No options here - Instead, shells will be distributed towards \na target shell " \
"like in the picture below. The target shell can\nbe located above, below, right or left of your stack.",
        parent=form2Distr,
    )
    
    imgTTDistr = pm.image(
        image=iconDict["distr2Target"],
        parent=form2Distr,
    )

    # Buttons
    btnApplyCloseDistr = pm.button(
        command=lambda *args: core.distributeShells(winDistr),
        label="Confirm",
        parent=form1Distr,
    )
    btnApplyDistr = pm.button(
        command=lambda *args: core.distributeShells(),
        label="Apply",
        parent=form1Distr,
    )
    btnResetDistr = pm.button(
        command=lambda *args: distrUIReset(),
        label="Reset",
        parent=form1Distr,
    )
    btnCloseDistr = pm.button(
        command=lambda *args: pm.deleteUI(winDistr),
        label="Close",
        parent=form1Distr,
    )
    
    # Layout frames
    pm.formLayout(
        form2Distr, edit=True,
        attachForm=[
            (frameMainDistr, "top", 0),
            (frameMainDistr, "left", 0),
            (frameMainDistr, "right", 0),

            (frameSettingsDistr, "left", 0),
            (frameSettingsDistr, "right", 0),

            (textTTDistr, "left", 0),
            (textTTDistr, "right", 0),

            (imgTTDistr, "left", 0),            
            # (imgTTDistr, "right", 0),
        ],
        attachControl=[
            (frameSettingsDistr, "top", 10, frameMainDistr),
            (textTTDistr, "top", 0, frameSettingsDistr),
            (imgTTDistr, "top", 10, textTTDistr),
        ],
        attachNone=[
            (imgTTDistr, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1Distr, edit=True,
        attachForm=[
            (scrollDistr, "top", 0),
            (scrollDistr, "left", 0),
            (scrollDistr, "right", 0),

            (btnApplyCloseDistr, "left", 5),
            (btnApplyCloseDistr, "bottom", 5),
            (btnApplyDistr, "bottom", 5),
            (btnResetDistr, "bottom", 5),
            (btnCloseDistr, "right", 5),
            (btnCloseDistr, "bottom", 5),
        ],
        attachControl=[
            (scrollDistr, "bottom", 0, btnApplyCloseDistr),
        ],
        attachPosition=[
            (btnApplyCloseDistr, "right", 3, 25),
            (btnApplyDistr, "left", 2, 25),
            (btnApplyDistr, "right", 3, 50),
            (btnResetDistr, "right", 3, 75),
            (btnResetDistr, "left", 2, 50),
            (btnCloseDistr, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseDistr, "top"),
            (btnApplyDistr, "top"),
            (btnResetDistr, "top"),
            (btnCloseDistr, "top"),
        ],
    )

    # Hide inactive
    distrSwitch()

    # Display the window
    pm.showWindow(window)


# FAQ UI
def faqUI():

    # Check for window duplicate
    if pm.window( winFAQ, exists=True ):
        pm.deleteUI(winFAQ)

    # Window
    window = pm.window(
        winFAQ,
        height=largeWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="FAQ",
        width=largeWinX
    )
    
    # Main column
    colMainFAQ = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
    )
    
    # Title image
    imageWorkflow = pm.image(
        image=iconDict["faq"],
        parent=colMainFAQ,
    )
    
    scrollFaq = pm.scrollLayout(
        childResizable=True,
        height=largeWinY,
        width=largeWinX,
    )
    
    # Secondary column
    colSecFaq = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=frameX, 
    )    
    
    # FAQ
    frameFAQ = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Common Questions",
        parent=colSecFaq,
    )
    colFAQ = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameFAQ,
        width=frameX,
    )
    
    textFaq = pm.scrollField(
        text="Q: Will NSUV interfere with other UV Editors that I use?\n"\
"A: No, it shouldn't! NSUV does not modify any native files! Additionally NSUV comes with"\
" a button for quickly switching to the native editor if/when you need it. \n\nNOTE: if your"\
" studio is using in-house scripts/tools hacked into the native Maya Editor, then you need to"\
" edit some rows in core.py for sourcing a custom script. More instructions are located in "\
"core.py under the function defaultEditor().\n\n"\
"Q: How do I flip shells vertically?\n"\
"A: Right-click the Flip UVs icon. Keep in mind that many icons in NSUV have double"\
" functionality like this. Other examples are Unfold Along U/V and Normalize Along U/V.\n\n"\
"Q: How do I use variables for the manipulator and texel density fields?\n"\
"A: Right-click an icon to WRITE a value and left-click it to READ a stored value.\n\n"\
"Q: How do I copy a UV Set with the integrated UV Set Editor?\n"\
"A: Click and hold the button on the copy icon. A popup menu will appear.\n\n"\
"Q: How do I do a planar projection or access the planar projection options?\n"\
"A: Click and hold the planar projection button. A popup menu will appear.\n\n"\
"Q: How do I rename a UV set?\n"\
"A: Double-click on it in the UV Set list.\n\n"\
"Q: NSUV is taking up too much screen space, how can I make it smaller?\n"\
"A: The window is scalable and the frames and icon groups can all be collapsed (hidden).\n\n"\
"Q: Where are the U and V input fields?\n"\
"A: NSUV only has one general-purpose field. Use it for both U and V manipulations.\n\n"\
"Q: Running Straighten shell doesn't work, what's wrong?\n"\
"A: Make sure that you have a legal selection active, such as no edges shared by two shells. "\
"See the manual for details.\n\n"\
"Q: Icons are missing! How do I get them back?\n"\
"A: You forgot to copy the prefs -folder from the NSUV zip file.\n\n"\
"Q: How do I reset all settings in NSUV?\n"\
"A: Close down the NSUV window, then open up the script editor (Python tab) and execute this:\n"\
"NSUV.core.resetOptVars()\n\n"\
"Q: My question isn't answered here, where can I send it?\n"\
"A: Send it to martin.dahlin@live.com\n",
        editable=False,
        height=largeWinY*1.9,
        parent=colFAQ,
        width=frameX,
        wordWrap=True,
    )

    # Button
    btnCloseFaq = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainFAQ,
        width=largeWinX,
    )

    # Display the window
    pm.showWindow(window)


# Options UI for layout
def layoutUI():

    # Vars
    layoutMethodVar = pm.optionVar["layoutMode_NSUV"]
    multiObjVar = pm.optionVar["layoutPackMode_NSUV"]
    u3dLoaded = pm.pluginInfo("Unfold3D", loaded=True, query=True)
    rad1PlaceLayout, rad2PlaceLayout, rad3PlaceLayout, rad4PlaceLayout, rad5PlaceLayout, \
    rad6PlaceLayout, rad7PlaceLayout, rad8PlaceLayout, rad9PlaceLayout, rad1PlaceLayout, \
    rad2PlaceLayout, rad3PlaceLayout, = (None,)*12

    # Switch UI controls
    def layoutControlSwitch():
        placeState = pm.optionVar["layoutPlace_NSUV"]

        if mayaVer >= 201650 and u3dLoaded:
            if radGrpLayout.getSelect() == 1:
                sliderResLayout.setVisible(True)
                sliderIterLayout.setVisible(True)
                menuTypeLayout.setVisible(False)
                cBoxMultiTileLayout.setVisible(True)

                if radGrpLayout.getSelect() == 1 and cBoxMultiTileLayout.getValue1() == True: 
                    rowTileLayout.setVisible(True)
                else: rowTileLayout.setVisible(False)

                radGrpSeparateLayout.setVisible(False)
                cBoxFlipLayout.setVisible(False)
                sep1Layout.setVisible(True)
                cBoxXformTransLayout.setVisible(True)
                menuXformDistrLayout.setVisible(True)

                if cBoxXformRotateLayout.getValue1() == True:
                    radGrpRotLayout.setVisible(False)
                    fieldGrpXformRotStepLayout.setVisible(True)
                    rowRotateLayout.setVisible(True)
                else:
                    radGrpRotLayout.setVisible(False)
                    fieldGrpXformRotStepLayout.setVisible(False)
                    rowRotateLayout.setVisible(False)

                menuScaleLayout.setVisible(True)
                itemNonUni.setEnable(True)
                radGrpFitLayout.setVisible(False)
                menuPreXformRotLayout.setVisible(True)
                menuSpaceLayout.setVisible(False)
                fieldGrpShellPaddingLayout.setVisible(True)
                fieldGrpShellPaddingOldLayout.setVisible(False)
                fieldGrpTilePaddingLayout.setVisible(True)

                if placeState == 1:
                    rowRangeULayout.setVisible(False)
                    rowRangeVLayout.setVisible(False)
                    formPlaceLayout.setVisible(True)
                else:
                    rowRangeULayout.setVisible(True)
                    rowRangeVLayout.setVisible(True)
                    formPlaceLayout.setVisible(False)

            elif radGrpLayout.getSelect() == 2:
                sliderResLayout.setVisible(False)
                sliderIterLayout.setVisible(False)
                menuTypeLayout.setVisible(True)
                cBoxMultiTileLayout.setVisible(False)

                if menuTypeLayout.getSelect() == 4: rowTileLayout.setVisible(True)
                else: rowTileLayout.setVisible(False)

                if radGrpModeLayout.getSelect() == 1: radGrpSeparateLayout.setVisible(False)
                else: radGrpSeparateLayout.setVisible(True)

                cBoxFlipLayout.setVisible(True)
                sep1Layout.setVisible(False)
                cBoxXformTransLayout.setVisible(False)
                menuXformDistrLayout.setVisible(False)

                if cBoxXformRotateLayout.getValue1() == 1:
                    radGrpRotLayout.setVisible(True)
                else:
                    radGrpRotLayout.setVisible(False)

                fieldGrpXformRotStepLayout.setVisible(False)
                rowRotateLayout.setVisible(False)

                radGrpFitLayout.setVisible(True)
                menuPreXformRotLayout.setVisible(False)
                menuSpaceLayout.setVisible(True)
                fieldGrpShellPaddingLayout.setVisible(False)
                fieldGrpShellPaddingOldLayout.setVisible(True)
                fieldGrpTilePaddingLayout.setVisible(False)

                if menuTypeLayout.getSelect() <= 2:
                    itemNonUni.setEnable(True)
                    if placeState == 1:
                        rowRangeULayout.setVisible(False)
                        rowRangeVLayout.setVisible(False)
                        formPlaceLayout.setVisible(True)
                    else:
                        rowRangeULayout.setVisible(True)
                        rowRangeVLayout.setVisible(True)
                        formPlaceLayout.setVisible(False)
                else:
                    itemNonUni.setEnable(False)
                    if menuScaleLayout.getSelect() == 3: menuScaleLayout.setSelect(1)

        else:

            if radGrpLayout.getSelect() != 3:
                sliderResLayout.setVisible(False)
                sliderIterLayout.setVisible(False)
                menuTypeLayout.setVisible(True)
                cBoxMultiTileLayout.setVisible(False)

                if radGrpLayout.getSelect() != 3 and menuTypeLayout.getSelect() == 4: rowTileLayout.setVisible(True)
                else: rowTileLayout.setVisible(False)

                if radGrpLayout.getSelect() == 1: radGrpSeparateLayout.setVisible(False)
                elif radGrpLayout.getSelect() == 2: radGrpSeparateLayout.setVisible(True)

                cBoxFlipLayout.setVisible(True)
                sep1Layout.setVisible(False)
                cBoxXformTransLayout.setVisible(False)
                menuXformDistrLayout.setVisible(False)

                if cBoxXformRotateLayout.getValue1() == 1: radGrpRotLayout.setVisible(True)
                else: radGrpRotLayout.setVisible(False)

                fieldGrpXformRotStepLayout.setVisible(False)
                rowRotateLayout.setVisible(False)
                menuScaleLayout.setVisible(True)
                radGrpFitLayout.setVisible(True)
                menuPreXformRotLayout.setVisible(False)
                menuSpaceLayout.setVisible(True)
                fieldGrpShellPaddingLayout.setVisible(False)
                fieldGrpShellPaddingOldLayout.setVisible(True)
                fieldGrpTilePaddingLayout.setVisible(False)

                if menuTypeLayout.getSelect() <= 3:
                    itemNonUni.setEnable(True)
                    if placeState == 1:
                        rowRangeULayout.setVisible(False)
                        rowRangeVLayout.setVisible(False)
                        formPlaceLayout.setVisible(True)
                    else:
                        rowRangeULayout.setVisible(True)
                        rowRangeVLayout.setVisible(True)
                        formPlaceLayout.setVisible(False)
                else:
                    itemNonUni.setEnable(False)
                    if menuScaleLayout.getSelect() == 3: menuScaleLayout.setSelect(2)


    # Switch UI frames
    def layoutFrameSwitch():

        layoutState = pm.optionVar["layoutShell_NSUV"]

        if mayaVer >= 201650 and u3dLoaded:
            if radGrpLayout.getSelect() == 1:
                frameShellLayout.setVisible(True)
                framePreXformLayout.setVisible(True)
                itemPreScaleA.setLabel("Preserve 3D Ratio")
                itemPreScaleB.setLabel("Preserve UV Ratio")

                if menuTypeLayout.getSelect() == 2:
                    frameSpacingLayout.setVisible(True)
                    framePlaceLayout.setVisible(True)
                elif menuTypeLayout.getSelect() == 3:
                    frameSpacingLayout.setVisible(False)
                    framePlaceLayout.setVisible(True)
                else:
                    frameSpacingLayout.setVisible(True)
                    framePlaceLayout.setVisible(False)

                frameQuickLayout.setVisible(False)

            elif radGrpLayout.getSelect() == 2:
                frameShellLayout.setVisible(True)

                if radGrpModeLayout.getSelect() == 1: framePreXformLayout.setVisible(True)
                else: framePreXformLayout.setVisible(False)
                itemPreScaleA.setLabel("Object")
                itemPreScaleB.setLabel("World")

                if menuTypeLayout.getSelect() == 3: frameSpacingLayout.setVisible(False)
                else: frameSpacingLayout.setVisible(True)

                if radGrpModeLayout.getSelect() == 1:
                    if layoutState == 2: 
                        frameSpacingLayout.setVisible(True)
                        framePlaceLayout.setVisible(True)
                    elif layoutState >= 4:
                        frameSpacingLayout.setVisible(True)
                        framePlaceLayout.setVisible(False)
                    else: # 1 or 3
                        frameSpacingLayout.setVisible(False)
                        framePlaceLayout.setVisible(True)
                else: 
                    if layoutState == 1 or layoutState == 3: frameSpacingLayout.setVisible(False)
                    else: frameSpacingLayout.setVisible(True)
                    framePlaceLayout.setVisible(False)

                frameQuickLayout.setVisible(False)

            else: # Quick
                frameShellLayout.setVisible(False)
                framePreXformLayout.setVisible(False)
                frameSpacingLayout.setVisible(False)
                framePlaceLayout.setVisible(False)
                frameQuickLayout.setVisible(True)

        else:
            if radGrpLayout.getSelect() != 3:
                frameShellLayout.setVisible(True)

                if radGrpLayout.getSelect() == 1:
                    framePreXformLayout.setVisible(True)
                    itemPreScaleA.setLabel("Object")
                    itemPreScaleB.setLabel("World")

                    if layoutState <= 3: framePlaceLayout.setVisible(True)
                    else: framePlaceLayout.setVisible(False)

                elif radGrpLayout.getSelect() == 2:
                    framePreXformLayout.setVisible(False)
                    framePlaceLayout.setVisible(False)

                if menuTypeLayout.getSelect() == 1: frameSpacingLayout.setVisible(False)
                elif menuTypeLayout.getSelect() == 3: frameSpacingLayout.setVisible(False)

                else: frameSpacingLayout.setVisible(True)

                frameQuickLayout.setVisible(False)

            else: # Quick
                frameShellLayout.setVisible(False)
                framePreXformLayout.setVisible(False)
                frameSpacingLayout.setVisible(False)
                framePlaceLayout.setVisible(False)
                frameQuickLayout.setVisible(True)

        # Save optVar
        pm.optionVar["layoutMode_NSUV"] = radGrpLayout.getSelect()

        layoutControlSwitch()


    # Update optVar
    def layoutOptVar(varType, control=None, control2=None, radBtn=None):

        if varType == 1:
            pm.optionVar["layoutGridUVal_NSUV"] = fieldTileULayout.getValue1()
            pm.optionVar["layoutGridVVal_NSUV"] = fieldTileVLayout.getValue1()

        elif varType == 2:
            pm.optionVar["layoutFlip_NSUV"] = cBoxFlipLayout.getValue1()

        elif varType == 3:
            pm.optionVar["layoutMultiTile_NSUV"] = cBoxMultiTileLayout.getValue1()
            layoutFrameSwitch()

        elif varType == 4:
            pm.optionVar["layoutFitting_NSUV"] = radGrpFitLayout.getSelect()

        elif varType == 5:
            pm.optionVar["layoutRotateOld_NSUV"] = radGrpRotLayout.getSelect()

        elif varType == 6:
            pm.optionVar["layoutSpaceMenu_NSUV"] = val = menuSpaceLayout.getSelect()

            if val == 1: # Custom
                pm.optionVar["layoutShellPadding_NSUV"] = fieldGrpShellPaddingOldLayout.getValue1()

            elif val == 2: # 8192
                fieldGrpShellPaddingOldLayout.setValue1(0.012)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.012

            elif val == 3:
                fieldGrpShellPaddingOldLayout.setValue1(0.055)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.055

            elif val == 4:
                fieldGrpShellPaddingOldLayout.setValue1(0.100)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.100

            elif val == 5: # 1024
                fieldGrpShellPaddingOldLayout.setValue1(0.200)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.200

            elif val == 6:
                fieldGrpShellPaddingOldLayout.setValue1(0.400)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.400

            elif val == 7:
                fieldGrpShellPaddingOldLayout.setValue1(0.840)
                pm.optionVar["layoutShellPadding_NSUV"] = 0.840

            elif val == 8: # 128
                fieldGrpShellPaddingOldLayout.setValue1(1.630)
                pm.optionVar["layoutShellPadding_NSUV"] =  1.630

            elif val == 9:
                fieldGrpShellPaddingOldLayout.setValue1(3.750)
                pm.optionVar["layoutShellPadding_NSUV"] = 3.750

        elif varType == 7:
            pm.optionVar["layoutShellPadding_NSUV"] = fieldGrpShellPaddingOldLayout.getValue1()
            menuSpaceLayout.setSelect(1) # Set to Custom

        elif varType == 8:
            pm.optionVar["layoutRes_NSUV"] = sliderResLayout.getValue()

        elif varType == 9:
            pm.optionVar["layoutItr_NSUV"] = sliderIterLayout.getValue()

        elif varType == 10:
            pm.optionVar["layoutTranslate_NSUV"] = cBoxXformTransLayout.getValue1()

        elif varType == 11:
            pm.optionVar["layoutDistr_NSUV"] = menuXformDistrLayout.getSelect()

        elif varType == 12:
            if radBtn == 1:
                pm.optionVar["layoutPlacePres_NSUV"] = 1
            elif radBtn == 2:
                pm.optionVar["layoutPlacePres_NSUV"] = 2
            elif radBtn == 3:
                pm.optionVar["layoutPlacePres_NSUV"] = 3
            elif radBtn == 4:
                pm.optionVar["layoutPlacePres_NSUV"] = 4
            elif radBtn == 5:
                pm.optionVar["layoutPlacePres_NSUV"] = 5
            elif radBtn == 6:
                pm.optionVar["layoutPlacePres_NSUV"] = 6
            elif radBtn == 7:
                pm.optionVar["layoutPlacePres_NSUV"] = 7
            elif radBtn == 8:
                pm.optionVar["layoutPlacePres_NSUV"] = 8
            elif radBtn == 9:
                pm.optionVar["layoutPlacePres_NSUV"] = 9

            control.setSelect()

        elif varType == 13:
            if radBtn == 1:
                pm.optionVar["layoutQuickType_NSUV"] = 1
            elif radBtn == 2:
                pm.optionVar["layoutQuickType_NSUV"] = 2
            elif radBtn == 3:
                pm.optionVar["layoutQuickType_NSUV"] = 3

            control.setSelect()

        elif varType == 14:
            pm.optionVar["layoutSepShells_NSUV"] = radGrpSeparateLayout.getSelect()
            layoutFrameSwitch()

        elif varType == 15:
            pm.optionVar["layoutRotStep_NSUV"] = fieldGrpXformRotStepLayout.getValue1()

        elif varType == 16:
            pm.optionVar["layoutRotMin_NSUV"] = fieldRotMinLayout.getValue1()

        elif varType == 17:
            pm.optionVar["layoutRotMax_NSUV"] = fieldRotMaxLayout.getValue1()

        elif varType == 18:
            pm.optionVar["layoutScaling_NSUV"] = menuScaleLayout.getSelect()

        elif varType == 19:
            pm.optionVar["layoutPreXformFrame_NSUV"] = framePreXformLayout.getCollapse()

        elif varType == 20:
            pm.optionVar["layoutPreRotation_NSUV"] = menuPreXformRotLayout.getSelect()

        elif varType == 21:
            pm.optionVar["layoutPreScaling_NSUV"] = menuPreXformScaleLayout.getSelect()

        elif varType == 22:
            pm.optionVar["layoutShellPadding_NSUV"] = fieldGrpShellPaddingLayout.getValue1()

        elif varType == 23:
            pm.optionVar["layoutShellPaddingOld_NSUV"] = fieldGrpShellPaddingOldLayout.getValue1()

        elif varType == 24:
            pm.optionVar["layoutTilePadding_NSUV"] = fieldGrpTilePaddingLayout.getValue1()

        elif varType == 25:
            pm.optionVar["layoutRangeMinU_NSUV"] = fieldRangeMinULayout.getValue1()

        elif varType == 26:
            pm.optionVar["layoutRangeMaxU_NSUV"] = fieldRangeMaxULayout.getValue1()

        elif varType == 27:
            pm.optionVar["layoutRangeMinV_NSUV"] = fieldRangeMinVLayout.getValue1()

        elif varType == 28:
            pm.optionVar["layoutRangeMaxV_NSUV"] = fieldRangeMaxVLayout.getValue1()

        elif varType == 29:
            pm.optionVar["layoutPackMode_NSUV"] = radGrpModeLayout.getSelect()
            layoutFrameSwitch()
            
        elif varType == 30:
            pm.optionVar["layoutShell_NSUV"] = menuTypeLayout.getSelect()
            layoutFrameSwitch()

        elif varType == 31:
            pm.optionVar["layoutRotate_NSUV"] = cBoxXformRotateLayout.getValue1()
            layoutControlSwitch()

        elif varType == 32:
            pm.optionVar["layoutPlace_NSUV"] = menuPlaceLayout.getSelect()
            layoutControlSwitch()

        elif varType == 33:
            pm.optionVar["layoutSpacingFrame_NSUV"] = frameSpacingLayout.getCollapse()

        elif varType == 34:
            pm.optionVar["layoutPlacementFrame_NSUV"] = framePlaceLayout.getCollapse()


    # Reset UI
    def layoutUIReset():

        # Reset UI controls
        if mayaVer >= 201650: radGrpLayout.setSelect(1) # 2016 Ext 2
        else: radGrpLayout.setSelect(2)
        if mayaVer >= 201650 and u3dLoaded: radGrpModeLayout.setSelect(1) # ...and Unfold3D loaded
        sliderResLayout.setValue(256)
        sliderIterLayout.setValue(1)
        menuTypeLayout.setSelect(2)
        cBoxMultiTileLayout.setValue1(False)
        fieldTileULayout.setValue1(1)
        fieldTileVLayout.setValue1(1)
        radGrpSeparateLayout.setSelect(3)
        cBoxFlipLayout.setValue1(True)
        cBoxXformTransLayout.setValue1(True)
        menuXformDistrLayout.setSelect(1)
        cBoxXformRotateLayout.setValue1(False)
        radGrpRotLayout.setSelect(1)
        fieldGrpXformRotStepLayout.setValue1(90)
        fieldRotMinLayout.setValue1(0.0000)
        fieldRotMaxLayout.setValue1(360.0000)
        menuScaleLayout.setSelect(2)
        radGrpFitLayout.setSelect(2)
        framePreXformLayout.setCollapse(True)
        menuPreXformRotLayout.setSelect(1)
        menuPreXformScaleLayout.setSelect(1)
        frameSpacingLayout.setCollapse(True)
        menuSpaceLayout.setSelect(5)
        fieldGrpShellPaddingLayout.setValue1(0.0000)
        fieldGrpShellPaddingOldLayout.setValue1(0.2000)
        fieldGrpTilePaddingLayout.setValue1(0.0000)
        framePlaceLayout.setCollapse(False)
        menuPlaceLayout.setSelect(1)
        fieldRangeMinULayout.setValue1(0.0)
        fieldRangeMaxULayout.setValue1(1.0)
        fieldRangeMinVLayout.setValue1(0.0)
        fieldRangeMaxVLayout.setValue1(1.0)
        radColPlaceLayout.setSelect(rad1PlaceLayout)
        radColQuickLayout.setSelect(rad1QuickLayout)

        # Reset optVars
        if mayaVer >= 201650: pm.optionVar["layoutMode_NSUV"] = 1 # 2016 Ext 2
        else: pm.optionVar["layoutMode_NSUV"] = 2
        pm.optionVar["layoutPackMode_NSUV"] = 1
        pm.optionVar["layoutRes_NSUV"] = 256
        pm.optionVar["layoutItr_NSUV"] = 1
        pm.optionVar["layoutShell_NSUV"] = 2
        pm.optionVar["layoutMultiTile_NSUV"] = False
        pm.optionVar["layoutGridUVal_NSUV"] = 1
        pm.optionVar["layoutGridVVal_NSUV"] = 1
        pm.optionVar["layoutSepShells_NSUV"] = 2
        pm.optionVar["layoutFlip_NSUV"] = True
        pm.optionVar["layoutTranslate_NSUV"] = True
        pm.optionVar["layoutDistr_NSUV"] = 1
        pm.optionVar["layoutRotate_NSUV"] = False
        pm.optionVar["layoutRotateOld_NSUV"] = 2
        pm.optionVar["layoutRotStep_NSUV"] = 90
        pm.optionVar["layoutRotMin_NSUV"] = 0.0000
        pm.optionVar["layoutRotMax_NSUV"] = 360.0000
        pm.optionVar["layoutScaling_NSUV"] = 2
        pm.optionVar["layoutFitting_NSUV"] = 2
        pm.optionVar["layoutPreXformFrame_NSUV"] = True
        pm.optionVar["layoutPreRotation_NSUV"] = 1
        pm.optionVar["layoutPreScaling_NSUV"] = 1
        pm.optionVar["layoutSpacingFrame_NSUV"] = True
        pm.optionVar["layoutSpaceMenu_NSUV"] = 5
        pm.optionVar["layoutShellPadding_NSUV"] = 0.0000
        pm.optionVar["layoutShellPaddingOld_NSUV"] = 0.2000
        pm.optionVar["layoutTilePadding_NSUV"] = 0.0
        pm.optionVar["layoutPlacementFrame_NSUV"] = False
        pm.optionVar["layoutPlace_NSUV"] = 1
        pm.optionVar["layoutRangeMinU_NSUV"] = 0.0
        pm.optionVar["layoutRangeMaxU_NSUV"] = 1.0
        pm.optionVar["layoutRangeMinV_NSUV"] = 0.0
        pm.optionVar["layoutRangeMaxV_NSUV"] = 1.0
        pm.optionVar["layoutPlacePres_NSUV"] = 1
        pm.optionVar["layoutQuickType_NSUV"] = 1

        # Switch to the correct frames and controls
        layoutFrameSwitch()
        layoutControlSwitch()


    # Check for window duplicate
    if pm.window( winLayout, exists=True ):
        pm.deleteUI(winLayout)

    # Prevent menu select overflow
    if not mayaVer >= 201600 and pm.optionVar["layoutShell_NSUV"] > 3:
        pm.optionVar["layoutShell_NSUV"] = 1

    # Window
    window = pm.window(
        winLayout,
        height=layoutWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="Layout UVs",
        width=largeWinX
    )

    # Create layouts
    form1Layout = pm.formLayout()
    scroll1Layout = pm.scrollLayout( childResizable=True )
    form2Layout = pm.formLayout( parent=scroll1Layout )

    frameMainLayout = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Layout Options",
        parent=form2Layout
    )

    # Method radioBtnGrp
    if mayaVer >= 201650 and u3dLoaded: # 2016 Ext 2 Unfold3D
        radGrpLayout = pm.radioButtonGrp(
            changeCommand=lambda *args: layoutFrameSwitch(),
            columnWidth2=[largeCol1, largeCol2],
            label="Method: ",
            labelArray3=["Unfold3D", "Legacy", "Quick"],
            numberOfRadioButtons=3,
            parent=frameMainLayout,
            select=layoutMethodVar,
            vertical=True,
        )
    else:
        radGrpLayout = pm.radioButtonGrp(
            changeCommand=lambda *args: layoutFrameSwitch(),
            columnWidth2=[largeCol1, largeCol2+100],
            labelArray3=["Together (non-overlapping)", "Separatly (overlapping)", "Quick"],
            label="Method: ",
            numberOfRadioButtons=3,
            select=layoutMethodVar,
            vertical=True,
        )


    ## Unfold3D

    # Layout Settings frame and column
    frameShellLayout = pm.frameLayout(
        label="Settings",
        parent=form2Layout,
    )
    colShellLayout = pm.columnLayout(
        parent=frameShellLayout
    )

    # Layout Settings elements
    if mayaVer >= 201650 and u3dLoaded: # 2016 Ext 2 Unfold3D
        radGrpModeLayout = pm.radioButtonGrp(
            changeCommand=lambda *args: layoutOptVar(29),
            columnWidth2=[largeCol1, largeCol2+100],
            labelArray2=["Together (non-overlapping)", "Separatly (overlapping)"],
            label="Layout objects: ",
            numberOfRadioButtons=2,
            select=pm.optionVar["layoutPackMode_NSUV"],
            vertical=True,
        )
    sliderResLayout = pm.intSliderGrp(
        changeCommand=lambda *args: layoutOptVar(8),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        dragCommand=lambda *args: layoutOptVar(8),
        field=True,
        fieldStep=1,
        label="Resolution: ",
        max=4096,
        min=64,
        sliderStep=1,
        step=1,
        visible=True,
        value=pm.optionVar["layoutRes_NSUV"],
    )
    sliderIterLayout = pm.intSliderGrp(
        changeCommand=lambda *args: layoutOptVar(9),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        dragCommand=lambda *args: layoutOptVar(9),
        field=True,
        fieldStep=1,
        label="Iterations: ",
        max=50,
        min=1,
        sliderStep=1,
        step=1,
        visible=True,
        value=pm.optionVar["layoutItr_NSUV"],
    )
    
    menuTypeLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(30),
        columnWidth2=[largeCol1, largeCol2],
        label="Shell layout: ",
        parent=colShellLayout,
    )

    itemNone = pm.menuItem(label="None")
    itemDefault = pm.menuItem(label="Default (Into region)")
    itemAlongU = pm.menuItem(label="Along U")    
    if mayaVer >= 201600:
        itemTile = pm.menuItem(label="Multi-tile (UDIM)")
        itemNearest = pm.menuItem(label="Nearest tile")

    menuTypeLayout.setSelect(pm.optionVar["layoutShell_NSUV"])
    
    cBoxMultiTileLayout = pm.checkBoxGrp(
        changeCommand=lambda *args: layoutOptVar(3), 
        columnWidth2=[largeCol1, largeCol2],
        label="Multi-tile (UDIM): ",
        label1="",
        value1=pm.optionVar["layoutMultiTile_NSUV"],
    )
    
    rowTileLayout = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
    )

    fieldTileULayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(1),
        columnWidth2=[largeCol1, largeCol2],
        label="Tiles U: ",
        parent=rowTileLayout,
        value1=pm.optionVar["layoutGridUVal_NSUV"],
    )
    fieldTileVLayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(1),
        columnAlign2=["left", "left"],
        columnWidth=[1, 12],
        label="V:",
        parent=rowTileLayout,
        value1=pm.optionVar["layoutGridVVal_NSUV"],
    )

    pm.setParent('..') # Set default parent to one step up
    
    radGrpSeparateLayout = pm.radioButtonGrp(
        changeCommand=lambda *args: layoutOptVar(14),
        columnWidth2=[largeCol1, largeCol2+100],
        labelArray3=["Off", "Along folds", "All intersecting"],
        label="Cut UV edges: ",
        numberOfRadioButtons=3,
        select=pm.optionVar["layoutSepShells_NSUV"],
        vertical=True,
    )
    
    cBoxFlipLayout = pm.checkBoxGrp(
        changeCommand=lambda *args: layoutOptVar(2),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Flip reversed",
        value1=pm.optionVar["layoutFlip_NSUV"],
    )

    sep1Layout = pm.separator(
        height=sepSpace2,
        parent=colShellLayout,
        style="in",
        width=largeWinX-12,
    )

    cBoxXformTransLayout = pm.checkBoxGrp(
        changeCommand=lambda *args: layoutOptVar(10),
        columnWidth2=[largeCol1, largeCol2],
        label="Translation: ",
        label1="",
        value1=pm.optionVar["layoutTranslate_NSUV"],
    )
    menuXformDistrLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(11),
        columnWidth2=[largeCol1, largeCol2],
        label="Shell distribution: ",
        parent=colShellLayout,
    )

    itemDistr = pm.menuItem(label="Distribute")    
    itemShellCenters = pm.menuItem(label="Shell centers")

    menuXformDistrLayout.setSelect(pm.optionVar["layoutDistr_NSUV"])

    sep2Layout = pm.separator(
        height=sepSpace2,
        parent=colShellLayout,
        style="in",
        width=largeWinX-12,
    )

    cBoxXformRotateLayout = pm.checkBoxGrp(
        changeCommand=lambda *args: layoutOptVar(31),
        columnWidth2=[largeCol1, largeCol2],
        label="Rotation: ",
        label1="",
        value1=pm.optionVar["layoutRotate_NSUV"],
    )   

    radGrpRotLayout = pm.radioButtonGrp(
        changeCommand=lambda *args: layoutOptVar(5),
        columnWidth2=[largeCol1, largeCol2],
        label1=("90" + u"\u00B0" + " steps"), # Degree sign
        label2="Free",
        label="",
        numberOfRadioButtons=2,
        select=pm.optionVar["layoutRotateOld_NSUV"],
        vertical=True,
    )

    fieldGrpXformRotStepLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(15),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        label="Rotation steps: ",
        extraLabel="(degrees). Lower = Slower!",
        precision=4,
        value1=pm.optionVar["layoutRotStep_NSUV"],
        visible=pm.optionVar["layoutRotate_NSUV"],
    )

    rowRotateLayout = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
        visible=pm.optionVar["layoutRotate_NSUV"],
    )

    fieldRotMinLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(16),
        columnWidth2=[largeCol1, largeCol2],
        label="Min. rotation: ",
        parent=rowRotateLayout,
        precision=4,
        value1=pm.optionVar["layoutRotMin_NSUV"],
    )
    fieldRotMaxLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(17),
        columnAlign2=["left", "left"],
        columnWidth=[1, 28],
        label="Max:",
        parent=rowRotateLayout,
        precision=4,
        value1=pm.optionVar["layoutRotMax_NSUV"],
    )

    pm.setParent('..') # Set default parent to one step up

    sep6Layout = pm.separator()

    sep3Layout = pm.separator(
        height=sepSpace2,
        parent=colShellLayout,
        style="in",
        width=largeWinX-12,
    )

    menuScaleLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(18),
        columnWidth2=[largeCol1, largeCol2],
        label="Scaling: ",
        parent=colShellLayout,
    )

    itemNone = pm.menuItem(label="None")
    itemUni = pm.menuItem(label="Uniform")
    itemNonUni = pm.menuItem(label="Non-uniform")

    menuScaleLayout.setSelect(pm.optionVar["layoutScaling_NSUV"])

    sep7Layout = pm.separator()

    radGrpFitLayout = pm.radioButtonGrp(
        changeCommand=lambda *args: layoutOptVar(4),
        columnWidth2=[largeCol1, largeCol2+30],
        label1="Bounding box",
        label2="Shell shape",
        label="Fitting: ",
        numberOfRadioButtons=2,
        select=pm.optionVar["layoutFitting_NSUV"],
        vertical=True,
    )

    # Pre-Xform frame and column
    framePreXformLayout = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["layoutPreXformFrame_NSUV"],
        collapseCommand=lambda *args: layoutOptVar(19),
        expandCommand=lambda *args: layoutOptVar(19),
        label="Pre-Transform",
        parent=form2Layout,
    )
    colPreXformLayout = pm.columnLayout(
        parent=framePreXformLayout
    )
    
    # Pre-Xform elements
    menuPreXformRotLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(20),
        columnWidth2=[largeCol1, largeCol2],
        label="Pre-rotation: ",
        parent=colPreXformLayout,
    )

    itemRotOff = pm.menuItem(label="Off")
    itemRotHoriz = pm.menuItem(label="Horizontal")
    itemRotVert = pm.menuItem(label="Vertical")
    itemRotXtoV = pm.menuItem(label="Align X to V")
    itemRotYtoV = pm.menuItem(label="Align Y to V")
    itemRotZtoV = pm.menuItem(label="Align Z to V")

    menuPreXformRotLayout.setSelect(pm.optionVar["layoutPreRotation_NSUV"])
    
    menuPreXformScaleLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(21),
        columnWidth2=[largeCol1, largeCol2],
        label="Pre-scaling: ",
        parent=colPreXformLayout,
    )

    itemPreScaleOff = pm.menuItem(label="Off")
    itemPreScaleA = pm.menuItem(label="Preserve 3D Ratio")
    itemPreScaleB = pm.menuItem(label="Preserve UV Ratio")

    menuPreXformScaleLayout.setSelect(pm.optionVar["layoutPreScaling_NSUV"])


    ## Legacy

    # Change pre-scale labels
    if (mayaVer >= 201650 and u3dLoaded and layoutMethodVar == 2) or (not u3dLoaded and layoutMethodVar == 1):
        itemPreScaleA.setLabel("Object")
        itemPreScaleB.setLabel("World")

    sep9Layout = pm.separator()

    # Spacing frame and column
    frameSpacingLayout = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["layoutSpacingFrame_NSUV"],
        collapseCommand=lambda *args: layoutOptVar(33),
        expandCommand=lambda *args: layoutOptVar(33),
        label="Spacing",
        parent=form2Layout,
    )
    colSpaceLayout = pm.columnLayout(
        parent=frameSpacingLayout,
    )
    
    # Spacing elements
    menuSpaceLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(6),
        columnWidth2=[largeCol1, largeCol2],
        label="Map size (Pixels): ",
    )

    item8192 = pm.menuItem(label="Custom")
    item8192 = pm.menuItem(label="8192 Map")
    item4096 = pm.menuItem(label="4096 Map")
    item2048 = pm.menuItem(label="2048 Map")
    item1024 = pm.menuItem(label="1024 Map")
    item512 = pm.menuItem(label="512 Map")
    item256 = pm.menuItem(label="256 Map")
    item128 = pm.menuItem(label="128 Map")
    item64 = pm.menuItem(label="64 Map")

    menuSpaceLayout.setSelect(pm.optionVar["layoutSpaceMenu_NSUV"])

    fieldGrpShellPaddingLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(22),
        columnWidth2=[largeCol1, largeCol2],
        label="Shell padding (Units): ",
        precision=4,
        value1=pm.optionVar["layoutShellPadding_NSUV"],
    )
    fieldGrpShellPaddingOldLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(23),
        columnWidth2=[largeCol1, largeCol2],
        label="Shell padding (%): ",
        precision=4,
        value1=pm.optionVar["layoutShellPaddingOld_NSUV"],
    )
    fieldGrpTilePaddingLayout = pm.floatFieldGrp(
        changeCommand=lambda *args: layoutOptVar(24),
        columnWidth2=[largeCol1, largeCol2],
        label="Tile padding (Units): ",
        precision=4,
        value1=pm.optionVar["layoutTilePadding_NSUV"],
    )

    # Placement frame and column
    framePlaceLayout = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["layoutPlacementFrame_NSUV"], 
        collapseCommand=lambda *args: layoutOptVar(34),
        expandCommand=lambda *args: layoutOptVar(34),
        label="Placement",
        parent=form2Layout,
    )
    colPlaceLayout = pm.columnLayout(
        parent=framePlaceLayout,
    )
    
    # Placement elements
    menuPlaceLayout = pm.optionMenuGrp(
        changeCommand=lambda *args: layoutOptVar(32),
        columnWidth2=[largeCol1, largeCol2],
        label="Range: ",
        parent=colPlaceLayout,
    )

    itemPredef = pm.menuItem(label="Predefined")
    itemCustom = pm.menuItem(label="Custom")

    menuPlaceLayout.setSelect(pm.optionVar["layoutPlace_NSUV"])

    rowRangeULayout = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
    )

    fieldRangeMinULayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(25),
        columnWidth2=[largeCol1, largeCol2],
        label="Min. U: ",
        parent=rowRangeULayout,
        value1=pm.optionVar["layoutRangeMinU_NSUV"],
    )
    fieldRangeMaxULayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(26),
        columnAlign2=["left", "left"],
        columnWidth=[1, 28],
        label="Max:",
        parent=rowRangeULayout,
        value1=pm.optionVar["layoutRangeMaxU_NSUV"],
    )

    pm.setParent('..') # Set default parent to one step up
    
    rowRangeVLayout = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
    )

    fieldRangeMinVLayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(27),
        columnWidth2=[largeCol1, largeCol2],
        label="Min. V: ",
        parent=rowRangeVLayout,
        value1=pm.optionVar["layoutRangeMinV_NSUV"],
    )
    fieldRangeMaxVLayout = pm.intFieldGrp(
        changeCommand=lambda *args: layoutOptVar(28),
        columnAlign2=["left", "left"],
        columnWidth=[1, 28],
        label="Max:",
        parent=rowRangeVLayout,
        value1=pm.optionVar["layoutRangeMaxV_NSUV"],
    )

    pm.setParent('..') # Set default parent to one step up

    # formLayout for the range section
    formPlaceLayout = pm.formLayout(
        parent=colPlaceLayout,
        )

    # Range buttons
    btn1PlaceLayout = pm.iconTextButton(
        annotation="Default UV range",
        command=lambda *args: layoutOptVar(12, rad1PlaceLayout, None, 1),
        image=iconDict["uvRangeI"],
        label="Default UV range",
    )
    btn2PlaceLayout = pm.iconTextButton(
        annotation="Left half",
        command=lambda *args: layoutOptVar(12, rad2PlaceLayout, None, 2),
        image=iconDict["uvRangeB"],
        label="Left half",
    )
    btn3PlaceLayout = pm.iconTextButton(
        annotation="Right half",
        command=lambda *args: layoutOptVar(12, rad3PlaceLayout, None, 3),
        image=iconDict["uvRangeG"],
        label="Right half",
    )
    btn4PlaceLayout = pm.iconTextButton(
        annotation="Top half",
        command=lambda *args: layoutOptVar(12, rad4PlaceLayout, None, 4),
        image=iconDict["uvRangeH"],
        label="Top half",
    )
    btn5PlaceLayout = pm.iconTextButton(
        annotation="Top left corner",
        command=lambda *args: layoutOptVar(12, rad5PlaceLayout, None, 5),
        image=iconDict["uvRangeL"],
        label="Top left corner",
    )
    btn6PlaceLayout = pm.iconTextButton(
        annotation="Top right corner",
        command=lambda *args: layoutOptVar(12, rad6PlaceLayout, None, 6),
        image=iconDict["uvRangeM"],
        label="Top right corner",
    )
    btn7PlaceLayout = pm.iconTextButton(
        annotation="Bottom half",
        command=lambda *args: layoutOptVar(12, rad7PlaceLayout, None, 7),
        image=iconDict["uvRangeA"],
        label="Bottom half",
    )
    btn8PlaceLayout = pm.iconTextButton(
        annotation="Bottom left corner",
        command=lambda *args: layoutOptVar(12, rad8PlaceLayout, None, 8),
        image=iconDict["uvRangeJ"],
        label="Bottom left corner",
    )
    btn9PlaceLayout = pm.iconTextButton(
        annotation="Bottom right corner",
        command=lambda *args: layoutOptVar(12, rad9PlaceLayout, None, 9),
        image=iconDict["uvRangeK"],
        label="Bottom right corner",
    )


    # Radio collection and radio buttons
    radColPlaceLayout = pm.radioCollection(
        parent=formPlaceLayout
    )
    rad1PlaceLayout = pm.radioButton(label="A", changeCommand=lambda *args: layoutOptVar(12, rad1PlaceLayout, None, 1))
    rad2PlaceLayout = pm.radioButton(label="B", changeCommand=lambda *args: layoutOptVar(12, rad2PlaceLayout, None, 2))
    rad3PlaceLayout = pm.radioButton(label="C", changeCommand=lambda *args: layoutOptVar(12, rad3PlaceLayout, None, 3))
    rad4PlaceLayout = pm.radioButton(label="D", changeCommand=lambda *args: layoutOptVar(12, rad4PlaceLayout, None, 4))
    rad5PlaceLayout = pm.radioButton(label="E", changeCommand=lambda *args: layoutOptVar(12, rad5PlaceLayout, None, 5))
    rad6PlaceLayout = pm.radioButton(label="F", changeCommand=lambda *args: layoutOptVar(12, rad6PlaceLayout, None, 6))
    rad7PlaceLayout = pm.radioButton(label="G", changeCommand=lambda *args: layoutOptVar(12, rad7PlaceLayout, None, 7))
    rad8PlaceLayout = pm.radioButton(label="H", changeCommand=lambda *args: layoutOptVar(12, rad8PlaceLayout, None, 8))
    rad9PlaceLayout = pm.radioButton(label="I", changeCommand=lambda *args: layoutOptVar(12, rad9PlaceLayout, None, 9))

    # Edit the radio collection and select item
    if pm.optionVar["layoutPlacePres_NSUV"] == 1:
        radColPlaceLayout.setSelect(rad1PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 2:
        radColPlaceLayout.setSelect(rad2PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 3:
        radColPlaceLayout.setSelect(rad3PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 4:
        radColPlaceLayout.setSelect(rad4PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 5:
        radColPlaceLayout.setSelect(rad5PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 6:
        radColPlaceLayout.setSelect(rad6PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 7:
        radColPlaceLayout.setSelect(rad6PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 8:
        radColPlaceLayout.setSelect(rad6PlaceLayout)
    elif pm.optionVar["layoutPlacePres_NSUV"] == 9:
        radColPlaceLayout.setSelect(rad6PlaceLayout)

    # Layout elements in the range formLayout
    pm.formLayout(
        formPlaceLayout, edit=True,
        attachForm=[
            (btn1PlaceLayout, "top", 5),
            (btn1PlaceLayout, "left", layoutCol1),
            (rad1PlaceLayout, "top", btnTop),

            (btn2PlaceLayout, "top", 5),
            (rad2PlaceLayout, "top", btnTop+3),

            (btn3PlaceLayout, "top", 5),
            (rad3PlaceLayout, "top", btnTop+3),

            (btn4PlaceLayout, "left", layoutCol1),
            
            (btn7PlaceLayout, "left", layoutCol1),
            (btn7PlaceLayout, "bottom", btnTop),
        ],
        attachControl=[
            (rad1PlaceLayout, "left", radLeft, btn1PlaceLayout),

            (btn2PlaceLayout, "left", btnLeft, rad1PlaceLayout),
            (rad2PlaceLayout, "left", radLeft, btn2PlaceLayout),

            (btn3PlaceLayout, "left", btnLeft, rad2PlaceLayout),
            (rad3PlaceLayout, "left", radLeft, btn3PlaceLayout),

            (btn4PlaceLayout, "top", btnTop, btn1PlaceLayout),
            (rad4PlaceLayout, "top", radTop+3, rad1PlaceLayout),
            (rad4PlaceLayout, "left", radLeft, btn4PlaceLayout),

            (btn5PlaceLayout, "top", btnTop, btn2PlaceLayout),
            (btn5PlaceLayout, "left", btnLeft, rad4PlaceLayout),
            (rad5PlaceLayout, "top", radTop+3, rad2PlaceLayout),
            (rad5PlaceLayout, "left", radLeft, btn5PlaceLayout),

            (btn6PlaceLayout, "top", btnTop, btn3PlaceLayout),
            (btn6PlaceLayout, "left", btnLeft, rad5PlaceLayout),
            (rad6PlaceLayout, "top", radTop+3, rad3PlaceLayout),
            (rad6PlaceLayout, "left", radLeft, btn6PlaceLayout),

            (btn7PlaceLayout, "top", btnTop, btn4PlaceLayout),
            (rad7PlaceLayout, "top", radTop+3, rad4PlaceLayout),
            (rad7PlaceLayout, "left", radLeft, btn7PlaceLayout),

            (btn8PlaceLayout, "top", btnTop, btn5PlaceLayout),
            (btn8PlaceLayout, "left", btnLeft, rad7PlaceLayout),
            (rad8PlaceLayout, "top", radTop+3, rad5PlaceLayout),
            (rad8PlaceLayout, "left", radLeft, btn8PlaceLayout),

            (btn9PlaceLayout, "top", btnTop, btn6PlaceLayout),
            (btn9PlaceLayout, "left", btnLeft, rad8PlaceLayout),
            (rad9PlaceLayout, "top", radTop+3, rad6PlaceLayout),
            (rad9PlaceLayout, "left", radLeft, btn9PlaceLayout),
        ]
    )


    ## Quick
    
    # Frame and form layouts
    frameQuickLayout = pm.frameLayout(
        label="Quick Presets",
        parent=form2Layout,
    )

    formQuickLayout = pm.formLayout(parent=frameQuickLayout)
    
    textQuickLayout = pm.text(label="No options here - Things just get done!!")
    
    # Elements
    btm1QuickLayout = pm.iconTextButton(
        annotation="Into region",
        command=lambda *args: layoutOptVar(13, rad1QuickLayout, None, 1),
        image=iconDict["qLayoutA"],
        label="Into region",
    )
    btm2QuickLayout = pm.iconTextButton(
        annotation="Along U",
        command=lambda *args: layoutOptVar(13, rad2QuickLayout, None, 2),
        image=iconDict["qLayoutB"],
        label="Along U",
    )
    btm3QuickLayout = pm.iconTextButton(
        annotation="Along V",
        command=lambda *args: layoutOptVar(13, rad3QuickLayout, None, 3),
        image=iconDict["qLayoutC"],
        label="Along V",
    )
    
    # Radio collection and radio buttons
    radColQuickLayout = pm.radioCollection(
        parent=formQuickLayout
    )
    rad1QuickLayout = pm.radioButton(label="A", changeCommand=lambda *args: layoutOptVar(13, rad1PlaceLayout, None, 1)) # into region
    rad2QuickLayout = pm.radioButton(label="B", changeCommand=lambda *args: layoutOptVar(13, rad2PlaceLayout, None, 2)) # along U
    rad3QuickLayout = pm.radioButton(label="C", changeCommand=lambda *args: layoutOptVar(13, rad3PlaceLayout, None, 3)) # along V
    
    # Edit the radio collection and select item
    if pm.optionVar["layoutQuickType_NSUV"] == 1:
        radColQuickLayout.setSelect(rad1QuickLayout)
    elif pm.optionVar["layoutQuickType_NSUV"] == 2:
        radColQuickLayout.setSelect(rad2QuickLayout)
    elif pm.optionVar["layoutQuickType_NSUV"] == 3:
        radColQuickLayout.setSelect(rad3QuickLayout)
        
    # Layout elements in the range formLayout
    pm.formLayout(
        formQuickLayout, edit=True,
        attachForm=[
            (textQuickLayout, "top", 5),
            (textQuickLayout, "left", layoutCol1),

            (btm1QuickLayout, "left", layoutCol1+1),
            (btm1QuickLayout, "bottom", btnTop),
        ],
        attachControl=[
            (btm1QuickLayout, "top", btnTop/2, textQuickLayout),
        
            (rad1QuickLayout, "top", btnTop+5, textQuickLayout),
            (rad1QuickLayout, "left", radLeft, btm1QuickLayout),

            (btm2QuickLayout, "top", btnTop/2, textQuickLayout),
            (btm2QuickLayout, "left", btnLeft, rad1QuickLayout),
            (rad2QuickLayout, "top", btnTop+5, textQuickLayout),
            (rad2QuickLayout, "left", radLeft, btm2QuickLayout),

            (btm3QuickLayout, "top", btnTop/2, textQuickLayout),
            (btm3QuickLayout, "left", btnLeft, rad2QuickLayout),
            (rad3QuickLayout, "top", btnTop+5, textQuickLayout),
            (rad3QuickLayout, "left", radLeft, btm3QuickLayout),
        ]
    )
    
    # Buttons
    btnApplyCloseLayout = pm.button(
        command=lambda *args: core.layoutUVs(winLayout),
        label="Confirm",
        parent=form1Layout,
    )
    btnApplyLayout = pm.button(
        command=lambda *args: core.layoutUVs(),
        label="Apply",
        parent=form1Layout,
    )
    btnResetLayout = pm.button(
        command=lambda *args: layoutUIReset(),
        label="Reset",
        parent=form1Layout,
    )
    btnCloseLayout = pm.button(
        command=lambda *args: pm.deleteUI(winLayout),
        label="Close",
        parent=form1Layout,
    )

    # Layout frames
    pm.formLayout(
        form2Layout, edit=True,
        attachForm=[
            (frameMainLayout, "top", 0),
            (frameMainLayout, "left", 0),
            (frameMainLayout, "right", 0),

            (frameShellLayout, "left", 0),
            (frameShellLayout, "right", 0),
            
            (framePreXformLayout, "left", 0),
            (framePreXformLayout, "right", 0),

            (frameSpacingLayout, "left", 0),
            (frameSpacingLayout, "right", 0),

            (framePlaceLayout, "left", 0),
            (framePlaceLayout, "right", 0),

            (frameQuickLayout, "left", 0),
            (frameQuickLayout, "right", 0),
        ],
        attachControl=[
            (frameShellLayout, "top", 10, frameMainLayout),
        
            (framePreXformLayout, "top", 10, frameShellLayout),

            (frameSpacingLayout, "top", 0, framePreXformLayout),

            (framePlaceLayout, "top", 10, frameSpacingLayout),

            (frameQuickLayout, "top", 0, framePlaceLayout),
        ],
        attachNone=[
            (frameShellLayout, "bottom"),

            (framePreXformLayout, "bottom"),

            (frameSpacingLayout, "bottom"),

            (framePlaceLayout, "bottom"),

            (frameQuickLayout, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1Layout, edit=True,
        attachForm=[
            (scroll1Layout, "top", 0),
            (scroll1Layout, "left", 0),
            (scroll1Layout, "right", 0),

            (btnApplyCloseLayout, "left", 5),
            (btnApplyCloseLayout, "bottom", 5),
            (btnApplyLayout, "bottom", 5),
            (btnResetLayout, "bottom", 5),
            (btnCloseLayout, "right", 5),
            (btnCloseLayout, "bottom", 5),
        ],
        attachControl=[
            (scroll1Layout, "bottom", 0, btnApplyCloseLayout),
        ],
        attachPosition=[
            (btnApplyCloseLayout, "right", 3, 25),
            (btnApplyLayout, "left", 2, 25),
            (btnApplyLayout, "right", 3, 50),
            (btnResetLayout, "right", 3, 75),
            (btnResetLayout, "left", 2, 50),
            (btnCloseLayout, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseLayout, "top"),
            (btnApplyLayout, "top"),
            (btnResetLayout, "top"),
            (btnCloseLayout, "top"),
        ],
    )

    # Hide inactive
    layoutFrameSwitch()
    layoutControlSwitch()

    # Display the window
    pm.showWindow(window)


# Ui for changing the automatic mapping options
def mapAutoUI():

    # Vars
    visState1, visState3 = (False,)*2
    visState2, visState4 = (True,)*2

    # Load selected as projection object
    def mapAutoLoadSel():

        # Check for mesh selection
        core.checkSel("mesh")

        # Get name from object
        projObj = pm.ls(selection=True, flatten=True)[0]

        # Update control, then the optVar
        fieldProjMapAuto.setText(projObj)
        mapAutoOptVar(5)


    # Switch projection method
    def mapAutoSwitch():

        if radGrpMethodMapAuto.getSelect() == 1:
            frameMSMapAuto.setVisible(True)
            frameProjMapAuto.setVisible(True)
            frameLayoutMapAuto.setVisible(True)
            frameSpaceMapAuto.setVisible(True)
            frameSetMapAuto.setVisible(True)
            textQuickMapAuto.setVisible(False)

        elif radGrpMethodMapAuto.getSelect() == 2:
            frameMSMapAuto.setVisible(False)
            frameProjMapAuto.setVisible(False)
            frameLayoutMapAuto.setVisible(False)
            frameSpaceMapAuto.setVisible(False)
            frameSetMapAuto.setVisible(False)
            textQuickMapAuto.setVisible(True)

        # Save optVar
        pm.optionVar["mapAutoMethod_NSUV"] = radGrpMethodMapAuto.getSelect()


    # Reset UI
    def mapAutoReset():

        # Reset UI controls
        radGrpMethodMapAuto.setSelect(1)
        menuMSMapAuto.setValue(6)
        menuMSMapAuto.setEnable(True)
        radGrpMS1MapAuto.setSelect(2) # Optimize for
        radGrpMS2MapAuto.setSelect(1) # Sample space
        cBox1MSMapAuto.setValue1(True)
        cBox2MSMapAuto.setValue1(True)
        cBoxProjMapAuto.setValue1(False)
        fieldProjMapAuto.setText("")
        fieldProjMapAuto.setEnable(False)
        cBoxProjBothMapAuto.setValue1(False)
        btnLoadProjMapAuto.setEnable(False)
        menuLayoutMapAuto.setValue("Into Square")
        menuLayoutScaleMapAuto.setSelect(2)
        radGrpLayoutStackMapAuto.setSelect(1)
        cBoxNormMapAuto.setValue1(False)
        menuSpaceMapAuto.setSelect(5)
        menuSpaceMapAuto.setEnable(True)
        sliderSpaceMapAuto.setValue(0.2000)
        sliderSpaceMapAuto.setEnable(True)
        cBoxSetMapAuto.setValue1(False)
        fieldSetMapAuto.setText("uvSet1")
        fieldSetMapAuto.setEnable(False)

        # Reset optVars
        pm.optionVar["mapAutoMethod_NSUV"] = 1
        pm.optionVar["mapAutoMSMenu_NSUV"] = 6
        pm.optionVar["mapAutoMS1RadGrp_NSUV"] = 2 # Optimize for
        pm.optionVar["mapAutoMS2RadGrp_NSUV"] = 1 # Sample space
        pm.optionVar["mapAutoMSBox1_NSUV"] = True
        pm.optionVar["mapAutoMSBox2_NSUV"] = True
        pm.optionVar["mapAutoProjBox1_NSUV"] = False
        pm.optionVar["mapAutoProjObj_NSUV"] = ""
        pm.optionVar["mapAutoProjBox2_NSUV"] = False
        pm.optionVar["mapAutoLayoutMenu_NSUV"] = "Into Square"
        pm.optionVar["mapAutoLayoutRadGrp1_NSUV"] = 2
        pm.optionVar["mapAutoLayoutRadGrp2_NSUV"] = 1
        pm.optionVar["mapAutoNormBox_NSUV"] = False
        pm.optionVar["mapAutoSpaceMenu_NSUV"] = 5
        pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.2000
        pm.optionVar["mapAutoSetBox_NSUV"] = False
        pm.optionVar["mapAutoSet_NSUV"] = "uvSet1"

        # Switch to the correct layouts
        mapAutoSwitch()


    # Update optVar
    def mapAutoOptVar(varType):

        if varType == 1:
            pm.optionVar["mapAutoMSMenu_NSUV"] = menuMSMapAuto.getValue()

        elif varType == 2:
            pm.optionVar["mapAutoMS1RadGrp_NSUV"] = radGrpMS1MapAuto.getSelect()

        elif varType == 3:
            pm.optionVar["mapAutoMSBox1_NSUV"] = cBox1MSMapAuto.getValue1()

        elif varType == 4:
            pm.optionVar["mapAutoProjBox1_NSUV"] = cBoxProjMapAuto.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapAutoProjBox1_NSUV"] == False:
                menuMSMapAuto.setEnable(True)
                fieldProjMapAuto.setEnable(False)
                cBoxProjBothMapAuto.setEnable(False)
                btnLoadProjMapAuto.setEnable(False)
            else:
                menuMSMapAuto.setEnable(False)
                fieldProjMapAuto.setEnable(True)
                cBoxProjBothMapAuto.setEnable(True)
                btnLoadProjMapAuto.setEnable(True)

        elif varType == 5:
            pm.optionVar["mapAutoProjObj_NSUV"] = fieldProjMapAuto.getText()

        elif varType == 6:
            pm.optionVar["mapAutoProjBox2_NSUV"] = cBoxProjBothMapAuto.getValue1()

        elif varType == 7:
            pm.optionVar["mapAutoLayoutMenu_NSUV"] = menuLayoutMapAuto.getValue()

            # Turn on/off UI controls
            if pm.optionVar["mapAutoLayoutMenu_NSUV"] == "Into Square":
                menuSpaceMapAuto.setEnable(True)
                sliderSpaceMapAuto.setEnable(True)
            else:
                menuSpaceMapAuto.setEnable(False)
                sliderSpaceMapAuto.setEnable(False)

        elif varType == 8:
            pm.optionVar["mapAutoLayoutRadGrp1_NSUV"] = menuLayoutScaleMapAuto.getSelect()

        elif varType == 9:
            pm.optionVar["mapAutoLayoutRadGrp2_NSUV"] = radGrpLayoutStackMapAuto.getSelect()

        elif varType == 10:
            pm.optionVar["mapAutoSpaceMenu_NSUV"] = val = menuSpaceMapAuto.getSelect()

            if val == 1: # Custom
                pm.optionVar["mapAutoSpaceVal_NSUV"] = sliderSpaceMapAuto.getValue()
            
            if val == 2: # 8192
                sliderSpaceMapAuto.setValue(0.012)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.012
                
            elif val == 3:
                sliderSpaceMapAuto.setValue(0.055)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.055

            elif val == 4:
                sliderSpaceMapAuto.setValue(0.100)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.100

            elif val == 5: # 1024
                sliderSpaceMapAuto.setValue(0.200)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.200

            elif val == 6:
                sliderSpaceMapAuto.setValue(0.400)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.400

            elif val == 7:
                sliderSpaceMapAuto.setValue(0.840)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.840

            elif val == 8: # 128
                sliderSpaceMapAuto.setValue(1.630)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 1.630

            elif val == 9:
                sliderSpaceMapAuto.setValue(3.750)
                pm.optionVar["mapAutoSpaceVal_NSUV"] = 3.750

        elif varType == 11:
            pm.optionVar["mapAutoSpaceVal_NSUV"] = sliderSpaceMapAuto.getValue()

            # Select custom in preset menu
            menuSpaceMapAuto.setValue("Custom")


        elif varType == 12:
            pm.optionVar["mapAutoSetBox_NSUV"] = cBoxSetMapAuto.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapAutoSetBox_NSUV"] == False:
                fieldSetMapAuto.setEnable(False)
            else:
                fieldSetMapAuto.setEnable(True)

        elif varType == 13:
            pm.optionVar["mapAutoSet_NSUV"] = fieldSetMapAuto.getText()

        elif varType == 14:
            pm.optionVar["mapAutoNormBox_NSUV"] = cBoxNormMapAuto.getValue1()

        elif varType == 15:
            pm.optionVar["mapAutoMS2RadGrp_NSUV"] = radGrpMS2MapAuto.getSelect()

        elif varType == 16:
            pm.optionVar["mapAutoMSBox2_NSUV"] = cBox2MSMapAuto.getValue1()
            
        elif varType == 17:
            pm.optionVar["mapAutoFrame1_NSUV"] = frameProjMapAuto.getCollapse()
            
        elif varType == 18:
            pm.optionVar["mapAutoFrame2_NSUV"] = frameSetMapAuto.getCollapse()


    # Check for window duplicate
    if pm.window( winMapAuto, exists=True ):
        pm.deleteUI(winMapAuto)

    # Read UI control optVars - Set visibility states
    if pm.optionVar["mapAutoProjBox1_NSUV"] == True:
        visState1 = True

    if pm.optionVar["mapAutoLayoutMenu_NSUV"] != "Into Square":
        visState2 = False

    if pm.optionVar["mapAutoSetBox_NSUV"] == True:
        visState3 = True

    # Window
    window = pm.window(
        winMapAuto,
        height=mapAutoWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Mapping: Automatic Projection",
        width=largeWinX
    )

    # Create layouts
    form1MapAuto = pm.formLayout()
    scrollMapAuto = pm.scrollLayout( childResizable=True )
    form2MapAuto = pm.formLayout( parent=scrollMapAuto )

    frameMainMapAuto = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Automatic Projection Options",
        parent=form2MapAuto
    )

    # Method radioBtnGrp
    radGrpMethodMapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoSwitch(),
        columnWidth2=[mappingCol1, mappingCol2],
        label="Method: ",
        labelArray2=["Custom", "Quick"],
        numberOfRadioButtons=2,
        parent=frameMainMapAuto,
        select=pm.optionVar["mapAutoMethod_NSUV"],
        vertical=True,
    )


    ## Custom

    # Mapping Settings: Frame and column
    frameMSMapAuto = pm.frameLayout(
        label="Settings",
        parent=form2MapAuto
    )
    colMSMapAuto = pm.columnLayout(
        parent=frameMSMapAuto
    )

    # Mapping Settings: UI elements
    menuMSMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoOptVar(1),
        columnWidth2=[mappingCol1, mappingCol2],
        enable=visState4,
        label="Planes: ",
        parent=colMSMapAuto,
    )

    planes3 = pm.menuItem(label="3")
    planes4 = pm.menuItem(label="4")
    planes6 = pm.menuItem(label="6")
    planes8 = pm.menuItem(label="8")
    planes10 = pm.menuItem(label="10")
    planes12 = pm.menuItem(label="12")

    menuMSMapAuto.setValue(pm.optionVar["mapAutoMSMenu_NSUV"])

    radGrpMS1MapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoOptVar(2),
        columnWidth2=[mappingCol1, mappingCol2],
        label1="Less distortion",
        label2="Fewer pieces",
        label="Optimize for: ",
        numberOfRadioButtons=2,
        parent=colMSMapAuto,
        select=pm.optionVar["mapAutoMS1RadGrp_NSUV"],
        vertical=True,
    )
    sep1MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapAuto,
        visible=True,
    )
    radGrpMS2MapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoOptVar(15),
        columnWidth2=[mappingCol1, mappingCol2],
        label1="World",
        label2="Local",
        label="Sample space: ",
        numberOfRadioButtons=2,
        parent=colMSMapAuto,
        select=pm.optionVar["mapAutoMS2RadGrp_NSUV"],
        vertical=True,
    )
    cBox1MSMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(3),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Insert projection before deformers",
        parent=colMSMapAuto,
        value1=pm.optionVar["mapAutoMSBox1_NSUV"],
    )
    cBox2MSMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(16),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colMSMapAuto,
        value1=pm.optionVar["mapAutoMSBox2_NSUV"],
    )
    sep2MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapAuto,
        visible=True,
    )

    # Projection: Frame and column
    frameProjMapAuto = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapAutoFrame1_NSUV"],
        collapseCommand=lambda *args: mapAutoOptVar(17),
        expandCommand=lambda *args: mapAutoOptVar(17),
        label="Custom Projection",
        parent=form2MapAuto,
    )
    colProjMapAuto = pm.columnLayout(
        parent=frameProjMapAuto
    )

    # Projection: UI elements
    cBoxProjMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(4),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Load projection",
        parent=colProjMapAuto,
        value1=pm.optionVar["mapAutoProjBox1_NSUV"],
    )
    if mayaVer == 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldProjMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoOptVar(5),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState1,
            label="Projection object: ",
            parent=colProjMapAuto,
            text=pm.optionVar["mapAutoProjObj_NSUV"],
        )
    else:
        fieldProjMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoOptVar(5),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState1,
            label="Projection object: ",
            parent=colProjMapAuto,
            text=pm.optionVar["mapAutoProjObj_NSUV"],
            textChangedCommand=lambda *args: mapAutoOptVar(5),
        )
    cBoxProjBothMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(6),
        columnWidth2=[mappingCol1, mappingCol2],
        enable=visState1,
        label="",
        label1="Project both directions",
        parent=colProjMapAuto,
        value1=pm.optionVar["mapAutoProjBox2_NSUV"],
    )
    rowLoadSelMapAuto = pm.rowLayout(
        columnWidth=[mappingCol1, mappingCol2],
        numberOfColumns=2,
        parent=colProjMapAuto,
    )
    fillerMapAuto = pm.text(label="", width=mappingCol1)
    btnLoadProjMapAuto = pm.button(
        command=lambda *args: mapAutoLoadSel(),
        enable=visState1,
        label="Load Selected",
        parent=rowLoadSelMapAuto,
        width=(mappingCol2+mappingCol3),
    )
    sep3MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colProjMapAuto,
        visible=True,
    )

    # Layout: Frame and column
    frameLayoutMapAuto = pm.frameLayout(
        label="Layout",
        parent=form2MapAuto
    )
    colLayoutMapAuto = pm.columnLayout(
        parent=frameLayoutMapAuto
    )

    # Layout: UI elements
    menuLayoutMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoOptVar(7),
        columnWidth2=[mappingCol1, mappingCol2],
        label="Layout: ",
        parent=colLayoutMapAuto,
    )

    layout1 = pm.menuItem(label="Overlap")
    layout2 = pm.menuItem(label="Along U")
    layout3 = pm.menuItem(label="Into Square")
    layout4 = pm.menuItem(label="Tile")

    menuLayoutMapAuto.setValue(pm.optionVar["mapAutoLayoutMenu_NSUV"])
    
    menuLayoutScaleMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoOptVar(8),
        columnWidth2=[mappingCol1, mappingCol2],
        label="Scaling: ",
        parent=colLayoutMapAuto,
    )

    itemNone = pm.menuItem(label="None")    
    itemUni = pm.menuItem(label="Uniform")    
    itemNonUni = pm.menuItem(label="Stretch to square")

    menuLayoutScaleMapAuto.setSelect(pm.optionVar["mapAutoLayoutRadGrp1_NSUV"])
        
    
    sep4MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colLayoutMapAuto,
        visible=True,
    )
    radGrpLayoutStackMapAuto = pm.radioButtonGrp(
        changeCommand=lambda *args: mapAutoOptVar(9),
        columnWidth2=[mappingCol1, mappingCol2],
        label1="Bounding box",
        label2="Shape",
        label="Shell stacking: ",
        numberOfRadioButtons=2,
        parent=colLayoutMapAuto,
        select=pm.optionVar["mapAutoLayoutRadGrp2_NSUV"],
        vertical=True,
    )
    cBoxNormMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(14),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Normalize",
        parent=colLayoutMapAuto,
        value1=pm.optionVar["mapAutoNormBox_NSUV"],
    )
    sep5MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colLayoutMapAuto,
        visible=True,
    )

    # Shell spacing: Frame and column
    frameSpaceMapAuto = pm.frameLayout(
        label="Shell Spacing",
        parent=form2MapAuto
    )
    colSpaceMapAuto = pm.columnLayout(
        parent=frameSpaceMapAuto
    )

    # Shell spacing: UI elements
    menuSpaceMapAuto = pm.optionMenuGrp(
        changeCommand=lambda *args: mapAutoOptVar(10),
        columnWidth2=[mappingCol1, mappingCol2],
        enable=visState2,
        label="Spacing preset: ",
        parent=colSpaceMapAuto,
    )

    itemCustom = pm.menuItem(label="Custom")
    item8192 = pm.menuItem(label="8192 Map")
    item4096 = pm.menuItem(label="4096 Map")
    item2048 = pm.menuItem(label="2048 Map")
    item1024 = pm.menuItem(label="1024 Map")
    item512 = pm.menuItem(label="512 Map")
    item256 = pm.menuItem(label="256 Map")
    item128 = pm.menuItem(label="128 Map")
    item64 = pm.menuItem(label="64 Map")

    menuSpaceMapAuto.setSelect(pm.optionVar["mapAutoSpaceMenu_NSUV"])

    sliderSpaceMapAuto = pm.floatSliderGrp(
        changeCommand=lambda *args: mapAutoOptVar(11),
        columnWidth3=[mappingCol1, mappingCol2, mappingCol3],
        enable=visState2,
        field=True,
        fieldMinValue=0.000,
        fieldMaxValue=5.000,
        label="Shell padding (%): ",
        minValue=0.000,
        maxValue=5.000,
        parent=colSpaceMapAuto,
        precision=3,
        step=0.001,
        value=pm.optionVar["mapAutoSpaceVal_NSUV"],
    )
    sep6MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSpaceMapAuto,
        visible=True,
    )

    # UV Set: Frame and column
    frameSetMapAuto = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapAutoFrame2_NSUV"],
        collapseCommand=lambda *args: mapAutoOptVar(18),
        expandCommand=lambda *args: mapAutoOptVar(18),
        label="UV Set",
        parent=form2MapAuto
    )
    colSetMapAuto = pm.columnLayout(
        parent=frameSetMapAuto
    )

    # UV Set: UI elements
    cBoxSetMapAuto = pm.checkBoxGrp(
        changeCommand=lambda *args: mapAutoOptVar(12),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapAuto,
        value1=pm.optionVar["mapAutoSetBox_NSUV"],
    )
    if mayaVer == 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoOptVar(13),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState3,
            label="UV Set name: ",
            parent=colSetMapAuto,
            text=pm.optionVar["mapAutoSet_NSUV"],
        )
    else:
        fieldSetMapAuto = pm.textFieldGrp(
            changeCommand=lambda *args: mapAutoOptVar(13),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState3,
            label="UV Set name: ",
            parent=colSetMapAuto,
            text=pm.optionVar["mapAutoSet_NSUV"],
            textChangedCommand=lambda *args: mapAutoOptVar(13),
        )
    sep7MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapAuto,
        visible=True,
    )


    ## Quick

    textQuickMapAuto = pm.text(
        label="No options here - Things just get done!!",
        parent=form2MapAuto
    )

    # Buttons
    btnApplyCloseMapAuto = pm.button(
        command=lambda *args: core.mapping("auto", None, winMapAuto),
        label="Confirm",
        parent=form1MapAuto,
    )
    btnApplyMapAuto = pm.button(
        command=lambda *args: core.mapping("auto"),
        label="Apply",
        parent=form1MapAuto,
    )
    btnResetMapAuto = pm.button(
        command=lambda *args: mapAutoReset(),
        label="Reset",
        parent=form1MapAuto,
    )
    btnCloseMapAuto = pm.button(
        command=lambda *args: pm.deleteUI(winMapAuto),
        label="Close",
        parent=form1MapAuto,
    )

    # Layout frames
    pm.formLayout(
        form2MapAuto, edit=True,
        attachForm=[
            (frameMainMapAuto, "top", 0),
            (frameMainMapAuto, "left", 0),
            (frameMainMapAuto, "right", 0),

            (frameMSMapAuto, "left", 0),
            (frameMSMapAuto, "right", 0),

            (frameProjMapAuto, "left", 0),
            (frameProjMapAuto, "right", 0),

            (frameLayoutMapAuto, "left", 0),
            (frameLayoutMapAuto, "right", 0),

            (frameSpaceMapAuto, "left", 0),
            (frameSpaceMapAuto, "right", 0),

            (frameSetMapAuto, "left", 0),
            (frameSetMapAuto, "right", 0),

            (textQuickMapAuto, "left", 0),
            (textQuickMapAuto, "right", 0),
        ],
        attachControl=[
            (frameMSMapAuto, "top", 10, frameMainMapAuto),

            (frameProjMapAuto, "top", 10, frameMSMapAuto),

            (frameLayoutMapAuto, "top", 10, frameProjMapAuto),

            (frameSpaceMapAuto, "top", 10, frameLayoutMapAuto),

            (frameSetMapAuto, "top", 10, frameSpaceMapAuto),

            (textQuickMapAuto, "top", 0, frameSetMapAuto),
        ],
        attachNone=[
            (frameMSMapAuto, "bottom"),

            (frameProjMapAuto, "bottom"),

            (frameLayoutMapAuto, "bottom"),

            (frameSpaceMapAuto, "bottom"),

            (frameSetMapAuto, "bottom"),

            (textQuickMapAuto, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1MapAuto, edit=True,
        attachForm=[
            (scrollMapAuto, "top", 0),
            (scrollMapAuto, "left", 0),
            (scrollMapAuto, "right", 0),

            (btnApplyCloseMapAuto, "left", 5),
            (btnApplyCloseMapAuto, "bottom", 5),
            (btnApplyMapAuto, "bottom", 5),
            (btnResetMapAuto, "bottom", 5),
            (btnCloseMapAuto, "right", 5),
            (btnCloseMapAuto, "bottom", 5),
        ],
        attachControl=[
            (scrollMapAuto, "bottom", 0, btnApplyCloseMapAuto),
        ],
        attachPosition=[
            (btnApplyCloseMapAuto, "right", 3, 25),
            (btnApplyMapAuto, "left", 2, 25),
            (btnApplyMapAuto, "right", 3, 50),
            (btnResetMapAuto, "right", 3, 75),
            (btnResetMapAuto, "left", 2, 50),
            (btnCloseMapAuto, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseMapAuto, "top"),
            (btnApplyMapAuto, "top"),
            (btnResetMapAuto, "top"),
            (btnCloseMapAuto, "top"),
        ],
    )

    # Hide inactive
    mapAutoSwitch()

    # Display the window
    pm.showWindow(window)


# UI for changing the cylindrical mapping options
def mapCylindricalUI():

    # Vars
    visState = False

    # Reset UI
    def mapCylindricalReset():

        # Reset UI controls
        sliderMapCylindrical.setValue(180)
        cBox1MSMapCylindrical.setValue1(True)
        cBox2MSMapCylindrical.setValue1(True)
        cBoxSetMapCylindrical.setValue1(False)
        fieldSetMapCylindrical.setEnable(False)
        fieldSetMapCylindrical.setText("uvSet1")

        # Reset optVars
        pm.optionVar["mapCylindricalSweep_NSUV"] = 180
        pm.optionVar["mapCylindricalMS1Box_NSUV"] = True
        pm.optionVar["mapCylindricalMS2Box_NSUV"] = True
        pm.optionVar["mapCylindricalSetBox_NSUV"] = False
        pm.optionVar["mapCylindricalSet_NSUV"] = "uvSet1"


    # Update optVar
    def mapCylindricalOptVar(varType):

        if varType == 1:
            pm.optionVar["mapCylindricalMS1Box_NSUV"] = cBox1MSMapCylindrical.getValue1()

        elif varType == 2:
            pm.optionVar["mapCylindricalMS2Box_NSUV"] = cBox2MSMapCylindrical.getValue1()

        elif varType == 3:
            pm.optionVar["mapCylindricalSetBox_NSUV"] = cBoxSetMapCylindrical.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapCylindricalSetBox_NSUV"] == False: fieldSetMapCylindrical.setEnable(False)
            else: fieldSetMapCylindrical.setEnable(True)

        elif varType == 4:
            pm.optionVar["mapCylindricalSet_NSUV"] = fieldSetMapCylindrical.getText()

        elif varType == 5:
            pm.optionVar["mapCylindricalSweep_NSUV"] = sliderMapCylindrical.getValue()
            
        elif varType == 6:
            pm.optionVar["mapCylindricalFrame1_NSUV"] = frameSetMapCylindrical.getValue()


    # Check for window duplicate
    if pm.window( winMapCylindrical, exists=True ):
        pm.deleteUI(winMapCylindrical)

    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapCylindricalSet_NSUV"] == True:
        visState = True

    # Window
    window = pm.window(
        winMapCylindrical,
        height=mapCylindricalWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Mapping: Cylindrical Projection",
        width=largeWinX
    )

    # Create layout
    form1MapCylindrical = pm.formLayout()
    scrollMapCylindrical = pm.scrollLayout( childResizable=True )
    form2MapCylindrical = pm.formLayout( parent=scrollMapCylindrical )

    # Mapping Settings: Frame and column
    frameMainMapCylindrical = pm.frameLayout(
        borderVisible=False,
        label="Cylindrical Projection Options",
        parent=form2MapCylindrical,
    )
    colSetCylindrical = pm.columnLayout(
        parent=frameMainMapCylindrical
    )

    # Mapping Settings: UI elements
    sliderMapCylindrical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapCylindricalOptVar(5),
        columnWidth3=[mappingCol1, mappingCol2, mappingCol3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=360.00,
        label="Projection sweep: ",
        minValue=0.00,
        maxValue=360.00,
        parent=colSetCylindrical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapCylindricalSweep_NSUV"],
    )
    cBox1MSMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalOptVar(1),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetCylindrical,
        value1=pm.optionVar["mapCylindricalMS1Box_NSUV"],
    )
    cBox2MSMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalOptVar(2),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetCylindrical,
        value1=pm.optionVar["mapCylindricalMS2Box_NSUV"],
    )
    sep1MapCylindrical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetCylindrical,
        visible=True,
    )

    # UV Set: Frame and column
    frameSetMapCylindrical = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapCylindricalFrame1_NSUV"],
        collapseCommand=lambda *args: mapCylindricalOptVar(6),
        expandCommand=lambda *args: mapCylindricalOptVar(6),
        label="UV Set",
        parent=form2MapCylindrical
    )
    colSetMapCylindrical = pm.columnLayout(
        parent=frameSetMapCylindrical
    )

    # UV Set: UI elements
    cBoxSetMapCylindrical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapCylindricalOptVar(3),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapCylindrical,
        value1=pm.optionVar["mapCylindricalSetBox_NSUV"],
    )
    if mayaVer == 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapCylindrical = pm.textFieldGrp(
            changeCommand=lambda *args: mapCylindricalOptVar(4),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapCylindrical,
            text=pm.optionVar["mapCylindricalSet_NSUV"],
        )
    else:
        fieldSetMapCylindrical = pm.textFieldGrp(
            changeCommand=lambda *args: mapCylindricalOptVar(4),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapCylindrical,
            text=pm.optionVar["mapCylindricalSet_NSUV"],
            textChangedCommand=lambda *args: mapCylindricalOptVar(4),
        )
    sep2MapCylindrical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapCylindrical,
        visible=True,
    )

    # Buttons
    btnApplyCloseMapCylindrical = pm.button(
        command=lambda *args: core.mapping("cyl", None, winMapCylindrical),
        label="Confirm",
        parent=form1MapCylindrical,
    )
    btnApplyMapCylindrical = pm.button(
        command=lambda *args: core.mapping("cyl"),
        label="Apply",
        parent=form1MapCylindrical,
    )
    btnResetMapCylindrical = pm.button(
        command=lambda *args: mapCylindricalReset(),
        label="Reset",
        parent=form1MapCylindrical,
    )
    btnCloseMapCylindrical = pm.button(
        command=lambda *args: pm.deleteUI(winMapCylindrical),
        label="Close",
        parent=form1MapCylindrical,
    )

    # Layout frames
    pm.formLayout(
        form2MapCylindrical, edit=True,
        attachForm=[
            (frameMainMapCylindrical, "top", 0),
            (frameMainMapCylindrical, "left", 0),
            (frameMainMapCylindrical, "right", 0),

            (frameSetMapCylindrical, "left", 0),
            (frameSetMapCylindrical, "right", 0),
        ],
        attachControl=[
            (frameSetMapCylindrical, "top", 10, frameMainMapCylindrical),
        ],
        attachNone=[
            (frameSetMapCylindrical, "bottom"),
        ],
    )

    # Layout main form
    pm.formLayout(
        form1MapCylindrical, edit=True,
        attachForm=[
            (scrollMapCylindrical, "top", 0),
            (scrollMapCylindrical, "left", 0),
            (scrollMapCylindrical, "right", 0),

            (btnApplyCloseMapCylindrical, "left", 5),
            (btnApplyCloseMapCylindrical, "bottom", 5),
            (btnApplyMapCylindrical, "bottom", 5),
            (btnResetMapCylindrical, "bottom", 5),
            (btnCloseMapCylindrical, "right", 5),
            (btnCloseMapCylindrical, "bottom", 5),
        ],
        attachControl=[
            (scrollMapCylindrical, "bottom", 0, btnApplyCloseMapCylindrical),
        ],
        attachPosition=[
            (btnApplyCloseMapCylindrical, "right", 3, 25),
            (btnApplyMapCylindrical, "left", 2, 25),
            (btnApplyMapCylindrical, "right", 3, 50),
            (btnResetMapCylindrical, "right", 3, 75),
            (btnResetMapCylindrical, "left", 2, 50),
            (btnCloseMapCylindrical, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseMapCylindrical, "top"),
            (btnApplyMapCylindrical, "top"),
            (btnResetMapCylindrical, "top"),
            (btnCloseMapCylindrical, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for changing the normal based mapping options
def mapNormalUI():

    # Vars
    visState = False

    # Reset UI
    def mapNormalReset():

        # Reset UI controls
        cBox1MSMapNormal.setValue1(True)
        cBox2MSMapNormal.setValue1(True)
        cBox3MSMapNormal.setValue1(True)
        cBoxSetMapNormal.setValue1(False)
        fieldSetMapNormal.setEnable(False)
        fieldSetMapNormal.setText("uvSet1")
        fieldSetMapNormal.setEnable(False)
        
        # Reset optVars
        pm.optionVar["mapNormalMS1_NSUV"] = True
        pm.optionVar["mapNormalMS2_NSUV"] = True
        pm.optionVar["mapNormalMS3_NSUV"] = True
        pm.optionVar["mapNormalSetBox_NSUV"] = False
        pm.optionVar["mapNormalSet_NSUV"] = "uvSet1"


    # Update optVar
    def mapNormalOptVar(varType):

        if varType == 1:
            pm.optionVar["mapNormalMS1_NSUV"] = cBox1MSMapNormal.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapNormalSetBox_NSUV"] == False: fieldSetMapNormal.setEnable(False)
            else: fieldSetMapNormal.setEnable(True)

        elif varType == 2:
            pm.optionVar["mapNormalMS2_NSUV"] = cBox2MSMapNormal.getValue1()

        elif varType == 3:
            pm.optionVar["mapNormalMS3_NSUV"] = cBox3MSMapNormal.getValue1()

        elif varType == 4:
            pm.optionVar["mapNormalSetBox_NSUV"] = cBoxSetMapNormal.getValue1()

            if pm.optionVar["mapNormalSetBox_NSUV"] == True: fieldSetMapNormal.setEnable(True)
            else: fieldSetMapNormal.setEnable(False)

        elif varType == 5:
            pm.optionVar["mapNormalSet_NSUV"] = fieldSetMapNormal.getText()
            
        elif varType == 6:
            pm.optionVar["mapNormalFrame1_NSUV"] = frameSetMapNormal.getCollapse()


    # Check for window duplicate
    if pm.window( winMapNormal, exists=True ):
        pm.deleteUI(winMapNormal)

    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapNormalSet_NSUV"] == True:
        visState = True

    # Window
    window = pm.window(
        winMapNormal,
        height=mapNormalWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Mapping: Normal Based Projection",
        width=largeWinX
    )

    # Create layout
    form1MapNormal = pm.formLayout()
    scrollMapNormal = pm.scrollLayout( childResizable=True )
    form2MapNormal = pm.formLayout( parent=scrollMapNormal )

    frameMainMapNormal = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Normal Based Projection Options",
        parent=form2MapNormal
    )

    sep1MapNormal = pm.separator(
        height=1,
        horizontal=True,
        parent=frameMainMapNormal,
        style="none",
        visible=True,
    )

    # Description text
    textDescMapNormal = pm.text(
        label="Creates a planar projection based on the average \n"
              "vector of the face normals in the active selection.\n"
              "Try and avoid backface selections for best results.",
        parent=frameMainMapNormal,
        width=(mappingCol1 + mappingCol2 + mappingCol3),
    )

    sep2MapNormal = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=frameMainMapNormal,
        visible=True,
    )

    # Mapping Settings: Frame and column
    frameMSMapNormal = pm.frameLayout(
        borderVisible=False,
        label="Settings",
        parent=form2MapNormal,
    )
    colSetNormal = pm.columnLayout(
        parent=frameMSMapNormal
    )

    # Mapping Settings: UI elements
    cBox1MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalOptVar(1),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Keep width/height ratio",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS1_NSUV"],
    )
    cBox2MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalOptVar(2),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS2_NSUV"],
    )
    cBox3MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalOptVar(3),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetNormal,
        value1=pm.optionVar["mapNormalMS3_NSUV"],
    )

    sep3MapNormal = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetNormal,
        visible=True,
    )

    # UV Set: Frame and column
    frameSetMapNormal = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapNormalFrame1_NSUV"],
        collapseCommand=lambda *args: mapNormalOptVar(6),
        expandCommand=lambda *args: mapNormalOptVar(6),
        label="UV Set",
        parent=form2MapNormal
    )
    colSetMapNormal = pm.columnLayout(
        parent=frameSetMapNormal
    )

    # UV Set: UI elements
    cBoxSetMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapNormalOptVar(4),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapNormal,
        value1=pm.optionVar["mapNormalSetBox_NSUV"],
    )
    if mayaVer >= 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapNormal = pm.textFieldGrp(
            changeCommand=lambda *args: mapNormalOptVar(5),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapNormal,
            text=pm.optionVar["mapNormalSet_NSUV"],
        )
    else:
        fieldSetMapNormal = pm.textFieldGrp(
            changeCommand=lambda *args: mapNormalOptVar(5),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapNormal,
            text=pm.optionVar["mapNormalSet_NSUV"],
            textChangedCommand=lambda *args: mapNormalOptVar(5),
        )
    sep3MapAuto = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapNormal,
        visible=True,
    )

    # Buttons
    btnApplyCloseMapNormal = pm.button(
        command=lambda *args: core.mapping("normal", None, winMapNormal),
        label="Confirm",
        parent=form1MapNormal,
    )
    btnApplyMapNormal = pm.button(
        command=lambda *args: core.mapping("normal"),
        label="Apply",
        parent=form1MapNormal,
    )
    btnResetMapNormal = pm.button(
        command=lambda *args: mapNormalReset(),
        label="Reset",
        parent=form1MapNormal,
    )
    btnCloseMapNormal = pm.button(
        command=lambda *args: pm.deleteUI(winMapNormal),
        label="Close",
        parent=form1MapNormal,
    )

    # Layout frames
    pm.formLayout(
        form2MapNormal, edit=True,
        attachForm=[
            (frameMainMapNormal, "top", 0),
            (frameMainMapNormal, "left", 0),
            (frameMainMapNormal, "right", 0),

            (frameMSMapNormal, "left", 0),
            (frameMSMapNormal, "right", 0),

            (frameSetMapNormal, "left", 0),
            (frameSetMapNormal, "right", 0),
        ],
        attachControl=[
            (frameMSMapNormal, "top", 10, frameMainMapNormal),

            (frameSetMapNormal, "top", 10, frameMSMapNormal),
        ],
        attachNone=[
            (frameMSMapNormal, "bottom"),

            (frameSetMapNormal, "bottom"),
        ],
    )

    # Layout main form
    pm.formLayout(
        form1MapNormal, edit=True,
        attachForm=[
            (scrollMapNormal, "top", 0),
            (scrollMapNormal, "left", 0),
            (scrollMapNormal, "right", 0),

            (btnApplyCloseMapNormal, "left", 5),
            (btnApplyCloseMapNormal, "bottom", 5),
            (btnApplyMapNormal, "bottom", 5),
            (btnResetMapNormal, "bottom", 5),
            (btnCloseMapNormal, "right", 5),
            (btnCloseMapNormal, "bottom", 5),
        ],
        attachControl=[
            (scrollMapNormal, "bottom", 0, btnApplyCloseMapNormal),
        ],
        attachPosition=[
            (btnApplyCloseMapNormal, "right", 3, 25),
            (btnApplyMapNormal, "left", 2, 25),
            (btnApplyMapNormal, "right", 3, 50),
            (btnResetMapNormal, "right", 3, 75),
            (btnResetMapNormal, "left", 2, 50),
            (btnCloseMapNormal, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseMapNormal, "top"),
            (btnApplyMapNormal, "top"),
            (btnResetMapNormal, "top"),
            (btnCloseMapNormal, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for changing the planar mapping options
def mapPlanarUI(axis):

    # Vars
    visState1, visState2 = (False,)*2

    # Overwrite optVar
    if axis == "x":
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 1
    elif axis == "y":
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 2
    elif axis == "z":
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 3
    elif axis == "cam":
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 4


    # Switch projection method
    def mapPlanarSwitch():

        if radGrpMethodMapPlanar.getSelect() == 1:
            frameMSMapPlanar.setVisible(True)
            frameSetMapPlanar.setVisible(True)
            textQuickMapPlanar.setVisible(False)

        elif radGrpMethodMapPlanar.getSelect() == 2:
            frameMSMapPlanar.setVisible(False)
            frameSetMapPlanar.setVisible(False)
            textQuickMapPlanar.setVisible(True)

        # Save optVar
        pm.optionVar["mapPlanarMethod_NSUV"] = radGrpMethodMapPlanar.getSelect()


    # Reset UI
    def mapPlanarReset():

        # Reset UI controls
        radGrpMethodMapPlanar.setSelect(1)
        radGrp1MSMapPlanar.setSelect(2)
        menuMSMapPlanar.setSelect(1)
        menuMSMapPlanar.setEnable(True)
        cBox1MSMapPlanar.setValue1(True)
        cBox2MSMapPlanar.setValue1(True)
        cBox3MSMapNormal.setValue1(True)
        cBoxSetMapPlanar.setValue1(False)
        fieldSetMapPlanar.setText("uvSet1")
        fieldSetMapPlanar.setEnable(False)

        # Reset optVars
        pm.optionVar["mapPlanarMethod_NSUV"] = 1
        pm.optionVar["mapPlanarMS1RadGrp_NSUV"] = 2
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 1
        pm.optionVar["mapPlanarMS1Box_NSUV"] = True
        pm.optionVar["mapPlanarMS2Box_NSUV"] = True
        pm.optionVar["mapPlanarMS3Box_NSUV"] = True
        pm.optionVar["mapPlanarSetBox_NSUV"] = False
        pm.optionVar["mapPlanarSet_NSUV"] = "uvSet1"

        # Hide inactive
        mapPlanarSwitch()


    # Update optVar
    def mapPlanarOptVar(varType):

        if varType == 1:
            pm.optionVar["mapPlanarMS1RadGrp_NSUV"] = radGrp1MSMapPlanar.getSelect()

            # Turn on/off UI controls
            if pm.optionVar["mapPlanarMS1RadGrp_NSUV"] == 1: menuMSMapPlanar.setEnable(False)
            else: menuMSMapPlanar.setEnable(True)

        elif varType == 2:
            pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = menuMSMapPlanar.getSelect()

        elif varType == 3:
            pm.optionVar["mapPlanarMS1Box_NSUV"] = cBox1MSMapPlanar.getValue1()

        elif varType == 4:
            pm.optionVar["mapPlanarMS2Box_NSUV"] = cBox2MSMapPlanar.getValue1()

        elif varType == 5:
            pm.optionVar["mapPlanarSetBox_NSUV"] = cBoxSetMapPlanar.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapPlanarSetBox_NSUV"] == False: fieldSetMapPlanar.setEnable(False)
            else: fieldSetMapPlanar.setEnable(True)

        elif varType == 6:
            pm.optionVar["mapPlanarSet_NSUV"] = fieldSetMapPlanar.getText()

        elif varType == 7:
            pm.optionVar["mapPlanarMS3Box_NSUV"] = cBox3MSMapNormal.getValue1()
            
        elif varType == 8:
            pm.optionVar["mapPlanarFrame1_NSUV"] = frameSetMapPlanar.getCollapse()


    # Check for window duplicate
    if pm.window( winMapPlanar, exists=True ):
        pm.deleteUI(winMapPlanar)

    # Read UI control optVars - Set visibility states
    if pm.optionVar["mapPlanarMS1RadGrp_NSUV"] == 2:
        visState1 = True

    if pm.optionVar["mapPlanarSetBox_NSUV"] == True:
        visState2 = True

    # Window
    window = pm.window(
        winMapPlanar,
        height=mapPlanarWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Mapping: Planar Projection",
        width=largeWinX
    )

    # Create layouts
    form1MapPlanar = pm.formLayout()
    scrollMapPlanar = pm.scrollLayout( childResizable=True )
    form2MapPlanar = pm.formLayout( parent=scrollMapPlanar )

    frameMainMapPlanar = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Planar Projection Options",
        parent=form2MapPlanar
    )

    # Method radioBtnGrp
    radGrpMethodMapPlanar = pm.radioButtonGrp(
        changeCommand=lambda *args: mapPlanarSwitch(),
        columnWidth2=[mappingCol1, mappingCol2],
        label="Method: ",
        labelArray2=["Custom", "Quick"],
        numberOfRadioButtons=2,
        parent=frameMainMapPlanar,
        select=pm.optionVar["mapPlanarMethod_NSUV"],
        vertical=True,
    )


    ## Custom

    # Mapping Settings: Frame and column
    frameMSMapPlanar = pm.frameLayout(
        label="Settings",
        parent=form2MapPlanar
    )
    colMSMapPlanar = pm.columnLayout(
        parent=frameMSMapPlanar
    )

    # Mapping Settings: UI elements
    radGrp1MSMapPlanar = pm.radioButtonGrp(
        changeCommand=lambda *args: mapPlanarOptVar(1),
        columnWidth2=[mappingCol1, mappingCol2],
        label1="Best plane",
        label2="Bounding box",
        label="Fit projection to: ",
        numberOfRadioButtons=2,
        parent=colMSMapPlanar,
        select=pm.optionVar["mapPlanarMS1RadGrp_NSUV"],
        vertical=True,
    )
    sep1MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )
    
    menuMSMapPlanar = pm.optionMenuGrp(
        changeCommand=lambda *args: mapPlanarOptVar(2),
        columnWidth2=[mappingCol1, mappingCol2],
        label="Projection from: ",
        parent=colMSMapPlanar,
    )

    itemAxisX = pm.menuItem(label="X axis")    
    itemAxisY = pm.menuItem(label="Y axis")    
    itemAxisZ = pm.menuItem(label="Z axis")
    itemCam = pm.menuItem(label="Camera")

    menuMSMapPlanar.setSelect(pm.optionVar["mapPlanarMS2RadGrp_NSUV"])
    
    sep2MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )
    cBox1MSMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarOptVar(3),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Keep width/height ratio",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS1Box_NSUV"],
    )
    cBox2MSMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarOptVar(4),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Insert projection before deformers",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS2Box_NSUV"],
    )
    cBox3MSMapNormal = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarOptVar(7),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colMSMapPlanar,
        value1=pm.optionVar["mapPlanarMS3Box_NSUV"],
    )
    sep3MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colMSMapPlanar,
        visible=True,
    )

    # UV Set: Frame and column
    frameSetMapPlanar = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapPlanarFrame1_NSUV"],
        collapseCommand=lambda *args: mapPlanarOptVar(8),
        expandCommand=lambda *args: mapPlanarOptVar(8),
        label="UV Set",
        parent=form2MapPlanar
    )
    colSetMapPlanar = pm.columnLayout(
        parent=frameSetMapPlanar
    )

    # UV Set: UI elements
    cBoxSetMapPlanar = pm.checkBoxGrp(
        changeCommand=lambda *args: mapPlanarOptVar(5),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapPlanar,
        value1=pm.optionVar["mapPlanarSetBox_NSUV"],
    )
    if mayaVer >= 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapPlanar = pm.textFieldGrp(
            changeCommand=lambda *args: mapPlanarOptVar(6),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState2,
            label="UV Set name: ",
            parent=colSetMapPlanar,
            text=pm.optionVar["mapPlanarSet_NSUV"],
        )
    else:
        fieldSetMapPlanar = pm.textFieldGrp(
            changeCommand=lambda *args: mapPlanarOptVar(6),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState2,
            label="UV Set name: ",
            parent=colSetMapPlanar,
            text=pm.optionVar["mapPlanarSet_NSUV"],
            textChangedCommand=lambda *args: mapPlanarOptVar(6),
        )
    sep4MapPlanar = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapPlanar,
        visible=True,
    )


    ## Quick

    textQuickMapPlanar = pm.text(
        label="No options here - Things just get done!!",
        parent=form2MapPlanar
    )

    # Buttons
    btnApplyCloseMapPlanar = pm.button(
        command=lambda *args: core.mapping("plane", None, winMapPlanar),
        label="Confirm",
        parent=form1MapPlanar,
    )
    btnApplyMapPlanar = pm.button(
        command=lambda *args: core.mapping("plane"),
        label="Apply",
        parent=form1MapPlanar,
    )
    btnResetMapPlanar = pm.button(
        command=lambda *args: mapPlanarReset(),
        label="Reset",
        parent=form1MapPlanar,
    )
    btnCloseMapPlanar = pm.button(
        command=lambda *args: pm.deleteUI(winMapPlanar),
        label="Close",
        parent=form1MapPlanar,
    )

    # Layout frames
    pm.formLayout(
        form2MapPlanar, edit=True,
        attachForm=[

            (frameMainMapPlanar, "top", 0),
            (frameMainMapPlanar, "left", 0),
            (frameMainMapPlanar, "right", 0),

            (frameMSMapPlanar, "left", 0),
            (frameMSMapPlanar, "right", 0),

            (frameSetMapPlanar, "left", 0),
            (frameSetMapPlanar, "right", 0),

            (textQuickMapPlanar, "left", 0),
            (textQuickMapPlanar, "right", 0),
        ],
        attachControl=[
            (frameMSMapPlanar, "top", 10, frameMainMapPlanar),

            (frameSetMapPlanar, "top", 10, frameMSMapPlanar),

            (textQuickMapPlanar, "top", 0, frameSetMapPlanar),
        ],
        attachNone=[
            (frameMSMapPlanar, "bottom"),

            (frameSetMapPlanar, "bottom"),

            (textQuickMapPlanar, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1MapPlanar, edit=True,
        attachForm=[
            (scrollMapPlanar, "top", 0),
            (scrollMapPlanar, "left", 0),
            (scrollMapPlanar, "right", 0),

            (btnApplyCloseMapPlanar, "left", 5),
            (btnApplyCloseMapPlanar, "bottom", 5),
            (btnApplyMapPlanar, "bottom", 5),
            (btnResetMapPlanar, "bottom", 5),
            (btnCloseMapPlanar, "right", 5),
            (btnCloseMapPlanar, "bottom", 5),
        ],
        attachControl=[
            (scrollMapPlanar, "bottom", 0, btnApplyCloseMapPlanar),
        ],
        attachPosition=[
            (btnApplyCloseMapPlanar, "right", 3, 25),
            (btnApplyMapPlanar, "left", 2, 25),
            (btnApplyMapPlanar, "right", 3, 50),
            (btnResetMapPlanar, "right", 3, 75),
            (btnResetMapPlanar, "left", 2, 50),
            (btnCloseMapPlanar, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseMapPlanar, "top"),
            (btnApplyMapPlanar, "top"),
            (btnResetMapPlanar, "top"),
            (btnCloseMapPlanar, "top"),
        ],
    )

    # Hide inactive
    mapPlanarSwitch()

    # Display the window
    pm.showWindow(window)

    
# UI for changing the spherical mapping options
def mapSphericalUI():

    # Vars
    visState = False


    # Reset UI
    def mapSphericalReset():

        # Reset UI controls
        slider1MapSpherical.setValue(180)
        slider2MapSpherical.setValue(90)
        cBox1MSMapSpherical.setValue1(True)
        cBox2MSMapSpherical.setValue1(True)
        cBoxSetMapSpherical.setValue1(False)
        fieldSetMapSpherical.setEnable(False)
        fieldSetMapSpherical.setText("uvSet1")
        
        # Reset optVars
        pm.optionVar["mapSphericalSweep1_NSUV"] = 180
        pm.optionVar["mapSphericalSweep2_NSUV"] = 90
        pm.optionVar["mapSphericalMS1Box_NSUV"] = True
        pm.optionVar["mapSphericalMS2Box_NSUV"] = True
        pm.optionVar["mapSphericalSetBox_NSUV"] = False
        pm.optionVar["mapSphericalSet_NSUV"] = "uvSet1"


    # Update optVar
    def mapSphericalOptVar(varType):

        if varType == 1:
            pm.optionVar["mapSphericalMS1Box_NSUV"] = cBox1MSMapSpherical.getValue1()

        elif varType == 2:
            pm.optionVar["mapSphericalMS2Box_NSUV"] = cBox2MSMapSpherical.getValue1()

        if varType == 3:
            pm.optionVar["mapSphericalSetBox_NSUV"] = cBoxSetMapSpherical.getValue1()

            # Turn on/off UI controls
            if pm.optionVar["mapSphericalSetBox_NSUV"] == False: fieldSetMapSpherical.setEnable(False)
            else: fieldSetMapSpherical.setEnable(True)

        elif varType == 4:
            pm.optionVar["mapSphericalSet_NSUV"] = fieldSetMapSpherical.getText()

        elif varType == 5:
            pm.optionVar["mapSphericalSweep1_NSUV"] = slider1MapSpherical.getValue()

        elif varType == 6:
            pm.optionVar["mapSphericalSweep2_NSUV"] = slider2MapSpherical.getValue()
            
        elif varType == 7:
            pm.optionVar["mapSphericalFrame1_NSUV"] = frameSetMapSpherical.getCollapse()


    # Check for window duplicate
    if pm.window( winMapSpherical, exists=True ):
        pm.deleteUI(winMapSpherical)

    # Read UI control optVar - Set visibility state
    if pm.optionVar["mapSphericalSet_NSUV"] == True:
        visState = True

    # Window
    window = pm.window(
        winMapSpherical,
        height=mapSphericalWinY,
        minimizeButton=True,
        maximizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="UV Mapping: Spherical Projection",
        width=largeWinX
    )

    # Create layout
    form1MapSpherical = pm.formLayout()
    scrollMapSpherical = pm.scrollLayout( childResizable=True )
    form2MapSpherical = pm.formLayout( parent=scrollMapSpherical )

    # Mapping Settings: Frame and column
    frameMainMapSpherical = pm.frameLayout(
        borderVisible=False,
        label="Spherical Projection Options",
        parent=form2MapSpherical,
    )
    colSetSpherical = pm.columnLayout(
        parent=frameMainMapSpherical
    )

    # Mapping Settings: UI elements
    slider1MapSpherical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapSphericalOptVar(5),
        columnWidth3=[mappingCol1, mappingCol2, mappingCol3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=360.00,
        label="Projection sweep (H): ",
        minValue=0.00,
        maxValue=360.00,
        parent=colSetSpherical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapSphericalSweep1_NSUV"],
    )
    slider2MapSpherical = pm.floatSliderGrp(
        changeCommand=lambda *args: mapSphericalOptVar(6),
        columnWidth3=[mappingCol1, mappingCol2, mappingCol3],
        field=True,
        fieldMinValue=0.00,
        fieldMaxValue=180.00,
        label="Projection sweep (V): ",
        minValue=0.00,
        maxValue=180.00,
        parent=colSetSpherical,
        precision=2,
        step=0.1,
        value=pm.optionVar["mapSphericalSweep2_NSUV"],
    )
    cBox1MSMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalOptVar(1),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Insert projection before deformers",
        parent=colSetSpherical,
        value1=pm.optionVar["mapSphericalMS1Box_NSUV"],
    )
    cBox2MSMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalOptVar(2),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Show projection manipulator(s)",
        parent=colSetSpherical,
        value1=pm.optionVar["mapSphericalMS2Box_NSUV"],
    )
    sep1MapSpherical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetSpherical,
        visible=True,
    )

    # UV Set: Frame and column
    frameSetMapSpherical = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["mapSphericalFrame1_NSUV"],
        collapseCommand=lambda *args: mapSphericalOptVar(7),
        expandCommand=lambda *args: mapSphericalOptVar(7),
        label="UV Set",
        parent=form2MapSpherical
    )
    colSetMapSpherical = pm.columnLayout(
        parent=frameSetMapSpherical
    )

    # UV Set: UI elements
    cBoxSetMapSpherical = pm.checkBoxGrp(
        changeCommand=lambda *args: mapSphericalOptVar(3),
        columnWidth2=[mappingCol1, mappingCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapSpherical,
        value1=pm.optionVar["mapSphericalSetBox_NSUV"],
    )
    if mayaVer >= 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapSpherical = pm.textFieldGrp(
            changeCommand=lambda *args: mapSphericalOptVar(4),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapSpherical,
            text=pm.optionVar["mapSphericalSet_NSUV"],
        )
    else:
        fieldSetMapSpherical = pm.textFieldGrp(
            changeCommand=lambda *args: mapSphericalOptVar(4),
            columnWidth2=[mappingCol1, (mappingCol2+mappingCol3)],
            enable=visState,
            label="UV Set name: ",
            parent=colSetMapSpherical,
            text=pm.optionVar["mapSphericalSet_NSUV"],
            textChangedCommand=lambda *args: mapSphericalOptVar(4),
        )
    sep2MapSpherical = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapSpherical,
        visible=True,
    )

    # Buttons
    btnApplyCloseMapSpherical = pm.button(
        command=lambda *args: core.mapping("sphere", None, winMapSpherical),
        label="Confirm",
        parent=form1MapSpherical,
    )
    btnApplyMapSpherical = pm.button(
        command=lambda *args: core.mapping("sphere"),
        label="Apply",
        parent=form1MapSpherical,
    )
    btnResetMapSpherical = pm.button(
        command=lambda *args: mapSphericalReset(),
        label="Reset",
        parent=form1MapSpherical,
    )
    btnCloseMapSpherical = pm.button(
        command=lambda *args: pm.deleteUI(winMapSpherical),
        label="Close",
        parent=form1MapSpherical,
    )

    # Layout frames
    pm.formLayout(
        form2MapSpherical, edit=True,
        attachForm=[
            (frameMainMapSpherical, "top", 0),
            (frameMainMapSpherical, "left", 0),
            (frameMainMapSpherical, "right", 0),

            (frameSetMapSpherical, "left", 0),
            (frameSetMapSpherical, "right", 0),
        ],
        attachControl=[
            (frameSetMapSpherical, "top", 10, frameMainMapSpherical),
        ],
        attachNone=[
            (frameSetMapSpherical, "bottom"),
        ],
    )

    # Layout main form
    pm.formLayout(
        form1MapSpherical, edit=True,
        attachForm=[
            (scrollMapSpherical, "top", 0),
            (scrollMapSpherical, "left", 0),
            (scrollMapSpherical, "right", 0),

            (btnApplyCloseMapSpherical, "left", 5),
            (btnApplyCloseMapSpherical, "bottom", 5),
            (btnApplyMapSpherical, "bottom", 5),
            (btnResetMapSpherical, "bottom", 5),
            (btnCloseMapSpherical, "right", 5),
            (btnCloseMapSpherical, "bottom", 5),
        ],
        attachControl=[
            (scrollMapSpherical, "bottom", 0, btnApplyCloseMapSpherical),
        ],
        attachPosition=[
            (btnApplyCloseMapSpherical, "right", 3, 25),
            (btnApplyMapSpherical, "left", 2, 25),
            (btnApplyMapSpherical, "right", 3, 50),
            (btnResetMapSpherical, "right", 3, 75),
            (btnResetMapSpherical, "left", 2, 50),
            (btnCloseMapSpherical, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseMapSpherical, "top"),
            (btnApplyMapSpherical, "top"),
            (btnResetMapSpherical, "top"),
            (btnCloseMapSpherical, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for changing the match UVs -tolerance value
def matchTolUI():

    # Vars
    sliderMatchTol = "NSUV_matchTolSlider"


    # Internal method for updating field and optVar
    def matchTolOptVar():
        pm.optionVar["matchTol_NSUV"] = sliderMatchTol.getValue()


    # Check for window duplicate
    if pm.window( winMatchTol, exists=True ):
        pm.deleteUI(winMatchTol)

    # Window
    window = pm.window(
        winMatchTol,
        height=matchTolWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Match UVs",
    )

    # Layouts
    form1MatchTol = pm.formLayout()
    form2MatchTol = pm.formLayout( parent=form1MatchTol )
    frameMatchTol = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Match UVs Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2MatchTol,
        width=smallWinX,
    )
    colMatchTol = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameMatchTol,
    )
    textMatchTol = pm.text(
        label="A higher value increases the likelyhood that UVs\n"\
"match to their neighboring UVs. The value is specified\nin UV units.",
        parent=colMatchTol,
    )

    # Slider
    sliderMatchTol = pm.floatSliderGrp(
        changeCommand=lambda *args: matchTolOptVar(),
        columnAlign=[1, "right"],
        columnWidth3=[smallCol1, 70, smallCol1],
        field=True,
        fieldMaxValue=0.05,
        fieldMinValue=0.001,
        label="Tolerance: ",
        maxValue=0.05,
        minValue=0.001,
        parent=colMatchTol,
        precision=3,
        sliderStep=0.01,
        value=pm.optionVar["matchTol_NSUV"],
    )

    # Buttons
    btnOkMatchTol = pm.button(
        command=lambda *args: core.matchUVs(),
        label="Match UVs",
        parent=form1MatchTol,
    )
    btnCloseMatchTol = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1MatchTol,
    )
    
    # Layout frame
    pm.formLayout(
        form2MatchTol, edit=True,
        attachForm=[
            (frameMatchTol, "top", 0),
            (frameMatchTol, "left", 0),
            (frameMatchTol, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1MatchTol, edit=True,
        attachForm=[
            (form2MatchTol, "top", 0),
            (form2MatchTol, "left", 0),
            (form2MatchTol, "right", 0),
        
            (btnOkMatchTol, "left", 5),
            (btnOkMatchTol, "bottom", 5),
            (btnCloseMatchTol, "right", 5),
            (btnCloseMatchTol, "bottom", 5),
        ],
        attachControl=[
            (form2MatchTol, "bottom", 0, btnCloseMatchTol),
        ],
        attachPosition=[
            (btnOkMatchTol, "right", 2, 50),
            (btnCloseMatchTol, "left", 1, 50),
        ],
        attachNone=[
            (btnOkMatchTol, "top"),
            (btnCloseMatchTol, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)

    
# Normalize/Unitize UI
def normalizeUI():

    # Vars
    visState1, visState2, visState3 = (False,)*3


    # Reset UI
    def normalizeReset():

        # Reset UI controls
        radGrp1Normalize.setSelect(1)
        radGrp2Normalize.setSelect(1)
        radGrp2Normalize.setEnable(True)
        radGrp3Normalize.setSelect(1)
        radGrp3Normalize.setEnable(True)
        cBoxSetMapNormalize.setValue1(False)
        fieldSetMapNormalize.setText("uvSet1")

        # Reset optVars
        pm.optionVar["normMethod_NSUV"] = 0
        pm.optionVar["normAspect_NSUV"] = 0
        pm.optionVar["normDirection_NSUV"] = 0
        pm.optionVar["normSetBox_NSUV"] = False
        pm.optionVar["normSet_NSUV"] = "uvSet1"


    # Internal method for updating field and optVar
    def normalizeOptVar(varType):
        
        if varType == 1:
            pm.optionVar["normMethod_NSUV"] = (radGrp1Normalize.getSelect() - 1) # 0- to 1-based
            
            if pm.optionVar["normMethod_NSUV"] != 2:                    
                radGrp2Normalize.setEnable(True)

                if pm.optionVar["normAspect_NSUV"] == 0:
                    radGrp3Normalize.setEnable(True)

            else:
                radGrp2Normalize.setEnable(False)
                radGrp3Normalize.setEnable(False)
         

        elif varType == 2:
            
            # Turn on/off UI control
            if radGrp2Normalize.getSelect() == 2: 
            
                radGrp3Normalize.setEnable(False)
                pm.optionVar["normAspect_NSUV"] = 1
                
                # Set direction radBtn to "U and V" and change it's optVar
                radGrp3Normalize.setSelect(1)
                pm.optionVar["normDirection_NSUV"] = 1
                
            else: 
                radGrp3Normalize.setEnable(True)
                pm.optionVar["normAspect_NSUV"] = 0

        elif varType == 3:
            pm.optionVar["normDirection_NSUV"] = radGrp3Normalize.getSelect()
            
        elif varType == 4:  
            pm.optionVar["normSetBox_NSUV"] = cBoxSetMapNormalize.getValue1()

            # Turn on/off UI control
            if pm.optionVar["normSetBox_NSUV"] == False: fieldSetMapNormalize.setEnable(False)
            else: fieldSetMapNormalize.setEnable(True)

        elif varType == 5:
            pm.optionVar["normSet_NSUV"] = fieldSetMapNormalize.getText()
            
        elif varType == 6:
            pm.optionVar["normFrame1_NSUV"] = frameSetMapNormalize.getCollapse()


    # Check for window duplicate
    if pm.window( winNormalize, exists=True ):
        pm.deleteUI(winNormalize)
        
    # Read UI control optVars - Set visibility states
    if pm.optionVar["normMethod_NSUV"] != 2:
        visState1 = True

        if pm.optionVar["normAspect_NSUV"] != 1:
            visState2 = True            
        
    if pm.optionVar["normSetBox_NSUV"] == True:
        visState3 = True

    # Window
    window = pm.window(
        winNormalize,
        height=normalizeWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Normalize UVs",
    )

    # Layouts
    form1Normalize = pm.formLayout()
    form2Normalize = pm.formLayout( parent=form1Normalize )
    frameMainNormalize = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Normalize UVs Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2Normalize,
        width=smallWinX,
    )
    colNormalize = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameMainNormalize,
    )
    
    # Elements
    radGrp1Normalize = pm.radioButtonGrp(
        changeCommand=lambda *args: normalizeOptVar(1),
        columnWidth2=[smallCol1, smallCol2],
        label="Method: ",
        labelArray3=["Normalize (selection)", "Normalize (shells)", "Unitize"],
        numberOfRadioButtons=3,
        parent=colNormalize,
        select=(pm.optionVar["normMethod_NSUV"] + 1), # 0- to 1-based
        vertical=True,
    )
    radGrp2Normalize = pm.radioButtonGrp(
        changeCommand=lambda *args: normalizeOptVar(2),
        columnWidth2=[smallCol1, smallCol2],
        enable=visState1,
        label="Aspect ratio: ",
        labelArray2=["Preserve", "Stretch"],
        numberOfRadioButtons=2,
        parent=colNormalize,
        select=(pm.optionVar["normAspect_NSUV"] + 1),
        vertical=True,
    )
    radGrp3Normalize = pm.radioButtonGrp(
        changeCommand=lambda *args: normalizeOptVar(3),
        columnWidth2=[smallCol1, smallCol2],
        enable=visState2,
        label="Direction: ",
        labelArray3=["U and V", "U only", "V only"],
        numberOfRadioButtons=3,
        parent=colNormalize,
        select=(pm.optionVar["normDirection_NSUV"] + 1),
        vertical=True,
    )
    
    # UV Set: Frame and column
    frameSetMapNormalize = pm.frameLayout(
        collapsable=True,
        collapse=pm.optionVar["normFrame1_NSUV"],
        collapseCommand=lambda *args: normalizeOptVar(6),
        expandCommand=lambda *args: normalizeOptVar(6),
        label="UV Set",
        parent=form2Normalize,
    )
    colSetMapNormalize = pm.columnLayout(
        parent=frameSetMapNormalize
    )

    # UV Set: UI elements
    cBoxSetMapNormalize = pm.checkBoxGrp(
        changeCommand=lambda *args: normalizeOptVar(4),
        columnWidth2=[smallCol1, smallCol2],
        label="",
        label1="Create new UV set",
        parent=colSetMapNormalize,
        value1=pm.optionVar["normSetBox_NSUV"],
    )
    if mayaVer >= 201200: # Because the textChangedCommand didnt exist in Maya 2012...
        fieldSetMapNormalize = pm.textFieldGrp(
            changeCommand=lambda *args: normalizeOptVar(5),
            columnWidth2=[smallCol1, smallCol2],
            enable=visState3,
            label="UV Set name: ",
            parent=colSetMapNormalize,
            text=pm.optionVar["normSet_NSUV"],
        )
    else:
        fieldSetMapNormalize = pm.textFieldGrp(
            changeCommand=lambda *args: normalizeOptVar(5),
            columnWidth2=[smallCol1, smallCol2],
            enable=visState3,
            label="UV Set name: ",
            parent=colSetMapNormalize,
            text=pm.optionVar["normSet_NSUV"],
            textChangedCommand=lambda *args: normalizeOptVar(5), # Added in 2013
        )
    sep2MapNormalize = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSetMapNormalize,
        visible=True,
    )

    # Buttons
    btnApplyCloseNormalize = pm.button(
        command=lambda *args: core.normalizeShells(0, winNormalize),
        label="Confirm",
        parent=form1Normalize,
    )
    btnApplyNormalize = pm.button(
        command=lambda *args: core.normalizeShells(0),
        label="Apply",
        parent=form1Normalize,
    )
    btnResetNormalize = pm.button(
        command=lambda *args: normalizeReset(),
        label="Reset",
        parent=form1Normalize,
    )
    btnCloseNormalize = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1Normalize,
    )
    
    # Layout frames
    pm.formLayout(
        form2Normalize, edit=True,
        attachForm=[
            (frameMainNormalize, "top", 0),
            (frameMainNormalize, "left", 0),
            (frameMainNormalize, "right", 0),

            (frameSetMapNormalize, "left", 0),
            (frameSetMapNormalize, "right", 0),
        ],
        attachControl=[
            (frameSetMapNormalize, "top", 10, frameMainNormalize),
        ],
        attachNone=[
            (frameSetMapNormalize, "bottom"),
        ],
    )
    
    # Layout main form
    pm.formLayout(
        form1Normalize, edit=True,
        attachForm=[
            (form2Normalize, "top", 0),
            (form2Normalize, "left", 0),
            (form2Normalize, "right", 0),

            (btnApplyCloseNormalize, "left", 5),
            (btnApplyCloseNormalize, "bottom", 5),
            (btnApplyNormalize, "bottom", 5),
            (btnResetNormalize, "bottom", 5),
            (btnCloseNormalize, "right", 5),
            (btnCloseNormalize, "bottom", 5),
        ],
        attachControl=[
            (form2Normalize, "bottom", 0, btnApplyCloseNormalize),
        ],
        attachPosition=[
            (btnApplyCloseNormalize, "right", 3, 25),
            (btnApplyNormalize, "left", 2, 25),
            (btnApplyNormalize, "right", 3, 50),
            (btnResetNormalize, "right", 3, 75),
            (btnResetNormalize, "left", 2, 50),
            (btnCloseNormalize, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseNormalize, "top"),
            (btnApplyNormalize, "top"),
            (btnResetNormalize, "top"),
            (btnCloseNormalize, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)
    

# UI for randomizing shells
def randomizeUI():

    # Vars
    cBox1Width = 40
    cBox2Width = 70
    
    cBoxR1Rnd, cBoxR2Rnd, cBoxS1Rnd, cBoxS2Rnd, cBoxT1Rnd, cBoxT2Rnd, \
    fSliderGrpRRnd, fSliderGrpSRnd, fSliderGrpTRnd = (None,)*9


    # Update optVar
    def randomizeOptVar(varType):

        if varType == 1:
            pm.optionVar["randTBox1_NSUV"] = cBoxT1Rnd.getValue()

        elif varType == 2:
            pm.optionVar["randTBox2_NSUV"] = cBoxT2Rnd.getValue()

        if varType == 3:
            pm.optionVar["randT_NSUV"] = fSliderGrpTRnd.getValue()

        elif varType == 4:
            pm.optionVar["randRBox1_NSUV"] = cBoxR1Rnd.getValue()

        elif varType == 5:
            pm.optionVar["randRBox2_NSUV"] = cBoxR2Rnd.getValue()

        elif varType == 6:
            pm.optionVar["randR_NSUV"] = fSliderGrpRRnd.getValue()

        elif varType == 7:
            pm.optionVar["randSBox1_NSUV"] = cBoxS1Rnd.getValue()

        elif varType == 8:
            pm.optionVar["randSBox2_NSUV"] = cBoxS2Rnd.getValue()

        elif varType == 9:
            pm.optionVar["randS_NSUV"] = fSliderGrpSRnd.getValue()

        else:
            print("Incorrect values specified for the UI.randomizeUI.randomizeOptVar() -method")


    # Check for window duplicate
    if pm.window( winRnd, exists=True ):
        pm.deleteUI(winRnd)

    # Main window
    window = pm.window(
        winRnd,
        height=randWinY,
        maximizeButton=False,
        minimizeButton=False,
        sizeable=True,
        title="Randomize Shells",
    )

    # Layouts
    form1Rnd = pm.formLayout()
    form2Rnd = pm.formLayout( parent=form1Rnd )
    frameRnd = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Randomize Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2Rnd,
        width=smallWinX,
    )
    colRnd = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameRnd,
    )

    # The translate row - and it's components
    rowTRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3,
        parent=colRnd,
    )
    textTRnd = pm.text(
        align="right",
        label="Translate: ",
        parent=rowTRnd,
        width=smallCol1,
    )
    cBoxT1Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(1),
        label="U",
        parent=rowTRnd,
        value=pm.optionVar["randTBox1_NSUV"],
        width=cBox1Width
    )
    cBoxT2Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(2),
        label="V",
        parent=rowTRnd,
        value=pm.optionVar["randTBox2_NSUV"],
        width=cBox2Width
    )
    fSliderGrpTRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randomizeOptVar(3),
        columnAlign=[1, "right"],
        columnWidth3=[smallCol1, cBox2Width, smallCol1],
        field=True,
        fieldMinValue=0.01,
        fieldMaxValue=1.0,
        label="Units (max): ",
        maxValue=1.0,
        minValue=0.001,
        parent=colRnd,
        precision=3,
        sliderStep=0.01,
        value=pm.optionVar["randT_NSUV"]
    )
    sep1Rnd = pm.separator(
        height=2,
        parent=colRnd,
        style="in",
    )

    # The rotate row - and it's components
    rowRRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3,
        parent=colRnd,
        width=smallWinX
    )
    textRRnd = pm.text(
        align="right",
        label="Rotate: ",
        parent=rowRRnd,
        width=smallCol1,
    )
    cBoxR1Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(4),
        label="CW",
        parent=rowRRnd,
        value=pm.optionVar["randRBox1_NSUV"],
        width=cBox1Width
    )
    cBoxR2Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(5),
        label="CCW",
        parent=rowRRnd,
        value=pm.optionVar["randRBox2_NSUV"],
        width=cBox2Width
    )
    fSliderGrpRRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randomizeOptVar(6),
        columnAlign=[1, "right"],
        columnWidth3=[smallCol1, cBox2Width, smallCol1],
        field=True,
        fieldMinValue=0.1,
        fieldMaxValue=180,
        label="Degrees (max): ",
        maxValue=180,
        minValue=1,
        parent=colRnd,
        value=pm.optionVar["randR_NSUV"]
    )
    sep2Rnd = pm.separator(
        height=2,
        parent=colRnd,
        style="in",
    )

    # The scale row - and it's components
    rowSRnd = pm.rowLayout(
        columnAttach3=["both", "both", "both"],
        numberOfColumns=3,
        parent=colRnd,
    )
    textSRnd = pm.text(
        align="right",
        label="Scale: ",
        parent=rowSRnd,
        width=smallCol1,
    )
    cBoxS1Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(7),
        label="Up",
        parent=rowSRnd,
        value=pm.optionVar["randSBox1_NSUV"],
        width=cBox1Width
    )
    cBoxS2Rnd = pm.checkBox(
        changeCommand=lambda *args: randomizeOptVar(8),
        label="Down",
        parent=rowSRnd,
        value=pm.optionVar["randSBox2_NSUV"],
        width=cBox2Width
    )
    fSliderGrpSRnd = pm.floatSliderGrp(
        changeCommand=lambda *args: randomizeOptVar(9),
        columnAlign=[1, "right"],
        columnWidth3=[smallCol1, cBox2Width, smallCol1],
        field=True,
        fieldMinValue=1,
        fieldMaxValue=180,
        label="Percent (max): ",
        maxValue=100,
        minValue=0.1,
        parent=colRnd,
        precision=1,
        sliderStep=1,
        value=pm.optionVar["randS_NSUV"]
    )

    # Buttons
    btnGoRnd = pm.button(
        command=lambda *args: core.randomizeShells(),
        label="Randomize",
        parent=form1Rnd,
    )
    btnCloseRnd = pm.button(
        command=lambda *args: pm.deleteUI(winRnd),
        label="Close",
        parent=form1Rnd,
    )

    # Layout frame
    pm.formLayout(
        form2Rnd, edit=True,
        attachForm=[
            (frameRnd, "top", 0),
            (frameRnd, "left", 0),
            (frameRnd, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1Rnd, edit=True,
        attachForm=[
            (form2Rnd, "top", 0),
            (form2Rnd, "left", 0),
            (form2Rnd, "right", 0),
        
            (btnGoRnd, "left", 5),
            (btnGoRnd, "bottom", 5),
            (btnCloseRnd, "right", 5),
            (btnCloseRnd, "bottom", 5),
        ],
        attachControl=[
            (form2Rnd, "bottom", 0, btnCloseRnd),
        ],
        attachPosition=[
            (btnGoRnd, "right", 2, 50),
            (btnCloseRnd, "left", 1, 50),
        ],
        attachNone=[
            (btnGoRnd, "top"),
            (btnCloseRnd, "top"),
        ],
    )

    pm.showWindow(window) # Display the window


# Options UI for the unfold feature
def relaxUI():

    # Vars
    visState1 = False

    radGrpRelax, sliderItrRelax, sliderAngleRelax, sliderPowerRelax, cBoxBorderRelax, \
    cBoxFlipsRelax, menuSpacingRelax, sliderSpacingRelax, cBoxPin1Relax, cBoxPin2Relax, \
    radGrpPinRelax, radGrpWeightRelax, sliderMaxItrRelax = (None,)*13
    
    # Look for the unfold3D plugin
    unfold3DLoaded = pm.pluginInfo("Unfold3D", query=True, loaded=True)

    # Fix array overflow
    if unfold3DLoaded == True and pm.optionVar["relaxMethod_NSUV"] == 3:
        pm.optionVar["relaxMethod_NSUV"] = 2


    # Switch relax method
    def relaxSwitch():

        # Unfold3D plugin loaded
        if unfold3DLoaded == True:

            # Unfold3D. Hide Legacy frames
            if radGrpRelax.getSelect() == 1:
                frameOptiRelax.setVisible(True)
                frameSpacingRelax.setVisible(True)
                framePinningRelax.setVisible(False)
                frameSettingsRelax.setVisible(False)
                textQuickRelax.setVisible(False)

            # Legacy. Hide Unfold3D frames
            elif radGrpRelax.getSelect() == 2 :
                frameOptiRelax.setVisible(False)
                frameSpacingRelax.setVisible(False)
                framePinningRelax.setVisible(True)
                frameSettingsRelax.setVisible(True)
                textQuickRelax.setVisible(False)

            else: # Quick. Hide all frames
                frameOptiRelax.setVisible(False)
                frameSpacingRelax.setVisible(False)
                framePinningRelax.setVisible(False)
                frameSettingsRelax.setVisible(False)
                textQuickRelax.setVisible(True)

        else: # Plugin not loaded

            if radGrpRelax.getSelect() == 1:
                frameOptiRelax.setVisible(False)
                frameSpacingRelax.setVisible(False)
                framePinningRelax.setVisible(True)
                frameSettingsRelax.setVisible(True)
                textQuickRelax.setVisible(False)

            else:
                frameOptiRelax.setVisible(False)
                frameSpacingRelax.setVisible(False)
                framePinningRelax.setVisible(False)
                frameSettingsRelax.setVisible(False)
                textQuickRelax.setVisible(True)

        # Save optVar
        pm.optionVar["relaxMethod_NSUV"] = radGrpRelax.getSelect()


    # Reset UI
    def relaxUIReset():

        # Reset UI controls
        radGrpRelax.setSelect(1)
        sliderItrRelax.setValue(1)
        sliderAngleRelax.setValue(1.0)
        sliderPowerRelax.setValue(100)
        cBoxBorderRelax.setValue1(True)
        cBoxFlipsRelax.setValue1(True)
        sliderSpacingRelax.setValue(2)
        sliderSizeRelax.setValue(1024)
        cBoxPin1Relax.setValue1(False)
        cBoxPin2Relax.setValue1(False)
        radGrpPinRelax.setSelect(1)
        radGrpWeightRelax.setSelect(1)
        sliderMaxItrRelax.setValue(5)

        # Reset optVars
        pm.optionVar["relaxMethod_NSUV"] = 1
        pm.optionVar["relaxItr_NSUV"] = 1
        pm.optionVar["relaxAngle_NSUV"] = 1.0
        pm.optionVar["relaxPower_NSUV"] = 100
        pm.optionVar["relaxBorder_NSUV"] = True
        pm.optionVar["relaxFlips_NSUV"] = True
        pm.optionVar["relaxSpacing_NSUV"] = 2
        pm.optionVar["relaxSize_NSUV"] = 1024
        pm.optionVar["relaxPinBorder_NSUV"] = False
        pm.optionVar["relaxPin_NSUV"] = False
        pm.optionVar["relaxPinType_NSUV"] = 1
        pm.optionVar["relaxEdge_NSUV"] = 1
        pm.optionVar["relaxMaxItr_NSUV"] = 5

        # Switch to the correct layouts
        relaxSwitch()


    # Update optVar
    def relaxOptVar(varType, control=None, control2=None):

        if varType == 1:
            pm.optionVar["relaxItr_NSUV"] = sliderItrRelax.getValue()

        elif varType == 2:
            pm.optionVar["relaxAngle_NSUV"] = sliderAngleRelax.getValue()

        elif varType == 3:
            pm.optionVar["relaxPower_NSUV"] = sliderPowerRelax.getValue()

        elif varType == 4:
            pm.optionVar["relaxBorder_NSUV"] = cBoxBorderRelax.getValue1()

        elif varType == 5:
            pm.optionVar["relaxFlips_NSUV"] = cBoxFlipsRelax.getValue1()

        elif varType == 6:
            pm.optionVar["relaxSize_NSUV"] = sliderSizeRelax.getValue()

        elif varType == 7:
            pm.optionVar["relaxSpacing_NSUV"] = sliderSpacingRelax.getValue()

        elif varType == 8:
            pm.optionVar["relaxPinBorder_NSUV"] = cBoxPin1Relax.getValue1()

        elif varType == 9:

            # Manipulate the other controls, then set optVar
            if control.getValue1() == True: control2.setEnable(True) # Show
            else: control2.setEnable(False) # Hide
            pm.optionVar["relaxPin_NSUV"] = control.getValue1()

        elif varType == 10:
            pm.optionVar["relaxPinType_NSUV"] = radGrpPinRelax.getSelect()

        elif varType == 11:
            pm.optionVar["relaxEdge_NSUV"] = radGrpRelax.getSelect()

        elif varType == 12:
            pm.optionVar["relaxMaxItr_NSUV"] = sliderMaxItrRelax.getValue()

        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.unfoldUI.relaxOptVar()")


    # Check for window duplicate
    if pm.window( winRelax, exists=True ):
        pm.deleteUI(winRelax)

    # Read UI control optVars - Het visibility states
    if pm.optionVar["relaxPin_NSUV"]:
        visState1 = True

    # Window
    window = pm.window(
        winRelax,
        height=relaxWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Relax UVs",
        width=largeWinX,
    )

    # Create layouts
    form1Relax = pm.formLayout()
    scrollRelax = pm.scrollLayout( childResizable=True )
    form2Relax = pm.formLayout( parent=scrollRelax )

    frameMainRelax = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Relax Options",
        parent=form2Relax
    )

    # Method radioBtnGrp
    if unfold3DLoaded == True: # Unfold3D plugin -check
        radGrpRelax = pm.radioButtonGrp(
            changeCommand=lambda *args: relaxSwitch(),
            columnWidth2=[largeCol1, largeCol2],
            numberOfRadioButtons=3,
            label="Method: ",
            labelArray3=["Unfold3D", "Legacy", "Quick"],
            vertical=True,
            parent=frameMainRelax,
            select=pm.optionVar["relaxMethod_NSUV"],
        )
    else: # Unfold3D not loaded
        radGrpRelax = pm.radioButtonGrp(
            changeCommand=lambda *args: relaxSwitch(),
            columnWidth2=[largeCol1, largeCol2],
            numberOfRadioButtons=2,
            label="Method: ",
            labelArray2=["Legacy", "Quick"],
            vertical=True,
            parent=frameMainRelax,
            select=pm.optionVar["relaxMethod_NSUV"],
        )


    ## Unfold 3D

    # Unfold 3D: Optimize frame and column
    frameOptiRelax = pm.frameLayout(
        label="Settings",
        parent=form2Relax
    )
    colSolver1Relax = pm.columnLayout(
        parent=frameOptiRelax
    )

    # Unfold3D: Solver elements
    sliderItrRelax = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        changeCommand=lambda *args: relaxOptVar(1),
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Iterations: ",
        maxValue=10,
        minValue=0,
        parent=colSolver1Relax,
        value=pm.optionVar["relaxItr_NSUV"],
    )
    sliderAngleRelax = pm.floatSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        changeCommand=lambda *args: relaxOptVar(2),
        field=True,
        fieldMaxValue=1.0,
        fieldMinValue=0.0,
        label="Surfangle: ",
        maxValue=1.0,
        minValue=0.0,
        parent=colSolver1Relax,
        value=pm.optionVar["relaxAngle_NSUV"],
    )
    sliderPowerRelax = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        changeCommand=lambda *args: relaxOptVar(3),
        field=True,
        fieldMaxValue=100,
        fieldMinValue=1,
        label="Power: ",
        maxValue=100,
        minValue=1,
        parent=colSolver1Relax,
        value=pm.optionVar["relaxPower_NSUV"],
    )
    cBoxBorderRelax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxOptVar(4),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Prevent self border intersections",
        parent=colSolver1Relax,
        value1=pm.optionVar["relaxBorder_NSUV"],
    )
    cBoxFlipsRelax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxOptVar(5),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Prevent triangle flips",
        parent=colSolver1Relax,
        value1=pm.optionVar["relaxFlips_NSUV"],
    )
    sep1Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver1Relax,
        visible=True,
    )

    # Unfold3D: Shell spacing frame and column
    frameSpacingRelax = pm.frameLayout(
        label="Shell Spacing",
        parent=form2Relax
    )
    colSpacingRelax = pm.columnLayout(
        parent=frameSpacingRelax,
    )

    sliderSizeRelax = pm.intSliderGrp(
        changeCommand=lambda *args: relaxOptVar(6, sliderSizeRelax),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        dragCommand=lambda *args: relaxOptVar(6, sliderSizeRelax),
        field=True,
        fieldStep=32,
        label="Map size (Pixels): ",
        max=8192,
        min=32,
        parent=colSpacingRelax,
        sliderStep=32,
        step=32,
        value=pm.optionVar["relaxSize_NSUV"]
    )
    sliderSpacingRelax = pm.intSliderGrp(
        changeCommand=lambda *args: relaxOptVar(7),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Shell padding (Pixels): ",
        maxValue=10,
        minValue=0,
        parent=colSpacingRelax,
        value=pm.optionVar["relaxSpacing_NSUV"],
    )
    sep2Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSpacingRelax,
        visible=True,
    )


    ## Legacy
    
    # Settings frame and column
    frameSettingsRelax = pm.frameLayout(
        label="Settings",
        parent=form2Relax,
    )
    colSettingsRelax = pm.columnLayout(
        parent=frameSettingsRelax,
    )

    # Settings elements
    radGrpWeightRelax = pm.radioButtonGrp(
        changeCommand = lambda *args: relaxOptVar(11),
        columnWidth2=[largeCol1, largeCol2+20],
        numberOfRadioButtons = 2,
        label = "Edge weights: ",
        labelArray2 = ["Uniform", "World space"],
        vertical = True,
        parent=colSettingsRelax,
        select=pm.optionVar["relaxEdge_NSUV"],
    )
    sliderMaxItrRelax = pm.intSliderGrp(
        changeCommand=lambda *args: relaxOptVar(12),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=10000,
        fieldMinValue=1,
        label="Max iterations: ",
        maxValue=10000,
        minValue=1,
        parent=colSettingsRelax,
        value=pm.optionVar["relaxMaxItr_NSUV"],
    )
    sep3Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSettingsRelax,
        visible=True,
    )

    # Pinning frame and column
    framePinningRelax = pm.frameLayout(
        label="Pinning",
        parent=form2Relax,
    )
    colPinningRelax = pm.columnLayout(
        parent=framePinningRelax,
    )

    # Pinning elements
    cBoxPin1Relax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxOptVar(8),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Pin UV shell border",
        parent=colPinningRelax,
        value1=pm.optionVar["relaxPinBorder_NSUV"],
    )
    cBoxPin2Relax = pm.checkBoxGrp(
        changeCommand=lambda *args: relaxOptVar(9, cBoxPin2Relax, radGrpPinRelax),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Pin UVs",
        parent=colPinningRelax,
        value1=pm.optionVar["relaxPin_NSUV"],
    )
    radGrpPinRelax = pm.radioButtonGrp(
        changeCommand=lambda *args: relaxOptVar(10),
        columnWidth2=[( largeCol1 + 15 ), ( largeCol2 + 55 )],
        enable=visState1,
        label1="Pin selected UVs",
        label2="Pin unselected UVs",
        label="",
        numberOfRadioButtons=2,
        parent=colPinningRelax,
        select=pm.optionVar["relaxPinType_NSUV"],
        vertical=True,
    )
    sep4Relax = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colPinningRelax,
        visible=True,
    )


    ## Quick

    textQuickRelax = pm.text(
        label="No options here - Things just get done!!",
        parent=form2Relax
    )

    # Buttons
    btnApplyCloseRelax = pm.button(
        command=lambda *args: core.relaxUVs(winRelax),
        label="Confirm",
        parent=form1Relax,
    )
    btnApplyRelax = pm.button(
        command=lambda *args: core.relaxUVs(),
        label="Apply",
        parent=form1Relax,
    )
    btnResetRelax = pm.button(
        command=lambda *args: relaxUIReset(),
        label="Reset",
        parent=form1Relax,
    )
    btnCloseRelax = pm.button(
        command=lambda *args: pm.deleteUI(winRelax),
        label="Close",
        parent=form1Relax,
    )

    # Layout frames
    pm.formLayout(
        form2Relax, edit=True,
        attachForm=[

            (frameMainRelax, "top", 0),
            (frameMainRelax, "left", 0),
            (frameMainRelax, "right", 0),

            (frameOptiRelax, "left", 0),
            (frameOptiRelax, "right", 0),

            (frameSpacingRelax, "left", 0),
            (frameSpacingRelax, "right", 0),
            
            (frameSettingsRelax, "left", 0),
            (frameSettingsRelax, "right", 0),

            (framePinningRelax, "left", 0),
            (framePinningRelax, "right", 0),

            (textQuickRelax, "left", 0),
            (textQuickRelax, "right", 0),
        ],
        attachControl=[
            (frameOptiRelax, "top", 10, frameMainRelax),

            (frameSpacingRelax, "top", 10, frameOptiRelax),
            
            (frameSettingsRelax, "top", 10, frameSpacingRelax),

            (framePinningRelax, "top", 0, frameSettingsRelax),

            (textQuickRelax, "top", 0, framePinningRelax),
        ],
        attachNone=[
            (frameOptiRelax, "bottom"),

            (frameSpacingRelax, "bottom"),

            (frameSettingsRelax, "bottom"),

            (framePinningRelax, "bottom"),

            (textQuickRelax, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1Relax, edit=True,
        attachForm=[
            (scrollRelax, "top", 0),
            (scrollRelax, "left", 0),
            (scrollRelax, "right", 0),

            (btnApplyCloseRelax, "left", 5),
            (btnApplyCloseRelax, "bottom", 5),
            (btnApplyRelax, "bottom", 5),
            (btnResetRelax, "bottom", 5),
            (btnCloseRelax, "right", 5),
            (btnCloseRelax, "bottom", 5),
        ],
        attachControl=[
            (scrollRelax, "bottom", 0, btnApplyCloseRelax),
        ],
        attachPosition=[
            (btnApplyCloseRelax, "right", 3, 25),
            (btnApplyRelax, "left", 2, 25),
            (btnApplyRelax, "right", 3, 50),
            (btnResetRelax, "right", 3, 75),
            (btnResetRelax, "left", 2, 50),
            (btnCloseRelax, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseRelax, "top"),
            (btnApplyRelax, "top"),
            (btnResetRelax, "top"),
            (btnCloseRelax, "top"),
        ],
    )

    # Hide inactive
    relaxSwitch()

    # Display the window
    pm.showWindow(window)


# UI for renaming a UV set
def renameSetUI(scrollListUVSet):

    # Get selected UV set
    selectedSet = scrollListUVSet.getSelectItem()

    # Check for window duplicate
    if pm.window( winRenameUVSet, exists=True ):
        pm.deleteUI(winRenameUVSet)

    # Main window
    window = pm.window(
        winRenameUVSet,
        height=renameSetWinY,
        maximizeButton=False,
        minimizeButton=False,
        sizeable=True,
        title="Rename UV Set",
    )

    # Layouts
    form1RenameUVSet = pm.formLayout()
    form2RenameUVSet = pm.formLayout( parent=form1RenameUVSet )
    frameRenameUVSet = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Rename UV Set Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2RenameUVSet,
        width=smallWinX,
    )
    colRenameUVSet = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        parent=frameRenameUVSet,
        rowSpacing=6,
    )
    rowRenameUVSet = pm.rowLayout(
        columnAttach=[1, "right", 0],
        columnWidth2=[renameCol1, renameCol1],
        numberOfColumns=2,
        parent=colRenameUVSet,
    )

    # Controls
    textRenameUVSet = pm.text(
        label="New UV set name: ",
        parent=rowRenameUVSet,
    )

    fieldRenameUVSet = pm.textField(
        alwaysInvokeEnterCommandOnReturn=True,
        annotation="Enter new UV set name",
        enterCommand=lambda *args: core.renameSet(scrollListUVSet, fieldRenameUVSet, winRenameUVSet),
        insertionPosition=0,
        parent=rowRenameUVSet,
        # text=pm.optionVar["copyNewUVSet_NSUV"],
        text=scrollListUVSet.getSelectItem()[0],
        width=renameCol2
    )    

    # Buttons
    btnOkRenameUVSet = pm.button(
        command=lambda *args: core.renameSet(scrollListUVSet, fieldRenameUVSet, winRenameUVSet),
        label="Rename",
        parent=form1RenameUVSet,
    )
    btnCancelRenameUVSet = pm.button(
        command=lambda *args: pm.deleteUI(winRenameUVSet),
        label="Close",
        parent=form1RenameUVSet,
    )
    
    # Layout frame
    pm.formLayout(
        form2RenameUVSet, edit=True,
        attachForm=[
            (frameRenameUVSet, "top", 0),
            (frameRenameUVSet, "left", 0),
            (frameRenameUVSet, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1RenameUVSet, edit=True,
        attachForm=[
            (form2RenameUVSet, "top", 0),
            (form2RenameUVSet, "left", 0),
            (form2RenameUVSet, "right", 0),
        
            (btnOkRenameUVSet, "left", 5),
            (btnOkRenameUVSet, "bottom", 5),
            (btnCancelRenameUVSet, "right", 5),
            (btnCancelRenameUVSet, "bottom", 5),
        ],
        attachControl=[
            (form2RenameUVSet, "bottom", 0, btnCancelRenameUVSet),
        ],
        attachPosition=[
            (btnOkRenameUVSet, "right", 2, 50),
            (btnCancelRenameUVSet, "left", 1, 50),
        ],
        attachNone=[
            (btnOkRenameUVSet, "top"),
            (btnCancelRenameUVSet, "top"),
        ],
    )

    pm.showWindow(window) # Display the window


# UI for changing working units
def workingUnitsUI():

    # Check for window duplicate
    if pm.window( winUnits, exists=True ):
        pm.deleteUI(winUnits)

    # Window
    window = pm.window(
        winUnits,
        height=workUnitsWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Set working units",
    )

    # Frame
    form1Units = pm.formLayout()
    form2Units = pm.formLayout( parent=form1Units )
    frameUnits = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Working Units Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2Units,
        width=smallWinX,
    )

    # Column
    colUnits = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameUnits,
    )

    # Label text
    textUnits = pm.text(
        label=("NOTE: Changing the working units HERE is the same\n"
           "as changing it under the Maya preferences! Also: The\n"
           "viewport grid will be affected by a new setting!"
        ),
        parent=colUnits,
    )

    # Units menu
    menuUnits = pm.optionMenuGrp(
        columnWidth=[1, 40],
        label="Linear: ",
        parent=colUnits,
    )
    pm.menuItem(label="millimeter")
    pm.menuItem(label="centimeter")
    pm.menuItem(label="meter")
    pm.menuItem(label="kilometer")
    pm.menuItem(label="inch")
    pm.menuItem(label="foot")
    pm.menuItem(label="yard")
    pm.menuItem(label="mile")

    # Get current linear unit and update the optionMenu
    menuVal = pm.currentUnit(query=True, linear=True)

    if menuVal == "mm":
        menuVal = "millimeter"
    elif menuVal == "cm":
        menuVal = "centimeter"
    elif menuVal == "m":
        menuVal = "meter"
    elif menuVal == "km":
        menuVal = "kilometer"
    elif menuVal == "in":
        menuVal = "inch"
    elif menuVal == "ft":
        menuVal = "foot"
    elif menuVal == "yd":
        menuVal = "yard"
    elif menuVal == "mi":
        menuVal = "mile"

    menuUnits.setValue(menuVal)


    # Buttons        
    btnOkUnits = pm.button(
        command=lambda *args: core.setUnits(menuUnits, winUnits),
        label="Okay",
        parent=form1Units,
    )
    btnCloseUnits = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Cancel",
        parent=form1Units,
    )
    
    # Layout frame
    pm.formLayout(
        form2Units, edit=True,
        attachForm=[
            (frameUnits, "top", 0),
            (frameUnits, "left", 0),
            (frameUnits, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1Units, edit=True,
        attachForm=[
            (form2Units, "top", 0),
            (form2Units, "left", 0),
            (form2Units, "right", 0),
        
            (btnOkUnits, "left", 5),
            (btnOkUnits, "bottom", 5),
            (btnCloseUnits, "right", 5),
            (btnCloseUnits, "bottom", 5),
        ],
        attachControl=[
            (form2Units, "bottom", 0, btnCloseUnits),
        ],
        attachPosition=[
            (btnOkUnits, "right", 2, 50),
            (btnCloseUnits, "left", 1, 50),
        ],
        attachNone=[
            (btnOkUnits, "top"),
            (btnCloseUnits, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)


# UI for the UV snapshot window
def snapshotUI():

    # Vars
    btn1SS, btn2SS, btn3SS, btn4SS, btn5SS, btn6SS, menuFormatSS, \
    menuRangeSS, rad1SS, rad2SS, rad3SS, rad4SS, rad5SS, rad6SS = (None,)*14
    menuLabel1 = "Normal (0 to 1)"
    menuLabel2 = "User-specified"
    ssSpacing = 120

    # File path browser
    def ssBrowse():

        cleanPath = ""

        # Run file browser
        unicodePath = pm.fileDialog2(
            caption="Set output path",
            dialogStyle=1,
            fileMode=0,
            startingDirectory=pm.optionVar["shotUVpath_NSUV"]
        )

        # Because fileDialog2 returns such a stupid data type, fix it!
        if unicodePath != "" and unicodePath != None:
            cleanPath = str(unicodePath[0])

        # Update the file path -control
        if cleanPath != "" and cleanPath != None:
            fieldSS.setText(cleanPath)

            # Update the optVar
            pm.optionVar["shotUVpath_NSUV"] = cleanPath

    # Range toggle
    def ssRangeToggle():

        # Read menu value and update optVar
        range = pm.optionVar["shotUVrange_NSUV"] = menuRangeSS.getSelect()

        # Toggle UI parts
        if range != 1:
            btn1SS.setEnable(True)
            btn2SS.setEnable(True)
            btn3SS.setEnable(True)
            btn4SS.setEnable(True)
            btn5SS.setEnable(True)
            btn6SS.setEnable(True)
            rad1SS.setEnable(True)
            rad2SS.setEnable(True)
            rad3SS.setEnable(True)
            rad4SS.setEnable(True)
            rad5SS.setEnable(True)
            rad6SS.setEnable(True)

        else:
            btn1SS.setEnable(False)
            btn2SS.setEnable(False)
            btn3SS.setEnable(False)
            btn4SS.setEnable(False)
            btn5SS.setEnable(False)
            btn6SS.setEnable(False)
            rad1SS.setEnable(False)
            rad2SS.setEnable(False)
            rad3SS.setEnable(False)
            rad4SS.setEnable(False)
            rad5SS.setEnable(False)
            rad6SS.setEnable(False)

    # "Reset to default"
    def ssReset():

        # Get root dir, set as default
        path = pm.workspace(query=True, rootDirectory=True) + "images/outUV"
        pm.optionVar["shotUVpath_NSUV"] = path

        # Switch front slashes for back slashes in the path optVar if OS = windows
        if pm.about(ntOS=True) == True:
            pm.optionVar["shotUVpath_NSUV"] = path = path.replace("/", "\\")

        # Reset UI controls to defaults
        cBoxAliasSS.setValue1(1)
        fieldSS.setText(path)
        menuFormatSS.setSelect(1)
        sliderColorSS.setRgbValue([1.0, 1.0, 1.0])
        sliderXSS.setValue(1024)
        sliderYSS.setValue(1024)
        cBoxMultiTileSS.setValue1(False)
        rowTileSS.setVisible(False)
        fieldTileUSS.setValue1(1)
        fieldTileVSS.setValue1(1)
        menuRangeSS.setValue(menuLabel1)

        # Reset optVars
        pm.optionVar["shotUVaa_NSUV"] = 0
        pm.optionVar["shotUVratio_NSUV"] = 1
        pm.optionVar["shotUVformat_NSUV"] = "Maya IFF"
        pm.optionVar["shotUVxSize_NSUV"] = 1024
        pm.optionVar["shotUVySize_NSUV"] = 1024
        pm.optionVar["shotUVcolor_NSUV"] = [ 1.0, 1.0, 1.0 ]
        pm.optionVar["snapshotMultiTile_NSUV"] = False
        pm.optionVar["snapshotGridUVal_NSUV"] = 1
        pm.optionVar["snapshotGridVVal_NSUV"] = 1
        pm.optionVar["shotUVrange_NSUV"] = 1

        # Toggle visibility
        ssRangeToggle()

    # Update optVar
    def ssOptVar(varType, control=None, radBtn=None):

        if varType == 1:
            pm.optionVar["shotUVpath_NSUV"] = fieldSS.getText()

        elif varType == 2:

            # Query slider, round to power of two
            newVal = sliderXSS.getValue()
            newVal = core.powerOfTwo(newVal)
            sliderXSS.setValue(newVal)

            pm.optionVar["shotUVxSize_NSUV"] = sliderXSS.getValue()

        elif varType == 3:

            # Query slider, round to power of two
            newVal = sliderYSS.getValue()
            newVal = core.powerOfTwo(newVal)
            sliderYSS.setValue(newVal)

            pm.optionVar["shotUVySize_NSUV"] = sliderYSS.getValue()

        elif varType == 4:
            pm.optionVar["shotUVcolor_NSUV"] = sliderColorSS.getRgbValue()

        elif varType == 5:
            pm.optionVar["shotUVaa_NSUV"] = cBoxAliasSS.getValue1()

        elif varType == 6:
            pm.optionVar["shotUVformat_NSUV"] = menuFormatSS.getValue()

        elif varType == 8:
            if radBtn == 1:
                pm.optionVar["shotUVtype_NSUV"] = 1
            elif radBtn == 2:
                pm.optionVar["shotUVtype_NSUV"] = 2
            elif radBtn == 3:
                pm.optionVar["shotUVtype_NSUV"] = 3
            elif radBtn == 4:
                pm.optionVar["shotUVtype_NSUV"] = 4
            elif radBtn == 5:
                pm.optionVar["shotUVtype_NSUV"] = 5
            elif radBtn == 6:
                pm.optionVar["shotUVtype_NSUV"] = 6
            else:
                pm.error("Incorrect radBtn sent to ss")

            control.setSelect()

        elif varType == 9:
            pm.optionVar["snapshotMultiTile_NSUV"] = mode = cBoxMultiTileSS.getValue1()
            rowTileSS.setVisible(mode)

            if mode == True:
                btnOkSS.setCommand(lambda *args: core.ssMultiShot(winSS))
                btnApplySS.setCommand(lambda *args: core.ssMultiShot())
            else:
                btnOkSS.setCommand(lambda *args: core.ssTakeShot(winSS))
                btnApplySS.setCommand(lambda *args: core.ssTakeShot())

        elif varType == 10:
            if fieldTileUSS.getValue1() >= 11:
                fieldTileUSS.setValue1(10)
                pm.optionVar["snapshotGridUVal_NSUV"] = 10
                core.errorCode(17) # Maximum U-value exceeded

            else: pm.optionVar["snapshotGridUVal_NSUV"] = fieldTileUSS.getValue1()

        elif varType == 11:
            if fieldTileUSS.getValue1() >= 1001:
                fieldTileUSS.setValue1(1000)
                pm.optionVar["snapshotGridVVal_NSUV"] = 1000
                core.errorCode(18) # Maximum V-value exceeded

            else: pm.optionVar["snapshotGridVVal_NSUV"] = fieldTileVSS.getValue1()

        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.snapshotUI.ssOptVar()")


    # Check for window duplicate
    if pm.window( winSS, exists=True ):
        pm.deleteUI(winSS)

    # Create window
    window = pm.window(
        winSS,
        height=snapshotWinY,
        maximizeButton=True,
        minimizeButton=True,
        resizeToFitChildren=True,
        sizeable=True,
        title="Snapshot UVs",
        width=largeWinX
    )

    # Create layouts
    form1SS = pm.formLayout()
    scrollSS = pm.scrollLayout( childResizable=True )
    form2SS = pm.formLayout( parent=scrollSS )

    frame1SS = pm.frameLayout(
        collapsable=False,
        label="Snapshot Options"
    )
    col1SS = pm.columnLayout(parent=frame1SS)

    # File path field
    fieldSS = pm.textFieldButtonGrp(
        buttonCommand=lambda *args: ssBrowse(),
        buttonLabel="Browse...",
        changeCommand=lambda *args: ssOptVar(1),
        columnWidth=( [1, ssSpacing], [3, 65] ),
        label="Path / File name: ",
        text=pm.optionVar["shotUVpath_NSUV"],
    )

    # Size sliders
    sliderXSS = pm.intSliderGrp(
        changeCommand=lambda *args: ssOptVar(2),
        columnWidth=[1, ssSpacing],
        dragCommand=lambda *args: ssOptVar(2),
        field=True,
        fieldStep=32,
        label="Size X (px): ",
        max=8192,
        min=32,
        sliderStep=32,
        step=32,
        value=pm.optionVar["shotUVxSize_NSUV"]
    )
    sliderYSS = pm.intSliderGrp(
        changeCommand=lambda *args: ssOptVar(3),
        columnWidth=[1, ssSpacing],
        dragCommand=lambda *args: ssOptVar(3),
        field=True,
        fieldStep=32,
        label="Size Y (px): ",
        max=8192,
        min=32,
        sliderStep=32,
        step=32,
        value=pm.optionVar["shotUVySize_NSUV"]
    )

    # Edge color slider
    redV, greenV, blueV = pm.optionVar["shotUVcolor_NSUV"]
    sliderColorSS = pm.colorSliderGrp(
        changeCommand=lambda *args: ssOptVar(4),
        columnWidth=[1, ssSpacing],
        label="Edge color: ",
        rgbValue=[redV, greenV, blueV]
    )

    # Anti-aliasing checkbox
    cBoxAliasSS = pm.checkBoxGrp(
        changeCommand=lambda *args: ssOptVar(5),
        columnWidth=[1, ssSpacing],
        label1="Anti-alias lines",
        label="",
        value1=pm.optionVar["shotUVaa_NSUV"]
    )

    # File format menu
    menuFormatSS = pm.optionMenuGrp(
        changeCommand=lambda *args: ssOptVar(6),
        columnWidth=[1, ssSpacing],
        label="Image format: ",
        parent=col1SS
    )

    # File format list on MacOS
    if pm.about(macOS=True):
        pm.menuItem(label="Maya IFF")
        pm.menuItem(label="JPEG")
        pm.menuItem(label="MacPaint")
        pm.menuItem(label="PSD")
        pm.menuItem(label="PNG")
        pm.menuItem(label="Quickdraw")
        pm.menuItem(label="Quickdraw Image")
        pm.menuItem(label="SGI")
        pm.menuItem(label="TGA")
        pm.menuItem(label="TIFF")
        pm.menuItem(label="BMP")

    else: # Windows

        # Query available image formats
        imfList = pm.imfPlugins(query=True)

        # Maya IFF is always available
        pm.menuItem(label="Maya IFF")

        # Create menuItem objects for all items in list
        counter = 0
        while counter < len(imfList):

            # Get keyword
            imfKey = pm.imfPlugins( imfList[counter], query=True, key=True )

            # Check for support types and make sure imfKey ain't "maya"
            wSupport = pm.imfPlugins(imfKey, query=True, writeSupport=True)
            mfSupport = pm.imfPlugins(imfKey, query=True, multiFrameSupport=True)

            if wSupport == True and mfSupport == False and imfKey != "maya":
                pm.menuItem( label=imfList[counter] ) # Create menuItem

            # Up the counter for the while loop
            counter += 1

        pm.setParent('..') # Set default parent to one step up

    # Select menuItem
    menuFormatSS.setValue(pm.optionVar["shotUVformat_NSUV"])
    formatIndex = menuFormatSS.getSelect()

    cBoxMultiTileSS = pm.checkBoxGrp(
        changeCommand=lambda *args: ssOptVar(9),
        columnWidth=[1, ssSpacing],
        label="Multi-tile (UDIM): ",
        label1="",
        value1=pm.optionVar["snapshotMultiTile_NSUV"],
    )

    rowTileSS = pm.rowLayout(
        columnAttach2=["left", "left"],
        numberOfColumns=2,
        visible=pm.optionVar["snapshotMultiTile_NSUV"],
    )

    fieldTileUSS = pm.intFieldGrp(
        changeCommand=lambda *args: ssOptVar(10),
        columnWidth=[1, ssSpacing],
        label="Tiles U: ",
        parent=rowTileSS,
        value1=pm.optionVar["snapshotGridUVal_NSUV"],
    )
    fieldTileVSS = pm.intFieldGrp(
        changeCommand=lambda *args: ssOptVar(11),
        columnAlign2=["left", "left"],
        columnWidth=[1, 12],
        label="V:",
        parent=rowTileSS,
        value1=pm.optionVar["snapshotGridVVal_NSUV"],
    )

    pm.setParent('..') # Set default parent to one step up

    # Layouts for the range section
    frame5SS = pm.frameLayout(
        collapsable=True,
        label="Coverage",
        parent=form2SS
    )
    col2SS = pm.columnLayout(parent=frame5SS)

    # Range toggle menu
    if pm.optionVar["shotUVrange_NSUV"] == 1:
        rangeSelVar = str(menuLabel1)
    else:
        rangeSelVar = str(menuLabel2)

    menuRangeSS = pm.optionMenuGrp(
        changeCommand=lambda *args: ssRangeToggle(),
        columnWidth=[1, ssSpacing],
        label="UV Range: ",
        parent=col2SS
    )

    # Create the menu items, select menuItem
    pm.menuItem(label=menuLabel1)
    pm.menuItem(label=menuLabel2)

    # formLayout for the range section
    form3SS = pm.formLayout(parent=col2SS)

    # Range buttons
    btn1SS = pm.iconTextButton(
        annotation="Lying rectangle",
        command=lambda *args: ssOptVar(8, rad1SS, 1),
        image=iconDict["uvRangeA"],
        label="Lying rectangle",
    )
    btn2SS = pm.iconTextButton(
        annotation="Standing rectangle",
        command=lambda *args: ssOptVar(8, rad2SS, 2),
        image=iconDict["uvRangeB"],
        label="Standing rectangle",
    )
    btn3SS = pm.iconTextButton(
        annotation="-1 to 1",
        command=lambda *args: ssOptVar(8, rad3SS, 3),
        image=iconDict["uvRangeC"],
        label="-1 to 1",
    )
    btn4SS = pm.iconTextButton(
        annotation="Second quadrant",
        command=lambda *args: ssOptVar(8, rad4SS, 4),
        image=iconDict["uvRangeD"],
        label="Second quadrant",
    )
    btn5SS = pm.iconTextButton(
        annotation="Third quadrant",
        command=lambda *args: ssOptVar(8, rad5SS, 5),
        image=iconDict["uvRangeE"],
        label="Third quadrant",
    )
    btn6SS = pm.iconTextButton(
        annotation="Fourth quadrant",
        command=lambda *args: ssOptVar(8, rad6SS, 6),
        image=iconDict["uvRangeF"],
        label="Fourth quadrant",
    )

    # Radio collection and radio buttons
    radColSS = pm.radioCollection(
        parent=form3SS
    )
    rad1SS = pm.radioButton(label="A", changeCommand=lambda *args: ssOptVar(8, rad1SS, 1))
    rad2SS = pm.radioButton(label="B", changeCommand=lambda *args: ssOptVar(8, rad2SS, 2))
    rad3SS = pm.radioButton(label="C", changeCommand=lambda *args: ssOptVar(8, rad3SS, 3))
    rad4SS = pm.radioButton(label="D", changeCommand=lambda *args: ssOptVar(8, rad4SS, 4))
    rad5SS = pm.radioButton(label="E", changeCommand=lambda *args: ssOptVar(8, rad5SS, 5))
    rad6SS = pm.radioButton(label="F", changeCommand=lambda *args: ssOptVar(8, rad6SS, 6))

    # Edit the radio collection and select item
    if pm.optionVar["shotUVtype_NSUV"] == 1:
        radColSS.setSelect(rad1SS)
    elif pm.optionVar["shotUVtype_NSUV"] == 2:
        radColSS.setSelect(rad2SS)
    elif pm.optionVar["shotUVtype_NSUV"] == 3:
        radColSS.setSelect(rad3SS)
    elif pm.optionVar["shotUVtype_NSUV"] == 4:
        radColSS.setSelect(rad4SS)
    elif pm.optionVar["shotUVtype_NSUV"] == 5:
        radColSS.setSelect(rad5SS)
    elif pm.optionVar["shotUVtype_NSUV"] == 6:
        radColSS.setSelect(rad6SS)

    # Layout elements in the range formLayout
    pm.formLayout(
        form3SS, edit=True,
        attachForm=[
            (btn1SS, "top", 5),
            (btn1SS, "left", ssSpacing),
            (rad1SS, "top", btnTop),

            (btn2SS, "top", 5),
            (rad2SS, "top", btnTop),

            (btn3SS, "top", 5),
            (rad3SS, "top", btnTop),

            (btn4SS, "left", ssSpacing),
        ],
        attachControl=[
            (rad1SS, "left", radLeft, btn1SS),

            (btn2SS, "left", btnLeft, rad1SS),
            (rad2SS, "left", radLeft, btn2SS),

            (btn3SS, "left", btnLeft, rad2SS),
            (rad3SS, "left", radLeft, btn3SS),

            (btn4SS, "top", btnTop, btn1SS),
            (rad4SS, "top", radTop+3, rad1SS),
            (rad4SS, "left", radLeft, btn4SS),

            (btn5SS, "top", btnTop, btn2SS),
            (btn5SS, "left", btnLeft, rad4SS),
            (rad5SS, "top", radTop+3, rad2SS),
            (rad5SS, "left", radLeft, btn5SS),

            (btn6SS, "top", btnTop, btn3SS),
            (btn6SS, "left", btnLeft, rad5SS),
            (rad6SS, "top", radTop+3, rad3SS),
            (rad6SS, "left", radLeft, btn6SS),
        ]
    )

    # Separator
    sep1 = pm.separator(
        horizontal=True,
        style="none"
    )

    # Buttons
    btnOkSS = pm.button(
        command=lambda *args: core.ssTakeShot(winSS),
        label="Ok",
        parent=form1SS
    )
    btnApplySS = pm.button(
        command=lambda *args: core.ssTakeShot(),
        label="Apply",
        parent=form1SS
    )
    btnDefaultSS = pm.button(
        command=lambda *args: ssReset(),
        label="Reset",
        parent=form1SS
    )
    btnCloseSS = pm.button(
        command=lambda *args: pm.deleteUI(winSS),
        label="Close",
        parent=form1SS
    )

    # Layout section frames
    pm.formLayout(
        form2SS, edit=True,
        attachForm=[
            (frame1SS, "top", 0),
            (frame1SS, "right", 0),
            (frame1SS, "left", 0),

            (frame5SS, "right", 0),
            (frame5SS, "left", 0),
            (frame5SS, "bottom", 0),
        ],
        attachControl=[
            (frame5SS, "top", 10, frame1SS),
        ],
        attachNone=[
            (frame1SS, "bottom")
        ]
    )

    # Layout main form
    pm.formLayout(
        form1SS, edit=True,
        attachForm=[
            (scrollSS, "top", 0),
            (scrollSS, "right", 0),
            (scrollSS, "left", 0),

            (btnOkSS, "left", 5),
            (btnOkSS, "bottom", 5),
            (btnApplySS, "bottom", 5),
            (btnDefaultSS, "bottom", 5),
            (btnCloseSS, "right", 5),
            (btnCloseSS, "bottom", 5),
        ],
        attachControl=[
            (scrollSS, "bottom", 5, btnOkSS),
        ],
        attachPosition=[
            (btnOkSS, "right", 3, 25),
            (btnApplySS, "right", 3, 50),
            (btnApplySS, "left", 2, 25),
            (btnDefaultSS, "right", 3, 75),
            (btnDefaultSS, "left", 2, 50),
            (btnCloseSS, "left", 2, 75),
        ],
        attachNone=[
            (btnOkSS, "top"),
            (btnDefaultSS, "top"),
            (btnCloseSS, "top"),
        ]
    )

    # In case a plugin has been unloaded, reducing the number of FF...
    if formatIndex > menuFormatSS.getNumberOfItems():

        # ...just pick the file format at the end of the list
        formatIndex = menuFormatSS.getNumberOfItems()

    # Edit the file format menu
    menuFormatSS.setSelect(formatIndex)

    # Edit the range menu and button commands
    menuRangeSS.setSelect(pm.optionVar["shotUVrange_NSUV"])
    ssRangeToggle() # Toggle visibility
    ssOptVar(9) # Updates btn cmds

    # Display the window
    pm.showWindow(window)


# UI for changing the straighten UVs options
def strUVsUI():

    # Reset UI
    def strUVsReset():
        pm.optionVar["strUVsAngle_NSUV"] = 30
        pm.optionVar["strUVsType_NSUV"] = 0
        radGrpStrUVs.setSelect(0)
        sliderStrUVs.setValue(30)

    # Update optVar
    def strUVsOptVar(varType):

        if varType == 0: pm.optionVar["strUVsAngle_NSUV"] = sliderStrUVs.getValue()-1
        elif varType == 1: pm.optionVar["strUVsType_NSUV"] = radGrpStrUVs.getSelect()-1


    # Check for window duplicate
    if pm.window( winStrUVs, exists=True ):
        pm.deleteUI(winStrUVs)

    # Window
    window = pm.window(
        winStrUVs,
        height=strUVWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Straighten UVs",
    )

    # Layouts
    form1StrUVs = pm.formLayout()
    form2StrUVs = pm.formLayout( parent=form1StrUVs )
    frameStrUVs = pm.frameLayout(
        collapsable=False,
        collapse=False,
        # height=strUVWinY,
        label="Straighten UVs Options",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2StrUVs,
        width=smallWinX,
    )
    colStrUVs = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameStrUVs,
    )
    textStrUVs = pm.text(
        label="A higher value results in more aggressive\nstraightening of the edge loops in the selection.")

    # Slider
    sliderStrUVs = pm.floatSliderGrp(
        changeCommand=lambda *args: strUVsOptVar(0),
        columnAlign=[1, "right"],
        columnWidth3=[smallCol1, 70, smallCol1],
        field=True,
        fieldMaxValue=44.99,
        fieldMinValue=0.01,
        label="Angle value: ",
        maxValue=44.99,
        minValue=0.01,
        parent=colStrUVs,
        precision=2,
        sliderStep=0.01,
        value=pm.optionVar["strUVsAngle_NSUV"]
    )

    # Radio collection and radio buttons
    radGrpStrUVs = pm.radioButtonGrp(
        changeCommand=lambda *args: strUVsOptVar(1),
        columnAlign=[1, "right"],
        columnWidth2=[smallCol1, smallCol2],
        label1="U and V",
        label2="U only",
        label3="V only",
        label="Straighten: ",
        numberOfRadioButtons=3,
        parent=colStrUVs,
        select=pm.optionVar["strUVsType_NSUV"],
        vertical=True,
    )

    # Buttons   
    btnOkStrUVs = pm.button(
        command=lambda *args: core.strUVs(),
        label="Straighten",
        parent=form1StrUVs,
    )
    btnResetStrUVs = pm.button(
        command=lambda *args: strUVsReset(),
        label="Reset",
        parent=form1StrUVs,
    )
    btnCloseStrUVs = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1StrUVs,
    )
    
    # Layout frame
    pm.formLayout(
        form2StrUVs, edit=True,
        attachForm=[
            (frameStrUVs, "top", 0),
            (frameStrUVs, "left", 0),
            (frameStrUVs, "right", 0),
        ]
    )
    
    # Layout button form
    pm.formLayout(
        form1StrUVs, edit=True,
        attachForm=[
            (form2StrUVs, "top", 0),
            (form2StrUVs, "left", 0),
            (form2StrUVs, "right", 0),

            (btnOkStrUVs, "left", 5),
            (btnOkStrUVs, "bottom", 5),
            (btnResetStrUVs, "bottom", 5),
            (btnCloseStrUVs, "right", 5),
            (btnCloseStrUVs, "bottom", 5),
        ],
        attachControl=[
            (form2StrUVs, "bottom", 0, btnCloseStrUVs),
        ],
        attachPosition=[
            (btnOkStrUVs, "right", 3, 33),
            (btnResetStrUVs, "left", 2, 33),
            (btnResetStrUVs, "right", 3, 66),
            (btnCloseStrUVs, "left", 2, 66),
        ],
        attachNone=[
            (btnOkStrUVs, "top"),
            (btnResetStrUVs, "top"),
            (btnCloseStrUVs, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)

    
# UI for reporting a bug or requesting a feature
def submitUI():

    # Vars
    margin = 10

    # Check for window duplicate
    if pm.window( winSubmit, exists=True ):
        pm.deleteUI(winSubmit)

    # Window
    window = pm.window(
        winSubmit,
        height=submitWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Submit Feedback",
        width=largeWinX
    )
    
    # Main column
    colMainSubmit = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
    )
    
    # Submission info
    frameSubmit = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Before Submitting",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainSubmit,
        width=largeWinX,
    )
    colSubmit = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameSubmit,
        width=frameX,
    )
    text1Submit = pm.text(
        label="Before submitting a bug report or a feature request, ask yourself these following questions:",
        font="boldLabelFont", 
        parent=colSubmit,
        width=frameX,
        wordWrap=True,
    )
    text2Submit = pm.text(
        label="-Have I read the manual?\n"\
"-Have I read the FAQ?\n"\
"-Have I made sure that my request or bug report haven't been posted already?\n"\
"-Have I made sure that this isn't a bug with Maya?\n"\
"-Have I made sure that my version of Maya is officially supported by NSUV?",
        parent=colSubmit,
        width=frameX,
        wordWrap=True,
    )
    text3Submit = pm.text(
        label="Also, before submitting a bug report, make sure you go to the Script Editor -> History and turn "\
"on the top four checkboxes. Restart Maya and run the broken script/tool again and post the error code and row "\
"number in the report.",
        font="boldLabelFont", 
        parent=colSubmit,
        width=frameX,
        wordWrap=True,
    )

    # Submission info
    frameSubmit2 = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Submission Form",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainSubmit,
        width=largeWinX,
    )
    colSubmit = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameSubmit2,
        width=frameX,
    )
    text4Submit = pm.text(
        label="Submitting a bug or feature request is done via the NSUV Creative Crash page. "\
"An account on Creative Crash is required. If you have none, you can send the report directly "\
"to me at martin.dahlin@live.com\n",
        font="boldLabelFont", 
        parent=colSubmit,
        width=frameX,
        wordWrap=True,
    )
    btnSubmit = pm.button(
        command=lambda *args: pm.launch(web="http://www.creativecrash.com/maya/script/nightshade-uv-editor"),
        label="Go to NSUV on Creative Crash",
        parent=colSubmit,
        width=(largeWinX/2),
    )
    
    # Button
    btnClose = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainSubmit,
        width=largeWinX,
    )
    
    pm.showWindow(window)
    
    
# UI for the Tip of the Day -popups
def totdUI():

    # Vars
    sliderMatchTol = "NSUV_matchTolSlider"

    # Internal method for showing the prev/next tip of the day
    def tipSwitch(dir, img, txt):
        count = pm.optionVar["totdCounter_NSUV"]

        # Modify counter
        if dir == 1: count += 1 # Next
        else: count -= 1 # Prev

        # Cycle around
        if count == len(totdImageDict):
            count = 1
        elif count == 0:
            count = len(totdImageDict) - 1

        # Modify UI and update optVar
        pm.optionVar["totdCounter_NSUV"] = count
        img.setImage(totdImageDict[count])
        txt.setText(totdTextDict[count])


    # Updates the display on startup optVar
    def totdOptVar():
        pm.optionVar["totd_NSUV"] = btnStartupTotd.getValue1()


    # Check for window duplicate
    if pm.window( winTotd, exists=True ):
        pm.deleteUI(winTotd)

    # Window
    window = pm.window(
        winTotd,
        height=totdWinY,
        minimizeButton=False,
        maximizeButton=False,
        resizeToFitChildren=True,
        sizeable=True,
        title="Tip of the Day",
    )

    # Layouts
    form1Totd = pm.formLayout()
    form2Totd = pm.formLayout( parent=form1Totd )
    frameTotd = pm.frameLayout(
        collapsable=False,
        collapse=False,
        label="Did you know?",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=form2Totd,
        width=smallWinX,
    )
    colTotd = pm.columnLayout(
        adjustableColumn=True,
        columnAlign="left",
        rowSpacing=6,
        parent=frameTotd,
    )

    # Totd content
    imageTotd = pm.image(
        image=totdImageDict[pm.optionVar["totdCounter_NSUV"]],
        parent=colTotd,
    )
    textTotd = pm.scrollField(
        editable=False,
        height=116,
        numberOfLines=7,
        parent=colTotd,
        text=totdTextDict[pm.optionVar["totdCounter_NSUV"]],
        wordWrap=True,
    )

    # Checkbox   
    btnStartupTotd = pm.checkBoxGrp(
        adjustableColumn2=2,
        annotation="Show the 'Tip of the Day' messages when starting NSUV",
        changeCommand=lambda *args: totdOptVar(),
        columnWidth2=[0, smallWinX],
        label="",
        label1="Show tips at startup*",
        parent=colTotd,
        value1=pm.optionVar["totd_NSUV"],
    )    
    textStartupTotd = pm.text(
        label="*Can be turned on again via the NSUV-menu\n",
        parent=colTotd,
    )

    # Buttons
    btnPrevTotd = pm.button(
        command=lambda *args: tipSwitch(0, imageTotd, textTotd),
        label="Previous tip",
        parent=form1Totd,
    )
    btnNextTotd = pm.button(
        command=lambda *args: tipSwitch(1, imageTotd, textTotd),
        label="Next tip",
        parent=form1Totd,
    )
    btnCloseTotd = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=form1Totd,
    )
    
    # Layout frame
    pm.formLayout(
        form2Totd, edit=True,
        attachForm=[
            (frameTotd, "top", 0),
            (frameTotd, "left", 0),
            (frameTotd, "right", 0),
        ]
    )
    
    # Layout main form
    pm.formLayout(
        form1Totd, edit=True,
        attachForm=[
            (form2Totd, "top", 0),
            (form2Totd, "left", 0),
            (form2Totd, "right", 0),
        
            (btnPrevTotd, "left", 5),
            (btnPrevTotd, "bottom", 5),
            (btnNextTotd, "bottom", 5),
            (btnCloseTotd, "right", 5),
            (btnCloseTotd, "bottom", 5),
        ],
        attachControl=[
            (form2Totd, "bottom", 0, btnCloseTotd),
        ],
        attachPosition=[
            (btnPrevTotd, "right", 3, 33),
            (btnNextTotd, "left", 2, 33),
            (btnNextTotd, "right", 3, 66),
            (btnCloseTotd, "left", 2, 66),
        ],
        attachNone=[
            (btnPrevTotd, "top"),
            (btnNextTotd, "top"),
            (btnCloseTotd, "top"),
        ],
    )

    # Display the window
    pm.showWindow(window)    
    

# Tips and Tricks UI
def tricksUI():

    # Check for window duplicate
    if pm.window( winTricks, exists=True ):
        pm.deleteUI(winTricks)

    # Window
    window = pm.window(
        winTricks,
        height=largeWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Tips and Tricks",
        width=largeWinX
    )
        
    # Main column
    colMainTricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
    )
    
    # Title image
    imageTricks = pm.image(
        image=iconDict["tricks"],
        parent=colMainTricks,
    )

    scrollTricks = pm.scrollLayout(
        childResizable=True,
        height=largeWinY,
        width=largeWinX,
    )
    
    # Secondary column
    colSecTricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=frameX,
    )    
    
    # Intro
    frame1Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Introduction",
        parent=colSecTricks,
    )
    col1Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame1Tricks
    )
    text1Workflow = pm.scrollField(
        text="Welcome to the Tips and Tricks -section of NSUV. Here I will go through some"\
" additional topics in UV Mapping not covered by the basic section. If you are new at UV "\
" Mapping, you should check out the Basic Workflow section first.\n",
        editable=False,
        height=103,
        parent=col1Tricks,
        width=frameX,
        wordWrap=True,
    )

    # Approaches
    frame2Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Different Approaches To UV Mapping ",
        parent=colSecTricks,
    )
    col2Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame2Tricks
    )
    text2Workflow = pm.scrollField(
        text="There are many ways that you can map a 3D object. It is all about the balancing"\
" act between optimization and minimizing stretching/pinching. Rarely you want one of these"\
" extremes, but sometimes it can be justified. Here I will cover the most common UV mapping"\
" setups, so that you can take on any kind of 3D that you chose to work with."\
" \n\nOptimized UV mapping:\n"\
"One of these extremes is the heavily optimized UV map - used exclusively for realtime"\
" graphics. The end-goal is to have as much coverage you can on map that is as small as"\
" possible. Heavily optimized UV maps are most common when working with mobile/lowpoly"\
" graphics where you have heavy limitations on your assets - but even for current gen graphics"\
" you need to keep in mind that loading texture maps into the graphics memory is heavy work."\
" The texel density will vary a lot and stretching and pinching will be created on purpose"\
" where it's needed. Every shell that can be mirrored (along a plane or radially) can - and"\
" sometimes should - be stacked on top of each other. Furthermore, shells are oriented"\
" straight along U/V, and those with odd shapes are cut up into smaller parts. Also do not be"\
" afraid of straightening border shells so that you can pack shells tighter together."\
" Additionally for mobile graphics, consider pushing the UVs of a shell into a line segment if"\
" you only need information in one direction (like a gradient) or even a point (if you only"\
" need a color)."\
" \n\nTechnical UV Mapping:\n"\
"On the other end of the spectrum you have UV mapping for technical models. If the model is"\
" going to be used for pre-rendered graphics, technical demonstrations or for promo material"\
" - then this is probably the discipline you need to adopt. Pixel aspect ratio is very"\
" important - while texture space and optimization is not. Here it is important that all your"\
" shells have the same Texel Density and that you eradicate stretching and pinching the best"\
" you can. In the VFX industry it is also common practise to use multiple large UV maps for"\
" different parts of the mesh (known as multi-tile UV mapping). Far from all pre-rendered"\
" art will require a UV map though, as it is more common to use procedual 3d textures for the"\
" different materials. So always check with your art director/art lead to make sure that the"\
" UV map is actually necessary."\
" \n\nContinuous UV mapping:\n"\
"Located somewhere in-between the previous two extremes. When working with more high-detail"\
" organic models, for example a character or a tree, the focus should be on reducing the"\
" number of seams and to preserve the Texel Density across the shells. Heavy optimzations"\
" are pretty much impossible as the layouting will be harder due to all the oddly-shaped UV"\
" itshells - but try not to neglect optimizing alltogether.\n",
        editable=False,
        height=809,
        parent=col2Tricks,
        width=frameX,
        wordWrap=True,
    )
    
    # Optimization
    frame3Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Optimization",
        parent=colSecTricks,
    )
    col3Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame3Tricks
    )
    text3Workflow = pm.scrollField(
        text="Unless you are mapping for technical models or VFX assets, you need to be"\
" thinking about optimization. The first step you can take here is to consider what parts of"\
" your model are going to be visible to the camera, how often, and at what distances. Start by"\
" setting a uniform TD to all UV shells and then scale up and scale down according to those"\
" factors. For example if you are working on a FPS weapon with iron sights then the scope part"\
" should have the highest TD, and the right and front side of the gun the lowest.\n\n"\
" Step two in the optimization process is something called symmetry-mapping. You stack shells"\
" on top of each other that are mirrored either over a plane, or radially. Here you need to be"\
" careful though as you need to consider what kind of ambient occlusion shadows the affected"\
" shells will recieve (if you use AO that is). Also if you are going to have some form of text"\
" or logo on only one side of the model but not the other, consider mirroring the entire shell"\
" except the area with the logo. Sometimes it can even be a good idea to add extra geometry"\
" around this logo so that you can cut out that particular part of the shell so that"\
" everything else from the large shells can be stacked. For making this part easier, cut your"\
" mesh in half before layouting.\n\n"\
"General advice on the layout: Divide and conquer! Start the UV puzzle by placing the largest"\
" and most oddly-shaped shells into the UV range (0 to 1). Also consider going for another ratio"\
" than 1:1, such as 2:1 or even 4:1 as the shape of the texture map does not affect the"\
" texture processing at all. The second advice is to start layouting from a single corner,"\
" working closer and closer to the opposite corner while trying to keep the layout ratio"\
" intact. This way if you end up with too little or too much UV space left, you can just"\
" select your entire UV layout and scale it. The shell spacing can also be tweaked afterwards"\
" using relative scaling in NSUV. More on this later.\n\n"\
"Loading textures into the graphics memory is slowed down by the following factors: How many"\
" channels there are in the texture (RGBA is 4x more expensive than a greyscale single-channel"\
" texture), how many pixels there are in the texture and how many texture maps your asset will"\
" use. The latter is very important. If you are doing environment art, you are strongly adviced"\
" to use texture atlases.\n",
        editable=False,
        height=700,
        parent=col3Tricks,
        width=frameX,
        wordWrap=True,
    )
    
    # Shell Spacing
    frame4Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Shell Spacing",
        parent=colSecTricks,
    )
    col4Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame4Tricks
    )
    text4Workflow = pm.scrollField(
        text="When doing UV mapping it is important to think about the issue of texture"\
" bleeding. Texture bleeding is when the color information inside one UV shell bleeds out"\
" into the area of another UV shell due to texture filtering. The general advice here is to"\
" keep a padding of at least 2 pixels around all UV shells - meaning that you get a 2px"\
" margin to the texture map border, and a 4px margin between UV shells. However (and this"\
" is IMPORTANT), that only applies to the final version of the texture. If the texture map"\
" is further reduced in size by the engine you need to increase this padding.\n\n"\
"If LoD models are to be used, extra care has to be taken. For every LoD/Mipmap step you"\
" also need to DOUBLE the shell spacing. For example: You have an asset with 3x LoD steps"\
" and an original texture size of 2048px. This means that on the smallest mipmap level,"\
" the texture is only 512px. So the spacing there needs to be 4px between shells, then"\
" 8px @ 1024px and 16px @ 2048px. So when doing the layout you need to make sure that you"\
" have 16px distance between shells and 8px distance to the UV map border. Thankfully in"\
" NSUV you can easily measure the distance between two UVs and get the result in pixels"\
" as well as UV units. Additionally, if you end up with a spacing that is too small or"\
" too large, you can try and tweak it using relative scaling. To use relative scaling in"\
" NSUV you right-click the scaling buttons. All shells in your selection will then be scaled"\
" around their own individual pivot center points.\n\n",
        editable=False,
        height=460,
        parent=col4Tricks,
        width=frameX,
        wordWrap=True,
    )
    
    # Pipes, roads, etc
    frame5Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Mapping Pipes, Roads and Walls",
        parent=colSecTricks,
    )
    col5Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame5Tricks
    )
    text5Workflow = pm.scrollField(
        text="UV mapping curved objects which tile only in one direction - either U or V -"\
" can be problematic for people who are new at 3D, but it's actually not that hard. In Maya"\
" 2016 Autodesk added a special UV projection type to combat this problem, called Contour"\
" Stretch Mapping. You will find the button for this new projection type under Project UVs"\
" in NSUV. You may be stuck with an older version of Maya, or have problems getting the right"\
" result with Contour Stretch so here is some additional advice:\n\n"\
"You can model your road/pipe straight, UV map it, and then use a bend deformer on it without"\
" removing history. Another approach is to do an automatic projection, unfold the shell and"\
" then select an edge loop and then run Straighten shell in NSUV followed by Straighten UVs."\
" A third method is to use Unitize, sew the shells together and then Unfold in one direction"\
" only - and follow up with Straighten UVs if necessary.\n",
        editable=False,
        height=299,
        parent=col5Tricks,
        width=frameX,
        wordWrap=True,
    )
    
    # Lightmaps
    frame6Tricks = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Creating Lightmap UVs",
        parent=colSecTricks,
    )
    col6Tricks = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame6Tricks
    )
    text6Workflow = pm.scrollField(
        text="Creating lightmaps is exceptionally easy in NSUV. Start by cloning map1 into a"\
" new UV set, and then turn on the shaded display in order to spot stacked and/or mirrored"\
" shells. Then set a uniform texel density for your entire mesh - unless ofc there are areas"\
" on the lightmap which you want to have a higher or lower resolution. Now use Spread Out"\
" Shells found under Arrange and make sure that you have no stacked UV shells anywhere. If"\
" you do, just cut them off and spread out the shells once more. Then layout the shells as"\
" usual, fit the map into the default range and make sure the spacing is correct.\n",
        editable=False,
        height=194,
        parent=col6Tricks,
        width=frameX,
        wordWrap=True,
    )
    
    # Button
    btnClose = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainTricks,
        width=largeWinX,
    )
    
    pm.showWindow(window)


# Options UI for the unfold feature
def unfoldUI():

    # Vars
    visState1 = False
    visState2 = True
    visState2 = False ## NOTE: Double declaration needed for unknown reasons

    cBoxBorderUnfold, cBoxFlipsUnfold, cBoxHistoryUnfold, cBoxPackUnfold, cBoxPin1Unfold, cBoxPin2Unfold, \
    cBoxRescaleUnfold, fieldOptUnfold, fieldWeightUnfold, menuSpaceUnfold, radGrpConstUnfold, \
    radGrpPinUnfold, radGrpUnfold, sliderItrUnfold, sliderMaxItrUnfold, sliderOptUnfold, sliderSpaceUnfold, \
    sliderScaleUnfold, sliderStopUnfold, sliderWeightUnfold = (None,)*20

    # Look for unfold3D plugin
    unfold3DLoaded = pm.pluginInfo("Unfold3D", query=True, loaded=True)
    
    # Fix array overflow
    if unfold3DLoaded == False and pm.optionVar["unfoldMethod_NSUV"] == 3:
        pm.optionVar["unfoldMethod_NSUV"] = 2


    # Switch unfold method
    def unfoldSwitch():

        # Unfold3D plugin loaded
        if unfold3DLoaded == True:

            # Unfold3D. Hide Legacy frames
            if radGrpUnfold.getSelect() == 1:
                frameSolver1Unfold.setVisible(True)
                frameSpacingUnfold.setVisible(True)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(False)

            # Legacy. Hide Unfold3D frames
            elif radGrpUnfold.getSelect() == 2 :
                frameSolver1Unfold.setVisible(False)
                frameSpacingUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(True)
                framePinningUnfold.setVisible(True)
                frameOtherUnfold.setVisible(True)
                textQuickUnfold.setVisible(False)

            else: # Quick. Hide all frames
                frameSolver1Unfold.setVisible(False)
                frameSpacingUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(True)

        else: # Plugin not loaded

            if radGrpUnfold.getSelect() == 1:
                frameSolver1Unfold.setVisible(False)
                frameSpacingUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(True)
                framePinningUnfold.setVisible(True)
                frameOtherUnfold.setVisible(True)
                textQuickUnfold.setVisible(False)

            else:
                frameSolver1Unfold.setVisible(False)
                frameSpacingUnfold.setVisible(False)
                frameSolver2Unfold.setVisible(False)
                framePinningUnfold.setVisible(False)
                frameOtherUnfold.setVisible(False)
                textQuickUnfold.setVisible(True)

        # Save optVar
        pm.optionVar["unfoldMethod_NSUV"] = radGrpUnfold.getSelect()


    # Reset UI
    def unfoldUIReset():

        # Reset UI controls
        radGrpUnfold.setSelect(1)
        sliderItrUnfold.setValue(1)
        cBoxPackUnfold.setValue1(True)
        cBoxBorderUnfold.setValue1(True)
        cBoxFlipsUnfold.setValue1(True)
        sliderSpaceUnfold.setValue(2)
        sliderSizeUnfold.setValue(1024)
        fieldWeightUnfold.setValue(0.0000)
        sliderWeightUnfold.setValue(0.0000)
        fieldOptUnfold.setValue(0.5)
        sliderOptUnfold.setValue(0.5)
        sliderOptUnfold.setEnable(False)
        cBoxPin1Unfold.setValue1(False)
        cBoxPin2Unfold.setValue1(True)
        radGrpPinUnfold.setSelect(2)
        radGrpConstUnfold.setSelect(1)
        sliderMaxItrUnfold.setValue(5000)
        sliderStopUnfold.setValue(0.0010)
        cBoxRescaleUnfold.setValue1(False)
        cBoxHistoryUnfold.setValue1(False)

        # Reset optVars
        pm.optionVar["unfoldMethod_NSUV"] = 1
        pm.optionVar["unfoldItr_NSUV"] = 1
        pm.optionVar["unfoldPack_NSUV"] = True
        pm.optionVar["unfoldBorder_NSUV"] = True
        pm.optionVar["unfoldFlips_NSUV"] = True
        pm.optionVar["unfoldSpaceVal_NSUV"] = 2
        pm.optionVar["unfoldSize_NSUV"] = 1024
        pm.optionVar["unfoldSolver_NSUV"] = 0.0000
        pm.optionVar["unfoldOtO_NSUV"] = 0.5000
        pm.optionVar["unfoldPinBorder_NSUV"] = False
        pm.optionVar["unfoldPin_NSUV"] = True
        pm.optionVar["unfoldPinType_NSUV"] = 2
        pm.optionVar["unfoldConst_NSUV"] = 1
        pm.optionVar["unfoldMaxItr_NSUV"] = 5000
        pm.optionVar["unfoldStop_NSUV"] = 0.0010
        pm.optionVar["unfoldRescale_NSUV"] = False
        pm.optionVar["unfoldSFact_NSUV"] = 0.0200
        pm.optionVar["unfoldHist_NSUV"] = False

        # Switch to the correct layouts
        unfoldSwitch()


    # Update optVar
    def unfoldOptVar(varType, control=None, control2=None):

        if varType == 1:
            pm.optionVar["unfoldItr_NSUV"] = sliderItrUnfold.getValue()

        elif varType == 2:
            pm.optionVar["unfoldPack_NSUV"] = cBoxPackUnfold.getValue1()

        elif varType == 3:
            pm.optionVar["unfoldBorder_NSUV"] = cBoxBorderUnfold.getValue1()

        elif varType == 4:
            pm.optionVar["unfoldFlips_NSUV"] = cBoxFlipsUnfold.getValue1()

        elif varType == 5:
            pm.optionVar["unfoldSize_NSUV"] = control.getValue()

        elif varType == 6:
            pm.optionVar["unfoldSpaceVal_NSUV"] = sliderSpaceUnfold.getValue()

        elif varType == 7:

            # Manipulate the other controls, then set optVar
            control2.setValue( control.getValue() )
            if control.getValue() == 0.0:
                fieldOptUnfold.setEnable(False) # Hide
                sliderOptUnfold.setEnable(False) # Hide
            else:
                fieldOptUnfold.setEnable(True) # Show
                sliderOptUnfold.setEnable(True) # Show
            pm.optionVar["unfoldSolver_NSUV"] = control.getValue()

        elif varType == 8:

            # Manipulate the other control, then set optVar
            control2.setValue( control.getValue() )
            pm.optionVar["unfoldOtO_NSUV"] = control.getValue()

        elif varType == 9:
            pm.optionVar["unfoldPinBorder_NSUV"] = cBoxPin1Unfold.getValue1()

        elif varType == 10:

            # Hide/Show other control, then set optVar
            if control2.getEnable() == True:
                control2.setEnable(False)
            else:
                control2.setEnable(True)
            pm.optionVar["unfoldPin_NSUV"] = control.getValue1()

        elif varType == 11:
            pm.optionVar["unfoldPinType_NSUV"] = radGrpPinUnfold.getSelect()

        elif varType == 12:
            pm.optionVar["unfoldConst_NSUV"] = radGrpConstUnfold.getSelect()

        elif varType == 13:
            pm.optionVar["unfoldMaxItr_NSUV"] = sliderMaxItrUnfold.getValue()

        elif varType == 14:
            pm.optionVar["unfoldStop_NSUV"] = sliderStopUnfold.getValue()

        elif varType == 15:

            # Hide/Show other control, then set optVar
            if control2.getEnable() == True:
                control2.setEnable(False)
            else:
                control2.setEnable(True)
            pm.optionVar["unfoldRescale_NSUV"] = control.getValue1()

        elif varType == 17:
            pm.optionVar["unfoldHist_NSUV"] = cBoxHistoryUnfold.getValue1()

        else: # Incorrect varType
            pm.error("Incorrect varType sent to UI.unfoldUI.unfoldOptVar()")


    # Check for window duplicate
    if pm.window( winUnfold, exists=True ):
        pm.deleteUI(winUnfold)

    # Read UI control optVars - Set visibility states
    if pm.optionVar["unfoldSolver_NSUV"] > 0:
        visState1 = True

    if pm.optionVar["unfoldRescale_NSUV"] == True:
        visState2 = True

    # Window
    window = pm.window(
        winUnfold,
        height=unfoldWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Unfold UVs",
        width=largeWinX
    )

    # Create layouts
    form1Unfold = pm.formLayout()
    scrollUnfold = pm.scrollLayout( childResizable=True )
    form2Unfold = pm.formLayout( parent=scrollUnfold )

    frameMainUnfold = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Unfold Options",
        parent=form2Unfold
    )

    # Method radioBtnGrp
    if unfold3DLoaded == True: # Unfold3D plugin -check
        radGrpUnfold = pm.radioButtonGrp(
            changeCommand=lambda *args: unfoldSwitch(),
            columnWidth2=[largeCol1, largeCol2],
            label="Method: ",
            labelArray3=["Unfold3D", "Legacy", "Quick"],
            numberOfRadioButtons=3,
            parent=frameMainUnfold,
            select=pm.optionVar["unfoldMethod_NSUV"],
            vertical=True,
        )
    else: # Unfold3D not loaded
        radGrpUnfold = pm.radioButtonGrp(
            changeCommand=lambda *args: unfoldSwitch(),
            columnWidth2=[largeCol1, largeCol2],
            label="Method: ",
            labelArray2=["Legacy", "Quick"],
            numberOfRadioButtons=2,
            parent=frameMainUnfold,
            select=pm.optionVar["unfoldMethod_NSUV"],
            vertical=True,
        )


    ## Unfold 3D

    # Unfold 3D: Solver frame and column
    frameSolver1Unfold = pm.frameLayout(
        label="Settings",
        parent=form2Unfold
    )
    colSolver1Unfold = pm.columnLayout(
        parent=frameSolver1Unfold
    )

    # Unfold3D: Solver elements
    sliderItrUnfold = pm.intSliderGrp(
        adjustableColumn=3,
        columnAttach3=["both", "both", "both"],
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        changeCommand=lambda *args: unfoldOptVar(1),
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Iterations: ",
        maxValue=10,
        minValue=0,
        parent=colSolver1Unfold,
        value=pm.optionVar["unfoldItr_NSUV"],
    )
    cBoxPackUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(2),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Pack",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldPack_NSUV"],
    )
    cBoxBorderUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(3),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Prevent self border intersections",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldBorder_NSUV"],
    )
    cBoxFlipsUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(4),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Prevent triangle flips",
        parent=colSolver1Unfold,
        value1=pm.optionVar["unfoldFlips_NSUV"],
    )
    sep1Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver1Unfold,
        visible=True,
    )

    # Unfold3D: Shell padding and Map Size frame and column
    frameSpacingUnfold = pm.frameLayout(
        label="Shell Spacing",
        parent=form2Unfold
    )
    colSpacingUnfold = pm.columnLayout(
        parent=frameSpacingUnfold,
    )

    # Shell padding and Map Size: Elements
    sliderSizeUnfold = pm.intSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(5, sliderSizeUnfold),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        dragCommand=lambda *args: unfoldOptVar(5, sliderSizeUnfold),
        field=True,
        fieldStep=32,
        label="Map size (px): ",
        max=8192,
        min=32,
        parent=colSpacingUnfold,
        sliderStep=32,
        step=32,
        value=pm.optionVar["unfoldSize_NSUV"]
    )

    sliderSpaceUnfold = pm.intSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(6),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=999,
        fieldMinValue=0,
        label="Shell padding (Pixels): ",
        maxValue=10,
        minValue=0,
        parent=colSpacingUnfold,
        value=pm.optionVar["unfoldSpaceVal_NSUV"],
    )
    sep2Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSpacingUnfold,
        visible=True,
    )


    ## Legacy

    # Legacy: Solver frame and column
    frameSolver2Unfold = pm.frameLayout(
        label="Settings",
        parent=form2Unfold
    )
    colSolver2Unfold = pm.columnLayout(
        parent=frameSolver2Unfold
    )

    # Legacy: Solver elements
    solverRowUnfold = pm.rowLayout(
        columnAttach=[1, "right", 0],
        columnWidth3=[largeCol1, largeCol2, 80],
        numberOfColumns=3,
        parent=colSolver2Unfold,
    )

    solverTextUnfold = pm.text(
        label="Weight solver towards: ",
        parent=solverRowUnfold,
    )

    fieldWeightUnfold = pm.floatField(
        changeCommand=lambda *args: unfoldOptVar(7, fieldWeightUnfold, sliderWeightUnfold),
        maxValue=1.0,
        minValue=0.0,
        parent=solverRowUnfold,
        value=pm.optionVar["unfoldSolver_NSUV"],
    )

    solverTextUnfoldWarn = pm.text(
        label="WARNING: The global solver is SLOW!",
        parent=solverRowUnfold,
    )

    sliderWeightUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(7, sliderWeightUnfold, fieldWeightUnfold),
        columnWidth3=[largeCol1, (largeCol2+largeCol3+2), 80],
        extraLabel=" Global solver",
        label="Local solver ",
        minValue=0.0,
        maxValue=1.0,
        parent=colSolver2Unfold,
        value=pm.optionVar["unfoldSolver_NSUV"],
    )

    optRowUnfold = pm.rowLayout(
        numberOfColumns=2,
        columnAttach=[1, "right", 0],
        columnWidth2=[largeCol1, largeCol2],
        parent=colSolver2Unfold,
    )

    optTextUnfold = pm.text(
        label="Optimize to original: ",
        parent=optRowUnfold,
    )

    fieldOptUnfold = pm.floatField(
        changeCommand=lambda *args: unfoldOptVar(8, fieldOptUnfold, sliderOptUnfold),
        enable=visState1,
        maxValue=1.0,
        minValue=0.0000,
        parent=optRowUnfold,
        value=pm.optionVar["unfoldOtO_NSUV"],
    )

    sliderOptUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(8, sliderOptUnfold, fieldOptUnfold),
        columnWidth3=[largeCol1, (largeCol2+largeCol3+2), 80],
        enable=visState1,
        extraLabel=" Face area",
        label="Edge length ",
        maxValue=1.0,
        minValue=0.0000,
        parent=colSolver2Unfold,
        precision=4,
        value=pm.optionVar["unfoldOtO_NSUV"],
    )

    areaRowUnfold = pm.rowLayout(
        numberOfColumns=2,
        columnAttach=[1, "right", 0],
        columnWidth2=[largeCol1, largeCol2],
        parent=colSolver2Unfold,
    )

    sep3Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colSolver2Unfold,
        visible=True,
    )

    # Legacy: Pinning frame and column
    framePinningUnfold = pm.frameLayout(
        label="Pinning",
        parent=form2Unfold,
    )
    colPinningUnfold = pm.columnLayout(
        parent=framePinningUnfold,
    )

    # Legacy: Pinning elements
    cBoxPin1Unfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(9),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Pin UV Shell Border",
        parent=colPinningUnfold,
        value1=pm.optionVar["unfoldPinBorder_NSUV"],
    )
    cBoxPin2Unfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(10, cBoxPin2Unfold, radGrpPinUnfold),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Pin UVs",
        parent=colPinningUnfold,
        value1=pm.optionVar["unfoldPin_NSUV"],
    )
    radGrpPinUnfold = pm.radioButtonGrp(
        changeCommand=lambda *args: unfoldOptVar(11),
        columnWidth2=[( largeCol1 + 15 ), ( largeCol2 + 55 )],
        enable=pm.optionVar["unfoldPin_NSUV"],
        label1="Pin selected UVs",
        label2="Pin unselected UVs",
        label="",
        numberOfRadioButtons=2,
        parent=colPinningUnfold,
        select=pm.optionVar["unfoldPinType_NSUV"],
        vertical=True,
    )
    
    sep4Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colPinningUnfold,
        visible=True,
    )
 
    radGrpConstUnfold = pm.radioButtonGrp(
        changeCommand=lambda *args: unfoldOptVar(12),
        columnWidth2=[largeCol1, largeCol2+10],
        label1="None",
        label2="Vertical",
        label3="Horizontal",
        label="Unfold constraint: ",
        numberOfRadioButtons=3,
        parent=colPinningUnfold,
        select=pm.optionVar["unfoldConst_NSUV"],
        vertical=True,
    )


    # Legacy: Other frame and column
    frameOtherUnfold = pm.frameLayout(
        label="Other Options",
        parent=form2Unfold,
    )
    colOtherUnfold = pm.columnLayout(
        parent=frameOtherUnfold,
    )

    # Legacy: Other elements
    sliderMaxItrUnfold = pm.intSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(13),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=10000,
        fieldMinValue=1,
        label="Max iterations: ",
        maxValue=10000,
        minValue=1,
        parent=colOtherUnfold,
        value=pm.optionVar["unfoldMaxItr_NSUV"],
    )
    sliderStopUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(14),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        field=True,
        fieldMaxValue=100.0,
        fieldMinValue=0.0,
        label="Stopping threshold: ",
        maxValue=100.0,
        minValue=0.0001,
        parent=colOtherUnfold,
        precision=4,
        value=pm.optionVar["unfoldStop_NSUV"]
    )
    sep5Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )
    cBoxRescaleUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(15, cBoxRescaleUnfold, sliderScaleUnfold),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Rescale",
        parent=colOtherUnfold,
        value1=pm.optionVar["unfoldRescale_NSUV"],
    )
    sliderScaleUnfold = pm.floatSliderGrp(
        changeCommand=lambda *args: unfoldOptVar(16),
        columnWidth3=[largeCol1, largeCol2, largeCol3],
        enable=visState2,
        field=True,
        fieldMaxValue=10000.0,
        fieldMinValue=0.00001,
        label="Scale factor: ",
        maxValue=10.0,
        minValue=0.00001,
        parent=colOtherUnfold,
        precision=5,
        value=pm.optionVar["unfoldSFact_NSUV"],
    )
    sep6Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )
    cBoxHistoryUnfold = pm.checkBoxGrp(
        changeCommand=lambda *args: unfoldOptVar(17),
        columnWidth2=[largeCol1, largeCol2],
        label="",
        label1="Keep history",
        parent=colOtherUnfold,
        value1=pm.optionVar["unfoldHist_NSUV"]
    )
    sep7Unfold = pm.separator(
        height=sepSpace,
        horizontal=True,
        parent=colOtherUnfold,
        visible=True,
    )


    ## Quick

    textQuickUnfold = pm.text(
        label="No options here - Things just get done!!",
        parent=form2Unfold
    )

    # Buttons
    btnApplyCloseUnfold = pm.button(
        command=lambda *args: core.unfoldUVs("both", winUnfold),
        label="Confirm",
        parent=form1Unfold,
    )
    btnApplyUnfold = pm.button(
        command=lambda *args: core.unfoldUVs(),
        label="Apply",
        parent=form1Unfold,
    )
    btnResetUnfold = pm.button(
        command=lambda *args: unfoldUIReset(),
        label="Reset",
        parent=form1Unfold,
    )
    btnCloseUnfold = pm.button(
        command=lambda *args: pm.deleteUI(winUnfold),
        label="Close",
        parent=form1Unfold,
    )

    # Layout frames
    pm.formLayout(
        form2Unfold, edit=True,
        attachForm=[

            (frameMainUnfold, "top", 0),
            (frameMainUnfold, "left", 0),
            (frameMainUnfold, "right", 0),

            (frameSolver1Unfold, "left", 0),
            (frameSolver1Unfold, "right", 0),

            (frameSpacingUnfold, "left", 0),
            (frameSpacingUnfold, "right", 0),

            (frameSolver2Unfold, "left", 0),
            (frameSolver2Unfold, "right", 0),

            (framePinningUnfold, "left", 0),
            (framePinningUnfold, "right", 0),

            (frameOtherUnfold, "left", 0),
            (frameOtherUnfold, "right", 0),

            (textQuickUnfold, "left", 0),
            (textQuickUnfold, "right", 0),
        ],
        attachControl=[
            (frameSolver1Unfold, "top", 10, frameMainUnfold),

            (frameSpacingUnfold, "top", 10, frameSolver1Unfold),

            (frameSolver2Unfold, "top", 0, frameSpacingUnfold),

            (framePinningUnfold, "top", 10, frameSolver2Unfold),

            (frameOtherUnfold, "top", 10, framePinningUnfold),

            (textQuickUnfold, "top", 0, frameOtherUnfold),
        ],
        attachNone=[
            (frameSolver1Unfold, "bottom"),

            (frameSpacingUnfold, "bottom"),

            (frameSolver2Unfold, "bottom"),

            (framePinningUnfold, "bottom"),

            (frameOtherUnfold, "bottom"),

            (textQuickUnfold, "bottom"),
        ]
    )

    # Layout main form
    pm.formLayout(
        form1Unfold, edit=True,
        attachForm=[
            (scrollUnfold, "top", 0),
            (scrollUnfold, "left", 0),
            (scrollUnfold, "right", 0),

            (btnApplyCloseUnfold, "left", 5),
            (btnApplyCloseUnfold, "bottom", 5),
            (btnApplyUnfold, "bottom", 5),
            (btnResetUnfold, "bottom", 5),
            (btnCloseUnfold, "right", 5),
            (btnCloseUnfold, "bottom", 5),
        ],
        attachControl=[
            (scrollUnfold, "bottom", 0, btnApplyCloseUnfold),
        ],
        attachPosition=[
            (btnApplyCloseUnfold, "right", 3, 25),
            (btnApplyUnfold, "left", 2, 25),
            (btnApplyUnfold, "right", 3, 50),
            (btnResetUnfold, "right", 3, 75),
            (btnResetUnfold, "left", 2, 50),
            (btnCloseUnfold, "left", 2, 75),
        ],
        attachNone=[
            (btnApplyCloseUnfold, "top"),
            (btnApplyUnfold, "top"),
            (btnResetUnfold, "top"),
            (btnCloseUnfold, "top"),
        ],
    )

    # Hide inactive
    unfoldSwitch()

    # Display the window
    pm.showWindow(window)


# Update NSUV -UI window
def updateUI():

    userResponse = pm.confirmDialog(
        button=["Yes", "No"],
        cancelButton="No",
        defaultButton="No",
        dismissString="No",
        message="Open up the NSUV Creative Crash page and look for an update?", 
        title="Update NSUV",
    )    
    if userResponse == "No": pass
    else:
        pm.launch(web="http://www.creativecrash.com/maya/script/nightshade-uv-editor")


# Welcome screen - displayed only once
def welcomeUI():

    # Reset optVar because this window only shows up once
    pm.optionVar["welcome_NSUV"] = False

    # Check for window duplicate
    if pm.window( winWelcome, exists=True ):
        pm.deleteUI(winWelcome)

    # Window
    window = pm.window(
        winWelcome,
        height=aboutWinY,
        minimizeButton=False,
        maximizeButton=False,
        sizeable=True,
        title="Welcome to Nightshade UV Editor",
        width=largeWinX
    )

    # Main column
    colMainWelcome = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=largeWinX,
    )

    # Title image
    imageNSUV = pm.image(
        image=iconDict["title"],
        parent=colMainWelcome,
    )

    # Information
    frameWelcome = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Information",
        marginHeight=frameMargin,
        marginWidth=frameMargin,
        parent=colMainWelcome,
        width=largeWinX,
    )
    colWelcome = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frameWelcome
    )
    text1Welcome = pm.scrollField(
        text="Welcome to Nightshade UV Editor! \nThank you for downloading this tool. \
Hopefully it will be the last and only UV editor you will ever need here inside Maya. \n\nBefore \
you get started you will need to create a shelf button - you can do that with the button below. \
Afterwards you can close down this window - it will not be shown again (but you can still \
create a new shelf button via the NSUV menu in case you placed it on the wrong shelf).",
        editable=False,
        height=160,
        parent=colWelcome,
        width=frameX,
        wordWrap=True,
    )

    # Create button
    btnCreateWelcome = pm.button(
        command=lambda *args: core.createShelfBtn(),
        label="Create Shelf Button",
        parent=colWelcome,
    )

    text2Welcome = pm.text(
        label="If you are completely new to UV-mapping then I suggest that you check out the \n\
workflow guide under the NSUV menu in order to get started. There under the menu \n\
you will also find a 'Tips and Tricks' section, as well as general info about NSUV.\n\n\
Once again, thank you for trying out NSUV.\n\n/Martin, creator of Nightshade UV Editor.",
        parent=colWelcome,
    )

    # Close button
    btnCloseWelcome = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainWelcome,
        width=largeWinX,
    )

    # Display the window
    pm.showWindow(window)


# UI for reporting a bug or requesting a feature
def workflowUI():

    # Check for window duplicate
    if pm.window( winWorkflow, exists=True ):
        pm.deleteUI(winWorkflow)

    # Window
    window = pm.window(
        winWorkflow,
        height=largeWinY,
        minimizeButton=True,
        maximizeButton=True,
        sizeable=True,
        title="Basic Workflow",
        width=largeWinX
    )
        
    # Main column
    colMainWorkflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
    )
    
    # Title image
    imageWorkflow = pm.image(
        image=iconDict["workflow"],
        parent=colMainWorkflow,
    )
    
    scrollWorkflow = pm.scrollLayout(
        childResizable=True,
        height=largeWinY,
        width=largeWinX,
    )
    
    # Secondary column
    colSecWorkflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        width=frameX, 
    )      
    
    # Intro
    frame1Workflow = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Introduction",
        parent=colSecWorkflow,
    )
    col1Workflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame1Workflow
    )
    text1Workflow = pm.scrollField(
        text="If you are new to 3D and asset creation or just do not not have that"\
" much experience with it, doing UV-related work can be both quite time-consuming and"\
" quite boring: but it doesn't have to be! With NSUV, previously quite tedious and"\
" annoying tasks will be done faster and easier - so that you can spend more time being"\
" creative and less time on combating technical hurdles.\n\nThe"\
" NSUV user-interface has a logical and intuitive layout that will help"\
" you get into the correct workflow with ease. The majority of things you need are available"\
" on the sidebar - only the move/grab tools, selections and visibility toggles are placed"\
" elsewhere. NOTE that many buttons in NSUV have a right-click functionality. For example:"\
" By clicking any of the scale buttons, you will scale your entire UV selection. But if you"\
" instead right-click any of these buttons, you will scale every shell around their own"\
" individual center points (based on the bounding box).\n",
        editable=False,
        height=298,
        parent=col1Workflow,
        width=frameX,
        wordWrap=True,
    )

    # UV Projection info info
    frame2Workflow = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="UV Mapping",
        parent=colSecWorkflow,
    )
    col2Workflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame2Workflow
    )
    text2Workflow = pm.scrollField(
        text="The first thing that needs to be done is something called UV Mapping."\
" UV Mapping is the process of projecting - or mapping - a 3D surface onto a 2D surface"\
" (the texture of your 3D mesh). When creating simple 3D primitives, Maya automagicly do"\
" the UV projections for you - but as soon as you modify, combine and split said primitives"\
" your UV map will become scrambled. Therefore it is necessary to create new UV projections"\
" once you are finished modelling. IMPORTANT: It is strongly adviced that you do not jump"\
" ahead and start projecting/map UVs BEFORE you are done with the modelling. Tweaking a mesh"\
" while containing the UV projection is a complicated process and you might end up ruining"\
" your UV mappings.\n\nNSUV comes with all the native UV projections that Maya offers,"\
" but also has one exclusive UV mapping method called \"Normal-based mapping\", which creates"\
" a planar projection from the average direction of the face normals in a face selection.\n",
        editable=False,
        height=320,
        parent=col2Workflow,
        width=frameX,
        wordWrap=True,
    )
    
    # UV Unwrapping info
    frame3Workflow = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="UV Unwrapping",
        parent=colSecWorkflow,
    )
    col3Workflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame3Workflow
    )
    text3Workflow = pm.scrollField(
        text="The process of creating UV projections is alternated with a sub-process"\
" called UV Unwrapping. These processes are known as UV Mapping.\n\nUV Unwrapping is the"\
" process of making sure that the UV projections are unwrapped or unfolded correctly"\
" in order to avoid heavy distortion and/or scrambled non-manifold UV shells. This is"\
" done by manually cutting and sewing together UV seams on your mesh, while repeatedly"\
" redoing the UV projections. Unwrapping also involves the process of manually smoothening"\
" and straightening shells after the projection(s) has been made.\n\nIt is recommended"\
" to apply a checker texture to your mesh while doing UV Mapping and to make sure that"\
" you remove distortion where you do not want it.\n\nNote that the checkers on your mesh"\
" does not have to be uniform, and there are actually cases where you want pinching,"\
" stretching or non-uniform UV shells. For example, when doing low-poly/mobile graphics"\
" it is often better with straight shells due to the texture limitations (size)."\
" Read more about this under NSUV > Tips And Tricks.\n",
        editable=False,
        height=383,
        parent=col3Workflow,
        width=frameX,
        wordWrap=True,
    )
    
    # Arrangement
    frame4Workflow = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Arranging UVs",
        parent=colSecWorkflow,
    )
    col4Workflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame4Workflow
    )
    text4Workflow = pm.scrollField(
        text="After you are done with the UV Mapping it is time to layout/arrange and"\
" pack the UV shells. The shells should be within the normal UV range (0 to 1) before you"\
" export your asset, but most game engine will not have a problem with shells expanding"\
" beyond the normal UV range. However (and this is IMPORTANT): Everything outside the"\
" normal UV range will simply repeat, and you will notice this if you apply a texture to your"\
" model (like a checker). Therefore it is important that no shells are place on the UV"\
" range border, as this is the same as stacking UV shells together.\n\nBefore you start"\
" arranging the UV shells, you need to ask yourself an important question: How large will"\
" the texture map be? The smaller your texture is, the more spacing you need between shells."\
" Another important factor is the amount of LOD-models you are going to use. For every"\
" LOD-step you need to DOUBLE the spacing between UV shells.\n\nIn NSUV it is easy to"\
" measure distance between shells: Simply select two UVs (one from each shell) and click"\
" the rulere icons under the Manipulator frame. You can both measure the pixel distance as"\
" well as the distance in UV units. When doing the latter, the unit distance will be copied"\
" to the manipulator input field. For more information regarding UV packing and spacing,"\
" check NSUV > Tips and Tricks.\n",
        editable=False,
        height=418,
        parent=col4Workflow,
        width=frameX,
        wordWrap=True,
    )
    
    # Final
    frame5Workflow = pm.frameLayout(
        borderVisible=False,
        collapsable=False,
        label="Finalizing the UV map",
        parent=colSecWorkflow,
    )
    col5Workflow = pm.columnLayout(
        adjustableColumn=False,
        columnAlign="left",
        rowSpacing=6,
        parent=frame5Workflow
    )
    text5Workflow = pm.scrollField(
        text="When the model has been UV Mapped, and the shells have been placed tightly"\
" together within the normal UV range (0 to 1), it is time to render a UV snapshot so"\
" that you can begin texturing your creation. Select the mesh in your scene and in NSUV you"\
" click the camera icon under UV Sets. Chenge the path, file format and texture size and"\
" press Ok.\n\nThere are a couple things that this basic workflow guide hasn't covered yet,"\
" such as the use of multiple UV sets and how to deal with Texel Density (TD). This is"\
" partly covered under NSUV > Tips and Tricks.\n",
        editable=False,
        height=208,
        parent=col5Workflow,
        width=frameX,
        wordWrap=True,
    )
    
    # Button
    btnCloseWorkflow = pm.button(
        command=lambda *args: pm.deleteUI(window),
        label="Close",
        parent=colMainWorkflow,
        width=largeWinX,
    )

    # Display the window
    pm.showWindow(window)