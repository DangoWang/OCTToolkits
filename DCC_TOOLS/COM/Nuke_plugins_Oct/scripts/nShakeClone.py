
#  Take all selected nodes and create dupliates that are linked via expressions 
#  to the original for all knobs except those an EXCLUSION_LIST...there may be 
#  value in defining different EXCLUSION_LISTs per node class...

import nuke

def shakeClone():
	EXCLUSION_LIST = ["white","black","xpos","ypos","help","hide_input","note_font_color","onCreate","updateUI","knobChanged","note_font","tile_color","selected","autolabel","process_mask","label","onDestroy","inject","indicators","maskFrom","maskChannelMask","maskChannelInput","Mask","disable","maskChannelMask", "panel", "maskFromFlag","name","cached","fringe", "maskChannelInput" , "note_font_size" , "filter", "gl_color","transform"]

	originals = nuke.selectedNodes()
	[ n['selected'].setValue(False) for n in nuke.allNodes() ]
	
	for original in originals:
		new = nuke.createNode(original.Class())
		
		for i in original.knobs():
			if i not in EXCLUSION_LIST:
                                # Try to set the expression on the knob
				new.knob(i).setExpression("%s.%s" % (original.name(), original.knob(i).name()))
                                
                                # This will fail if the knob is an Array Knob...use setSingleValue to compensate
                                # Thanks Hugh!
				if isinstance(new.knob(i), nuke.Array_Knob):
					new.knob(i).setSingleValue(original.knob(i).singleValue()) 

                                # This will fail if the knob is a String Knob...use a TCL expression link to compensate
                                # Thanks Michael!
				elif isinstance(new.knob(i), nuke.String_Knob): 
					new.knob(i).setValue("[value %s.%s]" % (original.name(), original.knob(i).name())) 
					
		new['selected'].setValue(False)	

	[ n['selected'].setValue(True) for n in originals ]


