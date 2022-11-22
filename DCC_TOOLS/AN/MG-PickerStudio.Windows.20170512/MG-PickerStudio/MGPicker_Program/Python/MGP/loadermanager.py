from maya import cmds
from maya import mel
import os
import imp
import inspect
import logging
logger = logging.getLogger(__name__)

from functools import partial
import translate as tr
import sys

MGPICKER_LOADER_LISTER_MODULES_ENV_NAME = 'MGPICKER_LOADER_PY_MODULES'

MGPICKER_LOADER_BASE_CLASS_NAME = 'MGPickerLoaderBase'
MGPICKER_RIG_LISTER_BASE_CLASS_NAME = 'MGPickerRigListerBase'
MGPICKER_LOAD_MEL_PRECEDURE_NAME = 'MGP_FindAndLoadPickerForName'

class MGPickerLoaderManager(object):
    '''
    Internally used for finding all loaders in /Autoloaders folder and autoload the picker file.
    '''
    _managerInstance = None
    _mayaSceneRigLister = []
    
    def __init__(self):
        pass
    
    @classmethod
    def _autoloaderDir(cls):
        return mel.eval('MGP_GetAutoLoaderDir')
    
    @classmethod
    def _instanceFromLoaderModule(cls, module, baseClassName):
        for item in module.__dict__.values():
            if not inspect.isclass(item):
                continue
            baseCls = item.__bases__
            if not baseCls:
                continue
            for c in baseCls:
                if c.__name__ == baseClassName:
                    try:
                        return item()
                    except:
                        logger.exception('Unable to create instance of loader/lister: %s' % c.__name__)
                        
    @classmethod
    def _loaderInstanceFromLoaderModule(cls, module):
        return cls._instanceFromLoaderModule(module, MGPICKER_LOADER_BASE_CLASS_NAME)
    
    @classmethod
    def _listerInstanceFromLoaderModule(cls, module):
        return cls._instanceFromLoaderModule(module, MGPICKER_RIG_LISTER_BASE_CLASS_NAME)            
            
    @classmethod  
    def _loadModuleDoit(cls, moduleName, reloadModule=False):
        try:
            mod = __import__(moduleName, locals(), globals())
            if reloadModule:
                reload(mod)
            return mod
        except:
            logger.exception('Unable to import module: %s' % (moduleName))
        return
    
    @classmethod       
    def _loadModule(cls, moduleNameOrFilePath, reloadModule=False):
        mod = None
        if '/' in moduleNameOrFilePath or os.path.isfile(moduleNameOrFilePath):
            dirPath = os.path.dirname(moduleNameOrFilePath)
            oldPyPaths = sys.path
            if not dirPath in sys.path:
                sys.path.insert(0, dirPath)
                
            try:
                moduleName = os.path.splitext(os.path.basename(moduleNameOrFilePath))[0]
                mod = cls._loadModuleDoit(moduleName, reloadModule=reloadModule)
                sys.path = oldPyPaths
                return mod
            finally:
                sys.path = oldPyPaths
        else:
            return cls._loadModuleDoit(moduleNameOrFilePath, reloadModule=reloadModule)
                        
    @classmethod
    def _instance(cls):
        if not cls._managerInstance:
            cls._managerInstance = cls()
        return cls._managerInstance
        
    @classmethod
    def _modulesFromEnvVar(cls, reloadModule=False):
        loaderModStr = os.environ.get(MGPICKER_LOADER_LISTER_MODULES_ENV_NAME, '')
        if not loaderModStr:
            return []
    
        loaderMods = loaderModStr.split(';')
        if not loaderMods:
            return []
        
        result = []
        for moduleNameOrFullpath in loaderMods:
            mod = cls._loadModule(moduleNameOrFullpath, reloadModule=reloadModule)
            if mod:
                result.append(mod)
                
        return result
            
    @classmethod
    def _loadPickerUsingLoaderFromEnvVar(cls, mayaNamespace):
        loaderMods = cls._modulesFromEnvVar()
        if not loaderMods:
            return False
    
        logger.debug('Find mgpicker loader modules in the environment variable: %s, will try to use them.' % MGPICKER_LOADER_LISTER_MODULES_ENV_NAME)
        for mod in loaderMods:
            try:
                loader = cls._loaderInstanceFromLoaderModule(mod)
                if not loader:
                    continue
                            
                if loader.loadPicker(mayaNamespace):
                    return True            
            except:
                logger.exception('Error using loader: %s' % (mod.__name__))
            
        return False
        
    @classmethod
    def _modulesFromDir(cls, reloadModule=False):
        autoloadDir = cls._autoloaderDir()
        if not autoloadDir or not os.path.isdir(autoloadDir):
            return []
        
        result = []
        loadedModules = []
        for f in os.listdir(autoloadDir):
            extension = os.path.splitext(f)[1]
            if not extension in ['.py', '.pyc']:
                continue
            
            if f == '__init__.py':
                continue      
                  
            moduleName = os.path.splitext(f)[0]
            if moduleName in loadedModules:
                continue
            
            loadedModules.append(moduleName)
            fullpath = os.path.join(autoloadDir, f)
            module = cls._loadModule(fullpath, reloadModule=reloadModule)
            if module:
                result.append(module)
                    
        return result
    
    @classmethod
    def _loadPickerUsingLoaderFromDir(cls, mayaNamespace):
        mods = cls._modulesFromDir()
        if not mods:
            return False
        
        for mod in mods:
            try:        
                loader = cls._loaderInstanceFromLoaderModule(mod)
                if not loader:
                    continue
            
                if loader.loadPicker(mayaNamespace):
                    return True
            except:
                logger.exception('Error using loader: %s' % mod.__name__)
                
        return False
    
    @classmethod
    def _initialiseRigLister(cls, reloadModule=False):
        cls._mayaSceneRigLister = []
        
        mods = cls._modulesFromEnvVar(reloadModule=reloadModule)
        mods.extend(cls._modulesFromDir(reloadModule=reloadModule))
        if not mods:
            return
        
        for mod in mods:
            lister = cls._listerInstanceFromLoaderModule(mod)
            if lister:
                cls._mayaSceneRigLister.append(lister)  
    
    @classmethod
    def _rigNamesForListerCategory(cls, lister, funcName):    
        if not funcName in dir(lister):
            return []
        try:
            function = getattr(lister, funcName)
            return function()
        except:
            logger.exception('Error try to get rig names lister: %s.%s' % (lister.__class__.__name__, funcName))
            return []
        
    @classmethod
    def _listRigNameOfCategory(cls, category):
        if not cls._mayaSceneRigLister:
            return []
        
        if not category or category == '*':
            methodName = 'mayaScene_rigs'
        else:            
            methodName = 'mayaScene_%s' % (category)
            
        result = [] 
        for lister in cls._mayaSceneRigLister:
            names = cls._rigNamesForListerCategory(lister, methodName)
            print lister, names
            if names:
                result.extend(names)
        return list(set(result))
            
    @classmethod        
    def loadPicker(cls, mayaNamespace):
        if cls._loadPickerUsingLoaderFromEnvVar(mayaNamespace):
            return True
        
        return cls._loadPickerUsingLoaderFromDir(mayaNamespace)
    
    @classmethod
    def listSceneRigs(cls, category='*'):
        cls._initialiseRigLister(reloadModule=False)
        return cls._listRigNameOfCategory(category)
    
    @classmethod
    def loadPickerForSceneRigs(cls, category, *args):
        names = cls.listSceneRigs(category=category)
        if not names:
            return
        
        for name in names:
            mel.eval('%s %s' % (MGPICKER_LOAD_MEL_PRECEDURE_NAME, name))
        
    @classmethod
    def _executeMel(cls, melCmd, *args):
        mel.eval(melCmd)
        
    @classmethod
    def _addReloadMenu(cls, parentMenuItem):
        cmds.menuItem(divider=True, p=parentMenuItem)  
        label = tr.MGP_Translate('pkr.loadAll.updateMenu.lbl')
        ann = tr.MGP_Translate('pkr.loadAll.updateMenu.ann')
        cmd = partial(cls._executeMel, 'MGP_RefreshAndReloadAllLoaderMenu')
        cmds.menuItem(label=label, c=cmd, p=parentMenuItem, ann=ann)   
        
    @classmethod
    def _addNoLoaderMenu(cls, parentMenuItem):
        logger.debug('No effective lister function found.')
        label = tr.MGP_Translate('pkr.loadAll.none.mi')
        cmds.menuItem(label=label, enable=False, p=parentMenuItem)
        cls._addReloadMenu(parentMenuItem)
        
    @classmethod
    def reloadLoaderAndListerModules(cls):
        cls._initialiseRigLister(reloadModule=True)
        
    @classmethod
    def reloadAndReturnCategories(cls):
        cls._initialiseRigLister(reloadModule=True)
        
        if not cls._mayaSceneRigLister:
            return []
        
        hasAllRigs = False
        builtCategories = []
        prefix = 'mayaScene_'
        prefixLen = len(prefix)
        for lister in cls._mayaSceneRigLister:
            for name in dir(lister):
                if name.startswith(prefix):
                    if len(name) == prefixLen or name[prefixLen:].lower() == 'rigs':
                        hasAllRigs = True       
                        continue     
                               
                    builtCategories.append(name[prefixLen:])
        builtCategories = sorted(list(set(builtCategories)))       
        if hasAllRigs:
            builtCategories.insert(0, 'rigs')
            
        return builtCategories
    
    @classmethod
    def refreshAndRebuildLoadAllMenu(cls, parentMenuItem):
        cmds.menu(parentMenuItem, e=True, dai=True)
        
        builtCategories = cls.reloadAndReturnCategories()
        if not builtCategories:
            cls._addNoLoaderMenu(parentMenuItem)
            return 0
                
        for category in builtCategories:
            label = tr.MGP_Translate_rep1('pkr.loadAll.loadAll.prefix.mi', category.title())
            ann = tr.MGP_Translate_rep1('pkr.loadAll.loadAll.prefix.mi', category.title())
            cmds.menuItem(label=label, c=partial(cls.loadPickerForSceneRigs, category), p=parentMenuItem, ann=ann)
            
        cls._addReloadMenu(parentMenuItem)         
        count = len(builtCategories)  
        logger.debug('%s loadable categories found.' % count)
        return count
    