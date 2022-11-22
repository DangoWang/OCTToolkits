# -*- coding: utf-8 -*-
"""

    Option variable initiation for Nightshade UV Editor (NSUV) v2.1.3
    
    NSUV offers extended utility to Maya´s native UV Editor.
    Made by Martin (Nightshade) Dahlin - martin.dahlin@live.com - martin.dahlin.net
    
    Special thanks to:
    Nathan Roberts, Robert Kovach, David Johnson and Viktoras Makauskas on CGTalk, 
    Robert White and Steve Theodore on Tech-Artists.org
    Anton Palmqvist, Malcolm Andrieshyn and my friends Alexander Lilja and Elin Rudén
    for all the feedback, criticism, bug reports and feature ideas. 
    Thank you all!

    Script downloaded from Creative Crash
    
"""

## Initialize

# Import PyMEL module
import pymel.core as pm


## Functions

# Create
def create():

    # Main
    if "editorTitle_NSUV" not in pm.env.optionVars: pm.optionVar["editorTitle_NSUV"] = ""
    if "manual_NSUV" not in pm.env.optionVars: pm.optionVar["manual_NSUV"] = ""
    pm.optionVar["mayaVer_NSUV"] = pm.about(api=True) # We always want to check this at startup
    if "popupType_NSUV" not in pm.env.optionVars: pm.optionVar["popupType_NSUV"] = 0
    if "sizeableWin_NSUV" not in pm.env.optionVars: pm.optionVar["sizeableWin_NSUV"] = False
    if "totdCounter_NSUV" not in pm.env.optionVars: pm.optionVar["totdCounter_NSUV"] = int(1)
    if "totd_NSUV" not in pm.env.optionVars: pm.optionVar["totd_NSUV"] = True # Tip of the day
    if "welcome_NSUV" not in pm.env.optionVars: pm.optionVar["welcome_NSUV"] = True
    
    # Tabs and T/R/S - Unused atm
    if "tabs_NSUV" not in pm.env.optionVars: pm.optionVar["tabs_NSUV"] = 1
    if "tMode_NSUV" not in pm.env.optionVars: pm.optionVar["tMode_NSUV"] = 1
    
    # Frames
    if "frame1_NSUV" not in pm.env.optionVars: pm.optionVar["frame1_NSUV"] = False
    if "frame2_NSUV" not in pm.env.optionVars: pm.optionVar["frame2_NSUV"] = False
    if "frame3_NSUV" not in pm.env.optionVars: pm.optionVar["frame3_NSUV"] = False
    if "frame4_NSUV" not in pm.env.optionVars: pm.optionVar["frame4_NSUV"] = False
    if "frame5_NSUV" not in pm.env.optionVars: pm.optionVar["frame5_NSUV"] = False
    if "frame6_NSUV" not in pm.env.optionVars: pm.optionVar["frame6_NSUV"] = False
    if "frame7_NSUV" not in pm.env.optionVars: pm.optionVar["frame7_NSUV"] = False  
    if "frame8_NSUV" not in pm.env.optionVars: pm.optionVar["frame8_NSUV"] = False  
    
    # Toolbar
    if "toolbarState_NSUV" not in pm.env.optionVars: pm.optionVar["toolbarState_NSUV"] = True
    if "showStatusTools_NSUV" not in pm.env.optionVars: pm.optionVar["showStatusTools_NSUV"] = 1
    if "showStatusPinning_NSUV" not in pm.env.optionVars: pm.optionVar["showStatusPinning_NSUV"] = 1
    if "showStatusSelection_NSUV" not in pm.env.optionVars: pm.optionVar["showStatusSelection_NSUV"] = 1
    if "showStatusIsolateSelect_NSUV" not in pm.env.optionVars: pm.optionVar["showStatusIsolateSelect_NSUV"] = 1
    if "showStatusCopyPasteDel_NSUV" not in pm.env.optionVars: pm.optionVar["showStatusCopyPasteDel_NSUV"] = 1

    # Visibility bar
    if "imgDisp_NSUV" not in pm.env.optionVars: pm.optionVar["imgDisp_NSUV"] = True       
    if "imgDim_NSUV" not in pm.env.optionVars: pm.optionVar["imgDim_NSUV"] = False       
    if "shellShade_NSUV" not in pm.env.optionVars: pm.optionVar["shellShade_NSUV"] = True       
    if "shellBorder_NSUV" not in pm.env.optionVars: pm.optionVar["shellBorder_NSUV"] = False       
    if "shellDist_NSUV" not in pm.env.optionVars: pm.optionVar["shellDist_NSUV"] = False       
    if "checkers_NSUV" not in pm.env.optionVars: pm.optionVar["checkers_NSUV"] = False
    if "imgFilter_NSUV" not in pm.env.optionVars: pm.optionVar["imgFilter_NSUV"] = True
    if "imgRGBA_NSUV" not in pm.env.optionVars: pm.optionVar["imgRGBA_NSUV"] = False
    if "gridDisp_NSUV" not in pm.env.optionVars: pm.optionVar["gridDisp_NSUV"] = True
    if "pxSnap_NSUV" not in pm.env.optionVars: pm.optionVar["pxSnap_NSUV"] = False
    if "editorBaking_NSUV" not in pm.env.optionVars: pm.optionVar["editorBaking_NSUV"] = True
    if "imgRatio_NSUV" not in pm.env.optionVars: pm.optionVar["imgRatio_NSUV"] = False    
    if "frontColor_NSUV" not in pm.env.optionVars: pm.optionVar["frontColor_NSUV"] = [0.0, 0.0, 255.0]
    if "frontAlpha_NSUV" not in pm.env.optionVars: pm.optionVar["frontAlpha_NSUV"] = 0.25
    if "backColor_NSUV" not in pm.env.optionVars: pm.optionVar["backColor_NSUV"] = [255.0, 0.0, 0.0]
    if "backAlpha_NSUV" not in pm.env.optionVars: pm.optionVar["backAlpha_NSUV"] = 0.25   
    if "colorMan_NSUV" not in pm.env.optionVars: pm.optionVar["colorMan_NSUV"] = False
    if "expField_NSUV" not in pm.env.optionVars: pm.optionVar["expField_NSUV"] = 0.00
    if "gamField_NSUV" not in pm.env.optionVars: pm.optionVar["gamField_NSUV"] = 1.00
    if "expToggle_NSUV" not in pm.env.optionVars: pm.optionVar["expToggle_NSUV"] = False
    if "gamToggle_NSUV" not in pm.env.optionVars: pm.optionVar["gamToggle_NSUV"] = False 
    if "vtName_NSUV" not in pm.env.optionVars: pm.optionVar["vtName_NSUV"] = "sRGB gamma"
    if "isoSelect_NSUV" not in pm.env.optionVars: pm.optionVar["isoSelect_NSUV"] = False
    if "tileLabels_NSUV" not in pm.env.optionVars: pm.optionVar["tileLabels_NSUV"] = True
    if "containedFaces_NSUV" not in pm.env.optionVars: pm.optionVar["containedFaces_NSUV"] = False
    if "connectedFaces_NSUV" not in pm.env.optionVars: pm.optionVar["connectedFaces_NSUV"] = False
    if "viewFaces_NSUV" not in pm.env.optionVars: pm.optionVar["viewFaces_NSUV"] = False

    # Manipulator
    if "absToggle_NSUV" not in pm.env.optionVars: pm.optionVar["absToggle_NSUV"] = False
    if "compSpace_NSUV" not in pm.env.optionVars: pm.optionVar["compSpace_NSUV"] = 0
    if "manipAmt_NSUV" not in pm.env.optionVars: pm.optionVar["manipAmt_NSUV"] = 1.0
    if "manipCoords_NSUV" not in pm.env.optionVars: pm.optionVar["manipCoords_NSUV"] = [0.0, 0.0]
    if "manipVarA_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarA_NSUV"] = 0.0
    if "manipVarB_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarB_NSUV"] = 0.0
    if "manipVarC_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarC_NSUV"] = 0.0

    # Match UVs
    if "matchTol_NSUV" not in pm.env.optionVars: pm.optionVar["matchTol_NSUV"] = 0.005

    # Projection
    if "mapAutoMethod_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMethod_NSUV"] = 1
    if "mapAutoMSMenu_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMSMenu_NSUV"] = 6
    if "mapAutoMS1RadGrp_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMS1RadGrp_NSUV"] = 2
    if "mapAutoMS2RadGrp_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMS2RadGrp_NSUV"] = 1
    if "mapAutoMSBox1_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMSBox1_NSUV"] = True
    if "mapAutoMSBox2_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoMSBox2_NSUV"] = True    
    if "mapAutoProjBox1_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoProjBox1_NSUV"] = False
    if "mapAutoProjObj_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoProjObj_NSUV"] = ""
    if "mapAutoProjBox2_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoProjBox2_NSUV"] = False
    if "mapAutoLayoutMenu_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoLayoutMenu_NSUV"] = "Into Square"
    if "mapAutoLayoutRadGrp1_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoLayoutRadGrp1_NSUV"] = 2
    if "mapAutoLayoutRadGrp2_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoLayoutRadGrp2_NSUV"] = 1
    if "mapAutoNormBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoNormBox_NSUV"] = False
    if "mapAutoSpaceMenu_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoSpaceMenu_NSUV"] = 5
    if "mapAutoSpaceVal_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoSpaceVal_NSUV"] = 0.2000
    if "mapAutoSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoSetBox_NSUV"] = False
    if "mapAutoSet_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoSet_NSUV"] = "uvSet1"
    if "mapAutoFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoFrame1_NSUV"] = True
    if "mapAutoFrame2_NSUV" not in pm.env.optionVars: pm.optionVar["mapAutoFrame2_NSUV"] = True

    if "mapCylindricalMS1Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalMS1Box_NSUV"] = True
    if "mapCylindricalMS2Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalMS2Box_NSUV"] = True
    if "mapCylindricalSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalSetBox_NSUV"] = False
    if "mapCylindricalSet_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalSet_NSUV"] = "uvSet1"
    if "mapCylindricalSweep_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalSweep_NSUV"] = 180
    if "mapCylindricalFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["mapCylindricalFrame1_NSUV"] = True

    if "mapNormalMS1_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalMS1_NSUV"] = True
    if "mapNormalMS2_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalMS2_NSUV"] = True
    if "mapNormalMS3_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalMS3_NSUV"] = True
    if "mapNormalSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalSetBox_NSUV"] = False
    if "mapNormalSet_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalSet_NSUV"] = "uvSet1"
    if "mapNormalFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["mapNormalFrame1_NSUV"] = True

    if "mapPlanarMethod_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMethod_NSUV"] = 1 
    if "mapPlanarMS1RadGrp_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMS1RadGrp_NSUV"] = 2
    if "mapPlanarMS2RadGrp_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 1
    if "mapPlanarMS1Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMS1Box_NSUV"] = True
    if "mapPlanarMS2Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMS2Box_NSUV"] = True
    if "mapPlanarMS3Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarMS3Box_NSUV"] = True
    if "mapPlanarSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarSetBox_NSUV"] = False
    if "mapPlanarSet_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarSet_NSUV"] = "uvSet1"
    if "mapPlanarFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["mapPlanarFrame1_NSUV"] = True

    if "mapSphericalMS1Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalMS1Box_NSUV"] = True
    if "mapSphericalSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalSetBox_NSUV"] = False
    if "mapSphericalMS2Box_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalMS2Box_NSUV"] = True
    if "mapSphericalSet_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalSet_NSUV"] = "uvSet1"
    if "mapSphericalSweep1_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalSweep1_NSUV"] = 180
    if "mapSphericalSweep2_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalSweep2_NSUV"] = 90
    if "mapSphericalFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["mapSphericalFrame1_NSUV"] = True

    # Normalize
    if "normMethod_NSUV" not in pm.env.optionVars: pm.optionVar["normMethod_NSUV"] = 1
    if "normAspect_NSUV" not in pm.env.optionVars: pm.optionVar["normAspect_NSUV"] = 1
    if "normDirection_NSUV" not in pm.env.optionVars: pm.optionVar["normDirection_NSUV"] = 1
    if "normSetBox_NSUV" not in pm.env.optionVars: pm.optionVar["normSetBox_NSUV"] = False
    if "normSet_NSUV" not in pm.env.optionVars: pm.optionVar["normSet_NSUV"] = "uvSet1"
    if "normFrame1_NSUV" not in pm.env.optionVars: pm.optionVar["normFrame1_NSUV"] = True

    # Shell randomize
    if "randT_NSUV" not in pm.env.optionVars: pm.optionVar["randT_NSUV"] = 0.1
    if "randTBox1_NSUV" not in pm.env.optionVars: pm.optionVar["randTBox1_NSUV"] = True
    if "randTBox2_NSUV" not in pm.env.optionVars: pm.optionVar["randTBox2_NSUV"] = True
    if "randR_NSUV" not in pm.env.optionVars: pm.optionVar["randR_NSUV"] = 22.5
    if "randRBox1_NSUV" not in pm.env.optionVars: pm.optionVar["randRBox1_NSUV"] = False
    if "randRBox2_NSUV" not in pm.env.optionVars: pm.optionVar["randRBox2_NSUV"] = False
    if "randS_NSUV" not in pm.env.optionVars: pm.optionVar["randS_NSUV"] = 5.0
    if "randSBox1_NSUV" not in pm.env.optionVars: pm.optionVar["randSBox1_NSUV"] = False
    if "randSBox2_NSUV" not in pm.env.optionVars: pm.optionVar["randSBox2_NSUV"] = False

    # Relax
    if "relaxMethod_NSUV" not in pm.env.optionVars: pm.optionVar["relaxMethod_NSUV"] = 1
    if "relaxItr_NSUV" not in pm.env.optionVars: pm.optionVar["relaxItr_NSUV"] = 1
    if "relaxAngle_NSUV" not in pm.env.optionVars: pm.optionVar["relaxAngle_NSUV"] = 1.0
    if "relaxPower_NSUV" not in pm.env.optionVars: pm.optionVar["relaxPower_NSUV"] = 100
    if "relaxBorder_NSUV" not in pm.env.optionVars: pm.optionVar["relaxBorder_NSUV"] = True
    if "relaxFlips_NSUV" not in pm.env.optionVars: pm.optionVar["relaxFlips_NSUV"] = True
    if "relaxSpacing_NSUV" not in pm.env.optionVars: pm.optionVar["relaxSpacing_NSUV"] = 4
    if "relaxSize_NSUV" not in pm.env.optionVars: pm.optionVar["relaxSize_NSUV"] = 1024
    if "relaxPinBorder_NSUV" not in pm.env.optionVars: pm.optionVar["relaxPinBorder_NSUV"] = False
    if "relaxPin_NSUV" not in pm.env.optionVars: pm.optionVar["relaxPin_NSUV"] = False
    if "relaxPinType_NSUV" not in pm.env.optionVars: pm.optionVar["relaxPinType_NSUV"] = False
    if "relaxEdge_NSUV" not in pm.env.optionVars: pm.optionVar["relaxEdge_NSUV"] = 1
    if "relaxMaxItr_NSUV" not in pm.env.optionVars: pm.optionVar["relaxMaxItr_NSUV"] = 5

    # Snapshot
    if "shotUVpath_NSUV" not in pm.env.optionVars:
        dir = pm.workspace(query=True, rootDirectory=True) + "images/outUV"
        pm.optionVar["shotUVpath_NSUV"] = dir

    if "shotUVxSize_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVxSize_NSUV"] = 1024
    if "shotUVySize_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVySize_NSUV"] = 1024
    if "shotUVaa_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVaa_NSUV"] = 0
    if "shotUVcolor_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVcolor_NSUV"] = [ 1.0, 1.0, 1.0 ]
    if "shotUVformat_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVformat_NSUV"] = "Maya IFF"
    if "snapshotMultiTile_NSUV" not in pm.env.optionVars: pm.optionVar["snapshotMultiTile_NSUV"] = False
    if "snapshotGridUVal_NSUV" not in pm.env.optionVars: pm.optionVar["snapshotGridUVal_NSUV"] = 1
    if "snapshotGridVVal_NSUV" not in pm.env.optionVars: pm.optionVar["snapshotGridVVal_NSUV"] = 1
    if "shotUVrange_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVrange_NSUV"] = 1
    if "shotUVtype_NSUV" not in pm.env.optionVars: pm.optionVar["shotUVtype_NSUV"] = 1

    # Stored selection
    if "storedSelA_NSUV" not in pm.env.optionVars: pm.optionVar["storedSelA_NSUV"] = ""
    if "storedSelB_NSUV" not in pm.env.optionVars: pm.optionVar["storedSelB_NSUV"] = ""

    # Straighten UVs
    if "strUVsAngle_NSUV" not in pm.env.optionVars: pm.optionVar["strUVsAngle_NSUV"] = 30
    if "strUVsType_NSUV" not in pm.env.optionVars: pm.optionVar["strUVsType_NSUV"] = 0

    # TD
    if "td_NSUV" not in pm.env.optionVars: pm.optionVar["td_NSUV"] = 32
    if "tdSize_NSUV" not in pm.env.optionVars: pm.optionVar["tdSize_NSUV"] = 512
    if "manipVarTDA1_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarTDA1_NSUV"] = 32.0
    if "manipVarTDA2_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarTDA2_NSUV"] = 512
    if "manipVarTDB1_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarTDB1_NSUV"] = 32.0
    if "manipVarTDB2_NSUV" not in pm.env.optionVars: pm.optionVar["manipVarTDB2_NSUV"] = 512

    # Unfold
    if "unfoldMethod_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldMethod_NSUV"] = 1
    if "unfoldItr_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldItr_NSUV"] = 1 
    if "unfoldPack_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldPack_NSUV"] = True
    if "unfoldBorder_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldBorder_NSUV"] = True
    if "unfoldFlips_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldFlips_NSUV"] = True
    if "unfoldSize_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldSize_NSUV"] = 1024
    if "unfoldSpaceVal_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldSpaceVal_NSUV"] = 2
    if "unfoldSolver_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldSolver_NSUV"] = 0.25
    if "unfoldOtO_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldOtO_NSUV"] = 0.5000
    if "unfoldPinBorder_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldPinBorder_NSUV"] = False
    if "unfoldPin_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldPin_NSUV"] = True
    if "unfoldPinType_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldPinType_NSUV"] = 2
    if "unfoldConst_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldConst_NSUV"] = 1
    if "unfoldMaxItr_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldMaxItr_NSUV"] = 5000
    if "unfoldStop_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldStop_NSUV"] = 0.0010
    if "unfoldRescale_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldRescale_NSUV"] = False
    if "unfoldSFact_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldSFact_NSUV"] = 0.0200
    if "unfoldHist_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldHist_NSUV"] = False

    # UV Sets
    if "copyNewUVSet_NSUV" not in pm.env.optionVars: pm.optionVar["copyNewUVSet_NSUV"] = "map2"
    if "newUVSet_NSUV" not in pm.env.optionVars: pm.optionVar["newUVSet_NSUV"] = "map2"
    if "newUVSetShare_NSUV" not in pm.env.optionVars: pm.optionVar["newUVSetShare_NSUV"] = 1
    if "scrollList_NSUV" not in pm.env.optionVars: pm.optionVar["scrollList_NSUV"] = ""
    if "copyFromSet_NSUV" not in pm.env.optionVars: pm.optionVar["copyFromSet_NSUV"] = None
    if "copyToSet_NSUV" not in pm.env.optionVars: pm.optionVar["copyToSet_NSUV"] = None

    # UV pinning
    if "polyPinUVVal_NSUV" not in pm.env.optionVars: pm.optionVar["polyPinUVVal_NSUV"] = 1.0

    # Unfold3d
    if "unfoldBrushSizeOrg_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldBrushSizeOrg_NSUV"] = False
    if "unfoldBrushSizeOverride_NSUV" not in pm.env.optionVars: pm.optionVar["unfoldBrushSizeOverride_NSUV"] = False
    if "uvBrushMode_NSUV" not in pm.env.optionVars: pm.optionVar["uvBrushMode_NSUV"] = ""
    if "uvBrushLastMode_NSUV" not in pm.env.optionVars: pm.optionVar["uvBrushLastMode_NSUV"] = ""
    
    # Layout
    if "layoutMode_NSUV" not in pm.env.optionVars: pm.optionVar["layoutMode_NSUV"] = 1
    if "layoutPackMode_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPackMode_NSUV"] = 1
    if "layoutRes_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRes_NSUV"] = 256
    if "layoutItr_NSUV" not in pm.env.optionVars: pm.optionVar["layoutItr_NSUV"] = 1
    if "layoutShell_NSUV" not in pm.env.optionVars: pm.optionVar["layoutShell_NSUV"] = 2
    if "layoutMultiTile_NSUV" not in pm.env.optionVars: pm.optionVar["layoutMultiTile_NSUV"] = False
    if "layoutGridUVal_NSUV" not in pm.env.optionVars: pm.optionVar["layoutGridUVal_NSUV"] = 1
    if "layoutGridVVal_NSUV" not in pm.env.optionVars: pm.optionVar["layoutGridVVal_NSUV"] = 1
    if "layoutSepShells_NSUV" not in pm.env.optionVars: pm.optionVar["layoutSepShells_NSUV"] = 2
    if "layoutFlip_NSUV" not in pm.env.optionVars: pm.optionVar["layoutFlip_NSUV"] = True
    if "layoutTranslate_NSUV" not in pm.env.optionVars: pm.optionVar["layoutTranslate_NSUV"] = True
    if "layoutDistr_NSUV" not in pm.env.optionVars: pm.optionVar["layoutDistr_NSUV"] = 1
    if "layoutRotate_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRotate_NSUV"] = False
    if "layoutRotateOld_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRotateOld_NSUV"] = 2
    if "layoutRotStep_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRotStep_NSUV"] = 90
    if "layoutRotMin_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRotMin_NSUV"] = 0.0000
    if "layoutRotMax_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRotMax_NSUV"] = 360.0000
    if "layoutScaling_NSUV" not in pm.env.optionVars: pm.optionVar["layoutScaling_NSUV"] = 2
    if "layoutFitting_NSUV" not in pm.env.optionVars: pm.optionVar["layoutFitting_NSUV"] = 2
    if "layoutPreXformFrame_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPreXformFrame_NSUV"] = True
    if "layoutPreRotation_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPreRotation_NSUV"] = 1
    if "layoutPreScaling_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPreScaling_NSUV"] = 1
    if "layoutSpacingFrame_NSUV" not in pm.env.optionVars: pm.optionVar["layoutSpacingFrame_NSUV"] = True
    if "layoutSpaceMenu_NSUV" not in pm.env.optionVars: pm.optionVar["layoutSpaceMenu_NSUV"] = 5
    if "layoutShellPadding_NSUV" not in pm.env.optionVars: pm.optionVar["layoutShellPadding_NSUV"] = 0.0000
    if "layoutShellPaddingOld_NSUV" not in pm.env.optionVars: pm.optionVar["layoutShellPaddingOld_NSUV"] = 0.2000
    if "layoutTilePadding_NSUV" not in pm.env.optionVars: pm.optionVar["layoutTilePadding_NSUV"] = 0.0
    if "layoutPlacementFrame_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPlacementFrame_NSUV"] = False
    if "layoutPlace_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPlace_NSUV"] = 1
    if "layoutRangeMinU_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRangeMinU_NSUV"] = 0.0
    if "layoutRangeMaxU_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRangeMaxU_NSUV"] = 1.0
    if "layoutRangeMinV_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRangeMinV_NSUV"] = 0.0
    if "layoutRangeMaxV_NSUV" not in pm.env.optionVars: pm.optionVar["layoutRangeMaxV_NSUV"] = 1.0
    if "layoutPlacePres_NSUV" not in pm.env.optionVars: pm.optionVar["layoutPlacePres_NSUV"] = 1
    if "layoutQuickType_NSUV" not in pm.env.optionVars: pm.optionVar["layoutQuickType_NSUV"] = 1

    # Distribute
    if "distrMethod_NSUV" not in pm.env.optionVars: pm.optionVar["distrMethod_NSUV"] = 1
    if "distrDir_NSUV" not in pm.env.optionVars: pm.optionVar["distrDir_NSUV"] = 1
    if "distrSpacing_NSUV" not in pm.env.optionVars: pm.optionVar["distrSpacing_NSUV"] = True
    if "distrFromManip_NSUV" not in pm.env.optionVars: pm.optionVar["distrFromManip_NSUV"] = True
    if "distrSpaceVal_NSUV" not in pm.env.optionVars: pm.optionVar["distrSpaceVal_NSUV"] = 0.0000

    # Auto seams
    if "autoSeamOperation_NSUV" not in pm.env.optionVars: pm.optionVar["autoSeamOperation_NSUV"] = 1
    if "autoSeamSegment_NSUV" not in pm.env.optionVars: pm.optionVar["autoSeamSegment_NSUV"] = 0.0
    if "autoSeamPipeCut_NSUV" not in pm.env.optionVars: pm.optionVar["autoSeamPipeCut_NSUV"] = True


