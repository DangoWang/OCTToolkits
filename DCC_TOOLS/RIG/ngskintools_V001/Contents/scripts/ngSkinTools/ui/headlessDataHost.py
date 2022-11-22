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

from ngSkinTools import selectionState
from ngSkinTools.ui.layerDataModel import LayerDataModel
from ngSkinTools.utils import Utils
from ngSkinTools.ui.events import MayaEvents, scriptJobs
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.log import getLogger


log = getLogger("HeadlessDataHost")


class RefCountedHandle:
    '''
    reference counted handle to a dynamically allocated instance;
    
    creates reference after first addReference() call, and destroys it 
    when last reference is removed via removeReference()
    '''
    
    def __init__(self,instantiator):
        self.instantiator=instantiator
        self.instance = None
        self.references = set()
    
    def getCurrentInstance(self):
        '''
        returns handle to currently created instance
        '''
        return self.instance

    def isInitialized(self):
        if self.references:
            return True
        return False

    def addReference(self,refSource):
        if refSource in self.references:
            return
        
        if len(self.references)==0:
            self.instance = self.instantiator()
            self.instance.initialize()
            
        self.references.add(refSource)
        
        
    def removeReference(self,refSource):
        '''
        returns false, if provided reference was not found in the stack
        '''
        if refSource not in self.references:
            return False
        
        self.references.remove(refSource)
        if len(self.references)==0:
            self.instance.cleanup()
            self.instance=None
            
        return True
            
        
class HeadlessDataHost:

    '''
    A singleton of this object is created when at least one UI window is opened,
    and performs a cleanup once all objects are closed
    '''
    
    HANDLE = None
    
    @staticmethod
    def get():
        return HeadlessDataHost.HANDLE.getCurrentInstance() 
    
    def __init__(self):
        self.documentation = SkinToolsDocs
        
        
    def initialize(self):
        log.debug("creating headless data host")
        
        Utils.loadPlugin()

        MayaEvents.registerScriptJobs()
        LayerDataModel.bindAll()
        selectionState.bindAll()
        LayerDataModel.getInstance().updateLayerAvailability()
        selectionState.selectionInfo.dropCache()
        selectionState.mirrorInfo.dropCache()


    def cleanup(self):
        '''
        cleanup any acquired resources
        '''
        scriptJobs.deregisterScriptJobs()

        from ngSkinTools.ui import events
        events.restartEvents()

        LayerDataModel.__instance = None

        log.debug("headless data host cleanup")


HeadlessDataHost.HANDLE = RefCountedHandle(HeadlessDataHost)        
    
