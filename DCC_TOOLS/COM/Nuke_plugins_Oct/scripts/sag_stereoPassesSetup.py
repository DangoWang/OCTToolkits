import nuke
import nukescripts

def sag_stereoPassesSetup():
	stereoL = [ '_l_', '_l.', '_L_', '_L.' ]
	stereoR = [ '_r_', '_r.', '_R_', '_R.' ]
	stereoNames = stereoL + stereoR
	passInputs = { 'beauty':(0, (0, 224)), 'motion':(1, (110, 224)), 'normals':(3, (-110, 124)), 'masks':(4, (110, 24)), 'passes':(5, (110, 124)), 'depth':(6, (-110, 224)), 'position':(7, (-110, 24)) }

	selList = nuke.selectedNodes( 'Read' )

	# CHANGE STEREO VIEW IN READ PATHS AND COLLECT KNOWN PASSES
	nukescripts.stereo.setViewsForStereo()
	pack = {}
	for each in selList:
		filePath = each[ 'file' ].value()
		for eachName in stereoNames:
			if len( filePath.split( eachName ) ) > 1:
				if eachName in stereoR:
					nuke.delete( each )
				else:
					each[ 'file' ].setValue( filePath[:filePath.rfind( eachName )+1] + '%v' + filePath[filePath.rfind( eachName )+2:] )
					passName = filePath[filePath.rfind( eachName )+3:]
					passName = passName[:passName.find( '.' )]
					if passName in passInputs:
						pack[ each ] = passName

	# COMBINE KNOWN PASSES WITH A MERGE AND PLACE THEM NICELY
	if len( pack ) > 1:
		mrg = nuke.nodes.Merge2( Achannels = 'none', Bchannels = 'none', output = 'none', also_merge = 'all' )

		for each in pack:
			mrg.setInput( passInputs[pack[each]][0], each )

		pos = [ mrg.xpos(), mrg.ypos() ]
		for each in pack:
			each.setXYpos( pos[0] - passInputs[pack[each]][1][0], pos[1] - passInputs[pack[each]][1][1] )

	# DESELECT EVERYTHING
	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
