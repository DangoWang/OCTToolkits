import nuke
import math

def sag_exportExrChans_remove( chans ):
	rems = []
	for i in xrange( int( math.ceil( len( chans ) / 4.0 ) ) ):
		rem = nuke.nodes.Remove( operation = 'remove' )
		if rems != []:
			rem.setInput( 0, rems[-1] )

		rem[ 'channels' ].setValue( chans[i*4] )
		if len( chans ) > i*4+1:
			rem[ 'channels2' ].setValue( chans[i*4+1] )
		if len( chans ) > i*4+2:
			rem[ 'channels3' ].setValue( chans[i*4+2] )
		if len( chans ) > i*4+3:
			rem[ 'channels4' ].setValue( chans[i*4+3] )

		rems.append( rem )

	return rems


def sag_exportExrChans():
	selList = nuke.selectedNodes( 'Read' )

	for each in nuke.selectedNodes():
		each.setSelected( False )

	outs = []
	allNodes = []
	for each in selList:
		chans = list( set( [chan.split( '.' )[0] for chan in each.channels()] ) )
		chans.sort()

		p = nuke.Panel( each.name() )
		for eachChan in chans:
			p.addBooleanCheckBox( eachChan, True )
		if not p.show():
			return

		chanDict = { 'beauty':[], 'passes':[], 'masks':[], 'motion':[], 'normals':[], 'depth':[], 'position':[] }
		for eachChan in chans:
			if eachChan == 'rgba' or eachChan == 'rgb' or eachChan == 'beauty':
				if p.value( eachChan ):
					chanDict[ 'beauty' ].append( eachChan )
			elif eachChan == 'Motion':
				if p.value( eachChan ):
					chanDict[ 'motion' ].append( eachChan )
			elif eachChan == 'Normal' or eachChan.find( 'bent' ) > -1:
				if p.value( eachChan ):
					chanDict[ 'normals' ].append( eachChan )
			elif eachChan == 'depth' or eachChan == 'Z' or eachChan == 'z' or eachChan == 'tk_z':
				if p.value( eachChan ):
					chanDict[ 'depth' ].append( eachChan )
			elif eachChan.find( 'specialC2' ) > -1 or eachChan == 'p':
				if p.value( eachChan ):
					chanDict[ 'position' ].append( eachChan )
			elif eachChan.find( 'specialC' ) > -1:
				if p.value( eachChan ):
					if eachChan.find( 'specialC1' ) > -1 and eachChan[-1] != '0':
						chanDict[ 'motion' ].append( eachChan )
					else:
						chanDict[ 'masks' ].append( eachChan )
			else:
				if p.value( eachChan ):
					chanDict[ 'passes' ].append( eachChan )

		inPath = each[ 'file' ].value()
		dir = inPath[:inPath.rfind( '/' )+1]
		filename = inPath.split( '/' )[-1].split( '.' )[0]

		for eachWrite in chanDict:
			if chanDict[ eachWrite ] != []:
				remChans = list( chans )

				for eachChan in chanDict[ eachWrite ]:
					remChans.remove( eachChan )

				if remChans != []:
					rems = sag_exportExrChans_remove( remChans )

					out = nuke.nodes.Write( channels = 'all', file_type = 'exr', autocrop = True, beforeFrameRender = 'import nuke, nukescripts;nukescripts.cache_clear("")' )

					rems[0].setInput( 0, each )
					out.setInput( 0, rems[-1] )
					out[ 'file' ].setValue( dir + eachWrite + '/' + filename + '_' + eachWrite + '.%04d.exr' )

					if eachWrite == 'depth' or eachWrite == 'position' or eachWrite == 'normals':
						out[ 'datatype' ].setValue( 1 )

					outs.append( out )
					allNodes += rems
					allNodes += [ out ]

		allNodes += [ each ]

	for eachNode in allNodes:
		eachNode.autoplace()

	for eachNode in nuke.selectedNodes():
		eachNode.setSelected( False )

	for eachOut in outs:
		eachOut.setSelected( True )
