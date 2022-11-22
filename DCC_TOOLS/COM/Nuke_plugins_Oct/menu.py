import nuke
import scripts
import WrapItUp
import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte_ui()



n = nuke.toolbar("Nodes")
ds_n = n.addMenu("MyGizmo", icon="glukoza.png")

#ds_n.addCommand( 'Submit To Deadline', 'scripts.sag_submitNukeToDeadline()', 'F6' )

ds_n.addSeparator()

nuke.load("ProEXR.py")
n.addCommand("MyGizmo/ProEXR", "ProEXR()","F2",icon="ProEXR.png")
ds_n.addCommand( 'AOV Tool', 'import aov_tools.aov_ui;wnd = aov_tools.aov_ui.AovWindow();wnd.show()', 'F3')

n.addCommand( "MyGizmo/ds_slate", "nuke.createNode('ds_slate')", "F4", icon="ds_slate.png")

n.addCommand( "MyGizmo/STMap_Generator", "nuke.createNode('STMap_Generator')", icon="STMap_Generator.png")

n.addCommand( "MyGizmo/Stereo_preview", "nuke.createNode('Stereo_preview')", icon="Stereo_preview.png")


n.addCommand( "MyGizmo/Cryptomatte", "nuke.createNode('Cryptomatte')", icon="Cryptomatte.png")

n.addCommand( "MyGizmo/DepthKeyer", "nuke.createNode('DepthKeyer')", icon="DepthKeyer.png")

n.addCommand( "MyGizmo/expressio-rays", "nuke.createNode('expressio-rays')", icon="expressio-rays.png")

n.addCommand( "MyGizmo/CompareView", "nuke.createNode('CompareView')", icon="CompareView.png")

n.addCommand( "MyGizmo/akromatism_stRub", "nuke.createNode('akromatism_stRub')", icon="akromatism_stRub.png")

n.addCommand( "MyGizmo/Displace", "nuke.createNode('Displace')", icon="Displace.png")

#n.addCommand( "Peregrine/pgBokeh", "nuke.createNode('pgBokeh')", icon="pgBokeh.png")


ds_n.addCommand( 'Expression Wave Generator', 'nuke.createNode( "ExpressionWaveGenerator" )' )

ds_n.addCommand( 'Open Explorer for Selected', 'scripts.sag_browseSelected()', 'ctrl+e' )


nuke.load("copy_images.py")
n.addCommand("MyGizmo/copy_images", "copy_images()",icon="copy_images.png")

#------------------------------------------------------------#

# IMAGE FORMATS
nuke.addFormat( ' 2048 858 1.0 DS_2k' )
nuke.addFormat( ' 1024 429 1.0 DS_1k' )

#------------------------------------------------------------#
nuke.knobDefault("Write.channels","rgba")
nuke.knobDefault("Roto.output","rgba")
nuke.knobDefault( 'Write.jpeg._jpeg_quality', '1' )
nuke.knobDefault( 'Write.jpeg._jpeg_sub_sampling', '4:4:4' )
nuke.knobDefault( 'Write.mov.meta_codec', 'rle' )
nuke.knobDefault( 'Write.mov.colorspace', 'sRGB' )
nuke.knobDefault( 'Root.format', 'DS_2k' )

nuke.knobDefault("Read.label",
                 "<font size=\"3\" color =#548DD4><b> Frame range :</b></font> "
                 "<font color = red>[value first] - [value last] </font>")

nuke.menu('Nuke').addCommand('Extra/Wrap It Up', "WrapItUp.WrapItUp()")







