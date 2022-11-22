#------------------------------------------------------------------nuke-
# file: sag_bugSetup.py
# version: 0.1
# date: 2014.02.20
# author: Arkadiy Demchenko (sagroth@sigillarium.com)
#-----------------------------------------------------------------------
# 2014.02.20 (v0.7) - main release
#-----------------------------------------------------------------------
# Takes locators from FBX named with _# at the end (_1, _11, _111) and
# creates a card and lights setup for lightning bugs.
#-----------------------------------------------------------------------

import nuke

def sag_bugsSetup():
# BROWSER DIALOG
	fileName = nuke.getFilename( 'Get FBX File', '*.fbx' )

# START GROUPING ALL NODES
	allNodes = []
	grp = nuke.createNode( 'Group' )
	grp.setName( 'bugs_1' )

	grp.begin()

# CAMERA INPUT
	camInput = nuke.nodes.Input( name = 'cam' )
	allNodes.append( camInput )

# INPUT FOR THE BUG IMAGE
	imgInput = nuke.nodes.Input( name = 'bug' )
	addZ = nuke.nodes.AddChannels()
	addZ[ 'channels' ].setValue( 'mask.a' )
	addZ.setInput( 0, imgInput )
	allNodes.append( imgInput )
	allNodes.append( addZ )

# CREATE AXIS WITH DATA FROM FBX TO GET THE LIST OF LOCATORS
	axMain = nuke.nodes.Axis2( name = 'bug_master', read_from_file = True, frame_rate = 25, file = fileName )
	axMain.metadata()
	allLocs = axMain[ 'fbx_node_name' ].values()
	allNodes.append( axMain )

# ADDITIONAL CONTROLS
	scaleGlobal = nuke.Double_Knob( 'scaleGlobal', 'Global Scale' )
	axMain.addKnob( scaleGlobal )
	scaleGlobal.setValue( 1.5 )

	clrVar = nuke.Double_Knob( 'clrVar', 'Color Variation' )
	axMain.addKnob( clrVar )
	clrVar.setValue( 0.5 )

	gain = nuke.Double_Knob( 'gain', 'Global Brightness' )
	axMain.addKnob( gain )
	gain.setValue( 1 )

	flicker = nuke.Double_Knob( 'flicker', 'Flickering' )
	axMain.addKnob( flicker )
	flicker.setValue( 0.5 )

	flickerFreq = nuke.Double_Knob( 'flickerFreq', 'Flickering Frequency' )
	axMain.addKnob( flickerFreq )
	flickerFreq.setValue( 1 )

	bugInt = nuke.Double_Knob( 'bugInt', 'Illumination Intensity' )
	axMain.addKnob( bugInt )
	bugInt.setValue( 500 )

	falloff = nuke.Enumeration_Knob( 'falloff', 'Illumination Falloff', ['No Falloff', 'Linear', 'Quadratic', 'Cubic'] )
	axMain.addKnob( falloff )
	falloff.setValue( 3 )

	illumClamp = nuke.Double_Knob( 'illumClamp', 'Illumination Clamp' )
	axMain.addKnob( illumClamp )
	illumClamp.setValue( 0.001 )

	illumSoften = nuke.Int_Knob( 'illumSoften', 'Softening' )
	axMain.addKnob( illumSoften )
	illumSoften.setValue( 2 )

	smp = nuke.Int_Knob( 'smp', 'Samples' )
	axMain.addKnob( smp )
	smp.setValue( 20 )

	sht = nuke.Double_Knob( 'sht', 'Shutter' )
	axMain.addKnob( sht )
	sht.setValue( 2 )

	zMerge = nuke.Boolean_Knob( 'zmerge', 'Depth Masking' )
	axMain.addKnob( zMerge )
	zMerge.setValue( True )

	zDil = nuke.Double_Knob( 'zdilate', 'Expand Depth' )
	axMain.addKnob( zDil )
	zDil.setValue( 20 )

