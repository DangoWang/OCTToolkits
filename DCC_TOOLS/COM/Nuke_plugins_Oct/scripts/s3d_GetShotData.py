
from subprocess import Popen
import nuke
import os
import re

def s3d_GetShotData():
	scriptPath = nuke.scriptName()
	scriptName = os.path.basename(scriptPath)
	#shotName = extractShotNameFrom_thisName(scriptName)
	appPath = 'x://SAVVA//_stereo//stereoscopic_folder//PippelineScripts//Cerebro_python//Externall_calls//cerebro_getShotData.bat'
	Popen([appPath, scriptName])