import os
import os.path
import math
import re

import maya.cmds as cmds
import maya.mel


# Default Nuke Camera Vert Aperture
DNCVA = 18.672
MODULUS = 25.39999962


# ##################################################################################################################################################################################

def getdata(camList=[]):
    if len(camList)==0:
        cam=cmds.ls(ca=1)
        for i in cam:
            c = cmds.listRelatives (i,p=1)[0]
            camList.append(c)
    global camDataDic
    camDataDic = {}
    
    global meshDataDic
    meshDataDic={}
    
    min = int(cmds.playbackOptions(q=1,min=1))
    max = int(cmds.playbackOptions(q=1,max=1)+1)
    camDataDic['timeRange'] = [min,max]
    for cam in camList:
        camDataDic[cam]={'translate':[[],[],[]],'rotate':[[],[],[]],'focal':[[]],'haperture':[[]],'vaperture':[[]]}
    gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar( gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    status='Camera Calculation ...',
                    maxValue=(max-min+1) )
    for time in range(min,max):
        cmds.currentTime(time,e=1)
        if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
            break
        cmds.progressBar(gMainProgressBar, edit=True, step=1)
        for cam in camList:
            t = cmds.xform(cam,q=1,ws=1,t=1)
            r = cmds.xform(cam,q=1,ws=1,ro=1)
            f = cmds.camera (cam,q=1,fl=1)
            hfa = cmds.camera (cam,q=1,hfa=1)*MODULUS
            vfa = cmds.camera (cam,q=1,vfa=1)*MODULUS
        
##            nukeFocalLength = DNCVA/2/math.tan(math.atan(vfa*MODULUS/(2*f)))
            for i in range(len(t)):
                camDataDic[cam]['translate'][i].append(' %s'%t[i])
            for i in range(len(r)):
                camDataDic[cam]['rotate'][i].append(' %s'%r[i])
            camDataDic[cam]['focal'][0].append(' %s'%f)
            camDataDic[cam]['haperture'][0].append(' %s'%hfa)
            camDataDic[cam]['vaperture'][0].append(' %s'%vfa)


    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
class CNuke:
    
    def __init__(self):
        self.nukeFile = ''
        self.setOption ()
        self.getMayaInfo()
        self.setCameraList()
        self.setMeshList()    
    def setSecne(self,scene='mayaToNuke'):
        self.scene = scene
        
    def setObj(self):
        cam = cmds.ls(sl=1,dag=1,typ='camera')
        mesh = cmds.ls(sl=1,dag=1,typ='mesh')
        cameraList = []
        meshList = []
        for i in cam:
            c = cmds.listRelatives (i,p=1)[0]
            cameraList.append(c)
        for i in mesh :
            m = cmds.listRelatives (i,p=1,f=1)[0]
            meshList.append(m)
        if 'Camera' in self.option['type']:
            self.setCameraList( cameraList)
        if 'Mesh' in self.option['type']:
            self.setMeshList( meshList)
            

    def setCameraList(self,camera=[]):
        self.camera =  camera
        self.camera.reverse()
    def setOption (self,option= {'type':['Camera','Mesh'],'anim':['Camera'],'net':'Bace'}):
        # net:None,Bace,ContactSheet
        self.option =     option
        
    def setMeshList(self,mesh=[]):
        'filter mesh list and set class mesh '
        removeIndex  = []
        self.mesh = {}
        if not 'Mesh' in self.option['type']:
            return
##        filter mesh

        for i in range(len(mesh)):
            for j in range(len(mesh)):
                if i ==j or j in removeIndex:
                    continue
                ad = cmds.listRelatives(mesh[i],f=1,ad=1)
                if mesh[j] in ad:
                    removeIndex.append(j)
                    
        for i in range(len(mesh)):
            if i not in removeIndex:
                    continue
            ad = cmds.listRelatives(mesh[i],f=1,ad=1)
            if mesh[j] in ad:
                    removeIndex.append(j)
                    
        for i in range(len(mesh)):
            if i not in removeIndex:
