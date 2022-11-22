import maya.cmds as cmds
import maya.mel as mel

#----------------------------------------------------------------------
def MG_getMayaVersionInt():
    """"""	
    version= cmds.about(api=True)/100	
    return version


def MG_maya2011orNot():
    """"""	
    global gMayaVersionInt
    if gMayaVersionInt >= 2011:
        return True
    else:
        return False

def MG_ChineseSysOrNot ():
    """"""
    import locale
    loc=locale.getlocale()
    if loc[0].startswith ('Chinese'):
        if cmds.optionVar(ex="MGtoolsDualLeng"):
            lanstr= cmds.optionVar(q="MGtoolsDualLeng")
            if lanstr == 'ch':
                return 1
            else:
                return 0
        else:
            return 1
    else:
        return 0
    
#init the global var:    
def MG_RefreshLanguageOption():
    global gMayaVersionInt
    gMayaVersionInt = MG_getMayaVersionInt()
    
    global gOSLangOption
    gOSLangOption = MG_ChineseSysOrNot()   
    
    global gMGToolsProTitle
    gMGToolsProTitle = MG_DualLan_forPY("up.pro.toolname")

#----------------------------------------------------------------------
def MG_DualLan_forPY(id):
    """"""    
    global gMayaVersionInt  
    global gOSLangOption
    if not gOSLangOption:
        return mel.eval('MG_DualLan '+str(id))
    else:
        if gMayaVersionInt > 2008:
            return mel.eval('MG_DualLan '+str(id))
        else:
            return mel.eval('MG_DualLan '+str(id)).decode('gb2312')
        
