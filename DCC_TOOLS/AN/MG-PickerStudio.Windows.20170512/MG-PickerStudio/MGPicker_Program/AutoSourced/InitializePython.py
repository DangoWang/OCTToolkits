import os
import sys
import inspect
def initializePythonModules():
    dirpath = inspect.getfile(inspect.currentframe())
    dirpath = os.path.dirname(dirpath)    
    dirpath = os.path.dirname(dirpath)
    pythonRoot = '/'.join([dirpath, 'Python'])
    if not sys.path.count(pythonRoot):
        sys.path.append(pythonRoot)
        
    autoloaderRoot = '/'.join([dirpath, 'AutoLoaders'])
    if not sys.path.count(autoloaderRoot):
        sys.path.append(autoloaderRoot)
        
initializePythonModules()

