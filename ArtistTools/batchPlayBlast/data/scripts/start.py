#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import maya.cmds as cmds
progamName = 'PlayBlast'
getP = cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+progamName+'/scripts/'
exe_file = cmds.internalVar(userScriptDir=True).rsplit('/',2)[0]+'/October_soft/'+progamName+"/bin/"
print "getPgetPgetP",getP
if getP not in sys.path:
    sys.path.append(getP)
import oct_batch_play_blast
oct_batch_play_blast.main(exe_file)