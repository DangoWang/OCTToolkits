# -*- coding: utf-8 -*-
"""

    Package initiation for Nightshade UV Editor (NSUV) v2.1.3

    NSUV offers extended utility to Maya´s native UV Editor.
    Made by Martin (Nightshade) Dahlin - martin.dahlin@live.com - martin.dahlin.net

    Special thanks to:
    Nathan Roberts, Robert Kovach, David Johnson and Viktoras Makauskas on CGTalk, 
    Robert White and Steve Theodore on Tech-Artists.org
    Anton Palmqvist, Malcolm Andrieshyn and my friends Alexander Lilja and Elin Rudén
    for all the feedback, criticism, bug reports and feature ideas. 
    Thank you all!

"""

## Initialize

import pymel.core as pm

# Option vars
import optVars as vars
vars.create()

# Set version name and filename of the PDF manual
pm.optionVar["editorTitle_NSUV"] = "Nightshade UV Editor Pro v2.1.3"
pm.optionVar["manual_NSUV"] = "Nightshade UV Editor 2.1 - User Manual.pdf"

# Plugins/Contexts
if pm.optionVar["mayaVer_NSUV"] >= 201600:

    # Load Unfold3D and toggle autoloading
    if not pm.pluginInfo("Unfold3D", loaded=True, query=True):
        pm.loadPlugin("Unfold3D")
        pm.pluginInfo("Unfold3D", edit=True, autoload=True)
        pm.pluginInfo("Unfold3D", savePluginPrefs=True)

    # Running pm.mel due to backwards compability
    if not pm.mel.Unfold3DContext("-exists", "texUnfoldUVContext"):
        pm.mel.Unfold3DContext("texUnfoldUVContext")
        pm.mel.initUVSculptTool()

    if pm.optionVar["mayaVer_NSUV"] >= 201650: # 2016 ext2

        # Load modelling toolkit and toggle autoloading
        if not pm.pluginInfo("modelingToolkit", loaded=True, query=True):
            pm.loadPlugin("modelingToolkit")
            pm.pluginInfo("modelingToolkit", edit=True, autoload=True)
            pm.pluginInfo("modelingToolkit", savePluginPrefs=True)

        if not pm.mel.SymmetrizeUVContext("-exists", "texSymmetrizeUVContext"):
            pm.mel.SymmetrizeUVContext("texSymmetrizeUVContext")
            pm.mel.initUVSculptTool()

# Callbacks (for the scriptedPanel
pm.scriptedPanelType(
    "polyTexturePlacementPanel", edit=True,
        addCallback="addTextureWindow_NSUV",
        createCallback="createTextureWindow_NSUV",
        removeCallback="removeTextureWindow_NSUV",
        )


## Startup

# Import and create UI
import UI as UI
pm.mel.source("NSUV/callbacks.mel") # Sadly, scripted Panels can only have MEL-callbacks
UI.createUI()

# Create tip of the day UI
if pm.optionVar["totd_NSUV"] == True:
    UI.totdUI()

# Create Welcome screen
if pm.optionVar["welcome_NSUV"] == True:
    UI.welcomeUI()