# Resets all
def reset():

    userResponse = pm.confirmDialog(
        button=["Yes", "No"],
        cancelButton="No",
        defaultButton="No",
        dismissString="No",
        message="Do you really want to reset all NSUV settings? Action is irreversible!", 
        title="Reset NSUV settings",
    )
    
    if userResponse == "No":
        pass
    else:
        pm.optionVar["mayaVer_NSUV"] = pm.about(api=True)
        pm.optionVar["popupType_NSUV"] = 0
        pm.optionVar["sizeableWin_NSUV"] = False
        pm.optionVar["totdCounter_NSUV"] = int(1)
        pm.optionVar["totd_NSUV"] = True
        pm.optionVar["welcome_NSUV"] = True
    
        pm.optionVar["tabs_NSUV"] = 1
        pm.optionVar["tMode_NSUV"] = 1
    
        pm.optionVar["frame1_NSUV"] = False
        pm.optionVar["frame2_NSUV"] = False
        pm.optionVar["frame3_NSUV"] = False
        pm.optionVar["frame4_NSUV"] = False
        pm.optionVar["frame5_NSUV"] = False
        pm.optionVar["frame6_NSUV"] = False
        pm.optionVar["frame7_NSUV"] = False
        pm.optionVar["frame8_NSUV"] = False
        
        pm.optionVar["toolbarState_NSUV"] = True
        pm.optionVar["showStatusTools_NSUV"] = 1
        pm.optionVar["showStatusPinning_NSUV"] = 1
        pm.optionVar["showStatusSelection_NSUV"] = 1
        pm.optionVar["showStatusIsolateSelect_NSUV"] = 1
        pm.optionVar["showStatusCopyPasteDel_NSUV"] = 1
        
        pm.optionVar["imgDisp_NSUV"] = True
        pm.optionVar["imgDim_NSUV"] = False
        pm.optionVar["shellShade_NSUV"] = True
        pm.optionVar["shellBorder_NSUV"] = False
        pm.optionVar["shellDist_NSUV"] = False
        pm.optionVar["checkers_NSUV"] = False
        pm.optionVar["imgFilter_NSUV"] = True
        pm.optionVar["imgRGBA_NSUV"] = False
        pm.optionVar["gridDisp_NSUV"] = True
        pm.optionVar["pxSnap_NSUV"] = False
        pm.optionVar["editorBaking_NSUV"] = True
        pm.optionVar["imgRatio_NSUV"] = False
        pm.optionVar["frontColor_NSUV"] = [0, 0, 1]
        pm.optionVar["frontAlpha_NSUV"] = 0.25
        pm.optionVar["backColor_NSUV"] = [1, 0, 0]
        pm.optionVar["backAlpha_NSUV"] = 0.25
        pm.optionVar["colorMan_NSUV"] = False
        pm.optionVar["expField_NSUV"] = 0.00
        pm.optionVar["gamField_NSUV"] = 1.00
        pm.optionVar["expToggle_NSUV"] = False
        pm.optionVar["gamToggle_NSUV"] = False 
        pm.optionVar["vtName_NSUV"] = "sRGB gamma"
        pm.optionVar["isoSelect_NSUV"] = False
        pm.optionVar["tileLabels_NSUV"] = True
        pm.optionVar["containedFaces_NSUV"] = False
        pm.optionVar["connectedFaces_NSUV"] = False
        pm.optionVar["viewFaces_NSUV"] = False
        
        pm.optionVar["absToggle_NSUV"] = False
        pm.optionVar["compSpace_NSUV"] = 0
        pm.optionVar["manipAmt_NSUV"] = 1.0
        pm.optionVar["manipCoords_NSUV"] = [0.0, 0.0]
        pm.optionVar["manipVarA_NSUV"] = 0.0
        pm.optionVar["manipVarB_NSUV"] = 0.0
        pm.optionVar["manipVarC_NSUV"] = 0.0

        pm.optionVar["matchTol_NSUV"] = 0.005
        
        pm.optionVar["mapAutoMethod_NSUV"] = 1
        pm.optionVar["mapAutoMSMenu_NSUV"] = 6
        pm.optionVar["mapAutoMS1RadGrp_NSUV"] = 2
        pm.optionVar["mapAutoMS2RadGrp_NSUV"] = 1
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
        pm.optionVar["mapAutoFrame1_NSUV"] = True
        pm.optionVar["mapAutoFrame2_NSUV"] = True
        
        pm.optionVar["mapCylindricalMS1Box_NSUV"] = True
        pm.optionVar["mapCylindricalMS2Box_NSUV"] = True
        pm.optionVar["mapCylindricalSetBox_NSUV"] = False
        pm.optionVar["mapCylindricalSet_NSUV"] = "uvSet1"
        pm.optionVar["mapCylindricalSweep_NSUV"] = 180
        pm.optionVar["mapCylindricalFrame1_NSUV"] = True 
        
        pm.optionVar["mapNormalMS1_NSUV"] = False
        pm.optionVar["mapNormalMS2_NSUV"] = True
        pm.optionVar["mapNormalMS3_NSUV"] = True
        pm.optionVar["mapNormalSetBox_NSUV"] = False
        pm.optionVar["mapNormalSet_NSUV"] = "uvSet1"
        pm.optionVar["mapNormalFrame1_NSUV"] = True
        
        pm.optionVar["mapPlanarMethod_NSUV"] = 1 
        pm.optionVar["mapPlanarMS1RadGrp_NSUV"] = 2
        pm.optionVar["mapPlanarMS2RadGrp_NSUV"] = 1
        pm.optionVar["mapPlanarMS1Box_NSUV"] = True
        pm.optionVar["mapPlanarMS2Box_NSUV"] = True
        pm.optionVar["mapPlanarMS3Box_NSUV"] = True
        pm.optionVar["mapPlanarSetBox_NSUV"] = False
        pm.optionVar["mapPlanarSet_NSUV"] = "uvSet1"
        pm.optionVar["mapPlanarFrame1_NSUV"] = True
        
        pm.optionVar["mapSphericalMS1Box_NSUV"] = True
        pm.optionVar["mapSphericalSetBox_NSUV"] = False
        pm.optionVar["mapSphericalMS2Box_NSUV"] = True
        pm.optionVar["mapSphericalSet_NSUV"] = "uvSet1"
        pm.optionVar["mapSphericalSweep1_NSUV"] = 180
        pm.optionVar["mapSphericalSweep2_NSUV"] = 90
        pm.optionVar["mapSphericalFrame1_NSUV"] = True
        
        pm.optionVar["normMethod_NSUV"] = 1
        pm.optionVar["normAspect_NSUV"] = 1
        pm.optionVar["normDirection_NSUV"] = 1
        pm.optionVar["normSetBox_NSUV"] = False
        pm.optionVar["normSet_NSUV"] = "uvSet1"
        pm.optionVar["normFrame1_NSUV"] = True
        
        pm.optionVar["randT_NSUV"] = 0.1
        pm.optionVar["randTBox1_NSUV"] = True
        pm.optionVar["randTBox2_NSUV"] = True
        pm.optionVar["randR_NSUV"] = 22.5
        pm.optionVar["randRBox1_NSUV"] = False
        pm.optionVar["randRBox2_NSUV"] = False
        pm.optionVar["randS_NSUV"] = 5.0
        pm.optionVar["randSBox1_NSUV"] = False
        pm.optionVar["randSBox2_NSUV"] = False
        
        pm.optionVar["relaxMethod_NSUV"] = 1
        pm.optionVar["relaxItr_NSUV"] = 1
        pm.optionVar["relaxAngle_NSUV"] = 1.0
        pm.optionVar["relaxPower_NSUV"] = 100
        pm.optionVar["relaxBorder_NSUV"] = True
        pm.optionVar["relaxFlips_NSUV"] = True
        pm.optionVar["relaxSize_NSUV"] = 1024
        pm.optionVar["relaxSpacing_NSUV"] = 2
        pm.optionVar["relaxPinBorder_NSUV"] = False
        pm.optionVar["relaxPin_NSUV"] = False
        pm.optionVar["relaxPinType_NSUV"] = 1
        pm.optionVar["relaxEdge_NSUV"] = 1
        pm.optionVar["relaxMaxItr_NSUV"] = 5
        
        dir = pm.workspace(query=True, rootDirectory=True) + "images/outUV"
        pm.optionVar["shotUVpath_NSUV"] = dir
        
        pm.optionVar["shotUVxSize_NSUV"] = 1024
        pm.optionVar["shotUVySize_NSUV"] = 1024
        pm.optionVar["shotUVaa_NSUV"] = 0
        pm.optionVar["shotUVcolor_NSUV"] = [ 1.0, 1.0, 1.0 ]
        pm.optionVar["shotUVformat_NSUV"] = "Maya IFF"
        pm.optionVar["snapshotMultiTile_NSUV"] = False
        pm.optionVar["snapshotGridUVal_NSUV"] = 1
        pm.optionVar["snapshotGridVVal_NSUV"] = 1
        pm.optionVar["shotUVrange_NSUV"] = 1
        pm.optionVar["shotUVtype_NSUV"] = 1
        
        pm.optionVar["storedSelA_NSUV"] = ""
        pm.optionVar["storedSelB_NSUV"] = ""
        
        pm.optionVar["strUVsAngle_NSUV"] = 30
        pm.optionVar["strUVsType_NSUV"] = 0
        
        pm.optionVar["td_NSUV"] = 32
        pm.optionVar["tdSize_NSUV"] = 512
        pm.optionVar["manipVarTDA1_NSUV"] = 32.0
        pm.optionVar["manipVarTDA2_NSUV"] = 512
        pm.optionVar["manipVarTDB1_NSUV"] = 32.0
        pm.optionVar["manipVarTDB2_NSUV"] = 512
        
        pm.optionVar["unfoldMethod_NSUV"] = 1
        pm.optionVar["unfoldItr_NSUV"] = 1 
        pm.optionVar["unfoldPack_NSUV"] = True
        pm.optionVar["unfoldBorder_NSUV"] = True
        pm.optionVar["unfoldFlips_NSUV"] = True
        pm.optionVar["unfoldSize_NSUV"] = 1024
        pm.optionVar["unfoldSpaceVal_NSUV"] = 2
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
        
        pm.optionVar["copyNewUVSet_NSUV"] = "map2"
        pm.optionVar["newUVSet_NSUV"] = "map2"
        pm.optionVar["newUVSetShare_NSUV"] = 1
        pm.optionVar["scrollList_NSUV"] = ""
        pm.optionVar["copyFromSet_NSUV"] = None
        pm.optionVar["copyToSet_NSUV"] = None
        
        pm.optionVar["polyPinUVVal_NSUV"] = 1.0
  
        pm.optionVar["unfoldBrushSizeOrg_NSUV"] = False
        pm.optionVar["unfoldBrushSizeOverride_NSUV"] = False
        pm.optionVar["uvBrushMode_NSUV"] = ""
        pm.optionVar["uvBrushLastMode_NSUV"] = ""
        
        pm.optionVar["layoutMode_NSUV"] = 1 
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
        pm.optionVar["layoutTilePadding_NSUV"] = 0.0000  
        pm.optionVar["layoutPlacementFrame_NSUV"] = False
        pm.optionVar["layoutPlace_NSUV"] = 1
        pm.optionVar["layoutRangeMinU_NSUV"] = 0.0
        pm.optionVar["layoutRangeMaxU_NSUV"] = 1.0
        pm.optionVar["layoutRangeMinV_NSUV"] = 0.0
        pm.optionVar["layoutRangeMaxV_NSUV"] = 1.0        
        pm.optionVar["layoutPlacePres_NSUV"] = 1
        pm.optionVar["layoutQuickType_NSUV"] = 1
        
        pm.optionVar["distrMethod_NSUV"] = 1
        pm.optionVar["distrDir_NSUV"] = 1
        pm.optionVar["distrSpacing_NSUV"] = True
        pm.optionVar["distrFromManip_NSUV"] = True
        pm.optionVar["distrSpaceVal_NSUV"] = 0.0000

        pm.optionVar["autoSeamOperation_NSUV"] = 1
        pm.optionVar["autoSeamSegment_NSUV"] = 0.0
        pm.optionVar["autoSeamPipeCut_NSUV"] = True

        # Restart NSUV
        pm.confirmDialog(
            button=["Yes"],
            cancelButton="Yes",
            defaultButton="Yes",
            dismissString="Yes",
            message="Settings resetted. Please close down and restart NSUV.",
            title="Reset complete",
        )