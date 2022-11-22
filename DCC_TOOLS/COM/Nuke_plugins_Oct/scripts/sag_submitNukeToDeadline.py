#------------------------------------------------------------------nuke-
# file: sag_submitNukeToDeadline.py
# version: 0.2
# date: 2014.10.03
# author: Arkadiy Demchenko (sagroth@sigillarium.com)
#-----------------------------------------------------------------------
# 2014.10.03 (v0.2) - works with Deadline6
# 2011.10.25 (v0.1) - main release
#-----------------------------------------------------------------------
# Nuke submission to Deadline utility.
#-----------------------------------------------------------------------

import nuke, nukescripts
import os, os.path, time


# VARIABLES
deadCmd = 'deadlineCommand'
if os.getenv( 'DEADLINE_PATH' ) != None:
	deadCmd = os.getenv( 'DEADLINE_PATH' ).replace( '\\', '/' ) + '/' + deadCmd

deadTempPath = 'c:/ProgramData/Frantic Films/Deadline/temp/' # PATH FOR DEADLINE JOB SUBMISSION FILES
infoFileName = 'nuke_plugin_info.job' # NAME OF THE FILE TO STORE INFO ABOUT THE JOB
jobFileName = 'nuke_plugin_job.job' # NAME OF THE FILE TO STORE THE JOB DATA

nkDir = 'x:/SAVVA/.nk/' # DEFAULT NK STORAGE
#nkDir = 'C:/_temp/.nk/' # HOME NK STORAGE


# GET DEADLINE DATA
def sag_submitNukeToDeadline_getData( data ):
	f = os.popen( deadCmd + ' -' + data )
	result = f.read().split()
	f.close()

	return result


# CHECKS OUTPUTS AND DIRS
def sag_submitNukeToDeadline_check():
	allWrites = nuke.allNodes( 'Write' )
   
	if allWrites == []:
		nuke.message( 'No write nodes exist!' )
		return 0

	outs = []
	for eachWrite in allWrites:
		if not eachWrite[ 'disable' ].value():
			outs.append( eachWrite )

	if outs == []:
		nuke.message( 'No write nodes enabled!' )
		return 0

	for eachOut in outs:
		outPath = eachOut[ 'file' ].value()
		outPath = outPath[ :outPath.rfind( '/' )+1 ]

		if not os.path.exists( outPath ):
			os.makedirs( outPath )

	return 1


# SUBMIT NUKE JOB TO DEADLINE
def sag_submitNukeToDeadline_submitJob( jobName, comment, frameList, pool, priority, framesPerHost, machineLimit, suspended, concurTasks ):
	# BAKE SLATES
	slt = nuke.allNodes( 'sag_slate' )

	sltDict = {}
	for eachSlt in slt:
		# ARTIST
		artistExpr = eachSlt[ 'artistname' ].toScript()
		artistValue = eachSlt[ 'artistname' ].getValue()

		eachSlt[ 'artistname' ].setValue( artistValue )

		# SHOT NAME
		shotExpr = eachSlt[ 'shotname' ].toScript()
		shotValue = eachSlt[ 'shotname' ].getValue()

		eachSlt[ 'shotname' ].setValue( shotValue )

		# VERSION
		verExpr = eachSlt[ 'versionnum' ].toScript()
		verValue = eachSlt[ 'versionnum' ].getValue()

		eachSlt[ 'versionnum' ].setValue( verValue )

		# DATE
		dateExpr = eachSlt[ 'shotdate' ].toScript()
		dateValue = eachSlt[ 'shotdate' ].getValue()

		eachSlt[ 'shotdate' ].setValue( dateValue )

		# TIME
		timeExpr = eachSlt[ 'shottime' ].toScript()
		timeValue = eachSlt[ 'shottime' ].getValue()

		eachSlt[ 'shottime' ].setValue( timeValue )

		sltDict[ eachSlt.name() ] = { 'artistname':artistExpr, 'shotname':shotExpr, 'versionnum':verExpr, 'shotdate':dateExpr, 'shottime':timeExpr }

	# SAVE NK TO SERVER AND RESTORE MODIFIED STATUS
	nk = nkDir + nuke.root().name().split( '/' )[-1][:-3] + '.' + time.strftime('%y%m%d') + '-' + time.strftime('%H%M%S') + '.nk'

	mod = nuke.modified()
	nuke.scriptSave( nk )
	nuke.modified( mod )

	# RESTORE SLATES
	for eachSlt in sltDict:
		for eachExpr in sltDict[ eachSlt ]:
			nuke.toNode( eachSlt )[ eachExpr ].setValue( sltDict[ eachSlt ][ eachExpr ] )

	# CREATE DEADLINE INFO FILE
	infoDict = { 'Plugin':'Nuke', 
				 'Name':jobName, 
				 'Comment':comment, 
				 'Pool':pool, 
				 'Priority':priority, 
				 'Frames':frameList, 
				 'Department':'compositing',
				 'ChunkSize':framesPerHost,
				 'MachineLimit':machineLimit }
	if concurTasks > 1:
		infoDict[ 'ConcurrentTasks' ] = str( concurTasks )
		infoDict[ 'LimitTasksToNumberOfCpus' ] = 'false'
	if suspended == 1:
		infoDict[ 'InitialStatus' ] = 'Suspended'

	infoFile = open( deadTempPath + infoFileName, 'w' )
	for each in infoDict:
		infoFile.write( each + '=' + infoDict[each] + '\n' )
	infoFile.close()

	# CREATE DEADLINE JOB FILE
	jobDict = { 'SceneFile':nk, 
				'Version':'7.0', 
				'Threads':'0', 
				'RamUse':'0' }

	jobFile = open( deadTempPath + jobFileName, 'w' )
	for each in jobDict:
		jobFile.write( each + '=' + jobDict[each] + '\n' )
	jobFile.close()

	# CREATE BATCH FILE WITH SUBMIT COMMAND FOR MANUAL SUBMISSION IF NEEDED
	batFile = open( deadTempPath + 'nuke_submitJob.bat', 'w' )
	batFile.write( deadCmd + ' "' + deadTempPath + infoFileName + '" "' + deadTempPath + jobFileName + '"' )
	batFile.close()

	# SUBMIT
	process = os.system( deadCmd + ' "' + deadTempPath + infoFileName + '" "' + deadTempPath + jobFileName + '"' )
	#process = subprocess.Popen( deadTempPath + 'nuke_submitJob.bat', shell = False, stdout = subprocess.PIPE )

	# FEEDBACK
	feedback = ' Deadline job "' + jobName + '" successfully submitted at ' + time.strftime('%H:%M:%S') + ' ' + time.strftime('%d.%m.%Y')
	liner = '#'
	for i in xrange( 0, len( feedback ) ):
		liner += '#'
	print ''
	print liner
	print feedback
	print liner

	nuke.message( feedback )


