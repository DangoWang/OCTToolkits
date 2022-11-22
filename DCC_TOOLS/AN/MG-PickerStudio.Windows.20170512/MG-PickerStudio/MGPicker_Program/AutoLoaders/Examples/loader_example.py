from MGP import loader

class My_PickerLoaderExample(loader.MGPickerLoaderBase):
    def pickerFileForAssetName(self, assetName):
        # This is a hard-code bad example, but anyway you should return a path to a picker file:
        return 'D:/My Documents/maya/MG_PickerData/Default/chase/chase.mgpkr'
    
    
class MGPickerRigListerExample(loader.MGPickerRigListerBase):
    
    def mayaScene_rigs(self):
        # Retrieve maya rigs you wanna load pickers somehow and return the list:
        return ['char1', 'char2', 'prop1', 'set1']
    
    def mayaScene_characters(self):
        return ['char1', 'char2']
    
    def mayaScene_props(self):
        return ['prop1']
    
    def mayaScene_sets(self):
        return ['set1']