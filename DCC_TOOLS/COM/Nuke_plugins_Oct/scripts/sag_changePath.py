import nuke

selList = nuke.allNodes( 'Read' )

for each in selList:
    pth = each['file'].getValue()
    each['file'].setValue( pth.replace( 'x:/', 'y:/' ) )
