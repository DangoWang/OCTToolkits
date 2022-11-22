#------------------------------------------------------------------nuke-
# file: sag_metaData.py
# version: 0.1
# date: 2012.12.14
# author: Arkadiy Demchenko (sagroth@sigillarium.com)
#-----------------------------------------------------------------------
# 2012.12.14 (v0.1) - main release
#-----------------------------------------------------------------------
# Tools to work with metadata in nuke.
#-----------------------------------------------------------------------

import nuke
from string import zfill


# RETURNS VALUE FOR THE KEY FROM METADATA FILE, SPECIFIED IN MODIFYMETADATA NODE
def readMetaKey( key, meta ):
	val = ''

	metaFile = nuke.toNode( meta )[ 'metaFile' ].value()

	if metaFile.rfind( '%' ) > -1:
		metaFileSplit = metaFile.split( '.' )
		seq = int( metaFile[ metaFile.rfind( '%' )+1:metaFile.rfind( '%' )+3 ] )
		metaFile = metaFile[:metaFile.rfind( '%' )] + zfill( nuke.frame(), seq ) + metaFile[metaFile.rfind( '%' )+4:]
	
	f = open( metaFile, 'r' )
	
	for line in f:
		data = line.split( ':' )
		if data[0] == key:
			val = data[2][:-1]
			if data[1] == 'f':
				val = float( val )
			elif data[1] == 'f3':
				val = val.split()
	f.close()

	return val


# CREATES MODIFYMETADATA NODE WITH NECESSARY SETUP
def addMeta( node, metaFile ):
	source = nuke.toNode( node )

	metaFile = metaFile.replace( '\\', '/' )

	for each in nuke.selectedNodes():
		each.setSelected( False )

	source.setSelected( True )

	metaNode = nuke.createNode( 'ModifyMetaData' )
	metaFileKnob = nuke.File_Knob( 'metaFile', 'MetaData File' )
	metaNode.addKnob( metaFileKnob )
	metaFileKnob.setValue( metaFile )

	meta = []
	f = open( metaFile, 'r' )
	for line in f:
		data = line.split( ':' )
		meta.append( '{set exr/' + data[0] + ' "[python scripts.sag_metaData.readMetaKey( \'' + data[0] + '\', nuke.thisNode().name() )]"}' )
	f.close()

	metaNode[ 'metadata' ].fromScript( '\n'.join( meta ) )


#scripts.sag_metaData.addMeta( 'Read1', 'x:/SAVVA/result/Tests/exrResave/Monkeys_Corridor_masks_01a.0001.dat' )
