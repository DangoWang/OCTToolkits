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

from ngSkinTools.ui.events import Signal


class ObservedValue(object):
    def __init__(self, name, initialValue=None):
        self.changed = Signal(name="cachedValue change (%s)" % name)
        self.value = initialValue

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.changed.emit()


class CachedValue(ObservedValue):
    undefined = {}

    def __init__(self, name, retrieveFunc):
        super(CachedValue, self).__init__(name, initialValue=CachedValue.undefined)
        self.retrieveFunc = retrieveFunc

    def dropCache(self):
        self.set(self.undefined)

    def get(self):
        if self.value is self.undefined:
            self.value = self.retrieveFunc()
        return self.value
