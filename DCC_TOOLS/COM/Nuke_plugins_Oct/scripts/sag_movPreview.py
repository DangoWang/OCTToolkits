import nuke

def sag_movPreview( mode, gainValue, gammaValue, scaleValue ):
    selList = nuke.selectedNodes()
    if selList == []:
        return
    
    for each in selList:
        curPath = each.knob( 'file' ).getValue()
        newPath = curPath[:curPath[:curPath.rfind( '/' )].rfind( '/' )] + curPath[curPath.rfind( '/' ):curPath.find('.')] + '.mov'

        gam = nuke.createNode( 'Grade' )
        gam.hideControlPanel()
        gam.knob( 'gamma' ).setValue( gammaValue )
        gam.knob( 'white' ). setValue( gainValue )
        gam.setInput( 0, each )

        ref = nuke.createNode( 'Reformat' )
        ref.hideControlPanel()
        ref.knob( 'type' ).setValue( 'scale' )
        ref.knob( 'scale' ).setValue( scaleValue )
        ref.setInput( 0, gam )

        out = nuke.createNode( 'Write' )
        out.hideControlPanel()
        out.knob( 'channels' ).setValue( 'rgb' )
        out.knob( 'file' ).setValue( newPath )
        out.setInput( 0, ref )
    
        if mode == 1:
            nuke.render( out, int( each.knob( 'first' ).getValue() ), int( each.knob( 'last' ).getValue() ) )
            nuke.delete( out )
            nuke.delete( ref )
            nuke.delete( gam )