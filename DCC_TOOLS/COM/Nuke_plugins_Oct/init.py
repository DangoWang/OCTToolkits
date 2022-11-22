import nuke
import os, os.path
import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()

# ENVIRONMENT VARIABLES
nuke_path = os.getenv( 'NUKE_PATH' )

# INFO FEEDBACK
feedback = ' Custom tools from ' + nuke_path 
liner = '-'
for i in xrange( 0, len( feedback ) ):
	liner += '-'
print ''
print liner
print feedback
print liner
print ''

# PATHS
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./scripts')

def createWriteDir():
    import nuke, os
    file = nuke.filename(nuke.thisNode())
    dir = os.path.dirname( file )
    osdir = nuke.callbacks.filenameFilter( dir )
    try:
        os.makedirs( osdir )
        return
    except:
        return  
nuke.addBeforeRender( createWriteDir )