# CREATE AXES AND OTHER SETUP NODES AND CONNECT EVERYTHING
	axes = []
	grades = []
	depths = []
	cards = []
	lights = []
	for loc in allLocs:
		ind = loc.split( '_' )[-1]
		typ = loc.split( '_' )[-2]

		ax = nuke.nodes.Axis2( name = 'bug_axis_' + typ + '_' + ind, read_from_file = True )
		ax[ 'file' ].setValue( '[value ' + axMain.fullName() + '.file]' )
		ax[ 'frame_rate' ].setExpression( axMain.fullName() + '.frame_rate' )
		ax[ 'read_from_file' ].setExpression( axMain.fullName() + '.read_from_file' )
		ax.metadata()
		ax[ 'fbx_node_name' ].setValue( loc )
		axes.append( ax )

		# FORCE RELOAD DATA
		cl = nuke.clone( ax )
		cl.metadata()
		nuke.delete( cl )

		# GRADE
		grd = nuke.nodes.Grade( name = 'bug_grade_' + typ + '_' + ind, channels = 'rgba' )
		grd[ 'white' ].setExpression( axMain.fullName() + '.gain * (clamp(' + ax.fullName() + '.scaling.x, 0.001, 1.0)-0.001) + (random(' + ind + ' + frame * ' + axMain.fullName() + '.flickerFreq) * ' + axMain.fullName() + '.flicker - (' + axMain.fullName() + '.flicker * 0.5))' )
		grd[ 'multiply' ].setValue( [1, 1, 1, 1] )
		grd[ 'multiply' ].setExpression( '1 - random(' + ind + ' + 10) * ' + axMain.fullName() + '.clrVar', 0 )
		grd[ 'multiply' ].setExpression( '1 - random(' + ind + ' + 20) * ' + axMain.fullName() + '.clrVar', 1 )
		grd[ 'multiply' ].setExpression( '1 - random(' + ind + ' + 30) * ' + axMain.fullName() + '.clrVar', 2 )
		grd.setInput( 0, addZ )
		grades.append( grd )

		# DEPTH
		grz = nuke.nodes.Grade( name = 'bug_depth_' + typ + '_' + ind )
		grz[ 'add' ].setExpression( 'sqrt(pow(parent.input0.translate.x - ' + ax.fullName() + '.translate.x, 2) + pow(parent.input0.translate.y - ' + ax.fullName() + '.translate.y, 2) + pow(parent.input0.translate.z - ' + ax.fullName() + '.translate.z, 2))' )
		grz.setInput( 0, grd )
		grz[ 'channels' ].setValue( 'mask' )
		depths.append( grz )

		# CARD
		crd = nuke.nodes.Card2( name = 'bug_card_' + typ + '_' + ind, rows = 1, columns = 1, orientation = 'YZ' )
		crd[ 'translate' ].setExpression( ax.fullName() + '.translate' )
		crd[ 'uniform_scale' ].setExpression( axMain.fullName() + '.scaleGlobal' )
		crd.setInput( 0, grz )
		cards.append( crd )

		# LIGHT
		lgt = nuke.nodes.Light2( name = 'bug_light_' + typ + '_' + ind )
		lgt[ 'color' ].setValue( [1, 1, 1] )
		lgt[ 'color' ].setExpression( grd.fullName() + '.multiply' )
		lgt[ 'intensity' ].setExpression( axMain.fullName() + '.bugInt * ' + ax.fullName() + '.scaling.x' )
		lgt[ 'falloff_type' ].setExpression( axMain.fullName() + '.falloff' )
		lgt[ 'translate' ].setExpression( ax.fullName() + '.translate' )
		lights.append( lgt )

# CREATE SCENE NODES
	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
	for crd in cards:
		crd.setSelected( True )
	crdScene = nuke.createNode( 'Scene' )
	crdScene.setName( 'bug_cards_scene' )

	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
	for lgt in lights:
		lgt.setSelected( True )
	lgtScene = nuke.createNode( 'Scene' )
	lgtScene.setName( 'bug_lights_scene' )

# BUGS COLOR
	rndColor = nuke.nodes.ScanlineRender( motion_vectors_type = 'off', MB_channel = 'none' )
	rndColor[ 'samples' ].setExpression( axMain.fullName() + '.smp' )
	rndColor[ 'shutter' ].setExpression( axMain.fullName() + '.sht' )
	rndColor.setInput( 1, crdScene )
	rndColor.setInput( 2, camInput )

