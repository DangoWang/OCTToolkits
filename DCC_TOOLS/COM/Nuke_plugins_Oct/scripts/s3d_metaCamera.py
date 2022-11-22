'''
toDo: add transform ORDER
'''

import nukescripts
import nuke

class ModalFramePanel( nukescripts.PythonPanel ):
    # Modal Dialog class
    def __init__( self,header,text ):
     nukescripts.PythonPanel.__init__( self, header, "uk.co.thefoundry.FramePanel" )
     #self.frame = nuke.Int_Knob( "frame", "Frame:" )
     self.text = nuke.Text_Knob('' )
     #self.addKnob( self.frame )
     self.addKnob( self.text )
     self.text.setValue( text )
    def showModalDialog( self ):
     result = nukescripts.PythonPanel.showModalDialog( self )  

def s3d_metaCamera():    
    # check current scene for stereo views
    if 'left' and 'right' not in nuke.views():
        nuke.message('WARNING!! No "left\right" stereo views found,\nplease setup default "stereo views" in composition global settings\n Script works only with "left" and "right" views names, not with "R" and "L" or\n something like that.')
        #ModalFramePanel('WARNING','No "left\right" stereo views found,\nplease setup default "stereo views" in composition global settings\n Script works only with "left" and "right" views names, not with "R" and "L" or\n something like that.').showModalDialog()
    else :
        metadatNode=nuke.createNode('ViewMetaData')
        metaNode=nuke.selectedNode()
        firstFrame = metaNode.firstFrame()
        lastFrame = metaNode.lastFrame()       
        metaCam=nuke.createNode('Camera')

        #--------- read metadata and assign to variables
        rotOrder = metaNode.metadata( 'exr/rotOrder', firstFrame )
        metaCam['rot_order'].setValue(rotOrder.upper())
        metaCam.setName(metaNode.metadata('exr/camName'))
        for i in xrange(lastFrame-firstFrame+1):
            frame = firstFrame+i
            if frame == firstFrame:                
                metaCam['focal'].setAnimated()
                metaCam['haperture'].setAnimated()
                metaCam['vaperture'].setAnimated()
                metaCam['win_translate'].splitView('right')
                metaCam['win_translate'].setAnimated(0,view = 'left')
                metaCam['win_translate'].setExpression("-win_translate.left.u",0,view='right')
                metaCam['rotate'].setAnimated()
                #metaCam['scaling'].setAnimated()
                metaCam['translate'].setAnimated()
                metaCam['translate'].splitView('right')
                
            metaCam[ 'focal' ].setValueAt(  float( metaNode.metadata( 'exr/focalLength', frame ) ), frame )
            metaCam[ 'haperture' ].setValueAt(  float( metaNode.metadata( 'exr/hAperture', frame ) )*25.4, frame )
            metaCam[ 'vaperture' ].setValueAt(  float( metaNode.metadata( 'exr/vAperture', frame ) )*25.4, frame )
            metaCam[ 'win_translate' ].setValueAt(  float( metaNode.metadata( 'exr/filmTranslateHL', frame ) ), frame,0,view='left' )
            metaCam[ 'rotate' ].setValueAt(  float( metaNode.metadata( 'exr/camRotate', frame )[0] ), frame,0)
            metaCam[ 'rotate' ].setValueAt(  float( metaNode.metadata( 'exr/camRotate', frame )[1] ), frame,1)
            metaCam[ 'rotate' ].setValueAt(  float( metaNode.metadata( 'exr/camRotate', frame )[2] ), frame,2)
            #metaCam[ 'scaling' ].setValueAt(  float( metaNode.metadata( 'exr/camScale', frame )[0] ), frame,0)
            #metaCam[ 'scaling' ].setValueAt(  float( metaNode.metadata( 'exr/camScale', frame )[1] ), frame,1)
            #metaCam[ 'scaling' ].setValueAt(  float( metaNode.metadata( 'exr/camScale', frame )[2] ), frame,2)
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateL', frame )[0] ), frame,0,view='left' )
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateL', frame )[1] ), frame,1,view='left' )
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateL', frame )[2] ), frame,2,view='left' )
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateR', frame )[0] ), frame,0,view='right' )
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateR', frame )[1] ), frame,1,view='right' )
            metaCam[ 'translate' ].setValueAt(  float( metaNode.metadata( 'exr/camTranslateR', frame )[2] ), frame,2,view='right' )
            
  
        #------------- update button command. For update camera 
        buttonCommand = '''class ModalFramePanel( nukescripts.PythonPanel ):
    # Modal Dialog class
    def __init__( self,header,text ):
     nukescripts.PythonPanel.__init__( self, header, "uk.co.thefoundry.FramePanel" )
     #self.frame = nuke.Int_Knob( "frame", "Frame:" )
     self.text = nuke.Text_Knob('' )
     #self.addKnob( self.frame )
     self.addKnob( self.text )
     self.text.setValue( text )
    def showModalDialog( self ):
     result = nukescripts.PythonPanel.showModalDialog( self )  

if not nuke.exists("{metaNode}"): 
    ModalFramePanel('OOPS','Source meta data node was renamed or deleted.I can`t find it.').showModalDialog()
else :
    firstFrame = nuke.toNode("{metaNode}").firstFrame()
    lastFrame = nuke.toNode("{metaNode}").lastFrame()   
    for i in xrange(lastFrame-firstFrame+1):
        frame = firstFrame+i
        if frame == firstFrame:
            metaCam = nuke.thisNode()
            metaCam['focal'].clearAnimated()
            metaCam['haperture'].clearAnimated()
            metaCam['vaperture'].clearAnimated()
            metaCam['win_translate'].clearAnimated(0,view = 'left')
            metaCam['rotate'].clearAnimated()
            metaCam['scaling'].clearAnimated()
            metaCam['translate'].clearAnimated(view = 'left')
            metaCam['translate'].clearAnimated(view = 'right')
            
            metaCam['focal'].setAnimated()
            metaCam['haperture'].setAnimated()
            metaCam['vaperture'].setAnimated()
            metaCam['win_translate'].setAnimated(0,view = 'left')
            metaCam['win_translate'].setExpression("-win_translate.left.u",0,view='right')
            metaCam['rotate'].setAnimated()
            metaCam['scaling'].setAnimated()
            metaCam['translate'].setAnimated(view = 'left')
            metaCam['translate'].setAnimated(view = 'right')
            
        metaCam[ 'focal' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/focalLength', frame ) ), frame )
        metaCam[ 'haperture' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/hAperture', frame ) ), frame )
        metaCam[ 'vaperture' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/vAperture', frame ) ), frame )
        metaCam[ 'win_translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/filmTranslateHL', frame ) ), frame,0,view='left' )
        metaCam[ 'rotate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camRotate', frame )[0] ), frame,0)
        metaCam[ 'rotate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camRotate', frame )[1] ), frame,1)
        metaCam[ 'rotate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camRotate', frame )[2] ), frame,2)
        metaCam[ 'scaling' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camScale', frame )[0] ), frame,0)
        metaCam[ 'scaling' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camScale', frame )[1] ), frame,1)
        metaCam[ 'scaling' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camScale', frame )[2] ), frame,2)
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateL', frame )[0] ), frame,0,view='left' )
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateL', frame )[1] ), frame,1,view='left' )
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateL', frame )[2] ), frame,2,view='left' )
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateR', frame )[0] ), frame,0,view='right' )
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateR', frame )[1] ), frame,1,view='right' )
        metaCam[ 'translate' ].setValueAt(  float( nuke.toNode("{metaNode}").metadata( 'exr/camTranslateR', frame )[2] ), frame,2,view='right' )'''.format(metaNode=metaNode.name())
        
        #------ create user knob : button  on camera, that execute camera update(bake) animation from metadata.
        updateButton = nuke.nuke.PyScript_Knob('updateCam', 'Update Camera')
        camtext = nuke.nuke.Text_Knob('camtext', 'meta-mather node: ')
        metaCam.addKnob(camtext)
        metaCam.addKnob(updateButton)
        camtext.setValue(metaNode.name())
        updateButton.setCommand(buttonCommand)
            
            