##              get image
                try:
                    shape = cmds.ls(mesh[i],dag=1,typ='mesh')[0]
                    sg = cmds.listConnections(shape,s=0,d=1,type="shadingEngine")[0]
                    shading = cmds.listConnections('%s.ss'%sg,s=1,d=0)[0]
                    imageNodeName = cmds.listConnections('%s.c'%shading,s=1,d=0,type="file")[0]
                except:
                    imageNodeName = ''     
                try:
                    imagePath = cmds.getAttr('%s.fileTextureName '%imageNodeName)
                    if not isAscii(imagePath):imagePath = ''
                except:
                    imagePath = ''
                self.mesh[mesh[i]]={'path':'','imageNodeName':imageNodeName,'imagePath':imagePath}                    
    def expObj(self):
        'export mesh,return export info'
        
        if not 'Mesh' in self.option['type'] :
            return
        
        if len(self.mesh)==0 :
            return
        global meshDataDic

##      adjust  frame  by animation option
        isAnim = 0
        if 'Mesh' in self.option['anim'] :
            isAnim = 1
        if  isAnim:
            min = self.min
            max = self.max+1
        else:
            min = self.frame
            max = self.frame+1
        gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
        cmds.progressBar( gMainProgressBar,
                        edit=True,
                        beginProgress=True,
                        isInterruptable=True,
                        status='Camera Calculation ...',
                        maxValue=(max-min+1) )
        
        for frame in range(min,max):
            cmds.currentTime(frame,update =1)
            if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
                break
            cmds.progressBar(gMainProgressBar, edit=True, step=1)
            
            for obj in self.mesh:
                shortName  =  cmds.ls(obj)[0]
                fileName = '%s/%s.%04d.obj'%(self.dirName,shortName,frame)
                if not  meshDataDic.has_key(obj):
                    meshDataDic [obj]=[]
            
                if not self.mesh[obj]['path']:
                    if isAnim:
                        self.mesh[obj]['path']='%s/%s.%%04d.obj'%(self.dirName,shortName)
                    else:
                        self.mesh[obj]['path']=fileName
##                 export obj

                if not frame in meshDataDic [obj]:
                    if os.path.exists(fileName):
                        try:
                            os.remove(fileName)
                        except:
                            continue                    
                    cmds.select(obj,r=1)
                    try:
                        cmds.file(fileName,op="groups=0;ptgroups=0;materials=0;smoothing=0;normals=1",typ="OBJexport",pr=1,es=1)
                    except:
                        if not 'objExport' in  cmds.pluginInfo (q=1,ls=1):
                            cmds.loadPlugin('objExport')
                        try:
                            cmds.file(fileName,op="groups=0;ptgroups=0;materials=0;smoothing=0;normals=1",typ="OBJexport",pr=1,es=1)
                        except:
                            continue
                    meshDataDic [obj].append(frame)
                    
                    
        cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
        
    def getMayaInfo(self):
        'get data from maya'
        try:
            self.frame = int (cmds.currentTime(q=1))
        except:
            self.frame = 1
            
        try:
            self.w= cmds.getAttr ("defaultResolution.width")
            self.h = cmds.getAttr ("defaultResolution.height")
        except:
            self.w= 640
            self.h = 480
            
        try:
            self.min = int(cmds.playbackOptions(q=1,min=1))
            self.max = int(cmds.playbackOptions(q=1,max=1))
        except:
            self.min = 1
            self.max = 24
        try:
            filePath = cmds.file(q=1,sn=1)
            if filePath:
                self.dirName ,self.scene = os.path.split(filePath)
                self.dirName+='/mayaTonuke'
            else:
                cmds.confirmDialog( title='Rest Setings', message='Save maya Scene First and Try again!',button = ['Ok'] )
        except:
            pass
            
        if not os.path.exists(self.dirName):
            try:
                os.makedirs(self.dirName)
            except:
                pass
    def setStack(self):
        nukeNode = '\nset N15f65a20 [stack 0]\npush 0'
        self.nukeFile +=nukeNode
        return nukeNode
    def pushStack(self):
        nukeNode = '\npush $N15f65a20\npush 0'
        self.nukeFile +=nukeNode
        return nukeNode
    def pushStack0(self):
        nukeNode = '\npush [stack 0]'
        self.nukeFile +=nukeNode
        return nukeNode
    def addCam(self,name='',pos=[0,0]):
        if  name =='' :return '\nCamera2 {\n inputs 0\n selected true\n xpos %s\n ypos %s\n}'%pos
        global camDataDic
        if not camDataDic.has_key(name) : return '\nCamera2 {\n inputs 0\n name "%s"\n selected true\n xpos %s\n ypos %s\n}'%(name,pos[0],pos[1])
        data = camDataDic[name]
        nukeNode =  '\nCamera2 {\n inputs 0\n name "%s"\n rot_order XYZ\n selected true\n xpos %s\n ypos %s\n'%(name,pos[0],pos[1])
        min = camDataDic['timeRange'][0]
        
        isAnim = 0
        frameIndex  = 0
        if 'Camera' in self.option['anim'] :
            isAnim = 1
            frameIndex  = self.frame - min
        try:
            translate = data['translate']            
            if isAnim :

                tx = ''
                ty = ''
                tz = ''
                for i in translate[0] :
                    tx+=i
                for i in translate[1]:
                    ty+=i
                for i in translate[2]:
                    tz+=i
                nukeNode += ' translate {{curve x%d%s} {curve x%d%s} {curve x%d%s}}\n'%(min,tx,min,ty,min,tz)
            else:
                nukeNode += ' translate {%s %s %s}\n'%(translate[0][frameIndex],translate[1][frameIndex],translate[2][frameIndex])
        except:
            pass
        
