# -*- coding:utf-8 -*- 
import os,shutil,codecs
import maya.cmds as cmds

global getPlace


def writeNewFileCode(path,string):
    file = codecs.open(path,'w','utf-8')
    file.write(string)
    file.close    
def readFileCode(path):
    con = ''
    if os.path.exists(path):
        Arg = codecs.open(path,'r','gbk')
        con = Arg.read()
        Arg.close()
    return con

class DeployTool():
    def __init__(self):
        pass

    def startDeploy(self,getPlace):
        getDataDir = getPlace+'/data/'
        getProgramName = readFileCode(getPlace+'/data/__name__.inf')
        
        getScriptDir = cmds.internalVar(userScriptDir=True)
        getMayaDocDir = getScriptDir.rsplit('/',2)[0]+'/'
        getAimDir = getMayaDocDir+'October_soft/'+getProgramName+'/'
        if os.path.exists(getAimDir+'config.inf'):
            try:
                os.remove(getAimDir+'config.inf')
            except:
                pass
        cmds.sysFile(getAimDir,md=True)
        cmds.sysFile(getMayaDocDir + 'modules',md=True)
        getModText = '+ '+getProgramName+' 1.0 '+getAimDir
        writeNewFileCode(getMayaDocDir + 'modules/'+getProgramName+'.mod',getModText)
        cmds.sysFile(getAimDir+'/scripts',md=True)
        for one in os.listdir(getDataDir+'/scripts/'):
            if one == 'SystemCore.pyd':
                if not os.path.exists(getAimDir+'/scripts/'+one):
                    shutil.copyfile(getDataDir+'/scripts/'+one,getAimDir+'/scripts/'+one)
            if not one == 'SystemCore.pyd':
                if os.path.exists(getAimDir+'/scripts/'+one):
                    os.remove(getAimDir+'/scripts/'+one) 
                shutil.copyfile(getDataDir+'/scripts/'+one,getAimDir+'/scripts/'+one)
            
        for one in ['bin','icons','maya_plugins','resources']:
            try:
                if os.path.exists(getAimDir+one):
                    shutil.rmtree(getAimDir+one)
                shutil.copytree(getDataDir+one,getAimDir+one)
            except:
                pass
        
        
        
        
        
        if cmds.iconTextButton(getProgramName,ex=True):
            cmds.deleteUI(getProgramName)
        cmds.iconTextButton(getProgramName,i=cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+getProgramName+'/icons/button.png',c='execfile(\''+getAimDir+'/scripts'+'/start.py\')',stp='python',hi=cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+getProgramName+'/icons/button_hover.png',p=cmds.iconTextButton('statusFieldButton',q=True,p=True))
        
        
        execfile(getAimDir+'/scripts/start.py')
        
if __name__ == '__main__':
    startDeploy = DeployTool()
    startDeploy.startDeploy(getPlace)
    