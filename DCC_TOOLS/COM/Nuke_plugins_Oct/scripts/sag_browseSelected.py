import nuke
import os.path, subprocess

def sag_browseSelected():
	selList = nuke.selectedNodes()

	if selList != []:
		for each in selList:
			if each.Class() == 'Read' or each.Class() == 'Write':
				filePath = each.knob( 'file' ).getValue()
				dirPath = filePath[:filePath.rfind( '/' )+1]
				if os.path.exists( dirPath ):
					subprocess.Popen( 'explorer "' + dirPath.replace( '/', '\\' ) + '"' )