##        set rotate
        try:
            rotate = data['rotate']
            if isAnim :
                rx = ''
                ry = ''
                rz = ''
                for i in rotate[0] :
                    rx+=i
                for i in rotate[1]:
                    ry+=i
                for i in rotate[2]:
                    rz+=i
                nukeNode += ' rotate {{curve x%d%s} {curve x%d%s} {curve x%d%s}}\n'%(min,rx,min,ry,min,rz)
            else:
                nukeNode += ' rotate {%s %s %s}\n'%(rotate[0][frameIndex],rotate[1][frameIndex],rotate[2][frameIndex])
        except:
            pass      
        try:
            focal = data['focal']
            if isAnim :
                fo= ''
                for i in focal[0] :
                    fo+=i
                nukeNode += ' focal {{curve x%d%s}}\n'%(min,fo)
            else:
                nukeNode += ' focal %s\n'%focal[0][frameIndex]
        except:
            pass
        try:
            haperture = data['haperture']
            if isAnim :
                
                ha= ''
                for i in haperture[0] :
                    ha+=i
                nukeNode += ' haperture {{curve x%d%s}}\n'%(min,ha)
            else:
                
                nukeNode += ' haperture %s\n'%haperture[0][frameIndex]
        except:
            pass
        try:
            vaperture = data['vaperture']
            if isAnim :
                
                va= ''
                for i in vaperture[0] :
                    va+=i
                nukeNode += ' vaperture {{curve x%d%s}}\n'%(min,va)
            else:
                nukeNode += ' vaperture %s\n'%vaperture[0][frameIndex]
        except:
            pass
        
        nukeNode +='}'
        self.nukeFile +=nukeNode
        return nukeNode
    def addRoot (self):
        nukeNode = '''
Root {
 inputs 0
 frame %s
 first_frame %s
 last_frame %s
 format "%s %s 0 0 %s %s 1 %s %s"
}'''%(self.frame,self.min,self.max,self.w+1,self.h,self.w+1,self.h,self.w+1,self.h)
        self.nukeFile +=nukeNode
        return nukeNode
    def addScenes(self,name='',inputs  = 0 ,pos=[0,0]):
        nukeNode =  '\nScene {\n inputs %s\n name "%s"\n selected true\n xpos %s\n ypos %s\n}'%(inputs,name,pos[0],pos[1])
        self.nukeFile +=nukeNode
        return nukeNode
    def addScanlineRender(self,name='',pos=[0,0]):
        nukeNode =   '\nScanlineRender {\n inputs 3\n name "render_%s"\n selected true\n xpos %s\n ypos %s\n}'%(name,pos[0],pos[1])
        self.nukeFile +=nukeNode
        return nukeNode
    def addContactSheet(self,size=1,pos=[0,0]):                 
        nukeNode =  '\nContactSheet {\n inputs %s\n width %s\n height %s\n rows %s\n columns %s\n center true\n selected true\n xpos %s\n ypos %s\n}'%(size,size*self.w,self.h,1,size,pos[0],pos[1])
        self.nukeFile +=nukeNode
        return nukeNode  
    def addRead(self,name='',file = '',pos=[0,0]):
        nukeNode =   '\nRead {\n inputs 0\n name "%s"\n selected true\n file "%s"\n xpos %s\n ypos %s\n}'%(name,file,pos[0],pos[1])
        self.nukeFile +=nukeNode
        return nukeNode 
    def addReadGeo2(self,name='',file = '',pos=[0,0],inputs  = 0):
        nukeNode =   '\nReadGeo2 {\n name "%s"\n inputs %s\n selected true\n file "%s"\n xpos %s\n ypos %s\n}'%(name,inputs,file,pos[0],pos[1])
        self.nukeFile +=nukeNode
        return nukeNode
    def generatorScens(self,yPos=0):
        self.expObj()
        size = len(self.mesh)
        num = 0
        xStart = size*-50+50
        if self.option['net']!='None':
            self.pushStack0()
        for obj in self.mesh:
            meshName = cmds.ls(obj)[0]
            path = self.mesh[obj]['path'].replace('\\','/')
            imageNodeName = self.mesh[obj]['imageNodeName']
            imagePath = self.mesh[obj]['imagePath'].replace('\\','/')
            xPos = xStart+num*100
            if imagePath:
                self.addRead(imageNodeName,imagePath,[xPos,yPos])
                self.addReadGeo2(meshName,path,[xPos,yPos+100],1)
            else:
                self.addReadGeo2(meshName,path,[xPos,yPos+100],0)
            num +=1
        if self.option['net']!='None':
            self.addScenes(self.scene,num,[0,yPos+200])
        return yPos+300
    def generator(self,yPos=0):
        self.addRoot()
        size = len(self.camera)
        xStart = size*-50+50
        if size==0:
            self.generatorScens(yPos)
        else:
            for i in range(size):
                xPos = xStart+i*100
                self.addCam(self.camera[i],[xPos,yPos+300])
                if(i==0):
                    self.generatorScens(yPos)
                    if self.option['net']!='None':
                        self.setStack()
                else:
                    if self.option['net']!='None':
                        self.pushStack()
                if self.option['net']!='None':    
                    self.addScanlineRender(self.camera[i],[xPos,yPos+400])
            if self.option['net']=='ContactSheet':
                self.addContactSheet(size,[0,yPos+500])
                
def mayaToNuke():
    window = "mayaToNuke"
    if cmds.window(window,ex=1) : cmds.deleteUI(window)
    cmds.window(window,menuBar=1 )
    cmds.menu(tearOff = 1,l='Edit')
    cmds.menuItem(l='Calculate Maya Data',c=getAllCamera)
    cmds.menuItem(divider =1)
    cmds.menuItem(l='Generator Nuke Script',c=generator)
    cmds.menuItem(l='Show Nuke Script',c = m2nShowText)    
    cmds.menuItem(l='Save Nuke Script As',c=saveNukeScript)
    cmds.menuItem(divider =1)
    cmds.menuItem(l='Rest Setings',c=restSetings)
    cmds.menuItem(l='Exit',c='cmds.deleteUI("mayaToNuke")')      
        
    cmds.menu(tearOff = 1,l='Type')
    cmds.menuItem('typeAll',l='All',checkBox=1,c=adjOption)
    cmds.menuItem(divider =1)
    cmds.menuItem('typeCamera',l='Camera',checkBox=1,c=setOption)
    cmds.menuItem('typeMesh',l='Mesh',checkBox=1,c=setOption)
    cmds.menu(tearOff = 1,l='Animation')
    cmds.menuItem('animAll',l='All',checkBox=1,c=adjOption)
    cmds.menuItem(divider =1)
    cmds.menuItem('animCamera',l='Camera',checkBox=1,c=setOption)
    cmds.menuItem('animMesh',l='Mesh',checkBox=0,c=setOption)
    cmds.menu(tearOff = 1,l='Networks')
    cmds.radioMenuItemCollection()
    cmds.menuItem('netNone',l='None',radioButton=0,c=setOption) 
    cmds.menuItem('netBace',l='Bace',radioButton=1,c=setOption) 
    cmds.menuItem('netContactSheet',l='ContactSheet',radioButton=0,c=setOption) 

    cmds.menu(l='Help')
    cmds.menuItem(l='Help',c = 'm2nShowText("help")') 
    cmds.menuItem(l='About',c = aboutThis)
    mianLayout=cmds.formLayout(nd=1000)
    b1 = cmds.outlinerEditor('dirList')
    cmds.outlinerEditor('dirList',
                        e=1,
                        mainListConnection="worldList",
                        selectionConnection="modelList",
                        showShapes=0,
                        showAttributes=0,
                        showConnected=0,
                        showAnimCurvesOnly=0,
                        autoExpand=0,
                        showDagOnly=1,
                        ignoreDagHierarchy=0,
                        expandConnections=0,
                        showNamespace=1,
                        showCompounds=1,
                        showNumericAttrsOnly=0,
                        highlightActive=1,
                        autoSelectNewObjects=0,
                        doNotSelectNewObjects=0,
                        transmitFilters=0,
                        showSetMembers=1,
##                        setFilter="DefaultAllLightsFilter"
                        )
    cmds.cmdScrollFieldExecuter('copytext',vis=0)
    b2 = cmds.textField('filterText',cc=setFilterName,ec = setFilterName)
    b3 = cmds.button(l="Generator",c=generator)
    cmds.formLayout(mianLayout,
                    e=1,
                    attachControl=[(b1,"top",3 ,b2),
                                   (b1,"bottom",3 ,b3)],
                    attachForm=[(b1 ,"left",3),
                                (b1 ,"right",3),
                                (b2 ,"top",3),
                                (b2 ,"left",3),
                                (b2 ,"right",3),
                                (b3 ,"bottom",3),
                                (b3 ,"left",3),
                                (b3 ,"right",3),],
                    attachNone=[(b2 ,"bottom" ),
                                (b3 ,"top" )])
    cmds.window(window,e=1,t="mayaToNuke",widthHeight=(300, 700))
    cmds.showWindow(window)
    getOption()
def adjOption (*args):
    typeAll = cmds.menuItem('typeAll',q=1,cb=1)
    animAll = cmds.menuItem('animAll',q=1,cb=1)
    if typeAll :
        cmds.menuItem('typeCamera',e=1,cb=1)
        cmds.menuItem('typeMesh',e=1,cb=1)
    else:
        cmds.menuItem('typeCamera',e=1,cb=0)
        cmds.menuItem('typeMesh',e=1,cb=0)
    if animAll :
        cmds.menuItem('animCamera',e=1,cb=1)
        cmds.menuItem('animMesh',e=1,cb=1)
    else:
        cmds.menuItem('animCamera',e=1,cb=0)
        cmds.menuItem('animMesh',e=1,cb=0)
    setOption(*args)
def restSetings (*args):
    cmds.optionVar( remove='m2nType' )
    cmds.optionVar( sva=('m2nType', 'Camera') )
    cmds.optionVar( sva=('m2nType', 'Mesh') )
    cmds.optionVar( remove='m2nAnim' )
    cmds.optionVar( sva=('m2nAnim', 'Camera') )
    cmds.optionVar( sv=('m2nNet', 'Bace') )
    getOption()
    cmds.confirmDialog( title='Rest Setings', message='Succeed!',button = ['Ok'] )