'''

        #--------- Expressions didn`t work in real time unfortunately
        #metaCam.setName(metaDat['exr/camName'])
        metaCam['focal'].setExpression("[python nuke.toNode('{0}').metadata('exr/focalLength')]".format(metaNode.name()))
        metaCam['haperture'].setExpression("[python nuke.toNode('{0}').metadata('exr/hAperture')*25.4]".format(metaNode.name()))
        metaCam['vaperture'].setExpression("[python nuke.toNode('{0}').metadata('exr/vAperture')*25.4]".format(metaNode.name()))
        metaCam['win_translate'].splitView('right')
        metaCam['win_translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/filmTranslateHL')]".format(metaNode.name()),0,view='left')
        metaCam['win_translate'].setExpression("-win_translate.left.u",0,view='right')
        
        metaCam['rotate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camRotate')\[0\]]".format(metaNode.name()),0)
        metaCam['rotate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camRotate')\[1\]]".format(metaNode.name()),1)
        metaCam['rotate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camRotate')\[2\]]".format(metaNode.name()),2)
        
        metaCam['scaling'].setExpression("[python nuke.toNode('{0}').metadata('exr/camScale')\[0\]]".format(metaNode.name()),0)
        metaCam['scaling'].setExpression("[python nuke.toNode('{0}').metadata('exr/camScale')\[1\]]".format(metaNode.name()),1)
        metaCam['scaling'].setExpression("[python nuke.toNode('{0}').metadata('exr/camScale')\[2\]]".format(metaNode.name()),2)
        
        metaCam['translate'].splitView('right')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateL')\[0\]]".format(metaNode.name()),0,view='left')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateR')\[0\]]".format(metaNode.name()),0,view='right')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateL')\[1\]]".format(metaNode.name()),1,view='left')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateR')\[1\]]".format(metaNode.name()),1,view='right')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateL')\[2\]]".format(metaNode.name()),2,view='left')
        metaCam['translate'].setExpression("[python nuke.toNode('{0}').metadata('exr/camTranslateR')\[2\]]".format(metaNode.name()),2,view='right')
'''