# BUGS DEPTH
	rndDepth = nuke.nodes.ScanlineRender( transparency = False, ztest_enabled = False, filter = 'Impulse', motion_vectors_type = 'off', MB_channel = 'none' )
	rndDepth.setInput( 1, crdScene )
	rndDepth.setInput( 2, camInput )

	copyZ = nuke.nodes.Copy()
	copyZ.setInput( 0, rndColor )
	copyZ.setInput( 1, rndDepth )
	copyZ[ 'from0' ].setValue( 'mask.a' )
	copyZ[ 'to0' ].setValue( 'depth.Z' )
	copyZ[ 'from1' ].setValue( 'mask.a' )
	copyZ[ 'to1' ].setValue( 'mask.a' )

	zDilate = nuke.nodes.Dilate()
	zDilate[ 'size' ].setExpression( axMain.fullName() + '.zdilate' )
	zDilate.setInput( 0, copyZ )
	zDilate[ 'channels' ].setValue( 'depth' )

# DEPTH MASKING
	bgInput = nuke.nodes.Input( name = 'bg' )
	blackBG = nuke.nodes.Grade( channels = 'rgba', white = 0 )
	blackBG.setInput( 0, bgInput )
	zMrg = nuke.nodes.ZMerge( alpha_channel = 'none' )
	zMrg[ 'disable' ].setExpression( '1 - ' + axMain.fullName() + '.zmerge' )
	zMrg.setInput( 0, zDilate )
	zMrg.setInput( 1, blackBG )

# MASKED DEPTH
	mskDilate = nuke.nodes.Dilate()
	mskDilate[ 'size' ].setExpression( axMain.fullName() + '.zdilate' )
	mskDilate.setInput( 0, zMrg )
	mskDilate[ 'channels' ].setValue( 'mask' )

	copyMsk = nuke.nodes.Copy()
	copyMsk[ 'disable' ].setExpression( '1 - ' + axMain.fullName() + '.zmerge' )
	copyMsk.setInput( 0, zMrg )
	copyMsk.setInput( 1, mskDilate )
	copyMsk[ 'from0' ].setValue( 'mask.a' )
	copyMsk[ 'to0' ].setValue( 'depth.Z' )

# ILLUMINATION
	interpIllum1 = nuke.nodes.Reformat( type = 'scale' )
	interpIllum1[ 'scale' ].setExpression( axMain.fullName() + '.illumSoften' )
	interpIllum1.setInput( 0, bgInput )
	interpIllum2 = nuke.nodes.Grade( black_clamp = False )
	interpIllum2.setInput( 0, interpIllum1 )
	interpIllum3 = nuke.nodes.Reformat( type = 'scale' )
	interpIllum3[ 'scale' ].setExpression( '1/' + axMain.fullName() + '.illumSoften' )
	interpIllum3.setInput( 0, interpIllum2 )

	nrmLay = nuke.Layer( 'Normal', [ 'Normal.NX', 'Normal.NY', 'Normal.NZ' ] )
	sc2Lay = nuke.Layer( 'tk_specialC2', [ 'tk_specialC2.red', 'tk_specialC2.green', 'tk_specialC2.blue' ] )
	illumLay = nuke.Layer( 'bug_illum', [ 'bug_illum.red', 'bug_illum.green', 'bug_illum.blue' ] )

	shd = nuke.nodes.Phong( diffuse = 2, specular = 0 )
	rel = nuke.nodes.ReLight()
	rel.setInput( 0, interpIllum3 )
	rel.setInput( 1, lgtScene )
	rel.setInput( 2, camInput )
	rel.setInput( 3, shd )
	rel[ 'normal' ].setValue( 'Normal' )
	rel[ 'position' ].setValue( 'tk_specialC2' )

	relClamp = nuke.nodes.Clamp( channels = 'rgb', maximum_enable = False, MinClampTo_enable = True )
	relClamp[ 'minimum' ].setExpression( axMain.fullName() + '.illumClamp' )
	relClamp.setInput( 0, rel )

	copyIllum = nuke.nodes.Copy()
	copyIllum.setInput( 0, copyMsk )
	copyIllum.setInput( 1, relClamp )
	copyIllum[ 'from0' ].setValue( 'rgba.red' )
	copyIllum[ 'from1' ].setValue( 'rgba.green' )
	copyIllum[ 'from2' ].setValue( 'rgba.blue' )
	copyIllum[ 'to0' ].setValue( 'bug_illum.red' )
	copyIllum[ 'to1' ].setValue( 'bug_illum.green' )
	copyIllum[ 'to2' ].setValue( 'bug_illum.blue' )