# GUI DIALOG
class sag_submitNukeToDeadline_dialog( nukescripts.PythonPanel ):
	def __init__( self ):
		nukescripts.PythonPanel.__init__( self, 'Submit to Deadline', 'sag_submitNukeToDeadline_dialog', False )
		self.setMinimumSize( 400, 310 )
		self.setMaximumSize( 400, 310 )

		self.jobName = nuke.String_Knob( 'jobName', 'Job Name:' )
		self.addKnob( self.jobName )
		self.jobName.setValue( nuke.root().name().split( '/' )[-1][:-3] )

		self.comment = nuke.String_Knob( 'comment', 'Comment:' )
		self.addKnob( self.comment )
		self.comment.setValue( '' )

		self.sep1 = nuke.Text_Knob( 'sep1', '' )
		self.addKnob( self.sep1 )

		self.frameList = nuke.String_Knob( 'frameList', 'Frame Range:' )
		self.addKnob( self.frameList )
		self.frameList.setValue( str( nuke.root().firstFrame() ) + '-' + str( nuke.root().lastFrame() ) )

		self.sep2 = nuke.Text_Knob( 'sep2', '' )
		self.addKnob( self.sep2 )

		allPools = sag_submitNukeToDeadline_getData( 'pools' )
		self.pools = nuke.Enumeration_Knob( 'pools', 'Pool:', allPools )
		self.addKnob( self.pools )
		if 'farm' in allPools:
			self.pools.setValue( 'farm' )
		else:
			self.pools.setValue( 0 )

		self.priority = nuke.Int_Knob( 'priority', 'Priority:' )
		self.addKnob( self.priority )
		self.priority.setValue( 50 )

		self.framesPerHost = nuke.Int_Knob( 'framesPerHost', 'Frames Per Host:' )
		self.addKnob( self.framesPerHost )
		self.framesPerHost.setValue( 5 )

		self.machineLimit = nuke.Int_Knob( 'machineLimit', 'Machine Limit:' )
		self.addKnob( self.machineLimit )
		self.machineLimit.setValue( 0 )

		self.concurTasks = nuke.Int_Knob( 'concurTasks', 'Concurrent Tasks:' )
		self.addKnob( self.concurTasks )
		self.concurTasks.setValue( 1 )

		self.suspended = nuke.Boolean_Knob( 'suspended', 'Submit Suspended' )
		self.suspended.setFlag( nuke.STARTLINE )
		self.addKnob( self.suspended )
		self.suspended.setValue( 0 )

		self.sep3 = nuke.Text_Knob( 'sep3', '' )
		self.addKnob( self.sep3 )

	def showModalDialog( self ):
		result = nukescripts.PythonPanel.showModalDialog( self )
		if result:
			jobName = self.jobName.value()
			if jobName == '':
				jobName = nuke.root().name().split( '/' )[-1][:-3]

			comment =  self.comment.value()

			frameList = self.frameList.value()
			if frameList == '':
				nuke.message( 'No frame range specified!' )
				return 0

			pool = self.pools.value()
			
			priority = str( min( max( 1, self.priority.value() ), 99 ) )

			framesPerHost = self.framesPerHost.value()
			frameRange = frameList.split( '-' )
			if len( frameRange ) > 1:
				framesPerHost = str( min( max( int( frameRange[0] ), int( frameRange[1] ) ) - min( int( frameRange[0] ), int( frameRange[1] ) ) + 1, framesPerHost ) )
			else:
				framesPerHost = '1'

			machineLimit = str( self.machineLimit.value() )

			suspended = self.suspended.value()

			concurTasks = self.concurTasks.value()

			sag_submitNukeToDeadline_submitJob( jobName, comment,  frameList, pool, priority,framesPerHost, machineLimit, suspended, concurTasks )


# RUNS THE DIALOG
def sag_submitNukeToDeadline():
	if sag_submitNukeToDeadline_check():
		sag_submitNukeToDeadline_dialog().showModalDialog()
