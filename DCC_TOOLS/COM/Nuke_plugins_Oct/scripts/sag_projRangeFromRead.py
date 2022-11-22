import nuke

def sag_projRangeFromRead():
	selList = nuke.selectedNodes()

	if selList != []:
		if selList[0].Class() == 'Read':
			nuke.toNode( 'root' ).knob( 'first_frame' ).setValue( selList[0].knob( 'first' ).value() )
			nuke.toNode( 'root' ).knob( 'last_frame' ).setValue( selList[0].knob( 'last' ).value() )
			nuke.toNode( 'root' ).knob( 'format' ).setValue( selList[0].knob( 'format' ).value() )