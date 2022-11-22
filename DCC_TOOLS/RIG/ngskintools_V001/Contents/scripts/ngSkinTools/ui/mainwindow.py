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

from maya import cmds
from ngSkinTools import version
from ngSkinTools.license import license
from ngSkinTools.utilities import removeLayerData
from ngSkinTools.utils import Utils
from ngSkinTools.ui.targetDataDisplay import TargetDataDisplay
from ngSkinTools.ui.actions import InfluenceFilterAction, NewLayerAction, \
    DeleteLayerAction, MoveLayerAction, LayerPropertiesAction, \
    ConvertMaskToTransparencyAction, ConvertTransparencyToMaskAction, \
    MirrorLayerWeightsAction, BaseAction, RemovePreferencesAction, \
    EnableDisableLayerAction, ExportAction, ImportAction, TransferWeightsAction, \
    MergeLayerDownAction, InvertPaintTargetAction
from ngSkinTools.log import getLogger
from ngSkinTools.importExport import Formats
from ngSkinTools.ui.utilities.importInfluencesUi import ImportInfluencesAction
from ngSkinTools.ui.utilities.duplicateLayerAction import DuplicateLayersAction
from ngSkinTools.ui.headlessDataHost import HeadlessDataHost
from ngSkinTools.doclink import SkinToolsDocs
from ngSkinTools.ui.utilities.weightsClipboardActions import CopyWeights, \
    CutWeights, PasteWeightsAdd, PasteWeightsReplace, PasteWeightsSubstract
from ngSkinTools.ui.options import PersistentValueModel
from ngSkinTools.ui.events import LayerEvents
from ngSkinTools.ui.uiWrappers import FormLayout

log = getLogger("MainWindow")


class MainMenu:
    def __init__(self):
        pass
    
    def execCheckForUpdates(self, *args):
        from ngSkinTools.versioncheck import checker
        checker.execute(silent=False)
        

    def execAbout(self, *args):
        from ngSkinTools.ui.dlgAbout import AboutDialog
        AboutDialog().execute()
        
    def createFileMenu(self, actions):
        cmds.menu(label='File', mnemonic='F')
        actions.exportWeights.newMenuItem("Export Layers/Weights...")
        actions.importWeights.newMenuItem("Import Layers/Weights...")

    def createLayersMenu(self, actions):
        cmds.menu(label='Layers', mnemonic='L')
        actions.newLayer.newMenuItem("New Layer...")
        actions.duplicateLayer.newMenuItem("Duplicate Selected Layer(s)")
        actions.deleteLayer.newMenuItem("Delete Selected Layer(s)")
        self.createDivider()
        actions.mergeLayerDown.newMenuItem("Merge Layer Down")
        self.createDivider()
        actions.moveLayerUp.newMenuItem("Move Current Layer Up")
        actions.moveLayerDown.newMenuItem("Move Current Layer Down")

        self.createDivider()
        actions.layerProperties.newMenuItem("Properties...")
        
    def createEditMenu(self, actions):
        cmds.menu(label='Edit', mnemonic='E')
        actions.copyWeights.newMenuItem('Copy Influence Weights')
        actions.cutWeights.newMenuItem('Cut Influence Weights')
        actions.pasteWeightsAdd.newMenuItem('Paste Weights (Add)')
        actions.pasteWeightsSubstract.newMenuItem('Paste Weights (Substract)')
        actions.pasteWeightsReplace.newMenuItem('Paste Weights (Replace)')
        self.createDivider()
        actions.convertMaskToTransparency.newMenuItem('Convert Mask to Transparency')
        actions.convertTransparencyToMask.newMenuItem('Convert Transparency to Mask')
        self.createDivider()
        actions.invertPaintTarget.newMenuItem('Invert')
        self.createDivider()
        cmds.menuItem(label='Delete Custom Nodes From Selection', command=lambda *args:removeLayerData.removeLayersFromSelection())
        cmds.menuItem(label='Delete All Custom Nodes', command=lambda *args:removeLayerData.removeAllNodes())

    def createToolsMenu(self, actions):
        cmds.menu(label='Tools', mnemonic='T')
        actions.importInfluences.newMenuItem("Import Influences...")
        actions.transferWeights.newMenuItem("Transfer Weights...")
        
    def viewManual(self, *args):
        documentation = HeadlessDataHost.get().documentation
        documentation.openLink(SkinToolsDocs.DOCUMENTATION_ROOT)
        
    def openLocation(self, url):
        import webbrowser
        webbrowser.open_new(url)
    
    def openIssueTracker(self, *args):
        self.openLocation("https://www.ngskintools.com/issue-tracker")

    def openContactForm(self, *args):
        self.openLocation("https://ngskintools.com/contact/")
        
    def openDonationsPage(self, *args):
        self.openLocation("https://ngskintools.com/donate/")
        
    def openLicenseDialog(self, *args):
        from ngSkinTools.ui.dlgActivation import ActivationDialog
        ActivationDialog().show()
        

    def createHelpMenu(self, actions):
        cmds.menu(label='Help', mnemonic='H')
        cmds.menuItem(label='View Manual Online', command=self.viewManual)
        cmds.menuItem(label='Contact Author directly', command=self.openContactForm)
        cmds.menuItem(label='Check for Updates', command=self.execCheckForUpdates)
        self.createDivider()
        # cmds.menuItem( label='Donate!',command=self.openDonationsPage )
        cmds.menuItem(label="Enter License Key...", command=self.openLicenseDialog)
        self.createDivider()
        actions.removePreferences.newMenuItem('Reset to Default Preferences')
        self.createDivider()
        cmds.menuItem(label='Planned Features and Known Issues', command=self.openIssueTracker)
        cmds.menuItem(label='About ngSkinTools', mnemonic='A', command=self.execAbout)
        
    def createDivider(self):
        cmds.menuItem(divider=True)
        
        
    def create(self,actions):
        self.createFileMenu(actions)
        self.createLayersMenu(actions)
        self.createEditMenu(actions)
        self.createToolsMenu(actions)
        self.createHelpMenu(actions)
    