def setOption (*args):    
    typeCamera = cmds.menuItem('typeCamera',q=1,cb=1)
    typeMesh = cmds.menuItem('typeMesh',q=1,cb=1)
    if typeCamera and  typeMesh:
        cmds.menuItem('typeAll',e=1,cb=1)
    else:
        cmds.menuItem('typeAll',e=1,cb=0)
    m2nType = []
    if typeCamera:
        m2nType.append('Camera')
    if typeMesh:
        m2nType.append('Mesh')
    cmds.optionVar( remove='m2nType' )
    for i in m2nType:
        cmds.optionVar( sva=('m2nType', i) )
    animCamera = cmds.menuItem('animCamera',q=1,cb=1)
    animMesh = cmds.menuItem('animMesh',q=1,cb=1)
    if animCamera and  animMesh:
        cmds.menuItem('animAll',e=1,cb=1)
    else:
        cmds.menuItem('animAll',e=1,cb=0)
    m2nAnim = []
    if animCamera:
        m2nAnim.append('Camera')
    if animMesh:
        m2nAnim.append('Mesh')
    cmds.optionVar( remove='m2nAnim' )
    for i in m2nAnim:
        cmds.optionVar( sva=('m2nAnim', i) )
    netNone = cmds.menuItem('netNone',q=1,radioButton=1)
    netBace = cmds.menuItem('netBace',q=1,radioButton=1)
    netCont = cmds.menuItem('netContactSheet',q=1,radioButton=1)

    m2nNet = 'Bace'
    if netNone:
        m2nNet = 'None'
    elif netBace :
        m2nNet = 'Bace'
    elif netCont:
        m2nNet = 'ContactSheet'
    cmds.optionVar( sv=('m2nNet', m2nNet) )
    
##    print cmds.optionVar( q='m2nNet' )
    setFilter()
def setFilter(nameFilter=''):
    m2nType = cmds.optionVar( q='m2nType' )
    types = []
    try:
        for i in m2nType:
            type = i.lower()
            types.append(type)
        filter = cmds.itemFilter  (byType =types )
    except:
        filter = cmds.itemFilter  (byType =['unknown'] )
        
    if not nameFilter:
        nameFilter = cmds.textField('filterText',q=1,tx=1)
    if nameFilter:
        name = '*%s*'%nameFilter
        nFilter = cmds.itemFilter  (byName =name )
        filter = cmds.itemFilter  (intersect = (nFilter,filter) )
        
    cmds.outlinerEditor ('dirList',e=1,filter=filter)
    
def setFilterName(*args):
    setFilter(args[0])
def getOption():
    type = ['Camera','Mesh']
    m2nType = cmds.optionVar( q='m2nType' )
    for i in type:
        name = 'type%s'%i        
        try:    
            cmds.menuItem(name,e=1,checkBox=(i in m2nType))         
        except:
            cmds.menuItem(name,e=1,checkBox=0)       
    
    m2nAnim = cmds.optionVar( q='m2nAnim' )
    for i in type:
        name = 'anim%s'%i        
        try:    
            cmds.menuItem(name,e=1,checkBox=(i in m2nAnim))         
        except:
            cmds.menuItem(name,e=1,checkBox=0)
            
    
    m2nNet = cmds.optionVar( q='m2nNet' )
    try:
        menuItemName = 'net%s'%m2nNet
        cmds.menuItem(menuItemName,e=1,radioButton=1)
    except:
        cmds.menuItem('netBace',e=1,radioButton=1)
    setOption ()
    global camDataDic
    try:
        temp = camDataDic
    except:
        getdata()
def aboutThis(*args):
    msg = '''This is  maya python script.
Able to translate maya data to nuke.

version 2.0.1

pzhaojing@163.com
'''
    cmds.confirmDialog( title='mayaToNuke', message=msg, button=['OK'] )

