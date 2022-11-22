import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import os, ConfigParser, time
import template as tp
from functools import partial
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement
import webbrowser
mainUiContent = {}
mayaNodeNames = ['defaultRenderUtilityList1',
 'defaultLightSet',
 'defaultTextureList1',
 'defaultObjectSet',
 'defaultShaderList1',
 'defaultLayer',
 'defaultRenderLayer',
 'defaultViewColorManager',
 'initialShadingGroup',
 'hyperLayout1',
 'initialParticleSE',
 'renderPartition',
 'persp',
 'perspShape',
 'top',
 'topShape',
 'front',
 'frontShape',
 'side',
 'sideShape',
 'layerManager',
 'sequenceManager1',
 'dof1',
 'dynController1',
 'globalCacheControl',
 'hardwareRenderGlobals',
 'hardwareRenderingGlobals',
 'defaultHardwareRenderGlobals',
 'ikSystem',
 'hikSolver',
 'ikRPsolver',
 'ikSCsolver',
 'ikSplineSolver',
 'lambert1',
 'lightLinker1',
 'particleCloud1',
 'characterPartition',
 'renderPartition',
 'shaderGlow1',
 'strokeGlobals',
 'time1']
minorNodeTypes = cmds.optionVar(query='minorNodeTypes')
mayaNodeTypes = []
for nodeTag in minorNodeTypes:
    nodeType = cmds.objectType(tpt=nodeTag)
    if nodeType != 'materialInfo':
        mayaNodeTypes.append(nodeType)

mayaNodeTypes.sort()
mayaNodeNames.sort()

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')


class shaderTypesFile():

    def __init__(self, fileDir, fileName, *args):
        self.shaderTypesFile = fileDir + '/' + fileName
        if not os.path.exists(self.shaderTypesFile):
            self.shaderTypeList = ['lambert',
             'blinn',
             'anisotropic',
             'phong',
             'aiStandard',
             'aiSkinSss',
             'RedshiftArchitectural']
            self.writeXmlFile(typeList=self.shaderTypeList)

    def typeList(self):
        tree = ElementTree.parse(self.shaderTypesFile)
        root = tree.getroot()
        typeElements = root.getiterator('type')
        typeList = []
        for type in typeElements:
            typeList.append(type.get('name'))

        typeList.sort()
        return typeList

    def removeType(self, removeType):
        newTypeList = []
        typeList = self.typeList()
        for shaderType in typeList:
            if shaderType != removeType:
                newTypeList.append(shaderType)

        self.writeXmlFile(newTypeList)

    def addType(self, addType):
        typeList = self.typeList()
        typeList.append(addType)
        typeList.sort()
        self.writeXmlFile(typeList)

    def writeXmlFile(self, typeList):
        shaderTypesElement = Element('shaderTypes')
        for shader in typeList:
            shaderElement = SubElement(shaderTypesElement, 'type')
            shaderElement.set('name', shader)

        psetCommand = prettify(shaderTypesElement)
        xFile = open(self.shaderTypesFile, 'w')
        xFile.write(psetCommand)
        xFile.close()


class iniFile():

    def __init__(self, fileDir, fileName, *args):
        self.iniFile = fileDir + '/' + fileName
        self.config = ConfigParser.ConfigParser()
        if not os.path.exists(self.iniFile):
            self.config.add_section('setting')
            self.config.set('setting', 'language', '')
            self.config.set('setting', 'presets_dir', '')
            self.config.write(open(self.iniFile, 'w'))

    def getValue(self, item, *args):
        self.config.readfp(open(self.iniFile))
        return self.config.get('setting', item)

    def setValue(self, item, value, *args):
        self.config.read(self.iniFile)
        self.config.set('setting', item, value)
        self.config.write(open(self.iniFile, 'w'))


class removeShaderTypeWin(tp.templateWindow):

    def __init__(self, shaderTypesFile, uiContent, *args):
        tp.templateWindow.__init__(self)
        self.shaderTypesFile = shaderTypesFile
        self.uiContent['window'] = 'jn_removeShaderTypeWindow'
        self.uiContent['title'] = u'Remove Shader Type'
        self.uiContent['size'] = (300, 360)
        self.uiContent['commonButton'] = True
        self.uiContent['commonButtonName'] = 'Remove'
        self.parentUiContent = uiContent

    def displayOptions(self, *args):
        self.uiContent['columnLayout'] = cmds.columnLayout(adj=True)
        self.uiContent['textScrollList'] = cmds.textScrollList(parent=self.uiContent['columnLayout'], numberOfRows=20, allowMultiSelection=True, showIndexedItem=4)
        for shader in self.shaderTypesFile.typeList():
            cmds.textScrollList(self.uiContent['textScrollList'], edit=True, append=shader)

        cmds.formLayout(self.uiContent['optionsForm'], e=True, attachForm=([self.uiContent['columnLayout'], 'top', 0],
         [self.uiContent['columnLayout'], 'left', 2],
         [self.uiContent['columnLayout'], 'right', 2],
         [self.uiContent['columnLayout'], 'bottom', 0]))
        cmds.window(self.uiContent['window'], widthHeight=self.uiContent['size'], sizeable=False, minimizeButton=True, maximizeButton=False, resizeToFitChildren=True, edit=True)

    def closeBtnCmd(self, *args):
        """Close window"""
        cmds.deleteUI(self.uiContent['window'], window=True)

    def commonButtons(self):
        """Create common buttons for all option boxes"""
        self.uiContent['commonBtnSize'] = ((self.uiContent['size'][0] - 18) / 3, 26)
        self.uiContent['actionBtn'] = cmds.button(parent=self.uiContent['mainForm'], label='Add', height=self.uiContent['commonBtnSize'][1], command=self.addTypeCmd)
        self.uiContent['applyBtn'] = cmds.button(parent=self.uiContent['mainForm'], label='Remove', height=self.uiContent['commonBtnSize'][1], command=self.removeTypeCmd)
        self.uiContent['closeBtn'] = cmds.button(parent=self.uiContent['mainForm'], label='Close', height=self.uiContent['commonBtnSize'][1], command=self.closeBtnCmd)
        cmds.formLayout(self.uiContent['mainForm'], e=True, attachForm=([self.uiContent['actionBtn'], 'left', 5],
         [self.uiContent['actionBtn'], 'bottom', 5],
         [self.uiContent['applyBtn'], 'bottom', 5],
         [self.uiContent['closeBtn'], 'bottom', 5],
         [self.uiContent['closeBtn'], 'right', 5]), attachPosition=([self.uiContent['actionBtn'],
          'right',
          1,
          33], [self.uiContent['closeBtn'],
          'left',
          0,
          67]), attachControl=([self.uiContent['applyBtn'],
          'left',
          4,
          self.uiContent['actionBtn']], [self.uiContent['applyBtn'],
          'right',
          4,
          self.uiContent['closeBtn']]), attachNone=([self.uiContent['actionBtn'], 'top'], [self.uiContent['applyBtn'], 'top'], [self.uiContent['closeBtn'], 'top']))

    def updateOptionMenuGrpCmd(self):
        cmds.textScrollList(self.parentUiContent['sourceNodeTextScrollList'], edit=True, removeAll=True)
        cmds.textScrollList(self.parentUiContent['targetNodeTextScrollList'], edit=True, removeAll=True)
        for shaderType in self.shaderTypesFile.typeList():
            cmds.textScrollList(self.parentUiContent['sourceNodeTextScrollList'], edit=True, append=shaderType)
            cmds.textScrollList(self.parentUiContent['targetNodeTextScrollList'], edit=True, append=shaderType)

    def addTypeCmd(self, *args):
        sels = cmds.ls(sl=True)
        typeList = self.shaderTypesFile.typeList()
        if sels:
            for addName in sels:
                addType = cmds.objectType(addName)
                if addType not in typeList:
                    self.shaderTypesFile.addType(addType=addType)
                    cmds.textScrollList(self.uiContent['textScrollList'], edit=True, removeAll=True)
                    for shader in self.shaderTypesFile.typeList():
                        cmds.textScrollList(self.uiContent['textScrollList'], edit=True, append=shader)

                    self.updateOptionMenuGrpCmd()
                    om.MGlobal.displayInfo('The "%s" shader type already added to the shader type library!' % addType)
                else:
                    om.MGlobal.displayWarning('The "%s" shader type already in the shader type library!' % addType)

        else:
            om.MGlobal.displayWarning('Please select need append shader type!')

    def removeTypeCmd(self, *args):
        removeTypes = cmds.textScrollList(self.uiContent['textScrollList'], selectItem=True, query=True)
        if removeTypes:
            for removeType in removeTypes:
                self.shaderTypesFile.removeType(removeType=removeType)
                om.MGlobal.displayInfo('The "%s" shader type already removed of the shader type library!' % removeType)

            cmds.textScrollList(self.uiContent['textScrollList'], edit=True, removeAll=True)
            for shader in self.shaderTypesFile.typeList():
                cmds.textScrollList(self.uiContent['textScrollList'], edit=True, append=shader)

            self.updateOptionMenuGrpCmd()
        else:
            om.MGlobal.displayWarning('Please select need remove shader type!')


