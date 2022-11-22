# -*- coding: utf-8 -*-

# Description:    + 移除晶格的同时，断开和物体的连接
# Author:         + xusheng
# Version:        + v001
# ChangeInfo      +
# Usage:          +



import maya.cmds as mc
import maya.mel as mel



latticeNodeType = 'lattice'
setNodeType = 'objectSet'


def getSelObjs():
    objList = mc.ls(sl=True, l=True)
    return objList

def getFFDNode(obj = ''):
    ffdNodeName = ''
    mc.select(cl=True)
    mc.select(obj, r=True)
    shapeObjList = mc.pickWalk(d='down')

    if mc.nodeType(shapeObjList[0]) == latticeNodeType:
        ffdList = mc.listConnections(shapeObjList[0] + '.latticeOutput', s=False, d=True)

        if len(ffdList) > 0:
            ffdNodeName = ffdList[0]
    return ffdNodeName

def disconnFFDWithMesh(objList = []):
    if objList and len(objList) > 0:
        for obj in objList:
            mc.select(cl=True)
            mc.select(obj, r=True)
            shapeObjList = mc.pickWalk(d='down')

            if (len(shapeObjList) > 0):
                try:
                    #polygon shape
                    shapeAttr = shapeObjList[0] + '.inMesh'
                    connAttrList = mc.listConnections(shapeAttr, d=False, s=True, p=True)

                    if (len(connAttrList) > 0 and connAttrList[0].find('ffd') > -1):
                        mc.disconnectAttr(connAttrList[0], shapeAttr)
                except:
                    #nurbs shape
                    shapeAttr = shapeObjList[0] + '.create'
                    connAttrList = mc.listConnections(shapeAttr, d=False, s=True, p=True)

                    if (len(connAttrList) > 0 and connAttrList[0].find('ffd') > -1):
                        mc.disconnectAttr(connAttrList[0], shapeAttr)

def rmLatticeFromObjs(objList = []):
    newList = []

    if len(objList) < 2:
        return
    else:
        ffdObj = getFFDNode(objList[0])
        ffdSetList = mc.ls('*'+ffdObj+'*', type=setNodeType)

        if len(ffdSetList) > 0:
            newList = objList[1:]
            mc.sets(newList, rm=ffdSetList[0])
    return newList


def addLatticeToObjs(objList = []):
    if len(objList) < 2:
        return
    else:
        ffdObj = getFFDNode(objList[0])
        ffdSetList = mc.ls('*' + ffdObj + '*', type=setNodeType)

        if len(ffdSetList) > 0:
            newList = objList[1:]
            mc.sets(newList, fe=ffdSetList[0])
