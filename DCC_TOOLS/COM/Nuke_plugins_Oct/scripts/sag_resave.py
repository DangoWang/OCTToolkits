import nuke
import os, os.path

def sag_resave( mode ):
	selList = nuke.selectedNodes()
	if selList == []:
		return
	
	curPath = selList[0].knob( 'file' ).getValue()
	fromPath = nuke.getInput( 'Which part to change?', curPath )
	toPath = nuke.getInput( 'What to change for?', fromPath )
    
	for each in selList:
		curPath = each.knob( 'file' ).getValue()
		newPath = toPath + curPath[len( fromPath ):curPath.rfind('.')] + '.exr'

		if not os.path.exists( newPath[:newPath.rfind('/')] ):
			os.makedirs( newPath[:newPath.rfind('/')] )

		out = nuke.createNode( 'Write' )
		out.hideControlPanel()
		out.knob( 'channels' ).setValue( 'all' )
		out.knob( 'file' ).setValue( newPath )
		out.knob( 'datatype' ).setValue( 0 )
		out.knob( 'compression' ).setValue( 2 )
		out.setInput( 0, each )
	
		if mode == 1:
			nuke.render( out, int( each.knob( 'first' ).getValue() ), int( each.knob( 'last' ).getValue() ) )
			nuke.delete( out )
