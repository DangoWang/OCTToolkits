import nuke
import os, os.path

def sag_writeCreateDirs( selList ):
	for each in selList:
		if each.Class() == 'Write':
			filePath = each.knob( 'file' ).value()
			dirPath = filePath[:filePath.rfind( '/' )+1]
			if not os.path.exists( dirPath ):
				os.makedirs( dirPath )