def m2nShowText(*args):
    window = "help"
    if cmds.window(window,ex=1) : cmds.deleteUI(window)
    cmds.window(window)
    mianLayout=cmds.formLayout(nd=1000)
    control1 = cmds.scrollField()
    cmds.formLayout(mianLayout,e=1,
                    attachPosition = [(control1,"left",0 ,0),
                                      (control1,"right",0 ,1000),
                                      (control1,"top",0 ,0),
                                      (control1,"bottom",0 ,1000)]
                    )
    cmds.window(window,e=1,t="Nuke Script",widthHeight=(500, 500))
    cmds.showWindow(window)
    text =cmds.cmdScrollFieldExecuter('copytext' ,q=1,t=1) 
    if args[0] =="help":
        text =r'''mayaToNuke v2.0.1

Now! Geometry can be exported. Usage is as simple as ever.

Features:

Export Geometry
Export Camera
Auto Export texture
Animation switch
Save as ". Nk" file
Improved interface
Smart Filter

Workflow:
    1. Copy mayaToNuke.py to "My Documents\maya\20XX\scripts"
    2. In python command port.Type "from mayaToNuke import *". Open mayaToNuke UI.
    3. In Type menu. Select export type. Camera, mesh or all.
    4. In Animation menu. Select animation type. Camera, mesh or all.
    5. in Networks menu.Choose nuke networks type.
         None: Only the original node
         Base: Build basic 3d scenemayaToNuke
         ContactSheet: Contact camera
    6. Select the object you want to export.
    8. Click Generator Button.
    9. into nuke press ctr + v.

Note:

When the maya scene is changed. You need to update mayaToNuke data. Click "edit / Calculate Maya Data".
You can view and save nukeScript. Click "edit / Show Nuke Script", "edit / Save Nuke Script As".

Good luck.

2010.6.17'''
        cmds.window(window,e=1,t="Help")
    cmds.scrollField(control1,e=1,tx = text)
def saveNukeScript(*args):
    text =cmds.cmdScrollFieldExecuter('copytext' ,q=1,t=1)
    if not text :
        cmds.confirmDialog( title='Save Nuke Script', message='Nothing script to be saved!',button = ['Ok'] )
        return
    fileName  = cmds.fileDialog(m=1,t = 'Save Nuke Script As',dm = '.nk',dfn='mayaToNukemayaToNuke.nk')
    f = file(fileName,'w')
    f.write(text)
    f.close()
def getAllCamera(*args):
    camera=[]
    cam=cmds.ls(ca=1)
    for i in cam:
        c = cmds.listRelatives (i,p=1)[0]
        camera.append(c)
    if args:
        getdata(camera)
    else:
        global camDataDic
        try:     
            if not camDataDic :getdata(camera)
        except:
            getdata(camera)
def generator(*args):
    nuke = CNuke()
    m2nType = cmds.optionVar( q='m2nType' )
    if m2nType ==0: m2nType = []
    m2nAnim = cmds.optionVar( q='m2nAnim' )
    if m2nAnim ==0:m2nAnim = []
    m2nNet = cmds.optionVar( q='m2nNet' )
    if m2nNet ==0: m2nNet = 'None'
    nuke.setOption({'type':m2nType,'anim':m2nAnim,'net':m2nNet})
    nuke.setObj()
    nuke.generator()
    
    cmds.cmdScrollFieldExecuter('copytext' ,e=1,clr=1)
    cmds.cmdScrollFieldExecuter('copytext' ,e=1,t=nuke.nukeFile)
    cmds.cmdScrollFieldExecuter('copytext' ,e=1,selectAll=1)
    cmds.cmdScrollFieldExecuter('copytext' ,e=1,copySelection=1)
    msg = '''Succeed!\nTo Nuke and press ctr+v.'''
    cmds.confirmDialog( title='mayaToNuke', message=msg, button=['OK'] ) 
    
def isAscii(s):
    try:
        return s == re.findall(r'^[\x00-\x7f]+$',s)[0]
    except:
        return False
mayaToNuke()
