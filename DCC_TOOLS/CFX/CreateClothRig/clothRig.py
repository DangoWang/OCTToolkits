# -*- coding: utf-8 -*-

# Description:    + cloth Rig maya相关执行函数
# Author:         + xusheng
# Version:        + v001
# ChangeInfo      +
# Usage:          +



import maya.cmds as mc
import maya.mel as mel
import os
import mayaCommon as macomm
reload(macomm)


class _OCT_CreateClothRig():
    def __init__(self):
        self.meshNodeType = 'mesh'
        self.transNodeType = 'transform'
        self.stdClothGrp = 'clothes_Grp'
        self.stdGeoGrp = 'Geometry'
        self.stdSimGrp = 'sim'
        self.stdColGrp = 'collider'

    def isObjsFromClothesGrp(self, objList = []):
        newObjList = []

        if objList and objList[0].split('|')[-1] == self.stdClothGrp:
            mc.select(objList[0], r=True, hi=True, ne=True)
            newObjList = mc.ls(sl=True, l=True)
        else:
            for obj in objList:
                objPart = obj.split('|')

                if len(objPart) > 4 and objPart[4] == self.stdClothGrp:
                    newObjList.append(obj)
        return newObjList

    def getSelObjs(self):
        objList = mc.ls(sl=True, l=True)
        return objList

    def filterMeshObjsInSelect(self, objList=[]):
        meshObjList = []

        for obj in objList:
            if self.transNodeType == mc.nodeType(obj):
                mc.select(cl=True)
                mc.select(obj, r=True)
                childNodeList = mc.pickWalk(d='down')

                if childNodeList and mc.nodeType(childNodeList[0]) == self.meshNodeType:
                    meshObjList.append(obj)
        mc.select(meshObjList, r=True)
        return meshObjList

    def arrangeOriClothGrp(self, selObjList = [], simGrp = ''):
        finalOriObjList = []
        finalOriClothesGrp = ''

        if selObjList:
            clothesGrpPart = selObjList[0].split('|')
            clothesGrpPart.remove(clothesGrpPart[-1])
            clothesGrp = '|'.join(clothesGrpPart)
            mc.select(cl=True)
            dupClothesGrp = mc.duplicate(clothesGrp, rr=True)
            mc.select(dupClothesGrp, r=True)
            newClothesGrp = mc.ls(sl=True, l=True)
            newClothesGrpPart = newClothesGrp[0].split('|')

            if self.stdGeoGrp == newClothesGrpPart[2]:
                #geoGrp = '|'.join(newClothesGrpPart[:3])
                mc.hide(newClothesGrp)
                newparentedClothesGrp = mc.parent(newClothesGrp, simGrp, r=True)
                finalOriClothesGrp = mc.rename(newparentedClothesGrp[0], self.stdClothGrp)
            else:
                mc.delete(newClothesGrp)

        if finalOriClothesGrp:
            mc.select(finalOriClothesGrp, r=True, hi=True, ne=True)
            finalOriObjList = mc.ls(sl=True, l=True)
            finalOriObjList = self.filterMeshObjsInSelect(finalOriObjList)
        return finalOriObjList

    def getSimGrp(self):
        simGrp = ''
        transGrpList = mc.ls(tr=True, l=True)

        for transGrp in transGrpList:
            transGrpPart = transGrp.split('|')

            if len(transGrpPart) == 3 and self.stdSimGrp == transGrpPart[2]:
                simGrp = transGrp
                break

        if not simGrp:
            for transGrp in transGrpList:
                transGrpPart = transGrp.split('|')

                if (len(transGrpPart) > 2) and transGrpPart[2] == self.stdGeoGrp:
                    parentGrp = '|'.join(transGrpPart[:2])
                    mc.select(cl=True)
                    #maya mel cannot raise error correctly, here lost em=True, can make program crush randomly, so should strictly use function
                    simGrp = mc.group(n=self.stdSimGrp, p=parentGrp, em=True)
                    simGrpList = mc.select(simGrp, r=True)
                    simGrpList = mc.ls(sl=True, l=True)
                    simGrp = simGrpList[0]
                    break
        #need the two steps ahead to generate simGrp
        if simGrp:
            try:
                mc.nodeType(simGrp + '|' + self.stdColGrp)
            except:
                colGrp = mc.group(n=self.stdColGrp, em=True, p=simGrp)
                constrainGrp = mc.group(n='constraint', em=True, p=simGrp)
        return simGrp

    def addSimSuffix(self, simObjList=[]):
        newSimObjList = []

        for simObj in simObjList:
            simObjPart = simObj.split('|')
            simObjFlag = simObjPart[-1].split('_')[-1]

            if simObjFlag != self.stdSimGrp:
                newName = simObjPart[-1] + '_' + self.stdSimGrp
                newName = mc.rename(simObj, newName)
                mc.select(newName, r=True)
                newNameLongList = mc.ls(sl=True, l=True)
                newSimObjList.append(newNameLongList[0])
        return newSimObjList

    def createClothObjs(self, meshObjList=[]):
        newClothObjList = []

        for mesh in meshObjList:
            mc.select(mesh, r=True)
            newClothShape = mel.eval('createNCloth 0')
            realName = mesh.split('|')[-1].split('_')[0]
            newClothShape = mc.rename(newClothShape, 'nCloth_' + realName + 'Shape')
            mc.select(newClothShape, r=True)
            newClothList = mc.pickWalk(d='up')
            newCloth = mc.rename(newClothList[0], 'nCloth_' + realName)
            mc.select(newCloth, r=True)
            newCloth = mc.ls(sl=True, l=True)
            newClothObjList.append(newCloth[0])
        return newClothObjList

    def putNClothSolverInSimGrp(self, simGrp=''):
        nucleusList = mc.ls(l=True, type='nucleus')
        newSolverList = []

        for nSolver in nucleusList:
            if nSolver.split('|')[-2] != self.stdSimGrp:
                newSolverList.append(nSolver)

        if newSolverList:
            mc.parent(newSolverList, simGrp, r=True)

    def putNClothInSimGrp(self, simGrp='', selSimObjList=[], clothObjList=[]):
        meshInSimGrpList = []

        if simGrp and selSimObjList:
            for obj in selSimObjList:
                mc.select(obj, r=True)
                objLongName = mc.ls(sl=True, l=True)
                longNamePart = objLongName[0].split('|')

                if len(longNamePart) != 4 or longNamePart[2] != self.stdSimGrp:
                    newSimObjList = mc.parent(obj, simGrp, r=True)
                    mc.select(newSimObjList[0], r=True)
                    newSimObjList = mc.ls(sl=True, l=True)
                    meshInSimGrpList.append(newSimObjList[0])
                else:
                    meshInSimGrpList.append(obj)

            if clothObjList:
                mc.parent(clothObjList, simGrp, r=True)
        return meshInSimGrpList

    def arrangeSimClothGrp(self, selSimObjList = []):
        simGrp = self.getSimGrp()
        newSimObjList = self.addSimSuffix(selSimObjList)

        if newSimObjList:
            selSimObjList = newSimObjList
        clothObjList = self.createClothObjs(selSimObjList)
        self.putNClothInSimGrp(simGrp, selSimObjList, clothObjList)
        self.putNClothSolverInSimGrp(simGrp)
        return clothObjList

    def createCollideObjs(self, simGrp, selColObjList = []):
        colGrp = simGrp + '|' + self.stdColGrp
        blendResultList = []
        rigidResultList = []

        for obj in selColObjList:
            realName = obj.split('|')[-1].split('_')[0]
            dupColObjList = mc.duplicate(obj, rr=True)
            newColObj = mc.rename(dupColObjList[0], realName + '_collide')
            blendResult = self.createColBlendShape(obj, newColObj)
            blendResultList.append(blendResult)
            mc.select(newColObj, r=True)
            rigidObjList = mel.eval('makeCollideNCloth')
            #no 'ne' flag
            mc.select(rigidObjList[0], r=True)
            #this gun return is a LIST,remember!
            rigidObjList = mc.pickWalk(d='up')
            newRigid = mc.rename(rigidObjList[0], 'nRigid_' + realName)
            rigidResultList.append(newRigid)
            mc.parent([newColObj,newRigid], colGrp, r=True)
        return [blendResultList, rigidResultList]

    def createColBlendShape(self, oriObj = '', targetObj = ''):
        if oriObj and targetObj:
            mc.select(oriObj, r=True)
            mc.select(targetObj, add=True)
            mc.blendShape(w=[(0, 1.0)])
            return (oriObj + ' ----> ' + targetObj)

    def arrangeColClothGrp(self, selColObjList = []):
        simGrp = self.getSimGrp()
        colResultList = [[''], ['']]

        if simGrp and selColObjList:
            colResultList = self.createCollideObjs(simGrp, selColObjList)
            self.putNClothSolverInSimGrp(simGrp)
        return colResultList

    def createWrap(self, oriObjList = [], tarObjList = []):
        wrapPairList = []

        for oriObj in oriObjList:
            for tarObj in tarObjList:
                realOriName = oriObj.split('|')[-1].split('_')[0]
                realTarName = tarObj.split('|')[-1].split('_')[0]

                if realOriName == realTarName:
                    mc.select(tarObj, r=True)
                    mc.select(oriObj, add=True)
                    mel.eval('performCreateWrap false')
                    wrapPairList.append(oriObj.split('|')[-1] + ' ----> ' + tarObj.split('|')[-1])
                    break
        return wrapPairList














