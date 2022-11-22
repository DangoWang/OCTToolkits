import nuke
import nukescripts

def sag_stereoPassesSetupCracked():
	passInputs = { 'beauty':(0, (0, 224)), 'motion':(1, (110, 224)), 'normals':(3, (-110, 124)), 'masks':(4, (110, 24)), 'passes':(5, (110, 124)), 'depth':(6, (-110, 224)), 'position':(7, (-110, 24)) }

	selList = nuke.selectedNodes( 'Read' )

	# KRIAKA-RASKORIAKA 
	nukescripts.stereo.setViewsForStereo()

	# COMBINE KNOWN PASSES WITH A MERGE AND PLACE THEM NICELY
	if 2 > 1:
		mrg = nuke.nodes.Merge2( Achannels = 'none', Bchannels = 'none', output = 'none', also_merge = 'all' )
		count = 4
		for each in selList:
			mrg.setInput( count, each )
			count = count + 1
		
		pos = [ mrg.xpos(), mrg.ypos() ]
		
		arr = sorted(passInputs.keys())
		count = 0
		for each in selList:
			each.setXYpos( pos[0] - passInputs[arr[count]][1][0], pos[1] - passInputs[arr[count]][1][1] )
			count = count + 1
		
	# DESELECT EVERYTHING
	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )
