'''
    * <Python API for MG-AssetLibrary>
    * Use these API call to build your asset projects.
    * For detailed help and the sample code, read MGTools manual.    
    * copyright Miguel @param  mgland animation studio. All rights resvered.
'''
import MG_GetFileDateSize
import MG_GetMBFileVersion
import maya.cmds as cmd
import maya.mel as mel

import re
import os
import fnmatch

from MG_ServeUtil import *
MG_RefreshLanguageOption()  #refresh the global var: gMayaVersionInt, gOSLangOption, gMGToolsProTitle

mel.eval("MGAssetLib_initAPI")


def MGAssetLibUtil_isLibraryWindowOpen():
    '''
    * Test if MG-AssetLibrary tool is opened in Maya.
    * Return True if opened, False if not.
    @return: bool
    '''
    return cmd.window(MG_DB_manager, exist = True)

def MGAssetLibUtil_openProjectIfLibraryToolOpen(projFilePath):
    '''
    * If MG-AssetLibrary tool is opened in Maya, then open the project file.
    * This will reopen the project if it is already opened.
    @param projFilePath: <str> represent a MG-AssetLibrary asset project file full path.
    @return: None
    '''
    mel.eval("MGDB_OpenProjectFileIfMainUIExists \""+projFilePath+"\"")

def MGAssetLibUtil_openCategoryIfLibraryToolOpen(projName, categoryName):
    '''
    * if MG-AssetLibrary tool is opened in Maya, and the project is already opened,
    * then this will read the category into the UI.
    * This will also reopen the category if it is already opened.
    @param projName: <str> A existed project name
    @param categoryName: <str> A existed category name in the project projName.
    @return: None
    '''
    mel.eval("MGDB_ReadCategoryFileIfMainUIExists \""+projName+"\" \""+categoryName+"\"") 

def MGAssetLibUtil_warning(warnMessage):
    '''
    * Helper function to issue a warning in Maya.
    @param warnMessage: <str> The message content text. 
    @return: None
    '''
    warnMessage = '[MGTools][MG-AssetLibrary] ' + warnMessage;
    cmd.warning(warnMessage)

def MGAssetLibUtil_getLocalRoot():
    '''
    * Get MG-AssetLibrary local root directory.
    @return: str
    '''
    result = cmd.internalVar(userAppDir = True) + "MGTools_GlobalData/MG_AssetLib/"    
    return result

#make sure the local root dir is there:
if not os.path.isdir(MGAssetLibUtil_getLocalRoot()):
    os.makedirs (MGAssetLibUtil_getLocalRoot())

def MGAssetLibUtil_getLocalProjectDir(projectName):
    '''
    * Get MG-AssetLibrary local project directory via the projectName you've provided.
    @param projectName: <str> The project name.
    @return: str
    '''
    projDir = (MGAssetLibUtil_getLocalRoot() + projectName + "/")   
    return projDir

def MGAssetLibUtil_getLocalProjectFilePath(projectName):
    '''
    * Get MG-AssetLibrary local project file full path via the projectName you've provided.
    * It is a file with a extension : .assetproj
    @param projectName: <str> The project name.
    @return: str
    '''
    filePth = (MGAssetLibUtil_getLocalRoot() + projectName + "/"+projectName + ".assetproj")   
    return filePth

def MGAssetLibUtil_getLocalCategoryFilePath(projectName, categoryName):
    '''
    * Get MG-AssetLibrary local category file full path via the projectName and categoryName you've provided.
    * It is a file with a extension : .asset
    @param projectName: <str> The project name.
    @param categoryName: <str> The category name.
    @return: str
    '''
    filePth = (MGAssetLibUtil_getLocalRoot() + projectName + "/"+categoryName + ".asset")   
    return filePth

def MGAssetLibUtil_validName(name):
    '''
    * Validate the name with the Maya node naming rules:
    * The leading character should be '_' or english letter,
    * while the other characters should be '_' or english letters or numeric letter.
    * The characters not meet the condition will be replaced with '_'.
    * Will return the validated version of name.
    @param name: <str> The name to validate.
    @return: str
    '''
    if not isinstance(name,str):
        return ''
    reObj = re.compile("[a-zA-Z_]+[a-zA-Z0-9_]*")
    if reObj.match(name):
        return name
    result = ''
    for c in name:
        if reObj.match(c):
            result = result + c
        else:
            result = result +'_'
    return result

def MGAssetLibUtil_compareTwoFileDate(file1, file2):
    '''
    * Compare two files with their modification dates.
    * If file1 is newer than file2, return 1
    * if file1 is the same modification date with file2, return 0
    * if file1 is older than file2, return -1
    @file1: <str> A file path
    @file2: <str> A file path
    @return: int
    '''
    file1Exist = os.path.isfile(file1)
    file2Exist = os.path.isfile(file2)
    if not file1Exist:
        if not file2Exist:
            return 0
        else:
            return -1
    file1DateInt = MG_GetFileDateSize.MGgetFileDateInt(file1)
    file2DateInt = MG_GetFileDateSize.MGgetFileDateInt(file2)
    if file1DateInt == file2DateInt:
        return 0
    elif file1DateInt > file2DateInt:
        return 1
    else:
        return -1

def MGAssetLibUtil_searchFilesFromDirectory(searchDir, patternStr, searchDepthLimit, currentSearchDepth):
    '''
    * Search files that matches the patternStr within the directory searchDir.
    * Return a empty list if no matched files found.
    @param searchDir: <str> represents a directory.
    @param patternStr: <str>
                 Note that patternStr should be '*.extension' like. 
                 If not the function will add '*.' at the front of it.
    @param searchDepthLimit: <int> The limit of the search directory depth.
                        the value 0 or less than 0 indicates that the search is unlimited in depth.
    @param currentSearchDepth: <int> Serves as a helper parameter indicate the current
                        searching depth for stopping the recursing purpose,
                        for the call you should always input 1 for this parameter.
    @return: list of str 
    '''
    if currentSearchDepth < 1:
        currentSearchDepth = 1
    if not os.path.isdir(searchDir):
        MGAssetLibUtil_warning(MG_DualLan_forPY("AssetPyAPI.searchDir.err.prefix")+searchDir+MG_DualLan_forPY("AssetPyAPI.searchDir.err.subfix"))
        return []
    if not isinstance(patternStr,str):
        MGAssetLibUtil_warning(MG_DualLan_forPY("MGdbManager.patternPara.notString.error"))
        return []
    if not len(patternStr):
        MGAssetLibUtil_warning(MG_DualLan_forPY("MGdbManager.patternPara.empty.error"))
        return []

    #format the patternstr:
    if patternStr.startswith('.'):
        patternStr = '*' + patternStr
    elif not patternStr.startswith('*.'):
        patternStr = '*.' + patternStr

    #test search depth:    
    if searchDepthLimit > 0:
        if currentSearchDepth > searchDepthLimit:
            return []

    if not searchDir.endswith('/'):
        searchDir = searchDir +'/'
    result = []
    for entry in os.listdir(searchDir):
        fullpath = (searchDir + entry)
        if fnmatch.fnmatch(entry,patternStr):
            result.append(fullpath)
        elif os.path.isdir(fullpath):
            fullpath = fullpath +'/'
            result.extend(MGAssetLibUtil_searchFilesFromDirectory(fullpath,patternStr,searchDepthLimit,(currentSearchDepth+1)))
    return result

def MGAssetLibUtil_searchPreviewImagesFromDirectory(searchDir,imageExtensions,searchDepthLimit):
    '''
    * Search images that matched the any pattern in imageExtensions within the directory searchDir.
    @param searchDir: <str> An existed directory to search in.
    @param imageExtensions: <list / str>
                      Note that each item in imageExtensions should be '*.extension' like. 
                      If not the function will add '*.' at the front of it.
    @param searchDepthLimit: <int> The limit of the search directory depth.
                        the value 0 or less than 0 indicate that search is unlimited in depth.
    @return: list of str                 
    '''
    if isinstance(imageExtensions,str):
        return MGAssetLibUtil_searchFilesFromDirectory(searchDir,imageExtensions,searchDepthLimit,1)
    elif isinstance(imageExtensions,list):
        result = []
        for extension in imageExtensions:
            result.extend(MGAssetLibUtil_searchFilesFromDirectory(searchDir,extension,searchDepthLimit,1))
        return result
    return []


def MGAssetLibUtil_searchMayaFileFromDirectory(searchDir,searchMA,searchMB,searchDepthLimit):
    '''
    * Search maya scene file within the directory searchDir.
    @param searchDir: <str> An existed directory to search in.
    @param searchMA: <bool> Indicate the maya ascii file should be searched.
    @param searchMB: <bool> Indicate the maya binary file should be searched.
                    Note that searchMA and searchMB should not be both False.
    @param searchDepthLimit: <int> Which is the limit of the search directory depth
                        the value 0 or less than 0 indicate that search is unlimited in depth.
    @return: list of str                 
    '''
    result = []
    extensionList = []
    if searchMA:
        extensionList.append('*.ma')
    if searchMB:
        extensionList.append('*.mb')
    if not len(extensionList):
        MGAssetLibUtil_warning(MG_DualLan_forPY("MGdbManager.neither.mbma.war"))
        return []

    for extension in extensionList:
        result.extend(MGAssetLibUtil_searchFilesFromDirectory(searchDir,extension,searchDepthLimit,1))
    return result

#----------------------------------------------------------------------
def MGAssetLibUtil_getBasename(filepath):
    '''
    * Get the basename of a file path or a file name.
    @param filepath: <str> A file full path. 
                     Note that it is a dirname, this function will return empty string. 
    @return: str
    '''
    if not isinstance(filepath,str):
        return ''
    fileName = os.path.basename(filepath)
    temp = fileName.rpartition('.')    
    basename = temp[0] 
    return basename

def MGAssetLibUtil_makeMayaAsciiFile(overrideIfExists,MAFile,referenceFiles,namespaceList=[],deferList=[]):
    '''
    * Generate a maya ascii file based on the info you have input.
    * Return True if the function successed else False.
    @param overrideIfExists: <bool> Decide whether override an existed maya ascii file.
    @param MAFile: <str> The full path of the target maya ascii file.
    @param referenceFiles: <list of strings> The asset full path that will be referenced in the target maya ascii file. 
    @param namespaceList: <list of strings> If namespaceList doesn't provide items as many as referenceFiles does, 
                          this function will use the validated version of the basename of referenceFiles item instead.
    @param deferList: <list of int> If it doesn't provide items as many as referenceFiles does, 0 will be used.
    @return: bool
    '''
    if not isinstance(MAFile,str):
        return False
    if os.path.isfile(MAFile):
        if not overrideIfExists:
            MGAssetLibUtil_warning(MG_DualLan_forPY("MGdbManager.return.maExists.war")+MAFile)
            return False
    if not MAFile.endswith('.ma'):
        MGAssetLibUtil_warning(MG_DualLan_forPY("MGdbManager.onlyMa.war"))
        return False
    MAFile.replace('\\','/')

    if isinstance (referenceFiles, str):
        refFiles = [referenceFiles]
    else: 
        refFiles = list(referenceFiles)

    if isinstance (namespaceList, str):
        nsList = [namespaceList]
    else:
        nsList = list(namespaceList)

    if isinstance (deferList, str):
        defList = [deferList]
    else:
        defList = list(deferList)        

    newLine = "\n"

    fileName = os.path.basename(MAFile)
    basename = MGAssetLibUtil_getBasename(fileName)  

    maContent = ("//Maya ASCII "+ cmd.about(file=True)+" scene"+newLine)
    maContent = (maContent + "//Name: "+basename +newLine)
    maContent = (maContent + "//Last modified: "+cmd.about(currentDate=True)+" "+cmd.about(currentTime=True) +newLine)
    maContent = (maContent + "//Codeset: " + cmd.about(codeset=True) + newLine)   
    secRefConent = ''

    refCount = len(refFiles)
    nsCount = len(nsList)
    defCount = len(defList)
    cNS = ''
    cdefStr = ''
    cBaseName = ''
    cRefPath = ''
    cRefNode = ''
    if refCount:
        for i in range(refCount):
            cRefPath = refFiles[i]
            #now get current namespace:
            if i < nsCount:
                cNS = MGAssetLibUtil_validName(nsList[i])
                if not len(cNS):
                    cNS = MGAssetLibUtil_validName(MGAssetLibUtil_getBasename(cRefPath))
            else:
                cNS = MGAssetLibUtil_validName(MGAssetLibUtil_getBasename(cRefPath))
            #noew get current refnodename:
            cRefNode = (cNS+'RN')
            #now get current defer str    
            if i < defCount:
                if defList[i]:
                    cdefStr = ' -dr 1'
                else:
                    cdefStr = ''
            else:
                cdefStr = ''  

            #now make string:    
            maContent = maContent + ("file -rdi 1 -ns \""+cNS+"\""+cdefStr+" -rfn \""+cRefNode+"\" \""+cRefPath+ "\";"+newLine)
            secRefConent = secRefConent + ("file -r -ns \""+cNS+"\" -dr 1 -rfn \""+cRefNode+"\" \""+cRefPath+"\";"+newLine)               

        maContent = (maContent + secRefConent) 
    maContent = (maContent + "// End of "+fileName+newLine+" ")    
    f = None
    try:
        f = open(MAFile,'w')
        f.write(maContent)
    finally:
        f.close()

    return True
#=========================================================================== 
class MGAssetAPIError (Exception):
    '''
    * Custom Exception for this API
    '''
    def __init__(self,description):
        self._errorMsg = description
    def __str__(self):
        return repr(self._errorMsg)

#=========================================================================== 
class MGAssetRecord():
    '''
    * MG-AssetLibrary asset record object.
    * Use MGAssetCategoryObj.addAssetRecords() method to create a instance of MGAssetRecord.
    '''
    #----------------------------------------------------------------------
    def __init__(self,categoryObject,assetPath, assetName='',assetStateStr='',previewImageStr='',noteStr='',sizeStr='',dateStr='',versionStr = ''):
        '''
        * Init a MGAssetRecord object.
        @param categoryObject: <MGAssetCategory> It should be a valid MGAssetCategory instance.
        @param assetPath: <str> It should be a full path to a maya scene file.
                           This parameter should not be an empty string and should endswith either '*.ma' or '*.mb'
        @param assetName: <str> The namespace of the maya file. 
                         Will use validated version of the basename of assetPath if this parameter is an empty string.
        @param assetStateStr: <str> The state name. No state color string included please, only the state name.
        @param previewImageStr: <str> The preview images. 
                            A string that could contain multiple image file paths, 
                            separate the paths with ';' please.
        @param noteStr: <str> A annotation string for this asset record.
        @param sizeStr: <str> A string represent the file size, in KB unit. eg. 1,150KB
                        If this parameter or the dateStr parameter is an empty string, will test and fill in the actually size of the assetPath.
        @param dateStr: <str> A string represent the file modification date, in format 'DD/MM/YYYY hh:mm:ss'. eg. 4/10/2014 21:55:4
                        If this parameter or the sizeStr parameter is an empty string, will test and fill in the actually date of the assetPath.
        @param versionStr: <str> The version string of the maya scene file. eg.2015
                        If this parameter is an empty string, will test and fill in the actually version of the assetPath.
        '''
        self._path = ''
        self._valid = False
        if not categoryObject.isValid():
            return
        self._categoryObject = categoryObject
        self._path = assetPath.strip().replace('\\','/')        
        if not len(self._path):
            return         
        if not self._path.endswith('.ma') and not self._path.endswith('.mb'):
            return
        self._ns = MGAssetLibUtil_validName(assetName.strip())
        if not len(self._ns):
            self._ns = MGAssetLibUtil_validName(MGAssetLibUtil_getBasename(self._path))
        if not len(self._ns):
            #the assetpath passed in is probably a directory but not a maya file.
            self._valid = False
            return
        self._valid = True              
        self._state = assetStateStr.strip()
        self._imageStr = previewImageStr
        self._note = noteStr.strip()
        self._size = sizeStr.strip()
        self._date = dateStr.strip()
        self._version = versionStr.strip()
        if os.path.isfile(self._path):
            if not len(self._size) or not len(self._date):            
                sizeDate = (MG_GetFileDateSize.MGgetFileDateSize(self._path)).split(';')
                self._size = sizeDate[0]
                self._date = sizeDate[1]
            if not len(self._version):
                if self._path.endswith('.ma'):
                    self._version = MG_GetMBFileVersion.MGreadMAVersionInfo(self._path)
                elif self._path.endswith('.mb'):
                    self._version = MG_GetMBFileVersion.MGreadMBVersionInfo(self._path)
    #----------------------------------------------------------------------
    def isValid(self):
        '''
        * Test if this MGAssetRecord instance is valid.
        @return: bool
        '''
        return self._valid
    #----------------------------------------------------------------------    
    def getAssetPath(self):
        '''
        * Get the maya scene file full path from this instance.
        * Will return an empty string if this instance is invalid.
        @return: str
        '''
        if not self.isValid():
            return  ""
        return self._path
    #----------------------------------------------------------------------
    def getDataString(self):
        '''
        * Get the data string of this instance.
        * Will return an empty string if this instance is invalid.
        * The result will also be used in print(instance)
        @return: str
        '''
        if not self.isValid():
            return  ""        
        return (self._ns+"{"+self._path+
                "{"+self._size+"{"+self._date+"{"+self._version+"{"+self._imageStr+"{"+self._state+"{"+self._note+"}\n")
    #----------------------------------------------------------------------        
    def __str__(self):
        '''
        * The method used to print this instance.
        '''
        return self.getDataString()


#===========================================================================   
class MGAssetCategory():
    '''
    * MG-AssetLibrary category object.
    * Use MGAssetProj.addCategory() method to create an instance of MGAssetCategory.
    * Or you can call MGAssetCategory(projectObject) to create an invalid instance, and then call initFromCategoryFile(categoryFile) to init it.
    '''
    #----------------------------------------------------------------------
    def __init__(self, projectObject, categoryName = ''):
        '''
        * Init the MGAssetCategory object.
        @param projectObject: <MGAssetProj> Should be an valid MGAssetProj instance.
        @param categoryName: <str> The category name, will validate it and use the validated version.
                            If this parameter is an empty string, you should call initFromCategoryFile(categoryFile) to init it,
                            or else this instance will be invalid.
        '''
        self._valid = False
        if not isinstance(projectObject,MGAssetProj):
            raise MGAssetAPIError('MGAssetCategory(): '+MG_DualLan_forPY("MGdbManager.invalidProjObj.war"))

        self._projectObject = projectObject
        self._name = MGAssetLibUtil_validName(categoryName)

        if self.doesCategoryFileExist():
            self.initFromCategoryFile(self.getCategoryFilePath())
            return

        self._assetDatas = []        
        if not len(self._name):
            self._valid = False
        else:
            self._valid = True
    #----------------------------------------------------------------------
    def initFromCategoryFile(self,categoryFile):  
        '''
        * Init the MGAssetCategory object with an existed category file (*.asset).
        * If the instance is successfully initialized, return True, else False.
        @param categoryFile: <str> Should be an existed '*.asset' file full path.
        @return: bool
        '''  
        if not os.path.isfile(categoryFile):
            self._valid = False
            return False
        self._name = MGAssetLibUtil_getBasename(categoryFile)
        self._assetDatas = []
        f = None
        try:
            f = open(categoryFile,'r')
            nextLine = f.readline()            
            cDatas = []
            while len(nextLine):                
                cDatas = nextLine.split('{')
                if len(cDatas) < 8:
                    continue
                cNS = cDatas[0]
                cPath = cDatas[1]
                cSize = cDatas[2]
                cDate = cDatas[3]
                cVer =  cDatas[4]
                cImg = cDatas[5]
                cState = cDatas[6]
                cNote = cDatas[7]
                assetRecord = MGAssetRecord(self,cPath,cNS,cState,cImg,cNote,cSize,cDate,cVer)
                if not assetRecord.isValid():              
                    nextLine = f.readline()
                    continue
                self._assetDatas.append(assetRecord)                
                nextLine = f.readline()
            self._valid = True
        finally:
            f.close
    #----------------------------------------------------------------------
    def getName(self):
        '''
        * Get the category name.
        @return: str
        '''  
        return self._name
    #----------------------------------------------------------------------
    def isValid(self):
        '''
        * Test if this MGAssetCategory instance is valid.
        @return: bool
        '''
        return self._valid
    #----------------------------------------------------------------------
    def getCategoryFilePath(self):
        '''
        * Get the category file full path. (path to a '*.asset' file)
        @return: str
        '''  
        return MGAssetLibUtil_getLocalCategoryFilePath(self._projectObject.getName(),self.getName())
    #----------------------------------------------------------------------
    def doesCategoryFileExist(self):
        '''
        * Test the category file actually exists.
        @return: bool
        '''   
        return os.path.isfile(self.getCategoryFilePath())
    #----------------------------------------------------------------------
    def clearAssetRecords(self):
        '''
        * Clear all asset records in this cateogry.
        * Return False if the category instance is invalid, True else.
        @return: bool
        '''   
        if not self.isValid():
            return False
        self._assetDatas = []
        return True
    #----------------------------------------------------------------------
    def doesAssetRecordExist(self, mayaFilePath):
        '''
        * Test if the record already exist in the category via the asset path.
        @param mayaFilePath: <str> A maya scene file full path. 
        @return: bool
        '''   
        if not len(mayaFilePath):
            return False
        for record in self._assetDatas:
            if record.getAssetPath() == mayaFilePath:
                return True            
        return False
    #----------------------------------------------------------------------
    def addAssetRecords(self, mayaFiles,namespaces=[],states=[],previewImages=[],notes=[], sizeDatas = [], dateDatas = [], versionDatas = []):
        '''
        * Create a MGAssetRecord instance and add it to the category if not existed.
        * If Failed, will return a empty list, else a list of MGAssetRecord instances.
        @param mayaFiles: <str / list of str> The Maya scene full paths.
        @param namespaces: <str / list of str> The namespaces. Will use the validated version of the basename of mayaFiles if it is vacant.        
        @param states: <str / list of str> Each item should just be state name, don't append the color info.  
        @param previewImages: <str / list of str> Each item should be paths of image files, connected with character ';'      
        @param notes: <str / list of str> Each item is a annotation for the asset item.  
        @param sizeDatas: <str / list of str> Each item is a size string for the asset item, in format of such as 1,560KB.
                          If vacant will test and use the actually file size string.         
        @param dateDatas: <str / list of str> Each item is a modification date string for the asset item, 
                          in format 'DD/MM/YYYY hh:mm:ss'. eg. 4/10/2014 21:55:4
                          If vacant then will test and use the actually file modification date string.
        @param versionDatas: <str / list of str> Each item is a maya version string of the asset item, 
                          If vacant then will test and use the actually file version string.
        @return: list of MGAssetRecord
        '''   
        if not self.isValid():
            return []
        mayaFileSize = 0
        mayaFileList = []
        if isinstance (mayaFiles,str):
            mayaFileSize = 1
            mayaFileList.append (mayaFiles)            
        else:  
            mayaFileSize = len(mayaFiles)
            mayaFileList = mayaFiles
        if not mayaFileSize:
            return []

        nsList = []
        nsSize = 0
        if isinstance (namespaces,str):
            nsSize = 1
            nsList.append (namespaces)            
        else:  
            nsSize = len(namespaces)
            nsList = namespaces
        stateList = []
        stateSize = 0
        if isinstance (states,str):
            stateSize = 1
            stateList.append (states)            
        else:  
            stateSize = len(states)
            stateList = states
        imgList = []
        imgSize = 0
        if isinstance (previewImages,str):
            imgSize = 1
            imgList.append (previewImages)            
        else:  
            imgSize = len(previewImages)
            imgList = previewImages
        noteList = []
        noteSize = 0
        if isinstance (notes,str):
            noteSize = 1
            noteList.append (notes)            
        else:  
            noteSize = len(notes)
            noteList = notes
        sizeList = []
        sizeSize = 0
        if isinstance (sizeDatas,str):
            sizeSize = 1
            sizeList.append (sizeDatas)            
        else:  
            sizeSize = len(sizeDatas)
            sizeList = sizeDatas
        dateList = []
        dateSize = 0
        if isinstance (dateDatas,str):
            dateSize = 1
            dateList.append (dateDatas)            
        else:  
            dateSize = len(dateDatas)
            dateList = dateDatas
        verList = []
        verSize = 0
        if isinstance (versionDatas,str):
            verSize = 1
            verList.append (versionDatas)            
        else:  
            verSize = len(versionDatas)
            verList = versionDatas

        result = []
        for i in range(mayaFileSize):
            cPath = mayaFileList[i].strip()
            cNS = ''
            cState = ''
            cImg = ''
            cNote = ''
            cSize = ''
            cDate = ''
            cVer = ''
            if not len(cPath):
                continue
            if self.doesAssetRecordExist(cPath):
                continue
            if i < nsSize:
                cNs = nsList[i]
            if i < stateSize:
                cState = stateList[i]
            if i < imgSize:
                cImg = imgList[i]
            if i < noteSize:
                cNote = noteList[i]
                cNote = cNote.replace('{','\\*?[')
                cNote = cNote.replace('}','\\*?]')
                cNote = cNote.replace('\n','\\*?m')
            if i < sizeSize:
                cSize = sizeList[i]
            if i < dateSize:
                cDate = dateList[i]
            if i < verSize:
                cVer = verList[i]
            assetRecord = MGAssetRecord(self,cPath,cNS,cState,cImg,cNote,cSize,cDate,cVer)
            if not assetRecord.isValid():
                continue
            self._assetDatas.append(assetRecord)
            result.append(assetRecord)
        return result
    #----------------------------------------------------------------------
    def deleteAssetRecords(self,mayaFiles):
        '''
        * Delete the records already exist in the category via the asset path list.
        * Return the actually deleted record count.
        @param mayaFiles: <str / list of str> Maya scene full paths.
        @return: int
        '''   
        if not self.isValid():
            return 0
        index = []
        assetSize = len(self._assetDatas)
        if not assetSize:
            return 0
        usedList = []
        if isinstance (mayaFiles, str):
            usedList.append (mayaFiles)
        else: 
            usedList = list(mayaFiles)
        for i in range(assetSize):
            if usedList.count(self._assetDatas[i].getAssetPath()):
                index.append(i)
        if not len(index):
            return 0
        index.reverse()
        count = 0
        for each in index:
            del self._assetDatas[each]
            count = count + 1

        return count
    #----------------------------------------------------------------------
    def getDataString(self):
        '''
        * Get the data string of this category.
        * It is the content when the category is written to disk.
        * It is also the content get printed when you call print(categoryObject)
        @return: str
        '''   
        cateContent = ''
        for record in self._assetDatas:
            if not record.isValid():
                continue
            cateContent = cateContent + record.getDataString()  
        return cateContent 
    #----------------------------------------------------------------------
    def writeToDisk(self):
        '''
        * Write the category into disk with a file ends with *.asset.
        * Return True if success.
        @return: bool
        '''   
        if not self.isValid():
            return False
        cateContent = self.getDataString()

        cateFile = self.getCategoryFilePath()
        f = None
        try:
            f = open(cateFile,'w')
            f.write(cateContent)
        finally:
            f.close()

        MGAssetLibUtil_openCategoryIfLibraryToolOpen(self._projectObject.getName(), self.getName())  
        return True    
    #----------------------------------------------------------------------        
    def __str__(self):
        '''
        * The method used to print this instance.
        '''
        return self.getDataString()    

#===========================================================================        
class MGAssetProj():
    '''
    * A MG-AssetLibrary project object.
    * When constructing the project object, if the projectName you passed in already exist in your local library root dir,
    * then it will skip all the other parameters you passed in , init the object from the existed asset project file.
    '''
    def __init__(self, projectName='', projectAnnotation='',globalPath='',statePresets=[]):     
        '''
        * Init the MGAssetProj object.
        @param projectName: <str> A validated version of this parameter will be actually used.
                          If this parameter is an empty string, you should call initFromProjectFile() to make the instance valid.
        @param projectAnnotation: <str> A project annotation string.
        @param globalPath: <str> A path that specify the global root of the project.
        @param statePresets: <list of str> A list of string, each string is of format: "statename stateColorFloatR stateColorFloatG stateColorFloatB"  
                             eg. "approved 0.2 0.8 0.2"

        '''
        self._projName = MGAssetLibUtil_validName(projectName)
        self._projName = self._projName.strip()
        self._valid = False
        self._lassError = ''
        self.__invalidError =  MG_DualLan_forPY("MGdbManager.invalidProj.war")
        self._categoryList = []
        if not len(self._projName):
            self._valid = False
            self._lassError = MG_DualLan_forPY("MGdbManager.invalidProjName.empty.war")
            #raise MGAssetAPIError('The project name to init MGAssetProj object should not be empty.')
            return

        if self.doesProjectExist():
            cmd.warning(MG_DualLan_forPY("MGdbManager.initViaExistProj.lbl"))
            self.initFromProjectFile(getProjectFilePath())
        else:
            self._projectAnn = projectAnnotation
            self._globalPath = globalPath.replace('\\','/')
            self._statePresets = statePresets
            self._valid = True
        self.initExistCategories()
    #----------------------------------------------------------------------
    def initExistCategories(self):
        '''
        * Read the project local directory, create MGAssetCategory object via the existed category files.
        * Return the initialized category count.
        @return: int
        '''
        projectDir = self.getProjectDir()
        if not os.path.isdir(projectDir):
            return 0
        count = 0
        for entry in os.listdir(projectDir):
            fullpath = (projectDir + entry)
            if fnmatch.fnmatch(entry,'*.asset'):
                cate = MGAssetCategory(self)
                cate.initFromCategoryFile(fullpath)  
                self._categoryList.append(cate)
                count = count + 1
        return count
    #----------------------------------------------------------------------
    def initFromProjectFile(self,projectFilePath):
        '''
        * Init the MGAssetProj object with a existed project file (*.assetproj).
        * Return True if succeed else False.
        @param projectFilePath: <str> A full path to a asset project file.
        @return: bool      
        '''
        if not os.path.isfile(projectFilePath):
            self._valid = False
            return False
        f = None
        try:
            f = open(projectFilePath,'r') 
            globalDir = f.readline().split('=')

            if len(globalDir) <= 1:
                self._globalPath = ''
            else:
                self._globalPath = globalDir[1].strip()

            stateData = f.readline().split('=')
            if len(stateData) <= 1:
                self._statePresets = []
            else:
                stateStr = globalDir[1].strip()        
                if not len(stateStr):
                    self._statePresets = []
                self._statePresets = stateStr.split(',')
            self._projectAnn = ''
            nextLine = f.readline()
            while len(nextLine):
                self._projectAnn = (self._projectAnn + nextLine)
                nextLine = f.readline()
        finally:
            f.close()

        self._valid = True
    #----------------------------------------------------------------------
    def isValid(self):
        '''
        * Test if this MGAssetProj instance is valid.
        @return: bool
        '''
        return self._valid
    #----------------------------------------------------------------------    
    def doesProjectExist(self):
        '''
        * Test if this project file already exists.
        @return: bool
        '''
        if not self._valid:
            return False
        return os.path.isfile(self.getProjectFilePath())
    #----------------------------------------------------------------------
    def getName(self):
        '''
        * Get the project name.
        @return: str
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return ""
        return self._projName 
    #----------------------------------------------------------------------    
    def getProjectDir(self):
        '''
        * Get the project local directory path.
        @return: str
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return ""
        return MGAssetLibUtil_getLocalProjectDir(self._projName)    
    #----------------------------------------------------------------------    
    def getProjectFilePath(self):
        '''
        * Get the project local directory file full path (*.assetproj).
        @return: str
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return ""
        return MGAssetLibUtil_getLocalProjectFilePath(self._projName)
    #----------------------------------------------------------------------
    def addStates(self,newStatePresets):
        '''
        * Add state presets to project.
        * Return True if succeed else False.
        @param newStatePresets: <str / list of str>
                             A list of string, each string is of format: "statename stateColorFloatR stateColorFloatG stateColorFloatB"
                             eg. "approved 0.2 0.8 0.2"
        @return: bool 
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return False
        if isinstance (newStatePresets, str):
            newStatePresets = [newStatePresets]

        if not len(newStatePresets):
            self._lassError = ('addStates(): '+MG_DualLan_forPY("MGdbManager.newStatePresets.parameterEmpty.war"))
            return False
        stateNames = []
        oldLen = len(self._statePresets)
        for oldState in self._statePresets:
            temp = oldState.split(' ')
            if len(temp):
                stateNames.append(temp[0])
        for newState in newStatePresets:
            temp = newState.split(' ')
            exist = False
            for i in range(oldLen):
                if stateNames[i] == temp[0]:
                    self._statePresets[i] = newState
                    exist = True
                    break
            if not exist:
                self._statePresets.append(newState) 
        return True
    #----------------------------------------------------------------------
    def getStates(self):
        '''
        * Get the project's state list.
        @return: list 
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return []
        return self._statePresets
    #----------------------------------------------------------------------
    def addCategory(self, categoryName):
        '''
        * Add a category called categoryName into the project.
        * Return the new created MGAssetCategory instance on success, or None if failed.
        @param categoryName: <str> The category name. Should not be an empty string.
        @return: None / MGAssetCategory 
        '''
        if not self._valid:
            self._lassError = self.__invalidError
            return None
        cateName = MGAssetLibUtil_validName(categoryName.strip())
        if not len(cateName):
            self._lassError = ('addCategory(): '+MG_DualLan_forPY("MGdbManager.categoryName.parameterEmpty.war"))
            return None
        for oldCate in self._categoryList:
            if oldCate.getName() == cateName:
                self._lassError = 'addCategory(): '+MG_DualLan_forPY("MGdbManager.cateAdded.war")
                return None
        newCate = MGAssetCategory(self,cateName)
        self._categoryList.append(newCate)
        return newCate
    #----------------------------------------------------------------------
    def getCategoryObjects(self):
        '''
        * Get all the MGAssetCategory objects in the project.
        * Return a list of MGAssetCategory on success, or an empty list if failed.
        @return: list of MGAssetCategory
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return []
        return self._categoryList
    #----------------------------------------------------------------------
    def getCategoryNames(self):
        '''
        * Get all the category names in the project.
        * Return a list of category names on success, or an empty list if failed.
        @return: list of str
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return []
        result = []
        for cate in self._categoryList:
            result.append(cate.getName())
        return result
    #----------------------------------------------------------------------
    def _getProjectDataString(self):
        '''
        * Get the project data string, the string will be written when you invoke writeProjectToDisk() method. 
        * Also the data string will be used in the call: print(projObject)
        @return: str
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return ""
        newLine = '\n'
        content = ("Global_Project_Root = "+self._globalPath+newLine)
        content = content + ("State = " + ','.join(self._statePresets)+newLine)
        content = content + ("[Description]" + newLine + self._projectAnn)
        return content
    #----------------------------------------------------------------------
    def writeProjectToDisk(self):
        '''
        * Write the project object to MG-AssetLibrary local root directory.
        * The file will be '*.assetproj'.
        * It will override even if the old project exists.
        * Will open the project in MG-AssetLibrary UI if the UI is opened.
        * Return Ture if succeed.
        * Will raise an exception if this project object is invalid.
        @return: bool
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            raise MGAssetAPIError(self.__invalidError)
        projectContent = self._getProjectDataString()

        projFilePath = self.getProjectFilePath()
        projDir = os.path.dirname(projFilePath)
        if not os.path.isdir(projDir):
            os.makedirs(projDir)
        f = None
        try:
            f = open(projFilePath,'w')
            f.write(projectContent)
        finally:
            f.close()

        self.openProjectInMGAssetLibrary()    
        return True
    #----------------------------------------------------------------------
    def getCategoryObjectByName(self,categoryName):
        '''
        * Get the MGAssetCategory object that has the name: categoryName. 
        * Return MGAssetCategory instance if found, else return None.
        @param categoryName: <str> The category name.
        @return: MGAssetCategory / None
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return None
        cateName = MGAssetLibUtil_validName(categoryName.strip())
        if not len(cateName):
            self._lassError = 'getCategoryObjectByName(): '+MG_DualLan_forPY("MGdbManager.categoryName.parameterEmpty.war")
            return None
        for oldCate in self._categoryList:
            if oldCate.getName() == cateName:
                return oldCate
        return None
    #----------------------------------------------------------------------
    def writeCategoryToDisk(self,categoryObject):
        '''
        * Write the category object to disk (*.asset).
        * It will override even if the old category exists.
        * Will open the category in MG-AssetLibrary UI if the UI is there and the project is also opened.
        * Return Ture if succeed.
        * Will raise an exception if this project object is invalid.
        @param categoryObject: <MGAssetCategory> Should be an valid MGAssetCategory instance.
        @return: bool                  
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            raise MGAssetAPIError(self.__invalidError)
        if not categoryObject.isValid():
            self._lassError = 'writeCategoryToDisk(): '+MG_DualLan_forPY("MGdbManager.invalidCateObj.war")
            return False
        projName = self.getName()
        categoryName = categoryObject.getName()
        categoryObject.writeToDisk()        
        return True
    #----------------------------------------------------------------------
    def writeAllCategoriesToDisk(self):
        '''
        * Write all the category objects to disk (*.asset).
        * It will override even if the old categories exists.
        * Will open each category one by one in MG-AssetLibrary UI if the UI is there and the project is also opened.
        * Return Ture if succeed.
        * Will raise an exception if this project object is invalid.
        @return: bool                  
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            raise MGAssetAPIError(self.__invalidError)        
        cateObjs = self.getCategoryObjects()
        if not len(cateObjs):
            self._lassError = 'writeAllCategoriesToDisk(): '+MG_DualLan_forPY("MGdbManager.noCateToWrite.war")
            return False
        result = True
        for cate in cateObjs:
            if not cate.isValid():
                self._lassError = 'writeAllCategoriesToDisk(): '+MG_DualLan_forPY("MGdbManager.invalidCateObj.war1")
                result = False        
                continue
            currentResult = self.writeCategoryToDisk(cate) 
            if not currentResult:
                result = False                
        return result
    #----------------------------------------------------------------------
    def openProjectInMGAssetLibrary(self):
        '''
        * Open this project in MG-AssetLibrary tool if the tool is opened.
        @return: bool
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return False
        projFilePath = self.getProjectFilePath()
        MGAssetLibUtil_openProjectIfLibraryToolOpen(projFilePath)
        return True
    #----------------------------------------------------------------------
    def openCategoryInMGAssetLibrary(self, categoryName):
        '''
        * Open the category in MG-AssetLibrary tool if the tool is there and the project is also opened.
        @param categoryName: <MGAssetCategory / str> This parameter could be a MGAssetCategory instance or a category name string.
        @return: bool
        '''
        if not self.isValid():
            self._lassError = self.__invalidError
            return False
        projName = self.getName()
        catename = ''
        if isinstance(categoryName, MGAssetCategory):
            catename = categoryName.getName()
        elif isinstance(categoryName,str):
            catename = MGAssetLibUtil_validName(categoryName.strip())
        else:
            raise MGAssetAPIError(MG_DualLan_forPY("MGdbManager.param.categoryName.invalid.war"))

        MGAssetLibUtil_openCategoryIfLibraryToolOpen(projName, catename)
        return True
    #----------------------------------------------------------------------
    def __str__(self):
        '''
        * The method used to print this instance.
        '''
        report = (MG_DualLan_forPY("MGdbManager.proj.prefix") + self.getName() + '\n')
        categoryNameList = []
        for cate in self._categoryList:
            cCategoryName = cate.getName()
            if not len(cCategoryName):
                cCategoryName = '<inValid>'
            categoryNameList.append(cCategoryName)
        cateStr = 'N/A'
        if len(categoryNameList):
            cateStr = '  '.join(categoryNameList)
        report = report + MG_DualLan_forPY("MGdbManager.cate.prefix") + cateStr +'\n'
        stateStr = ', '.join(self._statePresets)
        if not len(stateStr):
            stateStr = 'N/A'
        report = report + MG_DualLan_forPY("MGdbManager.state.prefix")+ stateStr + '\n'
        report = report + MG_DualLan_forPY("MGdbManager.ann.prefix")+ self._projectAnn
        return report
    #----------------------------------------------------------------------  
    def getLastError(self):
        '''
        * Get the last error string.
        * Return an empty string if no error happened. 
        @return: str
        '''
        return self._lassError
          
    
#end of file
