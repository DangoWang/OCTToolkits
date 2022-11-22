import nuke

def sag_lockNode():
	selList = nuke.selectedNodes()
	
	for eachNode in selList:
		knobList = eachNode.allKnobs()

		if eachNode.knob( 'selected' ).enabled():
			eachNode.hideControlPanel()
			eachNode.knob( 'note_font' ).setValue( 'Italic' )
			eachNode.knob( 'autolabel' ).setValue( '"LOCKED_" + str( nuke.thisNode().name() )' )

			for eachKnob in knobList:
				eachKnob.setEnabled( False )
		else:
			eachNode.knob( 'note_font' ).setValue( 'Verdana' )
			eachNode.knob( 'autolabel' ).setValue( '' )

			for eachKnob in knobList:
				eachKnob.setEnabled( True )
