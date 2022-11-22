import maya.cmds as cmds
import pymel.core as pmc
progamName = 'PlayBlast'
def buildButton_ZPlayBlast(progamName):
    getScriptDir = cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+progamName+'/scripts'
    cmds.iconTextButton(progamName,i=cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+progamName+'/icons/button.png',c='execfile(\''+getScriptDir+'\'+\'/start.py\')',stp='python',hi=cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+progamName+'/icons/button_hover.png',p=cmds.iconTextButton('statusFieldButton',q=True,p=True))
pmc.general.evalDeferred('buildButton_PlayBlast(\''+progamName+'\')')