class MainUiActions:
    def __init__(self, ownerUI):
        self.influenceFilter = InfluenceFilterAction(ownerUI) 
        self.newLayer = NewLayerAction(ownerUI)
        self.deleteLayer = DeleteLayerAction(ownerUI)
        self.moveLayerUp = MoveLayerAction(True, ownerUI)
        self.moveLayerDown = MoveLayerAction(False, ownerUI)
        self.layerProperties = LayerPropertiesAction(ownerUI)
        self.removePreferences = RemovePreferencesAction(ownerUI)
        
        self.convertMaskToTransparency = ConvertMaskToTransparencyAction(ownerUI)
        self.convertTransparencyToMask = ConvertTransparencyToMaskAction(ownerUI)
        
        self.invertPaintTarget = InvertPaintTargetAction(ownerUI)
        
        self.mirrorWeights = MirrorLayerWeightsAction(ownerUI)
        self.enableDisableLayer = EnableDisableLayerAction(ownerUI)
        
        self.importInfluences = ImportInfluencesAction(ownerUI)
        self.transferWeights = TransferWeightsAction(ownerUI)
        
        self.duplicateLayer = DuplicateLayersAction(ownerUI)
        
        self.mergeLayerDown = MergeLayerDownAction(ownerUI)
        
        self.copyWeights = CopyWeights(ownerUI)
        self.cutWeights = CutWeights(ownerUI)
        self.pasteWeightsAdd = PasteWeightsAdd(ownerUI)
        self.pasteWeightsReplace = PasteWeightsReplace(ownerUI)
        self.pasteWeightsSubstract = PasteWeightsSubstract(ownerUI)
        

                
        self.importWeights = ImportAction(ownerUI, ioFormat=Formats.getJsonFormat())
        self.exportWeights = ExportAction(ownerUI, ioFormat=Formats.getJsonFormat())
        
    def updateEnabledAll(self):
        '''
        updates all actions hosted in this instance
        '''
        
        # update all field-based actions
        for i in dir(self):
            field = getattr(self, i)
            if isinstance(field, BaseAction):
                field.updateEnabled()


