import os
import inspect
from maya import cmds

class HotkeyTip(object):
    def __init__(self, keyList, tip):
        self._ctrl = False
        self._shift = False
        self._alt = False
        self._key = ''
        self.tip = tip
        self.html = True # Use html format for str()
        for k in keyList:
            k = k.lower()
            if k == 'ctrl':
                self._ctrl = True
            elif k == 'shift':
                self._shift = True
            elif k == 'alt':
                self._alt = True
            else:
                self._key = k
                
    def isValid(self):
        return bool(self._key)
                
    def __str__(self, *args, **kwargs):
        if not self.isValid():
            return ""
        rep = []
        prefix = ''
        suffix = ''
        if self.html:
            prefix = '<b>'
            suffix = '</b>'
        if self._ctrl:
            if cmds.about(mac=True):
                rep.append(prefix + 'Command' + suffix)
            else:
                rep.append(prefix + 'Ctrl' + suffix)
        if self._shift:
            rep.append(prefix + 'Shift' + suffix)
        if self._alt:
            rep.append(prefix + 'Alt' + suffix)
        rep.append(prefix + self._key.capitalize() + suffix)
        return ((' + '.join(rep) ) + ' : ' + self.tip)
    
    def getKey(self):
        return self._key
        
        
class HotkeyLister(object):
    def __init__(self):
        self.html = True
        self._animatorHotkeys = {}
        self._designerHotkeys = {}
        self.readHotkeys()
        
    def getHotkeyDirectory(self):
        dirpath = inspect.getfile(inspect.currentframe()) 
        dirpath = os.path.dirname(dirpath)
        dirpath = os.path.dirname(dirpath)
        dirpath = os.path.dirname(dirpath)
        return '/'.join([dirpath, 'HotkeySets/'])
        
    def readHotkeysDoit(self, filePath, dictVar):
        dictVar.clear()
        with open(filePath, 'r') as f:
            for cLine in f:
                cLine = cLine.strip()
                if not cLine:
                    continue
                if cLine.startswith('#'):
                    continue
                keyValue = cLine.split(':')
                if len(keyValue) < 2:
                    continue
                keys = keyValue[0].strip().split(' ')
                tips = keyValue[-1].strip()
                cKey = HotkeyTip(keys, tips)
                if not cKey.isValid():
                    continue
                keyStroke = cKey.getKey()
                oldValues = dictVar.get(keyStroke, [])
                oldValues.append(cKey)
                dictVar[keyStroke] = oldValues
    
    def readHotkeys(self):
        hotkeyDir = self.getHotkeyDirectory()
        animHotkeyFile = hotkeyDir + 'animator.txt'
        designerHotkeyFile = hotkeyDir + 'designer.txt'
        self.readHotkeysDoit(animHotkeyFile, self._animatorHotkeys)
        self.readHotkeysDoit(designerHotkeyFile, self._designerHotkeys)
        
    def queryTip(self, mode, key):
        if not mode:
            keyObjList = self._animatorHotkeys.get(key)
        else:
            keyObjList = self._designerHotkeys.get(key)
        if not keyObjList:
            return ""
        newLine = '\n'
        if self.html:
            newLine = '<br>'
        return newLine.join([str(key) for key in keyObjList])
            