# OUTPUT
	cleanChan = nuke.nodes.Remove( channels = 'mask' )
	cleanChan.setInput( 0, copyIllum )
	out = nuke.nodes.Output()
	out.setInput( 0, cleanChan )

# GROUP EVERYTHING
	allNodes += axes + cards + lights + grades + depths + [crdScene, lgtScene, out]

	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
	for each in allNodes:
		each.setSelected( True )

	grp.end()

# EXTERNAL CONTROLS
	lnk = nuke.Link_Knob( 'read_from_file_link', 'Read From File' )
	lnk.makeLink( 'bug_master', 'read_from_file' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'file_link', 'File' )
	lnk.makeLink( 'bug_master', 'file' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'frame_rate_link', 'Frame Rate' )
	lnk.makeLink( 'bug_master', 'frame_rate' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'reload_link', 'Reload' )
	lnk.makeLink( 'bug_master', 'reload' )
	grp.addKnob( lnk )

	div = nuke.Text_Knob( 'div1', '', '' )
	grp.addKnob( div )

	lnk = nuke.Link_Knob( 'scaleGlobal_link', 'Global Scale' )
	lnk.makeLink( 'bug_master', 'scaleGlobal' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'clrVar_link', 'Color Variation' )
	lnk.makeLink( 'bug_master', 'clrVar' )
	grp.addKnob( lnk )

	div = nuke.Text_Knob( 'div5', '', '' )
	grp.addKnob( div )

	lnk = nuke.Link_Knob( 'gain_link', 'Global Brightness' )
	lnk.makeLink( 'bug_master', 'gain' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'flicker_link', 'Flickering' )
	lnk.makeLink( 'bug_master', 'flicker' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'flickerFreq_link', 'Flickering Frequency' )
	lnk.makeLink( 'bug_master', 'flickerFreq' )
	grp.addKnob( lnk )

	div = nuke.Text_Knob( 'div2', '', '' )
	grp.addKnob( div )

	lnk = nuke.Link_Knob( 'bugInt_link', 'Illumination Intensity' )
	lnk.makeLink( 'bug_master', 'bugInt' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'falloff_link', 'Illumination Falloff' )
	lnk.makeLink( 'bug_master', 'falloff' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'illumClamp_link', 'Illumination Clamp' )
	lnk.makeLink( 'bug_master', 'illumClamp' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'illumSoften_link', 'Softening' )
	lnk.makeLink( 'bug_master', 'illumSoften' )
	grp.addKnob( lnk )

	div = nuke.Text_Knob( 'div3', '', '' )
	grp.addKnob( div )

	lnk = nuke.Link_Knob( 'smp_link', 'Motion Samples' )
	lnk.makeLink( 'bug_master', 'smp' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'sht_link', 'Shutter' )
	lnk.makeLink( 'bug_master', 'sht' )
	grp.addKnob( lnk )

	div = nuke.Text_Knob( 'div4', '', '' )
	grp.addKnob( div )

	lnk = nuke.Link_Knob( 'zmerge_link', 'Depth Masking' )
	lnk.makeLink( 'bug_master', 'zmerge' )
	grp.addKnob( lnk )

	lnk = nuke.Link_Knob( 'zdilate_link', 'Expand Depth' )
	lnk.makeLink( 'bug_master', 'zdilate' )
	grp.addKnob( lnk )

# DISABLE READING FROM FBX
	grp[ 'read_from_file_link' ].setValue( False )

# SELECT GROUP
	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
	grp.setSelected( True )
