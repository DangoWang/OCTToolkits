import MGP.loader
import MGP.loadermanager

def MGP_LoadMGPickerViaPythonAutoLoaders(mayaNamespace):    
    return MGP.loadermanager.MGPickerLoaderManager.loadPicker(mayaNamespace)