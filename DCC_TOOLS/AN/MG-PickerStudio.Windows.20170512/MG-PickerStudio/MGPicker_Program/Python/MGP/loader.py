from maya import cmds
import os
import logging
logger = logging.getLogger(__name__)

class MGPickerLoaderBase(object):
    '''
    Base class for all user-implemented loader, which loads picker file for selected rig/rigs.
    
    Implement subclass to make your own picker auto-loader, and put the python module in the /AutoLoaders
    folder, or put the module path or python full path in environment variable "MGPICKER_LOADER_PY_MODULES" 
    to make it recongized.
    '''
    def pickerFileForAssetName(self, assetName):
        '''    
            This method is the only method that need to reimplemented in the sub-class,
            which returns a full path to a .mgpkr file for the specific maya node with namespace.  
        '''
        raise NotImplementedError('This method should be implemented by sub class')
    
    def loadPicker(self, assetName):
        '''
        This method don't need to be overrided, it is used by picker program to load the actual picker.
        '''
        if not hasattr(cmds, 'MGPicker') or not cmds.MGPicker(q=True, ex=True):
            raise RuntimeError('The MG-Picker Studio is not loaded.')
        
        pickerFile = self.pickerFileForAssetName(assetName)
        if (not pickerFile) or (not os.path.isfile(pickerFile)) or (not pickerFile.endswith('.mgpkr')):
            className = self.__class__.__name__
            logger.info('[%s]: Can not find picker file using loader: %s' % (assetName, className))
            return False
        
        viewId = cmds.MGPicker(e=True, readPickerFile=(pickerFile, False))
        if not viewId:
            return False
        
        cmds.MGPickerView(viewId, edit=True, namespace = assetName, tabLabel=assetName)
        logger.info('[%s]: Find picker file using loader: %s' % (assetName, self.__class__.__name__))
        return True


class MGPickerRigListerBase(object):
    '''
    
    Base class for all user-implemented maya scene rig lister, which list out the possible rig names that 
    need to load a picker, when user click submenu of the menu "Load All Pickers".
    
    For each rig name returned, loader is responsible to load the actual picker, will use default loader if
    no custom loader class found.
    
    Implement subclass to make your own scene rig lister, and put the python module in the /AutoLoaders
    folder, or put the module path or python full path in environment variable "MGPICKER_LOADER_LISTER_PY_MODULES" 
    to make it recongized.
    
    Each method starts with mayaScene_*, the * will be used as sub-menuitem label in the "Load All Pickers" menu.
    eg. If you wanna add "Load All Creatures" menu item, you implement "mayaScene_creatures" method.
        Examples (All these methods should return list or tuple):
        def mayaScene_creatures(self)   ---> "Load All Pickers / Load All Creatures"
        def mayaScene_characters(self)   ---> "Load All Pickers / Load All Characters"
        def mayaScene_male_characters(self)   ---> "Load All Pickers / Load All Male Characters"
        def mayaScene_props(self)   ---> "Load All Pickers / Load All Props"
        def mayaScene_rigged_sets(self)   ---> "Load All Pickers / Load All Rigged Sets"
        def mayaScene_rigs(self)    ---> "Load All Pickers / Load All Rigs"
        
    !! You can define multiple scene rig lister, but for spcial category of rigs, if one lister return non-empty 
    list, it won't use further lister to list it. eg. the first lister returns non-empty list for mayaScene_characters,
    then second lister won't be used.
    
    '''
    pass
    