class win(tp.templateWindow):

    def __init__(self):
        tp.templateWindow.__init__(self)
        self.uiContent['window'] = 'jn_shaderTransferWindow'
        self.uiContent['title'] = u'Transfer'
        self.uiContent['size'] = (700, 600)
        self.configFilePath = cmds.internalVar(userPrefDir=True)
        self.userAppDir = cmds.internalVar(userAppDir=True)
        self.initPresetFilePath()
        self.shaderTypesFile = shaderTypesFile(fileDir=self.userAppDir + '/Presets/jn_shaderTransfer/', fileName='shaderTypes.xml')
        self.shaderTypeList = self.shaderTypesFile.typeList()
        self.iniFile = iniFile(fileDir=self.configFilePath, fileName='jn_shaderTransfer.config')
        self.language = self.iniFile.getValue('language')
        self.presetsDir = self.iniFile.getValue('presets_dir')
        if self.language == '':
            self.iniFile.setValue('language', 'en_US')
            self.language = self.iniFile.getValue('language')
        if self.presetsDir == '' or not os.path.exists(self.presetsDir):
            self.iniFile.setValue('presets_dir', self.initPresetFilePath())
            self.presetsDir = self.iniFile.getValue('presets_dir')
        if not cmds.pluginInfo('animImportExport', query=True, loaded=True):
            cmds.loadPlugin('animImportExport')
        self.shaderTypeDic = {}
        self.shaderTypeDic['mayaArnoldVRayRedshiftShaders'] = ['useBackground',
         'layeredShader',
         'hairTubeShader',
         'shadingMap',
         'anisotropic',
         'blinn',
         'lambert',
         'phong',
         'phongE',
         'rampShader',
         'surfaceShader',
         'aiAmbientOcclusion',
         'aiHair',
         'aiRaySwitch',
         'aiShadowCatcher',
         'aiSkin',
         'aiStandard',
         'aiUtility',
         'aiWireframe',
         'RedshiftArchitectural',
         'RedshiftCarPaint',
         'RedshiftSubSurfaceScatter',
         'RedshiftSprite',
         'RedshiftMatteShadowCatcher',
         'RedshiftMaterialBlender',
         'RedshiftIncandescent',
         'RedshiftHair',
         'VRayBlendMtl',
         'VRayBumpMtl',
         'VRayCarPaintMtl',
         'VRayFastSSS2',
         'VRayFlakesMtl',
         'VRayLightMtl',
         'VRayMeshMaterial',
         'VRayMtl',
         'VRayMtl2Sided',
         'VRayMtlHair2',
         'VRayMtlHair3',
         'VRayMtlWrapper',
         'VRaySimbiont']
        self.shaderTypeDic['mayaShaders'] = ['oceanShader']
        self.shaderTypeDic['mentalRayShaders'] = ['builtin_bsdf_architectural',
         'builtin_bsdf_architectural_comp',
         'builtin_bsdf_ashikhmin',
         'builtin_bsdf_carpaint',
         'builtin_bsdf_lambert',
         'builtin_bsdf_mirror',
         'builtin_bsdf_phong',
         'mi_metallic_paint',
         'mib_illum_ward',
         'mib_glossy_refraction',
         'mib_illum_ward_deriv',
         'misss_skin_specular',
         'misss_fast_shader2',
         'mib_illum_phong',
         'misss_call_shader',
         'mi_car_paint_phen',
         'mib_illum_hair',
         'mib_illum_lambert',
         'path_material',
         'mib_illum_cooktorr',
         'mib_illum_blinn',
         'misss_fast_simple_maya',
         'misss_fast_shader',
         'mib_glossy_reflection',
         'misss_set_normal',
         'misss_mia_skin2_surface_phen']
        self.shaderTypeDic['mentalRayShadersA'] = ['mi_metallic_paint_x_passes',
         'misss_fast_shader2_x',
         'mi_metallic_paint_x',
         'mi_car_paint_phen_x_passes',
         'mi_car_paint_phen_x',
         'misss_fast_shader2_x',
         'misss_fast_shader_x',
         'misss_fast_shader_x_passes',
         'misss_fast_shader_x',
         'misss_fast_shader_x']
        self.shaderTypeDic['mentalRayShadersB'] = ['mia_material1', 'mia_material_x', 'mia_material_x_passes']
        self.shaderTypeDic['mentalRayShadersC'] = ['dgs_material',
         'dielectric_material',
         'misss_physical',
         'transmat']
        self.lightTypes = ['ambientLight',
         'areaLight',
         'directionalLight',
         'pointLight',
         'spotLight',
         'volumeLight',
         'RedshiftDomeLight',
         'RedshiftIESLight',
         'RedshiftPhysicalLight',
         'RedshiftPhysicalSun',
         'RedshiftPortalLight',
         'RedshiftLightGobo',
         'VRayLightDomeShape',
         'VRayLightIESShape',
         'VRayLightRectShape',
         'VRayLightSphereShape',
         'VRaySunShape',
         'aiAreaLight',
         'aiSkyDomeLight',
         'aiPhotometricLight',
         'aiLightDecay',
         'aiLightBlocker',
         'aiGoBo',
         'aiBarndoor']
        self.lightTypeMap = {'areaLight': 0,
         'pointLight': 1,
         'spotLight': 2,
         'directionalLight': 3}

    def displayOptions(self, *args):
        global mainUiContent
        self.uiContent['mainColumnLayout'] = cmds.columnLayout(adj=True)
        self.uiContent['mainPaneLayout'] = cmds.paneLayout(configuration='vertical2', staticWidthPane=2)
        self.uiContent['leftColumnLayout'] = cmds.columnLayout(parent=self.uiContent['mainPaneLayout'], adj=True)
        cmds.text(parent=self.uiContent['leftColumnLayout'], label='Transfer', font='plainLabelFont')
        self.uiContent['leftPaneLayout'] = cmds.paneLayout(configuration='vertical2')
        self.uiContent['oldColumnLayout'] = cmds.columnLayout(parent=self.uiContent['leftPaneLayout'], adjustableColumn=True, columnAttach=('both', 2), columnAlign='center', rowSpacing=2)
        cmds.separator(parent=self.uiContent['oldColumnLayout'], style='none', h=5)
        self.uiContent['oldRefreshButton'] = cmds.button(parent=self.uiContent['oldColumnLayout'], label=u'Current Shader -->>', height=30)
        self.uiContent['oldMiddleKeyPopupMenu'] = cmds.popupMenu(parent=self.uiContent['oldRefreshButton'], button=2, markingMenu=True)
        self.uiContent['oldTextScrollList'] = cmds.textScrollList(parent=self.uiContent['oldColumnLayout'], numberOfRows=20, width=80, height=510, allowMultiSelection=True, showIndexedItem=4)
        self.uiContent['oldTextScrollListPopupMenu'] = cmds.popupMenu(parent=self.uiContent['oldTextScrollList'], markingMenu=True)
        cmds.menuItem(parent=self.uiContent['oldTextScrollListPopupMenu'], label='Select All', radialPosition='E', command=partial(self.buttonMiddleKeyPopupMenuCmd, self.uiContent['oldTextScrollList']))
        cmds.menuItem(parent=self.uiContent['oldTextScrollListPopupMenu'], label='Delete', radialPosition='SE', command=partial(self.textScrollListPopupMenuCmd, self.uiContent['oldTextScrollList']))
        cmds.textScrollList(self.uiContent['oldTextScrollList'], doubleClickCommand=partial(self.textScrollLayoutClickCmd, self.uiContent['oldTextScrollList']), selectCommand=partial(self.textScrollLayoutClickCmd, self.uiContent['oldTextScrollList']), edit=True)
        self.uiContent['newColumnLayout'] = cmds.columnLayout(parent=self.uiContent['leftPaneLayout'], adjustableColumn=True, columnAttach=('both', 2), columnAlign='center', rowSpacing=2)
        cmds.separator(parent=self.uiContent['newColumnLayout'], style='none', h=5)
        self.uiContent['newRefreshButton'] = cmds.button(parent=self.uiContent['newColumnLayout'], label=u'<<-- Future Shader', height=30)
        self.uiContent['newMiddleKeyPopupMenu'] = cmds.popupMenu(parent=self.uiContent['newRefreshButton'], button=2, markingMenu=True)
        self.uiContent['newTextScrollList'] = cmds.textScrollList(parent=self.uiContent['newColumnLayout'], numberOfRows=20, width=80, height=510, allowMultiSelection=True, showIndexedItem=4)
        self.uiContent['newTextScrollListPopupMenu'] = cmds.popupMenu(parent=self.uiContent['newTextScrollList'], markingMenu=True)
        cmds.menuItem(parent=self.uiContent['newTextScrollListPopupMenu'], label='Select All', radialPosition='E', command=partial(self.buttonMiddleKeyPopupMenuCmd, self.uiContent['newTextScrollList']))
        cmds.menuItem(parent=self.uiContent['newTextScrollListPopupMenu'], label='Delete', radialPosition='SE', command=partial(self.textScrollListPopupMenuCmd, self.uiContent['newTextScrollList']))
        cmds.textScrollList(self.uiContent['newTextScrollList'], doubleClickCommand=partial(self.textScrollLayoutClickCmd, self.uiContent['newTextScrollList']), selectCommand=partial(self.textScrollLayoutClickCmd, self.uiContent['newTextScrollList']), edit=True)
        self.uiContent['presetsUpColumnLayout'] = cmds.columnLayout(parent=self.uiContent['mainPaneLayout'], adjustableColumn=True, columnAttach=('both', 2), columnAlign='center', rowSpacing=2)
        cmds.text(parent=self.uiContent['presetsUpColumnLayout'], label='Attribute Prests', font='plainLabelFont')
        cmds.separator(parent=self.uiContent['presetsUpColumnLayout'], style='none', h=5)
        self.uiContent['presetsFrameLayout'] = cmds.frameLayout(parent=self.uiContent['presetsUpColumnLayout'], lv=False, borderStyle='etchedIn', height=540)
        self.uiContent['presetsUpColumnLayout'] = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 2), columnAlign='center', rowSpacing=2)
        self.uiContent['shaderPresetsPathTFBG'] = cmds.textFieldButtonGrp(parent=self.uiContent['presetsUpColumnLayout'], label='Path: ', buttonLabel='...', editable=False, cw3=[40, 320, 20], text=self.presetsDir + '/', buttonCommand=self.presetFilePathBrowseButtonCmd)
        presetFiles = cmds.getFileList(folder=self.presetsDir + '/', filespec='*.xml')
        self.uiContent['presetFilesFrameLayout'] = cmds.frameLayout(parent=self.uiContent['presetsUpColumnLayout'], label='Preset Library', borderStyle='etchedIn', collapse=False, collapsable=False, height=396)
        fileBtnPM = cmds.popupMenu(parent=self.uiContent['presetFilesFrameLayout'], button=3)
        cmds.menuItem(parent=fileBtnPM, label='Delete', command=self.deletePresetFileCmd)
        self.uiContent['presetsScrollLayout'] = cmds.scrollLayout(parent=self.uiContent['presetFilesFrameLayout'], childResizable=True)
        self.uiContent['presetFilesTabLayout'] = cmds.tabLayout(parent=self.uiContent['presetsScrollLayout'], innerMarginWidth=5, innerMarginHeight=5, tabsVisible=0, childResizable=1)
        self.uiContent['presetFilesColumnLayout'] = cmds.columnLayout(parent=self.uiContent['presetFilesTabLayout'], adj=True)
        self.uiContent['presetDownColumnLayout'] = cmds.columnLayout(parent=self.uiContent['presetsFrameLayout'], adj=True)
        self.uiContent['presetNewFileTabLayout'] = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, tabsVisible=0, childResizable=1)
        self.uiContent['presetNewFileRowLayout'] = cmds.rowLayout(nc=4, columnWidth4=(150, 150, 5, 80))
        cmds.columnLayout(adj=True, parent=self.uiContent['presetNewFileRowLayout'])
        cmds.text(label='Source')
        self.uiContent['sourceNodeTextScrollList'] = cmds.textScrollList(allowMultiSelection=False, append=self.shaderTypeList, height=80)
        cmds.columnLayout(adj=True, parent=self.uiContent['presetNewFileRowLayout'])
        cmds.text(label='Target')
        self.uiContent['targetNodeTextScrollList'] = cmds.textScrollList(allowMultiSelection=False, append=self.shaderTypeList, height=80)
        cmds.text(label='  ', parent=self.uiContent['presetNewFileRowLayout'])
        cmds.columnLayout(adj=True, parent=self.uiContent['presetNewFileRowLayout'])
        cmds.text(label='')
        self.uiContent['presetNewButton'] = cmds.button(label='New', command=self.presetFileBtnCmd, height=80, width=80)
        cmds.formLayout(self.uiContent['optionsForm'], e=True, attachForm=([self.uiContent['mainColumnLayout'], 'top', 0],
         [self.uiContent['mainColumnLayout'], 'left', 2],
         [self.uiContent['mainColumnLayout'], 'right', 2],
         [self.uiContent['mainColumnLayout'], 'bottom', 0]))
        self.presetFilesBtnList = []
        self.updatePresetLibrary()
        cmds.button(self.uiContent['presetNewButton'], command=self.presetFileBtnCmd, edit=True)
        cmds.window(self.uiContent['window'], widthHeight=self.uiContent['size'], sizeable=False, minimizeButton=True, maximizeButton=True, edit=True)
        self.autoRefreshJobCmd()
        mainUiContent = self.uiContent

    def commonMenu(self):
        """Create common menu items for all option boxes"""
        self.uiContent['editMenu'] = cmds.menu(label='Edit')
        self.uiContent['editMenuSave'] = cmds.menuItem(label='Save Settings', command=self.editMenuSaveCmd)
        self.uiContent['editMenuReset'] = cmds.menuItem(label='Reset Settings', command=self.editMenuResetCmd)
        self.uiContent['editMenuDiv'] = cmds.menuItem(d=True)
        self.uiContent['editMenuRadio'] = cmds.radioMenuItemCollection()
        self.uiContent['editMenuTool'] = cmds.menuItem(label='As Tool', radioButton=True, enable=self.uiContent['supportsToolAction'], command=self.editMenuToolCmd)
        self.uiContent['editMenuAction'] = cmds.menuItem(label='As Action', radioButton=True, enable=self.uiContent['supportsToolAction'], command=self.editMenuActionCmd)
        self.uiContent['toolMenu'] = cmds.menu(label='Tool')
        self.uiContent['removeShaderType'] = cmds.menuItem(label='Add/Remove Shader Type', command=self.addAndRemoveShaderTypeCmd)
        self.uiContent['helpMenu'] = cmds.menu(label='Help')
        self.uiContent['helpMenuItem'] = cmds.menuItem(label='Help on %s' % self.uiContent['title'], command=self.helpMenuCmd)
        self.uiContent['updatePresetItem'] = cmds.menuItem(label='Fix Preset Files', command=self.updateFix)

    def helpMenuCmd(self, *args):
        """Override this method to display custom help"""
        print os.path.dirname(os.path.abspath(__file__)) + '/shaderTransfer_Help.mht'
        webbrowser.open(os.path.dirname(os.path.abspath(__file__)) + '/shaderTransfer_Help.mht')

    def addAndRemoveShaderTypeCmd(self, *args):
        win = removeShaderTypeWin(shaderTypesFile=self.shaderTypesFile, uiContent=self.uiContent)
        win.create()

    def addNewItemButtonCommand(self, layout, mode, *args):
        source = cmds.textScrollList(self.uiContent['sourceNodeTextScrollList'], selectItem=True, query=True)[0]
        target = cmds.textScrollList(self.uiContent['targetNodeTextScrollList'], selectItem=True, query=True)[0]
        if source == target:
            om.MGlobal.displayWarning('Please settting different source and target type!')
        elif cmds.button(self.uiContent['presetNewButton'], label=1, q=1) == 'Add':
            attr1 = cmds.listAttr(self.stempNode, settable=1, multi=1)
            attr2 = cmds.listAttr(self.ttempNode, settable=1, multi=1)
            attr1.sort()
            attr2.sort()
            if mode == 'direct':
                fl1 = cmds.frameLayout(lv=0, parent=layout, bs='in')
                cmds.rowLayout(parent=fl1, nc=6, columnAttach6=['both',
                 'both',
                 'both',
                 'both',
                 'both',
                 'both'])
                cmds.separator(width=2, style='none')
                cmds.text(label='', width=10, backgroundColor=(24 / 255.0, 201 / 255.0, 170 / 255.0))
                cmds.columnLayout(adj=True)
                om1 = cmds.optionMenuGrp(label=source + ' ')
                for attr in attr1:
                    cmds.menuItem(l=attr)

                om2 = cmds.optionMenuGrp(label=target + ' ')
                for attr in attr2:
                    cmds.menuItem(l=attr)

                cmds.setParent('..')
                cmds.columnLayout(adj=True)
                tfg1 = cmds.textFieldGrp(label='->', columnWidth2=[20, 100])
                tfg2 = cmds.textFieldGrp(label='->', columnWidth2=[20, 100])
                cmds.setParent('..')
                cmds.separator(width=85, style='none')
                itb1 = cmds.iconTextButton(style='iconOnly', image1='SP_TrashIcon.png', label='spotlight')
                cmds.iconTextButton(itb1, command=partial(self.iconTextButtonDirectCmd, fl1, om1, om2, tfg1, tfg2), e=1)
                cmds.setParent('..')
                self.uiContent['editorFrames'].append(fl1)
                self.uiContent['editorSourceOptionMenuGrp'].append(om1)
                self.uiContent['editorTargetOptionMenuGrp'].append(om2)
                self.uiContent['editorSourceTextFieldGrp'].append(tfg1)
                self.uiContent['editorTargetTextFieldGrp'].append(tfg2)
                return (om1,
                 tfg1,
                 om2,
                 tfg2)
            if mode == 'drivenKey':
                fl1 = cmds.frameLayout(lv=0, parent=layout, bs='in')
                cmds.rowLayout(parent=fl1, nc=6, columnAttach6=['both',
                 'both',
                 'both',
                 'both',
                 'both',
                 'both'])
                cmds.separator(width=2, style='none')
                cmds.text(label='', width=10, backgroundColor=(222 / 255.0, 114 / 255.0, 122 / 255.0))
                cmds.columnLayout(adj=True)
                om1 = cmds.optionMenuGrp(label=source + ' ')
                for attr in attr1:
                    cmds.menuItem(l=attr)

                om2 = cmds.optionMenuGrp(label=target + ' ')
                for attr in attr2:
                    cmds.menuItem(l=attr)

                cmds.setParent('..')
                cml0 = cmds.columnLayout(adj=True, columnOffset=['left', -140])
                cmds.optionMenuGrp(om1, changeCommand=partial(self.optionMenuGrpChangeCmd, om1, om2, cml0), edit=True)
                cmds.optionMenuGrp(om2, changeCommand=partial(self.optionMenuGrpChangeCmd, om1, om2, cml0), edit=True)
                cmds.setParent('..')
                cmds.columnLayout(adj=True)
                cmds.button(label='Key', command=partial(self.keyBtnCmd, om1, om2))
                cmds.button(label='Editor', command=self.graphEditorBtnCmd)
                cmds.setParent('..')
                itb1 = cmds.iconTextButton(style='iconOnly', image1='SP_TrashIcon.png', label='spotlight')
                cmds.iconTextButton(itb1, command=partial(self.iconTextButtonDrivenKeyCmd, fl1, om1, om2, cml0), e=1)
                cmds.setParent('..')
                self.uiContent['editorDrivenKeyFrames'].append(fl1)
                self.uiContent['editorSourceDrivenKeyOptionMenuGrp'].append(om1)
                self.uiContent['editorTargetDrivenKeyOptionMenuGrp'].append(om2)
                return (om1, om2, cml0)
            if mode == 'expr':
                fl1 = cmds.frameLayout(lv=0, parent=layout, bs='in')
                cmds.rowLayout(parent=fl1, nc=6, columnAttach6=['both',
                 'both',
                 'both',
                 'both',
                 'both',
                 'both'])
                cmds.separator(width=2, style='none')
                cmds.text(label='', width=10, backgroundColor=(203 / 255.0, 165 / 255.0, 241 / 255.0))
                cmds.columnLayout(adj=True)
                om1 = cmds.optionMenuGrp(label=source + ' ')
                for attr in attr1:
                    cmds.menuItem(l=attr)

                om2 = cmds.optionMenuGrp(label=target + ' ')
                for attr in attr2:
                    cmds.menuItem(l=attr)

                cmds.setParent('..')
                cl1 = cmds.columnLayout(adj=True)
                tfg1 = cmds.textFieldGrp(label='->', columnWidth2=[20, 200])
                self.createInsertKeywordMenu(tfg1)
                cmds.setParent(cl1)
                tfg2 = cmds.textFieldGrp(label='->', columnWidth2=[20, 200])
                self.createInsertKeywordMenu(tfg2)
                cmds.setParent('..')
                cmds.separator(width=5, style='none')
                itb1 = cmds.iconTextButton(style='iconOnly', image1='SP_TrashIcon.png', label='spotlight')
                cmds.iconTextButton(itb1, command=partial(self.iconTextButtonExpressionCmd, fl1, om1, om2, tfg1, tfg2), e=1)
                cmds.setParent('..')
                self.uiContent['editorExprFrames'].append(fl1)
                self.uiContent['editorSourceExprOptionMenuGrp'].append(om1)
                self.uiContent['editorTargetExprOptionMenuGrp'].append(om2)
                self.uiContent['editorSourceExprTextFieldGrp'].append(tfg1)
                self.uiContent['editorTargetExprTextFieldGrp'].append(tfg2)
                return (om1,
                 tfg1,
                 om2,
                 tfg2)
        else:
            om.MGlobal.displayWarning('Please Press The New Button!')

    def addPresetToXMLFile(self, *args):
        sourceAttribute = []
        targetAttribute = []
        sourceObject = []
        targetObject = []
        sourceDrivenKeyAttribute = []
        targetDrivenKeyAttribute = []
        sourceDrivenKeyInfo = []
        targetDrivenKeyInfo = []
        sourceExpressionAttribute = []
        targetExpressionAttribute = []
        sourceExpressionInfo = []
        targetExpressionInfo = []
        if self.uiContent['editorSourceOptionMenuGrp'] and self.uiContent['editorTargetOptionMenuGrp'] and self.uiContent['editorSourceTextFieldGrp'] and self.uiContent['editorTargetTextFieldGrp']:
            for index in range(0, len(self.uiContent['editorSourceOptionMenuGrp'])):
                sourceAttribute.append(cmds.optionMenuGrp(self.uiContent['editorSourceOptionMenuGrp'][index], v=1, q=1))
                sourceObject.append(cmds.textFieldGrp(self.uiContent['editorSourceTextFieldGrp'][index], text=1, q=1))
                targetAttribute.append(cmds.optionMenuGrp(self.uiContent['editorTargetOptionMenuGrp'][index], v=1, q=1))
                targetObject.append(cmds.textFieldGrp(self.uiContent['editorTargetTextFieldGrp'][index], text=1, q=1))

        if self.uiContent['editorSourceDrivenKeyOptionMenuGrp'] and self.uiContent['editorTargetDrivenKeyOptionMenuGrp']:
            for index in range(0, len(self.uiContent['editorSourceDrivenKeyOptionMenuGrp'])):
                sourceAttr = cmds.optionMenuGrp(self.uiContent['editorSourceDrivenKeyOptionMenuGrp'][index], v=1, q=1)
                targetAttr = cmds.optionMenuGrp(self.uiContent['editorTargetDrivenKeyOptionMenuGrp'][index], v=1, q=1)
                drivenChannel = self.ttempNode + '.' + targetAttr
                try:
                    animCurve = cmds.keyframe(drivenChannel, name=True, query=True)[0]
                    keyframeCount = cmds.keyframe(animCurve, keyframeCount=True, query=True)
                    driverVal = cmds.keyframe(drivenChannel, fc=True, query=True)
                    drivenVal = cmds.keyframe(drivenChannel, vc=True, query=True)
                    inTangentType = cmds.keyTangent(animCurve, inTangentType=True, query=True)
                    outTangentType = cmds.keyTangent(animCurve, outTangentType=True, query=True)
                    inAngle = cmds.keyTangent(animCurve, inAngle=True, query=True)
                    outAngle = cmds.keyTangent(animCurve, outAngle=True, query=True)
                    inWeight = cmds.keyTangent(animCurve, inWeight=True, query=True)
                    outWeight = cmds.keyTangent(animCurve, outWeight=True, query=True)
                    lock = cmds.keyTangent(animCurve, lock=True, query=True)
                    weightLock = cmds.keyTangent(animCurve, weightLock=True, query=True)
                    weightedTangents = cmds.keyTangent(animCurve, weightedTangents=True, query=True)
                    preInfinite = cmds.setInfinity(preInfinite=True, query=True)
                    if not preInfinite:
                        preInfinite = ['cycleRelative']
                    postInfinite = cmds.setInfinity(postInfinite=True, query=True)
                    if not postInfinite:
                        postInfinite = ['cycleRelative']
                    sourceKeyframeList = []
                    for index in range(0, keyframeCount):
                        sourceKeyframeDict = {}
                        sourceKeyframeDict['driverVal'] = driverVal[index]
                        sourceKeyframeDict['drivenVal'] = drivenVal[index]
                        sourceKeyframeDict['inTangentType'] = inTangentType[index]
                        sourceKeyframeDict['outTangentType'] = outTangentType[index]
                        sourceKeyframeDict['inAngle'] = inAngle[index]
                        sourceKeyframeDict['outAngle'] = outAngle[index]
                        sourceKeyframeDict['inWeight'] = inWeight[index]
                        sourceKeyframeDict['outWeight'] = outWeight[index]
                        sourceKeyframeDict['lock'] = int(lock[index])
                        sourceKeyframeDict['weightLock'] = int(weightLock[index])
                        sourceKeyframeDict['preInfinite'] = preInfinite[0]
                        sourceKeyframeDict['postInfinite'] = postInfinite[0]
                        sourceKeyframeDict['weightedTangents'] = int(weightedTangents[0])
                        sourceKeyframeList.append(sourceKeyframeDict)

                    targetKeyframeList = []
                    minDriverVal = 0
                    maxDriverVal = 0
                    for index in range(0, keyframeCount):
                        if index == 0:
                            minDriverVal = driverVal[index]
                        if index == keyframeCount - 1:
                            maxDriverVal = driverVal[index]

                    if maxDriverVal != minDriverVal:
                        if cmds.attributeQuery(targetAttr, node=self.ttempNode, attributeType=True) == 'bool':
                            stepNum = 1
                        else:
                            stepNum = 100
                        driverValStepVale = (maxDriverVal - minDriverVal) / float(stepNum)
                        for index in xrange(stepNum + 1):
                            keyFrameDriverVal = minDriverVal + driverValStepVale * index
                            cmds.setAttr(self.stempNode + '.' + sourceAttr, keyFrameDriverVal)
                            keyFrameDrivenVal = cmds.getAttr(self.ttempNode + '.' + targetAttr)
                            targetKeyframeDict = {}
                            targetKeyframeDict['driverVal'] = float(keyFrameDrivenVal)
                            targetKeyframeDict['drivenVal'] = float(keyFrameDriverVal)
                            targetKeyframeDict['inTangentType'] = 'linear'
                            targetKeyframeDict['outTangentType'] = 'linear'
                            targetKeyframeDict['inAngle'] = 0
                            targetKeyframeDict['outAngle'] = 0
                            targetKeyframeDict['inWeight'] = 0
                            targetKeyframeDict['outWeight'] = 0
                            targetKeyframeDict['lock'] = int(lock[0])
                            targetKeyframeDict['weightLock'] = int(weightLock[0])
                            targetKeyframeDict['preInfinite'] = preInfinite[0]
                            targetKeyframeDict['postInfinite'] = postInfinite[0]
                            targetKeyframeDict['weightedTangents'] = int(weightedTangents[0])
                            targetKeyframeList.append(targetKeyframeDict)

                    sourceDrivenKeyAttribute.append(sourceAttr)
                    targetDrivenKeyAttribute.append(targetAttr)
                    sourceDrivenKeyInfo.append(sourceKeyframeList)
                    targetDrivenKeyInfo.append(targetKeyframeList)
                except:
                    pass

        if self.uiContent['editorSourceExprOptionMenuGrp'] and self.uiContent['editorTargetExprOptionMenuGrp'] and self.uiContent['editorSourceExprTextFieldGrp'] and self.uiContent['editorTargetExprTextFieldGrp']:
            for index in range(0, len(self.uiContent['editorSourceExprOptionMenuGrp'])):
                sourceExpressionAttribute.append(cmds.optionMenuGrp(self.uiContent['editorSourceExprOptionMenuGrp'][index], v=1, q=1))
                sourceExpressionInfo.append(cmds.textFieldGrp(self.uiContent['editorSourceExprTextFieldGrp'][index], text=1, q=1))
                targetExpressionAttribute.append(cmds.optionMenuGrp(self.uiContent['editorTargetExprOptionMenuGrp'][index], v=1, q=1))
                targetExpressionInfo.append(cmds.textFieldGrp(self.uiContent['editorTargetExprTextFieldGrp'][index], text=1, q=1))

        tempAttrs = cmds.listConnections(self.stempNode, c=1, p=1)
        allAttrs = []
        if tempAttrs:
            for index in range(0, len(tempAttrs)):
                if index % 2:
                    if tempAttrs[index].split('.')[0] == self.ttempNode:
                        allAttrs.append(tempAttrs[index - 1])
                        allAttrs.append(tempAttrs[index])

        connectionProps = []
        changeProps = []
        drivenKeyProps = []
        expressionProps = []
        if allAttrs:
            for index in range(0, len(allAttrs)):
                if index % 2:
                    frontwardDic = {}
                    frontwardDic['source'] = allAttrs[index - 1].split('.')[1]
                    frontwardDic['target'] = allAttrs[index].split('.')[1]
                    frontwardDic['mode'] = 'frontward'
                    backwardDic = {}
                    backwardDic['source'] = allAttrs[index].split('.')[1]
                    backwardDic['target'] = allAttrs[index - 1].split('.')[1]
                    backwardDic['mode'] = 'backward'
                    connectionProps.append(frontwardDic)
                    connectionProps.append(backwardDic)

        if sourceAttribute and targetAttribute and sourceObject and targetObject:
            for index in range(0, len(sourceAttribute)):
                frontwardDic = {}
                frontwardDic['source'] = sourceAttribute[index]
                frontwardDic['target'] = targetAttribute[index]
                frontwardDic['sourceChangeInfo'] = sourceObject[index]
                frontwardDic['targetChangeInfo'] = targetObject[index]
                frontwardDic['mode'] = 'frontward'
                changeProps.append(frontwardDic)
                backwardDic = {}
                backwardDic['source'] = targetAttribute[index]
                backwardDic['target'] = sourceAttribute[index]
                backwardDic['sourceChangeInfo'] = targetObject[index]
                backwardDic['targetChangeInfo'] = sourceObject[index]
                backwardDic['mode'] = 'backward'
                changeProps.append(backwardDic)

        if sourceDrivenKeyAttribute and targetDrivenKeyAttribute and sourceDrivenKeyInfo and targetDrivenKeyInfo:
            for index in range(0, len(sourceDrivenKeyAttribute)):
                sourceDrivenKeyInfoDict = {}
                sourceDrivenKeyInfoDict['source'] = sourceDrivenKeyAttribute[index]
                sourceDrivenKeyInfoDict['target'] = targetDrivenKeyAttribute[index]
                sourceDrivenKeyInfoDict['preInfinite'] = sourceDrivenKeyInfo[index][0]['preInfinite']
                sourceDrivenKeyInfoDict['postInfinite'] = sourceDrivenKeyInfo[index][0]['postInfinite']
                sourceDrivenKeyInfoDict['weightedTangents'] = sourceDrivenKeyInfo[index][0]['weightedTangents']
                sourceDrivenKeyInfoDict['mode'] = 'frontward'
                sourceDrivenKeyInfoDict['drivenKeyInfo'] = sourceDrivenKeyInfo[index]
                drivenKeyProps.append(sourceDrivenKeyInfoDict)
                targetDrivenKeyInfoDict = {}
                targetDrivenKeyInfoDict['source'] = targetDrivenKeyAttribute[index]
                targetDrivenKeyInfoDict['target'] = sourceDrivenKeyAttribute[index]
                targetDrivenKeyInfoDict['preInfinite'] = targetDrivenKeyInfo[index][0]['preInfinite']
                targetDrivenKeyInfoDict['postInfinite'] = targetDrivenKeyInfo[index][0]['postInfinite']
                targetDrivenKeyInfoDict['weightedTangents'] = targetDrivenKeyInfo[index][0]['weightedTangents']
                targetDrivenKeyInfoDict['mode'] = 'backward'
                targetDrivenKeyInfoDict['drivenKeyInfo'] = targetDrivenKeyInfo[index]
                drivenKeyProps.append(targetDrivenKeyInfoDict)

        if sourceExpressionAttribute and targetExpressionAttribute and sourceExpressionInfo and targetExpressionInfo:
            for index in range(0, len(sourceExpressionAttribute)):
                frontwardExpressionDic = {}
                frontwardExpressionDic['source'] = sourceExpressionAttribute[index]
                frontwardExpressionDic['target'] = targetExpressionAttribute[index]
                frontwardExpressionDic['sourceExpressionInfo'] = sourceExpressionInfo[index]
                frontwardExpressionDic['targetExpressionInfo'] = targetExpressionInfo[index]
                frontwardExpressionDic['mode'] = 'frontward'
                expressionProps.append(frontwardExpressionDic)
                backwardExpressionDic = {}
                backwardExpressionDic['source'] = targetExpressionAttribute[index]
                backwardExpressionDic['target'] = sourceExpressionAttribute[index]
                backwardExpressionDic['sourceExpressionInfo'] = targetExpressionInfo[index]
                backwardExpressionDic['targetExpressionInfo'] = sourceExpressionInfo[index]
                backwardExpressionDic['mode'] = 'backward'
                expressionProps.append(backwardExpressionDic)

        presetSaveState = self.writeXMLFile(connectionProps=connectionProps, changeProps=changeProps, drivenKeyProps=drivenKeyProps, expressionProps=expressionProps)
        return presetSaveState

    def autoRefreshJobCmd(self, *args):
        try:
            cmds.scriptJob(kill=self.autoRefreshJob, force=True)
        except:
            pass

        cmds.setToolTo('selectSuperContext')
        self.autoRefreshJob = cmds.scriptJob(p=self.uiContent['window'], e=['SelectionChanged', self.autoUpdateNodeToTSLCmd])
        self.autoUpdateNodeToTSLCmd()

    def autoUpdateNodeToTSLCmd(self, *args):
        sels = cmds.ls(sl=True)
        allOldItems = cmds.textScrollList(self.uiContent['oldTextScrollList'], allItems=True, query=True)
        allNewItems = cmds.textScrollList(self.uiContent['newTextScrollList'], allItems=True, query=True)
        if not allOldItems:
            allOldItems = []
        if not allNewItems:
            allNewItems = []
        cmds.textScrollList(self.uiContent['oldTextScrollList'], deselectAll=True, edit=True)
        cmds.textScrollList(self.uiContent['newTextScrollList'], deselectAll=True, edit=True)
        for sel in sels:
            selNodeType = cmds.nodeType(sel)
            oldShaderType = cmds.button(self.uiContent['oldRefreshButton'], annotation=True, query=True)
            newShaderType = cmds.button(self.uiContent['newRefreshButton'], annotation=True, query=True)
            if selNodeType == oldShaderType:
                oldSelectItems = []
                if sel not in allOldItems:
                    cmds.textScrollList(self.uiContent['oldTextScrollList'], append=sel, edit=True)
                oldSelectItems.append(sel)
                cmds.textScrollList(self.uiContent['oldTextScrollList'], selectItem=oldSelectItems, edit=True)
            if selNodeType == newShaderType:
                newSelectItems = []
                if sel not in allNewItems:
                    cmds.textScrollList(self.uiContent['newTextScrollList'], append=sel, edit=True)
                newSelectItems.append(sel)
                cmds.textScrollList(self.uiContent['newTextScrollList'], selectItem=newSelectItems, edit=True)

    def bumpTransfer(self, oldShader, newShader, newSGNode, *args):
        if cmds.nodeType(oldShader) == 'aiStandard' and cmds.nodeType(newShader) == 'RedshiftArchitectural':
            try:
                tempNodeNormalCamera = cmds.connectionInfo(oldShader + '.normalCamera', sourceFromDestination=True).split('.')[0]
                tempNode = cmds.listConnections(tempNodeNormalCamera, s=1, d=0, p=1)[0].split('.')[0]
                redShiftBumpMapNode = cmds.createNode('RedshiftBumpMap', name=tempNode + 'RedShiftBumpMapNode')
                cmds.connectAttr(tempNode + '.outColor', redShiftBumpMapNode + '.input', f=1)
                cmds.connectAttr(redShiftBumpMapNode + '.outDisplacementVector', newSGNode + '.rsBumpmapShader')
                cmds.delete(tempNodeNormalCamera)
            except:
                pass

        elif cmds.nodeType(oldShader) == 'VRayMtl' and cmds.nodeType(newShader) == 'RedshiftArchitectural':
            try:
                bumpMultValue = cmds.getAttr(oldShader + '.bumpMult')
                fileNode = cmds.connectionInfo(oldShader + '.bumpMap', sourceFromDestination=True).split('.')[0]
                if fileNode:
                    bump2dNode = cmds.createNode('bump2d')
                    cmds.setAttr(bump2dNode + '.bumpDepth', bumpMultValue)
                    cmds.connectAttr(fileNode + '.outAlpha', bump2dNode + '.bumpValue', f=1)
                    cmds.connectAttr(bump2dNode + '.outNormal', newShader + '.bump_input', f=1)
            except:
                pass

        elif cmds.nodeType(oldShader) == 'RedshiftArchitectural' and cmds.nodeType(newShader) == 'VRayMtl':
            try:
                bump2dNode = cmds.connectionInfo(oldShader + '.bump_input', sourceFromDestination=True).split('.')[0]
                bumpDepthValue = cmds.getAttr(bump2dNode + '.bumpDepth')
                if bump2dNode:
                    fileNode = cmds.connectionInfo(bump2dNode + '.bumpValue', sourceFromDestination=True).split('.')[0]
                    cmds.delete(bump2dNode)
                    cmds.setAttr(newShader + '.bumpMult', bumpDepthValue)
                    cmds.connectAttr(fileNode + '.outColor', newShader + '.bumpMap', f=1)
            except:
                pass

    def buttonMiddleKeyPopupMenuCmd(self, tsl, *args):
        items = cmds.textScrollList(tsl, allItems=True, query=True)
        if items:
            for item in items:
                cmds.textScrollList(tsl, selectItem=item, edit=True)

        self.textScrollLayoutClickCmd(tsl=tsl)

    def called(self, p_call):
        uiContent = p_call(self.uiContent)
        return uiContent

    def conservList2String(self, asStringList, *args):
        asString = ''
        for string in asStringList:
            for elment in string:
                asString += str(elment) + ','

        return asString[:-1]

    def createInsertKeywordMenu(self, tfg, *args):
        popup = cmds.popupMenu(parent=tfg, button=3)
        cmds.menuItem(parent=popup, label='Insert node name <Node>', command=partial(self.insertKeywordMenuCallback, tfg, '<Node>'))
        cmds.menuItem(parent=popup, label='Insert node attribute .<Attr>', command=partial(self.insertKeywordMenuCallback, tfg, '.<Attr>'))
        cmds.menuItem(parent=popup, label='Insert dictionary  keyword <Dict>:', command=partial(self.insertKeywordMenuCallback, tfg, '<Dict>:'))

    def currentKeyChangedCmd(self, gc, ffg1, ffg2, *args):
        currentKey = cmds.gradientControlNoAttr(gc, currentKey=True, query=True)
        asString = cmds.gradientControlNoAttr(gc, asString=True, query=True)
        asStringList = self.resultAsStringList(asString=asString)
        cmds.floatFieldGrp(ffg1, value1=asStringList[currentKey][1], edit=True)
        cmds.floatFieldGrp(ffg2, value1=asStringList[currentKey][0], edit=True)

    def deletePresetFileCmd(self, *args):
        dirPath = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=True, query=True)
        libraryItems = cmds.columnLayout(self.uiContent['presetFilesColumnLayout'], ca=1, q=1)
        if libraryItems:
            for i in libraryItems:
                buttons = cmds.rowLayout(i, childArray=1, q=1)
                button = buttons[0]
                selectButton = buttons[1]
                buttonLabel = cmds.button(button, label=True, q=1)
                buttonAnnotation = cmds.button(button, annotation=True, q=1)
                selectState = cmds.iconTextCheckBox(selectButton, value=1, q=1)
                if selectState:
                    ppath = dirPath + buttonLabel
                    if os.path.exists(ppath):
                        tree = ElementTree.parse(ppath)
                        root = tree.getroot()
                        presetName = root.get('frontward')
                        if presetName == buttonAnnotation:
                            os.remove(ppath)

            self.updatePresetLibrary()

    def editorCmd(self, *args):
        cmds.setParent(self.uiContent['mainPaneLayout'])
        cmds.window(self.uiContent['window'], sizeable=True, minimizeButton=True, maximizeButton=True, edit=True)
        cmds.paneLayout(self.uiContent['mainPaneLayout'], configuration='vertical3', staticWidthPane=2, edit=True)
        self.uiContent['presetsDwFormLayout'] = cmds.formLayout(height=200)
        sl1 = cmds.scrollLayout(childResizable=True, width=750)
        cl1 = cmds.columnLayout(parent=sl1, adj=1, columnAttach=('both', 2), columnAlign='center', rowSpacing=2)
        self.uiContent['editorFrameLayout'] = cmds.frameLayout(parent=cl1, l='Editor', bs='in')
        cmds.rowLayout(nc=4, columnAttach4=['both',
         'both',
         'both',
         'both'])
        cmds.text(l='Add New Item ', align='right', width=142)
        self.uiContent['editorFrames'] = []
        self.uiContent['editorSourceOptionMenuGrp'] = []
        self.uiContent['editorTargetOptionMenuGrp'] = []
        self.uiContent['editorSourceTextFieldGrp'] = []
        self.uiContent['editorTargetTextFieldGrp'] = []
        self.uiContent['editorDrivenKeyFrames'] = []
        self.uiContent['editorSourceDrivenKeyOptionMenuGrp'] = []
        self.uiContent['editorTargetDrivenKeyOptionMenuGrp'] = []
        self.uiContent['editorSourceDrivenKeyAttrFieldSliderGrp'] = []
        self.uiContent['editorTargetDrivenKeyAttrFieldSliderGrp'] = []
        self.uiContent['editorExprFrames'] = []
        self.uiContent['editorSourceExprOptionMenuGrp'] = []
        self.uiContent['editorTargetExprOptionMenuGrp'] = []
        self.uiContent['editorSourceExprTextFieldGrp'] = []
        self.uiContent['editorTargetExprTextFieldGrp'] = []
        self.uiContent['directBtn'] = cmds.button(l='Attribute', w=150, command=partial(self.addNewItemButtonCommand, self.uiContent['editorFrameLayout'], 'direct'), enable=0, backgroundColor=(24 / 255.0, 201 / 255.0, 170 / 255.0))
        self.uiContent['drivenKeyBtn'] = cmds.button(l='Driven Key', w=150, command=partial(self.addNewItemButtonCommand, self.uiContent['editorFrameLayout'], 'drivenKey'), enable=0, backgroundColor=(222 / 255.0, 114 / 255.0, 122 / 255.0))
        self.uiContent['expressionBtn'] = cmds.button(l='Expression', w=150, command=partial(self.addNewItemButtonCommand, self.uiContent['editorFrameLayout'], 'expr'), enable=0, backgroundColor=(203 / 255.0, 165 / 255.0, 241 / 255.0))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout(self.uiContent['presetsDwFormLayout'], e=True, attachForm=([sl1, 'top', 2],
         [sl1, 'left', 2],
         [sl1, 'right', 2],
         [sl1, 'bottom', 2]))

    def editKeyFrame(self, targetNodeAndAttr, weightedTangents, keyframe, *args):
        driverVal = keyframe.get('driverVal')
        inTangentType = keyframe.get('inTangentType')
        outTangentType = keyframe.get('outTangentType')
        inAngle = keyframe.get('inAngle')
        outAngle = keyframe.get('outAngle')
        inWeight = keyframe.get('inWeight')
        outWeight = keyframe.get('outWeight')
        lock = keyframe.get('lock')
        weightLock = keyframe.get('weightLock')
        animCurves = cmds.keyframe(targetNodeAndAttr, name=True, query=True)
        if animCurves:
            animCurve = animCurves[0]
            cmds.selectKey(clear=True)
            mel.eval('selectKey -add -k -f %s "%s";\n' % (driverVal, animCurve))
            if weightedTangents:
                cmds.keyTangent(weightedTangents=weightedTangents)
                if weightLock:
                    cmds.keyTangent(weightLock=weightLock)
            if lock:
                cmds.keyTangent(lock=lock)
            cmds.keyTangent(itt=inTangentType, ott=outTangentType)
            if inTangentType == 'fixed':
                cmds.keyTangent(inAngle=inAngle, inWeight=inWeight)
            if outTangentType == 'fixed':
                cmds.keyTangent(inAngle=outAngle, inWeight=outWeight)

    def editPresetFileCmd(self, button, *args):
        if cmds.button(self.uiContent['presetNewButton'], label=True, q=1) == 'Add':
            om.MGlobal.displayWarning('Please press the [Add] button!')
            return
        presetsDir = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=1, q=1)
        buttonLabel = cmds.button(button, label=True, query=True)
        buttonAnnotation = cmds.button(button, annotation=True, query=True)
        presetNameBuf = buttonAnnotation.split('-')
        sourceNodeType = presetNameBuf[0]
        targetNodeType = presetNameBuf[1]
        presetFilePath = presetsDir + buttonLabel
        mappingRule = self.xmlFileToMappingRule(xmlFilePath=presetFilePath, mode=sourceNodeType + '-' + targetNodeType)
        cmds.textScrollList(self.uiContent['sourceNodeTextScrollList'], selectItem=sourceNodeType, edit=True)
        cmds.textScrollList(self.uiContent['targetNodeTextScrollList'], selectItem=targetNodeType, edit=True)
        self.presetFileBtnCmd()
        connectionItems = mappingRule.get('connection')
        if connectionItems:
            for cItem in connectionItems:
                cmds.connectAttr(self.stempNode + '.' + cItem.get('sourceAttribute'), self.ttempNode + '.' + cItem.get('targetAttribute'), f=1)

        changeItems = mappingRule.get('change')
        if changeItems:
            for cgItem in changeItems:
                controls = self.addNewItemButtonCommand(layout=self.uiContent['editorFrameLayout'], mode='direct')
                try:
                    cmds.optionMenuGrp(controls[0], value=cgItem.get('sourceAttribute'), edit=1)
                except:
                    pass

                cmds.textFieldGrp(controls[1], text=cgItem.get('sourceChangeInfo'), edit=1)
                try:
                    cmds.optionMenuGrp(controls[2], value=cgItem.get('targetAttribute'), edit=1)
                except:
                    pass

                cmds.textFieldGrp(controls[3], text=cgItem.get('targetChangeInfo'), edit=1)

        drivenKeyItems = mappingRule.get('drivenKey')
        if drivenKeyItems:
            cmds.select(self.ttempNode, r=True)
            for dItem in drivenKeyItems:
                if dItem.get('mode') == 'frontward':
                    sourceAttr = dItem.get('sourceAttribute')
                    targetAttr = dItem.get('targetAttribute')
                    sourceNodeAndAttr = self.stempNode + '.' + sourceAttr
                    targetNodeAndAttr = self.ttempNode + '.' + targetAttr
                    weightedTangents = dItem.get('weightedTangents')
                    preInfinite = dItem.get('preInfinite')
                    postInfinite = dItem.get('postInfinite')
                    controls = self.addNewItemButtonCommand(layout=self.uiContent['editorFrameLayout'], mode='drivenKey')
                    cmds.optionMenuGrp(controls[0], value=sourceAttr, edit=1)
                    cmds.optionMenuGrp(controls[1], value=targetAttr, edit=1)
                    self.optionMenuGrpChangeCmd(controls[0], controls[1], controls[2])
                    for index in range(0, len(dItem['keyframes'])):
                        keyframe = dItem['keyframes'][index]
                        cmds.setAttr(sourceNodeAndAttr, float(keyframe.get('driverVal')))
                        try:
                            cmds.setAttr(targetNodeAndAttr, float(keyframe.get('drivenVal')))
                        except:
                            cmds.setAttr(self.ttempNode + '.' + targetAttr + 'R', float(keyframe.get('drivenVal')))
                            cmds.setAttr(self.ttempNode + '.' + targetAttr + 'G', float(keyframe.get('drivenVal')))
                            cmds.setAttr(self.ttempNode + '.' + targetAttr + 'B', float(keyframe.get('drivenVal')))

                        cmds.setDrivenKeyframe(targetNodeAndAttr, currentDriver=sourceNodeAndAttr)
                        self.editKeyFrame(targetNodeAndAttr, weightedTangents, keyframe)

                    cmds.setInfinity(self.ttempNode, at=targetAttr, preInfinite=preInfinite, postInfinite=postInfinite)

        expressionItems = mappingRule.get('expression')
        if expressionItems:
            for expressionItem in expressionItems:
                controls = self.addNewItemButtonCommand(layout=self.uiContent['editorFrameLayout'], mode='expr')
                try:
                    cmds.optionMenuGrp(controls[0], value=expressionItem.get('sourceExpressionAttribute'), edit=1)
                except:
                    pass

                cmds.textFieldGrp(controls[1], text=expressionItem.get('sourceExpressionInfo'), edit=1)
                try:
                    cmds.optionMenuGrp(controls[2], value=expressionItem.get('targetExpressionAttribute'), edit=1)
                except:
                    pass

                cmds.textFieldGrp(controls[3], text=expressionItem.get('targetExpressionInfo'), edit=1)

        cmds.select(self.stempNode, r=1)
        cmds.select(self.ttempNode, add=1)
        cmds.ConnectionEditor()

    def flipAsStringList(self, asStringList, *args):
        newAsStringList = []
        for index in range(0, len(asStringList)):
            newElement = (asStringList[index][1], asStringList[index][0], asStringList[index][2])
            newAsStringList.append(newElement)

        asStringList = sorted(asStringList, key=lambda asStringElement: asStringElement[1])
        return asStringList

    def floatFieldExpression(self, control1, control2, *args):
        control1Value = cmds.floatField(control1, value=1, q=1)
        control2Value = 1 / float(control1Value)
        cmds.floatField(control2, value=control2Value, enable=True, e=1)

    def graphEditorBtnCmd(self, *args):
        mel.eval('GraphEditor')

    def iconTextButtonDirectCmd(self, ui, om1, om2, tfg1, tfg2, *args):
        cmds.deleteUI(ui)
        self.uiContent['editorFrames'].remove(ui)
        self.uiContent['editorSourceOptionMenuGrp'].remove(om1)
        self.uiContent['editorTargetOptionMenuGrp'].remove(om2)
        self.uiContent['editorSourceTextFieldGrp'].remove(tfg1)
        self.uiContent['editorTargetTextFieldGrp'].remove(tfg2)

    def iconTextButtonDrivenKeyCmd(self, ui, om1, om2, cml, *args):
        targetAttr = cmds.optionMenuGrp(om2, v=1, q=1)
        drivenChannel = self.ttempNode + '.' + targetAttr
        animCurves = cmds.keyframe(drivenChannel, name=True, query=True)
        if animCurves:
            for animCurve in animCurves:
                cmds.delete(animCurve)

        cmds.deleteUI(ui)
        self.uiContent['editorDrivenKeyFrames'].remove(ui)
        self.uiContent['editorSourceDrivenKeyOptionMenuGrp'].remove(om1)
        self.uiContent['editorTargetDrivenKeyOptionMenuGrp'].remove(om2)

    def iconTextButtonExpressionCmd(self, ui, om1, om2, tfg1, tfg2, *args):
        cmds.deleteUI(ui)
        self.uiContent['editorExprFrames'].remove(ui)
        self.uiContent['editorSourceExprOptionMenuGrp'].remove(om1)
        self.uiContent['editorTargetExprOptionMenuGrp'].remove(om2)
        self.uiContent['editorSourceExprTextFieldGrp'].remove(tfg1)
        self.uiContent['editorTargetExprTextFieldGrp'].remove(tfg2)

    def iconTextCheckBoxOffCmd(self, object, *args):
        cmds.iconTextCheckBox(object, edit=1, backgroundColor=[82 / 255.0, 82 / 255.0, 82 / 255.0], enableBackground=1, label='')

    def iconTextCheckBoxOnCmd(self, object, *args):
        cmds.iconTextCheckBox(object, edit=1, backgroundColor=[104 / 255.0, 140 / 255.0, 182 / 255.0], enableBackground=1, label='Sel')

    def initPresetFilePath(self):
        filePath = self.userAppDir + 'Presets/jn_shaderTransfer/presets'
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        return filePath

    def keyBtnCmd(self, om1, om2, *args):
        sourceAttr = cmds.optionMenuGrp(om1, value=True, query=True)
        targetAttr = cmds.optionMenuGrp(om2, value=True, query=True)
        cmds.setDrivenKeyframe('%s.%s' % (self.ttempNode, targetAttr), currentDriver='%s.%s' % (self.stempNode, sourceAttr), inTangentType='linear', outTangentType='linear')

    def insertKeywordMenuCallback(self, tfg, token, *args):
        expression = cmds.textFieldGrp(tfg, text=True, query=True)
        if expression == '':
            cmds.textFieldGrp(tfg, text=token, forceChangeCommand=True, edit=True)
        else:
            cmds.textFieldGrp(tfg, insertText=token, forceChangeCommand=True, edit=True)

    def modifyCurrentKeyCmd(self, gc, ffg1, ffg2, *args):
        value1 = cmds.floatFieldGrp(ffg2, value1=True, query=True)
        value2 = cmds.floatFieldGrp(ffg1, value1=True, query=True)
        currentKey = cmds.gradientControlNoAttr(gc, currentKey=True, query=True)
        asString = cmds.gradientControlNoAttr(gc, asString=True, query=True)
        asStringList = self.resultAsStringList(asString=asString)
        newValueAndPoint = (value1, value2, 1)
        newAsStringList = []
        for index in range(0, len(asStringList)):
            if index == currentKey:
                newAsStringList.append(newValueAndPoint)
            else:
                newAsStringList.append(asStringList[index])

        newAsStringList = sorted(newAsStringList, key=lambda asStringElement: asStringElement[1])
        asString = self.conservList2String(asStringList=newAsStringList)
        cmds.gradientControlNoAttr(gc, asString=asString, edit=True)

    def optionMenuGrpChangeCmd(self, om1, om2, cml, *args):
        childControl = cmds.columnLayout(cml, childArray=True, query=True)
        if childControl:
            [ cmds.deleteUI(child) for child in childControl ]
        sourceAttr = cmds.optionMenuGrp(om1, value=True, query=True)
        targetAttr = cmds.optionMenuGrp(om2, value=True, query=True)
        try:
            cmds.setParent(cml)
            afsg1 = cmds.attrControlGrp(label='', a='%s.%s' % (self.stempNode, sourceAttr), hideMapButton=True)
            afsg2 = cmds.attrControlGrp(label='', a='%s.%s' % (self.ttempNode, targetAttr), hideMapButton=True)
            self.uiContent['editorSourceExprAttrFieldSliderGrp'].append(afsg1)
            self.uiContent['editorTargetExprAttrFieldSliderGrp'].append(afsg2)
        except:
            pass

    def presetFileBtnCmd(self, *args):
        sourceNodeTypes = cmds.textScrollList(self.uiContent['sourceNodeTextScrollList'], selectItem=True, query=True)
        targetNodeTypes = cmds.textScrollList(self.uiContent['targetNodeTextScrollList'], selectItem=True, query=True)
        if sourceNodeTypes and targetNodeTypes:
            sourceNodeType = sourceNodeTypes[0]
            targetNodeType = targetNodeTypes[0]
            if sourceNodeType == targetNodeType:
                cmds.button(self.uiContent['presetNewButton'], bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), label='New', e=1)
                return om.MGlobal.displayWarning('Please settting different source and target type!')
            if cmds.button(self.uiContent['presetNewButton'], label=True, q=1) == 'New':
                self.editorCmd()
                if sourceNodeType in self.lightTypes:
                    self.stempParentNode = cmds.shadingNode(sourceNodeType, asLight=True)
                    self.stempNode = cmds.listRelatives(self.stempParentNode, shapes=True)[0]
                else:
                    self.stempNode = cmds.createNode(sourceNodeType, n=sourceNodeType + '_Preset')
                if targetNodeType in self.lightTypes:
                    self.ttempParentNode = cmds.shadingNode(targetNodeType, asLight=True)
                    self.ttempNode = cmds.listRelatives(self.ttempParentNode, shapes=True)[0]
                else:
                    self.ttempNode = cmds.createNode(targetNodeType, n=targetNodeType + '_Preset')
                cmds.select(self.stempNode, r=1)
                cmds.select(self.ttempNode, add=1)
                cmds.ConnectionEditor()
                cmds.button(self.uiContent['presetNewButton'], bgc=(0.2, 0.3, 0.4), label='Add', e=1)
                cmds.button(self.uiContent['directBtn'], enable=1, edit=1)
                cmds.button(self.uiContent['drivenKeyBtn'], enable=1, edit=1)
                cmds.button(self.uiContent['expressionBtn'], enable=1, edit=1)
            elif cmds.button(self.uiContent['presetNewButton'], label=True, q=1) == 'Add':
                if self.addPresetToXMLFile():
                    cmds.delete(self.stempNode, self.ttempNode)
                    try:
                        cmds.delete(self.stempParentNode, self.ttempParentNode)
                    except:
                        pass

                    cmds.button(self.uiContent['directBtn'], enable=0, edit=1)
                    cmds.button(self.uiContent['drivenKeyBtn'], enable=0, edit=1)
                    cmds.button(self.uiContent['expressionBtn'], enable=0, edit=1)
                    if self.uiContent['editorFrames']:
                        for editor in self.uiContent['editorFrames']:
                            cmds.deleteUI(editor)

                    if self.uiContent['editorDrivenKeyFrames']:
                        for editor in self.uiContent['editorDrivenKeyFrames']:
                            cmds.deleteUI(editor)

                    if self.uiContent['editorExprFrames']:
                        for editor in self.uiContent['editorExprFrames']:
                            cmds.deleteUI(editor)

                    self.uiContent['editorFrames'] = []
                    self.uiContent['editorSourceOptionMenuGrp'] = []
                    self.uiContent['editorTargetOptionMenuGrp'] = []
                    self.uiContent['editorSourceTextFieldGrp'] = []
                    self.uiContent['editorTargetTextFieldGrp'] = []
                    self.uiContent['editorDrivenKeyFrames'] = []
                    self.uiContent['editorSourceDrivenKeyOptionMenuGrp'] = []
                    self.uiContent['editorTargetDrivenKeyOptionMenuGrp'] = []
                    self.uiContent['editorExprFrames'] = []
                    self.uiContent['editorSourceExprOptionMenuGrp'] = []
                    self.uiContent['editorTargetExprOptionMenuGrp'] = []
                    self.uiContent['editorSourceExprTextFieldGrp'] = []
                    self.uiContent['editorTargetExprTextFieldGrp'] = []
                    cmds.button(self.uiContent['presetNewButton'], bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), label='New', e=1)
                    try:
                        cmds.deleteUI('connectWindow')
                        cmds.deleteUI(self.uiContent['presetsDwFormLayout'])
                        cmds.paneLayout(self.uiContent['mainPaneLayout'], configuration='vertical2', staticWidthPane=2, edit=True)
                        self.uiContent['size'] = (700, 600)
                        cmds.window(self.uiContent['window'], widthHeight=self.uiContent['size'], sizeable=False, edit=True)
                    except:
                        pass

                    self.updatePresetLibrary()

    def presetFilePathBrowseButtonCmd(self, *args):
        tempDir = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], q=1, text=1)
        tempBrowse = cmds.fileDialog2(fm=3, cap='Browse to Destination Directory', dir=tempDir, okCaption='Set')
        if tempBrowse != None:
            cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], e=1, text=tempBrowse[0] + '/')
            self.iniFile.setValue('presets_dir', '%s' % tempBrowse[0])
            self.updatePresetLibrary()
        return

    def renamePresetFileCmd(self, button, *args):
        buttonLabel = cmds.button(button, label=True, query=True)
        presetFilePath = self.presetsDir + '/' + buttonLabel
        if os.path.exists(presetFilePath):
            result = cmds.promptDialog(title='Rename Preset', message='Enter Name:', text=buttonLabel, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
            if result == 'OK':
                newName = cmds.promptDialog(query=True, text=True)
                newPresetFilePath = self.presetsDir + '/' + newName
                cmds.button(button, label=newName, e=1)
                os.rename(presetFilePath, newPresetFilePath)
                om.MGlobal.displayInfo('The "%s" file already renamed "%s!"' % (presetFilePath, newPresetFilePath))

    def resultAsStringList(self, asString, *args):
        asStringList = []
        asStringBuf = asString.split(',')
        for index in range(1, len(asStringBuf) + 1):
            if index != 0:
                if not index % 3:
                    tempList = (float(asStringBuf[index - 3]), float(asStringBuf[index - 2]), float(asStringBuf[index - 1]))
                    asStringList.append(tempList)

        asStringList = sorted(asStringList, key=lambda asStringElement: asStringElement[1])
        return asStringList

    def selectPresetsFileBtn(self, *args):
        source = cmds.button(self.uiContent['oldRefreshButton'], annotation=True, query=True)
        target = cmds.button(self.uiContent['newRefreshButton'], annotation=True, query=True)
        refreshButtonState = [False, False]
        for item in self.presetFilesBtnList:
            btn = item['button']
            btnLabel = cmds.button(btn, annotation=True, query=True)
            if btnLabel == source + '-' + target:
                cmds.button(btn, bgc=(59 / 255.0, 204 / 255.0, 148 / 255.0), edit=True)
                refreshButtonState[0] = True
            elif btnLabel == target + '-' + source:
                cmds.button(btn, bgc=(36 / 255.0, 169 / 255.0, 191 / 255.0), edit=True)
                refreshButtonState[1] = True
            else:
                cmds.button(btn, bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), edit=True)
                cmds.button(btn, nbg=0, edit=True)

        if refreshButtonState[0]:
            cmds.button(self.uiContent['oldRefreshButton'], bgc=(59 / 255.0, 204 / 255.0, 148 / 255.0), edit=True)
            cmds.button(self.uiContent['newRefreshButton'], bgc=(59 / 255.0, 204 / 255.0, 148 / 255.0), edit=True)
        else:
            cmds.button(self.uiContent['oldRefreshButton'], bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), edit=True)
            cmds.button(self.uiContent['newRefreshButton'], bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), edit=True)

    def shaderTypeMenuItemCmd(self, mode, buttonLabel, oldShaderType, newShaderType, oldButton, newButton, oldTsl, newTsl, shaderType, *args):
        presetsDir = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=1, q=1)
        presetFilePath = presetsDir + buttonLabel
        if mode == 'old2new':
            mappingRule = self.xmlFileToMappingRule(xmlFilePath=presetFilePath, mode=oldShaderType + '-' + newShaderType)
            cmds.button(self.uiContent['oldRefreshButton'], label=shaderType + '-->>', command=partial(self.transferButtonCmd, 'frontward', oldButton, newButton, oldTsl, newTsl, shaderType, mappingRule), annotation=shaderType, edit=True)
            self.updateTextScrollList(tsl=oldTsl, shaderType=shaderType)
        elif mode == 'new2old':
            mappingRule = self.xmlFileToMappingRule(xmlFilePath=presetFilePath, mode=oldShaderType + '-' + newShaderType)
            cmds.button(self.uiContent['newRefreshButton'], label='<<--' + shaderType, command=partial(self.transferButtonCmd, 'backward', oldButton, newButton, oldTsl, newTsl, shaderType, mappingRule), annotation=shaderType, edit=True)
            self.updateTextScrollList(tsl=newTsl, shaderType=shaderType)
        self.updatePresetLibrary()
        self.selectPresetsFileBtn()

    def tangentTypeCompare(self, string, *args):
        if string == 'fixed':
            return 'linear'
        else:
            return string

    def textScrollLayoutClickCmd(self, tsl, *args):
        selectItem = cmds.textScrollList(tsl, selectItem=True, query=True)
        cmds.select(selectItem, r=True)

    def textScrollListPopupMenuCmd(self, tsl, *args):
        items = cmds.textScrollList(tsl, selectItem=True, query=True)
        for item in items:
            cmds.textScrollList(tsl, removeItem=item, edit=True)
            outAttrs = cmds.listConnections(item, connections=True, plugs=False, source=False, destination=True, skipConversionNodes=False, type='shadingEngine')
            if outAttrs:
                cmds.delete(outAttrs[1])
            cmds.delete(item)

    def transferButtonCmd(self, mode, oldButton, newButton, oldTsl, newTsl, shaderType, mappingRule, *args):
        currentShaderType = cmds.button(oldButton, annotation=True, query=True)
        futureShaderType = cmds.button(newButton, annotation=True, query=True)
        if currentShaderType != futureShaderType:
            if mode == 'frontward':
                self.tsl2tslCmd(oldShader=currentShaderType, newShader=futureShaderType, oldButton=oldButton, newButton=newButton, oldTsl=oldTsl, newTsl=newTsl, mode='frontward', mappingRule=mappingRule)
            if mode == 'backward':
                self.tsl2tslCmd(oldShader=futureShaderType, newShader=currentShaderType, oldButton=newButton, newButton=oldButton, oldTsl=newTsl, newTsl=oldTsl, mode='backward', mappingRule=mappingRule)

    def tsl2tslCmd(self, oldShader, newShader, oldButton, newButton, oldTsl, newTsl, mode, mappingRule, *args):
        selectItem = cmds.textScrollList(oldTsl, selectItem=True, query=True)
        if selectItem:
            size = len(selectItem)
            if size:
                step = float(100 / size)
            else:
                step = 1
            amount = 0
            cmds.progressWindow(title='Progress', progress=amount, status='completed:', isInterruptable=True)
            for item in selectItem:
                attrs = cmds.listConnections(item, connections=True, plugs=True, source=True, destination=False, skipConversionNodes=False)
                SGNodes = cmds.listConnections(item, type='shadingEngine')
                if newShader:
                    newSGNode = ''
                    if newShader in self.lightTypes:
                        rsLightType = self.lightTypeMap.get(cmds.nodeType(item), None)
                        newShaderParentNode = cmds.shadingNode(newShader, asLight=True)
                        newShaderNode = cmds.listRelatives(newShaderParentNode, shapes=True)[0]
                        if rsLightType != None:
                            cmds.setAttr(newShaderNode + '.lightType', rsLightType)
                    else:
                        newShaderNode = cmds.shadingNode(newShader, asShader=True)
                        newSGNode = cmds.sets(name=newShaderNode + 'SG', renderable=True, noSurfaceShader=True, empty=True)
                        if newShader in self.shaderTypeDic['mayaArnoldVRayRedshiftShaders']:
                            try:
                                cmds.connectAttr(newShaderNode + '.outColor', newSGNode + '.surfaceShader', f=True)
                            except:
                                pass

                        if newShader in self.shaderTypeDic['mayaShaders']:
                            try:
                                cmds.connectAttr(newShaderNode + '.outColor', newSGNode + '.surfaceShader', f=True)
                                cmds.connectAttr(newShaderNode + '.displacement', newSGNode + '.displacementShader', f=True)
                            except:
                                pass

                        if newShader in self.shaderTypeDic['mentalRayShaders']:
                            try:
                                cmds.connectAttr(newShaderNode + '.outValue', newSGNode + '.miMaterialShader', f=True)
                            except:
                                pass

                        if newShader in self.shaderTypeDic['mentalRayShadersA']:
                            try:
                                cmds.connectAttr(newShaderNode + '.message', newSGNode + '.miMaterialShader', f=True)
                            except:
                                pass

                        if newShader in self.shaderTypeDic['mentalRayShadersB']:
                            try:
                                cmds.connectAttr(newShaderNode + '.message', newSGNode + '.miShadowShader', f=True)
                                cmds.connectAttr(newShaderNode + '.message', newSGNode + '.miPhotonShader', f=True)
                                cmds.connectAttr(newShaderNode + '.message', newSGNode + '.miMaterialShader', f=True)
                            except:
                                pass

                        if newShader in self.shaderTypeDic['mentalRayShadersC']:
                            try:
                                cmds.connectAttr(newShaderNode + '.outValue', newSGNode + '.miMaterialShader', f=True)
                                cmds.connectAttr(newShaderNode + '.outValue', newSGNode + '.miPhotonShader', f=True)
                            except:
                                pass

                    connectionItems = mappingRule['connection']
                    if connectionItems:
                        for connectionItem in connectionItems:
                            sourceAttribute = connectionItem.get('sourceAttribute')
                            targetAttribute = connectionItem.get('targetAttribute')
                            if attrs:
                                for i in range(0, len(attrs)):
                                    if i % 2:
                                        attrBuffer = attrs[i - 1].split('.')
                                        if sourceAttribute == attrBuffer[1]:
                                            cmds.disconnectAttr(attrs[i], attrs[i - 1])
                                            inputAttrBuffer = attrs[i].split('.')
                                            if cmds.nodeType(inputAttrBuffer[0]) == 'VRayPluginNodeTex' and cmds.nodeType(newShaderNode)[:8] == 'Redshift':
                                                samplerInfoNode = cmds.shadingNode('samplerInfo', asUtility=True)
                                                rampNode = cmds.shadingNode('ramp', asTexture=True)
                                                place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility=True)
                                                cmds.connectAttr(place2dTextureNode + '.outUV', rampNode + '.uv')
                                                cmds.connectAttr(place2dTextureNode + '.outUvFilterSize', rampNode + '.uvFilterSize')
                                                cmds.connectAttr(rampNode + '.outColor', newShaderNode + '.' + targetAttribute, f=True)
                                                cmds.connectAttr(inputAttrBuffer[0] + '.color1', rampNode + '.colorEntryList[1].color')
                                                cmds.connectAttr(inputAttrBuffer[0] + '.color2', rampNode + '.colorEntryList[0].color')
                                                cmds.connectAttr(samplerInfoNode + '.facingRatio', rampNode + '.uvCoord.uCoord')
                                                cmds.connectAttr(samplerInfoNode + '.facingRatio', rampNode + '.uvCoord.vCoord')
                                                cmds.removeMultiInstance(rampNode + '.colorEntryList[2]', b=True)
                                                cmds.setAttr(rampNode + '.colorEntryList[1].position', 1)
                                            elif cmds.nodeType(inputAttrBuffer[0]) == 'ramp' and cmds.nodeType(item)[:8] == 'Redshift':
                                                oldRampConnectNodes = cmds.listConnections(inputAttrBuffer[0], connections=False, plugs=False, source=True, destination=False, skipConversionNodes=False)
                                                rampConnectNodes = []
                                                [ rampConnectNodes.append(node) for node in oldRampConnectNodes if node not in rampConnectNodes ]
                                                for rampConnectNode in rampConnectNodes:
                                                    if cmds.nodeType(rampConnectNode) == 'VRayPluginNodeTex':
                                                        cmds.connectAttr(rampConnectNode + '.outColor', newShaderNode + '.' + targetAttribute, f=True)
                                                    else:
                                                        cmds.delete(rampConnectNode)

                                                cmds.delete(inputAttrBuffer[0])
                                            else:
                                                cmds.connectAttr(attrs[i], newShaderNode + '.' + targetAttribute, f=True)
                                                print 'the "%s" already with "%s" connected.' % (attrs[i], newShaderNode + '.' + targetAttribute)

                            currentValue = cmds.getAttr(item + '.' + sourceAttribute)
                            sourceAttrType = cmds.attributeQuery(sourceAttribute, node=item, attributeType=True)
                            if sourceAttrType == 'float3':
                                try:
                                    cmds.setAttr(newShaderNode + '.' + targetAttribute, currentValue[0][0], currentValue[0][1], currentValue[0][2], type='double3')
                                    print 'setAttr "%s" %s;' % (newShaderNode + '.' + targetAttribute,
                                     currentValue[0][0],
                                     currentValue[0][1],
                                     currentValue[0][2])
                                except:
                                    pass

                            else:
                                try:
                                    cmds.setAttr(newShaderNode + '.' + targetAttribute, currentValue)
                                    print 'setAttr "%s" %s;' % (newShaderNode + '.' + targetAttribute, currentValue)
                                except:
                                    pass

                    destNodeAndAttrs = cmds.listConnections(item, connections=False, plugs=True, source=False, destination=True, skipConversionNodes=False)
                    if destNodeAndAttrs:
                        for destNodeAndAttr in destNodeAndAttrs:
                            nodeName = destNodeAndAttr.split('.')[0]
                            nodeType = cmds.nodeType(nodeName)
                            if nodeName not in mayaNodeNames and nodeType not in mayaNodeTypes:
                                try:
                                    cmds.connectAttr(newShaderNode + '.outColor', destNodeAndAttr, f=True)
                                except:
                                    pass

                            if newShader in self.lightTypes:
                                cmds.connectAttr(newShaderNode + '.message', destNodeAndAttr, f=True)

                    changeItems = mappingRule['change']
                    if changeItems:
                        for changeItem in changeItems:
                            if attrs:
                                for i in range(0, len(attrs)):
                                    if i % 2:
                                        attrBuffer = attrs[i - 1].split('.')
                                        if changeItem.get('sourceAttribute') == attrBuffer[1]:
                                            attrs[i] = attrs[i].split('.')[0] + '.' + changeItem.get('sourceChangeInfo')
                                            cmds.connectAttr(attrs[i], newShaderNode + '.' + changeItem.get('targetAttribute'), f=True)
                                            print 'the "%s" already with "%s" connected.' % (attrs[i], newShaderNode + '.' + changeItem.get('targetAttribute'))

                    drivenKeyItems = mappingRule['drivenKey']
                    if drivenKeyItems:
                        tempName = '_reference%s' % str(time.time()).split('.')[0]
                        if not cmds.objExists(oldShader + tempName):
                            self.stempNode = cmds.createNode(oldShader, name=oldShader + tempName)
                            cmds.lockNode(self.stempNode, lock=True)
                        if not cmds.objExists(newShader + tempName):
                            self.ttempNode = cmds.createNode(newShader, name=newShader + tempName)
                            cmds.lockNode(self.ttempNode)
                        for eItem in drivenKeyItems:
                            if eItem.get('mode') == mode:
                                sourceAttr = eItem.get('sourceAttribute')
                                targetAttr = eItem.get('targetAttribute')
                                sourceNodeAndAttr = self.stempNode + '.' + sourceAttr
                                targetNodeAndAttr = self.ttempNode + '.' + targetAttr
                                weightedTangents = eItem.get('weightedTangents')
                                preInfinite = eItem.get('preInfinite')
                                postInfinite = eItem.get('postInfinite')
                                for index in range(0, len(eItem['keyframes'])):
                                    keyframe = eItem['keyframes'][index]
                                    cmds.setAttr(sourceNodeAndAttr, float(keyframe.get('driverVal')))
                                    cmds.setAttr(targetNodeAndAttr, float(keyframe.get('drivenVal')))
                                    cmds.setDrivenKeyframe(targetNodeAndAttr, currentDriver=sourceNodeAndAttr)
                                    self.editKeyFrame(targetNodeAndAttr, weightedTangents, keyframe)

                                cmds.setInfinity(self.ttempNode, at=targetAttr, preInfinite=preInfinite, postInfinite=postInfinite)
                                value = cmds.getAttr(item + '.' + sourceAttr)
                                valueType = type(value)
                                attrType = cmds.getAttr(item + '.' + sourceAttr, type=True)
                                if valueType == list:
                                    if len(value[0]) == 3:
                                        cmds.setAttr(sourceNodeAndAttr, tuple(value))
                                        newValue = cmds.getAttr(targetNodeAndAttr)
                                        try:
                                            cmds.setAttr(newShaderNode + '.' + targetAttr, tuple(newValue))
                                            print 'The "%s.%s" setting to %s.' % (newShaderNode, targetAttr, newValue)
                                        except:
                                            print 'The "%s.%s" have not setting to %s.' % (newShaderNode, targetAttr, newValue)

                                    elif type(value) == float:
                                        cmds.setAttr(sourceNodeAndAttr, value)
                                        newValue = cmds.getAttr(targetNodeAndAttr)
                                        try:
                                            cmds.setAttr(newShaderNode + '.' + targetAttr, newValue)
                                            print 'The "%s.%s" setting to %s.' % (newShaderNode, targetAttr, newValue)
                                        except:
                                            print 'The "%s.%s" have not setting to %s.' % (newShaderNode, targetAttr, newValue)

                                if attrType == 'float3':
                                    cmds.setAttr(sourceNodeAndAttr, value[0], value[1], value[2], type='double3')
                                    newValue = cmds.getAttr(targetNodeAndAttr)
                                    try:
                                        cmds.setAttr(newShaderNode + '.' + targetAttr, newValue[0][0], newValue[0][1], newValue[0][2], type='double3')
                                        print 'The "%s.%s" setting to %s.' % (newShaderNode, targetAttr, newValue)
                                    except:
                                        pass

                                else:
                                    cmds.setAttr(sourceNodeAndAttr, value)
                                    newValue = cmds.getAttr(targetNodeAndAttr)
                                    try:
                                        cmds.setAttr(newShaderNode + '.' + targetAttr, newValue)
                                        print 'The "%s.%s" setting to %s.' % (newShaderNode, targetAttr, newValue)
                                    except:
                                        print 'The "%s.%s" have not setting to %s.' % (newShaderNode, targetAttr, newValue)

                        cmds.lockNode(self.stempNode, lock=False)
                        cmds.lockNode(self.ttempNode, lock=False)
                        stempParentNode = cmds.listRelatives(self.stempNode, parent=True)
                        ttempParentNode = cmds.listRelatives(self.ttempNode, parent=True)
                        if stempParentNode:
                            cmds.delete(stempParentNode[0])
                        else:
                            cmds.delete(self.stempNode)
                        if ttempParentNode:
                            cmds.delete(ttempParentNode[0])
                        else:
                            cmds.delete(self.ttempNode)
                    expressionItems = mappingRule['expression']
                    if expressionItems:
                        for expressionItem in expressionItems:
                            sourceAttribute = expressionItem.get('sourceExpressionAttribute')
                            sourceNodeAndAttr = item + '.' + sourceAttribute
                            targetAttribute = expressionItem.get('targetExpressionAttribute')
                            targetNodeAndAttr = newShaderNode + '.' + targetAttribute
                            sourceExpressionInfo = expressionItem.get('sourceExpressionInfo')
                            if sourceExpressionInfo.find('<Dict>:') != -1:
                                attrMapDict = eval(sourceExpressionInfo[7:])
                                sourceAttrValue = cmds.getAttr(sourceNodeAndAttr)
                                targetAttrValue = attrMapDict.get(sourceAttrValue, None)
                                if isinstance(targetAttrValue, list):
                                    targetAttrValue = targetAttrValue[0]
                                cmds.setAttr(targetNodeAndAttr, targetAttrValue)
                                print 'The "%s" setting to %s' % (targetNodeAndAttr, targetAttrValue)
                            else:
                                try:
                                    expressionString = sourceExpressionInfo.replace('<Node>', item).replace('<Attr>', expressionItem.get('sourceExpressionAttribute'))
                                    nullGroup = cmds.group(empty=True)
                                    cmds.expression(string='%s.translateX = %s;' % (nullGroup, expressionString))
                                    resultValue = cmds.getAttr(nullGroup + '.translateX')
                                    cmds.setAttr(targetNodeAndAttr, resultValue, clamp=True)
                                    print 'The "%s" setting to %s' % (targetNodeAndAttr, resultValue)
                                    cmds.delete(nullGroup)
                                except:
                                    om.MGlobal.displayWarning(u'Please modify the expression setting.')

                    self.bumpTransfer(oldShader=item, newShader=newShaderNode, newSGNode=newSGNode)
                    try:
                        oldShaderParent = cmds.listRelatives(item, parent=True)[0]
                        newShaderParent = cmds.listRelatives(newShaderNode, parent=True)[0]
                        oldShaderParentMatrix = cmds.xform(oldShaderParent, matrix=True, worldSpace=True, query=True)
                        cmds.xform(newShaderParent, matrix=oldShaderParentMatrix)
                    except:
                        pass

                    if SGNodes:
                        SGNode = SGNodes[0]
                        sourceAttrs = cmds.listConnections(SGNode, plugs=True, source=True, destination=False, connections=True, shapes=True)
                        connectNodes = cmds.listConnections(SGNode, plugs=False, shapes=True, connections=False, type='groupId')
                        if connectNodes:
                            for connectNode in connectNodes:
                                cmds.lockNode(connectNode, lock=True)

                        try:
                            cmds.delete(SGNode)
                        except:
                            pass

                        if connectNodes:
                            for connectNode in connectNodes:
                                cmds.lockNode(connectNode, lock=False)

                        if sourceAttrs:
                            for indexA in range(0, len(sourceAttrs)):
                                if indexA % 2:
                                    attrBuf = sourceAttrs[indexA - 1].split('.')
                                    attr = attrBuf[1]
                                    try:
                                        cmds.connectAttr(sourceAttrs[indexA], '%s.%s' % (newSGNode, attr))
                                    except:
                                        om.MGlobal.displayInfo('The "%s" have not connect the "%s.%s"' % (sourceAttrs[indexA], newSGNode, attr))

                    cmds.textScrollList(newTsl, append=newShaderNode, edit=True)
                    if cmds.progressWindow(query=True, isCancelled=True):
                        break
                    if cmds.progressWindow(query=True, progress=True) >= 100:
                        break
                    amount += step
                    cmds.progressWindow(edit=True, progress=amount)
                    if not item == 'lambert1':
                        itemParentNodes = cmds.listRelatives(item, parent=True)
                        if itemParentNodes:
                            itemParentNode = itemParentNodes[0]
                            if cmds.nodeType(item) == 'VRayLightRectShape' and cmds.nodeType(newShaderNode) == 'RedshiftPhysicalLight' and cmds.getAttr(newShaderNode + '.lightType') == 0:
                                scaleXValue = cmds.getAttr(itemParentNode + '.scaleX')
                                scaleYValue = cmds.getAttr(itemParentNode + '.scaleY')
                                scaleZValue = cmds.getAttr(itemParentNode + '.scaleZ')
                                uSizeValue = cmds.getAttr(item + '.uSize')
                                vSizeValue = cmds.getAttr(item + '.vSize')
                                newShaderParentNode = cmds.listRelatives(newShaderNode, parent=True)[0]
                                resultXValue = scaleXValue * uSizeValue
                                resultYValue = scaleYValue * vSizeValue
                                resultZValue = scaleZValue
                                cmds.setAttr(newShaderParentNode + '.scaleX', resultXValue)
                                cmds.setAttr(newShaderParentNode + '.scaleY', resultYValue)
                                cmds.setAttr(newShaderParentNode + '.scaleZ', resultZValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleX', resultXValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleY', resultYValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleZ', resultZValue)
                            elif cmds.nodeType(item) == 'RedshiftPhysicalLight' and cmds.nodeType(newShaderNode) == 'VRayLightRectShape' and cmds.getAttr(item + '.lightType') == 0:
                                scaleXValue = cmds.getAttr(itemParentNode + '.scaleX')
                                scaleYValue = cmds.getAttr(itemParentNode + '.scaleY')
                                scaleZValue = cmds.getAttr(itemParentNode + '.scaleZ')
                                newShaderParentNode = cmds.listRelatives(newShaderNode, parent=True)[0]
                                cmds.setAttr(newShaderParentNode + '.scaleX', scaleXValue)
                                cmds.setAttr(newShaderParentNode + '.scaleY', scaleYValue)
                                cmds.setAttr(newShaderParentNode + '.scaleZ', scaleZValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleX', scaleXValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleY', scaleYValue)
                                print 'The "%s" setting to "%s".' % (newShaderParentNode + '.scaleZ', scaleZValue)
                            cmds.delete(itemParentNode)
                        else:
                            cmds.delete(item)
                        cmds.textScrollList(oldTsl, removeItem=item, edit=True)
                else:
                    om.MGlobal.displayWarning('Please Setting Future Shader!')

            cmds.progressWindow(endProgress=1)
        return

    def updateNoteAnnotation(self, btn, *args):
        xmlFilePath = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=1, q=1)
        xmlFile = cmds.button(btn, label=1, q=1)
        dom = xml.dom.minidom.parse(xmlFilePath + xmlFile)
        root = dom.documentElement
        if root.getElementsByTagName('text'):
            text = root.getElementsByTagName('text')[0]
            cmds.scrollField(self.uiContent['presetFileScrollField'], text=text.firstChild.data, edit=1)
        else:
            cmds.scrollField(self.uiContent['presetFileScrollField'], text='', edit=1)

    def updatePresetLibrary(self, *args):
        for item in self.presetFilesBtnList:
            cmds.deleteUI(item['button'])
            cmds.deleteUI(item['select'])
            cmds.deleteUI(item['layout'], layout=True)

        targetDir = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=True, query=True)
        presetFiles = cmds.getFileList(folder=targetDir, filespec='*.xml')
        self.presetFilesBtnList = []
        for presetFile in presetFiles:
            ppath = self.presetsDir + '/' + presetFile
            tree = ElementTree.parse(ppath)
            root = tree.getroot()
            presetName = root.get('frontward')
            rl1 = cmds.rowLayout(parent=self.uiContent['presetFilesColumnLayout'], numberOfColumns=2, adjustableColumn2=1)
            fileBtn = cmds.button(parent=rl1, label=presetFile, bgc=(94 / 255.0, 94 / 255.0, 94 / 255.0), annotation=presetName)
            fileBtnPM = cmds.popupMenu(parent=fileBtn, button=3)
            cmds.menuItem(parent=fileBtnPM, label='Edit', command=partial(self.editPresetFileCmd, fileBtn))
            cmds.menuItem(parent=fileBtnPM, label='Rename', command=partial(self.renamePresetFileCmd, fileBtn))
            itcb1 = cmds.iconTextCheckBox(parent=rl1, style='textOnly', align='center', width=20, backgroundColor=[82 / 255.0, 82 / 255.0, 82 / 255.0], enableBackground=1)
            cmds.iconTextCheckBox(itcb1, edit=1, onCommand=partial(self.iconTextCheckBoxOnCmd, itcb1), offCommand=partial(self.iconTextCheckBoxOffCmd, itcb1))
            cmds.button(fileBtn, command=partial(self.xmlFileBtnCmd, fileBtn), edit=1)
            self.presetFilesBtnList.append({'layout': rl1,
             'button': fileBtn,
             'select': itcb1})

        self.selectPresetsFileBtn()

    def updateTextScrollList(self, tsl, shaderType, *args):
        sels = cmds.ls(type=shaderType)
        cmds.textScrollList(tsl, removeAll=True, edit=True)
        for sel in sels:
            if sel == 'lambert1':
                continue
            if cmds.nodeType(sel) == shaderType:
                cmds.textScrollList(tsl, append=sel, edit=True)

    def updateFix(self, *args):
        result = cmds.confirmDialog(title='Preset file fix', message='Please backup preset file folder!', button=['Fix', 'Manual', 'Cancel'], defaultButton='Manual', cancelButton='Cancel', dismissString='Cancel')
        if result == 'Fix':
            for presetFile in os.listdir(self.presetsDir):
                presetFilePath = self.presetsDir + '/' + presetFile
                f = open(presetFilePath, 'r')
                fList = []
                for line in f:
                    fList.append(line.replace('expression', 'drivenKey').replace('expressionInfo', 'drivenKeyInfo'))

                f.close()
                f = open(presetFilePath, 'w')
                for line in fList:
                    f.writelines(line)
                    print line

                f.close()
                print '============================'

            om.MGlobal.displayInfo(u'Preset file fix final.')
        elif result == 'Manual':
            webbrowser.open(self.presetsDir)

    def writeXMLFile(self, connectionProps, changeProps, drivenKeyProps, expressionProps, *args):
        sourceNodeType = cmds.textScrollList(self.uiContent['sourceNodeTextScrollList'], selectItem=True, query=True)[0]
        targetNodeType = cmds.textScrollList(self.uiContent['targetNodeTextScrollList'], selectItem=True, query=True)[0]
        presetElement = Element('preset')
        presetElement.set('frontward', sourceNodeType + '-' + targetNodeType)
        presetElement.set('backward', targetNodeType + '-' + sourceNodeType)
        displayInfinities = cmds.animCurveEditor('graphEditor1GraphEd', displayInfinities=True, query=True)
        presetElement.set('displayInfinities', str(int(displayInfinities)))
        connectionPropsElement = SubElement(presetElement, 'connection')
        changePropsElement = SubElement(presetElement, 'change')
        drivenKeyPropsElement = SubElement(presetElement, 'drivenKey')
        expressionPropsElement = SubElement(presetElement, 'expression')
        if connectionProps:
            for connectionProp in connectionProps:
                connectionElement = SubElement(connectionPropsElement, 'connectionInfo')
                connectionElement.set('sourceAttribute', connectionProp['source'])
                connectionElement.set('targetAttribute', connectionProp['target'])
                connectionElement.set('mode', connectionProp['mode'])

        if changeProps:
            for changeProp in changeProps:
                changeElement = SubElement(changePropsElement, 'changeInfo')
                changeElement.set('sourceAttribute', changeProp['source'])
                changeElement.set('targetAttribute', changeProp['target'])
                changeElement.set('sourceChangeInfo', changeProp['sourceChangeInfo'])
                changeElement.set('targetChangeInfo', changeProp['targetChangeInfo'])
                changeElement.set('mode', changeProp['mode'])

        if drivenKeyProps:
            for drivenKeyProp in drivenKeyProps:
                drivenKeyElement = SubElement(drivenKeyPropsElement, 'drivenKeyInfo')
                drivenKeyElement.set('sourceAttribute', drivenKeyProp['source'])
                drivenKeyElement.set('targetAttribute', drivenKeyProp['target'])
                drivenKeyElement.set('mode', drivenKeyProp['mode'])
                drivenKeyElement.set('preInfinite', str(drivenKeyProp['drivenKeyInfo'][0]['preInfinite']))
                drivenKeyElement.set('postInfinite', str(drivenKeyProp['drivenKeyInfo'][0]['postInfinite']))
                drivenKeyElement.set('weightedTangents', str(drivenKeyProp['drivenKeyInfo'][0]['weightedTangents']))
                for index in range(0, len(drivenKeyProp['drivenKeyInfo'])):
                    keyframeElement = SubElement(drivenKeyElement, 'keyframe')
                    keyframeElement.set('driverVal', str(drivenKeyProp['drivenKeyInfo'][index]['driverVal']))
                    keyframeElement.set('drivenVal', str(drivenKeyProp['drivenKeyInfo'][index]['drivenVal']))
                    keyframeElement.set('inTangentType', str(drivenKeyProp['drivenKeyInfo'][index]['inTangentType']))
                    keyframeElement.set('outTangentType', str(drivenKeyProp['drivenKeyInfo'][index]['outTangentType']))
                    keyframeElement.set('inAngle', str(drivenKeyProp['drivenKeyInfo'][index]['inAngle']))
                    keyframeElement.set('outAngle', str(drivenKeyProp['drivenKeyInfo'][index]['outAngle']))
                    keyframeElement.set('inWeight', str(drivenKeyProp['drivenKeyInfo'][index]['inWeight']))
                    keyframeElement.set('outWeight', str(drivenKeyProp['drivenKeyInfo'][index]['outWeight']))
                    keyframeElement.set('lock', str(drivenKeyProp['drivenKeyInfo'][index]['lock']))
                    keyframeElement.set('weightLock', str(drivenKeyProp['drivenKeyInfo'][index]['weightLock']))

        if expressionProps:
            for expressionProp in expressionProps:
                expressionElement = SubElement(expressionPropsElement, 'expressionInfo')
                expressionElement.set('sourceExpressionAttribute', expressionProp['source'])
                expressionElement.set('targetExpressionAttribute', expressionProp['target'])
                expressionElement.set('sourceExpressionInfo', expressionProp['sourceExpressionInfo'])
                expressionElement.set('targetExpressionInfo', expressionProp['targetExpressionInfo'])
                expressionElement.set('mode', expressionProp['mode'])

        dirPath = cmds.textFieldGrp(self.uiContent['shaderPresetsPathTFBG'], q=1, text=1)
        presetFilePath = dirPath + sourceNodeType + '-' + targetNodeType + '.xml'
        saveState = False
        if os.path.exists(presetFilePath):
            result = cmds.confirmDialog(title='Confirm Override?', message='The "%s-%s.xml" file already exists! Confirm override?' % (sourceNodeType, targetNodeType), button=['Override', 'No'], cancelButton='No', dismissString='No')
            if result == 'Override':
                saveState = True
        else:
            saveState = True
        if saveState:
            presetCommand = prettify(presetElement)
            xFile = open(presetFilePath, 'w')
            xFile.write(presetCommand)
            xFile.close()
            om.MGlobal.displayInfo('--------------Shader Prests Saved--------------\tFile: %s' % presetFilePath)
        else:
            saveState = True
        cmds.select(self.ttempNode, r=True)
        return saveState

    def xmlFileBtnCmd(self, button, *args):
        presetsDir = cmds.textFieldButtonGrp(self.uiContent['shaderPresetsPathTFBG'], text=1, q=1)
        buttonLabel = cmds.button(button, label=True, query=True)
        presetFileName = cmds.button(button, annotation=True, query=True)
        presetNameBuf = presetFileName.split('-')
        oldShaderType = presetNameBuf[0]
        newShaderType = presetNameBuf[1]
        self.shaderTypeMenuItemCmd(mode='old2new', buttonLabel=buttonLabel, oldShaderType=oldShaderType, newShaderType=newShaderType, oldButton=self.uiContent['oldRefreshButton'], newButton=self.uiContent['newRefreshButton'], oldTsl=self.uiContent['oldTextScrollList'], newTsl=self.uiContent['newTextScrollList'], shaderType=oldShaderType)
        self.shaderTypeMenuItemCmd(mode='new2old', buttonLabel=buttonLabel, oldShaderType=newShaderType, newShaderType=oldShaderType, oldButton=self.uiContent['oldRefreshButton'], newButton=self.uiContent['newRefreshButton'], oldTsl=self.uiContent['oldTextScrollList'], newTsl=self.uiContent['newTextScrollList'], shaderType=newShaderType)
        self.autoUpdateNodeToTSLCmd()

    def xmlFileToMappingRule(self, xmlFilePath, mode, *args):
        mappingRule = {}
        tree = ElementTree.parse(xmlFilePath)
        root = tree.getroot()
        displayInfinities = root.get('displayInfinities')
        mel.eval('animCurveEditor -edit -displayInfinities %d graphEditor1GraphEd;' % int(displayInfinities))
        ward = ''
        if mode == root.get('frontward'):
            ward = 'frontward'
        elif mode == root.get('backward'):
            ward = 'backward'
        connectionInfos = tree.getiterator('connectionInfo')
        changeInfos = tree.getiterator('changeInfo')
        drivenKeyInfos = tree.getiterator('drivenKeyInfo')
        expressionInfos = tree.getiterator('expressionInfo')
        mappingRule['connection'] = []
        for connectionInfo in connectionInfos:
            if ward == connectionInfo.get('mode'):
                mappingDict = {}
                mappingDict['sourceAttribute'] = connectionInfo.get('sourceAttribute')
                mappingDict['targetAttribute'] = connectionInfo.get('targetAttribute')
                mappingDict['mode'] = connectionInfo.get('mode')
                mappingRule['connection'].append(mappingDict)

        mappingRule['change'] = []
        for changeInfo in changeInfos:
            if ward == changeInfo.get('mode'):
                mappingDict = {}
                mappingDict['sourceAttribute'] = changeInfo.get('sourceAttribute')
                mappingDict['targetAttribute'] = changeInfo.get('targetAttribute')
                mappingDict['sourceChangeInfo'] = changeInfo.get('sourceChangeInfo')
                mappingDict['targetChangeInfo'] = changeInfo.get('targetChangeInfo')
                mappingDict['mode'] = changeInfo.get('mode')
                mappingRule['change'].append(mappingDict)

        mappingRule['drivenKey'] = []
        for drivenKeyInfo in drivenKeyInfos:
            drivenKeyInfoDict = {}
            drivenKeyInfoDict['sourceAttribute'] = drivenKeyInfo.get('sourceAttribute')
            drivenKeyInfoDict['targetAttribute'] = drivenKeyInfo.get('targetAttribute')
            drivenKeyInfoDict['mode'] = drivenKeyInfo.get('mode')
            drivenKeyInfoDict['weightedTangents'] = int(drivenKeyInfo.get('weightedTangents'))
            drivenKeyInfoDict['preInfinite'] = drivenKeyInfo.get('preInfinite')
            drivenKeyInfoDict['postInfinite'] = drivenKeyInfo.get('postInfinite')
            drivenKeyInfoDict['keyframes'] = []
            keyframes = drivenKeyInfo.getiterator('keyframe')
            for keyframe in keyframes:
                keyframeDict = {}
                keyframeDict['driverVal'] = float(keyframe.get('driverVal'))
                keyframeDict['drivenVal'] = float(keyframe.get('drivenVal'))
                keyframeDict['inTangentType'] = keyframe.get('inTangentType')
                keyframeDict['outTangentType'] = keyframe.get('outTangentType')
                keyframeDict['inAngle'] = float(keyframe.get('inAngle'))
                keyframeDict['outAngle'] = float(keyframe.get('outAngle'))
                keyframeDict['inWeight'] = float(keyframe.get('inWeight'))
                keyframeDict['outWeight'] = float(keyframe.get('outWeight'))
                keyframeDict['lock'] = int(keyframe.get('lock'))
                keyframeDict['weightLock'] = int(keyframe.get('weightLock'))
                drivenKeyInfoDict['keyframes'].append(keyframeDict)

            mappingRule['drivenKey'].append(drivenKeyInfoDict)

        mappingRule['expression'] = []
        for expressionInfo in expressionInfos:
            if ward == expressionInfo.get('mode'):
                expressionDict = {}
                expressionDict['sourceExpressionAttribute'] = expressionInfo.get('sourceExpressionAttribute')
                expressionDict['targetExpressionAttribute'] = expressionInfo.get('targetExpressionAttribute')
                expressionDict['sourceExpressionInfo'] = expressionInfo.get('sourceExpressionInfo')
                expressionDict['targetExpressionInfo'] = expressionInfo.get('targetExpressionInfo')
                expressionDict['mode'] = expressionInfo.get('mode')
                mappingRule['expression'].append(expressionDict)

        return mappingRule


def main():
    win.showUI()


if __name__ == '__main__':
    main()