import nuke
from string import zfill

def sag_slateTests():
	durList = {}

	f = open( 'X:/SAVVA/data/Ep_dur.txt', 'r' )
	for line in f:
		sht = line.split()
		durList[ sht[0] ] = int( sht[1] )
	f.close()

	selList = nuke.selectedNodes( filter = 'Read' )

	outList = []
	for each in selList:
		exr = each['file'].value()
		if exr[-4:] == '.exr':
			fr = int( exr.split( '.' )[-2] )
			spl = exr.split( '.' )[0].split( '/' )[-1].split( '_' )
			shot = spl[0] + '_' + spl[1] + '_' + spl[2]
			task = spl[3]
			ver = spl[4]

			nuke.selectAll()
			nuke.invertSelection()
			each[ 'selected' ].setValue( 1 )
			slate = nuke.createNode( 'sag_slate' )
			slate[ 'duration' ].setValue( str(durList[shot]) )
			slate[ 'scriptname' ].setValue( shot + '_' + task + '_' + ver )
			nuke.toNode( slate.name() + '.frameCounter' )[ 'message' ].setValue( 'frame: ' + zfill( fr, len( str(durList[shot]) ) ) + ' of ' + str(durList[shot]) )

			wrt = nuke.createNode( 'Write' )
			wrt[ 'file' ].setValue( exr[:-4] + '.jpg' )
			outList.append( wrt )

	nuke.selectAll()
	nuke.invertSelection()
	for each in outList:
		each[ 'selected' ].setValue( 1 )