class MainWindow(object):
    WINDOW_NAME = 'ngSkinToolsMainWindow'
    DOCK_NAME = 'ngSkinToolsMainWindow_dock'
    
    currentInstance = None
    
    def __init__(self):
        if MainWindow.currentInstance!=None:
            raise Exception("creating window second time")
        
        MainWindow.currentInstance = self
        log.debug("creating main window")

        log.debug("loading plugin")
        Utils.loadPlugin()

        log.debug("initiating check for updates")
        Utils.silentCheckForUpdates()

        license.status.recalculate()

        self.windowTitle = self.createWindowTitle()
        
        self.mainTabLayout = None
        self.tabs = []
        
        
        self.targetUI = TargetDataDisplay()
        self.mainMenu = MainMenu()
        
        self.preferedWidth = PersistentValueModel('ngSkinToolsMainWindow_preferedWidth', 400);
        self.preferedHeight = PersistentValueModel('ngSkinToolsMainWindow_preferedHeight', 400);
        self.preferedTop = PersistentValueModel('ngSkinToolsMainWindow_preferedTop');
        self.preferedLeft = PersistentValueModel('ngSkinToolsMainWindow_preferedLeft');
        self.preferedFloating = PersistentValueModel('ngSkinToolsMainWindow_preferedFloating', False)
        
        self.defaultWidth = self.preferedWidth.get()
        self.defaultHeight = self.preferedHeight.get()
        
    @staticmethod
    def getInstance():
        '''
        returns instance of a currently opened main window; returned value is only valid while window is opened.
        
        :rtype: MainWindow
        '''
        
        if MainWindow.currentInstance is None:
            MainWindow()
            
        return MainWindow.currentInstance
        
        
    @staticmethod
    @Utils.visualErrorHandling
    def open():
        '''
        A default entry method for opening ngSkinTools main window.
        
        Do not remove or rename the method, as a lot of configurations depend on this exact
        behavior of the method, e.g., as a shelf button code.
        '''

        
        def openMaya2016():
            '''
            UI creation in 2016.5 and below
            '''
            window = MainWindow.getInstance()
            
            
            if cmds.control(MainWindow.DOCK_NAME, q=True, exists=True):
                cmds.control(MainWindow.DOCK_NAME, e=True, visible=True)
            else:
                contentWindowWidget = cmds.window(MainWindow.WINDOW_NAME)
                window.createUI(parent=contentWindowWidget)
                cmds.dockControl(MainWindow.DOCK_NAME, l=window.createWindowTitle(), content=contentWindowWidget,
                                 area='right', allowedArea=['right', 'left'],
                                 width=window.preferedWidth.get(),
                                 floating=window.preferedFloating.get(),
                                 visibleChangeCommand=window.visibilityChanged)

                if window.preferedFloating.get():
                    cmds.window(MainWindow.DOCK_NAME, e=True,
                                topEdge=window.preferedTop.get(), leftEdge=window.preferedLeft.get(),
                                w=window.preferedWidth.get(), h=window.preferedHeight.get())
                    

            # bring tab to front; evaluate lazily as sometimes UI can show other errors and this command somehow fails
            cmds.evalDeferred(lambda *args: cmds.dockControl(MainWindow.DOCK_NAME, e=True, r=True));
            
            # a bit of a fake, but can't find a better place for an infrequent save
            LayerEvents.layerAvailabilityChanged.addHandler(window.savePrefs, MainWindow.DOCK_NAME)

        def openMaya2017():
            '''
            UI creation for 2017 
            '''
            log.info("rebuilding main window")


            if not cmds.workspaceControl(MainWindow.DOCK_NAME,q=True,exists=True):
                cmds.workspaceControl(MainWindow.DOCK_NAME,
                    retain = False,
                    floating = True,
                    #ttc=["AttributeEditor",-1],
                    uiScript="from ngSkinTools.ui.mainwindow import MainWindow; MainWindow.resumeInWorkspaceControl()")


            # bring tab to front;
            cmds.evalDeferred(lambda *args: cmds.workspaceControl(MainWindow.DOCK_NAME, e=True, r=True));
            


        if Utils.getMayaVersion()<Utils.MAYA2017:
            openMaya2016()
        else:
            openMaya2017()

    @classmethod
    def resumeInWorkspaceControl(cls):
        '''
        used by workspace (Maya 2017+) to restore the main window control
        '''
        log.info("resume workspace control")

        # fix title between upgrades
        cmds.workspaceControl(MainWindow.DOCK_NAME, e=True,
                              label=MainWindow.createWindowTitle())

        try:
            window = MainWindow.getInstance()
            window.createUI(cmds.setParent(q=True))
        except Exception,err:
            log.error("failed to resume workspace control")
            # workspace kills any error messages; just making sure that any errors are printed anyway
            import traceback;traceback.print_exc()
     
    def visibilityChanged(self, *args):
        hidden = cmds.control(self.uiParent, q=True, isObscured=1)
            
        if hidden:
            self.savePrefs()

    def savePrefs(self):
        if cmds.dockControl(self.uiParent, exists=True):
            self.preferedFloating.set(cmds.dockControl(self.uiParent, q=True, floating=True))
            self.preferedWidth.set(cmds.dockControl(self.uiParent, q=True, w=True))

        if cmds.window(self.uiParent, exists=True):
            self.preferedWidth.set(cmds.window(self.uiParent, q=True, w=True))
            self.preferedHeight.set(cmds.window(self.uiParent, q=True, h=True))
            self.preferedTop.set(cmds.window(self.uiParent, q=True, topEdge=True))
            self.preferedLeft.set(cmds.window(self.uiParent, q=True, leftEdge=True))
        
    @staticmethod
    def createWindowTitle():
        '''
        creates main window title
        '''
        return version.getReleaseName()
    
    def createUI(self,parent):
        '''
            creates contents of the main UI window. assumes that current UI parent is the receiving container.
        '''

        cmds.setParent(parent)
        log.debug("create main window UI: p="+parent)
        
        self.uiParent = parent
        
        # make sure we run cleanup after
        from ngSkinTools.ui.events import scriptJobs
        scriptJobs.scriptJob(runOnce=True,uiDeleted=(parent,self.uiDeleted))
        HeadlessDataHost.HANDLE.addReference(self)

        self.actions = MainUiActions(parent)
        

        self.splitPosition = PersistentValueModel(name="ngSkinTools_mainWindow_splitPosition", defaultValue=70)
        def updateSplitPosition(*args):
            size = cmds.paneLayout(horizontalSplit, q=True, paneSize=True)
            # returns (widht, height, width, height)
            self.splitPosition.set(int(size[1]))
        
        horizontalSplit = cmds.paneLayout("horizontalSplit", parent=parent,configuration="horizontal2", width=100, height=300, separatorMovedCommand=updateSplitPosition)
        
        # top half
        topForm = FormLayout(parent=horizontalSplit)
        self.menuBar = cmds.menuBarLayout(parent=topForm.layout)
        self.mainMenu.create(self.actions);

        cmds.paneLayout(horizontalSplit, e=True, staticHeightPane=1)
        cmds.paneLayout(horizontalSplit, e=True, paneSize=(1, 100, self.splitPosition.get()))
        cmds.paneLayout(horizontalSplit, e=True, paneSize=(2, 100, 100 - self.splitPosition.get()))
        
        targetUiLayout = self.targetUI.create(topForm.layout)

        topForm.attachForm(self.menuBar, 0,0,None,0)
        topForm.attachForm(targetUiLayout.layout, None,0,0,0)
        topForm.attachControl(targetUiLayout, self.menuBar, 0, None, None, None)

        # bottom half
        self.mainTabLayout = cmds.tabLayout(parent=horizontalSplit, childResizable=True, scrollable=False, innerMarginWidth=3)

        from ngSkinTools.ui.tabPaint import TabPaint
        from ngSkinTools.ui.tabMirror import TabMirror
        from ngSkinTools.ui.tabSkinRelax import TabSkinRelax
        from ngSkinTools.ui.tabAssignWeights import TabAssignWeights
        from ngSkinTools.ui.tabSettings import TabSettings

        self.tabPaint = self.addTab(TabPaint())
        self.tabMirror = self.addTab(TabMirror())
        self.tabRelax = self.addTab(TabSkinRelax())
        self.tabAssignWeights = self.addTab(TabAssignWeights())
        self.tabSettings = self.addTab(TabSettings())
        
        self.actions.updateEnabledAll()
        log.debug("finished creating main window UI")
        
        
    def uiDeleted(self):
        try:
            MainWindow.currentInstance = None
            log.debug("ngSkinTools UI deleted: "+self.uiParent)
            HeadlessDataHost.HANDLE.removeReference(self)
        except:
            pass
        
    def getLayersUI(self):
        '''
        :rtype: LayerListsUI
        '''
        return self.targetUI.layersUI
        
    def addTab(self, tab):
        '''
        adds tab object to tab UI, creating it's ui and attaching to main window
        '''
        cmds.setParent(self.mainTabLayout)
        tab.parentWindow = self
        layout = tab.createUI(self.mainTabLayout)
        cmds.tabLayout(self.mainTabLayout, edit=True, tabLabel=(layout, tab.getTitle()));
        self.tabs.append(tab)
        
        return tab
    
    def setCurrentTab(self,tabInstance):
        cmds.tabLayout(self.mainTabLayout, edit=True, selectTabIndex=self.tabs.index(tabInstance)+1);
    
    def findTab(self, tabClass):
        for i in self.tabs:
            if isinstance(i, tabClass):
                return i
            
        return None    
