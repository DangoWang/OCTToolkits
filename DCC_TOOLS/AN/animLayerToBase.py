#-*- coding: utf-8 -*-
####################################################
# Copyright 2016 October Media. All rights reserved.
# Bake AnimLayer to BaseLayer
# Author: Gao Lei
####################################################
import maya.cmds as mc
import maya.OpenMaya as om

#A decorator that will make commands undoable in maya
def undoable(function):
    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)
        except:
            print sys.exc_info()[1]
        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn
    return decoratorCode

class animLayerToBase():
    def __init__(self, *arg):
        self.baseCurves=[]
        self._command()
    def findAnimCurve(self,attr):
        animCurve = None
        plugs = mc.listConnections(attr,d=0)
        if plugs:
            plugs = list(set(plugs))
            for p in plugs:
                if mc.nodeType(p) == 'animLayer':
                    continue
                if p in self.baseCurves:
                    animCurve = p
                    break
                else:
                    animCurve = self.findAnimCurve(p)
        return animCurve
    @undoable
    def _command(self):
        self.baseCurves = []
        baseAttrs = []
        baseLayer = mc.animLayer(q=1,r=1)
        layerList = []
        for l in mc.ls(type='animLayer'):
            if l == baseLayer:
                if not mc.animLayer(l,q=1,sel=1):
                    om.MGlobal.displayError(u'没选择基础动画层。')
                    return
                continue
            if mc.animLayer(l,q=1,sel=1):
                layerList.append(l)
        if not layerList:
            om.MGlobal.displayError(u'没选择要合并的动画层。')
            return
        for l in layerList:
            curves = mc.animLayer(l,q=1,bac=1)
            if curves:
                for c in curves:
                    if not c in self.baseCurves:
                        self.baseCurves.append(c)
            attrs = mc.animLayer(l,q=1,at=1)
            if attrs:
                for a in attrs:
                    a = mc.ls(a,l=1)[0]
                    if not a in baseAttrs:
                        baseAttrs.append(a)
        keyDict = {}
        valueDict = {}
        curveDict = {}
        keyList = []
        for a in baseAttrs:
            c = self.findAnimCurve(a)
            if c:
                curveDict[a] = c
                keys = mc.keyframe(c, q=1)
                keyDict[a] = keys
                for k in keys:
                    if not k in keyList:
                        keyList.append(k)
        keyList.sort()
        for k in keyList:
            mc.currentTime(k)
            for a in curveDict.keys():
                if k in keyDict[a]:
                    v = mc.getAttr(a)
                    valueDict.setdefault(a,[])
                    valueDict[a].append(v)

        for l in layerList:
            mc.animLayer(l,e=1, mute=1)
            mc.animLayer(l,e=1, lock=1)

        for a in curveDict.keys():
            k=keyDict[a]
            v=valueDict[a]
            c=curveDict[a]
            for i in range(len(k)):
                mc.setKeyframe(c,t=k[i],v=v[i])
        result = mc.confirmDialog(title=u'删除', message=u'是否删除已合并的动画层?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            for l in layerList:
                mc.delete(layerList)