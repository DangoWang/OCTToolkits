#
#    ngSkinTools
#    Copyright (c) 2009-2017 Viktoras Makauskas.
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by EULA.
#         
#    A copy of EULA can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

from ngSkinTools.ui.uiWrappers import StoredTextEdit, RadioButtonField
from maya import cmds
from ngSkinTools.ui.events import Signal
from ngSkinTools.ui.components import titledRow

class InfluencePrefixSuffixSelector(object):
    VAR_PREFIX = "ngSkinToolsInfluencePrefixSuffixSelector"
    
    def __init__(self):
        self.changeCommand = Signal("influence prefix suffix selector")
    
    def ignoreModeChanged(self):
        self.prefixesGroup.setVisible(self.isPrefixIgnoreMode())
        self.suffixesGroup.setVisible(not self.isPrefixIgnoreMode())
        self.changeCommand.emit()
        
    def isPrefixIgnoreMode(self):
        return self.ignorePrefixes.getValue()==1
    
    def createUI(self,parent):
        
        titledRow.create(parent, 'Ignore')
        cmds.radioCollection()
        self.ignorePrefixes = RadioButtonField(self.VAR_PREFIX+'ignoreMode_Prefixes',defaultValue=True,label="Prefixes")
        self.ignorePrefixes.changeCommand.addHandler(self.ignoreModeChanged,parent)        
        self.ignoreSuffixes = RadioButtonField(self.VAR_PREFIX+'ignoreMode_Suffixes',defaultValue=False,label="Suffixes")
        self.ignoreSuffixes.changeCommand.addHandler(self.ignoreModeChanged,parent)        


        self.prefixesGroup = titledRow.create(parent, 'Influence Prefixes')
        self.influencePrefixes = StoredTextEdit(self.VAR_PREFIX+'inflPrefix', annotation='Specifies influence prefixes to be ignored when matching by name;\nUsually you would put your left/right influence prefixes here;\nseparate them with commas, e.g. "L_, R_"')
        self.influencePrefixes.changeCommand.addHandler(self.changeCommand.emit, parent)
        
        self.suffixesGroup = titledRow.create(parent, 'Influence Suffixes')
        self.influenceSuffixes = StoredTextEdit(self.VAR_PREFIX+'inflSuffix', annotation='Specifies influence suffixes to be ignored when matching by name;\nUsually you would put your left/right influence suffixes here;\nseparate them with commas, e.g. "_Lf, _Rt"')
        self.influenceSuffixes.changeCommand.addHandler(self.changeCommand.emit, parent)
        
        self.ignoreModeChanged()
        